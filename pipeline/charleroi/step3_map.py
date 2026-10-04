"""Step 3 - Render Charleroi's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Charleroi-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/charleroi/processed/stations.csv
        data/charleroi/processed/businesses_clean.csv
        data/belgium/raw/tec_gtfs_static.zip           (the line overlay)
        data/charleroi/raw/osm_communes.json           (label anchoring)
Output: outputs/charleroi/heatmap.html

Run:  python pipeline/charleroi/step3_map.py

The lines come from the feed's shapes.txt (config.LINE_SHAPES, checked by step
1), drawn whole: M2 runs on to Anderlues (owner, 2026-10-03), and its stops
outside the commune get no ring. Labels are the bare line names.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.charleroi.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    COMMUNE_AREA_KM2,
    FETCH,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    LINES,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_SHAPES,
    NIS,
    OSM_COMMUNES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    TAXONOMY_SYSTEM,
)
from pipeline.countries.belgium import commune_geometry  # noqa: E402

SYSTEM = "Light metro"

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the commune - override only if a rendered
# map shows that landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (LINE_SHAPES[key], LINE_COLOURS[key], LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key in LINES
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP):
        if not path.exists():
            sys.exit(f"Missing {path}. Run {FETCH} and the earlier steps first.")
    lines = load_line_shapes(GTFS_ZIP, LINE_SPECS, SYSTEM)
    missing = sorted(set(LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Charleroi Light Metro Business Density Heatmap",
        city_name="Charleroi",
        system_name=SYSTEM,
        stations=pd.read_csv(STATIONS_CSV, dtype={"lines": str}),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=commune_geometry(OSM_COMMUNES_JSON, FETCH, NIS, COMMUNE_AREA_KM2,
                                     "Charleroi"),
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # accented letters in the names it prints. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
