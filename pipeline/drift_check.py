"""Re-run every city's pipeline from scratch and diff the regenerated
outputs/ against what is committed at git HEAD.

The deployed app only ever reads outputs/, so outputs/ can silently drift
from what the pipeline would actually produce if a script changes and
nobody re-runs it. This is the check that catches that.

Usage:
    python pipeline/drift_check.py                 # every city
    python pipeline/drift_check.py san_diego       # just one
    python pipeline/drift_check.py --changed       # only the cities your
                                                   #   changes can affect
    python pipeline/drift_check.py --changed --list    # show them, run nothing
    python pipeline/drift_check.py --since HEAD~3  # cities affected since a ref

Exit code 0 = zero drift, 1 = real drift (or a step failed).

--changed exists because the full sweep is O(number of cities) on a gate
that is supposed to run after every pipeline change, and the project keeps
adding cities. It maps changed files to the cities they can actually reach:

    pipeline/<city>/**        -> that city
    outputs/<city>/**         -> that city
    pipeline/taxonomies/<t>.py-> every city whose config sets
                                 TAXONOMY_SYSTEM = "<t>"
    anything else in pipeline/-> every city (map_common.py, theme.py and
                                 taxonomies/__init__.py are shared by all)

It is deliberately conservative: a shared file means the full sweep, because
a wrong "nothing to do" here is invisible until a deploy shows stale output.
--changed is the fast gate for ordinary work; the unfiltered sweep is still
what you run before a deploy or when recording a baseline in DECISIONS.md.

Two things it deliberately handles:
- Folium writes a random 32-hex-char id into every element on each save, so
  a raw diff of heatmap.html shows a change on every run. Those ids are
  normalized out before comparing.
- Files are compared as raw bytes, never decoded text: on Windows a text
  decode uses the console codepage and corrupts multi-byte characters
  (em dashes etc.), producing a false diff that has nothing to do with the
  pipeline.
- Line endings are normalized (CRLF -> LF) on both sides, at byte level. On
  Windows with core.autocrlf, pandas writes CRLF but git stores LF, so a
  regenerated CSV would otherwise always look like drift. Git normalizes the
  same way on commit, so this matches what actually gets committed.

It re-runs against the raw files already in data/<city>/raw/ - it does NOT
re-download. It prints each raw input's size and modified time so a reader
can tell code drift (raw files unchanged, outputs changed) from source
drift (raw files were refreshed since the baseline).

`--jobs N` runs CITIES concurrently (default 1, unchanged). The full sweep is
this project's only O(n)-in-pipeline-runs cost, so it is the binding
operational limiter as the city count grows - see
`docs/scaling_thresholds.md`. Steps WITHIN a city stay sequential, because
step 2 consumes step 1's output; the parallelism is strictly across cities,
which is safe since each touches only its own `data/<city>/` and
`outputs/<city>/`, and the one shared call (`git ls-tree`) is read-only and
takes no index lock. Opt-in rather than default because four cities' step 2
means four geopandas datasets resident at once.
"""

import concurrent.futures
import datetime
import io
import os
import re
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLIUM_ID = re.compile(rb"_[0-9a-f]{32}")


