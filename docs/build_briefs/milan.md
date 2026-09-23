# Milan — build brief

**Step 0 run 2026-09-22.** Every number below was measured against a live
source on that date, not read off a catalogue. Where something is asserted
rather than measured it says so.

Italy has never been built in. The country screen concluded *"nothing to
discover"* about Milan, and that was right about the country and wrong about
the city: **four of the screen's headline claims do not survive measurement**,
and they are the four a build would have leaned on. They are corrected below
rather than quietly replaced, because the pattern matters more than the
values — every one of them came from reading page one of an API.

## The one-line summary

Milan publishes **six disjoint premises registers** on one CKAN portal —
**48,845 rows, no key, no account, CC BY 4.0 on every one** — of which
**98–99% carry valid coordinates and none carries a personal name**. The
registers *are* the classification, so the taxonomy needs none of the portal's
own (unusable) classification fields. Rail comes from **ATM's own GIS layers
plus the agency GTFS**, not OpenStreetMap.

## ⚠️ What the screen recorded, and what is actually true

| Screened claim | Measured 2026-09-22 |
|---|---|
| "`insegna` — the shop sign — the trading name, **which is exactly what this project displays**" | **17.6% populated** on retail, 23.8% and 9.1% on the two food registers, and **absent entirely from three of the six datasets**. Page one reads 41.2%, which is the trap: a register's first page is its oldest rows |
| "`codice_ateco` — ATECO, Italy's NACE implementation" | **7.1% populated.** Unusable as a classification. `ds251` has no ATECO column at all |
| "two classifications and a floor area… **the best business source in the screen**" | Both classifications are unusable. `settore_merceologico` has **66 distinct values** for what should be three, half of that pure case variation, plus 2,759 concatenated rows (`AlimentareNon Alimentare`) |
| "three datasets" | **Six.** The food bucket is split by Milan's commercial plan (`in piano` / `fuori piano`), and there is a separate bakers register |
| "Milan ATM gives subway 5, tram 17 — current feed, **45 MB**" | Subway 5 ✅ and tram 17 ✅ both confirmed. **The feed is 33.05 MiB** (34,656,635 bytes). CKAN's own `size` field says 60,345,749 — also wrong. Neither figure is 45 MB |

**None of this disqualifies Milan.** The city is viable and its coordinates are
the best this project has seen. But a build that trusted the screen would have
keyed a taxonomy on a 7%-populated column and labelled its pins from a
17%-populated one.

## ✅ SETTLED 2026-09-22 — the owner's three calls

| Decision | Call | Where the reasoning is |
|---|---|---|
| **`fuori piano` scope** | **Include, filtering what is nameable** | "The food bucket is three registers" |
| **Pin label** | **`insegna` where it exists, `Ubicazione` otherwise** | "No source has a personal name" |
| **Taxonomy** | **Bucket = source; tooltip from each source's best local field** | "The classification fields are unusable" |

⚠️ **One scope decision is still open: whether the 17 tram routes are drawn.**
See "Rail leg".

---

## Business leg — `dati.comune.milano.it`, MEASURED 2026-09-22

CKAN, no key, no account, no CAPTCHA anywhere on the download path. The search
is real rather than inert — **control-tested**, `zzqqxxnonsense` returns 0
where `esercizi di vicinato` returns 64.

### The six registers

| Package | Rows | Valid coords | Trade name | Bucket |
|---|---|---|---|---|
| `ds49-economia-esercizi-vicinato-sede-fissa` | **28,131** | 27,886 (99.1%) | `insegna` 17.6% | Retail |
| `ds58_economia_pubblici_esercizi_in_piano` | **9,269** | 9,166 (98.9%) | `insegna` 23.8% | Food service |
| `ds62_economia_parrucchieri_estetisti_centri_abbronzatura` | **5,732** | 5,661 (98.8%) | **no column** | Personal services |
| `ds59-economia-pubblici-esercizi-fuori-piano` | **3,799** | 3,502 (92.2%) | `insegna` 9.1% | Food service |
| `ds250-economia-artigianato-settore-alimentare` | **1,471** | 1,444 (98.2%) | **no column** | Food service |
| `ds251-economia-panificatori` | **443** | 434 (98.0%) | **no column** | Retail |
| **Total** | **48,845** | | | |

