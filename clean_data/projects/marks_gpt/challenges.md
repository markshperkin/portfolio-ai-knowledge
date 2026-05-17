# Mark's GPT — Challenges & War Stories

## Summary
The RAG happy path was the easy part. The real engineering was operational: a vector store that went stale inside the running container after every reindex, a free-tier embedding API that rate-limited me mid-rebuild, a CI deploy order that silently wiped fresh indexes, and a VPS layout that corrupted data when I tried to be too clever with branches. These are the bugs that actually taught me something.

## Context
Mark's GPT spans three repos with three CI pipelines feeding one VPS. The corpus is built in one repo, embedded by a CLI in another, and deployed by a third pipeline into shared Docker volumes. That much indirection means the failure modes aren't in the code — they're in the seams between deploys. Every challenge below is a seam bug.

## Challenges & Solutions

### 1. ChromaDB singleton goes stale after reindex
The backend caches the Chroma collection handle in memory (`_collection` in `store.py`). The reindex CLI **deletes and recreates** the collection. So after a reindex, the still-running container is holding a handle to a collection that no longer exists — queries return nothing or error, even though the new index is perfectly fine on disk.

**Solution:** restart the backend container after every reindex (`docker compose restart backend-<env>`) so it rebuilds the handle against the new collection. The fix is trivial; *finding* it meant realizing the bug was in process memory, not in the data.

### 2. Voyage free-tier rate limit (3 RPM)
Voyage's free tier is 3 requests/minute. The corpus is ~183 chunks → 23 embedding batches. My first delay between batches was 21 seconds — too tight. The reindex got most of the way and then died at batch 22 of 23, wasting the whole run.

**Solution:** raised `BATCH_DELAY_SECONDS` to 25. Below ~25s the rolling request rate creeps over 3 RPM near the end of a long run. A reindex takes ~8–10 minutes now, which is fine — it's not a hot path.

### 3. Backend CI deploy wipes a fresh reindex
Natural instinct: update the corpus, reindex, then deploy the backend. Wrong order. A backend CI deploy restarts the container, and the restart blows away the reindex I just ran. I'd reindex, deploy, and find an empty/old index in production with no obvious cause.

**Solution:** always reindex *after* the backend finishes deploying, never before. Deploy order is load-bearing here, which is not obvious until it bites you.

### 4. Two VPS clones, not one with branch switching
I first tried a single VPS clone of the knowledge repo and switched branches (`test`/`prod`) in place. That caused race conditions and wrong data in the Docker volume mounts — whichever branch was checked out last won, regardless of which environment was being served.

**Solution:** two completely separate clones — `/opt/portfolio/knowledge/test/` and `/opt/portfolio/knowledge/prod/` — each pinned to its branch, each volume-mounted into its own environment. No switching, no races.

### 5. CI command timeout hid a successful reindex
The knowledge repo's CI uses drone-ssh (`appleboy/ssh-action`). Its default command timeout is far shorter than a ~10-minute reindex, so CI reported a hard failure even though the reindex had completed successfully on the VPS. A green task showing red.

**Solution:** set `command_timeout: 30m` on the SSH step so CI actually waits for the reindex instead of timing out and lying about the outcome.

## Results
Every one of these is now a known, documented operating procedure: restart after reindex, ≥25s batch delay, reindex-after-deploy, two clones, 30m CI timeout. The system is reliable not because the code is clever but because the seams are understood.

## Lessons Learned
In a multi-repo, multi-deploy system the bugs migrate out of the code and into the *order and state of deploys*. None of these were logic errors — they were "what's cached, what restarts, what runs first" errors. The general lesson: when you split a system across pipelines, draw the data-flow and the restart-flow explicitly, because that diagram is where your real bugs live. Also — a free tier is a real constraint to engineer around, not an inconvenience to ignore.

## Keywords
challenges, war stories, ChromaDB, stale singleton, in-memory cache, collection handle, reindex, Voyage AI rate limit, 3 RPM, batch delay, BATCH_DELAY_SECONDS, CI deploy order, container restart, idempotent reindex, VPS clones, branch isolation, race condition, volume mounts, drone-ssh, command_timeout, debugging, operational engineering, deploy ordering
