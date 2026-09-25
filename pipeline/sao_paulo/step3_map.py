"""Step 3 - Render São Paulo's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
São Paulo-specific.

Input:  data/sao_paulo/processed/stations.csv
        data/sao_paulo/processed/businesses_clean.csv
        data/sao_paulo/raw/osm_rail.json
        data/sao_paulo/raw/osm_boundary.json             (label anchoring)
Output: outputs/sao_paulo/heatmap.html

Run:  python pipeline/sao_paulo/step3_map.py

Lines from OpenStreetMap through load_osm_line_shapes (the owner's
2026-09-23 decision), keyed on `ref`: 1-5 are route=subway, 15 is
route=monorail, and no other relation carries those refs.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.sao_paulo.boundary import city_polygon  # noqa: E402
from pipeline.sao_paulo.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_ORDER,
    OSM_RAIL_JSON,
    OSM_TRAIN_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Metrô and CPTM"
LINE_LABEL_ENDS = {}
# CPTM's Line 9 lives in the train cache; the metro and monorail in the rail one.
TRAIN_REFS = ("9",)


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_RAIL_JSON, OSM_TRAIN_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    line_specs = {ln: (ln, LINE_COLOURS[ln], LINE_NAMES[ln], LINE_LABEL_ENDS.get(ln))
                  for ln in LINE_ORDER}
    lines = load_osm_line_shapes(
        OSM_RAIL_JSON, {k: v for k, v in line_specs.items() if k not in TRAIN_REFS}, SYSTEM)
    lines.update(load_osm_line_shapes(
        OSM_TRAIN_JSON, {k: v for k, v in line_specs.items() if k in TRAIN_REFS}, SYSTEM))
    missing = [ln for ln in LINE_ORDER if ln not in lines]
    if missing:
        sys.exit(f"no geometry for {missing}")
    render_heatmap(
        output_path=HEATMAP_HTML,
        # Mobile mode (owner, 2026-09-25): a light map without dots.
        lite_output_path=HEATMAP_HTML.with_name("heatmap_lite.html"),
        map_title="São Paulo Metrô and CPTM Business Density Heatmap",
        city_name="São Paulo",
        system_name=SYSTEM,
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
