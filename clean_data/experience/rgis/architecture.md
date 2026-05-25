# RGIS — Architecture

## Summary
I built two things at RGIS: contributions to AI-HUB (an internal React/TypeScript hub for all AI services) and Leads Finder (a standalone agentic lead-intelligence pipeline in Python with LangChain/LangGraph, the full Anthropic model suite, Perplexity, and 15+ external data APIs, deployed on Docker + Kubernetes). A custom orchestrator sits between frontend and backend, designed so new AI services can be added without restructuring.

## AI-HUB
An internal web application that serves as the central hub for all AI services available to RGIS personnel.
- **Frontend:** React, TypeScript.
- **Services hosted:** AI translation (free text + file types — docx, pptx, xlsx, and more) and AI performance review (KPI insights and improvement recommendations for RGIS personnel).

## Leads Finder
The flagship standalone web application — an end-to-end agentic lead-intelligence pipeline.

**Frontend:** React, TypeScript. Standalone app, separate from AI-HUB. The input form supports geography (30+ regions), verticals (supply chain, manufacturing, etc.), min/max revenue, min/max employees, keywords, signals, and pain points.

**Backend:** Python. AI frameworks: LangChain, LangGraph. LLMs: the full Anthropic model suite, plus Perplexity for missing-data generation. External data: 15+ APIs covering company data, news, business signals, data validation, and stakeholder/contact data (specific APIs withheld per NDA). Deployment: Docker + Kubernetes on internal RGIS servers.

**Orchestrator:** a custom middle layer between frontend and backend. Pure routing and coordination — no AI logic. I designed it deliberately for scalability, so new AI services can be added in the future without restructuring the system.

## Pipeline Architecture (Leads Finder)
A multi-stage sequential pipeline:
1. **Query generation** — an LLM parses user input and generates optimized search queries for the data APIs.
2. **Data collection** — 15+ APIs queried for company data, news, signals.
3. **Profile building** — raw API data aggregated and normalized into a structured company profile per candidate.
4. **Ranking & sorting** — companies ranked by relevance to the input criteria.
5. **Gap filling** — Perplexity generates missing profile data.
6. **Top-k selection** — top companies selected for deeper processing.
7. **Stakeholder search** — C-suite contacts identified and validated via multiple APIs.
8. **Summarization & scoring** — an LLM generates each company's inclusion rationale, relevance score, and overview.
9. **Self-refinement loop** — an LLM evaluates overall output quality and decides whether to re-trigger the pipeline from step 1. Built and functional, but disabled in production due to latency (one loop ≈ 15 min; multiple loops exceeded stakeholder tolerance).

## Performance
- Optimized end-to-end runtime: ~15 minutes.
- Pre-optimization runtime: 20–25 minutes.
- Average output: ~20 companies × 2–3 stakeholders each (~40–60 leads per run).

## LLM Usage Patterns
- Batched multi-company calls — batch size per LLM call tuned to balance output quality vs. cost.
- Prompt-level guardrails — explicit DO NOT constraints to reduce hallucination.
- LLM used for query generation, missing-data inference, scoring, and rationale generation.
- Verified API data prioritized over LLM-generated data wherever possible, to reduce both hallucination and cost.

## Lessons Learned
Designing the orchestrator as pure routing with no AI logic was the right call — it's what makes adding future AI services cheap. And grounding the LLM in verified API data, rather than letting it generate freely, was the single highest-leverage decision for quality and cost.

## Keywords
RGIS, architecture, Leads Finder, AI-HUB, LangChain, LangGraph, Anthropic, Perplexity, agentic pipeline, orchestrator, React, TypeScript, Python, Docker, Kubernetes, RAG, prompt guardrails, batching, self-refinement loop, FastAPI
