"""Angers step 1: the stations in scope, under the owner's pure-extract rule.

    python pipeline/angers/step1_stations.py

Thin over `pipeline/countries/france_tram.py`; reads the cache only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_tram import build_stations
from pipeline.angers import config

if __name__ == "__main__":
    build_stations(config, "Angers")
