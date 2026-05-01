---
title: AI and Machine Learning Skills
category: skills
tags: [ai, ml, rag, embeddings, llm, vector-search, prompt-engineering]
last_updated: 2026-05-01
weight: 1.5
---

# AI and Machine Learning Skills

## Retrieval-Augmented Generation (RAG)

Mark has designed and built RAG pipelines from the ground up across multiple projects. This includes the full pipeline: document ingestion, chunking strategy, embedding generation, vector indexing, retrieval, prompt construction, and streaming generation.

Key decisions he has made in production RAG systems:
- Chunking strategy: ~800 tokens per chunk, 100-token overlap to preserve context across boundaries
- Embedding model selection: Voyage AI `voyage-3-large` for retrieval-tuned 1024-dim vectors
- Index type: HNSW (Hierarchical Navigable Small World) with cosine similarity for fast approximate nearest neighbor search
- Threshold design: strong match (answer), weak match (clarify), no match (refuse) — empirically tuned

## Vector Databases

Experience with pgvector (Postgres extension) as a vector store. Chose pgvector over dedicated vector databases (Pinecone, Weaviate, Chroma) in production systems because it eliminates an external service dependency and Postgres already handles the rest of the persistence layer. Trade-off: less purpose-built scaling, but sufficient for most retrieval workloads.

## Language Models and APIs

- **Anthropic Claude**: primary LLM. Used Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) for cost-efficient streaming completions in RAG systems. Claude Sonnet/Opus for higher-stakes tasks.
- **Streaming**: Anthropic streaming API consumed via SSE, mapped to delta events, rendered character-by-character on the client
- **Prompt engineering**: system prompt design for grounding, refusal behavior, persona, multi-source synthesis
- **Context window management**: trimming history, chunk injection sizing, staying within token budgets

## Embeddings

- Voyage AI `voyage-3-large` (1024 dimensions, retrieval-tuned)
- Understand the difference between retrieval-tuned and general-purpose embedding models
- Familiar with embedding API patterns: batch embedding, async embedding, idempotent reindex

## Applied AI Safety

- Grounding enforcement: systems refuse to answer outside retrieved context rather than hallucinating
- Abuse classification: prompt-level heuristics for detecting jailbreak attempts
- Rate limiting: per-IP cap to prevent prompt abuse and cost overruns
- Error surface sanitization: never leak internal errors or stack traces to the client

## What Mark Does Not Do

Mark is an AI engineer, not an ML researcher. He does not train models, fine-tune weights, or design novel architectures. His work is applied: taking capable foundation models and building reliable, grounded, production-quality systems on top of them.
