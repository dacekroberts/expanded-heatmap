"""Choose a city's line colours: the SPATIAL form of the rule Kobe, Osaka,
Sapporo and Fukuoka applied by hand (their colour_search.py, 2026-09-27/28).

From the sRGB cube (steps of 8), the colours that read 3:1 against BOTH map
pages and clear CIE76 45 from every category pin. Each line, in config order,
takes the feasible colour nearest its operator's own hue (config.LINES[key]
["hue"]; lightness weighted half), holding:
  * CIE76 >= NEAR_DE from every line already chosen that comes within NEAR_M
    of it (step 1's lines.geojson, in the city's projected CRS) - lines a
    reader sees side by side;
  * CIE76 >= linecolour.HARD_FLOOR from every other line in the city, which
    check_line_colours() and check_map_markup.py require.
Osaka's 34 lines sat at the limit of the city-wide search (closest pair 18.0);
Tokyo's 52 do not fit it, which is why the constraint is spatial (the Tokyo
build handoff, 2026-09-28). The dark-mode labels are then separated the way
the renderer does it (dark_label_colours), so a choice it cannot draw fails
here, not at render.

Prints the choice and its margins; the city's config records it, citing this
run. Touches nothing.

    python scripts/line_colour_search.py <city> [--near-m 500] [--near-de 18]
"""
import argparse
import importlib
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import geopandas as gpd  # noqa: E402
from shapely.geometry import shape  # noqa: E402

from pipeline import linecolour as lc  # noqa: E402
from pipeline import theme  # noqa: E402
from pipeline.taxonomies import CATEGORY_BUCKETS  # noqa: E402

STEP = 8


def pull(lab, target):
    return math.sqrt(0.25 * (lab[0] - target[0]) ** 2 + (lab[1] - target[1]) ** 2 + (lab[2] - target[2]) ** 2)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("city")
    ap.add_argument("--near-m", type=float, default=500)
    ap.add_argument("--near-de", type=float, default=18)
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")

    pins = [c for _, c in CATEGORY_BUCKETS]
    pages = [theme.DARK["page"], theme.LIGHT["page"]]
    feasible = []
    for r in range(0, 256, STEP):
        for g in range(0, 256, STEP):
            for b in range(0, 256, STEP):
                h = f"#{r:02X}{g:02X}{b:02X}"
                if all(lc.contrast_ratio(h, p) >= 3 for p in pages) and all(lc.delta_e(h, p) >= 45 for p in pins):
                    feasible.append((h, lc.to_lab(h)))
    print(f"feasible colours: {len(feasible)} (3:1 on {pages}, CIE76 >= 45 from {pins})")

    feats = json.loads(Path(config.LINES_GEOJSON).read_text(encoding="utf-8"))["features"]
    geo = gpd.GeoSeries([shape(f["geometry"]) for f in feats], index=[f["properties"]["line"] for f in feats],
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    keys = [k for k in config.LINE_ORDER if k in geo.index]
    near = {k: {j for j in keys if j != k and geo[k].distance(geo[j]) <= args.near_m} for k in keys}

    chosen = {}
    for k in keys:
        target = lc.to_lab(config.LINES[k]["hue"])
        ok = [c for c in feasible
              if all(lc.delta_e(c[0], chosen[j]) >= (args.near_de if j in near[k] else lc.HARD_FLOOR)
                     for j in chosen)]
        if not ok:
            sys.exit(f"no feasible colour for {k} ({config.LINE_NAMES[k]}) with {len(near[k])} lines near it")
        chosen[k] = min(ok, key=lambda c: pull(c[1], target))[0]

    worst_near = min((lc.delta_e(chosen[a], chosen[b]), a, b) for a in keys for b in near[a])
    worst_all = min((lc.delta_e(chosen[a], chosen[b]), a, b) for i, a in enumerate(keys) for b in keys[i + 1:])
    print(f"\n{'key':4} {'operator hue':12} {'chosen':8} {'pins':>5} {'near':>5} {'dark':>5} {'light':>5}  line")
    for k in keys:
        pin = min(lc.delta_e(chosen[k], p) for p in pins)
        nearest = min((lc.delta_e(chosen[k], chosen[j]) for j in near[k]), default=float("nan"))
        print(f"{k:4} {config.LINES[k]['hue']:12} {chosen[k]:8} {pin:5.1f} {nearest:5.1f} "
              f"{lc.contrast_ratio(chosen[k], pages[0]):5.2f} {lc.contrast_ratio(chosen[k], pages[1]):5.2f}  "
              f"{config.LINE_NAMES[k]} ({len(near[k])} near)")
    print(f"\nclosest pair within {args.near_m:.0f} m: {worst_near[0]:.1f} ({worst_near[1]}, {worst_near[2]}); "
          f"closest pair anywhere: {worst_all[0]:.1f} ({worst_all[1]}, {worst_all[2]})")
    dark = lc.dark_label_colours(chosen, dark_halo=theme.DARK["page"], city=args.city)
    print(f"dark-mode labels separate: {len(set(dark.values()))} distinct of {len(dark)}")
    print("\n" + json.dumps(chosen))


if __name__ == "__main__":
    main()
