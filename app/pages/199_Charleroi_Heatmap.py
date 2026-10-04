"""Charleroi heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.charleroi.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Charleroi Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Charleroi")
render_city_title("Charleroi")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/charleroi/step3_map.py` to generate it.")

# The dates: the survey's own (August 2024 in Charleroi), and the day the
# operator's feed was fetched, read from outputs/charleroi/provenance.json so it
# cannot go stale. The operator is named "LETEC", never "TEC" (owner,
# 2026-10-04).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _feed = ((_prov.get("tec_gtfs") or {}).get("fetched_utc") or "")[:10]
        if _feed:
            st.caption("Shops and horeca premises from the Service public de Wallonie's LoGIC "
                       "2024 survey (CC BY 4.0), surveyed **August 2024**; the light-metro lines "
                       f"and their stations from LETEC's open data, fetched **{_feed}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The scaffold's bullets and the Charleroi brief's page text, filled in;
# sentences outside the template are flagged in docs/decisions_drafts/belgium.md
# (the 200 m2 and hotels sentences, M2's outside stops, the M1 sentence).
st.markdown(
    """
**The lines**

- Three light-metro lines are drawn, **M2, M3 and M4**, each labeled on the map and in the legend,
  in colors this project chose: the operator gives all three one color.
- M2 runs on beyond the city to Anderlues, so it is drawn to its end, but its 10 stations in
  Fontaine-l'Évêque and Anderlues get no ring and their businesses are not counted. They are
  listed below.
- M1 is not drawn: the current timetable runs it as a bus. M5, under construction, is not drawn.
  Buses and national-rail (SNCB) trains are not drawn.
- **Stations sit close together here**, a median of 385 m, so the rings are drawn at half the
  usual size (0.05 to 0.3 mi).
- The map covers the **City of Charleroi**, with its former communes (Gosselies, Jumet, Gilly,
  Marchienne-au-Pont and the others).

**The businesses**

- Businesses come from the Service public de Wallonie's LoGIC 2024 survey of shops, done on the
  ground in August 2024, under the name on each shop's sign.
- **This map has two categories, not three.** Wallonia's 2024 shop survey sorts each shop as
  retail, horeca, services or vacant. Its services class mixes hairdressers with banks and
  agencies, so it is left out, as are vacant units.
- The survey recorded every shop inside the city's 18 commercial districts, but only shops over
  200 m² outside them, so small shops away from those districts are missing.
- Horeca includes hotels, which the survey does not separate.
- A sign that reads as a person's own name shows the shop's category instead.
- **About seven storefronts in ten sit within a ring.**
"""
)

render_map_help("two business categories (Retail and Food service)")
render_excluded_stations("Charleroi")
render_country_links("Charleroi")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Charleroi")
