# Riga — build brief

**Written 2026-09-24 from three re-probes and the open gap's final probe**,
all run that day (`DECISIONS.md`; scratch in `reprobes/riga/` and
`gap_final/riga/`). Run `python scripts/brief_check.py riga` before writing
any code. **Latvia's first city.** Amsterdam's and Rotterdam's two-layer
shape, so copy them, not a single-register city.

**✅ Decided by the owner, 2026-09-24:**
1. **Band A, with the scoped vacancy disclosure** (below) on the page.
2. **All 7 tram routes are drawn**, thinned as Amsterdam and Rotterdam were.
   Colours come from Rīgas satiksme's own route maps.
3. **No suburban rail.** All five Vivi corridors fail the frequency test.
   The exclusion is disclosed in the station-scope section.
4. **Riga builds before Taiwan** (owner, 2026-09-24): a small build that fits
   the week's remaining budget. Taiwan's three follow the weekly reset.

---

## 🚩 Step 0 still open: the licence reads (the build's first step)

**No Riga source has a row in `docs/data_sources.md`.** Each licence below
is only as declared on `data.gov.lv`, never read. Run a `licence-read`
agent per source before any code, and follow `read-licence`: the portal's
own terms, anything incorporated by reference, and what must be DISPLAYED.

| # | Source | Publisher | Declared |
|---|---|---|---|
| 1 | Excise-goods licences (`pdb_akclicences_odata.csv`) | State Revenue Service (VID) | CC0 |
| 2 | Rīgas satiksme GTFS (`marsrutusaraksti08_2026.zip`, monthly) | Rīgas satiksme | CC0 |
| 3 | Cadastre open text data (`premisegroup.zip`, `building.zip`, `address.zip`) and the cadastral map (`0001000_kk_shp.zip`) | State Land Service (VZD) | CC BY 4.0 |
| 4 | Riga's own address points (`adreses.gpkg`, "Rīgas ielas un adreses"), neighbourhoods (`apkaimes.gpkg`), degrading buildings (`vidi_degradejosas_buves.gpkg`) | Riga municipality | CC BY 4.0 |

If a read comes back restrictive, stop. Taiwan is the fallback build.

---

## The one-line summary

**Two open layers placed at 96–99%: 1,596 food-service premises from the
national excise register and 4,816 shops from the cadastre's premise groups,
around 125 tram stations on 7 routes. The rings hold 78.5% of the shops and
82.6% of the food. The one caveat the page must carry is vacancy: measured
only in the historic centre.**

---

## Business layer 1: food service, from the excise register

| | |
|---|---|
| **File** | `https://data.gov.lv/dati/dataset/a1adb6dd-a4a1-41c9-9177-c1cd942e012e/resource/f88cd5ea-61b0-42e8-a0a8-25504dfbcdc9/download/pdb_akclicences_odata.csv` (**222.9 MB**, 144,151 rows nationally), updated daily |
| **Current filter** | `Statuss == "Spēkā"` AND `Darbiba_izbeigta_darbibas_vieta` empty |
| **Riga** | **2,898 current premises** (holder × address) at 2,193 addresses. Food service **1,596** (1.10× OSM); alcohol/tobacco retail 746 (0.14× OSM shops); fuel, warehouse, web and wholesale 335; other 221 |
| **Columns used** | `Darbibas_vietas_tips` (place type: kafejnīca, bārs, restorāns, veikals, DUS…; 99.9% filled), `Darbibas_vietas_adrese` (100%), `Licences_veids`, `Statuss`, `Darba_laiks` (opening hours, 99%), and the place start/end dates |
| ⛔ **NEVER READ** | **`Nodoklu_maksatajs`** (the licence holder, who may be a person) and **`NMR_kods`** (tax number). Select columns by EXACT name. The Japan build once printed three corporate names from a pattern match |
| **Placement** | Join `Darbibas_vietas_adrese` to Riga's own address points (`adreses.gpkg`, 48,749 points): **75.2% exact + 21.0% after dropping a unit suffix = 96.2%**; street only 3.2%; unmatched 0.6%. NFKC plus whitespace only (`reprobes/riga/akc_join.py`) |
| **Food classifier** | Place type matched on `kafejn|restor|bār|bistro|ēdn|krog|pub|picērij|ēdin|klub|kafe|suši|burger|grill`. The earlier pattern also matched `viesn|hotel`, and hotels are lodging, so drop those at build |

