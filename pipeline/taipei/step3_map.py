"""Step 3 - Render Taipei (Regional)'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Taipei-specific. The lines are the ones step 1 wrote to
processed/rail_lines.json, one relation per drawn line.

Run:  python pipeline/taipei/step3_map.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.taipei import config  # noqa: E402


def label_focus(stations):
    """No boundary is read (step 1): the labels are focused on the kept
    stations' extent, 1.5 km around them, so the Airport MRT's label lands on
    its in-region stretch rather than in Taoyuan."""
    import geopandas as gpd
    pts = gpd.GeoSeries(gpd.points_from_xy(stations.longitude, stations.latitude),
                        crs=config.CRS_GEOGRAPHIC)
    hull = pts.to_crs(config.CRS_PROJECTED).union_all().convex_hull.buffer(1500)
    return gpd.GeoSeries([hull], crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).iloc[0]


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.RAIL_LINES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    stations = pd.read_csv(config.STATIONS_CSV)
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Taipei (Regional) Metro Business Density Heatmap",
        city_name="Taipei (Regional)",
        system_name="Taipei Metro",
        stations=stations,
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(
            config.RAIL_LINES_JSON,
            {k: (k, s["colour"], s["name"], None) for k, s in config.LINES.items()},
            "Taipei Metro"),
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=label_focus(stations),
        lang="zh-TW",
    )


if __name__ == "__main__":
    main()
