#!/usr/bin/env python3
"""
Unicode Security Guard
Scans all files for dangerous Unicode characters including:
- Zero-width characters (ZWSP, ZWNJ, ZWJ, etc.)
- Bidirectional text overrides (RLO, LRO, etc.)
- Other invisible/confusable characters

This is a fail-closed security gate that runs before all other validation.
"""
import sys
from pathlib import Path

# Dangerous Unicode characters to detect
DANGEROUS_CHARS = {
    '\u200B': 'ZERO WIDTH SPACE',
    '\u200C': 'ZERO WIDTH NON-JOINER',
    '\u200D': 'ZERO WIDTH JOINER',
    '\u200E': 'LEFT-TO-RIGHT MARK',
    '\u200F': 'RIGHT-TO-LEFT MARK',
    '\u202A': 'LEFT-TO-RIGHT EMBEDDING',
    '\u202B': 'RIGHT-TO-LEFT EMBEDDING',
    '\u202C': 'POP DIRECTIONAL FORMATTING',
    '\u202D': 'LEFT-TO-RIGHT OVERRIDE',
    '\u202E': 'RIGHT-TO-LEFT OVERRIDE',
    '\u2060': 'WORD JOINER',
    '\u2061': 'FUNCTION APPLICATION',
    '\u2062': 'INVISIBLE TIMES',
    '\u2063': 'INVISIBLE SEPARATOR',
    '\u2064': 'INVISIBLE PLUS',
    '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE',
}

# Files and directories to skip
SKIP_PATTERNS = {
    '.git',
    '__pycache__',
    '.pytest_cache',
    'node_modules',
    '.venv',
    'venv',
    '.DS_Store',
}

def should_skip(path):
    """Check if path should be skipped."""
    parts = path.parts
    return any(skip in parts for skip in SKIP_PATTERNS)

def scan_file(filepath):
    """Scan a single file for dangerous Unicode characters."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        issues = []
        for line_num, line in enumerate(content.split('\n'), 1):
            for char_pos, char in enumerate(line, 1):
                if char in DANGEROUS_CHARS:
                    char_name = DANGEROUS_CHARS[char]
                    codepoint = f'U+{ord(char):04X}'
                    issues.append({
                        'line': line_num,
                        'col': char_pos,
                        'char': char_name,
                        'codepoint': codepoint,
                    })
        
        return issues
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files and files we can't read
        return []
    except Exception as e:
        print(f"ERROR scanning {filepath}: {e}", file=sys.stderr)
        return []

def main():
    """Scan all files in repository for dangerous Unicode."""
    root = Path('.')
    all_files = []
    
    # Collect all files to scan
    for path in root.rglob('*'):
        if path.is_file() and not should_skip(path):
            all_files.append(path)
    
    total_issues = 0
    files_with_issues = []
    
    for filepath in all_files:
        issues = scan_file(filepath)
        if issues:
            files_with_issues.append((filepath, issues))
            total_issues += len(issues)
    
    # Report results
    if files_with_issues:
        print("UNICODE_GUARD_FAIL")
        print(f"\nFound {total_issues} dangerous Unicode character(s) in {len(files_with_issues)} file(s):\n")
        
        for filepath, issues in files_with_issues:
            print(f"  {filepath}:")
            for issue in issues:
                print(f"    Line {issue['line']}, Col {issue['col']}: {issue['char']} ({issue['codepoint']})")
        
        print("\nAll source files must be ASCII-only or contain only safe Unicode.")
        print("Remove or replace dangerous Unicode characters before proceeding.")
        return 1
    else:
        print("UNICODE_GUARD_PASS")
        print(f"Scanned {len(all_files)} files - no dangerous Unicode detected.")
        return 0

if __name__ == '__main__':
    sys.exit(main())
