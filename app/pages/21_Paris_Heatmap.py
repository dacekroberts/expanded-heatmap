"""Paris heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.paris.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Paris Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Paris")
render_city_title('Paris')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/paris/step3_map.py` to generate it.")

# LICENCE MOBILITES Art. 5.7 - the transit data's snapshot date and update
# interval must be DISPLAYED, and this is the only city page that carries such
# an obligation (notice 24). Read from outputs/paris/provenance.json rather
# than hardcoded, because the IDFM zip contains no feed_info.txt: nothing
# inside the artifact records when it was current, so fetch_sources.py captures
# it and this line is the only honest way to show it.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _taken = (_prov.get("fetched_utc") or "")[:10]
        _valid = (_prov.get("nap") or {}).get("end_date") or ""
        if _taken:
            _line = (f"Transit data © Île-de-France Mobilités, snapshot taken "
                     f"**{_taken}**")
            if _valid:
                _line += f", feed valid to **{_valid}**"
            st.caption(_line + ".")
    except (ValueError, OSError):
        # A malformed or unreadable provenance file must not take the page
        # down; the notices below are the load-bearing obligation.
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

# Trams T3a and T3b added 2026-09-27 (the tram rescope), wording approved by
# the owner; set as bullets 2026-10-01.
st.markdown(
    """
**The métro and trams**

- Sixteen Métro lines are drawn — Lignes 1 to 14 plus the two short branch lines, 3bis and 7bis —
  each labelled on the map and in the legend, redrawn from Île-de-France Mobilités' own published
  geometry.
- Trams T3a and T3b are drawn too. They circle the city along the boulevards des Maréchaux and
  reach the edge districts between the Métro's radial ends.
- Île-de-France Mobilités gives T3a and T3b the same colours as Lignes 5 and 12, so this map draws
  them in lighter shades of its own. Those two colours are this project's, not RATP's.
- The map covers the **commune of Paris**. Métro stations outside it are not drawn, and every one
  is listed below.
- RER and Transilien are absent by a rule this project applies everywhere: they are commuter rail.
- The other trams are absent: T2 and T9 each have only a few stops inside the commune, and the
  rest never enter it.

**The businesses**

- Businesses come from **SIRENE**, France's national register of établissements, joined to
  INSEE's separate geolocation file.
- Records INSEE marks non-diffusible are already stripped at source — name, address and
  coordinates — so they never reach this map.
- **Where SIRENE records no shop sign or trading name, the dot shows the establishment's address
  instead** — about three dots in five on this map.
- Categories that describe no shopfront are excluded. Car dealers are not counted here, unlike on
  other cities' maps: most are one-person traders, probably registered at home. The What is
  counted page lists them.

**Reading the density**

- **Read the density as a register, not a street survey.** SIRENE records where a business is
  *registered*, and some registered establishments have no customer-facing shopfront — nothing in
  the data says which.
- Compared against OpenStreetMap's mapped shops inside the same commune, this map carries roughly
  **1.8 times** as many points. Part of that is OpenStreetMap being incomplete; part is the
  register including premises a passer-by would never see.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Paris")
render_country_links('Paris')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
