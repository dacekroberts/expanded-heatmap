"""Step 3 - Render Bremen's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Bremen-specific. Geneva's step 3.

Input:  data/bremen/processed/stations.csv
        data/bremen/processed/businesses_clean.csv
        data/bremen/raw/osm_rail.json        (the lines, OSM's route relations)
        data/bremen/raw/osm_boundary.json    (label anchoring)
Output: outputs/bremen/heatmap.html

Run:  python pipeline/bremen/step3_map.py

The lines come from OSM through load_osm_line_shapes, drawn whole: line 4 is
drawn to its Lilienthal end, and its stops there get no ring.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.bremen import config  # noqa: E402
from pipeline.bremen.boundary import city_geometry  # noqa: E402

SYSTEM = "BSAG"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def check_osm_colours():
    """Every drawn ref with an OSM colour still carries the one config records;
    a ref config colours from the project's palette still carries none."""
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e["type"] == "relation" and e.get("tags", {}).get("route") in config.ROUTES]
    for ref in config.DRAWN_LINES:
        seen = {(r["tags"].get("colour") or "").upper() for r in rels if r["tags"].get("ref") == ref
                and r["id"] not in config.NOT_DRAWN}
        want = {config.OSM_COLOURS[ref].upper()} if ref in config.OSM_COLOURS else {""}
        if seen != want:
            sys.exit(f"tram {ref}: OSM's colour is now {sorted(seen)}, config records "
                     f"{sorted(want)} - re-take the colour decision")


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    if set(config.LINE_COLOURS) != set(config.DRAWN_LINES):
        sys.exit("config.LINE_COLOURS must colour every drawn line")
    check_osm_colours()

    line_specs = {ref: (ref, config.LINE_COLOURS[ref], config.LINE_NAMES[ref],
                        LINE_LABEL_ENDS.get(ref)) for ref in config.DRAWN_LINES}
    lines = load_osm_line_shapes(config.OSM_ROUTES_JSON, line_specs, SYSTEM)
    missing = sorted(set(config.DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(config.STATIONS_CSV)
    businesses = pd.read_csv(config.BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} shops")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Bremen BSAG Tram Business Density Heatmap",
        city_name="Bremen",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=city_geometry(),
    )
    emit("lines_drawn", len(lines))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
