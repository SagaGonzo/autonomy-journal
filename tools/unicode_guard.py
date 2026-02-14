#!/usr/bin/env python3
"""
Unicode Security Guard for Autonomy Journal

Detects hidden/bidirectional Unicode characters that could be used for:
- Visual spoofing (bidi overrides, zero-width chars)
- Parser attacks (NBSP, other whitespace-like chars)

This runs FIRST in CI before any other validation.
"""
import sys
from pathlib import Path

# Dangerous Unicode categories
BIDI_OVERRIDES = [
    "\u202a",  # LEFT-TO-RIGHT EMBEDDING
    "\u202b",  # RIGHT-TO-LEFT EMBEDDING
    "\u202c",  # POP DIRECTIONAL FORMATTING
    "\u202d",  # LEFT-TO-RIGHT OVERRIDE
    "\u202e",  # RIGHT-TO-LEFT OVERRIDE
    "\u2066",  # LEFT-TO-RIGHT ISOLATE
    "\u2067",  # RIGHT-TO-LEFT ISOLATE
    "\u2068",  # FIRST STRONG ISOLATE
    "\u2069",  # POP DIRECTIONAL ISOLATE
]

ZERO_WIDTH = [
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\ufeff",  # ZERO WIDTH NO-BREAK SPACE (BOM)
]

NBSP_LIKE = [
    "\u00a0",  # NO-BREAK SPACE
    "\u202f",  # NARROW NO-BREAK SPACE
    "\u2007",  # FIGURE SPACE
]

ALL_DANGEROUS = BIDI_OVERRIDES + ZERO_WIDTH + NBSP_LIKE


def scan_file(filepath):
    """Scan a single file for dangerous Unicode characters."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [(0, f"READ_ERROR: {e}")]
    
    violations = []
    for line_num, line in enumerate(content.splitlines(), 1):
        for char in ALL_DANGEROUS:
            if char in line:
                char_name = {
                    "\u202a": "LRE", "\u202b": "RLE", "\u202c": "PDF",
                    "\u202d": "LRO", "\u202e": "RLO", "\u2066": "LRI",
                    "\u2067": "RLI", "\u2068": "FSI", "\u2069": "PDI",
                    "\u200b": "ZWSP", "\u200c": "ZWNJ", "\u200d": "ZWJ",
                    "\ufeff": "BOM", "\u00a0": "NBSP", "\u202f": "NNBSP",
                    "\u2007": "FIGURE_SPACE"
                }.get(char, f"U+{ord(char):04X}")
                violations.append((line_num, char_name))
    
    return violations


def main():
    """Scan all tracked files for dangerous Unicode."""
    repo_root = Path(__file__).parent.parent
    
    # Define paths to scan
    paths_to_scan = [
        repo_root / "tools",
        repo_root / "schemas",
        repo_root / "src",
        repo_root / ".github",
    ]
    
    # Also scan specific files
    files_to_scan = [
        "README.md",
        "MISSION.md",
        "PROOFS.md",
        "SECURITY.md",
        "ETHICS.md",
        "CODE_OF_CONDUCT.md",
        "LICENSE",
        "CITATION.cff",
    ]
    
    all_violations = {}
    
    # Scan directories
    for scan_path in paths_to_scan:
        if scan_path.exists():
            for filepath in scan_path.rglob("*"):
                if filepath.is_file() and not filepath.name.startswith('.'):
                    violations = scan_file(filepath)
                    if violations:
                        all_violations[str(filepath.relative_to(repo_root))] = violations
    
    # Scan individual files
    for filename in files_to_scan:
        filepath = repo_root / filename
        if filepath.exists():
            violations = scan_file(filepath)
            if violations:
                all_violations[filename] = violations
    
    # Scan proofs directory if it exists (including .jsonl files)
    proofs_dir = repo_root / "proofs"
    if proofs_dir.exists():
        for filepath in proofs_dir.glob("*.jsonl"):
            violations = scan_file(filepath)
            if violations:
                all_violations[str(filepath.relative_to(repo_root))] = violations
    
    # Report violations
    if all_violations:
        print("UNICODE_GUARD_FAIL")
        print("\nDangerous Unicode characters detected:\n")
        for filepath, violations in sorted(all_violations.items()):
            print(f"{filepath}:")
            for line_num, char_name in violations:
                print(f"  Line {line_num}: {char_name}")
        print("\nThese characters can cause:")
        print("  - Visual spoofing (bidi overrides)")
        print("  - Parser confusion (NBSP, zero-width)")
        print("  - Security vulnerabilities")
        print("\nRemove them before committing.")
        return 1
    
    print("UNICODE_GUARD_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
