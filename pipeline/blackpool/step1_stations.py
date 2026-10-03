"""Blackpool (Regional) step 1: the Blackpool Tramway's stops and its one line.

    python pipeline/blackpool/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's two T1 relations (one per direction,
both via the Blackpool North spur), their stops collapsed by name, gate 3
against NaPTAN only (the operator's site refuses scripts), Blackpool with
Wyre as scope, and the line merged from its relations by London's branch rule
(config.LINE_OSM_REFS).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.blackpool import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
