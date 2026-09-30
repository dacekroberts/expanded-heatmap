"""Step 3 - Render Palma's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Palma-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/palma/processed/stations.csv
        data/palma/processed/businesses_clean.csv
        data/palma/processed/lines.geojson        (Metro M1, step 1, OSM)
        data/palma/raw/city_boundary.geojson      (label anchoring)
Output: outputs/palma/heatmap.html

Run:  python pipeline/palma/step3_map.py

The line is OSM's, through step 1's GeoJSON (track ways only) and Madrid's
loader path, as Ottawa's and Kitchener–Waterloo's are.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.palma.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Metro de Palma"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {k: (k, LINE_COLOURS[k], LINE_NAMES[k], LINE_LABEL_ENDS.get(k)) for k in LINE_NAMES}
    lines = load_geojson_line_shapes(LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(LINE_NAMES):
        sys.exit(f"geometry for {sorted(lines)}, not every line in {sorted(LINE_NAMES)} - a "
                 "line this project draws must come from real geometry")
    city = shape(json.loads(CITY_BOUNDARY_GEOJSON.read_text(encoding="utf-8"))["geometry"])
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    for col in ("latitude", "longitude"):
        businesses[col] = pd.to_numeric(businesses[col])
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Palma Metro Business Density Heatmap",
        city_name="Palma",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city,
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
