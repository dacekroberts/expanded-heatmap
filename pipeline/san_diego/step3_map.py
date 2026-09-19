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

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.san_diego.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    TAXONOMY_SYSTEM,
)

SAN_DIEGO_CENTER = [32.7157, -117.1611]

# key -> (shape_id, color, real-world public-facing name, label offset in
# degrees). shape_id is each line's single most-used trip shape (counted
# per route, 2026-09-18) - re-derive if the GTFS feed is
# re-downloaded. The name is what MTS itself uses on signage (confirmed via
# Wikipedia's "<Color> Line (San Diego Trolley)" articles), not the GTFS
# route_short_name, which lacks "Line". Offset defaults to 0.006 deg
# (~650m); Silver gets a larger one because its whole route is the short
# downtown loop, where the default landed the label on the dense downtown
# business-cluster markers.
TROLLEY_LINE_SHAPES = {
    "Blue": ("510_0_352", "#0071bc", "Blue Line", 0.006),
    "Orange": ("520_3_283", "#f7941d", "Orange Line", 0.006),
    "Green": ("530_3_355", "#39b54a", "Green Line", 0.006),
    "Copper": ("535_2_2", "#b87333", "Copper Line", 0.006),
    "Silver": ("550_8_3", "#a6a6a6", "Silver Line", 0.016),
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        center=SAN_DIEGO_CENTER,
        zoom=12,
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
    )


if __name__ == "__main__":
    main()
