"""Step 3 - Render Brussels (Regional)'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Brussels (Regional)-specific.

Input:  data/brussels_regional/processed/stations.csv
        data/brussels_regional/processed/businesses_clean.csv
        data/brussels_regional/processed/line_shapes.json  (step 1's choice of shapes)
        data/brussels/raw/stib_gtfs.zip                    (the shapes themselves)
        data/brussels/raw/communes_region_bruxelles.geojson (label anchoring)
Output: outputs/brussels_regional/heatmap.html

Run:  python pipeline/brussels_regional/step3_map.py

Every STIB metro and tram line is drawn whole, from the shapes step 1 chose
to cover its regular route; labels anchor on the 18 communes, the scope. The
City of Brussels' stations are the Brussels page's and carry no rings here.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.brussels_regional.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_COMMUNE_CODE,
    COMMUNES_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_ORDER,
    LINE_SHAPES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.countries.belgium import brussels_region_communes  # noqa: E402
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402

SYSTEM_NAME = "STIB-MIVB metro and tram"

# Which end a line's label goes at, where the automatic tail choice lands
# badly. Empty until a render shows a need.
LINE_LABEL_ENDS = {}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP, LINE_SHAPES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    chosen = json.loads(LINE_SHAPES_JSON.read_text(encoding="utf-8"))
    missing = [ln for ln in LINE_ORDER if not chosen.get(ln)]
    if missing:
        sys.exit(f"no shape for {missing} - a line this project draws must come from "
                 f"real geometry")
    line_specs = {ln: (tuple(chosen[ln]), LINE_COLOURS[ln], LINE_NAMES[ln],
                       LINE_LABEL_ENDS.get(ln))
                  for ln in LINE_ORDER}
    for ln in LINE_ORDER:
        print(f"  {LINE_NAMES[ln]:<9} {LINE_COLOURS[ln]}  {len(chosen[ln])} shape(s)")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")
    com = brussels_region_communes(COMMUNES_GEOJSON, "pipeline/brussels/fetch_sources.py")
    scope = com[com["nis"] != CITY_COMMUNE_CODE].geometry.union_all()

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Brussels (Regional) Metro and Tram Business Density Heatmap",
        city_name="Brussels (Regional)",
        system_name=SYSTEM_NAME,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, line_specs, SYSTEM_NAME),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=scope,
    )


if __name__ == "__main__":
    main()
