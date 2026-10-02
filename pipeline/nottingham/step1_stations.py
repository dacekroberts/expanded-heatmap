"""Nottingham (Regional) step 1: NET's stops and its two lines.

    python pipeline/nottingham/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's relations kept or named in NOT_DRAWN,
their stops collapsed by name, gate 3 against NET's per-line counts and
NaPTAN, the four authorities as scope, and each line's two directional
relations merged by London's branch rule (config.LINE_OSM_REFS).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.nottingham import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
