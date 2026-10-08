"""Fail when one transit line carries two colours across the site's maps.

    python scripts/check_line_identity.py                # the gate (check_all.py runs it)
    python scripts/check_line_identity.py --rendered     # also the committed maps' legends
    python scripts/check_line_identity.py --neighbours   # also the neighbour rule (off by default)
    python scripts/check_line_identity.py --verbose      # list every neighbour pair

THE RULE (owner, 2026-10-07, a hard line): a line drawn on more than one
city's map has one colour on every map. pipeline/line_registry.py holds those
lines, one entry each (identity: operator plus public line). Before it the JR
Kobe Line was five colours on six maps.

WHAT IT CHECKS
--------------
  A. Every registered line's colour, as each city config that draws it resolves
     it, is the registry's. A config key the registry names and the config
     lacks fails too (a renamed key leaves the registry stale).
  B. Every INHERITED page draws each line its parent draws in the parent's
     colour (committed legends, by line name).
  C. No two maps draw what looks like one line without an entry joining them:
       - the same line name (a leading line code allowed: Tokyo's "KO Keio
         Line" is "Keio Line") over at least OVERLAP_M of shared track, from
         the committed maps' polylines;
       - in Japan, the same public name under one operator in two cities'
         configs (MLIT N02's operator names; Tokyo's and Kyoto's Tozai Lines
         are different operators and do not match).
     Such a pair passes when the registry joins both under one identity, when
     the pages are an INHERITED pair, or when NOT_SAME parts them.
  --rendered: each registered line's legend colour on its committed map is the
     registry's. Off in the gate, because a config change reaches the map only
     at the next render; drift_check.py catches a stale map. Run it after a
     re-render.
  --neighbours: THE NEIGHBOUR RULE, OPEN WITH THE OWNER and OFF by default.
     Two DIFFERENT lines on two different maps, within NEIGHBOUR_M of each
     other, drawn within linecolour.HARD_FLOOR of one colour (Higashimurayama's
     Seibu Tamako Line and Tokorozawa's Seibu Yamaguchi Line, both #A06030).
     Every run prints the count; the flag makes a pair fail.

Colours come from the configs where a config names the line (dict entries'
`colour`, the Korean tuples' second field, LINE_COLOURS, LINE_COLOUR) and
from the committed legend otherwise. Geometry is measured in metres in a local
equirectangular projection about each line pair, never in degrees.
"""
import argparse
import importlib
import json
import math
import re
import sys
from collections import defaultdict
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shapely.geometry import MultiLineString  # noqa: E402

from pipeline import line_registry as reg  # noqa: E402
from pipeline.linecolour import HARD_FLOOR, delta_e  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Shared track a same-named pair must run over to count as one line. The
# shortest real pair measured 2026-10-07: 561 m (Fuchu and Tokyo, Keio Line);
# the longest same-named pair that is two lines, none above 300 m.
OVERLAP_M = 500.0
TOL_M = 60.0             # how far apart two drawings of one track may lie
NEIGHBOUR_M = 2000.0     # lines this close on two maps can be read as one

ROW = re.compile(r'class="hm-line-row" data-line="(\d+)".*?background:(#[0-9A-Fa-f]{6});.*?</span>(.*?)\n\s*</div>',
                 re.S)
POLY = re.compile(r'L\.polyline\(\s*(\[\[.*?\]\]),\s*\{[^}]*?"className": "hm-line hm-line-(\d+)"', re.S)


def norm(name):
    s = re.sub(r"\(.*?\)", "", name)
    s = s.replace("ō", "o").replace("ū", "u").replace("Ō", "O")
    return " ".join(s.split()).lower()


def same_name(a, b):
    """Equal names, or one is the other behind a line code of up to four
    characters ("ko keio line" / "keio line")."""
    a, b = norm(a), norm(b)
    if a == b:
        return True
    long_, short = (a, b) if len(a) > len(b) else (b, a)
    head = long_[:-len(short)].strip()
    return long_.endswith(" " + short) and " " not in head and len(head) <= 4


def load_maps():
    """{city: [{label, colour, segs, bbox}]} from every committed map."""
    maps = {}
    for html in sorted((ROOT / "outputs").glob("*/heatmap.html")):
        doc = html.read_text(encoding="utf-8")
        rows = {int(n): (c.upper(), " ".join(unescape(lab).split())) for n, c, lab in ROW.findall(doc)}
        segs = defaultdict(list)
        for arr, n in POLY.findall(doc):
            pts = json.loads(arr)
            if len(pts) > 1:
                segs[int(n)].append(pts)
        lines = []
        for n, (colour, label) in sorted(rows.items()):
            s = segs.get(n, [])
            pts = [p for seg in s for p in seg]
            bbox = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts),
                    max(p[1] for p in pts)) if pts else None
            lines.append(dict(label=label, colour=colour, segs=s, bbox=bbox))
        maps[html.parent.name] = lines
    return maps


