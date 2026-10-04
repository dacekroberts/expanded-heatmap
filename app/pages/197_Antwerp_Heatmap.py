"""Antwerp heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py, in the
city-page format of 2026-10-01 (owner): title, map, captions, bullets, map help,
country links, notices.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.antwerp.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Antwerp Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Antwerp")
render_city_title("Antwerp")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/antwerp/step3_map.py` to generate it.")

# The dates, read from outputs/antwerp/provenance.json so they cannot go stale:
# FAVV-AFSCA's extract, the day VKBO's points were paged, and the day De
# Lijn's feed was fetched (the Antwerp brief's caption, Den Haag's shape).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _favv = ((_prov.get("favv") or {}).get("extract_date") or "")[:10]
        _vkbo = ((_prov.get("vkbo") or {}).get("fetched_utc") or "")[:10]
        _feed = ((_prov.get("gtfs") or {}).get("fetched") or "")[:10]
        if _favv and _vkbo and _feed:
            st.caption(f"Food premises from FAVV-AFSCA, extract of **{_favv}**, placed on VKBO's "
                       f"address points, extracted **{_vkbo}**; the tram lines and their stops "
                       f"from De Lijn's open data, fetched **{_feed}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city template, filled in for Antwerp, with the Antwerp brief's
# one-bucket sentences; sentences outside the template are flagged in
# DECISIONS.md.
st.markdown(
    """
**The trams**

- Twelve De Lijn tram lines are drawn, **trams 1, 2, 4, 6, 7, 8, 10, 11, 12, 24, A3 and A9**, each
  labeled on the map and in the legend, redrawn from De Lijn's open data in De Lijn's own colors,
  with line 11's white made gray so it shows on the map.
- Lines 3, 5, 9 and 15 are not in the current timetable, and no tram serves the left bank
  (Linkeroever) while works go on; trams A3 and A9 run on the right bank in their place.
  One stop, Hoboken Jan Van de Wouwer, is closed for works and listed below.
- Antwerp has no metro of its own: its premetro is trams in tunnels, so its trams are its rapid
  transit, as in Riga. Every tram stop here gets rings.
- **Tram stops sit closer together than metro stations**, a median of 274 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **City of Antwerp**, with Borsbeek, part of the city since January 1, 2025.
  Several lines run on into Mortsel, Wijnegem, Wommelgem and Boechout, so their 16 stops
  there are left out.
- The lines are still drawn to their ends, but those stops get no ring and their businesses are
  not counted. They are listed below.
- Buses and national-rail (NMBS) trains are not drawn.

**The businesses**

- **This map shows food only, not three categories.** Its dots are the food businesses registered
  with FAVV-AFSCA, Belgium's food safety agency: restaurants, bars and cafés, friteries and pita
  shops, and food shops (bakers, butchers, fishmongers and other food retailers), shown as Food
  service and Food shops.
- So **clothes shops, hairdressers and the like are not on this map**.
- Each business is placed at the point Flanders' copy of the business register (VKBO) gives its
  registered address; about 4 in 100 food-service businesses could not be placed.
- A dot shows the type of business, never its name: the register lists none.
- Caterers, food sold beside another trade, school and care kitchens, and market and mobile sales
  are left out.
- **About four storefronts in five sit within a ring.**
"""
)

render_map_help("business categories (Food service and Food shops)")
render_excluded_stations("Antwerp")
render_country_links("Antwerp")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Antwerp")
