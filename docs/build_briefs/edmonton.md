# Build brief — Edmonton

> ## BUILT 2026-09-21. This brief is now HISTORY, not guidance.
>
> Read `pipeline/edmonton/config.py` and
> `pipeline/taxonomies/edmonton_licencecategory.py` for what is true; they
> carry the measurements and the reasoning. Kept because **four of its claims
> were wrong in ways worth recording**, and because three of the four were
> wrong in the same direction — a sentence was read and its consequence was
> not checked.
>
> **1. "A BETTER PATH EXISTS, and it sidesteps staleness entirely" — REVERSED.**
> The brief recommended Edmonton's eight individual Socrata GTFS tables over
> the zip. They are **expired**: their `calendar_dates` run to 2026-08-29, and
> the Stops table had not been written since April. The agency zip is the only
> current source, and it is at
> `https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip`, found in
> the `accessPoints.DOWNLOAD` field of the catalogue's href-type dataset
> `urjq-fvmq`. Reading each table's `updatedAt` was the brief's own argument
> for them and would have shown this; the dates were cited as a *feature*
> rather than checked.
>
> **2. "Edmonton's feed carries no `feed_info.txt`" — WRONG.** The agency feed
> has one, declaring `feed_start_date` 20260911 and `feed_end_date` 20261128.
> That claim was true of the stale republications and was generalised to the
> city.
>
> **3. "No required notice, uniquely among the Canadian candidates" — WRONG,
> and this is the most consequential.** Edmonton's Terms of Use do say credit
> is "not required" but "encouraged". The obligation is in a different clause
> and is not about credit: distributing the datasets "in original or modified
> form" requires including the Terms of Use URL and passing them on "without
> introducing any further restrictions of any kind". `outputs/edmonton/` is
> committed to a public repo, so it engages. See `docs/data_sources.md` item
> 14. The brief read the credit sentence and stopped.
>
> **4. The station count was 33 and the real answer is 30.** Not the platform
> error that hit Toronto and Calgary — `parent_station` collapses Edmonton's 65
> served stops to 33 correctly, at a healthy 713 m median. Three of those 33
> are **non-revenue**: two garage access points and a tail track, with
> `pickup_type` and `drop_off_type` both 1 on every one of their stop_times.
> A new error class for this project, and one every earlier city should have
> been checked for.
>
> **What the brief got right, and it was the expensive half:** no residence
> inference (`licencetype` states it), no geocoding step (99.4% of storefront
> rows carry coordinates), no name-fallback problem, the `;` delimiter, the
> 60-category vocabulary, EPSG:32612, and the corporate-boundary naming trap.
> Its three corrections to the country profile all held.
>
> **Final measured figure: 2,380 storefronts within the 0.6 mi ring across 30
> stations = 79 per station**, on the build-grade taxonomy. The brief's 76 used
> 33 stations and a 17-category screening map.

Claims are **MEASURED** or **ASSERTED**, per
[`session_roles.md`](../session_roles.md).

---

## Where it ranks, and on what

**MEASURED 2026-09-21**, reproducible with
`python scripts/rank_canada_storefront_density.py`:

**76 storefronts within the 0.6 mi ring per in-city station** — 2,520 across
33 stations. For scale: Vancouver 206, Montréal 151, Surrey 135, **Edmonton
76**, Calgary 75, Toronto 81 (corrected 2026-09-21 — its published 41 was per
PLATFORM; see `toronto.md`), against D.C. ~173 and Boston ~39.

**The published figure was 153**, measured on every licence rather than
storefronts (2.0x inflation). So Edmonton fell from "clearly ahead of Calgary"
to "tied with it" — 76 against 75. Choose between the two on cost, not
density.

**It is the smallest map of the remaining candidates**: 33 stations, half
Boston's 71. Roughly 2x Boston's density on a third of the stations.

## Claims re-measured 2026-09-21, before any build

- **`business_name` is effectively never blank** (was ASSERTED): blank on
  **6 of 43,672 rows, 0.01%**, and 6 of 25,105 Commercial rows, with 21,793
  distinct names on the Commercial set. They are company-shaped - TBOOTH,
  OASIS APARTMENTS, THE MINI DONUT KING, HASKIN CANOE INC, BUREAU VERITAS - so
  **Edmonton has no name-fallback problem at all**, which removes the last
  unknown from its privacy position.
