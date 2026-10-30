#!/usr/bin/env python3
"""Check a small explicitly defined JSON field contract (not full JSON Schema)."""
import argparse
import json
from pathlib import Path

KINDS = {"string", "number", "integer", "boolean", "object", "array", "null"}

def is_kind(value, kind):
    return {
        "string": lambda x: isinstance(x, str),
        "number": lambda x: (isinstance(x, (int, float)) and not isinstance(x, bool)),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "boolean": lambda x: isinstance(x, bool),
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "null": lambda x: x is None,
    }[kind](value)

def check(config_path):
    config_path = Path(config_path).resolve()
    spec = json.loads(config_path.read_text(encoding="utf-8-sig"))
    if not isinstance(spec, dict) or not isinstance(spec.get("fields"), dict) or not spec["fields"]:
        raise ValueError("fields에 검사할 필드를 한 개 이상 지정해야 합니다")
    fields = spec["fields"]
    if any(not isinstance(k, str) or not k or v not in KINDS for k, v in fields.items()):
        raise ValueError("필드 이름 또는 자료형이 올바르지 않습니다")
    required = spec.get("required", list(fields))
    if not isinstance(required, list) or not all(isinstance(x, str) and x in fields for x in required):
        raise ValueError("required는 fields의 이름으로 구성해야 합니다")
    if len(required) != len(set(required)):
        raise ValueError("required에 중복 필드가 있습니다")
    allow_extra = spec.get("allow_extra", True)
    if type(allow_extra) is not bool:
        raise ValueError("allow_extra는 true/false여야 합니다")
    data_path = (config_path.parent / spec["source"]).resolve()
    records = json.loads(data_path.read_text(encoding="utf-8-sig"))
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list) or any(not isinstance(row, dict) for row in records):
        raise ValueError("JSON은 객체 또는 객체 배열이어야 합니다")
    issues = []
    for idx, row in enumerate(records, start=1):
        for name in required:
            if name not in row:
                issues.append({"record": idx, "field": name, "problem": "missing"})
        for name, kind in fields.items():
            if name in row and not is_kind(row[name], kind):
                issues.append({"record": idx, "field": name, "problem": "wrong_type", "expected": kind})
        if not allow_extra:
            for name in row.keys() - fields.keys():
                issues.append({"record": idx, "field": name, "problem": "extra"})
    return {"source": str(data_path), "records_checked": len(records),
            "issues": len(issues), "examples": issues[:20],
            "passed": bool(records) and not issues,
            "notes": ["JSON Schema 표준 전체 기능을 구현한 검증기가 아닙니다.",
                      "검사하지 않은 의미·값 범위·업무 조건은 별도로 확인하세요.",
                      "실제 원시 값은 결과에 출력하지 않습니다."]}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    args = p.parse_args()
    try:
        result = check(args.config)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["passed"] else 1
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        p.exit(2, f"오류: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
