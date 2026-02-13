#!/usr/bin/env python3
"""
Unicode Guard - Detect hidden Unicode characters in source files.
Scans for BIDI overrides, zero-width characters, and NBSP-like characters.
Acts as a security gatekeeper in CI.
"""
import sys
from pathlib import Path
import re

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
    '\uFEFF',  # ZERO WIDTH NO-BREAK SPACE (BOM)
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

ALL_DANGEROUS_CHARS = set(BIDI_CHARS + ZERO_WIDTH_CHARS + NBSP_LIKE_CHARS)

# File extensions to scan
SCAN_EXTENSIONS = {
    '.py', '.sh', '.yml', '.yaml', '.json', '.jsonl', '.md', '.txt',
    '.js', '.ts', '.jsx', '.tsx', '.css', '.html', '.xml',
    '.toml', '.ini', '.cfg', '.conf'
}

# Files to always scan (dotfiles)
SCAN_DOTFILES = {
    '.gitignore', '.gitattributes', '.editorconfig', '.dockerignore'
}


def scan_file(filepath):
    """Scan a single file for dangerous Unicode characters."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Binary files are skipped
        return []
    except Exception as e:
        print(f"ERROR: Cannot read {filepath}: {e}")
        return []
    
    violations = []
    for line_num, line in enumerate(content.split('\n'), 1):
        for char_pos, char in enumerate(line, 1):
            if char in ALL_DANGEROUS_CHARS:
                char_name = f"U+{ord(char):04X}"
                if char in BIDI_CHARS:
                    char_type = "BIDI"
                elif char in ZERO_WIDTH_CHARS:
                    char_type = "ZERO_WIDTH"
                else:
                    char_type = "NBSP_LIKE"
                
                violations.append({
                    'file': filepath,
                    'line': line_num,
                    'col': char_pos,
                    'char': char_name,
                    'type': char_type
                })
    
    return violations


def should_scan(filepath):
    """Determine if a file should be scanned."""
    path = Path(filepath)
    
    # Skip .git directory specifically (contains binary data and metadata)
    if '.git' in path.parts:
        return False
    
    # Skip hidden directories that appear after non-hidden directories
    # Example: foo/.hidden/bar.py should be skipped
    # But .github/workflows/ci.yml should be scanned
    seen_nonhidden = False
    for part in path.parts[:-1]:  # Exclude the filename itself
        if part.startswith('.'):
            # If we've seen a non-hidden directory before this, skip
            if seen_nonhidden:
                return False
        else:
            seen_nonhidden = True
    
    # Scan dotfiles
    if path.name in SCAN_DOTFILES:
        return True
    
    # Scan by extension
    return path.suffix in SCAN_EXTENSIONS


def scan_directory(root_path='.'):
    """Recursively scan directory for files."""
    root = Path(root_path)
    all_violations = []
    
    for filepath in root.rglob('*'):
        if filepath.is_file() and should_scan(filepath):
            violations = scan_file(filepath)
            all_violations.extend(violations)
    
    return all_violations


def main():
    """Main entry point."""
    print("Running Unicode Guard...")
    
    violations = scan_directory('.')
    
    if violations:
        print("\nUNICODE_GUARD_FAIL")
        print(f"Found {len(violations)} dangerous Unicode character(s):\n")
        
        for v in violations:
            print(f"  {v['file']}:{v['line']}:{v['col']}")
            print(f"    Type: {v['type']}, Character: {v['char']}")
        
        print("\nThese characters can be used for supply chain attacks.")
        print("Please remove them before committing.")
        return 1
    else:
        print("UNICODE_GUARD_PASS")
        return 0


if __name__ == '__main__':
    sys.exit(main())
