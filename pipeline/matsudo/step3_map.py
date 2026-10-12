"""Step 3 - Render Matsudo's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Matsudo-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/matsudo/processed/stations.csv
        data/matsudo/processed/businesses_clean.csv
        data/matsudo/processed/lines.geojson       (N02 track, from step 1)
        data/japan/raw/N03-20250101_12_GML.zip    (label anchoring ONLY)
Output: outputs/matsudo/heatmap.html

Run:  python pipeline/matsudo/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.matsudo import config  # noqa: E402

SYSTEM_NAME = "Matsudo rail"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (key, spec["colour"], spec["name"], LINE_LABEL_ENDS.get(key))
    for key, spec in config.LINES.items()
}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Matsudo Rail Business Density Heatmap",
        city_name="Matsudo",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        # The city line anchors each label on its line's in-city stretch: the
        # Keisei Matsudo Line runs on to Kamagaya, the JR Joban Line to
        # Katsushika (Tokyo) and Kashiwa, the JR Musashino Line to Nagareyama
        # and Ichikawa, the Hokuso and Narita Sky Access lines to Katsushika,
        # Ichikawa and Kamagaya, the Ryutetsu to Nagareyama, the Tobu Urban
        # Park Line to Kashiwa and Kamagaya. N03 is used here and NEVER
        # drawn (the Survey Act; japan.city_boundary).
        label_focus=japan.city_boundary(config.SLUG),
        # Trade names are Japanese; this orders the Japanese faces first
        # (theme.font_stack) and render_heatmap raises without it.
        lang="ja",
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Han and kana. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
