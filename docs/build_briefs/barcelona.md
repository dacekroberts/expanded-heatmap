# Barcelona — build brief

**Step 0's answers, banked 2026-09-22.** Read this before `add-city` Step 0,
then run `python scripts/brief_check.py barcelona`. Every claim that can be
re-run is declared in the `brief-checks` block at the end; a failing check is a
brief to correct, never a check to relax.

Spain's country-level facts are in `docs/build_briefs/madrid.md` — read that
first if Madrid has not been built yet.

---

## The one-line summary

Business leg is **complete and clean, but four years old**. Licence **read
and permissive**, with an unusual duty to notify the Council. Rail leg is **settled in
favour of OSM** - TMB is registration-gated, and OSM returns TMB, FGC, TRAM
and the funiculars in one query where the agency route needs four feeds.
One owner decision (which census year), no open probes.

---

## ⚠️ The decision that shapes everything: which census year

The portal publishes the census as **one package with a resource per survey
year**. They are not revisions of each other — each is its own survey.

| Resource | Rows | `Actiu` | Published |
|---|---|---|---|
| `38babeec…` **2024** | **44,000** | 39,980 | 2025-02-14 |
| `99764d55…` **2022** | **66,088** | **58,908** | 2023-09-07 |
| `d5225049…` 2019 | 71,250 | — | 2024-12-05 |
| `e6e7610c…` 2016 | 78,033 | — | 2024-12-05 |

**The 2024 resource is geographically incomplete. Do not use it.** It sums
exactly to its own declared 44,000, so nothing is truncated — but the
shortfall against 2022 is wildly uneven by district:

| District | 2024 | 2022 | Δ |
|---|---|---|---|
| Ciutat Vella | 6,569 | 6,922 | −5% |
| Eixample | 12,321 | 14,673 | −16% |
| Sants-Montjuïc | 5,254 | 6,270 | −16% |
| Gràcia | 4,835 | 5,953 | −19% |
| Sant Martí | 5,548 | 8,159 | −32% |
| Sarrià-Sant Gervasi | 4,407 | 6,752 | −35% |
| Les Corts | 1,732 | 3,183 | −46% |
| Horta-Guinardó | 1,369 | 4,427 | **−69%** |
| Nou Barris | 1,117 | 4,737 | **−76%** |
| Sant Andreu | 848 | 5,012 | **−83%** |

A census that *narrowed its definition* would shrink roughly evenly. This
covers the central districts and barely touches the periphery. The totals trend
confirms it: 78,033 → 71,250 → 66,088 decline gently, then 2024 drops a third.

**This is the dangerous kind of wrong.** A map built on 2024 would show outer
stations as commercially dead — which is exactly what a reader expects anyway,
so nothing would look broken. Corroborating signal: the package's own data
dictionary is headed **"ESTRUCTURA RECURS DE L'ANY 2022"**, i.e. the publisher
documents the 2022 file as the reference one.

### ⚠️ …and 2022 means publishing four-year-old data

If the build uses 2022 — the recommendation — then **the survey year is 2022
and the page will go up in 2026**. That is a disclosure obligation, not a
footnote:

- The project already bars implying data is *"accurate, complete, or timely"*
  (the MTA / WMATA §6 clause, now a cross-city prose rule).
- A station-density map reads as current unless it says otherwise.
- **The city page must state the census year**, in the same place the source
  is credited.

**The real trade is recency against completeness**, and it is the owner's call,
not a probe: 2024 is two years fresher and missing most of four districts;
2022 is complete and four years old. The recommendation here is **2022 with the
vintage disclosed**, because an incomplete map is wrong in a way a reader
cannot detect, while a dated one is honest if it is labelled.

---

## Business leg — `opendata-ajuntament.barcelona.cat`, MEASURED 2026-09-22

- Portal is **CKAN**. Control verified: `zzqqxxnonsense` → **0 results**, a real
  term → 4. The search filters.
- Package: **`cens-locals-planta-baixa-act-economica`** — *Census of premises on
  the ground floor intended for economic activity*
- Licence: **CC-BY-4.0**, declared per dataset via the API
- **The API is not CAPTCHA-walled** even though the human-facing legal notice
  is — see the licence section.
