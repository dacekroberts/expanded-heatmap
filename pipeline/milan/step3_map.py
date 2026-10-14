"""Step 3 - Render Milan's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Milan-specific.

Input:  data/milan/processed/stations.csv
        data/milan/processed/businesses_clean.csv
        data/milan/processed/metro_lines.geojson   (written by step 1)
        data/milan/processed/tram_shapes.json      (written by step 1)
        data/milan/raw/gtfs.zip                    (tram geometry)
        data/milan/raw/confine_comune.geojson      (label anchoring)
Output: outputs/milan/heatmap.html

Run:  python pipeline/milan/step3_map.py
"""

import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.map_common import (  # noqa: E402
    load_geojson_line_shapes,
    load_line_shapes,
    render_heatmap,
)
from pipeline.milan.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    BOUNDARY_GEOJSON,
    LINES_GEOJSON,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    LINES,
    GTFS_ZIP,
    TAXONOMY_SYSTEM,
    TRAM_COLOURS,
    TRAM_SHAPES_JSON,
)

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail farthest from the other
# lines, on the stretch inside the comune. Override only if a rendered map
# shows one landing badly.
LINE_LABEL_ENDS = {}

# key -> (feature property value, colour, real public name, label end).
# THE COLOURS ARE THE AGENCY'S OWN, read from the GTFS `route_color`, so the
# project's rule keeps them even where they score badly against the category
# pins - the opposite of Dublin, whose feed carried none.
LINE_SPECS = {
    key: (source_key, colour, label, LINE_LABEL_ENDS.get(key))
    for key, (source_key, colour, label) in LINES.items()
}


def tram_specs():
    """The tram lines step 1 drew, each on the GTFS shapes it chose there.
    Keys are "T1".."T33", so tram 1 and metro M1 stay apart."""
    shapes = json.loads(TRAM_SHAPES_JSON.read_text(encoding="utf-8"))
    if set(shapes) != set(TRAM_COLOURS):
        sys.exit(f"step 1 drew tram lines {sorted(shapes)}; config colours "
                 f"{sorted(TRAM_COLOURS)}. Re-run the colour search (config).")
    return {f"T{key}": (tuple(ids), TRAM_COLOURS[key], f"Tram {key}", None)
            for key, ids in sorted(shapes.items(), key=lambda kv: int(kv[0]))}


def comune_geometry():
    """The comune as one polygon, so each line's label goes at the tail of its
    in-city stretch rather than out at Gessate or Rho."""
    data = json.loads(BOUNDARY_GEOJSON.read_text(encoding="utf-8"))
    gdf = gpd.GeoDataFrame.from_features(data["features"],
                                         crs=CRS_GEOGRAPHIC)
    return gdf.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON,
                 TRAM_SHAPES_JSON, GTFS_ZIP):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Milan Metro Business Density Heatmap",
        city_name="Milan",
        system_name="ATM metro and trams",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines={**load_geojson_line_shapes(LINES_GEOJSON, LINE_SPECS,
                                          "Metropolitana di Milano"),
               **load_line_shapes(GTFS_ZIP, tram_specs(), "ATM tram")},
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=comune_geometry(),
        place_index_url=place_index.index_url("milan"),
    )


if __name__ == "__main__":
    main()
