"""Step 3 - Render Birmingham (Regional)'s heatmap to a standalone HTML file.

All rendering is pipeline/map_common.py's `render_heatmap()`, which
pipeline/countries/uk.py's step3 calls, never forked; this file supplies only
what is Birmingham-specific. The line comes from step 1's lines.geojson (the
six ref-1 relations merged into one); the map labels it "West Midlands Metro"
and the legend adds its ends.

Input:  data/birmingham/processed/stations.csv
        data/birmingham/processed/businesses_clean.csv
        data/birmingham/processed/lines.geojson         (from step 1)
        data/birmingham/raw/city_boundary.geojson       (label anchoring)
Output: outputs/birmingham/heatmap.html

Run:  python pipeline/birmingham/step3_map.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import uk  # noqa: E402
from pipeline.birmingham import config  # noqa: E402

SYSTEM_NAME = "West Midlands Metro"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step3(config, system_name=SYSTEM_NAME,
             map_title="West Midlands Metro Business Density Heatmap",
             label_ends=LINE_LABEL_ENDS)
