---
name: korea-city
description: Build a South Korean city on the national SEMAS modules Incheon built - the keyless storefront file (data.go.kr 15083033) read through korea_sbiz, cut by 시군구코드 never by name, the korea_sbiz taxonomy, the Korean name rule and privacy pass, notice 68 and the Visuals card hold, OSM rail with the Korean line rules and rail tests, the regional and single-station add-on pattern, the quarterly SEMAS refresh, and a sheet for Gimpo, Siheung, Yangsan, Gyeongsan, the regional add-ons and the commuter-rail tier. Use for any Korean city or Korean regional page after Incheon; read with add-city, osm-rail, cjk-text and publish-city, which it does not replace. Not for Seoul's, Daegu's or Busan's own LOCALDATA pipelines (except where a regional page joins them), and not for screening a new country (add-country).
---

# Building a South Korean city

**Drafted from the repo record on 2026-10-04 by the staging session, not by
the build sessions that wrote the Korean modules.** Each claim names its
source; anything marked *(inferred)* was not read anywhere. The first Korean
build session should check this file against the code before relying on it,
and correct it in place.

Sixteen Korean cities are built (`docs/city_master_list.md` line 889), on
**two different business sources**:

| Shape | Cities | Module | Notices |
|---|---|---|---|
| **LOCALDATA permit registers**, city republications | Seoul, Daegu, Busan | Seoul's own step 2; `pipeline/countries/korea.py` + `taxonomies/korea_localdata.py` for Daegu and Busan | 18, 48, 49 |
| **SEMAS 상가(상권)정보**, one national file | Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang, Daejeon, Gwangju, Gimhae | `pipeline/countries/korea_sbiz.py` + `taxonomies/korea_sbiz.py` | 68 |

**Every new Korean city is a SEMAS city.** The national LOCALDATA API
(data.go.kr 15154916) needs a key, and data.go.kr membership needs a Korean
identity check (본인인증), closed to this project (`docs/decisions/2026-09-27.md`,
"Incheon built on SEMAS's national storefront register"). SEMAS is Mexico's
shape: a city is a config, one Overpass query and the privacy pass
(`docs/build_briefs/gimpo.md`, summary). Read the city's brief first and run
`python scripts/brief_check.py <city>`.

## What already exists - reuse it, do not rewrite it

| Module | What it does |
|---|---|
| `pipeline/countries/korea_sbiz.py` | `province(sido)` finds a province's CSV by its first row's 시도명 and loads only `READ` (13 columns). `storefronts(sido, prefixes, sigungu_codes=None)` cuts the city, classifies, drops pointless rows, names the pin (상호명 + 지점명), withholds personal names. `edition()` reads the edition date from the cache's metadata JSON |
| `pipeline/countries/korea_sbiz_fetch.py` | The ONLY download: the keyless ZIP into the national cache `data/korea/raw/sbiz_15083033.zip` plus a `.json` (sha256, Content-Disposition, licence). Stops if the answer is not a ZIP. `--force` replaces the one file every SEMAS city reads |
| `pipeline/taxonomies/korea_sbiz.py` | `GROUPS` (중분류 to bucket), `OUT` (소분류 overrides), `KINDS` (English pin label per 소분류). An unknown 중분류 or 소분류 RAISES |
| `pipeline/korean_names.py` | `personal_name_at_home()`: a bare surname-plus-two-syllables name, optionally with a trade word, at an address that reads residential and not commercial |
| `scripts/check_personal_exposure.py` | `korean=True` entries, lines 91-123: `processed="businesses_clean.csv"`, `address=("address",)`, `withheld="Name withheld"` |

