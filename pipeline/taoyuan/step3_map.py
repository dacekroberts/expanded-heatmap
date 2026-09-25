"""Step 3 - Render Taoyuan's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Taoyuan-specific. The line is the one step 1 wrote to processed/rail_lines.json.

Run:  python pipeline/taoyuan/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.taoyuan import config  # noqa: E402


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.RAIL_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    stations = pd.read_csv(config.STATIONS_CSV)
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Taoyuan Airport MRT Business Density Heatmap",
        city_name="Taoyuan",
        system_name="Taoyuan Metro",
        stations=stations,
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(
            config.RAIL_LINES_JSON,
            {config.LINE_KEY: (config.LINE_KEY, config.LINE_COLOUR, config.LINE_NAME, None)},
            "Taoyuan Metro"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        # The line runs on to Taipei; its label belongs on the Taoyuan stretch,
        # so the focus is the kept stations' own extent.
        label_focus=config.label_focus(stations),
        lang="zh-TW",
    )


if __name__ == "__main__":
    main()
