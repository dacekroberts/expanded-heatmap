# Canada, start to finish: what the first country profile actually cost

A chronological record of the 2026-09-21 Canadian screen, written so the next
country is cheaper. The *process* generalised into
[`.claude/skills/add-country/`](../.claude/skills/add-country/SKILL.md); the
*findings* live in [`canada_step0_endpoints.md`](canada_step0_endpoints.md) and
[`licenses/`](licenses/). This file is the narrative that connects them, and
the record of what was got wrong.

**Nothing was built.** Six cities passed Step 0. That is the claim.

> **That sentence was true when it was written and is now history.** All five
> viable cities were built the same day, 2026-09-21, between 14:19 and 21:24 -
> the sixth candidate, Surrey, shipped inside the Vancouver regional map rather
> than separately. **Part Two below** is the builds: what the process gained,
> what broke, and what to change before a sixth city. Read Part One for what a
> screen costs and Part Two for what a build costs; they are different
> questions and the answers turned out to be different shapes.

## The order it ran in, and why the order was right

| # | Stage | Outcome |
|---|---|---|
| 1 | **Rail screen** | 13 candidates → **6**, before a data catalogue was opened |
| 2 | Business-data schemas | 6 → 6, but Ottawa dropped and Montréal nearly lost |
| 3 | Licences | 11 texts stored; 5 cities carry prescribed notices |
| 4 | Privacy regimes | 4 provinces, and they disagree |
| 5 | Boundaries | 6 found; **5 had a trap** |
| 6 | Geocoding | Only 1 of 6 needed it |
| 7 | **Station density** | Produced the ranking, and inverted it |
| 8 | Classifications | Found the multi-value trap |

**Rail first was the single best decision.** It is the cheapest disqualifier —
a city with no urban rail is out however good its registry — and it removed
almost half the list for the cost of reading `routes.txt`. `scripts/screen_rail.py`
came out of this stage and is reusable for any country.

**Station density last was the second best.** It is the only stage that
produced a *ranking* rather than a pass/fail, and it overturned the working
assumption that Toronto, being largest, was the prize.

## What the screen concluded

| City | Sites/station | Buckets | Notes |
|---|---|---|---|
| **Vancouver** | **861** | 3 | Densest map measured anywhere in this project |
| **Surrey** | 549 | 3 | No rail of its own; a regional pair with Vancouver |
| **Montréal** | 252 | 3 | Best-documented source in the project |
| **Edmonton** | 153 | 3 | 100% in-city stations |
| **Calgary** | 103 | 3 | 83 in-city stations — a bigger map than Boston's 71 |
| **Toronto** | **41** | **2** | Boston's twin; retail absent |

**Ruled out:** Ottawa (rail, but no general business register — food inspections
only), Winnipeg, Hamilton, Québec City, Halifax (no urban rail), Mississauga
and Brampton (no urban rail reaches them; Brampton's data is excellent and
unusable until the Hurontario LRT opens, revisit mid-2027).

## Five conclusions that had to be reversed

Recorded because the pattern matters more than any individual error. **Every
one came from asserting off a column's existence, a dataset title, or a
plausible-looking flag instead of measuring.**

| # | Asserted | Actually |
|---|---|---|
| 1 | Montréal is food-only | A 28,621-premises survey with NAICS and 100% coordinates — found by reading the catalogue instead of grepping it |
| 2 | Publishing a sole trader's name would breach the licence | Ontario excludes business-capacity information **explicitly, even from a dwelling** |
| 3 | Edmonton and Vancouver need geocoders | 111 and 1,583 rows respectively; the rest have no address at all |
| 4 | Surrey's Home Occupation flag doesn't fix its exposure | It does — the earlier test measured name-pattern rate, not privacy exposure |
| 5 | Toronto mis-codes its subway as `route_type 0` | The **mirror was three months stale and had no subway in it**; the real feed codes it as type 1 |

Number 5 was the most consequential because it had already propagated into
three files. It produced a durable fix: `screen_rail.py` now reads
`feed_info.txt` and prints `[FEED EXPIRED]`.

Number 4 is the subtlest, and worth understanding rather than just noting. The
claim "dropping Home Occupation does not resolve the exposure" was *true as
measured* — the person-name rate is 9.11% on the dropped side and 9.38% on the
kept side — and *wrong as reasoned*, because it tested the wrong thing. The
exposure that matters is a person's name published **at their home**, and the
split removes exactly where those coincide. A premises filter has no reason to
change a name-pattern rate.

## Canada versus the US, as implementation differences