**Coordinates are the best in this project**: `LONG_X_4326`/`LAT_Y_4326`, EPSG:4326,
**zero corrupt values, zero zeros, and every parsed pair inside the Milan
bbox**. No geocoding leg, and no Los Angeles-style validity problem — the 9%
of LA rows whose longitude was copied from latitude has no analogue here.

### `Codice` is a real primary key, and the registers are DISJOINT

Measured on all five bulk-downloaded registers: **zero duplicate `Codice`
within any source, and zero `Codice` collisions between any pair.** The
prefixes are distinct per register — `EV`/`C-EV`, `PA`/`C-PA`, `AE`/`C-AE`,
`PE`/`C-PE`, `FP`/`C-FP`.

⚠️ **THIS IS WHY THERE IS NO CROSS-SOURCE DEDUPLICATION, and the decision runs
opposite to New York's.** `multi-source-city` says to merge on address AND a
normalised name, because one storefront can hold several licences. That
reasoning does not transfer here, for two measured reasons:

1. **Address cannot be a key at all.** **15,613 of 28,131** `vicinato` rows
   already sit at an address shared with another row in the same register, and
   `vicinato` × `pe_in_piano` share **4,855** addresses. Milan's buildings hold
   many premises; merging on address would delete real businesses wholesale.
2. **Name-based merging is unavailable.** With `insegna` at 17.6% and absent
   from three registers, there is no name to normalise on for most rows.

So the six are treated as what they measurably are: **separate registers of
different activities.** A shop and a bar at the same address are two premises.
The residual risk is a genuine over-count where one business holds two
licences; **under-merging is the safer error** and it should be stated on the
city page rather than hidden.

### The classification fields are unusable — and do not need to be used

| Field | Source | State |
|---|---|---|
| `codice_ateco` | vicinato | **7.1% populated** |
| `settore_merceologico` | vicinato | 66 distinct (34 lowercased), 2,759 concatenated |
| `tipo_eser_pa` | servizi persona | 92 distinct, 5% blank, `Acconciatore` / `ACCONCIATORE` both present |
| `tipo_eser_storico_pe` | pe in piano | **60% blank** |
| `denominazione_pe` | pe in piano | 26% blank, concatenated (`a - Ristorante…similif - Bar caffè e simili`) |
| `settore_storico_pe` | pe fuori piano | **64% blank**, 336 distinct in 3,799 rows |
| `tipo_eser_ae` | artigianato | 33% blank |

**`Area di Competenza` is the one clean field: a single value per dataset, at
100%, in all six.** `VENDITA - In sede fissa`, `SERVIZI ALLA PERSONA`,
`SOMMINISTRAZIONE - In piano`, `SOMMINISTRAZIONE - Fuori piano`,
`ATTIVITA ECONOMICHE - Alimentari`.

✅ **Settled: bucket = source.** This is `multi-source-city`'s *"membership is
often the classification"* in its purest form — do not build a mapping table
where a constant will do. No dirty field decides a bucket.

The tooltip's category line then uses each source's own best field, normalised
for case and split on concatenation, **falling back to the source's own name
when blank** — which it is 26–64% of the time on the food registers.

⚠️ **Note what the bucketing is NOT doing.** `settore_merceologico`'s
alimentare/non-alimentare split is deliberately ignored, because a food *shop*
(grocer, butcher, baker) is **Retail** under the NAICS 445 line every other
city here follows, not Food service. Food service is the *pubblici esercizi* —
consumption on the premises. `ds251` (bakers) is Retail for the same reason.

### ⚠️ `fuori piano` — what it is, and the filter it needs

`pubblici esercizi fuori piano` is the register of premises licensed to serve
food and drink **outside** Milan's commercial plan, under specific statutory
exemptions. Its own columns say what that means:

| Not a public storefront | Rows | Share |
|---|---|---|
| Staff canteen (`Mensa`) | 472 | 12.4% |
| Private club (`club privato`, `circolo`) | 132 | 3.5% |
| Parish club (`parrocchiali`) | 53 | 1.4% |
| **Total identifiable** | **604** | **15.9%** |

✅ **Settled: include the register, filter what is nameable, and say so.**
⚠️ **15.9% is a FLOOR, not the figure.** The `fuori_piano` clause column is
**62.4% blank**, so premises exempted under `art.3 comma 6 lett.*` cannot be
classified from it at all. The city page must say that some non-public
premises remain, in the shape of New York's thin-Retail disclosure — a stated
limitation, not a silent one.

### No source has a personal name — and one has no name at all

**None of the six carries `titolare`, `ragione_sociale`, `nominativo` or any
owner field**, confirmed against live headers for all six. This is the
France/Edmonton pattern: **the publisher already did the stripping**, so the
residence-filter work San Diego, Los Angeles and Philadelphia each needed does
not arise.

✅ **Settled: `insegna` where present, `Ubicazione` (100% on every source)
otherwise.** Because the fallback is an address rather than an owner, **Los
Angeles' failure mode cannot occur** — there is no person to fall back to.

⚠️ **Still run `check_personal_exposure.py`.** `insegna` is free text and a
sole trader can sign a shop with their own name, which is a different risk from
a registrant-name column and is not answered by the absence of one. Add Milan
with `trade="insegna"`, `owner=None`, and expect the heuristics to fire on
Italian street names the way they did on Dublin's — the `name_is_address` flag
added for Dublin applies to the ~80% of rows using the fallback.

---

## Rail leg — ATM's own layers plus the agency GTFS, NOT OpenStreetMap

Both of `osm-rail`'s first two steps pass, so OSM is not justified and is not
used. **This is the check Dublin's brief skipped**, one city earlier.

### Source 1 — ATM GIS layers, for the metro

Same portal, CC-BY, publisher AMAT (Agenzia Mobilità Ambiente Territorio), all
**CRS84 / EPSG:4326**:

| Package | What | Records | Geometry |
|---|---|---|---|
| **`ds535_atm-fermate-linee-metropolitane`** | metro stations | **130** | Point |
| **`ds539_atm-percorsi-linee-metropolitane`** | metro alignments | **31** | LineString |
| `ds533_atm-composizione-percorsi-linee-metropolitane` | station→route join | 650 | none |

Stations per line, from `ds533`: **M1 38 · M2 35 · M3 21 · M4 21 · M5 19**
(union 130, so only 4 rows are shared).

The longest variant per line, which is the one to draw:

```
M1  percorso 100035  123 verts  21.16 km   Sesto 1 Maggio FS - Rho Fieramilano
M2  percorso 100053  354 verts  33.25 km   Assago Milanofiori Forum - Gessate
M3  percorso 100081  349 verts  15.63 km   Comasina - San Donato
M4  percorso 100164  110 verts  14.16 km   San Cristoforo - Linate Aeroporto
M5  percorso 100084  129 verts  12.18 km   Bignami - San Siro Stadio
```

⚠️ **`id_ferm` is a STRING in `ds533` and an INT in `ds535`.** A raw join gives
**130 of 130 misses** — a total failure that looks like a scope problem. Cast
before joining; after the cast there are zero orphans either way.

### Source 2 — the agency GTFS, for colours and tram geometry

**`https://dati.comune.milano.it/gtfs.zip`** — a stable short URL documented in
the dataset's own notes, byte-identical to the long resource URL (sha256
matched). HTTP 200, `application/zip`, magic `PK\x03\x04`, **34,656,635 bytes**.

`route_type` distribution, **extended TPEG set explicitly checked**:
**`0` → 17 trams · `1` → 5 metro · `3` → 144 bus.** No 3- or 4-digit values at
all, so the extended-route-type trap that reported Berlin and Stockholm as
railless does not apply here. The four trolleybus routes are plain `3`.

