"""Step 3 - Render Liège's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Liège-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/liege/processed/stations.csv
        data/liege/processed/businesses_clean.csv
        data/belgium/raw/tec_gtfs_static.zip       (the line overlay)
        data/liege/raw/osm_communes.json           (label anchoring)
Output: outputs/liege/heatmap.html

Run:  python pipeline/liege/step3_map.py

T1 is drawn from three of the feed's shapes (config.LINE_SHAPES, checked by
step 1): the line forks at its northern end and runs one way each through the
centre, and one shape alone would leave four stops off the drawn line. The
label is the bare line name.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.liege.config import (  # noqa: E402
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

SYSTEM = "Tram"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the commune.
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
        map_title="Liège Tram Business Density Heatmap",
        city_name="Liège",
        system_name=SYSTEM,
        stations=pd.read_csv(STATIONS_CSV, dtype={"lines": str}),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=commune_geometry(OSM_COMMUNES_JSON, FETCH, NIS, COMMUNE_AREA_KM2, "Liège"),
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # accented letters in the names it prints. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
