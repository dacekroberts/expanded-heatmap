"""Liverpool (Regional) step 1: Merseyrail's stations and its two lines.

    python pipeline/liverpool/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The method is
pipeline/countries/uk.py's step1: OSM's Merseyrail relations kept or named in
NOT_DRAWN (the City Line's three), their stops collapsed by name, gate 3
against Merseytravel's per-line counts and NaPTAN's rail records (RLY), the
four councils as scope, and each line's relations merged by London's branch
rule (config.LINE_OSM_REFS). The light-rail test's track share reads 100%
railway=rail: heavy rail, expected, and drawn as a commuter-rail exception
(owner, 2026-10-03), not on that test.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.liverpool import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step1(config)
