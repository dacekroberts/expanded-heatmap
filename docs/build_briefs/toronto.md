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
| subway, Lines 1/2/4 | 148 | **72** | 2.06 |
| subway + LRT Lines 5/6 | **234** | **111** | 2.11 |

The stop names say so outright — "Finch Station - Southbound Platform" — and
**`parent_station` is not populated at all**, so nothing ever collapsed them.

### CORRECTED AGAIN 2026-09-21 (second pass): 111, not 118

**The first correction fixed the error and then made a smaller one of the same
kind.** Re-measured by `scripts/brief_check.py`, which exists because of
exactly this: 148 platforms collapse to **72** stations and 234 to **111**, not
77 and 118.

**Two naming conventions live in one feed**, which is what the 118 missed:

- the subway hyphenates — `Finch Station - Southbound Platform`
- **the LRT does not** — `Aga Khan Park & Museum Station Eastbound Platform`,
  plus a bare `Finch West Station LRT Platform`

A pattern written for the subway leaves all 86 LRT platforms uncollapsed. It
also missed a third form: three stations appear **twice**, once plain and once
suffixed `- Subway` — `Kipling Station` against `Kipling Station - Subway`, 33 m
apart, and the same for Don Mills and Vaughan Metropolitan Centre.

**Checked against the network as riders know it**, because a collapse is only
evidence if it agrees with the operator: Line 1 has 38 stations, Line 2 31 and
Line 4 5, sharing 3 interchanges — **71**, against the measured 72. Adding Line
5's 25 and Line 6's 18 less their shared stations gives ≈110, against the
measured 111. The old 77 and 118 agree with nothing.

**Nearest-neighbour spacing confirms it, and would have failed the 118.** At
111 stations the median is **632 m**; the intermediate figure that leaves the
LRT uncollapsed gives 160 stations at **70 m**, which is platform spacing and
not station spacing.

**And Toronto has NO non-revenue stops** — `pickup_type`/`drop_off_type` are
boardable on every rail stop_time — so Edmonton's garage problem does not
apply here. Worth recording as a checked absence rather than an unexamined one.

**Rescaled to real stations, Toronto is 86 per station, not 41 and not 81:**

> Vancouver 206 · Montréal 151 · Surrey 135 · **Toronto 86** · Edmonton 79 ·
> Calgary 137

So Toronto moves from clearly last to **third of the six on density**, above
Edmonton's built figure. The rescaling is valid because the numerator —
storefronts inside the rings — does not depend on how stations are counted; and
86 is still a FLOOR, because the 41 rested on a 71.4% geocode match.

**This is the fifth denominator error in this project and the second on this
one number.** The lesson is not "count stations carefully" — it is that a
station count must be checked against the operator's own published count and
against the spacing, every time, because each collapse mechanism can leave a
different residue.

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

**41 storefronts per PLATFORM, across 234 platforms — which is 86 per
station across 111 stations.** The per-platform figure is what the ranking
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

### ANSWERED 2026-09-21: the 71.4% is the WRONG DENOMINATOR, and the answer is 92.8%

**Open question 1 was "are the unmatched 29% biased?" — the one question the
brief said could move Toronto. Tested, and the honest answer is that the
question was built on a misleading number.**

The 71.4% is measured across **all 159,872 licence rows**, and more than half of
those are not storefronts at all — they are tow-truck owners, master plumbers,
taxicab owners and driving instructors, licences held by a **person** with no
premises address to match. Measured separately, with the unit suffix stripped
(see below):

| | rows | exact match |
|---|---|---|
| **Storefront categories** — the only rows a map uses | 80,110 | **92.8%** |
| Everything else | 79,762 | 53.4% |
| **All rows — the published figure** | 159,872 | **73.1%** |

So this is **the sixth denominator error in the project**, and the first found
in a brief's own statement of its weakest point. Toronto's density is not a
floor resting on a 71.4% match; it rests on **92.8%** coverage of the rows that
matter, and the true per-station figure is therefore roughly 7% above the
measured 86 rather than "plausibly a lot" above it.

**The normalisation that matters is one line, and it is not street
normalisation.** A raw case-and-whitespace join matches only 48.1%, because the
register writes the unit into the address (`280 SPADINA AVE, #308`, `1835
EGLINTON AVE W, 2ND FLR`) and the address repository does not carry units.
Dropping everything from the first comma takes it to 73.1% overall and 92.8% on
storefronts. The brief's "with no street normalisation" was describing the
wrong obstacle.

**And the bias itself: NOT material.** Checked on the axes that would hurt:

- **By ward** — the axis that would distort the map's spatial pattern, which is
  the thing this project actually shows. Across the 26 wards with ≥200
  storefront rows the match rate runs **73.6% to 97.8%, a 1.3x spread, standard
  deviation 5.4 points**. Mild. *A first pass on the broken 48.1% join showed a
  12x spread and looked disqualifying — it was an artefact of the join, not a
  property of the data, and it is recorded here because it nearly became a
  finding.*
