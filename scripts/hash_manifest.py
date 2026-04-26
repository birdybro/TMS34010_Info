#!/usr/bin/env python3
"""Recompute SHA256 + size for every locally-present file in MANIFEST.csv.

For each row, if `local_path` exists under the repo root, fill or refresh
the `sha256` and `file_size_bytes` columns. Rows pointing at missing files
keep their existing values (or remain blank).

Use Python stdlib only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_CSV = REPO_ROOT / "MANIFEST.csv"
COLS = [
    "title", "device", "category", "date", "publication_number",
    "source_url", "local_path", "sha256", "file_size_bytes",
    "copyright_status", "redistribution_status", "notes",
]


def sha256_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            buf = f.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=MANIFEST_CSV)
    p.add_argument("--write", action="store_true",
                   help="Write changes back to the manifest. "
                        "Without this flag, only print a diff summary.")
    args = p.parse_args()

    if not args.manifest.exists():
        print(f"manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    with args.manifest.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or COLS

    changed = 0
    missing: list[str] = []
    for row in rows:
        local = (row.get("local_path") or "").strip()
        if not local:
            continue
        path = (REPO_ROOT / local).resolve()
        if not path.is_file():
            missing.append(local)
            continue
        sha = sha256_of(path)
        size = path.stat().st_size
        old_sha = (row.get("sha256") or "").strip()
        old_size = (row.get("file_size_bytes") or "").strip()
        if old_sha != sha or old_size != str(size):
            print(f"{'CHG' if old_sha else 'NEW'} {local}")
            print(f"    sha256: {old_sha or '(empty)'} -> {sha}")
            print(f"    size:   {old_size or '(empty)'} -> {size}")
            row["sha256"] = sha
            row["file_size_bytes"] = str(size)
            changed += 1

    print()
    print(f"changed rows: {changed}")
    print(f"missing files (rows skipped): {len(missing)}")
    for m in missing:
        print(f"  - {m}")

    if changed and args.write:
        tmp = args.manifest.with_suffix(args.manifest.suffix + ".tmp")
        with tmp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        tmp.replace(args.manifest)
        print(f"wrote {args.manifest}")
    elif changed:
        print("(re-run with --write to persist changes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
