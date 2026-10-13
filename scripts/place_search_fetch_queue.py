"""Decide which cities of a place-search wave still need their fetch, and run
the existing fetch script for them one after another, with no session
attending.

    python scripts/place_search_fetch_queue.py CITY [CITY ...] [--log FILE] [--dry-run] [--retries N] [--host MIRROR]
    python scripts/place_search_fetch_queue.py --selftest

For each city, in the order given, read pipeline.CITY.config and take its two
cache paths, PLACE_OSM_JSON and PLACE_OSM_EXTRA_JSON. Skip the city when both
files exist. Otherwise run `python pipeline/place_index_fetch.py CITY --wait 30`
as a child process, with the same interpreter and the repository root as the
working directory, and record its exit code, the seconds it took and the last
non-empty line of its output.

A city whose config cannot be imported, or that carries no PLACE_OSM_JSON or
no PLACE_OSM_EXTRA_JSON, is reported "not queued" with the reason, and counts
as a failure for the exit code. A city named twice is run once, and the repeat
is said. A city that exits non-zero goes on a retry list; after the last city,
each is tried once more, alone, in the same order, and a city that fails twice
is listed at the end and the script exits non-zero. After a child exits 0,
both cache files are checked; a missing one counts as failed with the reason
"exit 0 but a cache file is missing".

--retries N (default 1) is the number of retry rounds. A city fetched in
tiles (config.PLACE_SPLIT) keeps each tile that answered and must be re-run
until every tile is in, so a wave holding one takes a higher N. A child still
running after CHILD_TIMEOUT_MIN minutes is stopped and counts as failed: a
hung fetch would otherwise hold the queue and the fetch lock all night. The
lock file it leaves names a dead process, which the next fetch replaces.

--host MIRROR is passed to every child: the whole queue asks that one
Overpass mirror and holds only its lock, so a second queue with the other
mirror and a DIFFERENT city list may run beside it (owner, 2026-10-12: one
query in flight per mirror). Two queues must never share a city: nothing
here stops both from fetching it. The heavy cities, and every city fetched
in tiles, go to overpass-api.de: overpass.kumi.systems has read-timed out on
heavy queries (pipeline/osm.py).

WHAT IT DOES NOT DO. This script makes no request itself and holds no lock
itself: the fetch script holds the mirror's FetchLock (both mirrors' with no
--host), and pipeline/osm.py holds the wait after a 504 or 429. It never
starts two children at once: one child is started and waited for to the end,
and only then the next.
"""
import argparse
import datetime
import functools
import importlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FETCH_SCRIPT = "pipeline/place_index_fetch.py"
WAIT_MINUTES = "30"
# Longer than any fetch measured: London's twelve tiles with their waits took
# under an hour (2026-10-11), and the lock wait adds at most WAIT_MINUTES.
CHILD_TIMEOUT_MIN = 180
# The mirrors a queue may be pinned to: pipeline/osm.py's OVERPASS_HOSTS by
# name, repeated here so this script still imports nothing that can fetch
# (the selftest fails if the two lists differ).
MIRRORS = ("overpass-api.de", "overpass.kumi.systems")

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


