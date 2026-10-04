# Geneva (Regional) - build brief

**Band A, owner-approved 2026-10-04** (`docs/decisions_drafts/staging.md`,
"The probe wave's first results: Korea and Europe banded; Korean regional
expansions marked (owner)", then "The paused wave's results banded; probes
stay stopped (owner)": the narrow indemnity accepted, ge.ch's website terms
read as the website's only, **regional scope**). Licence read 2026-10-04
(same file, "Geneva's REG read, and the second group outside Europe
screened"). Brief written 2026-10-04 from the cached register and TPG's own
line pages. Run `python scripts/brief_check.py geneva` before writing any
code.

Switzerland's second city: read `tram-city` (its Zurich sheet),
`docs/build_briefs/zurich.md` and `docs/data_sources/switzerland.md` first.
Skills: `add-city`, `scaffold-city`, `premises-taxonomy` (NOGA, a new
module), `osm-rail`, `publish-city`. **Copy Zurich's pipeline** for the tram
leg and the LV95 handling; the business leg is new.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | TPG trams 12, 14, 15, 17, 18; no metro. Léman Express (CEVA) is commuter rail, out as everywhere, and named on the page |
| **`coverage`** | **`full`** | All three buckets from one register |
| **Scope** | **Regional: the 12 Swiss communes the trams serve**, `SCOPE = "regional"` | Owner, 2026-10-04. The register is cantonal, so the scope can follow the lines (Zurich's could not) |
| **Page name** | **"Geneva (Regional)"**, slug `geneva` | Lille's and Vancouver's pattern: a regional page carries "(Regional)", the slug stays the plain city |
| **Lines drawn** | **12, 14, 15, 17, 18**, each to its end | TPG's line list, read 2026-10-04 |
| **Tram 17 into France** | **Drawn to Annemasse, its 4 French stops listed as outside, no rings** | Florence's T1 precedent (the kit's call 17): a line's end beyond the business source, not a stub (22 of 26 stops inside) |
| **Rings** | **By the spacing rule** (`tram-city` section 3); halved expected | Urban tram spacing; measure the median gap on the stations drawn |
| **Projected CRS** | **EPSG:2056** (LV95) | The register's `E`/`N` are already LV95 (extent 2,486,212-2,512,815 E, 1,110,446-1,135,444 N), Zurich's reason; the derived UTM zone is EPSG:32632 |
| **Records** | **Establishment rows only** (`TYPE_REG` = Etablissement), company rows as a disclosed gap | The probe's proposal; the gap is measured below and goes to the owner with the build |
| **Region** | `"Europe"`, country `"Switzerland"` | |

**Calls for the owner at build** (each with its precedent):
1. **Company rows with no establishment row** (1,848 in scope, below):
   leave out, disclosed. A company row carries no premises type, so the
   home-based filter cannot reach it.
2. **Sole traders' names** (1,498 kept establishments belong to an
   "Entreprise individuelle"): withhold the name where it reads as the
   registrant's own, as Tucson (the kit's call 15) and Kansas City (call 11).
3. **The ambiguous NOGA codes** listed under Classification.

---

## The one-line summary

**The canton's business register (REG), cached: 5,885 storefront
establishments in the 12 tram communes after the home-based and itinerant
rows are dropped, every one with an LV95 point. TPG's five tram lines, 85
stops (81 in Switzerland). SITG Level A terms, the narrow indemnity accepted.
The work is a NOGA taxonomy, the name rule and the source line.**

---

## Scope - the 12 communes, from TPG's own stop names

