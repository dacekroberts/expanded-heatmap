"""Measure the Overview's macro map at the size the site is heading for: every
built city plus the staged ones in docs/staged_cities.json, under each way of
splitting Japan into regions (owner, 2026-10-04: "more regions okay: typical
japanese regions or prefecture").

Nothing in app/ changes. The script copies app/'s modules and
scripts/check_macro_labels.py into a temporary tree, adds the staged cities
to that copy of cities.py, re-tags Japan for the scenario, and runs there:

  1. check_macro_labels.py as written: the label problems hand placement
     would have to clear (staged cities sit at the default offset, above the
     dot, as a new city's entry does until tuned);
  2. the Global competition (app/label_competition.py) run inside each region
     instead, with the region's own labelled cities as the entrants: how many
     names fit and how many go unlabelled;
  3. the menu and list sizes: regions in the menu, cities in the largest
     region's list.

`--compete REGION` (repeatable) puts that region in the copy's
COMPETING_REGIONS, so step 1 scores it as the app would draw it: the check's
problems for it should fall to zero. `--country-view COUNTRY` gives a
country a view of its own (Romania, as Czechia and Belgium have), built and
staged cities alike; `--group "NAME=Country,Country"` makes a region of whole
countries (an Eastern Europe); `--split-meridian LON` cuts what is still
Europe into Europe West and Europe East at a longitude, and
`--snap-countries` keeps each country whole on its mean longitude's side.

Staged names without a measured pill width get an estimate from the table's
own width per character, reported as such; measure them before trusting a
count near the line.

    python scripts/stress_overview.py [--scenario NAME ...] [--compete REGION ...]
                                      [--country-view COUNTRY ...] [--group NAME=C1,C2 ...]
                                      [--split-meridian LON [--snap-countries]] [--keep DIR]

Scenarios: now (Japan West / Japan East), eight (the eight traditional
regions), eight_osaka (the eight, with Osaka Prefecture a view of its own),
six (Hokkaido and Tohoku together, Chugoku and Shikoku together), pref (one
region per prefecture). Fetches nothing; any Python runs it.
"""
import argparse
import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGED = ROOT / "docs" / "staged_cities.json"

JP8 = {**{"01": "Hokkaido"},
       **{f"{p:02d}": "Tohoku" for p in range(2, 8)},
       **{f"{p:02d}": "Kanto" for p in range(8, 15)},
       **{f"{p:02d}": "Chubu" for p in range(15, 24)},
       **{f"{p:02d}": "Kansai" for p in range(24, 31)},
       **{f"{p:02d}": "Chugoku" for p in range(31, 36)},
       **{f"{p:02d}": "Shikoku" for p in range(36, 40)},
       **{f"{p:02d}": "Kyushu-Okinawa" for p in range(40, 48)}}
SIX = {"Hokkaido": "Hokkaido and Tohoku", "Tohoku": "Hokkaido and Tohoku",
       "Chugoku": "Chugoku and Shikoku", "Shikoku": "Chugoku and Shikoku"}
PREF = dict(zip([f"{p:02d}" for p in range(1, 48)], (
    "Hokkaido Aomori Iwate Miyagi Akita Yamagata Fukushima Ibaraki Tochigi "
    "Gunma Saitama Chiba Tokyo Kanagawa Niigata Toyama Ishikawa Fukui Yamanashi "
    "Nagano Gifu Shizuoka Aichi Mie Shiga Kyoto Osaka Hyogo Nara Wakayama Tottori "
    "Shimane Okayama Hiroshima Yamaguchi Tokushima Kagawa Ehime Kochi Fukuoka Saga "
    "Nagasaki Kumamoto Oita Miyazaki Kagoshima Okinawa").split()))

# The built Japanese cities' prefectures, by display name (cities.py carries
# none). The script stops if a Japanese city is missing here.
BUILT_PREF = {
    "Sapporo": "01", "Hakodate": "01", "Tokyo": "13", "Yokohama": "14", "Kawasaki": "14",
    "Yokosuka": "14", "Utsunomiya": "09", "Toyama": "16", "Fukui": "18", "Toyota": "23",
    "Hamamatsu": "22", "Yokkaichi": "24", "Kobe": "28", "Himeji": "28", "Nishinomiya": "28",
    "Osaka": "27", "Sakai": "27", "Higashiōsaka": "27", "Kyoto": "26", "Ōtsu": "25",
    "Nara": "29", "Hiroshima": "34", "Okayama": "33", "Shimonoseki": "35",
    "Matsuyama": "38", "Kōchi": "39", "Takamatsu": "37", "Fukuoka": "40",
    "Kitakyushu": "40", "Kurume": "40", "Kumamoto": "43", "Nagasaki": "42",
    "Sasebo": "42", "Kagoshima": "46",
}
SCENARIOS = ("now", "six", "eight", "eight_osaka", "pref")


