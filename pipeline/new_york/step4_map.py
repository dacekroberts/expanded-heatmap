"""Step 4 - Render New York's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
New York-specific.

Input:  data/new_york/processed/stations.csv
        data/new_york/processed/businesses_geocoded.csv   (step 3's output)
        data/new_york/raw/gtfs.zip                        (for the line overlay)
        data/new_york/raw/city_boundary.geojson           (label anchoring)
Output: outputs/new_york/heatmap.html

Unlike the other cities, a "line" here is a TRUNK made of several GTFS shapes:
the 1, 2 and 3 share the 7 Avenue line through Manhattan and branch apart in
the Bronx and Brooklyn, so the trunk is drawn as several polylines under one
name, one colour and one legend entry (see load_line_shapes). Drawing all 29
service patterns instead would also overflow the label layout's legend
obstacle - 178 + 19*29 px in a 650 px map. See config.py.

Each member route's shape is its most-used trip shape, counted from trips.txt
at run time rather than hardcoded, because MTA reshapes service often and a
stale shape_id fails silently as a missing line.

Run:  python pipeline/new_york/step4_map.py
"""

import sys
import zipfile
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.new_york.config import (  # noqa: E402
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAW_EXCLUDE_ROUTES,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_TO_TRUNK,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)


def modal_shapes_by_trunk():
    """{trunk: [shape_id, ...]} - each drawn route's single most-used trip
    shape, grouped into its trunk. Longest-first ordering is done by
    load_line_shapes, which anchors the label to the longest segment."""
    with zipfile.ZipFile(GTFS_ZIP) as z, z.open("trips.txt") as f:
        trips = pd.read_csv(f, dtype=str, usecols=["route_id", "shape_id"])

    by_trunk = {}
    for route_id, trunk in sorted(ROUTE_TO_TRUNK.items()):
        if route_id in DRAW_EXCLUDE_ROUTES:
            continue
        shapes = trips.loc[trips["route_id"] == route_id, "shape_id"].dropna()
        if shapes.empty:
            print(f"WARNING: route {route_id!r} has no trips in this feed - "
                  "its geometry will be missing from the map.")
            continue
        shape_id, n_trips = Counter(shapes).most_common(1)[0]
        by_trunk.setdefault(trunk, []).append(shape_id)
        print(f"  {route_id:<4} -> {trunk:<10} {shape_id:<22} ({n_trips:,} trips)")

    missing = sorted(set(LINE_NAMES) - set(by_trunk))
    if missing:
        print(f"WARNING: trunks with no drawn geometry: {missing}")
    return by_trunk


def city_geometry():
    """The five borough polygons, so each trunk's label goes at the tail of its
    stretch inside the city."""
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    return boundary.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_GEOCODED_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    if not GTFS_ZIP.exists():
        sys.exit(f"Missing {GTFS_ZIP}. Run fetch_sources.py first.")

    print("Most-used trip shape per drawn route:")
    by_trunk = modal_shapes_by_trunk()

    line_specs = {
        trunk: (tuple(shape_ids), LINE_NAMES[trunk][1], LINE_NAMES[trunk][0],
                LINE_LABEL_ENDS.get(trunk))
        for trunk, shape_ids in by_trunk.items()
    }
    print(f"\n{len(line_specs)} trunk lines, "
          f"{sum(len(s) for s in by_trunk.values())} shapes drawn")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="New York Subway Business Density Heatmap",
        city_name="New York",
        system_name="MTA rail",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_GEOCODED_CSV, dtype={"business_category": str}),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, line_specs, "MTA rail"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
        # 496 stations a median 482 m apart: shown by default the rings are an
        # indistinct wash over Manhattan. They read cleanly around the
        # outer-borough and Staten Island stations, so they stay available in
        # the layer control instead of being dropped. See render_heatmap.
        rings_shown=False,
    )


if __name__ == "__main__":
    main()
