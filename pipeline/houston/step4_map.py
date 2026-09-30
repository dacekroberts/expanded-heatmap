"""Step 4 - Render Houston's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Houston-specific.

Input:  data/houston/processed/stations.csv
        data/houston/processed/businesses_geocoded.csv  (step 3)
        data/houston/processed/lines.geojson            (Red, Green, Purple; step 1, OSM)
        data/houston/raw/city_boundary_tiger.geojson    (label anchoring)
Output: outputs/houston/heatmap.html

Run:  python pipeline/houston/step4_map.py

The lines come through step 1's GeoJSON (track ways only, one direction per
line) and Madrid's loader path.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.houston import config  # noqa: E402
from pipeline.houston.step1_stations import city_polygon  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "METRORail"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_PLACED_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {ref: (ref, config.LINE_COLOURS[ref], config.LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
             for ref in config.LINE_REFS}
    lines = load_geojson_line_shapes(config.LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(config.LINE_REFS):
        sys.exit("a drawn line has no geometry")
    stations = pd.read_csv(config.STATIONS_CSV)
    businesses = pd.read_csv(config.BUSINESSES_PLACED_CSV,
                             dtype={"zip": str, "permit": str, "naics": str})
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Houston METRORail Business Density Heatmap",
        city_name="Houston",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city_polygon(),
    )


if __name__ == "__main__":
    main()
