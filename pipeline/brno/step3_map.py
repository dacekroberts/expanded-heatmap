"""Step 3 - Render Brno's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Brno-specific. Scaffolded by scripts/scaffold_city.py, then pointed at OSM.

Input:  data/brno/processed/stations.csv          (step 1, KORDIS's feed)
        data/brno/processed/businesses_clean.csv  (step 2)
        data/brno/raw/osm_tram.json               (the line geometry)
        data/brno/raw/osm_boundary.json           (label anchoring)
Output: outputs/brno/heatmap.html

Run:  python pipeline/brno/step3_map.py

THE LINES ARE OSM'S, THE STOPS AND COLOURS KORDIS'S. The feed has no
shapes.txt, so each line is drawn from OSM's route relations by `ref`, one
alignment per line (the relation with the most geometry, load_osm_line_shapes),
matched to the feed's route_short_name - the GTFS cities' "most-used shape"
rule, in OSM. Only relations of the operator are considered (step 1 checks
every drawn ref has one).
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.brno.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DATA_PROCESSED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_ORDER,
    OSM_TRAM_JSON,
    OSM_TRAM_OPERATOR,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)
from pipeline.brno import config  # noqa: E402
from pipeline.countries.czechia_boundary import city_polygon  # noqa: E402
from pipeline.map_common import load_osm_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "Brno trams"

# Per-line label end override: "start" or "end". The default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def operator_routes():
    """The OSM file filtered to the operator's route relations, so another
    operator's relation with the same ref can never be drawn."""
    payload = json.loads(OSM_TRAM_JSON.read_text(encoding="utf-8"))
    payload["elements"] = [e for e in payload["elements"] if e["type"] != "relation"
                           or e.get("tags", {}).get("operator") == OSM_TRAM_OPERATOR]
    out = DATA_PROCESSED / "osm_tram_operator.json"
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_TRAM_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run fetch_sources.py and the earlier steps first.")

    specs = {k: (k, LINE_COLOURS[k], LINE_NAMES[k], LINE_LABEL_ENDS.get(k)) for k in LINE_ORDER}
    lines = load_osm_line_shapes(operator_routes(), specs, SYSTEM)
    missing = sorted(set(LINE_ORDER) - set(lines), key=LINE_ORDER.index)
    if missing:
        sys.exit(f"no OSM geometry for line(s) {missing} - every drawn line needs real "
                 f"geometry, a label and a legend entry")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts, "
          f"{len(lines)} lines")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Brno Trams Business Density Heatmap",
        city_name="Brno",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_polygon(config, verbose=False),
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Czech letters. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
