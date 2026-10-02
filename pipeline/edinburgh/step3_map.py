"""Step 3 - Render Edinburgh's heatmap to a standalone HTML file.

All rendering is pipeline/map_common.py's `render_heatmap()`, which
pipeline/countries/uk.py's step3 calls, never forked; this file supplies only
what is Edinburgh-specific. The line comes from step 1's lines.geojson (the
two through relations merged by London's branch rule); the map labels it
"Edinburgh Trams" and the legend adds its ends, "(Airport - Newhaven)".

Input:  data/edinburgh/processed/stations.csv
        data/edinburgh/processed/businesses_clean.csv
        data/edinburgh/processed/lines.geojson         (from step 1)
        data/edinburgh/raw/city_boundary.geojson       (label anchoring)
Output: outputs/edinburgh/heatmap.html

Run:  python pipeline/edinburgh/step3_map.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import uk  # noqa: E402
from pipeline.edinburgh import config  # noqa: E402

SYSTEM_NAME = "Edinburgh Trams"
# Per-line label end override ("start" / "end"); automatic unless a rendered
# map shows a label landing badly.
LINE_LABEL_ENDS = {}

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step3(config, system_name=SYSTEM_NAME,
             map_title="Edinburgh Trams Business Density Heatmap",
             label_ends=LINE_LABEL_ENDS)
