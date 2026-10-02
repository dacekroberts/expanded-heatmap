"""Where this data comes from - renders docs/data_sources.md in the app, then
each per-country file in docs/data_sources/.

WHY THIS PAGE EXISTS, AND WHY IT BLOCKS PUBLISHING. Three separate obligations
converge on it:

  * New York City's Technical Standards Manual reserves the right to require a
    third party to "explicitly identify the source, version, and modifications
    made to a public data set" when re-publishing it. `data_sources.md` is the
    source and the version (endpoint plus retrieval date per dataset); its
    sibling page is the modifications.
  * Chicago's, SFMTA's, LA Metro's and MassDOT's notices have to appear where
    the SITE is accessed, not on one city page. They render on every page from
    `components.render_site_notices()`, and this page is where the reasoning
    behind each one can actually be read.
  * The map legends are deliberately broad - "Retail - NAICS Code: 44/45"
    overstates what the maps contain - so the exclusions must be reachable
    from them, and provenance without exclusions is half an answer.

The document is rendered as committed rather than re-written for the web: it
was written to be published as-is, and a hand-maintained web copy would drift
from the file the pipeline's authors actually read.

ONE COUNTRY AT A TIME (owner, 2026-10-01). A country selector shows that
country's file in docs/data_sources/ and the parts of data_sources.md that
belong to it (its numbered notices, an indemnity accepted for one of its
sources); the rest of data_sources.md, which applies to every city, follows in
full. Both files stay whole on disk: app/country_sections.py splits
data_sources.md at render time, so check_provenance.py still reads every
numbered notice there. ?country= (the country in cities.py) opens the page on
that country, which is how a city page links here.
"""

import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from components import (  # noqa: E402
    DIFFERENCES_PAGE,
    EXCLUSIONS_PAGE,
    OVERVIEW_PAGE,
    SITE_NAME,
    render_site_notices,
    set_base_font,
)
from country_sections import (  # noqa: E402
    country_link,
    country_slug,
    country_text,
    parts_of,
    public,
    select_country,
    shared_text,
)
from cities import COUNTRY_ORDER  # noqa: E402

DOC = Path(__file__).parent.parent.parent / "docs" / "data_sources.md"
# Split by country on 2026-09-27: the entry point above keeps the notices and
# the gate, and each country's sources moved verbatim to docs/data_sources/.
# Both are the provenance record, so the page renders both - the entry point
# alone would publish the notices and drop every endpoint.
COUNTRY_DOCS = sorted((DOC.parent / "data_sources").glob("*.md"))

# The files link to each other as FILES (`data_sources/canada.md`,
# `../data_sources.md`), which works on GitHub and opens a blank page here:
# the app serves its own HTML for any path. deploy-verify found the index
# table's links dead on 2026-09-27, the day of the split. Here a country
# file's link selects that country (?country=), the folder's link jumps to the
# selector, and the entry point's link jumps to its index table, which is
# always on the page.
FILE_LINK = re.compile(r"\]\((?:\.\./)?data_sources/([a-z-]+)\.md\)")
FOLDER_LINK = re.compile(r"\]\((?:\.\./)?data_sources/\)")
ENTRY_LINK = re.compile(r"\]\(\.\./data_sources\.md\)")
COUNTRY_OF_STEM = {country_slug(k): k for k in COUNTRY_ORDER}


def _file_link(match):
    country = COUNTRY_OF_STEM.get(match.group(1))
    return f"]({country_link(country)})" if country else "](#ds-countries)"


def in_page(text):
    text = public(text)
    text = FILE_LINK.sub(_file_link, text)
    text = FOLDER_LINK.sub("](#ds-countries)", text)
    return ENTRY_LINK.sub("](#where-each-countrys-sources-live)", text)

st.set_page_config(page_title=f"Where this data comes from — {SITE_NAME}",
                   page_icon="\U0001f5fa️", layout="wide")
set_base_font()

with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
    st.page_link(OVERVIEW_PAGE, label="← Global View")
    st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")
    st.page_link(DIFFERENCES_PAGE, label="Why the maps differ")

st.title("Where this data comes from")

# Rendered after the selected country's section (owner, 2026-10-01): a reader
# arriving from a city page lands on that country with no scrolling.
INTRO = (
    """
Every dataset behind these maps is public, and this page is the
project's own provenance record: the exact web address each one was downloaded
from, the filter applied at download, the date it was retrieved, and the
license or terms it carries. It is shown here as the project keeps it, without
the notes on maintaining it.

It is long on purpose. Three things in it are worth knowing before reading
any map: **a government open-data portal does not guarantee open terms** (Los
Angeles' business registry is CC0, public domain, while its transit feed
forbids modifying the data); **several sources say nothing at all about
reuse**, and those are recorded as unresolved rather than read generously; and
**every retrieval date is a warning about staleness**, because a register only
ever describes the day it was downloaded.
"""
)

st.markdown('<div id="ds-countries"></div>', unsafe_allow_html=True)
country = select_country("sources_country")

country_doc = DOC.parent / "data_sources" / f"{country_slug(country)}.md"
if country_doc.exists():
    st.markdown(in_page(country_doc.read_text(encoding="utf-8")))
else:
    st.warning(f"docs/data_sources/{country_doc.name} is missing from this "
               "checkout.")
if DOC.exists():
    parts = parts_of(DOC)
    st.markdown(in_page(country_text(parts, country)))
    st.divider()
    st.markdown(INTRO)
    st.markdown(in_page(shared_text(parts, skip_titles=("How to keep this current",))))
else:
    st.divider()
    st.markdown(INTRO)
    st.warning(f"{DOC.name} is missing from this checkout.")

# A country file whose country has no city in cities.py would have no place
# under the selector; it renders here, so a file is never published unseen.
for orphan in COUNTRY_DOCS:
    if orphan.stem not in COUNTRY_OF_STEM:
        st.divider()
        st.markdown(in_page(orphan.read_text(encoding="utf-8")))

render_site_notices(show_links=False)
