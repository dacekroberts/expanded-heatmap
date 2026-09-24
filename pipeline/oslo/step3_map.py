"""Step 3 - Render Oslo's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Oslo-specific.

Input:  data/oslo/processed/stations.csv
        data/oslo/processed/businesses_clean.csv
        data/oslo/raw/gtfs.zip
        data/oslo/raw/city_boundary.geojson   (label anchoring)
Output: outputs/oslo/heatmap.html

Run:  python pipeline/oslo/step3_map.py

The shape-selection rule is Dublin's, as every GTFS city here takes it: shapes
in descending trip order, keep any that reaches a stop the kept ones do not,
stop when the route's stops are covered.

The T-bane's western branches are DRAWN to their Bærum termini, though their
12 stations there are uncounted - the network a reader rides is drawn whole,
and the rings are what the map counts. The colours are Ruter's per-line
colours, not the feed's: see config.LINE_COLOURS.
"""
import json
import sys
import zipfile
from pathlib import Path

import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.oslo.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_IDS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the kommune.
LINE_LABEL_ENDS = {}


def shape_ids_for_routes(zf):
    """The shape_ids needed to draw each route's WHOLE alignment."""
    routes = pd.read_csv(zf.open("routes.txt"), dtype=str)
    rail = routes[routes["route_id"].isin(ROUTE_IDS)]
    short_of = dict(zip(rail["route_id"], rail["route_short_name"]))

    trips = pd.read_csv(zf.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id", "shape_id"])
    trips = trips[trips["route_id"].isin(set(rail["route_id"]))].dropna(subset=["shape_id"])
    st = pd.read_csv(zf.open("stop_times.txt"), dtype=str, usecols=["trip_id", "stop_id"])
    st = st[st["trip_id"].isin(set(trips["trip_id"]))]

    link = st.merge(trips[["trip_id", "route_id", "shape_id"]], on="trip_id")
    shape_stops = link.groupby(["route_id", "shape_id"])["stop_id"].agg(set).to_dict()
    shape_trips = trips.groupby(["route_id", "shape_id"])["trip_id"].count().to_dict()
    route_stops = link.groupby("route_id")["stop_id"].agg(set).to_dict()

    chosen = {}
    for rid in ROUTE_IDS:
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
            sys.exit(f"no shape covers {LINE_NAMES.get(short_of.get(rid), rid)}"
                     f" - a line this project draws must come from real geometry")
        chosen[rid] = picked
        flag = "  <- branches" if len(picked) > 1 else ""
        print(f"  {LINE_NAMES[short_of[rid]]:10s} {len(picked)} shape(s) "
              f"covering {len(covered)}/{len(want)} stops{flag}")
    return chosen, short_of


def kommune_geometry():
    """Oslo kommune, so each line's label goes at the tail of the stretch
    inside it - which matters for T-bane 2, 3 and 5, whose western ends are in
    Bærum and uncounted."""
    return shape(json.loads(CITY_BOUNDARY_GEOJSON.read_text(encoding="utf-8"))["geometry"])


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    print("Line shapes:")
    with zipfile.ZipFile(GTFS_ZIP) as zf:
        chosen, short_of = shape_ids_for_routes(zf)

    line_specs = {
        rid: (tuple(chosen[rid]), LINE_COLOURS[short_of[rid]],
              LINE_NAMES[short_of[rid]], LINE_LABEL_ENDS.get(rid))
        for rid in ROUTE_IDS
    }

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Oslo T-bane and Trikk Business Density Heatmap",
        city_name="Oslo",
        system_name="T-bane and Trikk",
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, line_specs, "T-bane and Trikk"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=kommune_geometry(),
    )


if __name__ == "__main__":
    main()
