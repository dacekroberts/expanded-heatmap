"""Step 3 - Render Mexico City's heatmap to a standalone HTML file.

Thin, like every other city's: the rendering lives in pipeline/map_common.py
and must not be forked here. The only thing unusual about this city is which
loader it calls - load_osm_line_shapes rather than load_line_shapes - because
every `*.cdmx.gob.mx` host is unreachable and the geometry comes from
OpenStreetMap. Both loaders return the same contract, so render_heatmap does
not know or care which one ran.
"""

import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.mexico_city.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Each spec is (OSM ref, colour, real public name, label end) - the same
# 4-tuple the GTFS cities use, with `ref` in place of a shape_id.
#
# Label ends are all automatic (None) for now: CDMX's twelve lines cross in the
# centre and each one's tail is unambiguous, unlike San Francisco's or Los
# Angeles' where a label had to be forced. Check the render before assuming
# that holds.
LINE_SPECS = {
    ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], None)
    for ref in LINE_NAMES
}


def city_boundary():
    """CDMX's own outline, for anchoring each line's label at the end farthest
    from the others. Same admin_level=4 relation step 1 filtered stations
    against, read from step 1's cache rather than re-fetched - so the map and
    the station scope cannot disagree about where the city is."""
    if not OSM_BOUNDARY_JSON.exists():
        sys.exit(f"Missing {OSM_BOUNDARY_JSON}. Run step1 first.")
    data = json.loads(OSM_BOUNDARY_JSON.read_text(encoding="utf-8"))
    rels = [e for e in data["elements"] if e["type"] == "relation"]
    lines = [
        [(p["lon"], p["lat"]) for p in m["geometry"]]
        for m in rels[0].get("members", [])
        if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")
    ]
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    if not polys:
        sys.exit("CDMX boundary did not assemble into a polygon.")
    return unary_union(polys)


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run step1 and step2 first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Metro CDMX: commercial density around stations",
        city_name="Mexico City",
        system_name="Metro CDMX and Tren Ligero",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(OSM_ROUTES_JSON, LINE_SPECS,
                                   "Metro CDMX and Tren Ligero"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_boundary(),
        # 283,345 coordinate pairs against 133,362 in the default layer - see
        # map_common. Stated on the city page rather than dropped silently.
        all_city_heat=False,
    )


if __name__ == "__main__":
    main()
