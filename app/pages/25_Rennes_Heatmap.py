"""Rennes heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.rennes.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Rennes Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Rennes")

st.title("Rennes: commercial density around Métro station areas")

st.markdown(
    """
Two STAR lines are drawn — **Métro a and Métro b** — each labelled on the map
and in the legend, redrawn from the operator's own published geometry.

The map covers the **commune of Rennes**. Métro a runs entirely inside it.
**Métro b runs past it at both ends**, so four of its fifteen stations are left
out: Atalante and Cesson - Viasilva in Cesson-Sévigné, and La Courrouze and
Saint-Jacques - Gaîté in Saint-Jacques-de-la-Lande. The line is still drawn to
its ends, but those four stations get no ring and their businesses are not
counted. They are listed in `outputs/rennes/excluded_stations.csv`. Their
communes' businesses are in the same national register this map reads, so
leaving them out is a choice rather than a limit of the data: the map keeps to
the commune so that Rennes can be read alongside Paris, Marseille and Toulouse
on the same terms.

Businesses come from **SIRENE**, France's national register of établissements,
joined to INSEE's separate geolocation file, the same sources as the other
French cities. Roughly one active establishment in six here is marked
non-diffusible by INSEE, which withholds its name, address and coordinates
together, so those never reach this map.

**Read the density as a register, not a street survey.** SIRENE records where a
business is *registered*, and some registered establishments have no
customer-facing shopfront; nothing in the data says which. Against
OpenStreetMap's mapped restaurants in the same commune, where the two schemes
mean nearly the same thing, this map carries about **1.3 times** as many
points, level with Toulouse and closer to OpenStreetMap's count than Paris,
Marseille or Lille.

**About two storefronts in three sit within a station ring.** The category
toggles show every storefront; the rings show the share the two lines actually
reach.

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

# The snapshot, read from outputs/rennes/provenance.json rather than hardcoded
# so it cannot go stale on the next fetch.
#
# ✅ THIS FEED SELF-ATTESTS - Marseille's case, not Paris's or Toulouse's - so
# the caption can name the window STAR itself published the feed for, from
# feed_info.txt, alongside the date this project took it. A four-week window:
# when it has lapsed, the fix is a refetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _fi = _prov.get("feed_info") or {}

        def _iso(d):
            d = str(d or "")
            return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 and d.isdigit() else ""

        _start, _end = _iso(_fi.get("feed_start_date")), _iso(_fi.get("feed_end_date"))
        if _taken:
            _line = "Transit data © STAR (Keolis Rennes)"
            if _start and _end:
                _line += (f", from the feed STAR published for **{_start}** to "
                          f"**{_end}**")
            st.caption(_line + f"; snapshot taken **{_taken}**.")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/rennes/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
