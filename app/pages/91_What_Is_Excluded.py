"""What is counted, and what is not - renders docs/excluded_categories.md.

The companion to 90_About_the_Data.py, and the half that the map legends
actually need. A legend row reading "Retail - NAICS Code: 44/45" claims more
than any of these maps contain: nonstore retailers are excluded everywhere,
parking is excluded everywhere, and several cities exclude a catch-all code
that would otherwise put home-based sole traders on a public map. Until this
page is reachable, that legend is overstating its own contents.

IT COVERS TWO SCOPES, NOT ONE. Until 2026-09-23 this page was entirely about
businesses, while the other half of the same sentence - "density around
rail-transit stations" - was scoped just as deliberately and said nowhere a
reader would look. Every city page names its own network in its title, so a
reader on the San Francisco page is told it is a Muni Metro map; what none of
them said is that BART, Caltrain and commuter rail generally are excluded
everywhere, by a rule with two recorded judgment calls in it. The question that
prompted this was "is BART in the San Francisco build?" - asked by someone who
had read the site.

THE STATION TABLE IS COMPUTED, NOT WRITTEN. Its numbers come from the
committed `outputs/<city>/excluded_stations.csv` files at render time, so they
cannot drift from the pipeline the way a hand-kept count does - the denominator
here is open (it grows with every city) and this project has already been
bitten by writing one of those into prose. Adding a city adds its row with no
edit here. The reading of those files lives in `app/station_scope.py`, shared
with `scripts/check_scope_disclosure.py` so that one vocabulary decides both
what is shown and what is enforced.

It also carries the standing commitment that a removal request is honoured
rather than argued, which is the one thing on this site a reader might need to
act on.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cities import CITIES  # noqa: E402
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    set_base_font,
)
from station_scope import scope_rows  # noqa: E402

ROOT = Path(__file__).parent.parent.parent
DOC = ROOT / "docs" / "excluded_categories.md"

# Where the generated station table is spliced into the document: the table
# belongs at the end of the station half, and the document is rendered as one
# string. Missing, the whole document renders and the table follows it - a
# worse layout, never a crash. scripts/check_scope_disclosure.py asserts the
# marker is still there, because a silent fallback nobody checks is how this
# would rot.
BUSINESS_HEADING = "## Which businesses are counted"

st.set_page_config(page_title=f"What is excluded — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← Global View")
    st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")

st.title("What is counted, and what is not")

st.markdown(
    """
These maps answer a narrow question - how much walk-in commerce sits within a
few hundred metres of a rapid-transit station - and they answer it by leaving
two different things out.

**Which stations.** Each map covers one rapid-transit network, the one named
in that city's page title. Commuter rail is excluded everywhere, stations in
neighbouring municipalities are dropped because no register covers them, and
where a light-rail line stops every other block its surface stops are thinned
so the rings stay readable.

**Which businesses.** The legends are broader than the maps. "Retail" does not
mean every retailer; "Food service" does not mean every kitchen. Some things
are **excluded** - a choice made here, and reversible: vending machines and
mail-order sellers are not storefronts, parking garages sit outside this
project's question, and a few catch-all licence codes were dropped because
sampling showed they were mostly home-based sole traders rather than shops.
Other things are **missing**, which is not a choice at all: Philadelphia and
Boston license no personal-service trade that publishes addresses, so those
cities have two categories rather than three, and no filter here could add a
hairdresser that no register records.

If you believe a specific listing should not be on these maps, the last section
says how that is handled. The short version: it comes down, and it is not
argued about.
"""
)


@st.cache_data(show_spinner=False)
def station_table():
    """The markdown table, and the three totals the paragraph above it uses."""
    rows = scope_rows(ROOT, CITIES)
    outside = sum(r["counts"][0] for r in rows if r["counts"])
    thinned = sum(r["counts"][1] for r in rows if r["counts"])
    other = sum(r["counts"][2] for r in rows if r["counts"])

    # A MARKDOWN TABLE, NOT st.dataframe. The grid widget renders collapsed
    # here - 52 px wide with no canvas at all, measured 2026-09-23 in the lean
    # venv - and even working it would be the only interactive element on a
    # page that is otherwise a document: no sorting worth doing on 22 rows, and
    # its contents would not appear in the page text.
    header = ["City", "Network mapped", "Outside the city", "Stops thinned"]
    if other:
        header.append("Other")
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join("---" if i < 2 else "--:"
                            for i, _ in enumerate(header)) + "|"]
    for row in rows:
        cells = [row["name"], row["network"]]
        if row["counts"] is None:
            cells += ["—"] * (len(header) - 2)
        else:
            cells += [f"{n:,}" for n in row["counts"][:len(header) - 2]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines), outside, thinned, other


if DOC.exists():
    table, outside, thinned, other = station_table()
    text = DOC.read_text(encoding="utf-8")
    head, marker, tail = text.partition(BUSINESS_HEADING)
    st.markdown(head)

    st.markdown(
        f"""
**{outside + thinned + other:,} stations are left out across these maps** -
{outside:,} for standing outside the city whose register the map is built from,
and {thinned:,} thinned out of street-running stretches where the stops are
closer together than the rings. Every one of them is named in its city's
`excluded_stations.csv`.
"""
    )
    st.markdown(table)
    st.caption(
        "A dash is a city with no excluded-stations file: every station of "
        "its network is on its map."
    )

    st.markdown(marker + tail)
else:
    st.warning(f"{DOC.name} is missing from this checkout.")

render_site_notices(show_links=False)
