"""Does a script's selftest fail when one of its rules is broken? A selftest
that cannot fail proves nothing, so each rule is broken in a temporary copy
and the selftest is run on the copy.

    python scripts/rule_breaks.py SCRIPT BREAKS_JSON [--arg --selftest]
    python scripts/rule_breaks.py --selftest

BREAKS_JSON is a JSON list of objects {"label": ..., "old": ..., "new": ...}.
For each, `old` must occur exactly once in SCRIPT; it is replaced by `new` in
a copy written beside nothing of the repository (a temporary folder), and the
copy is run with --selftest (or the arguments after --arg). A break is CAUGHT
when the copy exits non-zero, MISSED when it exits 0. The script as it stands
is run first and must exit 0.

Exits non-zero when any break is MISSED, when a break's `old` text does not
occur exactly once (the break list is stale, which is said by label), when
the unbroken script fails, or when the input cannot be read. A MISSED break
is either a rule no case tests or a break that changes nothing: say which in
the review, never drop it from the list.

A copy runs from a temporary folder, so a script that finds the repository
through its own path (ROOT = Path(__file__)...) will not find it there. That
is right for a selftest, which must build what it needs in a temporary tree;
a selftest that reads the repository cannot be judged by this tool.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_copy(path, args, timeout=600):
    """Exit code and the BAD lines of one run of a script copy."""
    proc = subprocess.run([sys.executable, str(path), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)
    bad = [ln.strip() for ln in (proc.stdout + proc.stderr).splitlines() if "BAD" in ln]
    return proc.returncode, bad


def check(script, breaks, args, out=print):
    """Run every break; return 0 only when the script passes unbroken and
    every break is caught."""
    try:
        source = Path(script).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        out(f"cannot read {script}: {exc}")
        return 1
    with tempfile.TemporaryDirectory(prefix="rule_breaks_") as tmp:
        copy = Path(tmp) / Path(script).name
        copy.write_bytes(source.encode("utf-8"))
        code, _ = run_copy(copy, args)
        if code != 0:
            out(f"{script}: fails before any rule is broken (exit {code}); nothing to judge")
            return 1
        caught = missed = stale = 0
        for i, item in enumerate(breaks, 1):
            label = item.get("label") or f"break {i}"
            old, new = item.get("old"), item.get("new")
            if not isinstance(old, str) or not isinstance(new, str) or not old or old == new:
                out(f"STALE   {label}: needs an 'old' text and a different 'new' text")
                stale += 1
                continue
            n = source.count(old)
            if n != 1:
                out(f"STALE   {label}: its 'old' text occurs {n} times in {Path(script).name}, not once")
                stale += 1
                continue
            copy.write_bytes(source.replace(old, new).encode("utf-8"))
            code, bad = run_copy(copy, args)
            if code != 0:
                caught += 1
                out(f"caught  {label}" + (f": {bad[0][:110]}" if bad else f": exit {code}"))
            else:
                missed += 1
                out(f"MISSED  {label}: the selftest still passes")
    out(f"\n{caught} caught, {missed} missed, {stale} stale, of {len(breaks)} rule breaks.")
    return 0 if breaks and not missed and not stale else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("script")
    ap.add_argument("breaks_json")
    ap.add_argument("--arg", action="append", default=None, metavar="ARG",
                    help="an argument for the copy instead of --selftest; repeat for several")
    args = ap.parse_args(argv)
    try:
        breaks = json.loads(Path(args.breaks_json).read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"cannot read {args.breaks_json}: {exc}")
        return 1
    if not isinstance(breaks, list) or not all(isinstance(b, dict) for b in breaks):
        print(f"{args.breaks_json}: must hold a JSON list of objects with label, old and new")
        return 1
    return check(args.script, breaks, args.arg or ["--selftest"])


def selftest():
    cases = []

    def report(label, ok):
        cases.append(ok)
        print(f"  {'ok ' if ok else 'BAD'} {label}")

    target = ("import sys\n"
              "def even(n):\n"
              "    return n % 2 == 0\n"
              "def unused(n):\n"
              "    return n + 1\n"
              "ok = even(4) and not even(3)\n"
              "print('ok' if ok else 'BAD even')\n"
              "sys.exit(0 if ok else 1)\n")
    with tempfile.TemporaryDirectory(prefix="rule_breaks_selftest_") as tmp:
        tmp = Path(tmp)
        script = tmp / "target.py"
        script.write_bytes(target.encode("utf-8"))

        def run(breaks, path=script):
            lines = []
            return check(str(path), breaks, ["--selftest"], out=lines.append), "\n".join(lines)

        rc, text = run([{"label": "parity flipped", "old": "n % 2 == 0", "new": "n % 2 == 1"}])
        report("a break the selftest catches is CAUGHT and the exit code is 0",
               rc == 0 and "caught  parity flipped" in text and "1 caught, 0 missed" in text)

        rc, text = run([{"label": "untested function", "old": "return n + 1", "new": "return n + 2"}])
        report("a break no case tests is MISSED and the exit code is non-zero",
               rc != 0 and "MISSED  untested function" in text)

        rc, text = run([{"label": "gone", "old": "no such text", "new": "x"}])
        report("a break whose text is not in the script is STALE, named, exit non-zero",
               rc != 0 and "STALE   gone" in text and "occurs 0 times" in text)

        rc, text = run([{"label": "twice", "old": "return n", "new": "return 0 * n"}])
        report("a break whose text occurs twice is STALE, not applied to the first",
               rc != 0 and "occurs 2 times" in text)

        rc, text = run([])
        report("an empty break list is no pass", rc != 0)

        failing = tmp / "failing.py"
        failing.write_bytes(b"import sys\nsys.exit(1)\n")
        rc, text = run([{"label": "x", "old": "exit(1)", "new": "exit(2)"}], path=failing)
        report("a script that fails unbroken is refused before any break runs",
               rc != 0 and "fails before any rule is broken" in text and "caught" not in text)

        breaks_file = tmp / "breaks.json"
        breaks_file.write_bytes(json.dumps(
            [{"label": "parity flipped", "old": "n % 2 == 0", "new": "n % 2 == 1"}]).encode("utf-8"))
        report("main: the entry point reads the files and returns the result's exit code",
               main([str(script), str(breaks_file)]) == 0)
        breaks_file.write_bytes(b'{"not": "a list"}')
        report("main: a breaks file that is not a list is refused",
               main([str(script), str(breaks_file)]) != 0)
        report("main: a breaks file that does not exist is refused",
               main([str(script), str(tmp / "none.json")]) != 0)

    good = sum(cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:] == ["--selftest"] else main())