- **By issue year** — flat, 48–55% across 2017–2026 on the raw join, with no
  trend, so no bias toward older or newer registrations.
- **By category** — biased, and *in Toronto's favour*: the misses concentrate in
  the non-storefront categories (`MASTER PLUMBER` 0%, `DRIVING INSTRUCTOR` 0%,
  `TAXICAB OWNER` 11.5%), exactly as a person-licence with no premises should.

**The residual 7.2% is benign and disclosable.** The 5,800 unmatched storefront
rows concentrate on a handful of plaza and mall addresses that the address
repository does not carry as a single string — `1571 SANDHURST CIR` (137 rows),
`8 WESTMORE DR` (95), `45 FOUR WINDS DR` (52). That under-counts a few malls,
not a district.

**So Q1 is closed and it does NOT argue against building Toronto.** What
remains is the two-bucket problem, and the category distribution below makes it
worse than the brief did.

## Why it is structurally the weakest, independent of the number

**Toronto is a two-bucket city — Boston's shape.** It licenses food and trades
but **not general retail**, so the Retail bucket cannot be filled from the
municipal register. Boston's page had to say a category was missing entirely,
and Philadelphia's had no personal-services source at any level of government.
That is a coverage problem no amount of geocoding fixes, and it is why a
reader would misread the map as a fact about Toronto's high streets rather than
about its licensing.

**MEASURED 2026-09-21, and it is starker than "two-bucket" conveys.** Of the
80,110 storefront-relevant licence rows across 92 categories:

| bucket | rows | share | what fills it |
|---|---|---|---|
| Food service | 62,901 | **78.5%** | `EATING OR DRINKING ESTABLISHMENT` 36,615, `TAKE-OUT OR RETAIL FOOD ESTABLISHMENT` 26,286 |
| Personal services | 15,403 | 19.2% | `PERSONAL SERVICES SETTINGS` 11,105, `LAUNDRY PREMISES` 2,247, `HOLISTIC CENTRE` 2,051 |
| **Retail** | **1,806** | **2.3%** | `SECOND HAND SHOP`, and that is the whole of it |

**Retail is not thin here, it is absent.** One category, 2.3% of the
storefronts, and it is second-hand goods — no grocer, no clothing, no
pharmacy, no hardware. A Toronto map would be a **food map with a
personal-services layer**, and the Retail legend entry would be close to empty
across 111 stations. New York's page had to explain a thin Retail bucket; this
is a further step again, and Boston — the existing comparison — at least has
package stores and cannabis retail in its Retail bucket.

**This, not the density, is the argument against building it** — and after
the denominator correction it is the ONLY argument left. A city with 111
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
- **Station counts, by scope:** subway only 148 platforms / **72 stations**;
  subway + LRT 234 / **111** (both corrected on the second pass — see the top of
  this brief); adding all 18 streetcar routes takes it to 913
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
- **A taxonomy module** for its own licence categories — **MEASURED 2026-09-21:
  92, not the 72 asserted** in `PLAN.md`. A fourth brief claim corrected by
  measuring it.
- **A missing-bucket disclosure** on the city page and in
  `docs/excluded_categories.md`, under what is *missing* rather than
  *excluded* — Boston and New York are the models.
- **A streetcar/LRT scope decision** for the 20 `route_type 0` routes.
- **One notice**: `Contains information licensed under the Open Government
  Licence – Toronto.`


## Machine checks

**Every claim below is re-run by `python scripts/brief_check.py toronto`.**
This block exists because Edmonton inherited three wrong claims from its own
brief, each one an HTTP call from being caught, and the MEASURED/ASSERTED
labels did not stop it — by the time a brief recommends something, the label
has been reasoned away. A claim written here and a claim written in the prose
above are the same claim; if they drift, this fails.

