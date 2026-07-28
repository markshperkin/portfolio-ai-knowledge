# Agentic Investment Firm — Guardrails and the Risk Engine

## Summary

Eight guardrails, applied on every path, defense in depth. The organizing principle: **safety is code, not persuasion.** An LLM can be prompt-injected or simply wrong, so it must never be the thing that enforces a money limit. Limits live in deterministic modules an agent cannot reach, argue with, or bypass.

## The Full Stack

| Guardrail | Where | Effect |
|---|---|---|
| **Lookahead assertion** | `guardrails/lookahead.py` | Hard boundary — no document or price dated after `as_of` enters context. Raises and aborts. |
| **Injection quarantine** | `rag/retriever.py` → `guardrails/injection.py` | Retrieved chunks scanned; prompt-injection content quarantined before reaching an agent. |
| **Corrective-RAG refusal** | `rag/crag.py` | Bad retrieval retries ≤ 2, then honest `INSUFFICIENT_EVIDENCE`. Never fabricates a thesis. |
| **Citation verification** | `guardrails/citations.py` | Uncited claims and unsupported numbers stripped; ungrounded stance collapses to a refusal. |
| **Exit-bound clamp** | `agents/pm.py` | LLM-proposed stop/target forced inside firm caps. |
| **Risk gate + HITL** | `guardrails/risk_engine.py` + `firm/hitl.py` | Buys at or above the notional threshold pause for the human Risk Committee; sells auto-approve. |
| **Budget circuit-breaker** | `guardrails/budget.py` | Per-run caps on LLM calls, tokens, and wall-clock. Breach halts the run. |
| **Partial-failure isolation** | `firm/runner.py` | One ticker's error degrades to an error span; the run continues. |

Plus the broker itself: slippage and commission, market-hours checks, no-oversell, idempotency, single-transaction fills.

## The Risk Engine

The risk engine is the **only** gate to the book, and it's about forty lines of pure function with no LLM anywhere near it:

```python
if side == "SELL":
    return AUTO_APPROVE          # risk-reducing; the broker still refuses an oversell
if notional >= approval_notional_threshold:
    return REQUIRE_HUMAN         # pauses the run
return AUTO_APPROVE
```

Configurable hard limits sit alongside it: max position % of equity, max single-order notional, max daily loss, max trades per day, no over-shorting, market-hours-only. All in `config.py`, all overridable by environment.

### Why there's no policy REJECT

This is the design call I'd most want to be asked about. The engine never rejects a trade on a rule for being *impossible* — insufficient cash, selling more shares than you hold. Those are refused **physically by the broker at fill time**.

The reasoning: a rule that says "don't spend more cash than you have" is a restatement of reality that can be misconfigured, forgotten, or fall out of sync with the actual ledger. The broker refusing to produce a fill it cannot fund is not a rule at all — it's the shape of the system. Making impossibility physical rather than policy means there's no configuration under which it stops working.

Policy limits (notional thresholds, position caps) are genuinely policy and belong in config. Physical impossibility belongs in the broker.

### Re-check before fill

The engine re-evaluates immediately before the fill, not just at proposal time. During a human-approval pause the book can change — another path may have executed, cash may have moved. Approving a trade that was legal twenty minutes ago doesn't make it legal now. That pre-fill re-check closes the HITL-wait race.

## Deterministic Sizing

```python
target_notional = min(equity * max_position_pct * confidence, cash)
quantity = max(int(target_notional // price), 0)
```

Confidence-scaled fraction of equity, clamped by available cash. The LLM never picks the size — it only supplies the confidence that scales it, and confidence is itself bounded 0–1 by the schema.

The sizer deliberately does **not** try to stay under the human-approval threshold. If the math produces a big order, it produces a big order, and escalating it is the risk engine's job. Two components, two responsibilities; a sizer that quietly shrinks orders to dodge the approval gate would be the worst kind of bug.

## Bound Clamping

The PM proposes a stop and a target sized to its conviction. Code then forces them inside firm caps: floor `min_bound_pct` (0.5%), ceilings `max_stop_loss_pct` (4%) and `max_take_profit_pct` (10%).

The phrasing I kept coming back to: **the LLM proposes, code enforces.** The model gets real influence — a high-conviction position can carry a tighter stop than a marginal one — but it cannot set a 40% stop because it convinced itself the thesis was strong, and it cannot be talked into one by injected text.

## Budget Circuit-Breaker

Per-run caps on LLM calls (200), tokens (500k), and wall-clock seconds (600). A breach raises `BudgetExceeded` and **halts the whole run** — this is explicitly not isolated per ticker, because a runaway loop is a systemic failure, not a local one.

One detail I'm pleased with: `credit_wait()`. Time spent blocked on a human approval is credited back to the wall-clock budget. Waiting for a person is not runaway compute, and without that credit any run with a real human in it would trip the timer and die. It's a small function that only exists because I actually ran the human-in-the-loop flow end to end.

I'm also honest in the runbook that the budget numbers are first-pass guesses. The right way to set them is to measure a normal live run and derive real caps; that's tracked as a follow-up rather than dressed up as tuned.

## Partial-Failure Isolation

One ticker's pipeline error becomes an error span and the run continues for the others. The exceptions that halt everything: budget breaches and approval timeouts.

That split is intentional. A single ticker failing is a local problem — you still want the rest of the day's decisions and the report. A budget breach or a stalled human gate means the run's assumptions are broken, and continuing produces a report that lies about what happened.

## What This Buys

The property I'd defend: **an agent in this system cannot exceed a trading limit even if it tries.** Not because the prompt tells it not to, but because the code path from "the model said something" to "money moved" goes through a sizer it doesn't control, a clamp it can't widen, a gate it can't open, and a broker that refuses impossible fills. A successful prompt injection gets you a bad thesis, not a bad trade.

## Keywords

guardrails, defense in depth, risk engine, deterministic enforcement, hard limits, position sizing, bound clamping, stop loss, take profit, circuit breaker, budget limits, token limits, rate limiting, prompt injection defense, lookahead prevention, citation verification, partial failure isolation, fail-safe design, human-in-the-loop, HITL, approval threshold, idempotency, paper broker, oversell prevention, safety by construction, LLM safety, AI safety engineering
