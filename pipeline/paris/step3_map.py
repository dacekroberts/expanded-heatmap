"""Step 3 - Render Paris's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Paris-specific.

Input:  data/paris/processed/stations.csv
        data/paris/processed/businesses_clean.csv
        data/paris/raw/gtfs.zip
        data/paris/raw/city_boundary.geojson   (label anchoring)
Output: outputs/paris/heatmap.html

Run:  python pipeline/paris/step3_map.py

TWO THINGS THIS CITY NEEDS THAT A SINGLE-ALIGNMENT SYSTEM DOES NOT:

  * **M7 AND M13 BRANCH.** Taking each route's modal trip shape - which is
    right for a line with one alignment - would draw one branch of each and
    simply not draw the other, and no count in this pipeline would notice.
    Dublin hit the same thing with the Luas Red line and the fix is its
    coverage rule, kept here: take shapes in descending trip order, keep any
    that reaches a stop the kept ones do not, stop when the route's stops are
    covered. That reduces to "the modal shape" for an unbranched line.
  * **stop_times.txt IS 885 MB UNCOMPRESSED**, because the feed is the whole
    Ile-de-France network. Dublin reads its trimmed feed with csv.DictReader;
    here that is read with pandas and filtered to metro trips first.
"""
import json
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.paris.config import (  # noqa: E402
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
    ROUTE_TYPE_METRO,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the commune. Override only if a rendered
# map shows one landing badly.
LINE_LABEL_ENDS = {}


def shape_ids_for_routes(zf):
    """The shape_ids needed to draw each route's WHOLE alignment.

    See the module docstring: M7 and M13 branch, so this is coverage-based
    rather than modal.
    """
    routes = pd.read_csv(zf.open("routes.txt"), dtype=str)
    metro = routes[routes["route_type"] == ROUTE_TYPE_METRO]
    metro = metro[metro["route_id"].isin(ROUTE_IDS)]
    short_of = dict(zip(metro["route_id"], metro["route_short_name"]))

    trips = pd.read_csv(zf.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id", "shape_id"])
    trips = trips[trips["route_id"].isin(set(metro["route_id"]))]
    trips = trips.dropna(subset=["shape_id"])

    st = pd.read_csv(zf.open("stop_times.txt"), dtype=str,
                     usecols=["trip_id", "stop_id"])
    st = st[st["trip_id"].isin(set(trips["trip_id"]))]

    link = st.merge(trips[["trip_id", "route_id", "shape_id"]], on="trip_id")
    shape_stops = (link.groupby(["route_id", "shape_id"])["stop_id"]
                   .agg(set).to_dict())
    shape_trips = (trips.groupby(["route_id", "shape_id"])["trip_id"]
                   .count().to_dict())
    route_stops = link.groupby("route_id")["stop_id"].agg(set).to_dict()

    chosen = {}
    for rid in ROUTE_IDS:
        want = route_stops.get(rid, set())
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
        if not picked:
            sys.exit(f"no shape covers {LINE_NAMES.get(short_of.get(rid), rid)} "
                     f"- the feed has trips with no shape_id, and a line this "
                     f"project draws must come from real geometry")
        chosen[rid] = picked
        name = LINE_NAMES[short_of[rid]]
        flag = "  <- branches" if len(picked) > 1 else ""
        print(f"  {name:14s} {len(picked)} shape(s) covering "
              f"{len(covered)}/{len(want)} stops{flag}")
    return chosen, short_of


def commune_geometry():
    """The commune of Paris, so each line's label goes at the tail of the
    stretch INSIDE it rather than out in the banlieue - several lines run well
    past the boundary and 76 of their stations are not drawn at all."""
    return shape(json.loads(
        CITY_BOUNDARY_GEOJSON.read_text(encoding="utf-8"))["geometry"])


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    print("Line shapes:")
    with zipfile.ZipFile(GTFS_ZIP) as zf:
        chosen, short_of = shape_ids_for_routes(zf)

    line_specs = {
        rid: (tuple(chosen[rid]),
              LINE_COLOURS[short_of[rid]],
              LINE_NAMES[short_of[rid]],
              LINE_LABEL_ENDS.get(rid))
        for rid in ROUTE_IDS
    }

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Paris Metro Business Density Heatmap",
        city_name="Paris",
        system_name="Métro",
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, line_specs, "Métro"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=commune_geometry(),
    )


if __name__ == "__main__":
    main()
