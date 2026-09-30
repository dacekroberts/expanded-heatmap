"""Aarhus step 2: CVR + DAR + OSM's DAR address points -> the storefronts
located in Aarhus Kommune.

    python pipeline/aarhus/step2_clean_businesses.py

Thin over `pipeline/countries/denmark_register.py`, as Copenhagen's. What is
Aarhus's own lives in `config.py` - the kommune, the sanity box, the catch-all
verdict and the placement.

What a reader should know before trusting the counts printed below:

  * the filter is each production unit's own LOCATION address and CVR's own
    kommune code on it (751), never a polygon;
  * CVR and DAR are the NATIONAL caches Copenhagen fetched (generations 505
    and 761), read here and never refreshed - a HEAVY read, ~5 GB;
  * the point is OSM's address point whose `osak:identifier` equals the DAR
    Husnummer id - NOT the adgangspunkt id, which places 80% where the right
    key places 97%, and the step prints both;
  * a personally owned business's name is never shown, nor any name carrying
    the sole-trader marker `v/` - the pin carries the address.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.aarhus import config  # noqa: E402
from pipeline.countries.denmark_register import build_storefronts  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, config.AARHUS_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