def region_for(scenario, pref, today):
    if scenario == "now":
        return today
    if scenario == "eight":
        return JP8[pref]
    if scenario == "eight_osaka":
        return "Osaka Prefecture" if pref == "27" else JP8[pref]
    if scenario == "six":
        return SIX.get(JP8[pref], JP8[pref])
    return PREF[pref]


def replace_once(text, old, new, what):
    if text.count(old) != 1:
        raise SystemExit(f"stress_overview: cities.py no longer has {what} in the expected "
                         f"form; update replace_once()'s anchor for it")
    return text.replace(old, new)


def build_tree(tmp, scenario, staged, competing=(), country_views=(), groups=None,
               meridian=None, snap=False):
    app = tmp / "app"
    shutil.copytree(ROOT / "app", app, ignore=shutil.ignore_patterns("__pycache__", "pages", "assets"))
    (tmp / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "check_macro_labels.py", tmp / "scripts")

    sys.path.insert(0, str(ROOT / "app"))
    import cities as built
    import label_competition as lc
    sys.path.pop(0)
    jp_built = [c["name"] for c in built.CITIES if c["country"] == "Japan"]
    unknown = sorted(set(jp_built) - set(BUILT_PREF))
    if unknown:
        raise SystemExit(f"stress_overview: add {unknown} to BUILT_PREF")
    today = {c["name"]: c["region"] for c in built.CITIES}
    retag = {n: region_for(scenario, BUILT_PREF[n], today[n]) for n in jp_built}
    retag.update({c["name"]: c["country"] for c in built.CITIES if c["country"] in country_views})
    # A region made of whole countries, cut from wherever they sit today.
    group_of = {k: g for g, ks in (groups or {}).items() for k in ks}
    retag.update({c["name"]: group_of[c["country"]] for c in built.CITIES if c["country"] in group_of})
    rows = []
    for s in staged:
        row = {"name": s["name"], "country": s["country"], "lat": s["lat"], "lon": s["lon"],
               "mode": s["mode"], "coverage": "narrowed", "page": "pages/staged.py",
               "region": (region_for(scenario, s["pref"], s["region"])
                          if s["country"] == "Japan" else
                          s["country"] if s["country"] in country_views else
                          group_of.get(s["country"], s["region"]))}
        if s.get("label_tier"):
            row["label_tier"] = s["label_tier"]
        rows.append(row)
    # EUROPE CUT BY A MERIDIAN (owner, 2026-10-04): what is still tagged
    # Europe goes to Europe West or Europe East by its longitude, or, with
    # `snap`, by its country's mean longitude so no country is cut in two.
    if meridian is not None:
        europe = [(c["name"], c["country"], c["lon"]) for c in built.CITIES
                  if retag.get(c["name"], c["region"]) == "Europe"]
        europe += [(r["name"], r["country"], r["lon"]) for r in rows if r["region"] == "Europe"]
        mean = {}
        for _, k, lon in europe:
            mean.setdefault(k, []).append(lon)
        side = {}
        for name, k, lon in europe:
            x = sum(mean[k]) / len(mean[k]) if snap else lon
            side[name] = "Europe West" if x < meridian else "Europe East"
        retag.update({n: s for n, s in side.items() if n in today})
        for r in rows:
            if r["name"] in side:
                r["region"] = side[r["name"]]

    # Japan's regions in prefecture-code order, north to south.
    first = {}
    for p in list(BUILT_PREF.values()) + [s["pref"] for s in staged if s["country"] == "Japan"]:
        r = region_for(scenario, p, "")
        first[r] = min(first.get(r, p), p)
    jp_regions = (["Japan West", "Japan East"] if scenario == "now"
                  else sorted(first, key=first.get))
    new_regions = list(dict.fromkeys(
        r for r in [row["region"] for row in rows] + list(retag.values())
        if r not in built.REGION_ORDER and r not in jp_regions))
    (tmp / "stage.json").write_text(json.dumps({"retag": retag, "rows": rows}, ensure_ascii=False),
                                    encoding="utf-8")

    src = (app / "cities.py").read_text(encoding="utf-8")
    block = (
        "\nimport json as _json\n"
        f"_STAGE = _json.loads(open({str(tmp / 'stage.json')!r}, encoding='utf-8').read())\n"
        "for _c in CITIES:\n"
        "    if _c['name'] in _STAGE['retag']:\n"
        "        _c['region'] = _STAGE['retag'][_c['name']]\n"
        "    _rof = {k: v for k, v in (_c.get('label_offset_by_region') or {}).items()\n"
        f"            if not (k in ('Japan West', 'Japan East') and {scenario != 'now'!r})\n"
        f"            and not (k == 'Europe' and {meridian is not None!r})}}\n"
        "    if 'label_offset_by_region' in _c:\n"
        "        _c['label_offset_by_region'] = _rof\n"
        "CITIES.extend(_STAGE['rows'])\n"
    )
    src = replace_once(src, "\nIN_DEFAULT_VIEW = ", block + "\nIN_DEFAULT_VIEW = ", "IN_DEFAULT_VIEW")
    jp_lines = "".join(f'    "{r}",\n' for r in jp_regions)
    src = replace_once(src, '    "Japan West",\n    "Japan East",\n', jp_lines, "REGION_ORDER's Japan rows")
    src = replace_once(src, '    "West Asia",\n]', '    "West Asia",\n'
                       + "".join(f'    "{r}",\n' for r in new_regions) + "]", "REGION_ORDER's end")
    jp_tuple = ", ".join(f'"{r}"' for r in jp_regions)
    views = "".join(f', "{c}"' for c in country_views)
    src = replace_once(src, '"Japan West", "Japan East")', jp_tuple + views + ")", "COUNTRY_VIEWS")
    src = replace_once(src, '"East Asia": ("Japan West", "Japan East", ',
                       f'"East Asia": ({jp_tuple}, ', "REGION_LABELS_ALSO")
    if scenario != "now":
        src = replace_once(src, ', "Japan West": 6.0}', "}", "REGION_ZOOM's Japan West")
    if meridian is not None:
        src = replace_once(src, '    "Europe",\n    "France North",',
                           '    "Europe West",\n    "Europe East",\n    "France North",',
                           "REGION_ORDER's Europe")
        src = replace_once(src, 'REGION_ZOOM_WITHOUT = {"Europe": (',
                           'REGION_ZOOM_WITHOUT = {"(Europe before the split)": (', "REGION_ZOOM_WITHOUT")
        src = replace_once(src, '"Europe": ("United Kingdom",)',
                           '"Europe West": ("United Kingdom",)', "REGION_LABELS_ALSO's Europe")
    if competing:
        src = replace_once(src, "\nCOMPETING_REGIONS = ()\n",
                           f"\nCOMPETING_REGIONS = {tuple(competing)!r}\n", "COMPETING_REGIONS")
    (app / "cities.py").write_text(src, encoding="utf-8")

    # Estimated widths for names the table has not measured.
    per_char = sum(lc.TEXT_WIDTH.values()) / sum(len(n) for n in lc.TEXT_WIDTH)
    est = {r["name"]: round(len(r["name"]) * per_char, 1) for r in rows
           if r["name"] not in lc.TEXT_WIDTH}
    lsrc = (app / "label_competition.py").read_text(encoding="utf-8")
    lsrc = replace_once(lsrc, "\nPILL_H = ", f"\nTEXT_WIDTH.update({est!r})\nPILL_H = ",
                        "label_competition.py's PILL_H")
    (app / "label_competition.py").write_text(lsrc, encoding="utf-8")
    return len(est), round(per_char, 2)


