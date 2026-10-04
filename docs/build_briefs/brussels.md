# Brussels (City of Brussels) — build brief

**Screened 2026-10-03/04 (staging, the coverage sweep's first group); Band A,
owner-approved 2026-10-03, Belgium's first city.** Run
`python scripts/brief_check.py brussels` before writing any code. The trail:
`docs/decisions_drafts/staging.md`, 2026-10-03 "The sweep's first group
banded: eleven cities on the owner's approval", "Seven licence reads for the
sweep's first group; Brussels and Tacoma to A (owner)" and "KBO measured:
Belgian bands kept; Brussels (Regional) D to C" (the City keeps hub.brussels;
KBO is a cross-check only). Master list: `docs/city_master_list.md`, Band A,
"City of Brussels".

**A new country.** Run `add-country`'s questions only as far as this build
needs them (they are answered in the drafts entries above), then read
`docs/spain_retrospective.md`: Belgium is bespoke per city (the City of
Brussels, Antwerp and Ghent, Charleroi and Liège each have a different
business source), not one national register. The build opens
`docs/data_sources/belgium.md`. Skills: `add-city`, `scaffold-city`,
`premises-taxonomy`, `publish-city`; `osm-rail` only on the fallback below.
**Not** `tram-city`: the map's backbone is the metro.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot color) | **`metro`** | **25 metro and premetro stations** in the commune (the City's own entrances dataset, 93 entrances in Bruxelles) |
| **`coverage`** | **`full`** | All three buckets from one field survey |
| **Scope** | **The City of Brussels commune** (Bruxelles-Ville / Stad Brussel, NIS 21004), `SCOPE = "city"` | The inventory is the City's extract: every row inside the commune polygon, none outside. The other 18 communes are **Brussels (Regional)**, a separate Band C row on KBO; never merged into this page |
| **Trams** | **Drawn and thinned** (Amsterdam's precedent; Oslo drew its trams too, unthinned) | The commune is long and thin, and trams carry most of its surface service: without them Laeken and Neder-Over-Heembeek north of Bockstael/Heysel and the Avenue Louise strip are served only by stations at their ends. The thinning rule is below |
| **Page name** | **"Brussels"**, slug `brussels`; the scope bullet names the City of Brussels, one of the Region's 19 communes | **Owner, 2026-10-03** ("recommendation accepted"). A later regional page would be "Brussels (Regional)" |
| **Rings** | by the spacing rule (`docs/ring_rules.md`) | Pentagon stations sit close together (Bourse, De Brouckère, Anneessens); measure the median gap among the stations kept. Under about 550 m means halved rings, as Oslo and Paris |
| **Region** | `"Europe"`, country `"Belgium"` | — |

---

## The one-line summary

**hub.brussels's ground-floor shop inventory for the City of Brussels: 6,880
units, every one with a point inside the commune, one survey dated
2025-10-17, CC BY 4.0; 25 metro and premetro stations plus thinned trams.
The work is the taxonomy (285 single types, multi-valued) and the credit.**

| | **City of Brussels** |
|---|---|
| Rail | STIB-MIVB: metro M1, M2, M5, M6 and the premetro; trams |
| Stations in scope | **25** underground metro and premetro stations, plus thinned tram stops |
| Projected CRS | **EPSG:32631** (UTM 31N, 4.35° E) |
| Business source | "Commerces recensés par hub.brussels situés sur le territoire de la Ville de Bruxelles", opendata.brussels.be, 6,880 rows, CC BY 4.0 |

---

## Scope — the commune, measured

- **One polygon.** The Region's commune-limits dataset
  (`limites-administratives-des-communes-en-region-de-bruxelles-capitale`,
  PARADIGM, CC0 1.0, NIS code `21004`) holds the City as a MultiPolygon of
  **one part with no holes**: no exclave. Its shape is the trap: the
  Pentagon, the European quarter to the east, the former communes of
  **Laeken (1020), Neder-Over-Heembeek (1120) and Haren (1130)** to the
  north, and to the south the **Avenue Louise strip and the Bois de la
  Cambre**, joined to the core by little more than the avenue's width.
- **Scope by polygon, never by postcode.** The commune's own postcodes are
  1000, 1020, 1120 and 1130, but its eastern and southern parts share other
  communes' postcodes. The inventory's rows: 1000 5,322; 1020 989; **1050
  221; 1040 114**; 1120 141; 1130 79; 1105 12; 1099 2. All 6,880 fall inside
  the NIS 21004 polygon (screen, `screens/belgium.md`); step 2 re-checks it.
- The boundary source needs its own row in `docs/data_sources/belgium.md`
  (CC0 1.0: no notice required; a credit is a courtesy).

---

## Business leg — hub.brussels's inventory

| | |
|---|---|
| Dataset | `commerces-recenses-par-hubbrussels-vbx` on opendata.brussels.be (Opendatasoft, Explore API v2.1). Publisher **Ville de Bruxelles/Data Management**; `source` = hub.brussels on every row; metadata `attributions` = Google Maps, hub.brussels |
| Rows | **6,880**, every one with `geo_point_2d` |
| Date | **`last_update` 2025-10-17 on every row**: one survey. The portal reprocesses daily (`data_processed`), but the content is that survey |
| Fields | `objectid`, `category_fr/nl/en`, `type_fr/nl/en`, `name_fr/nl/en`, `address_fr/nl`, `postalcode`, `municipality_fr/nl`, `google_maps`, `google_street_view`, `geo_point_2d`, `geo_shape`, `source`, `last_update` |
| Names | Trade names (shop signs), not registrants |
| **Fetch** | `pipeline/brussels/fetch_sources.py` pages the Explore records API or takes the dataset's export, **without `google_maps` and `google_street_view`** (drop them at fetch, never stored in `processed/`). A step never fetches |

### Currency — passes, and the page says it is one survey

A complete ground-floor survey, vacant units included (1,068), so closures
drop out rather than linger. **The page states the date: a single survey,
17 October 2025** (the data-age caption and a bullet under The businesses).
Re-check by 2030-10 under the five-year ceiling; a new survey means a re-pull
and a re-measure.

### Classification — `type_fr`, multi-valued

- **9 top categories** (`category_*`, too coarse to key on) and **285
  distinct single types** once `type_fr` is split. **1,817 rows carry two or
  more types.**
- ⚠️ **Split outside parentheses only.** A naive comma split breaks types
  such as "Station-service (essence, gaz)" and "Dégustation - Cours
  (Cuisine, alcools, Bricolage…)". Write the splitter first and assert the
  distinct-type count (285) in step 2.
- **The screen's mapping** (`screens/hub_buckets.mjs`, a rough map for
  counts, not a taxonomy; priority Food service > Retail > Personal services
  among a row's kept types):

| Class | Rows |
|---|---|
| **Food service** | **1,908** |
| **Retail** | **2,459** |
| **Personal services** | **508** |
| Vacant (`Cellule vide - Statut inconnu`) | **1,068 — out** |
| Out: finance, agencies, post, printing, rentals, call shops, telecom providers | 321 |
| Out: recreation, culture, sport (gyms, museums, cinemas, venues) | 170 |
| Out: lodging | 132 |
| Out: repairs (garages, car wash, shoe repair, key cutting, alterations, tailors) | 94 |
| Out: gambling 10, funeral 8, adult (cabaret, peep show) 5, catch-all 1 | 24 |
| Ambiguous-only rows (below) | 196 |

The 10 rows sum to 6,880.

- **The build's taxonomy decides, with `premises-taxonomy`** (a new module,
  `pipeline/taxonomies/brussels_hub.py` or similar; `filter_to_storefront()`,
  never a code prefix). Measure the catch-all share first. Every keep or drop
  is checked against `docs/category_rules.md`, and
  `check_category_continuity.py` must answer the new taxonomy.
