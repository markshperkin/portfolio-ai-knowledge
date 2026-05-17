# Mark's GPT — Security & UX

## Summary
Mark's GPT is a public, unauthenticated chatbot wired to a paid LLM API, so it needs guardrails against abuse and cost runaway. It defends with a regex abuse classifier, a per-IP rate limiter, anonymized IP logging, and a retrieval threshold that blocks ungrounded answers. On the UX side it leans into a deliberate terminal aesthetic with a few hidden slash-command Easter eggs.

## Context
Anything public and hooked to a metered API is a target — jailbreak attempts, prompt injection, someone scripting a thousand requests to burn my Anthropic and Voyage quota. I also didn't want to store visitor IPs in the clear just to rate-limit them. So the security model had to be lightweight (this is a portfolio, not a bank) but real.

## Technical Details

### Abuse classifier
Regex-based jailbreak/abuse detection runs before any LLM call. Flagged messages are logged to a SQLite database (via aiosqlite) so I can see attempts. Cheap, synchronous, and it catches the obvious stuff before it costs an API call.

### Rate limiter
Per-IP, in-process limiter. No external store — it lives in the backend process, which is fine for a single-instance deployment. Stops one client from hammering the endpoint and draining the LLM budget.

### IP anonymization
IPs are never stored raw. They're hashed with HMAC-SHA256 using a secret salt (`IP_HASH_SALT`). I can still distinguish clients for rate limiting and abuse logging, but the logs don't hold personal data in the clear.

### Grounded refusal as a safety property
The RAG threshold gate (similarity < 0.30 → refuse) is also a security feature: it stops the model from being talked into answering off-topic or made-up questions. Combined with the persona/guardrail system prompt, the bot stays on the subject of me and declines the rest.

### Terminal aesthetic
The UI is a CLI: green text on a dark `#1c1c1c` background, JetBrains Mono throughout, `>` for user prompts and `$` for assistant responses. There's an ASCII bootup banner (which respects `prefers-reduced-motion`) and a set of suggested starter prompts. Responses render with a typewriter drip effect.

### Slash commands / Easter eggs
A few commands short-circuit the whole RAG pipeline with instant canned responses — no LLM call:
- `whoami` — quick identity blurb
- `/help` — lists what you can do
- `sudo hire-mark` — the hire-me pitch
- `cat resume.pdf` — triggers an `action` SSE event that downloads the résumé

These are both fun and functional: `cat resume.pdf` is the fastest path to my actual résumé, and the joke commands reward anyone who treats it like a real terminal.

## Challenges
Keeping security cheap. Every defense had to run before the LLM call to actually save money, and none of it could need external infrastructure (no Redis, no auth provider) — it's a portfolio, the ops surface has to stay tiny.

## Solutions
Push every guard in front of the expensive call: slash-command short-circuit first, then regex abuse check, then rate limit, *then* embedding and LLM. By the time anything costs money, the request has already survived the cheap filters. IP hashing gave me per-client logic without per-client data retention.

## Results
- A public endpoint that resists casual abuse and runaway cost without any auth or external infra.
- Rate limiting and abuse logging that work on anonymized identifiers.
- A UI that's memorable on purpose — the terminal framing is part of the portfolio statement, and the Easter eggs make people stay and poke at it.

## Lessons Learned
Ordering the pipeline by cost was the key insight: the cheapest checks (commands, regex) run first, the expensive ones (embedding, generation) run last and only if everything before passed. And for a portfolio, a distinctive UI does real work — people remember the terminal that talks back.

## Keywords
security, abuse classifier, jailbreak detection, prompt injection, rate limiting, per-IP, HMAC-SHA256, IP anonymization, SQLite, aiosqlite, cost control, grounded refusal, threshold gate, terminal UI, CLI aesthetic, JetBrains Mono, slash commands, Easter eggs, whoami, sudo hire-mark, cat resume.pdf, typewriter, prefers-reduced-motion, UX