def config_lines(city):
    """{key: (name, colour)} as the city's config resolves them, or {}."""
    try:
        cfg = importlib.import_module(f"pipeline.{city}.config")
    except Exception:  # a city whose config cannot load has nothing to compare here
        return {}
    out = {}
    lines = getattr(cfg, "LINES", None)
    if isinstance(lines, dict):
        for k, v in lines.items():
            if isinstance(v, dict) and "colour" in v:
                out[k] = (v.get("name", str(k)), v["colour"].upper())
            elif isinstance(v, tuple) and len(v) > 2 and isinstance(v[1], str) and v[1].startswith("#"):
                out[k] = (v[2], v[1].upper())
    names = getattr(cfg, "LINE_NAMES", {})
    for k, c in (getattr(cfg, "LINE_COLOURS", None) or {}).items():
        if isinstance(c, str) and k not in out:
            out[k] = (names.get(k, str(k)), c.upper())
    if getattr(cfg, "LINE_KEY", None) and getattr(cfg, "LINE_COLOUR", None):
        out[cfg.LINE_KEY] = (getattr(cfg, "LINE_NAME", cfg.LINE_KEY), cfg.LINE_COLOUR.upper())
    return out


def key_for_label(cfg_lines, label):
    """The config key whose name the legend label shows (a line code allowed)."""
    hits = [k for k, (name, _) in cfg_lines.items() if same_name(label, name)]
    exact = [k for k in hits if norm(cfg_lines[k][0]) == norm(label)]
    if exact:
        return exact[0]
    return max(hits, key=lambda k: len(cfg_lines[k][0])) if hits else None


def japan_operators(city):
    """{key: (public name, {N02 operators})} for a city built on japan_step1."""
    step1 = ROOT / "pipeline" / city / "step1_stations.py"
    if not step1.exists() or "japan_step1" not in step1.read_text(encoding="utf-8"):
        return {}
    cfg = importlib.import_module(f"pipeline.{city}.config")
    out = {}
    for k, v in cfg.LINES.items():
        if not isinstance(v, dict):
            continue
        ops = {op for op, _ in v.get("n02", [])} | {leg[0] for leg in v.get("route", [])}
        branch = getattr(cfg, "BRANCHES", {}).get(k)
        if branch:
            ops.add(branch["line"][0])
        out[k] = (v["name"], ops)
    return out


def metres(segs, lat0, lon0):
    kx = 111320.0 * math.cos(math.radians(lat0))
    ky = 110540.0
    return MultiLineString([[((p[1] - lon0) * kx, (p[0] - lat0) * ky) for p in s] for s in segs])