- **The 160 rows typed in two buckets** (an épicerie that is also a
  sandwicherie, and so on) need a stated rule. The screen used food over
  retail over personal; that rule or another is the build's, recorded with
  its counts in the drafts file.
- **Ambiguous types, with the precedent to recommend:**
  - **`Galerie d'art (hors photo)`, 145 rows: Retail** by precedent (NAICS
    459920 in New Orleans, Sacramento, Buenos Aires).
  - **`Cantine - Cafétéria - Food-court`, 19:** R1 leaves institutional and
    staff canteens out; a street-level cafeteria or food court open to the
    public is a counter of its own. Read the 19 at build and bring the call
    with the count; `Location de salle pour banquet` (hall hire) is out.
  - **`Spa`, `Sauna`, `Hammam`, `Soins de la personne - Général`, 11:
    Personal services** (Korea's saunas), except any the register or its
    signage names as adult (R3): check them at build.
  - **`Clubs privés`, 2:** out unless read as a bar or nightclub open to the
    public (nightclubs are kept as Food service, R5).
  - Small retail catch-alls (`Autres accessoires` 3, `Équipement de la maison
    - Non déterminé` 1): Retail. Contractor and craft types (`Portes - Châssis
    - Volets` 10, `Chauffage - Climatisation` 2, glass/wood craft, framers,
    engravers): decide by what the premises is. `Autre activité`, `Autres
    loisirs`, `Autre infrastructure`: out (R2's logic).
  - `Tailleur - Costumes` 22 sits with repairs (alterations out); suit shops
    would be Retail. `Fournisseur téléphonie - Internet` 9 and
    `Téléphonie-cabine - Web café` 14 were filed out.

### Cross-checks, never layers

- **FAVV's operator list** (postcodes 1000/1020/1120/1130 only, so it misses
  the commune's 1040/1050 parts): 2,133 registered food-service
  establishments against hub's 1,908 commune-wide; hub holds about 90% of the
  food register's count (FAVV also counts upstairs and in-hotel premises).
- **KBO** (the owner's full file, extract 501): companies' establishment
  units in the City, retail 4,477, food 2,765, personal 443, about 1.9 times
  hub's retail and 1.5 times its food, because it counts registered
  establishments, not storefronts. The owner's call: hub.brussels stays the
  source (2026-10-03).

---

## Rail — STIB-MIVB

### Stations: 25 underground, and the premetro trap

- **25 distinct metro and premetro stations in the commune**, from the City's
  "Entrées des stations souterraines de métro et prémétro"
  (`entrees-stations-souterraines-metro-premetro-ingangen-ondergrondse-metro-premetro-stations`,
  CC BY 4.0, 109 entrances, 93 in Bruxelles): Anneessens, Arts-Loi, Bockstael,
  Botanique, Bourse, De Brouckère, Gare Centrale, Heysel, Hôtel des Monnaies,
  Houba-Brugmann, Lemonnier, Louise, Madou, Maelbeek, Pannenhuis, Parc, Porte
  de Hal, Porte de Namur, Rogier, Roi Baudouin, Sainte-Catherine, Schuman,
  Stuyvenbergh, Trône, Yser.
- ⚠️ **Three of them are served by trams alone.** The City's stop list files
  22 of the 25 as metro stops; **Anneessens, Bourse and Lemonnier** are
  North-South premetro stations with no metro service. A step 1 that keeps
  the metro route type and thins everything else would thin these three
  underground stations as surface tram stops. Mark all 25 as the central
  corridor by name, whatever the feed's route type.
- **Gate 3:** STIB's own per-line station lists for the metro (read for the
  count only), in `OPERATOR_STATION_COUNTS` and `OPERATOR_COUNTS_SOURCE`;
  English Wikipedia as a named secondary fallback (69 metro and premetro
  stations network-wide). Not looked up for this brief.

### Trams: drawn and thinned, Amsterdam's rule

- **The rule** (`docs/sub_transit_line_filters.md`, with
  `pipeline/stations.py`'s `thin()`, Amsterdam's config as the model):
  1. the 25 underground metro and premetro stations are the central
     corridor, always kept;
  2. each tram line's own two terminals inside the commune are kept;
  3. a stop shared by two or more lines is kept (an interchange resets the
     count);
  4. the rest are thinned to **one per half mile** (`THIN_SPACING_MILES =
     0.5`), measured along the line's own stop sequence, one direction per
     line.
  Each cut goes to `outputs/brussels/excluded_stations.csv` with a reason
  containing "spacing", and the city page names the thinned lines.
- **The size of it (ASSERTED, one source):** the City's stop list
  (`arrets-bus-tram-metro-societes-transport-public-vbx`, a region-wide
  snapshot of STIB, De Lijn and TEC stops, 2,908 rows dated 2026-04-10)
  holds **138 tram platform rows in Bruxelles, 61 distinct names** (premetro
  stations included), by postcode 1000 51, 1020 47, 1120 18, 1050 14, 1130 8.
  The build counts from the feed, not this list.
- **Lines:** the screen named T3, T4, T7, T8, T62 and T93 among the lines
  serving the commune (ASSERTED); count them from the feed. Each drawn line
  gets its permanent on-map label and a legend entry. Border stops along
  Avenue Louise and in Laeken are decided by the polygon. Stations outside
  the commune get no ring.
- Buses are not drawn; SNCB trains are commuter rail, out as everywhere. The
  page says so.

### Rail source: STIB's GTFS, after the owner accepts the portal's terms

- **STIB's static GTFS is open**: the Belgian Mobility Company's portal
  (`data.belgianmobility.io`, where `data.stib-mivb.brussels` now redirects)
  serves `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/stibmivb/static`
  at the anonymous tier, **no account, no key** (100 requests a day, 10 a
  minute), updated daily. Current, the operator's own stop sequences, and
  what the thinning rule needs (one stop sequence per line). **Recommended.**
- ⚠️ **Accessing it is accepting terms.** The portal's Terms of Use
  (December 2025, effective 2026-01-01) say "By accessing the data, the User
  acknowledges having read, understood, and accepted these Terms of Use", and
  the download button opens a consent box first. **Accepting terms is the
  owner's act**, and **the owner approved it on 2026-10-03** ("recommendation
  accepted") for the build's first fetch; a re-fetch after the terms change
  goes back to the owner. This brief carries no check that fetches the feed. Once accepted, add `gtfs_files`
  (look for `shapes.txt`) and `gtfs_feed_window` checks here.
- **Licence, to read (`licence-read`, one call) before the build uses it**:
  the terms put every PTO's data under **CC BY 4.0, with STIB-MIVB the sole
  licensor** (art. 3); the minimum credit is "Source: [PTO Name] – Open Data
  – [Date of dataset update]", and for modified data "Contains data
  originally published by [PTO Name], modified by [User Name]" is
  recommended (art. 4); the terms may change, "continued use" being
  acceptance (art. 8). Its row goes in `docs/data_sources/belgium.md` and its
  notice in the published-notices list.
- **Fallback: OpenStreetMap through `osm-rail`** if the owner declines the
  terms or the feed fails gate 3. One Overpass query for the city, never
  parallel; after a 504 or 429 wait at least 60 s. OSM's ODbL is the site's
  notice 1.
- The City's entrances and stop-list datasets are cross-checks for counts.
  If the build draws any point from them, each needs its own source row and
  credit, and their `google_maps` / `google_street_view` columns are dropped
  as below.

---

## Licence — CC BY 4.0, read (`licence-read` 2026-10-03)

- **Permitted with conditions.** CC BY 4.0: the portal adopts the
  producer's licence. hub.brussels describes the inventory as its field
  agents' own.
- **The "Google Maps" credit.** It sits on 79 of the portal's datasets and
  matches the two link columns built from each record's own point; **21 of
  24 comparable points lie within 0.03-0.35 m of UrbIS address points**
  (CC0), so the points are not Google geocodes. **The publisher never states
  what the credit covers**: recorded as an open terms question, not a block.
- **What the build must do:**
  - **drop `google_maps` and `google_street_view`**, and never link a pin to
    Google;
  - **name the publisher's listed contributors in the credit** (hub.brussels
    and Google Maps, as the metadata lists them), with the publisher, Ville
    de Bruxelles;
  - **no City logo and no "BXL" mark** (portal terms 3.1), and nothing
    implying endorsement by the City or hub.brussels.
- **The notice (one number; the Belgium kit assigns it):** credit to Ville
  de Bruxelles (Data Management) and hub.brussels, with the publisher's
  listed contributors hub.brussels and Google Maps; the dataset title and its
  page, `https://opendata.brussels.be/explore/dataset/commerces-recenses-par-hubbrussels-vbx/`;
  the licence link, `https://creativecommons.org/licenses/by/4.0/`; and **a
  statement of the modifications**: filtered to storefront types, vacant
  units removed, grouped into three categories, and the Google Maps and
  Street View link columns removed. No wording is prescribed; the build
  drafts it, and a sentence no template covers is a proposal in the drafts
  file.
- Honor any removal request (the removal rule), from the City, hub.brussels
  or a business.

## Privacy

- `name_*` holds shop signs, but a sign can be a person's own name. Run
  `python scripts/check_personal_exposure.py brussels` after step 2; record
  the verdict in the drafts file and `docs/privacy_verdicts.md`. A withheld
  list holds keys (`pipeline/name_keys.py`), never names.
- **Never print a row.** Field names and counts only, in this brief, the
  drafts file and the commit messages.

## Scope, CRS, region

- **Scope:** the City of Brussels commune, `SCOPE = "city"`. The scope
  bullet says it is one of the Region's 19 communes and that the other 18 are
  not on this map.
- **CRS:** UTM 31N, **EPSG:32631**, from 4.35° E. The points are read in
  EPSG:4326 and projected; never buffer in 4326.
- **Region:** `"Europe"`, country `"Belgium"` (a new country: a new
  `docs/data_sources/belgium.md`, a new country section on the two reference
  pages, and `check_macro_labels.py` at 375, 768 and 1200 for the new label).
- **Scaffold:** `scaffold_city.py --slug brussels --name Brussels
  --system-name "STIB-MIVB" --taxonomy <the new key> --lat 50.846 --lon 4.352
  --region Europe --country Belgium --mode metro --page-number <the kit's>`
  (`--dry-run` first).

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for each notice, **card face or
caption only**, and any open terms question:
- **The hub.brussels CC BY 4.0 credit: caption.** CC BY 4.0 section 3(a)
  lets attribution be given in any reasonable manner for the medium; nothing
  asks for the card face.
- **STIB-MIVB's credit (or, on the fallback, OSM's notice 1): caption**, on
  the same reading.
