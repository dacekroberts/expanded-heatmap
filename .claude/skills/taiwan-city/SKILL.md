---
name: taiwan-city
description: Build a Taiwanese city on the national modules Taichung built - the tax register reader, the door-plate join with its district-code mapping, the owner's name rule and head-office rule, OGDL v1's load-bearing attribution - plus the traps Taichung measured and a sheet for Taoyuan and Taipei (Regional). Use for any Taiwanese city after Taichung; read with add-city, osm-rail, address-join and cjk-text, which it does not replace.
---

# Building a Taiwanese city

Written 2026-09-25 from **Taichung**, Taiwan's first city (`DECISIONS.md`,
"Taichung built"). Two more are briefed: **Taoyuan** and **Taipei
(Regional)** (Taipei + New Taipei). Kaohsiung is geo-blocked (Band D). Taiwan is
**Mexico's shape**, like Brazil: one national business source, so the second
city should cost a fraction of the first - a config, a door-plate file, a rail
leg and three thin steps.

Read the three briefs first (`docs/build_briefs/taipei.md` carries the national
argument; `taichung.md` and `taoyuan.md` only what is theirs), then this.

## What already exists - reuse it, do not rewrite it

| Module | What it does |
|---|---|
| `pipeline/countries/taiwan.py` | The register URL and SHARED cache (`data/taiwan/raw/BGMOPEN1.zip`, one file for every city); `register_rows(prefixes)`; `register_date()` (the register's own date, from its first data row); `bucket_of(code)` (47/48 Retail, 56 Food, 96 Personal, 487 out); `parse()` and `plate_key()` - **the join method, moved unchanged from `scripts/screen_taiwan_join.py`**; `is_trade_name()` - the owner's name rule |
| `pipeline/taxonomies/taiwan_fia.py` | The taxonomy: `industry` (the register's own Chinese name for the code) and `industry_code` |
| `pipeline/taichung/step2_clean_businesses.py` | The template step 2: register → head-office rule → district-aware join → name rule. **Copy it**; change the config |
| `pipeline/taichung/fetch_sources.py` | The template fetch, including a Google Drive large-file download and truststore |
| `scripts/check_personal_exposure.py` | `taiwan=True` on a city's entry runs the name-rule test (must print 0) |

**`parse()` has a control: Taipei.** Any change to it re-runs
`python scripts/screen_taiwan_join.py taipei` first and must reproduce 92.4%.
Taichung did NOT change it - it was moved byte for byte - because Taipei's
files were not cached to run the control against. Keep it that way until the
Taipei build downloads them.

## The owner's standing calls - do not re-ask

- **Name rule** (2026-09-23): a name is shown only when it is a trade name -
  companies and branches, and sole proprietors whose name carries a business
  marker; otherwise the pin shows its industry. The FIA itself refuses to
  publish owners' names. **Taichung measured 18.0% of storefronts shown by
  industry** - far above Taipei's "4.9% read as a person", because the rule
  hides every unmarked sole proprietor. That is the rule erring toward hiding,
  as decided; it is not a defect to tune away.
- **The marker list excludes given-name characters.** 美, 軒 and 莊 were
  considered and left out (陳美玲, 宇軒; 莊 is a surname). Adding a marker is a
  privacy decision, not a coverage tweak.
- **Head-office rule** (2026-09-25): drop a COMPANY head-office row on the 3rd
  floor or higher or with a room (室), unless its building holds 20+ storefront
  rows. Taichung: 1,904 flagged, 383 exempt, **1,521 dropped**.
- **Fault-based liability (OGDL v1 §六(三))** accepted for all of Taiwan.
- **A one-line metro earns a page** (Taichung, 2026-09-25).
- **Region: East Asia** (exists). Country: "Taiwan".

## The traps Taichung measured

1. **The door-plate file names a district by CODE, the register by NAME.**
   Taichung: `鄉鎮市區代碼` (6600100...). And **14,723 street/number keys occur
   in more than one district** - the 2010 city-county merger left one street
   name in several districts - so a key without the district joins some
   addresses to the wrong district. Step 2 LEARNS code → name from keys that
   exist in one district only, prints the table, and refuses any district
   below 90% agreement (Taichung: all 29 at 96.6-100%). Check what the next
   file carries before assuming the same: Taipei's has 街路段/巷/弄/號 in
   Chinese, New Taipei's is English-headed (`street、road、section`, `lane`...).
2. **The portals prefix CSVs with SEVERAL byte-order marks.** Taichung's index
   and station table start `﻿﻿﻿...`; `utf-8-sig` strips one. Read
   bytes, decode UTF-8, `lstrip(chr(0xFEFF))`.
3. **A door-plate file on Google Drive.** Taichung's portal index lists one
   file per month, each a Drive link; `fetch_sources.py` reads the index for
   the NEWEST month and submits Drive's large-file confirmation form (its
   action and hidden fields, as a browser does). It is not a CAPTCHA. Record
   the edition name in provenance; the page's snapshot caption reads it.
4. **OSM carries no colour for Taichung's line**, and neither does the
   operator's table. Do not invent the operator's colour; the owner decides
   (project palette, or a colour read from a cited operator source).
5. **Do not pull `route=train` in a city's box.** Taichung's query included it
   and fetched 24 MB of high-speed and TRA geometry for one metro line. Query
   `subway|light_rail` unless a train service is actually in scope.
6. **The boundary may not be needed.** Overpass 504ed on Taichung's boundary
   from all three mirrors; the build did without it - the register is scoped
   by address prefix, and the station check is the operator's own station
   addresses (every one must begin with the city's name). A REGIONAL city
   (Taipei) does need its two boundaries.
7. **The operator's table can carry a data error.** Taichung's gives 烏日 and
   高鐵臺中站 both code G17. Key stations by name; record, do not fix.
8. **A one-line city is mostly outside its rings.** Taichung: 12,588 of
   66,115 storefronts (19%) are in a ring. The whole-city heat layer shows the
   rest; say so on the page if the owner wants it said.
9. **Misses the parser does not reach** (left, not fixed - `parse()` has a
   control): a village name containing 路 (`六路里臺灣大道...`), a lane with no
   street (`中興１巷２６號`), intersections (`廍子路與祥順二路口`), and stalls
   (`號前`, `攤`, `市場`, `高架橋下`).

## Notices - one per source, and the statement is LOAD-BEARING

OGDL v1 §三(二): without the attribution statement the licence is deemed never
granted, and it covers derivatives (the joined coordinates). Each source gets
the prescribed form `提供機關／<agency> [year] [dataset title]` + the fixed
sentence + `https://data.gov.tw/license`. Taichung's sources:

| Source | 提供機關 | Title |
|---|---|---|
| Tax register (every city) | 財政部財政資訊中心 | 全國營業(稅籍)登記資料集 - plus FIA's own: cite the source, no emblems, no endorsement, and **do not present the filtered points as the register** |
| Taichung's Green Line stations | 臺中捷運股份有限公司 | 臺中捷運綠線車站資訊 |
| Taichung's door plates | *(see `docs/data_sources.md`)* | 臺中市…GIS門牌號碼 |

The FIA notice is national: the next city ADDS its own door-plate and rail
notices and names itself in the FIA one; it does not add a second FIA notice.

## The two cities still to build

**Taoyuan** (`taoyuan.md`): 49,282 storefronts, joined 94.0%. Door plates are
`TGOS_A68000_11508.csv` (the national TGOS edition) - check its district
column. Rail: Taoyuan Metro's network XML; the railway bureau's airport-MRT
file sits behind an Incapsula challenge and is NOT worked around - use the
national `捷運車站` layer. One line (Airport MRT), which leaves Taoyuan for
Taipei at both ends: decide the scope with the owner.

**Taipei (Regional)** (`taipei.md`): Taipei + New Taipei, 152,839 storefronts,
93.9%. Two door-plate files, one English-headed. Rail geometry from Taipei's
own network map (GeoJSON `MultiLineString`, `RouteName`, EPSG:3826) - its
colour source is unmeasured, and whether it carries New Taipei's Circular Line
and light rail is open. Market stalls: 5,239 rows (6.8%); placing them at the
market's plate is the build's call. **Run the `parse()` control here first.**
Macro label widths measured 2026-09-25: Taoyuan 57.4 px, Taipei (Regional)
112.5 px - the two sit close together, so expect offsets.
