# Gelsenkirchen - build brief

**Band B, owner-approved 2026-10-04** (`docs/city_master_list.md`, Band B;
`docs/decisions_drafts/staging.md`: "Germany north" (to C with a licence
read), "Bremen to B, retail only; Gelsenkirchen's licence settled; Kurashiki
measured", "Probe slip in the Gelsenkirchen measurement" and "Gelsenkirchen
to B; Wuppertal discarded"). Brief written 2026-10-05 by staging from the
five layers cached in `data/gelsenkirchen/raw/` (fetched 2026-10-04 22:23
UTC, `gelsenkirchen_gewerbe_meta.json`), counts and schema read live from the
city's WFS (hit counts only, no feature), the Ruhr portal's catalogue records
and BOGESTRA's timetable index page. Nothing was downloaded for this brief
and no Overpass query was run. Run `python scripts/brief_check.py
gelsenkirchen` before writing any code.

**Germany's second city, and its first city survey.** Berlin is a chamber's
register; this is the City of Gelsenkirchen's own survey of its commercial
premises, kept for retail and centres planning (the "Infrastrukturdatenbank").
The shape is **Liège's and Charleroi's** (a municipal field survey keyed to
designated centres, vacant units in the same file) with **Brussels'** sign
names. Read `docs/build_briefs/liege.md` (the survey reader, the centres
gap, the sign rule) and `docs/build_briefs/berlin.md` (the German rows, the
cut at the border). Skills: `add-city`, `scaffold-city`, `tram-city`,
`osm-rail`, `premises-taxonomy` (a new module), `publish-city`.
**Templates:** Liège (`pipeline/liege/`) for the business leg and the page;
Zurich or Florence (`pipeline/osm_tram.py` wrappers) for the OSM tram step 1.

---

## For the owner, with the build

✅ **The six open calls answered as recommended (owner, 2026-10-05, calls
15-20; `docs/decisions_drafts/staging.md`):** (1) a sign that reads as a
person's name shows its category instead, stored as keys (Liège's and
Brussels' rule); (2) the OSM boundary from the build's one Overpass query;
(3) lines 302, 107 and U11 **cut at the city line**, as Berlin at its Land
border; if 107 is left a stub, bring it back with Rotthausen's case
measured; (4) `mode` stays `tram` if OSM types U11 light rail; (5)
Fax, Info, Internetbeschreibung, Strasse and ADRKOMBI join the never-read
list, the build fetches only the fields it uses, and the 2026-10-04 cache is
kept until the owner says otherwise; (6) gate 3 for 107 and U11 from
**Ruhrbahn's current timetables** (a page read, the operator's own; name the
URL in the build's notes). The six page sentences stay proposals for review
time.

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | Trams 301, 302 and 107 carry the network; U11 is an Essen Stadtbahn line whose Gelsenkirchen end is a few stops (open call 4) |
| **`coverage`** | **`narrowed`**, `categories` **"Personal services thin"** | All three buckets from one survey, personal services measured thin (104 rows, recorded mainly inside designated centres). Berlin's value; New Orleans' and Kansas City's shape ("All three, one thin" is `narrowed`, `tram-city` section 5) |
| **Scope** | **The City of Gelsenkirchen**, `SCOPE = "city"` | The survey covers the city only. Bochum and Essen, where 302, 107 and U11 run on, were discarded on absence (2026-10-04), so no regional page is possible |
| **Lines** | **301, 302, 107, U11**, each labeled on the map and in the legend | BOGESTRA's timetable index (below). How lines that cross the city line are drawn is open call 3 |
| **Rings** | **By the spacing rule**; halved expected | Urban tram spacing; the median nearest-neighbour gap is measured on the stops drawn (`tram-city` section 3). No thinning (owner's trams-only calls) |
| **Projected CRS** | **EPSG:32632** (WGS 84 / UTM 32N) | Derived from the survey's mean longitude, 7.078 E (zone 32). The layers are stored in EPSG:25832 (ETRS89 / UTM 32N); reprojecting 25832 to 32632 is sub-metre, Berlin's 25833-to-32633 handling |
| **Region** | `"Europe"`, country `"Germany"` | `add-city`: a European city tags Europe, no country region. Berlin, the German precedent, is Europe with no tier |
| **Label tier** | **None by default**; `"minor"` only if `check_macro_labels.py` cannot place the pill | Europe's small tram cities (Odense, Liepāja, Daugavpils) carry no tier; a minor tag here would only take the pill out of Global (its own region is Europe). Decided by `check_macro_labels.py` at 375, 768 and 1200, never by eye |
| **`record_kind`** | "Street survey or census" | Brussels', Charleroi's and Liège's value |
| **`placement`** | "Survey coordinates (100%)" | Every one of the 2,312 business rows carries a point |
| **`data_age`** | A proposal: "Undated survey (earlier files 2024)" | The owner's currency call (below); the wording is the build's proposal |

### Owner calls already made (do not re-ask)

- **Band B, all three buckets, personal services a measured gap** (owner,
  2026-10-04).
- **Licence settled: Datenlizenz Deutschland - Zero - Version 2.0** on every
  city record in the city's catalogue and on the Ruhr portal; open.nrw's
  "other-closed" is a harvester default where the Ruhr portal's DCAT export
  carries no licence (staging's licence read, 2026-10-04).
- **Currency dated from the earlier files' 2024 labels, disclosed**: the page
  states the survey is undated (owner, 2026-10-04). The alternative was waiting
  for the city's retail plan on a host that refuses curl.
- **The 188 uncategorised rows are left out and disclosed** (54 food, 134
  services; owner, 2026-10-04).
- **Telefon, EMail, Internet and `DL_Vermarktung` are never read** (the probe
  slip of 2026-10-04: `DL_Vermarktung` holds a person's name and phone
  numbers).
- **Standing:** trams-only maps; no stop thinning; rings by the spacing rule;
  a route drawn only if it runs at least every 20 minutes by day (all four
  do); feeds rolling; the category rules (`docs/category_rules.md`); Europe as
  the region.

### Calls open for the owner at build (each with a recommendation)

1. **The privacy rule on `Name`** (open at build per the row). Recommended:
   **Liège's and Brussels' sign rule**: the dot shows the name on the sign, and
   a sign that reads as a person's own name shows the category instead
   (`config.PERSON_NAMED`, keys from `pipeline/name_keys.py`, never names).
   Tradeoff: the build reads the flagged names by eye (up to 324, below)
   against Berlin's structural rule (category only on every dot), which needs
   no reading but drops every shop's sign, including chains and brands.
2. **The city boundary.** Recommended: **the city's OpenStreetMap boundary
   from the build's one Overpass query** (Antwerp's and Thessaloniki's route;
   ODbL, the site's own notice, no new publisher). The alternative is
   Geobasis NRW's official municipal boundary (Berlin used ALKIS, its Land's
   equivalent, dl-de/zero-2.0): more authoritative, but a source this brief
   does not name, so it goes to the owner first. The infrastructure database
   holds no city-boundary layer (its 97 collections were listed 2026-10-05).
3. **Lines that cross the city line: 302 into Bochum (to Langendreer), 107
   into Essen (to Bredeney), U11 into Essen (to Messe/Gruga).** Recommended:
   **cut every line at the city line, Berlin's precedent** (lines cut at the
   Land border, the stations beyond listed as excluded on the page). Every
   tram stop inside Gelsenkirchen gets rings, and the stops beyond are listed
   as outside. Tradeoff: the tram kit drew short overhangs to their ends
   (Florence's T1, Geneva's 17, Göteborg's 4 and 12, Den Haag's 1: calls 17,
   21, 26) and left out lines mostly outside the scope as stubs (Den Haag's E,
   Zurich's 20: calls 22, 25). Here the overhangs run deep into two other
   cities, and a stub rule could drop 107 or U11 together with Gelsenkirchen
   stops that no other line serves (107 is ASSERTED to serve Rotthausen, a
   designated district centre). The build brings, per line, its stops inside
   and outside the city and the stops inside that it alone serves.
4. **`mode` if U11 is drawn.** `tram-city` section 1: `mode` is the highest
   order the map draws, read from what step 1 keeps (OSM `route=`), never from
   a marketing name. BOGESTRA files U11 under "U-Bahn", which decides nothing.
   If OSM types U11 `route=light_rail` (ASSERTED) and it is drawn, the rule
   gives `light_rail`. Recommended: **keep `tram`**, on the owner's
   "substantial" principle for Japan (2026-10-02: a second mode beside the
   trams sets `mode` only where it is the city's main network) and Dublin's
   precedent. Tradeoff: the macro dot's color would understate the one
   Stadtbahn line, which inside the city is a short end section.
5. **Fields never read, widened, and a reduced fetch.** Recommended: add
   **`Fax`, `Info` and `Internetbeschreibung`** (a contact field and two
   free-text fields) and the address fields **`Strasse` and `ADRKOMBI`** to
   the never-read list, and have `fetch_sources.py` request only the
   properties the build uses (WFS `PROPERTYNAME`, or the OGC API's property
   selection if GeoServer honours it; test at build), so contact fields never
   reach disk. Tradeoff: none in the data the map uses; the full copies cached
   on 2026-10-04 in the shared `data/` folder stay until the owner says
   whether to delete them once the reduced fetch reproduces the counts.
6. **Gate 3's sources for 107 and U11.** BOGESTRA's index links a 107
   timetable file dated 2016 (`107-Inter-20160614.pdf`); both lines are
   ASSERTED to be Ruhrbahn's (Essen). Recommended: **read Ruhrbahn's own
   current 107 and U11 timetables for the count only**, a source this brief
   cannot yet name by URL, so the owner approves it first; failing that,
   `OPERATOR_COUNTS_GAP` records what was looked for.

---

## The one-line summary

**The City of Gelsenkirchen's commercial-premises survey: 1,772 storefronts
(food service 346, retail 1,322, personal services 104), every one a point
with a sign name, undated (earlier files labelled 2024), dl-de/zero-2.0.
Trams 301, 302 and 107 and Stadtbahn U11, about 60 stops in the city. The work
is a small taxonomy, the sign rule, the cut at the city line and the dating
sentence.**

---

## Business leg - the Infrastrukturdatenbank's commercial layers

| | |
|---|---|
| **Publisher** | Stadt Gelsenkirchen (the Ruhr portal's records name it publisher and contact) |
| **Service** | GeoServer OGC API Features, `https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/ogc/features/v1/collections/<layer>/items`; the same layers by WFS 2.0 at `https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs` (capabilities keyword `ge:constraints_dl_zero_de`, `Fees` NONE) |
| **Catalogue** | `opendata.ruhr` records `gewerbe-gastronomie-der-stadt-gelsenkirchen`, `gewerbe-einzelhandel-der-stadt-gelsenkirchen`, `gewerbe-dienstleistung-der-stadt-gelsenkirchen` (plus `leerstande-...` and `gewerbestandorte-...`), each `license_id` `dl-zero-de/2.0`; record `issued` 2026-09-16 (publication metadata, not a survey date) |
| **Cached** | `data/gelsenkirchen/raw/`: `gewerbe_gastronomie.geojson` (403 rows, 531,085 bytes), `gewerbe_einzelhandel.geojson` (1,318, 1,719,483), `gewerbe_dienstleistung.geojson` (591, 751,623), `gewerbe.geojson` (2,787, 3,549,872), `gewerbe-leerstand.geojson` (467, 566,538); sha256 in `gelsenkirchen_gewerbe_meta.json`. Live WFS hit counts on 2026-10-05 match: 403, 1,318, 591. **Re-read 2026-10-07 (the Abroad build): the services layer holds 594 rows, 122 of them without `KAT_DL`** (134 on 2026-10-05): the city edits the layer, so the build's own reduced fetch (call 5) gives the figures |
| **Fetch** | `pipeline/gelsenkirchen/fetch_sources.py` takes the **three themed layers only**, paged at 1,000 (`limit`/`startIndex`), from the city's own host (pre-permitted: named here). A step never fetches |
| **Licence** | **Datenlizenz Deutschland - Zero - Version 2.0** (`https://www.govdata.de/dl-de/zero-2-0`): any use, no condition, no attribution required |

### The five layers and how they relate

- **`gewerbe` (2,787) is the union of the other layers**: the 403 food, 1,318
  retail and 591 services rows by `id` (no overlap between the three), plus
  475 rows typed `Leerstand` (vacant). **`gewerbe-leerstand` (467) is a subset
  of those vacant rows** (every point coincides with a `gewerbe` point; it has
  no `id` field).
- **The build reads the three themed layers** and never `gewerbe` or
  `gewerbe-leerstand`: vacant units are not storefronts (Liège's and
  Charleroi's "cellule vide").
- Every themed layer has a unique integer `id` on every row, and
  `GEWERBETYPUSBEZ` is constant per layer (`Gastronomie`, `Einzelhandel`,
  `Dienstleistung`). Step 2 asserts both.

### Fields (49 on the themed layers; 48 on `gewerbe-leerstand`, no `id`)

`id`, `Name`, `ArtId`, `ARTBEZ`, `TraegerId`, `TRAEGERBEZ`, `OrtId`,
`ADRKOMBI`, `PLZ`, `Strasse`, `X`, `Y`, `Info`, `Internetbeschreibung`,
`Veroeffentlicht`, `Telefon`, `Fax`, `EMail`, `Internet`,
`stadtDienststelle`, `WEinheit`, `LageId`, `LAGEBEZ`, `GewerbetypusId`,
`GEWERBETYPUSBEZ`, `Letzte_Nutzung`, `HauptwarengruppeId`,
`HAUPTWARENGRUPPEBEZ`, `KernsortimentId`, `KERNSORTIMENTBEZ`,
`SortimentsrelevanzId`, `SORTIMENTSRELEVANZBEZ`, `BedarfsstufeId`,
`BEDARFSSTUFEBEZ`, `VKF`, `GVKF`, `Grundversorgung`, `Fl_Gastraum`, `Nutzfl`,
`Schaufenster`, `KAT_GASTRO`, `Gastro_Sitzplaetze`, `Gastro_Außenbereich`,
`Lage_Gastro_ID`, `DL_Vermarktung`, `KAT_DL`, `FotoVorhanden`, `FotoId`,
`Istonline`. The WFS schema adds the geometry column `Shape`.

**How a build reads them:**

| Read | Fields |
|---|---|
| **Classification** | `KAT_GASTRO` (food), `HAUPTWARENGRUPPEBEZ` and `KERNSORTIMENTBEZ` (retail: main goods group and core assortment), `KAT_DL` (services) |
| **Shown** | `Name` (the sign, under call 1) and the bucket label; nothing else |
| **Measured, never written to `outputs/`** | `LAGEBEZ` (centre class, below), `PLZ` (scope cross-check), `TRAEGERBEZ` (`Sonstiges` or `privat`; 6 kept rows are `privat`, meaning not documented) |
| **Asserted** | `Veroeffentlicht` and `Istonline` are `True` on every row (the city's own publish flags; a row not marked published must not be drawn); `GEWERBETYPUSBEZ` per layer |
| **Never read** | `Telefon`, `EMail`, `Internet`, `DL_Vermarktung` (owner); proposed in call 5: `Fax`, `Info`, `Internetbeschreibung`, `Strasse`, `ADRKOMBI` |
| **Not used** | The retail planning fields (`VKF` sales floor, `GVKF`, `Grundversorgung`, `SORTIMENTSRELEVANZBEZ`, `BEDARFSSTUFEBEZ`), `WEinheit`, `OrtId`, `FotoVorhanden`, `FotoId`, `stadtDienststelle`, and the empty ones |

**No date field of any kind.** `Letzte_Nutzung` ("last use", for vacancies)
is empty on every row; the OGC collection records carry a spatial extent and
no temporal one; the catalogue's `issued` and `modified` (2026-09-16) are
publication metadata. One sign that the survey was assembled over time:
`BEDARFSSTUFEBEZ` is coded two ways in retail ("kurzfristig" 110,
"mittelfristig" 64, "langfristig" 80, against "kurzfristige Bedarfsstufe" 614
and its two siblings 449), which says nothing about either part's date.

### CRS

- **Geometry**: GeoJSON points in CRS84 (lon/lat), the OGC API default.
  **Storage CRS EPSG:25832** (the collection record's `storageCrs`).
- **`X`/`Y` are EPSG:25832 eastings and northings** (about 368,000 E,
  5,708,000 N) and agree with the geometry to 5 mm on all 1,772 kept rows
  (median 4 mm). Step 2 reads the geometry and may assert the agreement as a
  trap check.
- **Project in EPSG:32632** for every buffer and distance (7.078 E, UTM 32N).
  Never measure in 4326.

### Buckets under `docs/category_rules.md` (re-measured 2026-10-05 from the cache)

Every figure below reproduces the master-list row exactly: **food 346, retail
1,322, personal services 104 (1,772); 188 uncategorised out.**

| Bucket | Rows | Composition |
|---|---|---|
| **Food service** | **346** | `KAT_GASTRO`: Restaurant 112, Imbissbetrieb 101, Bar/Kneipe/Wirtshaus 69, Café/Eisdiele 51, Systemgastronomie 13 |
| **Retail** | **1,322** | All 1,318 retail-layer rows, plus **4 car dealers** from the services layer (`KAT_DL` "KFZ-Handel / Autohäuser inkl. Krafträder", R4). Main goods groups: Nahrungs- und Genussmittel 554, Bekleidung 139, Gesundheit und Körperpflege 87, medizinische und orthopädische Artikel 66, Elektronik / Multimedia 63, Baumarktsortimente 54, Möbel 53, and 14 smaller groups |
| **Personal services** | **104** | `KAT_DL`: Friseur, Barbershop **88**; Kosmetik-, Nagel-, Fußpfl.-, Haarentf.-, Sonnenst. **4**; Textil- und Lederreinigung **6**; Tattoo-/Piercingstudio **6** (own code, kept) |

**Left out (540 of the 2,312 business rows):**

- **Uncategorised, 188** (owner): `KAT_GASTRO` empty on 54 food rows,
  `KAT_DL` empty on 134 services rows. **All 54 food rows lie in the two main
  centres** (`HZ_`); the 134 services rows lie in centres (119) or integrated
  locations (15). No `Info` text on the food rows; 3 services rows carry some
  (not read).
- **Lodging, 3**: `Hotel/Gasthof/Pension` (the lodging row).
- **Services out, 349**, each by its rule: gambling (Spielhallen, Casinos 34;
  Wettbüros 16; R5); funeral (Bestattungsinstitut 12); repairs and
  alterations (Änderungsschneiderei 18, Schuster 2, Schlüsseldienst 3,
  KFZ-Reparatur 1); finance and offices (Versicherung 35, Bankfiliale 24,
  Reisebüro 29, Immobilienmakler 11, Rechtsanwälte 16, Sonstige freie Berufe
  7, Werbung 1, Copyshop 3, Postfiliale 2, Fotograf 7); health and care
  (Sonstige Einrichtungen Gesundheit, Soziales, Sport 36; Pflegedienst 17;
  Physiotherapie 13; Arztpraxen 6; Zahnarztpraxen 3); recreation (Fitness 4,
  Kampfsport 1); education and religion (Fahrschulen 17, Religiöse
  Institutionen 16, Bildung 3, Musikschulen 1, Kindergärten 1); trades
  (Sonstiges Handwerk 6, Elektroinstallateur 2); the services catch-all
  (Sonstige nicht genannte Dienstleistungen 2, R2).
- **Kept by the rules, worth a line in the taxonomy:** sex shops
  (Erotikartikel 4, retail), pharmacies (pharmazeutische Artikel 54),
  opticians and medical supply (in the two health groups), car parts
  (Kfz-Zubehör 10), weapons and angling (2), retail's own catch-all
  (`HAUPTWARENGRUPPEBEZ` "Sonstiges" 8, 0.6%, kept on the Rev. 2.1 precedent;
  nothing marks it as non-store). No fuel station, nonstore seller, market
  stall or named adult venue appears. Commercial massage has no code of its
  own (it may sit in the beauty code, the health catch-all or the
  uncategorised rows).
- **Every place a rule lands is a module entry**: a new
  `pipeline/taxonomies/gelsenkirchen_idb.py`, keyed on (layer, category
  label), the labels kept in German as the city writes them (premises-taxonomy;
  the `taxonomy_catchall` check cannot read an OGC API or WFS yet, as Berlin
  found, so the shares above are this brief's). `check_category_continuity.py`
  must answer it before the push.

### The personal-services gap, measured (the centres)

`LAGEBEZ` places each row in the city's centres hierarchy: two main centres
(`HZ_Gelsenkirchen City`, `HZ_Gelsenkirchen Buer`), four district centres
(`STZ_`), seven local-supply centres (`NVZ_`), five prospective local centres
(`persp. NVZ_`), three supplementary sites (`Erg.St._`), integrated locations
(`int`) and non-integrated locations (`niL`).

| | HZ + STZ + NVZ | + prospective NVZ | + supplementary sites | `int` | `niL` |
|---|---|---|---|---|---|
| Services layer, 591 | 81.4% | 81.9% | **82.2%** | 17.4% | 0.3% |
| Retail layer, 1,318 | 47.3% | 49.5% | **52.6%** | 39.8% | 7.5% |
| Food layer, 403 | 51.6% | 52.6% | 53.3% | 37.5% | 9.2% |
| Personal services bucket, 104 | 80.8% | 81.7% | 82.7% | 17.3% | 0.0% |
| Retail bucket, 1,322 | 47.1% | 49.4% | 52.4% | 39.9% | 7.6% |
| Food bucket, 346 | 43.9% | 45.1% | 46.0% | 43.6% | 10.4% |

**The row's "82% against 53%" is the widest reading** (every centre class
except `int` and `niL`); on the designated centres alone it is 81% against
47%. Either way, services were recorded chiefly inside centres while retail
and food reach the whole city, so **personal services away from the centres
are thin**, and the page says so (a proposal, below). 88 hairdressers in a
city of about 260,000 is the other sign.

### Placement and stacking

- **Every row has a point** (2,312 of 2,312). 12 points hold 2 kept rows each
  (24 rows); no point holds more. No stacked-address problem (Berlin's 65%).
- `PLZ`: 1 kept row carries a postcode outside Gelsenkirchen's set (45866) and
  9 carry none; the boundary polygon (call 2) decides scope, never `PLZ`. The
  collection's extent (6.995-7.136 E, 51.485-51.622 N) sits inside the city.

---

## Privacy (`check_personal_exposure.py`, verdict before publishing)

- **`Name` is filled on every row** (1,772 of 1,772 kept; 2,312 of 2,312 in
  the three layers): the survey's sign name, with **no holder, owner or
  registrant column** to fall back to, so Los Angeles' failure mode cannot
  occur. Register it as Brussels and Zurich are (`raw=None, trade=None,
  owner=None`), with the address check skipped (no address reaches the map).
- **Measured on the kept rows, counts only (no name was printed or stored):**

  | | Food 346 | Retail 1,322 | Personal 104 | All 1,772 |
  |---|---|---|---|---|
  | Person-shaped, the project heuristic (`looks_personal`) | 87 | 385 | 37 | **509** |
  | of which no German trade word | 71 | 230 | 23 | **324** |
  | A company form (GmbH, AG, KG, UG, e.K., ...) | 4 | 8 | 1 | 13 |
  | One word | 70 | 478 | 10 | 558 |
  | "Inh." or "Inhaber" | 0 | 0 | 0 | 0 |
  | A phone number, email or web address inside the name | 0 | 0 | 0 | 0 |

  The heuristic's organisation words are English, so most of the 324 will be
  brands and German trade names (Zurich's note: about 900 person-shaped names
  there were trade names). **The build reads the flagged names by eye** and
  puts the person-like signs in `config.PERSON_NAMED` as keys (call 1). 1,934
  distinct names over 2,312 rows; 143 names repeat (chains and generic signs),
  the largest 42 times.
- **Suspects first**: the personal-services bucket (hairdressers and beauty,
  23 person-shaped names with no trade word), then food's one-word signs.
- **Contact and free-text fields never leave `raw/`** (the owner's four; call
  5's five). The probe slip of 2026-10-04 is why.
- Record the verdict in the session's drafts file and
  `docs/privacy_verdicts.md`.

---

## Rail - BOGESTRA's and Ruhrbahn's lines in Gelsenkirchen

**Read 2026-10-05 from BOGESTRA's line-timetable index**
(`https://www.bogestra.de/fahrplan-mobilitaet/linienfahrplaene`, curl, the
project's agent; the PDFs were not opened):

| Line | BOGESTRA's route description | Timetable file on the index | Day headway (the row, BOGESTRA's timetables) |
|---|---|---|---|
| **301** | Gelsenkirchen Hbf - Bismarck - Erle - Buer - Horst | `301-Inter-20260902.pdf` | every 7-8 min |
| **302** | GE-Buer - Schalke - Gelsenkirchen Hbf - BO-Wattenscheid - Bochum Hbf - Altenbochum - Laer - Langendreer | `302-Inter-20260614.pdf` | every 7-8 min |
| **107** | Gelsenkirchen Hbf - Essen-Katernberg - Zollverein - Essen Hbf - Bredeney | `107-Inter-20160614.pdf` (dated 2016) | every 10 min |
| **U11** | Gelsenkirchen-Horst - Essen-Karnap - Altenessen - Essen Hbf - Rüttenscheid - Messe/Gruga (filed under "U-Bahn") | `U11-20250712.pdf` | every 10-15 min |

- **About 60 stops in the city** (the row; the border stops' side ASSERTED).
  301 is ASSERTED wholly inside the city (every place in its description is a
  Gelsenkirchen district); 302 runs on into Bochum, 107 and U11 into Essen.
- **Geometry and stops: OpenStreetMap through `osm-rail`**, wrapped on
  `pipeline/osm_tram.py` (`routes=("tram", "light_rail")` if U11 is drawn).
  **One Overpass query for the city, never parallel; after a 504 or 429 wait at
  least 60 s.** A GTFS feed (VRR's, or Germany's national one) is not in this
  brief and goes to the owner first; OSM's notice is the site's own.
- **Traps to expect (ASSERTED):** the city-centre Stadtbahn tunnel (Hbf and
  the stops north of it, shared by 301, 302 and 107) puts underground
  platforms beside surface stops of the same name, so collapse by name within
  200 m (Aarhus's rule) and exit on a wider spread; U11 meets 301 at Horst;
  OSM may carry several relations per ref (`load_osm_line_shapes` draws the
  one with most geometry); every relation is kept or `NOT_DRAWN` with a
  reason.
- **Frequency:** all four lines run every 15 minutes or better by day, over
  the kit's 20-minute floor. The page states the range.
- **Gate 3 (required, `tram-city` section 2):** BOGESTRA's own timetable files
  for 301, 302 and U11, read at build for the per-line stop count only, never
  republished, with `OPERATOR_COUNTS_SOURCE` naming file and date; 107 and U11
  per call 6. Count the whole line before the scope split.
- **Not drawn:** buses (including BOGESTRA's night and express lines), the
  S-Bahn and regional trains at Gelsenkirchen Hbf and Buer: commuter and
  national rail, out as everywhere.
- **Colors:** OSM's `colour` tags, else the project's palette; two lines with
  one color are refused (`pipeline/linecolour.py`, `check_map_markup.py`).

---

## Licence and notices

- **Datenlizenz Deutschland - Zero - Version 2.0: no notice is required**, no
  attribution, no condition. Recorded in `docs/data_sources/germany.md` beside
  Berlin's rows, with the verdict "PERMITTED, nothing to display".
- **What the project shows anyway** (Berlin's precedent, where the owner
  approved a courtesy credit for a CC0 register): a credit to **Stadt
  Gelsenkirchen** with the licence name linked to
  `https://www.govdata.de/dl-de/zero-2-0`, in the caption under the map. It
  also satisfies the stricter reading in staging's licence read (the city's
  website terms defer to each dataset's metadata but name the BY 2.0 version,
  which asks for the publisher's name and the licence link). No city logo or
  coat of arms. The wording follows Berlin's "Business data: IHK Berlin (CC0)"
  form; a new wording is a proposal.
- **OpenStreetMap** for the lines, the stops and (call 2) the boundary: the
  site's own ODbL notice.
- **BOGESTRA's timetables** (and Ruhrbahn's, call 6) are read for gate 3 only,
  never republished: a supporting-source row each in
  `docs/data_sources/germany.md` (`#support-sources`), with their terms as
  read; no BOGESTRA or Ruhrbahn logo or line signet.
- **Removal requests** from the city or a business are honoured first
  (`CLAUDE.md`, the removal rule).

## The page (`tram-city` section 6, `docs/city_page_format.md`)

Braces are the build's own measurements. Sentences outside the template are
**proposals**, flagged in the session's drafts file.

- **Caption (proposal for the dating clause):** "Shops, food service and
  personal services from the City of Gelsenkirchen's survey of commercial
  premises (Datenlizenz Deutschland - Zero - Version 2.0), undated, fetched
  **{date}**; the tram lines and their stops from OpenStreetMap, fetched
  **{date}**."
- **The trams:** "{4} lines are drawn, **301, 302, 107 and U11**, each labeled
  on the map and in the legend, redrawn from OpenStreetMap's route geometry{,
  in OpenStreetMap's own colors}." (Proposal for the operators: "BOGESTRA's
  trams 301 and 302, Ruhrbahn's tram 107 and its Stadtbahn line U11", since
  the template names one operator.) "Trams run about every 7 to 15 minutes by
  day." "Buses and suburban and regional trains are not drawn."
  "Gelsenkirchen has no metro, so its trams are its rapid transit, as in Riga.
  Every tram stop here gets rings." The halved-rings bullet with {spacing}. "The
  map covers the **City of Gelsenkirchen**." Under call 3 as recommended: "302
  runs on into Bochum, and 107 and U11 into Essen, so their {k} stops there
  are left out." with the template's "listed below" sentence adapted to a cut
  line (a proposal).
- **The businesses:** the source in Liège's wording, adapted: "Businesses come
  from the City of Gelsenkirchen's survey of its shops, food service and
  services, under the name on each sign." (Proposal.) "A sign that reads as a
  person's own name shows the business's category instead." (Liège's
  sentence.) **The thin bucket** (proposal): "**Personal services are thin
  on this map.** The survey recorded services mainly in the city's designated
  shopping centers, so hairdressers and other personal services away from
  them are missing." The left-out rows (proposal): "{188} surveyed businesses
  with no category are left out." Then "**About {...} storefronts ... sit
  within a ring.**"
- **Reading the density:** the dating sentence, Göteborg's and Den Haag's
  shape (proposal): "**The survey carries no date.** The city publishes it
  without one, and its earlier files were labeled 2024, so businesses that
  opened or closed since then may be missing or still shown." Then "**Read
  the density as a survey, not a register.**" with the source's caveat (a
  proposal: the template says "a register, not a street survey").
- `render_map_help("three business categories (Retail, Food service and
  Personal services)")`.
- **What Is Excluded** (`### Gelsenkirchen - ...` in
  `docs/excluded_categories.md`): the uncategorised 188, the hotels, the
  services left out by rule, the vacant units, and the centres gap in the
  city's own section; the rail half (the lines beyond the city line, the
  commuter rail) under the rail heading. `check_scope_disclosure.py` decides.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

- **The Stadt Gelsenkirchen credit: caption** (a courtesy, not required).
- **OSM's notice: caption.**
- **Open terms question: none** (licence settled 2026-10-04); gate-3 sources
  per call 6.

## What the build must still measure

- ⚠️ **Calls 1 to 6** above, with their numbers.
- **Scope by polygon**: the boundary (call 2); storefronts and stops inside;
  the stops per line inside and outside, and those only one line serves (call
  3).
- **Stops after collapse**, the median gap and the ring size; gate 3 against
  the operators' counts; OSM's `route=` per line and the resulting `mode`
  (call 4).
- **The reduced fetch** reproducing 403, 1,318 and 591 rows and the bucket
  counts (call 5).
- **The privacy verdict**, names read by eye into keys.
- **The in-ring share**, and Liège's "measure first" figure if the owner wants
  it: personal services inside the rings, inside and outside the centres.
- `check_category_continuity.py` on the new taxonomy; `check_macro_labels.py`
  for the label (tier); `check_provenance.py` naming the city OK.

```brief-checks
[
  {
    "id": "gelsenkirchen-licence-gastro",
    "claim": "The Ruhr portal's record for the city's food layer is Datenlizenz Deutschland Zero 2.0, published by Stadt Gelsenkirchen, and points at the OGC API collection",
    "kind": "http_contains",
    "url": "https://opendata.ruhr/api/3/action/package_show?id=gewerbe-gastronomie-der-stadt-gelsenkirchen",
    "present": ["dl-zero-de/2.0", "Stadt Gelsenkirchen", "collections/gewerbe_gastronomie/items"]
  },
  {
    "id": "gelsenkirchen-licence-retail",
    "claim": "The Ruhr portal's record for the city's retail layer is Datenlizenz Deutschland Zero 2.0",
    "kind": "http_contains",
    "url": "https://opendata.ruhr/api/3/action/package_show?id=gewerbe-einzelhandel-der-stadt-gelsenkirchen",
    "present": ["dl-zero-de/2.0", "Stadt Gelsenkirchen", "collections/gewerbe_einzelhandel/items"]
  },
  {
    "id": "gelsenkirchen-licence-services",
    "claim": "The Ruhr portal's record for the city's services layer is Datenlizenz Deutschland Zero 2.0",
    "kind": "http_contains",
    "url": "https://opendata.ruhr/api/3/action/package_show?id=gewerbe-dienstleistung-der-stadt-gelsenkirchen",
    "present": ["dl-zero-de/2.0", "Stadt Gelsenkirchen", "collections/gewerbe_dienstleistung/items"]
  },
  {
    "id": "gelsenkirchen-wfs-licence-keyword",
    "claim": "The city's WFS declares the dl-zero-de constraint and no fees",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&request=GetCapabilities",
    "present": ["ge:constraints_dl_zero_de", "<ows:Fees>NONE</ows:Fees>", "Stadt Gelsenkirchen"]
  },
  {
    "id": "gelsenkirchen-ogc-crs-no-date",
    "claim": "The food collection is stored in EPSG:25832 and publishes a spatial extent but no temporal one (the survey is undated; if a date appears, the page's dating sentence changes)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/ogc/features/v1/collections/gewerbe_gastronomie?f=application/json",
    "present": ["\"storageCrs\":\"http://www.opengis.net/def/crs/EPSG/0/25832\"", "Standorte von Gastronomiebetrieben in Gelsenkirchen"],
    "absent": ["temporal"]
  },
  {
    "id": "gelsenkirchen-schema",
    "claim": "The layers' schema carries the classification, centre and name fields the build reads, the contact and free-text fields it never reads, and no date field",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typenames=gewerbe_gastronomie",
    "present": ["name=\"Name\"", "name=\"KAT_GASTRO\"", "name=\"KAT_DL\"", "name=\"HAUPTWARENGRUPPEBEZ\"", "name=\"KERNSORTIMENTBEZ\"", "name=\"LAGEBEZ\"", "name=\"GEWERBETYPUSBEZ\"", "name=\"Veroeffentlicht\"", "name=\"Telefon\"", "name=\"DL_Vermarktung\""],
    "absent": ["datum", "erfasst", "aktualisiert"]
  },
  {
    "id": "gelsenkirchen-hits-food",
    "claim": "The food layer holds 403 rows (2026-10-04 cache and 2026-10-05 live)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_gastronomie&resultType=hits",
    "present": ["numberMatched=\"403\""]
  },
  {
    "id": "gelsenkirchen-hits-retail",
    "claim": "The retail layer holds 1,318 rows",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_einzelhandel&resultType=hits",
    "present": ["numberMatched=\"1318\""]
  },
  {
    "id": "gelsenkirchen-hits-services",
    "claim": "The services layer holds 594 rows (591 on 2026-10-05; re-read 2026-10-07 by the Abroad build, the city edits the layer)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_dienstleistung&resultType=hits",
    "present": ["numberMatched=\"594\""]
  },
  {
    "id": "gelsenkirchen-uncategorised-food",
    "claim": "54 food rows have no KAT_GASTRO (the uncategorised food rows left out, owner)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_gastronomie&resultType=hits&CQL_FILTER=KAT_GASTRO%20IS%20NULL",
    "present": ["numberMatched=\"54\""]
  },
  {
    "id": "gelsenkirchen-uncategorised-services",
    "claim": "122 services rows have no KAT_DL (the uncategorised services rows left out, owner; 134 on 2026-10-05, re-read 2026-10-07)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_dienstleistung&resultType=hits&CQL_FILTER=KAT_DL%20IS%20NULL",
    "present": ["numberMatched=\"122\""]
  },
  {
    "id": "gelsenkirchen-hairdressers",
    "claim": "The services layer holds 88 hairdressers, the bulk of the thin personal-services bucket (104)",
    "kind": "http_contains",
    "url": "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs?service=WFS&version=2.0.0&request=GetFeature&typenames=gewerbe_dienstleistung&resultType=hits&CQL_FILTER=KAT_DL%3D%27Friseur%2C%20Barbershop%27",
    "present": ["numberMatched=\"88\""]
  },
  {
    "id": "gelsenkirchen-bogestra-lines",
    "claim": "BOGESTRA's timetable index still describes 301 inside Gelsenkirchen, 302 on into Bochum, 107 and U11 on into Essen, with the timetable files gate 3 reads",
    "kind": "http_contains",
    "url": "https://www.bogestra.de/fahrplan-mobilitaet/linienfahrplaene",
    "present": ["Gelsenkirchen Hbf - Bismarck - Erle - Buer - Horst", "GE-Buer - Schalke - Gelsenkirchen Hbf - BO-Wattenscheid - Bochum Hbf", "Gelsenkirchen Hbf - Essen-Katernberg - Zollverein - Essen Hbf - Bredeney", "Gelsenkirchen-Horst - Essen-Karnap - Altenessen - Essen Hbf", "301-Inter-20260902.pdf", "302-Inter-20260614.pdf", "U11-20250712.pdf", "107-Inter-20160614.pdf"]
  },
  {
    "id": "gelsenkirchen-projected-crs",
    "claim": "Gelsenkirchen (mean survey longitude 7.078 E) projects in UTM 32N; tram mode, narrowed coverage, city scope",
    "kind": "utm_zone_from_longitude",
    "lon": 7.078,
    "expect": "EPSG:32632",
    "mode": "tram",
    "coverage": "narrowed",
    "scope": "city",
    "crs": "EPSG:32632",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
