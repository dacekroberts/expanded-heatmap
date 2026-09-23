"""Step 3 - Render Lille (Regional)'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Lille-specific.

Input:  data/lille/processed/stations.csv
        data/lille/processed/businesses_clean.csv
        data/lille/processed/tram_lines_by_line.geojson   (step 1, from MEL)
        data/lille/processed/served_boundary.geojson      (step 1, label focus)
        data/lille/raw/osm_routes.json                    (métro geometry)
Output: outputs/lille/heatmap.html

Run:  python pipeline/lille/step3_map.py

THE FIRST CITY DRAWN FROM TWO LINE LOADERS AT ONCE. The tram comes through
load_geojson_line_shapes (Madrid's path) from MEL's first-party layer; the
métro through load_osm_line_shapes (Mexico City's path), because no agency
layer carries it. Both return the same {key: (segments, colour, label, end)}
contract, so the two dicts simply merge and render_heatmap never learns there
were two sources - which is the point of keeping all three loaders in
map_common rather than forking it.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.lille.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINES,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    SERVED_BOUNDARY_GEOJSON,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
    TRAM_LINES_BY_LINE_GEOJSON,
)
from pipeline.map_common import (  # noqa: E402
    load_geojson_line_shapes,
    load_osm_line_shapes,
    render_heatmap,
)

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at. Override only if a render shows one badly.
LINE_LABEL_ENDS = {}

SYSTEM = "Métro and Tramway"


def specs(mode):
    return {key: (source_key, LINE_COLOURS[key], LINE_NAMES[key],
                  LINE_LABEL_ENDS.get(key))
            for key, (m, source_key, _name) in LINES.items() if m == mode}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, TRAM_LINES_BY_LINE_GEOJSON,
                 SERVED_BOUNDARY_GEOJSON, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run fetch_sources.py and the earlier steps.")

    lines = {}
    lines.update(load_osm_line_shapes(OSM_ROUTES_JSON, specs("metro"), SYSTEM))
    lines.update(load_geojson_line_shapes(TRAM_LINES_BY_LINE_GEOJSON,
                                          specs("tram"), SYSTEM,
                                          key_property="line"))
    missing = sorted(set(LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - every drawn line needs real "
                 f"geometry, a label and a legend entry")
    for key, (segments, colour, label, _end) in lines.items():
        print(f"  {label:10} {colour}  {len(segments)} segment(s), "
              f"{sum(len(s) for s in segments)} vertices")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Lille (Regional) Métro and Tramway Business Density Heatmap",
        city_name="Lille (Regional)",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        # The eleven served communes, not the commune of Lille: every line's
        # label belongs on the stretch this map counts, and that is all eleven.
        label_focus=shape(json.loads(SERVED_BOUNDARY_GEOJSON.read_text(
            encoding="utf-8"))["geometry"]),
    )


if __name__ == "__main__":
    main()
