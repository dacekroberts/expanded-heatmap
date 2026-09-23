"""Step 3 - Render Dublin's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Dublin-specific.

Input:  data/dublin/processed/stations.csv
        data/dublin/processed/businesses_clean.csv
        data/dublin/raw/gtfs_dublin_rail.zip     (the trimmed NTA feed)
        data/dublin/raw/local_authorities.geojson (label anchoring)
Output: outputs/dublin/heatmap.html

Run:  python pipeline/dublin/step3_map.py
"""

import csv
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.dublin.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    BOUNDARY_GEOJSON,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTES,
    BOUNDARY_NAME_FIELD,
)

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the region. Override only if a rendered
# map shows one landing badly.
LINE_LABEL_ENDS = {}


def shape_ids_for_routes():
    """The shape_ids needed to draw each route's WHOLE alignment.

    Not simply the most-used shape. `add-city` says to take the modal trip
    shape per route, and that is right for a line with one alignment - but
    LUAS RED BRANCHES, to Tallaght and to Saggart, and DART runs several
    patterns over one corridor. The modal shape covers one branch and the other
    would simply not be drawn, which no count in this pipeline would notice.

    So: take shapes in descending order of trip count, keeping any that reaches
    a stop the ones already kept do not, and stop when every stop on the route
    is covered. That reduces to "the modal shape" for a line with no branches,
    and `load_line_shapes` already accepts several shape_ids for one line
    (New York's branching trunks needed it first).
    """
    with zipfile.ZipFile(GTFS_ZIP) as zf:
        def read(name):
            with zf.open(name) as fh:
                return list(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")))
        trips = read("trips.txt")
        stop_times = read("stop_times.txt")

    trip_shape = {t["trip_id"]: t.get("shape_id") for t in trips}
    trip_route = {t["trip_id"]: t["route_id"] for t in trips}

    shape_stops, shape_trips, route_stops = {}, Counter(), {}
    for st in stop_times:
        tid = st["trip_id"]
        sid, rid = trip_shape.get(tid), trip_route.get(tid)
        if not sid or rid not in ROUTES:
            continue
        shape_stops.setdefault((rid, sid), set()).add(st["stop_id"])
        route_stops.setdefault(rid, set()).add(st["stop_id"])
    for tid, sid in trip_shape.items():
        if sid and trip_route.get(tid) in ROUTES:
            shape_trips[(trip_route[tid], sid)] += 1

    chosen = {}
    for rid in ROUTES:
        want = set(route_stops.get(rid, ()))
        ranked = sorted((k for k in shape_trips if k[0] == rid),
                        key=lambda k: (-shape_trips[k], k[1]))
        picked, covered = [], set()
        for key in ranked:
            new = shape_stops[key] - covered
            if not new and picked:
                continue
            picked.append(key[1])
            covered |= shape_stops[key]
            if covered >= want:
                break
        chosen[rid] = picked
        print(f"  {ROUTES[rid][0]:18s} {len(picked)} shape(s) covering "
              f"{len(covered)}/{len(want)} stops  {picked}")
    return chosen


def region_geometry():
    """The four authorities as one polygon, so each line's label goes at the
    tail of the stretch inside the region rather than out at Greystones."""
    boundary = json.loads(BOUNDARY_GEOJSON.read_text(encoding="utf-8"))
    gdf = gpd.GeoDataFrame(
        [{"authority": f["properties"][BOUNDARY_NAME_FIELD],
          "geometry": shape(f["geometry"])} for f in boundary["features"]],
        crs=CRS_GEOGRAPHIC)
    return gdf.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    print("Line shapes:")
    chosen = shape_ids_for_routes()
    line_specs = {
        rid: (tuple(chosen[rid]), colour, label, LINE_LABEL_ENDS.get(rid))
        for rid, (label, colour) in ROUTES.items()
    }

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Dublin Luas and DART Business Density Heatmap",
        city_name="Dublin",
        system_name="Luas and DART",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system="dublin_uses",
        lines=load_line_shapes(GTFS_ZIP, line_specs, "Luas and DART"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=region_geometry(),
    )


if __name__ == "__main__":
    main()
