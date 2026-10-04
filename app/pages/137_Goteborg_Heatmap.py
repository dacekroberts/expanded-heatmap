"""Göteborg heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from datetime import date
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.goteborg.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Göteborg Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Göteborg")
render_city_title('Göteborg')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/goteborg/step3_map.py` to generate it.")

# The fetch dates, read from outputs/goteborg/provenance.json so they cannot go
# stale: the register carries no dates, so the day it was fetched is its date.
_reg, _rail = "", ""

if PROVENANCE_JSON.exists():
    try:
        _files = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8")).get("files_utc") or {}
        _reg = (_files.get("livsmedelsverksamheter.csv") or "")[:10]
        _rail = (_files.get("osm_rail.json") or "")[:10]
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

if _reg and _rail:
    render_caption(f"Food business data from Göteborgs Stad (CC0), fetched **{_reg}**; the tram "
               f"lines and their stops from OpenStreetMap, fetched **{_rail}**.")

def _long(iso):
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return "the fetch date above"
    return f"{d.day} {d:%B %Y}"

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Göteborg's own step 1 and step 2 figures;
# the business paragraphs follow Stockholm's, the template city for a Swedish
# food register; set as bullets 2026-10-01. No frequency sentence: no timetable
# was read for it.
st.markdown(
    f"""
**The trams**

- Thirteen Göteborgs Spårvägar tram lines are drawn, **Tram 1 to Tram 13**, each labeled on the
  map and in the legend, redrawn from OpenStreetMap's route geometry. They are in OpenStreetMap's
  own colors, with line 4's made a little lighter so it stands apart from the dots.
- Buses, ferries and commuter trains are not drawn, and neither is Lisebergslinjen, the heritage
  tram line.
- Göteborg has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 390 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers **Göteborgs Stad**, the City of Gothenburg. Trams 4 and 12 run on into Mölndal,
  so their 5 stops there are left out.
- The lines are still drawn to their ends, but those stops get no ring and their businesses are
  not counted. They are listed below.

**The businesses**

- **The premises come from the City of Gothenburg's register of food businesses**
  (Livsmedelsverksamheter), kept by its Environment Administration.
- Each dot is placed at the point the register records for it and shows the premises' name and
  its type. Where a premises is registered under a person's name alone, its dot shows the street
  address instead.
- **This map shows food only, not three categories.** The register lists every premises the city's food
  control has registered: restaurants, cafés and bars, and food shops from kiosks to
  supermarkets, shown as Food service and Food shops.
- So **clothes shops, hairdressers and the like are not on this map**.
- Where the register gives a premises no type, it is shown only if its name identifies a
  restaurant or a food shop, and its pin is marked "classified from its name".
- **About three storefronts in four sit within a ring.**

**Reading the density**

- **The register carries no dates.** It lists the food businesses active on the day it was
  fetched ({_long(_reg)}), and says nothing about when each opened.
- **Read the density as a register, not a street survey.** A food registration is not always a
  food business: gyms, cinemas, bingo halls and general stores that sell some food are registered
  as cafés or food shops and are counted, and a few staff restaurants registered under a company
  name remain.
"""
)

render_map_help('business categories (Food service and Food shops)')
render_excluded_stations("Göteborg")
render_country_links('Göteborg')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Göteborg")
