# Barcelona — build brief

**Step 0's answers, banked 2026-09-22.** Read this before `add-city` Step 0,
then run `python scripts/brief_check.py barcelona`. Every claim that can be
re-run is declared in the `brief-checks` block at the end; a failing check is a
brief to correct, never a check to relax.

Spain's country-level facts are in `docs/build_briefs/madrid.md` — read that
first if Madrid has not been built yet.

---

## The one-line summary

Business leg is **complete and clean, but four years old**. Rail leg is **settled in
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
| Rail route relations | **54** — subway **28**, tram **22**, funicular **4** |
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

Tram `T1`–`T6` and funiculars `FM`, `FV` are separate decisions: this project
has drawn tram networks before, but whether Barcelona's belong on a *metro*
density map has not been decided.

---

## Licence — CC-BY-4.0, with one genuine residual

`license_id = "CC-BY-4.0"` comes straight from the CKAN API, per dataset.

⚠️ **The portal's general legal notice has never been read.**
`opendata-ajuntament.barcelona.cat` serves **hCaptcha** on `/en/avis-legal`,
`/ca/avis-legal` and `/es/aviso-legal` alike (*"PLEASE PROVE THAT YOU ARE
HUMAN"*). **This project does not defeat CAPTCHAs**, so the document is
unread — and `read-licence` step 3 exists precisely because a named licence can
sit on top of an incorporated-by-reference document that overrides it, which is
how Philadelphia's prohibition hid.

**This is Barcelona's one true residual.** It is not resolvable by this
session; it needs a human to open one page.

---

## Still unknown — the honest list

- **Which census year** (above) — recency vs completeness, owner's call.
- **TMB account or OSM** (above).
- **The general legal notice**, CAPTCHA-walled.
- Whether trams (T1-T6) and the two funiculars belong on a metro-density
  map. OSM carries them; nobody has decided.
- Whether mall/gallery interiors (`SN_CComercial`, `SN_Galeria`) should be
  excluded from a street-level map. The flags make it possible; nobody has
  decided whether it is right.
- `check_personal_exposure.py` against a Catalan register. `Nom_Local` is a
  trade name, which is the safe field.

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
    "id": "barcelona-utm-zone",
    "claim": "Barcelona at about 2.17E falls in UTM 31N; the source CRS EPSG:25831 is the ETRS89 flavour of that same zone",
    "kind": "utm_zone_from_longitude",
    "lon": 2.1734,
    "expect": "EPSG:32631"
  }
]
```