| | US | Canada |
|---|---|---|
| Licence regime | Heterogeneous — PDDL through MTA forbidding modification | One OGL template; 4 of 6 near-identical |
| Attribution | Varies; several require none | Prescribed wording, 5 of 6 |
| Breach | Usually unspecified | **Automatic termination** in 3 of 4 OGLs |
| Personal information | The project chose its own line | **Carved out of the licence grant itself** |
| Home signal | Inferred: parcel land use + owner-occupancy | **Stated on the licence** |
| Owner-occupancy data | Open (assessor rolls) | **Not open anywhere** |
| Geocoding | Census bulk geocoder, national and free | **No equivalent** — city address points instead |
| Classification | NAICS usually | Local, and often **multi-valued** |
| Coordinate quality | LA had ~9% corrupt | 99.8–100% clean in all six |
| Transit licence | The loosest end of every review | Mostly the city's own OGL |

Two of these change how a build is written, not just what it is allowed to do:

**The home signal moves up the stack.** The US pipeline infers residence from a
parcel join. Canada states it on the licence — Surrey's `LicenseType`,
Edmonton's `<Home Based Business>`, Calgary's `homeoccind`. That is better
evidence and less code. Only Vancouver needs the US-style approach, and for it
the *address* join fails at 6.5% while the **spatial** join reaches 99.9%.

**Personal information stops being only an ethical choice.** In the US the
project declined to publish ~4,000 individuals' names in Los Angeles although
the data was public. In Canada the same restraint is partly a licence
condition, because every OGL carves Personal Information out of the grant. The
project's existing standard sits above the legal floor in all four provinces —
which is a sturdier position, because it does not move when a statute is
repealed, as Alberta's was in June 2025.

## The language work, concretely

Montréal was the first non-English source, and most of it was already handled:

- **Column names** — solved by the existing architecture. Each city's config
  names its own columns and step 2 renames to the taxonomy's `VALUE_COLUMN`, so
  `NOM_ETAB` is no harder than `dbaname`.
- **Category labels** — belong to the taxonomy module, which the project's own
  invariant already makes the single owner of tooltip and legend text. If
  Montréal keys off `SCIAN` the question disappears entirely, because `SCIAN`
  **is** NAICS and the English bucket labels come from `naics.py`.
- **Encoding** — `SOURCE_ENCODING` is now declared per city and passed at all
  11 raw reads. All six Canadian sources are UTF-8; Québec data is often
  `latin-1`, which is where it will first bite.
- **Terminal mojibake is not file corruption.** The Windows console codepage
  mangles accented output; `PYTHONIOENCODING=utf-8` fixes the display. This
  cost real time twice.
- **Business names stay in their own language.** Always.
- **The search vocabulary is the real language problem.** Not encoding, not
  labels. `locaux-commerciaux` contains none of *business*, *licence*,
  *permis*, *entreprise* or *commerce*, and a keyword scan concluded the city
  was food-only. The fix is now in `add-city` Step 0: read the whole
  catalogue.

## What a second country should cost

Most of what this produced is reusable: `screen_rail.py`, the `add-country`
checklist, the per-city fetch patterns for all four portal types, and the
structure of the licence store. What will not transfer is the licence template
and the privacy statute — those are per country, and they are the expensive
half.

So the estimate for a country like Australia, with municipal licensing and
open portals, is **considerably less than this one**, and most of the remaining
cost is reading terms and statutes rather than finding data.

For a country shaped differently — France's SIRENE is a national, open,
address-level establishment register covering every city at once — the data is
*easier* and the project's assumptions are *harder*, because scoping and
taxonomy were both built around per-city municipal registers. That is a design
question, not a screening one, and it should be recognised before the screen
rather than after.

---

# Part Two: the five builds

**Canada ran 14:19 to 21:24 on 2026-09-21** - about seven hours for five cities,
after roughly a day of profiling. A second session worked `worktree-staging` in
parallel from 14:59, screening other countries while cities were built here.

The headline is not the speed. It is that **the same class of error recurred in
four of the five cities**, was caught four separate times, and was only turned
into a shared check after the fourth. That is the lesson this half of the file
exists for.

## The order it actually ran in

