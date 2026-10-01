"""Step 3 - Render Ostrava's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; `czechia_osm_tram.step3` draws
the lines step 1 kept (data/ostrava/processed/lines.geojson) in the project's
own colours (config.LINE_COLOURS, from scripts/line_colour_search.py).

Run:  python pipeline/ostrava/step3_map.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.ostrava import config  # noqa: E402
from pipeline.countries.czechia_osm_tram import step3  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    step3(config, "DPO trams")
