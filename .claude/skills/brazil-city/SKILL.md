---
name: brazil-city
description: Build a Brazilian city on the national CNEFE modules - what São Paulo already built, what each city adds, the traps São Paulo measured, the owner's standing calls, and a sheet for each of the eight cities still to build. Use for any Brazilian city after São Paulo; read with add-city, osm-rail and publish-city, which it does not replace.
---

# Building a Brazilian city

Written 2026-09-24 from São Paulo, Brazil's first city (`DECISIONS.md`, "São
Paulo built on its branch"). Eight more are briefed and their data is cached:
Rio de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza (Regional), Porto
Alegre (Regional), Recife (Regional), Santos (Regional). Brazil is **Mexico's
shape** (`docs/mexico_retrospective.md`): one national source, so the second
city should cost a fraction of the first. It will only if nothing below is
re-derived.

## What already exists - use it, never copy it

| Module | Does | Never |
|---|---|---|
| `pipeline/taxonomies/brazil_cnefe.py` | Classifies `DSC_ESTABELECIMENTO` (free text) into the three buckets: staging's rules, the edit-distance pass, then `WEAK_RULES` (version 2) | Copy rules into a city. A word a city needs goes HERE, as a weak rule, read first (below) |
| `pipeline/countries/brazil.py` | The facts: CSV shape, `COD_ESPECIE`, coordinate levels 1-4 (a whitelist), the lot-aware `address_key` (Brasília's), the dwelling rule | Re-decide a coordinate level per city |
| `pipeline/countries/brazil_register.py` | `build_storefronts(cfg, bbox, polygon)` -> (storefronts, unclassifiable points). Reads every zip in `cfg.CNEFE_ZIPS`, applies the dwelling rule, emits the drift baseline | Write a city step 2 longer than São Paulo's (40 lines) |
| `pipeline/countries/brazil_boundary.py` | `municipios(path)` and `scope_polygon(path, codes, area_km2, crs, label)` - by IBGE code, outer AND inner ways, area-gated | Find a município by NAME (São Paulo is also a state) |
| `scripts/measure_rail_backbone.py` | Spacing and coverage of one OSM line in scope - two parts of the rail test (below) | Decide a commuter line without it |
| `pipeline/sao_paulo/build_check.py` | The unclassifiable share by ring band - the number the page states | Skip it: the share moves with the city |

## What a city adds

```
pipeline/<slug>/config.py            CNEFE_ZIPS (all municípios for a regional page),
                                     IBGE codes, bbox, CRS (UTM 23S or 24S or 25S -
                                     derive from longitude), rail whitelist, gate-3 counts
pipeline/<slug>/fetch_sources.py     the queries below, recording provenance
pipeline/<slug>/boundary.py          scope_polygon() + municipios() for naming
pipeline/<slug>/step1_stations.py    rail - the only genuinely per-city step
pipeline/<slug>/step2_clean_businesses.py   build_storefronts() and two to_csv calls
pipeline/<slug>/step3_map.py         render_heatmap(taxonomy_system="brazil_cnefe")
pipeline/<slug>/build_check.py       São Paulo's, pointed at this config
```

Plus a `REGISTRIES` entry in `scripts/check_personal_exposure.py` (São Paulo's:
no raw file, no trade or owner column, `address=None`), rows in
`docs/data_sources/brazil.md`, and - at the end of the batch - the app entries.

**Write the generic OSM step 1 ONCE, as `pipeline/countries/brazil_rail.py`,
before the second OSM city** (osm-rail's meta-lesson: a lesson in one city's
code does not reach the next). Seven of the eight are OSM-railed. Its shape,
from Rome's and São Paulo's step 1s: a whitelist of RELATION IDS per line (a
`ref` can be shared or absent - Rome's B1 is tagged `B`, the Expresso Aeroporto
has none); every other relation in the cache named in a left-out table with its
reason, else STOP; stops are named `stop*` members, collapsed by name with the
spread printed and capped; gate 3 per line; scope by `scope_polygon`; every
station outside it written to `excluded_stations.csv` naming its município;
the kept relations written for step 3, retagged with the line key.

## Data - already cached for all eight (2026-09-24)

Under `data/<slug>/raw/` (gitignored), with sha256 in the session's manifest:
- **CNEFE zips**, one per município - the regional pages' neighbours included.
- `osm_municipios.json`: every admin_level-8 relation with `IBGE:GEOCODIGO` in
  the bbox, `out geom`.
- `osm_rail.json`: every `route` in `subway|light_rail|monorail|train|tram` in
  the bbox, `out geom; node(r); out tags center;` - **the `node(r)` clause is
  what gives stops their names**; São Paulo's first CPTM probe lacked it and
  every stop came back as `?`.
- Agency layers: Rio's four (metro and VLT stations and lines), Brasília's
  three, Recife's station file, Santos's EMTU stops.

The bboxes are in each city's sheet below; `fetch_sources.py` must carry the
same query strings, so a fresh checkout reproduces the cache.

## Traps São Paulo measured - each cost something

1. **A row is one USE-TYPE at one ADDRESS**, not one business. A shopping
   centre is one pin or a few. Every mapped row has its own
   `COD_UNICO_ENDERECO`; the reader asserts it.
2. **Coordinate level 6 is a census-tract centroid**, not the premises - 13
   rows in São Paulo, 0.2% in Rio. Levels 1-4 are kept by whitelist.
3. **A new keyword never goes into `RULES`.** "The head noun wins" means a word
   added there can RE-ROUTE rows already classified: PET, added to retail,
   took `PET BANHO E TOSA` (pet grooming) and `PET ... CLINICA VETERINARIA` (a
   vet) - 238 rows moved in São Paulo, mostly wrongly. Add it to
   `WEAK_RULES`, which only a still-unmatched row reaches. Before adding, list
   the word's most frequent captures among the unmatched rows and READ them:
   SOFA, FRUTA and PECAS were rejected that way.
4. **A sample cannot measure the words chosen from it.** São Paulo's first 150
   in-ring rows implied the new words would rescue 14.7%; across all in-ring
   rows it was 3.5%. Estimate what is still missing from a FRESH sample,
   drawn after the change with a new seed.
5. **The unreadable share is highest where the map looks.** São Paulo: 40.0%
   of possible storefronts unreadable inside the rings, 30.6% beyond. Station
   areas are commercial districts full of bare trade names. Run `build_check`,
   read a fresh sample, and state the estimate on the page, under **Reading
   the map** (São Paulo's: "the map misses roughly one storefront in ten to
   one in seven within the station rings").
6. **At an address that also holds a dwelling, the pin shows its category** -
   the owner's decision, an LGPD condition, structural. Brasília's addresses
   name a block, not a door; the lot-aware key handles it and is already in
   `brazil.address_key`.
7. **`check_personal_exposure.py`'s person heuristic misfires on upper-case
   Portuguese**: it flags any two words (`SALAO COMERCIAL`, `CACAU SHOW`) -
   17.9% of São Paulo's pins, 0 of them a name by the module's own
   `person_name_in`. Measure with that, and say so in the verdict.
8. **OSM station names carry naming-rights sponsors** (`Saúde - Ultrafarma`,
   `Morumbi - Claro`), the agency's do not - so gate 3 compares COUNTS, and the
   printed name difference is expected, not a failure.
9. **An agency layer can be a status source without being a geometry source.**
   GeoSampa's licence is ambiguous, so São Paulo reads it only for which lines
   operate and how many stations each has (the owner's rule, 2026-09-23).
   Rio's layers are CC BY 4.0 and ARE the geometry - with a notice.
10. **Overpass rail queries time out** on every mirror at once for a large
    bbox (Porto Alegre did); retry later, never trust an empty 200.
11. **Mechanics**: run steps with `PYTHONIOENCODING=utf-8` (relation names
    carry `⇒`); no backslash in a `-c` string (the hook); and after merging two
    appended `app/cities.py` entries, COUNT the cities - Rome's merge fused two
    dicts into one and parsed cleanly.

## The rail test - the owner's standing call for this batch

Commuter or diesel rail is drawn where, inside the scope, it runs like a metro:
**spacing** near metro spacing, **frequency** near metro frequency, and
**coverage** of districts no drawn line reaches. `measure_rail_backbone.py`
prints spacing and coverage (use `--exclude-line` once the line is drawn);
frequency comes from the operator or a cited secondary source. **A clear pass
is drawn and a clear fail left out, each recorded with its numbers; anything
borderline - as Line 9 was, on spacing - goes to the owner in the batch
review.** The precedents are in the tool's docstring.

## The eight - one sheet each

IBGE codes are the file prefixes. bbox is (s, w, n, e), as fetched.

**Rio de Janeiro** - 3304557 · bbox (-23.08, -43.80, -22.75, -43.10) · UTM 23S
- Rail from **the city's own layers** (`pgeo3.rio.rj.gov.br` Transporte_publico,
  CC BY 4.0, PERMITTED WITH CONDITIONS - the credit wording is in the brief):
  metro stations layer 19 (41; line membership as integer flags `flg_linha1/2/4`),
  metro lines 18 (**`flg_ativa` NULL on two of three - never filter on it**),
  VLT stops 9 (31), VLT lines 10 (4). 🚨 **VLT `linha_4` is `Sim`/`Não` where
  `linha_1`-`3` are `1`/`2`** - normalise all four or Line 4 vanishes silently.
  OSM only for colours (VLT colours are CSS names - resolve them).
- Owner: Bonde de Santa Teresa and Trem do Corcovado **out**; Teleférico
  **drawn if operating** (measure status); **SuperVia through the rail test**.
- Its own notice (IPP / DATA.RIO) beside IBGE's.

**Belo Horizonte** - 3106200 · bbox (-20.10, -44.15, -19.75, -43.80) · UTM 23S
- OSM: Metrô BH Linha 1 and **Linha 2 (opened 2026-07-03, two stations,
  weekdays 9h-16h at first) - DRAWN, the page notes the hours** (owner).
- One of the four relations has no colour - source it from the operator.
- `*.pbh.gov.br` refuses curl's default user agent; the agency line file is a
  Linha 1 cross-check only.

**Brasília** - 5300108 (the whole Federal District) · bbox (-16.06, -48.30, -15.49, -47.30) · UTM 23S (centre -47.9; the DF's far west edge crosses into 22S, which does not change the zone)
- Stations: OSM membership, gate 3 against IPEDF's `ESTACOES_METRO` (24 in
  operation; public domain); the 5 under construction are NOT drawn. The agency
  line is ONE MultiLineString for both lines, so per-line geometry is OSM's.
- The block-addressed city: the lot-aware dwelling key applies (decided).
  Asa Sul's unreadable share was 48% at screening - expect a strong skew.

**Salvador** - 2927408 · bbox (-13.05, -38.60, -12.70, -38.25) · UTM 24S
- OSM L1 and L2, **0 of 4 relations coloured**: colours from CCR Metrô Bahia's
  own material, cited (a map PDF is pre-approved if the pages lack them).
- The highest classifiable share in Brazil (42.8%) and the flattest skew.

**Fortaleza (Regional)** - 2304400 + Caucaia 2303709 + Maracanaú 2307650 +
Pacatuba 2309706 · bbox (-4.05, -38.80, -3.68, -38.40) · UTM 24S
- OSM Metrofor: Linha Sul (subway), VLT Parangaba-Mucuripe, **Linha Oeste
  (diesel) - through the rail test**, and a ref `5` relation to identify.
- 41 stations, 31 in Fortaleza (brief). Metrofor's GTFS host has an expired
  certificate - not bypassed.

**Porto Alegre (Regional)** - 4314902 + Canoas 4304606 + Esteio 4307708 +
Sapucaia do Sul 4320008 + São Leopoldo 4318705 + Novo Hamburgo 4313409 · bbox
(-30.30, -51.35, -29.60, -50.95) · UTM 22S
- OSM Trensurb (the network, drawn; the regional scope is its corridor).
  **Aeromóvel NOT drawn** (owner). 23 stations, only 7 in Porto Alegre.

**Recife (Regional)** - 2611606 + Jaboatão dos Guararapes 2607901 + Cabo de
Santo Agostinho 2602902 + Camaragibe 2603454 · bbox (-8.40, -35.15, -7.92, -34.83) · UTM 25S
- OSM Metrô do Recife: Linha Centro 1 and 2, Linha Sul; **the diesel VLTs
  (Curado-Cajueiro Seco, Cajueiro Seco-Cabo) through the rail test** - note
  the regional scope already reaches Cabo because of the second.
- The city's station file (ODbL) is a CROSS-CHECK ONLY: a point from it in
  the published table would make the table a Derivative Database.

**Santos (Regional)** - 3548500 + São Vicente 3551009 · bbox (-24.05, -46.60, -23.85, -46.20) · UTM 23S
- OSM VLT da Baixada Santista L1 and L2; the Bonde Turístico excluded. EMTU's
  CPGSTM layers are a status cross-check only (owner unconfirmed). Santos sits
  about 55 km from São Paulo on the macro map - score the labels together.

## The batch - the owner's process (2026-09-24)

1. Each city to **drafted page text** - no `deploy-verify` per city.
2. The owner approves all nine cities' text at once (São Paulo's is approved;
   its wording is the model - DECISIONS and the session's review file).
3. App side for all nine together: `cities.py` entries in a new **"South
   America"** region (owner), pages numbered in build order, label widths
   measured IN THE APP with Space Grotesk, `check_macro_labels.py` PROBLEMS 0.
   Notice "IBGE (Brazil)" is ONE notice for every Brazilian city.
4. Merge master, re-render on the current renderer (`check_render_current.py`),
   one `deploy-verify` over the batch, fetch, push, reboot, live check.

## How the batch came out (2026-09-24) - for the next Brazilian city

- **The pages were generated in 2026-09**, from one template holding the
  census paragraphs (São Paulo's approved wording, one figure changed per
  city); the 2026-10-01 pass set them as bullets. The page format is now
  `docs/city_page_format.md` (read it before writing any reader-facing text):
  a further city starts from `scaffold_city.py`'s page, never a copy of an
  older one, and fills it as below.
- **The caption reads its dates from `provenance.json`**: the CNEFE zip's
  `last_modified` (IBGE's server date, 2024-05-20 for every file so far - the
  fetch now records it on download) and the rail cache's `retrieved`. It
  replaces the scaffold's `render_data_age` and reads "Snapshot:
  establishments as recorded in the 2022 census (IBGE CNEFE, file(s) dated
  **<date>**); <rail source>, retrieved **<date>**." (São Paulo's code, with
  the city's own `_RAIL` list.)
- **The page's bullets** (São Paulo, Rio de Janeiro, Salvador and the rest;
  approved wording, no read-back):
  - **The lines**: "<N> lines are drawn — **<lines>** — each labeled on the
    map and in the legend", where the lines and stations come from, the rail
    test ("Suburban railways are left out of these maps unless, inside the
    city, they run like a metro. <Line> does: <its spacing and frequency>."),
    what is not drawn and why, and "The map covers the **município of
    <City>**; <stations beyond it> are not counted." A new city's rail
    sentences are its own, so each is a proposal for the drafts file and
    review time (spec, section 6).
  - **The businesses**, verbatim on every Brazilian page: "Businesses come
    from **the national address register of the 2022 census** (CNEFE), kept by
    IBGE, Brazil's statistics agency. Census enumerators walking every street
    recorded each establishment, what it was, and a map point for it. **Read
    it as a 2022 picture, not today's.**"; "IBGE did not classify the
    establishments: each dot's category is this project's reading of the
    enumerator's words, and the names were not checked against any business
    register."; "Where one entry stands for several shops, as in a shopping
    center or a gallery, it is one dot."; "At an address that is also
    someone's home, the dot shows only its category." (Brasília adds one
    bullet on its block addresses.)
  - **Reading the map**: "**About a third of the establishments that might be
    shops, cafés or salons carry a description no rule can read, and are not
    drawn.** Most are brand or trade names with no word saying what they
    sell." with the city's own share from `build_check` ("Almost half" in
    Porto Alegre), the near-station figure where it differs, and the ring
    share in bold ("**About one storefront in five sits within a station
    ring.**").
  - `render_map_help("three business categories (Retail, Food service and
    Personal services)")`.
- **`docs/excluded_categories.md`'s section is built from the step 2 log**:
  the classification table gives the excluded counts, and the unreadable figure
  is `unmatched` plus `catch-all`. Keep São Paulo's shape, under "Excluded in
  one city": `### <City> - the same census, <what is its own>`, then
  **Excluded by what the enumerator wrote**, **Missing rather than excluded**,
  **Shown, but not named**, **One dot for many**, **Stations.** and the
  shared census blocks. The city's own gaps and limits stay in that section,
  never the shared "What is missing" or "Honest limits". Its rows in
  `docs/data_sources/brazil.md` carry the data and its terms; who read a
  licence goes between `<!-- internal -->` markers, as the Brazil rail
  heading there does.
- **Macro-map labels**: São Paulo and Santos sit 6 px apart at South America's
  fitted zoom (3.04), so São Paulo's name runs west, Rio's east and Santos's
  below. A new city near either needs its label scored with all three.
- **The five batch calls** (owner, 2026-09-24): Rio's SuperVia Belford Roxo
  and Santa Cruz out; Fortaleza's Parangaba-Mucuripe VLT out; Fortaleza's and
  Recife's regional scopes kept although Caucaia and Cabo have no drawn
  station; Santos Linha 2 drawn with its hours stated.
