"""Gelsenkirchen heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.gelsenkirchen.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Gelsenkirchen Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Gelsenkirchen")
render_city_title("Gelsenkirchen")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/gelsenkirchen/step3_map.py` to generate it.")

# The survey's fetch date and the date of the OpenStreetMap data the rail came
# from, read from outputs/gelsenkirchen/provenance.json so they cannot go stale
# on the next fetch. The survey carries no date of its own (owner, 2026-10-04).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _survey = ((_prov.get("survey") or {}).get("fetched_utc") or "")[:10]
        _osm = ((_prov.get("osm") or {}).get("osm_base") or "")[:10]
        if _survey and _osm:
            render_caption(f"Shops, food service and personal services from the City of "
                           f"Gelsenkirchen's survey of commercial premises (Datenlizenz "
                           f"Deutschland – Zero – Version 2.0), undated, fetched **{_survey}**; the "
                           f"tram lines and their stops from OpenStreetMap, as mapped on **{_osm}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Gelsenkirchen's own step 1 to step 3 figures.
# Sentences the template does not cover are proposals in
# docs/decisions_drafts/worktree-abroad-batch.md, for review time: the two-
# operator lines bullet, the caption's OSM date, the survey bullets, the thin
# personal-services bullet, the uncategorised bullet and the survey-date and
# survey-reading bullets.
st.markdown(
    """
**The trams**

- Four lines are drawn, **BOGESTRA's trams 301 and 302, Ruhrbahn's tram 107 and its Stadtbahn
  line U11**, each labeled on the map and in the legend, redrawn from OpenStreetMap's route
  geometry, in OpenStreetMap's own colors.
- Trams run about every 7 to 15 minutes by day.
- Buses and suburban and regional trains are not drawn.
- Gelsenkirchen has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here
  gets rings.
- **Tram stops sit closer together than metro stations**, a median of 380 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **City of Gelsenkirchen**. 302 runs on into Bochum, and 107 and U11 into
  Essen, so their 73 stops there are left out.
- The lines are still drawn to their ends, but those stops get no ring and their businesses are
  not counted. They are listed below.

**The businesses**

- Businesses come from the City of Gelsenkirchen's survey of its shops, food service and
  services, under the name on each sign.
- A sign that reads as a person's own name shows the business's category instead.
- **Personal services are thin on this map.** The survey recorded services mainly in the city's
  designated shopping centers, so hairdressers and other personal services away from them are
  missing.
- 176 surveyed businesses with no category are left out.
- **About two storefronts in three sit within a ring.**

**Reading the density**

- **The survey carries no date.** The city publishes it without one, and its earlier files were
  labeled 2024, so businesses that opened or closed since then may be missing or still shown.
- **Read the density as a survey, not a register.** The city records premises chiefly in and
  around its shopping centers.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Gelsenkirchen")
render_country_links("Gelsenkirchen")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Gelsenkirchen")
