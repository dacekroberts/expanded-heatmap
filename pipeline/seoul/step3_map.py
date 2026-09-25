"""Step 3 - Render Seoul's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Seoul-specific. The lines are the ones step 1 wrote to
processed/rail_lines.json - one relation per drawn line, in the shape
load_osm_line_shapes reads.

Run:  python pipeline/seoul/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.seoul import config  # noqa: E402
from pipeline.seoul.step1_stations import boundary_polygon  # noqa: E402


def render(output_path, pins):
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.RAIL_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=output_path,
        map_title="Seoul Metropolitan Subway Business Density Heatmap",
        city_name="Seoul",
        system_name="Seoul Metropolitan Subway",
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(config.RAIL_LINES_JSON, config.LINES,
                                   "Seoul Metropolitan Subway"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=boundary_polygon(),
        # Trade names are Korean; this orders the Korean faces first
        # (theme.font_stack) and render_heatmap raises without it.
        lang="ko",
        # No whole-city heat layer (owner, 2026-09-25): at 239,410 storefronts it
        # carried nearly a quarter of a million points a second time, and the
        # 30 MB map would not load on the owner's phone. 94% of the storefronts
        # are inside the rings anyway. Mexico City's precedent; the page says so.
        all_city_heat=False,
        pins=pins,
    )


def main():
    render(config.HEATMAP_HTML, pins=True)
    # Mobile mode (owner, 2026-09-25): the same map without business dots,
    # which a phone cannot hold in memory for Seoul.
    render(config.HEATMAP_LITE_HTML, pins=False)


if __name__ == "__main__":
    main()