⚠️ **THERE IS NO `feed_end_date`.** `feed_info.txt` carries
`feed_start_date 20260914` and two **non-standard** columns instead:
`surface_end_date 20261002` (trams and buses) and `mm_end_date 20261015`
(metro). **A check that greps for `feed_end_date` will find nothing and must
not read that as expiry.** Freshness is therefore checked against
`calendar_dates.txt`, which holds all service (`calendar.txt` is a header row
with **zero records**): 2,768 rows over **36 dates, 20260914 → 20261019**.

### Colours — half free, half this project's problem

`route_color` is populated **only for the five metro lines**, and
`route_text_color` is **empty on all 166 routes**:

| Line | `route_color` | Official name |
|---|---|---|
| M1 | `#ff0000` | linea rossa |
| M2 | `#73ff01` | linea verde |
| M3 | `#fcff01` | linea gialla |
| M4 | `#0000ee` | linea blu |
| M5 | `#c876b1` | linea lilla |

These are the agency's own, so the project's rule keeps them **even if they
score badly** against the category pins — unlike Dublin, where `route_color`
was empty and the palette was therefore this project's to choose. ⚠️ **Score
them at build time anyway and record the numbers**: `#fcff01` yellow and
`#73ff01` green are both bright and unmixed, and M3's yellow has no
`route_text_color` to pair with, so a contrast rule for its label is this
project's to supply.

⚠️ **`route_short_name` is `"1"`…`"5"`, not `"M1"`…`"M5"`.** The `M` lives only
in `route_id` and `route_long_name`. **The on-map label must be built, not
copied** — and every drawn line needs its real public name.

### Three traps, each measured

1. **`stops.txt` cannot select metro stations.** 4,897 stops with
   `location_type` **empty on all of them** and `parent_station` **empty on all
   of them** — completely flat. **532** stop names match `m1`–`m5`, because
   tram and bus stops are named after the metro station they serve (`bonola m1`
   appears three times). Use `ds535`'s 130 clean points.
2. **`ds535`'s 130 features are not 130 physical stations, and interchanges are
   modelled two incompatible ways.** Four are a single point carrying both
   lines (`CENTRALE FS` `"2,3"`, `GARIBALDI FS` `"2,5"`, `ZARA` `"3,5"`,
   `SAN BABILA` `"1,4"`); the rest are two points needing three different
   rules — a ` M<n>` suffix (`DUOMO M3`/`DUOMO M1`, 111 m), a spelling
   variant (`SAN AMBROGIO`/`S.AMBROGIO`, 22 m) and a name alias
   (`LOTTO M5`/`LOTTO FIERAMILANOCITY`, 71 m). Suffix-strip alone gives 127;
   with the two aliases, **~125 physical stations**. ⚠️ **A distance threshold
   is wrong in both directions**: `WAGNER`↔`BUONARROTI` at 277 m and
   `DUOMO`↔`CORDUSIO` at 259 m are genuinely different stations. This is the
   per-city collapse `osm-rail` says is never inheritable, and
   `pipeline/stations.py`'s spacing gate must be run over the result.
3. **The GIS tram layer is missing a line the GTFS has.** `ds538` carries
   **16** tram lines; the GTFS carries **17** — **tram 27 (`fontana -
   ungheria`) is absent from `ds538` entirely**, and the difference is one-way.
   Drawing trams from `ds538` would silently lose a line, which is exactly
   Guadalajara's Línea 4. **Take tram geometry from the GTFS `shapes.txt`**, or
   add a raising check of `ds538` against `routes.txt`.

### Suburban rail is cleanly separate — nothing to exclude

The ATM feed contains **one agency**, **no `route_type=2`**, and **zero** stop
or route names matching `trenord|passante|ferrovi|S1|S2|S5|S13|regional`. The
S-line network lives in a separate, older pair (`ds80`, `ds81`) which is
excluded simply by not fetching it — and which could not be published anyway,
because every row carries the publisher's own caveat **"Dati indicativi non
ufficiali"** (indicative, unofficial data).