- **`<REDACTED FOR PRIVACY>` confirmed at 4,074 rows, 9.3%** - the
  `read-licence` step-6b case, where the publisher did the privacy work
  upstream. Those rows carry no address to map, so they are lost rather than
  suppressed.
- **STILL ASSERTED, and it still BLOCKS the 76/station figure: the agency
  GTFS.** Two guessed URLs 404'd. The catalogue names the answer though:
  **`ETS Bus Schedule GTFS Data Schedules - zipped files`, id `urjq-fvmq`,
  type `href`** - a link to an external file rather than a Socrata download, so
  it needs resolving before fetching.
- **A BETTER PATH EXISTS, and it sidesteps staleness entirely.** Edmonton
  publishes GTFS as **individual Socrata tables**: Routes `d577-xky7`, Stops
  `4vt2-8zrq`, Trips `ctwr-tvrd`, Stop Times `greh-g7ac`, Route Shapes
  `7f8n-igfx`, Calendar Dates `f2sy-bth7`, Agency `isug-45sj`, Transfers
  `hnhf-yaps`. Reading those directly means no zip and no 93-day-stale mirror,
  and each table exposes its own `updatedAt` - which matters because, like
  Calgary's and Toronto's, **Edmonton's feed carries no `feed_info.txt`.**
  Prefer this over the zip.

## Sources

### Business — `qhi4-bdpu`, Socrata

| | |
|---|---|
| Endpoint | `https://data.edmonton.ca/resource/qhi4-bdpu.csv` (add `$limit`) |
| Licence | **Edmonton Open Data Terms of Use** — credit is "not required" but "encouraged"; the real obligation is on redistribution |
| `SOURCE_ENCODING` | `utf-8` |

**MEASURED:** 43,672 rows, 18 columns — `business_licence_category,
business_name, business_address, externalid, most_recent_issue_date,
expiry_date, business_improvement_area, neighbourhood_id, neighbourhood, ward,
latitude, longitude, location, count, geometry_point, originalissuedate,
licenceduration, licencetype`.

**CORRECTION 1 — Edmonton HAS a licence-level home-business flag, and the
profile missed it.** `licencetype` splits:

| value | rows |
|---|---|
| Commercial | **25,105** |
| Home Based | 14,114 |
| Non-Resident | 2,108 |
| Massage Practitioner | 1,582 |
| Adult Services | 763 |

That is **Surrey's shape — the city states it** — so Edmonton needs **no
residence inference at all**, which is the expensive part of a Vancouver-style
build. The profile had recorded only the `<Home Based Business>` *address
placeholder*, which is the same fact seen through a weaker signal.

Keep `Commercial`. `Massage Practitioner` and `Adult Services` are licences
held by a **person** rather than a premises — the New York `Individual`
distinction — and `Non-Resident` is a mobile trade.

**CORRECTION 2 — coordinate coverage is 92.7% where it matters, not 53.3%.**
The 53.3% was measured across the whole file, including the Home Based rows
whose addresses are placeholders. **MEASURED:** on `Commercial` rows, 23,265
of 25,105 carry coordinates, and on the storefront subset **99.3%** do. So
**no geocoding step is needed** — the profile's "marginal" verdict was a
denominator error, the fourth instance of that error in this project.

**CORRECTION 3 — `business_licence_category` has 60 real categories, not 67.**
**MEASURED:** 1,247 naive distinct → **60** true distinct on `";"`, with
**5,340 rows carrying more than one**. The top 40 cover **99.2%** of rows, so
the vocabulary is small and concentrated.

```
3,518  Restaurant or Food Service        1,035  Retail Sales (Major)
3,506  Retail Sales (Minor)                742  Tobacco and Vaping Product Sales
2,701  Administration Office / Prof. Svc   583  Food Processing / Catering Service
2,635  Construction, Contracting, Labour   560  Health Enhancement Centre (Accredited)
2,484  Residential Rental (Long-Term)      528  Vehicle Sales and Rental
1,703  Residential Rental (Short-Term)     519  Retail Sales (Convenience Store)
1,649  Personal Service                    503  Financial Service
1,518  Wholesale, Warehouse, Storage        450  Participant Recreation Service
1,385  Manufacturer                         428  Commercial School
1,174  Vehicle Repair, Maint., Modification 393  Alcohol Sales (Off-Premises)
1,165  Alcohol Sales (On-Premises/Minors Allowed)
```

