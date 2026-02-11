#!/usr/bin/env python3
"""
PII Scanner for Autonomy Journal
Scans JSONL files for personally identifiable information.
"""
import re
import sys
import json
from pathlib import Path

# PII patterns to detect
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
}

def load_allowlist(allowlist_path):
    """Load allowed PII patterns from regex file."""
    if not Path(allowlist_path).exists():
        return []
    with open(allowlist_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def scan_text(text, allowlist_patterns):
    """Scan text for PII, excluding allowlisted patterns."""
    violations = []
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        for match in matches:
            # Check if match is in allowlist
            allowed = False
            for allow_pattern in allowlist_patterns:
                if re.match(allow_pattern, match):
                    allowed = True
                    break
            if not allowed:
                violations.append((pii_type, match))
    return violations

def scan_jsonl_file(filepath, allowlist_patterns):
    """Scan a JSONL file for PII."""
    violations = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                line_violations = scan_text(line, allowlist_patterns)
                if line_violations:
                    violations.append((line_num, line_violations))
    return violations

def main():
    """Main PII scanning function."""
    # Load allowlist
    allowlist_path = Path(__file__).parent / 'pii_allowlist.regex'
    allowlist = load_allowlist(allowlist_path)
    
    # Scan proofs directory if it exists
    proofs_dir = Path('proofs')
    if proofs_dir.exists():
        for jsonl_file in proofs_dir.glob('*.jsonl'):
            violations = scan_jsonl_file(jsonl_file, allowlist)
            if violations:
                print(f"PII_VIOLATIONS_FOUND in {jsonl_file}")
                for line_num, line_violations in violations:
                    for pii_type, match in line_violations:
                        print(f"  Line {line_num}: {pii_type} - {match}")
                return 1
    
    print("PII_SCAN_PASS")
    return 0

if __name__ == '__main__':
    sys.exit(main())
