#!/usr/bin/env python3
"""
Unicode Guard for Autonomy Journal
Scans text files for dangerous Unicode characters that could be used for obfuscation.

This includes:
- Zero-width characters (ZWJ, ZWNJ, ZWS)
- Bidirectional text override characters (RLO, LRO, etc.)
- Other invisible or confusable characters
"""
import sys
from pathlib import Path

# Dangerous Unicode characters
DANGEROUS_UNICODE = {
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


def scan_file_for_dangerous_unicode(filepath):
    """
    Scan a file for dangerous Unicode characters.
    Returns list of (line_num, char, char_name, position) tuples.
    """
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for pos, char in enumerate(line):
                    if char in DANGEROUS_UNICODE:
                        violations.append((
                            line_num,
                            repr(char),
                            DANGEROUS_UNICODE[char],
                            pos
                        ))
    except UnicodeDecodeError:
        # File is not UTF-8, skip it
        return []
    except Exception as e:
        print(f"ERROR scanning {filepath}: {e}", file=sys.stderr)
        return []
    
    return violations


def main():
    """Main Unicode guard function."""
    # Scan Python and shell scripts in tools/
    tools_dir = Path('tools')
    
    # Also scan schemas and other important files
    scan_patterns = [
        'tools/*.py',
        'tools/*.sh',
        'schemas/*.json',
        'src/**/*.py',
        '*.md',
    ]
    
    all_clean = True
    files_scanned = 0
    
    for pattern in scan_patterns:
        for filepath in Path('.').glob(pattern):
            if filepath.is_file():
                files_scanned += 1
                violations = scan_file_for_dangerous_unicode(filepath)
                
                if violations:
                    print(f"UNICODE_VIOLATION {filepath}")
                    all_clean = False
                    for line_num, char_repr, char_name, pos in violations:
                        print(f"  Line {line_num}, pos {pos}: {char_name} ({char_repr})")
    
    if all_clean:
        print(f"UNICODE_GUARD_PASS (scanned {files_scanned} files)")
        return 0
    else:
        print("UNICODE_GUARD_FAIL: Dangerous Unicode characters detected")
        return 1


if __name__ == '__main__':
    sys.exit(main())
