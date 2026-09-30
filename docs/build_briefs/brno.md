# Brno — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on the live feed).** Run `python scripts/brief_check.py brno`
before writing code. T1 on the tram list: trams-only maps approved by the
owner on 2026-09-29.

---

## For the owner, with the build

**Approved (owner, 2026-09-30; DECISIONS "The Czech batch's calls and prose approved as recommended")**: every call below as recommended, and the prose. **Build order: Brno, Plzeň, Olomouc, Ostrava, Liberec, Most.** Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams, no metro |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets |
| **Scope** | **Obec Brno** | See the rail section |
| **Lines drawn** | Trams 1–10 and 12 (11 lines), KORDIS's feed; OSM geometry | |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi: median gap 329 m | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): H4 and P1** | **Out**: heritage and event services, no weekday trips | |

---

## The one-line summary

**Prague's modules with a new obec code, one coordinate control to declare,
and a tram-only rail leg from the regional feed.** The register chain (ROS02
establishments, RES activity and legal form, the RÚIAN join), the CZ-NACE
prefix taxonomy and the natural-person rule are shared
(`pipeline/countries/czechia.py`, `pipeline/countries/czechia_register.py`).
What is Brno's own: the obec, the control address, the feed, the CRS zone and
the halved rings.

| | Prague (built) | **Brno** |
|---|---|---|
| Obec (RÚIAN / ROS02 `PKODADM`) | 554782 | **582786** |
| Rail | Metro A–C, and trams under Prague's rules | **Trams only**: 11 regular lines (1–10, 12) |
| Stations in scope | Prague's | **147 stop names inside the city** (live feed, 2026-09-30) |
| Median station gap | — | **329 m**, so halved rings |
| Rings | Prague's | **0.05 / 0.1 / 0.2 / 0.3 mi** (the owner's spacing rule for the tram batch) |
| Projected CRS | EPSG:32633 | **EPSG:32633** (UTM 33N, 16.6° E) |
| Storefronts placed (screen) | Prague's | **7,229**: retail 2,520 · food 2,126 · personal services 2,583 |
| In the outer ring | — | **about 83%** at 0.3 mi (OSM stand-in; up to 3 points high on the Montpellier control) |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram, `coverage`
full.

---

## Business leg — the national chain, unchanged

Screened 2026-09-27 with `czechia_register.build_storefronts` on a stub
config (`data/_staging_scratch_2026-09-27/second_cities/czechia/business_leg.py`,
`business_results.json`):

- **26,882 active establishments** in the obec (ROS02, deduplicated on `ICP`;
  active = no `DATUKON`, or one in the future). 8,109 in the three buckets,
  and 7,820 after `filter_to_storefront()`.
- **Natural persons: 4,180 (53.5%).** The 591 at their own registered seat
  (7.6%) are **excluded**, Prague's rule. For the rest, the name is
  suppressed for the natural-person forms (`NAME_SUPPRESSED_FORMS`), and 50%
  of storefronts show a name.
- **7,229 placed of 7,229 (100%)** on RÚIAN's obec file (62,520 addresses,
  coordinates on 99.76%).
- **The restaurant control:** 2,110 at NACE 5611 is 1.61× OSM's
  restaurants. Prague reads 1.59–1.63×.
- **Currency:** ROS02's `DATPLAT` is 2026-08-31, the September 2026
  edition. The register drops closed establishments by `DATUKON`, so it
  passes the one-clock rule.
- **The national files are cached once** in the main checkout's
  `data/czechia/raw/` (ROS02, RES, CZ-NACE) and shared with Prague. Never
  refresh them from a Brno branch: `data/` is shared.

### ⚠️ The RÚIAN coordinate control — declare it, or `ruian()` stops

