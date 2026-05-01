---
title: About Mark Shperkin
category: meta
tags: [bio, overview, contact, ai, software-engineering]
last_updated: 2026-05-01
weight: 2.0
---

# About Mark Shperkin

Mark Shperkin is a software engineer focused on applied AI — building systems that use language models, retrieval, and embeddings to solve real problems. He works across the full stack, with particular depth in AI/ML pipelines, backend services, and product-quality frontends.

## What He Builds

Mark's work sits at the intersection of AI engineering and product development. He designs and implements RAG pipelines, embedding strategies, streaming APIs, and the user-facing interfaces that make these systems accessible. He thinks carefully about the product side — not just whether a feature works technically, but whether it serves the person using it.

Recent focus areas:
- **Retrieval-Augmented Generation**: designing knowledge pipelines, embedding strategies, retrieval tuning, confidence thresholds
- **Streaming systems**: Server-Sent Events, character-level rendering, stateless API design
- **Full-stack AI products**: FastAPI backends, Next.js frontends, Postgres/pgvector, Docker deployment
- **AI safety surface**: grounding, hallucination mitigation, graceful fallbacks, abuse handling

## Strongest AI Work

Mark's strongest AI work is the RAG pipeline work seen across Tutor-AI and this portfolio chatbot. Both systems required making principled decisions about where the model is allowed to speak (inside the retrieved context) and where it should refuse (outside it). The threshold-based fallback system — no-match refusal, weak-match clarification — is a deliberate safety boundary that required empirical tuning against real queries.

## Contact

To reach Mark, run `sudo hire-mark` in the chat, or ask "how do I reach Mark?". His contact details, LinkedIn, and Calendly link are surfaced there.

## Skills Summary

- **Languages**: Python, TypeScript, SQL
- **AI/ML**: RAG pipelines, vector embeddings (Voyage AI), Anthropic Claude API, prompt engineering
- **Backend**: FastAPI, asyncpg, Postgres, pgvector, Docker
- **Frontend**: Next.js, React, Tailwind CSS, SSE streaming
- **Infrastructure**: Docker Compose, GitHub Actions, Linux VPS deployment

## Approach

Mark prefers building things that are simple, correct, and maintainable over clever abstractions that optimize prematurely. He makes explicit architectural decisions (recorded as ADRs), keeps services stateless where possible, and designs for observable failure rather than silent degradation.

He is direct about tradeoffs: every design decision in his projects has a documented reason, not just a result.
