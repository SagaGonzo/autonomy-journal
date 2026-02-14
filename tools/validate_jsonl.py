#!/usr/bin/env python3
"""
JSONL Validator for Autonomy Journal
Validates JSONL files for proper format.
Emits: JSONL_VALIDATE_PASS/FAIL

Note: Schema meta-validation is done separately by check_schemas.py
"""
import json
import sys
from pathlib import Path

def validate_jsonl_structure(filepath):
    """Validate that file is proper JSONL format."""
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    json.loads(line)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Line {line_num}: {str(e)}"
    except Exception as e:
        return False, str(e)

def main():
    """Main validation function."""
    # Validate JSONL files in proofs directory
    proofs_dir = Path('proofs')
    jsonl_valid = True
    
    if proofs_dir.exists():
        jsonl_files = list(proofs_dir.glob('*.jsonl'))
        for jsonl_file in jsonl_files:
            valid, error = validate_jsonl_structure(jsonl_file)
            if not valid:
                print(f"JSONL_PARSE_FAIL {jsonl_file}: {error}")
                jsonl_valid = False
            else:
                print(f"JSONL_PARSE_PASS {jsonl_file.name}")
    
    if jsonl_valid:
        print("JSONL_VALIDATE_PASS")
        return 0
    else:
        print("JSONL_VALIDATE_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
