"""Re-run every city's pipeline from scratch and diff the regenerated
outputs/ against what is committed at git HEAD.

The deployed app only ever reads outputs/, so outputs/ can silently drift
from what the pipeline would produce if a script changes and nobody re-runs
it. This check catches that.

Usage:
    python pipeline/drift_check.py                 # every city
    python pipeline/drift_check.py san_diego       # just one
    python pipeline/drift_check.py --changed       # only the cities the
                                                   #   working changes can affect
    python pipeline/drift_check.py --changed --list    # show them, run nothing
    python pipeline/drift_check.py --since HEAD~3  # cities affected since a ref
    python pipeline/drift_check.py --render-only   # only each city's MAP step
                                                   #   (see "RENDER-ONLY" below)

Exit code 0 = zero drift, 1 = real drift (or a step failed, or a city was
refused).

RENDER-ONLY (`--render-only`, 2026-09-30). A change that touches only map
rendering (pipeline/map_common.py's drawing, theme.py) cannot change what
steps 1-2 write to data/<city>/processed/, yet the full sweep re-runs them for
every city, and their register reads make the sweep the heaviest job on the
machine. `--render-only` runs exactly ONE step per city: the file
named `step*_map.py` (step3_map.py in 117 cities, step4_map.py in the seven
that have a step 3 before it). It does NOT run step3_geocode.py or
step3_place.py: those join or geocode businesses into
data/<city>/processed/businesses_geocoded.csv (a map INPUT, never an
outputs/ file; checked 2026-09-30 for all seven), and geocoding is not
rendering. The map step still runs under the offline guard, and outputs/ is
diffed exactly as the full check diffs it.

What it ASSUMES, and the reason it is never the pre-deploy gate: that
data/<city>/processed/ is current for the code being checked. data/ is one
folder shared by every worktree, so processed files are whatever the last
run of steps 1-2 (on any branch) left there; the city header prints how many
processed files there are and when the newest was written, so a reader can
see it. A city with no processed inputs at all is REFUSED (counted as a
failure) rather than reported clean; a city with no map step, or more than
one, is refused too. The baseline counts are not checked, since no map step
emits any. `--update-baseline` with `--render-only` is refused.

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
the one to run before a deploy or when recording a baseline in DECISIONS.md.

Three things it deliberately handles:
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

It re-runs against the raw files already in data/<city>/raw/; it does NOT
re-download. It prints each raw input's size and modified time so a reader
can tell code drift (raw files unchanged, outputs changed) from source
drift (raw files were refreshed since the baseline).

`--jobs N` runs CITIES concurrently (default 1, at most MAX_JOBS = 2 since
2026-09-28's memory crashes; one drift check per machine at a time). The full
sweep is this project's only O(n)-in-pipeline-runs cost, so it is the binding
operational limiter as the city count grows; see
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
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# This file is run as a script, so the repo root is not on sys.path the way it
# is for the step scripts (which insert it themselves).
sys.path.insert(0, str(ROOT))

from pipeline import baseline, offline  # noqa: E402
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


def check_baseline(city: str, measured: dict, *, update: bool = False) -> bool:
    """Diff a city's emitted row counts against outputs/<city>/baseline.json.

    The output files are compared byte for byte elsewhere; this catches what
    that cannot: a COUNT that moved while the map still rendered plausibly.
    """
    if update and measured:
        path = baseline.save(city, measured)
        print(f"\n  baseline: wrote {len(measured)} figure(s) to "
              f"{path.relative_to(ROOT).as_posix()}")
        return True
    ok, lines = baseline.compare(city, measured)
    if lines:
        print()
        for line in lines:
            print(line)
    return ok


def map_steps(city: str) -> list:
    """A city's map-rendering step(s): `step*_map.py`. Exactly one is valid."""
    return sorted((ROOT / "pipeline" / city).glob("step*_map.py"))


def render_only_refusal(city: str) -> str | None:
    """Why `--render-only` cannot check this city, or None when it can."""
    found = map_steps(city)
    if len(found) != 1:
        names = ", ".join(p.name for p in found) or "none"
        return (f"pipeline/{city}/ has {len(found)} step*_map.py files ({names}); "
                "render-only needs exactly one. Run the full check for this city.")
    processed = ROOT / "data" / city / "processed"
    if not processed.is_dir() or not any(p.is_file() for p in processed.rglob("*")):
        return (f"data/{city}/processed/ is missing or empty. Render-only re-runs "
                "only the map step, which reads steps 1-2's output from there. "
                f"Run the full check instead: python pipeline/drift_check.py {city}")
    return None


