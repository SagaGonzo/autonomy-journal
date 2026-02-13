#!/usr/bin/env python3
"""
JSONL Schema Validator for Autonomy Journal
Validates JSONL files against JSON schemas.
Performs full instance validation, not just parsing.
"""
import json
import sys
import argparse
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, validators
except ImportError:
    print("ERROR: jsonschema package not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


def load_schema(schema_path):
    """Load a JSON schema file."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Cannot load schema {schema_path}: {e}")
        return None


def validate_jsonl_against_schema(jsonl_path, schema):
    """
    Validate a JSONL file against a JSON schema.
    Returns (success: bool, errors: list)
    """
    errors = []
    
    try:
        with open(jsonl_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")
                    continue
                
                try:
                    validate(instance=data, schema=schema)
                except ValidationError as e:
                    errors.append(f"Line {line_num}: Schema validation failed - {e.message}")
    except Exception as e:
        errors.append(f"Cannot read file: {e}")
    
    return len(errors) == 0, errors


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description='Validate JSONL files against JSON schemas'
    )
    parser.add_argument(
        '--schema',
        help='Path to JSON schema file (default: auto-detect from schemas/)',
        default=None
    )
    parser.add_argument(
        '--jsonl',
        help='Path to JSONL file or directory (default: proofs/)',
        default='proofs'
    )
    
    args = parser.parse_args()
    
    # Load schema
    if args.schema:
        schema = load_schema(args.schema)
        if schema is None:
            print("JSONL_SCHEMA_VALIDATE_FAIL: Cannot load schema")
            return 1
    else:
        # Auto-detect schema - use autonomy_journal schema
        schema_path = Path('schemas/autonomy_journal.v1.autonomy.schema.json')
        if not schema_path.exists():
            print("JSONL_SCHEMA_VALIDATE_FAIL: Default schema not found")
            return 1
        schema = load_schema(schema_path)
        if schema is None:
            print("JSONL_SCHEMA_VALIDATE_FAIL: Cannot load default schema")
            return 1
    
    # Find JSONL files
    jsonl_path = Path(args.jsonl)
    
    if jsonl_path.is_file():
        jsonl_files = [jsonl_path]
    elif jsonl_path.is_dir():
        jsonl_files = list(jsonl_path.glob('*.jsonl'))
    else:
        print(f"JSONL_SCHEMA_VALIDATE_FAIL: Path not found: {jsonl_path}")
        return 1
    
    if not jsonl_files:
        print(f"JSONL_SCHEMA_VALIDATE_FAIL: No JSONL files found in {jsonl_path}")
        return 1
    
    print(f"Validating {len(jsonl_files)} JSONL file(s) against schema...")
    
    all_valid = True
    for jsonl_file in sorted(jsonl_files):
        success, errors = validate_jsonl_against_schema(jsonl_file, schema)
        
        if success:
            print(f"  ✓ {jsonl_file.name}")
        else:
            print(f"  ✗ {jsonl_file.name}")
            for error in errors:
                print(f"    {error}")
            all_valid = False
    
    if all_valid:
        print("\nJSONL_SCHEMA_VALIDATE_PASS")
        return 0
    else:
        print("\nJSONL_SCHEMA_VALIDATE_FAIL")
        return 1


if __name__ == '__main__':
    sys.exit(main())
