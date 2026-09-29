"""Step 3 - Render Berlin's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Berlin-specific. Lines come from step 1's lines.geojson (each line's GTFS
shape(s), chosen by rule there, because VBB reissues shape_ids every release).

Input:  data/berlin/processed/stations.csv
        data/berlin/processed/businesses_clean.csv
        data/berlin/processed/lines.geojson         (from step 1)
        data/berlin/raw/city_boundary.geojson       (label anchoring)
Output: outputs/berlin/heatmap.html

Run:  python pipeline/berlin/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.berlin import config  # noqa: E402

SYSTEM_NAME = "U-Bahn and S-Bahn"
# Per-line label end override: "start" or "end". Automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

# The on-map label is the line's own code, which is its public name ("U1",
# "S41"): BVG and S-Bahn Berlin sign nothing longer.
LINE_SPECS = {
    key: (key, config.LINE_COLOURS[key], config.LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key in config.LINE_ORDER
}


def city_geometry():
    """The Land, so each label goes at the tail of the in-Berlin stretch of the
    S-Bahn lines that run on into Brandenburg."""
    boundary = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    return boundary.geometry.union_all()


def main():
    missing_colour = sorted(set(config.LINE_NAMES) - set(config.LINE_COLOURS))
    if missing_colour:
        sys.exit(f"no colour for {missing_colour}: run scripts/line_colour_search.py berlin")
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Berlin U-Bahn and S-Bahn Business Density Heatmap",
        city_name="Berlin",
        system_name=SYSTEM_NAME,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype={"nace_id": str,
                                                                    "ihk_branch_id": str}),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, LINE_SPECS, SYSTEM_NAME),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
