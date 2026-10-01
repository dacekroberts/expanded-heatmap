"""Step 3 - Render New Orleans's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
New Orleans-specific.

Input:  data/new_orleans/processed/stations.csv
        data/new_orleans/processed/businesses_clean.csv
        data/new_orleans/raw/osm_rail.json                (the line, OSM's route relations)
        data/new_orleans/raw/city_boundary_tiger.geojson  (label anchoring)
Output: outputs/new_orleans/heatmap.html

Run:  python pipeline/new_orleans/step3_map.py

The lines come from OSM through load_osm_line_shapes, drawn whole: every
line lies entirely inside the city. 47's relations also carry Loyola Avenue,
which RTA's 47 does not run; config.LINE_WAYS_NOT_DRAWN takes those ways out
of the cached answer before the shared loader reads it (2026-10-01).
"""
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_orleans.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAWN_LINES,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_WAYS_NOT_DRAWN,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.new_orleans.step1_stations import city_polygon  # noqa: E402
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "RTA streetcars"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def without_ways_not_drawn(path):
    """The cached Overpass answer with `LINE_WAYS_NOT_DRAWN` taken out of its
    line's relations (47's Loyola Avenue ways), for the shared loader to draw
    as it draws every city. Exits on an id no longer in that line's relations."""
    data = json.loads(path.read_text(encoding="utf-8"))
    for ref, ways in LINE_WAYS_NOT_DRAWN.items():
        rels = [e for e in data["elements"] if e["type"] == "relation"
                and e.get("tags", {}).get("ref") == ref]
        seen = set()
        for r in rels:
            seen |= {m["ref"] for m in r["members"]
                     if m["type"] == "way" and m["ref"] in ways}
            r["members"] = [m for m in r["members"]
                            if not (m["type"] == "way" and m["ref"] in ways)]
        stale = sorted(set(ways) - seen)
        if stale:
            sys.exit(f"LINE_WAYS_NOT_DRAWN {ref}: way(s) {stale} are no longer in "
                     f"{ref}'s relations - re-read OSM and update the entry")
        print(f"  {ref}: {len(ways)} way(s) not drawn ({', '.join(sorted(set(ways.values())))})")
    return data


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    line_specs = {ref: (ref, LINE_COLOURS[ref], LINE_NAMES[ref], LINE_LABEL_ENDS.get(ref))
                  for ref in DRAWN_LINES}
    with tempfile.TemporaryDirectory() as tmp:
        drawn = Path(tmp) / OSM_ROUTES_JSON.name
        drawn.write_text(json.dumps(without_ways_not_drawn(OSM_ROUTES_JSON)),
                         encoding="utf-8")
        lines = load_osm_line_shapes(drawn, line_specs, SYSTEM)
    missing = sorted(set(DRAWN_LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come "
                 f"from real geometry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="New Orleans Streetcar Business Density Heatmap",
        city_name="New Orleans",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(),
    )


if __name__ == "__main__":
    main()
