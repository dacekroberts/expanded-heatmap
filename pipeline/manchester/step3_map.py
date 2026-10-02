"""Step 3 - Render Manchester (Regional)'s heatmap to a standalone HTML file.

All rendering is pipeline/map_common.py's `render_heatmap()`, which
pipeline/countries/uk.py's step3 calls, never forked; this file supplies only
what is Manchester-specific. Lines come from step 1's lines.geojson (TfGM's nine lines
routed over OSM's track); the map labels each "<Colour> line" and the legend
adds its ends as TfGM writes them.

Input:  data/manchester/processed/stations.csv
        data/manchester/processed/businesses_clean.csv
        data/manchester/processed/lines.geojson         (from step 1)
        data/manchester/raw/city_boundary.geojson       (label anchoring)
Output: outputs/manchester/heatmap.html

Run:  python pipeline/manchester/step3_map.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import uk  # noqa: E402
from pipeline.manchester import config  # noqa: E402

SYSTEM_NAME = "Manchester Metrolink"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step3(config, system_name=SYSTEM_NAME,
             map_title="Manchester Metrolink Business Density Heatmap",
             label_ends=LINE_LABEL_ENDS)
