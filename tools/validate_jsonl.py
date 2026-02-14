#!/usr/bin/env python3
"""
JSONL Schema Instance Validator for Autonomy Journal
Validates JSONL files against JSON Schema definitions.
Performs full schema validation, not just JSON parsing.
Fail-closed design: exit 1 on any validation failure.
"""
import sys
import json
import argparse
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validators, Draft7Validator
except ImportError:
    print("JSONL_SCHEMA_VALIDATE_FAIL: jsonschema package not installed")
    print("Run: pip install jsonschema")
    sys.exit(1)


def load_schema(schema_path):
    """Load and validate a JSON Schema file."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Validate the schema itself
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
        
        return schema
    except Exception as e:
        print(f"JSONL_SCHEMA_VALIDATE_FAIL: Could not load schema {schema_path}: {e}")
        sys.exit(1)


def validate_jsonl_against_schema(jsonl_path, schema):
    """
    Validate a JSONL file against a JSON Schema.
    Returns (is_valid, errors_list).
    """
    errors = []
    validator = Draft7Validator(schema)
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    instance = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append((line_num, f"JSON parse error: {e}"))
                    continue
                
                # Validate instance against schema
                validation_errors = list(validator.iter_errors(instance))
                if validation_errors:
                    for error in validation_errors:
                        error_path = '.'.join(str(p) for p in error.path) if error.path else 'root'
                        errors.append((line_num, f"Schema validation error at {error_path}: {error.message}"))
    
    except Exception as e:
        errors.append((0, f"File read error: {e}"))
    
    return len(errors) == 0, errors


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate JSONL files against JSON Schema'
    )
    parser.add_argument(
        'jsonl_files',
        nargs='+',
        help='JSONL files to validate'
    )
    parser.add_argument(
        '--schema',
        required=True,
        help='Path to JSON Schema file'
    )
    
    args = parser.parse_args()
    
    # Load schema
    schema = load_schema(args.schema)
    
    all_valid = True
    
    for jsonl_file in args.jsonl_files:
        jsonl_path = Path(jsonl_file)
        
        if not jsonl_path.exists():
            print(f"JSONL_SCHEMA_VALIDATE_FAIL: File not found: {jsonl_file}")
            all_valid = False
            continue
        
        is_valid, errors = validate_jsonl_against_schema(jsonl_path, schema)
        
        if is_valid:
            print(f"JSONL_SCHEMA_VALIDATE_OK: {jsonl_file}")
        else:
            print(f"JSONL_SCHEMA_VALIDATE_FAIL: {jsonl_file}")
            for line_num, error_msg in errors:
                if line_num > 0:
                    print(f"  Line {line_num}: {error_msg}")
                else:
                    print(f"  {error_msg}")
            all_valid = False
    
    if all_valid:
        print("JSONL_SCHEMA_VALIDATE_PASS")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
