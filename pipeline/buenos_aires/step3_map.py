"""Step 3 - Render Buenos Aires' heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Buenos Aires-specific. Lines come from step 1's lines.geojson (SBASE's track
layer, each line dissolved), coloured with the operator's line colours as OSM
tags them.

Input:  data/buenos_aires/processed/stations.csv
        data/buenos_aires/processed/businesses_clean.csv
        data/buenos_aires/processed/lines.geojson       (from step 1)
        data/buenos_aires/raw/osm_boundary.json         (label anchoring)
Output: outputs/buenos_aires/heatmap.html

Run:  python pipeline/buenos_aires/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.buenos_aires.step1_stations import load_boundary              # noqa: E402
from pipeline.buenos_aires import config                                     # noqa: E402

SYSTEM_NAME = "Subte"
# Per-line label end override: "start" or "end". Automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    ref: (ref, config.LINE_COLOURS[ref], config.LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
    for ref in config.LINE_NAMES
}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Buenos Aires Subte Business Density Heatmap",
        city_name="Buenos Aires",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=load_boundary(),
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
