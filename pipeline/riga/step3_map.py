"""Step 3 - Render Riga's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Riga-specific: each tram line's most-used GTFS shape (chosen in step 1), this
project's colour for it, and the city outline for label placement.

Run:  python pipeline/riga/step3_map.py
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.riga import config  # noqa: E402
from pipeline.riga.step1_stations import city_polygon  # noqa: E402

# Per-line label end override ("start"/"end"); automatic unless a render shows
# a label landing badly.
LINE_LABEL_ENDS = {}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINE_SHAPES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    shapes = json.loads(config.LINE_SHAPES_JSON.read_text(encoding="utf-8"))
    specs = {s: (shapes[s], config.LINE_COLOURS[s], config.LINE_NAMES[s], LINE_LABEL_ENDS.get(s))
             for s in config.LINE_ORDER}
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Riga Tram Business Density Heatmap",
        city_name="Riga",
        system_name="Rīgas satiksme trams",
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_line_shapes(config.GTFS_ZIP, specs, "Rīgas satiksme trams"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city_polygon()[2],
    )


if __name__ == "__main__":
    main()
