"""Brussels (Regional) heatmap page - embeds the pre-rendered Folium HTML.

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
from pipeline.brussels.config import PROVENANCE_JSON as CITY_PROVENANCE_JSON  # noqa: E402
from pipeline.brussels_regional.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Brussels (Regional) Heatmap", page_icon="\U0001f5fa\ufe0f", layout="wide")
set_base_font()

render_city_nav("Brussels (Regional)")
render_city_title("Brussels (Regional)")

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/brussels_regional/step3_map.py` to generate it.")

# The dates: KBO's snapshot and BeST's file (fixed until the owner places a
# new extract), and the day STIB's feed was fetched, read from the Brussels
# page's outputs/brussels/provenance.json (one feed serves both pages).
_feed = ""
if CITY_PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(CITY_PROVENANCE_JSON.read_text(encoding="utf-8"))
        _feed = ((_prov.get("gtfs") or {}).get("file_utc") or "")[:10]
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass
st.caption("Shops and restaurants from KBO/BCE Open Data, the federal register of enterprises, "
           "snapshot of **2026-10-02**, their addresses matched to BeST-Address Brussels of "
           "**2026-09-30**" + (f"; the metro and tram lines and their stations from STIB-MIVB's "
                               f"open data, fetched **{_feed}**." if _feed else "."))

# The scaffold's bullets filled in for the 18 communes; sentences outside the
# template are flagged in docs/decisions_drafts/belgium.md (the different-
# method sentence, the near-City-station sentence, the several-codes sentence).
st.markdown(
    """
**The lines**

- STIB's four metro lines, **Metro 1, 2, 5 and 6**, and all eighteen of its tram lines, **trams 4,
  7, 8, 9, 10, 18, 19, 25, 35, 39, 44, 51, 55, 62, 81, 82, 92 and 93**, are drawn, each labeled on
  the map and in the legend, redrawn from STIB-MIVB's open data in STIB's own colors. Eight trams
  are shown a shade lighter or darker, so no two lines look alike.
- Every underground metro and premetro station in these communes gets rings, 45 in all.
- Tram stops sit a few hundred meters apart, so they are thinned to about one per half mile along
  each line; stops shared by two lines, and each line's ends, are kept. The thinned stops are
  listed below.
- **Stations sit close together here**, a median of 437 m to the nearest one, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **Brussels-Capital Region's 18 communes outside the City of Brussels**, from
  Anderlecht and Molenbeek to Ixelles, Schaerbeek, Uccle and the Woluwes. The City of Brussels has
  its own page; its stations get no ring here and are listed below, as are the stations beyond
  the Region. The lines are still drawn to their ends.
- Buses and national-rail (SNCB) trains are not drawn.

**The businesses**

- Businesses come from the federal register of enterprises (KBO/BCE), not from a street survey
  as on the City of Brussels page, so the two maps are built differently and their counts do not
  compare. Each dot is a company's registered establishment, at its address matched to the
  Region's address points (96.8% placed).
- **Companies only**: businesses run by a sole trader are not in the data this map uses, so many
  small shops and cafés are missing.
- **Shops and restaurants only**: Personal services (hairdressers, salons and the like) are not
  shown here.
- Establishments filed only under catch-all activities, addresses shared by five or more
  companies mostly in other trades, units in a numbered box (a flat or an upper-floor office) and
  units listing ten or more activities are left out, as likely offices rather than storefronts.
- An establishment registered under several activities is shown once, as Food service if any of
  them is, else as Retail.
- **The register is a snapshot of October 2, 2026**, and records registrations, not open doors:
  a business that has closed may still be shown.
- **About three storefronts in four sit within a ring.** 995 sit within 0.3 mi of a City of
  Brussels station but of no station here, so neither page's rings count them.
"""
)

render_map_help("three business categories (Retail, Food service and Personal services)")
render_excluded_stations("Brussels (Regional)")
render_country_links("Brussels (Regional)")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices("Brussels (Regional)")
