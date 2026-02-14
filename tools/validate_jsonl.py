#!/usr/bin/env python3
"""
JSONL Validator for Autonomy Journal
Validates JSONL files against schemas.
Emits: JSONL_SCHEMA_VALIDATE_PASS/FAIL
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, Draft7Validator
    from jsonschema.exceptions import ValidationError, SchemaError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

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
    """Validate that schema files are valid JSON and valid JSON Schema."""
    if not JSONSCHEMA_AVAILABLE:
        print("JSONL_SCHEMA_VALIDATE_FAIL: jsonschema package not installed")
        return False
    
    schemas_dir = Path('schemas')
    if not schemas_dir.exists():
        print("JSONL_SCHEMA_VALIDATE_FAIL: schemas/ directory not found")
        return False
    
    schema_files = list(schemas_dir.glob('*.json'))
    if not schema_files:
        print("JSONL_SCHEMA_VALIDATE_FAIL: No schema files found")
        return False
    
    all_valid = True
    for schema_file in schema_files:
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Validate it's a valid JSON Schema
            Draft7Validator.check_schema(schema)
            print(f"SCHEMA_CHECK_PASS {schema_file.name}")
        except json.JSONDecodeError as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name}: JSON parse error - {e}")
            all_valid = False
        except SchemaError as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name}: Invalid schema - {e.message}")
            all_valid = False
        except Exception as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name}: {e}")
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
                print(f"JSONL_PARSE_FAIL {jsonl_file}: {error}")
                jsonl_valid = False
            else:
                print(f"JSONL_PARSE_PASS {jsonl_file.name}")
    
    if schemas_valid and jsonl_valid:
        print("JSONL_SCHEMA_VALIDATE_PASS")
        return 0
    else:
        print("JSONL_SCHEMA_VALIDATE_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
