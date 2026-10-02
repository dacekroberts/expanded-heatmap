"""Marseille heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.marseille.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Marseille Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Marseille")
render_city_title('Marseille')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/marseille/step3_map.py` to generate it.")

# The snapshot date, read from outputs/marseille/provenance.json rather than
# hardcoded so it cannot go stale on the next fetch. Marseille's feed DOES
# self-attest (feed_info.txt carries Mecatran and its validity window), unlike
# Paris's - so this is honesty about what is drawn rather than, as on Paris,
# the only way to satisfy a licence that demands a date the artifact lacks.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _end = (_prov.get("feed_info") or {}).get("feed_end_date") or ""
        if _taken:
            _line = ("Transit data © Régie des Transports Métropolitains, via "
                     "the Métropole Aix-Marseille-Provence feed, snapshot "
                     f"taken **{_taken}**")
            if len(_end) == 8:
                _line += f", feed valid to **{_end[:4]}-{_end[4:6]}-{_end[6:]}**"
            st.caption(_line + ".")
    except (ValueError, OSError):
        # A malformed provenance file must not take the page down.
        pass

# INSEE's prescribed attribution, verbatim: reuse is permitted « sous réserve
# de mentionner la source sous la forme « Source : Insee » »
# (docs/licenses/france-licence-ouverte-2.0.md, MUST DISPLAY 1). It covers
# SIRENE and its geolocation file. Kept outside the provenance block so a
# missing or malformed provenance file cannot drop it, and
# check M of scripts/check_provenance.py refuses a French page without it.
# The edition is hardcoded because outputs/<city>/provenance.json does not
# record it: it is the title fetch_sources.py recorded for the shared national
# cache (data/france/raw, fetched 2026-09-23). Change it with the next SIRENE
# refetch.
st.caption("Business data: Source : Insee, SIRENE (01 septembre 2026 edition)"
           " and its geolocation file.")

st.markdown(
    """
**The métro and trams**

- Five RTM lines are drawn — **Métro 1 and 2, Tramway 1, 2 and 3** — each labelled on the map and
  in the legend, redrawn from the operator's own published geometry.
- The map covers the **commune of Marseille**, and unlike most cities here that costs it nothing:
  every station on all five lines falls inside the boundary.
- What the boundary does exclude is a *sixth* rail line in the same feed — the tram at Aubagne, a
  separate town with its own network — and those seven stations are listed below.
- Two other modes are absent by rules this project applies everywhere: TER regional trains are
  commuter rail, and ferries are not rail. Marseille's harbour shuttles are closer to urban
  transit than that rule usually implies.

**The businesses**

- Businesses come from **SIRENE**, France's national register of établissements, joined to
  INSEE's separate geolocation file — the same source Paris uses.
- Records INSEE marks non-diffusible are stripped at source, name, address and coordinates
  together, so they never reach this map.
- **Where SIRENE records no shop sign or trading name, the dot shows the establishment's address
  instead** — more than half the dots on this map.

**Reading the density**

- **Read the density as a register, not a street survey.** SIRENE records where a business is
  *registered*, and some registered establishments have no customer-facing shopfront — nothing in
  the data says which.
- Against OpenStreetMap's mapped shops in the same commune this map carries roughly **2.6 times**
  as many points. Part of that is the register; part is that OpenStreetMap covers Marseille far
  less completely than it covers Paris.
- On restaurants, where the two schemes mean nearly the same thing, the gap narrows to 1.7× —
  close to Paris's 1.8×, which is the comparison worth trusting.
- **Fewer than six in ten of these storefronts sit within a station ring**, which is a fact about
  the city rather than the data: Marseille's commune is more than twice the area of Paris's and its
  rail network is a fifth the size.
- The category toggles show every storefront; the rings show the share the Métro and Tramway
  actually reach.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Marseille")
render_country_links('Marseille')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
