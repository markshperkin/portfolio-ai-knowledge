#!/usr/bin/env python3
"""Validates YAML frontmatter on all knowledge .md files."""
import re
import sys
from pathlib import Path

SKIP_FILES = {"README.md", "INDEX.md"}
VALID_CATEGORIES = {"project", "experience", "education", "skills", "paper", "meta"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    m = FM_RE.match(text)
    if not m:
        return None
    result: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        # handle inline lists: [a, b, c]
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            result[key] = [v.strip() for v in inner.split(",")] if inner else []
        else:
            result[key] = raw
    return result


def validate_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: missing frontmatter"]

    # title
    if not fm.get("title") or not isinstance(fm["title"], str) or not fm["title"]:
        errors.append(f"{path}: 'title' is required and must be a non-empty string")

    # category
    cat = fm.get("category", "")
    if cat not in VALID_CATEGORIES:
        errors.append(f"{path}: 'category' must be one of {sorted(VALID_CATEGORIES)}, got '{cat}'")

    # tags
    if "tags" not in fm:
        errors.append(f"{path}: 'tags' is required (use [] for empty list)")
    elif not isinstance(fm["tags"], list):
        errors.append(f"{path}: 'tags' must be a list")

    # last_updated
    lu = fm.get("last_updated", "")
    if not DATE_RE.match(str(lu)):
        errors.append(f"{path}: 'last_updated' must be YYYY-MM-DD, got '{lu}'")

    # weight (optional)
    if "weight" in fm:
        try:
            float(fm["weight"])
        except (ValueError, TypeError):
            errors.append(f"{path}: 'weight' must be a number, got '{fm['weight']}'")

    return errors


def main() -> int:
    root = Path(__file__).parent.parent
    errors: list[str] = []
    count = 0

    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        parts = rel.parts
        # skip .github/, scripts/, and named skip-list files
        if parts[0] in {".github", "scripts"}:
            continue
        if md.name in SKIP_FILES:
            continue
        count += 1
        errors.extend(validate_file(md))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print(f"OK: {count} file(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
