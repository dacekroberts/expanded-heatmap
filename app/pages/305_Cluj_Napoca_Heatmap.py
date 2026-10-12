"""Cluj-Napoca heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.cluj_napoca.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_data_age,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Cluj-Napoca Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Cluj-Napoca")
render_city_title("Cluj-Napoca")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/cluj_napoca/step3_map.py` to generate it.")

# The date caption: cities.py's data_age. A city that reads a provenance file
# replaces this with its own caption of the sources' dates and credits.
render_data_age("Cluj-Napoca")

# From Bucharest's page (approved wording) and the tram kit's halved-rings
# sentence; the sentences they do not cover (the county lists cut to the
# city, the range of dates, the paired stops, the waits, the nearest-number
# tier) are proposals in docs/decisions_drafts/worktree-japan-kansai-2.md.
# Step 2, 2026-10-11: 5,334 storefront premises, 3,801 placed (71.3%), 447 of
# them by the nearest-number tier; step 3: 1,237 of 3,801 within a ring
# (32.5%). The waits are CTP's weekday timetables of 2026-09-07.
st.markdown(
    """
**The lines**

- Three lines are drawn: CTP's trams **100**, **101** and **102**, redrawn from OpenStreetMap,
  each labeled on the map and in the legend. Line 102 runs the whole route; lines 100 and 101 each
  run one half of it, on the same track.
- At midday on weekdays a tram runs about every 14 minutes on line 102, every 11 on line 101 and
  every 17 to 18 on line 100, which runs only from about 9 a.m. to 9 p.m.
- CTP names each direction's stop separately. The map pairs them into 20 stations; where the two
  stops have different names, the station shows both.
- **Tram stops sit closer together than metro stations**, a median of 475 m here, so the rings
  are drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **Municipality of Cluj-Napoca**; every tram stop lies inside it.
- The depot runs numbered 102L carry no stops and are not drawn. The metro is under construction
  and not on the map.

**The businesses**

- **This map shows food businesses only.** They come from the lists of Cluj County's
  Sanitary-Veterinary and Food Safety Directorate (DSVSA Cluj), which records every food unit it
  registers: restaurants, cafés, bars and fast food, and food shops from butchers and bakeries to
  supermarkets.
- The lists cover the whole county; a business is on this map where its address names
  Cluj-Napoca.
- No open register of other shops or of personal services covers Romania, so **clothes shops,
  hairdressers and the like are not on this map**.
- The lists are dated from April 30 to October 6, 2026: the bars list is the oldest, and the
  restaurants list is dated June 29.
- They are lists of registrations and mark no closures, so a dot is a registered premises, not
  necessarily one open today.
- Canteens, catering, pastry labs, pharmacies, market stalls, mobile units, trailers and vending
  machines are left out.
- A premises with several registrations (a supermarket's butcher and bakery counters) is shown
  once.
- Names are the operating company's, without its legal form; a sole trader, or a company named
  only for a person, is shown by category only.

**Reading the map**

- **About three storefronts in ten cannot be placed.** The register gives an address but no map
  position. Each premises is placed by matching its street and house number to OpenStreetMap's
  address points.
- Where OpenStreetMap has the street but not the number, the dot sits at the nearest number it
  lists on the same side of the street, at most six numbers away: about one placed storefront in
  eight.
- Where OpenStreetMap has no addresses on the street, the register gives no house number, or the
  same number is in two places, the premises is left off rather than guessed.
- **About one placed storefront in three sits within a station ring.**
"""
)

render_map_help("business categories (Food service and Food shops)")
render_excluded_stations("Cluj-Napoca")
render_country_links("Cluj-Napoca")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Cluj-Napoca")
