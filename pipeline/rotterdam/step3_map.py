"""Step 3 - Render Rotterdam's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Rotterdam-specific.

Input:  data/rotterdam/processed/stations.csv
        data/rotterdam/processed/businesses_clean.csv
        data/rotterdam/processed/ret_rail_shapes.zip   (step 1's extract)
        data/rotterdam/processed/line_shapes.json      (step 1's choice)
        data/rotterdam/raw/osm_boundary.json           (label anchoring)
Output: outputs/rotterdam/heatmap.html

Run:  python pipeline/rotterdam/step3_map.py

Each line is drawn from the shapes step 1 chose to cover its REGULAR route
(Amsterdam's rule, shared). Lines that run on into Schiedam, Vlaardingen,
Capelle, Spijkenisse, Barendrecht or The Hague are drawn whole, though their
stations there are uncounted - the network a reader rides is drawn, and the
rings are what the map counts.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.rotterdam.boundary import city_polygon  # noqa: E402
from pipeline.rotterdam.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_ORDER,
    LINE_SHAPES_JSON,
    RET_SHAPES_ZIP,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM_NAME = "RET metro and tram"

# Which end a line's label goes at, where the automatic tail choice lands
# badly. Empty until a render shows a need.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, RET_SHAPES_ZIP, LINE_SHAPES_JSON):
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
        map_title="Rotterdam Metro and Tram Business Density Heatmap",
        city_name="Rotterdam",
        system_name=SYSTEM_NAME,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(RET_SHAPES_ZIP, line_specs, SYSTEM_NAME),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(verbose=False),
    )


if __name__ == "__main__":
    main()
