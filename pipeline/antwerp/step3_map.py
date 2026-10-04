"""Step 3 - Render Antwerp's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Antwerp-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/antwerp/processed/stations.csv
        data/antwerp/processed/businesses_clean.csv
        data/antwerp/processed/tram_shapes.zip    (step 1: the drawn shapes only)
        data/antwerp/processed/line_shapes.json   (step 1: each line's shapes)
        data/antwerp/raw/osm_communes.json        (label anchoring)
Output: outputs/antwerp/heatmap.html

Run:  python pipeline/antwerp/step3_map.py

Each line is drawn from De Lijn's own shapes.txt: its most-used shape, plus
the shapes needed to reach every station it serves (step 1). Lines that run on
into Mortsel, Wijnegem, Wommelgem and Boechout are drawn to their ends; their
stops there get no ring.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.antwerp import config  # noqa: E402
from pipeline.countries.belgium import commune_geometry  # noqa: E402

SYSTEM = "De Lijn"
FETCH = "pipeline/antwerp/fetch_sources.py"

# Per-line label end override: "start" or "end". Default picks the tail
# farthest from the other lines, on the stretch inside the city.
LINE_LABEL_ENDS = {}


def main():
    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINE_SHAPES_ZIP,
                 config.LINE_SHAPES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    shapes = json.loads(config.LINE_SHAPES_JSON.read_text(encoding="utf-8"))
    line_specs = {ln: (tuple(shapes[ln]), config.LINE_COLOURS[ln], config.LINE_NAMES[ln],
                       LINE_LABEL_ENDS.get(ln)) for ln in config.LINES}
    lines = load_line_shapes(config.LINE_SHAPES_ZIP, line_specs, SYSTEM)
    missing = sorted(set(config.LINES) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing} - a line this project draws must come from real "
                 f"geometry")

    stations = pd.read_csv(config.STATIONS_CSV, dtype={"lines": str})
    businesses = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype={"postcode": str, "vkbo_nis": str})
    print(f"\n  {len(stations):,} stations, {len(businesses):,} food premises")

    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title="Antwerp De Lijn trams Business Density Heatmap",
        city_name="Antwerp",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=config.CRS_GEOGRAPHIC,
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=commune_geometry(config.OSM_COMMUNES_JSON, FETCH, config.OWN_NIS,
                                     config.COMMUNE_AREA_KM2, "Antwerp"),
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