A screening-level bucket map is in
`scripts/rank_canada_storefront_density.py` (`EDMONTON_BUCKETS`). **It maps 17
categories and is a ranking aid, not a build-grade taxonomy** — `classify()`
raising on unknowns needs an explicit verdict for all 60. Start from it, do not
ship it.

Two calls it encodes, worth carrying forward:

- **`Food Processing / Catering Service` (583) is excluded**, and it is the
  largest single sensitivity in the ranking. It merges NAICS 311 manufacturing
  with 7223 catering and *leads* with processing, so it was left out rather
  than split on a guess — the same treatment Vancouver's `Printing Imaging and
  Photo Services` got. Counting it would add 583 rows.
- **`Public Market Vendor`, `Food Truck / Food Cart` and `Travelling or
  Temporary Sales` are excluded as mobile trade**, on the project-wide NAICS
  454 reasoning.
- **`Health Enhancement Centre (Accredited)` counts as a personal service**,
  as Vancouver's `Health Enhancement Services` does, and because Alberta does
  not regulate massage therapy as a health profession.

**`business_name` blank rate: ASSERTED.** The profile recorded "no trade-name
column", which is true — there is one name field. Whether it is ever blank, and
what it holds for a sole proprietor, was not measured. Check before assuming
there is no name problem.

### Transit — Edmonton ETS LRT

**MEASURED:** 3 routes at `route_type 0` — Capital Line (`021R`), Metro Line
(`022R`), Valley Line (`023R`) — 65 served stops, `parent_station` populated on
all 65, collapsing to **33 stations**. All in-city.

**Its catalogue feed (Mobility Database id 714) is 93 DAYS EXPIRED**
(`feed_end_date` 20260620, read 2026-09-21) — the worst staleness found in this
project, worse than the TTC mirror that hid an entire mode.

**This matters more here than anywhere else**: the **Valley Line is actively
extending**, so a 93-day-old feed may be missing stations outright. The station
count of 33 happened to match the profile's, but that is not evidence the feed
is current. **A build must take the agency's own feed and re-count.** The
ranking figure above should be treated as provisional for that reason.

### Boundary

**ASSERTED — with a naming trap.** Edmonton's boundary is published as a
*corporate* boundary, which is why a search for "city boundary" misses it
(recorded in `add-country`'s failure modes: "a dataset named in a vocabulary
you did not search"). All 33 stations are in-city, so it is a check rather
than a filter.

### Projected CRS

**EPSG:32612** (UTM 12N), from longitude ≈ −113.5. Per city, never copied.

## What a build would cost

- **A taxonomy module for 60 categories**, split on `";"`, with a dispatch rule
  for the 5,340 multi-category rows.
- **No residence inference** — `licencetype` states it.
- **No geocoding step** — 99.3% of the storefront subset is coordinated.
- **No required notice**, uniquely among the Canadian candidates: Edmonton says
  credit is "not required" but "encouraged". What it *does* require is that if
  you redistribute the **datasets**, you include the Terms of Use URL and bind
  recipients "without introducing any further restrictions of any kind". This
  project publishes derived maps rather than the datasets, but
  `outputs/` is committed to a public repo — worth a deliberate reading before
  building, not after.
- **Re-fetching the feed from ETS** and re-counting stations.

## Open questions

1. **The agency's own GTFS URL**, and whether the Valley Line has stations the
   93-day-stale mirror lacks. Blocks the density figure being called final.
2. **A build-grade verdict for all 60 categories.**
3. **The dispatch rule** for multi-category rows.
4. **`business_name`'s blank rate**, and what it holds for a sole proprietor.
5. **`Food Processing / Catering Service`** — include as food service, or keep
   excluded? Worth 583 rows.
6. **Whether committing `outputs/` engages Edmonton's redistribution clause.**
   Probably not — the maps are derived, not the datasets — but it is the one
   term here that needs a reading rather than a note.
