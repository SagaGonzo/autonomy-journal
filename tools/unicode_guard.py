#!/usr/bin/env python3
"""
Unicode Guard - Detect hidden/bidirectional Unicode characters.
Scans source files including .jsonl and dotfiles for dangerous Unicode.
"""
import sys
import unicodedata
from pathlib import Path
from typing import List, Tuple


DANGEROUS_CATEGORIES = {
    'Cf',  # Format (includes zero-width characters)
    'Cc',  # Control (except newline, tab, carriage return)
}

DANGEROUS_BIDI = {
    '\u202A',  # LEFT-TO-RIGHT EMBEDDING
    '\u202B',  # RIGHT-TO-LEFT EMBEDDING
    '\u202C',  # POP DIRECTIONAL FORMATTING
    '\u202D',  # LEFT-TO-RIGHT OVERRIDE
    '\u202E',  # RIGHT-TO-LEFT OVERRIDE
    '\u2066',  # LEFT-TO-RIGHT ISOLATE
    '\u2067',  # RIGHT-TO-LEFT ISOLATE
    '\u2068',  # FIRST STRONG ISOLATE
    '\u2069',  # POP DIRECTIONAL ISOLATE
}

ALLOWED_CONTROL = {'\n', '\r', '\t'}


def scan_file(path: Path) -> List[Tuple[int, str, str]]:
    """Scan a file for dangerous Unicode characters.
    
    Returns list of (line_number, character, category/type) tuples.
    """
    issues = []
    try:
        content = path.read_text(encoding='utf-8')
        for line_no, line in enumerate(content.splitlines(), start=1):
            for char in line:
                if char in DANGEROUS_BIDI:
                    issues.append((line_no, char, 'BIDI'))
                elif unicodedata.category(char) in DANGEROUS_CATEGORIES:
                    if char not in ALLOWED_CONTROL:
                        issues.append((line_no, char, unicodedata.category(char)))
    except UnicodeDecodeError as e:
        issues.append((0, '', f'DECODE_ERROR: {e}'))
    except Exception as e:
        issues.append((0, '', f'READ_ERROR: {e}'))
    
    return issues


def main() -> int:
    """Scan repository files for dangerous Unicode."""
    # Define file patterns to scan
    patterns = [
        '**/*.py',
        '**/*.sh',
        '**/*.md',
        '**/*.json',
        '**/*.jsonl',
        '**/*.yml',
        '**/*.yaml',
        '**/*.txt',
        '**/.*',  # dotfiles
    ]
    
    # Exclude patterns
    excludes = {
        '.git',
        '__pycache__',
        'node_modules',
        '.venv',
        'venv',
    }
    
    root = Path('.')
    files_to_scan = set()
    
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file() and not any(ex in path.parts for ex in excludes):
                files_to_scan.add(path)
    
    all_ok = True
    files_checked = 0
    
    for path in sorted(files_to_scan):
        issues = scan_file(path)
        if issues:
            all_ok = False
            for line_no, char, cat in issues:
                if line_no == 0:
                    print(f"UNICODE_FAIL {path} {cat}")
                else:
                    char_code = f"U+{ord(char):04X}" if char else "???"
                    print(f"UNICODE_FAIL {path}:{line_no} {char_code} {cat}")
        else:
            files_checked += 1
    
    if all_ok:
        print(f"UNICODE_GUARD_PASS ({files_checked} files)")
        return 0
    else:
        print("UNICODE_GUARD_FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
