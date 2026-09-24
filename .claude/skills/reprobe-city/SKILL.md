---
name: reprobe-city
description: Re-probe a city that screening left thin - ask the city's OWN host, enumerate its whole catalogue, read who a 403 is for, and look for a second layer in a different shape (a building register's use class) - then measure the new shape's defect, control each layer, read licences in parallel and record. Use for every row in the master list's open screening gap, and for the one-bucket cities in Band C (Stockholm, Göteborg, Zurich, Singapore, Bucharest) to find out whether a second source exists. Not for a city screened for the first time - that is add-city Step 0.
---

# Re-probing a city: its own host, its whole catalogue, a second layer

Distilled from **Amsterdam, 2026-09-24**. It had been discarded as *"register
is aggregate"* on the top hits of ONE national search. Re-probed in one
evening, it went **discard → Band C** (a live hospitality-permit register on
the city's own API) **→ Band A** (plus the BAG's shop units as a second layer).
Every step that moved it was a probe the original screen never ran. Evidence:
`docs/global_country_shortlist.md`, the 2026-09-24 audit section; the brief is
`docs/build_briefs/amsterdam.md`.

**Two uses.** The **open screening gap** (17 rows in `docs/city_master_list.md`,
each naming its next probe) — the question is whether a register exists at
all. The **one-bucket cities in Band C** — the question is whether a SECOND
source exists, and Step 4 is the step that matters.

## Step 1 — Ask the city's own host, not the national portal

Amsterdam's discard rested on `data.overheid.nl`; everything that moved it sat
on `api.data.amsterdam.nl`, which no one had asked. A national catalogue's
harvest of a city is not the city: the permits were not in its results.

- Find the city's data host — portal, API, ArcGIS org, statistics office.
  Try `www.`; try the API root with **`Accept: */*`** (Amsterdam's refused
  without it). Sevilla's lesson also applies: a dead portal's last Internet
  Archive capture can name its successor.
- If the city's host is blocked, diagnose before recording (Globalping from
  inside the country against a foreign control — `address-join` Step 3). A
  geo-block is Band D's shape, never something to route around.

## Step 2 — Enumerate, don't search

- **List every dataset.** Amsterdam's API root holds 100. It was first
  recorded as 383, which counted dataset AND table paths — count datasets.
- Read the list by eye for anything premises-shaped, then for each candidate
  list its tables with **row count and field names** — one request per table
  with `_pageSize=1&_count=true` on a DSO API; `package_show` on CKAN.
- **Before believing any server-side filter, send a nonsense value.**
  Amsterdam's BAG filter returned 11,607 for `winkelfunctie` and 0 for
  `zzzzqqq`; a filter that is silently ignored returns the whole table.

## Step 3 — A 403 is a finding about access: read who it is for

Never worked around. Read the published schema or metadata for the dataset's
**authorisation scope**: Amsterdam's `hr_kvk` carries `FP/MDW` and `HR/R`,
`standbedrijven` `BSK/BEDRIJVEN` (`schemas.data.amsterdam.nl/datasets/<name>/dataset`)
— city-staff scopes, so a written request was judged unlikely to land and was
not drafted. A scope open to public registration is different: that is an
**owner's act** (a form with a name and e-mail), never this project's.

## Step 4 — Look for the second layer in a different SHAPE

The one-bucket problem is usually structural — Sweden has no general business
licence, Switzerland's STATENT is aggregate — so a second REGISTER of the same
shape will not appear. **Look for premises by permitted use instead: a
building or address register with a use class.**

- **Amsterdam's**: the BAG, `verblijfsobjecten` filtered to `gebruiksdoel =
  winkelfunctie` — **10,898 units in use, 100% with a point, 90% shop-only**.
- What the shape gives: every premises, a location, a current status. What it
  lacks: **no name, no activity, no occupancy**, and retail and personal
  services share one class. The owner accepted all of that for Amsterdam on
  one condition (Step 5).
- Where the shape may exist — **ASSERTED, unprobed; probe targets, not
  findings**: Sweden (Lantmäteriet's building register, purpose codes),
  Switzerland (the federal building and dwelling register, GWR), Denmark (BBR
  use codes), Norway (Matrikkelen building type), Czechia (RÚIAN building
  use), Spain (Catastro *uso*), Finland (the building register). Singapore
  and Bucharest: unknown. **Read the use-class field's values and fill before
  counting on it** — a class that is empty or one catch-all is no layer.
- Keep looking for the ordinary shapes too: a sector inspection register
  (food), a market or street-trading register, a licensing register for one
  trade (hairdressers). Two narrow sources can make the second bucket.

## Step 5 — Measure the defect the new shape brings, then filter or disclose

Name the defect and measure it before asking the owner. For a use-class layer
it is **vacancy** — an empty shop still has the shop class.

1. **Look for a per-unit filter first**: an occupancy or actual-use field
   (Amsterdam's `feitelijkGebruik` was empty on all 10,898), a per-unit energy
   or tax field, a join to a business register. Amsterdam's property snapshot
   (`standvastgoed`, 134 fields) had none; energy use was per neighbourhood;
   the per-unit sources (Locatus, the KvK) were paid or staff-only.
2. **If none is open, find the RATE.** City statistics often republish a
   commercial survey: Amsterdam's `bbga` carries Locatus's vacant sales points
   — **660 of 14,314, 4.6%**, per district and per neighbourhood.
3. **Put the number to the owner**: disclosable (Amsterdam — *"about 5% of
   shop units are empty (Locatus, 2026)"* on the page) or not.
4. **Check overlap between layers**: a takeaway can hold a food permit AND sit
   in a shop-class unit — de-duplicate by address at build.

## Step 6 — Control each layer on its own

Each layer against its own OSM control, with the ratio and its direction:
Amsterdam's permits **0.89×** OSM restaurants, BAG **1.77×** OSM shops.
Comparators: Prague 1.63×, Rome 2.60×. Overpass 504s are routine — try a
second host before recording anything.

## Step 7 — Licences: one `licence-read` agent per source, in parallel

Run them in the background while the brief is drafted. Amsterdam's took 10–12
minutes and ~135–145k tokens each. Two things they turned up that recur:

- **A city's copy of a national register may be SILENT while the national
  publisher is explicit** — the Kadaster's Public Domain Mark governs the BAG;
  use only the national fields, since the city's additions carry no licence.
- **SILENT with a conflict** (the permits: no licence live, CC BY in a retired
  record) is not resolved in the project's favour. Offer the owner the display
  that satisfies BOTH readings — Amsterdam: credit as CC BY 4.0.

Record access conditions separately from licence terms: Amsterdam's API key,
mandatory from an unset date, is a form the owner fills in.

## Step 8 — Record

- **A gap row that stays negative** goes to the discard table only if
  `python scripts/check_discard_evidence.py` passes it — kind, methods, host.
- **A band move is the owner's**; recommend with the tradeoff.
- **A brief** with a `brief-checks` block: the live endpoints, the filter, the
  licence pages (`present` / `absent`), the gated scope. Amsterdam's reads 8/8.
- The shortlist evidence section, a `DECISIONS.md` entry, and **the master
  list's counts in all four places** — the summary box, the band table, the
  band heading and the country table.
