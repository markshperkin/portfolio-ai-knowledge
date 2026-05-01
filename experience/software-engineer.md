---
title: Software Engineering Experience
category: experience
tags: [software-engineering, fullstack, ai, backend, frontend]
last_updated: 2026-05-01
weight: 1.0
---

# Software Engineering Experience

## Overview

Mark has experience building full-stack software systems with a strong lean toward backend services and AI/ML pipelines. His work spans from data pipeline design to user-facing product interfaces.

**TODO (TASK-28)**: Replace this placeholder with real work history including company names, dates, titles, and specific accomplishments.

## Technical Depth

Mark's engineering experience covers:

**Backend systems**: RESTful and streaming APIs in Python (FastAPI) and TypeScript (Next.js API routes). Async database access with asyncpg and Postgres. Docker-containerized services with multi-stage builds. Non-root runtime users, healthchecks, and production-safe Docker Compose configurations.

**Database design**: Relational schema design in Postgres. Extension usage (pgvector). Index strategy including HNSW for vector similarity and compound B-tree indexes for query patterns. Migration management.

**AI/ML pipelines**: Document ingestion pipelines that parse, chunk, embed, and index unstructured text. Retrieval pipelines that embed queries, search vector indexes, and inject results into LLM prompts. Streaming generation pipelines with SSE event protocols.

**Frontend**: Next.js App Router (React 19, TypeScript, Tailwind CSS). Server-side and client-side data fetching. SSE consumption and incremental UI rendering. Browser storage strategies (sessionStorage for conversation state).

**Infrastructure**: GitHub Actions CI/CD pipelines. Docker Compose orchestration. Linux VPS deployment (Hostinger, Ubuntu 24.04). Nginx reverse proxy. Rootless Docker for sandboxed dev environments.

## Approach to Engineering

Mark treats software engineering as a design discipline. He documents decisions as ADRs, keeps services stateless where feasible, designs for observable failure modes, and prefers explicit over implicit contracts. He tests the happy path and the edges, not just the happy path.

He is comfortable owning a feature end to end: from database schema through API contract through UI rendering and deployment.

## Projects That Demonstrate Experience

- **Tutor-AI**: Full-stack RAG tutoring platform. Python/FastAPI backend, Next.js frontend, pgvector, Voyage AI, Anthropic Claude. End-to-end owned by Mark.
- **Portfolio Chatbot**: This system. Same stack. Designed as a portfolio artifact that demonstrates the AI engineering skills it describes.

See individual project documents for technical depth on each.
