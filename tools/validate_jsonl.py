#!/usr/bin/env python3
"""
JSONL Instance Validator for Autonomy Journal

Validates JSONL files against JSON schemas.
Performs full schema instance validation (not just parsing).
"""
import json
import sys
import argparse
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validators
except ImportError:
    print("ERROR: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

def load_schema(schema_path):
    """Load a JSON schema from file."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        return schema, None
    except Exception as e:
        return None, str(e)

def validate_jsonl_against_schema(jsonl_path, schema):
    """
    Validate a JSONL file against a JSON schema.
    
    Returns (success: bool, violations: list)
    """
    violations = []
    ValidatorClass = validators.validator_for(schema)
    validator = ValidatorClass(schema)
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse JSON
                    obj = json.loads(line)
                    
                    # Validate against schema
                    errors = list(validator.iter_errors(obj))
                    if errors:
                        for error in errors:
                            violations.append({
                                'line': line_num,
                                'path': '.'.join(str(p) for p in error.absolute_path),
                                'message': error.message
                            })
                
                except json.JSONDecodeError as e:
                    violations.append({
                        'line': line_num,
                        'path': 'parse',
                        'message': f"JSON parse error: {e}"
                    })
    
    except Exception as e:
        violations.append({
            'line': 0,
            'path': 'file',
            'message': f"File error: {e}"
        })
    
    return len(violations) == 0, violations

def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description='Validate JSONL files against JSON schemas'
    )
    parser.add_argument(
        '--schema',
        type=str,
        default='schemas/autonomy_journal.v1.autonomy.schema.json',
        help='Path to JSON schema file'
    )
    parser.add_argument(
        '--jsonl',
        type=str,
        nargs='*',
        help='JSONL files to validate (default: proofs/*.jsonl)'
    )
    
    args = parser.parse_args()
    
    print("Running JSONL Instance Validation...")
    
    # Load schema
    schema, error = load_schema(args.schema)
    if error:
        print(f"ERROR: Failed to load schema {args.schema}: {error}")
        print("JSONL_SCHEMA_VALIDATE_FAIL")
        return 1
    
    print(f"Using schema: {args.schema}")
    
    # Determine which JSONL files to validate
    if args.jsonl:
        jsonl_files = [Path(f) for f in args.jsonl]
    else:
        proofs_dir = Path('proofs')
        if not proofs_dir.exists():
            print("WARNING: proofs/ directory not found, nothing to validate")
            print("✓ JSONL_SCHEMA_VALIDATE_PASS")
            return 0
        jsonl_files = sorted(proofs_dir.glob('*.jsonl'))
    
    if not jsonl_files:
        print("WARNING: No JSONL files found to validate")
        print("✓ JSONL_SCHEMA_VALIDATE_PASS")
        return 0
    
    # Validate each file
    all_passed = True
    for jsonl_file in jsonl_files:
        if not jsonl_file.exists():
            print(f"✗ {jsonl_file} - FILE NOT FOUND")
            all_passed = False
            continue
        
        success, violations = validate_jsonl_against_schema(jsonl_file, schema)
        
        if success:
            print(f"✓ {jsonl_file.name} - valid")
        else:
            print(f"✗ {jsonl_file.name} - FAILED")
            for v in violations[:5]:  # Show first 5 violations
                if v['path']:
                    print(f"  Line {v['line']}: {v['path']} - {v['message']}")
                else:
                    print(f"  Line {v['line']}: {v['message']}")
            if len(violations) > 5:
                print(f"  ... and {len(violations) - 5} more violation(s)")
            all_passed = False
    
    # Print final result
    if all_passed:
        print("\n✓ JSONL_SCHEMA_VALIDATE_PASS")
        return 0
    else:
        print("\n✗ JSONL_SCHEMA_VALIDATE_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
