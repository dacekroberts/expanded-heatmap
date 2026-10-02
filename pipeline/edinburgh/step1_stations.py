"""Edinburgh step 1: Edinburgh Trams' stops and its one line.

    python pipeline/edinburgh/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's relations kept (by the ref config gives
them, REF_BY_RELATION) or named in NOT_DRAWN, their stops collapsed by name,
gate 3 against the operator's 23 and NaPTAN, the City of Edinburgh as scope,
and the line merged from its two through relations (config.LINE_OSM_REFS).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.edinburgh import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
