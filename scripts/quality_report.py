#!/usr/bin/env python3
"""Generate a Markdown report using explicitly configured sources and metrics."""
import argparse
import json
import re
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

from tabular_io import read_table


OPERATIONS = {'count', 'count_nonmissing', 'sum', 'mean', 'min', 'max'}


def present(value):
    return value is not None and (not isinstance(value, str) or bool(value.strip()))


def as_decimal(value):
    if isinstance(value, bool):
        raise ValueError('불리언은 숫자가 아닙니다')
    text = str(value).strip().replace(',', '')
    if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', text):
        raise ValueError(f'숫자가 아닌 값: {value!r}')
    try:
        num = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f'숫자가 아닌 값: {value!r}') from exc
    if not num.is_finite():
        raise ValueError(f'유효하지 않은 숫자: {value!r}')
    return num


def aggregate(rows, headers, operation, column=None):
    if operation not in OPERATIONS:
        raise ValueError(f'지원하지 않는 연산: {operation}')
    if operation == 'count':
        return Decimal(len(rows))
    if not column or column not in headers:
        raise ValueError(f'해당 열이 없습니다: {column}')
    values = [row.get(column) for row in rows if present(row.get(column))]
    if operation == 'count_nonmissing':
        return Decimal(len(values))
    if not values:
        raise ValueError(f'계산할 숫자 값이 없습니다: {column}')
    nums = [as_decimal(v) for v in values]
    if operation == 'sum':
        return sum(nums, Decimal(0))
    if operation == 'mean':
        return sum(nums, Decimal(0)) / Decimal(len(nums))
    if operation == 'min':
        return min(nums)
    return max(nums)


def pretty(value):
    return format(value.quantize(Decimal('.000001')).normalize(), 'f') if value else '0'


def safe(value):
    return str(value).replace('|', '\|').replace('\r', ' ').replace('\n', ' ')


def generate(spec_path):
    spec_path = Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding='utf-8-sig'))
    if not isinstance(spec, dict) or not isinstance(spec.get('sources'), list) or not spec['sources']:
        raise ValueError('설정에 sources 배열이 필요합니다')
    title = str(spec.get('title') or '데이터 요약 보고서')
    datasets = {}
    for source in spec['sources']:
        name, rel = source['name'], source['path']
        if name in datasets:
            raise ValueError(f'중복된 데이터 이름: {name}')
        path = (spec_path.parent / rel).resolve()
        rows, headers = read_table(path, int(spec.get('max_rows', 100000)), source.get('sheet'))
        datasets[name] = {'rows': rows, 'headers': headers, 'path': path}
    metrics = {}
    lines = [f'# {safe(title)}', '', '## 사용한 데이터', '', '| 이름 | 원본 파일 | 행 수 | 열 수 |', '| --- | --- | ---: | ---: |']
    for name, ds in datasets.items():
        lines.append(f"| {safe(name)} | {safe(ds['path'])} | {len(ds['rows'])} | {len(ds['headers'])} |")
    lines += ['', '## 계산 결과', '', '| 지표 | 계산 방식 | 값 | 단위 |', '| --- | --- | ---: | --- |']
    for metric in spec.get('metrics', []):
        name, operation = metric['name'], metric['operation']
        if name in metrics:
            raise ValueError(f'중복 지표 이름: {name}')
        if operation == 'ratio_percent':
            a, b = metric['numerator'], metric['denominator']
            if a not in metrics or b not in metrics:
                raise ValueError('비율 지표는 앞서 계산된 지표 이름을 참조해야 합니다')
            if metrics[b] == 0:
                raise ValueError('비율의 분모가 0입니다')
            result = metrics[a] / metrics[b] * 100
            method = f'{a} / {b} × 100'
            unit = metric.get('unit', '%')
        else:
            source = metric['source']
            if source not in datasets:
                raise ValueError(f'데이터를 찾을 수 없습니다: {source}')
            ds = datasets[source]
            column = metric.get('column')
            result = aggregate(ds['rows'], ds['headers'], operation, column)
            method = f'{operation}({source}.{column})' if column else f'{operation}({source})'
            unit = metric.get('unit', '')
        metrics[name] = result
        lines.append(f'| {safe(name)} | {safe(method)} | {pretty(result)} | {safe(unit)} |')
    for group in spec.get('groups', []):
        name, source, by = group['name'], group['source'], group['by']
        if source not in datasets:
            raise ValueError(f'데이터를 찾을 수 없습니다: {source}')
        ds = datasets[source]
        if by not in ds['headers']:
            raise ValueError(f'그룹 열을 찾을 수 없습니다: {by}')
        buckets = defaultdict(list)
        for row in ds['rows']:
            label = str(row.get(by) if present(row.get(by)) else '(값 없음)')
            buckets[label].append(row)
        lines += ['', f'## {safe(name)}', '', f'| {safe(by)} | 값 |', '| --- | ---: |']
        for label, rows in sorted(buckets.items()):
            val = aggregate(rows, ds['headers'], group['operation'], group.get('column'))
            lines.append(f'| {safe(label)} | {pretty(val)} |')
    lines += ['', '## 확인 사항', '', '- 표의 값은 설정 파일의 열과 연산을 적용한 결과입니다.', '- 데이터의 업무적 의미, 합격 기준, 통계적 타당성은 별도 확인이 필요합니다.', '- 비율의 분자·분모는 설정 파일에 명시된 지표를 사용합니다.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, help='설정 JSON 경로')
    parser.add_argument('--output', required=True, help='결과 Markdown 파일 경로')
    args = parser.parse_args()
    try:
        result = generate(args.config)
        target = Path(args.output)
        if target.exists():
            raise ValueError(f'기존 파일을 덮어쓸 수 없습니다: {target}')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result, encoding='utf-8')
        print(f'생성 완료: {target}')
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(2, f'오류: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
