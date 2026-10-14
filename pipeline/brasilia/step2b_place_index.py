"""Step 2b - Build Brasília's place-search index (scripts/place_search_scaffold.py, 2026-10-13).

All the work is pipeline/place_index.py (run); this file names the city. Places
only, never business records (DECISIONS.md, "Four ideas assessed before the
large review", item 3). Runs before step 3, whose map carries the index's hash.

Input:  data/brasilia/raw/osm_places_2026-10-13.json        (pipeline/place_index_fetch.py)
        data/brasilia/raw/osm_places_extra_2026-10-13.json  (the same, its second query)
Output: app/static/places/brasilia.json  (served by Streamlit's static serving;
        ODbL 1.0, the notice inside the file);
        outputs/brasilia/place_search.json  (the page's summary: the languages
        its search bullet names, measured)

Run:  python pipeline/brasilia/step2b_place_index.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.brasilia import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    place_index.run(config)
