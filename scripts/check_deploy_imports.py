"""Import smoke test against a CLEAN CLONE, in the lean deploy environment.

WHY THIS EXISTS. On 2026-09-22 the live app was down for over three hours with
`ImportError: cannot import name 'DEFAULT_REGION' from 'cities'`, and every
check this project had reported green throughout. Two defects in one file got
past them:

  1. `app/cities.py` gained `DEFAULT_REGION`/`REGIONS`, `app/Overview.py`
     started importing them, and a deployment that had one file and not the
     other could not import at all.
  2. Mexico City was added with no `label_offset`, so `pd.DataFrame(CITIES)`
     filled it with `float('nan')`, `nan is None` was False, and `tuple(nan)`
     raised `TypeError` on every page load.

Neither was reachable by the existing checks, and the reason is structural:

  * `drift_check.py` runs the PIPELINE. It never imports `app/`.
  * `deploy-verify` runs the app, but from the WORKING TREE and always in a
    FRESH process - so it cannot see an uncommitted file, and it cannot see a
    stale module in a long-running process by construction.

So this script does the two things neither can: it runs against a clean clone
of a committed ref (what a deploy actually gets), and it checks the app's
module-level imports and the specific data shapes that have broken it.

It does NOT start a server and is not a substitute for `deploy-verify`. It is
the cheap check to run before every push that touches `app/` or `pipeline/`.

    python scripts/check_deploy_imports.py            # HEAD
    python scripts/check_deploy_imports.py --ref origin/master
"""

import argparse
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEAN = REPO / ".venv-lean" / "Scripts" / "python.exe"
if not LEAN.exists():                       # macOS/Linux layout
    LEAN = REPO / ".venv-lean" / "bin" / "python"

# Runs INSIDE the clone, under the lean interpreter. Kept as a string so the
# clone needs nothing copied into it but this file.
INNER = r'''
import ast, importlib, os, sys, traceback

ROOT = os.path.abspath(".")
# Streamlit puts the entry script's directory first, then the repo root is
# reachable because components.py inserts it. Mirror both.
sys.path.insert(0, os.path.join(ROOT, "app"))
sys.path.insert(1, ROOT)

problems = []


def module_level_imports(path):
    """(module, [names]) for every top-level import in one file."""
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module, [a.name for a in node.names]
        elif isinstance(node, ast.Import):
            for a in node.names:
                yield a.name, []


targets = ["app/Overview.py", "app/components.py", "app/cities.py"]
targets += sorted(str(p) for p in
                  __import__("pathlib").Path("app/pages").glob("*.py"))

for f in targets:
    for mod, names in module_level_imports(f):
        # third-party (streamlit, pandas, pydeck) is the lean venv's job, and
        # an ImportError there is a real finding too.
        try:
            m = importlib.import_module(mod)
        except Exception as exc:
            problems.append(f"{f}: import {mod} -> {type(exc).__name__}: {exc}")
            continue
        for n in names:
            if n == "*":
                continue
            if not hasattr(m, n):
                problems.append(
                    f"{f}: cannot import name {n!r} from {mod!r} "
                    f"({getattr(m, '__file__', '?')})")

# --- the data shapes that have actually broken this app --------------------
try:
    import pandas as pd
    from cities import CITIES, REGION_ORDER

    missing = [c["name"] for c in CITIES if "label_offset" not in c]
    if missing:
        problems.append(
            "cities.py: %s declare no label_offset. pd.DataFrame fills the "
            "missing key with float('nan'), which is NOT None - this took the "
            "Overview down on 2026-09-22." % missing)

    col = pd.DataFrame(CITIES).get("label_offset")
    if col is not None:
        nan = int(col.isna().sum())
        if nan:
            problems.append(f"cities.py: label_offset has {nan} NaN value(s)")

    untagged = [c["name"] for c in CITIES if c.get("region") not in REGION_ORDER]
    if untagged:
        problems.append(f"cities.py: {untagged} have no region in REGION_ORDER")

    for c in CITIES:
        p = os.path.join("app", c["page"])
        if not os.path.exists(p):
            problems.append(f"cities.py: {c['name']} page missing: {c['page']}")
except Exception:
    problems.append("cities.py data checks raised:\n" + traceback.format_exc())

# --- the app must not pull the pipeline's heavy deps into the deploy -------
HEAVY = ("folium", "geopandas", "shapely", "pyproj", "fiona", "pyogrio", "branca")
for mod in HEAVY:
    if mod in sys.modules:
        problems.append(f"{mod} was imported by app code - it is not in "
                        "requirements.txt and will break the deploy")

for p in problems:
    print("FAIL", p)
print("PROBLEMS", len(problems))
sys.exit(1 if problems else 0)
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", default="HEAD",
                    help="git ref to test (default HEAD; use origin/master to "
                         "test exactly what a deploy would pull)")
    ap.add_argument("--keep", action="store_true",
                    help="keep the clone for inspection")
    args = ap.parse_args()

    if not LEAN.exists():
        sys.exit(f"No lean venv at {LEAN}. Build it first:\n"
                 "  python -m venv .venv-lean\n"
                 "  .venv-lean/Scripts/python.exe -m pip install -r requirements.txt")

    tmp = Path(tempfile.mkdtemp(prefix="deploy-imports-"))
    clone = tmp / "repo"
    try:
        print(f"cloning {args.ref} -> {clone}")
        subprocess.run(["git", "clone", "--quiet", "--no-local", str(REPO), str(clone)],
                       check=True)
        subprocess.run(["git", "-C", str(clone), "checkout", "--quiet", args.ref],
                       check=True)
        head = subprocess.run(["git", "-C", str(clone), "log", "--oneline", "-1"],
                              capture_output=True, text=True).stdout.strip()
        print(f"  at {head}")

        # A clone has no __pycache__, which is exactly the point: a stale .pyc
        # is one of the things this check exists to make impossible.
        inner = clone / "_deploy_import_check.py"
        inner.write_text(INNER, encoding="utf-8")
        r = subprocess.run([str(LEAN), str(inner)], cwd=str(clone),
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.stderr.strip():
            sys.stderr.write(r.stderr)
        if r.returncode == 0:
            print("\nRESULT: clean clone imports cleanly under the lean venv")
        else:
            print("\nRESULT: FAILED - this is what the deploy would do")
        return r.returncode
    finally:
        if args.keep:
            print(f"clone kept at {clone}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
