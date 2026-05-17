# Mark's GPT — Portfolio Project Overview

## Summary
Mark's GPT is my portfolio website — but it's not a website in the usual sense. Instead of a static landing page with a project grid, the whole site *is* a RAG-backed AI chatbot. Visitors ask questions about me in plain English ("what did Mark do at RGIS?", "is he good with LLMs?") and get grounded, cited answers streamed back in a terminal-style interface. The chatbot is the portfolio, and building it is itself the proof that I can do AI engineering.

## Context
I wanted a portfolio, but I didn't want it to look like everyone else's — a simple landing page showcasing a few projects. Every developer has that. It says nothing about what I can actually build.

So I flipped it: the site is a retrieval-augmented chatbot trained on a structured corpus of my own work, experience, education, athletics, and research. To use my portfolio you have a conversation with it. The medium is the message — a recruiter who talks to it has already seen me design a RAG pipeline, wire up streaming, handle abuse, and ship the whole thing to production. That's a much stronger signal for an AI Engineer role than a screenshot gallery.

It's live and public, built solo in roughly 12 hours. It's a deliberately simple project in scope, but a complete end-to-end system.

## Technical Details
The system spans three Git repositories, each with its own CI/CD:

- **portfolio-ai-frontend** — Next.js 15 (App Router), React 19, TypeScript, Tailwind. A terminal-aesthetic chat UI that streams responses character-by-character over Server-Sent Events.
- **portfolio-ai-backend** — Python FastAPI. The RAG brain: embeds the query, retrieves relevant chunks from a Chroma vector store, injects them into a system prompt, and streams a grounded answer from Anthropic Claude Haiku. Also handles rate limiting and abuse detection.
- **portfolio-ai-knowledge** — the knowledge corpus itself (this repo). Structured Markdown about my background. A reindex CLI in the backend walks these files, chunks and embeds them via Voyage AI, and writes them to ChromaDB.

The flow end to end: knowledge repo → reindex → ChromaDB → backend retrieval → Claude Haiku → SSE → frontend drip render.

## Challenges
The hard parts weren't the happy-path RAG code — they were operational: keeping the vector store in sync across deploys, working inside free-tier rate limits, and getting a clean self-hosted deploy story across three repos. Those are documented in `challenges.md`.

## Results
- Shipped live and public, solo, in ~12 hours.
- A working RAG system: query embedding, vector retrieval, grounded generation with a refusal path, citations, and real-time streaming.
- A portfolio that demonstrates AI engineering by being an AI engineering artifact, not by describing one.

## Lessons Learned
The strongest portfolio piece is one a reviewer experiences rather than reads. Building the thing that showcases the skill, using the skill, beats listing the skill. Also: scoping it "simple" kept it shippable in a day instead of becoming a forever-project — the constraint was the feature.

## Keywords
Mark's GPT, portfolio, RAG, retrieval-augmented generation, AI chatbot, LLM, Next.js, FastAPI, ChromaDB, Voyage AI, Anthropic Claude Haiku, Server-Sent Events, SSE, vector search, embeddings, three-repo architecture, CI/CD, self-hosted, solo project, AI Engineer portfolio
