# Berlin - build brief

**Written 2026-09-28 by the Berlin build session**, from staging's Band B
screen (DECISIONS 2026-09-28, "German screen from the large-transit gap" and
"Berlin from the discards to Band B") and this session's own live probes the
same day (scratch only; every number below is a WFS hit count, a spread
sample or an Overpass read, and nothing large was downloaded). Run
`python scripts/brief_check.py berlin` before writing any code.

**Germany's first city, and its only one.** Munich, Frankfurt and Cologne were
discarded on full enumerations the same day and Hamburg on currency, so the
country profile is this brief's "Germany" section rather than a
`germany_step0_endpoints.md`: there is no second city for a country file to
serve. The shape is **one bespoke register** (a chamber of commerce's
membership, not a municipal licence and not a national register) - the
Oslo/Copenhagen/Prague family of NACE Rev. 2.1 premises registers.

---

## 🚩 Calls for the owner before any code

1. **Retail catch-all `47122`** (IHK: "Einzelhandel mit Waren verschiedener
   Art, Hauptrichtung Nicht-Nahrungsmittel"): keep, or exclude as Berlin's
   `CATCH_ALL_EXCLUDE`? Evidence below. Recommendation: **exclude**.
2. **Personal services:** the Band B row says "missing". Measured, only
   hairdressers (9621) and laundries (9610) are missing; beauty, spa/sauna/
   massage and tattoo studios are present. Draw a partial bucket, disclosed, or
   leave the bucket off? Recommendation: **draw it, disclosed.**
3. **Trams:** draw BVG's 22 tram lines, or U-Bahn + S-Bahn only?
   Recommendation: **decide on the ring-coverage numbers**, measured once the
   register is cached (below).
4. **The download:** the register CSV, 126,348,283 bytes, from IHK Berlin's
   GitHub (Git LFS), and VBB's GTFS, 78,379,003 bytes, from `www.vbb.de/gtfs`.
   Both need the owner's OK. Both licences are read (below).

---

## Germany, profiled (`add-country`, questions in cost order)

| Question | Answer for Germany |
|---|---|
| 2. Where commerce happens, or where companies register? | **Neither register the skill expects.** The Handelsregister is company-level; the Gewerberegister is municipal and not open (Berlin, Munich, Frankfurt, Cologne all probed). **IHK Berlin publishes its own membership as premises points** - unique among the chambers probed (IHK München sells addresses, IHK Köln has lookups, IHK Frankfurt nothing) |
| Cost per marginal city | **Bespoke, and there is no second city.** No national register, and no other chamber publishes |
| 1. Rail in readable data | VBB's GTFS (Berlin-Brandenburg, on `daten.berlin.de`, cc-by) and OSM, both complete for U-Bahn, S-Bahn and tram (below) |
| 3. Portal software | `daten.berlin.de` is CKAN at `datenregister.berlin.de/api/3/action/`; the web front end answers plain fetches with a JavaScript challenge (bunny shield), the API does not. Geodata is GeoServer WFS 2.0 at `gdi.berlin.de/services/wfs/<layer>` - `CQL_FILTER` and `RESULTTYPE=hits` both work, so composition can be counted server-side |
| 4. Personal information | **GDPR, and the licences say nothing.** Data about a sole trader can be personal data. The register carries **no names**, and IHK calls it its anonymised stock; CC0 §4(c) hands clearing third-party rights to the re-user. See "Privacy" |
| 5. Residence signal | None in the register. Available: `business_type` (Kleingewerbetreibender vs Handelsregister) and `employees_range`; neither is a home flag. ALKIS building use would be the parcel-style join if one is ever needed |
| 6. Geocoder | **Not needed.** Every row is a point (EPSG:25833) |
| 7. Classification | **WZ 2025 = NACE Rev. 2.1** at 4 digits (`nace_id`), plus IHK's own finer `ihk_branch_id` (5-6 digits). Single-valued |
| 8. Language and encoding | German labels, UTF-8 JSON (the console mangles umlauts; set `PYTHONIOENCODING=utf-8`) |

---

## Business layer: IHK Berlin's Gewerbedaten

| | |
|---|---|
| **Publisher** | IHK Berlin (the chamber of commerce); the WFS is served by SenStadt |
| **Endpoints** | WFS `https://gdi.berlin.de/services/wfs/gewerbedaten`, typename `gewerbedaten:gewerbedaten`, WFS 2.0.0, `OUTPUTFORMAT=application/json`. CSV `media.githubusercontent.com/media/IHKBerlin/IHKBerlin_Gewerbedaten/master/data/IHKBerlin_Gewerbedaten.csv` (**126,348,283 bytes**, Last-Modified 2026-09-28, Git LFS). CKAN `gewerbedaten-ihkberlin` (CSV), `gewerbedaten-ihk-berlin-wfs-b76e3aef` (WFS). A monthly archive at `cloud.ihk.berlin/d/62fad06b540745098ab7/` (terms not read, not needed) |
| **Rows** | **367,575** (WFS `numberMatched`, 2026-09-28), updated monthly |
| **Fields (18)** | `opendata_id`, `postcode`, `city`, `bezirk`, `ortsteil`, `prognoseraum`, `bezirksregion`, `planungsraum`, `planungsraum_id`, `ihk_branch_id`, `ihk_branch_desc`, `nace_id`, `nace_desc`, `branch_top_level_id`, `branch_top_level_desc`, `employees_range`, `business_age`, `business_type`, plus `geom` (Point) |
| **No name, no street address** | Not a column of any kind. The point is the place; `planungsraum` is the finest area label |
| **CRS** | **EPSG:25833** (ETRS89 / UTM 33N) native. Project in **EPSG:32633** (UTM 33N, 13.4° E) for all geometry, reprojecting from 25833 (sub-metre) |
| **Value sets** | `business_type`: 2 values (`im Handelsregister eingetragen`, `Kleingewerbetreibender` - 198,970, 54%). `employees_range`: 11 bands incl. `0 Beschäftigte` and `unbekannt`; never null |
| **Licence** | **PERMITTED, nothing to display or do** (`licence-read`, 2026-09-28). CSV and CKAN: **CC0 1.0** (`license_id cc-zero`, empty `attribution_text`; GitHub `CC0-1.0`). WFS: **Datenlizenz Deutschland - Zero - 2.0** (GetCapabilities `Fees`; "Jede Nutzung ist ohne Einschränkungen oder Bedingungen zulässig"). Cite the channel the pipeline fetches. Website terms (IHK Haftung, the Extranet's Nutzungsbedingungen, SenStadt's Impressum) cover pages, not data. CC0 §4(a): IHK's name and logo are not released - credit by name, no logo, no implied partnership. A courtesy credit is optional |
| **Completeness (the publisher's own FAQ)** | Dated and incomplete: closures and moves arrive late or never; **crafts businesses (Handwerkskammer members) and liberal professions are generally absent**; some addresses fail to geocode. The page must not call it complete |

### Composition of the three divisions (WFS hit counts, 2026-09-28)

Every count below is a server-side `RESULTTYPE=hits`; controls: a nonsense
code returns 0, an unknown field returns an error, and each level's children
sum to their parent.

| Division | Rows | Codes |
|---|---|---|
| **47 Retail** | **51,233** | 4711 4,560 · **4712 13,173** · 4721-4727 4,252 · 4730 fuel 311 · 4740 ICT 1,878 · 4751-4755 6,053 · 4761-4769 5,210 · 4771-4779 11,530 · **4781-4783 motor vehicles 3,810** · 4791/4792 intermediation 332 · ragged (`47`, `471`, `472`, `474`, `478`) 124 |
| **56 Food** | **20,771** | **5611 restaurants 14,962** · 5612 mobile 21 · 5621 event catering 1,897 · 5622 other catering 1,261 · **5630 bars 2,544** · 5640 intermediation 1 · ragged (`56`, `561`) 85 |
| **96 Personal services** | **14,042** | 9610 laundry **215** · 9621 hair **180** · **9622 beauty 1,792** · **9623 spa/sauna/massage 1,595** · 9630 funeral 44 · 9640 intermediation 26 · 9691 household 18 · **9699 n.e.c. 10,170** · ragged 2 |

**It is NACE Rev. 2.1, not WZ 2008 subclasses.** `nace_id='5610'` → 0 rows,
`'5611'` → 14,962: 56.11 Restaurants is a Rev. 2.1 class (Rev. 2 had 56.10).
Staging's first probe keyed on 5610 and found 10 restaurants where OSM had 104.
**So the Rev. 2.1 consequences Oslo, Copenhagen and Prague measured hold**:
car retail is in 47, and **online shops cannot be excluded by code** - no
branch label in the register mentions mail order or online retail
(`internet`/`online` labels are all IT and marketing services; `versand` 0).

### The two catch-alls, read at IHK's level

**`9699` (10,170)**, IHK's children: tattoo and piercing 1,253 · pet care 248
(+545 in 96993x, incl. dog grooming 85) · **prostitution 16 · escort 148** ·
trade-fair hosts 1,275 · "services in the hospitality trade" 1,630 · clearance
335 · spiritual/wellness advice 273 · itinerant trade 13 · photo booths 15 ·
residual `96999` 2,983 and bare `9699` 1,436. Oslo (96.990) and Copenhagen
(969900) excluded the class on home-based signatures; Berlin's is mostly
non-premises too. **Excluded as a class** (the module's per-city
`CATCH_ALL_EXCLUDE`), and prostitution/escort would be excluded whatever
happened to the rest.

**`4712` (13,173), of which `47122` is 12,141 - 24% of all retail**, IHK's
children: `47122` general non-food retail 12,141 · `47121` 323 · Sonderposten
63 · erotic retail 46 · department stores 11 · bare 589. The evidence on
`47122`:

- **91% report 0 employees** (11,019) and **90% are Kleingewerbe** (10,930) -
  but the rest of retail is 57-69% zero-employee in every Bezirk, so this is a
  difference of degree, not a flag.
- **Evenly spread**: 19-31% of retail in all 12 Bezirke, the same pattern as
  the rest of retail, so no borough-level signal either way.
- **Point match against OSM, 4 station boxes of 600 m** (Hackescher Markt,
  Kottbusser Tor, Wilmersdorfer Straße, Rathaus Steglitz): share of points
  within 30 m of an OSM shop - **47122 63%**, other retail 81%, beauty 93%;
  **office controls** (divisions 62, 68, 70, 73) **62-77%**. Stacked addresses
  (shops downstairs, offices up) make 30 m a weak test, but it places 47122
  with the offices, not with the shops.
- Staging's storefront/OSM ratios (retail 1.18-1.40×) included 47122; its
  in-box share (about 15%) is about the size of that excess.

Precedent keeps the Rev. 2.1 retail catch-all (Oslo, Copenhagen, Prague,
France: "shops by product"). **Recommendation: exclude `47122` in Berlin
anyway, on Berlin's numbers** - it is the generic registration a sole trader
takes to sell anything, anywhere (online, markets, from home), and nothing
above says "shop". Keep `47121` and its siblings. **The owner's call** (1).

### Personal services: partial, not missing

Present: beauty 1,792 (nail studios 972, cosmetic foot care 99, make-up 48),
spa/sauna/massage 1,595 (non-medical massage 1,313, solaria 120), and, inside
the excluded 9699, tattoo 1,253. Near OSM in the boxes: beauty 93%, spa 81%.
**Missing: hairdressers (180) and laundries (215)**, which are
Handwerkskammer members - the largest personal-services classes everywhere
else. **Recommendation: draw the bucket, with a legend label and a disclosure
that say hairdressers and laundries are not in it.** The owner's call (2).

### Proposed storefront filter (WZ 2025, prefix-matched as in `czech_nace2025`)

- **Buckets by division**: 47 Retail, 56 Food service, 96 Personal services.
- **Structural exclusions** (Oslo/Copenhagen/Prague's Rev. 2.1 set): 479
  intermediation, 5612 mobile, 562 catering, 564 and 964 intermediation, 9691
  household. 9630 funeral stays in, as in Prague (not in the Rev. 2.1 set).
- **Per-city catch-alls** (config, on `ihk_branch_id` where the NACE class is
  too coarse): `9699` class-wide; `47122` if the owner agrees.
- Kept: car retail (4781-4783), fuel (4730), 5630 bars.
- **Rough size** (before the rail scope): food 17,591 · retail 50,901 (38,760
  without `47122`) · personal services 3,828 (9610, 9621-9623, 9630 and 2
  ragged `969`; 9699 and the structural exclusions out).

**A new module, `pipeline/taxonomies/germany_wz2025.py`**, national (WZ 2025
is Destatis's), keyed on `nace_id` with labels from the register's own
`nace_desc`; IHK's `ihk_branch_id` is read only for per-city verdicts. It
should copy `czech_nace2025.py`'s shape, not import it: the labels are German.

---

## Privacy (`check_personal_exposure.py`, DECISIONS verdict before publishing)

- **No names of any kind**, so Los Angeles' failure mode (an owner's name as
  the fallback) cannot occur. Structurally Dublin's case: register the city
  with no name column, and `step 2` should exit if a name-like column ever
  appears.
- **The residual risk is a point at a home.** A Kleingewerbe point with 0
  employees in a residential building identifies nobody by itself, but
  category + age + employee band + a flat's address narrows it. **So the
  tooltip carries the category only, never `employees_range`, `business_age`
  or `business_type`** (read in step 2 for measuring, never written to
  `outputs/`). That is Copenhagen's structural rule ("at an address that is
  also a home, a dot shows only its category") applied to every dot.
- **Excluding `9699` removes prostitution and escort**, the two codes where a
  point is most sensitive; home-based beauty and massage remain and are the
  exposure check's first suspects.

---

## Rail: U-Bahn, S-Bahn and trams, measured 2026-09-28

**Scope: the Land of Berlin.** IHK Berlin's register stops at the Land
border, so lines are cut there (Tokyo's city-line precedent); S-Bahn stations
in Brandenburg are not drawn. Boundary: ALKIS Berlin `alkis_land`
(`gdi.berlin.de/services/wfs/alkis_land`, SenStadt, dl-de/zero-2.0 - a
supporting-source row, no notice), cross-checked against OSM relation
**62422** (Berlin, admin_level 4).

**OSM route relations with a stop inside the Land** (Overpass, VBB network):

| Mode | Operator | Lines |
|---|---|---|
| U-Bahn (`subway`) | BVG | **9**: U1 U2 U3 U4 U5 U6 U7 U8 U9 |
| S-Bahn (`light_rail`) | S-Bahn Berlin GmbH | **16**: S1 S2 S25 S26 S3 S41 S42 S46 S47 S5 S7 S75 S8 S85 S9 S15 |
| Tram (`tram`) | BVG | **22**: M1 M2 M4 M5 M6 M8 M10 M13 M17, 12 16 18 21 27 37 50 60 61 62 63 67 68 (plus 87 and 88, other operators, outside the Land) |

- **The S-Bahn is drawn**: Copenhagen's S-tog and Dublin's DART passed the
  spacing-and-frequency test, and Berlin's ring and Stadtbahn run like a
  metro. It is `route_type` 109 in the extended set, which `screen_rail.py`
  reads.
- **Label load is the Tokyo lesson**: 25 lines before trams, and the S-Bahn
  trunks are heavily shared (S3/S5/S7/S9 on the Stadtbahn, S1/S2/S25/S26 in
  the north-south tunnel, S41/S42 the same ring in two directions). Measure
  the labels early in a scratch render at 343 px, and the legend's real width
  against the solver's 274 px at the 1000 px frame.
- **Trams**: 22 lines, mostly east of the centre, where some districts
  (Prenzlauer Berg's east, Weißensee, Hohenschönhausen) have no U- or S-Bahn.
  Precedent is split (drawn: Amsterdam, Rotterdam, Oslo, Riga; left out:
  Barcelona, Milan, Toronto, Paris). **Measure the ring coverage with and
  without trams once the register is cached**, as Riga's table did, and take
  it to the owner (3). Tram stops are ~400 m apart, so thin as Amsterdam did
  (`docs/sub_transit_line_filters.md`).
- **Source**: VBB's GTFS is the agency feed - `https://www.vbb.de/vbbgtfs`
  (307 → `/gtfs`, **78,379,003 bytes**) and a stop-level variant at
  `unternehmen.vbb.de/.../gtfs-mastscharf/GTFS.zip` (83,251,265 bytes,
  2026-08-21); CKAN `vbb-fahrplandaten-via-gtfs`, `cc-by`, modified
  2026-08-28. OSM is the cross-check either way (`osm-rail`).
- **VBB's licence (`licence-read`, 2026-09-28): CC BY 4.0, PERMITTED WITH
  CONDITIONS, all of them on the page.** The grant is VBB's own dataset page
  (`unternehmen.vbb.de/digitale-services/datensaetze/`; CKAN's `cc-by` is
  unversioned). Display: the credit **"VBB Verkehrsverbund Berlin-Brandenburg
  GmbH"** (CKAN's `attribution_text`), the licence name linked, a link to the
  source, **that the data was modified** (stations selected, lines derived),
  and a reference to VBB's disclaimer ("kann Fehler enthalten und/oder
  unvollständig sein"). Must not imply the map is official VBB information;
  no logos or line signets (trademarks, not licensed). Nothing to do. The
  site's Impressum (private use only) governs web pages, not the datasets.
  Wording is drafted with the page texts, for the owner.
- **VBB's line colours are published data**: a "Linienfarben" CSV on the same
  page, same licence (updated April 2026) - the colour source before OSM's
  `colour` tags. When the zip is cached, read `feed_info.txt` and
  `agency.txt` for any added terms.

---

## Still unknown

- Ring coverage by mode, and the storefront count in the rings (needs the
  cached register).
- Whether VBB's Linienfarben CSV covers all 47 lines; else OSM's `colour`
  tags.
- `check_personal_exposure.py` on the built step 2, and the stacked-address
  counts within the rings (staging: 65% of storefront entries at Hackescher
  Markt share a point with 10+).
- The `taxonomy_catchall` check cannot read a WFS yet (it speaks Socrata and
  CKAN's datastore); the shares above are hit counts. Adding a WFS branch to
  `_classification_column` would page ~86,000 rows of two columns - a data
  pull, so it waits for the download OK.

```brief-checks
[
  {
    "id": "berlin-wfs-licence",
    "claim": "IHK Berlin's Gewerbedaten WFS declares Datenlizenz Deutschland - Zero - 2.0 and no access constraints in its capabilities",
    "kind": "http_contains",
    "url": "https://gdi.berlin.de/services/wfs/gewerbedaten?SERVICE=WFS&REQUEST=GetCapabilities",
    "present": ["Datenlizenz Deutschland - Zero - Version 2.0", "Es gelten keine Zugriffsbeschränkungen", "gewerbedaten:gewerbedaten", "EPSG::25833"]
  },
  {
    "id": "berlin-wfs-schema",
    "claim": "The register's schema carries the WZ class, IHK's branch code, employee band and business type, and no name or street column",
    "kind": "http_contains",
    "url": "https://gdi.berlin.de/services/wfs/gewerbedaten?SERVICE=WFS&VERSION=2.0.0&REQUEST=DescribeFeatureType&TYPENAMES=gewerbedaten:gewerbedaten",
    "present": ["name=\"nace_id\"", "name=\"ihk_branch_id\"", "name=\"employees_range\"", "name=\"business_type\"", "name=\"planungsraum\"", "PointPropertyType"],
    "absent": ["name=\"name\"", "firma", "inhaber", "strasse", "street", "hausnummer"]
  },
  {
    "id": "berlin-nace-rev21-no-5610",
    "claim": "nace_id is NACE Rev. 2.1 / WZ 2025: the Rev. 2 class 5610 has no rows",
    "kind": "http_contains",
    "url": "https://gdi.berlin.de/services/wfs/gewerbedaten?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=gewerbedaten:gewerbedaten&RESULTTYPE=hits&CQL_FILTER=nace_id%3D%275610%27",
    "present": ["numberMatched=\"0\""]
  },
  {
    "id": "berlin-nace-rev21-5611",
    "claim": "Restaurants are the Rev. 2.1 class 5611 (14,962 rows on 2026-09-28)",
    "kind": "http_contains",
    "url": "https://gdi.berlin.de/services/wfs/gewerbedaten?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=gewerbedaten:gewerbedaten&RESULTTYPE=hits&CQL_FILTER=nace_id%3D%275611%27",
    "present": ["numberMatched=\""],
    "absent": ["numberMatched=\"0\""]
  },
  {
    "id": "berlin-ckan-cc0",
    "claim": "The register's CSV package on Berlin's CKAN is CC0 with no attribution text",
    "kind": "http_contains",
    "url": "https://datenregister.berlin.de/api/3/action/package_show?id=gewerbedaten-ihkberlin",
    "present": ["cc-zero", "IHKBerlin_Gewerbedaten"]
  },
  {
    "id": "berlin-github-cc0",
    "claim": "IHK Berlin's GitHub repository holding the CSV is licensed CC0-1.0",
    "kind": "http_contains",
    "url": "https://api.github.com/repos/IHKBerlin/IHKBerlin_Gewerbedaten",
    "present": ["CC0-1.0"]
  },
  {
    "id": "berlin-vbb-gtfs-package",
    "claim": "VBB's GTFS is listed on Berlin's CKAN as cc-by, pointing at www.vbb.de/vbbgtfs",
    "kind": "http_contains",
    "url": "https://datenregister.berlin.de/api/3/action/package_show?id=vbb-fahrplandaten-via-gtfs",
    "present": ["cc-by", "vbb.de/vbbgtfs"]
  },
  {
    "id": "berlin-vbb-licence-page",
    "claim": "VBB's own dataset page grants its datasets (GTFS included) under CC BY 4.0, with a disclaimer the credit must refer to",
    "kind": "http_contains",
    "url": "https://unternehmen.vbb.de/digitale-services/datensaetze/",
    "present": ["Creative Commons Attribution 4.0", "Haftungsausschluss", "Linienfarben"]
  },
  {
    "id": "berlin-land-boundary",
    "claim": "ALKIS Berlin's Land boundary WFS answers, under dl-de/zero-2.0",
    "kind": "http_contains",
    "url": "https://gdi.berlin.de/services/wfs/alkis_land?SERVICE=WFS&REQUEST=GetCapabilities",
    "present": ["Datenlizenz Deutschland - Zero"]
  },
  {
    "id": "berlin-osm-rail-refs",
    "claim": "OSM carries U1-U9, the S-Bahn's 16 lines and BVG's 22 tram lines as route relations with refs",
    "kind": "osm_route_refs",
    "bbox": [52.33, 13.08, 52.68, 13.77],
    "routes": ["subway", "light_rail", "tram"],
    "require_refs": {
      "subway": ["U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9"],
      "light_rail": ["S1", "S2", "S25", "S26", "S3", "S41", "S42", "S46", "S47", "S5", "S7", "S75", "S8", "S85", "S9", "S15"],
      "tram": ["M1", "M2", "M4", "M5", "M6", "M8", "M10", "M13", "M17", "12", "16", "18", "21", "27", "37", "50", "60", "61", "62", "63", "67", "68"]
    }
  },
  {
    "id": "berlin-utm-zone",
    "claim": "Berlin (13.40 E) projects in UTM 33N",
    "kind": "utm_zone_from_longitude",
    "lon": 13.40,
    "expect": "EPSG:32633"
  }
]
```
