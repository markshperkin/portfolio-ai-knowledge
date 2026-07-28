# Agentic Investment Firm — Challenges and Lessons

## Summary

A 3–4 day timed take-home where the hard part wasn't any single technical problem — it was deciding what "done" meant, and then holding that line while the clock ran. **It passed and I moved to the next interview round.**

## Challenge: Scoping A System That Could Absorb Infinite Work

An AI investment firm is a bottomless brief. You could spend a month on it and still have a backlog.

**What I did:** before writing code, I re-derived the grading criteria from the brief and ranked them — multi-agent design, production readiness, RAG groundedness, eval rigor, code quality. Then I wrote a single priority line into the repo and treated it as a constraint rather than a slogan:

> agentic system → guardrails → observability. Reliability and safety over features.

Everything that didn't serve those three went to a parking lot with a note: live market operation, multi-day backtests, portfolio optimization, Slack and email channels, cloud deployment, auth. The plan was excellent on the top three criteria, honest and present on the rest.

**Lesson:** in a timed build, the ranking is the deliverable. Once the priority order existed, every "should I add X?" answered itself in seconds, and I stopped burning decision energy on scope.

## Challenge: Where To Draw The Line Between LLM And Code

The genuinely interesting design problem. Too much LLM and it's an impressive demo that can't be trusted. Too little and it's just software with a chatbot bolted on.

**Where I landed:** the LLM makes judgments — what evidence is relevant, what the thesis is, buy/sell/hold, how tight the exit bounds should be given conviction. Code makes every decision that touches money or truth — retrieval routing, sizing, clamping, enforcement, execution.

The concrete tests of that line:

- The PM proposes a stop and target, and gets real influence over them, but code clamps the result into firm caps.
- The PM emits BUY/SELL/HOLD but has no `quantity` field at all — the schema simply doesn't let it size a trade.
- The risk *agent* narrates the case for the human; the risk *engine* decides. If the narration is nonsense, nothing about the gate changes.

**Lesson:** the useful question isn't "how agentic should this be?" It's "what happens if this specific model output is adversarial or wrong?" Ask it per field. Where the answer is unacceptable, that field belongs to code.

## Challenge: Committing To LangGraph, Then Undoing It

ADR-001 chose LangGraph on day one. The brief's HITL phrasing — "graph state persists across the wait" — reads like a checkpointed graph, and I took the bait.

Partway in it became clear I was going to build the span-emitting instrumentation *inside* the framework's nodes anyway, because the requirement was offline replay from committed artifacts and LangGraph's native tracing path is a hosted SaaS. At that point the framework was adding a layer over machinery I'd already built.

**What I did:** superseded the ADR in place rather than deleting it, and wrote a standalone `why-not-langgraph.md` that's deliberately fair — correcting two misconceptions in the framework's favor, explaining where it genuinely would earn its place, and only then making my case.

**Lesson:** documenting a reversal honestly is stronger than pretending the first decision never happened. A reviewer who sees "Accepted → Superseded, here's what changed my mind" learns more about how I think than a clean set of ADRs that were all right the first time. And writing the fair version forced me to check I wasn't just rationalizing not learning a framework.

## Challenge: Citation Verification That Doesn't Eat Good Analysis

The first version of the citation check compared numbers in the model's prose against the source. It stripped valid points constantly — a research view saying "revenue grew 64% year over year" is derived from two figures in the filing and appears verbatim nowhere.

**Fix:** verify the **quote's** numbers against the source, not the prose's. The quote is a claim about what the document says, so it must be literally true. The prose is analysis, and analysis is allowed to compute.

Then a second failure: models annotate quotes with bracket labels to clarify table columns — `[Q1 FY2027]` — and the `2027` read as a fabricated source number, killing perfectly good citations. Stripping bracketed labels before number extraction fixed it.

**Lesson:** grounding checks fail in both directions, and false positives are the expensive kind. A verifier that strips good analysis makes the whole system look incapable, and you'll blame the model instead of your checker. Both bugs presented as "the LLM is bad at citations."

## Challenge: Making The Human Gate Real Without Breaking CI

A blocking approval gate is what makes the demo convincing — the day genuinely stops until a person clicks. It's also poison for a deterministic test suite that can't wait thirty minutes.

**Fix:** a context-variable switch. Live replays block; eval and CI queue the approval and continue. One code path, one flag — rather than a test-only pipeline that would mean CI validating something other than what ships.

The related detail: the wall-clock budget had to credit back time spent waiting on a human. Without `credit_wait()`, any run with a real person in it trips the circuit-breaker and dies. That's a bug you only find by actually running the flow end to end instead of unit-testing around it.

## Challenge: Recovery That Can't Make Things Worse

A crash between "approval marked APPROVED" and "fill written" leaves a phantom: the system believes it traded, and it didn't. Naive recovery — re-drive the approval — risks the opposite failure, a double-fill, which is worse.

**Fix:** the approval id *is* the idempotency key. Re-driving is safe by construction: a fill that already happened replays as a no-op. Then verify the ledger invariant — rebuild cash and share counts from the FILLED trade log and compare to the stored book. A clean boot stays silent; anything fixed or drifted writes a `crash_recovery` span.

**Lesson:** recovery code runs exactly when the system is already in a bad state, which is the worst time to discover it has its own failure mode. Idempotency isn't an optimization there — it's what makes retry a legitimate strategy at all.

## Challenge: Being Honest About Weak Results

The eval reports +0.79% portfolio return against SPY's +0.00% on the replay day. It would have been easy to present that as alpha.

It's one day and one ticker. It's noise. I wrote it as noise, put the weight on the process metrics — groundedness 1.0, red-team block rate 1.0 — and stated in the runbook that the budget caps are still first-pass guesses that need a measured live run.

**Lesson:** on a submission judged by senior engineers, calibrated honesty reads as competence. Overclaiming on a number any reviewer can see through costs more than the number was worth. I'd rather be the candidate who says "this metric doesn't mean what it looks like."

## What I'd Do Differently

- **Measure the budget caps.** The call/token/time limits are guesses. One instrumented live run gives real numbers.
- **Strengthen injection defense.** Regex pattern matching catches documented attack shapes, not a creative adversary. A classifier pass or structural constraints on retrieved text would be the next layer — though the architecture already means a successful injection gets you a bad thesis, not a bad trade.
- **Guard against cassette drift.** Deterministic CI is the right call, but a scheduled live smoke run would catch the day the recorded responses stop resembling reality.
- **More red-team scenarios.** Three is enough to prove the pattern works. Ten would start to be coverage.

## Keywords

challenges, lessons learned, scope management, timed take-home, prioritization, LLM versus code boundary, agentic design, ADR reversal, superseded decision, citation verification, false positives, grounding, human-in-the-loop, blocking approval, CI determinism, crash recovery, idempotency, ledger invariant, honest reporting, calibrated claims, prompt injection limits, cassette drift, engineering judgment, interview assessment, passed to next round
