# Addendum: the full arc, from the 25-city screen

The first retrospective (`us_build_retrospective.md`) was written by the
session that built Washington D.C., and it shows: it covers the last session in
detail and the first six cities barely at all. This addendum is the missing
two-thirds, reconstructed from `DECISIONS.md` (4,151 lines, 2026-09-18 to
2026-09-21) and `docs/city_shortlist.md`.

Everything here is **MEASURED** unless marked otherwise — the numbers and
quotations come from the entries themselves, not from recollection.

---

## 1. The selection funnel: 25 → 10 → 9 built

My first pass never described how cities were chosen, which is where several of
the project's most reusable rules came from.

**25 most populous US cities**, screened on three criteria: expansive rail
transit; public transit open data; public business-licence data with a
classification field plus address or geometry. That produced a **shortlist of
10**: New York, Chicago, Los Angeles, Philadelphia, San Diego, San Francisco,
San Jose, Denver, Boston, Washington D.C.

**Seattle was swapped out for D.C. by explicit decision** — it was the
prototype's city and the only one with a known-good pipeline, but "its code
patterns carry over and its dataset does not."

### The two that failed on contact, and the rule they produced

**Denver.** Its "Active Business Licenses" dataset has no address, no
classification and no geometry — only licence number, type, sub-type, status,
entity name, trade name, expiry. All **347 datasets** in Denver's catalogue
were searched for an alternative. And the detail worth keeping: a "Business
License Data Explorer" that the first-pass research had cited turned out to be
**Anaheim's**, identified by its owner account and map extent.

**San Jose.** No bulk business-tax dataset on either official portal; the only
source was a third-party lookup tool with no export.

Those two produced the rule the whole project now runs on, written into
`CLAUDE.md` and `add-city` Step 0: **live-verify a city's actual field schema
before any pipeline work; dataset titles and search summaries are not
evidence.** Every later correction in this project is a variation on it.

### The architectural decision that saved three cities

Re-verifying all ten found that **New York, Chicago and Philadelphia failed on
NAICS alone** — each had real geocoded licence data under its own taxonomy. The
response was to **drop the requirement that a classification be NAICS**
("taxonomy plurality"), superseding a same-day plan to use NAICS as a single
shared national layer. That plan had assumed every US city self-reports NAICS
at licensing; verification showed **three of ten do not.**

This is the single highest-leverage decision in the project. It reclassified
three of the four largest cities from fail to pass, and it is why five local
taxonomy modules now coexist with NAICS while `map_common.py` names none of
them. The note in the entry is worth quoting: the bucket-based design from the
superseded plan "survived intact — it is why adding taxonomies was cheap." It
also set up non-US cities (NACE was the concrete example) as one more module
rather than a rewrite — which is exactly the position Vancouver now walks into.

### Everything ruled out afterwards, and on what grounds

| City | Ruled out on | Detail |
|---|---|---|
| Denver | schema | no address, classification or geometry; 347 datasets checked |
| San Jose | no bulk source | third-party lookup only, no export |
| Dallas | **currency**, on the second look | its only usable source froze on 2022-11-15; and `ync5-xnfn`, the dashboard `PLAN.md` said to check, **is not a dataset** — HTTP 403, 0 columns |
| Fort Worth | rail | data workable (72,065 rows) but only TEXRail + TRE; ~19% missing coordinates |
| Austin | no business data | the file named "Certificates Of Occupancy" is **291,759 construction permits** with no business name or classification |
| Charlotte | no business data | zoning and permit-review only; county GIS had none |

**Dallas is the instructive one**: ruled out twice, on different grounds each
time. The first pass called it marginal on schema; the second killed it on
currency. A frozen dataset passes every schema check ever written.

A later pass screened the whole remaining list and **surfaced three candidates
the shortlist never had** — including Seattle re-framed as a multi-municipality
build. That pass also ran the distribution checks the 2026-09-18 screen had
skipped, which is how D.C.'s office catch-all and 49%-residential-rentals were
found before any code was written.

---

## 2. Founding architecture, and why each choice was made

Absent from the first summary, and all four are still load-bearing.

**The hybrid macro→detail architecture** was chosen over one global map because
of a measured ceiling in the prototype: it needed marker clustering for
**11,409 points in one city**, plus a custom cluster-icon fix and a fixed-pixel
map to work around **Leaflet.heat issue 95** — an uncaught `IndexSizeError` on
init when the container size isn't resolved, which *silently stops every later
`.addTo(map)`*. Those problems compound across cities in one instance. Each
city map is its own Leaflet instance with its own bounds.

That same bug resurfaced twice more, and both fixes trace back to it: the maps
keep a fixed 1000 px layout for initialisation, and phone-width rendering was
fixed by **resizing after init, not before**.

**The pipeline/app split** exists because geopandas cannot be a runtime
dependency on Streamlit Cloud. `requirements.txt` stays at streamlit + pandas;
the geo stack lives in `requirements-pipeline.txt`. Every later decision about
`outputs/` being committed follows from this.