def utc_now():
    """The current UTC time to the second, for one log line."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def child_command(city, script=FETCH_SCRIPT, host=None):
    """The argument list the real runner starts for one city: this
    interpreter, the fetch script, the city, --wait 30, and --host MIRROR
    when the queue is pinned. Built here so a test can assert on it without
    starting it."""
    return [sys.executable, script, city, "--wait", WAIT_MINUTES] + (["--host", host] if host else [])


def _last_line(stdout, stderr, failed=False):
    """The last non-empty line of a child's output. A child that failed says
    why on stderr (a traceback's last line), so stderr is read first then;
    a child that succeeded reports on stdout."""
    for text in ((stderr, stdout) if failed else (stdout, stderr)):
        for line in reversed(text.splitlines()):
            line = line.strip()
            if line:
                return line
    return ""


def real_runner(city, script=FETCH_SCRIPT, timeout_min=CHILD_TIMEOUT_MIN, host=None):
    """Start the fetch script for one city and wait for it to the end. Returns
    (exit code, last non-empty line). The child holds the fetch lock; this
    process makes no request. The child's pipes are UTF-8 whatever the
    console's code page is, as scripts/check_all.py sets for its checks. A
    child past timeout_min is stopped and reported as exit 124."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run(child_command(city, script, host), cwd=ROOT, env=env,
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout_min * 60)
    except subprocess.TimeoutExpired as exc:
        # What the child had said so far tells a lock wait from a hung
        # request; the pipes may hold bytes, text or nothing.
        def text(part):
            if isinstance(part, bytes):
                return part.decode("utf-8", errors="replace")
            return part or ""
        said = _last_line(text(exc.stdout), text(exc.stderr))
        return 124, (f"stopped after {timeout_min:g} min with no end"
                     + (f"; it last said: {said}" if said else ""))
    return proc.returncode, _last_line(proc.stdout, proc.stderr,
                                       failed=proc.returncode != 0)


def read_place_paths(city, importer=importlib.import_module):
    """(json, extra, None) for a city's two place caches, or (None, None, why)
    when the config cannot be imported, carries no such path, or carries
    something that is not a path. Importing a config module runs no request.
    A config that ends its import with sys.exit is refused like any other
    failure: only an interrupt from the keyboard passes through."""
    try:
        config = importer(f"pipeline.{city}.config")
    except KeyboardInterrupt:
        raise
    except BaseException as exc:
        return None, None, (f"cannot import pipeline.{city}.config: "
                            f"{type(exc).__name__}: {exc}")
    json_path = getattr(config, "PLACE_OSM_JSON", None)
    extra_path = getattr(config, "PLACE_OSM_EXTRA_JSON", None)
    missing = [key for key, value in (("PLACE_OSM_JSON", json_path),
                                      ("PLACE_OSM_EXTRA_JSON", extra_path))
               if value is None]
    if missing:
        return None, None, (f"pipeline.{city}.config carries no "
                            f"{' or '.join(missing)}")
    not_paths = [key for key, value in (("PLACE_OSM_JSON", json_path),
                                        ("PLACE_OSM_EXTRA_JSON", extra_path))
                 if not isinstance(value, Path)]
    if not_paths:
        return None, None, (f"pipeline.{city}.config: {' and '.join(not_paths)} "
                            f"must be a pathlib.Path")
    return json_path, extra_path, None


def _cache_state(path):
    """None when a cache file is there and whole, else what is wrong with it.
    Whole means it parses as JSON and holds an "elements" list, as every
    Overpass answer does: a child stopped in the middle of its write leaves a
    file that exists and does neither. Parsing a cache of tens of megabytes
    takes a second or two a city, once, before a fetch of many minutes."""
    if not path.exists():
        return "missing"
    if path.stat().st_size == 0:
        return "empty"
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return "cut short or not JSON"
    if not isinstance(data, dict) or not isinstance(data.get("elements"), list):
        return 'not a place cache (no "elements" list)'
    return None


def real_cached(city, json_path, extra_path):
    """None when both place caches are there and whole, else which one is
    not and why. The city argument is unused here; the selftest's lookup keys
    off it instead."""
    # The outline cache sits beside the place cache under one name for every
    # city (place_index.OUTLINE_CACHE_NAME): a city fetched before the
    # outline existed (2026-10-12) is queued again and fetches only that.
    from pipeline import place_index
    for key, path in (("PLACE_OSM_JSON", json_path), ("PLACE_OSM_EXTRA_JSON", extra_path),
                      ("the outline cache", json_path.parent / place_index.OUTLINE_CACHE_NAME)):
        state = _cache_state(path)
        if state is not None:
            return f"{key} {state}"
    return None


def _print(line):
    print(line, flush=True)


