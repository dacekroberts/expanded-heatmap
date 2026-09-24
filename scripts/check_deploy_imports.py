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
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path


# A CLONE ON WINDOWS CANNOT BE DELETED WITH A PLAIN rmtree. Git writes its pack
# files read-only, and Windows refuses to delete a read-only file, so every
# run until 2026-09-23 left `.git/objects/pack/pack-*.{idx,pack,rev}` behind:
# 53 `deploy-imports-*` folders, 1.7 GB, found by Oslo's deploy-verify. The
# old `ignore_errors=True` is why nobody saw it. So: clear the read-only bit
# and retry, and SAY so if a folder still will not go.
def _make_writable_and_retry(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path):
    handler = ({"onexc": _make_writable_and_retry} if sys.version_info >= (3, 12)
               else {"onerror": _make_writable_and_retry})
    try:
        shutil.rmtree(path, **handler)
    except OSError as e:
        print(f"  WARNING: could not remove {path}: {e}", file=sys.stderr)


# Clones older than this came from an earlier run, not a concurrent one, so
# they are cleared at the start of every run - which also cleared the backlog.
STALE_AFTER_S = 2 * 3600


def remove_stale_clones():
    cutoff = time.time() - STALE_AFTER_S
    for old in Path(tempfile.gettempdir()).glob("deploy-imports-*"):
        if old.is_dir() and old.stat().st_mtime < cutoff:
            remove_tree(old)

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

# --- page chrome: every one of these caught a real defect on 2026-09-22 -----
import re as _re
try:
    from cities import CITIES as _C
    by_page = {c["page"].split("/")[-1]: c for c in _C}
    import pathlib as _p
    for f in sorted(_p.Path("app/pages").glob("*_Heatmap.py")):
        src = f.read_text(encoding="utf-8")
        city = by_page.get(f.name)
        if city is None:
            problems.append(f"{f.name}: no cities.py entry points at this page")
            continue
        # Chicago's terms require its disclaimer wherever the app is accessed.
        # Four pages shipped without this because the scaffold template omitted
        # it; on those pages the notices were ABSENT, not collapsed.
        if "render_site_notices()" not in src:
            problems.append(f"{f.name}: never calls render_site_notices() - "
                            "the five mandatory notices would be absent")
        m = _re.search(r'render_city_nav\("([^"]+)"\)', src)
        if not m:
            problems.append(f"{f.name}: never calls render_city_nav()")
        elif m.group(1) != city["name"]:
            problems.append(
                f"{f.name}: render_city_nav({m.group(1)!r}) does not match "
                f"cities.py name {city['name']!r} - inert under MAP_ONLY_NAV, "
                "wrong the moment that flag flips")
        t = _re.search(r'page_title="([^"]+)"', src)
        if t and not t.group(1).startswith(city["name"]):
            problems.append(f"{f.name}: page_title {t.group(1)!r} does not "
                            f"start with {city['name']!r}")
    for d in sorted(_p.Path("outputs").iterdir()):
        if d.is_dir() and not (d / "heatmap.html").exists():
            problems.append(f"outputs/{d.name}/ has no heatmap.html")
except Exception:
    problems.append("page-chrome checks raised:\n" + traceback.format_exc())

