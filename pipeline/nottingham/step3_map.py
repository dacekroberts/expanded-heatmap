"""Step 3 - Render Nottingham (Regional)'s heatmap to a standalone HTML file.

All rendering is pipeline/map_common.py's `render_heatmap()`, which
pipeline/countries/uk.py's step3 calls, never forked; this file supplies only
what is Nottingham-specific. Lines come from step 1's lines.geojson (each NET
line's two directional relations merged); the map labels each "Line 1" or
"Line 2" and the legend adds its ends.

Input:  data/nottingham/processed/stations.csv
        data/nottingham/processed/businesses_clean.csv
        data/nottingham/processed/lines.geojson         (from step 1)
        data/nottingham/raw/city_boundary.geojson       (label anchoring)
Output: outputs/nottingham/heatmap.html

Run:  python pipeline/nottingham/step3_map.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import uk  # noqa: E402
from pipeline.nottingham import config  # noqa: E402

SYSTEM_NAME = "Nottingham Express Transit"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step3(config, system_name=SYSTEM_NAME,
             map_title="Nottingham Express Transit Business Density Heatmap",
             label_ends=LINE_LABEL_ENDS)
