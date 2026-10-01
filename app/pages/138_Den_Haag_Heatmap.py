"""Den Haag heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.den_haag.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_city_title,
    render_country_links,
    render_excluded_stations,
    render_map_help,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Den Haag Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Den Haag")
render_city_title('Den Haag')

# Nothing between the title and the map (owner, 2026-10-01).
if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/den_haag/step3_map.py` to generate it.")

# The dates, read from outputs/den_haag/provenance.json so they cannot go
# stale: the permit layer's own last edit (it is never called current), and the
# days the BAG units and the OSM lines were fetched.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _horeca = _prov.get("horeca") or {}
        _edited = (_horeca.get("data_last_edited_utc") or "")[:10]
        _files = _prov.get("files_utc") or {}
        _bag = (_files.get("bag_verblijfsobjecten_winkelfunctie.json") or "")[:10]
        _rail = (_files.get("osm_rail.json") or "")[:10]
        if _edited and _bag and _rail:
            st.caption(f"Permit data from the Gemeente Den Haag, its permit layer last edited "
                       f"**{_edited}**; shop units from the BAG (Kadaster, via PDOK), fetched "
                       f"**{_bag}**; the tram lines and their stops from OpenStreetMap, "
                       f"fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError):
        # A malformed provenance file must not take the page down.
        pass

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Den Haag's own step 1 and step 2 figures; the
# business paragraphs follow Rotterdam's and Amsterdam's (the template city and
# the precedent for a city's own permit layer); set as bullets 2026-10-01. The
# data-date paragraph is the owner's (call 27). Sentences outside the template
# are flagged in the build's DECISIONS draft: the colour sentence, RandstadRail
# E's, "of its own", and the vacancy and permit caveats. No frequency sentence:
# no timetable was read.
st.markdown(
    """
**The trams**

- Fourteen HTM tram lines are drawn, **trams 1, 2, 6, 9, 10, 11, 12, 15, 16, 17 and 19, and
  RandstadRail 3, 4 and 34**, each labelled on the map and in the legend, redrawn from
  OpenStreetMap's route geometry, in OpenStreetMap's own colours.
- Trams 10 and 34, for which it records none, are in colours this project chose, and trams 1 and
  19, which share one colour, and 4 and 16, which nearly do, are shown a shade apart.
- RandstadRail E, Rotterdam's metro line, has 4 of its 23 stops in the city, all served by
  RandstadRail 3 and 4 as well, and is not drawn. Buses, the short 9S tram working and
  national-rail (NS) trains are not drawn.
- Den Haag has no metro of its own: its trams are its rapid transit, as Riga's are, so every tram
  stop gets rings.
- **Tram stops sit closer together than metro stations**, a median of 326 m here, so the rings are
  drawn at half the usual size (0.05 to 0.3 mi).
- The map covers the **Gemeente Den Haag**. Ten of the lines run on into Delft, Rijswijk,
  Leidschendam-Voorburg, Pijnacker-Nootdorp, Westland, Zoetermeer and Lansingerland, so their 64
  stops there are left out.
- The lines are still drawn to their ends, but those stops get no ring and their businesses are
  not counted. They are listed below.

**The businesses**

- Businesses come from two sources.
- **Food service** is the city's own layer of hospitality permits, the one behind its permit map:
  every restaurant, café, lunchroom, snack bar, takeaway, beach pavilion, coffeeshop and nightclub
  whose permit was granted or notified, under the trade name the permit gives.
- **Shops and services** comes from the national buildings register (BAG): every unit whose
  registered use is a shop and which is in use. The BAG records what a unit is for, not who is in
  it, so these dots show an address rather than a name.
- A shop unit that is also registered as a home is left off. Where a permit and a shop unit share
  an address, the permit is kept, because it names the business.
- **This map has two categories, not three.** The buildings register cannot tell a hairdresser
  from a clothes shop, so retail and personal services are one category, Shops and services, and
  the split other cities show is not available here.
- **About nine storefronts in ten sit within a ring.**

**Reading the map**

- **The permit data runs to 2025.** The city last edited its permit layer on 23 May 2025, so
  premises that opened or closed since then may be missing or still shown.
- **Read the density as a register, not a street survey.** Cafés and restaurants inside hotels,
  sports clubs, theatres and care homes hold the same permit and are left out, and takeaways that
  need no hospitality permit are thin on the map.
- About one Den Haag shop unit in twenty-five was registered as vacant at the start of 2025, by
  the national statistics office's count, and no open source says which.
"""
)

render_map_help('two business categories (Shops and services, and Food service)')
render_excluded_stations("Den Haag")
render_country_links('Den Haag')

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
