"""Step 4 - Render Toronto's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
specific to Toronto.

Input:  data/toronto/processed/stations.csv
        data/toronto/processed/businesses_geocoded.csv
        data/toronto/raw/gtfs.zip                      (line overlay)
        data/toronto/raw/toronto_boundary_wgs84.zip    (label anchoring)
Output: outputs/toronto/heatmap.html

It is step FOUR, not three: Toronto's register carries no coordinates at all,
so step 3 geocodes against the City's own address points. Only Los Angeles and
Washington D.C. also number their map step 4, and they geocode against the US
Census bulk service - which has no Canadian equivalent, hence the address-point
join.

`label_focus` is the city boundary and it does real work here, unlike
Calgary's: Line 1 runs past the city limit into York Region, and two of its
stations (Highway 407 and Vaughan Metropolitan Centre) are excluded for that
reason. Without the focus, Line 1's label would be taken on the out-of-city
stretch.

Run:  python pipeline/toronto/step4_map.py
"""

import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.toronto.config import (  # noqa: E402
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    STREETCAR_COLOURS,
    STREETCAR_LEGEND_NAMES,
    STREETCAR_LINE_NAMES,
    STREETCAR_SHAPES_JSON,
    TAXONOMY_SYSTEM,
)

# Each spec is (shape_id, colour, real public name, label end).
LINE_SPECS = {
    rid: (LINE_SHAPES[rid], LINE_COLOURS[rid], LINE_NAMES[rid],
          LINE_LABEL_ENDS.get(rid))
    for rid in LINE_NAMES
}


def streetcar_specs():
    """The streetcar lines step 1 drew, each on the shapes it chose there. The
    on-map label is "Streetcar 501"; the legend row adds the street."""
    shapes = json.loads(STREETCAR_SHAPES_JSON.read_text(encoding="utf-8"))
    if set(shapes) != set(STREETCAR_COLOURS):
        sys.exit(f"step 1 drew streetcar lines {sorted(shapes)}; config colours "
                 f"{sorted(STREETCAR_COLOURS)}. Re-run the colour search (config).")
    return {key: (tuple(ids), STREETCAR_COLOURS[key], STREETCAR_LINE_NAMES[key], None)
            for key, ids in shapes.items()}


def city_boundary():
    """Toronto's own outline, for anchoring each line's label on the in-city
    stretch - Line 1 leaves the city, so this matters here."""
    b = gpd.read_file(CITY_BOUNDARY_ZIP)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("boundary has no geometry.")
    return b.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_GEOCODED_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_ZIP, STREETCAR_SHAPES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2, step3).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Toronto TTC: commercial density around stations",
        city_name="Toronto",
        system_name="TTC subway, LRT and streetcars",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_GEOCODED_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, {**LINE_SPECS, **streetcar_specs()}, "TTC"),
        legend_names={k: STREETCAR_LEGEND_NAMES[k] for k in STREETCAR_COLOURS},
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_boundary(),
        place_index_url=place_index.index_url("toronto"),
    )


if __name__ == "__main__":
    main()
