"""Geneva (Regional) heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.geneva.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Geneva (Regional) Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Geneva (Regional)")
render_city_title("Geneva (Regional)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/geneva/step3_map.py` to generate it.")

# The register's extract date and the rail's fetch date, read from
# outputs/geneva/provenance.json so they cannot go stale on the next fetch.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        # ISO like every other caption (owner, 2026-09-30, call B7): the zip
        # writes "04.10.2026 07:32:19".
        _d = ((_prov.get("register") or {}).get("zip_created") or "").split(" ")[0].split(".")
        _reg = (f"{_d[2]}-{_d[1].zfill(2)}-{_d[0].zfill(2)}"
                if len(_d) == 3 and all(p.isdigit() for p in _d) else "")
        _rail = (_prov.get("osm_fetched_utc") or "")[:10]
        if _reg and _rail:
            render_caption(f"Business register data from the Canton of Geneva (SITG), extracted "
                           f"**{_reg}**; the tram lines and their stops from OpenStreetMap, "
                           f"fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError, TypeError, IndexError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Geneva's own step 1 and step 2 figures.
# Sentences the template does not cover are proposals in
# docs/decisions_drafts/worktree-abroad-batch.md, for review time: the scope
# bullet's list of communes, the register's bullet, the firms-without-premises
# bullet and the premises-type bullet. No frequency sentence: no operator
# timetable was read for it.
st.markdown(
    """
**The trams**

- Five TPG tram lines are drawn, **trams 12, 14, 15, 17 and 18**, each labeled on the map and in
  the legend, redrawn from OpenStreetMap's route geometry, in OpenStreetMap's own colors.
- Buses and the Léman Express are not drawn: the Léman Express is a suburban railway.
- Geneva has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 330 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **12 Swiss communes the trams serve**: the City of Geneva, Lancy, Meyrin,
  Carouge, Bernex, Vernier, Onex, Plan-les-Ouates, Chêne-Bougeries, Chêne-Bourg, Thônex and
  Confignon. Tram 17 runs on into Gaillard, Ambilly and Annemasse, in France, so its 4 stops there
  are left out.
- The line is still drawn to its end, but those stops get no ring and their businesses are not
  counted. They are listed below.

**The businesses**

- Businesses come from the **Canton of Geneva's business register** (Répertoire des entreprises):
  every establishment of an active business, with its activity. Restaurants, cafés and bars; shops
  of every kind; and hairdressers, beauty institutes, laundries and saunas.
- Each is placed at the point the register records for it, and each dot shows the trade name and
  its activity; where a trade name is a person's own name, the dot shows the street address
  instead.
- Businesses the register types as run from home, itinerant trades and market stands are left out.
- About 1,800 firms registered with no separate establishment are left out too: the register gives
  them no premises, so a shop cannot be told from a home address.
- **About four storefronts in five sit within a ring.**

**Reading the density**

- **Read the density as a register, not a street survey.** It counts each establishment once, by
  its main activity, and a few establishments typed as offices, such as a beauty practice in an
  office building, are counted with the rest.
"""
)

render_map_help('three business categories (Retail, Food service and Personal services)')
render_excluded_stations("Geneva (Regional)")
render_country_links('Geneva (Regional)')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Geneva (Regional)")
