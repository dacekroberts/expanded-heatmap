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
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Rennes Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Rennes")
render_city_title('Rennes')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/rennes/step3_map.py` to generate it.")

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
**The métro**

- Two STAR lines are drawn — **Métro a and Métro b** — each labeled on the map and in the legend,
  redrawn from the operator's own published geometry.
- The map covers the **commune of Rennes**. Métro a runs entirely inside it.
- **Métro b runs past it at both ends**, so four of its fifteen stations are left out: Atalante and
  Cesson - Viasilva in Cesson-Sévigné, and La Courrouze and Saint-Jacques - Gaîté in
  Saint-Jacques-de-la-Lande.
- The line is still drawn to its ends, but those four stations get no ring and their businesses
  are not counted. They are listed below.
- Their communes' businesses are in the same national register this map reads, so leaving them
  out is a choice rather than a limit of the data: the map keeps to the commune so that Rennes can
  be read alongside Paris, Marseille and Toulouse on the same terms.

**The businesses**

- Businesses come from **SIRENE**, France's national register of établissements, joined to
  INSEE's separate geolocation file, the same sources as the other French cities.
- Roughly one active establishment in six here is marked non-diffusible by INSEE, which withholds
  its name, address and coordinates together, so those never reach this map.
- **Where SIRENE records no shop sign or trading name, the dot shows the establishment's address
  instead** — about two dots in five on this map.

**Reading the density**

- **Read the density as a register, not a street survey.** SIRENE records where a business is
  *registered*, and some registered establishments have no customer-facing shopfront; nothing in
  the data says which.
- Counting restaurants alone, which SIRENE and OpenStreetMap define in nearly the same way, this
  map has about **1.3 times** as many in the commune as OpenStreetMap does: level with Toulouse,
  and closer to OpenStreetMap's count than Paris, Marseille or Lille.
- **About two storefronts in three sit within a station ring.** The category toggles show every
  storefront; the rings show the share the two lines actually reach.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Rennes")
render_country_links('Rennes')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Rennes")
