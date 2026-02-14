#!/usr/bin/env python3
"""
Unicode Guard - Security scanner for hidden/malicious Unicode characters
Detects bidirectional overrides, zero-width characters, and suspicious Unicode.
Exit 1 on detection (fail-closed). Scans all tracked files including .jsonl and dotfiles.
"""
import sys
import re
from pathlib import Path
import subprocess

# Dangerous Unicode categories
BIDI_CHARS = [
    '\u202A',  # LEFT-TO-RIGHT EMBEDDING
    '\u202B',  # RIGHT-TO-LEFT EMBEDDING
    '\u202C',  # POP DIRECTIONAL FORMATTING
    '\u202D',  # LEFT-TO-RIGHT OVERRIDE
    '\u202E',  # RIGHT-TO-LEFT OVERRIDE
    '\u2066',  # LEFT-TO-RIGHT ISOLATE
    '\u2067',  # RIGHT-TO-LEFT ISOLATE
    '\u2068',  # FIRST STRONG ISOLATE
    '\u2069',  # POP DIRECTIONAL ISOLATE
]

ZERO_WIDTH_CHARS = [
    '\u200B',  # ZERO WIDTH SPACE
    '\u200C',  # ZERO WIDTH NON-JOINER
    '\u200D',  # ZERO WIDTH JOINER
    '\uFEFF',  # ZERO WIDTH NO-BREAK SPACE (BOM in middle of file)
]

NBSP_LIKE_CHARS = [
    '\u00A0',  # NO-BREAK SPACE
    '\u1680',  # OGHAM SPACE MARK
    '\u2000',  # EN QUAD
    '\u2001',  # EM QUAD
    '\u2002',  # EN SPACE
    '\u2003',  # EM SPACE
    '\u2004',  # THREE-PER-EM SPACE
    '\u2005',  # FOUR-PER-EM SPACE
    '\u2006',  # SIX-PER-EM SPACE
    '\u2007',  # FIGURE SPACE
    '\u2008',  # PUNCTUATION SPACE
    '\u2009',  # THIN SPACE
    '\u200A',  # HAIR SPACE
    '\u202F',  # NARROW NO-BREAK SPACE
    '\u205F',  # MEDIUM MATHEMATICAL SPACE
    '\u3000',  # IDEOGRAPHIC SPACE
]

ALL_DANGEROUS = BIDI_CHARS + ZERO_WIDTH_CHARS + NBSP_LIKE_CHARS


def get_tracked_files():
    """Get all files tracked by git, including .jsonl and dotfiles."""
    result = subprocess.run(
        ['git', 'ls-files'],
        capture_output=True,
        text=True,
        check=True
    )
    return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]


def scan_file(filepath):
    """
    Scan a file for dangerous Unicode characters.
    Returns list of (line_number, char, char_name, position) tuples.
    """
    violations = []
    char_names = {
        '\u202A': 'LEFT-TO-RIGHT EMBEDDING',
        '\u202B': 'RIGHT-TO-LEFT EMBEDDING',
        '\u202C': 'POP DIRECTIONAL FORMATTING',
        '\u202D': 'LEFT-TO-RIGHT OVERRIDE',
        '\u202E': 'RIGHT-TO-LEFT OVERRIDE',
        '\u2066': 'LEFT-TO-RIGHT ISOLATE',
        '\u2067': 'RIGHT-TO-LEFT ISOLATE',
        '\u2068': 'FIRST STRONG ISOLATE',
        '\u2069': 'POP DIRECTIONAL ISOLATE',
        '\u200B': 'ZERO WIDTH SPACE',
        '\u200C': 'ZERO WIDTH NON-JOINER',
        '\u200D': 'ZERO WIDTH JOINER',
        '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE',
        '\u00A0': 'NO-BREAK SPACE',
        '\u1680': 'OGHAM SPACE MARK',
        '\u2000': 'EN QUAD',
        '\u2001': 'EM QUAD',
        '\u2002': 'EN SPACE',
        '\u2003': 'EM SPACE',
        '\u2004': 'THREE-PER-EM SPACE',
        '\u2005': 'FOUR-PER-EM SPACE',
        '\u2006': 'SIX-PER-EM SPACE',
        '\u2007': 'FIGURE SPACE',
        '\u2008': 'PUNCTUATION SPACE',
        '\u2009': 'THIN SPACE',
        '\u200A': 'HAIR SPACE',
        '\u202F': 'NARROW NO-BREAK SPACE',
        '\u205F': 'MEDIUM MATHEMATICAL SPACE',
        '\u3000': 'IDEOGRAPHIC SPACE',
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                for pos, char in enumerate(line):
                    if char in ALL_DANGEROUS:
                        char_name = char_names.get(char, f'U+{ord(char):04X}')
                        violations.append((line_num, char, char_name, pos))
    except Exception as e:
        # Skip binary files or files that can't be read
        return []
    
    return violations


def main():
    """Main entry point."""
    try:
        tracked_files = get_tracked_files()
    except subprocess.CalledProcessError:
        print("UNICODE_GUARD_FAIL: git ls-files failed (not in a git repo?)")
        return 1
    
    all_violations = {}
    
    for filepath in tracked_files:
        path = Path(filepath)
        if not path.exists():
            continue
        
        violations = scan_file(filepath)
        if violations:
            all_violations[filepath] = violations
    
    if all_violations:
        print("UNICODE_GUARD_FAIL: Hidden Unicode characters detected")
        for filepath, violations in all_violations.items():
            print(f"\n  {filepath}:")
            for line_num, char, char_name, pos in violations:
                print(f"    Line {line_num}, pos {pos}: {char_name} (U+{ord(char):04X})")
        return 1
    
    print("UNICODE_GUARD_PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())
