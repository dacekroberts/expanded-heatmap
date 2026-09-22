# Build brief — Toronto

**Not the next city — but NOT for the reason this brief originally gave.**
Its published ranking figure was the only Canadian one already measured on
storefronts, yet its *denominator* was wrong: see the correction below, which
moves Toronto from sixth of six to **fourth**. The argument against building it
is coverage, not density.

Claims are **MEASURED** or **ASSERTED**, per
[`session_roles.md`](../session_roles.md).

---

## CORRECTION 2026-09-21: Toronto is FOURTH, not last

**Re-measured before any build, and it overturns this brief's own premise.**
The "234 stations" every Toronto figure rests on is a **PLATFORM count**, not a
station count. Measured from the agency feed:

| | platforms | **stations** | ratio |
|---|---|---|---|
| subway, Lines 1/2/4 | 148 | **77** | 1.92 |
| subway + LRT Lines 5/6 | **234** | **118** | 1.98 |

The stop names say so outright — "Finch Station - Southbound Platform" — and
**`parent_station` is not populated at all**, so nothing ever collapsed them.

**Rescaled to real stations, Toronto is 81 per station, not 41:**

> Vancouver 206 · Montréal 151 · Surrey 135 · **Toronto 81** · Edmonton 76 ·
> Calgary 75

So Toronto moves from clearly last to **fourth, ahead of both Calgary and
Edmonton**. The rescaling is valid because the numerator — storefronts inside
the rings — does not depend on how stations are counted; and 81 is still a
FLOOR, because the 41 rested on a 71.4% geocode match.

**This is the fourth denominator error in this project**, and the first
introduced by trusting a station count recorded in this project's own notes
rather than re-deriving it.

**What has NOT changed is the real argument against building Toronto**, and it
was never the density: it is a **two-bucket city**. It licenses food and trades
but not general retail, so the Retail bucket cannot be filled from the
municipal register at all. That is a coverage problem no denominator fixes, and
it is why Calgary and Edmonton remain the better next builds despite ranking
below it.

## Where it ranks, and why the re-ranking did not rescue it

**41 storefronts per PLATFORM, across 234 platforms — which is 81 per
station across 118 stations.** The per-platform figure is what the ranking
published; the corrected one is above. For scale: Vancouver 206, Montréal 151,
Surrey 135, **Toronto 81**, Edmonton 76, Calgary 75 — against D.C. ~173 and
Boston ~39.

**Toronto's 41 was the only Canadian figure already measured on storefronts**,
so it is the one number the 2026-09-21 re-ranking did not change. The other
five were inflated 1.4x–4.2x by counting every mappable licence.

**An intermediate claim made during the Vancouver build turned out to be
RIGHT, after being recorded here as wrong.** It was suggested that Toronto's
last place was "the least trustworthy number in the table". This brief then
recorded that the gap narrowed only from 2.5x to 1.8x and that Toronto "still
sits clearly last" — which held only while its denominator was platforms. On a
consistent station count it does not: Toronto is fourth. **Both the original
suspicion and its rebuttal are left here**, because the sequence is the lesson —
the suspicion was correct for a reason nobody had identified yet.

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

**This, not the density, is the argument against building it** — and after
the denominator correction it is the ONLY argument left. A city with 118
stations and one absent bucket produces a large map that is systematically
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
- **THREE personal columns, not one.** `Client Name` was already recorded (395
  surname-first forms in a 32k sample), but the field list measured 2026-09-21
  also carries **`Business Phone` and `Business Phone Ext.`** All three must be
  omitted at the download boundary and asserted absent, as New York,
  Philadelphia, Miami, Boston and Surrey all do. `Operating Name` is blank on
  only 0.8%, so no fallback is needed and there is no excuse for loading any of
  them. Full field list: `_id, Category, Licence No., Operating Name, Issued,
  Client Name, Business Phone, Business Phone Ext., Licence Address Line 1-3,
  Ward, Conditions, Free Form Conditions Line 1-2, Plate No., Endorsements,
  Cancel Date, Last Record Update` — note there is **no coordinate field of any
  kind**, confirming the geocoding requirement. 159,872 rows confirmed.
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

**MEASURED 2026-09-21, both claims resolved** (the station count is corrected
at the top of this brief):

- **The LRT/streetcar split IS a lookup, not a research problem.** The two LRT
  lines are named `Line 5 Eglinton` and `Line 6 Finch West`; the other 18
  `route_type 0` routes carry street names — Bathurst, Carlton, Dundas,
  Harbourfront, King, Kingston Rd, Lake Shore, Long Branch, Queen and so on. A
  `^Line \d` test separates them cleanly. This brief previously called it a
  scope decision; it is a regex.
- **Station counts, by scope:** subway only 148 platforms / **77 stations**;
  subway + LRT 234 / **118**; adding all 18 streetcar routes takes it to 913
  platforms / 706 names — the shape that would make Toronto a street-running
  city like San Francisco rather than a rapid-transit one.
- **The agency feed carries NO `feed_info.txt`**, so — like Calgary's and
  Edmonton's — its staleness cannot be checked from the feed. Only Montréal's
  STM and Vancouver's TransLink publish a validity window.

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
5. **Whether a two-bucket map of 118 stations is worth publishing at all**, or
   whether Toronto is better left out with its reason recorded. A
   project-owner question, not a Step 0 one.