- All the CSV resources are `datastore_active`, so `datastore_search` works and
  no download is needed for counts.

### Schema — 50 fields, and unusually rich

- **Coordinates, both projected and geographic**: `X_UTM_ETRS89` /
  `Y_UTM_ETRS89` **and** `Latitud` / `Longitud`. **0.00% zero or unparseable**
  across all three in a 6,000-row sample — Barcelona does **not** have Madrid's
  `'0.0'` defect. Source CRS is EPSG:25831 (ETRS89 / UTM 31N).
- **Trade name**: `Nom_Local`, **100% populated**.
- **Four-level taxonomy**: `Nom_Principal_Activitat` → `Nom_Sector_Activitat`
  → `Nom_Grup_Activitat` → `Nom_Activitat`, each with a paired `Codi_`. A
  documented local taxonomy — do not force it into NAICS. The code list is a
  **separate package**, `cens-activitats-economiques-class-bcn`.
- **Site-type flags**, which no other city in this project supplies:
  `SN_Mercat` / `Nom_Mercat` (municipal market), `SN_Galeria`, `SN_CComercial`
  (shopping centre), `SN_Eix` / `Nom_Eix` (commercial axis), `SN_Obert24h`,
  `SN_Oci_Nocturn`, `SN_Coworking`, `SN_Servei_Degustacio`. These allow
  excluding mall interiors from a *street*-level density map, which elsewhere
  has to be inferred.
- Geography: 10 districts (`Nom_Districte`), plus barri, census section,
  cadastral reference.

### ⚠️ The vacancy filter is mandatory

`Nom_Principal_Activitat` has two values: **`Actiu`** and **`Sense activitat
Econòmica`**. The second is vacant units — `Nom_Sector_Activitat` then reads
*Locals buits en venda i lloguer*, *Locals buits en lloguer*, *Locals buits en
venda*.

**2022: 66,088 rows → 58,908 `Actiu`.** Filter, or roughly 11% of pins are
empty shopfronts. Barcelona hands you the vacancy signal explicitly, the way
Montréal's `locaux-commerciaux` does; most registers make it be inferred.

---

## Rail leg — TMB is gated, same shape as Madrid

| Feed | Modes | State |
|---|---|---|
| **`mdb-2359` TMB** (L1–L5, L9–L11) | the actual Metro | ⛔ **`"Authentication failed. Authentication parameters missing"`** — `api.tmb.cat` needs `app_id` + `app_key` |
| `mdb-1007` TMB via navitia | — | ⛔ returns **HTML**, not a zip. Broken mirror |
| **`mdb-1856` FGC** | **4 × `route_type=1`**, 14 × rail, **3 × funicular**, 1 bus; 305 stops | ✅ direct, **current** (`2026-09-16`), `shapes.txt` |
| `mdb-1003` TRAM Barcelona | 2 × `route_type=0`, 86 stops | ✅ direct, `shapes.txt` |
| `mdb-1004` TRAM Besòs | 3 × `route_type=0`, 85 stops | ✅ direct, `shapes.txt` |
| `mdb-892` AMB | 139 × `route_type=3` | bus only — not relevant |

**FGC is not the Barcelona Metro.** It is the Catalan government railway
(Generalitat), and its four `route_type=1` routes are the L6/L7/L8-family lines
plus the Vallès and Llobregat services. TMB runs L1–L5 and L9–L11, which is the
majority of the network and all of the dense central coverage. **Without TMB
there is no Barcelona metro map.**

So the same two options Madrid had:

1. **A free TMB developer account** at `api.tmb.cat` — the WMATA / Sevilla
   shape. An owner action; this project does not create accounts.
2. **OSM**, the CDMX and Madrid precedent.

**Recommendation: OSM — and here it is the *better* source, not the fallback.**
Unlike Madrid, option 1 is live rather than closed (TMB's feed exists behind a
free registration). But the agency route needs **four feeds stitched together**
— TMB (gated) + FGC + TRAM + TRAM Besòs — with four licences and four
refresh cadences. OSM returns the whole network in one query.

### OSM validated for Barcelona — MEASURED 2026-09-22

Bbox `41.30,2.03,41.50,2.30`.

