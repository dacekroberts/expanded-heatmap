# Seattle (Regional): how the build came together, beside the Seattle-only project

Built 2026-10-02 on branch `seattle-tbilisi-build` (page 174), held for review
time. The comparison is with `link-station-commercial`, the earlier
Seattle-only project (read, not touched).

## At a glance

| | Seattle-only project (`link-station-commercial`) | Seattle (Regional) (this build) |
|---|---|---|
| Stations | 16: the 1 Line inside Seattle, Northgate to Rainier Beach | 39: the 1 and 2 Lines end to end, in 11 cities (Pinehurst, opened 2026-09-30, included) |
| Rail source | Sound Transit GTFS | OpenStreetMap route relations. Sound Transit's feed terms ("No Changes", flow-down, indemnity) ruled it out (owner). Pinehurst placed from Sound Transit's own station page; gate 3 exact against its line pages (27 and 26) |
| Business sources | 1: Seattle's Active Business License Tax Certificate table (Socrata `wnbq-64tb`, manual CSV export), with the GIS layer as geometry donor and the Census geocoder for 1,121 misses | 5: Seattle's ArcGIS "Business Locations (Active)" layer (every row already has a point, so no geocoder); Bellevue's register; King County's food inspections placed by parcel; Snohomish County's 2025 food list; the Liquor Board's off-premise list |
| "In Seattle" | the register's `City` field = SEATTLE (a postal city) | point-in-polygon on King County's city polygons: 988 rows that read "SEATTLE" lie in White Center, Skyway, Burien and the like, and are dropped |
| Categories | NAICS 44/45/722/812; out: parking (812930) and the personal catch-all (812990); 459999 kept after a hand sample | The shared NAICS module: the same two out, plus the project's later national carve-outs (funeral, canteens, caterers and mobile food, massage parlors, nonstore vending and fuel dealers); 459999 kept, as before |
| Lapsed licenses | not handled (one snapshot) | every year kept (owner); a lapsed restaurant license only if King County inspected a business of the same trade name in 2025 or 2026 (331 dropped) |
| Names | a blank trade name fell back to the legal name | never a legal name. Legal names are not downloaded; the server is asked which trade names equal the legal name (ids only), and those that read as a person's show the category. Bellevue's sole proprietors likewise |
| Analysis | rings, density gradient, ridership correlation (r = 0.684), chains, tenure, findings pages | a map only: ridership and analysis are out of scope in this project |
| Headline | 11,409 Seattle businesses, 4,120 within 0.6 mi of the 16 (36.1%) | 14,431 storefronts in 11 cities; Seattle 10,199, of them **3,763 within 0.6 mi of the same 16 stations (36.9%)**, 3,313 from the register alone |

The like-for-like Seattle count lands close to the old one, for different
reasons pulling both ways. Fewer, because of the polygon scope, the later
carve-outs and the lapsed-food rule. More, because of the King County food
premises the register lacks (inside Seattle).

## How it came together, in order

1. **The brief held:** `brief_check.py seattle` passed 16 of 16 before any
   code was written. Every owner call in it was already settled.
2. **Scaffold** at page 174, notices 109 to 116 claimed, staging told.
3. **Fetch, columns chosen at the source:**
   - Seattle without its contact, phone, mailing and legal-name columns.
   - Bellevue without its legal name and mailing fields.
   - King County's address points without their USPS-derived fields.
   - The Liquor Board's list read without the licensee and phone columns.
   - One Overpass query for the whole corridor.
4. **Rail:** OSM carried 38 of the 39 stations. Pinehurst came from Sound
   Transit's page, at King County's address point for 13110 5th Ave NE, and
   step 1 refuses that patch once OSM adds the station. The spacing median is
   1,350 m. The streetcar and the airport's people mover are named and not
   drawn.
5. **Scope:** the 11 station cities, plus every ring wherever it falls. That
   adds slivers of Des Moines, unincorporated King County, Beaux Arts and
   0.34 km² of unincorporated Snohomish County beside Lynnwood, each taking the
   neighbor's data.
6. **Two agent legs in parallel**, each returning a module and its counts:
   - **The Liquor Board list:** 1,409 of 1,837 premises joined by address
     (King County 96.0%), against a control that reproduced at 96.6%.
   - **The Snohomish food layer:** Lynnwood 310 and Mountlake Terrace 56
     facilities, as the brief said (329 and 70 after the owner's call on blank
     jurisdictions, below).
7. **Step 2, the spine:**
   - Seattle: 1,246 exact duplicate rows in the export dropped; one row per
     location.
   - Bellevue: retail and personal services only, issued since 2010.
   - King County food: placed by parcel (99.1%).
   - Each source used only in its own places.
   - Dedup on address plus name, then grocers sharing a street address.
8. **Three corrections the data forced:**
   - **The shape test was too blunt for names.** It read 2,079 Seattle shop
     names ("BLUE MOON") as people, so structural signals replaced it.
   - **King County's food is a source in Seattle too**, as the brief's table
     says. Reading it as a cross-reference only had left a quarter of
     Seattle's inspected food premises off the map.
   - **Workplace cafeterias are not restaurants.** King County files
     Microsoft's campus cafes ("BUILDING nn"), Amazon, Google and Meta staff
     cafes, vending routes, hotel kitchens and members' clubs as food
     service. Minneapolis's precedent leaves them out by name (about 760).
9. **Gates:**
   - Privacy verdict: publish, with 0 person-like names at a residential
     unit.
   - Provenance OK, scope disclosure OK, the inconsistency rows, the master
     list (Band C to Built).
   - Macro facts, and the label measured in a browser.
   - Drift check zero, with a 40-figure baseline.
   - `check_all` 44 of 44; pushed at 0 behind master.

## The owner's calls (2026-10-02)

1. **Lapsed Seattle food is kept only on a trade-name match.** A street match
   alone had kept 157 rows; in a 20-row hand sample about 7 were a different
   business now at the address. 331 lapsed food rows dropped in all.
2. **The 32 Snohomish facilities with a blank jurisdiction field are placed
   by the place their point falls in**, as every other source is: Lynnwood
   329 and Mountlake Terrace 70 facilities.
3. **Approved with the build:** mode `light_rail`, coverage "narrowed", the
   five notices' wording and the page's bullets.

After the calls: **14,431 storefronts** (was 14,500), 5,548 within 0.6 mi of a
station (38%). Drift check zero, baseline re-recorded.
