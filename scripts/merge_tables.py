#!/usr/bin/env python3
"""Join two local tabular files on an explicitly named key and export CSV."""
import argparse
import csv
from pathlib import Path

from tabular_io import read_table


def join(left_path, right_path, key, how='left', prefix='right_'):
    if how not in {'left', 'inner'}:
        raise ValueError('how는 left 또는 inner여야 합니다')
    if not prefix:
        raise ValueError('right-prefix를 지정해야 열 이름 충돌을 방지할 수 있습니다')
    left_rows, left_cols = read_table(left_path)
    right_rows, right_cols = read_table(right_path)
    if key not in left_cols or key not in right_cols:
        raise ValueError(f'두 파일 모두 연결 키가 있어야 합니다: {key}')
    new_cols = [prefix + col for col in right_cols if col != key]
    if any(col in left_cols for col in new_cols):
        raise ValueError('접두사를 붙인 열 이름이 왼쪽 파일의 열과 충돌합니다')
    lookup = {}
    for row in right_rows:
        val = row.get(key)
        if val is None or not str(val).strip():
            raise ValueError('오른쪽 파일에 빈 연결 키가 있습니다')
        token = str(val).strip()
        if token in lookup:
            raise ValueError(f'오른쪽 파일에 중복된 연결 키가 있습니다: {token}')
        lookup[token] = row
    results = []
    for row in left_rows:
        val = row.get(key)
        token = str(val).strip() if val is not None else ''
        match = lookup.get(token) if token else None
        if how == 'inner' and match is None:
            continue
        out = dict(row)
        for col in right_cols:
            if col != key:
                out[prefix + col] = match.get(col) if match else ''
        results.append(out)
    return results, left_cols + new_cols


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--left', required=True)
    p.add_argument('--right', required=True)
    p.add_argument('--key', required=True)
    p.add_argument('--how', choices=['left', 'inner'], default='left')
    p.add_argument('--right-prefix', default='right_')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        out = Path(args.output)
        if out.exists():
            raise ValueError(f'기존 파일은 덮어쓰지 않습니다: {out}')
        rows, cols = join(args.left, args.right, args.key, args.how, args.right_prefix)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            writer.writerows(rows)
        print(f'생성 완료: {out} ({len(rows)}행)')
        return 0
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f'오류: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
