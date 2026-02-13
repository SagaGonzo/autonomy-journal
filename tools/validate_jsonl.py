#!/usr/bin/env python3
"""
JSONL Instance Validator for Autonomy Journal
Validates JSONL files against JSON schemas (full instance validation).
"""
import json
import sys
from pathlib import Path
import argparse
import jsonschema

def load_schema(schema_path):
    """Load a JSON schema from file."""
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_jsonl_against_schema(jsonl_path, schema):
    """Validate each line of a JSONL file against a schema."""
    violations = []
    try:
        with open(jsonl_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        obj = json.loads(line)
                        # Validate against schema
                        jsonschema.validate(instance=obj, schema=schema)
                    except json.JSONDecodeError as e:
                        violations.append((line_num, f"JSON parse error: {e}"))
                    except jsonschema.ValidationError as e:
                        violations.append((line_num, f"Schema violation: {e.message}"))
    except Exception as e:
        violations.append((0, f"File read error: {str(e)}"))
    
    return violations

def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description='Validate JSONL files against JSON schemas')
    parser.add_argument('--schema', type=str, 
                       default='schemas/autonomy_journal.v1.autonomy.schema.json',
                       help='Path to JSON schema file')
    parser.add_argument('--jsonl', type=str, nargs='+',
                       help='JSONL files to validate (optional, defaults to proofs/*.jsonl)')
    args = parser.parse_args()
    
    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"JSONL_SCHEMA_VALIDATE_FAIL: Schema not found: {args.schema}")
        return 1
    
    try:
        schema = load_schema(schema_path)
    except Exception as e:
        print(f"JSONL_SCHEMA_VALIDATE_FAIL: Cannot load schema: {e}")
        return 1
    
    # Determine which JSONL files to validate
    if args.jsonl:
        jsonl_files = [Path(f) for f in args.jsonl]
    else:
        # Default: validate all JSONL files in proofs/
        proofs_dir = Path('proofs')
        if not proofs_dir.exists():
            print("JSONL_SCHEMA_VALIDATE_PASS: No proofs/ directory (nothing to validate)")
            return 0
        jsonl_files = list(proofs_dir.glob('*.jsonl'))
        if not jsonl_files:
            print("JSONL_SCHEMA_VALIDATE_PASS: No JSONL files found in proofs/")
            return 0
    
    # Validate each file
    all_valid = True
    for jsonl_file in jsonl_files:
        if not jsonl_file.exists():
            print(f"JSONL_SCHEMA_VALIDATE_FAIL: File not found: {jsonl_file}")
            all_valid = False
            continue
        
        violations = validate_jsonl_against_schema(jsonl_file, schema)
        if violations:
            print(f"JSONL_SCHEMA_VALIDATE_FAIL: {jsonl_file}")
            for line_num, message in violations:
                if line_num > 0:
                    print(f"  Line {line_num}: {message}")
                else:
                    print(f"  {message}")
            all_valid = False
        else:
            print(f"JSONL_SCHEMA_VALIDATE_OK: {jsonl_file}")
    
    if all_valid:
        print("JSONL_SCHEMA_VALIDATE_PASS")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
