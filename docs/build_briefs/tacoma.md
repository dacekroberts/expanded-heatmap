# Tacoma — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band A,
owner-approved 2026-10-03** ("license readings look good": Tacoma from C to
A). Run `python scripts/brief_check.py tacoma` before writing code. The trail:
`docs/decisions_drafts/staging.md`, 2026-10-03 "Seven licence reads for the
sweep's first group; Brussels and Tacoma to A (owner)" and "The sweep's first
group banded". A trams-only city: read the `tram-city` skill with this brief
(trams-only maps approved 2026-09-29; rings by the spacing rule; no stop
thinned; gate 3 against the operator's own count; the approved page text).
Seattle (Regional) did not draw the T Line because Tacoma is outside Link's
11 cities (`docs/build_briefs/seattle.md`), not on any ruling about Tacoma.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot color) | **`tram`** | Street-running on purpose-built track, median stop gap about 450-470 m: it stayed on the tram list |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets (Milwaukee, Detroit and Tampa were dropped 2026-09-28 as food only on one short line; Tacoma has all three) |
| **Scope** | **City of Tacoma**, `SCOPE = "city"` | The register's in-city marker; the Census place polygon for the station check |
| **Lines drawn** | **T Line** (Sound Transit), from OpenStreetMap | Sound Transit's GTFS is not used (owner, 2026-10-02, for Seattle) |
| **Rings** | **halved**: median gap about 450-470 m | The owner's spacing rule (`docs/ring_rules.md`); recompute on the stops drawn |
| **Not drawn** | Sounder S Line (commuter rail), Pierce Transit buses | Sounder fails the commuter-rail exception (below) |
| **Region** | `"United States West"` | Seattle's and Tucson's |
| **Call: Color** | chosen at build if OSM has none | tram-city call 3 |

---

## The one-line summary

