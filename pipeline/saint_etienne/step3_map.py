"""Saint-Étienne step 3: render the heatmap to outputs/saint_etienne/heatmap.html.

    python pipeline/saint_etienne/step3_map.py

Thin over `pipeline/countries/france_tram.py`, which calls
`pipeline/map_common.py`'s render_heatmap(); nothing here forks it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_tram import render
from pipeline.saint_etienne import config

if __name__ == "__main__":
    render(config, "Saint-Étienne")
