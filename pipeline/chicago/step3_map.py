"""Step 3 - Render Chicago's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Chicago-specific.

Input:  data/chicago/processed/stations.csv
        data/chicago/processed/businesses_clean.csv
        data/chicago/raw/gtfs.zip                    (for the line overlay)
        data/chicago/raw/city_boundary.geojson       (label anchoring)
Output: outputs/chicago/heatmap.html

Run:  python pipeline/chicago/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.chicago.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    CTA_LINE_NAMES,
    TAXONOMY_SYSTEM,
)

# key (route_id) -> (shape_id, colour). shape_id is each line's single
# most-used trip shape (counted per route, 2026-09-20; where directions tie,
# either is the same alignment) - EXCEPT Purple: its most-used shapes are the
# Linden-Howard stub in Evanston (about 1% inside the city), so the shape used
# is its rush-hour Loop express, the only one that reaches the city (its
# alignment overlaps Red and Brown between Howard and the Loop). Colours are
# CTA's own line colours from the feed's route_color: unambiguous and what
# riders recognise.
LINE_SHAPES = {
    "Red": ("309200007", "#C60C30"),
    "P": ("309200024", "#522398"),
    "Blue": ("309200001", "#00A1DE"),
    "Pink": ("309200035", "#E27EA6"),
    "G": ("309200009", "#009B3A"),
    "Org": ("309200034", "#F9461C"),
    "Brn": ("309200017", "#62361B"),
}
# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the city - override only if a rendered map
# shows that landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (shape_id, color, CTA_LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key, (shape_id, color) in LINE_SHAPES.items()
}


def city_geometry():
    """Chicago's city limits, so each line's label goes at the tail of the
    stretch inside the city (the 'L' runs on to Evanston, Oak Park, ...)."""
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None else boundary.to_crs(CRS_GEOGRAPHIC)
    return boundary.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Chicago 'L' Business Density Heatmap",
        city_name="Chicago",
        system_name="CTA 'L'",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "CTA 'L'"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
