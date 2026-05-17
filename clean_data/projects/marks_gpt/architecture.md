# Mark's GPT — Architecture

## Summary
Mark's GPT is a three-repo system: a Next.js frontend, a FastAPI backend, and a Markdown knowledge corpus. The frontend never talks to the backend directly — it proxies through its own route — and the backend runs a guarded RAG pipeline that ends in a streamed Claude response. Everything between the user and the model is Server-Sent Events.

## Context
I split the system into three repos on purpose. The knowledge corpus changes for completely different reasons than the app code (I add a project; I don't touch the streaming logic), so it gets its own repo and its own deploy. The frontend and backend are separate because they have different runtimes, different CI checks, and different scaling concerns. Clean seams.

## Technical Details

### Request flow (backend)
A chat message hits `POST /api/chat` and runs this pipeline:

1. **Slash command check** — if the message is a command (`whoami`, `/help`, `sudo hire-mark`, `cat resume.pdf`), short-circuit with a canned response. No LLM call.
2. **Abuse classifier** — regex-based jailbreak/abuse detection, logged to SQLite (aiosqlite).
3. **Rate limiter** — per-IP, in-process.
4. **Embed the query** — Voyage AI `voyage-3-large`, 1024 dimensions.
5. **Vector search** — ChromaDB HNSW index, cosine similarity, top-5 chunks.
6. **Threshold gate** — best score < 0.30 → refuse to answer (no grounded context). ≥ 0.30 → proceed. This is the anti-hallucination guard.
7. **Build the system prompt** — persona + guardrails + the retrieved chunks.
8. **Stream Claude Haiku** — `claude-haiku-4-5-20251001`, streamed back as SSE events.

### SSE event protocol
The backend and frontend share an event contract (backend Pydantic models mirrored by frontend TypeScript union types):

| Event | Payload | Meaning |
|---|---|---|
| `retrieval_step` | `{step: "retrieving"\|"searching"\|"synthesizing"}` | Pipeline status for the UI |
| `delta` | `{text}` | A streamed token |
| `citation` | `{sources: [{title}]}` | Which documents grounded the answer |
| `done` | `{}` | Stream complete |
| `error` | `{code, message}` | Error condition |
| `action` | `{action_type: "download"\|"open", url}` | Tells the client to trigger an action (e.g. download résumé) |

### Frontend
Next.js 15 App Router, React 19, strict TypeScript, Tailwind, JetBrains Mono. Key pieces:

- **`ChatStream.tsx`** — the main UI: consumes the SSE stream, manages a drip queue, holds chat state.
- **SSE proxy (`api/chat/route.ts`)** — the browser hits a Next.js route, which proxies the backend stream. The browser never calls the backend directly. Sets `X-Accel-Buffering: no` so no proxy buffers the stream.
- **Drip queue (`drip.ts`)** — renders characters at ~5ms/tick for a typewriter effect. When the queue gets long it batches `ceil(queue.length / 80)` chars per tick so it never falls behind a fast stream. Slash command responses bypass the drip and render instantly.
- **Session storage** — conversation persists across same-tab refreshes, lost on tab close. Matches the stateless backend.
- **Bootup banner** — an ASCII boot animation that respects `prefers-reduced-motion`.

### Knowledge corpus
The third repo holds the source-of-truth Markdown. A reindex CLI in the backend walks it, chunks each doc, embeds via Voyage, and atomically replaces the Chroma collection. Covered in `rag_pipeline.md`.

## Challenges
The architectural friction was state synchronization: the vector store is built from one repo, consumed by another, and deployed by a third pipeline. Keeping those in lockstep across deploys is where the real bugs lived — see `challenges.md`.

## Solutions
The decoupling itself was the solution: the proxy route keeps the backend URL private and buffer-free; the shared SSE event contract keeps frontend and backend in sync; the threshold gate keeps the model honest. Each seam has one job.

## Results
A clean separation where each repo deploys independently, the browser only ever talks to its own origin, and the model only ever answers from retrieved context.

## Lessons Learned
The SSE event contract was worth defining up front — mirroring the backend Pydantic models as frontend TypeScript types meant the stream parser and the server never drifted. If I'd hand-rolled the events ad hoc, the frontend would have broken every time I added an event type.

## Keywords
architecture, RAG pipeline, FastAPI, Next.js, Server-Sent Events, SSE, SSE proxy, ChromaDB, HNSW, cosine similarity, Voyage AI, voyage-3-large, Claude Haiku, threshold gate, anti-hallucination, drip queue, typewriter, three-repo, system prompt, Pydantic, TypeScript, slash commands, session storage
