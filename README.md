# portfolio-ai-knowledge

Knowledge corpus for Mark's GPT — a RAG-backed portfolio assistant.

## Directory Structure

```
projects/       # Software projects
experience/     # Work history
education/      # Degrees and courses
skills/         # Technical skills
papers/         # Research papers
meta/           # About Mark, career goals
scripts/        # Tooling (lint, etc.)
```

## Update Workflow

1. Add or edit `.md` files in the appropriate category directory
2. Include valid frontmatter (see schema below)
3. Push — CI runs the frontmatter linter automatically
4. After merging, run `python -m app.reindex --corpus /knowledge` on the backend to re-embed

## Frontmatter Schema

Every `.md` file (except `README.md`, `INDEX.md`) must have:

```yaml
---
title: string           # required, non-empty
category: project | experience | education | skills | paper | meta  # required
tags: [tag1, tag2]      # required, can be empty list []
last_updated: YYYY-MM-DD  # required
weight: 1.0             # optional, float, default 1.0
---
```

## Running Lint Locally

```bash
python scripts/validate_frontmatter.py
```

Exits 0 if all files are valid, 1 if any fail with path + reason printed.
