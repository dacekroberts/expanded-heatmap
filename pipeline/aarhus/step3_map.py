"""Step 3 - Render Aarhus's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Aarhus-specific.

Input:  data/aarhus/processed/stations.csv
        data/aarhus/processed/businesses_clean.csv
        data/aarhus/processed/lines.geojson   (L2 cut to the new tramway, step 1)
        data/aarhus/raw/osm_kommuner.json     (label anchoring)
Output: outputs/aarhus/heatmap.html

Run:  python pipeline/aarhus/step3_map.py

Lines come from OSM, through step 1's GeoJSON (Madrid's loader path) rather
than load_osm_line_shapes: that loader draws a relation whole, and L2's
relations run on to Odder over Odderbanen, which is out of scope. Step 1 cuts
L2 at Aarhus H and keeps the Lisbjergskolen branch, so what is drawn is the
new city tramway and nothing else. L1 is not drawn (config).
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.aarhus.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAWN_LINES,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.aarhus.kommuner import scope_geometry  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "Letbanen"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the kommune.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    line_specs = {ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
                  for ref in DRAWN_LINES}
    lines = load_geojson_line_shapes(LINES_GEOJSON, line_specs, SYSTEM)
    missing = sorted(set(DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Aarhus Letbanen Business Density Heatmap",
        city_name="Aarhus",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=scope_geometry(),
    )


if __name__ == "__main__":
    main()
