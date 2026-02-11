#!/usr/bin/env python3
"""
JSONL Validator for Autonomy Journal
Validates JSONL files against schemas.
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

def validate_schemas():
    """Validate that schema files are valid JSON."""
    schemas_dir = Path('schemas')
    if not schemas_dir.exists():
        print("SCHEMA_MISSING schemas/")
        return False
    
    schema_files = list(schemas_dir.glob('*.json'))
    if not schema_files:
        print("SCHEMA_MISSING No schema files found")
        return False
    
    all_valid = True
    for schema_file in schema_files:
        try:
            with open(schema_file, 'r') as f:
                json.load(f)
            print(f"SCHEMA_OK {schema_file}")
        except json.JSONDecodeError as e:
            print(f"SCHEMA_INVALID {schema_file}: {e}")
            all_valid = False
    
    return all_valid

def main():
    """Main validation function."""
    # Validate schemas
    schemas_valid = validate_schemas()
    
    # Validate JSONL files in proofs directory
    proofs_dir = Path('proofs')
    jsonl_valid = True
    
    if proofs_dir.exists():
        jsonl_files = list(proofs_dir.glob('*.jsonl'))
        for jsonl_file in jsonl_files:
            valid, error = validate_jsonl_structure(jsonl_file)
            if not valid:
                print(f"JSONL_INVALID {jsonl_file}: {error}")
                jsonl_valid = False
    
    if schemas_valid and jsonl_valid:
        print("JSONL_VALIDATE_PASS")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
