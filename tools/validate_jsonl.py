#!/usr/bin/env python3
"""
Validate JSONL files: parse + JSON Schema instance validation.

Receipt tokens:
  SCHEMA_CHECK_PASS <schema_path>
  JSONL_SCHEMA_VALIDATE_PASS <file>:<line>
  JSONL_SCHEMA_VALIDATE_FAIL <file>:<line> :: <message> @ <json_path>
  JSONL_PARSE_FAIL <file>:<line> :: <message>
"""
import argparse
import json
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema import ValidationError
from jsonschema.validators import validator_for


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="Schema JSON file")
    ap.add_argument("jsonl_files", nargs="+", help="JSONL files to validate")
    args = ap.parse_args()

    schema_path = Path(args.schema)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Validator = validator_for(schema)
    Validator.check_schema(schema)
    print(f"SCHEMA_CHECK_PASS {schema_path.as_posix()}")

    validator = Validator(schema, format_checker=FormatChecker())

    ok = True
    for jsonl_path in args.jsonl_files:
        p = Path(jsonl_path)
        with p.open(encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                s = line.strip()
                if not s:
                    continue
                try:
                    instance = json.loads(s)
                    validator.validate(instance)
                    print(f"JSONL_SCHEMA_VALIDATE_PASS {p.as_posix()}:{line_num}")
                except json.JSONDecodeError as e:
                    ok = False
                    print(f"JSONL_PARSE_FAIL {p.as_posix()}:{line_num} :: {e}")
                except ValidationError as e:
                    ok = False
                    loc = "/".join(str(x) for x in e.absolute_path) or "$"
                    print(
                        f"JSONL_SCHEMA_VALIDATE_FAIL {p.as_posix()}:{line_num} :: {e.message} @ {loc}"
                    )

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