- ⚠️ **Open terms question, known:** what the publisher's "Google Maps"
  contributor credit means is unstated; the build names it as listed and
  drops the link columns. Record it so Visuals can decide whether a card
  carries the credit.

## Still unknown

- ✅ **The Belgian Mobility Company's terms**: accepted by the owner for the
  first fetch (2026-10-03); the STIB licence read is done (permitted with
  conditions, `docs/decisions_drafts/staging.md`). Add the feed's checks
  after the fetch. Credit: "Source: STIB-MIVB – Open Data – [feed date]",
  the modified-data line, and the Belgian Mobility Company portal.
- ⚠️ **The taxonomy**: the splitter, the catch-all share, the two-bucket
  rule, and the ambiguous types above.
- ⚠️ **Tram lines and stops in the commune**, the thinned count, and gate 3.
- ⚠️ **The ring size** from the median station gap.
- ⚠️ **The privacy verdict.**

```brief-checks
[
  {
    "id": "brussels-hub-dataset-meta",
    "claim": "THE BUSINESS LEG: the City's hub.brussels inventory is still CC BY 4.0, published by Ville de Bruxelles/Data Management, 6,880 records, crediting Google Maps and hub.brussels, and still carrying the two Google link columns the build drops. If the attributions change, re-read the licence",
    "kind": "http_contains",
    "url": "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/commerces-recenses-par-hubbrussels-vbx",
    "present": ["\"license\": \"CC BY 4.0\"", "Ville de Bruxelles/Data Management", "\"records_count\": 6880", "\"attributions\": [\"Google Maps\", \"hub.brussels\"]", "google_street_view", "type_fr"]
  },
  {
    "id": "brussels-hub-one-survey-date",
    "claim": "Every one of the 6,880 rows carries last_update 2025-10-17: one survey, the date the page states",
    "kind": "http_contains",
    "url": "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/commerces-recenses-par-hubbrussels-vbx/records?select=last_update%2Ccount%28%2A%29%20as%20n&group_by=last_update",
    "present": ["\"total_count\": 1,", "2025-10-17", "\"n\": 6880"]
  },
  {
    "id": "brussels-hub-vacant-units",
    "claim": "1,068 rows are vacant units (type Cellule vide), dropped by the build",
    "kind": "http_contains",
    "url": "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/commerces-recenses-par-hubbrussels-vbx/records?limit=0&where=type_fr%20like%20%22Cellule%20vide%2A%22",
    "present": ["\"total_count\": 1068"]
  },
  {
    "id": "brussels-underground-stations",
    "claim": "The City's metro and premetro entrances dataset names 25 distinct underground stations in the commune (municipality Bruxelles) - the central corridor, never thinned",
    "kind": "http_contains",
    "url": "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/entrees-stations-souterraines-metro-premetro-ingangen-ondergrondse-metro-premetro-stations/records?select=station_fr&group_by=station_fr&where=municipality_fr%3D%22Bruxelles%22&limit=100",
    "present": ["\"total_count\": 25", "ANNEESSENS", "LEMONNIER", "BOURSE", "STUYVENBERGH"]
  },
  {
    "id": "brussels-stib-gtfs-portal-terms",
    "claim": "STIB's static GTFS is offered on the Belgian Mobility Company's portal at the anonymous tier (100 requests a day), CC BY 4.0, behind a terms-of-use consent box - the owner accepts the terms before the first fetch, so no check here fetches the feed",
    "kind": "http_contains",
    "url": "https://data.belgianmobility.io/en/data.html",
    "present": ["api/gtfs/feed/stibmivb/static", "Creative Commons Attribution 4.0 International (CC BY 4.0)", "Source: [PTO Name]", "Terms of Use Consent", "100 requests per day"]
  },
  {
    "id": "brussels-projected-crs",
    "claim": "The City of Brussels projects to UTM 31N (EPSG:32631); metro mode, full coverage, the commune alone",
    "kind": "utm_zone_from_longitude",
    "lon": 4.352,
    "expect": "EPSG:32631",
    "mode": "metro",
    "coverage": "full",
    "scope": "city",
    "crs": "EPSG:32631",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