## Business layer 2: shops, from the cadastre's premise groups

| | |
|---|---|
| **File** | VZD cadastre open text data, part 6 "Telpu grupu raksturojošie dati": `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/5d8b1cfa-1e67-4b77-a6ac-b4e37eba0d7e/download/premisegroup.zip` (65.6 MB; Riga ATVK `0001000`, prepared 2026-09-20) |
| **Riga** | 573,240 premise groups. Use class **1230** (trade premise group): **7,169**. Class 1211 (hotel or catering): 5,207, but 81% hotel rooms, so **not used** (the excise register is the food layer) |
| **Which 1230 rows** | **4,816 (67%) whose `PremiseGroupName` reads as a shop** (veikals, salons…); 84% on the ground floor; only 3.8% wholesale, storage or office; 0.93× OSM shops including hair and beauty. 62% were last surveyed before 2010 |
| **Placement** | `ObjectCadastreNr` → KKBuilding footprints (`0001000_kk_shp.zip`): **7,133 of 7,169 (99.5%)**. A second route, the building's address to the address register, agrees at a median **3.6 m** |
| **Drop** | **208 shops (4.3%)** in buildings the city lists as degrading (`vidi_degradejosas_buves.gpkg`, CC BY 4.0) |
| **Category** | One "Shops and services" category, **Amsterdam's reason**: a building register cannot tell a hairdresser from a clothes shop. De-duplicate against the excise register's shops by address |

## ⚠️ Vacancy: the disclosure the page must carry (owner-approved scope)

- **There is no citywide rate.** CSP has no non-residential vacancy table.
  None of the cadastre's 57 building or 13 premise-group fields records
  occupancy. Market reports are silent, dated 2012, or 403 (Colliers, left
  alone).
- **Two municipal figures, each with its area and date:**
  - **20.4% vacant** of 2,324 street-front ground-floor premises, historic
    centre and its protection zone, August–November 2024. The municipality's
    own headline for the same survey is **73% occupied**, so quote the
    report's definitions, not a derived figure.
  - **15% vacant** (87 of 573), Old Town only, summer 2025.
- **"Not measured elsewhere"**: about 62% of in-ring named shops.
- The cadastre counts the same premises the survey counts: street by street,
  Spearman 0.96, and 2,259 against 2,324 with socle floors. **An OSM
  occupancy proxy matched the centre's level but could not rank streets
  (Spearman 0.23), so it is never published as a rate.**

---

## Rail: trams, measured 2026-09-24

**Scope: the city.** OSM relation **13048688** (Rīga, admin_level 5) equals
the union of Riga's 58 neighbourhoods (304.1 against 304.0 km²). Project in
**EPSG:32635** (UTM 35N) for all geometry. The cadastre and address files
arrive in LKS-92 (EPSG:3059).

**Source: Rīgas satiksme's GTFS** on data.gov.lv
(`https://data.gov.lv/dati/dataset/6d78358a-0095-4ce3-b119-6cde5d0ac54f/resource/2e9922e8-d863-41d3-9ff4-9a97ec9031a3/download/marsrutusaraksti08_2026.zip`).
It is a monthly file (uploaded 2026-09-08), with the calendar running to
2027-09-01. Every trip has a shape. **7 tram routes**, matching the
operator's list. 243 stop IDs make **125 stations** by name, **all inside
Riga**.

