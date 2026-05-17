# Mark's GPT — Technical Decisions

## Summary
Every stack choice in Mark's GPT — Voyage embeddings, Claude Haiku, ChromaDB, Caddy, a self-hosted VPS — was driven by the same four-way tradeoff: cost, quality, skill showcase, and full control. This file is the "why did you pick X over Y" reference, which is exactly what gets asked about a portfolio project in an interview.

## Context
This is a portfolio piece, so the decisions carry double weight: they have to produce a good system *and* they have to demonstrate judgment. I optimized for four things at once — keep it cheap (it runs on my dime), keep retrieval quality high (a hallucinating portfolio bot is a liability), deliberately use tools that show AI-Engineer breadth, and own the whole pipeline end to end rather than rent it.

## Technical Details — the decisions

### Embeddings: Voyage AI `voyage-3-large`
- **Quality:** Voyage's retrieval embeddings are best-in-class; for a RAG bot, retrieval quality is the ceiling on answer quality.
- **Cost:** the free tier is enough for a corpus this size (the only catch is the 3 RPM limit, which I engineered around).
- **Showcase:** choosing a dedicated embedding model over the default OpenAI one shows I actually think about the retrieval layer, not just the LLM.

### LLM: Anthropic Claude Haiku 4.5
- **Cost:** Haiku is cheap per token — the right tier for a public endpoint that strangers can hit freely.
- **Quality:** more than capable for grounded Q&A over retrieved context. The hard work is retrieval + the system prompt; the model just has to synthesize faithfully, which Haiku does well.
- **Control:** with a tight grounding prompt and the threshold gate, a small fast model is the correct choice — not a weaker compromise.

### Vector store: ChromaDB
- **Cost / control:** file-based, runs in-process, no managed vector DB bill and no external service to depend on. HNSW + cosine, persistent on disk.
- **Simplicity:** for a single-instance portfolio backend, a hosted vector DB would be over-engineering. Chroma is the right size.
- **The tradeoff:** in-process means the cached collection handle goes stale after a reindex (see `challenges.md`). I accepted that and handle it with a container restart — a known cost of the simple choice.

### Reverse proxy / TLS: Caddy
- **Control / cost:** Caddy gives automatic Let's Encrypt TLS and clean reverse-proxy routing with almost no config. Free, self-managed, no platform.

### Hosting: self-hosted Hostinger VPS + Docker
- **Cost:** no per-invocation or per-seat platform fees.
- **Control:** I own Docker, the proxy, TLS, CI, the deploy path — all of it.
- **Showcase:** owning the full deployment story is itself the portfolio statement. Anyone can deploy to a managed platform; doing the whole pipeline is the differentiator.

## Challenges
The four-way optimization isn't free — every "cheap + controlled" choice has a tradeoff. The clearest one: in-process ChromaDB saved cost and complexity but created the stale-singleton bug. I chose to accept and manage tradeoffs rather than buy them away with managed services.

## Solutions
Make the tradeoff explicit and handle it operationally instead of architecturally. Stale Chroma handle → restart on reindex. Voyage rate limit → batch with delay. Self-host complexity → push-to-deploy CI so the complexity is paid once. Cheap choices with understood, documented mitigations beat expensive choices that hide the mechanics.

## Results
A system that costs near-zero to run, retrieves well, demonstrates real AI-Engineer breadth (embeddings, vector search, LLM streaming, security, self-hosted deploy), and is fully under my control end to end — all four goals met simultaneously.

## Lessons Learned
For a portfolio, the *reasoning* behind a stack is worth more than the stack. "I used Voyage because retrieval quality is the ceiling on a RAG bot, and Haiku because the model just has to synthesize faithfully over good context" is a far stronger interview answer than a list of technologies. I built this so I could give those answers honestly, because I actually made those calls.

## Keywords
technical decisions, tradeoffs, Voyage AI, voyage-3-large, embeddings, Claude Haiku, claude-haiku-4-5, LLM selection, ChromaDB, vector database, HNSW, cosine similarity, Caddy, Let's Encrypt, TLS, Hostinger, VPS, self-hosted, Docker, cost optimization, retrieval quality, full control, skill showcase, interview answers, RAG design
