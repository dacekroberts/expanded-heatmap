"""Step 3 - Render Gelsenkirchen's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Gelsenkirchen-specific. Geneva's step 3.

Input:  data/gelsenkirchen/processed/stations.csv
        data/gelsenkirchen/processed/businesses_clean.csv
        data/gelsenkirchen/raw/osm_rail.json         (the lines, OSM's route relations)
        data/gelsenkirchen/raw/osm_boundaries.json   (label anchoring)
Output: outputs/gelsenkirchen/heatmap.html

Run:  python pipeline/gelsenkirchen/step3_map.py

The lines come from OSM through load_osm_line_shapes, drawn whole: 302 is
drawn to Langendreer, 107 to Bredeney and U11 to Messe/Gruga, and their stops
beyond the city line get no ring.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402
from pipeline.gelsenkirchen import config  # noqa: E402
from pipeline.gelsenkirchen.boundary import city_geometry  # noqa: E402

# Two operators (BOGESTRA's 301 and 302, Ruhrbahn's 107 and U11), so the
# layer prefix names the modes, as Berlin's does.
SYSTEM = "Tram and Stadtbahn"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def check_osm_colours():
    """Every drawn ref's relations still carry the colour config records
    (None where OSM records none and the project's own colour is drawn)."""
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e["type"] == "relation" and e.get("tags", {}).get("route") in config.ROUTES]
    for ref in config.DRAWN_LINES:
        seen = {(r["tags"].get("colour") or "").upper() or None
                for r in rels if r["tags"].get("ref") == ref}
        want = config.OSM_COLOURS.get(ref)
        if seen != {want.upper() if want else None}:
            sys.exit(f"{ref}: OSM's colour is now {sorted(map(str, seen))}, config records "
                     f"{want} - re-take the colour decision")


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    check_osm_colours()

    line_specs = {ref: (ref, config.LINE_COLOURS[ref], config.LINE_NAMES[ref],
                        LINE_LABEL_ENDS.get(ref)) for ref in config.DRAWN_LINES}
    lines = load_osm_line_shapes(config.OSM_ROUTES_JSON, line_specs, SYSTEM)
    missing = sorted(set(config.DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(config.STATIONS_CSV)
    businesses = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype={"id": str},
                             keep_default_na=False, na_values=[])
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Gelsenkirchen Tram Business Density Heatmap",
        city_name=config.NAME,
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


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
