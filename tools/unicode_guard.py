#!/usr/bin/env python3
"""
Fail if files contain hidden Unicode (bidi, zero-width, NBSP-like).

Tokens:
- UNICODE_GUARD_PASS
- UNICODE_GUARD_FAIL <file1>:<file2>:...:
"""
import sys
import re
from pathlib import Path

# Dangerous Unicode characters to detect
DANGEROUS_UNICODE = {
    # Bidirectional text override characters
    '\u202A': 'LEFT-TO-RIGHT EMBEDDING',
    '\u202B': 'RIGHT-TO-LEFT EMBEDDING',
    '\u202C': 'POP DIRECTIONAL FORMATTING',
    '\u202D': 'LEFT-TO-RIGHT OVERRIDE',
    '\u202E': 'RIGHT-TO-LEFT OVERRIDE',
    '\u2066': 'LEFT-TO-RIGHT ISOLATE',
    '\u2067': 'RIGHT-TO-LEFT ISOLATE',
    '\u2068': 'FIRST STRONG ISOLATE',
    '\u2069': 'POP DIRECTIONAL ISOLATE',
    
    # Zero-width characters
    '\u200B': 'ZERO WIDTH SPACE',
    '\u200C': 'ZERO WIDTH NON-JOINER',
    '\u200D': 'ZERO WIDTH JOINER',
    '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE',
    
    # NBSP-like characters
    '\u00A0': 'NO-BREAK SPACE',
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

def scan_file_for_unicode(filepath):
    """Scan a file for dangerous Unicode characters."""
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='strict') as f:
            for line_num, line in enumerate(f, 1):
                for char in line:
                    if char in DANGEROUS_UNICODE:
                        violations.append({
                            'line': line_num,
                            'char': char,
                            'name': DANGEROUS_UNICODE[char],
                            'codepoint': f'U+{ord(char):04X}'
                        })
    except UnicodeDecodeError:
        # Skip files that aren't valid UTF-8 (likely binary files)
        return []
    except (IOError, OSError):
        # Skip files we can't read (permissions, etc.)
        return []
    
    return violations

def should_scan_file(filepath):
    """Determine if a file should be scanned for Unicode issues."""
    # Skip binary files, git internals, and build artifacts
    skip_patterns = [
        '.git/',
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.so',
        '*.dylib',
        '*.dll',
        '*.exe',
        '*.bin',
        '*.png',
        '*.jpg',
        '*.jpeg',
        '*.gif',
        '*.ico',
        '*.pdf',
        '*.zip',
        '*.tar',
        '*.gz',
        '*.bz2',
        '*.xz',
    ]
    
    filepath_str = str(filepath)
    
    # Check skip patterns
    for pattern in skip_patterns:
        if pattern.startswith('*.'):
            if filepath_str.endswith(pattern[1:]):
                return False
        elif pattern in filepath_str:
            return False
    
    # Only scan text-like files
    return True

def scan_directory(directory='.'):
    """Recursively scan directory for Unicode violations."""
    violations = {}
    root_path = Path(directory)
    
    # Get all files recursively
    for filepath in root_path.rglob('*'):
        if filepath.is_file() and should_scan_file(filepath):
            file_violations = scan_file_for_unicode(filepath)
            if file_violations:
                violations[str(filepath)] = file_violations
    
    return violations

def main():
    """Main Unicode guard function."""
    violations = scan_directory('.')
    
    if violations:
        # Print failures with file list
        failed_files = ':'.join(violations.keys())
        print(f"UNICODE_GUARD_FAIL {failed_files}:")
        print("")
        for filepath, file_violations in violations.items():
            print(f"File: {filepath}")
            for violation in file_violations:
                print(f"  Line {violation['line']}: {violation['name']} ({violation['codepoint']})")
        return 1
    
    print("UNICODE_GUARD_PASS")
    return 0

if __name__ == '__main__':
    sys.exit(main())
