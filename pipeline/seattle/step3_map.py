"""Step 3 - Render Seattle (Regional)'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Seattle (Regional)-specific.

Input:  data/seattle/processed/stations.csv
        data/seattle/processed/businesses_clean.csv
        data/seattle/processed/lines.geojson          (1 and 2 Lines, step 1, OSM)
        data/seattle/processed/business_scope.geojson (label anchoring)
Output: outputs/seattle/heatmap.html

Run:  python pipeline/seattle/step3_map.py

The lines are OSM's, through step 1's GeoJSON (track ways only) and Madrid's
loader path. The two lines share track from Lynnwood City Center to
International District/Chinatown; each is drawn whole, under its own label.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.seattle.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_REFS,
    LINES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    SCOPE_GEOJSON,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Link light rail"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON, SCOPE_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {k: (k, LINE_COLOURS[k], LINE_REFS[k], LINE_LABEL_ENDS.get(k)) for k in LINE_REFS}
    lines = load_geojson_line_shapes(LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(LINE_REFS):
        sys.exit("a line has no geometry - a line this project draws must come "
                 "from real geometry")
    scope = gpd.read_file(SCOPE_GEOJSON).to_crs(CRS_GEOGRAPHIC).geometry.union_all()
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"naics": str})
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Seattle (Regional) Link Light Rail Business Density Heatmap",
        city_name="Seattle (Regional)",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=scope,
    )


if __name__ == "__main__":
    main()
