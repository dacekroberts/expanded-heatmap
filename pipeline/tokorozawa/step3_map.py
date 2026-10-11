"""Step 3 - Render Tokorozawa's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Tokorozawa-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/tokorozawa/processed/stations.csv
        data/tokorozawa/processed/businesses_clean.csv
        data/tokorozawa/processed/lines.geojson         (N02 track, from step 1)
        data/japan/raw/N03-20250101_11_GML.zip    (label anchoring ONLY)
Output: outputs/tokorozawa/heatmap.html

Run:  python pipeline/tokorozawa/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan  # noqa: E402
from pipeline.tokorozawa import config  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402

SYSTEM_NAME = "Tokorozawa rail"
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
        map_title="Tokorozawa Rail Business Density Heatmap",
        city_name="Tokorozawa",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        # The city line anchors each label on the in-city stretch of lines that
        # run on to Ikebukuro, Hanno, Seibu-Shinjuku, Hon-Kawagoe, Tamako,
        # Fuchuhommachi and Nishi-Funabashi. N03 is used here and NEVER drawn
        # (the Survey Act; japan.city_boundary).
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
