# Spain — country profile and Step 0 endpoints

Profiled 2026-09-22, following `.claude/skills/add-country/`. Spain is the
**fifth country** screened to this depth (after the US, Canada, Mexico and the
global sweep's country legs) and the **first in Europe**.

Most of the business and rail evidence was banked by the staging session's
global screen and is cited here rather than repeated; what this pass added is
the **licence leg read end to end**, the **boundary layer**, and **live
re-verification** that the endpoints resolve today. `docs/global_country_shortlist.md`
is the evidence trail and wins if the two ever disagree.

**Nothing here is promoted into `docs/data_sources.md` until a city is actually
built** — that file's numbered notice gate is meant to list obligations that
apply, not ones that might.

---

## The one-line answer

**Madrid is ready to build.** Every leg is confirmed live, both licences are
read in full, and the classification, CRS, encoding and boundary are known.
Two new required notices come with it, and one clause needs an owner decision.

**Spain is BESPOKE PER CITY** — the `add-country` cost table puts it with the
US and Canada, not with Mexico or France. Madrid and Barcelona share no parser,
no taxonomy and no portal software. The skill says plainly that *"Korea
outranks Spain"* on cost per marginal city. Spain earns its place on the
**quality of each city's data**, not on how cheaply the second one arrives.

---

## Q1 — Rail: does urban rail exist in data we can read?

**YES, and from the regional authority rather than a catalogue.** The
`add-country` rule is to ask the mapping/transport agency before the Mobility
Database, and it paid off exactly as it did for Japan.

`datos.crtm.es` — Consorcio Regional de Transportes de Madrid, an ArcGIS Hub
site with an enumerable `data.json` (**280 datasets**, retrieved 2026-09-22).

| Dataset | What it carries | Formats |
|---|---|---|
| **Datos abiertos: Elementos de la Red de Metro** | stations, entrances, platforms, vestibules | ArcGIS GeoServices REST |
| **Datos abiertos: Líneas de la Red de Metro** | **line geometry** | ArcGIS GeoServices REST |
| Datos Abiertos: Elementos de la Red de Metro Ligero | the tram/light-rail equivalent | ArcGIS GeoServices REST |
| Datos abiertos: Líneas de la Red de Metro Ligero | line geometry | ArcGIS GeoServices REST |
| GTFS Red de Metro / GTFS Red de Metro Ligero | timetables + shapes | Web page |

**Both halves of question 1 pass.** The skill warns that Korea's station
dataset has 1,099 stations *and no lines at all*, which passes a
stations-only screen and fails this project; Madrid has both, as separate
published layers.

Three consequences worth carrying into Step 4:

- **`accesos` (entrances) is its OWN layer, separate from stations.** The
  `osm-rail` skill's first trap is entrances outnumbering stations; here the
  publisher has already separated them, so the trap is avoided by picking the
  right layer rather than by de-duplicating.
- **Metro, Metro Ligero and Cercanías are separate categories.** This project
  excludes commuter rail (basic `route_type 2`, extended `109`), and here that
  is a choice of *layer* rather than a filter — Cercanías simply is not loaded.
- **A REST API, not a zip.** No `shapes.txt` mode-counting needed; geometry
  arrives as GeoJSON.

**Probed and NOT used:** `crtm.maps.arcgis.com/...`/data returned HTTP 400.
That was a guessed item id, i.e. a fact about the guess, not about CRTM —
recorded so the next session does not re-derive it as a finding.

### ⚠ The rail-source decision is REOPENED — CRTM's feature layers are maintained even though its GTFS is not

`docs/build_briefs/madrid.md` closes this question in favour of OpenStreetMap,
on the finding that CRTM's ArcGIS org holds six GTFS items of which **Metro's
is the stale one** (2025-05-30, against 2026-07-29 for the other four), so
CRTM's own "siempre actualizada" condition rules it out and *"nothing newer
exists to find"*.

**That is correct about GTFS ITEMS and not about CRTM's catalogue.** The
feature services are a different product on a different refresh cycle, and
they are current. Measured 2026-09-22 from `editingInfo.lastEditDate`:

| Product | Last edited | Age today |
|---|---|---|
| GTFS Red de Metro | 2025-05-30 | ~16 months |
| **M4_Red** (`.../M4_Red/FeatureServer`) | **2026-06-05** | **~3.5 months** |
| **M4_Lineas** (`.../M4_Lineas/FeatureServer`) | **2026-04-21** | ~5 months |

`M4_Red` alone carries the whole leg, `copyrightText: © CRTM`:

| Layer | Geometry | n | Carries |
|---|---|---|---|
| `M4_Estaciones` | point | **293** | `DENOMINACION` (name), `CODIGOESTACION`, `CODIGOMUNICIPIO`, `DISTRITO`, `BARRIO`, `FECHAACTUAL` |
| `M4_Tramos` | **polyline** | **560** | **`NUMEROLINEAUSUARIO`** (the line as riders name it, e.g. `10b`), `SENTIDO`, `MUNICIPIO`, `CORONATARIFARIA` |
| `M4_Accesos` | point | 802 | entrances — **already separate**, so the `osm-rail` trap cannot bite |
| `M4_Andenes` / `M4_Vestibulos` | point | 599 / 354 | platforms, vestibules |

Why this looks better than OSM on every axis the brief used to prefer OSM:

- **Operator-authoritative**, so no CDMX-style per-city exception is needed and
  no page notice explaining why rail came from OSM.
- **Native EPSG:25830 — the same CRS as the business data**, so the rail and
  premises legs share a projection with no reprojection step between them.
- **`NUMEROLINEAUSUARIO` is the public line name from the operator**, which
  satisfies the "real public name for label AND legend" invariant without a
  hand-assigned palette. (`10b` also shows Madrid splits Line 10 operationally
  — a naming subtlety OSM's `ref` dedupe to 13 would flatten.)
- **`CODIGOMUNICIPIO` names the municipality per station**, so stations outside
  Madrid can be *named* in `excluded_stations.csv` without sourcing a
  multi-city boundary layer — the Los Angeles pattern, for free. `MUNICIPIO:
  ALCOBENDAS` in the sample confirms the Metro does leave the city.
- **The currency condition reads far better at 3.5 months than at 16**, stated
  alongside `FECHAACTUAL` (20260529), which Madrid's own licence already
  obliges this project to display.

**Carry forward regardless of which source wins:**

- **560 tramos is NOT 560 segments to draw.** `SENTIDO` 1/2 duplicates every
  stretch by direction — CRTM's form of exactly the trap the brief records for
  OSM's 28 relations. Dedupe before counting or drawing.
- **293 is NOT the station count.** OSM gives 236 `station=subway` and GTFS 230
  boardable; 293 needs reconciling in Step 4 (interchanges, out-of-municipality
  stations, possible per-line rows) before any figure is quoted. Do not take
  the largest number because it is the largest — that is the Guadalajara-Spain
  boundary error's shape.
- **The OSM work is not wasted.** It becomes an independent cross-check of a
  kind this project rarely gets: a second, unrelated source agreeing on line
  count and station positions is gate-3-grade corroboration, and gate 3 is
  otherwise UNAVAILABLE for Madrid the way it was for Mexico City.

**Owner decision.** This does not make the brief wrong — its reasoning was
sound on the evidence it enumerated — but the conclusion rested on a scope
("CRTM item" = GTFS item) that the feature services fall outside of.

---

## Q2 — Does Spain record WHERE COMMERCE HAPPENS?

**YES, and in the best of the four shapes: a premises field survey.**

Madrid's *Censo de locales, sus actividades y terrazas de hostelería y
restauración* is a census of **premises**, not of companies, so it sidesteps
the registered-office trap that closed Germany, Austria, Latvia and Slovakia
and that nearly closed France. It is the same shape as Montréal's
`locaux-commerciaux` and Barcelona's `cens de locals`.

Portal: **`datos.madrid.es` is CKAN 2.9.11 at the bare host** — verified live
2026-09-22 via `/api/3/action/status_show`. The earlier "unreachable" reading
was a wrong path (`/egob`).

**Control run, per the skill's nonsense-term rule:** `q=locales` → 26 results,
`q=zzzqqxx` → **0**. The search genuinely filters; result lists can be trusted.

Dataset `200085-0-censo-locales`, **15 resources**; resource `200085-5` is the
locales+actividades join.

| | MEASURED (staging's screen, 2026-09-22) |
|---|---|
| Rows | 225,667 × 47 columns |
| `desc_situacion_local` | 100% — Abierto 159,835 · Cerrado 40,407 · Baja 12,557 · **Uso vivienda 8,486** · Baja Reunificación 4,382 |
| Open + classified + coordinates | 148,814 |
| **Genuinely mappable** | **119,070** — see the coordinate trap below |
| `rotulo` (shop sign) | **100%** on those rows |
| Classification | three levels: `desc_seccion` → `desc_division` → `desc_epigrafe` |
| Districts | 22 of 22 |
| CRS | **EPSG:25830** (ETRS89 / UTM 30N) |
| Encoding / delimiter | **UTF-8 BOM, semicolon** |

Buckets, all three in one file: COMERCIO 45,951 · HOSTELERÍA 27,932 · OTROS
SERVICIOS 14,887 (SERVICIO DE PELUQUERIA 6,012, CENTRO DE ESTETICA 3,058).

### The coordinate trap, and the one open measurement

`coordenada_x_local` / `coordenada_y_local` are **non-empty on every row** and
**29,744 are a literal `0`** — which projected from EPSG:25830 lands in the
Atlantic off West Africa, vanishing silently on a station-radius map rather
than erroring.

**This is the one Madrid number still unsettled**, and it must be settled on
the full download **before any density is published**:

- 19.99% per the evidence trail (29,744 / 148,814)
- 5.85% on a later, explicitly unrepresentative sample

Those may both be arithmetically right over different denominators —
29,744/225,667 is 13.2%. **Reconcile what each is a fraction of before calling
either wrong.**

**And measure the DISTRIBUTION, not just the rate.** Los Angeles' bad
coordinates were 22% of businesses registered since 2020 against ~1% of older
ones, so dropping them would have systematically under-counted new openings.
If Madrid's zeros cluster by district or by `desc_epigrafe`, they cannot simply
be dropped and Q6 below stops being moot. **Settled in step 2, where the full
file is already in hand.**

### Cost per marginal city

**Bespoke.** Barcelona is a different publisher, a different portal
(CAPTCHA-walled to a browser, though its CKAN API is not), a different
classification and a different language. Valencia, Bilbao and Málaga each need
their own register found — Band B, one narrow question each.

---

## Q3 — Portal software

| Portal | Software | Notes |
|---|---|---|
| `datos.madrid.es` | **CKAN 2.9.11** | Bare host. Control-verified |
| `datos.crtm.es` | **ArcGIS Hub** | `data.json` enumerates all 280 datasets; `hub.arcgis.com/api/v3` returned 400 for the query shape tried |

Both speak formats the existing fetch code already handles. No refusals seen
from a plain `urllib` client with a browser user agent.

---

## Q4 — Licences, read in full

Both are **PERMITTED WITH CONDITIONS**. Both are `Ley 37/2007` reuse
licences — Spain's PSI statute — which is the country-level pattern: expect
the same skeleton for Valencia, Bilbao and Málaga, with per-publisher
conditions bolted on.

### Business data — Ayuntamiento de Madrid

Declared in CKAN as `cc-by` / **CC BY 4.0**, `license_url` pointing at the
Spanish legalcode. But CC BY is **not the whole instrument**: the portal's
*Condiciones de uso* adds *Condiciones generales para la modalidad general de
puesta a disposición*, and those are **binding by use** — *"obligan a
cualquier persona y/o empresa que reutilice datos por el mero hecho de hacer
uso de los documentos"*.

> **The stale-link finding.** CRTM's own dataset metadata cites Madrid's notice
> at `datos.madrid.es/egob/catalogo/aviso-legal`, which **404s**. The live pages
> are `/pages/aviso-legal` and `/pages/condiciones-de-uso`. A cited URL that
> 404s is not an absent document — `read-licence` step 2 says a citation is
> unread, and here it was also mis-addressed.

Reuse authorised **for commercial and non-commercial purposes**, expressly
including *"copia, difusión, modificación, adaptación, extracción,
reordenación y combinación"*. Conditions:

1. **Prohibited to distort the sense of the information** (`desnaturalizar`).
2. **Cite the source.** A form is offered: *"Origen de los datos: Ayuntamiento
   de Madrid"*.
3. **State the last-update date** of the reused documents, where the original
   carries one.
4. Must not indicate, insinuate or suggest that the Ayuntamiento participates
   in, sponsors or supports the reuse.
5. Preserve update-date and reuse-condition metadata.
6. **Re-identification of anonymised data is expressly prohibited.**

`/pages/aviso-legal` is a **website disclaimer** — accuracy, availability, no
warranty — written for web pages rather than data (`read-licence` step 4), so
it does not govern dataset reuse. Recorded as read, not as governing.

### Transit data — CRTM

`https://www.crtm.es/licencia-de-uso`, a *licencia-tipo* under Ley 37/2007
art. 4.2(b). Reuse permitted **"para fines comerciales y no comerciales"**,
including modification, adaptation, extraction, reordering and combination.

Share-alike applies to **the data** (*"ofreciendo los datos bajo el mismo tipo
de licencia"*), while **value-added derivative works may be offered under
different licences** — which is what a rendered density map is.

Conditions:

1. **Cite CRTM as the source, "especificando si son datos en bruto o
   explotados"** — a **disclosure-of-transformation** duty, the same family as
   Montréal's *"ou si des interprétations en ont été tirées"* and INEGI's
   §1(g). A bare credit does not satisfy it; this project transforms on every
   map.
2. **"Powered by CRTM"** must appear clearly on digital platforms, **with a
   link to `http://www.crtm.es/`** — prescribed wording.
3. Must not manipulate in bad faith or falsify.
4. Must not use the information to damage CRTM's or the transport system's
   public image, nor alongside illegal acts.
5. Preserve update-date and reuse-condition metadata.
6. Must not indicate, insinuate or suggest CRTM participates in, sponsors or
   supports the product.

> **⚠ OWNER DECISION NEEDED — not resolved here.** Condition: *"Garantizar que
> la información mostrada en su sistema esté siempre actualizada"* — guarantee
> the information shown is **always up to date**. This site is a deliberately
> **pre-rendered static snapshot**, and `components._AS_RECORDED` already tells
> readers the data is as-of a date. Those two are in tension. `add-city` Step
> 0.4 says to raise a clause like this rather than read it generously, so it is
> raised: the options are to state the snapshot date prominently beside the
> CRTM credit, to commit to a refresh cadence, or to ask CRTM. **Do not treat
> the existing as-recorded notice as automatically sufficient.**

### Notices this would add when Madrid is built

Not yet in `docs/data_sources.md` — promote on commit, not before.

| Source | Wording |
|---|---|
| Ayuntamiento de Madrid | *Origen de los datos: Ayuntamiento de Madrid* + the census's last-update date + a statement that this project filtered, grouped and measured the data |
| CRTM | **Powered by CRTM** with a link to `http://www.crtm.es/`, + whether the data is raw or processed (it is processed) |

---

## Q5 — Residence signal

**Stated at source, which is Canada's pattern rather than the US parcel-join
one.** `desc_situacion_local` carries **`Uso vivienda` (8,486)** — premises in
residential use — as a first-class value alongside Abierto/Cerrado/Baja.
Filtering to `Abierto` excludes them without any inference.

That is *better* evidence than a heuristic, and it pairs with the licence's
explicit re-identification ban. `rotulo` being **100% populated** on the
mappable rows means there is no registrant-name fallback of the kind that
would have published ~4,000 individuals' names in Los Angeles — the structural
claim New York can make, available here too. **Still run
`scripts/check_personal_exposure.py` and record the verdict**; the claim is
strong enough to state and not strong enough to skip.

---

## Q6 — Geocoding

**Not needed for Madrid** — the register ships coordinates. It becomes
relevant only if the zero-coordinate rows prove to be *biased* rather than
merely numerous (see Q2).

**ASSERTED, unprobed:** Spain has a national geocoder in **CartoCiudad**
(IGN). Nothing here has tested it, so it carries an ASSERTED label per the
skill's evidence rule and must not be relied on until two methods agree.

---

## Q7 — Classification

**Madrid uses its own three-level scheme, and this is the trap to avoid
repeating from Mexico.** `desc_seccion` → `desc_division` → `desc_epigrafe`.

- It is **not NAICS** and **not SCIAN**, so nothing from the Mexico build
  transfers. `pipeline/taxonomies/scian.py` is as irrelevant here as
  `naics.py` was there — SCIAN retail is 46, NACE-family retail is 47.
- It is **not directly CNAE either**, so the hoped-for shared NACE module with
  Milan's `codice_ateco` does **not** arrive with Madrid. Reassess for
  Barcelona and Valencia separately; do not assume Spain has one taxonomy.
- Expect `pipeline/taxonomies/madrid_epigrafe.py`, built the way Chicago's
  was: pull the full distinct values **with counts, restricted to the rows
  step 2 keeps**, map each to a bucket, and hand-sample the catch-alls.
- **Check for multi-valued cells before counting distinct values.** Three of
  six Canadian registers stored several categories per row with three
  different delimiters, and a `value_counts()` there returns *combinations* —
  Calgary's 1,169 naive categories were really 173.

---

## Q8 — Language and encoding

- **UTF-8 with BOM, semicolon-delimited.** Declare `SOURCE_ENCODING` and the
  delimiter in the city config; a BOM read as data corrupts the first column
  name.
- **Spanish accents throughout** — Hostelería, Peluquería, Chamartín,
  Tetuán, Alcalá. The macro map's TextLayer already carries
  `character_set="auto"`, without which deck.gl silently drops accented glyphs
  to blanks (this is why "Montréal" once rendered as "Montr al"). Madrid's
  own map labels inherit that fix; **no new work, but do not remove it.**
- **Normalise for join keys, never for display.** NFC, map U+2013/U+2014 to
  `-` and U+2018/U+2019 to `'`, compare with `casefold()`. Street names and
  district names are the join risk.
- **Barcelona will be CATALAN, not Spanish** — `cens de locals`, `avís legal`.
  Do not assume Madrid's column vocabulary carries over.

---

## Boundary

`datos.madrid.es` publishes all three, found by searching the catalogue in the
local vocabulary rather than in English:

| Dataset | Formats |
|---|---|
| **Término municipal de Madrid** (the municipal boundary) | KML, ZIP |
| Distritos municipales de Madrid | CSV, KML, TXT, XLSX, ZIP |
| Límites administrativos actuales | JSON, ZIP |

Step 4 needs the **término municipal** for the in-city filter; the **distritos**
layer is what lets an excluded station be named, the way Los Angeles'
multi-city layer does.

**Watch for the CRS.** The business data is EPSG:25830; a boundary published
as KML is EPSG:4326. Surrey's boundary declared 4326 and contained UTM metres,
which silently put it millions of metres away and returned zero containment —
**check the coordinate magnitudes, not the declared CRS.**

---

## What is NOT established

Recorded so the next session does not mistake silence for a pass.

- **The zero-coordinate rate and its distribution** (Q2). The one blocking
  measurement before a density is quoted.
- **The CRTM currency clause** (Q4) — an owner decision.
- **CartoCiudad** — ASSERTED, never probed.
- **Barcelona's general `avís legal`** — still behind an hCaptcha. Its
  per-dataset CC-BY-4.0 is MEASURED from the CKAN API; the general notice is
  UNREAD, and reading it needs a human solving one challenge. Does not block
  Madrid.
- **Valencia, Bilbao, Málaga** — each needs its own register found.
- The **Metro layer schemas** — field names, station-name column, line
  identifiers. That is `add-city` Step 4, not screening.
