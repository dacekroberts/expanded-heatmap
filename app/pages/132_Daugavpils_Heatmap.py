"""Daugavpils heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.daugavpils.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_caption,
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Daugavpils Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Daugavpils")
render_city_title('Daugavpils')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/daugavpils/step3_map.py` to generate it.")

# The snapshot dates, read from outputs/daugavpils/provenance.json so they cannot
# go stale on the next fetch: the portal's own last-modified dates for the
# excise register, the premise groups, the cadastral map and the address
# register, and the date the OSM tram file was taken.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))

        def _lm(key):
            return ((_prov.get(key) or {}).get("last_modified") or "")[:10]

        _rail = (((_prov.get("osm") or {}).get("rail") or {}).get("file_utc") or "")[:10]
        _bits = []
        if _lm("excise"):
            _bits.append(f"excise licenses as published **{_lm('excise')}** (VID, via data.gov.lv)")
        if _lm("premise_groups"):
            _bits.append(f"cadastre premise groups as published **{_lm('premise_groups')}** "
                         f"(VZD, via data.gov.lv)")
        if _lm("address_register"):
            _bits.append(f"address register as published **{_lm('address_register')}** "
                         f"(VZD, via data.gov.lv)")
        if _rail:
            _bits.append(f"tram line and stops from OpenStreetMap, fetched **{_rail}**")
        if _bits:
            render_caption("Snapshot: " + "; ".join(_bits) + ".")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Daugavpils's own step 1 and step 2 figures; the
# business paragraphs are Riga's, the template city for these two layers; set as
# bullets 2026-10-01.
st.markdown(
    """
**The trams**

- Daugavpils Satiksme's five tram routes are drawn, **trams 1, 2, 3, 4 and 5**, each labeled on
  the map and in the legend (3 and 5 share one line), redrawn from OpenStreetMap's route geometry,
  in colors this project chose, since the source records none.
- Trams run about every 10 to 15 minutes by day on route 1 and every 20 to 30 minutes on routes 3
  and 5; routes 2 and 4 run about once an hour.
- Buses and suburban trains are not drawn.
- Daugavpils has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here
  gets rings.
- **Tram stops sit closer together than metro stations**, a median of 287 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **city of Daugavpils**.

**The businesses**

- Businesses come from two sources.
- **Food service** is from the State Revenue Service's register of premises licensed to sell
  alcohol or tobacco — cafés, bars, restaurants and canteens — placed by address on the State
  Address Register. These dots show the kind of place and its street address, never the license
  holder.
- **Shops and services** is from the national cadastre: every premises registered for trade whose
  name reads as a shop or a service, placed at its building.
- **This map has two categories, not three.** A café that sells neither alcohol nor tobacco is not
  in the license register, so read the food layer as a lower bound. The cadastre records what a
  premises is for, not who is in it, so a hairdresser and a clothes shop are one category.
- **About four storefronts in five sit within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** The cadastre does not record whether a
  premises is in use, and no vacancy figure is published for Daugavpils, so read the shops layer
  as an upper bound.
"""
)

render_map_help('two business categories (Shops and services, and Food service)')
render_excluded_stations("Daugavpils")
render_country_links('Daugavpils')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Daugavpils")
