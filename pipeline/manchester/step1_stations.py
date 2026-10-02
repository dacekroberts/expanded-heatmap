"""Manchester (Regional) step 1: Metrolink's stops and TfGM's nine lines.

    python pipeline/manchester/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's relations kept or named in NOT_DRAWN,
their stops collapsed by name, gate 3 against TfGM's 99 and NaPTAN, the seven
districts as scope, and each of TfGM's lines routed over OSM's track through
its own stop sequence (config.LINE_STOPS).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.manchester import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
