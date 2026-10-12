"""Check the Travel map packs against MANIFEST.csv (SHA-256 and byte size).

    python scripts/verify_manifest.py <upload folder>            # the local files
    python scripts/verify_manifest.py <upload folder> --remote   # also what the public host serves

The upload folder holds MANIFEST.csv and packs/*.pmtiles and lives outside
the repository. Local mode proves the local files match the manifest; with
an upload tool's own bucket-against-folder check, that proves the bucket
matches the manifest. --remote downloads every pack from HOST (about 2.2 GB)
and hashes the served bytes.

Not a pipeline step and never run by a check: --remote is the only part
that uses the network, and only when asked. Holds no credential; the upload
tool's configuration stays outside the repository. HOST is the same address
as pipeline/travel_packs.py's PACK_HOST. Standard library only.
"""

import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

HOST = "https://files.dacekroberts.dev"
CHUNK = 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def sha256_url(url: str) -> tuple[str, int]:
    req = urllib.request.Request(url, headers={"User-Agent": "manifest-check/1.0"})
    h = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(req, timeout=120) as resp:
        for block in iter(lambda: resp.read(CHUNK), b""):
            h.update(block)
            size += len(block)
    return h.hexdigest(), size


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1])
    remote = "--remote" in sys.argv[2:]
    manifest = root / "MANIFEST.csv"
    if not manifest.is_file():
        print(f"MANIFEST.csv not found in {root}")
        return 2

    with manifest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    listed = {r["pack"].replace("\\", "/") for r in rows}
    on_disk = {p.relative_to(root).as_posix() for p in (root / "packs").glob("*.pmtiles")}

    problems = 0
    for name in sorted(on_disk - listed):
        print(f"NOT IN MANIFEST : {name}")
        problems += 1
    for name in sorted(listed - on_disk):
        print(f"MISSING ON DISK : {name}")
        problems += 1

    for i, r in enumerate(rows, 1):
        rel = r["pack"].replace("\\", "/")
        want_hash = r["sha256"].strip().lower()
        want_size = int(r["bytes"])
        local = root / rel
        if local.is_file():
            if local.stat().st_size != want_size:
                print(f"SIZE MISMATCH   : {rel} (local {local.stat().st_size}, manifest {want_size})")
                problems += 1
            elif sha256_file(local) != want_hash:
                print(f"HASH MISMATCH   : {rel} (local)")
                problems += 1
        if remote:
            try:
                got_hash, got_size = sha256_url(f"{HOST}/{rel}")
                if got_size != want_size or got_hash != want_hash:
                    print(f"REMOTE MISMATCH : {rel} (served {got_size} bytes)")
                    problems += 1
            except Exception as e:  # noqa: BLE001
                print(f"REMOTE ERROR    : {rel} ({e})")
                problems += 1
        if i % 25 == 0:
            print(f"  ...checked {i}/{len(rows)}")

    print()
    print(f"Manifest rows: {len(rows)}   Packs on disk: {len(on_disk)}   Remote check: {'yes' if remote else 'no'}")
    print("RESULT: all match" if problems == 0 else f"RESULT: {problems} problem(s)")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
