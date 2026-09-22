"""Country-level settings, one module per country.

WHY THIS DIRECTORY EXISTS, and why it did not exist for the first fifteen
cities. Every city built before Mexico had its own register: San Diego's,
Chicago's, Toronto's, Vancouver's. The endpoint, the licence, the encoding and
the column names were genuinely per-city facts, so `pipeline/<city>/config.py`
was the right and only home for them.

Mexico is the first country here where **one national register covers every
city**. INEGI's DENUE is downloaded per entidad federativa, but the URL shape,
the member path, the encoding, the column names, the privacy carve-out and the
premises-type filter are facts about DENUE - not about Mexico City or
Guadalajara. Duplicating them per city means a licence correction has to be
made once per city, and this project's record is that licence positions DO get
corrected.

The split was scheduled deliberately for the SECOND city rather than the first
(see PLAN.md, 2026-09-22): one city cannot show which of its settings are
national. Guadalajara showed it.

**What belongs here:** a fact about the country's register, portal, licence or
language that every city in that country shares.

**What does NOT, however tempting:** anything a second city in the same country
turned out to differ on. Mexico's two cities differ on the state code, the
projected CRS, the municipio scope, the line specs, the operator's published
counts, and - the one nobody predicted - **the OSM station tagging itself**
(Mexico City has 184 `railway=station` nodes; Guadalajara has one, its stations
being `railway=stop` positions). A setting that looks national after one city
is a guess; after two it is a measurement.

France, Korea, Japan, Taiwan and Brazil are all one-national-register countries
on `docs/global_country_shortlist.md`, so this pattern is what the next four
countries will need. Japan's ~9 subway cities are the case that makes it worth
having: the same national facts in nine files, corrected nine times.
"""
