"""Step 4 - Render Sacramento's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Sacramento-specific.

Input:  data/sacramento/processed/stations.csv
        data/sacramento/processed/businesses_geocoded.csv   (step 3)
        data/sacramento/processed/lines.geojson             (Blue, Gold; step 1, OSM)
        data/sacramento/raw/osm_boundaries.json             (label anchoring)
Output: outputs/sacramento/heatmap.html

Run:  python pipeline/sacramento/step4_map.py

The lines come through step 1's GeoJSON (track ways only, one direction per
line) and Madrid's loader path. The Green Line is suspended and not drawn.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.sacramento import config  # noqa: E402
from pipeline.sacramento.step1_stations import boundaries  # noqa: E402

SYSTEM = "SacRT light rail"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_GEOCODED_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {ref: (ref, config.LINE_COLOURS[ref], config.LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
             for ref in config.LINE_REFS}
    lines = load_geojson_line_shapes(config.LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(config.LINE_REFS):
        sys.exit("a drawn line has no geometry")
    b = boundaries()
    city = b[b["id"] == config.OSM_CITY_RELATION].geometry.iloc[0]
    stations = pd.read_csv(config.STATIONS_CSV)
    businesses = pd.read_csv(config.BUSINESSES_GEOCODED_CSV, dtype={"zip": str, "account": str})
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Sacramento SacRT Light Rail Business Density Heatmap",
        city_name="Sacramento",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city,
    )


if __name__ == "__main__":
    main()