def run_queue(cities, *, runner, config_reader, cached, out=_print, log=None,
              dry_run=False, retries=1):
    """Run the queue and return 0 only when every city named was skipped or
    fetched. runner starts one child and returns (exit code, last line);
    cached returns None when both caches exist; out prints one stdout line.
    When log is given, each finished-city line is also appended there as
    bytes with LF endings, flushed per line."""
    seen = set()
    ordered = []
    for city in cities:
        if city in seen:
            out(f"{city}: named twice, run once")
        else:
            seen.add(city)
            ordered.append(city)

    # The log is opened before anything runs, so a path that cannot be
    # written stops the queue with a sentence, not a traceback hours in.
    log_file = None
    if log is not None:
        try:
            log_file = open(log, "ab")
        except OSError as exc:
            out(f"cannot open --log {log}: {exc}. Create its folder or name "
                f"another file; nothing was run.")
            return 2

    def emit(line):
        out(line)
        if log_file is not None:
            log_file.write((line + "\n").encode("utf-8"))
            log_file.flush()

    def finish(code):
        """Write the end marker, close the log and pass the exit code on. A
        log with no END line is a run that was killed."""
        emit(f"{utc_now()} END exit={code}")
        if log_file is not None:
            log_file.close()
        return code

    def read_city(city):
        """(json, extra, why) from the config reader and the cache test, with
        any error in either turned into a reason: one city's broken config
        never ends the queue."""
        try:
            json_path, extra_path, why = config_reader(city)
            if why is not None:
                return None, None, why, None
            return json_path, extra_path, None, cached(city, json_path, extra_path)
        except Exception as exc:
            return None, None, f"error reading its config or caches: {type(exc).__name__}: {exc}", None

    if dry_run:
        would_fetch, would_skip, not_queued = [], [], []
        for city in ordered:
            json_path, extra_path, why, missing = read_city(city)
            if why is not None:
                not_queued.append(f"{city} ({why})")
                emit(f"{city}: not queued ({why})")
                continue
            if missing is None:
                would_skip.append(city)
                emit(f"{city}: skip (both cache files present)")
            else:
                would_fetch.append(city)
                emit(f"{city}: fetch ({missing})")
        emit("")
        emit("dry run: no child was started")
        emit(f"  would fetch {len(would_fetch)}" + (f": {', '.join(would_fetch)}" if would_fetch else ""))
        emit(f"  would skip {len(would_skip)}" + (f": {', '.join(would_skip)}" if would_skip else ""))
        emit(f"  not queued {len(not_queued)}" + (f": {', '.join(not_queued)}" if not_queued else ""))
        return finish(0 if not not_queued else 1)

    fetched, skipped, failed_twice, not_queued, retry = [], [], [], [], []
    not_queued_names = set()
    # What a city that never succeeded is called: twice with the one default
    # retry round, else the number of tries.
    final = "failed twice" if retries == 1 else f"failed {retries + 1} times"

    def attempt(city, json_path, extra_path):
        """One child and the cache test after it. An error raised by either
        is that city's failure (exit 125), never the queue's end."""
        start = time.monotonic()
        try:
            exit_code, last = runner(city)
            missing = cached(city, json_path, extra_path)
        except Exception as exc:
            exit_code, last, missing = 125, f"queue error: {type(exc).__name__}: {exc}", "not tested"
        return exit_code, time.monotonic() - start, last, missing

    interrupted = False
    reached, retried = set(), set()
    try:
        for city in ordered:
            reached.add(city)
            json_path, extra_path, why, missing = read_city(city)
            if why is not None:
                not_queued.append(f"{city} ({why})")
                not_queued_names.add(city)
                emit(f"{utc_now()} {city} not queued: {why}")
                continue
            if missing is None:
                skipped.append(city)
                emit(f"{utc_now()} {city} skipped (both cache files present)")
                continue
            exit_code, seconds, last, missing = attempt(city, json_path, extra_path)
            if exit_code == 0 and missing is None:
                fetched.append(city)
                emit(f"{utc_now()} {city} fetched exit=0 {seconds:.1f}s last: {last}")
            elif exit_code == 0:
                retry.append((city, json_path, extra_path))
                emit(f"{utc_now()} {city} failed exit=0 {seconds:.1f}s "
                     f"reason: exit 0 but a cache file is missing")
            else:
                retry.append((city, json_path, extra_path))
                emit(f"{utc_now()} {city} failed exit={exit_code} {seconds:.1f}s last: {last}")

        for round_no in range(1, retries + 1):
            again = []
            for city, json_path, extra_path in retry:
                retried.add(city)
                exit_code, seconds, last, missing = attempt(city, json_path, extra_path)
                why = (f"last: {last}" if exit_code else "reason: exit 0 but a cache file is missing")
                if exit_code == 0 and missing is None:
                    fetched.append(city)
                    emit(f"{utc_now()} {city} retried and fetched exit=0 {seconds:.1f}s last: {last}")
                elif round_no == retries:
                    failed_twice.append(city)
                    emit(f"{utc_now()} {city} {final} exit={exit_code} {seconds:.1f}s {why}")
                else:
                    again.append((city, json_path, extra_path))
                    emit(f"{utc_now()} {city} failed again exit={exit_code} {seconds:.1f}s {why}")
            retry = again
        if retries < 1:
            for city, _, _ in retry:
                failed_twice.append(city)
    except KeyboardInterrupt:
        interrupted = True
        emit("interrupted: stopping after the current child")

    # The summary goes to the log as well as the screen: a log is all that
    # is left of a run nobody watched.
    emit("")
    emit("Summary:")
    emit(f"  fetched {len(fetched)}" + (f": {', '.join(fetched)}" if fetched else ""))
    emit(f"  skipped {len(skipped)}" + (f": {', '.join(skipped)}" if skipped else ""))
    emit(f"  {final} {len(failed_twice)}" + (f": {', '.join(failed_twice)}" if failed_twice else ""))
    emit(f"  not queued {len(not_queued)}" + (f": {', '.join(not_queued)}" if not_queued else ""))
    if interrupted:
        # An interrupted run says what it left, so no city is lost from view:
        # the one in flight or failed once and not yet retried, and the ones
        # the first round never reached.
        settled = set(fetched) | set(skipped) | set(failed_twice) | not_queued_names
        unsettled = [c for c in ordered if c in reached and c not in settled]
        unreached = [c for c in ordered if c not in reached]
        emit(f"  interrupted, not settled {len(unsettled)}"
             + (f": {', '.join(unsettled)}" if unsettled else ""))
        emit(f"  interrupted, not reached {len(unreached)}"
             + (f": {', '.join(unreached)}" if unreached else ""))
    return finish(1 if interrupted or failed_twice or not_queued else 0)


