# Agentic Investment Firm — Tech Decisions and Trade-offs

## Summary

Seven ADRs, one of which I superseded mid-build, plus a dedicated write-up on the orchestration choice. This file is the "why X over Y" reference — the questions I expected in the follow-up interview and wanted crisp answers to.

## Deterministic Orchestration, Not LangGraph

The decision I'd most expect to be challenged on, and the one I put the most care into defending fairly.

**ADR-001 originally chose LangGraph.** The brief's HITL wording — "graph state persists across the wait" — maps almost literally onto a checkpointed graph with `interrupt()`. I superseded it during the build and wrote `docs/why-not-langgraph.md` explaining why, deliberately without strawmanning the framework.

**What I did not claim:** that LangGraph is less observable, or non-deterministic. Both are false. LangGraph edges can be deterministic conditional edges where code picks the next node; it's a graph runtime, and you control determinism by how you write edges. It also has solid tracing.

**The actual argument:** for a small, fixed, deterministic, single-process workflow, everything it provides — durable state, checkpoint/resume, a node/edge model — I already get directly:

| LangGraph gives… | I get it via… |
|---|---|
| durable state across steps | SQLite (portfolio, ticker memory, approvals) |
| checkpoint + resume after a pause | the persisted `PENDING` approval row |
| a node/edge execution model | the deterministic dispatcher + runner loop |
| interrupt/resume for HITL | stop-and-persist; the approval HTTP call resumes it |
| committed, offline-replayable trace | my own span store, built directly |

**The observability nuance, honestly:** LangGraph's native tracing path is LangSmith — external, key-gated, not committed to the repo. The brief wanted replay from *committed artifacts, offline*. To get that I'd instrument spans inside each LangGraph node anyway. So the framework wouldn't reduce the observability work; it would add a layer on top of the same span-emitting.

**And the concrete cost of adopting it:** state becomes graph channels with reducer semantics for the per-ticker fan-out; a checkpointer and thread management to configure; `interrupt()`/resume across an HTTP boundary (re-entering the graph with the right thread and checkpoint, versus a stateless endpoint reading a row); and debugging through the framework's execution model instead of plain stack traces.

**Where it would earn its place** — and I say this in the doc: large, branching, or cyclic workflows; dynamic agentic routing where an LLM picks the next node; long-running multi-step agents needing checkpoint/resume you don't want to build; or a team already living in LangSmith. None of those describe a fixed single-process day replay.

**The one-line version:** "The workflow is a small fixed pipeline, so orchestration stayed as explicit deterministic code with state in the database. 'Graph state persists across the wait' is satisfied by the persisted approval — without a framework whose checkpointing I'd be duplicating and whose native tracing wouldn't meet the committed-offline-replay requirement."

## SQLite over Postgres

**Chose:** SQLite via SQLAlchemy. Every fill is one ACID transaction; `cash + Σ holdings = equity` recomputed on startup; `idempotency_key` makes resume safe.

**Over Postgres:** needed for concurrent-write scale this doesn't have, and it adds a service to the demo path. A reviewer should clone and run in under ten minutes with no infra. Because it's all ORM, Postgres is a config swap — that's the documented production path.

**Over JSON/pickle:** no ACID, corrupts on a crash mid-write. Disqualifying for money state, full stop.

## Chroma + Voyage over FAISS / hosted

**Chose:** Chroma (persistent, local, no service) with Voyage `voyage-3.5` embeddings behind a provider abstraction, plus a local fallback so CI runs offline at zero cost.

**Over FAISS:** fast, but no built-in metadata filtering or persistence ergonomics — and metadata filtering is exactly what the time-box needs.

**Over Pinecone/Weaviate:** external dependency in the demo path, key-gated. Rejected on the same grounds as hosted tracing.

Vectors are persisted once, so replay and CI never re-embed and no Voyage key is needed at replay time.

## SEC EDGAR as the only corpus source

Public domain (safe to commit publicly), authoritatively timestamped (acceptance datetime = published date), queryable by date/form/company, deep history. 10-K/10-Q for citable numbers; 8-K and press-release exhibits for events.

Third-party news APIs would have meant licensing questions, softer timestamps — which is fatal when your core guarantee is no lookahead — and a dependency I couldn't ship in the repo.

## Anthropic with cost-aware routing

**Chose:** a single `LLMRouter` over Anthropic. Claude Haiku as the default for every agent step, with Sonnet wired in and available to escalate if an eval ever shows Haiku is insufficient. Per-call cost and tokens recorded in spans.

The design lets me be relaxed about model tier precisely *because* the hard decisions aren't the model's. Judgment and synthesis run on the cheap model; risk limits, sizing, and bound clamps are deterministic, and humans gate large trades. If the model tier mattered to safety, the architecture would be wrong.

**Over one large model everywhere:** simpler but higher cost, and the brief flagged token consumption as an evaluation concern.

**Over OpenAI:** fine in principle, but Anthropic was the assumed provider and structured output + tool use fit the typed-contract design well.

The provider interface is what makes the cassette mode possible — the recorded-response provider is just another implementation.

## Deterministic risk engine, not an LLM judge

**Chose:** a deterministic module as the only gate to the book, re-checked immediately before fill.

**Over LLM-judged risk:** flexible, but bypassable and hallucinable. Unacceptable for money.

**Over limits in prompts:** not enforceable — a single injection defeats them. This one isn't a trade-off, it's a category error, and I wanted the ADR to say so plainly.

Consequence I accept: the engine is less nuanced than a model would be. That's fine — the risk *agent* still provides narrative assessment for the human. Narration is judgment; enforcement is code.

## Self-built trace store over hosted tracing

Covered in the observability file. Short version: hosted tracing is external, key-gated, and not committable, and the requirement was offline replay from committed artifacts.

## Deterministic eval via frozen data + cassettes

**Chose:** frozen market snapshot + time-boxed corpus + recorded LLM responses keyed by prompt hash. CI needs no key, costs nothing, and is reproducible.

**Over live LLM in CI:** non-deterministic, costs tokens, needs secrets, flaky.

**Over return metrics only:** misses the process-quality rigor that actually matters here.

**Accepted downside:** cassettes drift from live model behavior. Mitigated by a separate non-CI live smoke run, and stated in the ADR rather than hidden.

## What I Deliberately Cut

Scope discipline was half the job. Out of V1: live (non-replay) operation, multi-day backtests, portfolio optimization, email and Slack channels, cloud deployment and IaC, managed agent runtimes, auth and multi-user, and position-level risk analytics like VaR and beta.

Each got parked with a note rather than half-built. Given the priority order — agentic system, then guardrails, then observability — going wide would have meant every one of those being shallow. I'd rather defend a small system that's actually production-minded than demo five features that fall over.

The one stretch item I did ship, kept deliberately minimal, is on-demand ticker ingestion — so the universe isn't hardcoded.

## Keywords

architecture decision records, ADR, technical trade-offs, LangGraph, why not LangGraph, deterministic orchestration, framework versus code, SQLite versus Postgres, ChromaDB, FAISS, Pinecone, Voyage AI, SEC EDGAR, Anthropic, Claude Haiku, Claude Sonnet, cost-aware routing, model routing, LLM provider abstraction, cassettes, deterministic evaluation, LangSmith, OpenTelemetry, risk engine, scope management, SLC, interview defense, engineering judgment
