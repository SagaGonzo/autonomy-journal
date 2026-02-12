#!/usr/bin/env python3
"""
JSONL Validator for Autonomy Journal
Validates JSONL files for syntax and schema conformance.
"""
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def validate_jsonl_structure(filepath, schema=None):
    """Validate that file is proper JSONL format and optionally validate against schema."""
    try:
        line_num = 0
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    instance = json.loads(line)
                    # If schema provided, validate instance against it
                    if schema is not None:
                        try:
                            validate(instance=instance, schema=schema)
                        except ValidationError as ve:
                            return False, f"Line {line_num} schema validation: {ve.message}"
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
    # Validate schemas (syntax only)
    schemas_valid = validate_schemas()
    
    # Load autonomy schema for instance validation
    autonomy_schema = None
    schema_path = Path('schemas/autonomy_journal.v1.autonomy.schema.json')
    if schema_path.exists():
        try:
            with open(schema_path, 'r') as f:
                autonomy_schema = json.load(f)
            print(f"SCHEMA_LOADED {schema_path.name}")
        except Exception as e:
            print(f"SCHEMA_LOAD_ERROR {schema_path.name}: {e}")
            return 1
    
    # Validate JSONL files in proofs directory
    proofs_dir = Path('proofs')
    jsonl_valid = True
    
    if proofs_dir.exists():
        jsonl_files = list(proofs_dir.glob('*.jsonl'))
        for jsonl_file in jsonl_files:
            valid, error = validate_jsonl_structure(jsonl_file, autonomy_schema)
            if not valid:
                print(f"JSONL_INVALID {jsonl_file}: {error}")
                jsonl_valid = False
    
    if schemas_valid and jsonl_valid:
        print("JSONL_VALIDATE_PASS (syntax + schema)")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
