"""Watch scripts/check_no_fetch_in_steps.py fail, six ways.

    python scripts/check_no_fetch_in_steps_selftest.py

WHY THIS FILE EXISTS. A check that has only ever been seen to pass is an
assertion about its author's intent, not about the code - the
`consistency-sweep` rule is "never ship a check you have not watched fail",
and this project has twice shipped a limb that was quietly examining nothing:
`check_provenance.py`'s CRS limb parsed 0 of 16 longitudes while printing
green, because negative numbers are `ast.UnaryOp` rather than `ast.Constant`.
Watching it once is not enough either, because the next person to edit the
check inherits the claim and not the evidence.

NOTHING IN THE REPOSITORY IS MODIFIED. Every case copies the files the check
reads into a temporary tree, breaks the copy, and runs the check there with
`--root`. An earlier version of this mutated the working tree and restored it
in a `finally`, which is one Ctrl-C away from leaving a broken repository -
and which is also how its first run produced a false result: it read bytes and
patched "...\\n" patterns against a working-tree file that is CRLF, so every
pattern matched nothing and the harness reported a working check as broken.
Hence `read_text`, which normalises newlines, everywhere below.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_no_fetch_in_steps.py"


def build_tree(dest):
    """The subset the check actually reads: shared pipeline modules and every
    city's step files. Copied rather than symlinked so a case can break one."""
    (dest / "scripts").mkdir(parents=True)
    shutil.copy2(CHECK, dest / "scripts" / CHECK.name)
    for src in sorted((ROOT / "pipeline").glob("*.py")):
        out = dest / "pipeline" / src.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    for src in sorted((ROOT / "pipeline").glob("*/step*.py")):
        out = dest / "pipeline" / src.parent.name / src.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    return dest


def run(root):
    r = subprocess.run(
        [sys.executable, str(root / "scripts" / CHECK.name), "--root", str(root)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def case(label, rel, mutate, expect_in, expect_code=1):
    with tempfile.TemporaryDirectory() as d:
        root = build_tree(Path(d))
        p = root / rel
        text = p.read_text(encoding="utf-8")     # normalises CRLF - see above
        changed = mutate(text)
        if changed == text:
            print(f"BROKEN TEST  {label}\n      the mutation matched nothing, "
                  f"so this case proves nothing about the check")
            return False
        p.write_text(changed, encoding="utf-8")
        code, out = run(root)
        hit = [ln for ln in out.splitlines() if expect_in in ln]
        ok = code == expect_code and hit
        verdict = ("PASS" if ok else
                   "DID NOT FAIL" if expect_code == 1 else "WRONG VERDICT")
        print(f"{verdict}  {label}")
        print(f"      exit {code} (wanted {expect_code}); "
              f"{hit[0].strip() if hit else 'expected text not found'}")
        return bool(ok)


CASES = [
    # A step reaching for the network itself.
    ("a step imports an HTTP client again",
     "pipeline/guadalajara/step1_stations.py",
     lambda t: t.replace("import json\n", "import json\nimport requests\n", 1),
     "pipeline/guadalajara/step1_stations.py", 1),

    # The transitive limb, which is what found the three geocode steps. A
    # guarded module is reported and classified, never silently passed.
    ("a step importing a guarded shared module is classified, not failed",
     "pipeline/guadalajara/step1_stations.py",
     lambda t: t.replace(
         "from pipeline.stations import verify_stations",
         "from pipeline.stations import verify_stations\n"
         "from pipeline.census_geocoder import geocode_addresses", 1),
     "reaches via pipeline.census_geocoder", 0),

    # ... and the same step fails the moment the guard goes.
    ("the offline guard removed from a shared module",
     "pipeline/census_geocoder.py",
     lambda t: t.replace("        refuse_if_offline(", "        _gone(", 1),
     "pipeline/los_angeles/step3_geocode.py", 1),

    # A guard nobody arms is worse than no guard.
    ("drift_check no longer arms the guard",
     "pipeline/drift_check.py",
     lambda t: t.replace('offline.NO_NETWORK_ENV: "1"', '"UNUSED": "1"', 1),
     "not armed", 1),

    # A KNOWN_GAPS list that cannot expire becomes a place defects go to be
    # forgotten.
    ("a KNOWN_GAPS entry that has quietly been fixed",
     "scripts/check_no_fetch_in_steps.py",
     lambda t: t.replace(
         '    "pipeline/madrid/step1_stations.py":',
         '    "pipeline/toronto/step1_stations.py":\n'
         '        "invented by the self-test; toronto does not fetch.",\n'
         '    "pipeline/madrid/step1_stations.py":', 1),
     "Delete the entry", 1),

    # A glob that matches nothing passes every assertion ever written.
    ("no step files found at all",
     "scripts/check_no_fetch_in_steps.py",
     lambda t: t.replace('PIPELINE.glob("*/step*.py")',
                         'PIPELINE.glob("*/step_NO_SUCH*.py")', 1),
     "vacuously", 1),
]


def main():
    print(f"Self-test for {CHECK.relative_to(ROOT).as_posix()}\n")
    results = [case(*c) for c in CASES]

    with tempfile.TemporaryDirectory() as d:
        code, _ = run(build_tree(Path(d)))
    clean = code == 0
    print(f"\n{'PASS' if clean else 'FAIL'}  an unmodified copy passes "
          f"(exit {code})")

    failed = len([r for r in results if not r]) + (0 if clean else 1)
    print(f"\n{len(results) + 1 - failed} of {len(results) + 1} cases behaved "
          f"as intended.")
    if failed:
        print("\nA case that did not fail means the check does not decide what "
              "it claims to, OR that this self-test's expectation went stale "
              "when the check legitimately changed. Read which before "
              "'fixing' either - on 2026-09-22 the second was true, and the "
              "check was right.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
