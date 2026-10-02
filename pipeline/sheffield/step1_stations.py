"""Sheffield step 1: Supertram's stops and its three routes.

    python pipeline/sheffield/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's relations kept or named in NOT_DRAWN
(the Tram-Train is not drawn), their stops collapsed by name, gate 3 against
NaPTAN only (the operator's site refuses scripts), the City of Sheffield as
scope, and each route's two relations merged by London's branch rule.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.sheffield import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
