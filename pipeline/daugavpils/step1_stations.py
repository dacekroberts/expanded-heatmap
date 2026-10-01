"""Daugavpils step 1: every stop of tram routes 1-5.

    python pipeline/daugavpils/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
nine kept relations (refs 1-4; ref 3 is routes 3 and 5), with one untagged
member accepted by node (config.ACCEPT_MEMBERS) and one misspelling aliased,
plus Užvaldes iela, which OSM does not map, at a vertex of OSM's own track
(config.TRACK_STOPS).
Every route lies inside the city, so step 3 draws each ref's relation whole.
All five routes are drawn (owner, 2026-09-30, overruling call 28); no stop is
thinned (call 13).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.daugavpils import config  # noqa: E402

FETCH = "pipeline/daugavpils/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def city_polygon():
    """The city of Daugavpils (OSM relation 13048685), EPSG:4326, area-gated."""
    rels = [e for e in osm_tram.read_elements(config.OSM_CITY_JSON, "city boundary", FETCH)
            if e["type"] == "relation" and e["id"] == config.OSM_CITY_RELATION]
    if len(rels) != 1:
        sys.exit(f"relation {config.OSM_CITY_RELATION} not in {config.OSM_CITY_JSON.name}")
    outer, inner = _rings(rels[0], "outer"), _rings(rels[0], "inner")
    if outer is None or outer.is_empty:
        sys.exit("Daugavpils's outer ways did not close into a polygon")
    poly = outer.difference(inner) if inner is not None else outer
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.CITY_AREA_KM2
    print(f"    {rels[0]['tags'].get('name')}: {km2:.1f} km2")
    if not lo <= km2 <= hi:
        sys.exit(f"the city polygon is {km2:.1f} km2, outside {lo}-{hi}")
    return poly


def track_stops(els, q):
    """Rows for the stops OSM does not map (config.TRACK_STOPS), each at a
    vertex of OSM's own track way, one point for every listed line (New
    Orleans's precedent). Exits if the vertex left its way, if the way left a
    listed line's relations, if a line already has a stop of that name, or if
    OSM has since mapped a stop within 60 m (then STATION_ADD it)."""
    stops = [e for e in els if e["type"] == "node"
             and (osm_tram._is_stop(e.get("tags", {}))
                  or e.get("tags", {}).get("public_transport") == "platform")]
    near = gpd.GeoSeries(gpd.points_from_xy([n["lon"] for n in stops],
                                            [n["lat"] for n in stops]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    rows = []
    for name, (lines, verts, _src) in config.TRACK_STOPS.items():
        for line in lines:
            if (q.loc[q["line"] == line, "stop_name"] == name).any():
                sys.exit(f"TRACK_STOPS {name!r}: {line} now has a stop of that name - "
                         f"remove the entry")
        for wid, lat, lon in verts:
            for line in lines:
                geoms = [m.get("geometry") or [] for r in els if r["type"] == "relation"
                         and r.get("tags", {}).get("route") == config.ROUTE
                         and r.get("tags", {}).get("ref") == line
                         for m in r["members"] if m["type"] == "way" and m["ref"] == wid]
                if not geoms:
                    sys.exit(f"TRACK_STOPS {name!r}: way {wid} is no longer on a route-{line} "
                             f"relation - re-read OSM")
                if not any(p["lat"] == lat and p["lon"] == lon for g in geoms for p in g):
                    sys.exit(f"TRACK_STOPS {name!r}: ({lat}, {lon}) is no longer a vertex "
                             f"of way {wid} - re-read OSM")
            pt = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs=config.CRS_GEOGRAPHIC
                               ).to_crs(config.CRS_PROJECTED).iloc[0]
            close = [stops[i]["tags"].get("name") for i, d in enumerate(near.distance(pt))
                     if d < 60]
            if close:
                sys.exit(f"TRACK_STOPS {name!r}: OSM now maps stop(s) {close} within "
                         f"60 m - add it by STATION_ADD and remove this entry")
            rows += [{"line": line, "node": -wid, "stop_name": name, "latitude": lat,
                      "longitude": lon, "source": "track"} for line in lines]
            print(f"    ADD  {name!r} on {'/'.join(lines)} at way {wid}'s vertex "
                  f"({lat}, {lon})")
    return pd.concat([q, pd.DataFrame(rows)], ignore_index=True)


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    poly = city_polygon()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD,
                           name_aliases=config.STATION_NAME_ALIASES,
                           accept_members=config.ACCEPT_MEMBERS)
    q = track_stops(els, q)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    # Gate 3: the operator's own stop counts (config.OPERATOR_STATION_COUNTS),
    # per route over every collapsed station.
    res = station_gates.verify_stations(
        city="Daugavpils", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})
    # A tram step 1 stops on a mismatch (tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the operator - "
                 + "; ".join(f"route {ln}: build {b}, operator {o}"
                             for ln, (b, o) in res["per_line_mismatches"].items()))

    places = gpd.GeoDataFrame([{"ref": config.ATVK, "name": config.CITY_NAME_LV,
                                "geometry": poly}], crs=config.CRS_GEOGRAPHIC)
    inside, outside = osm_tram.split_by_places(st, places, keep={config.ATVK})
    if len(outside):
        sys.exit("split_by_places should have exited on a stop in no place")
    print(f"\n  {len(st)} tram stations, all inside the city")
    if len(inside) != config.EXPECTED_STATIONS:
        sys.exit(f"{len(inside)} stations, not {config.EXPECTED_STATIONS} - re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m; the halved rings were chosen "
                 f"at 298 m - re-take the ring decision")

    # Every stop is in the city, so this is header-only; it stays written so a
    # stop that moves outside is recorded, not lost.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stop_positions_added", int((q["source"] == "added").sum()))
    emit("stations_in_scope", len(keep))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
