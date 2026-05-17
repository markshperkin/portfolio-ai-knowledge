# Mark's GPT — RAG Pipeline

## Summary
The retrieval-augmented generation pipeline is the core of Mark's GPT. It turns a folder of Markdown into a queryable knowledge base: chunk the docs, embed them with Voyage AI, store the vectors in ChromaDB, and at query time retrieve the top matches and feed them to Claude — but only if they clear a relevance threshold. If nothing relevant comes back, the bot refuses rather than hallucinates.

## Context
The whole portfolio depends on the model answering *only* from facts about me. A general LLM with no grounding would happily invent a job I never had. So the design priority was grounding and refusal, not fluency. Retrieval quality and a hard relevance gate matter more than a clever prompt.

## Technical Details

### Indexing (the reindex CLI)
A CLI in the backend (`python -m app.reindex`) builds the index:

1. Walks the corpus path recursively for `*.md` files. Skips `README.md`, `INDEX.md`, `.github/`, `scripts/`.
2. Infers metadata from directory structure — no frontmatter required. `projects/` → category `project`, `research/` → category `paper`; tags derived from the subdirectory name.
3. Chunks each doc to ~400 tokens with ~70-token overlap.
4. Embeds each chunk via Voyage AI `voyage-3-large` (1024 dims), batch size 8.
5. **Deletes** the existing Chroma collection and recreates it — fully idempotent. Re-running always produces a clean, complete index.
6. Writes the persistent index to `data/chroma_db/`.

This is why the knowledge files don't need YAML frontmatter — the directory layout *is* the metadata. Drop a file into `clean_data/projects/foo/` and reindex; it's categorized automatically.

### Retrieval (query time)
1. Embed the incoming query with the same Voyage model (1024-dim).
2. ChromaDB HNSW index, cosine similarity, return top-5 chunks.
3. **Threshold gate:** if the best similarity score is below 0.30, refuse — there's no grounded context, so the bot says it can't answer that rather than guessing.
4. If it clears 0.30, the chunks go into the system prompt (persona + guardrails + retrieved context) and Claude Haiku generates a grounded, streamed answer.
5. A `citation` SSE event reports which source documents were used, so answers are traceable back to the corpus.

### Why the corpus is many small redundant files
The RAG system retrieves *chunks*, not whole documents. So the corpus is intentionally written as many small files with deliberate redundancy — important facts repeated across files — so that whatever chunk gets retrieved still carries the key information. That's a corpus-design decision driven by how chunk retrieval actually works.

## Challenges
The Voyage free tier rate limit (3 requests/minute) made reindexing slow and fragile, and the ChromaDB collection could go stale in the running container after a reindex. Both are detailed in `challenges.md`.

## Solutions
- **Rate limit:** batch the embeddings (size 8) with a delay between batches tuned to stay under 3 RPM.
- **Idempotent reindex:** delete-and-recreate the collection every run, so there's never a partial or stale-on-disk index — the only correct state is "fully rebuilt."
- **Refusal over hallucination:** the 0.30 threshold gate is the single most important line for a portfolio bot. I'd rather it say "I don't have that" than invent a credential.

## Results
- A grounded assistant that answers from my real corpus and cites its sources.
- A reindex that's safe to run repeatedly — no drift, no partial states.
- Zero-frontmatter authoring: metadata inferred from directory structure, so adding knowledge is just dropping a Markdown file in the right folder.

## Lessons Learned
The refusal path is worth more than the answer path here. A portfolio bot that confidently makes things up is worse than useless — it's a liability in front of a recruiter. Spending the design effort on the threshold gate and grounding, instead of prompt cleverness, was the right call.

## Keywords
RAG, retrieval-augmented generation, ChromaDB, HNSW, cosine similarity, Voyage AI, voyage-3-large, embeddings, 1024-dim, chunking, token overlap, reindex, idempotent, threshold gate, grounding, hallucination, refusal, citations, Claude Haiku, system prompt, vector store, metadata inference
