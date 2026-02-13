#!/usr/bin/env python3
"""
Meta-validate JSON schemas in ./schemas.
Tokens:
  SCHEMA_CHECK_PASS <file>:<file>:<file>
  SCHEMA_CHECK_FAIL <file> <reason>
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema.validators import validator_for
except ImportError:
    print("SCHEMA_CHECK_FAIL Missing jsonschema library")
    sys.exit(1)


def main() -> int:
    schemas_dir = Path("schemas")
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL schemas/ directory not found")
        return 1

    schema_files = sorted(schemas_dir.glob("*.json"))
    if not schema_files:
        print("SCHEMA_CHECK_FAIL No schema files found in schemas/")
        return 1

    ok = True
    validated_files = []

    for schema_file in schema_files:
        try:
            with open(schema_file, encoding="utf-8") as f:
                schema = json.load(f)

            # Get the appropriate validator class for the schema
            validator_cls = validator_for(schema)
            
            # Check if the schema itself is valid
            validator_cls.check_schema(schema)
            
            validated_files.append(schema_file.name)

        except json.JSONDecodeError as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name} Invalid JSON: {e}")
            ok = False
        except jsonschema.SchemaError as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name} Invalid schema: {e}")
            ok = False
        except Exception as e:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name} {e}")
            ok = False

    if ok:
        files_str = ":".join(validated_files)
        print(f"SCHEMA_CHECK_PASS {files_str}")
    
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
