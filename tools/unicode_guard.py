#!/usr/bin/env python3
"""
Unicode Guard - Detects hidden/dangerous Unicode characters in source files.

Scans for:
- Bidirectional override characters (U+202A-U+202E, U+2066-U+2069)
- Zero-width characters (U+200B-U+200D, U+FEFF)
- Non-breaking spaces (U+00A0)

Exits with code 1 if dangerous characters are found.
"""
import sys
import os
from pathlib import Path

# Dangerous Unicode characters to detect
DANGEROUS_UNICODE = {
    # Bidirectional text control characters
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
    '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE (BOM)',
    
    # Non-breaking space
    '\u00A0': 'NON-BREAKING SPACE',
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {
    '.py', '.sh', '.yml', '.yaml', '.json', '.jsonl', '.md', '.txt',
    '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.xml', '.toml',
    '.ini', '.cfg', '.conf', '.env', '.gitignore', '.gitattributes',
}

# Patterns to match dotfiles (without extension)
DOTFILES = {'.gitignore', '.gitattributes', '.editorconfig', '.pylintrc'}

def should_scan_file(filepath):
    """Determine if a file should be scanned."""
    path = Path(filepath)
    
    # Skip .git directory
    if '.git' in path.parts:
        return False
    
    # Scan dotfiles
    if path.name in DOTFILES:
        return True
    
    # Scan files with recognized extensions
    if path.suffix.lower() in SCANNABLE_EXTENSIONS:
        return True
    
    # Scan files without extension if they're likely scripts
    if not path.suffix and path.is_file():
        try:
            with open(path, 'rb') as f:
                first_line = f.readline()
                if first_line.startswith(b'#!'):
                    return True
        except:
            pass
    
    return False

def scan_file(filepath):
    """Scan a single file for dangerous Unicode characters."""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, start=1):
                for char in line:
                    if char in DANGEROUS_UNICODE:
                        violations.append({
                            'file': str(filepath),
                            'line': line_num,
                            'char': char,
                            'name': DANGEROUS_UNICODE[char],
                            'codepoint': f'U+{ord(char):04X}'
                        })
    except Exception as e:
        print(f"WARNING: Could not scan {filepath}: {e}", file=sys.stderr)
    
    return violations

def scan_directory(root_dir='.'):
    """Recursively scan directory for dangerous Unicode characters."""
    all_violations = []
    root_path = Path(root_dir)
    
    for item in root_path.rglob('*'):
        if item.is_file() and should_scan_file(item):
            violations = scan_file(item)
            all_violations.extend(violations)
    
    return all_violations

def main():
    """Main entry point."""
    print("Running Unicode Guard...")
    
    violations = scan_directory('.')
    
    if violations:
        print("\n❌ UNICODE_GUARD_FAIL")
        print(f"\nFound {len(violations)} dangerous Unicode character(s):\n")
        
        for v in violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Character: {v['name']} ({v['codepoint']})")
        
        print("\nThese characters can be used for supply chain attacks or cause")
        print("unexpected behavior. Please remove them from the source files.")
        return 1
    else:
        print("✓ UNICODE_GUARD_PASS")
        return 0

if __name__ == '__main__':
    sys.exit(main())
