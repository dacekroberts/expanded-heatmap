"""Step 3 - Render Kansas City's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Kansas City-specific.

Input:  data/kansas_city/processed/stations.csv
        data/kansas_city/processed/businesses_clean.csv
        data/kansas_city/raw/osm_rail.json                (the line, OSM's route relations)
        data/kansas_city/raw/city_boundary_tiger.geojson  (label anchoring)
Output: outputs/kansas_city/heatmap.html

Run:  python pipeline/kansas_city/step3_map.py

The line comes from OSM through load_osm_line_shapes, drawn whole: the
streetcar lies entirely inside the city.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.kansas_city.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAWN_LINES,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.kansas_city.step1_stations import city_polygon  # noqa: E402
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "KC Streetcar"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    line_specs = {ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
                  for ref in DRAWN_LINES}
    lines = load_osm_line_shapes(OSM_ROUTES_JSON, line_specs, SYSTEM)
    missing = sorted(set(DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="KC Streetcar Business Density Heatmap",
        city_name="Kansas City",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(),
    )


if __name__ == "__main__":
    main()
