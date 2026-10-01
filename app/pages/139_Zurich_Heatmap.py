"""Zurich heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.zurich.config import HEATMAP_HTML, PROVENANCE_JSON  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="Zurich Heatmap", page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_city_nav("Zurich")

st.title("Zurich: commercial density around tram stops")

# The tram-city skill's page-text template, approved by the owner word for
# word on 2026-09-30, filled from Zurich's own step 1 and step 2 figures; the
# business paragraphs follow Stockholm's, the template city for one city
# register, and Seoul's for a partial retail layer. Sentences the template
# does not cover are flagged in the build's DECISIONS draft: the colour
# clause, the not-drawn trams 12, 20 and the Forchbahn, the 2026 construction
# lines 50 and 51, and the person-name rule. No frequency sentence: no
# operator timetable was read for it.
st.markdown(
    """
Sixteen VBZ tram lines are drawn, **trams 2 to 11, 13, 14, 15, 17, 50 and 51**,
each labelled on the map and in the legend, redrawn from OpenStreetMap's route
geometry, in VBZ's colours as OpenStreetMap records them, except where two
lines share one: trams 9, 11, 15, 50 and 51 take a shade of their own, and tram
10's magenta is darkened so it stays distinct from the Food service dots.
Zurich has no metro: its trams are its rapid transit, as Riga's are, so every
tram stop gets rings. Trams 50 and 51 run only while the Bahnhofquai stop is
rebuilt, until December 2026; they take over the northern ends of trams 4, 11,
13 and 14, which run shortened until then. Buses, the S-Bahn and the Forchbahn
(S18) are not drawn: the Forchbahn is a suburban railway, and its four stops in
the city are all tram stops too. Trams 12 and 20, the Glattalbahn's airport line
and the Limmattalbahn, run almost entirely outside the city and are not drawn,
so two of tram 20's stops in the city, Bahnhof Altstetten and Seidelhof, are on
no drawn line and get no ring.

The map covers the **Stadt Zürich**, the city itself. Trams 2, 4, 10 and 50 run
on into Schlieren, Zollikon, Opfikon, Kloten and Rümlang, so their 15 stops
there are left out. The lines are still drawn to their ends, but those stops
get no ring and their businesses are not counted. They are listed in
`outputs/zurich/excluded_stations.csv`.

Businesses come from the **Stadt Zürich's register of licensed food and drink
premises** (Gastwirtschaftsbetriebe), kept by the city police's licensing
office: restaurants, cafés, bars, clubs and takeaways, and the shops, kiosks
and petrol stations licensed to sell alcohol. The register lists open premises
only. Each is placed at the point the register records for it, and each dot
shows the trade name and the kind of licence; where a trade name is a person's
own name, the dot shows the street address instead. Canteens, cabarets, event
rooms, food stands and caterers are left out.

**This map has two categories, not three.** Its shops are only those licensed
to sell alcohol: supermarkets, wine shops, kiosks and petrol-station shops,
among others. A clothes shop, a bookshop or a bakery that sells no alcohol
needs no such licence and is absent, so read the Licensed shops layer as a
slice of the city's retail, not all of it. The register holds no hairdressers,
beauty salons or other personal services.

**Read the density as a register, not a street survey.** Some restaurant
licences belong to kitchens that are not open to the public, in care homes,
staff restaurants, hospitals and clubhouses; about one food licence in thirty
is of this kind, and they remain. Likewise, a few shop licences belong to
offices and online sellers with no shop. Several premises often share one
address, and each is counted.

**Tram stops sit closer together than metro stations**, a median of 282 m
here, so the rings are drawn at half the usual size (0.05 to 0.3 mi). **About
nine storefronts in ten sit within a ring.**

Concentric ring boundaries and the two business categories (Licensed shops and
Food service) are toggleable via the layer control in the top left. When
enabled, business density will display as numbered circles summing areas when
zoomed out. Zooming in will show individual dots; hover over those to see
further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

# The register's own last-update date and the fetch dates, read from
# outputs/zurich/provenance.json so they cannot go stale on the next fetch.
# The register is CC0; the city asks for "Source: Stadt Zürich" as a courtesy.
if PROVENANCE_JSON.exists():
    try:
        _prov = json.loads(PROVENANCE_JSON.read_text(encoding="utf-8"))
        _files = _prov.get("files_utc") or {}
        _upd = ((_prov.get("register") or {}).get("date_last_updated") or "").strip()
        _reg = (_files.get("gastwirtschaftsbetriebe.geojson") or "")[:10]
        _rail = (_files.get("osm_rail.json") or "")[:10]
        if _reg and _rail:
            _as_of = f"last updated **{_upd}**, " if _upd else ""
            st.caption(f"Premises data: Stadt Zürich, Gastwirtschaftsbetriebe (CC0), "
                       f"{_as_of}fetched **{_reg}**; the tram lines and their stops "
                       f"from OpenStreetMap, fetched **{_rail}**.")
    except (ValueError, OSError, AttributeError, TypeError):
        # A malformed provenance file must not take the page down.
        pass

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/zurich/step3_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
