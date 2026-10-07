"""Step 3 - Render Thessaloniki's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Thessaloniki-specific. The line is the one step 1 wrote to
processed/rail_lines.json, already cut at the city line, in the shape
load_osm_line_shapes reads (Gimhae's shape).

Input:  data/thessaloniki/processed/stations.csv
        data/thessaloniki/processed/businesses_clean.csv
        data/thessaloniki/processed/rail_lines.json
        data/thessaloniki/raw/osm_boundaries.json      (label anchoring)
Output: outputs/thessaloniki/heatmap.html

Run:  python pipeline/thessaloniki/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.thessaloniki import config  # noqa: E402
from pipeline.thessaloniki.step1_stations import boundary_polygon  # noqa: E402


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.RAIL_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    poly, _rel, _area = boundary_polygon(verbose=False)
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Thessaloniki Metro Business Density Heatmap",
        city_name="Thessaloniki",
        system_name="Thessaloniki Metro",
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(config.RAIL_LINES_JSON, config.LINES, "Thessaloniki Metro"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=poly,
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
