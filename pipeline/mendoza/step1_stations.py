"""Mendoza step 1: the Metrotranvia's stations in the Ciudad de Mendoza.

    python pipeline/mendoza/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the two
MTM relations, collapsed by name. The line runs on into Las Heras, Godoy Cruz
and Maipu: its stops there are drawn with the line but not ringed, and are
listed with the department each lies in (owner, 2026-10-03; Florence's shape).
No stop is thinned.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.mendoza import config  # noqa: E402

FETCH = "pipeline/mendoza/fetch_sources.py"
CAPITAL = "Departamento Capital"
LF = chr(10)


def departments():
    """The departments in the cache, each polygonised from its outer ways."""
    if not config.OSM_JSON.exists():
        sys.exit(f"missing {config.OSM_JSON}\nRun: python {FETCH}")
    els = json.loads(config.OSM_JSON.read_text(encoding="utf-8"))["elements"]
    rows = []
    for e in els:
        t = e.get("tags", {})
        if e["type"] != "relation" or t.get("boundary") != "administrative":
            continue
        lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                 for m in e.get("members", []) if m.get("type") == "way"
                 and m.get("role") == "outer" and len(m.get("geometry") or []) >= 2]
        poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
        rows.append({"ref": str(e["id"]), "name": t.get("name", "").replace("Departamento ", ""),
                     "full_name": t.get("name", ""), "geometry": poly})
    g = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    if CAPITAL not in set(g["full_name"]):
        sys.exit(f"{CAPITAL} is not in the cached boundaries - re-run {FETCH}")
    return g


def capital_polygon():
    g = departments()
    poly = g.loc[g["full_name"] == CAPITAL, "geometry"].iloc[0]
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.CAPITAL_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"{CAPITAL} is {km2:,.1f} km2, outside {lo:,}-{hi:,}: a partial answer?")
    return poly


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    deps = departments()
    capital_polygon()                       # the scope's area gate
    km2 = deps.to_crs(config.CRS_PROJECTED).set_index("full_name").area / 1e6
    print("    " + ", ".join(f"{n} {a:,.1f} km2" for n, a in km2.items()))
    els = osm_tram.read_elements(config.OSM_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=config.ROUTES, refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    res = station_gates.verify_stations(
        city="Mendoza", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the line's count - " + "; ".join(
            f"{ref}: build {b}, source {o}" for ref, (b, o) in res["per_line_mismatches"].items()))

    capital_ref = deps.loc[deps["full_name"] == CAPITAL, "ref"].iloc[0]
    inside, outside = osm_tram.split_by_places(st, deps, keep={capital_ref})
    print(f"\n  {len(st)} stations -> {len(inside)} in the Ciudad de Mendoza, "
          f"{len(outside)} elsewhere")
    if len(inside) != config.EXPECTED_IN_SCOPE:
        sys.exit(f"{len(inside)} stations in the capital, not the city stop list's "
                 f"{config.EXPECTED_IN_SCOPE} - re-read the border stops")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-capital spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-capital median gap is {d.median():.0f} m, outside {lo:.0f}-{hi:.0f} m, "
                 f"where the ring edges were chosen - re-take the ring decision")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n}, outside the Ciudad de Mendoza" for n in outside["name"]],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV, index=False,
                                                  encoding="utf-8", lineterminator=LF)
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for s, r in zip(out["station"], out["reason"]):
        print(f"    {s:<28} {r}")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator=LF)
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}: "
          + ", ".join(keep["station"]))

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))
    emit("median_gap_m", int(round(d.median())))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
