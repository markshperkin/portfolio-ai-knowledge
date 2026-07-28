# Agentic Investment Firm — The Agents and the Pipeline

## Summary

Seven LLM agents, each with a narrow job and a Pydantic-typed output contract. No free-form text ever crosses an agent boundary — a downstream stage consumes a validated schema or the call retries and then fails loudly. This is what makes the multi-agent design real collaboration rather than a chain of prompts hoping for the best.

## The Roster

### Query-Gen
Plans retrieval for a ticker. Emits a `QueryPlan`: one or more queries, a retrieval `strategy` (`BASELINE`, `DECOMPOSE`, `STEPBACK`, `HYDE`, `FILTER_FIX`), and an optional date window. On a retry it receives the previous queries and the critic's critique, so the second attempt is informed rather than random.

### Relevance-Critic
Grades the retrieved chunks against the query. Emits `RelevanceGrade`: `relevant` (bool), `coverage` (0–1), what's `missing`, a `failure_kind` (`NO_HITS`, `WRONG_ENTITY`, `STALE`, `TOO_GENERIC`, `OFF_TOPIC`), and a `fix_hint`. The failure taxonomy is what lets Query-Gen actually correct itself — "no hits" and "wrong entity" call for different reformulations.

### Research
Forms the view. Emits `ResearchView`: ticker, `stance` (BULLISH / BEARISH / NEUTRAL / INSUFFICIENT_EVIDENCE), `confidence` 0–1, and a list of `KeyPoint`s where **every point carries a `Citation`** with chunk id, source, published date, and a quote. The citation isn't decoration — it's checked (see the RAG and grounding file).

### PM (Portfolio Manager)
Takes the research view plus the current book and emits `PMDecision`: BUY / SELL / HOLD, a `ThesisCard`, and proposed `stop_loss_pct` / `take_profit_pct`. Note what's absent: **quantity**. The PM never sizes a trade.

The `ThesisCard` is a nice piece of structure — headline, why now, expected edge, risks, confidence, key evidence. It's the artifact the human Risk Committee reads when deciding, so it's written for a person, not for a log.

### Risk (narration)
Packages the case for the human: reasoning plus a severity rating. Crucially the risk *agent* only narrates — the risk *engine*, which is deterministic code, is what actually enforces. If the agent hallucinates a reassuring paragraph it changes nothing about whether the trade is allowed.

### Day-Review
Pre-close. Emits `EodDecision`: HOLD / TRIM / FLATTEN with reasoning and a `gap_risk` rating. The only agent that can produce a partial exit.

### Reporting
Narrates the end-of-day report into `ReportSummary` (headline, summary, risk note). Has a deterministic no-LLM fallback so the reporting channel works even fully offline.

## Typed Contracts, Concretely

Everything is Pydantic v2 with real constraints:

```python
class TradeProposal(BaseModel):
    ticker: str
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0)
    est_notional: float = Field(ge=0.0)
    thesis_card: ThesisCard
    stop_loss_pct: float = Field(gt=0.0, le=1.0)
    take_profit_pct: float = Field(gt=0.0, le=1.0)
```

A malformed structured output gets **one retry** in the router — a model leaking tool-call tags into a field is usually transient, and re-asking yields a clean parse. Second failure raises. I chose one retry rather than three because a persistently malformed schema is a bug I want to see, not paper over.

## How A Path Runs End To End

**`CONTEXT_BUILD` — tick 0, per ticker:**

1. Is there a price? No → skip.
2. Run the CRAG loop: plan → retrieve → grade, retrying up to twice on bad retrieval.
3. `INSUFFICIENT_EVIDENCE` → refuse honestly, write it to memory, done. No thesis gets fabricated.
4. Otherwise Research produces a view from the chunks.
5. NEUTRAL or INSUFFICIENT → no actionable view, recorded.
6. BULLISH or BEARISH → into the shared PM → bounds → risk → execute sub-flow.

**`INCREMENTAL_NEWS` — a filing landed:** deduped against `processed_doc_ids` on the ticker's memory, then the **new chunks go straight to Research with the prior view as context — no retrieval at all**. You already know what's new; searching for it again is wasted latency and tokens.

**`PRICE_REEVAL` — material move, no new evidence:** no retrieval, no re-research. Reuse the cached research view and re-run only the PM against the new price. If the cached view was neutral, it no-trades immediately.

**`MONITOR_SELL`:** zero LLM calls. Pure deterministic scan and protective sell.

**`DAY_REVIEW`:** delta-retrieve evidence since the last tick, then the day-review agent decides against overnight gap risk.

## Per-Ticker Memory

Each ticker carries a memory record — its belief timeline across the day: what the stance was at each tick, what changed it, which document ids have already been processed. Two things fall out of that:

- **Dedupe** — `INCREMENTAL_NEWS` never re-reacts to a filing it already consumed.
- **Belief evolution** — the observability view can show how the firm's opinion on a ticker moved through the day, and why. That turned out to be one of the more compelling things to show a reviewer.

## Failure Modes Are Defined, Not Discovered

Each agent has an explicit degradation path:

| Failure | Behavior |
|---|---|
| Retrieval returns nothing useful | CRAG retries ≤ 2, then `INSUFFICIENT_EVIDENCE` — an honest refusal |
| Research cites a chunk that doesn't exist | Citation verifier strips the point; a stanced view with no surviving points collapses to `INSUFFICIENT_EVIDENCE` |
| Model emits malformed JSON | One retry in the router, then raise |
| One ticker's pipeline throws | Degrades to an error span; the run continues for other tickers |
| Run exceeds call / token / time budget | `BudgetExceeded` halts the whole run cleanly |
| Human never answers an approval | Approval times out; no fill |

The distinction between "isolate and continue" and "halt everything" is deliberate. A single ticker blowing up shouldn't kill the day. A runaway budget should.

## Keywords

LLM agents, agent roles, typed contracts, Pydantic schemas, structured outputs, query generation, relevance critic, research agent, portfolio manager agent, risk agent, day review agent, reporting agent, thesis card, citations, failure modes, graceful degradation, ticker memory, belief evolution, deduplication, corrective RAG, multi-agent collaboration, retry logic, schema validation
