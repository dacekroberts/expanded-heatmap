"""What is counted, and what is not - renders docs/excluded_categories.md.

The companion to About_the_Data.py, and the half that the map legends
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

It also carries the standing commitment that a removal request is honored
rather than argued, which is the one thing on this site a reader might need to
act on.

ONE COUNTRY AT A TIME (owner, 2026-10-01). A country selector shows that
country's station rows and its "Excluded in one city" sections; the rest of the
document, which applies to every city, follows in full. The document stays
whole on disk: app/country_sections.py splits it at render time. ?country=
(the country in cities.py) opens the page on that country, which is how a city
page links here.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from cities import CITIES  # noqa: E402
from components import (  # noqa: E402
    ABOUT_DATA_PAGE,
    DIFFERENCES_PAGE,
    SITE_NAME,
    render_reference_nav,
    render_site_notices,
    scroll_table,
    set_base_font,
)
from country_sections import country_text, parts_of, public, select_country, shared_text  # noqa: E402
from station_scope import scope_rows  # noqa: E402

ROOT = Path(__file__).parent.parent.parent
DOC = ROOT / "docs" / "excluded_categories.md"

# Where the site-wide station totals are spliced into the shared part: at the
# end of the station half. Missing, the whole shared part renders and the
# totals follow it - a worse layout, never a crash.
# scripts/check_scope_disclosure.py asserts the marker is still there, because
# a silent fallback nobody checks is how this would rot.
BUSINESS_HEADING = "## Which businesses are counted"
# The section whose subsections are all one city each: its heading and opening
# sentence move with the selected country's sections, rather than standing
# empty in the shared part.
PER_CITY_SECTION = "Excluded in one city"
COUNTRY_OF = {c["name"]: c["country"] for c in CITIES}

st.set_page_config(page_title=f"What is counted, and what is not — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

render_reference_nav([(ABOUT_DATA_PAGE, "Where this data comes from"),
                      (DIFFERENCES_PAGE, "Why the maps differ")])

st.title("What is counted, and what is not")

# Rendered after the selected country's section (owner, 2026-10-01): a reader
# arriving from a city page lands on that country with no scrolling.
INTRO = (
    """
These maps answer a narrow question - how much walk-in commerce sits within a
few hundred meters of a rapid-transit station - and they answer it by leaving
two different things out.

**Which stations.** Each map covers one rapid-transit network, the one named
on that city's page. Commuter rail is left out, except where it runs like a metro inside the city
(*Why the maps differ* says where). Stations in neighboring municipalities
are dropped, because no register covers them. Where a light-rail line stops
every other block, its surface stops are thinned so the rings stay readable.

**Which businesses.** The legends are broader than the maps. "Retail" does not
mean every retailer; "Food service" does not mean every kitchen. Some things
are **excluded**, by a choice made here that can be reversed. Vending machines
and mail-order sellers are not storefronts. Parking garages sit outside this
project's question. And a few license codes that cover any kind of business
were dropped, because sampling showed they were mostly home-based sole traders
rather than shops. Other things are **missing**, which is not a choice at all.
Philadelphia and Boston license no personal-service trade that publishes
addresses, so those cities have two categories rather than three. No filter
here could add a hairdresser that no register records.

If you believe a specific listing should not be on these maps, the last section
says how that is handled. The short version: it comes down, and it is not
argued about.
"""
)


@st.cache_data(show_spinner=False)
def station_rows():
    """Every city's row, and the site-wide totals the shared paragraph uses."""
    rows = scope_rows(ROOT, CITIES)
    totals = tuple(sum(r["counts"][i] for r in rows if r["counts"]) for i in range(5))
    return rows, totals


def station_table(rows, totals):
    """The table's header and body for the given rows.

    components.scroll_table since 2026-09-28: as a markdown table it widened
    this page to 518 px at 375 (deploy-verify, review time). Not st.dataframe:
    the grid widget rendered collapsed here (52 px wide, no canvas, lean venv,
    2026-09-23), and its contents would not appear in the page text. Each
    optional column is picked by its index in counts_for()'s tuple, so "Closed
    for works" can appear without "Other" (Berlin, 2026-09-28). The columns
    follow the site-wide totals, so every country's table has the same ones.
    """
    outside, thinned, other, closed, infrequent = totals
    columns = [("Outside the city", 0), ("Stops thinned", 1)]
    if other:
        columns.append(("Other", 2))
    if closed:
        columns.append(("Closed for works", 3))
    if infrequent:
        columns.append(("Too infrequent", 4))
    header = ["City", "Network mapped"] + [c for c, _ in columns]
    body = []
    for row in rows:
        cells = [row["name"], row["network"]]
        if row["counts"] is None:
            cells += ["—"] * len(columns)
        else:
            cells += [f"{row['counts'][i]:,}" for _, i in columns]
        body.append(cells)
    return header, body


country = select_country("excluded_country")

if DOC.exists():
    rows, totals = station_rows()
    outside, thinned, other, closed, infrequent = totals
    parts = parts_of(DOC)
    per_city = "\n".join(next(p["lines"] for p in parts
                              if p["title"] == PER_CITY_SECTION))

    # "the United States", "the Netherlands", "the United Kingdom".
    article = "the " if country in ("United States", "Netherlands", "United Kingdom") else ""
    st.header(f"Stations left out in {article}{country}")
    header, body = station_table(
        [r for r in rows if COUNTRY_OF[r["name"]] == country], totals)
    scroll_table(header, body, right=header[2:])
    st.caption(
        "A dash means nothing is left out: every station of that city's "
        "network is on its map."
    )
    st.markdown(public(country_text(parts, country, {PER_CITY_SECTION: per_city})))

    st.divider()
    st.markdown(INTRO)
    text = public(shared_text(parts, skip_titles=(PER_CITY_SECTION,)))
    head, marker, tail = text.partition(BUSINESS_HEADING)
    st.markdown(head)

    st.markdown(
        f"""
**{outside + thinned + other + closed + infrequent:,} stations are left out across these maps.**
{outside:,} stand outside the city whose register the map is built from;
{thinned:,} were thinned out of street-running stretches where the stops are
closer together than the rings; {infrequent:,} are on light-rail or suburban
stretches that run less often than every 15 minutes; and {closed:,} are closed for works. Every
one of them is listed under "Stations left out" on its city's page.
"""
    )

    st.markdown(marker + tail)
else:
    st.markdown(INTRO)
    st.warning(f"{DOC.name} is missing from this checkout.")

render_site_notices(show_links=False)
