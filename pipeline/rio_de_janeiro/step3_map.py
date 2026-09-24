"""Rio de Janeiro step 3: render the heatmap - all rendering in pipeline/map_common.py.

    python pipeline/rio_de_janeiro/step3_map.py

The lines are step 1's GeoJSON: the metro's agency geometry and the VLT's OSM
ways, one feature per line keyed on `line`.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.rio_de_janeiro import config as c  # noqa: E402
from pipeline.rio_de_janeiro.boundary import city_polygon  # noqa: E402

LINE_LABEL_ENDS = {}


def main():
    for path in (c.STATIONS_CSV, c.BUSINESSES_CLEAN_CSV, c.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {ln: (ln, c.LINE_COLOURS[ln], c.LINE_NAMES[ln], LINE_LABEL_ENDS.get(ln))
             for ln in c.LINE_ORDER}
    lines = load_geojson_line_shapes(c.LINES_GEOJSON, specs, c.SYSTEM)
    missing = [ln for ln in c.LINE_ORDER if ln not in lines]
    if missing:
        sys.exit(f"no geometry for {missing}")
    render_heatmap(
        output_path=c.HEATMAP_HTML, map_title=c.MAP_TITLE, city_name=c.NAME,
        system_name=c.SYSTEM, stations=pd.read_csv(c.STATIONS_CSV),
        businesses=pd.read_csv(c.BUSINESSES_CLEAN_CSV), taxonomy_system=c.TAXONOMY_SYSTEM,
        lines=lines, crs_geographic=c.CRS_GEOGRAPHIC, crs_projected=c.CRS_PROJECTED,
        ring_edges_meters=c.RING_EDGES_METERS, ring_labels=c.RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