| Route | Termini | Stops | Median gap | Peak / midday headway |
|---|---|---|---|---|
| 1 | Imanta – Jugla | 37 | 433–455 m | 5 / 10 min |
| 7 | Ausekļa iela – Ķengarags | 23 | 467–483 m | 6 / 9 min |
| 11 | Ausekļa iela – Mežaparks | 22–23 | 395–398 m | 9 / 11–12 min |
| 10 | Centrāltirgus – Bišumuiža | 16–18 | 413–443 m | 24 / 24 min |
| 5 | Iļģuciems – Mīlgrāvis | 34 | 388–424 m | 30 / 30–33 min |
| 8 | Mīlgrāvis – Tapešu iela | 37 | 381–385 m | 40 / 30–33 min |
| 14 | Iļģuciems – Ķengarags | 33 | 454–458 m | 30–40 / 33 min |

- 🚨 **Every route is the same red (`#FF000C`) in both OSM and the GTFS.**
  `check_map_markup.py` refuses two lines that close. Take each line's
  colour from Rīgas satiksme's route maps
  (`https://www.rigassatiksme.lv/en/current%20information/route-maps`, not
  yet opened), as Amsterdam did.
- **OSM has a route 8a** that is in neither the GTFS nor the operator's
  list: **do not draw it**.
- **Stops are 380–480 m apart**, so thin the rings with
  `docs/sub_transit_line_filters.md`, as Amsterdam and Rotterdam were.
- **Suburban rail is out** (Vivi GTFS `https://vivi.lv/uploads/GTFS.zip`,
  declared CC0 on data.gov.lv, 24 stations in Riga). Best case, Jūrmala: 15
  minutes at the evening peak, 30 at midday. Adding all five corridors would
  bring in only 164 shops and 49 food premises.

### Ring coverage (966 m, clipped to the city)

| Stations | City area | Named shops | Food premises |
|---|---|---|---|
| **Trams, all 7 routes** | 30.4% | **3,753 (78.5%)** | **1,282 (82.6%)** |
| Trams, routes 1/7/11 only | 20.7% | 3,333 (69.7%) | 1,177 (75.8%) |
| Trams + all 24 rail stations | 37.2% | 3,917 (81.9%) | 1,331 (85.8%) |

Without the 208 degrading-building shops: 3,558. Amsterdam holds 95.5%.

---

## Traps

- **`data.gov.lv` is CKAN at `/dati/api/3/action/`**, not `/api/3/`.
- **The excise register is a licence ledger, not a premises list**: one
  premises can hold several licences (alcohol, tobacco, beer), so
  de-duplicate on holder × address before counting.
- **The PVD food-business register** (`pakalpojumi.pvd.gov.lv`) is
  **geo-blocked** (Latvia and Germany only). Not used, and not routed around.
- **`opendata.riga.lv` does not resolve.** The city's 79 datasets are on
  data.gov.lv.

## Still unknown

- The four licence reads above.
- Each tram line's colour, from the route maps.
- Whether the degrading-buildings drop and the excise/cadastre
  de-duplication change the ring figures by more than a few percent.

```brief-checks
[
  {
    "id": "riga-excise-dataset",
    "claim": "The State Revenue Service's excise-licence dataset answers on data.gov.lv's CKAN (the food layer: 1,596 current Riga food-service premises)",
    "kind": "http_ok",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=a1adb6dd-a4a1-41c9-9177-c1cd942e012e",
    "min_bytes": 1000
  },
  {
    "id": "riga-cadastre-dataset",
    "claim": "VZD's cadastre open text data (premise groups, buildings, addresses) answers on data.gov.lv (the shops layer: class 1230)",
    "kind": "http_ok",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=be841486-4af9-4d38-aa14-6502a2ddb517",
    "min_bytes": 1000
  },
  {
    "id": "riga-tram-gtfs-dataset",
    "claim": "Rīgas satiksme's GTFS dataset answers on data.gov.lv (7 tram routes, 125 stations, monthly file)",
    "kind": "http_ok",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=6d78358a-0095-4ce3-b119-6cde5d0ac54f",
    "min_bytes": 1000
  },
  {
    "id": "riga-address-points-dataset",
    "claim": "Riga's own address points (adreses.gpkg, 48,749 points) answer on data.gov.lv - the excise join target (96.2%)",
    "kind": "http_ok",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=4e2bd2d1-69e1-4598-b2f0-713e963e55e3",
    "min_bytes": 1000
  }
]
```
