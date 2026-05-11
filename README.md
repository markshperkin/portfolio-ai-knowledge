# portfolio-ai-knowledge

Structured knowledge corpus for Mark's GPT — a RAG-backed AI assistant. Contains Markdown documents about Mark Shperkin's projects, experience, skills, and background. These files are the source of truth the AI draws from when answering questions.

## How It Fits In

This repo feeds the RAG pipeline in `portfolio-ai-backend`. A reindex CLI walks these files, chunks each document, embeds the chunks using Voyage AI `voyage-3-large`, and writes them to a ChromaDB vector store. The backend retrieves relevant chunks at query time and injects them into the LLM prompt.

```
portfolio-ai-knowledge/  →  python -m app.reindex  →  ChromaDB  →  Anthropic Claude Haiku
```

## Directory Structure

```
projects/     # Software projects and side projects
experience/   # Work history and roles
education/    # Degrees and courses
skills/       # Technical skills and tools
papers/       # Research papers and publications
meta/         # About Mark, general bio, career goals
scripts/      # Tooling (frontmatter validator)
clean_data/   # Intermediate processed source data
raw_data/     # Original source documents (PDFs, Word files)
```

## Frontmatter Schema

Every `.md` file (except `README.md` and `INDEX.md`) must have valid YAML frontmatter:

```yaml
---
title: string                                              # required, non-empty
category: project|experience|education|skills|paper|meta  # required
tags: [tag1, tag2]                                        # required, can be []
last_updated: YYYY-MM-DD                                  # required
weight: 1.0                                               # optional, float
---
```

`weight` controls retrieval relevance — default `1.0`; increase for high-signal documents.

## Update Workflow

1. Edit or add `.md` files in the appropriate category directory
2. Include valid frontmatter
3. Push — CI runs the frontmatter linter automatically
4. After merging, trigger a reindex on the backend:

```bash
python -m app.reindex --corpus /path/to/portfolio-ai-knowledge
```

## Validating Frontmatter Locally

```bash
python scripts/validate_frontmatter.py
```

Exits `0` if all files pass. Prints `ERROR: <path>: <reason>` for each failure. CI blocks merges on any failure.
