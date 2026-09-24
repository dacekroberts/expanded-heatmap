"""Step 3 - Render Prague's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Prague-specific.

Input:  data/prague/processed/stations.csv
        data/prague/processed/businesses_clean.csv
        data/prague/raw/pid_gtfs.zip           (line geometry)
        data/prague/raw/osm_boundary.json      (label anchoring)
Output: outputs/prague/heatmap.html

Run:  python pipeline/prague/step3_map.py

The shape-selection rule is Oslo's: shapes in descending trip order, keep any
that reaches a stop the kept ones do not, stop when the route's stops are
covered. Metro A's shapes still run through Flora, closed or not - the track
is there - so the line needs no special case.
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.prague.boundary import city_polygon  # noqa: E402
from pipeline.prague.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_TYPE_METRO,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Metro"
# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def shape_ids_for_routes(zf):
    routes = pd.read_csv(zf.open("routes.txt"), dtype=str)
    metro = routes[routes["route_type"] == ROUTE_TYPE_METRO]
    short_of = dict(zip(metro["route_id"], metro["route_short_name"]))
    trips = pd.read_csv(zf.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id", "shape_id"])
    trips = trips[trips["route_id"].isin(short_of)].dropna(subset=["shape_id"])
    parts = []
    for ch in pd.read_csv(zf.open("stop_times.txt"), dtype=str, chunksize=1_000_000,
                          usecols=["trip_id", "stop_id"]):
        parts.append(ch[ch["trip_id"].isin(set(trips["trip_id"]))])
    st = pd.concat(parts, ignore_index=True)
    link = st.merge(trips, on="trip_id")
    shape_stops = link.groupby(["route_id", "shape_id"])["stop_id"].agg(set).to_dict()
    shape_trips = trips.groupby(["route_id", "shape_id"])["trip_id"].count().to_dict()
    route_stops = link.groupby("route_id")["stop_id"].agg(set).to_dict()

    chosen = {}
    for rid, short in short_of.items():
        want = route_stops.get(rid, set())
        ranked = sorted((k for k in shape_trips if k[0] == rid),
                        key=lambda k: (-shape_trips[k], k[1]))
        picked, covered = [], set()
        for key in ranked:
            if not (shape_stops[key] - covered) and picked:
                continue
            picked.append(key[1])
            covered |= shape_stops[key]
            if covered >= want:
                break
        if not picked:
            sys.exit(f"no shape covers {LINE_NAMES[short]} - a drawn line must come "
                     f"from real geometry")
        chosen[short] = tuple(picked)
        print(f"  {LINE_NAMES[short]:8s} {len(picked)} shape(s) covering "
              f"{len(covered)}/{len(want)} stops")
    return chosen


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    print("Line shapes:")
    with zipfile.ZipFile(GTFS_ZIP) as zf:
        chosen = shape_ids_for_routes(zf)
    line_specs = {short: (chosen[short], LINE_COLOURS[short], LINE_NAMES[short],
                          LINE_LABEL_ENDS.get(short))
                  for short in LINE_NAMES}

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")
    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Prague Metro Business Density Heatmap",
        city_name="Prague",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, line_specs, SYSTEM),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
