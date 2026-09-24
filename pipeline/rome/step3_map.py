"""Step 3 - Render Rome's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Rome-specific.

Input:  data/rome/processed/stations.csv
        data/rome/processed/businesses_clean.csv
        data/rome/processed/osm_lines.json   (step 1's kept relations)
        data/rome/raw/osm_boundary.json       (label anchoring)
Output: outputs/rome/heatmap.html

Run:  python pipeline/rome/step3_map.py

Lines come from OpenStreetMap through load_osm_line_shapes, on the ground
recorded in config.RAIL_SOURCE_GROUND. Metro C is drawn to its terminus at
Monte Compatri - Pantano, though that one station, outside the comune, is
uncounted.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.rome.boundary import city_polygon  # noqa: E402
from pipeline.rome.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_ORDER,
    OSM_LINES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Metro"
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    line_specs = {ln: (ln, LINE_COLOURS[ln], LINE_NAMES[ln], LINE_LABEL_ENDS.get(ln))
                  for ln in LINE_ORDER}
    lines = load_osm_line_shapes(OSM_LINES_JSON, line_specs, SYSTEM)
    missing = [ln for ln in LINE_ORDER if ln not in lines]
    if missing:
        sys.exit(f"no geometry for {missing} - every drawn line needs real geometry")
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")
    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Rome Metro Business Density Heatmap",
        city_name="Rome",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