def inner(tmp):
    """Runs inside the temporary tree: one scenario's numbers, as JSON."""
    sys.path.insert(0, str(tmp / "app"))
    sys.path.insert(0, str(tmp / "scripts"))
    import cities
    import check_macro_labels as cml
    import label_competition as lc

    sys.argv = ["check_macro_labels.py"]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            cml.main()
        except SystemExit:
            pass
    out = buf.getvalue()
    names = sorted((r["name"] for r in cities.REGIONS), key=len, reverse=True)
    per_region = {}
    in_problems = False
    for line in out.splitlines():
        if line.startswith("PROBLEMS"):
            in_problems = True
            continue
        if in_problems and line.startswith("  "):
            body = line.strip()
            r = next((n for n in names if body.startswith(n)), "(other)")
            per_region[r] = per_region.get(r, 0) + 1
    facts = json.loads((tmp / "app" / "macro_facts.json").read_text(encoding="utf-8"))
    store = facts.get("storefronts", {})
    regions = []
    for region in cities.REGIONS:
        if region["name"] == cities.DEFAULT_REGION or region["name"] in cities.REGION_MEMBERS:
            continue
        clat, clon, zoom = cml.region_view(region)
        # The hand rule's set, not a competing region's winners.
        saved = cml.REGION_WON.pop(region["name"], None)
        labelled = cml.scored_labels(region, clat, clon, zoom)
        if saved is not None:
            cml.REGION_WON[region["name"]] = saved
        won = lc.compete(cities.CITIES, clat, clon, zoom, store, entrants=labelled,
                         region=region["name"])
        regions.append({"region": region["name"], "cities": len(region["cities"]),
                        "labelled": len(labelled), "won": len(won),
                        "hand_problems": per_region.get(region["name"], 0)})
    total = int(re.search(r"PROBLEMS (\d+)", out).group(1))
    print(json.dumps({"menu": len(cities.REGIONS), "cities": len(cities.CITIES),
                      "problems": total, "global_problems": per_region.get("Global", 0),
                      "regions": regions}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", action="append", choices=SCENARIOS)
    ap.add_argument("--compete", action="append", default=[],
                    help="a region to score as competing (repeatable)")
    ap.add_argument("--country-view", action="append", default=[],
                    help="give a country a view of its own, built and staged cities alike")
    ap.add_argument("--group", action="append", default=[],
                    help='a region of whole countries: "Eastern Europe=Latvia,Romania"')
    ap.add_argument("--split-meridian", type=float,
                    help="cut Europe into Europe West and Europe East at this longitude")
    ap.add_argument("--snap-countries", action="store_true",
                    help="with --split-meridian, keep each country whole, by its mean longitude")
    ap.add_argument("--keep", help="build the trees here and keep them")
    ap.add_argument("--inner", help=argparse.SUPPRESS)
    args = ap.parse_args()
    groups = {g.split("=")[0]: g.split("=")[1].split(",") for g in args.group}
    if args.inner:
        return inner(Path(args.inner))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    staged = json.loads(STAGED.read_text(encoding="utf-8"))["cities"]
    for scenario in args.scenario or SCENARIOS:
        base = Path(args.keep) if args.keep else Path(tempfile.mkdtemp(prefix="stress_"))
        tmp = base / scenario
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        try:
            n_est, per_char = build_tree(tmp, scenario, staged, args.compete, args.country_view, groups,
                                         args.split_meridian, args.snap_countries)
            res = subprocess.run([sys.executable, __file__, "--inner", str(tmp)],
                                 capture_output=True, text=True, encoding="utf-8")
            if res.returncode:
                raise SystemExit(res.stderr[-2000:])
            r = json.loads(res.stdout.strip().splitlines()[-1])
        finally:
            if not args.keep:
                shutil.rmtree(base, ignore_errors=True)
        print(f"\n## Scenario {scenario}: {r['cities']} cities, {r['menu']} menu entries, "
              f"{r['problems']} label problems under hand placement "
              f"({r['global_problems']} in Global); {n_est} widths estimated at {per_char} px/char"
              + (f"; competing: {', '.join(args.compete)}" if args.compete else "")
              + (f"; own views: {', '.join(args.country_view)}" if args.country_view else "")
              + "".join(f"; {g}: {', '.join(ks)}" for g, ks in groups.items())
              + (f"; Europe cut at {args.split_meridian} E"
                 + (", countries whole" if args.snap_countries else "")
                 if args.split_meridian is not None else ""))
        print(f"{'region':<24}{'cities':>7}{'labelled':>10}{'fit':>6}{'unlabelled':>12}{'hand problems':>15}")
        for g in sorted(r["regions"], key=lambda g: -g["labelled"]):
            print(f"{g['region']:<24}{g['cities']:>7}{g['labelled']:>10}{g['won']:>6}"
                  f"{g['labelled'] - g['won']:>12}{g['hand_problems']:>15}")


if __name__ == "__main__":
    main()
