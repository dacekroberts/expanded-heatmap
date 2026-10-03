"""Birmingham (Regional) step 1: West Midlands Metro's stops and its one line.

    python pipeline/birmingham/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's ref-1 relations kept and Line 2's
named in NOT_DRAWN (not yet in passenger service), their stops collapsed by
name (four relations' role-less stop members read as stops,
config.ROLELESS_STOP_RELATIONS), gate 3 against the operator's 35 and NaPTAN,
the three authorities as scope, and the six ref-1 relations merged into one
drawn line by London's branch rule on Birmingham's thresholds.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.birmingham import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
