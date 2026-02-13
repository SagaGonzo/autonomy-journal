#!/usr/bin/env python3
"""
JSONL Instance Validator
Validates JSONL files against JSON Schema using instance validation.
This validates actual data against schema constraints.
This is fail-closed: exits with code 1 on any failure.
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("JSONL_VALIDATE_FAIL: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

def load_schema(schema_path):
    """Load a JSON schema file."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading schema {schema_path}: {e}")
        return None

def validate_jsonl_file(jsonl_path, schema):
    """Validate a JSONL file against a schema."""
    issues = []
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    instance = json.loads(line)
                except json.JSONDecodeError as e:
                    issues.append(f"Line {line_num}: Invalid JSON - {e}")
                    continue
                
                try:
                    jsonschema.validate(instance=instance, schema=schema)
                except jsonschema.ValidationError as e:
                    issues.append(f"Line {line_num}: Schema validation failed - {e.message}")
                except jsonschema.SchemaError as e:
                    issues.append(f"Line {line_num}: Schema error - {e}")
    
    except Exception as e:
        issues.append(f"File read error: {e}")
    
    return issues

def main():
    """Main instance validation function."""
    # Load the main schema for autonomy journal events
    schema_path = Path('schemas/autonomy_journal.v1.autonomy.schema.json')
    
    if not schema_path.exists():
        print("JSONL_VALIDATE_FAIL")
        print(f"ERROR: Schema file not found: {schema_path}")
        return 1
    
    schema = load_schema(schema_path)
    if schema is None:
        print("JSONL_VALIDATE_FAIL")
        return 1
    
    # Validate JSONL files in proofs directory
    proofs_dir = Path('proofs')
    
    if not proofs_dir.exists():
        print("JSONL_VALIDATE_PASS")
        print("Note: proofs/ directory does not exist, nothing to validate")
        return 0
    
    jsonl_files = list(proofs_dir.glob('*.jsonl'))
    
    if not jsonl_files:
        print("JSONL_VALIDATE_PASS")
        print("Note: No JSONL files found in proofs/")
        return 0
    
    all_valid = True
    for jsonl_file in sorted(jsonl_files):
        issues = validate_jsonl_file(jsonl_file, schema)
        
        if issues:
            print(f"JSONL_VALIDATE_FAIL {jsonl_file.name}:")
            for issue in issues:
                print(f"  {issue}")
            all_valid = False
        else:
            print(f"JSONL_VALIDATE_OK {jsonl_file.name}")
    
    if all_valid:
        print("JSONL_VALIDATE_PASS")
        return 0
    else:
        print("JSONL_VALIDATE_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