### ⚠️ STILL OPEN — are the 17 tram routes drawn?

The one scope decision not yet taken.

- **Metro only (M1–M5)** — ~125 stations, five lines, all with agency colours.
  Consistent with **Barcelona**, which excluded its T1–T6 trams, and with
  **Toronto**, which excluded streetcars while keeping subway and LRT.
- **Metro + trams** — 22 drawn lines and a dense street-running network whose
  stops sit one or two blocks apart. That is San Francisco's Muni Metro shape,
  which needed `docs/sub_transit_line_filters.md`: central stops kept,
  terminals kept, surface stops thinned to a target spacing, interchanges
  force-kept. It also needs 17 invented colours, since `route_color` is empty
  for every tram.

**Recommendation: metro only for the first build**, with the trams recorded as
a costed extension rather than a discard — the geometry is in the GTFS and the
decision is reversible.

---

## Boundary leg — one polygon, no dissolve

**`ds2841-confini-amministrativi-del-comune-di-milano`**, GeoJSON, CC-BY.

- **1 feature, 1 Polygon, EPSG:4326**, measuring **181.8 km²** against Milan's
  ~181.8 km² comune area.
- No multipart problem (Dublin's layer had 90 parts), no dissolve needed, no
  async download endpoint (the Surrey trap does not apply).

**Projected CRS: EPSG:32632, UTM zone 32N**, derived from Milan's longitude
(~9.19, inside the 6–12 band) and independently the zone a third-party ArcGIS
copy of the metro layer uses. This is an ordinary per-city UTM — Italy's
national grids (Monte Mario, EPSG:3003/3004) are **not** used, because unlike
Dublin's ITM no source publishes in them.

---

## Licence — CC BY 4.0, PERMITTED WITH CONDITIONS

Established by the `licence-read` agent, which opened 15 documents.

**The version was not visible where anyone would look.** CKAN's
`package_show` reports `license_id: cc-by` with **no version at all**, and its
`license_url` points at opendefinition's version-less register entry. Three
independent sources give **4.0**: the portal's **DCAT-AP_IT** serialisation
(`owl:versionInfo "4.0"`, `dct:license <…/licenses/by/4.0/>`), the portal
footer, and the national catalogue `dati.gov.it`.

⚠️ **This is why `brief_check.py` gained a `http_contains` kind.** A licence
claim pinned to `package_show` would keep passing while the version — which
decides the attribution obligations — went unwatched. The check below reads the
`.ttl`.

**All six datasets are CC BY 4.0**, verified per dataset rather than
generalised. ⚠️ **Do not generalise to the portal**: neighbouring datasets in
the same searches carry `other-at` and `cc-zero`, so any further Milan dataset
needs its own `package_show`.

Two decoys, both real and both about something else: the portal footer's
`CC-BY 3.0` link is attribution the portal owes **upstream** for its theme
icons, and `comune.milano.it`'s Note Legali licenses **the institutional
website** under CC BY 3.0 IT — that page names *"il sito ufficiale"* and
self-defers with *"salvo dove è diversamente specificato"*.

### MUST DISPLAY

**No wording is prescribed**, so CC BY 4.0 §3(a)(2) applies — "any reasonable
manner". The components are still mandatory, and one of them is work:

> **"indicate if You modified the Licensed Material and retain an indication of
> any previous modifications"** — CC BY 4.0 §3(a)(1)

**A bare "Source: Comune di Milano" does not satisfy the licence**, because
this project filters, re-buckets and derives densities. That is the
disclosure-of-transformation family for the **sixth** time, after Montréal,
INEGI, Madrid, Barcelona and Tailte Éireann. Note it is the *weaker* form: CC
BY 4.0 requires disclosing **modification**, and says nothing about
interpretation, where Montréal's licence names both.

Rights holder for attribution: **Comune di Milano** (`dct:rightsHolder`,
`c_f205`).

### MUST DO — nothing

**No affirmative act is owed.** The Italian trigger phrases (`informare`,
`comunicare al`, `registraz`, `previa autorizzazione`, `obbligo di`) return
**zero** across the dataset page and the portal's `/about`. A channel exists if
the project ever wants to notify voluntarily —
**`opendatamilano@comune.milano.it`**, consistent across three sources.

### MUST NOT SAY

- Nothing implying affiliation or endorsement (CC BY 4.0 §2(a)(5)(C)).
- ⚠️ **Prudential, not an obligation:** the publisher's own description warns
  the register is not internally consistent — *"le informazioni contenute nel
  dataset non sono necessariamente omogenee, perché riferite al momento
  dell'ultima comunicazione"*. Nothing forbids calling the data current; the
  publisher's own statement makes it unwise.

⚠️ **The rail sources' licence is recorded as CC-BY but has NOT been read to
this project's standard.** `ds535`, `ds539` and the GTFS are a separate
`read-licence` job before the deploy gate.

---

## Still unknown — the honest list

1. **Whether the trams are drawn.** The one open scope decision; metro-only
   recommended above.
2. **The rail sources' licence**, unread. `ds535`/`ds539`/`gtfs.zip` declare
   CC-BY on CKAN, but that is a citation, not a reading — and the version
   question above shows why that distinction bites on this portal.
3. **The true non-storefront share of `fuori piano`.** 15.9% is a floor; 62.4%
   of the clause column is blank and cannot be classified.
4. **Whether `insegna` ever carries a person's name.** Structurally a trade
   name; free text in practice. `check_personal_exposure.py` is the measure and
   has not been run, because the city is not built.
5. **The exact physical station count.** ~125 after the alias collapse, against
   130 raw features. It needs the per-city collapse written and the shared
   spacing gate run over it.
6. **Whether the metro colours clear `map_common`'s CIE76 separation check.**
   They are agency colours so they are kept either way, but M3's `#fcff01` has
   no `route_text_color` and its label contrast is this project's to solve.

---

```brief-checks
[
  {
    "id": "milan-retail-register",
    "claim": "The retail register holds 28,131 rows on CKAN with no key. This is the largest of the six and the only one carrying `insegna` at any useful rate",
    "kind": "ckan_rows",
    "domain": "dati.comune.milano.it",
    "resource_id": "95ef10f2-c825-451d-aa3d-6ff4ed7fd267",
    "expect": 28131,
    "tolerance": 1500
  },
  {
    "id": "milan-retail-fields",
    "claim": "The retail register carries the address, the coordinates, the trade name and BOTH classification fields - the last two are present but nearly empty, which is the point: presence is not population",
    "kind": "ckan_fields",
    "domain": "dati.comune.milano.it",
    "resource_id": "95ef10f2-c825-451d-aa3d-6ff4ed7fd267",
    "present": ["Codice", "Ubicazione", "Area di Competenza", "DescrizioneVia", "Civico", "insegna", "codice_ateco", "settore_merceologico", "LONG_X_4326", "LAT_Y_4326", "MUNICIPIO", "NIL"],
    "absent": []
  },
  {
    "id": "milan-food-in-piano",
    "claim": "The in-plan bars and restaurants register holds 9,269 rows. With `fuori piano` and the artisan food register it is the whole Food service bucket",
    "kind": "ckan_rows",
    "domain": "dati.comune.milano.it",
    "resource_id": "d70a4002-af24-42db-9ace-00d4a102ccb8",
    "expect": 9269,
    "tolerance": 600
  },
  {
    "id": "milan-personal-services",
    "claim": "The personal-services register holds 5,732 rows and carries NO name column of any kind - the bucket the country screen could not confirm existed",
    "kind": "ckan_rows",
    "domain": "dati.comune.milano.it",
    "resource_id": "1f7244e8-a6ae-4777-a09f-06a325338be8",
    "expect": 5732,
    "tolerance": 400
  },
  {
    "id": "milan-licence-is-cc-by-4",
    "claim": "The retail dataset is CC BY 4.0. THIS CHECK READS THE DCAT .ttl AND NOT package_show, because CKAN reports `cc-by` with NO VERSION - a claim pinned to package_show cannot see the thing it guards. It also asserts no NonCommercial or NoDerivatives clause has appeared",
    "kind": "http_contains",
    "url": "https://dati.comune.milano.it/dataset/ds49-economia-esercizi-vicinato-sede-fissa.ttl",
    "present": ["creativecommons.org/licenses/by/4.0"],
    "absent": ["licenses/by-nc", "licenses/by-nd"]
  },
  {
    "id": "milan-boundary",
    "claim": "The comune boundary is ONE polygon measuring 181.8 km2 in UTM 32N - no multipart dissolve needed, unlike Dublin's 90-part layer",
    "kind": "geojson_area_km2",
    "url": "https://dati.comune.milano.it/dataset/ds2841-confini-amministrativi-del-comune-di-milano/resource/f56cb432-83e6-48de-ae30-d39b4be61e85/download",
    "crs": "EPSG:32632",
    "min": 175.0,
    "max": 190.0
  },
  {
    "id": "milan-crs",
    "claim": "Milan's projected CRS is UTM zone 32N, derived from its longitude and not copied. Italy's national grids are NOT used, because no source publishes in them",
    "kind": "utm_zone_from_longitude",
    "lon": 9.19,
    "expect": "EPSG:32632"
  },
  {
    "id": "atm-gtfs-downloads",
    "claim": "ATM's GTFS downloads from the stable short URL with no key, ~33 MiB. The screen recorded 45 MB and CKAN's own size field says 60 MB; both are wrong",
    "kind": "http_ok",
    "url": "https://dati.comune.milano.it/gtfs.zip",
    "min_bytes": 25000000,
    "content_type_contains": "zip"
  },
  {
    "id": "atm-gtfs-has-shapes",
    "claim": "The feed carries shapes.txt, which is where tram geometry must come from because the GIS tram layer is missing tram 27",
    "kind": "gtfs_files",
    "url": "https://dati.comune.milano.it/gtfs.zip",
    "present": ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt", "shapes.txt", "feed_info.txt", "calendar_dates.txt"],
    "absent": []
  },
  {
    "id": "atm-gtfs-is-current",
    "claim": "Freshness is read from calendar_dates, NOT feed_info: AMAT publishes no feed_end_date and substitutes non-standard surface_end_date and mm_end_date columns, so a feed_end_date check would find nothing and must not read that as expiry",
    "kind": "gtfs_calendar_window",
    "url": "https://dati.comune.milano.it/gtfs.zip",
    "expect": "current"
  },
  {
    "id": "atm-route-types",
    "claim": "5 metro + 17 tram + 144 bus, in the BASIC route_type set - no 3- or 4-digit TPEG values anywhere, so the extended-route-type trap that reported Berlin and Stockholm railless does not apply here",
    "kind": "gtfs_route_type_counts",
    "url": "https://dati.comune.milano.it/gtfs.zip",
    "expect": {"0": 17, "1": 5, "3": 144}
  },
  {
    "id": "atm-metro-stations-layer",
    "claim": "ATM's metro station layer resolves and is ~24 KB of GeoJSON. 130 features, which are NOT 130 physical stations - see the collapse trap",
    "kind": "http_ok",
    "url": "https://dati.comune.milano.it/dataset/b7344a8f-0ef5-424b-a902-f7f06e32dd67/resource/dd6a770a-b321-44f0-b58c-9725d84409bb/download/tpl_metrofermate.geojson",
    "min_bytes": 15000
  },
  {
    "id": "atm-metro-lines-layer",
    "claim": "ATM's metro ALIGNMENT layer resolves - 31 LineStrings, the geometry the five metro lines are drawn from. Station points and line geometry are two separate datasets here, and a source with one and not the other fails this project",
    "kind": "http_ok",
    "url": "https://dati.comune.milano.it/dataset/5d24ff16-26c7-4f3a-98dd-b5b8f0b65003/resource/df024fd8-9c4e-4e22-a39e-7e91295b7a7b/download/tpl_metropercorsi.geojson",
    "min_bytes": 150000
  }
]
```
