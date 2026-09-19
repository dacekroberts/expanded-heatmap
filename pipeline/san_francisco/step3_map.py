"""Step 3 - Render San Francisco's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only
what is San Francisco-specific.

Input:  data/san_francisco/processed/stations.csv
        data/san_francisco/processed/businesses_clean.csv
        data/san_francisco/raw/gtfs.zip       (for the Muni Metro line overlay)
Output: outputs/san_francisco/heatmap.html

Run:  python pipeline/san_francisco/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.san_francisco.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    MUNI_METRO_LINE_NAMES,
    TAXONOMY_SYSTEM,
)

# Centered on the actual station spread's centroid (from stations.csv,
# 2026-09-18), not the city's geographic center - SF's compact,
# diagonal shape means those differ, and centering on the wrong one left
# too much open water in the default view.
SAN_FRANCISCO_CENTER = [37.7509, -122.4414]

# key -> (shape_id, color). shape_id is each line's single most-used trip
# shape (2026-09-18). Colors are this project's OWN palette, not
# SFMTA's official ones - those have changed across map revisions and some
# lines currently share a color, which would defeat a map that needs 6
# distinct lines. Chosen to stay apart from each other and from the
# blue/orange/green business-category palette.
LINE_SHAPES = {
    "J": ("9301", "#d62828"),   # red
    "K": ("9436", "#7209b7"),   # purple
    "L": ("9501", "#ffb703"),   # gold
    "M": ("9651", "#f72585"),   # magenta
    "N": ("9717", "#6f4518"),   # brown
    "T": ("354", "#495057"),    # dark gray
}
# Per-line label offset override (degrees); default 0.006. Bump a line here
# if a rendered map shows its label on a cluster or another line - check
# visually, don't assume the default works.
LINE_LABEL_OFFSETS = {}

LINE_SPECS = {
    key: (shape_id, color, MUNI_METRO_LINE_NAMES[key], LINE_LABEL_OFFSETS.get(key, 0.006))
    for key, (shape_id, color) in LINE_SHAPES.items()
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        center=SAN_FRANCISCO_CENTER,
        zoom=13,
        map_title="San Francisco Muni Metro Business Density Heatmap",
        city_name="San Francisco",
        system_name="Muni Metro",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"naics": str}),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Muni Metro"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
    )


if __name__ == "__main__":
    main()
