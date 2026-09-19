"""Step 4 - Render Los Angeles's heatmap to a standalone HTML file.

(Step 3 is geocoding, which this city needs and San Diego/San Francisco do
not.) All rendering lives in pipeline/map_common.py; this file supplies only
what is Los Angeles-specific.

Input:  data/los_angeles/processed/stations.csv
        data/los_angeles/processed/businesses_geocoded.csv
        data/los_angeles/raw/gtfs_rail.zip    (for the line overlay)
        data/los_angeles/raw/la_county_incorporated_cities.geojson  (label anchoring)
Output: outputs/los_angeles/heatmap.html

Run:  python pipeline/los_angeles/step4_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.los_angeles.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_GEOCODED_CSV,
    CITIES_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_FIELD,
    CITY_BOUNDARY_NAME,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    LA_METRO_LINE_NAMES,
    TAXONOMY_SYSTEM,
)

# Centred on the in-city station spread (station latitudes 33.93-34.17,
# longitudes -118.45 to -118.19), not the city's geographic centre - LA is
# huge and mostly not on a rail line.
LOS_ANGELES_CENTER = [34.05, -118.31]

# key (route_id) -> (shape_id, colour). shape_id is each line's single
# most-used trip shape (counted per route, 2026-09-18; where the two
# directions tie, either is the same alignment). Colours are Metro's own
# official line colours, straight from the feed's route_color - unlike San
# Francisco's, they are unambiguous, and riders recognise them.
LINE_SHAPES = {
    "801": ("801SB_P2B_250722", "#0072BC"),     # A Line
    "802": ("802WB_190513", "#EB131B"),         # B Line
    "803": ("803SB_241015", "#58A738"),         # C Line
    "804": ("804EB_RC_221121", "#FDB913"),      # E Line
    "805": ("805WB_PLE1_260423", "#A05DA5"),    # D Line
    "807": ("807SB_241015", "#E56DB1"),         # K Line
}
# Per-line label offset override (degrees); default 0.006. Bump a line here
# if a rendered map shows its label on a cluster or another line. A negative
# value puts the label on the opposite side of the track. The B and D Lines
# share the same subway corridor, so their default labels landed 9 px apart;
# D's goes to the other side.
LINE_LABEL_OFFSETS = {"805": -0.012}

LINE_SPECS = {
    key: (shape_id, color, LA_METRO_LINE_NAMES[key], LINE_LABEL_OFFSETS.get(key, 0.006))
    for key, (shape_id, color) in LINE_SHAPES.items()
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_GEOCODED_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    cities = gpd.read_file(CITIES_BOUNDARY_GEOJSON)
    cities = cities.set_crs(CRS_GEOGRAPHIC) if cities.crs is None else cities.to_crs(CRS_GEOGRAPHIC)
    city_geometry = cities[cities[CITY_BOUNDARY_FIELD] == CITY_BOUNDARY_NAME].geometry.union_all()

    render_heatmap(
        output_path=HEATMAP_HTML,
        center=LOS_ANGELES_CENTER,
        zoom=11,
        map_title="Los Angeles Metro Rail Business Density Heatmap",
        city_name="Los Angeles",
        system_name="Metro Rail",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_GEOCODED_CSV, dtype={"naics": str}),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Metro Rail"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry,
    )


if __name__ == "__main__":
    main()
