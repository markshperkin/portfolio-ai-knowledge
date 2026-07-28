# Agentic Investment Firm — RAG and Groundedness

## Summary

The firm's research is grounded in a **time-boxed corpus of SEC filings**. Retrieval runs a corrective-RAG loop that grades its own results and reformulates, and refuses honestly when it can't do better. Every claim that survives has to be traceable to a real retrieved chunk with figures that actually appear in the source. Nothing about this is prompt-based — it's all verification code after the model speaks.

## Corpus: SEC EDGAR, Only

I chose SEC EDGAR as the sole document source, and that choice does a lot of work:

- **Public domain**, so it's safe to commit to a public repo.
- **Authoritatively timestamped** — the filing acceptance datetime is the published date, not a guess from a news scraper.
- **Queryable by date, form type, and company.**
- **Deep history** — any past trading day is usable, which matters for a replay system.

10-K and 10-Q for citable numbers; 8-K and press-release exhibits for the events and triggers that actually move a day. No third-party news APIs, which would have meant licensing questions, unreliable timestamps, and a dependency I couldn't commit.

## Time-Boxing: No Lookahead

The single most disqualifying bug in a replay system is letting a model see the future. Two independent defenses:

1. **Retrieval filters** `published_date <= as_of` at query time, inside the vector store search.
2. **A hard boundary assertion** (`guardrails/lookahead.py`) runs on **every path**, including the ones that bypass the retriever entirely — direct news push, cached-view reuse. It raises `LookaheadViolation` and aborts the run loudly rather than silently corrupting results.

The second one exists precisely because the first one is easy to trust and easy to route around. The filter does the work; the assertion proves the filter held.

## Corrective RAG (CRAG)

Instead of "retrieve top-k and hope," retrieval is a bounded self-correcting loop:

```
plan (query_gen) → retrieve → grade (relevance_critic)
    ├─ accepted            → return chunks
    └─ rejected, attempt<2 → reformulate from the critique → retry
                             (exhausted) → INSUFFICIENT_EVIDENCE
```

Details that matter:

- **The retry is informed.** Query-Gen gets the queries it already tried plus the critic's structured critique — including a `failure_kind` (no hits / wrong entity / stale / too generic / off-topic) and a `fix_hint`. It reformulates against a diagnosis, not blindly.
- **Multi-query merge.** A plan can emit several queries; results are merged by chunk id keeping the best score, then re-ranked and truncated to k.
- **Acceptance is two-sided** — the critic saying "relevant," *or* coverage clearing a minimum threshold (0.3). I'm grading for a decision-useful trading view, not for complete financial statements. A strict critic that demands exhaustive coverage would refuse forever.
- **Retries only on bad retrieval, never on a negative decision.** If the evidence is good and the answer is "bearish" or "don't trade," that's a result — not something to retry until it changes. This is the difference between correcting retrieval and rerolling until you like the answer.
- **Bounded at 2 retries**, then an honest `INSUFFICIENT_EVIDENCE` refusal that propagates all the way up: no thesis, no trade, recorded to memory.

The whole loop is traced as a tree — `crag → attempt N → {query_gen, relevance_critic}` — so a reviewer can see exactly what was searched, what came back, and why it was rejected.

## Citation Verification

The research agent must attach a citation to every key point: a chunk id and a quote. After the model speaks, code checks it:

```python
for kp in view.key_points:
    if kp.citation.chunk_id not in retrieved_ids:
        continue                      # fabricated citation → dropped
    if not quoted_numbers(kp.citation.quote) <= numbers(source_text):
        continue                      # a quoted figure isn't in the source → dropped
    kept.append(kp)

if view.stance in ("BULLISH", "BEARISH") and not kept:
    view.stance = "INSUFFICIENT_EVIDENCE"   # a stance with no grounding is no stance
    view.confidence = 0.0
```

Two subtleties I had to get right:

- **I check the quote's numbers, not the prose's.** The point's prose may legitimately paraphrase or derive a figure — "64% higher" might be computed from two numbers in the source and appear nowhere verbatim. Checking the prose would strip valid analysis. Checking the quote catches the actual failure mode: a model inventing a figure and attributing it to a document.
- **Model-inserted bracket labels get stripped before number extraction.** Models like to annotate quotes with things like `[Q1 FY2027]` to clarify which table column they're reading. Without stripping those, the `2027` reads as a fabricated source number and a perfectly good citation gets thrown out. That one cost me a debugging session.

The collapse rule at the end is the important part: a bullish stance whose every supporting point failed verification doesn't become a weakly bullish stance. It becomes a refusal.

## Embeddings and Vector Store

**Voyage `voyage-3.5`** for embeddings, chosen for retrieval quality, behind a provider abstraction. Voyage aligns queries and documents better when told which is which, so `input_type="query"` for search strings and `"document"` for stored chunks.

**Chroma** as the vector store — persistent, local, no service to run. Vectors keyed by chunk id with metadata `{ticker, published_date, source, form_type}`, which is exactly what the time-box filter needs. I rejected FAISS (no built-in metadata filtering or persistence ergonomics) and hosted options like Pinecone/Weaviate (external dependency in the demo path).

For offline runs there's a **deterministic hashing-trick fake embedder**: shared tokens map to the same dimensions, so cosine similarity stays lexically meaningful. It's not good retrieval, but it's *stable* retrieval — which is what a deterministic test suite needs. Vectors are persisted once, so CI replays stored vectors and never re-embeds; no Voyage key is needed at replay time.

## Injection Quarantine

Retrieved corpus text is **untrusted input**. Every chunk is scanned before it reaches an agent, and anything matching imperative or tool-directive patterns is quarantined out — "ignore all previous instructions," "you are now," "system:", "buy now at any price," "transfer funds," "override the risk engine."

Quarantined chunks emit a `GUARDRAIL` span with status `REJECTED`, so the block is visible in the trace rather than silent.

I'm honest about the limits of this: it's regex-based pattern matching, which catches the obvious documented attack shapes and not a sophisticated adversary. The real defense is architectural — even a successful injection can't move money, because the LLM doesn't hold the keys to the book. Sizing, limits, and the human gate are all downstream of anything a prompt could influence. Defense in depth means the pattern scan is the first layer, not the only one.

## Keywords

RAG, retrieval augmented generation, corrective RAG, CRAG, self-correcting retrieval, groundedness, citation verification, hallucination prevention, SEC EDGAR, 10-K, 10-Q, 8-K, time-boxing, lookahead bias, Voyage AI, voyage-3.5, embeddings, ChromaDB, vector store, metadata filtering, prompt injection, injection quarantine, untrusted input, refusal, INSUFFICIENT_EVIDENCE, relevance grading, query reformulation, fake embedder, deterministic testing
