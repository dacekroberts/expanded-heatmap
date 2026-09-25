"""Step 3 - Render Hong Kong's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Hong Kong-specific. The lines are the ones step 1 wrote to
processed/rail_lines.json - one relation per drawn line, in the shape
load_osm_line_shapes reads, with each line's colour on it.

Run:  python pipeline/hong_kong/step3_map.py
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.hong_kong import config  # noqa: E402
from pipeline.hong_kong.step1_stations import boundary_polygon  # noqa: E402

# Per-line label end override ("start"/"end"); automatic unless a render shows
# a label landing badly.
LINE_LABEL_ENDS = {}


def line_specs():
    rels = json.loads(config.RAIL_LINES_JSON.read_text(encoding="utf-8"))["elements"]
    colour = {r["tags"]["ref"]: r["tags"]["colour"] for r in rels}
    return {k: (k, colour[k], config.LINE_NAMES[k], LINE_LABEL_ENDS.get(k))
            for k in config.LINE_ORDER}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.RAIL_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Hong Kong MTR Business Density Heatmap",
        city_name="Hong Kong",
        system_name="MTR",
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(config.RAIL_LINES_JSON, line_specs(), "MTR"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=boundary_polygon(),
        # Shop signs are Traditional Chinese in Hong Kong's own forms; without
        # this the Japanese faces drew every Han character (theme.font_stack).
        lang="zh-HK",
    )


if __name__ == "__main__":
    main()
