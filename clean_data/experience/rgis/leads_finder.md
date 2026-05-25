# RGIS — Leads Finder (Flagship Project)

## Summary
Leads Finder is the flagship project I built at RGIS: a standalone GenAI-driven lead-intelligence platform, designed and developed end-to-end by me as the sole developer, iterated over ~3 months with twice-weekly production releases. It takes a user-defined search query and produces a ranked list of target companies with validated C-suite contacts and AI-generated rationale.

## Context / Problem
RGIS had no automated system for identifying high-value enterprise sales targets. The sales and business-development function needed a way to surface relevant companies and C-suite contacts at scale, filtered by geography, vertical, revenue size, and business signals. There was no prior system — the baseline was zero.

## What I Built
A standalone agentic pipeline application. Input is a user-defined search query; output is a ranked list of target companies with validated C-suite stakeholder contacts and AI-generated rationale.

**Input parameters:**
- Geography (30+ supported regions)
- Verticals (supply chain, manufacturing, logistics, etc.)
- Revenue range (min/max)
- Employee count range (min/max)
- Keywords
- Business signals
- Pain points

**Pipeline stages:**
1. LLM generates structured API search queries from user input.
2. 15+ APIs queried for company data, news, signals, and stakeholder data.
3. Raw data aggregated into structured company profiles.
4. Companies ranked and sorted by fit.
5. Perplexity fills missing profile data.
6. Top-k companies selected.
7. C-suite stakeholder search and validation across multiple APIs.
8. LLM generates scoring, rationale, and an overview per company.
9. Self-refinement loop evaluates output and re-triggers if needed (built; disabled in production for latency).

**Output:** ~20 target companies with 2–3 validated C-suite contacts each, plus AI-generated scoring and rationale per company.

## Tech Used
React + TypeScript (frontend), Python (backend), LangChain, LangGraph, the Anthropic model suite, Perplexity, 15+ external APIs, Docker, Kubernetes.

## Release Cadence
A new production version twice per week throughout the engagement — sustained for the full 3 months, including through an international relocation during an active war.

## Results
- Lead quality went from 0% actionable (no prior system) to 50–60% actionable (stakeholder-reported), within 3–4 weeks of starting development.
- Runtime optimized from 20–25 minutes down to ~15 minutes.
- ~40–60 qualified leads produced per run.

## Lessons Learned
Building a full agentic system solo, from zero, and shipping it twice a week, taught me to make scalability and grounding decisions early — the orchestrator design and the "verified data over LLM data" rule are what kept quality up while cost and hallucination stayed down. The recurring friction was requirements arriving second-hand; direct stakeholder access would have made the output more precisely tailored.

## Keywords
Leads Finder, RGIS, agentic pipeline, lead intelligence, LangChain, LangGraph, Anthropic, Perplexity, sole developer, GenAI, sales intelligence, C-suite, stakeholder validation, production releases, scalable architecture, FastAPI
