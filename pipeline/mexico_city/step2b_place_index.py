"""Step 2b - Build Mexico City's place-search index (batch 3, 2026-10-11).

All the work is pipeline/place_index.py (run); this file names the city. Places
only, never business records (DECISIONS.md, "Four ideas assessed before the
large review", item 3). Runs before step 3, whose map carries the index's hash.

Input:  config.PLACE_OSM_JSON and config.PLACE_OSM_EXTRA_JSON, the caches
        pipeline/place_extract_fetch.py or place_index_fetch.py writes
Output: app/static/places/mexico_city.json  (served by Streamlit's static serving;
        ODbL 1.0, the notice inside the file);
        outputs/mexico_city/place_search.json  (the page's summary: the languages
        its search bullet names, measured)

Run:  python pipeline/mexico_city/step2b_place_index.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.mexico_city import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    place_index.run(config)
