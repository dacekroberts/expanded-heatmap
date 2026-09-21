# Build brief — Montréal

**For the session taking Montréal.** Everything Step 0 asks for is below,
measured 2026-09-21 and re-measured the same day after the Canada ranking was
found not to be comparable. Sources:
[`canada_step0_endpoints.md`](../canada_step0_endpoints.md),
[`licenses/canada-required-notices.md`](../licenses/canada-required-notices.md),
[`licenses/canada-privacy-regimes-note.md`](../licenses/canada-privacy-regimes-note.md).

Claims are labelled **MEASURED** (a number and the check that produced it) or
**ASSERTED** (plausible, unchecked — verify before building on it), per
[`session_roles.md`](../session_roles.md).

**Read this brief in the knowledge that Vancouver's was wrong on five of
eleven checkable claims.** Two of those would have changed its pipeline. Every
number here that came from the original profile has been re-measured, and where
the two disagree the brief says so.

---

## Why this city

**MEASURED, on the basis every other city in this project uses.** **151
storefronts within the 0.6 mi ring per in-city station** — 9,695 across 64
on-island stations. That puts Montréal just under Washington D.C.'s ~173 and
second among Canadian candidates behind Vancouver's 206.

**The published figure was 252, and it was not comparable.** It counted every
surveyed premises rather than storefronts. Montréal's inflation was the
*smallest* of the five mis-measured cities (1.7x against Vancouver's 4.2x),
which is why re-ranking **moved it up past Surrey** rather than down.
Reproduce with `python scripts/rank_canada_storefront_density.py`.

**It is also the cheapest build remaining, and the best-matched source in the
project.** Three reasons, all measured:

- **`SCIAN` IS NAICS**, so `pipeline/taxonomies/naics.py` applies unchanged and
  this city needs **no taxonomy module at all** — the only Canadian city of the
  six where that is true, against Calgary's 96 categories and Edmonton's 60.
- **69.4% of non-vacant rows are storefronts**, against Vancouver's 28.2%,
  because the source is a *street-level commerce survey* rather than a licence
  register. Nothing has to be filtered out on scope grounds.
- **No geocoding step, and no name problem.** `LAT`/`LONG` are 100% populated
  and `NOM_ETAB` is 100% populated with an establishment name.

## Start here

```bash
python scripts/scaffold_city.py --dry-run \
  --slug montreal --name "Montréal" --system-name "Métro" \
  --taxonomy naics \
  --lat 45.5019 --lon -73.5674
```

**No `--new-taxonomy`, and that is the headline.** `--taxonomy naics` reuses
the existing module. Step 2 renames `SCIAN` to the taxonomy's `VALUE_COLUMN`
(`naics`) and everything downstream already works. `--map-step` stays at the
default 3.

**ASSERTED:** that the accented slug/name causes no trouble. Every other city
here is ASCII. `--name "Montréal"` flows into a page filename and a
`cities.py` entry; if it bites, use `Montreal` as the display name and say so
in `DECISIONS.md`. The page-number convention is in `app/cities.py`: cities are
1..N in implementation order, information pages sit at 90/91, and
`next_page_number()` returns **11** for this city.

## Sources

### Business — `locaux-commerciaux`, CKAN

| | |
|---|---|
| Portal | `donnees.montreal.ca`, CKAN |
| Package | `locaux-commerciaux` |
| Resource (2025) | `01ded48e-f982-4703-975e-4be0769ef3ee` |
| Direct URL | `https://donnees.montreal.ca/dataset/f8582c4d-a933-4306-bb27-d883e13dd207/resource/01ded48e-f982-4703-975e-4be0769ef3ee/download/occupation-commerciale-2025.csv` |
| Licence | **CC-BY 4.0, with a broader attribution clause** — see "Before you commit" |
| `SOURCE_ENCODING` | `utf-8` |
| Delimiter | **comma** |

**MEASURED 2026-09-21:** 28,621 rows, 34 columns. `LAT`/`LONG` 100%,
`NOM_ETAB` 100% (20,243 distinct), `SCIAN` 99.6% (127 distinct values),
`ARRONDISSEMENT` 100% (32 distinct), `VACANT_A_LOUER` Non 27,909 / Oui 712.

Columns: `ID, ORIGINE, T_COMMERCE, DATE_CREATION, CIVIQUE, TYPE_VOIE,
LIEN_VOIE, NOM_VOIE, ORIENTATION, ADRESSE, SUITE, ETAGE, NOM_CENTRE, NOM_ETAB,
ID_USAGE1, USAGE1, ID_USAGE2, USAGE2, ID_USAGE3, USAGE3, SCIAN,
ACCES_MOBILITE_REDUITE, VACANT_A_LOUER, ARRONDISSEMENT, QUARTIER, SDC_NOM,
SECTEUR_PME, ENFANT, MULTIUSAGE, MULTIOCCUPANT, COORDY, COORDX, LAT, LONG`.

**Three traps, all MEASURED:**

- **`donnees.montreal.ca` answers a plain client with `RBAC: access denied`.**
  A browser `User-Agent` is required. This is a portal-wide behaviour, not a
  dataset one.
- **3,500 rows are `USAGE1 = 'VACANT'`** — an empty shopfront, not a business.
  **The original profile did not record this at all.** They must be excluded
  before anything is counted, and they are 12.2% of the file. `VACANT_A_LOUER`
  is a *separate*, narrower flag (712 rows) and is not a substitute for it.
- **`SCIAN` is a 1-character placeholder on 294 non-vacant rows.** So usable
  6-digit codes cover **98.8% of non-vacant rows**, not "99.6%" of everything —
  the profile's figure was measured on the wrong set, which is the denominator
  error this project has now hit four times. Filter on
  `SCIAN.str.len() == 6`.

**ASSERTED:** that 2025 is still the current vintage. The package holds
2021–2025 as separate resources and gains one a year; `package_show` lists
them. Re-check rather than copying the resource id.

**ASSERTED, and worth ten minutes before step 2:** `MULTIUSAGE`,
`MULTIOCCUPANT` and `ENFANT` are flags this brief has *not* interrogated. In a
premises survey they plausibly mark one address holding several businesses, or
a parent/child record pair. If they mark duplicates, dedup must account for
them — and unlike a licence register there is no `licence_id` to dedup on.
Check the distribution and a sample before choosing a premises key.

### Transit — STM Métro

**MEASURED. Use the AGENCY's feed, not the catalogue mirror, and this city is
the proof.**

| | |
|---|---|
| Agency feed | `https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip` |
| Validity | `feed_start_date` 20260615, `feed_end_date` **20261025** (+34 days on 2026-09-21) |
| Mobility Database mirror (id 2126) | `feed_end_date` 20260823 — **29 days EXPIRED** |

The mirror is stale *for this city, today*. Station counts happen to match
(68 either way), so the ranking was safe — but this is the Toronto lesson
recurring, and a build must not take the mirror. `feed_info.txt` carries no
`feed_license` column, so the feed declares no licence of its own; STM's
attribution obligation comes from the portal, not the feed.

**MEASURED:** 4 routes at `route_type 1`, the Métro lines exactly, with the
agency's own colours from `route_color`:

| route_id | name | colour |
|---|---|---|
| 1 | Ligne 1 – Verte | `#00B300` |
| 2 | Ligne 2 – Orange | `#D95700` |
| 4 | Ligne 4 – Jaune | `#FFD900` |
| 5 | Ligne 5 – Bleue | `#0095E6` |

**Measure contrast in BOTH modes, dark first.** `#FFD900` is a bright yellow
and `#00B300` a saturated green; the project's method and the reason it matters
are in `pipeline/vancouver/config.py`, and D.C.'s Silver Line is the case where
measuring only the light basemap produced a backwards answer.

**MEASURED:** 72 served stops collapsing to **68 stations**, with
`parent_station` populated on all 72 — so the collapse is clean and needs no
suffix regex and no alias dict, unlike Vancouver's `@ Platform N` names. Names
are of the form `Station Angrignon`. **Do not strip a trailing word blindly**:
Boston's bug turned "North Station" into "North".

**MEASURED:** `shapes.txt` is present, so line geometry is real rather than
straight-line. Two lines may branch — verify a covering shape set per line as
Vancouver's config does, because the single most-used shape silently drops a
branch.

### Boundary — `limites-administratives-agglomeration`

```
https://donnees.montreal.ca/dataset/9797a946-9da8-41ec-8815-f6b276dec7e9/resource/e18bfd07-edc8-4ce8-8a5a-3b617662a794/download/limites-administratives-agglomeration.geojson
```

**MEASURED:** 34 features in **EPSG:4326** (real degrees — take the WGS 84
resource, not the `-nad83` one, which is MTM zone 8). They dissolve to **one
Polygon of 619.0 km²**.

**The `TYPE` column is what makes scope selectable**, and it is the reason to
use this layer: `Arrondissement` 19, `Ville liée` 15. So "city proper" and
"agglomeration" are one filter apart.

**The 619 km² includes water** — the agglomeration's land area is ~499 km² —
because the boundary follows the river channel rather than the shoreline. That
is harmless for a point-in-polygon containment test, but it means an *area
check* on this layer cannot be tight the way Vancouver's 118.8 km² one is. Do
not copy that tolerance.

### Projected CRS

**EPSG:32618** (UTM 18N), derived from longitude ≈ −73.57 per the project
invariant. Note this differs from every other Canadian candidate (Vancouver
32610, Calgary 32611, Edmonton 32612) — the CRS is per city, never copied.

## Station scope — 4 stations are off the island

**MEASURED.** The Métro leaves the agglomeration: **3 stations in Laval**
(Cartier, De la Concorde, Montmorency) and **1 in Longueuil**
(Longueuil–Université-de-Sherbrooke). Those are excluded, giving **64 in-city
stations**, which independently reproduces the profile's "64 in agglomeration".

**The data names them without a boundary layer**: each of the four has **zero**
surveyed premises within its outer ring, because the survey stops at the
agglomeration's edge. Useful as a cross-check — but filter on the boundary, not
on the zero, so the reason is explicit.

**Do NOT drop Station Jean-Drapeau.** It also scores zero: it is on Île
Sainte-Hélène, inside Montréal, in a park with no commerce. It is a genuine
in-city station and dropping it would inflate the per-station rate. This is the
one place where "zero nearby" and "out of scope" come apart.

**ASSERTED:** whether the survey covers all 15 villes liées. `ARRONDISSEMENT`
has **32** distinct values against the boundary's 34 features, so two are
missing or named differently. Resolve this before scoping: if the survey is
thin in the villes liées, an agglomeration-scoped map will look sparse there
for a data reason, and the city page has to say so.

## Sub-line filters — probably none, but measure

**ASSERTED.** The Métro is fully underground and grade-separated, which is
D.C.'s and SkyTrain's shape, so all in-city stations should be kept and no
thinning applies (`docs/sub_transit_line_filters.md`). **But measure the
spacing**: central Montréal stations are close together, and Vancouver's
downtown median nearest-neighbour was 841 m against a 966 m ring. Print the
distribution rather than asserting it, as every built city does.

## Privacy — the strongest position in the project

**MEASURED, and this is the easiest privacy verdict here so far.** The survey
publishes **no registrant-name column at all**. `NOM_ETAB` is the
*establishment's* name, populated on 100% of rows, so:

- there is **no trade-name/legal-name fallback**, so no pin can display a
  person's name the pipeline substituted — the structural claim New York,
  Miami and Boston can make, and which Vancouver could not;
- there is nothing to omit at the download boundary.

Still required, per `CLAUDE.md`: add `montreal` to
`scripts/check_personal_exposure.py`'s `REGISTRIES` with `raw=None`,
`trade=None`, `owner=None` so the fallback measure reports as **structurally
absent** — a stronger statement than a low count — run it, and record the
verdict in `DECISIONS.md`.

**Québec's privacy regime is the strictest of the three provinces profiled**
and does NOT clearly exclude information about an individual in a business
capacity (see `licenses/canada-privacy-regimes-note.md`). That matters much
less here than it would for a licence register, precisely because no
individual's name is in this file — but it is the reason not to add a second,
name-bearing Montréal source without reading the statute again.

## Before you commit

**TWO notices, from two different owners, and one has a clause no other source
in this project has.** Promote both into `docs/data_sources.md`, "Notices this
project MUST display when published", in the same commit as the city.

**1. Ville de Montréal** — the business data, CC-BY 4.0. The portal's
attribution condition is **broader than standard CC-BY**: you must

> "créditer les données et les contenus que vous utilisez et préciser si des
> modifications ont été effectuées **ou si des interprétations en ont été
> tirées**"

— state whether modifications were made **or interpretations drawn**. This
project plainly draws interpretations: ring density, category buckets,
storefront filtering. **A bare "data from the Ville de Montréal" does not meet
it.** The notice must say the map interprets the data. This is the first source
in the project whose attribution has to describe what was done to the data.

**2. STM** — the transit data, separately. The dataset's notes state it is
STM's property and that "selon la clause d'attribution de la licence Creative
Commons 4.0, la paternité des données doit être attribuée à la Société de
transport de Montréal." Credit **STM**, not the City.

Montréal also requires no suggestion of endorsement, and **prohibits
restricting access to the original data by legal or technical means** — nothing
this project does, but it is a term rather than a courtesy.

Also standing: the OSM basemap attribution, and the removal commitment in
`docs/data_sources.md`.

## Language — the first non-English source

- **Column names stay French**; the city's config names its own columns and
  step 2 renames to the shared ones. `NOM_ETAB` is no harder than `dbaname`.
- **Category labels belong to the taxonomy module**, which here is
  `naics.py` — so the legend and tooltips are already English and already
  shared with five other cities. `USAGE1`'s French labels are *not* used for
  bucketing and need no translation.
- **Business names stay in French, always.**
- `SOURCE_ENCODING = "utf-8"` (MEASURED: accented names parse correctly).
  Set `PYTHONIOENCODING=utf-8` before blaming the data for mojibake — it is
  usually the console codepage.

## Open questions, collected

1. **`MULTIUSAGE` / `MULTIOCCUPANT` / `ENFANT`** — do they mark duplicate or
   child records? There is no licence id to dedup on, so this decides the
   premises key. The largest genuine unknown here.
2. **Scope** — agglomeration (34) or city proper (19 arrondissements)?
   Agglomeration was already decided, but see (3) before committing to it.
3. **`ARRONDISSEMENT` has 32 values against the boundary's 34** — which two are
   absent, and is the survey thin in the villes liées?
4. **2025 resource id** — confirm it is still the newest vintage.
5. **Line branching** — verify a covering shape set per Métro line.
6. **Colour contrast** in both modes for `#FFD900` and `#00B300`.
7. **Station spacing** — measure against the 966 m ring rather than assuming
   the Métro needs no thinning.
