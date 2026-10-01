"""Dijon step 3: render the heatmap to outputs/dijon/heatmap.html.

    python pipeline/dijon/step3_map.py

Thin over `pipeline/countries/france_tram.py`, which calls
`pipeline/map_common.py`'s render_heatmap(); nothing here forks it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_tram import render
from pipeline.dijon import config

if __name__ == "__main__":
    render(config, "Dijon")
