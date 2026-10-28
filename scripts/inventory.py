#!/usr/bin/env python3
"""Read-only inventory of a local directory (standard library only)."""
import argparse
import json
from collections import Counter
from pathlib import Path

EXCLUDE = {".git", ".venv", "venv", "node_modules", "__pycache__", ".next"}


def build_inventory(root: Path, max_files: int = 2000) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    files = []
    skipped = 0
    for path in sorted(root.rglob("*")):
        if any(part in EXCLUDE for part in path.relative_to(root).parts):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        if len(files) >= max_files:
            skipped += 1
            continue
        stat = path.stat()
        files.append({
            "path": path.relative_to(root).as_posix(),
            "extension": path.suffix.lower() or "(none)",
            "bytes": stat.st_size,
        })
    return {
        "root": str(root),
        "file_count": len(files),
        "omitted_after_limit": skipped,
        "total_bytes_listed": sum(x["bytes"] for x in files),
        "extensions": dict(sorted(Counter(x["extension"] for x in files).items())),
        "files": files,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", nargs="?", default=".")
    p.add_argument("--max-files", type=int, default=2000)
    args = p.parse_args()
    try:
        if args.max_files <= 0:
            raise ValueError("--max-files must be > 0")
        print(json.dumps(build_inventory(Path(args.folder), args.max_files), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        p.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
