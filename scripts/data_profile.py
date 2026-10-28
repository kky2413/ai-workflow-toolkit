#!/usr/bin/env python3
"""Preview CSV/JSON structure, nulls, and numeric columns without dependencies."""
import argparse
import csv
import io
import json
import math
from collections import Counter
from pathlib import Path


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Text encoding not recognized (tried UTF-8 and CP949)")


def read_records(path: Path) -> tuple[list[dict], str]:
    text = load_text(path)
    if path.suffix.lower() == ".csv":
        if not text.strip():
            return [], "csv"
        sample = text[:8192]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(io.StringIO(text), dialect=dialect)
        if not reader.fieldnames:
            return [], "csv"
        if any(not name for name in reader.fieldnames):
            raise ValueError("CSV has empty header cells")
        records = list(reader)
        if any(None in rec for rec in records):
            raise ValueError("CSV has rows with more fields than header columns")
        return records, "csv"
    if path.suffix.lower() == ".json":
        obj = json.loads(text)
        if isinstance(obj, dict):
            return [obj], "json_object"
        if isinstance(obj, list) and all(isinstance(v, dict) for v in obj):
            return obj, "json_array"
        raise ValueError("JSON must be an object or an array of objects")
    raise ValueError("Only .csv and .json are supported")


def missing(value: object) -> bool:
    return value is None or isinstance(value, str) and not value.strip()


def to_number(value: object) -> float | None:
    if missing(value) or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        val = float(value)
    elif isinstance(value, str):
        try:
            val = float(value.strip().replace(",", ""))
        except ValueError:
            return None
    else:
        return None
    return val if math.isfinite(val) else None


def profile(path: Path, max_rows: int = 100_000) -> dict:
    if max_rows < 1:
        raise ValueError("max_rows must be >= 1")
    rows, file_type = read_records(path)
    truncated = len(rows) > max_rows
    rows = rows[:max_rows]
    names = list(dict.fromkeys(k for r in rows for k in r.keys()))
    if not names and file_type == "csv":
        # Preserve header names for an empty but valid CSV.
        text = load_text(path)
        first = next(csv.reader(io.StringIO(text)), [])
        names = first
    cols = {}
    for name in names:
        values = [r.get(name) for r in rows]
        present = [v for v in values if not missing(v)]
        numeric = [to_number(v) for v in present]
        info = {
            "non_missing": len(present),
            "missing": len(values) - len(present),
            "unique_non_missing": len({json.dumps(v, ensure_ascii=False, sort_keys=True, default=str) for v in present}),
            "sample_values": list(dict.fromkeys(str(v) for v in present))[:5],
        }
        if present and all(n is not None for n in numeric):
            nums = [n for n in numeric if n is not None]
            info["numeric"] = {
                "min": min(nums), "max": max(nums),
                "mean": round(sum(nums) / len(nums), 6),
                "sum": round(sum(nums), 6),
            }
        cols[name] = info
    return {
        "source": str(path.resolve()),
        "format": file_type,
        "rows_profiled": len(rows),
        "truncated": truncated,
        "column_count": len(names),
        "columns": cols,
        "notes": "Statistics describe parsed rows, not domain meaning or data quality.",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", help="Local .csv or .json file")
    p.add_argument("--max-rows", type=int, default=100_000)
    args = p.parse_args()
    try:
        print(json.dumps(profile(Path(args.file), args.max_rows), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        p.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
