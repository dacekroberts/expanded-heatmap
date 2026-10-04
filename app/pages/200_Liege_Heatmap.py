"""Liège heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.liege.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Liège Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Liège")
render_city_title("Liège")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/liege/step3_map.py` to generate it.")

# The dates: the survey's own (July and August 2024 in Liège), and the day the
# operator's feed was fetched, read from outputs/liege/provenance.json so it
# cannot go stale. The operator is named "LETEC", never "TEC" (owner,
# 2026-10-04).
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _feed = ((_prov.get("tec_gtfs") or {}).get("fetched_utc") or "")[:10]
        if _feed:
            st.caption("Shops and horeca premises from the Service public de Wallonie's LoGIC "
                       "2024 survey (CC BY 4.0), surveyed **July and August 2024**; the tram line "
                       f"and its stops from LETEC's open data, fetched **{_feed}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city template and the Liège brief's page text, filled in; sentences
# outside the template are flagged in docs/decisions_drafts/belgium.md (the
# 200 m2 and hotels sentences, the fork sentence).
st.markdown(
    """
**The tram**

- One tram line is drawn, **T1**, labeled on the map and in the legend, in the operator's own
  color. Trams run about every 6 minutes by day.
- In the north the line runs on to both Coronmeuse and Liège Expo, about half the trams to each.
- Liège has no metro, so its tram is its rapid transit, as in Riga. Every tram stop here gets
  rings.
- **Tram stops sit closer together than metro stations**, a median of 351 m here, so the rings
  are drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **City of Liège**. Every stop of the line is inside it.
- Buses and national-rail (SNCB) trains are not drawn.

**The businesses**

- Businesses come from the Service public de Wallonie's LoGIC 2024 survey of shops, done on the
  ground in July and August 2024, under the name on each shop's sign.
- **This map has two categories, not three.** Wallonia's 2024 shop survey sorts each shop as
  retail, horeca, services or vacant. Its services class mixes hairdressers with banks and
  agencies, so it is left out, as are vacant units.
- The survey recorded every shop inside the city's 20 commercial districts, but only shops over
  200 m² outside them, so small shops away from those districts are missing.
- Horeca includes hotels, which the survey does not separate.
- A sign that reads as a person's own name shows the shop's category instead.
- **More than half of the storefronts sit within a ring.**
"""
)

render_map_help("two business categories (Retail and Food service)")
render_excluded_stations("Liège")
render_country_links("Liège")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Liège")