**Per-city config, not a shared registry loader** — deliberately not
generalised at one or two cities. Nine cities in, a shared registry still
hasn't been built, and the per-city configs have absorbed five genuinely
different data shapes without one.

**Per-city projected CRS as a value**, because the prototype hardcoded UTM 10N.
The entry's phrasing is the best one-line statement of the hazard in this
project: *"a wrong zone is the degrees-vs-metres bug one level deeper."* San
Diego derived EPSG:32611 and San Francisco EPSG:32610 independently from
longitude rather than copying.

Two identity decisions were made at city #1 and have held: the project is
**never named after a city**, and the UI was made deliberately unlike the
prototype's — light base, teal, Space Grotesk against the prototype's dark and
Inter — "so the two portfolio projects read as distinct products."

---

## 3. Station scope: the work my summary reduced to one line

**San Diego** established that a boundary polygon beats a name list. 63 station
names collapsed to 47 in-city, **16 outside** (El Cajon, La Mesa, Lemon Grove,
Santee, National City, Chula Vista) — and crucially, several were *not
guessable by name*: 24th Street and 8th Street are in National City; Palm
Avenue and Beyer Blvd are in San Diego. A hand-curated list would have got
those wrong silently.

**San Francisco** produced the four sub-transit-line filters, specified by the
owner, and both rejected alternatives were measured rather than argued:

- **Keep all 147 stops** → rings overlap continuously, flattening the distance
  gradient the whole project is about.
- **Subway only** (~12 stations) → **74% of the 125 surface stops are more than
  0.6 mi from the nearest subway station**, median just over 1 mi. It would have
  dropped the Sunset, Bayview/Visitacion Valley and Ingleside districts
  entirely.

San Francisco also needed **four hand-curated aliases after** the
direction-suffix regex, found by a pairwise physical-distance check that
surfaced four pairs under 200 ft apart which the regex could not merge — "Van
Ness Station" vs "Metro Van Ness Station", "King St & 4th St" vs "4th St & King
St". The generalisable part: after collapsing names, measure the distances, or
you keep duplicates that look like distinct stations.

And SF was the first city to use **its own palette** rather than the agency's,
for a reason unrelated to trademarks: SFMTA's colours have changed across
revisions and some lines currently *share* a colour to signal combined service,
which defeats a map needing six distinct lines.

---

## 4. The privacy arc — the project's strongest thread, and my biggest omission

My first pass mentioned Boston's and D.C.'s measurement gaps. It missed the
trajectory entirely, and the trajectory is the interesting part: **four
consecutive corrections, each finding the previous method wrong.**

### The principle, decided at Los Angeles

*"Publish public commercial information, not personal information."* And the
sharp part, which is easy to lose: **"it is in a public dataset" settles the
licence question, not the publishing question.** This project republishes the
data in a new, more usable form — a searchable pin at a precise coordinate —
which is a different act from the registry's own listing. Where the two
conflict, the map loses the row.

### Los Angeles: the catch-all that was two problems at once

68.1% of LA's rows carry no `dba_name`, so step 2 fell back to the registrant's
name for **12,465 of 23,839 pins (52.3%)**; ~3,998 matched a conservative
personal-name pattern, and 37% of sampled rows had an APT/UNIT/STE/# in the
address. Excluding NAICS 812990 fixed it — that code supplied **2,255 of the
~4,100** person-like pins. One exclusion resolved both a privacy finding and a
long-standing data-quality item, because they were the same rows.

Heavier options were rejected as disproportionate: dropping the registrant
fallback everywhere (loses real storefronts whose registry has no dba), and
removing names from tooltips entirely.

### Philadelphia: ~93,000 individuals, avoided by a scope filter

Excluding `Rental` was a privacy fix as much as a scope fix. `business_name` is
never blank there — but **on rental licences it holds the owner's own name**,
with `legalentitytype = 'Individual'`: sampled rows returned real people's
names at their own property addresses. **Mapping active licences unfiltered
would have published ~93k individuals at their home addresses.**

### Then the residence signals were tested, and most of them failed

This is the entry I'd most want anyone to read. Four candidate signals, checked
against the City's own property register (583,779 rows, 94% join rate):

- **Mailing address matching the premises: worthless.** 41.9% of mapped pins — a
  shop's mailing address is normally its own premises. Removed from `PLAN.md`
  rather than left to mislead someone later.
- **Parcel land use alone: actively dangerous.** "Purely residential parcel"
  flags 7.95% of pins, *including 147 thirty-plus-seat restaurants on
  `APARTMENTS > 4 UNITS` parcels*. Acting on it would have deleted hundreds of
  real storefronts to remove a few dozen homes.
- **Homestead exemption** — the best signal, and one nobody proposed: granted
  only on an owner's primary residence, so it is a claim the owner made to the
  City rather than an inference. It still over-fires alone (2.22%).