| | Count |
|---|---|
| Rail route relations | **54** — subway **28**, tram **20**, funicular **6** |
| Named | **54 / 54** |
| With a `colour` tag | **54 / 54** |
| Flagged construction/proposed | 0 |
| `station=subway` nodes | **181** |

**Operators present: TMB (22 relations), TRAM (22), FGC (10).** So a single OSM
query covers what would otherwise be four separate agency feeds, one of them
behind a login. That is the argument for OSM here.

The invariant that every drawn line gets a real public name and a legend entry
is satisfiable **directly from OSM tags** — 54 of 54 carry both a name and a
colour, with no hand-assigned palette.

⚠️ **14 subway `ref`s, and do NOT collapse them to 11.**

```
L1  L2  L3  L4  L5  L6  L7  L8  L11  L12
L9N  L9S        L10 Nord  L10S
```

L9 and L10 genuinely run as **two disconnected segments each** — that is the
real network, not an OSM artefact, and the segments do not connect. Merging
`L9N` with `L9S` would draw a line through track that does not exist.

**This is the mirror image of Madrid's trap.** There, 28 relations collapse to
13 because they are directional pairs; here, 28 relations give 14 refs that
must stay 14. Same query shape, opposite correct answer — which is why the
rule is *look at the refs*, never *count the relations* and never *assume a
merge*.

### ✅ SETTLED 2026-09-22 — scope is decided by the operator's own `network` tag

**Two counts above were wrong, and the error hid because the TOTAL was right.**
Re-measured with an explicit `route=funicular` query: the split is tram **20**
and funicular **6**, not tram 22 and funicular 4. Two relations sat in the
wrong column and 54 still summed to 54, so nothing flagged it. **A breakdown
that adds up is not a breakdown that is correct** — re-run the parts, not the
total.

**Funiculars are directional pairs — 6 relations, 3 refs.** So Barcelona
carries BOTH traps at once, in opposite directions:

| | Relations | Refs | Rule |
|---|---|---|---|
| Subway | 28 | **14** | **MUST NOT collapse** — L9/L10 segments do not meet |
| Funicular | 6 | **3** | **MUST collapse** — plain directional pairs |
| Tram | 20 | 6 | T1–T6 |

Madrid's trap and the mirror-image trap the section above warns about are the
same city's problem here. Which is exactly why the rule is *look at the refs*
rather than count relations — it survives both.

**The scope test, measured rather than asserted: draw a line if its `network`
tag names a metro network.** The domestic operators have already made this
call and published it:

| Line | Operator | `network` | Drawn |
|---|---|---|---|
| L1–L12 (14 refs) | TMB | `Metro de Barcelona` | ✅ |
| **FM** Montjuïc | **TMB** | **`Metro de Barcelona`** | ✅ |
| **FV** Vallvidrera | **FGC** | **`Metro del Vallès`** | ✅ |
| **FT** Tibidabo | **Barcelona de Serveis Municipals** | **none** | ❌ |
| T1–T6 | TRAM | `Trambaix`, `Trambesòs` | ❌ |

So **16 lines are drawn**: the 14 metro refs plus FM and FV. FM runs from
Paral·lel, an L2/L3 interchange, and TMB publishes it as Metro; FV is route
`FV` in FGC's own GTFS on its Metro del Vallès network. FT is operated by the
municipal *parks and services* company — it is access to the Tibidabo funfair
— and carries no network tag at all. Trams are their own two networks, neither
a metro, so the same test excludes them without a separate judgment.

⚠️ **`route_type=7` alone would have been wrong.** FGC's three GTFS funicular
routes are `FV`, `Cremallera Montserrat` and `Cremallera de Núria` — two rack
railways 50 km and 150 km from Barcelona. The mode tag does not know where the
city ends.

---

## Licence — CC-BY-4.0, with one genuine residual

`license_id = "CC-BY-4.0"` comes straight from the CKAN API, per dataset.

### ✅ RESOLVED 2026-09-22 — read from the Internet Archive

The live pages are hCaptcha-walled (*"PLEASE PROVE THAT YOU ARE HUMAN"*) and
this project does not defeat CAPTCHAs. The notice and the terms it points to
were read instead from the **Internet Archive** — notice at snapshot
**2025-01-18**, terms of use at **2025-03-21**. Full record in
`docs/data_sources.md`.

