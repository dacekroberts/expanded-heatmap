"""Step 3 - Render Ghent's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Ghent-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/ghent/processed/stations.csv
        data/ghent/processed/businesses_clean.csv
        data/ghent/processed/tram_shapes.zip    (step 1: the drawn shapes only)
        data/ghent/processed/line_shapes.json   (step 1: each line's shapes)
        data/ghent/raw/osm_communes.json        (label anchoring)
Output: outputs/ghent/heatmap.html

Run:  python pipeline/ghent/step3_map.py

Each line is drawn from De Lijn's own shapes.txt (step 1 picks the shapes);
T2 is drawn to its end in Melle, whose stop gets no ring.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.countries.belgium import commune_geometry  # noqa: E402
from pipeline.ghent import config  # noqa: E402

SYSTEM = "De Lijn"
FETCH = "pipeline/ghent/fetch_sources.py"

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
        map_title="Ghent De Lijn trams Business Density Heatmap",
        city_name="Ghent",
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
                                     config.COMMUNE_AREA_KM2, "Ghent"),
    )


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
