"""Downloads shared by the Belgian cities' fetch scripts.

Imported only by `pipeline/<city>/fetch_sources.py`, never by a step
(`scripts/check_no_fetch_in_steps.py`). One Overpass query per city, never in
parallel; `pipeline/osm.py` waits out the owner's minute after a 504 or 429.
"""
import sys

from pipeline import osm
from pipeline.countries.belgium import NIS_TAG


def fetch_communes(bbox, cache_json, own_nis, force=False):
    """Every municipality relation in `bbox` (s, w, n, e), `out geom`, cached.

    Exits if the city's own NIS code is not among them: an empty or partial
    answer is a failed fetch, not a city with no boundary.
    """
    s, w, n, e = bbox
    q = ("[out:json][timeout:240];"
         f'relation["boundary"="administrative"]["admin_level"="8"]["{NIS_TAG}"]'
         f"({s},{w},{n},{e});out geom;")
    els, host = osm.fetch(q, cache_json, force=force)
    codes = {x.get("tags", {}).get(NIS_TAG) for x in els}
    if own_nis not in codes:
        sys.exit(f"  communes: NIS {own_nis} missing from the answer - a failed fetch")
    print(f"  communes: {len(els)} boundary relations via {host}")
    return host
