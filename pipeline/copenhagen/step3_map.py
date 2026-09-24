"""Step 3 - Render Copenhagen's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Copenhagen-specific.

Input:  data/copenhagen/processed/stations.csv
        data/copenhagen/processed/businesses_clean.csv
        data/copenhagen/raw/osm_rail.json       (line geometry)
        data/copenhagen/raw/osm_kommuner.json   (label anchoring)
Output: outputs/copenhagen/heatmap.html

Run:  python pipeline/copenhagen/step3_map.py

Lines come from OSM through load_osm_line_shapes - Lille's and Barcelona's
path - on the ground recorded in config: Rejseplanen's GTFS terms are
unresolved. One relation per line is drawn, the most complete of its
directions. S-tog's suburban reaches are DRAWN to their termini (Koge,
Hillerod, Frederikssund), though the 59 stations there are uncounted - the
network a reader rides is drawn whole, and the rings are what the map counts.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.copenhagen.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.copenhagen.kommuner import scope_geometry  # noqa: E402
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "Metro and S-tog"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the two kommuner.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    line_specs = {ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
                  for ref in LINE_NAMES}
    lines = load_osm_line_shapes(OSM_ROUTES_JSON, line_specs, SYSTEM)
    missing = sorted(set(LINE_NAMES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Copenhagen Metro and S-tog Business Density Heatmap",
        city_name="Copenhagen",
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
