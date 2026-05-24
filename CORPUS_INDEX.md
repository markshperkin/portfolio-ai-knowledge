# Knowledge Corpus Index

This file tracks every source processed into `clean_data/`. Auto-maintained by the `populate-knowledge` skill — each new processing run appends an entry at the top.

---

## 2026-05-24 — Processing Run

Enriched the `profile/` section after a gap analysis flagged it as the thinnest part of the corpus (only 3 files, no personal/human content). Source material was an interactive interview conducted via the `grill-me` skill — not `raw_data/`. The user was asked one branch at a time across personal background, personality/values, hobbies, military service, and learning workflow; answers were synthesized into 5 new first-person files following struct.md's General Template (section names adapted where Challenges/Solutions/Results don't fit a profile topic).

### Profile (1 interview transcript → 5 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| Interactive interview via `grill-me` | Conversation | `clean_data/profile/` | 5 |

Files: `personal_background.md`, `personality_and_values.md`, `interests_and_hobbies.md`, `military_service.md`, `reading_learning.md`.

### Run Summary

- **Total sources processed:** 1 interview (no `raw_data/` input)
- **Total files written:** 5
- **Sections touched:** `profile/`
- **Notes:**
  - `technical_skills_summary.md` was intentionally **skipped** per user — tech stack is already documented per-project and per-experience; consolidating it again would be redundant.
  - `military_service.md` is deliberately light on locations/unit details per user preference; covers the elite-athlete-status duality, communication lessons, and professional carry-over only.
  - `personal_background.md` introduces context that prior files referenced but never defined: wife (American RN, met at USC first class, married Aug 2025), Bukharian Jewish identity, parents' Soviet-immigrant backgrounds (Uzbekistan + Ukraine, both with master's degrees), Russian as home language, current life in Israel.
  - `personality_and_values.md` complements `what_sets_him_apart.md` — that file is the interview-positioning highlight reel; this one is the day-to-day "what is Mark like to work with" version, with concrete anecdotes (USC swim-team driver-seat story) and two quotes that drive his worldview.
  - `interests_and_hobbies.md` fixes the prior impression that the user has no life outside engineering + swimming. Surfaces freediving (20m+ in Eilat), competitive FPS gaming, cooking plov, Israeli/electronic music concerts, and travel.
  - `reading_learning.md` documents the actual learning workflow (LLM → papers → fundamentals from coursework → LLM gap-fill) and the current focus area (agentic AI / LLM pipelines, with Mark's GPT as the live sandbox).
  - `raw_data/` untouched; no git actions taken.

---

## 2026-05-17 — Processing Run

Added the portfolio project itself — **Mark's GPT**, the RAG chatbot that *is* this portfolio — to `clean_data/projects/marks_gpt/`. Not sourced from `raw_data/`: source material was the three repo READMEs (`portfolio-ai-frontend`, `portfolio-ai-backend`, `portfolio-ai-knowledge`), `portfolio-ai-backend/reindexing.md`, and deployment-pipeline facts carried in project memory. User-supplied context confirmed via Q&A: live & public, ~12h solo build, stack driven by cost + quality + skill-showcase + full-control, and approval to document the real deployment war-stories.

### Projects (1 project → 7 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| 3 repo READMEs + reindexing.md + project memory | Markdown / context | `clean_data/projects/marks_gpt/` | 7 |

Files: `overview.md`, `architecture.md`, `rag_pipeline.md`, `security_and_ux.md`, `deployment.md`, `challenges.md`, `tech_decisions.md`.

### Run Summary

- **Total sources processed:** 1 multi-repo project (no `raw_data/` input — README + memory sourced)
- **Total files written:** 7
- **Sections touched:** `projects/`
- **Notes:**
  - Destination `clean_data/projects/marks_gpt/` per struct.md (`projects/` = one subdir per project, focused files per topic).
  - This is a self-referential entry: the corpus now documents the chatbot it feeds.
  - The 5 deployment war-stories in `challenges.md` (stale ChromaDB singleton, Voyage 3 RPM limit, CI-deploy-order wipe, two-clone VPS layout, drone-ssh `command_timeout`) come from prior-session operational memory, approved by the user for inclusion.
  - `tech_decisions.md` written as an explicit interview-prep "why X over Y" reference per the project's portfolio purpose.
  - `raw_data/` untouched; no git actions taken.

---

## 2026-05-16 — Processing Run

Sections processed: `athletics/`, `profile/` (career_goals), `education/`, `experience/`. Research dir skipped per request. Education PDFs (3 eDiploma certs + 2 official transcripts) intentionally skipped — degree/credential data already captured in the curated education markdown; no semester-by-semester transcript ingested per request.

### Athletics (1 source → 6 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| raw_data/athletics/swimming.md | Markdown | `clean_data/athletics/` | 6 |

### Profile (1 source → 2 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| raw_data/career_goals/goals.md | Markdown | `clean_data/profile/` | 2 |

### Education (5 sources → 7 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| raw_data/education/{overview,architecture,projects,challenges,results}.md | Markdown | `clean_data/education/` | 7 |
| raw_data/education/*.pdf (5 transcripts/diplomas) | PDF | — (skipped, redundant) | 0 |

### Experience (15 sources → 14 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| raw_data/experience/rgis/{overview,architecture,projects,challenges,results}.md | Markdown | `clean_data/experience/rgis/` | 6 |
| raw_data/experience/cleanrate/{overview,architecture,projects,challenges,results}.md | Markdown | `clean_data/experience/cleanrate/` | 3 |
| raw_data/experience/USC/{overview,architecture,projects,challenges,results}.md | Markdown | `clean_data/experience/usc/` | 5 |

### Run Summary

- **Total sources processed:** 22 markdown sources (5 education PDFs deliberately skipped as redundant)
- **Total files written:** 29
- **Sections touched:** `athletics/`, `profile/`, `education/`, `experience/`
- **Notes:**
  - `research/` skipped per user request (already processed in the 2026-05-14 run).
  - Education PDFs skipped per user request: 3 are bare eDiploma/eCertificate scans (name/degree/date only, already in `education/overview.md`); the 2 official transcripts' grade data is already captured in `education/coursework.md`. No full semester-by-semester transcript ingested.
  - `athletics/` placed at its own top-level dir (not folded into `misc/`) per user request, overriding struct.md.
  - `career_goals` mapped to `profile/` per struct.md (`profile/career_goals.md` + a `what_sets_him_apart.md` split).
  - `experience/USC/` → `clean_data/experience/usc/` (the USC Teaching Assistant role).
  - Source markdown was rewritten first-person/conversational and split per the General Template; redundancy across files is intentional for RAG chunk retrieval.
  - Smaller engagement (Cleanrate) got 3 files to avoid padding a thin source; richer sources (athletics, education, RGIS) split more granularly.

---

## 2026-05-14 — Initial Processing Run

### Research (4 sources → 44 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| Multi-Task Deep Learning Approach for Segmenting and Classifying Competitive Swimming Activities Using a Single IMU (Mark's master's thesis, 48 pages) | PDF | `clean_data/research/thesis/` | 23 |
| From Heuristics to Neural Nets: Backgammon AI Agents (CSCE 775 paper, 5 pages) | PDF | `clean_data/research/From Heuristics to Neural Nets Backgammon AI/` | 8 |
| Wearable Sensor-Based System for Real-Time Human Activity Recognition (5 pages) | PDF | `clean_data/research/Wearable Sensor-Based System for Real-Time Human Activity Recognition/` | 8 |
| Swimming Pose Estimation (4 pages) | PDF | `clean_data/research/Swimmig Pose Estimation/` | 5 |

### Projects (11 sources → 29 files)

| Source | Type | Destination | Files |
|--------|------|-------------|-------|
| https://github.com/markshperkin/LabelingSoftware | GitHub repo | `clean_data/projects/labeling_software/` | 5 |
| https://github.com/markshperkin/EdgeFaceSearch | GitHub repo | `clean_data/projects/edge_face_search/` | 5 |
| https://github.com/david-eta/fancybear | GitHub repo (USC capstone, Mark co-owner) | `clean_data/projects/fancybear/` | 3 |
| https://github.com/markshperkin/CustomCNNforCIFAR-10 | GitHub repo | `clean_data/projects/custom_cnn_cifar10/` | 2 |
| https://github.com/markshperkin/MNIST | GitHub repo | `clean_data/projects/mnist/` | 2 |
| https://github.com/markshperkin/Game-AI | GitHub repo | `clean_data/projects/game_ai/` | 2 |
| https://github.com/markshperkin/location | GitHub repo | `clean_data/projects/location/` | 2 |
| https://github.com/markshperkin/CameraXApp | GitHub repo | `clean_data/projects/camerax_app/` | 2 |
| https://github.com/markshperkin/MiniPaint | GitHub repo | `clean_data/projects/mini_paint/` | 2 |
| https://github.com/markshperkin/Sensor-Game-Application | GitHub repo | `clean_data/projects/sensor_game/` | 2 |
| https://github.com/markshperkin/shesh-besh | GitHub repo | `clean_data/projects/shesh_besh/` | 2 |

### Run Summary

- **Total sources processed:** 15 (4 research papers + 11 GitHub repos)
- **Total files written:** 73
- **Sections touched:** `research/`, `projects/`
- **Notes:**
  - All 4 research papers are authored by Mark Shperkin (primary/sole author).
  - `fancybear/` files explicitly document Mark's contributions (UI, automated email responses, "leave feedback" page, "leave a comment" page) on a 5-person USC Capstone team.
  - Thesis was split heavily (23 files) — content depth warranted granular splits across the model architecture, training procedure, hyperparameter experiments, and lessons learned.
  - Smaller Android projects (Location, CameraXApp, MiniPaint, Sensor-Game-Application) got 2 files each to avoid padding thin sources.

---
