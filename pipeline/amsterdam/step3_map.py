"""Step 3 - Render Amsterdam's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Amsterdam-specific.

Input:  data/amsterdam/processed/stations.csv
        data/amsterdam/processed/businesses_clean.csv
        data/amsterdam/processed/gvb_rail_shapes.zip   (step 1's extract)
        data/amsterdam/processed/line_shapes.json      (step 1's choice)
        data/amsterdam/raw/osm_boundary.json           (label anchoring)
Output: outputs/amsterdam/heatmap.html

Run:  python pipeline/amsterdam/step3_map.py

Each line is drawn from the shapes step 1 chose to cover its REGULAR route -
Dublin's rule (shapes in descending use, keep any that reaches a stop the kept
ones do not), restricted to trips whose every stop is regular, so a works
diversion is never what is drawn. Lines that run on into Amstelveen, Diemen,
Ouder-Amstel or Uithoorn are drawn whole, though their stations there are
uncounted - the network a reader rides is drawn, and the rings are what the
map counts.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.amsterdam.boundary import city_polygon  # noqa: E402
from pipeline.amsterdam.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GVB_SHAPES_ZIP,
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
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402

SYSTEM_NAME = "GVB metro and tram"

# Which end a line's label goes at, where the automatic tail choice lands
# badly. Empty until a render shows a need.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GVB_SHAPES_ZIP, LINE_SHAPES_JSON):
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

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Amsterdam Metro and Tram Business Density Heatmap",
        city_name="Amsterdam",
        system_name=SYSTEM_NAME,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GVB_SHAPES_ZIP, line_specs, SYSTEM_NAME),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
