"""Step 3 - Render Guadalajara (Regional)'s heatmap to a standalone HTML file.

Thin, like every other city's. Calls load_osm_line_shapes for the same reason
Mexico City does, on different grounds: here a GTFS feed exists and was
rejected as three and a half years stale and missing Línea 4 entirely (see
config.py).

`label_focus` is the UNION of the four municipios, so each line's label is
anchored on the in-region stretch - Línea 4 runs out to Tlajomulco Centro and
Línea 3 to Arcos de Zapopan, and both would otherwise pull a label toward an
end that is far from the other lines.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.guadalajara.step1_stations import load_boundaries       # noqa: E402
from pipeline.guadalajara.config import (                             # noqa: E402
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

# (OSM ref, colour, real public name, label end) - the GTFS cities' 4-tuple
# with `ref` in place of a shape_id.
LINE_SPECS = {
    ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], None)
    for ref in LINE_NAMES
}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run step1 and step2 first.")

    # Reuses step 1's cached boundary rather than re-fetching, so the map and
    # the station scope cannot disagree about where the region is.
    _by_muni, union = load_boundaries()

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Tren Ligero: commercial density around Guadalajara stations",
        city_name="Guadalajara",
        system_name="Tren Ligero (Mi Tren)",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(OSM_ROUTES_JSON, LINE_SPECS, "Tren Ligero"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=union,
        # 117,454 businesses against a within-ring subset - the same shape that
        # made Mexico City's map 6.7 MB heavier. Off here too, and stated on
        # the city page.
        all_city_heat=False,
    )


if __name__ == "__main__":
    main()