**Step 1 is copied, not shared.** Gwangju's docstring calls its step 1
"Incheon's step 1 (itself Busan's, Daegu's and Seoul's)", and Ansan's
English-name override was "copied into Gwangju's step 1" (DECISIONS.md,
"Gwangju built"). Copy the closest built city's five files; Daejeon is the
template for a code-keyed city (`pipeline/daejeon/config.py`;
`step2_clean_businesses.py` lines 26-27, 39 lines in all). *(Inferred:
osm-rail's meta-rule would put a shared Korean step 1 in
`pipeline/countries/`; whether to write one is the owner's call.)*

## The owner's standing calls - do not re-ask

- **SEMAS for Incheon and the Gyeonggi satellites** (2026-09-29), then
  Daejeon, Gwangju and Gimhae (Band A, 2026-10-03).
- **Taxonomy keyed at 소분류** (catch-all 6.4% there, 13.1% at 중분류; all 247
  categories homed). Food service is all of 음식 less staff canteens
  (구내식당), hostess bars (일반 유흥 주점) and dance halls (무도 유흥 주점); Retail
  is all of 소매 less household fuel dealers; Personal services is salons,
  laundries, baths, body-shaping and massage. Out: offices, education,
  health, estate agents, lodging, recreation, repairs, funeral services,
  wedding halls, matchmaking (`korea_sbiz.py` docstring).
- **Massage counts**, for continuity with every other country; proposing it
  out breaks `docs/category_rules.md` line 44. Hostess venues out is R3
  (line 41).
- **Licence**: the 2026-09-29 read and the owner's reasoned position on
  SEMAS's website copyright policy cover every city; nothing is
  per-province, so no new read (`gimpo.md`, "License").
- **Codes, never names**, to cut a city (owner, 2026-10-03; DECISIONS.md,
  "Gwangju built").
- **One page per satellite**, region **Seoul Capital Area** with
  `in_default_view: False` (2026-09-29). Cities outside the capital area go
  in the **South Korea** view (DECISIONS.md, "A South Korea view on the macro
  map", 2026-10-04). **Gimhae is its own page**, not Busan's (2026-10-03).
- **The Gyeonggi scope**: "the smaller 시군" (Hanam, Gwangmyeong, Guri,
  Gwacheon, Uiwang, Gunpo) get no standalone page (`docs/build_briefs/gyeonggi.md`
  lines 252-264; `docs/decisions_drafts/staging.md`, "The probe wave's first
  results"). Gimpo came back on the owner's call of 2026-10-04.

## Cutting a city: 시군구코드, never 시군구명

Given `sigungu_codes`, `storefronts()` keys on them; given prefixes too, both
must pick identical rows or the step exits; an unknown code exits
(DECISIONS.md, "korea_sbiz: a 시군구코드 filter beside the 시군구명 prefix"). The
filter landed with the Korea sweep: commit 8f0471c9 is on `origin/master`
(`docs/session_roles.md` line 88).

- **Names repeat.** Gwangju's 동구, 서구, 남구 and 북구 recur in other
  metropolitan cities, and **경기도 광주시 is another city** (the master list's
  "Gyeonggi-Gwangju", discarded on rail).
- **The 2026 merger** put Gwangju's five 구 in the member **전남광주통합특별시**
  (시도코드 12) with all of South Jeolla: **12210 동구, 12240 서구, 12270 남구,
  12300 북구, 12330 광산구**. The old 29xxx codes are gone
  (`pipeline/gwangju/config.py` lines 26-39).
- **Codes as a tripwire**: Daejeon's five codes are the whole member on this
  edition, so a sixth district or a merger stops step 2 instead of widening
  the page (`daejeon/config.py`, register section).
- Built codes: Daejeon 30110/30140/30170/30200/30230, Gwangju above, Gimhae
  48250 (`docs/data_sources/south-korea.md` lines 26-28). The ten older SEMAS
  cities still pass prefixes only (Anyang `("안양시",)`).
- **New cities: `SEMAS_SIGUNGU = None` and codes**, as Daejeon and Gwangju
  do *(inferred from their configs; the Gimpo and Siheung briefs say the
  prefix is unmeasured against the code)*.

## Measured traps

1. **The ZIP's member names decode as neither UTF-8 nor CP949**: find a
   province by its first row's 시도명 (`south-korea.md` line 16).
2. **The file id changes each quarter**: a new edition is a change to
   `korea_sbiz_fetch.py`'s `URL` and moves every SEMAS city at once.
3. **Placement is 100% on the register's own point** in every built SEMAS city
   (`south-korea.md` lines 16-28). The businesses are the register's rows; the
   OSM boundary scopes only the stations.
4. **SEMAS and LOCALDATA counts never compare or sum.** SEMAS lists every
   storefront, LOCALDATA licensed trades only, so Retail is thin in Seoul,
   Daegu and Busan; SEMAS pages say so (`app/pages/190_Daejeon_Heatmap.py`
   line 76), and Gimhae's exclusions say Busan's map is another record.
5. **OSM may lack the city's own relation.** After the merger no 광주광역시
   relation came back; step 1 took the union of the five 구 relations, each by
   id, checked by name and box, gated at 490-510 km2 (`gwangju/config.py`
   lines 50-59). Incheon's relation includes territorial sea, Ansan's
   Daebudo (`south-korea.md` lines 60, 67).
6. **SEMAS has no phone or owner column.** The LOCALDATA files do (전화번호,
   소재지전화, sitetel), never read, enforced by `korea.py`.

## Privacy and the name rule

- A bare Korean personal name at an address that reads residential shows
  "Name withheld" (Seoul's rule, `korean_names.py`), the address read with its
  building name. The Latin heuristics read a Korean name as nothing; the
  Korean pass is the check (`korean_names.py` docstring; `cjk-text`).
- **Run `python scripts/check_personal_exposure.py <city>`** after step 2, with
  a `korean=True` entry: 0 still shown. Built SEMAS cities withheld 9 to 107
  (`south-korea.md` lines 16-28).
- Record the verdict in the drafts file and `docs/privacy_verdicts.md` (the
  Korean rows run from Seoul's, line 65, to Gimhae's, line 141). Never quote a
  withheld name.

## Rail: OpenStreetMap and the Korean line rules

- **OSM, because no Korean agency publishes GTFS** and the national station
  dataset has no geometry (`south-korea.md` lines 36-51). One Overpass query
  per city for routes, station names and boundary, split by
  `fetch_sources.py`; one query in flight per session.
- **Match on route type and `ref`, never `network`**; every relation in the
  answer is drawn or named in `NOT_DRAWN`, or step 1 stops. Stations by route
  membership, collapsed by Korean name (trailing 역 and parenthesized
  subtitles dropped) and distance (Gwangju step 1, `korean_key()`).
- **Drawn** (Seoul's precedent, `gyeonggi.md` lines 338-344): Lines 1-9,
  Shinbundang, Ui LRT, Sillim, the Korail metro lines 경의·중앙, 수인·분당, 경춘,
  and 서해 on Bucheon's precedent, plus the city's local line, drawn to its
  ends with stations cut at the boundary. Capital-area configs pull the
  Korail lines by ref (`anyang/config.py` line 43); Daejeon and Gwangju never
  ask for route=train.
- **Never drawn**: GTX-A (an express), AREX, KTX and Korail intercity lines,
  lines under construction (Daejeon and Gwangju Line 2), and 대경선 (Daegu) and
  동해선 (Busan) on spacing (owner) (`south-korea.md` lines 36-51).
- **The rail tests.** A light metro passes on its own track with service
  inside 15 minutes and spacing above the 550 m guide (`gimpo.md` line 121).
  Fifteen Korean cities were discarded on 2026-10-04 on spacing (2.0-5.3 km)
  or frequency (18-28 min), from Seoul Metro's timetables and the cached OSM
  relations (`city_master_list.md` lines 661-675). Spacing screens a city,
  not a line in a network already mapped: Goyang's Gyeongui-Jungang stays,
  Namyangju's Gyeongchun stays with its wait stated (DECISIONS.md,
  "Namyangju's Gyeongchun Line stays drawn"). Borderline 15-minute lines
  pass on Ansan's and Bucheon's precedent, disclosed (`siheung.md` line 119).
- **Gate 3** against the operator's count where readable (Daejeon 22, Gwangju
  20), else Wikipedia as a secondary source. Line 1 is never gated whole;
  an ungateable line's in-city stations are read against its line table
  (`anyang/config.py`, gate-3 comment).
- **Colors**: the operator's as OSM tags it, checked with
  `pipeline/linecolour.py`, Delta-E floor 10, preferred 45; Seoul Line 8,
  Daegu Line 2 and Busan Line 4 were darkened, Daejeon's 23.1 kept
  (DECISIONS.md, "Daejeon built").
- **English names**: `name:en`, `name:ko-Latn`, `name:ko_rm`; a misspelling is
  overridden to the operator's signed form (`OSM_NAME_EN_OVERRIDES`).
- **CRS**: UTM 52N (EPSG:32652) in every built Korean city; derive it per
  city from longitude, never copy it.

## Notices and the Visuals card hold

- **Notice 68, Small Enterprise and Market Service** (`docs/data_sources.md`
  lines 2246-2264): PERMITTED WITH CONDITIONS, 이용허락범위 제한 없음. Display a
  source credit (no wording prescribed) and state the categories and counts
  as this project's; never present them as SEMAS's, or the data as accurate
  or complete on SEMAS's behalf.
- A new city **joins notice 68**: its heading in `docs/data_sources.md` and
  the `Notice(68, ...)` title and text in `app/components.py`, wording
  otherwise unchanged, no new number (`gimpo.md`, "License"). The `app/`
  change waits for review time. **Notice 1** (OSM) gains the city's rail,
  boundary and names in `app/osm_notice.py` (DECISIONS.md, "Daejeon built").
- **The Visuals hold**: the Visuals registry holds every notice-68 city off
  the cards while whether SEMAS's permission reaches social posts is open; a
  city with notice 68 only inherits it (DECISIONS.md, "Daejeon built",
  Downstream; `gimpo.md` line 189). Record "notice 68: caption" and the hold
  in the drafts file.

## The page and the reference docs

- **Bucheon's approved text with the city's line** (owner, 2026-09-29),
  under the 2026-09-30 pre-approval; model `app/pages/190_Daejeon_Heatmap.py`
  (edition caption from `provenance.json`, then **The lines** and **The
  businesses**). A sentence no template covers ("Not drawn: ...", a merger
  note) is a drafts-file proposal; the Korea sweep's three were approved as
  written (DECISIONS.md, "Review time: the Korea sweep's page proposals").
- **What Is Excluded**: "### <City> - SEMAS's national storefront register,
  all three buckets", Daejeon's shape: **Out by name** counts, **Names
  withheld**, **Stations** (`docs/excluded_categories.md` lines 5406-5460).
- **About the Data**: a row in each of `south-korea.md`'s three tables.
- Then `check_provenance.py`, `check_scope_disclosure.py`, and
  `check_macro_labels.py` at 375, 768 and 1200 (`gimpo.md`, "Scope").

## Regional pages and single-station add-ons

- **The pattern** (`city_master_list.md` lines 244-249): a neighbor with too
  few stations for its own page joins a built city's regional page. Uiwang (1
  station, 19% in a ring) was discarded as a city and marked an Anyang
  (Regional) add-on (line 674); Mexico's Naucalpan "follows Anyang + Uiwang"
  (`docs/decisions_drafts/staging.md`, 2026-10-04).
- **A SEMAS regional page is a longer code list** (Anyang + Gunpo + Uiwang).
  **A Seoul, Busan or Daegu regional page joins LOCALDATA and SEMAS**
  (`multi-source-city`, Los Angeles + Long Beach's shape).
- **The city alone proves zero drift first**, then extends (line 249).
- Marked, not scheduled (owner, 2026-10-04): Busan + Yangsan; Daegu +
  Gyeongsan; Seoul + Gwacheon (Line 4, 5 stations), Gwangmyeong (Line 7, 2),
  Hanam (Line 5, 4), Guri (Line 8, 4); Anyang + Gunpo (Lines 4 and 1, 6) and
  Uiwang (1).

## The quarterly SEMAS refresh

- Next due **2026-10-31** (차기 등록 예정일; the 2026-09-30 edition may land in
  early November): one shared re-run of the SEMAS cities, step 2, privacy
  check, drift check (`docs/recheck_calendar.md` line 409). Line 44 of that
  file still says "10 Korean cities"; line 409 lists 13. *(Discrepancy, not
  fixed here.)*
- Order *(inferred from the calendar row and the fetch docstring)*: read the
  new file id from the dataset page, edit `URL`, run `korea_sbiz_fetch.py
  --force` once, then each city's step 2 and privacy check under
  `heavy_job.py`. Measured peaks: Goyang alone 0.38 GB, two cities at a time
  0.75 GB (DECISIONS.md, "korea_sbiz: a 시군구코드 filter").
- Until then **every new city stays on the 2026-06-30 edition** (`gimpo.md`).

## Per-city sheet

**Gimpo** (Band A, `docs/build_briefs/gimpo.md`). 경기도, code **41570**; 13,398
storefronts, 53.4% in a ring. The Gimpo Goldline (ref `김포 골드라인`,
light_rail), 9 stations in Gimpo, every 6 min, 1,457 m median spacing;
김포공항 (Seoul) excluded. Copy Uijeongbu. Gate 3 from a named source.

**Siheung** (Band A, `docs/build_briefs/siheung.md`). 경기도, code **41390**;
15,206 storefronts, 41.2% in a ring. Line 4, Suin-Bundang and Seohae, 9
stations (오이도 and 정왕 shared). Copy Ansan's `LINES`, colors and gate 3.
시흥능곡 and 달월 lack `name:en`: take the station object's name first.

**Their open question.** Both briefs say the build "waits for [the
시군구코드 filter] to land, or carries that commit" (`gimpo.md` line 73,
`siheung.md` line 70). It has landed (8f0471c9 on `origin/master`), so the
wait is over; whether each city's 시군구명 prefix agrees with its code is
still unmeasured. Re-run `brief_check.py` first either way.

**Yangsan** (Band C, `city_master_list.md` line 139): 11,202 storefronts; Busan
Line 2, 5 stations, headway unread (Busan's operator pages refuse scripts);
26% in a ring. Own page or Busan (Regional): the owner's call.

**Gyeongsan** (Band C, line 140): 8,943 storefronts; Daegu Lines 1 and 2, 5
stations (Daegu's site answers a cookie challenge); 35% in a ring. As
Yangsan, with Daegu, whose map lists these 5 as outside it (`south-korea.md`
line 58).

**The commuter-rail tier** (`city_master_list.md` lines 834-847): Pyeongtaek,
Osan, Yangju, Dongducheon, Cheonan, Asan, Paju, Chuncheon, Gyeonggi-Gwangju,
Icheon, Yeoju, Ulsan, Gumi, Hwaseong, all with SEMAS as the business leg. Not
candidates and not screened further until a commuter-rail rule exists (owner,
2026-10-04). No urban rail open: Changwon, Sejong, Cheongju, Pohang, Jeju
(lines 676-680).

## Not sourced, so left out

- The Visuals registry itself (`visuals/data/restrictions.json` is not in this
  worktree): the hold is read from DECISIONS and the briefs only.
- A UTM zone other than 52N for any future Korean city: not measured.
