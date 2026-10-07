"""Bremen heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.bremen.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
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

st.set_page_config(page_title="Bremen Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Bremen")
render_city_title("Bremen")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/bremen/step3_map.py` to generate it.")

# The survey's fieldwork dates (fixed: the 2022 survey) and the rail's fetch
# date, read from outputs/bremen/provenance.json so the latter cannot go stale.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _rail = (_prov.get("osm_fetched_utc") or "")[:10]
        if _rail:
            render_caption(f"Retail survey data from the Kommunalverbund Niedersachsen/Bremen e.V. "
                           f"(CC BY), surveyed **March to September 2022**; the tram lines and "
                           f"their stops from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, in Göteborg's one-bucket shape, filled from Bremen's own
# step 1 to step 3 figures. Sentences the template does not cover are
# proposals in docs/decisions_drafts/worktree-abroad-batch.md, for review time
# (the brief's "The page"): the two-figure frequency bullet, the line 8
# bullet, the one-bucket sentence and the two survey-date bullets.
st.markdown(
    """
**The trams**

- Eight BSAG tram lines are drawn, **Tram 1, 2, 3, 4, 5, 6, 8 and 10**, each labeled on the map and
  in the legend, redrawn from OpenStreetMap's route geometry, in OpenStreetMap's own colors.
- Trams run every 7 to 10 minutes by day on most lines, and every 20 minutes on lines 5 and 8.
- Buses, BSAG's night lines and the Regio-S-Bahn's suburban trains are not drawn.
- Bremen has no metro, so its trams are its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 351 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- Tram 8's route through the city center is drawn as OpenStreetMap still records it, before
  BSAG's August 2026 change; its stops are the current ones.
- The map covers the **City of Bremen**. Tram 4 runs on into Lilienthal, so its 10 stops there are
  left out.
- The line is still drawn to its end, but those stops get no ring and their businesses are not
  counted. They are listed below.

**The businesses**

- **The shops come from the 2022 regional retail survey** of the Kommunalverbund
  Niedersachsen/Bremen e.V., which counted every retail site in the region.
- Each dot is placed at the point the survey records and shows the shop's main goods group, never
  a name: the published survey has none.
- **This map shows shops only, not three categories.** The survey counted every shop, from grocers
  and bakeries to furniture and DIY stores. So **restaurants, cafés, hairdressers and the like are
  not on this map**.
- **About two shops in three sit within a ring.**

**Reading the density**

- **The survey dates from 2022.** It counted the shops open between March and September 2022, so
  shops that opened since then are missing, and some that have closed are still shown.
- **Read the density as a 2022 survey.** It counts each shop once by its main goods group, whatever
  its size.
"""
)

render_map_help("business layer")
render_excluded_stations("Bremen")
render_country_links("Bremen")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap.
render_site_notices("Bremen")
