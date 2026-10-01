"""Country-level settings, one module per country.

Cities before Mexico each had their own register, so the endpoint, licence,
encoding and column names were per-city facts in `pipeline/<city>/config.py`.
Where **one national register covers every city**, those facts belong to the
register, not the city: INEGI's DENUE has one URL shape, member path,
encoding, set of column names, privacy carve-out and premises-type filter for
every entidad federativa. Kept here, a licence correction is made once rather
than once per city, and licence positions DO get corrected.

The split waits for a country's SECOND city (see PLAN.md, 2026-09-22): one
city cannot show which of its settings are national.

**What belongs here:** a fact about the country's register, portal, licence or
language that every city in that country shares.

**What does NOT, however tempting:** anything a second city in the same country
differs on. Mexico's two cities differ on the state code, the projected CRS,
the municipio scope, the line specs, the operator's published counts, and
**the OSM station tagging itself** (Mexico City has 184 `railway=station`
nodes; Guadalajara has one, its stations being `railway=stop` positions). A
setting that looks national after one city is a guess; after two it is a
measurement.
"""
