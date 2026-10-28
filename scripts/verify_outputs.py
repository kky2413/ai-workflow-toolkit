#!/usr/bin/env python3
"""Check exact expected local deliverables from a JSON manifest; never uploads."""
import argparse
import json
from pathlib import Path, PurePosixPath


def verify(root: Path, manifest: Path) -> dict:
    root = root.resolve()
    spec = json.loads(manifest.read_text(encoding="utf-8-sig"))
    entries = spec.get("files") if isinstance(spec, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("Manifest must contain a non-empty 'files' array")
    results = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("Each file entry needs a string path")
        rel = entry["path"].replace("\\", "/")
        parts = PurePosixPath(rel)
        if parts.is_absolute() or ".." in parts.parts or not rel or ":" in rel:
            raise ValueError(f"Manifest path must be relative inside root: {rel}")
        min_bytes = entry.get("min_bytes", 0)
        if not isinstance(min_bytes, int) or isinstance(min_bytes, bool) or min_bytes < 0:
            raise ValueError(f"Invalid min_bytes for {rel}")
        target = (root / rel).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"File path escapes root: {rel}")
        exists = target.is_file()
        size = target.stat().st_size if exists else None
        passed = exists and size >= min_bytes
        results.append({"path": rel, "exists": exists, "bytes": size, "min_bytes": min_bytes, "passed": passed})
    return {"root": str(root), "passed": all(x["passed"] for x in results), "checks": results}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".")
    p.add_argument("--manifest", required=True)
    args = p.parse_args()
    try:
        report = verify(Path(args.root), Path(args.manifest))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 1
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        p.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
