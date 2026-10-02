"""Nottingham (Regional) step 2: the FSA's four authority files -> the food
storefronts placed inside the four NET authorities.

    python pipeline/nottingham/step2_clean_businesses.py

Reads the cache only (fetch_sources.py downloads). The method is
pipeline/countries/uk.py's step2, Newcastle's: only pipeline/fsa.py's READ
fields; the flat and childminder rules; the FSA's own point, else a full
postcode's Code-Point centroid; a private address (an outward code, no point)
never placed; a business type the taxonomy does not know stops the step.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk  # noqa: E402
from pipeline.nottingham import config  # noqa: E402
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk.step2(config, load_taxonomy_module(config.TAXONOMY_SYSTEM))