TPG's line pages (`tpg.ch/fr/lignes/<n>`, read by curl 2026-10-04, timetable
valid 2025-12-14 to 2026-12-12) name each stop "Commune, Stop". Distinct stop
names across both directions of all five lines, grouped by commune (Lancy's
stops carry Grand-Lancy, Petit-Lancy, Lancy-Bachet and Lancy-Pont-Rouge;
Genève's include Genève-Eaux-Vives, gare):

| Commune | Tram stops | Lines | Food | Retail | Personal | Kept establishments |
|---|---|---|---|---|---|---|
| Genève (Ville) | 31 | all five | 1,370 | 1,921 | 765 | 4,056 |
| Lancy | 13 | 12, 14, 15, 17, 18 | 77 | 164 | 50 | 291 |
| Meyrin | 9 | 14, 18 | 88 | 131 | 35 | 254 |
| Carouge | 5 | 12, 15, 17, 18 | 127 | 218 | 92 | 437 |
| Bernex | 5 | 14 | 12 | 30 | 11 | 53 |
| Vernier | 4 | 14, 18 | 82 | 215 | 48 | 345 |
| Plan-les-Ouates | 3 | 15, 18 | 31 | 53 | 20 | 104 |
| Chêne-Bougeries | 3 | 12, 17 | 15 | 23 | 12 | 50 |
| Chêne-Bourg | 2 | 12, 17 | 28 | 48 | 23 | 99 |
| Thônex | 2 | 12, 17 | 27 | 56 | 23 | 106 |
| Onex | 2 | 14 | 21 | 32 | 18 | 71 |
| Confignon | 2 | 14 | 4 | 8 | 7 | 19 |
| **12 communes** | **81** | | **1,882** | **2,899** | **1,104** | **5,885** |

- **France, outside the scope:** tram 17's Gaillard (2), Ambilly (1) and
  Annemasse (1) stops. Drawn, listed as outside, no rings: the register
  holds no French business.
- **Not served:** Le Grand-Saconnex (the probe's desk list named it; tram 15
  ends at Nations, in Genève). Its 85 storefront establishments stay off.
  Confignon is served (tram 14) and the probe had missed it.
- **The stop prefix is TPG's label, not a polygon.** Step 1 assigns each stop
  to a commune by the commune polygon, and step 2 scopes businesses by
  polygon (or `PHYS_COMMUNE`, cross-checked). The Ville appears in the
  register as five labels: Genève, Genève-Cité, Genève-Eaux-Vives,
  Genève-Petit-Saconnex, Genève-Plainpalais.
- The commune boundary source needs its own row in
  `docs/data_sources/switzerland.md` (SITG's commune layer is Level A under
  the same conditions; a source not in this brief goes to the owner first).

---

## Business leg - Répertoire des entreprises du canton de Genève (REG)

| | |
|---|---|
| **Source** | SITG dataset `REG_ENTREPRISE_ETABLISSEMENT` (`https://sitg.ge.ch/donnees/reg-entreprise-etablissement`), contributor Département de l'économie et de l'emploi (OCIRT); opendata.swiss `repertoire-des-entreprises-reg1` |
| **File** | `data/geneva/raw/REG_ENTREPRISE_ETABLISSEMENT-CSV.zip` (cached, 11,344,581 bytes, sha256 `45aff219...fa3d616`): `REG_ENTREPRISE_ETABLISSEMENT.csv` (38,545,834 bytes, UTF-8 with BOM, `;`), the CU PDF, the dataset PDF and `DOC/Informations_date.txt` |
| **Data date** | Zip created 2026-10-04 07:32; extracted from SITG's geodatabase the Friday evening before (2026-10-02). The source line carries the extract date of the file the build uses |
| **Also served** | FeatureServer `vector.sitg.ge.ch/arcgis/rest/services/REG_ENTREPRISE_ETABLISSEMENT/FeatureServer/0` (point layer, maxRecordCount 4,000, no `editingInfo`) |
| **Cadence** | Daily. Currency passes: every row is `STATUT_REG` "En activité" |
| **Rows** | **100,588**: 63,224 Entreprise, 37,364 Etablissement. Every row has a point (`E`, `N`, LV95) |
| **Fetch** | `pipeline/geneva/fetch_sources.py` takes the CSV zip from `ge.ch/sitg/geodata/SITG/OPENDATA/` (the brief's source, pre-permitted). A step never fetches |

### Fields (35)

`OBJECTID`, `TYPE_REG`, `ID_ETABLISSEMENT`, `NOM`, `UNITE_LOCALE`,
`COMPLEMENT_LOCALI`, `STATUT_REG`, `IMMAT_DT`, `TYPE_LOCAL`, `CODE_NOGA`
(6-digit NOGA 2008 on every row), `BRANCHE` (its label), `ACTIVITE_DETAIL`,
`TAILLE`, `RAISON_SOC_PARENT`, `ID_ENTREPRISE`, `TEL_PRINCIPAL`,
`TEL_SECONDAIRE`, `FAX`, `EMAIL`, `SITE_INTERNET`, `PHYS_RUE`,
`PHYS_NUMRUE`, `PHYS_NPA`, `PHYS_LOCALITE`, `PHYS_COMMUNE`, `IDPADR`,
`ADRESSE`, `NUM_IDE`, `RAISON_SOCIALE`, `NATURE_JURID`, `SIEGE_CANTON`,
`SIEGE_PAYS`, `SOUS_TYPE`, `E`, `N`.

- **Never read into `processed/`:** `TEL_PRINCIPAL`, `TEL_SECONDAIRE`,
  `FAX`, `EMAIL`, `RAISON_SOCIALE` and `RAISON_SOC_PARENT` (a sole trader's
  legal name is the person's). Step 2 keeps the code, the premises type, the
  trade name subject to the name rule, the commune and the point.
- `NATURE_JURID` is on company rows only; an establishment reaches it
  through `ID_ENTREPRISE` (every establishment carries one).

### Counting rules used here (a rough map; the build's taxonomy decides)

Georgia's NACE precedent (`pipeline/taxonomies/georgia_nace.py`) applied to
NOGA, checked against `docs/category_rules.md`:
- **Food:** 561001 restaurants, cafés, snack bars, tea rooms; 561002;
  563001 bars; 563002 discothèques and night clubs (kept, R5). Out: 562100
  traiteurs and 562900 other food service (R1), 561003 restaurant management.
- **Retail:** division 47 except 4781/4789 (stalls and markets, R1),
  4791/4799 (non-store) and 477801 (fuel dealers, the nonstore row); 473000
  fuel stations kept (R4); 451102, 451902, 453200 and 454000 (vehicle and
  parts retail, R4). Out: 451101 (wholesale and intermediation), 4520
  (repairs), 453100.
- **Personal services:** 960101 laundries, 960102 dry cleaning, 960201
  hairdressers, 960202 beauty, 960401 saunas and solariums, 960402 other
  physical well-being. Out: 960300 funeral, 960900 the catch-all (R2).
- **Dropped by premises type:** `TYPE_LOCAL` "Activité à domicile" and
  "Activité itinérante". In scope that removed 62 home-based (personal 43,
  retail 19) and 70 itinerant (personal 51, retail 14, food 5) bucket rows.

### Measured 2026-10-04 (cached file, row by row, `heavy_job.py` label `geneva-brief`, peak 0.12 GB)

| | Food | Retail | Personal | Total |
|---|---|---|---|---|
| **12 tram communes, kept establishments** | **1,882** | **2,899** | **1,104** | **5,885** |
| of which with a point | | | | 5,885 (100%) |
| of which sole traders ("Entreprise individuelle") | 340 | 509 | 649 | 1,498 (25.5%) |
| Canton, same rules | 2,090 | 3,224 | 1,218 | 6,532 |

- **Premises types among the 5,885:** Commerce/magasin/arcade 3,568;
  Hôtel/restaurant/bar/dancing 1,844; Bureau/étude/cabinet 326; Atelier 62;
  Station-service 50; **Stand ambulant 22**; six other types 14.
- **747 kept establishments have no company row in the file** (a seat
  outside the canton: chains and branches), so their legal form is unknown.
- **Company rows, the gap:** 6,168 company rows in scope carry a bucket
  code; **1,848 have no establishment row anywhere** (food 333, retail 883,
  personal 632; 960 of them sole traders). They have no premises type, so
  home-based seats cannot be told from shops. The probe found the rest
  mostly duplicate an establishment on the same address point.

### Classification - open at build (`premises-taxonomy`)

- **Stand ambulant (22):** out on R1 and the mobile-units row; kept rows
  would then be 5,863.
- **Bureau/étude/cabinet (326):** a storefront code on an office-typed
  premises (an agency office of a chain, a beauty practice in an office
  building). Read the split by code and bring a call; the premises type is
  the register's own signal, as Göteborg's non-storefront share was.
- **562100 traiteurs:** out here by R1 and Georgia; France kept 56.21Z as
  usually a shop. Bring the count if the owner wants France's reading.
- **477801 (3 canton-wide), 451101, 454000 (motorcycle sale and repair in one
  code; Georgia keeps 45.40):** small; follow the precedent named above.
- Measure the catch-all share with `brief_check.py`'s `taxonomy_catchall`
  kind once the module exists; `check_category_continuity.py` must answer
  the new taxonomy.

---

## Rail - TPG trams

- **Lines and per-line stop counts (gate 3, the operator's own):** TPG's
  line pages, both directions, distinct names, read 2026-10-04:

  | Line | Ends | Stops |
  |---|---|---|
  | 12 | Lancy-Bachet, gare - Thônex, Moillesulaz | 25 |
  | 14 | Bernex, Vailly - Meyrin, Gravière | 30 |
  | 15 | Plan-les-Ouates, ZIPLO - Genève, Nations | 22 (21 each way; each direction has one stop the other lacks) |
  | 17 | Lancy-Pont-Rouge, gare - Annemasse, Parc Montessuit | 26 (22 in Switzerland) |
  | 18 | Grand-Lancy, Palettes - Meyrin, CERN | 31 |

  85 distinct stop names on the network. These go in
  `OPERATOR_STATION_COUNTS` with `OPERATOR_COUNTS_SOURCE` naming the pages
  and the date. ⚠️ **TPG announces a timetable change valid from
  2026-10-18**: re-read the five pages at build.
- **Geometry and stops: OpenStreetMap through `osm-rail`** (Zurich's route),
  one Overpass query for the city, never parallel; after a 504 or 429 wait at
  least 60 s. A national GTFS (opentransportdata.swiss) is not in this brief:
  it goes to the owner first. OSM's ODbL notice is the site's own.
- **Every stop gets a ring, no thinning** (the owner's trams-only calls).
  Each drawn line gets its permanent on-map label and a legend entry.
- **Frequency:** every 6 to 10 minutes by day (the probe), over the kit's
  20-minute floor on every line.

---

## Licence - SITG, permitted with conditions (`licence-read` 2026-10-04)

- **Level A, "Accès libre"**, under SITG's "Conditions d'utilisation des
  données du Portail SITG" (version of 19 May 2026; the copy inside the zip
  is byte-identical): reproduce, publish, adapt, combine, commercial use
  included. Conditions page:
  `https://sitg.ge.ch/ressources/conditions-utilisation-donnees`.
- **What the build must do:**
  - display the source line verbatim with the extract date (CU 5.3.1);
  - state the derived use (CU 5.3.2: a map made on the basis of SITG portal
    data, with the date; the CU gives an example wording the build adapts);
  - link the conditions (CU 5.5);
  - **no re-identification** (CU 5.4.2): no join of REG to any other source
    to identify a person; data-protection law applies;
  - no resale (RIRT art. 62).
- **The indemnity (CU 7.2), accepted by the owner 2026-10-04.** Narrower
  than Hong Kong's: limited to third-party claims arising from the user's own
  infringements, personality and data-protection rights named. **At build it
  is recorded in `docs/data_sources.md`'s accepted indemnities**, beside Hong
  Kong's and Sacramento's, citing the owner's date; it is not a notice and
  not a build step.
- **ge.ch's website terms** (applied by SITG's footer to its subdomains):
  read by the owner as the website's only, not the dataset's (2026-10-04).
- The licence row goes in `docs/data_sources/switzerland.md`, with the
  verdict and the notice. Honour any removal request (the removal rule), from
  the canton or a business.

## Notices (the build assigns the number in the published-notices list)

- **SITG, verbatim (CU 5.3.1):** "Source : Portail des données SITG (État de
  Genève), téléchargé et/ou extrait en date du […]." with the file's extract
  date in the brackets.
- **The derived-use statement (CU 5.3.2)**, drafted by the build in French
  on the CU's example, and a sentence linking the conditions page. A sentence
  no template covers is a proposal in the drafts file.
- OSM's ODbL notice for the rail (the site's own).

## Privacy

- 1,498 kept establishments belong to sole traders, whose trade name is
  often the person's own. Apply the name rule; run
  `python scripts/check_personal_exposure.py geneva` after step 2; record the
  verdict in the drafts file and `docs/privacy_verdicts.md`. A withheld list
  holds keys (`pipeline/name_keys.py`), never names.
- **Never print a row.** Field names and counts only, in this brief, the
  drafts file and the commit messages.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for each notice, **card face or
caption only**, and any open terms question:
- **The SITG source line and derived-use statement: caption**, clearly
  visible with the card. The CU asks for "de manière clairement visible" and
  names no place; a card that would travel without its caption carries the
  line on its face.
- **OSM's notice: caption.**
- **Open terms question: none** (the indemnity accepted and ge.ch's terms
  read, owner 2026-10-04).

## Still unknown

- ⚠️ **The two owner calls above:** company rows with no establishment row
  (1,848), and the sole-trader name rule.
- ⚠️ **The taxonomy:** Bureau/étude/cabinet (326), Stand ambulant (22),
  traiteurs, the catch-all share.
- ⚠️ **Stops by polygon**, the median gap and the ring size; gate 3 after
  the 2026-10-18 timetable.
- ⚠️ **The commune boundary source** and its row.
- ⚠️ **The privacy verdict.**

```brief-checks
[
  {
    "id": "geneva-reg-featureserver",
    "claim": "THE BUSINESS LEG: SITG's REG point layer still serves about 100,588 active rows (2026-10-04, daily) with the fields step 2 reads: the record type, the NOGA code, the premises type, the company link, the legal form and the commune",
    "kind": "arcgis_layer",
    "url": "https://vector.sitg.ge.ch/arcgis/rest/services/REG_ENTREPRISE_ETABLISSEMENT/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 100588,
    "tolerance": 3000,
    "present": ["TYPE_REG", "CODE_NOGA", "TYPE_LOCAL", "ID_ENTREPRISE", "NATURE_JURID", "PHYS_COMMUNE", "STATUT_REG"]
  },
  {
    "id": "geneva-reg-dataset-page",
    "claim": "SITG's dataset page still lists REG as Level A (Accès libre), updated daily, in LV95, and points at the conditions of use",
    "kind": "http_contains",
    "url": "https://sitg.ge.ch/donnees/reg-entreprise-etablissement",
    "present": ["REG_ENTREPRISE_ETABLISSEMENT", "Accès libre", "Quotidienne", "conditions-utilisation-donnees"]
  },
  {
    "id": "geneva-sitg-conditions",
    "claim": "SITG's conditions page still grants Level A data for commercial use with the source and any processing stated, and links the full Conditions d'utilisation (the version of 19 May 2026 was read). If it changes, re-read the licence",
    "kind": "http_contains",
    "url": "https://sitg.ge.ch/ressources/conditions-utilisation-donnees",
    "present": ["A - Accès libre", "fins commerciales", "indiquer la source", "Conditions%20d%27utilisation%20Donn%C3%A9es%20Portail%20SITG.pdf"]
  },
  {
    "id": "geneva-tpg-tram-17-ends",
    "claim": "TPG's own page for tram 17 still runs from Lancy-Pont-Rouge to Annemasse, Parc Montessuit (22 of its 26 stops in Switzerland); the French end is drawn and listed as outside",
    "kind": "http_contains",
    "url": "https://www.tpg.ch/fr/lignes/17",
    "present": ["Lancy-Pont-Rouge, gare", "Annemasse, Parc Montessuit", "Gaillard, ", "Ambilly, "]
  },
  {
    "id": "geneva-projected-crs",
    "claim": "The derived UTM zone is EPSG:32632, but the build projects in LV95 (EPSG:2056), the register's own grid (Zurich's precedent); tram mode, full coverage, regional scope",
    "kind": "utm_zone_from_longitude",
    "lon": 6.14,
    "expect": "EPSG:32632",
    "mode": "tram",
    "coverage": "full",
    "scope": "regional",
    "crs": "EPSG:2056",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
