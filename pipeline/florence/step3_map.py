"""Step 3 - Render Florence's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Florence-specific.

Input:  data/florence/processed/stations.csv
        data/florence/processed/businesses_clean.csv
        data/florence/raw/osm_rail.json        (the line, OSM's route relations)
        data/florence/raw/osm_comuni.json      (label anchoring)
Output: outputs/florence/heatmap.html

Run:  python pipeline/florence/step3_map.py

The lines come from OSM through load_osm_line_shapes, drawn whole: T1 is
drawn to its end in Scandicci (owner, call 17), whose stops get no ring.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.florence.config import (  # noqa: E402
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
from pipeline.florence.comuni import comune_geometry  # noqa: E402

SYSTEM = "Tramvia di Firenze"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the comune.
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
        map_title="Tramvia di Firenze Business Density Heatmap",
        city_name="Florence",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=comune_geometry(),
    )


if __name__ == "__main__":
    main()
