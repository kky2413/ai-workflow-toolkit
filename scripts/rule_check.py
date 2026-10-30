#!/usr/bin/env python3
"""Run user-specified numeric threshold rules; no invented standards or data changes."""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from tabular_io import read_table

def number(value):
    if isinstance(value, bool) or value is None or str(value).strip() == "":
        raise ValueError("값 없음")
    try:
        result = Decimal(str(value).replace(",", "").strip())
    except InvalidOperation as exc:
        raise ValueError("숫자 변환 실패") from exc
    if not result.is_finite():
        raise ValueError("유효하지 않은 숫자")
    return result

def check(config):
    config = Path(config).resolve()
    spec = json.loads(config.read_text(encoding="utf-8-sig"))
    if not isinstance(spec, dict) or not isinstance(spec.get("rules"), list) or not spec["rules"]:
        raise ValueError("규칙이 0개면 통과로 판단하지 않습니다")
    source = (config.parent / spec["source"]).resolve()
    rows, headers = read_table(source)
    checks = []
    for rule in spec["rules"]:
        if rule.get("field") not in headers:
            raise ValueError(f"없는 열: {rule.get('field')}")
        if rule.get("direction") not in ("min", "max"):
            raise ValueError("direction은 min 또는 max여야 합니다")
        if type(rule.get("inclusive")) is not bool:
            raise ValueError("inclusive는 true/false로 지정하세요")
        if not isinstance(rule.get("reference"), str) or not rule["reference"].strip():
            raise ValueError("각 규칙에는 실제 근거(reference)가 필요합니다")
        checks.append((rule, number(rule.get("limit"))))
    violations = {str(rule.get("name") or rule["field"]): 0 for rule, _ in checks}
    passed = failed = invalid = 0
    for row in rows:
        row_failed, row_invalid = False, False
        for rule, limit in checks:
            try:
                value = number(row.get(rule["field"]))
                if rule["direction"] == "min":
                    ok = value >= limit if rule["inclusive"] else value > limit
                else:
                    ok = value <= limit if rule["inclusive"] else value < limit
            except ValueError:
                ok, row_invalid = False, True
            if not ok:
                row_failed = True
                violations[str(rule.get("name") or rule["field"])] += 1
        if row_invalid:
            invalid += 1
        elif row_failed:
            failed += 1
        else:
            passed += 1
    return {
        "source": str(source), "rows_checked": len(rows), "rules_checked": len(checks),
        "passed": bool(rows) and not failed and not invalid,
        "result": {"pass": passed, "fail": failed, "invalid": invalid},
        "failed_rule_counts": violations,
        "notes": ["비어 있는 입력은 통과가 아닙니다.",
                  "코드는 지정된 기준만 평가하며 기준의 적절성을 자동 판단하지 않습니다."],
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    try:
        result = check(args.config)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["passed"] else 1
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        ap.exit(2, f"오류: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
