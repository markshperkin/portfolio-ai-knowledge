---
title: Tutor-AI
category: project
tags: [ai, llm, education, rag, fastapi, nextjs]
last_updated: 2026-05-01
weight: 1.0
---

# Tutor-AI

Tutor-AI is an AI-powered tutoring platform built to deliver personalized, on-demand academic assistance across a range of subjects. The system uses a Retrieval-Augmented Generation (RAG) pipeline backed by course-specific knowledge bases, enabling the model to give grounded, cite-backed answers rather than generic completions.

## What It Does

Students interact with Tutor-AI through a conversational interface. They can ask questions about lecture material, problem sets, or concepts, and the system retrieves the most relevant course documents before generating an answer. This keeps responses grounded in the actual curriculum rather than the model's general training.

Key capabilities:
- **Subject-scoped retrieval**: Each course gets its own vector-indexed knowledge base. Queries are routed to the right scope before retrieval.
- **Multi-turn dialogue**: The system maintains conversation history within a session, so follow-up questions carry context.
- **Citation surface**: Every answer lists the source documents used, giving students a way to trace claims back to course material.
- **Adaptive difficulty**: The system prompt is tuned to match the student's level — introductory vs. advanced — based on the enrolled course level.

## Architecture

The backend is a Python FastAPI service. Embeddings are generated with Voyage AI's `voyage-3-large` model and stored in a pgvector-enabled Postgres database. At query time, the top-k chunks are retrieved by cosine similarity, injected into the system prompt, and sent to Claude (Anthropic) for completion. The response streams back to the client via Server-Sent Events (SSE).

The frontend is built with Next.js and React. It consumes the SSE stream and renders text character-by-character for a terminal-like typing effect, consistent with the overall design aesthetic.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, asyncpg, Voyage AI, Anthropic Claude
- **Database**: Postgres 16 with pgvector (HNSW index, cosine similarity)
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Infrastructure**: Docker Compose, Hostinger VPS, GitHub Actions CI/CD

## Mark's Role

Mark built the full stack end to end — from the RAG pipeline design and embedding strategy to the streaming frontend and deployment pipeline. He made the key architectural decisions: choosing pgvector over a dedicated vector store for simplicity, selecting Voyage AI for its retrieval-tuned embeddings, and opting for SSE over WebSockets to keep the backend stateless.

## What Makes It Interesting

The interesting engineering problem was keeping the system grounded. Large language models hallucinate, especially on domain-specific course content. The solution was to enforce a tight retrieval-before-generation loop with cosine similarity thresholds: if no document scores above a confidence floor, the system tells the student it doesn't have enough context from course material rather than making something up. This is a deliberate product choice as much as a technical one.
