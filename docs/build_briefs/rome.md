# Rome — build brief

**Step 0 measured 2026-09-24.** Run `python scripts/brief_check.py rome`
before writing any code. The coordinate method is the `address-join` skill.

---

## The one-line summary

**A premises register joined to Italy's national house-number archive on the
city's own street code — 95.7% at civic level, no geocoder — with one question
the build must answer: the food-and-drink control reads 2.60×.**

---

## Business leg — SUAP's *Elenco delle attività produttive*, MEASURED

| | |
|---|---|
| **File** | `opendata_suap_luglio_2025.csv` — dataset `elenco-delle-attivita-produttive-del-suap-di-roma-capitale-anno-2025` on `dati.comune.roma.it` (CKAN at `/catalog/api/3/action/`). **25,646,982 bytes**, UTF-8 with BOM, comma-separated. Monthly files; **July 2025 is the newest, no 2026 dataset exists** |
| Rows | **168,255** |
| **Establishment key** | **(`STRUTTURA_GESTIONE`, `NUMERO_ESERCIZIO`)** → **155,448** establishments; 12,807 carry two rows (food / non-food split). `NUMERO_ESERCIZIO` alone is NOT unique (37,486 values) — it restarts per municipio |
| Location | `CODICE_VIA` (the city's street code) + `DESCRIZIONE_VIA` + `CIVICO` (95.8%) + `ESP_CIVICO` — **no coordinates** |
| Activity | `DESCRIZIONE_MACRO_ATTIVITA` (99.2%) + `DESCRIZIONE` (100%) + `SPECIALIZZAZIONE` (sparse) |
| `DATA_INIZIO` | **an Excel serial date** (22715 = 1962-03-10) — convert from 1899-12-30. Starts run from the 1950s to **4,146 in January–July 2025**: a live stock, not a flow |
| Names | **None** — the file has no name column at all |

### Taxonomy — `DESCRIZIONE`, with `SPECIALIZZAZIONE` inside the workshops

Distinct establishments, first-cut mapping:

| Bucket | `DESCRIZIONE` | Establishments |
|---|---|---|
| Retail | *Esercizio di Vicinato*, *Medie/Grandi Strutture*, *Vendita di Quotidiani e Periodici*, *Panificatori* | **65,107** |
| Food service | *Somministrazione Alimenti e Bevande*, *Somministrazione (EX ART. 18)* | **19,223** |
| Personal services | *Acconciatori ed Estetisti* | **11,163** |
| **Total** | | **95,493** |

⚠️ **`Laboratorio Artigianale e non` (37,831 rows) is a catch-all with a usable
second level.** `SPECIALIZZAZIONE` is blank on **19,963** of its rows (dropped,
and disclosed); the rest include food — PIZZERIA AL TAGLIO 1,266, ARTIGIANATO
ALIMENTARE 1,000, PASTICCERIA 795, GASTRONOMIA CALDA 693 / FREDDA 470 — and
personal services — ONICOTECNICA 744, LAVANDERIA 617 (+ a gettoni 188),
TINTORIA 255, TATUAGGIO 414 — beside repairs and car work that stay OUT (the
project's NAICS rule). `premises-taxonomy` decides these at build.

**Excluded outright**: *Commercio Elettronico* (9,756 rows — NAICS 454's
twin), *Depositi ed Esposizioni*, *Commercio all'ingrosso*, *Vendita presso il
Domicilio*, *Vendita per Corrispondenza*, vehicle hire and garages, phone
centres, gaming, private clubs (*Circoli Privati*), festivals (*sagre*).

### 🚩 THE BUILD CHECK — owner's decision 2026-09-24

**The food-and-drink control reads 2.60×** — SUAP's 19,223 food-service
establishments against OSM's **7,405** (`restaurant` 3,268 · `cafe` 2,202 ·
`fast_food` 909 · `bar` 453 · `ice_cream` 333 · `pub` 231 · others; node+way
inside the comune). France reads 1.26–1.80×, Prague 1.63×. **A sharper,
restaurant-only control is impossible here**: `SPECIALIZZAZIONE` is blank on
every food-service row, so restaurants cannot be told from bars.

Two plausible causes, neither measured: **the register has no closure date**
(ceased premises may never leave it — Japan's permits share the gap), and
Italy's *bar* is dense and under-tagged in OSM. **Owner's call: Band A, with
this check at build** — compare SUAP with OSM street by street, split the
excess by start year, and then either set an age cut-off or state the
over-count on the page, as Brazil states its catch-all. **This is not
Prague's failure**: Prague's register recorded seats; this one records
premises.

---

## ✅ Coordinates — a JOIN to ANNCSU, 95.7%

| | |
|---|---|
| **File** | ANNCSU's Lazio address list — `https://anncsu.open.agenziaentrate.gov.it/age-inspire/opendata/anncsu/getds.php?INDIR_LAZI` → `indirizzarioLazio20260915.zip`, **24,574,080 bytes** (156.6 MB unzipped), `;`-separated, monthly. ⚠️ Answers **403 to `HEAD`**, 200 to `GET` — probe with a GET |
| Roma rows | `CODICE_ISTAT == "058091"` → **516,337** civic numbers |
| **Join key** | **`CODICE_COMUNALE` = SUAP's `CODICE_VIA`** (440 = Arco degli Acetari in both), + `CIVICO`, + `ESPONENTE`. Strip leading zeros; upper-case the suffix |
| Coordinates | `COORD_X_COMUNE` / `COORD_Y_COMUNE`, **WGS84 longitude / latitude with DECIMAL COMMAS** (`12,4713327`), 100% filled for Roma |

| Tier | Rows | Share |
|---|---|---|
| Exact — street code + civic + suffix | 154,737 | **92.0%** |
| Civic, suffix ignored | 6,157 | 3.7% |
| Street centroid | 7,042 | 4.2% |
| Unmatched | 319 | 0.2% |

**Civic-level 95.7%; every municipio 90.9% or better** (IX and X lowest, VII
highest at 97.7%). The unmatched are mostly **Galleria Termini**, the station's
shopping arcade — premises with no civic number, Taipei's market-stall shape.
⚠️ **ANNCSU's fill varies by comune** — the first comune in the Lazio file has
neither the street code nor coordinates. Check any other Italian city's own
rows before assuming this join.

---

## 🚇 Rail

OSM, counted 2026-09-24: `route=subway` **Metro A** (`#F68B1F`), **Metro B** incl.
the **B1** branch (`#3783C6`), **Metro C** (`#008751`), and **Metromare**
(`#7EB9E6`, the Roma–Lido railway tagged as metro); **87 distinct stop names**
inside the comune. Roma Mobilità's static GTFS answers keyless
(`romamobilita.it/sites/default/files/rome_static_gtfs.zip`) — licence unread;
`osm-rail` puts it first.

🚨 **A `Metro D` relation exists in OSM (colour `#FFBF00`, no ref) for a line
that has not been built** — **Tel Aviv's trap. Exclude it.**

⚠️ **Metromare is a suburban railway under a metro brand** — whether it is
urban rail under the standing rule is an owner call at build.

## Scope

Comune (1,287 km², which includes Ostia). ⚠️ Metro C's eastern terminus,
**Pantano, is in the comune of Monte Compatri** — ASSERTED, check which
stations fall outside at build.

## ✅ Licences — both READ 2026-09-24, both CC BY 4.0

- **SUAP register — PERMITTED WITH CONDITIONS.** The portal's own *Licenze*
  page: *"Tutti i dati contenuti nei Dataset che Roma Capitale pubblica su
  http://dati.comune.roma.it/ sono pubblicati secondo le norme della licenza
  Attribuzione 4.0 Internazionale (CC BY 4.0)"*; version confirmed by each
  resource's `license_type` (`A21_CCBY40`). **MUST DISPLAY**: credit Roma
  Capitale, link the licence, **state that the data were modified**; **MUST NOT
  SAY** anything implying endorsement. No wording prescribed; no act owed
  (`info.opendata@comune.roma.it` invites, never requires, a note). ⚠️ One
  document unread: the old *Linee guida per l'Open Data di Roma Capitale* PDF,
  now behind the city's SSO — not attempted.
- **ANNCSU — PERMITTED WITH CONDITIONS.** `dati.gov.it` declares *"Creative
  Commons Attribuzione 4.0 Internazionale (CC BY 4.0)"*; the INSPIRE record says
  no conditions; the EU HVD regulation (2023/138, Annex 1.2) requires CC BY 4.0
  or looser for addresses. **MUST DISPLAY**: credit Agenzia delle Entrate and
  ISTAT, link the licence, **say the coordinates were used to place other
  data**. No wording prescribed; no act owed.

## Privacy

The register carries **no names**, so nothing personal is published beyond an
activity at a premises address. `check_personal_exposure.py` still runs.

## Region

`"region": "Europe"`.

## Still unknown

- 🚩 **The 2.60× control** — the owner's build check above.
- ⚠️ `Laboratorio Artigianale` specialisations — which join the buckets.
- ⚠️ Metromare in or out; Metro D excluded; which stations fall outside the comune.
- ⚠️ Roma Mobilità GTFS licence (only if it replaces OSM).
- ⚠️ The register's currency — newest file July 2025.

```brief-checks
[
  {
    "id": "rome-suap-file-live",
    "claim": "The SUAP establishment register's July 2025 monthly file is keyless and live - 168,255 rows, the business leg",
    "kind": "http_ok",
    "url": "https://dati.comune.roma.it/catalog/it/dataset/94848d96-0197-486b-b143-485f00285928/resource/3fc5fd67-6ed5-428a-88c4-cf5245f9ec0f/download/opendata_suap_luglio_2025.csv",
    "min_bytes": 3000000
  },
  {
    "id": "rome-suap-licence-cc-by-40",
    "claim": "Roma Capitale's portal publishes every dataset under CC BY 4.0 - attribution, a licence link and a statement of modification",
    "kind": "http_contains",
    "url": "https://dati.comune.roma.it/od/it/legal.page",
    "present": ["Attribuzione 4.0 Internazionale"]
  },
  {
    "id": "rome-anncsu-lazio-live",
    "claim": "ANNCSU's Lazio address list answers a GET (it refuses HEAD) - Roma's 516,337 civic numbers with the municipal street code and WGS84 coordinates, the join target at 95.7%",
    "kind": "http_ok",
    "url": "https://anncsu.open.agenziaentrate.gov.it/age-inspire/opendata/anncsu/getds.php?INDIR_LAZI",
    "min_bytes": 3000000
  },
  {
    "id": "rome-anncsu-licence",
    "claim": "Italy's national catalogue declares ANNCSU's regional address files CC BY 4.0",
    "kind": "http_contains",
    "url": "https://www.dati.gov.it/opendata/api/3/action/package_show?id=stradari-ed-indirizzari-regionali-e-nazionali-da-anncsu",
    "present": ["CC BY 4.0", "INDIR_LAZI"]
  },
  {
    "id": "rome-osm-metro",
    "claim": "OSM carries Rome's metro lines A, B and C as subway relations - the geometry source; Metro D (no ref) is a phantom to exclude",
    "kind": "osm_route_refs",
    "bbox": [41.75, 12.30, 42.00, 12.70],
    "routes": ["subway"],
    "require_refs": {"subway": ["A", "B", "C"]}
  },
  {
    "id": "rome-projected-crs",
    "claim": "Rome projects to UTM 33N",
    "kind": "utm_zone_from_longitude",
    "lon": 12.49,
    "expect": "EPSG:32633"
  }
]
```