`czechia_register.ruian()` reads `cfg.RUIAN_CRS_CONTROL` and exits without
one (fixed 2026-09-27; Prague's is the castle). **Brno's, measured
2026-09-30:**

```python
RUIAN_CRS_CONTROL = ("19095597", 49.1936, 16.6069, "Brno New Town Hall")
```

- The address is Dominikánské náměstí 196/1, the Nová radnice. The RÚIAN
  file (EPSG:5513) transforms it to 49.19392, 16.60611.
- The expected point comes from the building's published coordinates, a
  source independent of this file. The two agree within 0.0003° of latitude
  and 0.0008° of longitude, inside the check's 0.001.
- The file is `20260831_OB_582786_ADR.csv.zip`, through `RUIAN_ATOM_TEMPLATE`
  with obec 582786. It is already cached in `data/brno/raw/`.

---

## Rail — IDS JMK's GTFS, trams only

The feed is `https://kordis-jmk.cz/gtfs/gtfs.zip`, published by KORDIS JMK
and listed on data.brno.cz (item `379d2e9a…`, CC BY 4.0 declared). It is
updated weekly on Sunday. Read 2026-09-30: `calendar` 2026-09-25 to
2026-12-13, `calendar_dates` to 2026-12-10, no `feed_info.txt`. **Fetch it
at build, never across weeks.**

- **Route types:** 299 bus, 28 rail, 14 trolleybus (800), 13 tram (0) and 1
  ferry. Draw **route_type 0 only**. The S-trains (Brno's 11 train
  stations, 1,974 m median gap) fail spacing, which the tram audit
  measured on 2026-09-29.
- **The 13 tram routes:**
  - **Draw the 11 regular lines**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 and 12,
    each in its feed colour (`route_color`): 1 `D40000`, 2 `4AB95D`, 3
    `009E9E`, 4 `EE7E1E`, 5 `F31D7F`, 6 `0777C1`, 7 `939DAC`, 8 `E1CB31`,
    9 `8C4A9A`, 10 `A05A2C`, 12 `00CCFF`.
  - ⚠️ **H4** (Komenského náměstí – Nové sady, 9 stops) and **P1** (Arena
    Brno – Hlavní nádraží, an event shuttle, 17 stops) run no weekday trips
    on 2026-10-07. **A build call: recommend leaving both out**, as
    heritage and event services. P1 also shares line 1's colour.
- **Per line, stop names inside the city:** every line is whole except line
  2, which keeps 36 of 38 (95%; its Modřice branch leaves the city). No
  stub.
- **Frequency** is disclosed, not gated, on street track. At each line's
  busiest stop on Wednesday 2026-10-07, 07–19h, the worst hour is **6 trips
  one way** on every regular line except line 10 (3 an hour).
- **Stations are the feed's `parent_station` rows, Prague's shape** (the Czech kit, 2026-09-30): all 329 platforms of the 11 regular lines carry a parent. That gives **149 parents network-wide, no two sharing a name, and 147 inside the city**; the two outside are Modřice, Tyršova and Modřice, smyčka on line 2's branch. The tram list's 146 was the screen's count. The median gap is 329 m. Czech diacritics are kept as published.

---

## Licences

- **ROS02, RES and RÚIAN: read for Prague, CC BY 4.0, permitted with
  conditions.** They carry the same display obligations and transformation
  notices as Prague's page (`docs/build_briefs/prague.md`, "Licence";
  `docs/data_sources.md`).
