"""Step 3 - Render Monterrey (Regional)'s heatmap to a standalone HTML file.

Thin, like every other city's, and shaped like Guadalajara's: the line geometry
comes from OpenStreetMap route relations (Nuevo León publishes no Metrorrey
feed), and `label_focus` is the union of the four municipios, read from step
1's cached boundaries so the map and the station scope cannot disagree.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.monterrey.step1_stations import load_boundaries         # noqa: E402
from pipeline.monterrey.config import (                               # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# (OSM ref, colour, real public name, label end) - Guadalajara's shape.
LINE_SPECS = {
    ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], None)
    for ref in LINE_NAMES
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run step1 and step2 first.")

    _by_muni, union = load_boundaries()

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Metrorrey: commercial density around Monterrey stations",
        city_name="Monterrey",
        system_name="Metrorrey",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(OSM_ROUTES_JSON, LINE_SPECS, "Metrorrey"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=union,
    )


if __name__ == "__main__":
    main()
