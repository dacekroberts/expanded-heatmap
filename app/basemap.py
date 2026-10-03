"""The Overview macro map's basemap: CARTO Positron, keyed on every request.

CARTO's Basemap Terms (2026-09-29, s3.b) grant free use only with a
CARTO-issued API key, passed as `?key=` on every style, TileJSON, tile, sprite
and glyph URL under basemaps.cartocdn.com (carto.com/basemaps/apikey/).
Streamlit 1.64 sets a key of its own as a deck property but appends nothing to
any request, and pydeck's `api_keys={"carto": ...}` only sets that same
property, so the key has to be written into the style itself (DECISIONS,
2026-10-02, and the drafts file `docs/decisions_drafts/` for this branch).

The style is CARTO's own open-source Positron (`assets/carto_positron/`,
BSD-3 code, CC BY 4.0 design; its LICENSE.md sits beside it), committed
key-free with CARTO's `{api_key}` placeholder. Its layers match the copy
basemaps.cartocdn.com serves layer for layer (compared 2026-10-02). The keyed
copy is built in memory and handed to the map as a data: URL, so the key is
never written to disk and no static file route is needed.

The key comes only from `st.secrets["CARTO_BASEMAP_KEY"]`: Streamlit Cloud's
Secrets for the public key, the user-level secrets file for the
localhost-locked one. Without it the map draws NO basemap and says so. A
keyless CARTO fallback would be outside the terms, so there is none.

CARTO s9: tiles are fetched by the visitor's browser straight from CARTO,
never proxied or cached here.
"""

import base64
import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

import streamlit as st

SECRET_NAME = "CARTO_BASEMAP_KEY"
_STYLE = Path(__file__).parent / "assets" / "carto_positron" / "style.json"
_PLACEHOLDER = "{api_key}"

# CARTO's TileJSON answers a keyed request with KEYLESS tile URLs (measured
# 2026-10-02), so the source lists the tile URLs itself, keyed. mapbox-gl
# merges the source's own `tiles` and `attribution` over the TileJSON's, which
# is still fetched (keyed) for its zoom range and bounds. Re-measure if CARTO's
# TileJSON changes its tile hosts or path.
_TILES = [f"https://tiles-{s}.basemaps.cartocdn.com/vectortiles/carto.streets/v1/{{z}}/{{x}}/{{y}}.mvt"
          for s in "abcd"]

# The credit CARTO prescribes (carto.com/attribution/: "(c) OpenStreetMap
# contributors, (c) CARTO", OSM to its copyright page, CARTO to that page),
# plus OpenMapTiles, whose schema the tiles use (basemap-styles LICENSE.md).
# It replaces the TileJSON's, which links CARTO to /about-carto/ and OSM to
# /about/. app/components.py's fixCredit() and
# scripts/check_macro_attribution.mjs hold the same three links.
ATTRIBUTION = (
    '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" '
    'rel="noopener">OpenStreetMap contributors</a>, '
    '&copy; <a href="https://carto.com/attribution/" target="_blank" rel="noopener">CARTO</a>, '
    '&copy; <a href="https://openmaptiles.org/" target="_blank" rel="noopener">OpenMapTiles</a>'
)


def _with_key(url, key):
    return url + ("&" if "?" in url else "?") + "key=" + key


@lru_cache(maxsize=2)
def _style_data_url(key):
    style = json.loads(_STYLE.read_text(encoding="utf-8"))
    for source in style["sources"].values():
        url = source["url"]
        # CARTO's template carries `{api_key}` where the query string goes;
        # a template without it would load keyless, so refuse rather than guess.
        if _PLACEHOLDER not in url:
            raise ValueError(f"{_STYLE}: source url has no {_PLACEHOLDER} placeholder")
        source["url"] = url.replace(_PLACEHOLDER, "?key=" + key)
        source["tiles"] = [_with_key(t, key) for t in _TILES]
        source["attribution"] = ATTRIBUTION
    # mapbox-gl appends "@2x.json" / ".png" to the sprite PATH and keeps the
    # query string, so one parameter covers all four sprite requests.
    style["sprite"] = _with_key(style["sprite"], key)
    style["glyphs"] = _with_key(style["glyphs"], key)
    raw = json.dumps(style, separators=(",", ":"), ensure_ascii=False)
    return "data:application/json;base64," + base64.b64encode(raw.encode("utf-8")).decode("ascii")


def carto_positron_style():
    """The keyed Positron style as a data: URL, or None when no key is set."""
    try:
        key = st.secrets[SECRET_NAME]
    except (KeyError, FileNotFoundError):
        return None
    key = str(key).strip()
    if not key:
        return None
    return _style_data_url(quote(key, safe=""))
