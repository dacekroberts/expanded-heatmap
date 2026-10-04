"""Watch scripts/check_no_fetch_in_steps.py fail, twelve ways.

    python scripts/check_no_fetch_in_steps_selftest.py

WHY. A check that has only ever been seen to pass is an assertion about its
author's intent, not about the code. The `consistency-sweep` rule is "never
ship a check you have not watched fail", and this project has twice shipped a
limb that was quietly examining nothing: `check_provenance.py`'s CRS limb
parsed 0 of 16 longitudes while printing green, because negative numbers are
`ast.UnaryOp` rather than `ast.Constant`. Watching it once is not enough
either: the next person to edit the check inherits the claim, not the
evidence.

NOTHING IN THE REPOSITORY IS MODIFIED. The files the check reads are copied
once into a temporary tree; each case breaks the copy, runs the check there
with `--root`, and puts the copy back. Mutating the working tree and
restoring it in a `finally` is one Ctrl-C away from a broken repository; the
same in a throwaway tree costs nothing. Reading bytes and patching "...\\n"
patterns against a CRLF working-tree file matches nothing and reports a
working check as broken; hence `read_text`, which normalises newlines,
everywhere below.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_no_fetch_in_steps.py"


def build_tree(dest):
    """The subset the check actually reads: every .py under pipeline/, since
    it follows a step's imports into any of them. Copied rather than
    symlinked so a case can break one."""
    (dest / "scripts").mkdir(parents=True)
    shutil.copy2(CHECK, dest / "scripts" / CHECK.name)
    src_root = ROOT / "pipeline"
    for src in sorted(src_root.rglob("*.py")):
        out = dest / "pipeline" / src.relative_to(src_root)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    return dest


def run(root):
    r = subprocess.run(
        [sys.executable, str(root / "scripts" / CHECK.name), "--root", str(root)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def case(root, label, rel, mutate, expect_in, expect_code=1):
    """`rel` and `mutate` are one path and one function, or two tuples of
    the same length when a case needs to break more than one file. `root` is
    the shared throwaway copy; every file broken here is put back before the
    next case."""
    if isinstance(rel, str):
        rel, mutate = (rel,), (mutate,)
    originals = {}
    try:
        for r, m in zip(rel, mutate):
            p = root / r
            originals[p] = p.read_bytes()
            text = p.read_text(encoding="utf-8")  # normalises CRLF - see above
            changed = m(text)
            if changed == text:
                print(f"BROKEN TEST  {label}\n      the mutation of {r} "
                      f"matched nothing, so this case proves nothing about "
                      f"the check")
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
    finally:
        for p, data in originals.items():
            p.write_bytes(data)


CASES = [
    # A step reaching for the network itself.
    ("a step imports an HTTP client again",
     "pipeline/guadalajara/step1_stations.py",
     lambda t: t.replace("import json\n", "import json\nimport requests\n", 1),
     "pipeline/guadalajara/step1_stations.py", 1),

    # The transitive limb. A guarded module is reported and classified, never
    # silently passed.
    ("a step importing a guarded shared module is classified, not failed",
     "pipeline/guadalajara/step1_stations.py",
     # Anchored on the import's opening line: Guadalajara's step 1 imports
     # several names from pipeline.stations since 2026-10-04.
     lambda t: t.replace(
         "from pipeline.stations import (",
         "from pipeline.census_geocoder import geocode_addresses\n"
         "from pipeline.stations import (", 1),
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

    # A helper inside the step's own city folder, which the check did not
    # read before 2026-10-02 (the Seattle (Regional) build's finding).
    ("a city helper a step imports fetches at import",
     "pipeline/seattle/sno_food.py",
     lambda t: t.replace("import pandas as pd\n",
                         "import pandas as pd\nimport requests\n", 1),
     "reaches via pipeline.seattle.sno_food", 1),

    # The same helper reached by a bare sibling import, which works because a
    # step run as a script has its own folder first on sys.path.
    ("a city helper imported by bare name fetches",
     ("pipeline/seattle/sno_food.py",
      "pipeline/seattle/step2_clean_businesses.py"),
     (lambda t: t.replace("import pandas as pd\n",
                          "import pandas as pd\nimport urllib.request\n", 1),
      lambda t: t.replace("    from pipeline.seattle import sno_food\n",
                          "    import sno_food\n", 1)),
     "reaches via pipeline.seattle.sno_food", 1),

    # The fence is the HTTP import inside `def fetch`; hoisted out of it, the
    # helper fetches at import.
    ("a fenced helper's HTTP import hoisted to module level",
     "pipeline/seattle/lcb_offpremise.py",
     lambda t: t.replace("    import requests\n", "", 1).replace(
         "import numpy as np\n", "import numpy as np\nimport requests\n", 1),
     "reaches via pipeline.seattle.lcb_offpremise", 1),

    # ... and the fence holds only while no step calls it.
    ("a step calls a helper's fetch()",
     "pipeline/seattle/step2_clean_businesses.py",
     lambda t: t.replace("    lcb = lcb_offpremise.load()\n",
                         "    lcb_offpremise.fetch()\n"
                         "    lcb = lcb_offpremise.load()\n", 1),
     "calls pipeline.seattle.lcb_offpremise.fetch()", 1),

    # ... nor the helper itself, from what a step does call.
    ("a fenced helper's load() calls its own fetch()",
     "pipeline/seattle/lcb_offpremise.py",
     lambda t: t.replace("    out = place(premises(verbose), verbose)\n",
                         "    fetch()\n"
                         "    out = place(premises(verbose), verbose)\n", 1),
     "calls pipeline.seattle.lcb_offpremise.fetch()", 1),

    # A taxonomy module is loaded by name through importlib, which no import
    # statement shows; reaching pipeline.taxonomies reaches all of them.
    ("a taxonomy module fetches",
     "pipeline/taxonomies/naics.py",
     lambda t: "import requests\n" + t,
     "pipeline.taxonomies.naics", 1),

    # A KNOWN_GAPS list that cannot expire becomes a place defects go to be
    # forgotten. The case writes into an EMPTY table, the state the list
    # should normally be in; aimed at a real entry, it stops matching the day
    # that entry is fixed (Madrid's, 2026-09-22).
    ("a KNOWN_GAPS entry that has quietly been fixed",
     "scripts/check_no_fetch_in_steps.py",
     lambda t: t.replace(
         "KNOWN_GAPS = {}",
         'KNOWN_GAPS = {\n'
         '    "pipeline/toronto/step1_stations.py":\n'
         '        "invented by the self-test; toronto does not fetch.",\n'
         '}', 1),
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
    # One copy for every case: the whole pipeline tree copied per case cost
    # a minute. The unmodified run comes last, so it also proves each case
    # put back what it broke.
    with tempfile.TemporaryDirectory() as d:
        root = build_tree(Path(d))
        results = [case(root, *c) for c in CASES]
        code, _ = run(root)
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
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