def normalize_eol(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n")


def normalize(raw: bytes) -> bytes:
    return FOLIUM_ID.sub(b"_ID", normalize_eol(raw))


def git(*args) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def cities_with_pipelines():
    return sorted(
        p.name for p in (ROOT / "pipeline").iterdir()
        if p.is_dir() and any(p.glob("step*.py"))
    )


def taxonomy_of(city: str) -> str | None:
    """Which taxonomy system a city's config declares, or None."""
    config = ROOT / "pipeline" / city / "config.py"
    if not config.exists():
        return None
    m = re.search(r'^TAXONOMY_SYSTEM\s*=\s*["\']([^"\']+)', config.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else None


def changed_paths(ref: str) -> list[str]:
    """Repo-relative paths differing from `ref`, including untracked files."""
    tracked = git("diff", "--name-only", ref).decode("utf-8").split()
    untracked = git("ls-files", "--others", "--exclude-standard").decode("utf-8").split()
    return sorted(set(tracked) | set(untracked))


def cities_affected(paths, all_cities) -> tuple[set, list]:
    """Map changed paths to the cities they can reach. Returns (cities, why)."""
    affected, why = set(), []
    for path in paths:
        parts = path.split("/")
        if parts[0] == "outputs" and len(parts) > 1 and parts[1] in all_cities:
            affected.add(parts[1])
            why.append(f"{path} -> {parts[1]}")
        elif parts[0] != "pipeline" or len(parts) < 2:
            continue
        elif parts[1] in all_cities:
            affected.add(parts[1])
            why.append(f"{path} -> {parts[1]}")
        elif parts[1] == "taxonomies" and len(parts) > 2 and parts[2] != "__init__.py":
            system = parts[2].removesuffix(".py")
            hit = {c for c in all_cities if taxonomy_of(c) == system}
            affected |= hit
            why.append(f"{path} -> {', '.join(sorted(hit)) or 'no city uses it'}")
        elif parts[-1] == "drift_check.py":
            why.append(f"{path} -> (this script; affects no output)")
        else:
            affected |= set(all_cities)
            why.append(f"{path} -> SHARED, every city")
    return affected, why


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
        current = normalize_eol((ROOT / path).read_bytes())
        if path not in committed:
            print(f"     NEW (not in HEAD): {path}")
            clean = False
            continue
        base = normalize_eol(git("show", f"HEAD:{path}"))
        if current == base:
            print(f"     identical: {path}")
        elif path.endswith(".html") and normalize(current) == normalize(base):
            print(f"     identical after Folium-id normalization: {path}")
        else:
            print(f"     DRIFT: {path}")
            clean = False
    return clean


def resolve_changed(ref: str, all_cities) -> list:
    paths = changed_paths(ref)
    touches_pipeline = any(p.startswith(("pipeline/", "outputs/")) for p in paths)
    if ref == "HEAD" and not touches_pipeline:
        # Nothing uncommitted reaches the pipeline. The usual reason is that the
        # change was just committed - which is exactly when "commit after each
        # green step" says to run this - so look one commit back rather than
        # reporting nothing to do and being trusted.
        try:
            paths = changed_paths("HEAD~1")
            print("  nothing uncommitted touches pipeline/ - falling back to HEAD~1")
        except subprocess.CalledProcessError:
            return []
    cities, why = cities_affected(paths, all_cities)
    for line in why:
        print(f"  {line}")
    return sorted(cities)


def main():
    args = sys.argv[1:]
    list_only = "--list" in args
    args = [a for a in args if a != "--list"]

    # --jobs N runs CITIES concurrently. Default 1, i.e. exactly the old
    # behaviour on the default path - see the note at the parallel branch for
    # why the default was not flipped.
    jobs = 1
    if "--jobs" in args:
        i = args.index("--jobs")
        if i + 1 >= len(args) or not args[i + 1].isdigit() or int(args[i + 1]) < 1:
            sys.exit("--jobs needs a positive integer, e.g. --jobs 4")
        jobs = int(args[i + 1])
        del args[i:i + 2]

    all_cities = cities_with_pipelines()
    ref = None
    if "--changed" in args:
        args.remove("--changed")
        ref = "HEAD"
    if "--since" in args:
        i = args.index("--since")
        ref = args[i + 1] if i + 1 < len(args) else "HEAD"
        del args[i:i + 2]

    if ref is not None:
        print(f"=== cities affected by changes vs {ref} ===")
        requested = resolve_changed(ref, all_cities)
        if not requested:
            print("\nRESULT: no city's pipeline can be affected - nothing to check.")
            sys.exit(0)
        print(f"\n  -> checking {len(requested)} of {len(all_cities)}: {', '.join(requested)}")
    else:
        requested = args or all_cities

    unknown = [c for c in requested if c not in all_cities]
    if unknown:
        sys.exit(f"No pipeline for: {', '.join(unknown)}")

    if list_only:
        print("\n".join(requested))
        sys.exit(0)

    all_clean = True
    if jobs == 1:
        # The default path, unchanged: print straight to stdout as it goes, so
        # a long sweep shows progress and the output is byte-identical to what
        # this script has always produced.
        for city in requested:
            print(f"\n=== {city} ===")
            show_raw_inputs(city)
            if not run_steps(city):
                all_clean = False
                continue
            if not compare_outputs(city):
                all_clean = False
    else:
        # --jobs N: cities run concurrently. Safe because each city touches only
        # its own data/<city>/ and outputs/<city>/, and the only shared call is
        # `git ls-tree`, which is read-only and takes no index lock. The STEPS
        # WITHIN a city stay sequential - step 2 consumes step 1's output - so
        # the parallelism is strictly across cities.
        #
        # Threads rather than processes: the work is `subprocess.run`, which
        # releases the GIL while it waits, so threads get the full speedup with
        # no pickling and no re-import of the module per worker.
        #
        # Each city's output is buffered and printed as ONE block, in the
        # requested order rather than the completion order. Interleaved prints
        # from concurrent cities would make the report unreadable, and worse,
        # would attach a step's row counts to the wrong city.
        # WHY THE DEFAULT IS STILL 1. The full sweep is the pre-deploy gate and
        # the only part of this project whose cost is O(n) in PIPELINE RUNS
        # rather than file comparisons - which makes it the binding operational
        # limiter as the city count grows (docs/scaling_thresholds.md). Running
        # cities concurrently fixes that. It is opt-in anyway because each
        # city's step 2 loads a full business dataset through geopandas, and
        # four of those at once is four times the peak memory: New York's is the
        # largest, so --jobs 4 on a small machine can swap or be killed, and a
        # killed sweep before a deploy is worse than a slow one. Raise it
        # deliberately: --jobs 4 is a reasonable pre-deploy setting on a machine
        # with room, and the default stays the one that always works.
        print(f"\n(running {len(requested)} cities with --jobs {jobs}; "
              "each city's report is printed as a block when it finishes)")

        # A THREAD-LOCAL stdout proxy, installed once. Swapping `sys.stdout`
        # per worker instead would be a race: it is one global, so two threads
        # assigning it concurrently clobber each other and a city's step row
        # counts end up printed under a different city's heading - which is
        # worse than no parallelism, because it looks fine.
        real_stdout = sys.stdout

        class _PerThreadOut:
            def __init__(self):
                self._local = threading.local()

            def _target(self):
                return getattr(self._local, "buf", None) or real_stdout

            def bind(self, buf):
                self._local.buf = buf

            def write(self, s):
                return self._target().write(s)

            def flush(self):
                return self._target().flush()

        proxy = _PerThreadOut()

        def one_city(city: str):
            buf = io.StringIO()
            proxy.bind(buf)          # touches only THIS thread's local
            print(f"\n=== {city} ===")
            show_raw_inputs(city)
            ok = run_steps(city) and compare_outputs(city)
            return city, ok, buf.getvalue()

        sys.stdout = proxy
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
                results = dict(
                    (city, (ok, text))
                    for city, ok, text in pool.map(one_city, requested)
                )
        finally:
            sys.stdout = real_stdout
        for city in requested:
            ok, text = results[city]
            print(text, end="")
            if not ok:
                all_clean = False

    print("\nRESULT:", "zero drift" if all_clean else "DRIFT or failure - see above")
    if len(requested) < len(all_cities):
        skipped = sorted(set(all_cities) - set(requested))
        print(f"PARTIAL: {len(requested)} of {len(all_cities)} cities. Not checked: {', '.join(skipped)}.")
        print("Run without a filter before a deploy, or when recording a baseline.")
    print("Compare the step row counts above against the latest baseline entry in DECISIONS.md.")
    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
