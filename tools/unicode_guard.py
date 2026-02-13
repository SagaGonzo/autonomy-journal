#!/usr/bin/env python3
"""
Unicode Guard for Autonomy Journal
Detects hidden or bidirectional Unicode characters in source files.
"""
import sys
from pathlib import Path

# Files and directories to check
CHECK_PATTERNS = [
    '.github/workflows/*.yml',
    '.github/workflows/*.yaml',
    'tools/*.py',
    'tools/*.sh',
    'proofs/*.jsonl',
    'schemas/*.json',
    'PROOFS.md',
    '.gitignore'
]

# Dangerous Unicode ranges and characters
DANGEROUS_CHARS = {
    # Bidirectional text control characters (U+202A to U+202E)
    '\u202A', '\u202B', '\u202C', '\u202D', '\u202E',
    # Zero-width characters
    '\u200B', '\u200C', '\u200D', '\u2060', '\uFEFF',
    # Line/paragraph separators
    '\u2028', '\u2029',
    # Other invisible/formatting characters
    '\u00A0',  # Non-breaking space
    '\u180E',  # Mongolian vowel separator
}

def is_dangerous_char(char):
    """Check if a character is dangerous."""
    if char in DANGEROUS_CHARS:
        return True
    
    code_point = ord(char)
    
    # Bidirectional override and isolate characters (U+202A - U+202E, U+2066 - U+2069)
    if 0x202A <= code_point <= 0x202E or 0x2066 <= code_point <= 0x2069:
        return True
    
    # Zero-width characters
    if code_point in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF):
        return True
    
    # Line and paragraph separators
    if code_point in (0x2028, 0x2029):
        return True
    
    return False

def check_file(filepath):
    """Check a file for dangerous Unicode characters."""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for line_num, line in enumerate(content.splitlines(), 1):
            for char_pos, char in enumerate(line, 1):
                if is_dangerous_char(char):
                    violations.append({
                        'line': line_num,
                        'col': char_pos,
                        'char': repr(char),
                        'code': f'U+{ord(char):04X}'
                    })
    except Exception as e:
        print(f"UNICODE_CHECK_ERROR {filepath}: {e}")
        return None
    
    return violations

def main():
    """Main function."""
    all_violations = {}
    
    # Check each pattern
    for pattern in CHECK_PATTERNS:
        base_path = Path('.')
        
        if '/' in pattern:
            parts = pattern.split('/')
            pattern_path = '/'.join(parts[:-1])
            pattern_glob = parts[-1]
            base_path = Path(pattern_path)
            
            if not base_path.exists():
                continue
            
            files = list(base_path.glob(pattern_glob))
        else:
            files = list(Path('.').glob(pattern))
        
        for filepath in files:
            if filepath.is_file():
                violations = check_file(filepath)
                if violations is not None and len(violations) > 0:
                    all_violations[str(filepath)] = violations
    
    # Report results
    if all_violations:
        print("UNICODE_GUARD_FAIL: Hidden Unicode detected")
        for filepath, violations in all_violations.items():
            print(f"\n{filepath}:")
            for v in violations:
                print(f"  Line {v['line']}, Col {v['col']}: {v['char']} ({v['code']})")
        return 1
    else:
        print("UNICODE_GUARD_PASS")
        return 0

if __name__ == '__main__':
    sys.exit(main())
