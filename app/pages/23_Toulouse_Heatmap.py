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
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Toulouse Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Toulouse")
render_city_title('Toulouse')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/toulouse/step3_map.py` to generate it.")

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
**The network**

- Four Tisséo lines are drawn — **Métro A and B, Tramway T1, and Téléo** — each labeled on the
  map and in the legend, redrawn from the operator's own published geometry.
- **Téléo is a cable car**, and it is the first thing on this site that is not a train. It is
  drawn because Tisséo runs and tickets it as it does the métro, it crosses the Garonne where no
  other line does, and one of its three stations is a Métro B interchange.
- The map covers the **commune of Toulouse**, and here that costs something real. Métro A loses
  one station and Métro B one; **Tramway T1 loses twelve of its twenty-five** — the whole branch
  out through Blagnac and Beauzelle, the Airbus works and the exhibition center with it. All
  fourteen are listed below.
- Blagnac's businesses are in the same national register this map reads, so leaving them out is a
  choice rather than a limit of the data: the map keeps to the commune so that Toulouse can be
  read alongside Paris and Marseille on the same terms.

**The businesses**

- Businesses come from **SIRENE**, France's national register of établissements, joined to
  INSEE's separate geolocation file — the same two sources Paris and Marseille use.
- **More is withheld here than in either of them.** INSEE marks roughly one active establishment
  in five here as non-diffusible and withholds its name, address and coordinates together, so
  those never reach this map.
- So a street that looks thin may be a quiet one, or one whose businesses are withheld; nothing in
  the data tells the two apart.
- **Where SIRENE records no shop sign or trading name, the dot shows the establishment's address
  instead** — about half the dots on this map.

**Reading the density**

- **Read the density as a register, not a street survey.** SIRENE records where a business is
  *registered*, and some registered establishments have no customer-facing shopfront — nothing in
  the data says which.
- Counting restaurants alone, which SIRENE and OpenStreetMap define in nearly the same way, this
  map has about **1.3 times** as many in the commune as OpenStreetMap does, closer than Paris's
  1.8× or Marseille's 1.7×; part of the difference here is simply the masking above.
- **About two storefronts in three sit within a station ring.** The category toggles show every
  storefront; the rings show the share the four lines actually reach.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Toulouse")
render_country_links('Toulouse')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Toulouse")