- **IDS JMK's GTFS: READ 2026-09-30, PERMITTED WITH CONDITIONS (CC BY
  4.0).**
  - **The grant comes from the publisher itself.** KORDIS's "Otevřená data
    (GTFS)" block on `idsjmk.cz/a/kontakty.html` says the data may be used
    under CC BY 4.0.
  - **The portal agrees.** The copy on data.brno.cz is byte-identical to
    `kordis-jmk.cz/gtfs/gtfs.zip`.
  - **Not the licence for the data:** idsjmk.cz's BY-NC-SA footer covers
    only its web pages.
  - **Must display:**
    - credit KORDIS JMK, a.s. and DPMB. The feed's `agency.txt` reads
      "IDS JMK (Data from: KORDIS JMK, DPMB)", which CC BY §3(a)(1)(A)
      says to retain;
    - name data.brno.cz (Statutární město Brno) as the distributor;
    - CC BY 4.0, linked;
    - a link to the feed;
    - **a modification statement**: filtered to trams, rings computed.
  - **Must not:** imply endorsement, or use the IDS JMK, KORDIS or DPMB
    logos.
  - **Owner's attention, not a blocker:** data.brno.cz's 2021 "Licence &
    GDPR" page (ArcGIS item `cabcc7ed…`, no longer shown on the site, not
    linked from the dataset) adds "keep the licence when redistributing"
    and a resale ban. Taking the file from KORDIS, whose own CC BY
    statement governs, leaves that page aside, and the map resells
    nothing. **Decided (owner, 2026-09-30): fetch from `kordis-jmk.cz`**,
    under KORDIS's own grant.
  - **Build:** the notice goes in `docs/data_sources.md` before the page
    exists.
- ⚠️ **The feed has no `shapes.txt`**, so the tram line geometry cannot come
  from it. Draw the lines from OSM's tram relations (`osm-rail`; ODbL, the
  basemap's credit already on the page), matched to the feed's lines by
  ref. The alternative, data.brno.cz's dissolved "Trasy linek IDS JMK", has
  no line attributes.
- **Do not use `content.idsjmk.cz/kestazeni/gtfs.zip`**, the English page's
  link. It is a stale 2022 copy.
- **OSM:** the stand-in ring share only; the basemap credit as everywhere.

## Build-time calls

1. **H4 and P1**: out, as recommended above.
2. **The ring share**: re-measure on the register's own points. The stand-in
   read 83.2% at 0.3 mi.
3. **The macro legend's `mode` and `coverage`**: tram and full, as proposed.

```brief-checks
[
  {
    "id": "brno-gtfs-serves",
    "claim": "KORDIS's IDS JMK GTFS zip serves (about 9 MB on 2026-09-30)",
    "kind": "http_ok",
    "url": "https://kordis-jmk.cz/gtfs/gtfs.zip",
    "min_bytes": 5000000
  },
  {
    "id": "brno-gtfs-tram-routes",
    "claim": "The feed carries 13 tram routes (route_type 0): the 11 regular lines, H4 and P1 (2026-09-30)",
    "kind": "gtfs_route_type_counts",
    "url": "https://kordis-jmk.cz/gtfs/gtfs.zip",
    "expect": {
      "0": 13
    }
  },
  {
    "id": "brno-gtfs-current",
    "claim": "The feed's calendar_dates run into the future (to 2026-12-10 on 2026-09-30); it is republished weekly",
    "kind": "gtfs_calendar_window",
    "url": "https://kordis-jmk.cz/gtfs/gtfs.zip",
    "expect": "current"
  },
  {
    "id": "brno-gtfs-declared-cc-by",
    "claim": "data.brno.cz lists the feed as CC-BY-4.0 (item 379d2e9a7907460c8ca7fda1f3e84328)",
    "kind": "http_contains",
    "url": "https://data.brno.cz/api/search/v1/collections/all/items/379d2e9a7907460c8ca7fda1f3e84328",
    "present": [
      "CC-BY-4.0",
      "kordis-jmk.cz/gtfs/gtfs.zip"
    ]
  },
  {
    "id": "brno-ruian-atom",
    "claim": "ČÚZK's ATOM service resolves obec 582786's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_582786",
    "present": [
      "582786"
    ]
  },
  {
    "id": "brno-projected-crs",
    "claim": "Brno's derived UTM zone is 33N (EPSG:32633)",
    "kind": "utm_zone_from_longitude",
    "lon": 16.608,
    "expect": "EPSG:32633",
    "mode": "tram",
    "coverage": "full",
    "scope": "obec",
    "crs": "EPSG:32633",
    "obec_codes": [
      "582786"
    ],
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED",
      "obec_codes": "OBEC_CODES"
    }
  }
]
```