**Sound Transit's T Line, one 12-stop line inside the city, and the City's
daily business-license layer under a site-wide disclaimer the City
requires (Chicago's template).**

| | **Tacoma** |
|---|---|
| Rail | **T Line** (formerly Tacoma Link), Tacoma Dome to St Joseph, one line, `route_type` 0 in Sound Transit's feed |
| Stations in scope | **12, all inside the city**: Tacoma Dome, S 25th, Union Station, Convention Center, Theater District, Old City Hall, S 4th, Stadium District, 6th Ave, Hilltop District, St Joseph, Tacoma General (the Hilltop extension opened September 2023) |
| Median station gap | **452 m** on platform means (469 m on the parent-station points), so halved rings (0.05 / 0.1 / 0.2 / 0.3 mi) |
| Projected CRS | **EPSG:32610** (UTM 10N, 122.44° W) |
| Register | "Business Licenses - Map (Tacoma)", item `2fa3b14b4de44c16b44893fee2cadefd`, point layer, 22,128 rows, **11,812 in the city**, NAICS, refreshed daily |

---

## Business leg — the point layer, never the table

| | |
|---|---|
| **Source** | **"Business Licenses - Map (Tacoma)"**, item `2fa3b14b4de44c16b44893fee2cadefd`, `https://services3.arcgis.com/SCwJH1pD8WSn5T5y/arcgis/rest/services/BusinessLicenses_Map/FeatureServer/0` (owner IT.OpenDataMgr, credit "City of Tacoma, Tax & License"). The licence read named this item; the table item `8efa2724e88a44a286894d33cb5fb331` (`Business_Licenses/FeatureServer/0`, a Table with the same rows and no geometry) is **not** the source |
| Rows | **22,128** (2026-10-03), data last edited 2026-10-02: refreshed daily |
| Fields | `objectid, license_number, business_name, trade_name, naics_code, naics_code_description, business_open_date, business_open_year, business_open_date_text, mailing_street, mailing_unit_number, mailing_po_box, mailing_city, mailing_state, mailing_zip_code, site_street, site_unit_number, site_po_box, site_city, site_state, site_zip_code, police_sector, council_district, neighborhood_businessdistrict, map_status, x, y, globalid` |
| Geometry | points in **EPSG:2927** (Washington State Plane South, US feet); `x`, `y` are WGS84 longitude and latitude (the screen, on the table). Request `outSR=4326` and check the two agree |
| **In the city** | **`council_district` 1-5 = 11,812 rows** (1: 2,010; 2: 3,498; 3: 3,181; 4: 1,471; 5: 1,652). 3,522 mapped rows have no district (outside the city); 6,794 are "Not Mapped", almost all out-of-town site addresses (6 with `site_city` TACOMA) |
| Points | 8,105 distinct points among the mapped rows (6,760 single-row; the largest stack 133): address-level. No address join needed |
| Currency | **Passes.** The item is a "Directory of businesses with an active Tacoma Tax & License business account"; closed accounts drop out. In the publisher's words it "does not indicate whether a business has a business license for the current year", and it has no status or expiry field. Openings by `business_open_date`: 2,145 in 2025, 1,793 in 2026 |

### Classification — NAICS 2022, `naics.py` as is

- `naics_code` is NAICS 2022, 3 to 6 digits, never blank. In the city through
  `naics_group()`: **Retail 1,520 · Food service 600 · Personal services
  811** · out 8,881.
- Largest: 812112 beauty salons 429, 812199 other personal care 146; 459999
  miscellaneous retail 264, 458110 clothing 142; 722511 246, 722513 186,
  722515 104, 722410 61.
- **Catch-alls named at the screen**: 812990 all other personal services
  (194, already out), **459999 all other miscellaneous retailers (264,
  kept)**, 455219 all other general merchandise (71). Read each against
  `docs/category_rules.md` before keeping it.
- 721199 all other traveler accommodation (367 in the city, probably
  short-term rentals in homes) is out as lodging. The separate "Business
  Licenses for Rental Activity" layer is not needed.

### ⚠️ Privacy — trade names that are the entity name

- **`trade_name` is never blank, but equals `business_name` on 4,690
  in-city rows, 712 in the three buckets** (Retail 413, Food 88, Personal
  211). Where the entity is a sole proprietor, that name can be a person's
  own. There is no ownership-type field, so Houston's and Tucson's
  `OWN_TYPE` rule has nothing to key on: **Vancouver's rule of 2026-09-21**
  is the precedent (a name that reads as a person's own shows the business
  type; "&" or a digit never counts). A withheld-name list holds keys
  (`pipeline/name_keys.py`).
- **The mailing fields are never used to place or label a pin.** Leave
  `mailing_*` out of the query's `outFields` altogether (Den Haag's "never
  fetch" precedent).
- `site_street` equals `mailing_street` on 6,986 in-city rows (1,413 in the
  buckets): a home-address marker to read in the privacy check, not a
  verdict. No home-based flag exists.
- Run `python scripts/check_personal_exposure.py tacoma`, record the verdict
  in the drafts file and `docs/privacy_verdicts.md`.

---

## Rail — the T Line, from OpenStreetMap

- **Source: OpenStreetMap** through `osm-rail` and the shared
  `pipeline/osm_tram.py` (route-relation membership, Aarhus's collapse). Not
  queried for this brief: one Overpass query for the city, never parallel,
  60 s after a 504 or 429.
- **Sound Transit's GTFS is not a source** (owner, 2026-10-02, "we can use
  openstreetmap here", for Seattle: its Transit Data Terms add a "No
  Changes" clause, pass-on terms and an open indemnity). The cached feed
  (release SC-Fall-2026.3, 2026-09-01 to 2027-03-26) measured the 12
  stations, 22 platforms and a median gap of 452-469 m for this brief only; the check
  below re-measures it.
- **Frequency, stated as a fact** (Kansas City's way, without citing or
  reproducing a schedule): every 12 minutes on weekdays (about 04:36-22:32)
  and Saturdays (07:00-22:32); every 20 minutes on Sundays (about
  09:40-18:32). Every 20 minutes or better by day, so tram-city call 2's
  floor is met.
- **Gate 3**: Sound Transit's own T Line page or station list, read for the
  count only (12 expected), in `OPERATOR_STATION_COUNTS` and
  `OPERATOR_COUNTS_SOURCE`. Not the feed, not OSM. Not looked up for this
  brief.
- **Scope polygon**: the Census Bureau's place polygon, Kansas City's and
  Tucson's layer: TIGERweb `Places_CouSub_ConCity_SubMCD/MapServer/4`,
  `GEOID='5370000'` ("Tacoma city", 128.9 km² land). Every stop is expected
  inside; step 1 stops on one outside.
- **Sounder S Line: excluded.** Two stations in Tacoma (Tacoma Dome, South
  Tacoma); weekday trips at Tacoma Dome are peak-only (one at 10:00 and one
  at 15:00 outside the peaks) at commuter spacing, so it fails the
  commuter-rail exception. Named on the page as not drawn, with the buses.
- **Label**: "T Line", its public name, on the map and in the legend. Color
  from OSM's `colour` if present, else the project's palette. No Sound
  Transit logo.

### Page text

The `tram-city` template, section 6. The first heading for one line is
**The tram**; Sound Transit markets the T Line as light rail and US pages say
"streetcar", so whichever word the page uses beyond the template is a
proposal flagged in the drafts file. The scope bullet takes the US form
(", as the US Census Bureau draws its limits. Every stop is inside it.").
**Business bullets**: the pins are **"active business license accounts"**,
never "currently licensed" or "licensed businesses" (licence read,
2026-10-03); "Read the density as a register" carries the publisher's
caveat that an active account does not mean a license for the current year.

---

## Licence — permitted with conditions (`licence-read` 2026-10-03)

- **Grant**: Resolution 39378 (2016) and the City's open-data page: no
  restrictions on reuse.
- **The City's disclaimer must be displayed, site-wide**, word for word, as
  Chicago's (notice 2) and Kansas City's (notice 80) are in
  `render_site_notices()` (`every_page=True`). The exact text (115 words,
  from the City's disclaimer page, kept in the staging scratchpad as
  `notice_utf8.txt`):

  > The information and data made available here has been modified for use from its original source, which is the City of Tacoma. The City of Tacoma makes no claims as to the completeness, accuracy, or timeliness of any information and data contained in this application; makes no representation of any kind, including, but not limited to, warranty of the accuracy or fitness for a particular use; nor are any such warranties to be implied or inferred with respect to the information or data furnished herein. The information and data is subject to change without notice. It is understood that the information and data contained in the web site is being used at user’s own risk.

  Keep its own spelling and punctuation (the curly apostrophe in "user’s").
  It is a required notice, exempt from the American-spelling pass.
- **Revocation**: the City may "require the termination" of any display or
  use, for any reason. Accepted as Chicago's template, without Chicago's
  indemnity or IP reservation; **honored through the removal rule**: take
  the layer or the city down first, then record it.
- **Cite `data.tacoma.gov`**, never `data.cityoftacoma.org`: the item's
  `licenseInfo` still links the old host, which no longer resolves. The
  credit: "Business license data: City of Tacoma, Tax & License
  (data.tacoma.gov)", drafted by the build.
- Rows in `docs/data_sources/united-states.md` for the layer and the TIGER
  polygon; the disclaimer in "Notices this project MUST display when
  published". OSM: ODbL, the site's notice 1.

## Downstream

Per `docs/session_roles.md`, "Downstream sessions": the build records in its
drafts file, for each notice (the disclaimer and the credit), **card face or
caption only**, read from the terms' own words on where the notice must
appear, and **any open terms question**. One to record: the disclaimer binds
"applications" that use the data and the City's right to end any use, so
whether a city card counts as such an application is Visuals' question to
carry.

## Build-time calls

1. **The line color**, if OSM records none.
2. **The name rule** on the 712 in-bucket rows whose trade name is the
   entity name, and the privacy verdict.
3. **The three catch-alls** (459999, 455219, 812990) against the category
   rules.

```brief-checks
[
  {
    "id": "tacoma-point-layer",
    "claim": "THE BUSINESS LEG: 'Business Licenses - Map (Tacoma)' is a point layer of about 22,128 active accounts (2026-10-03), carrying the trade and entity names, NAICS, the site address, the council district and map status, and still refreshed daily",
    "kind": "arcgis_layer",
    "url": "https://services3.arcgis.com/SCwJH1pD8WSn5T5y/arcgis/rest/services/BusinessLicenses_Map/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 22128,
    "tolerance": 1500,
    "present": ["trade_name", "business_name", "naics_code", "site_street", "site_city", "council_district", "map_status", "business_open_date", "x", "y"],
    "max_age_days": 14
  },
  {
    "id": "tacoma-item-active-accounts",
    "claim": "The item describes active Tax & License accounts, warns it does not show a license for the current year, and its licenseInfo still links the old disclaimer host",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/2fa3b14b4de44c16b44893fee2cadefd?f=json",
    "present": ["Directory of businesses with an active Tacoma Tax & License business account", "does not indicate whether a business has a business license for the current year", "BusinessLicenses_Map", "data.cityoftacoma.org/pages/disclaimer"]
  },
  {
    "id": "tacoma-disclaimer-text",
    "claim": "The City's disclaimer page still carries the required notice and the termination clause",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/da55cd2590204362af6b5a58ed87dbbb/data?f=json",
    "present": ["has been modified for use from its original source, which is the City of Tacoma", "makes no claims as to the completeness, accuracy, or timeliness", "being used at user", "require the termination"]
  },
  {
    "id": "tacoma-tline-stations",
    "claim": "Sound Transit's feed (a measurement, not the build's source) serves the T Line at 22 platforms, 12 stations collapsed on parent_station, median nearest-neighbour 452 m on platform means (469 m on the parent-station points), well under the 550 m line for halved rings",
    "kind": "gtfs_stations",
    "url": "https://www.soundtransit.org/GTFS-rail/40_gtfs.zip",
    "route_ids": ["TLINE"],
    "expect_parent_station_populated": true,
    "expect_platforms": 22,
    "expect_stations": 12,
    "crs": "EPSG:32610",
    "station_spacing_median_m_min": 300
  },
  {
    "id": "tacoma-census-place",
    "claim": "The Census Bureau's place polygon for the scope is GEOID 5370000, 'Tacoma city'",
    "kind": "http_contains",
    "url": "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID%3D%275370000%27&outFields=NAME,GEOID&returnGeometry=false&f=json",
    "present": ["\"NAME\":\"Tacoma city\"", "\"GEOID\":\"5370000\""]
  },
  {
    "id": "tacoma-projected-crs",
    "claim": "The derived UTM zone is EPSG:32610; tram, full coverage, the city",
    "kind": "utm_zone_from_longitude",
    "lon": -122.44,
    "expect": "EPSG:32610",
    "mode": "tram",
    "coverage": "full",
    "scope": "city",
    "crs": "EPSG:32610",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
