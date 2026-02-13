#!/usr/bin/env python3
from pathlib import Path

BIDI = {"\u202A", "\u202B", "\u202D", "\u202E", "\u202C", "\u2066", "\u2067", "\u2068", "\u2069"}
ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\ufeff"}
NBSP_LIKE = {"\u00a0", "\u202f", "\u2007"}

EXTS = {".py", ".sh", ".yml", ".yaml", ".md", ".json", ".jsonl", ".toml", ".txt"}
NAMES = {".gitignore", ".gitattributes", ".dockerignore", ".editorconfig"}

SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "dist", "build",
    ".mypy_cache", ".pytest_cache", ".ruff_cache",
}

def main() -> int:
    ok = True
    for p in Path(".").rglob("*"):
        if p.is_dir() or any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name not in NAMES and p.suffix not in EXTS:
            continue

        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except Exception:
            ok = False
            print(f"UNICODE_GUARD_FAIL UTF8 {p.as_posix()}")
            continue

        for chset, name in [(BIDI, "BIDI"), (ZERO_WIDTH, "ZERO_WIDTH"), (NBSP_LIKE, "NBSP")]:
            if any(c in text for c in chset):
                ok = False
                print(f"UNICODE_GUARD_FAIL {name} {p.as_posix()}")

    if ok:
        print("UNICODE_GUARD_PASS")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
