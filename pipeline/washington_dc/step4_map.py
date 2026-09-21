"""Step 4 - Render Washington D.C.'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
D.C.-specific.

Input:  data/washington_dc/processed/stations.csv
        data/washington_dc/processed/businesses_geocoded.csv
        data/washington_dc/raw/gtfs.zip              (for the line overlay)
        data/washington_dc/raw/city_boundary.geojson (label anchoring)
Output: outputs/washington_dc/heatmap.html

It is step FOUR, not three, because this city needs a geocoding step - the
register carries no coordinates on 6.9% of its storefront rows. Los Angeles is
the other city numbered this way, and nothing hardcodes the numbers:
pipeline/drift_check.py globs step*.py.

Run:  python pipeline/washington_dc/step4_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.washington_dc.config import (  # noqa: E402
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_GROUPS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Everything city-specific is in config.py, so this stays a thin assembly of
# it. Each spec is (shape_id(s), colour, real public name, label end). None of
# the six lines branches, so each needs only one shape - unlike Boston's Green
# Line or Miami's Metromover loops.
LINE_SPECS = {
    key: (LINE_SHAPES[key], LINE_NAMES[key][1], LINE_NAMES[key][0],
          LINE_LABEL_ENDS.get(key))
    for key in ROUTE_GROUPS
}


def district_boundary():
    """The District's own outline, for anchoring each line's label at the end
    farthest from the others.

    This matters more here than in most cities: 58 of 98 Metrorail stations are
    outside the District, so all six lines run far beyond the mapped area, and
    without this anchor every label would be taken on a stretch in Maryland or
    Virginia that the map never shows.
    """
    dc = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    dc = (dc.set_crs(CRS_GEOGRAPHIC) if dc.crs is None
          else dc.to_crs(CRS_GEOGRAPHIC))
    return dc.geometry.iloc[0]


def main():
    for path in (STATIONS_CSV, BUSINESSES_GEOCODED_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2, step3).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Washington D.C. Metrorail: commercial density around stations",
        city_name="Washington D.C.",
        system_name="Metrorail",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_GEOCODED_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Metrorail"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=district_boundary(),
    )


if __name__ == "__main__":
    main()
