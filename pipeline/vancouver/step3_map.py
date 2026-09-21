"""Step 3 - Render the Vancouver + Surrey heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
specific to this city.

Input:  data/vancouver/processed/stations.csv
        data/vancouver/processed/businesses_clean.csv
        data/vancouver/raw/gtfs.zip                       (line overlay)
        data/vancouver/raw/vancouver_local_areas.geojson   (label anchoring)
        data/vancouver/raw/surrey_city_boundaries.geojson  (label anchoring)
Output: outputs/vancouver/heatmap.html

It is step THREE, not four: no geocoding step is needed. Of the 58,346
current-year Issued licences, 27,103 have neither coordinates nor a house-and-
street address, and they are overwhelmingly categories this project excludes
anyway - Long-term Rental, Short-term Rental Operator, contractors, consulting.
Only 1,583 rows (2.7%) have a real address and no coordinates, and those are
accepted as a loss rather than recovered: Canada has no national geocoder, and
Vancouver's own `property-addresses` layer has never been match-tested. A row
missing coordinates is not automatically a row needing geocoding.

TWO THINGS HERE DIFFER FROM EVERY OTHER CITY'S MAP STEP.

  **`label_focus` is the UNION of two cities**, not one boundary. All three
  SkyTrain lines run far beyond both - 30 of 54 stations are in Burnaby,
  Richmond, New Westminster, Coquitlam and Port Moody - so without an anchor
  every line label would be taken on a stretch the map never shows. The union
  is the mapped area, so that is what the labels are anchored to.

  **Two lines need a TUPLE of shape_ids** because they branch: the Canada Line
  splits for YVR-Airport and Richmond-Brighouse, the Expo Line for King George
  and Production Way-University. The single most-used shape would silently draw
  only one branch. New York's trunk lines needed the same thing.

Run:  python pipeline/vancouver/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.vancouver.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_IDS,
    STATIONS_CSV,
    SURREY_BOUNDARY_GEOJSON,
    SURREY_BOUNDARY_NAME_FIELD,
    SURREY_BOUNDARY_NAME_KEEP,
    TAXONOMY_SYSTEM,
)

# Each spec is (shape_id(s), colour, real public name, label end).
LINE_SPECS = {
    route_id: (LINE_SHAPES[route_id], LINE_COLOURS[route_id],
               LINE_NAMES[route_id], LINE_LABEL_ENDS.get(route_id))
    for route_id in ROUTE_IDS
}


def mapped_area():
    """Vancouver's local areas UNION Surrey's city polygon - the area this map
    actually covers, for anchoring each line's label at the end farthest from
    the others.

    Stanley Park is a hole in the local-area layer (see step 2), which does not
    matter here: a label anchor needs the general extent, not every parcel.
    """
    van = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    van = (van.set_crs(CRS_GEOGRAPHIC) if van.crs is None
           else van.to_crs(CRS_GEOGRAPHIC))
    sur = gpd.read_file(SURREY_BOUNDARY_GEOJSON)
    sur = (sur.set_crs(CRS_GEOGRAPHIC) if sur.crs is None
           else sur.to_crs(CRS_GEOGRAPHIC))
    sur = sur[sur[SURREY_BOUNDARY_NAME_FIELD].astype(str).str.upper()
              == SURREY_BOUNDARY_NAME_KEEP]
    if len(sur) != 1:
        sys.exit(f"Surrey boundary matched {len(sur)} features, expected 1 - "
                 f"9 of its 10 are town centres.")
    return van.union_all().union(sur.geometry.iloc[0])


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON, SURREY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="SkyTrain: commercial density around stations "
                  "(Vancouver and Surrey)",
        city_name="Vancouver (Regional)",
        system_name="SkyTrain",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "SkyTrain"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=mapped_area(),
    )


if __name__ == "__main__":
    main()
