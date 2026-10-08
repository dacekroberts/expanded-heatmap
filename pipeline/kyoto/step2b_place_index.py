"""Step 2b - Build Kyoto's place-search index (pilot, 2026-10-07).

All the work is pipeline/place_index.py; this file supplies only what is
Kyoto's. Places only, never business records (DECISIONS.md, "Four ideas
assessed before the large review", item 3).

Input:  data/kyoto/raw/osm_places_2026-10-07.json  (pipeline/place_index_fetch.py)
Output: app/static/places/kyoto.json  (served by Streamlit's static serving;
        ODbL 1.0, the notice inside the file)

Run:  python pipeline/kyoto/step2b_place_index.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.kyoto import config  # noqa: E402

OUT = place_index.index_path(config.SLUG)


def main():
    if not config.PLACE_OSM_JSON.exists():
        sys.exit(f"Missing {config.PLACE_OSM_JSON}.\nRun: python pipeline/place_index_fetch.py kyoto")
    payload = json.loads(config.PLACE_OSM_JSON.read_text(encoding="utf-8"))
    # The retrieval date is the cache's own, from its file name: never today.
    retrieved = config.PLACE_OSM_JSON.stem.rsplit("_", 1)[-1]
    index, report = place_index.build(payload["elements"], city=config.NAME, retrieved=retrieved, fold="ja")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Bytes, LF only, no BOM: the file is served as-is.
    OUT.write_bytes(json.dumps(index, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(index['rows']):,} places)")
    for k in sorted(report):
        print(f"  {k}: {report[k]:,}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
