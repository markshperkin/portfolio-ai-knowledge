---
title: Portfolio Chatbot (Mark's GPT)
category: project
tags: [ai, rag, portfolio, nextjs, fastapi, pgvector, anthropic]
last_updated: 2026-05-01
weight: 1.0
---

# Portfolio Chatbot — Mark's GPT

Mark's GPT is the RAG-backed AI assistant you are talking to right now. It is a conversational interface on top of a structured knowledge base containing Mark's actual work history, projects, skills, and experience. Rather than a static resume page, it lets visitors ask questions in plain English and get cited, grounded answers drawn from real documents.

## Why It Exists

Traditional portfolio sites are passive. A visitor has to navigate categories, read walls of text, and build their own mental model. Mark's GPT inverts this: the visitor asks what they care about, and the system surfaces exactly that, with citations so they can verify.

## Architecture

The system is three repos working together:

**Knowledge repo** (`portfolio-ai-knowledge`): A structured set of Markdown files with YAML frontmatter. Each file covers one topic — a project, a role, a skill set, a publication. A GitHub Actions workflow enforces frontmatter schema on every push, keeping the knowledge base machine-readable.

**Backend** (`portfolio-ai-backend`): A Python FastAPI service with a RAG pipeline. A reindex CLI walks the knowledge corpus, chunks each document into ~800-token segments with 100-token overlap, embeds them with Voyage AI `voyage-3-large` (1024 dimensions), and writes them to a pgvector-enabled Postgres database. At query time: embed the question, retrieve top-5 chunks by cosine similarity (HNSW index), inject into the system prompt, stream from Anthropic Claude Haiku 4.5 via Server-Sent Events.

**Frontend** (`portfolio-ai-frontend`): A Next.js 15 / React 19 terminal-aesthetic UI. The boot sequence shows an ASCII banner character-by-character. The chat interface renders streaming delta tokens in real time and displays a citation footer after each answer. Suggested prompts surface on first load. Conversation persists across same-tab reloads via `sessionStorage`.

## Key Design Decisions

- **pgvector over a dedicated vector store**: eliminates an external service, keeps the stack simple, and Postgres handles the persistence needs anyway.
- **Voyage AI `voyage-3-large`**: retrieval-tuned embeddings outperform general-purpose models on domain-specific Q&A.
- **SSE over WebSockets**: the server is stateless; SSE is a simpler fit for one-directional streaming.
- **Character-by-character drip rendering**: matches the terminal aesthetic and makes the AI feel responsive even at low token rates.
- **sessionStorage (not localStorage)**: conversation is session-scoped by design — a new tab starts fresh, consistent with the stateless server model.

## Tech Stack

- Python 3.11 · FastAPI · asyncpg · Voyage AI · Anthropic Claude Haiku 4.5
- Postgres 16 · pgvector · HNSW index · cosine similarity
- Next.js 15 · React 19 · TypeScript · Tailwind CSS
- Docker Compose · Hostinger VPS · GitHub Actions

## What It Demonstrates

This project demonstrates full-stack AI engineering: knowledge pipeline design, embedding strategy, RAG retrieval tuning, streaming API design, and production-ready deployment. Every component was built from scratch by Mark, including the chunking strategy, the SSE event protocol, and the terminal-style UI.
