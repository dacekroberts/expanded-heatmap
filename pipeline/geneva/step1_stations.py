"""Geneva (Regional) step 1: every stop of TPG's five trams in the 12 tram
communes.

    python pipeline/geneva/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Zurich's step 1 on the shared `pipeline/osm_tram.py`: stations are the stop
members of the kept tram relations, collapsed by name. Tram 17 runs on into
France (Gaillard, Ambilly, Annemasse): its stops there are drawn with the
line but not ringed, and are listed with the commune each lies in (Florence's
T1 precedent, the kit's call 17). No stop is thinned.
"""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.geneva import config  # noqa: E402
from pipeline.geneva.communes import FETCH, commune_polygons  # noqa: E402


PLATFORM_LETTER = re.compile(r"\s*\(\s*[A-Z]\s*\)$")


def fold_platform_letters(q):
    """Strip TPG's platform letter from OSM's stop names (config's comment),
    checking the stops it touches against config.PLATFORM_LETTER_STOPS."""
    lettered = q["stop_name"].str.contains(PLATFORM_LETTER)
    folded = set(q.loc[lettered, "stop_name"].str.replace(PLATFORM_LETTER, "", regex=True))
    if folded != config.PLATFORM_LETTER_STOPS:
        sys.exit(f"platform letters: OSM letters {sorted(folded - config.PLATFORM_LETTER_STOPS)} "
                 f"not in config, config lists {sorted(config.PLATFORM_LETTER_STOPS - folded)} "
                 f"OSM no longer letters - re-read OSM and update the list")
    q = q.copy()
    q["stop_name"] = q["stop_name"].str.replace(PLATFORM_LETTER, "", regex=True)
    print(f"\n  {int(lettered.sum())} stop position(s) lose a platform letter, "
          f"{len(folded)} stops")
    return q


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    places = commune_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=config.ROUTES, refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    q = fold_platform_letters(q)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=config.MAX_SPREAD_M)
    print()
    res = station_gates.verify_stations(
        city="Geneva (Regional)", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})
    # Gate 3 stops a tram step 1 (the tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with TPG's own stop counts - " + "; ".join(
            f"{ref}: build {b}, TPG {o}" for ref, (b, o) in res["per_line_mismatches"].items()))

    inside, outside = osm_tram.split_by_places(st, places, keep=set(config.COMMUNES))
    print(f"\n  {len(st)} tram stops -> {len(inside)} in the 12 tram communes, "
          f"{len(outside)} elsewhere")
    if (config.EXPECTED_IN_SCOPE is not None
            and (len(inside), len(outside)) != (config.EXPECTED_IN_SCOPE, config.EXPECTED_OUTSIDE)):
        sys.exit(f"expected {config.EXPECTED_IN_SCOPE} inside and {config.EXPECTED_OUTSIDE} "
                 f"outside (the build of 2026-10-07) - re-read OSM")
    print("  stops per commune: " + ", ".join(
        f"{n} {c}" for n, c in inside["name"].value_counts().items()))

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-scope median gap is {d.median():.0f} m, outside {lo:.0f}-{hi:.0f} - "
                 f"re-take the ring decision")
    emit("median_gap_m", round(float(d.median())))

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n}, France, outside the 12 tram communes"
                                   if str(r).startswith("FR-") else
                                   f"in {n}, outside the 12 tram communes"
                                   for n, r in zip(outside["name"], outside["ref"])],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for s, r, ln in zip(out["station"], out["reason"], out["lines"]):
        print(f"    {s:<32} {ln:<8} {r}")

    keep = (inside.rename(columns={"stop_name": "station", "name": "commune"})
            [["station", "commune", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    per_line = {ref: int(keep["lines"].str.split("/").apply(lambda x: ref in x).sum())
                for ref in config.LINE_REFS}
    print(f"  stations per line in scope: {per_line}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
