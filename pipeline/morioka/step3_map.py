"""Step 3 - Render Morioka's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Morioka-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/morioka/processed/stations.csv
        data/morioka/processed/businesses_clean.csv
        data/morioka/processed/lines.geojson          (N02 track, from step 1)
        data/japan/raw/N03-20250101_03_GML.zip       (label anchoring ONLY)
Output: outputs/morioka/heatmap.html

Run:  python pipeline/morioka/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan  # noqa: E402
from pipeline.morioka import config  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402

SYSTEM_NAME = "Morioka rail"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (key, spec["colour"], spec["name"], LINE_LABEL_ENDS.get(key))
    for key, spec in config.LINES.items()
}


def in_city_first(lines, city):
    """Each line's segments with the one holding most points inside the city
    line first. render_heatmap anchors a label on segments[0] (the longest),
    and N02 files a line in sections that can lie wholly outside the city
    (Gifu's step3_map.py, which found it; Akita's Oga Line). Only the order
    changes; every segment is still drawn."""
    from shapely.geometry import Point
    from shapely.prepared import prep

    focus = prep(city)

    def inside(seg):
        return sum(1 for lat, lon in seg if focus.contains(Point(lon, lat)))

    return {key: (sorted(segments, key=lambda s: (-inside(s), -len(s))), *rest)
            for key, (segments, *rest) in lines.items()}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    city = japan.city_boundary(config.SLUG)
    lines = in_city_first(load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME), city)
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Morioka Rail Business Density Heatmap",
        city_name="Morioka",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        # The city line anchors each label on the in-city stretch of lines that
        # run on to Takizawa, Yahaba, Iwate, Hachimantai, Miyako and beyond.
        # N03 is used here and NEVER drawn (the Survey Act; japan.city_boundary).
        label_focus=city,
        # Trade names are Japanese; this orders the Japanese faces first
        # (theme.font_stack) and render_heatmap raises without it.
        lang="ja",
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
