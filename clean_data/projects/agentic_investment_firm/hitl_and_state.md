# Agentic Investment Firm — Human-in-the-Loop and Durable State

## Summary

Every buy at or above the notional threshold pauses the run and waits for a human Risk Committee decision — approve, edit the quantity, or reject. The requirement was that state persists across that wait, and it does: a pending trade is a durable database row that survives a restart. Crash recovery re-drives approved-but-unfilled trades idempotently and re-verifies the ledger against its own history.

## The Approval Flow

1. The risk engine returns `REQUIRE_HUMAN` for a buy at or above $25k notional.
2. `submit_for_approval` writes an `ApprovalRequest` row — ticker, side, quantity, reference price, notional, the thesis card, the risk narrative and severity, **and the clamped stop/target bounds** — with status `PENDING`. A `HITL` span is emitted.
3. In a live replay the run **blocks**, polling for the row to leave `PENDING`, up to a configurable timeout (default 30 minutes).
4. A human hits the Approvals inbox in the dashboard and decides.
5. On approve or edit, the risk engine **re-evaluates against the current book** (the state may have moved during the wait), then the broker executes with the approval id as the idempotency key.
6. The bounds carried on the approval row get stamped onto the resulting position.
7. On reject or timeout: no fill, and the outcome is traced either way.

Sells never wait. A risk-reducing sell and a protective stop execute automatically — pausing a stop-loss for human review would defeat its purpose.

## Blocking vs Queuing

There's a context-variable switch for whether the run actually blocks at the gate:

- **Live replay** — blocking. The day genuinely stops until a person decides. That's what makes the demo real.
- **Eval, CI, unit tests** — queue the approval and continue. A deterministic test suite that waits thirty minutes for a human is not a test suite.

Same code path, one flag. The alternative — a separate test-only pipeline — would mean CI validating something other than what ships.

## "Graph State Persists Across The Wait"

The brief's HITL wording maps almost literally onto a checkpointed graph framework, and my first ADR chose LangGraph for exactly that reason. I superseded it during the build.

The requirement is that decision state **survives the pause and a restart** so an in-flight trade is never lost. A durable `PENDING` `ApprovalRequest` row satisfies that completely. It survives a restart trivially — it's a row in a database — and it's resumed by the approval HTTP call, which is a stateless endpoint reading a row rather than a re-entry into a suspended execution with the right thread and checkpoint.

I wrote the full reasoning up in `docs/why-not-langgraph.md`, deliberately fair to the framework rather than strawmanning it. The honest version is in the tech-decisions file.

## State Store

SQLite via SQLAlchemy ORM. Every book mutation is one ACID transaction writing Trade, Position, and P&L snapshot atomically. Trade `idempotency_key` makes resume safe.

Why SQLite: zero-ops, file-based, commits to the repo, and gives crash recovery for free. A reviewer clones and runs it in under ten minutes with no infrastructure. Postgres would buy concurrent-write scale this system doesn't have while adding a service to the demo path — and since it's all through the ORM, it's a config swap when it's actually needed. A JSON file or pickle was disqualifying: no ACID, corrupts on a crash mid-write, and this is money state.

Persisted models: portfolio, positions, trades, P&L snapshots, approval requests, spans and runs, ticker memory, documents and chunks, dataset assets.

## Crash Recovery

On boot the server reconciles. Two steps:

**1. Re-drive unfilled approvals.** An approval can be marked `APPROVED` while the fill that should have followed was lost to a crash between the two writes. Every such approval gets re-driven through the broker using the approval id as the idempotency key — so a fill that already happened replays as a no-op and **it can never double-fill**. Idempotency is what makes "just retry it" safe here; without it, recovery would be more dangerous than the crash.

**2. Verify the ledger invariant.** For each run, rebuild cash and share counts from that run's FILLED trade ledger and compare against the stored book:

```
starting_cash − Σ(buy notional + commission) + Σ(sell notional − commission) == stored cash
Σ(buys) − Σ(sells) per ticker                                                == stored quantity
```

Any drift means a book diverged from its own history, which is the thing you most want to know about immediately.

A clean boot stays silent. If anything was fixed or the book is off, a `crash_recovery` span records exactly what happened — so recovery is auditable rather than invisible. You can kill the process mid-cycle, restart, and watch it reconcile.

## Why This Mattered For The Assessment

"Production readiness" was the second-highest-weighted criterion, and it's the one where most take-home submissions quietly wave. It's easy to demo an agent making a decision. It's harder to show a system where a person pauses it mid-flight, where the process can be killed and restarted without losing or duplicating a trade, and where the book can prove it matches its own transaction log.

That's also just what I'd want if it were real money. The reconciliation-on-boot design isn't there to impress a reviewer — it's there because the failure it prevents (a phantom fill, a drifted book) is the kind you discover far too late.

## Keywords

human-in-the-loop, HITL, approval workflow, risk committee, blocking approval, approval timeout, durable state, state persistence, SQLite, SQLAlchemy, ACID transactions, idempotency, idempotency key, crash recovery, reconciliation, ledger invariant, double-fill prevention, restart safety, LangGraph alternative, checkpoint, paper trading, portfolio state, production readiness
