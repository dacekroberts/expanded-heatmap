"""Re-run every city's pipeline from scratch and diff the regenerated
outputs/ against what is committed at git HEAD.

The deployed app only ever reads outputs/, so outputs/ can silently drift
from what the pipeline would actually produce if a script changes and
nobody re-runs it. This is the check that catches that.

Usage:
    python pipeline/drift_check.py                 # every city
    python pipeline/drift_check.py san_diego       # just one

Exit code 0 = zero drift, 1 = real drift (or a step failed).

Two things it deliberately handles:
- Folium writes a random 32-hex-char id into every element on each save, so
  a raw diff of heatmap.html shows a change on every run. Those ids are
  normalized out before comparing.
- Files are compared as raw bytes, never decoded text: on Windows a text
  decode uses the console codepage and corrupts multi-byte characters
  (em dashes etc.), producing a false diff that has nothing to do with the
  pipeline.

It re-runs against the raw files already in data/<city>/raw/ - it does NOT
re-download. It prints each raw input's size and modified time so a reader
can tell code drift (raw files unchanged, outputs changed) from source
drift (raw files were refreshed since the baseline).
"""

import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLIUM_ID = re.compile(rb"_[0-9a-f]{32}")


def normalize(raw: bytes) -> bytes:
    return FOLIUM_ID.sub(b"_ID", raw)


def git(*args) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def cities_with_pipelines():
    return sorted(
        p.name for p in (ROOT / "pipeline").iterdir()
        if p.is_dir() and any(p.glob("step*.py"))
    )


def show_raw_inputs(city: str):
    raw_dir = ROOT / "data" / city / "raw"
    if not raw_dir.exists():
        print("  (no data/<city>/raw/ - nothing to run against)")
        return
    for f in sorted(raw_dir.iterdir()):
        if f.is_file():
            when = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  raw input: {f.name}  {f.stat().st_size:,} bytes  modified {when}")


def run_steps(city: str) -> bool:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    for step in sorted((ROOT / "pipeline" / city).glob("step*.py")):
        print(f"\n  >> {step.name}")
        proc = subprocess.run(
            [sys.executable, str(step)], cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        for line in proc.stdout.splitlines():
            print(f"     {line}")
        if proc.returncode != 0:
            print(f"     STEP FAILED (exit {proc.returncode})\n{proc.stderr}")
            return False
    return True


def compare_outputs(city: str) -> bool:
    prefix = f"outputs/{city}"
    committed = set(
        git("ls-tree", "-r", "--name-only", "HEAD", prefix).decode("utf-8").split()
    )
    on_disk = {
        p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob("*") if p.is_file()
    } if (ROOT / prefix).exists() else set()

    clean = True
    print(f"\n  outputs/{city} vs HEAD:")
    for path in sorted(committed | on_disk):
        if path not in on_disk:
            print(f"     MISSING now (committed but not regenerated): {path}")
            clean = False
            continue
        current = (ROOT / path).read_bytes()
        if path not in committed:
            print(f"     NEW (not in HEAD): {path}")
            clean = False
            continue
        base = git("show", f"HEAD:{path}")
        if current == base:
            print(f"     identical: {path}")
        elif path.endswith(".html") and normalize(current) == normalize(base):
            print(f"     identical after Folium-id normalization: {path}")
        else:
            print(f"     DRIFT: {path}")
            clean = False
    return clean


def main():
    requested = sys.argv[1:] or cities_with_pipelines()
    all_clean = True
    for city in requested:
        print(f"\n=== {city} ===")
        show_raw_inputs(city)
        if not run_steps(city):
            all_clean = False
            continue
        if not compare_outputs(city):
            all_clean = False

    print("\nRESULT:", "zero drift" if all_clean else "DRIFT or failure - see above")
    print("Compare the step row counts above against the latest baseline entry in DECISIONS.md.")
    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
