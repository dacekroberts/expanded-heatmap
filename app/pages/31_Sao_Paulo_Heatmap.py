"""São Paulo heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.sao_paulo.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="São Paulo Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("São Paulo")

st.title("São Paulo: commercial density around metro and CPTM stations")

# Approved by the owner 2026-09-24, with the Brazil batch's rail and scope
# calls applied as recommended.
st.markdown(
    """
Seven lines are drawn — **Metrô Linhas 1-Azul, 2-Verde, 3-Vermelha, 4-Amarela, 5-Lilás
and 15-Prata, and CPTM's Linha 9-Esmeralda** — each labelled on the map and in the legend,
in the colours OpenStreetMap records for them. The lines and stations are
OpenStreetMap's. The city's own station list (GeoSampa) is used only to check which
lines are running and how many stations each has. Linha 15 is a monorail. Linhas
6-Laranja and 17-Ouro are still being built and are not drawn.

Suburban railways are left out of these maps unless, inside the city, they run like a
metro. CPTM's Linha 9 does: a train comes every 4 to 7 minutes along the Pinheiros river,
and most of its stations have no metro nearby, though they are about 1.8 km apart.
CPTM's other lines, with stations 2 to 3.5 km apart, are not drawn, and neither are buses
or bus corridors. The map covers the **município of São Paulo**; Linha 9 is drawn to its
end in Osasco, but its two stations there are not counted.

Businesses come from **IBGE's national address register for the 2022 census** (CNEFE).
Census enumerators walking every street recorded each establishment, what it was, and a
map point for it. **Read it as a 2022 picture, not today's.** IBGE did not classify the
establishments: each dot's category is this project's reading of the enumerator's words,
and the names were not checked against any business register. Where one entry stands
for several shops, as in a shopping centre or a gallery, it is one dot. At an address
that is also someone's home, the dot shows only its category.

**About a third of the establishments that might be shops, cafés or salons carry a
description no rule can read, and are not drawn.** Most are brand or trade names with no
word saying what they sell. They are commoner in commercial districts and near stations,
so those areas are under-drawn: judging by hand-read samples, the map misses roughly one
storefront in ten to one in seven within the station rings.

**About one storefront in five sits within a station ring**, because the rail, dense in
the centre, leaves most of a very large city beyond walking distance of a station.

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The snapshot dates, read from outputs/sao_paulo/provenance.json so they cannot
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

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/sao_paulo/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
