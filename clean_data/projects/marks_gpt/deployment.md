# Mark's GPT — Deployment & CI/CD

## Summary
All three repos deploy themselves. Push to a `test` or `prod` branch and GitHub Actions takes over: the app repos build Docker images, push to GHCR, and SSH-deploy to a Hostinger VPS behind Caddy; the knowledge repo SSHes in, pulls, and triggers a reindex. It's fully self-hosted — I own the whole pipeline end to end.

## Context
I deliberately self-host instead of using a managed platform. Part of it is cost (no per-seat or per-invocation platform fees), part of it is that owning the entire deploy path — Docker, reverse proxy, TLS, CI — is itself portfolio signal. An AI Engineer who can only run things on someone else's button is half an engineer.

## Technical Details

### App repos (frontend, backend)
Push to `test` or `prod` → GitHub Actions:
- Frontend: runs ESLint + TypeScript check, builds a multi-stage Docker image (Node 20 Alpine), pushes to `ghcr.io/markshperkin/portfolio-ai-frontend:<branch>`, SSH-deploys to the VPS.
- Backend: builds the Docker image, pushes to `ghcr.io/markshperkin/portfolio-ai-backend:<branch>`, SSH-deploys via `docker compose up -d`.

Two environments — `test` and `prod` — run side by side on the VPS from the same compose stack.

### Knowledge repo (this repo)
Only `clean_data/` and `README.md` are tracked in git; `raw_data/` is gitignored and stays local. CI is `appleboy/ssh-action` (drone-ssh): on push to `test` or `prod`, it SSHes to the VPS, `git pull`s in `/opt/portfolio/knowledge/$BRANCH`, then runs the reindex inside the matching backend container:

```
cd /opt/portfolio/knowledge/$BRANCH
git pull
docker compose exec -T backend-$BRANCH python -m app.reindex
```

### VPS layout
- Hostinger VPS, Caddy as reverse proxy (routing + automatic Let's Encrypt TLS).
- `/opt/portfolio/knowledge/test/` and `/opt/portfolio/knowledge/prod/` — **two separate clones**, one per branch.
- docker-compose volume mounts: `./knowledge/test/clean_data:/app/knowledge` and `./knowledge/prod/clean_data:/app/knowledge`.
- `CORPUS_PATH=/app/knowledge` in both `.env.test` and `.env.prod`.

### Why direct SSH instead of cross-repo dispatch
The original idea was knowledge repo → `repository_dispatch` → backend CI → VPS. I chose direct SSH from the knowledge CI instead: fewer moving parts and no personal access token to manage. Simple beats clever for a one-person ops surface.

## Challenges
The deployment is where almost every real bug lived — stale vector collections after reindex, free-tier rate limits, CI deploy order wiping a fresh index, and the need for two separate VPS clones. All four are documented in `challenges.md`. There was also a CI timeout: the drone-ssh step's default command timeout was far shorter than the ~8–10 minute reindex, so it reported failure even though the reindex finished.

## Solutions
- Two clones, not one with branch-switching — eliminates volume-mount race conditions.
- Reindex *after* the backend deploys, never before — a backend deploy restarts the container and would wipe a pre-deploy reindex.
- Bumped the drone-ssh `command_timeout` to 30m so CI waits for the full reindex instead of failing cosmetically.
- Restart the backend container after reindex so it picks up the rebuilt collection (the in-memory ChromaDB handle is otherwise stale).

## Results
- Three independent repos, each with push-to-deploy CI/CD.
- Fully self-hosted: Docker, Caddy, automatic TLS, GHCR images, SSH deploys — no managed platform.
- Test and prod environments isolated on the same VPS, each with its own knowledge clone and corpus path.

## Lessons Learned
Self-hosting taught me more than a managed platform would have — every gotcha (stale singleton, deploy ordering, CI timeouts) was a lesson I only got because I owned the whole path. And the simplest integration that works (direct SSH over cross-repo dispatch) is usually the right one when you're the only operator.

## Keywords
deployment, CI/CD, GitHub Actions, Docker, multi-stage build, GHCR, container registry, Caddy, reverse proxy, Let's Encrypt, TLS, Hostinger, VPS, self-hosted, docker-compose, volume mounts, test environment, prod environment, SSH deploy, appleboy/ssh-action, drone-ssh, command_timeout, reindex, repository_dispatch, branch-per-environment, FastAPI