| Time | Commit | Event |
|---|---|---|
| **14:19** | `3488f11` | **Canada screened: 13 candidates to 6 viable.** Rail first - `screen_rail.py` removed 6 before a data catalogue was opened |
| 14:30 | `c66e638` | The screen generalised into the **`add-country` skill** |
| **14:59** | `3f19031` | Sessions split by role and path; **the staging session forks here** and runs the global country screen in parallel until 17:26 |
| **16:26** | `60e4df3` | **Vancouver + Surrey** - first non-US city, first regional build, two registries, two licences, two taxonomies |
| 16:51 | `78747ad` | **Canada re-ranked on storefront counts.** The published ranking counted every mappable licence for five of six cities and only storefronts for the sixth, so it was not internally comparable. Montreal next, not Surrey |
| 16:58 | `9788294` | The four remaining cities re-briefed from the corrected measurements |
| **17:14** | `65138bb` | **Montreal** - the first field survey (`locaux-commerciaux`), and the first city needing no taxonomy module at all |
| 17:22 | `be4de74` | Macro-map labels moved pre-emptively to clear the cities not yet built |
| 17:59 | `92ddab3` | Three briefs re-measured in advance. **Toronto's 234 "stations" were PLATFORMS** - it moves from sixth to fourth |
| **18:58** | `7380eba` | **Calgary** - its ranking figure was platforms too, 75 to 137 per station. Its register names premises itself |
| 19:12 | `2c86056` | The font stack reaches the tooltip, where non-Latin names actually land |
| 19:49 | `e66655a` | *(staging)* `drift_check --jobs N` - the real scaling limiter |
| **19:59** | `5341b62` | **Edmonton** - three of its 33 "stations" are garages nobody can board at |
| 20:14 | `1b75367` | A race that could strand any embedded map at a narrow-width zoom |
| 20:28 | `fe28df3` | **`brief_check.py`** - briefs made executable. Its first run corrects Toronto again, 118 to 111 |
| 20:29 | `de01955` | `decisions_index.py`, over what turned out to be 100 entries and 57k words |
| 20:38 | `b731452` | Staging merged: the global screen, `--jobs`, and the WMATA licence notes |
| 20:44 | `624a2a6` | Toronto's last open question closed: **the 71.4% was the wrong denominator**, 92.8% on storefronts |
| **21:09** | `b93afc5` | **Toronto** - 234 platforms to 110 stations to 108 in-city, every line matching the TTC exactly |
| 21:15 | `e9ed983` | Toronto's brief checks synced: they had been **stale and passing** |
| 21:24 | `e2b481c` | Paperwork closed. **Canada complete at five cities.** |

Per-city marginal cost fell steeply. Vancouver was the longest (two registries,
a parcel-join residence inference, a boundary that is a line not a polygon);
Edmonton the shortest (the register sorts itself); Toronto the most expensive
of the five, entirely because of the geocoding step.

## What the process gained

**New tooling, all of it born from a specific failure:**

- **`add-country`** - the national facts that disqualify every city at once,
  profiled once instead of per city. 13 candidates to 6 for about a day.
