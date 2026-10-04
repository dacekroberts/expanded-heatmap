# DECISIONS drafts - new-cities build (`new-cities-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30). The build
is Liverpool (Regional), Tacoma and Mendoza
(`docs/handoff_new_cities_2026-10-03.md`).

### 2026-10-04 - Liverpool (Regional) built: Merseyrail's Northern and Wirral Lines as a commuter-rail exception, gate 3 exact against Merseytravel's booklets and NaPTAN's rail records, food only on the FSA register

- **Built on the UK six's shared steps as config** (`pipeline/liverpool/`,
  page 195), the first UK map on heavy rail: Merseyrail drawn as a
  commuter-rail exception (owner, 2026-10-03), map mode `metro` (owner,
  2026-10-03, "1. metro"), the scope Liverpool, Sefton, Knowsley and Wirral
  (owner, 2026-10-03). Brief claims held (`brief_check.py liverpool`, 5 of 5).
- **Rail, from the one Overpass query** (2026-10-04, overpass-api.de, 1,088
  elements; train routes of Merseyrail's network or operator only, and the
  four councils' boundaries by GSS code):
  - 13 relations: the Northern Line's 6 and the Wirral Line's 4 kept (ref,
    operator Merseyrail); the City Line's 3 (289382-289384, tagged
    `network=Merseyrail` but run by Northern Trains, one still tagged London
    Midland) named in NOT_DRAWN with the 15-minute reason.
  - 135 stop positions -> 69 stations by name (widest spread 182 m, Seaforth
    & Litherland's two platforms).
  - **Gate 3, the operator: exact.** Merseytravel's timetable booklets, the
    brief's named sources, read for the line diagram on each cover: the
    Northern Line (valid from 17 May 2026) 37 stations, the Wirral Line (from
    20 September 2026) 34 Merseyrail stations, the Bidston - Wrexham line's
    Upton and Heswall (Transport for Wales) not counted. The build: 37 and 34.
    Merseyrail's own site sits behind a bot challenge and was not tried.
  - **Gate 3, NaPTAN: 59 of 59 names match** against the active RLY records
    (ATCO area 910, prefix 9100) inside the four councils, three under
    NaPTAN's other names (NAPTAN_NAME_ALIASES: Birkenhead Hamilton Square;
    Liverpool Central's loop platforms and Lime Street's low-level station,
    each a record of its own). 13 NaPTAN-only stations are explained in
    NAPTAN_EXPLAINED as on lines not drawn: ten on the City Line (Broad Green,
    Edge Hill, Halewood, Huyton, Mossley Hill, Prescot, Roby, Wavertree
    Technology Park, West Allerton, Whiston), Upton and Heswall on TfW's
    Bidston - Wrexham line, Meols Cop on Northern's Southport - Wigan line.
  - The light-rail test's track print reads railway=rail 100%, 12.5% in tunnel
    or on a bridge: heavy rail, expected, drawn on the commuter-rail exception
    rather than on that test.
  - **Scope: 59 inside, 10 outside** (Ormskirk, Aughton Park, Town Green;
    Hooton, Capenhurst, Bache, Chester, Little Sutton, Overpool, Ellesmere
    Port), as the brief counted. Northern 34 and Wirral 27 in scope.
  - **Spacing: median 1,182 m in scope** (min 210, mean 1,149, max 3,100), so
    the standard rings (0.1 / 0.2 / 0.3 / 0.6 mi), well over the spacing
    rule's 550 m; MEDIAN_GAP_BOUNDS_M (1,000, 1,400).
  - Lines merged by London's branch rule: Northern 3 of 6 relations, 64.6 km;
    Wirral 4 of 4, 100.3 km, the one-way loop drawn once within the merge.
  - **Colors adjusted, on measurement:** OSM's #036ebc and #00a654 (the
    operator's blue and green) moved to #08A0C0 and #28A800 by
    `line_colour_search.py liverpool` (45.1 and 45.6 from the pins, 3:1 on
    both pages, the pair 94.8 apart).
- **The brief's two frequency checks, from the same booklets:** every
  Kirkby-branch train runs to Headbolt Lane (Fazakerley, Kirkby and Headbolt
  Lane share every column); and Bebington's autumn pattern (from 21 September
  2026, Chester and Ellesmere Port lines only) is minutes 19, 27, 34, 49, 57,
  04 towards Chester, gaps of 8, 7 and 15, so every Wirral station short of
  Hooton keeps 15 minutes or better by day.
