# Thessaloniki - build brief

**Band B, owner-approved 2026-10-04** (`docs/decisions_drafts/staging.md`,
"The paused wave's results banded; probes stay stopped (owner)", then
"Geneva (Regional)'s three build calls, and Thessaloniki's licence reading
(owner)": CC BY 4.0 read on the layer's data.gov.gr record, the map portal's
splash read as the web app's terms only, **build from the GeoServer WFS
only**). Brief written 2026-10-04 from the cached layer and Elliniko Metro's
own pages. Run `python scripts/brief_check.py thessaloniki` before writing
any code.

⚠️ **Greece's first city, and the first on this source.** Read `add-country`
and `docs/spain_retrospective.md` (a bespoke municipal source), then
`add-city`, `scaffold-city`, `premises-taxonomy` (a new module keyed on the
layer's activity text), `osm-rail`, `publish-city`. **Matsuyama
(`app/pages/162_Matsuyama_Heatmap.py`) is the page template**: three
layers, Food service, Food shops and Personal services, with food shops as
a partial Retail layer. Antwerp (`docs/build_briefs/antwerp.md`) is the
precedent for a food-shops layer from a food register.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`metro`** | Thessaloniki Metro, driverless, underground; no tram |
| **`coverage`** | **`narrowed`** | Food service and personal services whole, food shops as a partial Retail layer (Matsuyama's shape); no general retail is licensed here |
| **Scope** | **The Municipality of Thessaloniki** (the five municipal communities and the Triandria unit), `SCOPE = "city"` | The layer covers the municipality only: every row carries one of its six community labels |
| **Lines drawn** | **The metro inside the city**, named as the operator names it (call 4) | The owner's scope, 2026-10-04: the five Kalamaria stations are out |
| **Stations** | **13 in the city** (18 on the network, less Kalamaria's 5), by polygon at build | Elliniko Metro's station pages, read 2026-10-04 (below). "18 stations" in the master list is the network total |
| **Rings** | **Halved expected** (desk median gap 506 m on the 13) | The spacing rule (`docs/ring_rules.md`: about 550 m or less), Paris's and Marseille's metro precedent; recompute on the stations drawn |
| **Projected CRS** | **EPSG:32634** (WGS 84 / UTM 34N, derived from 22.94° E) | The layer serves EPSG:2100 (GGRS87 / Greek Grid), but `check_provenance.py`'s CRS invariant accepts only UTM zones and its listed national grids, and 2100 is not listed. Reproject from 2100 on read (Antwerp's Lambert 72 handling); both grids are metric and their scale error here is under 0.03% |
| **Region** | `"Europe"`, country `"Greece"` (new) | A new `docs/data_sources/greece.md` |

**Calls for the owner at build** (each with its precedent and count):
1. **Κυλικείο (canteen), 246 rows: out on R1** (recommended). The Greek
   licence type names a canteen inside another premises (offices, hospitals,
   sports grounds, parks), the R1 row's institutional and staff canteens
   (Madrid's 1,157). Kept, food service would read 3,931.
2. **"Sale of packaged ice cream, soft drinks and certain confectionery in a
   ψιλικά shop", 376 rows: kept as Food shops** (recommended). A ψιλικά shop
   is a convenience store, and convenience stores are kept as food retail
   (NAICS 445131; Japan's コンビニ in `japan_eigyo.py`). **The precedent it
   could break:** Antwerp's and Ghent's "complementary retail" (food beside a
   non-food main trade) left out (owner, 2026-10-03). Some rows may be street
   kiosks (περίπτερα); the layer cannot tell, and fixed kiosks are not the
   mobile-units row. Out, food shops would read 2,055.
3. **Ζαχαροπλαστείο (patisserie), 99, and "coffee sold to passers-by from a
   bread shop or coffee roaster", 37: Food shops** (recommended): the
   premises is a pastry, bread or coffee shop, as Antwerp's bakeries and
   Matsuyama's confectioners. Patisseries with tables could read as food
   service; the layer does not say.
4. **The line's name and the Kalamaria branch.** Elliniko Metro's notice of
   2026-08-26 describes **one line with a branch** (κλάδος) and three
   termini (Νέος Σιδηροδρομικός Σταθμός, Νέα Ελβετία, Μίκρα); Wikipedia (a
   desk read, not a source) calls the branch **Line 2**, sharing the 11
   stations from the New Railway Station to 25ης Μαρτίου with Line 1. The
   operator's own site (THEMA, `thessmetro.gr`) refused curl (below), so the
   public name is unconfirmed. Options: (a) one drawn line, labeled and
   listed in the legend by the operator's public name; (b) M1 and M2 drawn on
   the shared trunk, each labeled and in the legend. Separately: **draw the
   branch beyond the city line without rings** (Geneva's tram 17 to
   Annemasse) **or cut it at the city line** (Matsuyama's lines cut at the
   city line). Recommended: whichever name the operator's own map uses, and
   the cut (the owner set the branch out of scope).
5. **Gate 3 from Elliniko Metro**, the state company that built and owns the
   metro, since the operator's site refuses this machine. Recommended: accept
   it, naming it in `OPERATOR_COUNTS_SOURCE`.
6. **The city boundary source.** Nomarchia and Nea Elvetia sit on the city
   line (below); the polygon decides them. Recommended: the municipality's
   OSM boundary from the build's one Overpass query (Antwerp's route), ODbL,
   the site's own notice. A boundary from another publisher goes to the
   owner first.
7. **The headway is unmeasured** (below): read at build, or the gap
   recorded.
8. **The operator's site**: refused curl's default user agent (403) but
   answered the project's own identified user agent (200), under "Rail"
   below. Whether that counts as a refusal decides whether calls 4, 5 and 7
   can be read from the operator itself.

---

## The one-line summary

**The City of Thessaloniki's active-shop-licence layer, cached: 8,103 rows,
every one with a point and no name field. On the recommended calls, 7,137
kept: 3,685 food service, 2,431 food shops, 1,021 personal services. The
metro inside the city, 13 stations on Elliniko Metro's own list. CC BY 4.0
on data.gov.gr. The work is a small activity taxonomy, the boundary, and
naming the line.**

---

## Business leg - Ενεργές Άδειες Καταστημάτων (active shop licences)

| | |
|---|---|
| **Source** | City of Thessaloniki (Δήμος Θεσσαλονίκης) GeoServer layer `saloniki:tsp_poi_energes_adeies_katastimaton`, title "Ενεργές Άδειες Καταστημάτων", abstract: a point dataset of the locations of shops holding an active licence |
| **Endpoint** | **`https://sdi.thessaloniki.gr/geoserver/wfs` only.** Never the copy on `maps.thessaloniki.gr` (MapServer), whose portal splash forbids redistribution (owner, 2026-10-04) |
| **File** | `data/thessaloniki/raw/tsp_poi_energes_adeies_katastimaton.geojson` (cached 2026-10-04 by one WFS 2.0.0 GetFeature, `OUTPUTFORMAT=application/json`, `SORTBY=gid`; 4,274,423 bytes, sha256 `ff9a494f...9014252e`, meta JSON beside it). One request returned all 8,103 rows (`numberMatched` = `numberReturned`) |
| **Native CRS** | EPSG:2100 (the GeoJSON's `crs` member); extent X 407,485-414,256, Y 4,493,154-4,500,381 |
| **Data date** | **None published.** The page gives the retrieval date and never calls the data current, complete or official (owner, 2026-10-04) |
| **Fetch** | `pipeline/thessaloniki/fetch_sources.py` repeats the one GetFeature (the brief's source, pre-permitted), writes the meta JSON, and refuses a response where `numberReturned` is under `numberMatched`. A step never fetches |

### Fields (13, from DescribeFeatureType)

`gid`, `geom` (point), `objectid`, `kodikos_katasthmatos` (shop code,
unique), `x`, `y`, `address`, `street`, `number`, `zip`, `city`,
`antikeimeno` (the licensed activity, free text from a list of 79 values),
`dimotiki_koinotita` (municipal community).

- **No name field of any kind** (confirmed on the schema; a brief check
  watches it). The activity text holds trade types only: the 79 values were
  read in full.
- **Never read into `processed/`:** `address`, `street`, `number`, `zip`,
  `city`. Step 2 needs the activity, the community, the code and the point.
  The `city` text is noisy (10 rows name Pylaia or Menemeni inside a
  Thessaloniki community); the point and the community decide.

### Measured 2026-10-04 (cached file, `heavy_job.py` label `thes-brief`, peak 0.01 GB)

- **8,103 rows; 8,103 with a point (100%)**; 8,102 also carry `x`/`y`. The
  one row without them has no activity and no code: out as blank.
- **8,070 distinct points**; 26 points carry two to four rows, each a
  different shop code (shops sharing a building).
- **Communities:** Α' 3,033; Ε' 2,488; Δ' 1,311; Β' 796; Γ' 369; Triandria
  106.

### Classification (rough map; the build's taxonomy decides)

Matched by what the premises is (`docs/category_rules.md`):

| Bucket | Rows | Activity values (counts) |
|---|---|---|
| **Food service** | **3,685** | αναψυκτήριο (refreshment bar) 840 (+5 with a pastry workshop); καφετέρια 750 (+76 "or modernized καφενείο"); εστιατόριο 432; καφενείο 424; οβελιστήριο (souvlaki) 223; σνακ μπαρ 176; μπαρ 169 (+2 open bar); ψητοπωλείο 158; πιτσαρία 146; μπουγατσατζίδικο 106; κέντρο διασκέδασης (nightclub, kept by R5) 52 (+5 over 200 seats); ουζερί 44; ψαροταβέρνα 22, οινομαγειρείο 15, ταβέρνα 13; παγωτοπωλείο 11; the long restaurant-and-bar licence 6; ready meals 4; takeaway coffee 3; λουκουματζίδικο 3 |
| **Food shops** (partial Retail) | **1,919** | παντοπωλείο (grocery) 577 (+12 retail food business); πρατήριο άρτου (bread shop) 199; κρεοπωλείο 180; milk and pastry shop 154; supermarket 151; οπωρολαχανοπωλείο 137; pastry shop 95; ιχθυοπωλείο 93; nuts and sweets 79; καφεκοπτείο 73; bottled drinks 60; deli 33; poultry and eggs 26; frozen foods 19; γαλακτοπωλείο 18; olive oil 9; οινοπωλείο 4 |
| **Personal services** | **1,021** | κομμωτήριο 663; manicure-pedicure 160; κουρείο 132; tattoo (its own value, kept by R2) 38; στεγνοκαθαριστήριο 27; beauty 1 |
| **Calls 1-3** | **758** | κυλικείο 246; packaged food in a ψιλικά shop 376; ζαχαροπλαστείο 99; coffee from a bread shop or roaster 37 |
| **Out** | **720** | internet cafés 168 and other recreation 112 (cinemas, theaters, play areas, amusement games, gyms, pools, concert halls; NAICS 71); wholesale and storage 106; vending machines 86; school canteens 66 (R1); funeral 61 (incl. a coffin store); pet shop and second-hand goods 39 (non-food retail: no general retail layer); οίκος ανοχής 30 (licensed brothels, R3); food workshops 19 (manufacturing); "ANEY" 14 (no activity); preparation kitchens 10 (R1); bicycle rental 7; a mobile canteen 1; blank 1 |

- **On the recommended calls: 7,137 kept** (food service 3,685, food shops
  2,431, personal services 1,021). With calls 1 and 2 the other way: food
  service 3,931, food shops 2,055.
- **The master list's rough figures** (about 4,300, 1,900 and 1,000) came
  from the probe's first pass, which counted κυλικείο and the ψιλικά licence
  in food service. This table supersedes them; the build updates the row.
- The build writes the 79-value table as the taxonomy module and runs
  `check_category_continuity.py` against it (a new taxonomy fails until it
  answers every row). Measure the catch-all share with `brief_check.py`'s
  `taxonomy_catchall` kind once the module exists ("ANEY" and blank are the
  only catch-alls seen: 15 rows).

---

## Rail - Thessaloniki Metro

- **Stations, from Elliniko Metro's own pages** (read by curl 2026-10-04):
  the base line's 13, `emetro.gr/?page_id=15008`: Νέος Σιδηροδρομικός
  Σταθμός, Δημοκρατίας, Βενιζέλου, Αγίας Σοφίας, Σιντριβάνι, Πανεπιστήμιο,
  Παπάφη, Ευκλείδης, Φλέμινγκ, Αναλήψεως, 25ης Μαρτίου, Βούλγαρη, Νέα
  Ελβετία; and the Kalamaria extension's 5, `?page_id=15499`: Νομαρχία,
  Καλαμαριά, Αρετσού, Νέα Κρήνη, Μίκρα. **18 on the network.**
- **The Kalamaria branch opened 2026-08-27** (Elliniko Metro's notice of
  2026-08-26, `emetro.gr/?p=36058`), with full hours restored: 05:15 to
  00:30, to 02:00 on Fridays and Saturdays. Its 5 stations are out of scope
  (owner).
- **In the city, a desk check** (station coordinates from Wikipedia, tested
  against the licence layer's own points, which cover the municipality
  only): the 11 trunk stations and Βούλγαρη sit among licence points on
  every side. **Νέα Ελβετία** (nearest licence point 214 m, points in 2 of
  8 directions) and **Νομαρχία** (98 m, 3 of 8) sit on the city line; the
  other four Kalamaria stations are 0.6 to 2.1 km from any licence point.
  So 13 in the city if Nea Elvetia is in and Nomarchia out; **the polygon
  decides, and step 1 asserts the count.**
- **Geometry: OpenStreetMap through `osm-rail`**, one Overpass query for the
  city (lines, stations and the boundary together), never parallel; after a
  504 or 429 wait at least 60 s. No GTFS was probed; a feed not in this
  brief goes to the owner first.
- **Gate 3:** 13 in the city from Elliniko Metro's list (call 5), in
  `OPERATOR_STATION_COUNTS` with `OPERATOR_COUNTS_SOURCE` naming the two
  pages and the date.
- **The operator's site refused:** `www.thessmetro.gr` and `thessmetro.gr`
  answer curl's default user agent with HTTP 403 (a Cloudflare challenge
  page), 2026-10-04. Recorded as a refusal (the coordinator's rule: never
  retried with a browser user agent or any other header). **But
  `brief_check.py`, which sends the project's own identified user agent
  (`expanded-heatmap (github.com/...)`), got HTTP 200 from
  `www.thessmetro.gr` the same day**, in a check written to watch the
  refusal. Nothing was read from that response and the check was removed.
  **Owner call 8:** whether the project's own honest user agent may read the
  operator's pages (the line's public name, stations, headway), or the
  site stays a refusal.
- **Headway: unmeasured.** No reachable operator page states one (Elliniko
  Metro's pages give hours only). Read it at build from an operator page if
  one opens, else record the gap; a driverless metro is not in doubt
  against the 20-minute floor, but the brief does not assert a number.
- Each drawn line gets its permanent on-map label and a legend entry.

---

## Licence - CC BY 4.0 (read 2026-10-04, owner's reading)

- **Set on the layer's data.gov.gr record**
  (`data.gov.gr/dataset/gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton`):
  every resource carries the EU licence URI `CC_BY_4_0`, and every resource
  URL points at `sdi.thessaloniki.gr/geoserver`. A harvester default under
  the City's organization; the City portal's default and Decision
  11654/2026 (Art. 8(3)) agree. The package-level `license_id` is empty;
  the resource-level licence is what was read.
- **What the build must do:** credit the City, link the licence, link the
  source, state that the data was modified, imply no endorsement.
- **The map portal's no-redistribution splash** is read as the web app's
  terms only (owner, 2026-10-04). Tradeoff accepted: if the City meant it
  for all its GIS data, the page comes down on request (the removal rule).
- The row goes in a new `docs/data_sources/greece.md`, with the verdict and
  the notice; the full read is in the staging session's scratchpad
  (`lic_thes/`), summarized in the drafts entry above.

## Notices (the build claims the number in `docs/session_roles.md`)

- **The suggested wording, from the licence read:** "Active shop licenses:
  City of Thessaloniki (Δήμος Θεσσαλονίκης), dataset "Ενεργές Άδειες
  Καταστημάτων"
  (https://data.gov.gr/dataset/gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton),
  licensed under Creative Commons Attribution 4.0 International
  (https://creativecommons.org/licenses/by/4.0/). This map filters the
  data, groups it into categories and aggregates it into a heatmap; the
  City of Thessaloniki has not reviewed or endorsed it." With the retrieval
  date beside it.
- OSM's ODbL notice for the rail and the boundary (the site's own).

## The page (`docs/city_page_format.md`; Matsuyama's bullets)

- **Caption:** the retrieval date of the layer and the OSM fetch date; no
  data date exists to show.
- **The businesses**, proposals for the drafts file where no template
  covers them: the source named as the city's register of shops holding an
  active licence; "shops other than food shops (clothing, electronics,
  pharmacies) do not appear: the Food shops layer is food retail only"
  (Matsuyama's sentence, filled); a dot shows the type of business, never
  its name; the retrieval date, and that the layer publishes no date of its
  own.
- `render_map_help("three business categories (Food shops, Food service and
  Personal services)")`, Matsuyama's string.

## Privacy

- **No name field**; the tooltip shows the activity category only
  (Antwerp's and Berlin's "no names" precedent). The address fields are not
  carried past step 1's read.
- `python scripts/check_personal_exposure.py thessaloniki` after step 2;
  the verdict in the drafts file and `docs/privacy_verdicts.md`.
- **Never print a row.** Field names, activity values and counts only.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for the City's notice, **card face or
caption only** (CC BY 4.0 asks for credit "reasonable to the medium"; a card
that travels without its caption carries it on its face), and the open
terms question: **the map portal's splash**, read as the web app's only
(owner). New inputs: a new country, a new city, a new taxonomy, the notice,
the licence row.

## Still unknown

- ⚠️ **The owner's calls 1-8 above.**
- ⚠️ **The boundary**, Nomarchia and Nea Elvetia, the median gap and the
  ring size.
- ⚠️ **The line's public name and the headway**, while the operator's site
  refuses.
- ⚠️ **The privacy verdict.**

```brief-checks
[
  {
    "id": "thessaloniki-wfs-rows",
    "claim": "THE BUSINESS LEG: the City's GeoServer WFS still serves the active-shop-licence layer with about 8,100 rows (8,103 on 2026-10-04); a count-only request. It fails outside 8,100-8,199: re-measure the buckets if it does",
    "kind": "http_contains",
    "url": "https://sdi.thessaloniki.gr/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=saloniki:tsp_poi_energes_adeies_katastimaton&resultType=hits",
    "present": ["numberMatched=\"81"]
  },
  {
    "id": "thessaloniki-wfs-schema",
    "claim": "The layer still carries the activity text, the community, the shop code and a point, and still has no name field (the privacy reading rests on it)",
    "kind": "http_contains",
    "url": "https://sdi.thessaloniki.gr/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=DescribeFeatureType&TYPENAMES=saloniki:tsp_poi_energes_adeies_katastimaton",
    "present": ["name=\"antikeimeno\"", "name=\"dimotiki_koinotita\"", "name=\"kodikos_katasthmatos\"", "gml:PointPropertyType"],
    "absent": ["name=\"onoma", "name=\"eponymia", "name=\"eponimia", "name=\"eponymo", "name=\"name\"", "name=\"afm\""]
  },
  {
    "id": "thessaloniki-datagov-licence",
    "claim": "The layer's data.gov.gr record still sets CC BY 4.0 (the EU licence URI on its resources) and still points at the sdi.thessaloniki.gr GeoServer, the endpoint the build reads. If it changes, re-read the licence",
    "kind": "http_contains",
    "url": "https://data.gov.gr/api/3/action/package_show?id=gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton",
    "present": ["licence/CC_BY_4_0", "sdi.thessaloniki.gr/geoserver/wfs", "tsp_poi_energes_adeies_katastimaton"]
  },
  {
    "id": "thessaloniki-emetro-base-stations",
    "claim": "Elliniko Metro's page still lists the base line's 13 stations, from the New Railway Station to Nea Elvetia (gate 3's source for the stations in the city)",
    "kind": "http_contains",
    "url": "https://www.emetro.gr/?page_id=15008",
    "present": ["ΝΕΟΣ ΣΙΔΗΡΟΔΡΟΜΙΚΟΣ ΣΤΑΘΜΟΣ", "ΔΗΜΟΚΡΑΤΙΑΣ", "ΒΕΝΙΖΕΛΟΥ", "ΑΓΙΑΣ ΣΟΦΙΑΣ", "ΣΙΝΤΡΙΒΑΝΙ", "ΠΑΝΕΠΙΣΤΗΜΙΟ", "ΠΑΠΑΦΗ", "ΕΥΚΛΕΙΔΗΣ", "ΦΛΕΜΙΓΚ", "ΑΝΑΛΗΨΕΩΣ", "25ΗΣ ΜΑΡΤΙΟΥ", "ΒΟΥΛΓΑΡΗ", "ΝΕΑ ΕΛΒΕΤΙΑ"]
  },
  {
    "id": "thessaloniki-emetro-kalamaria-opened",
    "claim": "Elliniko Metro's notice still says the Kalamaria branch's five stations (out of scope) opened to passengers on 27 August 2026, with the line's three termini",
    "kind": "http_contains",
    "url": "https://www.emetro.gr/?p=36058",
    "present": ["27 Αυγούστου 2026", "Νομαρχία, Καλαμαριά, Αρετσού, Νέα Κρήνη και Μίκρα", "Νέα Ελβετία"]
  },
  {
    "id": "thessaloniki-projected-crs",
    "claim": "Thessaloniki's derived UTM zone is 34N (EPSG:32634) and the build projects in it, reprojecting from the layer's EPSG:2100 (not a grid the provenance check accepts); metro mode, narrowed coverage, city scope",
    "kind": "utm_zone_from_longitude",
    "lon": 22.94,
    "expect": "EPSG:32634",
    "mode": "metro",
    "coverage": "narrowed",
    "scope": "city",
    "crs": "EPSG:32634",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