- **`scripts/brief_check.py`** - 13 check kinds, claims declared as JSON in a
  fenced ```brief-checks block beside the prose that relies on them. Built
  because Edmonton inherited three wrong claims from its own brief and the
  MEASURED/ASSERTED labels did not stop it.
- **`drift_check --jobs N`** - 14 cities in **37 seconds**, from minutes.
- **`scripts/decisions_index.py`** - a generated index, because
  `drift_check` ends every run telling you to find "the latest baseline entry"
  by eye in 5,400 lines.
- **`scripts/probe_geodata.py`**, and `screen_rail.py` now prints feed expiry -
  the latter because a catalogue mirror hid an entire transit mode.

**Discipline added to `add-city`:**

- **A station count needs TWO gates and a cross-check**, never a name check:
  nearest-neighbour **spacing** (are these platforms?), **boardability** (are
  these stations?), and agreement with the operator's own published per-line
  counts.
- **Line colours are measured, not chosen** - CIE76 Delta-E of about 45 against
  the three category pin colours - and the constraint is scoped explicitly as
  **intra-city only**. Reuse across cities costs nothing, because no map shows
  two cities' lines at once.
- **Sample the names before applying a rule.** The merged-category rule was
  wrong twice in Edmonton, and a sample overrode it both times.

**Bugs found and fixed in passing:** `scaffold_city.py` splicing new cities
into a comprehension (third occurrence; repaired by hand the first two),
the embedded-map fit race, `.leaflet-tooltip` inheriting a Latin-only font, and
Calgary's Blue Line shipping at Delta-E 3.3 from Retail blue - the same colour
as the pins drawn over it.

## The error taxonomy

Sorted by frequency, because the shape matters more than any instance.

**Denominator errors: six during the builds, plus two committed while writing
them up.** The dominant class by a wide margin, and the project had already
recorded it as a recurring fault before Canada started.

| # | The wrong number | The right one |
|---|---|---|
| 1 | Montreal 440 per station, summing per-station counts | **151**, counting the union of rings |
| 2 | Toronto 41 per PLATFORM across 234 | per station |
| 3 | Calgary 75 per station on 83 platforms | **137** on 45 stations |
| 4 | Edmonton 76 on 33 stops, 3 being garages | **79** on 30 stations |
| 5 | Toronto 118 stations, one naming convention handled | **110**, three conventions |
| 6 | Toronto 71.4% geocode match across all licence rows | **92.8%** on storefront rows |
| 7 | "92 categories, not the 72 asserted" | both right: 92 all history, 72 active |
| 8 | "blank names on 21.4% of rows" | **0.5%** of the rows that reach the map |

Numbers 7 and 8 are mine, made while correcting numbers 1 to 6, which is the
most useful thing in this table: **knowing the failure mode does not prevent
it.** Only naming the set alongside the number does.

**Trusting a cited document instead of opening it: three, and all three were
licence positions.** New York's site footer (which covers the website, not the
data), Philadelphia's terms incorporated by reference, and Edmonton's notice
that "was not required" - where the obligation sat in a redistribution clause
the credit sentence never mentions. This was already the `read-licence` skill's
entire premise, and it happened again.

**A stale mirror or a duplicated layer: four.** The Mobility Database's TTC copy
was three months expired and contained **no subway at all**; Edmonton's eight
individual Socrata GTFS tables were *staler* than the zip its brief recommended
replacing; Calgary publishes two "City Boundary" datasets, one of them 53 bytes
of valid empty GeoJSON; Edmonton publishes four "Corporate Boundary" layers,
two of them pre-annexation.

**A field that looks like a filter and is not: two.** Los Angeles' city field
(postal community names) and Toronto's `MUNICIPALITY_NAME`, which holds the six
pre-1998 municipalities - so matching "Toronto" keeps 30% of the city and
would have dropped most of Line 2. Caught before it ran, by checking the values
rather than the column name.

**Broken instruments producing confident findings: three.** A weak geocode join
manufactured a **12x ward-level bias** that read as disqualifying and was an
artefact; a WKT pattern against GeoJSON geometry produced a 0% join; and
`brief_check` reported 9/9 while disagreeing with the build, because a check
can only test what it encodes. The guard that caught the second one -
`GEOCODE_MATCH_RATE_MIN` - is the pattern worth copying: **an instrument has to
reproduce a known number before its new numbers mean anything.**

## What to change before a sixth city

Ranked by value, and the first is worth more than the rest together.

1. **Make the station count a shared module.** It was wrong in **four of five**
   Canadian cities, in per-city `step1` code, differently each time. A
   `pipeline/stations.py` owning the four collapse mechanisms, both gates and an
   `expected_per_line` cross-check would have caught Toronto and Edmonton before
   they shipped, and stops city six re-deriving it. Everything needed already
   exists, scattered across five `step1_stations.py` files.

2. **Make the drift baseline machine-readable.** `drift_check` ends by telling
   you to compare per-step counts against `DECISIONS.md` by eye. Write them to
   JSON and diff them, so a count regression is loud rather than a reading
   exercise.

3. **Put the denominator convention in code.** Eight errors in one class says
   prose is not working. A helper that cannot format a percentage without naming
   the set it was measured on would make the error unwriteable.

4. **Give `brief_check` a `--vs-config` mode.** Checks passing while
   disagreeing with the build is a flaw in the tool's premise, not a one-off.
   Diff a brief's expectations against the built city's constants.

5. **Assert colour separation at render time.** `map_common` should refuse to
   draw a line within about 45 Delta-E of a category colour. Calgary shipped at
   3.3 and it went unnoticed until Edmonton's build ran the check for the first
   time.

6. **Keep the country-before-city order.** Validated: rail is the cheapest
   disqualifier, and per-city marginal cost genuinely collapsed after the
   profile. Depth per country beats breadth across countries.

## What is worth keeping unchanged

`classify()` raising on an unknown value rather than returning None - it caught
schema drift in three cities. `filter_to_storefront()` as the single filter
entry point. Recording a **verified** absence distinctly from an unexamined one
(Toronto has zero non-revenue stops, and that is a measurement, not a
silence). And the append-only decisions trail: it is long *because* the
convention works, and what was missing was a way in rather than less content.

## The five cities, as one comparable measurement

| City | Storefronts in ring | Stations | Per station |
|---|---|---|---|
| Vancouver | 4,668 | 24 (with Surrey) | **206** |
| Montreal | 9,733 | 64 | **151** |
| Calgary | 6,171 | 45 | **137** |
| Surrey | - | - | **135** |
| Toronto | 8,739 | 108 | **81** |
| Edmonton | 2,380 | 30 | **79** |

**Three of these six numbers moved during the builds, two by more than 1.8x,
and every move was a wrong station count or a wrong denominator rather than a
change in the data.** The largest city came fifth, which is the same conclusion
Part One reached for a different reason: Toronto licenses food and trades but
not general retail, so its Retail bucket is the regulated slice alone.
