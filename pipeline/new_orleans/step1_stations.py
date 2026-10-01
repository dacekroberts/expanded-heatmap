"""New Orleans step 1: every stop of the drawn streetcar lines.

    python pipeline/new_orleans/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
kept relations, collapsed by name, corrected to RTA's own stop lists (gate 3)
by `config.STOP_LINE_FIXES` and `config.TRACK_STOPS`, applied here. Scope is the City of New Orleans, as
TIGER draws it (Houston's layer). The whole line lies inside the
city, so step 3 draws OSM's relation whole. No stop is thinned.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.new_orleans import config  # noqa: E402

FETCH = "pipeline/new_orleans/fetch_sources.py"


def city_polygon():
    """The City of New Orleans (TIGER place 2255000), EPSG:4326."""
    if not config.CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.CITY_BOUNDARY_GEOJSON}\nRun: python {FETCH}")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    km2 = float(city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.CITY_AREA_KM2
    print(f"    New Orleans (TIGER place {config.CITY_GEOID}): {km2:,.1f} km2")
    if not lo <= km2 <= hi:
        sys.exit(f"the place polygon is {km2:,.1f} km2, outside {lo:,}-{hi:,}")
    return city.geometry.union_all()


def fix_stop_lines(q):
    """Moves or drops the stop rows `config.STOP_LINE_FIXES` names: stop
    members of a kept relation that RTA's line does not serve. Exits on an
    entry that matches no row, so a stale fix cannot outlive the gap."""
    q = q.copy()
    for (line, node), (to, name, why) in config.STOP_LINE_FIXES.items():
        hit = (q["line"] == line) & (q["node"] == node)
        if not hit.any() or (q.loc[hit, "stop_name"] != name).any():
            sys.exit(f"STOP_LINE_FIXES ({line}, {node}) {name!r}: no such stop row "
                     f"now - re-read OSM and remove or correct the entry")
        if to is None:
            q = q[~hit].copy()
            print(f"    DROP node {node} {name!r} from {line} - {why}")
        else:
            q.loc[hit, "line"] = to
            print(f"    MOVE node {node} {name!r} from {line} to {to} - {why}")
    return q.drop_duplicates(["line", "node"]).reset_index(drop=True)


def track_stops(els, q):
    """Rows for the stops OSM does not map (`config.TRACK_STOPS`), each at a
    vertex of OSM's own track way for that line. Exits if a vertex left its
    way, or OSM has since mapped a stop within 60 m (then STATION_ADD it)."""
    nodes = [e for e in els if e["type"] == "node"
             and any(e.get("tags", {}).get(k) == v for k, v in osm_tram.STOP_TAGS)]
    rows = []
    for name, (line, verts, _src) in config.TRACK_STOPS.items():
        if (q.loc[q["line"] == line, "stop_name"] == name).any():
            sys.exit(f"TRACK_STOPS {name!r}: {line} now has a stop of that name - "
                     f"remove the entry")
        ways = {m["ref"]: m.get("geometry") or []
                for r in els if r["type"] == "relation"
                and r.get("tags", {}).get("ref") == line
                for m in r["members"] if m["type"] == "way"}
        for wid, lat, lon in verts:
            if not any(p["lat"] == lat and p["lon"] == lon for p in ways.get(wid, [])):
                sys.exit(f"TRACK_STOPS {name!r}: ({lat}, {lon}) is no longer a vertex "
                         f"of way {wid} on {line} - re-read OSM")
            pt = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs=config.CRS_GEOGRAPHIC
                               ).to_crs(config.CRS_PROJECTED).iloc[0]
            near = gpd.GeoSeries(gpd.points_from_xy([n["lon"] for n in nodes],
                                                    [n["lat"] for n in nodes]),
                                 crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
            close = [nodes[i]["tags"].get("name") for i, d in enumerate(near.distance(pt))
                     if d < 60]
            if close:
                sys.exit(f"TRACK_STOPS {name!r}: OSM now maps stop(s) {close} within "
                         f"60 m - add it by STATION_ADD and remove this entry")
            rows.append({"line": line, "node": -wid, "stop_name": name, "latitude": lat,
                         "longitude": lon, "source": "track"})
            print(f"    ADD  {name!r} on {line} at way {wid}'s vertex ({lat}, {lon})")
    return pd.concat([q, pd.DataFrame(rows)], ignore_index=True)


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached inputs:")
    poly = city_polygon()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD,
                           name_aliases=config.NAME_ALIASES)
    print()
    q = fix_stop_lines(q)
    q = track_stops(els, q)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    # Gate 3 against RTA's own stop lists (config), counted before the city
    # split. A tram step 1 stops on a mismatch (tram-city skill); the exit was
    # off until the station fix of 2026-10-01 (Sycamore; 47/48 down Canal to
    # the ferry) and is live again.
    res = station_gates.verify_stations(
        city="New Orleans", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the operator's own count - "
                 + "; ".join(f"{line}: build {b}, operator {o}"
                             for line, (b, o) in res["per_line_mismatches"].items()))

    places = gpd.GeoDataFrame([{"ref": config.CITY_GEOID, "name": "New Orleans",
                                "geometry": poly}], crs=config.CRS_GEOGRAPHIC)
    inside, outside = osm_tram.split_by_places(st, places, keep={config.CITY_GEOID})
    if len(outside):
        sys.exit("split_by_places should have exited on a stop in no place")
    print(f"\n  {len(st)} streetcar stops, all inside the city")
    if len(inside) != config.EXPECTED_STATIONS:
        sys.exit(f"{len(inside)} stations, not the brief's {config.EXPECTED_STATIONS} - "
                 f"re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m; the halved rings were chosen "
                 f"at 164 m - re-take the ring decision")

    # Every stop is in the city, so this is header-only; it stays written so a
    # stop that moves outside is recorded, not lost.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_in_scope", len(keep))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
