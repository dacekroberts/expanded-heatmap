"""Tokyo step 2: each active ward's own food list, MHLW's online filings for
Chūō, Minato, Shinjuku and Kōtō, and the barber, beauty and laundry registers
of Minato, Taitō, Meguro and Shibuya - every source read against its OWN ward,
classified and joined to MLIT's block file (the shared Japanese step 2,
pipeline/countries/japan_step2.py). Which wards and files is
pipeline/tokyo/wards.py; each ward's share of the official restaurant count is
measured and written to outputs/tokyo/official_shares.json.

Reads the cache and NEVER fetches.

    python pipeline/tokyo/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.tokyo import config  # noqa: E402

if __name__ == "__main__":
    run(config)
