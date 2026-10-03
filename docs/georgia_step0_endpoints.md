# Georgia - Step 0 endpoints and country profile

**THE EVIDENCE TRAIL, NOT THE RECORD.** Tbilisi was built on 2026-10-02 and
its rows were re-derived from `pipeline/tbilisi/config.py` into
[`data_sources/georgia.md`](data_sources/georgia.md). **Where this file and
`data_sources/georgia.md` disagree, `data_sources/georgia.md` wins.**
Corrected at build: a 10,000-row page now outlasts the API's gateway (HTTP
502), so the build pulls 2,000-row pages; the build's one Overpass query also
fetched the city boundary (relation 1996871), which §1 left unfetched;
Geostat's own definition of "active" was found ("an enterprise which is
engaged in economic activity", Business Demography metadata), so §2 trap 4's
turnover-and-staff criterion stays a secondary source's.

**Profiled 2026-10-02 (`add-country`), for one city: Tbilisi.** Nothing was
built when this profile was written. Every endpoint below was fetched that day unless marked ASSERTED. When
Tbilisi is built, these rows are re-derived from its `config.py` into
`docs/data_sources/georgia.md` (the "PROVISIONAL" section of `add-country`),
and this file becomes the evidence trail. The city brief is
[`build_briefs/tbilisi.md`](build_briefs/tbilisi.md); the owner's calls of
2026-10-01 are in `docs/decisions_drafts/staging.md` ("Tbilisi moves from C to
B", "Geostat's Business Register: PERMITTED WITH CONDITIONS").

## Verdict

**No disqualifier.** Georgia is the **national establishment register** shape
(`add-country` §2), with one national publisher and one keyless API:

| Question | Answer | Evidence |
|---|---|---|
| 1. Urban rail in readable data | **Yes, from OSM.** Tbilisi Metro, 2 lines, 23 stations (operator's count). No public GTFS found | §1 |
| 2. Where commerce happens | **Yes: a FACTUAL address, distinct from the legal address**, on every row, with coordinates on 91.1% | §2 |
| 3. Portal software, refusals | A React app over a keyless JSON API; a **50-requests-per-window rate limit** (HTTP 429 with `retryAfter`) | §3 |
| 4. Personal information | No carve-out in the licence; individual entrepreneurs are half the register and are natural persons. Owner's call taken (unnamed dots) | §4 |
| 5. Residence signal | **None usable.** No home-based flag; legal address equals factual address on 3.5% of kept individual-entrepreneur rows | §5 |
| 6. Geocoder / address file | Not needed for 81% of kept rows; a national address layer exists on the NSDI geoportal (ASSERTED, not probed) | §6 |
| 7. Classification | **NACE Rev. 2 with a national fifth digit** (NCG 006-2016), single-valued, 98.9% classified | §7 |
| 8. Language | Georgian script (Mkhedruli) for every name; English labels for classifications only; OSM carries `name:en` for all 23 stations | §8 |

**Cost per marginal city: national register.** Any other Georgian city is one
region or municipality code on the same API, but the master list holds one
Georgian city, Tbilisi (`docs/city_master_list.md`, Georgia row): no other
Georgian city has metro, light rail or tram.

---

## 1. Rail

| Endpoint | Result (2026-10-02) |
|---|---|
| Overpass, ONE query (bbox `41.60,44.65,41.86,45.05`): subway route relations, their route_masters, member nodes and ways with geometry, and every `station=subway` node. Cached at `data/tbilisi/raw/osm_metro.json` (114,486 B) | **93 elements** from `overpass-api.de` on the second attempt: 4 route relations (two per line, one per direction), 2 route_masters, **23 `station=subway` nodes**, 18 ways. The first attempt drew a 504 from `overpass-api.de` and a read timeout from `overpass.kumi.systems`; the retry waited more than 60 s and used a cheaper form (`out body` for relations and nodes, `out geom` for ways only) |
| `https://ttc.com.ge/sites/default/files/2024-10/Tbilisi%20Metro_New%20RS_SEP_09Oct2024_0.pdf` (797,435 B, the operator's Stakeholder Engagement Plan, October 2024) | **"27.3 km with 23 stations on two lines"**: the operator's own count, for gate 3 |
| `https://ttc.com.ge/en`, `/index.php/en/about-us`, `/en/history` | Operator site (Drupal). No station count in the static HTML; the "number of travel" counters render 0 without JavaScript |
| `https://transit.ttc.com.ge/` | The journey planner. Its API (`/pis-gateway/api/v2`, `/v3`) requires an `X-api-key` header that the web app embeds. **Not used**: a key lifted from someone's front-end is not a published feed |
| GTFS | **None found** on the operator's hosts or by web search (2026-10-02). The Mobility Database catalogue was NOT consulted (the fetch of its CSV was refused in this session), so "no GTFS" is **ASSERTED**, one method |

**What OSM holds**, read from the cache:

- Line 1, `ref=1`, **Akhmeteli-Varketili Line**, `colour=#FF0000`, 16 stop
  members: Akhmeteli Theatre ... Varketili.
- Line 2, `ref=2`, **Saburtalo Line**, `colour=green`, 7 stop members: State
  University ... Station Square-2.
- `operator`: თბილისის სატრანსპორტო კომპანია (Tbilisi Transport Company);
  `network`: თბილისის მეტროპოლიტენი.
- **16 + 7 = 23 = the operator's count.** The interchange is two OSM station
  nodes, **Station Square-1 and Station Square-2, 110 m apart**, and the
  operator counts both. Nearest-neighbour spacing: min 110 m (that pair),
  median 1,033 m, max 1,536 m. No platform duplication.
- Every station sits inside Tbilisi (longitude 44.719 to 44.871); no station is
  outside the city, so no naming layer is needed for excluded stations.

**Traps:**

- `colour=green` is a CSS keyword, not a hex value. Map it explicitly.
- OSM spells **"Nadzaledevi"** (`name:en`) where the operator and most
  sources write **Nadzaladevi**; the register's district is "Nadzaladevi
  District". Check the operator's spelling before it becomes a map label.
- The Station Square pair: one interchange, two stations in the operator's
  count. Gate 3 counts 23; whether the map draws one ring or two there is a
  build decision (⚠️ in the brief).

**Boundary.** Not needed to scope the business leg (the register's own
factual-address region code does that) or the stations (all inside). For the
map frame, two sources exist: OSM's administrative boundary (not fetched: this
session held one Overpass query) and Geostat's GIS app
(`https://gis.geostat.ge/`), whose JS bundle embeds municipality polygons with
Tbilisi as feature id `"11"` (`"ქ. თბილისი"`). The bundle's filename is a
build hash, so it is not a stable URL.

## 2. Business register: Geostat's Statistical Business Register

**The shape.** Each row is an **economic entity** (legal person or individual
entrepreneur), not a premises. It carries a **legal address** (`Address`,
`Region_Code`, `City_Code`) AND a **factual address** (`Address2`,
`Region_Code2`, `City_Code2`): the second is where the entity operates, and is
the field that makes this a map of commerce rather than of registered offices.
Filtering on the factual region is what the screen did and what the build
must do.

| Endpoint | Result (2026-10-02) |
|---|---|
| `https://br.geostat.ge/register_geo/` | 200, a 2,114-byte React shell (`ბიზნეს რეგისტრი | Business Register`). Loading it in the browser pane showed the search form and its API module, `/assets/api-*.js` |
| `https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&limit=10000&page=N&lang=en` | **THE SOURCE.** JSON `{data, pagination}`. **`total` 63,511**, `totalPages` 7 at `limit=10000`. ~16.7 MB per full page; about 106 MB for the whole pull. Keyless |
| same, without `isActive` | `total` 228,964 (every status) |
| same, `factualAddressRegion=zzqq` | `total` 0: **the filter is real** (nonsense control) |
| same, `isActive=zzqq` | `total` 0: the active filter is real too; `isActive=1` and `=true` both give 63,511 |
| `https://br-api.geostat.ge/api/locations/regions?lang=en` | Region codes: **`11` = "The city of Tbilisi"** |
| `https://br-api.geostat.ge/api/locations/code/11?lang=en` | Tbilisi's ten districts as `"11 25"` (Gldani) ... `"11 58"` (Samgori), plus Didgori |
| `https://br-api.geostat.ge/api/legal-forms?lang=en` | Legal forms; **`ID 30` = "Individual Entreprises"** (sic), `Stat_ID_Type` 2 (a natural person); `1` = Limited liability companies |
| `https://br-api.geostat.ge/api/activities?lang=en` | The activity list behind the search form (not needed by a build) |
| `/api/documents/export?...` | The app's own export for over 200,000 rows (streamed CSV in a ZIP). Its column list (`X` in the bundle) has **no coordinates**, so `/documents` is the endpoint to use. Not fetched |
| `/api/representatives`, `/api/partners`, `/api/partners-vw`, `/api/full-name-web`, `/api/legal-unit-web?personId=` | Person-level endpoints. **Never call** |

**Columns** (`/documents`, 48 keys): `Stat_ID`, `Legal_Code`, `Personal_no`,
`Legal_Form_ID`, `Abbreviation`, `Full_Name`, `Ownership_Type_ID`,
`Ownership_Type`, `Region_Code`, `Region_name`, `City_Code`, `City_name`,
`Comunity_Code`, `Community_name`, `Village_Code`, `Village_name`, `Address`,
the same eight with suffix `2` (factual address), `Activity_ID`,
`Activity_Code`, `Activity_Name`, `Activity_2_ID`, `Activity_2_Code`,
`Activity_2_Name`, `Head`, `mob`, `Email`, `ISActive`, `Zoma`, `Zoma_old`,
`X`, `Y`, `Change`, `Reg_Date`, `Partner`, `Head_PN`, `Partner_PN`,
`Init_Reg_date`, `web`, `Legal_Form`.

**Measured on the 63,511 active Tbilisi rows** (pulled with every personal
column dropped in memory, page by page; `data/tbilisi/raw/geostat_br_tbilisi_active_2026-10-02.csv`, 22.1 MB):

- **Composition**: individual entrepreneurs 31,854 (50.2%), LLCs 29,784,
  non-commercial legal persons 1,011, joint-stock 446, others under 200 each.
- **Top divisions**: 47 retail 14,493 · 46 wholesale 6,445 · 62 IT 3,332 ·
  68 real estate 3,298 · 45 motor vehicles 2,762 · 41 construction 2,417 ·
  43 1,985 ... **56 food service 1,628** · **96 personal services 1,374**. The
  screen's three bucket figures reproduce exactly.
- **Coordinates**: present on **57,869 (91.1%)**, every one inside a Tbilisi
  box, none swapped. But see the placeholder trap below: the real figure for
  storefronts is 81%.
- **Dates**: `Reg_Date` max 2026-08-31, `Init_Reg_date` max 2026-08-25:
  the register is live, with rows to the end of August 2026. `Change` is
  empty on every row.

### Traps

1. **`X` is LATITUDE and `Y` is LONGITUDE.** The app's own code reads
   `lat: X, lng: Y`. A config that maps X to longitude puts every pin in Iran.
2. **Placeholder coordinates: 91% present is not 91% real.** 464 points carry
   10 or more rows (19,901 rows). Reading the company addresses on the
   largest showed **district and settlement centroids**: the commonest
   factual address at 41.725938,44.750388 is just "საბურთალო" (Saburtalo), at
   41.68655,44.840891 "ისანი" (Isani), at 41.709599,44.756885 "ვაკე" (Vake);
   41.693803,44.801517 carries rows from **seven** districts; 41.695,44.789167
   has three decimals. Ten such points hold **1,295 of the 13,331 kept
   storefront rows with coordinates (9.7%)**. **Four of them sit ON metro
   stations** (Didube 1 m, Isani 77 m, Samgori 87 m, Liberty Square 113 m), so
   they would inflate exactly the innermost rings. The real markets are
   different points with real addresses: Lilo (Kakheti Highway 112, 484 kept
   rows) and Eliava (Tsabadze 8 and Khosharauli, 309).
3. **Two geocoding generations.** `X` arrives with 6-7 decimals (mostly rows
   registered 2020 onward) or 12-15 decimals (mostly earlier). Not a defect,
   but the placeholder test must not key on precision alone.
4. **"Active" lags new registrations.** Kept storefront rows by first
   registration year: 2021 1,193 · 2022 788 · 2023 484 · 2024 189 · 2025 99 ·
   2026 33. "Active" is read from tax declarations (turnover, employees or tax
   paid above zero; the criterion as published in a secondary source, IEM
   journal, ASSERTED), so a new business appears only after it has declared.
5. **The rate limit.** `X-RateLimit-Limit: 50` per window; over it, HTTP 429
   (or a JSON body `{"error": "...", "retryAfter": N}`). A 10,000-row page
   counts once. A fetch script sleeps between pages and honours `retryAfter`.
6. **Git Bash rewrites a leading `/` in an argument** into a Windows path
   (`/locations/regions` became `C:/Program Files/Git/locations/regions`),
   which the API answers with an ASP.NET 400 page. Pass API paths inside a
   Python file, not as shell arguments.
7. **`lang=en` translates labels, not names.** Legal-entity names arrive in
   Georgian script either way (9,630 Georgian, 370 Latin in a 10,000-row
   page); `Activity_2_Name`, `Legal_Form` and district names come back in
   English.
8. **The app's footer says "© All rights reserved."** beside its link to
   Geostat's "Terms of Data Usage". The data terms govern the data (the licence
   read of 2026-10-01); the footer is the site's.
9. **Enterprises, not premises.** A chain is one row at one factual address.
   The owner accepted the undercount, disclosed (2026-10-01).

## 3. Portal software and refusals

- `br.geostat.ge`: a Vite/React single-page app; `br-api.geostat.ge`: Express
  in front of ASP.NET (`X-Powered-By: Express, ASP.NET, ARR/3.0`). Keyless, no
  CAPTCHA, no account. Plain `requests` and curl user agents both answered
  200; no client-signature refusal.
- `www.geostat.ge`: server-rendered; answered plain curl.
- `ttc.com.ge`: Drupal, answered plain curl. `metro.ttc.com.ge` does not
  resolve.

## 4. Personal information

- **Licence**: Geostat's Terms of Use carve out third-party copyright and
  logos only. **No personal-data carve-out** (§9 below).
- **Who is a person here**: individual entrepreneurs (`Legal_Form_ID` 30) are
  natural persons: **31,854 of 63,511 rows (50.2%)** and **9,536 of 14,806
  kept storefront rows (64.4%)**. For them `Full_Name` is the person's name and
  `Legal_Code` / `Personal_no` the 11-digit personal number.
- **Personal columns on every row**: `Legal_Code`, `Personal_no`,
  `Full_Name` (for individual entrepreneurs), `Head`, `Head_PN`, `Partner`,
  `Partner_PN`, `mob`, `Email`, `web`, `Address` (legal address: for an
  individual entrepreneur usually a residence), `Address2` (factual address).
- **The API offers no column selection**, so the download boundary cannot omit
  them: the fetch script must drop them in memory before anything is written,
  and step 2 must assert they are absent (the owner's "dropped at fetch").
- **The statute**: the licence read of 2026-10-01 recorded that Georgia's
  personal-data law makes processing of public data lawful and gives the data
  subject a right to restriction, which the project's removal rule already
  honours; statistical confidentiality does not bind public-registry data
  (Art. 34(4) of the statistics law). The statute text was not re-read here.
- **The owner's call (2026-10-01)**: individual entrepreneurs as **unnamed
  dots, category only** (Taichung's precedent); personal ID columns dropped.
- **`check_personal_exposure.py` reads Latin script only** (its Korean and
  Taiwan passes exist for the same reason). Georgian names need their own
  pass, or the build relies on the structural rule (no name shown for legal
  form 30) and says so.

## 5. Residence signal

**None that the register states.** No home-based flag, no premises type. The
only proxy, legal address string equal to factual address string, holds on
**331 of 9,536 kept individual-entrepreneur rows (3.5%)** and 21 of 5,277
companies: too weak to act on, and too strong to quote as "home-based". No
open parcel or land-use layer was probed. The owner's unnamed-dot rule is the
control.

## 6. Geocoder and address file

- **Kept storefront rows without coordinates: 1,475 (10.0%)**; 1,453 of them
  have a factual address string, 892 have district "Unknown".
- **Plus 1,295 on placeholder points** (§2, trap 2).
- **A national address layer is ASSERTED, not probed**: Georgia's NSDI
  geoportal (`https://nsdi.gov.ge/en`, NAPR) lists address attributes
  (`ADDRESSST`, `ADDRESSNO`) and describes downloads behind a login. Per
  `address-join`, it is the place to look before any geocoder, and only if
  the owner wants the 19% placed rather than disclosed.

## 7. Classification

- **`Activity_2_Code`: NACE Rev. 2 with a national fifth digit** (Geostat's
  "National Classification of Georgia NCG 006-2016"; e.g. `47.59.2`
  household utensils). Single-valued; no delimiter. Depth on the 63,511:
  62,687 at the national leaf, 136 at class, 5 at group, **683 `Z`
  ("ACTIVITY UNKNOWN", 1.1%)**, none blank.
- **`Activity_Code` is the OLD scheme** (NACE Rev. 1.1 shape: `52.11.0`
  retail, `93.02.0` hairdressing) or `R`, blank on 247. **Never key on it.**
- The project's three buckets are divisions 47, 56 and 96, as in France's NAF
  (`pipeline/taxonomies/france_naf.py`). 52 distinct leaf codes occur in the
  kept rows (47: 47, 56: 2, 96: 3). Counts and the catch-all share are in the
  brief.

## 8. Language and encoding

- API JSON is UTF-8. Names are **Georgian Mkhedruli** (U+10D0 to U+10FF; Mtavruli
  capitals U+1C90 to U+1CBF exist and must be folded for any join key).
- **Business names stay in Georgian.** Category labels come from the API in
  English (`Activity_2_Name`, British spelling, "jewellery"); the taxonomy
  module owns the American-English bucket labels and keeps the source label in
  the tooltip.
- **Station names**: OSM's `name:en` exists on all 23 (national romanisation,
  2002 system: "Ghrmaghele", "Tsereteli"). No GTFS `translations.txt` to
  prefer. Watch "Nadzaledevi" (§1).
- `pipeline/theme.py`'s `FONT_STACK` must reach a face with Georgian glyphs
  (Segoe UI and Noto Sans Georgian do; check before the first render).

## 9. Licence: Geostat

- **Terms of Use**: `https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi`
  (Georgian: `/ka/page/...`), linked from the register app's own footer as
  "Terms of Data Usage". Read 2026-10-02; the licence-read verdict of
  2026-10-01 stands: **PERMITTED WITH CONDITIONS**.
- The grant: Geostat "allows its users ... the right to download, use, adapt,
  modify, create derivative works of, disseminate, copy, and share to the
  third parties, for any purpose, including commercial and non-commercial
  use, without restriction ... without prior permission".
- **Must display**: "Users should indicate Geostat as a source of information
  when using data of GEOSTAT." (also Art. 43(6) of the statistics law, per the
  2026-10-01 read).
- **Must not**: use Geostat's logo or trademarks.
- Disclaimer: Geostat is not responsible for loss from use, nor for
  "incorrectly processed and misinterpreted data by the user".
- SHA-256 of the saved English page: `8321dc6675309bad0f3ff583f4b76b637ebf0b904abcc786a7b6824513636449`
  (59,523 B; the page carries dated news, so the hash of the terms block's
  text, `1dcde3059e82f815fdbdd938129788dbbad06bfe45d9fdfacd1afe5ee3fcaefc`, is
  the stable one).
- **OSM**: ODbL 1.0, the project's standing attribution.
- **TTC**: only its published station count is used; no TTC data is
  redistributed, so no TTC licence row is needed unless the build uses its
  data.

## Required notices (promoted with Tbilisi, 2026-10-02: notice 114 in `data_sources.md`)

1. **Geostat**: name Geostat as the source, for example "Business data:
   National Statistics Office of Georgia (Geostat), Statistical Business
   Register, retrieved <date>; processed by this project." No Geostat logo.
2. **OpenStreetMap** (rail): the project's existing ODbL credit.
