#!/usr/bin/env python3
"""Compare two local snapshots by a composite key without exposing row values."""
import argparse
import json
from tabular_io import read_table

def indexed(rows, headers, keys, side):
    if not keys or len(keys) != len(set(keys)) or any(k not in headers for k in keys):
        raise ValueError(f"{side}: 키 열이 없거나 중복됐습니다")
    found = {}
    for idx, row in enumerate(rows, 2):
        vals = [row.get(k) for k in keys]
        if any(x is None or str(x).strip() == "" for x in vals):
            raise ValueError(f"{side}: {idx}번째 데이터 행에 빈 키가 있습니다")
        key = tuple(str(x) for x in vals)
        if key in found:
            raise ValueError(f"{side}: 키 중복, 비교 중단")
        found[key] = row
    return found

def compare(before, after, keys):
    left, lh = read_table(before)
    right, rh = read_table(after)
    if set(lh) != set(rh):
        raise ValueError("열 이름 구성이 다릅니다. 먼저 스키마를 확인하세요")
    a = indexed(left, lh, keys, "이전 파일")
    b = indexed(right, rh, keys, "이후 파일")
    altered = 0
    by_column = {}
    for k in a.keys() & b.keys():
        changed = [col for col in lh if a[k].get(col) != b[k].get(col)]
        if changed:
            altered += 1
            for col in changed:
                by_column[col] = by_column.get(col, 0) + 1
    added, removed = len(b.keys() - a.keys()), len(a.keys() - b.keys())
    return {"identical": bool(left) and bool(right) and not (added or removed or altered), "keys": keys,
            "before_rows": len(left), "after_rows": len(right),
            "added_rows": added, "removed_rows": removed,
            "changed_rows": altered, "unchanged_rows": len(a.keys() & b.keys()) - altered,
            "changed_column_counts": dict(sorted(by_column.items())),
            "notes": ["원본 입력값을 직접 비교합니다. 키·원시 값을 결과에 출력하지 않습니다.",
                      "동일성은 자료형과 표현 방식에 영향을 받을 수 있습니다."]}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("before")
    p.add_argument("after")
    p.add_argument("--keys", required=True)
    args = p.parse_args()
    try:
        result = compare(args.before, args.after, [v.strip() for v in args.keys.split(",")])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["identical"] else 1
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f"오류: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
