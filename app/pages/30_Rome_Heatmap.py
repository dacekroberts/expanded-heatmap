"""Rome heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.rome.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Rome Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Rome")

st.title("Rome: commercial density around metro and urban rail stations")

# Approved by the owner 2026-09-24, with the Roma-Viterbo urban service drawn
# on the owner's call the same morning.
st.markdown(
    """
Five lines are drawn — **Metro A, B, B1 and C, and the Roma–Viterbo railway's
urban service** from Piazzale Flaminio to Montebello — each labelled on the map
and in the legend. The metro is in ATAC's colours, with the B1 branch a shade
lighter than line B so the two stay distinct. The lines and stations are
OpenStreetMap's, because the data Rome's transport agency publishes comes with a
condition that it be used for travel information.

Suburban railways are left out of these maps unless, inside the city, they run
like a metro. The Roma–Viterbo urban service does: its stations are under a
kilometre apart, a train comes every 10 to 15 minutes, and it serves the
districts north of Flaminio that no metro line reaches. The Roma–Lido railway
(Metromare) does not, because its stations are about two kilometres apart and
its trains come every 15 to 20 minutes, so Ostia and Acilia have no station
rings. Trams, the Roma–Viterbo railway beyond Montebello and suburban trains are
not drawn.

The map covers the **comune di Roma**, Ostia included. Metro C's last stop,
Monte Compatri – Pantano, is in a neighbouring comune and is not counted; the
line is drawn to it.

Businesses come from **Roma Capitale's register of productive activities**
(SUAP), which records each authorised premises at its own street address, placed
using Italy's national archive of house numbers (ANNCSU). The register carries
no business names, so each dot shows what the premises is authorised for and its
address. About one premises in twenty has an address that could not be matched
to a house number and is left off. A premises authorised for more than one kind
of trade, such as a bar that also sells goods, is shown once, under the more
specific one.

**Read the food-and-drink layer as an upper bound.** The register records no
closing date, and it lists about 2.7 times as many restaurants, bars and cafés
as OpenStreetMap maps in the city. The difference is not concentrated in old
registrations — the oldest premises are the likeliest to match a mapped place —
so part of it is OpenStreetMap under-mapping Rome's bars and part is recently
registered premises that may not have opened. The newest register file is from
**July 2025**. Many workshops record no trade at all and are not shown; of those
that do, food makers such as pizza-by-the-slice counters and pastry shops count
as food service, and laundries, nail bars and tattoo studios as personal
services, while repair shops and garages are left out.

**About half the storefronts sit within a station ring**, because Rome's rail,
dense in the centre, leaves much of a very large comune beyond walking distance
of a station.

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

# The snapshot dates, read from outputs/rome/provenance.json so they cannot go
# stale on the next fetch: the SUAP file's own month (in its name, e.g.
# opendata_suap_luglio_2025.csv - the portal publishes no other date), the
# ANNCSU extract's date (in its member name, INDIR_LAZI_YYYYMMDD.csv), and the
# day the rail was read from OpenStreetMap (the same fetch run).
_MESI = {"gennaio": "January", "febbraio": "February", "marzo": "March",
         "aprile": "April", "maggio": "May", "giugno": "June", "luglio": "July",
         "agosto": "August", "settembre": "September", "ottobre": "October",
         "novembre": "November", "dicembre": "December"}
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _bits = []
        _m = re.search(r"_([a-z]+)_(\d{4})\.csv$", (_prov.get("suap") or {}).get("file", ""))
        if _m and _m.group(1) in _MESI:
            _bits.append(f"premises as of **{_MESI[_m.group(1)]} {_m.group(2)}** (SUAP)")
        _a = re.search(r"_(\d{4})(\d{2})(\d{2})\.csv$", (_prov.get("anncsu") or {}).get("member", ""))
        if _a:
            _bits.append(f"house numbers as of **{_a.group(1)}-{_a.group(2)}-{_a.group(3)}** (ANNCSU)")
        _got = ((_prov.get("suap") or {}).get("retrieved") or "")[:10]
        if _got:
            _bits.append(f"metro and rail lines and stations from OpenStreetMap, "
                         f"retrieved **{_got}**")
        if _bits:
            st.caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/rome/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
