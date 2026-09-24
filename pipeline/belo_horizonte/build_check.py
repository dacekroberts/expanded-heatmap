"""Belo Horizonte build check: the unclassifiable share by ring band.

    python pipeline/belo_horizonte/build_check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_build_check import ring_bands  # noqa: E402
from pipeline.belo_horizonte import config  # noqa: E402

if __name__ == "__main__":
    ring_bands(config)
