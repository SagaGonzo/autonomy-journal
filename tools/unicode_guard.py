#!/usr/bin/env python3
"""
Unicode Security Guard for Autonomy Journal
Detects hidden/dangerous Unicode characters in source files.
"""
import sys
import re
from pathlib import Path

# Dangerous Unicode categories to detect
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
    '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE',
    
    # Non-breaking space (sometimes used to hide content)
    '\u00A0': 'NO-BREAK SPACE',
}

def scan_file_for_dangerous_unicode(filepath):
    """Scan a file for dangerous Unicode characters."""
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for char in line:
                    if char in DANGEROUS_UNICODE:
                        violations.append((line_num, char, DANGEROUS_UNICODE[char]))
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        return []
    return violations

def should_scan_file(filepath):
    """Determine if a file should be scanned."""
    # Skip binary/compiled files and common non-text formats
    skip_extensions = {
        '.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
        '.pdf', '.zip', '.tar', '.gz', '.bz2',
        '.mp3', '.mp4', '.avi', '.mov',
        '.woff', '.woff2', '.ttf', '.eot',
    }
    
    # Check extension
    if filepath.suffix.lower() in skip_extensions:
        return False
    
    # Skip common build/dependency directories
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}
    for part in filepath.parts:
        if part in skip_dirs:
            return False
    
    return True

def main():
    """Main scanning function."""
    repo_root = Path.cwd()
    
    # Files to scan: source code, configs, docs, scripts
    scan_patterns = [
        '**/*.py',
        '**/*.sh',
        '**/*.yml',
        '**/*.yaml',
        '**/*.json',
        '**/*.jsonl',
        '**/*.md',
        '**/*.txt',
        '**/*.rst',
        '**/*.toml',
        '**/*.cfg',
        '**/*.ini',
        '**/.*',  # dotfiles
    ]
    
    all_violations = []
    scanned_files = set()
    
    for pattern in scan_patterns:
        for filepath in repo_root.glob(pattern):
            if filepath.is_file() and filepath not in scanned_files:
                if should_scan_file(filepath):
                    scanned_files.add(filepath)
                    violations = scan_file_for_dangerous_unicode(filepath)
                    if violations:
                        all_violations.append((filepath, violations))
    
    if all_violations:
        print("UNICODE_GUARD_FAIL")
        print("\nDangerous Unicode characters detected:")
        for filepath, violations in all_violations:
            print(f"\n{filepath}:")
            for line_num, char, name in violations:
                print(f"  Line {line_num}: U+{ord(char):04X} ({name})")
        return 1
    
    print("UNICODE_GUARD_PASS")
    return 0

if __name__ == '__main__':
    sys.exit(main())
