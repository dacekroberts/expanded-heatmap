"""The heavy-job gate: at most four heavy jobs on the machine, each admitted
against the memory actually available (owner, 2026-09-30; three since
2026-10-04; four since 2026-10-05, when the machine went from 16 GB to 32 GB).

WHY A GATE, NOT A MONITOR. Every session shares one machine (16 GB until
2026-10-05, 32 GB since). On
2026-09-28 overlapping jobs ran it out of memory and Windows closed the Claude
app twice. A monitor polls all day and reacts after the damage; a gate is
asked once, before the damage, by the session about to cause it. A FIXED
budget ("two jobs under 12 GB") was wrong too: measured 2026-09-30, the apps
alone (eight Claude sessions, a browser) hold about 8 GB, and one orphaned
grep held 4.7 GB more. So admission reads available memory, now.

    python scripts/heavy_job.py run --label "oslo step 2" --session cleanup -- python pipeline/oslo/step2_clean_businesses.py
    python scripts/heavy_job.py run --label "osaka step 2" --peak-gb 1.0 --estimate "scaled from Kyoto 0.33 GB by raw size" --session S -- ...
    python scripts/heavy_job.py status
    python scripts/heavy_job.py start --label L --peak-gb N --session S --pid P   # a job that cannot be wrapped
    python scripts/heavy_job.py end --pid P
    python scripts/heavy_job.py --selftest                                         # touches nothing

`run` is the normal path: it admits the job, runs it, removes its entry when
it exits (whatever the exit), and records the MEASURED peak (the process and
its children, sampled every 2 s) in the history, so the next session states a
real figure instead of a guess. A French SIRENE step 2, estimated at 1.5 GB,
measured 0.37 GB (2026-09-30); Oslo's step 2 peaks near 5.4 GB.

ADMISSION: fewer than MAX_JOBS live entries, and
    available - reserved >= peak + MARGIN_GB
where `reserved` is each live job's declared peak minus what it already
holds: a job that has just started has not reached its peak, and without the
reservation two jobs started seconds apart would both be admitted and collide.
MEASURED FIGURES ARE THE NORM (owner, 2026-10-03). The declared peak is,
in order: the label's last MEASURED peak (`--peak-gb` omitted or
`measured`); else an ESTIMATE scaled from measured jobs, which says so
(`--peak-gb N --estimate "scaled from ..."`); else DEFAULT_PEAK_GB, the
per-process cap. In a series of like jobs the first is the measurement and
the rest declare from it, so labels stay stable ("<city> step 2", "drift
<city>"). Each ENDED line prints the measured peak; `status` lists the
latest per label. Until 2026-10-03 no peak was ever recorded: remove() read
the ledger through the dead-pid filter after the job's child had exited.
Refused: exit 3, with the status printed so the refused session can see the
culprit.

THE LEDGER is data/_heavy_jobs.json. data/ is one junction shared by every
worktree, so every session reads the same file; it is gitignored. An entry
whose pid is dead is dropped on read, so a crashed job never blocks anyone.
Writes take an O_EXCL lock file, so two sessions starting at once cannot both
slip in. The Python cap (scripts/python_memcap.py, 8 GB a process, 16 GB with
children) stays as the backstop.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[1]
# Two from 2026-09-30; three from 2026-10-04 (owner: "allow three heavy jobs
# since i have no other open processes"); four from 2026-10-05, when the RAM
# went from 16 GB to 32 GB (owner: "tweak our memory gate"). The count now
# guards the 6 physical cores more than memory; memory still decides each job.
MAX_JOBS = 4
MARGIN_GB = 2.0
DEFAULT_PEAK_GB = 8.0
BIG_PROCESS_GB = 1.5
GB = 2 ** 30


def paths():
    base = Path(os.environ.get("HEAVY_JOB_DIR", ROOT / "data"))
    return base / "_heavy_jobs.json", base / "_heavy_jobs.lock", base / "_heavy_jobs_history.json"


class Lock:
    def __init__(self, path, timeout=30):
        self.path, self.timeout = path, timeout

    def __enter__(self):
        t0 = time.time()
        while True:
            try:
                os.close(os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
                return self
            except FileExistsError:
                try:   # a lock older than a minute is a crashed writer's
                    if time.time() - self.path.stat().st_mtime > 60:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.time() - t0 > self.timeout:
                    raise SystemExit(f"heavy_job: could not take {self.path} in {self.timeout}s")
                time.sleep(0.2)

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def _read(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return default


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def tree_rss(pid):
    """Resident memory of a process and all its children, in bytes (0 if gone)."""
    try:
        p = psutil.Process(pid)
        procs = [p] + p.children(recursive=True)
    except psutil.Error:
        return 0
    total = 0
    for q in procs:
        try:
            total += q.memory_info().rss
        except psutil.Error:
            pass
    return total


def live(jobs, alive=psutil.pid_exists):
    return [j for j in jobs if alive(j["pid"])]


def decide(jobs, peak_gb, available_gb, held_gb):
    """Pure admission rule. jobs: live entries; held_gb: {pid: GB already held}."""
    if len(jobs) >= MAX_JOBS:
        return False, f"{len(jobs)} heavy jobs already running (at most {MAX_JOBS})", 0.0
    reserved = sum(max(0.0, j["peak_gb"] - held_gb.get(j["pid"], 0.0)) for j in jobs)
    need = peak_gb + MARGIN_GB
    ok = available_gb - reserved >= need
    why = (f"available {available_gb:.1f} GB - reserved {reserved:.1f} GB "
           f"{'>=' if ok else '<'} peak {peak_gb:.1f} + margin {MARGIN_GB:.1f} GB")
    return ok, why, reserved


def status_text(jobs):
    vm = psutil.virtual_memory()
    lines = [f"available {vm.available / GB:.1f} GB of {vm.total / GB:.1f} GB"]
    for j in jobs:
        lines.append(f"  RUNNING pid {j['pid']}: {j['label']} ({j['session']}), declared "
                     f"{j['peak_gb']:.1f} GB ({j.get('basis', 'stated')}), holds {tree_rss(j['pid']) / GB:.1f} GB, since {j['started']}")
    if not jobs:
        lines.append("  no heavy job running")
    big = []
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        try:
            rss = p.info["memory_info"].rss
        except Exception:
            continue
        if rss > BIG_PROCESS_GB * GB:
            big.append((rss, p.info["pid"], p.info["name"]))
    for rss, pid, name in sorted(big, reverse=True):
        lines.append(f"  big process: {name} pid {pid} {rss / GB:.1f} GB")
    hist = _read(paths()[2], [])
    if hist:
        lines.append("  measured peaks (latest per label):")
        latest = {}
        for h in hist:
            latest[h["label"]] = h
        for label, h in sorted(latest.items()):
            lines.append(f"    {label}: {h['measured_gb']:.2f} GB (declared {h['peak_gb']:.1f}, {h['ended']})")
    return "\n".join(lines)


def latest_measured(label, hist):
    """The most recent history entry for `label` with a measured peak, or None."""
    found = [h for h in hist if h.get("label") == label and h.get("measured_gb") is not None]
    return found[-1] if found else None


def resolve_peak(label, given, estimate, hist):
    """The figure a job declares, and what it rests on (owner, 2026-10-03:
    measured figures are the norm). A measured peak is the threshold; a job
    with none declares an estimate scaled from measured ones and says so; only
    a job with neither falls back to DEFAULT_PEAK_GB."""
    last = latest_measured(label, hist)
    if given is None or str(given).lower() == "measured":
        if last:
            return float(last["measured_gb"]), f"measured {last['ended']}"
        if given is not None:
            raise ValueError(f"no measured peak recorded for label {label!r}: declare an "
                             "estimate with --peak-gb N --estimate 'scaled from ...'")
        return DEFAULT_PEAK_GB, "unknown: the per-process cap"
    peak = float(given)
    if estimate:
        return peak, f"estimate, {estimate}"
    if last:
        return peak, f"stated; last measured {last['measured_gb']:.2f} GB"
    return peak, "stated, never measured: give --estimate with its basis"


def admit(label, peak_gb, session, pid, available_gb=None, basis=None):
    """`available_gb` is for the selftest only: the live figure otherwise. A
    selftest that asks the real machine fails whenever other jobs hold its
    memory (2026-09-30)."""
    ledger, lock, _ = paths()
    with Lock(lock):
        jobs = live(_read(ledger, []))
        held = {j["pid"]: tree_rss(j["pid"]) / GB for j in jobs}
        if available_gb is None:
            available_gb = psutil.virtual_memory().available / GB
        ok, why, _ = decide(jobs, peak_gb, available_gb, held)
        if ok:
            jobs.append({"pid": pid, "label": label, "peak_gb": peak_gb, "session": session,
                         "basis": basis or "stated",
                         "started": time.strftime("%Y-%m-%d %H:%M:%S")})
        _write(ledger, jobs)
    return ok, why, jobs


def remove(pid, measured_gb=None):
    ledger, lock, history = paths()
    with Lock(lock):
        # Found BEFORE the dead-pid filter: the job's own child has exited by
        # now, so live() would drop its entry and no peak was ever recorded
        # (the history file never existed until 2026-10-03).
        recorded = _read(ledger, [])
        mine = [j for j in recorded if j["pid"] == pid]
        _write(ledger, [j for j in live(recorded) if j["pid"] != pid])
        if mine and measured_gb is not None:
            hist = _read(history, [])
            hist.append({**mine[0], "measured_gb": round(measured_gb, 2),
                         "ended": time.strftime("%Y-%m-%d %H:%M:%S")})
            _write(history, hist[-200:])


def cmd_run(args, command):
    if not command:
        raise SystemExit("heavy_job run: give the command after --")
    wait_until = time.time() + args.wait * 60
    while True:
        # Admit under a placeholder pid (this process), then hand the entry to the child.
        ok, why, jobs = admit(args.label, args.peak_gb, args.session, os.getpid(), basis=args.basis)
        if ok:
            break
        if time.time() >= wait_until:
            print(f"REFUSED: {args.label}: {why}\n{status_text(jobs)}")
            return 3
        time.sleep(30)
    print(f"ADMITTED: {args.label}: {why}", flush=True)
    peak = 0
    try:
        child = subprocess.Popen(command)
        ledger, lock, _ = paths()
        with Lock(lock):
            jobs = _read(ledger, [])
            for j in jobs:
                if j["pid"] == os.getpid():
                    j["pid"] = child.pid
            _write(ledger, jobs)
        while child.poll() is None:
            peak = max(peak, tree_rss(child.pid))
            time.sleep(2)
        code = child.returncode
    finally:
        remove(child.pid if "child" in locals() else os.getpid(), peak / GB)
    print(f"ENDED: {args.label}: exit {code}, measured peak {peak / GB:.2f} GB")
    return code


def _raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


def selftest():
    """Touches nothing: a temporary ledger, fake pids, fake memory figures."""
    results = []

    def case(name, ok):
        results.append(ok)
        print(f"{'ok  ' if ok else 'FAIL'} {name}")

    job = lambda pid, peak: {"pid": pid, "label": "x", "peak_gb": peak, "session": "t", "started": "t"}
    # Positive control first.
    ok, _, _ = decide([], 5.4, 8.0, {})
    case("an idle machine with 8 GB free admits a 5.4 GB job", ok)
    ok, why, _ = decide([], 5.4, 6.9, {})
    case("5.4 GB + 2 GB margin is refused with 6.9 GB free", not ok and "<" in why)
    ok, _, reserved = decide([job(1, 5.4)], 0.5, 6.0, {1: 1.0})
    case("a just-started 5.4 GB job holding 1 GB reserves 4.4 GB", abs(reserved - 4.4) < 1e-9 and not ok)
    ok, _, _ = decide([job(1, 5.4)], 0.5, 7.0, {1: 5.0})
    case("the same job at 5 GB reserves 0.4, so a 0.5 GB job fits in 7 GB", ok)
    ok, _, _ = decide([job(1, 0.5), job(2, 0.5)], 0.5, 12.0, {})
    case("a third job is admitted when memory allows", ok)
    ok, _, _ = decide([job(1, 0.5), job(2, 0.5), job(3, 0.5)], 0.5, 12.0, {})
    case("a fourth job is admitted when memory allows", ok)
    ok, why, _ = decide([job(n, 0.5) for n in range(1, MAX_JOBS + 1)], 0.5, 12.0, {})
    case(f"job {MAX_JOBS + 1} is refused however much is free", not ok and "at most" in why)
    case("a dead pid is dropped on read", live([job(1, 1), job(2, 1)], alive=lambda p: p == 2) == [job(2, 1)])

    hist = [{"label": "kyoto step 2", "measured_gb": 0.30, "ended": "d1"},
            {"label": "kyoto step 2", "measured_gb": 0.33, "ended": "d2"}]
    case("an omitted peak takes the label's LATEST measured figure",
         resolve_peak("kyoto step 2", None, None, hist) == (0.33, "measured d2"))
    case("'measured' with no record refuses, asking for an estimate",
         _raises(lambda: resolve_peak("osaka step 2", "measured", None, hist)))
    case("an omitted peak with no record falls back to the cap",
         resolve_peak("osaka step 2", None, None, hist)[0] == DEFAULT_PEAK_GB)
    case("an estimate is declared as one, with its basis",
         resolve_peak("osaka step 2", "1.0", "scaled from Kyoto by raw size", hist)
         == (1.0, "estimate, scaled from Kyoto by raw size"))

    old = os.environ.get("HEAVY_JOB_DIR")
    with tempfile.TemporaryDirectory() as d:
        os.environ["HEAVY_JOB_DIR"] = d
        try:
            ok1, _, _ = admit("a", 0.1, "t", os.getpid(), available_gb=8.0)
            case("admit writes the ledger", ok1 and len(_read(paths()[0], [])) == 1)
            remove(os.getpid(), 0.05)
            hist = _read(paths()[2], [])
            case("remove empties the ledger and records the measured peak",
                 _read(paths()[0], []) == [] and bool(hist) and hist[0]["measured_gb"] == 0.05)
            # The real case: the child has already exited when remove() runs.
            gone = subprocess.Popen([sys.executable, "-c", "pass"])
            gone.wait()
            _write(paths()[0], [job(gone.pid, 0.2)])
            remove(gone.pid, 0.07)
            hist = _read(paths()[2], [])
            case("a job whose child has exited still records its measured peak",
                 _read(paths()[0], []) == []
                 and hist[-1]["measured_gb"] == 0.07)
            lock = paths()[1]
            lock.write_text("")
            os.utime(lock, (time.time() - 120, time.time() - 120))
            with Lock(lock, timeout=2):
                pass
            case("a stale lock (over a minute old) is broken", not lock.exists())
        finally:
            if old is None:
                os.environ.pop("HEAVY_JOB_DIR", None)
            else:
                os.environ["HEAVY_JOB_DIR"] = old
    print(f"{sum(results)} of {len(results)} selftest cases pass")
    return 0 if all(results) else 1


def main():
    argv = sys.argv[1:]
    if argv[:1] == ["--selftest"]:
        return selftest()
    command = []
    if "--" in argv:
        i = argv.index("--")
        argv, command = argv[:i], argv[i + 1:]
    ap = argparse.ArgumentParser(description="The heavy-job gate (see the module docstring).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("run", "start"):
        s = sub.add_parser(name)
        s.add_argument("--label", required=True)
        s.add_argument("--peak-gb", default=None,
                       help="a number, or 'measured'; omitted means the label's last measured "
                            f"peak, else {DEFAULT_PEAK_GB} GB")
        s.add_argument("--estimate", default=None, metavar="BASIS",
                       help="marks --peak-gb as an estimate and says what it was scaled from")
        s.add_argument("--session", required=True)
        if name == "run":
            s.add_argument("--wait", type=float, default=0, help="minutes to keep retrying if refused")
        else:
            s.add_argument("--pid", type=int, required=True, help="the job's own pid")
    e = sub.add_parser("end")
    e.add_argument("--pid", type=int, required=True)
    sub.add_parser("status")
    args = ap.parse_args(argv)
    if args.cmd in ("run", "start"):
        try:
            args.peak_gb, args.basis = resolve_peak(
                args.label, args.peak_gb, args.estimate, _read(paths()[2], []))
        except ValueError as exc:
            raise SystemExit(f"heavy_job: {exc}")
        print(f"DECLARED: {args.label}: {args.peak_gb:.2f} GB ({args.basis})", flush=True)

    if args.cmd == "run":
        return cmd_run(args, command)
    if args.cmd == "start":
        ok, why, jobs = admit(args.label, args.peak_gb, args.session, args.pid, basis=args.basis)
        print(("ADMITTED: " if ok else "REFUSED: ") + f"{args.label}: {why}")
        if not ok:
            print(status_text(jobs))
        return 0 if ok else 3
    if args.cmd == "end":
        remove(args.pid)
        print(f"ended pid {args.pid}")
        return 0
    ledger = paths()[0]
    print(status_text(live(_read(ledger, []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
