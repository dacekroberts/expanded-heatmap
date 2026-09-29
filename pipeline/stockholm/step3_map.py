"""Step 3 - Render Stockholm's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Stockholm-specific. Lines come from step 1's lines.geojson (OSM route
relations, SL's three Tunnelbana lines, clipped to Stockholms kommun); the map
labels each line and the legend names its routes (Melbourne's treatment).

Input:  data/stockholm/processed/stations.csv
        data/stockholm/processed/businesses_clean.csv
        data/stockholm/processed/lines.geojson         (from step 1)
        data/stockholm/raw/city_boundary.geojson       (label anchoring)
Output: outputs/stockholm/heatmap.html

Run:  python pipeline/stockholm/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.stockholm import config  # noqa: E402

SYSTEM_NAME = "Tunnelbana"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (key, config.LINE_COLOURS[key], config.LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key in config.LINE_ORDER
}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Stockholm Tunnelbana Business Density Heatmap",
        city_name="Stockholm",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype={"objekt_id": str}),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city,
        legend_names=config.LEGEND_NAMES,
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