- **Businesses (the FSA's four files, every extract 2026-10-02):**
  - 10,179 register rows; 7,400 storefront rows, the brief's figure exactly.
  - 4 at a "Flat" address never placed; no childminders.
  - 622 without the FSA's point: 399 placed at a Code-Point centroid, 223
    (3.0%) not placed (Sefton 3.8%, Wirral 3.7%, Knowsley 2.5%, Liverpool
    2.4%); no outward-only postcodes. **Sefton's full file places 94.1% at the
    FSA's own point**, so the brief's 75.3% all-type sample did not hold.
  - 1 outside the sanity box and 2 outside the councils; 11 trading-as names
    show the trade name.
  - **7,170 storefronts placed** (Food service 4,797, Food shops 2,373): 94.4%
    at the FSA's point, 5.6% at a centroid. 3,732 (52%) within a ring: Food
    service 2,625, Food shops 1,107.
  - Canteens by name are at least 1.9% of Restaurant/Cafe/Canteen (names
    with canteen, cafeteria, staff restaurant, a contract caterer's name or
    hospital), not separated (London's precedent).
- **Personal exposure (`check_personal_exposure.py liverpool`):** 3,732 pins,
  3,303 distinct names; no fallback name exists, since step 2 never loads an
  owner column; 0 emails, phone numbers or c/o markers; 0 surname-first
  names and 22 "person's name (trade name)" shapes (Manchester had 12); the
  heuristic reads 899 (24.1%) as person-like, which on the FSA register is
  mostly pubs and cafés named for people. **Verdict: publish**, London's,
  Newcastle's and the UK six's on the same register.
- **Notices (Staging's numbers):** 143 Food Standards Agency (Liverpool),
  Newcastle's notice 62 as Manchester's 84 with the city and date changed;
  **153** Ordnance Survey (Liverpool), Manchester's 85 with the city changed.
  The kit had reserved only 141-143; the centroid tier needs an Ordnance
  Survey notice of its own, so Staging assigned 153 (2026-10-04) after
  Belgium's 144-152. The Department for Transport, NaPTAN notice 86 takes the
  owner's reworded first sentence (2026-10-03) and Liverpool's page; notice
  1's rail sentence and `app/osm_notice.py` name Merseyrail.
- **For Visuals:** 143 and 153 in the caption only (the OGL's "including or
  linking to", as the eight Ordnance Survey cities and London's FSA notice);
  notice 86's new first sentence changes UK captions, not faces; the rail and
  boundaries are OpenStreetMap's, so the OSM line goes on the card face. No
  open terms question.
- **Macro map:** label width 135.0 px, measured in the browser pane with the
  Google Fonts face loaded (controls Blackpool (Regional) 139.7 and
  Nottingham (Regional) 151.7 reproduced). Liverpool's pill below its dot;
  **Manchester (Regional)'s United Kingdom pill raised 14 px** (("end", -10,
  0) to ("end", -10, -14)), because level with its dot it covered
  Liverpool's marker. A search over 64 pairs of offsets with
  `check_macro_labels.py`'s geometry found two with PROBLEMS 0 at all three
  widths, both needing Manchester's pill raised; the simpler was taken.
- **Proposals for review time (no template covers them):** on the page, the
  bullets "Merseyrail is suburban rail that runs as a metro ...", "In the
  evening and on Sundays most stations have a train every 30 minutes." and
  the City Line bullet; in What Is Excluded, the Merseyrail sentences in
  "Which stations these maps are drawn around" and Liverpool's Stations
  paragraph; the new row in `docs/commuter_rail_list.md`. The brief flagged
  the evening sentence and the City Line sentence as proposals too.
- **For the owner, one call:** `label_tier`. The UK rule is "tram and light
  rail against metro", which would make a metro city major, while the brief
  carries "minor, as the UK six". Set to minor (a pill only in the United
  Kingdom view) pending the owner; major would put a fourth UK pill in the
  Europe view beside London, Glasgow and Newcastle and needs that view
  re-scored.

### 2026-10-04 - The UK steps take heavy rail: a configurable NaPTAN stop type, a route filter and boundaries by GSS code; zero drift on the UK six

- **`pipeline/countries/uk.py`'s NaPTAN gate reads `config.NAPTAN_STOP_TYPE`,
  MET when unset; Liverpool (Regional) sets RLY.** Merseyrail's stations are
  rail access nodes (StopType RLY, ATCO area 910, prefix 9100), never the
  tram stops' MET in area 940, so the gate's hard-coded `"MET"` would have
  counted zero. The default keeps the six built UK cities on MET without a
  config edit. `norm_name` also drops NaPTAN's rail suffix "Rail Station" and
  a county qualifier left trailing once it is gone ("Walton (Merseyside) Rail
  Station"): area 910 names 95 of its 98 records in a Merseyside box that way
  (read 2026-10-04 from a scratch probe of the area file). The alternative, a
  per-city alias for every station, would have been 59 entries restating one
  suffix rule.
- **`pipeline/countries/uk_fetch.py` gains `config.OSM_ROUTE_FILTERS` and
  `config.BOUNDARY_GSS`, both fetch-only.** The first narrows a route mode to
  one network (tag filters, each its own selector, unioned), because every
  `route=train` in a Merseyside box would otherwise come back (the osm-rail
  skill's rule against box-wide train queries). The second selects the scope's
  admin relations by `ref:gss` when their relation ids are not yet known, so
  the city's one Overpass query also reads the ids, which the config then
  records; each code must match exactly one relation. `fetch_osm` now counts
  route relations by `type=route` rather than by not being a boundary id,
  the same set for every built city.
- **Proved at zero drift on the six built UK cities, twice**:
  `drift_check.py manchester birmingham edinburgh sheffield nottingham
  blackpool`, once after the stop-type change and once after `norm_name`'s,
  both "RESULT: zero drift", every baseline figure unchanged and every
  NaPTAN name match as before (Manchester 99, Birmingham 35, Edinburgh 23,
  Sheffield 48, Nottingham 50, Blackpool 40); measured peak 0.48 GB through
  `heavy_job.py`. The fetch change cannot be drift-checked (no step runs
  it), so the six cities' Overpass query strings were generated from git
  HEAD's `uk_fetch.py` and from the new one and compared: identical for all
  six. Cleanup confirmed the shape of the change before it landed
  (2026-10-03).