def main(argv=None, *, runner=real_runner, config_reader=read_place_paths,
         cached=real_cached, out=_print):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("city", nargs="+", metavar="CITY")
    ap.add_argument("--log", metavar="FILE",
                    help="append each finished-city line to this file")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and start no child")
    ap.add_argument("--retries", type=int, default=1, metavar="N",
                    help="retry rounds after the first pass (default 1; more for a city fetched in tiles)")
    ap.add_argument("--host", metavar="MIRROR", choices=MIRRORS,
                    help="pin every child to this one Overpass mirror: " + " or ".join(MIRRORS))
    args = ap.parse_args(argv)
    if args.retries < 1:
        ap.error("--retries must be 1 or more")
    if args.host and runner is real_runner:
        runner = functools.partial(real_runner, host=args.host)
    log_path = Path(args.log) if args.log else None
    return run_queue(args.city, runner=runner, config_reader=config_reader,
                     cached=cached, out=out, log=log_path, dry_run=args.dry_run,
                     retries=args.retries)


def selftest():
    import tempfile

    cases = []

    def report(label, ok):
        cases.append((label, ok))
        print(f"  {'ok ' if ok else 'BAD'} {label}")

    class State:
        def __init__(self, present=()):
            self.present = set(present)

        def cached(self, city, json_path, extra_path):
            return None if city in self.present else "PLACE_OSM_JSON missing"

    class Runner:
        def __init__(self, state, plan=None, writes=True):
            self.state = state
            self.plan = {c: list(codes) for c, codes in (plan or {}).items()}
            self.writes = writes
            self.calls = []
            self.events = []
            self.active = None
            self.overlap = False

        def __call__(self, city):
            self.calls.append(city)
            if self.active is not None:
                self.overlap = True
            self.active = city
            self.events.append(("enter", city))
            codes = self.plan.get(city)
            code = codes.pop(0) if codes else 0
            if code == 0 and self.writes:
                self.state.present.add(city)
            self.events.append(("leave", city))
            self.active = None
            return code, f"{city}: last line"

    def config_ok(city):
        return f"{city}.json", f"{city}_extra.json", None

    def run(cities, runner, config_reader, cached, dry_run=False, log=None, retries=1):
        lines = []
        rc = run_queue(cities, runner=runner, config_reader=config_reader,
                       cached=cached, out=lines.append, dry_run=dry_run, log=log,
                       retries=retries)
        return rc, "\n".join(lines)

    state = State(present=("a", "b"))
    runner = Runner(state)
    rc, text = run(["a", "b"], runner, config_ok, state.cached)
    report("every city cached: the runner is never called and the exit code is 0",
           rc == 0 and runner.calls == [])

    state = State()
    runner = Runner(state, plan={"a": [1, 0], "b": [0]})
    rc, text = run(["a", "b"], runner, config_ok, state.cached)
    report("one city fails once then succeeds on the retry, after the last city",
           rc == 0 and runner.calls == ["a", "b", "a"]
           and "a failed exit=1" in text and "a retried and fetched exit=0" in text)

    state = State()
    runner = Runner(state, plan={"a": [1, 1]})
    rc, text = run(["a"], runner, config_ok, state.cached)
    report("one city fails twice: the exit code is non-zero and the summary names it",
           rc != 0 and "failed twice 1: a" in text and "a failed twice exit=1" in text)

    state = State()
    runner = Runner(state)
    rc, text = run(["b", "a", "c"], runner, config_ok, state.cached)
    report("first-round runs follow the order given", runner.calls == ["b", "a", "c"])

    state = State()
    runner = Runner(state, plan={"a": [1, 1, 0], "b": [1, 1, 1, 1]})
    rc, text = run(["a", "b"], runner, config_ok, state.cached, retries=3)
    report("--retries 3: a city in tiles succeeds on its third try, one that never does is named",
           rc != 0 and runner.calls == ["a", "b", "a", "b", "a", "b", "b"]
           and "a failed again exit=1" in text and "a retried and fetched exit=0" in text
           and "failed 4 times 1: b" in text)

    state = State()
    runner = Runner(state, plan={"a": [1, 1, 0]})
    rc, text = run(["a"], runner, config_ok, state.cached)
    report("the default is one retry round: a third try is never made",
           rc != 0 and runner.calls == ["a", "a"] and "failed twice 1: a" in text)

    state = State()
    runner = Runner(state)
    rc, text = run(["a", "b"], runner, config_ok, state.cached)
    stack = []
    nested = True
    for event, city in runner.events:
        if event == "enter":
            if stack:
                nested = False
            stack.append(city)
        elif not stack or stack.pop() != city:
            nested = False
    report("never two children at once",
           nested and not stack and not runner.overlap and runner.calls == ["a", "b"])

    state = State(present=("b",))
    runner = Runner(state)
    rc, text = run(["a", "b"], runner, config_ok, state.cached, dry_run=True)
    report("dry-run starts no child and prints fetch or skip per city",
           runner.calls == [] and "a: fetch" in text and "b: skip" in text)

    state = State()

    def config_mixed(city):
        if city == "nope":
            return None, None, f"cannot import pipeline.{city}.config: No module named '{city}'"
        return config_ok(city)

    runner = Runner(state)
    rc, text = run(["nope", "a"], runner, config_mixed, state.cached)
    report("a city with no place config is not queued, the rest still run, exit non-zero",
           rc != 0 and "nope not queued" in text and "a fetched exit=0" in text
           and runner.calls == ["a"])

    state = State()
    runner = Runner(state, plan={"a": [0, 0]}, writes=False)
    rc, text = run(["a"], runner, config_ok, state.cached)
    report("a child that exits 0 but leaves a cache file missing counts as failed",
           rc != 0 and "exit 0 but a cache file is missing" in text
           and "a failed twice" in text)

    state = State()
    runner = Runner(state)
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "queue.log"
        rc, text = run(["a", "b"], runner, config_ok, state.cached, log=str(log_path))
        data = log_path.read_bytes()
        city_lines = [l for l in data.split(b"\n") if b" fetched exit=0" in l]
        report("with --log, the file holds one line per finished city, LF endings",
               rc == 0 and len(city_lines) == 2 and b"\r" not in data
               and b" a fetched exit=0" in data and b" b fetched exit=0" in data)
        report("the log ends with the summary and an END line carrying the exit code",
               b"Summary:" in data and b"  fetched 2: a, b" in data
               and data.rstrip().endswith(b"END exit=0"))

    state = State()
    runner = Runner(state)
    rc, text = run(["a", "a", "b"], runner, config_ok, state.cached)
    report("a city named twice is run once and the repeat is said",
           runner.calls == ["a", "b"] and "a: named twice, run once" in text)

    import re as _re
    osm_text = (ROOT / "pipeline" / "osm.py").read_text(encoding="utf-8")
    block = osm_text.split("OVERPASS_HOSTS = (", 1)[1].split(")", 1)[0]
    report("MIRRORS is pipeline/osm.py's host list, in its order",
           tuple(_re.findall(r"https://([^/]+)/", block)) == MIRRORS)
    report("a pinned queue's command ends --host MIRROR; an unpinned one has none",
           child_command("somewhere", host=MIRRORS[1])[-2:] == ["--host", MIRRORS[1]]
           and "--host" not in child_command("somewhere"))
    report("the real runner's command is the interpreter, the fetch script, the city, --wait, 30",
           child_command("somewhere") == [sys.executable, FETCH_SCRIPT, "somewhere",
                                          "--wait", WAIT_MINUTES]
           and FETCH_SCRIPT == "pipeline/place_index_fetch.py"
           and WAIT_MINUTES == "30")

    state = State()
    runner = Runner(state)
    lines = []
    rc = main(["a", "b", "--dry-run"], runner=runner, config_reader=config_ok,
              cached=state.cached, out=lines.append)
    report("main: the entry point parses --dry-run and returns the queue's exit code",
           rc == 0 and runner.calls == [] and "a: fetch" in "\n".join(lines))

    state = State()
    runner = Runner(state, plan={"a": [1, 1]})
    lines = []
    rc = main(["a"], runner=runner, config_reader=config_ok,
              cached=state.cached, out=lines.append)
    report("main: a failure makes the entry point exit non-zero",
           rc != 0 and "failed twice 1: a" in "\n".join(lines))

    # The real functions, on temporary files and a stand-in child: no city,
    # no config and no request.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        a, b = tmp / "a.json", tmp / "b.json"
        none = real_cached("x", a, b)
        a.write_bytes(b'{"elements": []}')
        one = real_cached("x", a, b)
        b.write_bytes(b'{"elements": []}')
        both = real_cached("x", a, b)
        from pipeline import place_index
        (tmp / place_index.OUTLINE_CACHE_NAME).write_bytes(b'{"elements": []}')
        three = real_cached("x", a, b)
        report("the real cache test names the missing file and passes only with all three",
               none == "PLACE_OSM_JSON missing" and one == "PLACE_OSM_EXTRA_JSON missing"
               and both == "the outline cache missing" and three is None)

        class Config:
            PLACE_OSM_JSON = a
            PLACE_OSM_EXTRA_JSON = b

        class NoExtra:
            PLACE_OSM_JSON = a

        def raising(name):
            raise ImportError(f"No module named {name!r}")

        full = read_place_paths("x", importer=lambda name: Config)
        part = read_place_paths("x", importer=lambda name: NoExtra)
        gone = read_place_paths("x", importer=raising)
        report("the real config reader returns both paths, and refuses a config "
               "missing one or a city that cannot be imported",
               full == (a, b, None)
               and part[0] is None and "PLACE_OSM_EXTRA_JSON" in part[2]
               and "PLACE_OSM_JSON or" not in part[2]
               and gone[0] is None and "cannot import pipeline.x.config" in gone[2])

        child = tmp / "child.py"
        child.write_bytes(b"import sys\n"
                          b"print('progress on stdout')\n"
                          b"print(' '.join(sys.argv[1:]))\n"
                          b"if sys.argv[1] == 'bad':\n"
                          b"    print('the reason on stderr', file=sys.stderr)\n"
                          b"    sys.exit(3)\n")
        good_run = real_runner("good", script=str(child))
        bad_run = real_runner("bad", script=str(child))
        report("the real runner passes the child's exit code on, gives it the city "
               "and --wait 30, and reads a failure's reason from stderr",
               good_run == (0, "good --wait 30") and bad_run == (3, "the reason on stderr"))

        slow = tmp / "slow.py"
        slow.write_bytes(b"import time\ntime.sleep(30)\n")
        began = time.monotonic()
        hung = real_runner("x", script=str(slow), timeout_min=1 / 60)
        report("the real runner stops a child past its time and reports exit 124",
               hung[0] == 124 and "stopped after" in hung[1] and time.monotonic() - began < 15)

        lines = []
        try:
            main(["a", "--retries", "0"], runner=Runner(State()), config_reader=config_ok,
                 cached=State().cached, out=lines.append)
            refused = False
        except SystemExit as exc:
            refused = exc.code != 0
        report("main: --retries 0 is refused", refused)

        state = State()
        runner = Runner(state)
        log_path = tmp / "main.log"
        lines = []
        rc = main(["a", "--log", str(log_path)], runner=runner, config_reader=config_ok,
                  cached=state.cached, out=lines.append)
        report("main: --log reaches the queue and the file is written",
               rc == 0 and log_path.exists() and b" a fetched exit=0" in log_path.read_bytes())

    class Interrupting(Runner):
        def __call__(self, city):
            if city == "b":
                raise KeyboardInterrupt
            return super().__call__(city)

    state = State()
    runner = Interrupting(state, plan={"a": [1]})
    rc, text = run(["a", "b", "c"], runner, config_ok, state.cached)
    report("an interrupt stops the queue, exits non-zero and names what it left",
           rc != 0 and runner.calls == ["a"]
           and "interrupted, not settled 2: a, b" in text
           and "interrupted, not reached 1: c" in text)

    # Found by an adversarial review (2026-10-12): each is a way an unattended
    # run could look fine and not be.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        whole, empty, cut = tmp / "whole.json", tmp / "empty.json", tmp / "cut.json"
        whole.write_bytes(b'{"elements": []}\n')
        empty.write_bytes(b"")
        cut.write_bytes(b'{"elements": [{"id": 1')
        other = tmp / "other.json"
        other.write_bytes(b'{"remark": "runtime error: timed out"}')
        from pipeline import place_index
        (tmp / place_index.OUTLINE_CACHE_NAME).write_bytes(b'{"elements": []}\n')
        report("a cache that is empty, cut short or not an Overpass answer is not a cache",
               real_cached("x", whole, whole) is None
               and real_cached("x", whole, empty) == "PLACE_OSM_EXTRA_JSON empty"
               and "cut short" in (real_cached("x", cut, whole) or "")
               and "elements" in (real_cached("x", whole, other) or ""))

        class Strings:
            PLACE_OSM_JSON = "a.json"
            PLACE_OSM_EXTRA_JSON = whole

        def exiting(name):
            raise SystemExit(0)

        as_strings = read_place_paths("x", importer=lambda name: Strings)
        # Caught here, or a config's sys.exit(0) would end this selftest with
        # exit 0 and hide the very failure the case is for.
        try:
            as_exit = read_place_paths("x", importer=exiting)
        except SystemExit:
            as_exit = ("escaped", None, "")
        report("a config whose path is a string, or whose import calls sys.exit, is refused",
               as_strings[0] is None and "PLACE_OSM_JSON must be a pathlib.Path" in as_strings[2]
               and as_exit[0] is None and "SystemExit" in as_exit[2])

        def breaking(city):
            if city == "bad":
                raise AttributeError("'str' object has no attribute 'exists'")
            return config_ok(city)

        state = State()
        runner = Runner(state)
        rc, text = run(["bad", "a"], runner, breaking, state.cached)
        report("an error reading one city's config does not end the queue",
               rc != 0 and runner.calls == ["a"] and "bad not queued: error reading" in text
               and "a fetched exit=0" in text and "Summary:" in text)

        class Raising(Runner):
            def __call__(self, city):
                if city == "a":
                    self.calls.append(city)
                    raise OSError("the child could not be started")
                return super().__call__(city)

        state = State()
        runner = Raising(state)
        rc, text = run(["a", "b"], runner, config_ok, state.cached)
        report("an error starting one child is that city's failure, and the next city runs",
               rc != 0 and runner.calls == ["a", "b", "a"] and "exit=125" in text
               and "b fetched exit=0" in text and "failed twice 1: a" in text)

        state = State()
        runner = Runner(state)
        rc, text = run(["a"], runner, config_ok, state.cached,
                       log=str(tmp / "no_such_folder" / "queue.log"))
        report("a --log that cannot be opened stops the queue with a sentence, before any child",
               rc == 2 and runner.calls == [] and "cannot open --log" in text)

        state = State(present=("b",))
        runner = Runner(state)
        dry_log = tmp / "dry.log"
        rc, text = run(["a", "b"], runner, config_ok, state.cached, dry_run=True, log=str(dry_log))
        dry = dry_log.read_bytes()
        report("a dry run writes its plan to the log too, and still starts no child",
               runner.calls == [] and b"a: fetch" in dry and b"b: skip" in dry
               and dry.rstrip().endswith(b"END exit=0"))

        state = State()
        runner = Interrupting(state, plan={"a": [1]})
        kill_log = tmp / "kill.log"
        rc, text = run(["a", "b", "c"], runner, config_ok, state.cached, log=str(kill_log))
        killed = kill_log.read_bytes()
        report("an interrupted run's log holds what it left and its END line",
               b"interrupted: stopping" in killed
               and b"interrupted, not reached 1: c" in killed
               and killed.rstrip().endswith(b"END exit=1"))

        def mixed(city):
            if city == "a (x)":
                return None, None, "cannot import"
            return config_ok(city)

        class StopAtA(Runner):
            def __call__(self, city):
                if city == "a":
                    raise KeyboardInterrupt
                return super().__call__(city)

        state = State()
        runner = StopAtA(state)
        rc, text = run(["a (x)", "a"], runner, mixed, state.cached)
        report("a city whose name begins another's refusal is still named as not settled",
               "interrupted, not settled 1: a" in text)

        slow = tmp / "slow.py"
        slow.write_bytes(b"import sys, time\n"
                         b"print('waiting for the lock', flush=True)\n"
                         b"time.sleep(30)\n")
        code, last = real_runner("x", script=str(slow), timeout_min=0.02)
        report("a child past the time limit is stopped as exit 124 with what it last said",
               code == 124 and "waiting for the lock" in last)

    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
