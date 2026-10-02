"""Fortaleza (Regional) heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. One of nine Brazilian pages on the national
CNEFE modules (pipeline/countries/brazil*.py); the census paragraphs are São
Paulo's, approved by the owner 2026-09-24, with one figure changed per city.
"""

import json
import sys
from email.utils import parsedate_to_datetime
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.fortaleza.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Fortaleza (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Fortaleza (Regional)")
render_city_title('Fortaleza (Regional)')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/fortaleza/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/fortaleza/provenance.json so they cannot
# go stale on the next fetch: the date IBGE published each CNEFE file (the
# server's Last-Modified, which fetch_sources.py records) and the day each
# rail source was read.
_RAIL = [
    ('rail lines and stations from OpenStreetMap',
     ('osm_rail', 'osm_train')),
]

if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _cnefe = [v for k, v in _prov.items() if k.startswith("cnefe") and isinstance(v, dict)]
        _pub = sorted({parsedate_to_datetime(v["last_modified"]).date().isoformat()
                       for v in _cnefe if v.get("last_modified")})
        _bits = []
        if _pub:
            _bits.append("establishments as recorded in the 2022 census (IBGE CNEFE, "
                         + ("files" if len(_cnefe) > 1 else "file") + " dated **"
                         + " to ".join(dict.fromkeys((_pub[0], _pub[-1]))) + "**)")
        for _what, _keys in _RAIL:
            _got = sorted(str(_prov[k]["retrieved"])[:10] for k in _keys
                          if isinstance(_prov.get(k), dict) and _prov[k].get("retrieved"))
            if _got:
                _bits.append(f"{_what}, retrieved **{_got[-1]}**")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, TypeError, KeyError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# Approved by the owner 2026-09-24, with the Brazil batch's rail and scope
# calls applied as recommended; set as bullets 2026-10-01.
st.markdown(
    """
**The line**

- One line is drawn — **Metrofor's Linha Sul** — labelled on the map and in the legend, in
  the colour OpenStreetMap records.
- Metrofor's three diesel lines — Linha Oeste, the Parangaba–Mucuripe VLT and the airport
  branch — are not drawn: suburban railways are left out of these maps unless they run like
  a metro, and these run every 30 to 60 minutes.
- The map covers **Fortaleza with Caucaia, Maracanaú and Pacatuba**, the municípios the
  network serves; Caucaia has no drawn station, since Linha Oeste is not drawn, and is
  counted for its businesses only.

**The businesses**

- Businesses come from **the national address register of the 2022 census** (CNEFE), kept
  by IBGE, Brazil's statistics agency.
  Census enumerators walking every street recorded each establishment, what it was, and a
  map point for it. **Read it as a 2022 picture, not today's.**
- IBGE did not classify the establishments: each dot's category is this project's reading of
  the enumerator's words, and the names were not checked against any business register.
- Where one entry stands for several shops, as in a shopping centre or a gallery, it is one
  dot.
- At an address that is also someone's home, the dot shows only its category.

**Reading the map**

- **About four in ten of the establishments that might be shops, cafés or salons carry a
  description no rule can read, and are not drawn.** Most are brand or trade names with no
  word saying what they sell.
- Near the stations it is slightly more.
- **About one storefront in seven sits within a station ring.**
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Fortaleza (Regional)")
render_country_links('Fortaleza (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
