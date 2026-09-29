"""Why the maps differ - the reader's version of docs/map_inconsistencies.md.

The third information page, beside 90_About_the_Data.py (where the data comes
from) and 91_What_Is_Excluded.py (what is left out). This one answers the
question a reader asks when comparing two cities: why does this map look
different from that one? The owner's shape (DECISIONS, 2026-09-28): its own
page, linked from every page's footer; eleven short themes written for a
general reader; and one summary row per city. Tables A-D of the source document
stay internal - they are the evidence, full of method notes, and they went
stale by hand while they were the only copy.

NO COUNT THAT GROWS WITH THE CITY LIST IS WRITTEN HERE. The themes name one to
three examples and never "all N cities" or a list of every member, because the
re-check before this page was drafted found five of six stale spots in the
source were hand-written city lists that had missed a later city. The one
open-ended figure in the prose - the range of in-ring shares - is filled from
the same file as the table.

THE TABLE IS BUILT, NOT WRITTEN. Each row comes from the city's app/cities.py
entry (`rail_extra`, `record_kind`, `categories`, `data_age`; the area from the
"(Regional)" in its name) and app/ring_shares.json (generated from the
committed maps by scripts/check_ring_shares.py). Adding a city adds its row
with no edit here; scripts/check_inconsistency_list.py fails a city without the
three fields, and check_ring_shares.py one without a share.

AN HTML TABLE IN A SCROLLING BOX (components.scroll_table), NOT st.dataframe
AND NOT A MARKDOWN TABLE: seven columns would widen the whole page at 375 px.
The helper's docstring has the measurements.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cities import SWITCHER_ORDER  # noqa: E402
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    EXCLUSIONS_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    scroll_table,
    set_base_font,
)
from station_scope import slug  # noqa: E402

SHARES = Path(__file__).parent.parent / "ring_shares.json"

st.set_page_config(page_title=f"Why the maps differ — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← Global View")
    st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")
    st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")


@st.cache_data(show_spinner=False)
def summary_rows():
    """One row per city, in the switcher's order, and the share of each."""
    try:
        shares = json.loads(SHARES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        shares = {}
    rows = []
    for c in SWITCHER_ORDER:
        rec = shares.get(slug(c["page"]))
        share = round(100 * rec["in_ring"] / rec["all"]) if rec and rec["all"] else None
        rows.append({
            "City": c["name"].replace(" (Regional)", ""),
            "Area": "Regional" if "(Regional)" in c["name"] else "City",
            "Trams or suburban rail": c.get("rail_extra", "—"),
            "Business record": c.get("record_kind", "—"),
            "Categories": c.get("categories", "—"),
            "Storefronts near a station": share,
            "Data date": c.get("data_age", "—"),
        })
    return rows


rows = summary_rows()
known = [r["Storefronts near a station"] for r in rows
         if r["Storefronts near a station"] is not None]
share_range = (f"about {min(known)}% to {max(known)}%" if known
               else "from a small minority to nearly all")

st.title("Why the maps differ")

st.markdown(
    """
Every map on this site is drawn the same way: rings around rapid-transit
stations, and storefronts from the best public list of businesses each city
has. But the lists and the rail networks differ between places, and the
differences show on the maps. This page explains the ones a reader is most
likely to notice. Each city's page has the details, and the table at the end
sums up every city in one row.

**Each map counts a different kind of record.** Cities don't all publish the
same kind of list. Some maps are drawn from a business-licence register, some
from a street survey or census, some from a national business or tax register,
and some from permits for particular trades. Hong Kong's, for example, is built
from food licences alone. Each counts something slightly different (a licence,
a premises, a company), so a denser map is not necessarily a busier city.
Compare patterns within a city rather than totals between cities.

**Not every map has all three categories.** Most maps sort storefronts into
Retail, Food service and Personal services. Some can't, because the city
doesn't license that trade or its records can't tell trades apart.
Philadelphia and Boston have no Personal services layer. Amsterdam, Rotterdam
and Riga merge Retail and Personal services into one "Shops and services"
layer. In Japan, where only food shops need a licence, the shop layer holds
food shops alone. A missing or thin layer is a gap in the records, not a quiet
street.

**Suburban trains appear on only a few maps.** Most maps draw metro-type lines
and leave commuter rail off. A commuter line is included where, inside the
city, it works like a metro: stations close together, frequent trains, and
neighbourhoods no metro reaches. Dublin's DART and Copenhagen's S-tog are drawn
for that reason; Paris's RER is not. The Japanese maps draw their JR and
private railways as well.

**Trams are on some maps and not others.** Trams and light rail are drawn where
they are the city's rapid transit, as in Calgary or Riga, or where they reach
districts the metro doesn't. They are left off where they run on the streets
above a dense metro, as in Milan or Prague. Cities have weighed this a little
differently, so tram lines are the least consistent part of the rail layer.

**Some maps cover one city, others a region.** Most maps stop at the city
boundary. Stations beyond it are drawn on their line but get no rings, because
the business records stop there too. Maps labelled "(Regional)" cover several
municipalities that share one register or one network, such as Miami-Dade
County, or Taipei with New Taipei. Tokyo is a special case: its rail is drawn
across all 23 wards, but only some wards publish usable data, and stations in
the others are drawn hollow.

**Some cities have half-size rings.** Where stations are only a few hundred
metres apart, as in Paris, New York or Oslo, the rings are drawn at half the
usual size so they don't swallow the next station. The pin counts in those
maps' layer menus cover a smaller area and don't compare with other cities'
counts.
"""
)

st.markdown(
    f"""
**How much of a city's storefronts lie near a station varies widely.** Each
page gives the share of the city's storefronts that fall inside its rings.
Across the site it runs from {share_range}. A high share can mean the rail
network reaches most of the city, or that the source covers mainly the centre.
A low one means much of the city's commerce is far from rail. The share
describes the city and its data, not how good its transit is.
"""
)

st.markdown(
    """
**Some dots show an address or a type, not a name.** A dot normally shows the
business's trade name. Where the record has none, or where the only name is a
person's own at what may be their home, the dot shows something else: an
address, the kind of business, or "Name withheld". Dublin's and Rome's records
carry no names at all, and Paris shows an address wherever the register has no
shop sign. Leaving a person's name off a pin is deliberate: this site
publishes businesses, not people.

**The data comes from different dates.** Each map is a snapshot of its records
on the day they were downloaded, mostly in September 2026. A few sources are
older: the Brazilian maps use the 2022 census, and Barcelona a 2022 street
survey. Where a source gives its own date, the page shows it; some sources
publish none.

**Some maps undercount, some overcount.** No record is a perfect list of open
shopfronts. Some miss businesses: France withholds a share of establishments
for privacy, and in Japan food shops that only notify the city hold no permit.
Others count too many: a register may keep closed businesses, empty units, or
premises with no shopfront. Where it is known, each city's page says which way
its map leans.

**A few businesses fall into different categories.** The three categories are
meant to mean the same thing everywhere, but national classifications and
local rules move some businesses at the edges. Car dealers count as Retail in
most cities but not in France. Massage is a Personal service in Alberta but is
left out as health care in British Columbia. Street stalls are left out in
Mexico.
"""
)

st.subheader("Every city in one row")
cols = list(rows[0])
scroll_table(cols,
             [["—" if r[c] is None else f"{r[c]}%" if c == "Storefronts near a station"
               else r[c] for c in cols] for r in rows],
             right=("Storefronts near a station",), min_width=760)
st.caption(
    "\"Trams\" includes light rail. \"Retail thin\" or \"Personal services thin\" "
    "means that layer holds only part of its trades, such as the ones the city "
    "licenses. \"Storefronts near a station\" is the "
    "share of the map's storefronts inside its station rings."
)

render_site_notices(show_links=False)
