# Canada, start to finish: what the first country profile actually cost

A chronological record of the 2026-09-21 Canadian screen, written so the next
country is cheaper. The *process* generalised into
[`.claude/skills/add-country/`](../.claude/skills/add-country/SKILL.md); the
*findings* live in [`canada_step0_endpoints.md`](canada_step0_endpoints.md) and
[`licenses/`](licenses/). This file is the narrative that connects them, and
the record of what was got wrong.

**Nothing was built.** Six cities passed Step 0. That is the claim.

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
