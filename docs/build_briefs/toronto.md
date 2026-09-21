# Build brief — Toronto

**Not the next city, and the only Canadian candidate whose published ranking
figure was already correct.** Ranked sixth of six. This brief exists to record
why its last place survived the re-ranking, and what the one soft spot in its
number is.

Claims are **MEASURED** or **ASSERTED**, per
[`session_roles.md`](../session_roles.md).

---

## Where it ranks, and why the re-ranking did not rescue it

**41 storefronts within the 0.6 mi ring per in-city station**, across 234
stations. For scale: Vancouver 206, Montréal 151, Surrey 135, Edmonton 76,
Calgary 75, **Toronto 41** — against D.C. ~173 and Boston ~39.

**Toronto's 41 was the only Canadian figure already measured on storefronts**,
so it is the one number the 2026-09-21 re-ranking did not change. The other
five were inflated 1.4x–4.2x by counting every mappable licence.

**A correction to an intermediate claim made during the Vancouver build.** It
was suggested that Toronto's last place was "the least trustworthy number in
the table" and that a common basis would narrow the gap substantially, because
Toronto alone was being compared against five inflated figures. **The narrowing
is real but small in effect**: Calgary-to-Toronto goes from 2.5x to 1.8x, and
Toronto still sits clearly last. The published *order* was directionally right
all along; only the magnitudes were wrong. Recorded because the wrong inference
was reasonable and someone may make it again.

**Its real soft spot is different, and it is a floor rather than a point
estimate.** The 41 rests on geocoding **159,872** licence rows against the
City's own address repository at a **71.4% exact-match rate, with no street
normalisation**. The unmatched 29% are **ASSERTED** to be distributed evenly,
and that has never been checked. If they are concentrated — in older
addresses, in a borough, in a licence category — the true figure is higher, and
plausibly by a lot. **Anyone tempted to build Toronto should test that before
anything else**, because it is the single number that decides whether the city
is Boston-thin or mid-table.

## Why it is structurally the weakest, independent of the number

**Toronto is a two-bucket city — Boston's shape.** It licenses food and trades
but **not general retail**, so the Retail bucket cannot be filled from the
municipal register. Boston's page had to say a category was missing entirely,
and Philadelphia's had no personal-services source at any level of government.
That is a coverage problem no amount of geocoding fixes, and it is why a
reader would misread the map as a fact about Toronto's high streets rather than
about its licensing.

**This, not the density, is the argument against building it.** A city with
234 stations and one absent bucket produces a large map that is systematically
wrong in a way the page has to apologise for.

## Sources

### Business — Municipal Licensing & Standards

| | |
|---|---|
| Portal | CKAN, `open.toronto.ca` |
| Resource | `169e90ba-3ae0-43dd-8b2f-919e87002f50` |
| Licence | **OGL – Toronto** (terminates automatically on breach) |
| Rows | **159,872** |

**Three MEASURED traps, all recorded during the Canada profile:**

- **No coordinates at all.** Zero. Toronto is the only Canadian candidate of
  the six that genuinely needs a geocoding step, and Canada has no national
  bulk geocoder. The answer is the City's **One Address Repository** (525,440
  points, same licence), which matched **71.4% on exact string match with no
  normalisation** and returns `MUNICIPALITY_NAME`, so it doubles as the in-city
  filter.
- **`Client Name` is a person column and must never be downloaded** — 395
  surname-first forms in a 32k sample. `Operating Name` is blank on only 0.8%,
  so there is no need for a fallback and no excuse for loading the other. Omit
  it at the download boundary and assert it stays absent, as New York,
  Philadelphia, Miami and Boston all do.
- **`datastore_search_sql` 404s** on this portal. Use `datastore_search` with
  `filters`, and note **join keys are case-sensitive**: `ADDRESS_FULL` is title
  case, and matching it in upper case returned **0 of 150**.

### Transit — TTC

**THIS IS THE CITY THAT TAUGHT THE PROJECT NOT TO TRUST A CATALOGUE MIRROR.**

The Mobility Database copy (id 2253) was **three months expired** and contained
**no subway at all** — 209 bus, 17 tram, 2 ferry, zero `route_type 1`, with the
only subway-named entries being shuttle *buses*. The screen read 17 trams and
concluded "Toronto codes its subway as route_type 0", which is **false** and
propagated into `screen_rail.py`, the `add-city` skill and
`docs/city_shortlist.md` before being caught.

**The agency's real feed**, from the City's own CKAN package
`ttc-routes-and-schedules` (36 MB, OGL – Toronto):

| route_type | count | what |
|---|---|---|
| **1** | **3** | Line 1 Yonge-University, Line 2 Bloor-Danforth, Line 4 Sheppard |
| **0** | **20** | 13 streetcars **plus Line 5 Eglinton and Line 6 Finch West** (LRT) |
| 3 | 213 | bus |

So Toronto is *richer* than the screen suggested — three subway lines and two
new LRT lines — and separating rail from streetcar is trivial rather than the
San Francisco problem it was described as. **`screen_rail.py` now prints feed
expiry because of this city.**

**ASSERTED:** the 234 station count, and which of the 20 `route_type 0` routes
are LRT rather than streetcar. Both need re-deriving from the agency feed
before any build; the streetcar/LRT split in particular is a scope decision,
not a lookup.

### Projected CRS

**EPSG:32617** (UTM 17N), from longitude ≈ −79.4. **ASSERTED** — derived here
from the longitude but not used in anger.

## What a build would cost

The most expensive of the six, and the reasons compound:

- **A geocoding step** against the One Address Repository, plus a real answer
  on whether the unmatched 29% are biased.
- **A taxonomy module** for its own licence categories (**ASSERTED: 72**,
  recorded in `PLAN.md` but not re-measured in the 2026-09-21 pass).
- **A missing-bucket disclosure** on the city page and in
  `docs/excluded_categories.md`, under what is *missing* rather than
  *excluded* — Boston and New York are the models.
- **A streetcar/LRT scope decision** for the 20 `route_type 0` routes.
- **One notice**: `Contains information licensed under the Open Government
  Licence – Toronto.`

## Open questions

1. **Are the 29% of unmatched addresses biased?** The one question that could
   move Toronto up the ranking. Everything else is cost.
2. **Which `route_type 0` routes are LRT**, and does the map include
   streetcars?
3. **The real station count** from the agency feed, not the 234 asserted here.
4. **The licence-category count and vocabulary** — 72 is asserted, not
   measured.
5. **Whether a two-bucket map of 234 stations is worth publishing at all**, or
   whether Toronto is better left out with its reason recorded. A
   project-owner question, not a Step 0 one.