def bbox_near(a, b, pad):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rendered", action="store_true")
    ap.add_argument("--neighbours", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    problems = []

    # A: configs against the registry
    cfgs = {}
    for ident, city, key in reg.members():
        cfgs.setdefault(city, config_lines(city))
        if key not in cfgs[city]:
            problems.append(f"A {ident}: {city}'s config has no line {key!r}")
        elif cfgs[city][key][1] != reg.colour(ident).upper():
            problems.append(f"A {ident}: {city}.{key} draws {cfgs[city][key][1]}, the registry {reg.colour(ident)}")

    maps = load_maps()

    # each legend row's identity and effective colour
    ident_of = {(c, k): i for i, c, k in reg.members()}
    rowinfo = {}
    for city, lines in maps.items():
        cl = cfgs.setdefault(city, config_lines(city))
        for n, ln in enumerate(lines):
            key = key_for_label(cl, ln["label"]) if cl else None
            colour = cl[key][1] if key else ln["colour"]
            rowinfo[(city, n)] = dict(key=key, colour=colour,
                                      ident=ident_of.get((city, key)) or f"{city}:{norm(ln['label'])}")
    for child, parent in reg.INHERITED.items():
        for n, ln in enumerate(maps.get(child, [])):
            for m, pl in enumerate(maps.get(parent, [])):
                if norm(ln["label"]) == norm(pl["label"]):
                    rowinfo[(child, n)]["ident"] = rowinfo[(parent, m)]["ident"]

    # B: inherited pages
    for child, parent in reg.INHERITED.items():
        pc = {norm(ln["label"]): ln["colour"] for ln in maps.get(parent, [])}
        for ln in maps.get(child, []):
            want = pc.get(norm(ln["label"]))
            if want and want != ln["colour"]:
                problems.append(f"B {child} draws {ln['label']} {ln['colour']}, {parent} {want}")

    not_same = {frozenset(p) for p in reg.NOT_SAME}

    def joined(a, b):
        ia, ib = ident_of.get(a), ident_of.get(b)
        if ia and ia == ib:
            return True
        if reg.INHERITED.get(a[0]) == b[0] or reg.INHERITED.get(b[0]) == a[0]:
            return True
        return frozenset((a, b)) in not_same

    # C1: same name over shared track
    cities = sorted(maps)
    found = 0
    for i, ca in enumerate(cities):
        for cb in cities[i + 1:]:
            for na, la in enumerate(maps[ca]):
                for nb, lb in enumerate(maps[cb]):
                    if not (la["bbox"] and lb["bbox"]) or not bbox_near(la["bbox"], lb["bbox"], 0.001):
                        continue
                    if not same_name(la["label"], lb["label"]):
                        continue
                    lat0 = (la["bbox"][0] + la["bbox"][2]) / 2
                    lon0 = (la["bbox"][1] + la["bbox"][3]) / 2
                    ga, gb = metres(la["segs"], lat0, lon0), metres(lb["segs"], lat0, lon0)
                    if ga.intersection(gb.buffer(TOL_M)).length < OVERLAP_M:
                        continue
                    found += 1
                    a = (ca, rowinfo[(ca, na)]["key"] or la["label"])
                    b = (cb, rowinfo[(cb, nb)]["key"] or lb["label"])
                    if not joined(a, b):
                        problems.append(f"C {ca} '{la['label']}' and {cb} '{lb['label']}' share track under one "
                                        f"name but no registry entry joins them")

    # C2: Japan, one operator and one public name in two cities
    jp = {c: japan_operators(c) for c in cities}
    by_name = defaultdict(list)
    for c, lines in jp.items():
        for k, (name, ops) in lines.items():
            by_name[norm(name)].append((c, k, ops))
    for name, items in by_name.items():
        for i, (ca, ka, oa) in enumerate(items):
            for cb, kb, ob in items[i + 1:]:
                if ca != cb and oa & ob and not joined((ca, ka), (cb, kb)):
                    problems.append(f"C {ca}.{ka} and {cb}.{kb} are both {name!r} under "
                                    f"{sorted(oa & ob)} but no registry entry joins them")

    # --rendered
    if args.rendered:
        for ident, city, key in reg.members():
            for n, ln in enumerate(maps.get(city, [])):
                if rowinfo[(city, n)]["key"] == key and ln["colour"] != reg.colour(ident).upper():
                    problems.append(f"R {city}'s map draws {ln['label']} {ln['colour']}, the registry "
                                    f"{reg.colour(ident)} ({ident}): re-render it")

    # neighbour rule
    pairs = []
    for i, ca in enumerate(cities):
        for cb in cities[i + 1:]:
            for na, la in enumerate(maps[ca]):
                ra = rowinfo[(ca, na)]
                for nb, lb in enumerate(maps[cb]):
                    rb = rowinfo[(cb, nb)]
                    if ra["ident"] == rb["ident"] or not (la["bbox"] and lb["bbox"]):
                        continue
                    if not bbox_near(la["bbox"], lb["bbox"], 0.03):
                        continue
                    d = delta_e(ra["colour"], rb["colour"])
                    if d >= HARD_FLOOR:
                        continue
                    lat0 = (la["bbox"][0] + la["bbox"][2]) / 2
                    lon0 = (la["bbox"][1] + la["bbox"][3]) / 2
                    if metres(la["segs"], lat0, lon0).distance(metres(lb["segs"], lat0, lon0)) > NEIGHBOUR_M:
                        continue
                    pairs.append((ca, la["label"], ra["colour"], cb, lb["label"], rb["colour"], d))
    if args.verbose:
        for p in pairs:
            print(f"  neighbours: {p[0]} '{p[1]}' {p[2]} / {p[3]} '{p[4]}' {p[5]} (CIE76 {p[6]:.1f})")
    if args.neighbours:
        problems += [f"N {p[0]} '{p[1]}' {p[2]} and {p[3]} '{p[4]}' {p[5]} are different lines within "
                     f"{NEIGHBOUR_M / 1000:.0f} km at CIE76 {p[6]:.1f}" for p in pairs]

    print(f"check_line_identity: {len(reg.REGISTRY)} registered lines on {len({c for _, c, _ in reg.members()})} "
          f"maps; {found} same-name shared-track pairs; neighbour rule "
          f"{'ON' if args.neighbours else 'off'}: {len(pairs)} pair(s) of different lines within "
          f"{NEIGHBOUR_M / 1000:.0f} km under {HARD_FLOOR:.0f}")
    if problems:
        print(f"\nPROBLEMS {len(problems)}:")
        for p in problems:
            print("  " + p)
        return 1
    print("\nPROBLEMS 0 - every line drawn on more than one map has one colour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
