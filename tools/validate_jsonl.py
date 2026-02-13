#!/usr/bin/env python3
"""
Validate JSONL instances against a JSON Schema (Draft inferred from $schema).
Default schema: schemas/autonomy_journal.v1.autonomy.schema.json
Default files: proofs/*.jsonl
"""
import argparse
import json
from pathlib import Path

from jsonschema import validators


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_jsonl(path: Path):
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        yield i, json.loads(line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--schema",
        default="schemas/autonomy_journal.v1.autonomy.schema.json",
        help="Path to JSON Schema file",
    )
    ap.add_argument(
        "files",
        nargs="*",
        help="JSONL files to validate. If omitted, uses proofs/*.jsonl",
    )
    args = ap.parse_args()

    ok = True
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"SCHEMA_FILE_MISSING {schema_path}")
        return 1

    try:
        schema = load_json(schema_path)
    except Exception as e:
        print(f"SCHEMA_JSON_PARSE_FAIL {schema_path} {e}")
        return 1

    try:
        ValidatorCls = validators.validator_for(schema)
        ValidatorCls.check_schema(schema)
        validator = ValidatorCls(schema)
        print(f"SCHEMA_CHECK_PASS {schema_path.name} ({ValidatorCls.__name__})")
    except Exception as e:
        print(f"SCHEMA_CHECK_FAIL {schema_path.name} {e}")
        return 1

    files = [Path(p) for p in args.files] if args.files else sorted(Path("proofs").glob("*.jsonl"))
    if not files:
        print("JSONL_NO_FILES (nothing to validate)")
        return 0

    for p in files:
        if not p.exists():
            ok = False
            print(f"JSONL_MISSING {p}")
            continue
        try:
            for line_no, obj in iter_jsonl(p):
                # full instance validation
                validator.validate(obj)
            print(f"JSONL_SCHEMA_VALIDATE_PASS {p.name}")
        except Exception as e:
            ok = False
            print(f"JSONL_SCHEMA_VALIDATE_FAIL {p.name} {e}")

    if ok:
        print("JSONL_VALIDATE_PASS")
        return 0
    else:
        print("JSONL_VALIDATE_FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
