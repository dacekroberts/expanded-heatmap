"""Toulouse heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.toulouse.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Toulouse Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Toulouse")

st.title("Toulouse: commercial density around Métro, Tramway and Téléo station areas")

st.markdown(
    """
Four Tisséo lines are drawn — **Métro A and B, Tramway T1, and Téléo** — each
labelled on the map and in the legend, redrawn from the operator's own
published geometry.

**Téléo is a cable car**, and it is the first thing on this site that is not a
train. It is drawn because Tisséo runs and tickets it exactly as it does the
métro, because it crosses the Garonne where no other line does, and because one
of its three stations is a Métro B interchange. It is an ordinary part of this
network rather than a curiosity attached to it.

The map covers the **commune of Toulouse**, and here that costs something real.
Métro A loses one station and Métro B one; **Tramway T1 loses twelve of its
twenty-five** — the whole branch out through Blagnac and Beauzelle, the Airbus
works and the exhibition centre with it. All fourteen are listed in
`outputs/toulouse/excluded_stations.csv`. Blagnac's businesses are in the
same national register this map reads, so leaving them out is a choice rather
than a limit of the data: the map keeps to the commune so that Toulouse can be
read alongside Paris and Marseille on the same terms.

Businesses come from **SIRENE**, France's national register of établissements,
joined to INSEE's separate geolocation file — the same two sources Paris and
Marseille use. **Toulouse withholds more than either of them.** INSEE marks
roughly one active establishment in five here as non-diffusible and strips the
name, the address and the coordinates together, so those never reach this map
at all. Where a street looks thin, it may be a quiet street or it may be a
private one, and nothing in the data distinguishes them.

**Read the density as a register, not a street survey.** SIRENE records where a
business is *registered*, and some registered establishments have no
customer-facing shopfront — nothing in the data says which. Against
OpenStreetMap's mapped restaurants in the same commune, where the two schemes
mean nearly the same thing, this map carries about **1.3 times** as many
points. That is the closest of the three French cities: Paris runs 1.8× and
Marseille 1.7×, and part of the difference here is simply the masking above.

**About two storefronts in three sit within a station ring.** The category
toggles show every storefront; the rings show the share the four lines actually
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

# The snapshot date, read from outputs/toulouse/provenance.json rather than
# hardcoded so it cannot go stale on the next fetch.
#
# ⚠ THIS FEED HAS NO feed_info.txt - Paris's gap, not Marseille's Mecatran
# window - so the artifact declares no validity period and the fetch date is
# not merely honest, it is the only thing pinning the snapshot. Toulouse does
# have a second attestation Paris lacked: the portal's own `modified`
# timestamp, captured at fetch time and shown here when present.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _mod = ((_prov.get("catalogue") or {}).get("modified") or "")[:10]
        if _taken:
            _line = ("Transit data © Tisséo, via Toulouse Métropole's open data "
                     f"portal, snapshot taken **{_taken}**")
            if _mod:
                _line += f", dataset last updated **{_mod}**"
            st.caption(_line + ".")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/toulouse/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