# --- macro-map label collisions --------------------------------------------
# Label pills are placed by PIXEL offsets at a pinned zoom, so every added city
# can collide with an existing one, and the failure is invisible until someone
# looks at the map. Boston and Toronto overlapped by 30x12 px unnoticed. This
# model reproduced four pixel-measured pills to within 2 px on 2026-09-22.
try:
    import math
    from cities import CITIES as _ALL, IN_DEFAULT_VIEW as _IDV
    from cities import REGION_ORDER as _RO, cities_in as _cities_in

    # ⚠ SCORE ONLY THE CITIES THIS VIEW ACTUALLY LABELS, which since
    # 2026-09-23 is the region's own and no longer every city on earth.
    # `Overview.py` dropped the composite's exemption after measuring that all
    # three collisions in the landing view involved a NON-MEMBER and 6 of its
    # 13 non-member labels were drawn off-canvas at 375 px anyway.
    #
    # This check kept its OWN copy of the collision model - a second
    # implementation of check_macro_labels.py's geometry - so it went on
    # reporting two Marseille overlaps that the app no longer draws. Caught by
    # running it, which is the argument for running it. The duplication itself
    # is left standing deliberately: this file must work from a CLEAN CLONE
    # with only the lean venv, so importing the other script is not free.
    # Recorded in PLAN.md as worth unifying.
    _CC = _cities_in(_RO[0])
    _MARKERS = _ALL          # every city still renders a DOT in every view

    def _fit(lats, lons, w=320, h=460, fill=0.7, west_pad=0.12):
        lon_min = min(lons) - west_pad * max(max(lons) - min(lons), 0.5)
        lat_span = max(max(lats) - min(lats), 0.5)
        lon_span = max(max(lons) - lon_min, 0.5)
        clat = (max(lats) + min(lats)) / 2
        zl = math.log2(w * 360 * fill / (512 * lon_span))
        za = math.log2(h * 360 * fill * math.cos(math.radians(clat)) / (512 * lat_span))
        return max(1.0, min(zl, za, 9.0)), clat, (max(lons) + lon_min) / 2

    ZOOM, CLAT, CLON = _fit([c["lat"] for c in _IDV], [c["lon"] for c in _IDV])
    SCALE = 512 * (2 ** ZOOM)
    DEFAULT_OFFSET = ("middle", 0, -22)
    CHAR_W, PAD_W, PILL_H = 7.0, 11.0, 17.0

    def _mercy(lat):
        return (1 - math.log(math.tan(math.radians(lat)) +
                             1 / math.cos(math.radians(lat))) / math.pi) / 2

    def _box(c, W):
        off = c.get("label_offset") or DEFAULT_OFFSET
        anchor, dx, dy = off
        x = (c["lon"] - CLON) / 360 * SCALE + W / 2
        y = (_mercy(c["lat"]) - _mercy(CLAT)) * SCALE + 460 / 2
        w = CHAR_W * len(c["name"]) + PAD_W
        cx = x + dx
        # background_padding=[5,2]: the pill extends 5 px past the text anchor
        x0 = cx - w / 2 if anchor == "middle" else (cx - 5 if anchor == "start"
                                                   else cx + 5 - w)
        y0 = y + dy - PILL_H / 2
        return x0, x0 + w, y0, y0 + PILL_H

    seen = set()
    for W in (343, 726, 1030):          # 375 / 768 / 1200 px viewports
        boxes = {c["name"]: _box(c, W) for c in _CC}
        names = sorted(boxes)
        for i, n1 in enumerate(names):
            for n2 in names[i + 1:]:
                a, b = boxes[n1], boxes[n2]
                ox = min(a[1], b[1]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[2], b[2])
                # >1 px on BOTH axes, not >0. Pills that ABUT are fine and
                # common - deploy-verify measured Toronto and New York touching
                # at 0 px from rendered pixels and reported it as clearance,
                # not collision. Flagging a sub-pixel touch would make this
                # check fail permanently, and a check that always fails is a
                # check somebody disables. Real collisions are tens of pixels:
                # Boston/Toronto was 30x12, Philadelphia/Washington D.C. was
                # 102x13.
                if ox > 1 and oy > 1 and (n1, n2) not in seen:
                    seen.add((n1, n2))
                    problems.append(
                        f"macro map: {n1!r} and {n2!r} labels overlap by "
                        f"{ox:.0f}x{oy:.0f} px - adjust label_offset in "
                        "cities.py (offsets are PIXELS at a pinned zoom)")
        for c in _CC:
            if _box(c, W)[0] < 0 and c["name"] not in ("Vancouver (Regional)",):
                problems.append(f"macro map: {c['name']!r} label is clipped by "
                                f"the west edge at a {W}px canvas")
            # A LABEL MUST NOT COVER ITS OWN MARKER. The pills are opaque
            # (alpha 235), so a pill over a dot erases the dot - Guadalajara
            # shipped with no visible marker on 2026-09-22 because
            # ("end", 12, 0) put its pill across its own point, and the owner
            # found it by looking at the map rather than any check finding it.
            #
            # Deliberately ONLY the city's own dot. Pills covering OTHER
            # cities' dots happen in the east-coast cluster by design - the
            # dots there are 6-15 px apart and cities.py documents that as an
            # accepted trade-off - so flagging those would be noise.
            x0, x1, y0, y1 = _box(c, W)
            dx_, dy_ = ((c["lon"] - CLON) / 360 * SCALE + W / 2,
                        (_mercy(c["lat"]) - _mercy(CLAT)) * SCALE + 230)
            if (x0 - 5 < dx_ < x1 + 5) and (y0 - 5 < dy_ < y1 + 5):
                key = ("owndot", c["name"])
                if key not in seen:
                    seen.add(key)
                    problems.append(
                        f"macro map: {c['name']!r} label pill covers its own "
                        "marker - the dot will be invisible. A pill is 17 px "
                        "tall and a marker 5 px in radius, so |dy| >= 14, or "
                        "move it clear horizontally.")
except Exception:
    problems.append("label-collision check raised:\n" + traceback.format_exc())

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

    remove_stale_clones()
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
            remove_tree(tmp)
            if tmp.exists():
                print(f"  WARNING: clone left behind at {tmp}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
