"""Step 3 - Render San Diego's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only
what is San Diego-specific.

Input:  data/san_diego/processed/stations.csv
        data/san_diego/processed/businesses_clean.csv
        data/san_diego/raw/gtfs.zip           (for the Trolley line overlay)
Output: outputs/san_diego/heatmap.html

Run:  python pipeline/san_diego/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.san_diego.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    GTFS_ZIP,
    MUNICIPAL_BOUNDARIES_GEOJSON,
    CITY_BOUNDARY_NAME,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    TAXONOMY_SYSTEM,
)

# key -> (shape_id, color, real-world public-facing name, label end).
# shape_id is each line's single most-used trip shape (counted per route,
# 2026-09-18) - re-derive if the GTFS feed is re-downloaded. The name is what
# MTS itself uses on signage (confirmed via Wikipedia's "<Color> Line (San
# Diego Trolley)" articles), not the GTFS route_short_name, which lacks
# "Line". Label end: None = automatic (the tail end farthest from the other
# lines, on the stretch inside the city); "start"/"end" forces one.
TROLLEY_LINE_SHAPES = {
    "Blue": ("510_0_352", "#0071bc", "Blue Line", None),
    "Orange": ("520_3_283", "#f7941d", "Orange Line", None),
    "Green": ("530_3_355", "#39b54a", "Green Line", None),
    "Copper": ("535_2_2", "#b87333", "Copper Line", None),
    "Silver": ("550_8_3", "#a6a6a6", "Silver Line", None),
}


def city_geometry():
    """San Diego's city limits, so each line's label goes at the tail of the
    stretch inside the city (the Trolley runs on to El Cajon and Santee)."""
    boundary = gpd.read_file(MUNICIPAL_BOUNDARIES_GEOJSON)
    boundary = boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None else boundary.to_crs(CRS_GEOGRAPHIC)
    return boundary[boundary["Name"] == CITY_BOUNDARY_NAME].geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="San Diego Trolley Business Density Heatmap",
        city_name="San Diego",
        system_name="Trolley",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"naics": str}),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, TROLLEY_LINE_SHAPES, "Trolley"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
