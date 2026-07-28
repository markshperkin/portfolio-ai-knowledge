# Agentic Investment Firm — Architecture

## Summary

The system replays one historical US trading day, sliced into ticks (hourly by default). On each tick a **deterministic dispatcher** picks exactly one path per ticker, first-match-wins. LLM agents run only at the leaves; every money-touching step is deterministic code; every step emits a span. Orchestration is explicit code with state in SQLite — not a graph framework.

## The Core Split

This is the single most important design decision in the project:

- **LLM agents make judgments** — what evidence is relevant, what the thesis is, buy/sell/hold, and where exit bounds should sit.
- **Deterministic code makes decisions that touch money or truth** — retrieval routing, position sizing, bound clamping, stop/target enforcement, and execution.

Everything else in the architecture follows from holding that line.

## Component Layers

```
API / UI          POST /run · report[.xlsx] · HITL approve/edit/reject · SSE event feed
     ↓
Orchestration     runner (day loop) · clock (ticks) · dispatcher (first-match-wins)
(firm/)           pipeline (research → execution) · monitor (stop/target + day review)
                  hitl (approval gate) · memory (per-ticker belief timeline)
     ↓
LLM agents        query_gen · relevance_critic · research · pm · risk · day_review · reporting
(agents/)
     ↓
RAG (rag/)        crag loop · retriever (+injection scan) · vector_store / embeddings
     ↓
Deterministic     risk_engine · sizing · clamp_bounds · paper broker · portfolio/positions
core
     ↓
Guardrails        budget circuit-breaker · citation verifier · lookahead assertion
(cross-cutting)
```

## The Daily Loop

`runner._run_ticks` walks each tick, gathers three signals — max absolute price move, whether new documents landed, whether any stop/target triggered — and asks the dispatcher for the path.

The dispatcher is about twenty lines of pure function. Same inputs, same path, every run:

```python
if tick_index == 0:              return "CONTEXT_BUILD"   # market open
if tick_index == n_ticks - 1:    return "DAY_REVIEW"      # pre-close
if has_new_docs:                 return "INCREMENTAL_NEWS"
if has_stop_trigger:             return "MONITOR_SELL"
if max_abs_move >= threshold:    return "PRICE_REEVAL"
return "SKIP"
```

Priority ordering matters and I made each choice deliberately:

- The **last tick is always `DAY_REVIEW`**, even if a filing also landed. Closing the day cleanly outranks reacting to late news.
- A **protective stop fires before a discretionary price re-eval**. A hard exit must trigger on the move that breached it, not get shadowed by a re-decision path that might do nothing.

## The Six Dispatch Paths

| Path | Trigger | Research? | LLM? | What happens |
|---|---|---|---|---|
| `CONTEXT_BUILD` | tick 0 (open) | full corrective RAG | yes | build the opening thesis → maybe trade |
| `INCREMENTAL_NEWS` | new filing since last tick | new docs only, skips retrieval | yes | revise thesis vs prior view → maybe trade |
| `PRICE_REEVAL` | absolute move ≥ 2% | reuse cached view | PM only | re-decide against the new price |
| `MONITOR_SELL` | price crosses a stop/target | none | **no** | deterministic protective sell |
| `DAY_REVIEW` | last tick | delta evidence only | yes | HOLD / TRIM / FLATTEN vs overnight gap risk |
| `SKIP` | no signal | none | no | no-op |

`CONTEXT_BUILD` and `DAY_REVIEW` fan out to all tickers. The other three only touch the affected ticker.

The cost story is baked into that table. Only the open and the incremental-news paths run fresh research. A material price move with no new evidence doesn't need a new thesis — it needs the PM to re-decide against the new price, so that's all it does. A stop trigger doesn't need an LLM at all.

## The Shared Sub-Flow: PM → Bounds → Risk → Execution

`CONTEXT_BUILD`, `INCREMENTAL_NEWS`, and `PRICE_REEVAL` all converge here. It's where exit bounds are born and where the human gate lives.

1. **Actionable?** Stance must be bullish or bearish *and* confidence ≥ 0.6. Otherwise: no trade, recorded to memory.
2. **PM decides** BUY / SELL / HOLD, and proposes `stop_loss_pct` and `take_profit_pct` sized to its conviction.
3. **Clamp bounds** — the proposed stop is forced into 0.5%–4%, the target into 0.5%–10%. Regardless of what the model emitted.
4. **Position sizer** — deterministic: `min(equity × max_position_pct × confidence, cash) // price`. The PM never picks the quantity.
5. **Risk engine evaluates** — SELL auto-approves; BUY under $25k auto-approves; BUY at or above $25k requires the human Risk Committee and **pauses the run**.
6. **Broker executes** — with slippage and commission, market-hours checks, no-oversell, idempotency, single-transaction fills.
7. **On a BUY fill**, the clamped bounds are stamped onto the position.

Two details I'd call out:

- The **risk engine has no policy REJECT**. Impossible fills — insufficient cash, selling more than you hold — are refused *physically* by the broker, not by a rule that could be misconfigured. Rules can drift; physics can't.
- The human-approval path **persists the bounds on the approval row**, so a trade approved twenty minutes later still stamps the correct stop and target onto the position.

## Exit-Bounds Lifecycle

```
PM picks stop/target %  →  clamped to firm caps  →  stored on the Position
                                                          ↓
                             every later tick: scan price vs cost basis
                                                          ↓
        price ≤ basis × (1 − stop)  →  STOP_LOSS → full exit
        price ≥ basis × (1 + target) →  TAKE_PROFIT → full exit
        inside the band              →  no action
```

Bounds are set at the BUY fill and persisted per position (falling back to config defaults if a position somehow carries none). Enforcement runs on the deterministic `MONITOR_SELL` path — **no LLM on the protective-sell hot path**. On new data the PM may revise bounds, but only when it actually trades again; a plain HOLD keeps the existing ones.

That last rule took a moment of thought. It would have been easy to let every HOLD rewrite the bounds, but then a chatty model could quietly widen its own stop every hour and the protection would evaporate. Bounds change only on a real trade decision.

## Day Review Is Not The Same As A Stop

`DAY_REVIEW` is the overnight-gap check, and it's deliberately distinct from intraday bounds. A position can sit comfortably inside its stop/target band and still get flattened pre-close because holding it overnight is a different risk than holding it for another hour. It's also the only path that can do a **partial** exit — a TRIM of 50%.

## Keywords

architecture, deterministic orchestration, dispatcher, first-match-wins, tick loop, trading day replay, dispatch paths, CONTEXT_BUILD, INCREMENTAL_NEWS, PRICE_REEVAL, MONITOR_SELL, DAY_REVIEW, position sizing, exit bounds, stop loss, take profit, clamping, risk engine, paper broker, idempotency, FastAPI, SQLite, SQLAlchemy, LLM proposes code enforces, agentic pipeline, multi-agent