def show_processed_inputs(city: str):
    files = [p for p in (ROOT / "data" / city / "processed").rglob("*") if p.is_file()]
    newest = max(files, key=lambda p: p.stat().st_mtime)
    when = datetime.datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    print(f"  processed inputs: {len(files)} file(s), newest {newest.name} modified {when} "
          "(render-only assumes these are current)")


def check_city(city: str, *, render_only: bool, update_baseline: bool) -> bool:
    """One city's whole check, printed to stdout. Returns True when clean."""
    print(f"\n=== {city} ===")
    if render_only:
        started = time.monotonic()
        refusal = render_only_refusal(city)
        if refusal:
            print(f"  REFUSED: {refusal}")
            return False
        show_processed_inputs(city)
        ran, _ = run_steps(city, only=map_steps(city))
        ok = ran and compare_outputs(city)
        print("\n  baseline: not checked (render-only runs no step that emits counts)")
        print(f"  render-only: {city} took {time.monotonic() - started:.1f} s")
        return ok
    show_raw_inputs(city)
    ran, measured = run_steps(city)
    if not ran:
        return False
    ok = compare_outputs(city)
    return check_baseline(city, measured, update=update_baseline) and ok


def run_steps(city: str, only: list | None = None):
    """Run a city's steps in order (or just `only`). Return (ok, emitted_baseline_figures).

    The figures come from `##BASELINE key=value` lines a step prints via
    pipeline.baseline.emit(). Captured here because stdout already is, so a step
    needs no other change to be watched, and filtered out of the echoed output,
    since they are data rather than narration.
    """
    # A DRIFT CHECK MUST NOT REACH THE NETWORK. Steps do not download their
    # own inputs (scripts/check_no_fetch_in_steps.py enforces it),
    # but three step3_geocode.py files still call the US Census geocoder for
    # batches they compute themselves, which cannot move to a fetch script.
    # This makes such a call refuse here while leaving it available to a
    # person running the step. See pipeline/offline.py.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8",
           offline.NO_NETWORK_ENV: "1"}
    measured = {}
    steps = only if only is not None else sorted((ROOT / "pipeline" / city).glob("step*.py"))
    for step in steps:
        print(f"\n  >> {step.name}")
        proc = subprocess.run(
            [sys.executable, str(step)], cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        for line in proc.stdout.splitlines():
            if line.strip().startswith(baseline.MARKER):
                continue
            print(f"     {line}")
        measured.update(baseline.parse(proc.stdout))
        if proc.returncode != 0:
            print(f"     STEP FAILED (exit {proc.returncode})\n{proc.stderr}")
            return False, measured
    return True, measured


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
        # change was just committed (exactly when "commit after each green
        # step" says to run this), so look one commit back rather than
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


# Owner, 2026-09-28, after two memory-exhaustion crashes: at most two cities
# at once on this 16 GB machine, whose Python is capped at 12 GB a process tree
# (scripts/python_memcap.py). Change it with the owner's word, not to go faster.
MAX_JOBS = 2
LOCK_OFFSET = 1 << 20  # lock a byte past the text, so a waiter can read who holds it


def hold_machine_lock():
    """One drift check at a time on this machine, across every worktree.

    On 2026-09-28 overlapping heavy jobs ran the machine out of memory twice
    (DECISIONS.md). The lock file
    sits in the git directory every worktree shares, and the lock is the
    operating system's: it dies with the process, so a crash leaves nothing
    stale to clear. Returns the open file; the lock lasts while it is open.
    """
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()
    path = (ROOT / common).resolve() / "drift_check.lock"
    path.touch(exist_ok=True)
    fh = open(path, "r+", encoding="utf-8")
    try:
        fh.seek(LOCK_OFFSET)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.lockf(fh, fcntl.LOCK_EX | fcntl.LOCK_NB, 1, LOCK_OFFSET)
    except OSError:
        fh.seek(0)
        holder = fh.readline().strip() or "holder unknown"
        sys.exit(f"Another drift check is running on this machine ({holder}). "
                 "One at a time: wait for it to finish, then run this again.")
    fh.seek(0)
    fh.write(f"pid {os.getpid()} in {ROOT.name}, since "
             f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}".ljust(120) + "\n")
    fh.flush()
    return fh


def main():
    # Steps print place and business names (Czech, Korean, Chinese...), and a
    # Windows console defaults to cp1252: `drift_check.py prague` raised
    # UnicodeEncodeError on a Czech letter (2026-09-27). UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    list_only = "--list" in args
    args = [a for a in args if a != "--list"]

    # --jobs N runs CITIES concurrently. Default 1; see "WHY THE DEFAULT IS
    # STILL 1" at the parallel branch.
    update_baseline = "--update-baseline" in args
    if update_baseline:
        args = [a for a in args if a != "--update-baseline"]
    render_only = "--render-only" in args
    if render_only:
        args = [a for a in args if a != "--render-only"]
        if update_baseline:
            sys.exit("--update-baseline cannot be used with --render-only: the counts "
                     "come from steps 1-2, which render-only does not run.")
    jobs = 1
    if "--jobs" in args:
        i = args.index("--jobs")
        if i + 1 >= len(args) or not args[i + 1].isdigit() or int(args[i + 1]) < 1:
            sys.exit("--jobs needs a positive integer, e.g. --jobs 2")
        jobs = int(args[i + 1])
        if jobs > MAX_JOBS:
            sys.exit(f"--jobs {jobs} is over this machine's limit of {MAX_JOBS} "
                     "(owner, 2026-09-28: Oslo's step 2 alone peaks near 5.4 GB, and "
                     "Python is capped at 12 GB a process tree). Use --jobs "
                     f"{MAX_JOBS} or fewer.")
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

    lock = hold_machine_lock()  # noqa: F841 - held until the process exits
    all_clean = True
    if jobs == 1:
        # The default path: print straight to stdout as it goes, so a long
        # sweep shows progress, in the same output format as before --jobs.
        for city in requested:
            if not check_city(city, render_only=render_only, update_baseline=update_baseline):
                all_clean = False
    else:
        # --jobs N: cities run concurrently (safe for the reasons in the
        # module docstring). The STEPS WITHIN a city stay sequential.
        #
        # Threads rather than processes: the work is `subprocess.run`, which
        # releases the GIL while it waits, so threads get the full speedup with
        # no pickling and no re-import of the module per worker.
        #
        # Each city's output is buffered and printed as ONE block, in the
        # requested order rather than the completion order. Interleaved prints
        # from concurrent cities would make the report unreadable, and worse,
        # would attach a step's row counts to the wrong city.
        # WHY THE DEFAULT IS STILL 1. Running cities concurrently answers the
        # sweep's O(n) cost (docs/scaling_thresholds.md), but each city's step
        # 2 loads a full business dataset through geopandas, and four of those
        # at once is four times the peak memory: New York's is the largest, so
        # --jobs 4 on a small machine can swap or be killed, and a killed sweep
        # before a deploy is worse than a slow one. MAX_JOBS caps it (see
        # there); the default stays the one that always works.
        print(f"\n(running {len(requested)} cities with --jobs {jobs}; "
              "each city's report is printed as a block when it finishes)")

        # A THREAD-LOCAL stdout proxy, installed once. Swapping `sys.stdout`
        # per worker instead would be a race: it is one global, so two threads
        # assigning it concurrently clobber each other and a city's step row
        # counts end up printed under a different city's heading, which is
        # worse than no parallelism because it looks fine.
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
            ok = check_city(city, render_only=render_only, update_baseline=update_baseline)
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
    if render_only:
        print("RENDER-ONLY: only each city's map step ran, against data/<city>/processed/ "
              "as it stands, which this mode assumes is current. It is not the pre-deploy "
              "gate: run without --render-only for that.")
    if len(requested) < len(all_cities):
        skipped = sorted(set(all_cities) - set(requested))
        print(f"PARTIAL: {len(requested)} of {len(all_cities)} cities. Not checked: {', '.join(skipped)}.")
        print("Run without a filter before a deploy, or when recording a baseline.")
    # Row counts were once compared by hand against the latest baseline entry
    # in DECISIONS.md. A city with outputs/<city>/baseline.json has that diff
    # done above; one without is named here so the gap is visible rather than
    # silently unchecked.
    print("Row counts are diffed against outputs/<city>/baseline.json where one "
          "exists (--update-baseline to record an intended change).")
    print("Cities with no baseline yet emit no figures - see pipeline/baseline.py.")
    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