**It was the Philadelphia shape and it came out the other way.** The legal
notice does incorporate a second document by reference — *"reuse … within the
limits provided for under the **terms of use**"* — and that document **grants**
rather than prohibits: CC-BY 4.0, expressly including *"derived works as a
result of their analysis or study"* and commercial use.

**Four obligations, two of them unusual for this project:**

1. Prescribed wording: **"Source of the data: Barcelona City Council"**
2. **Modifications must be identified at distribution** — density rings and
   storefront filtering are modifications
3. ⚠️ **Users must NOTIFY the Council of every project derived from the
   data.** An affirmative act owed to the publisher, not a line of page text.
   **No built city has required this.**
4. The Council may request reuse statistics

**And Spanish Act 37/2007 Article 8**, incorporated expressly: content may not
be altered, meaning may not be distorted, source must be cited, and
⚠️ **"the most up-to-date data are referred to"** — which bears directly on
the census-year decision above. 2022-because-2024-is-incomplete is
reconcilable with it, but only as a *stated* decision with the year on the
page.

⚠️ **The archive is not the live document**, and these terms reserve the right
to amend themselves with effect on publication. **Before Barcelona goes
public, a human should open the live page and confirm.** That is now a
confirmation rather than an unknown.

---

## Still unknown — the honest list

### Decided 2026-09-22 — owner's calls, so the build is unblocked

- **Census year: 2022**, complete at 66,088 rows (58,908 `Actiu`), **with the
  survey year stated on the page where the source is credited.** An incomplete
  map is wrong in a way a reader cannot detect; a dated one is honest if it is
  labelled. This is also what satisfies Act 37/2007 Art. 8's *"most up-to-date
  data"* wording — as a *stated* decision, not a silent one.
- **Rail: OSM**, and as the better source rather than the fallback.
- **Scope: 16 lines** — the 14 metro refs plus funiculars FM and FV, by the
  operators' own `network` tag. Trams and FT excluded. See above.
- **Mall and gallery interiors: KEPT.** A mall near a station is real
  commercial density a rider can reach, and excluding it would import a
  judgment none of the other 16 cities makes, so cross-city comparison stays
  honest. `SN_CComercial`, `SN_Galeria` and `SN_Mercat` are recorded as
  available-but-unused rather than forgotten — they are the only flags of their
  kind in the project, and a later decision can use them.

### Genuinely still open

- ⚠️ **Notify the Barcelona City Council**, which obligation 3 of the licence
  requires of every derived project. **An affirmative act owed to the
  publisher, not a line of page text, and no built city has needed one.**
  Owner action; pairs with the item below since both pages are CAPTCHA-walled.
- **Re-confirm the terms on the LIVE page** before publishing — they were
  read from a 2025 archive, and they permit their own amendment.
- `check_personal_exposure.py` against a Catalan register. `Nom_Local` is a
  trade name and 100% populated, which is the safe field — so this is expected
  to be clean, but expected is not measured.

