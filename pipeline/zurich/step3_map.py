"""Step 3 - Render Zurich's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Zurich-specific.

Input:  data/zurich/processed/stations.csv
        data/zurich/processed/businesses_clean.csv
        data/zurich/raw/osm_rail.json        (the lines, OSM's route relations)
        data/zurich/raw/osm_gemeinden.json   (label anchoring)
Output: outputs/zurich/heatmap.html

Run:  python pipeline/zurich/step3_map.py

The lines come from OSM through load_osm_line_shapes, drawn whole: trams 2, 4,
10 and 50 are drawn to their ends outside the Stadt, whose stops get no ring.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.zurich.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAWN_LINES,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_COLOURS,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.zurich.gemeinden import city_geometry  # noqa: E402

SYSTEM = "VBZ"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the Stadt.
LINE_LABEL_ENDS = {}


def check_osm_colours():
    """Every drawn ref's relations still carry the colour config records."""
    rels = [e for e in json.loads(OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e["type"] == "relation" and e.get("tags", {}).get("route") == "tram"]
    for ref in DRAWN_LINES:
        seen = {(r["tags"].get("colour") or "").upper() for r in rels if r["tags"].get("ref") == ref}
        if seen != {OSM_COLOURS[ref].upper()}:
            sys.exit(f"tram {ref}: OSM's colour is now {sorted(seen)}, config records "
                     f"{OSM_COLOURS[ref]} - re-take the colour decision")


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    check_osm_colours()

    line_specs = {ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
                  for ref in DRAWN_LINES}
    lines = load_osm_line_shapes(OSM_ROUTES_JSON, line_specs, SYSTEM)
    missing = sorted(set(DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Zurich VBZ Tram Business Density Heatmap",
        city_name="Zurich",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # some letters. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