- The final filter is the **conjunction**: person-like name AND `Individual`
  entity AND a purely-residential parcel. **8 pins.** All single-family; 5 are
  food preparation and 2 are caterers — home kitchens.

And the honest verdict on the earlier number: **0.00% was a false negative**,
corrected to ~0.1–0.5%. *"The model's conclusion survived — the exposure is
still negligible — but its precision did not, and the number it reported was
wrong."*

A reversal inside the same entry is worth noting too: an earlier version used
the homestead exemption as an *alternative* to the land-use test and removed 17
rows — but 8 sat on `MIXED USE` parcels, the rowhouse with a shop below and the
owner's flat above, "arguably Philadelphia's most characteristic" storefront.
The exemption is now **reported and not acted on**.

### San Diego: 42 pins became 315, because the question was wrong

The corrected figure is **315 (2.80%), 7.5× the original 42** — and the cause
was asking the wrong spatial question. San Diego's business coordinates sit
**5–15 m outside their own lot** (placed at street frontage; SanGIS parcels
exclude road right-of-way), so a point-in-parcel test matched **1 of 30**
sampled pins. The right question is *which parcel is nearest*, not *which
contains this point*. The earlier filter's fallback — "every parcel within 25 m
must be residential and owner-occupied" — answers a third question, and clears
any home with a rental next door.

Three further details worth carrying forward:

- The method's own flaw was checked rather than assumed away. Ranking by
  centroid while querying by boundary could misattribute a business to a small
  neighbouring house; measured, every one of the 315 flagged rows has its chosen
  centroid within **39.1 m** (median 21.6), because single-family lots are small.
- **The removed rows validate the filter by their own classifications**, which
  is stronger than any distance statistic: **23 "COTTAGE FOOD OPERATOR"** —
  California's licence category for food produced in a *home kitchen*,
  definitionally a home business — plus 20 "beauty shops – booth rental".
- The rate limit was **measured, not guessed** (~2 req/s sustained), and the
  script **aborts after 25 refusals writing nothing**, because a partial cache
  filters only where the lookup happened to succeed.

### The bug that came back within the hour

The **prefilter snapshot** bug was fixed in Los Angeles and reintroduced in San
Diego an hour later. When the bulk fetcher stopped reading business data, the
snapshot looked like dead code and was deleted; the per-point version then read
step 2's *filtered* output on the reasoning that "the filter only removes rows,
so the candidate set can only shrink." True, and beside the point: **the
shrinkage is exactly the rows that must stay removed, and without cache entries
they return.** Now stated in all three files.

---

## 5. Smaller lessons the first pass skipped

- **Probe output belongs in the scratchpad.** A screening pass left eight files
  in the home directory — including a saved 404 and a file named `.json` that
  was HTML — sitting there for three days. Now a rule in `CLAUDE.md`.
- **Map files cut ~28% by removing emitted waste, not content.** Worth
  remembering before anyone proposes dropping data to shrink a map.
- **The legend collapses itself when the frame is too narrow** — a responsive
  behaviour, not a bug, and the reason the label checker must drive both states
  explicitly (see the false failure in the first retrospective).
- **`.gitattributes` pins line endings**, without which every `outputs/` file
  churns on a Windows checkout.
- **`drift_check.py` went incremental**, and `docs/scaling_thresholds.md`
  records what breaks at what city count: the macro map at ~10, **`outputs/` in
  git at ~20 — the real ceiling** — and hosting at 40+.
- **Rect-derived geometry is unreliable in this browser pane**, and produces
  convincing false failures; a screenshot is the authority for anything about
  label position. Learned from a scoped verify, and it saved me from
  misreporting Boston's Blue Line twice.

---

## 6. What the arc looks like whole

Read end to end, the project's defining pattern is not that it got things
right. It is that **each city broke the method that worked on the previous
one**, and the method was changed rather than the city forced to fit:

1. **San Diego** — a name list won't scope stations; use a polygon.
2. **San Francisco** — "keep every station" fails on street-running rail; four
   measured filters instead.
3. **Los Angeles** — coordinates in a public registry can be corrupt (9%), and
   a trade-name fallback can publish people; exclude the catch-all.
4. **Chicago** — a city's own licence taxonomy needs catch-all types classified
   by a second field.
5. **New York** — one registry may not exist at all; assemble four, and reduce
   the rings when stations are 482 m apart.
6. **Philadelphia** — 79% of a register can be landlords; two buckets is an
   honest answer, and residence signals must be tested not assumed.
7. **Miami** — a county register can cover 34 municipalities at once, which
   makes a regional map cheaper than a city one.
8. **Boston** — three registries, and a category can be *absent* rather than
   thin.
9. **Washington D.C.** — one register can cover everything, and a feed can
   expire in ten days.

Nine cities, nine method changes. The cost was re-work; the benefit is that
`add-city` now encodes all nine, which is why D.C. — the most unusual data
shape of the set — took one session rather than three.
