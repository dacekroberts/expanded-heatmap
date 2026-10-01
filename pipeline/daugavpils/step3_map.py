"""Step 3 - Render Daugavpils's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Daugavpils-specific.

Input:  data/daugavpils/processed/stations.csv
        data/daugavpils/processed/businesses_clean.csv
        data/daugavpils/raw/osm_rail.json       (the line, OSM's route relations)
        data/daugavpils/raw/osm_city.json       (label anchoring)
Output: outputs/daugavpils/heatmap.html

Run:  python pipeline/daugavpils/step3_map.py

The lines come from OSM through load_osm_line_shapes, each drawn whole (the
relation with the most geometry per ref): all four refs lie inside the city.
Ref 3 is the Stropu loop, which riders know as routes 3 and 5 (one loop run
each way), drawn once and labelled with both.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.daugavpils.config import (  # noqa: E402
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
from pipeline.daugavpils.step1_stations import city_polygon  # noqa: E402

SYSTEM = "Daugavpils tram"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the kommune.
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
        map_title="Daugavpils Tram Business Density Heatmap",
        city_name="Daugavpils",
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
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
