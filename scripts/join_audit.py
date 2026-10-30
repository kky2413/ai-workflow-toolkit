#!/usr/bin/env python3
"""Read-only join-cardinality audit; no data rows or identifiers emitted."""
import argparse
import json
from collections import Counter
from tabular_io import read_table

RELATIONS = {"one_to_one", "one_to_many", "many_to_one", "many_to_many"}

def count_keys(rows, headers, keys, label):
    if not keys or len(keys) != len(set(keys)) or any(k not in headers for k in keys):
        raise ValueError(f"{label}: 연결 열이 없거나 중복됐습니다")
    counter = Counter()
    for idx, row in enumerate(rows, 2):
        vals = [row.get(k) for k in keys]
        if any(x is None or str(x).strip() == "" for x in vals):
            raise ValueError(f"{label}: {idx}번째 데이터 행에 빈 연결 키가 있습니다")
        counter[tuple(str(x) for x in vals)] += 1
    return counter

def audit(left_path, right_path, keys, relationship="many_to_one"):
    if relationship not in RELATIONS:
        raise ValueError("알 수 없는 관계 유형")
    left, lc = read_table(left_path)
    right, rc = read_table(right_path)
    a, b = count_keys(left, lc, keys, "왼쪽"), count_keys(right, rc, keys, "오른쪽")
    common, aonly, bonly = a.keys() & b.keys(), a.keys() - b.keys(), b.keys() - a.keys()
    inner = sum(a[k] * b[k] for k in common)
    lmiss = sum(a[k] for k in aonly)
    rmiss = sum(b[k] for k in bonly)
    ld, rd = sum(v > 1 for v in a.values()), sum(v > 1 for v in b.values())
    valid = {"one_to_one": not ld and not rd, "one_to_many": not ld,
             "many_to_one": not rd, "many_to_many": True}[relationship]
    return {
        "valid": bool(valid) and bool(left) and bool(right), "relationship": relationship, "keys": keys,
        "left": {"rows": len(left), "distinct_keys": len(a), "duplicate_key_groups": ld, "unmatched_rows": lmiss},
        "right": {"rows": len(right), "distinct_keys": len(b), "duplicate_key_groups": rd, "unmatched_rows": rmiss},
        "predicted_rows": {"inner": inner, "left": inner + lmiss,
                           "right": inner + rmiss, "full": inner + lmiss + rmiss},
        "notes": ["키를 정규화하거나 중복을 제거하지 않았습니다.",
                  "조인 전후 합계와 고유 개체 수는 업무 정의에 따라 별도로 검증해야 합니다."],
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--left", required=True)
    p.add_argument("--right", required=True)
    p.add_argument("--keys", required=True, help="쉼표로 구분한 키 열 이름")
    p.add_argument("--relationship", choices=sorted(RELATIONS), default="many_to_one")
    args = p.parse_args()
    try:
        result = audit(args.left, args.right, [k.strip() for k in args.keys.split(",")], args.relationship)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["valid"] else 1
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f"오류: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