```brief-checks
[
  {
    "id": "business-rows",
    "claim": "The MLS register has 159,872 rows",
    "kind": "ckan_rows",
    "domain": "ckan0.cf.opendata.inter.prod-toronto.ca",
    "resource_id": "169e90ba-3ae0-43dd-8b2f-919e87002f50",
    "expect": 159872,
    "tolerance": 8000
  },
  {
    "id": "business-personal-columns",
    "claim": "THREE personal columns exist and must be omitted at download; and there is NO coordinate field of any kind",
    "kind": "ckan_fields",
    "domain": "ckan0.cf.opendata.inter.prod-toronto.ca",
    "resource_id": "169e90ba-3ae0-43dd-8b2f-919e87002f50",
    "present": ["Client Name", "Business Phone", "Business Phone Ext.", "Operating Name", "Category"],
    "absent": ["latitude", "longitude", "geometry", "Latitude", "Longitude", "geo_point_2d"]
  },
  {
    "id": "no-datastore-sql",
    "claim": "datastore_search_sql 404s on this portal; use datastore_search with filters",
    "kind": "endpoint_absent",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search_sql?sql=SELECT%20count(*)%20FROM%20%22169e90ba-3ae0-43dd-8b2f-919e87002f50%22"
  },
  {
    "id": "ttc-feed-downloads",
    "claim": "The agency feed downloads from the City's own CKAN package, ~36 MB",
    "kind": "http_ok",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip",
    "min_bytes": 20000000
  },
  {
    "id": "ttc-no-feed-info",
    "claim": "The agency feed carries NO feed_info.txt, so its staleness cannot be checked from the feed",
    "kind": "gtfs_files",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip",
    "present": ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt", "shapes.txt"],
    "absent": ["feed_info.txt"]
  },
  {
    "id": "ttc-route-types",
    "claim": "3 subway routes at route_type 1, 20 at route_type 0 (13 streetcar + Lines 5 and 6), 213 bus - NOT the mirror's zero subway",
    "kind": "gtfs_route_type_counts",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip",
    "expect": {"1": 3, "0": 20, "3": 213}
  },
  {
    "id": "ttc-subway-stations",
    "claim": "Subway only: 148 platforms -> 71 stations, matching the TTC exactly (38 + 31 + 5 less 3 interchanges)",
    "kind": "gtfs_stations",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip",
    "route_types": [1],
    "expect_platforms": 148,
    "expect_stations": 71,
    "expect_parent_station_populated": false,
    "strip_patterns": [
      "\\s*-\\s*\\w+bound Platform Towards .*$",
      "\\s+\\w+bound Platform Towards .*$",
      "\\s*-\\s*\\w+bound Platform\\s*$",
      "\\s+\\w+bound Platform\\s*$",
      "\\s+LRT Platform\\s*$",
      "\\s*-\\s*Platform\\s*\\d*\\s*$",
      "\\s+Platform\\s*\\d*\\s*$",
      "\\s*-\\s*Subway\\s*$"
    ],
    "crs": "EPSG:32617",
    "station_spacing_median_m_min": 400
  },
  {
    "id": "ttc-subway-lrt-stations",
    "claim": "Subway + LRT Lines 5/6: 234 platforms -> 110 stations (108 in-city), no non-revenue stops, median spacing 635 m",
    "kind": "gtfs_stations",
    "url": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip",
    "route_types": [0, 1],
    "route_name_regex": "^Line \\d",
    "expect_platforms": 234,
    "expect_stations": 110,
    "expect_boardable_stations": 110,
    "expect_parent_station_populated": false,
    "strip_patterns": [
      "\\s*-\\s*\\w+bound Platform Towards .*$",
      "\\s+\\w+bound Platform Towards .*$",
      "\\s*-\\s*\\w+bound Platform\\s*$",
      "\\s+\\w+bound Platform\\s*$",
      "\\s+LRT Platform\\s*$",
      "\\s*-\\s*Platform\\s*\\d*\\s*$",
      "\\s+Platform\\s*\\d*\\s*$",
      "\\s*-\\s*Subway\\s*$"
    ],
    "crs": "EPSG:32617",
    "station_spacing_median_m_min": 400
  },
  {
    "id": "projected-crs",
    "claim": "EPSG:32617 (UTM 17N) is derivable from longitude -79.4",
    "kind": "utm_zone_from_longitude",
    "lon": -79.4,
    "expect": "EPSG:32617"
  }
]
```

**Still not machine-checked, and each is a judgment rather than a fact:**
whether the unmatched 29% of geocoded addresses are biased (open question 1,
the one that could still move Toronto); the licence-category vocabulary, which
`brief_check` could cover but only once a `ckan_distinct` kind exists; and
whether a two-bucket map of 111 stations is worth publishing at all, which is
the owner's call.

> **These checks were STALE and PASSING, which is worth recording.** They were
> written before the build and encoded a strip pattern the build then improved:
> Union Station names its *destination* ("Union Station - Northbound Platform
> Towards Finch"), which no pattern here handled, so Union counted twice and
> Line 1 read 39 stations against the TTC's 38. The checks passed at 111/72
> because they measured their own worse method. **A check can only test what it
> encodes**, so when a build improves on a brief's method the checks have to be
> brought forward too - synced to `pipeline/toronto/config.py`'s
> `STATION_STRIP_PATTERNS` on 2026-09-21, giving 110 stations and 71 subway.

## Open questions

1. ~~**Are the 29% of unmatched addresses biased?**~~ — **ANSWERED
   2026-09-21, see above.** No, not materially: storefront coverage is 92.8%
   (the 71.4% counted person-licences with no premises), the ward spread is
   1.3x, and there is no temporal bias. It does not argue against building
   Toronto.
2. **Which `route_type 0` routes are LRT**, and does the map include
   streetcars?
3. ~~**The real station count** from the agency feed~~ — **answered twice**:
   234 platforms, **111** stations. See the second correction above, and
   `scripts/brief_check.py` keeps it answered.
4. **The licence-category count and vocabulary** — 72 is asserted, not
   measured.
5. **Whether a two-bucket map of 111 stations is worth publishing at all**, or
   whether Toronto is better left out with its reason recorded. A
   project-owner question, not a Step 0 one.