```brief-checks
[
  {
    "id": "census-2022-rows",
    "claim": "The 2022 census resource holds 66,088 rows - the complete one, and the one the data dictionary documents",
    "kind": "ckan_rows",
    "domain": "opendata-ajuntament.barcelona.cat/data",
    "resource_id": "99764d55-b1be-4281-b822-4277442cc721",
    "expect": 66088,
    "tolerance": 3000
  },
  {
    "id": "census-2024-is-smaller",
    "claim": "The 2024 resource is GEOGRAPHICALLY INCOMPLETE at 44,000 rows, a third below 2022. If this check fails the city may have republished it - recheck the district breakdown before using it",
    "kind": "ckan_rows",
    "domain": "opendata-ajuntament.barcelona.cat/data",
    "resource_id": "38babeec-5c47-43d3-84e7-b13a4b89004f",
    "expect": 44000,
    "tolerance": 2000
  },
  {
    "id": "census-fields",
    "claim": "The census carries a trade name, BOTH projected and geographic coordinates, the four-level taxonomy, and the site-type flags",
    "kind": "ckan_fields",
    "domain": "opendata-ajuntament.barcelona.cat/data",
    "resource_id": "99764d55-b1be-4281-b822-4277442cc721",
    "present": ["Nom_Local", "X_UTM_ETRS89", "Y_UTM_ETRS89", "Latitud", "Longitud", "Nom_Principal_Activitat", "Nom_Sector_Activitat", "Nom_Grup_Activitat", "Nom_Activitat", "Nom_Districte", "SN_Mercat", "SN_CComercial"],
    "absent": []
  },
  {
    "id": "tmb-is-gated",
    "claim": "TMB's GTFS is registration-gated - api.tmb.cat rejects an unauthenticated fetch. When this check fails, TMB has opened up and the rail decision should be revisited",
    "kind": "endpoint_absent",
    "url": "https://api.tmb.cat/v1/static/datasets/gtfs.zip"
  },
  {
    "id": "fgc-downloads",
    "claim": "FGC's feed downloads direct with no account, ~1.8 MB",
    "kind": "http_ok",
    "url": "https://www.fgc.cat/google/google_transit.zip",
    "min_bytes": 900000
  },
  {
    "id": "fgc-has-rail-and-shapes",
    "claim": "FGC carries shapes.txt so its lines can be drawn, and feed_info.txt so staleness is checkable",
    "kind": "gtfs_files",
    "url": "https://www.fgc.cat/google/google_transit.zip",
    "present": ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt", "shapes.txt", "feed_info.txt"],
    "absent": []
  },
  {
    "id": "fgc-route-types",
    "claim": "FGC is 4 subway + 14 rail + 3 funicular + 1 bus - it is NOT the Barcelona Metro, which is TMB's L1-L5 and L9-L11",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.fgc.cat/google/google_transit.zip",
    "expect": {"1": 4, "2": 14, "7": 3, "3": 1}
  },
  {
    "id": "tram-downloads",
    "claim": "TRAM Barcelona's feed downloads direct with no account",
    "kind": "http_ok",
    "url": "https://opendata.tram.cat/GTFS/zip/TBX.zip",
    "min_bytes": 300000
  },
  {
    "id": "osm-relations-and-refs",
    "claim": "OSM holds 28 subway / 20 tram / 6 funicular route relations, giving 14 / 6 / 3 distinct refs. The SPLIT is what goes wrong: the brief first recorded tram 22 and funicular 4, and 54 still summed to 54. Subway refs must stay 14 (L9/L10 segments do not meet); funicular relations must collapse to 3 (directional pairs)",
    "kind": "osm_route_refs",
    "bbox": [41.30, 2.03, 41.50, 2.30],
    "routes": ["subway", "tram", "funicular"],
    "expect_relations": {"subway": 28, "tram": 20, "funicular": 6},
    "expect_refs": {"subway": 14, "tram": 6, "funicular": 3},
    "require_refs": {
      "subway": ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9N", "L9S", "L10N", "L10S", "L11", "L12"],
      "funicular": ["FM", "FV", "FT"]
    }
  },
  {
    "id": "barcelona-utm-zone",
    "claim": "Barcelona at about 2.17E falls in UTM 31N; the source CRS EPSG:25831 is the ETRS89 flavour of that same zone",
    "kind": "utm_zone_from_longitude",
    "lon": 2.1734,
    "expect": "EPSG:32631"
  },
  {
    "id": "taxonomy-keyed-at-the-right-level",
    "claim": "Altres is 2.6% of active rows at Nom_Activitat, the level this build keys on, against 35% at Nom_Grup_Activitat one level up - which is WHY it keys at the finest level, the opposite of Madrid. The small catch-all still spans several parents, so it is dispatched rather than bucketed",
    "kind": "taxonomy_catchall",
    "domain": "opendata-ajuntament.barcelona.cat/data",
    "resource_id": "99764d55-b1be-4281-b822-4277442cc721",
    "column": "Nom_Activitat",
    "parent_column": "Nom_Grup_Activitat",
    "catchall": ["Altres"],
    "compare": ["Nom_Grup_Activitat"],
    "filters": {"Nom_Principal_Activitat": "Actiu"},
    "max_share": 0.05
  }
]
```
