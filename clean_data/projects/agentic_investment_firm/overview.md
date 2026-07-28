# Agentic Investment Firm — Overview

## Summary

The Agentic Investment Firm is a multi-agent AI system that runs a paper-trading desk over a **replayed US trading day**. A deterministic clock steps the day from open to close; at each tick a dispatcher routes to exactly one pipeline. LLM agents make the judgment calls — what evidence is relevant, what the thesis is, buy/sell/hold, where the exit bounds sit — and deterministic code owns everything that touches money or truth: sizing, risk limits, bound clamping, execution.

I built it as a timed take-home assessment for an agentic-AI engineering role, with a 3–4 day window. **It passed and I was moved to the next interview round.**

GitHub: https://github.com/markshperkin/agentic-investment-firm

## What It Actually Does

It simulates a real investment desk — the chain of specialized humans (research, portfolio management, risk, execution, reporting) that make stateful decisions under hard safety limits and leave an audit trail — and asks whether a multi-agent AI system can run that whole desk for a day. Believably, observably, auditably.

The goal was explicitly **not to beat the market**. It was to demonstrate trustworthy, reliable, grounded agent automation. That framing shaped every decision I made.

The three headline properties:

- **Every buy passes a human Risk Committee.** Above the notional threshold, the run pauses and waits for a person to approve, edit the quantity, or reject.
- **Every claim carries a verified citation** from a time-boxed RAG corpus. If evidence is insufficient, the system refuses instead of inventing a thesis.
- **Every action leaves a full, offline-replayable trace.** Any decision can be reconstructed end-to-end from committed artifacts, with no network and no API keys.

## The Design Priority I Chose

I wrote this priority order into the repo and then actually held to it:

> **agentic system → guardrails → observability.** Reliability and safety over features.

That meant I deliberately did not chase breadth. No multi-day backtests, no portfolio optimization, no cloud deployment, no auth, no Slack channel. One replayed day, done properly, with the full guardrail stack and a real audit trail. The bet was that senior engineers reviewing the submission would rather see one thing done to production standard than five things done shallowly.

## What Was Being Evaluated

I re-derived the grading criteria from the brief before writing any code, and ranked them:

1. **Multi-agent design** — real role-based collaboration, typed contracts, defined failure modes.
2. **Production readiness** — persistent state that survives a crash, human-in-the-loop, observability, guardrails, evals.
3. **RAG groundedness** — citations, refusal when evidence is insufficient, no hallucinated numbers.
4. **Eval rigor** — return metrics *and* process metrics, reported honestly.
5. **Code quality, architecture clarity, and the ability to defend trade-offs.**

The plan was to be excellent on 1–3 and honest and present on 4–5. Doing that ranking first is what kept me from wandering — I knew where to spend the days I had.

## The Seven Agents

| Agent | Job |
|---|---|
| **Query-Gen** | Plans retrieval queries for a ticker, with a strategy (baseline / decompose / step-back / HyDE / filter-fix) |
| **Relevance-Critic** | Grades whether the retrieved chunks actually answer the question, and says what's missing |
| **Research** | Forms a stance (bullish / bearish / neutral / insufficient evidence) with confidence and cited key points |
| **PM** | Turns a research view + the current book into BUY / SELL / HOLD plus proposed stop-loss and take-profit bounds |
| **Risk** | Narrates the case for the human Risk Committee — thesis card, citations, severity |
| **Day-Review** | Pre-close: HOLD / TRIM / FLATTEN against overnight gap risk |
| **Reporting** | Narrates the end-of-day report (with a deterministic no-LLM fallback) |

Every agent speaks in Pydantic-typed contracts. No free-form text passing between stages — a downstream agent consumes a validated schema or the call fails and retries.

## The Stack

- **Backend** — Python 3.11, FastAPI, SQLAlchemy over SQLite, Pydantic v2
- **Agents** — Anthropic Claude (Haiku default, Sonnet available for escalation) behind a single `LLMRouter`
- **RAG** — Voyage `voyage-3.5` embeddings + Chroma, with a deterministic local fallback for offline runs
- **Data** — yfinance for prices, SEC EDGAR for the document corpus
- **Frontend** — React 18 + TypeScript + Vite dashboard (event feed, approvals inbox, portfolio, report, observability, datasets)
- **Ops** — Docker Compose one-command run, GitHub Actions CI running the full test suite and eval harness with zero tokens

## What Ships In The Repo

- A committed **sample run** — the end-of-day report as both JSON and Excel, plus the complete span trace as JSONL, generated offline with no keys.
- A **deterministic eval harness** — three golden scenarios and three red-team scenarios, run in CI.
- Full docs — architecture, runbook, PRD, seven ADRs, and a dedicated "why not LangGraph" write-up.

## Why I'm Proud Of It

The part I'd defend hardest in an interview is the split between judgment and enforcement. It's easy to build an agent demo where the LLM decides everything and it looks impressive until something goes wrong. Here the LLM literally cannot pick a trade size, cannot widen a stop past the firm cap, and cannot talk its way past the risk gate — because none of those are prompts, they're code. That's the difference between a demo and something you'd let near money.

## Keywords

agentic AI, multi-agent system, LLM agents, Anthropic Claude, Claude Haiku, Claude Sonnet, FastAPI, SQLite, SQLAlchemy, Pydantic, RAG, corrective RAG, CRAG, Voyage embeddings, ChromaDB, SEC EDGAR, yfinance, human-in-the-loop, HITL, risk engine, guardrails, observability, OpenTelemetry spans, trace store, paper trading, portfolio manager agent, deterministic orchestration, React, TypeScript, Vite, Docker Compose, GitHub Actions, eval harness, red-team, take-home assessment, passed to next interview round
