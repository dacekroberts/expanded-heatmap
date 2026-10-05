# Coverage sweep: Asia, the Middle East and Africa (2026-10-03)

Desk work only. No Overpass, no OSM API, no data downloads, no portal probing
beyond confirming a portal exists. Region: Asia without Türkiye, the Caucasus
and Russia (the Europe agent's), plus the Middle East and Africa.

**Universe.** Built from Wikipedia's "List of metro systems" and "List of tram
and light rail transit systems", with recent openings checked by web search
(Astana LRT 2026-05-16; Jerusalem Green Line L3 2026-08-21; East Nile Monorail
2026-05-06; Meerut Metro 2026-02; Bhopal 2025-12-21; Indore extended
2026-09-06; Mumbai Line 9 into Mira-Bhayandar 2026-04-07). Network sizes
marked (kn) are general knowledge, not measured.

**Checked against.** `docs/city_master_list.md`, `city_master_list_evidence.md`,
`city_master_list_2026-09-30.md`, `global_country_shortlist.md`,
`commuter_rail_list.md`, `docs/*tram*.md`, `japan_city_list.md`,
`global_transit_gap.md`, `app/cities.py`, `docs/build_briefs/`. Any city with no
hit there was also grepped across every other `docs/**/*.md`, `DECISIONS.md`
and `PLAN.md`, in romaji with and without macrons and in kanji or hangul where
relevant. Grep script and outputs: `grep_names.py`, `grep_out.tsv`,
`grep_japan.tsv` in this folder.

---

## Headline findings

1. **The three Korean Band R cities may be unblocked by a file already on
   disk.** Daejeon, Gwangju and Gimhae went to Band R on 2026-09-27
   (`city_master_list.md:155-157`) because "the national register sits on
   data.go.kr behind the residency and CAPTCHA wall". Two days later Incheon
   and the Gyeonggi satellites were built on **SEMAS's 상가(상권)정보**, a
   *national* storefront file with WGS84 points, which is already cached
   (`data/korea/raw/sbiz_15083033.zip`, `docs/data_sources/south-korea.md:16-23`).
   No file records anyone re-reading the three R rows against SEMAS. If the
   cached file includes 대전, 광주 and 경상남도 rows, all three could move
   straight to a brief: Daejeon Metro Line 1 has 22 stations, Gwangju Line 1
   has 20, and the Busan-Gimhae LRT has 12 stations in Gimhae. **This is the
   strongest lead in the region, though strictly speaking it is not a
   never-recorded city.**
2. **No Kazakh city appears anywhere in the tracked files.** Almaty shows up
   only in staging's own drafts (`docs/decisions_drafts/staging.md:18`). Two
   systems are missing: Almaty Metro and the new Astana LRT. There may be a
   national statistical business register, the shape of Tbilisi's Geostat.
3. **Jerusalem appears only in staging's drafts.** Its light rail grew to two
   lines in August 2026. Tel Aviv's discard rests on Tel Aviv's own terms, so
   it does not cover Jerusalem or the four other Red Line municipalities
   (Petah Tikva, Bnei Brak, Ramat Gan, Bat Yam).
4. **India: 23 metro cities appear nowhere.** That includes the Delhi and
   Mumbai satellites and every second-tier metro. All of them rest only on
   the national-catalogue verdict of 2026-09-21. **One error to fix:**
   `global_country_shortlist.md:234` calls Ahmedabad one of the "cities with no
   metro". Ahmedabad Metro opened in 2019 and has about 45 stations (kn).
5. **Macau has never been screened.** It is noted once in `DECISIONS.md:12700`
   ("not screened for business data; its LRT would class as an edge network").
6. **Japan: about 50 municipalities from the wave-2 scoping universe have no
   romaji or kanji hit in any tracked file.** That universe covers every
   municipality with a subway, tram, monorail or AGT station, and lives in an
   untracked scratchpad (`...\dcee6a2e-...\scratchpad\japan_wave2\SCOPE.md`,
   `universe_mhlw.csv`). Among them are "mode" cities: the Tama Monorail
   cluster, Kawaguchi, Kamakura, Urayasu, Ibaraki, Minoh and Urasoe. Japan
   section below.

---

## Counts (cities; non-Japan, with Japan on its own line)

| Status | Non-Japan | Cities |
|---|---|---|
| BUILT | 17 | Hong Kong; Taipei (Regional), Taoyuan, Taichung; 13 Korean |
| IN A BAND | 12 (all Band R) | Hyderabad, Delhi, Bengaluru, Daejeon, Gwangju, Gimhae, Dubai, Bangkok, Riyadh, Tashkent, Hanoi, Kaohsiung |
| DISCARDED | 20 | Algiers, Doha, Mumbai, Kolkata, Chennai, Kochi, Manila, Tel Aviv, Jakarta, Cairo, Kuala Lumpur, Tainan, Hsinchu, Singapore, Ho Chi Minh City, Casablanca, Rabat-Salé, Tunis, Lagos, Addis Ababa |
| COUNTRY RULED OUT | China (one line) + 6 | Mainland China; Iran (Tehran named; Mashhad, Isfahan, Shiraz, Tabriz, Karaj by the country call) |
| Screened or noted, no row | 9 | Macau (DECISIONS only); Gimpo; Hwaseong; Gwangmyeong, Hanam, Guri, Gwacheon, Uiwang ("the smaller 시군"); Yangsan |
| **Covered only by a country or sibling verdict** | **58** | list at the end |
| **NEVER RECORDED** | **22** | list at the end |
| Japan | — | Built 20 · A 9 · B 5 · R 3 · discarded 3 · wave-2 remainder named in the handoff 25 · neighbour mentions only ~20 · **no tracked hit ~50** (section below) |


## Full classified table (non-Japan)

### East Asia

| City | Country | System | Status | Evidence |
|---|---|---|---|---|
| Hong Kong | HK | MTR, Light Rail, Tramways | BUILT | `app/cities.py`; `city_master_list.md:55` |
| Macau | MO | Macau LRT (Taipa, Seac Pai Van, Barra, Hengqin; ~14 stations, kn) | NOTED, never screened | `DECISIONS.md:12700` |
| Mainland China (all cities) | CN | many | COUNTRY RULED OUT (owner, 2026-09-28) | `city_master_list.md:596` |
| Taipei (Regional, with New Taipei; Danhai and Ankeng LRT) | TW | Taipei Metro, New Taipei Metro | BUILT | `city_master_list_evidence.md:25` |
| Taoyuan | TW | Airport MRT | BUILT | `app/cities.py` |
| Taichung | TW | Green Line | BUILT | `app/cities.py` |
| Kaohsiung | TW | KMRT, Circular LRT | BAND R (geo-blocked door-plate file) | `city_master_list.md:164` |
| Tainan | TW | none (TRA locals) | DISCARDED, rail | `city_master_list.md:319` |
| Hsinchu | TW | none (TRA locals) | DISCARDED, rail | `city_master_list.md:320` |
| Keelung | TW | TRA only | Not in scope (no urban rail) | — |
| Seoul, Busan, Daegu, Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang | KR | Seoul Metropolitan Subway, Busan Metro, Daegu Metro, Incheon Subway, etc. | BUILT (13) | `app/cities.py`; `city_master_list.md:545` |
| Daejeon | KR | Daejeon Metro Line 1, 22 stations | BAND R; **see headline 1 (SEMAS)** | `city_master_list.md:155` |
| Gwangju | KR | Gwangju Metro Line 1, 20 stations | BAND R; **see headline 1** | `city_master_list.md:156` |
| Gimhae | KR | Busan-Gimhae LRT, 12 stations | BAND R; **see headline 1** | `city_master_list.md:157` |
| Gimpo | KR | Gimpo Goldline, 9-10 stations | Screened (edge network), left out on the owner's satellite scope | `build_briefs/gyeonggi.md:35,261`; `city_master_list_2026-09-30.md:562` |
| Hwaseong | KR | Line 1, Suin-Bundang (3 stations after recount) | Measured, out (5.2% in a ring) | `build_briefs/gyeonggi.md:119,168` |
| Gwangmyeong, Hanam, Guri, Gwacheon, Uiwang | KR | Lines 7/1, 5, 8, 4, 1 | Pattern only: "under 8,000 storefronts and five stations each" | `build_briefs/gyeonggi.md:127,263` |
| Siheung, Paju, Pyeongtaek, Gunpo, Osan, Yangju, Dongducheon, Icheon, Gwangju (Gyeonggi), Yeoju | KR | Seohae, Suin-Bundang, Gyeongui-Jungang, Line 1, Line 4, Gyeonggang | **Covered only by the Gyeonggi sibling screen** (province portal measured all 31 시군; these are never named) | `build_briefs/gyeonggi.md` (no row) |
| Cheonan, Asan | KR | Line 1 (Korail, outer section) | **NEVER RECORDED** (Line 1 frequency there is likely commuter-grade) | — |
| Yangsan | KR | Busan Line 2 (5 stations); Yangsan LRT (kn: under construction) | Named only as Busan's excluded stations | `build_briefs/busan.md:42` |
| Ulsan, Changwon, Sejong, Cheongju | KR | none open (Ulsan tram under construction, kn) | Not in scope | — |
| Pyongyang, Chongjin, Wonsan | KP | Pyongyang Metro and trams; trams | **NEVER RECORDED** (infeasible: no open data, sanctions) | — |

### South and Southeast Asia

| City | Country | System | Status | Evidence |
|---|---|---|---|---|
| Delhi | IN | Delhi Metro (~300 stations) | BAND R | `city_master_list.md:167` |
| Noida, Greater Noida, Ghaziabad, Gurugram, Faridabad, Bahadurgarh | IN | Delhi Metro lines plus Aqua Line (NMRC) and Rapid Metro Gurgaon | **Country/sibling only** (India's national catalogue; Delhi's MCD/NDMC read covers NCT only) | — |
| Mumbai | IN | Mumbai Metro, Monorail | DISCARDED | `city_master_list.md:286` |
| Thane, Mira-Bhayandar, Navi Mumbai | IN | Line 4 (scheduled Aug 2026, unverified), Line 9 (3 stations since 2026-04), Navi Mumbai Metro Line 1 (11) | **Country/sibling only** | — |
| Kolkata | IN | Kolkata Metro, trams | DISCARDED | `city_master_list.md:287` |
| Howrah, Bidhannagar (Salt Lake) | IN | Kolkata Metro Green and Orange Lines | **Country/sibling only** | — |
| Chennai | IN | Chennai Metro | DISCARDED | `city_master_list.md:288` |
| Bengaluru | IN | Namma Metro | BAND R | `city_master_list.md:159` |
| Hyderabad | IN | Hyderabad Metro | BAND R | `city_master_list.md:153` |
| Kochi | IN | Kochi Metro | DISCARDED | `city_master_list.md:295` |
| Ahmedabad | IN | Ahmedabad Metro (~45 stations, kn) | **Country only**; misdescribed as having "no metro" | `global_country_shortlist.md:234`; `city_master_list_evidence.md:1220` |
| Gandhinagar | IN | Ahmedabad Metro Phase 2 (kn) | **Country only** | — |
| Pune, Pimpri-Chinchwad | IN | Pune Metro (~30 stations, kn) | **Country only** | — |
| Nagpur | IN | Nagpur Metro (~37) | **Country only** | — |
| Lucknow | IN | Lucknow Metro (21) | **Country only** | — |
| Jaipur | IN | Jaipur Metro (11) | **Country only** | — |
| Kanpur | IN | Kanpur Metro (~14-16, kn) | **Country only** | — |
| Agra | IN | Agra Metro (~6-7) | **Country only** | — |
| Bhopal | IN | Bhopal Metro Orange Line, 8 stations (2025-12-21) | **Country only** | — |
| Indore | IN | Indore Metro Yellow Line, 11 stations (extended 2026-09-06) | **Country only** | — |
| Patna | IN | Patna Metro, 5 stations, 20-min headway | **Country only** (fails frequency as reported) | — |
| Meerut | IN | Meerut Metro, 12 stations (2026-02) | **Country only** | — |
| Surat | IN | Surat Metro (under construction, kn) | Not open | — |
| Lahore | PK | Orange Line, 26 stations | **NEVER RECORDED** | — |
| Karachi | PK | none (KCR not running; BRT) | Not in scope | — |
| Dhaka | BD | MRT Line 6, ~16 stations | **NEVER RECORDED** | — |
| Colombo, Kathmandu | LK, NP | none | Not in scope | — |
| Singapore | SG | MRT, LRT | DISCARDED | `city_master_list.md:386` |
| Kuala Lumpur | MY | LRT, MRT, Monorail | DISCARDED | `city_master_list.md:308` |
| Petaling Jaya, Subang Jaya, Shah Alam, Kajang, Ampang Jaya, Putrajaya/Sepang | MY | Kelana Jaya, Sri Petaling, Kajang, Putrajaya lines; Shah Alam LRT3 (kn) | **Country/sibling only** (data.gov.my enumerated; KL's DBKL) | `city_master_list_evidence.md:1221` |
| Penang, Kuching | MY | Penang LRT under construction; Kuching ART is rubber-tyred | Not in scope | — |
| Bangkok | TH | BTS, MRT, ARL | BAND R | `city_master_list.md:160` |
| Nonthaburi, Samut Prakan, Pathum Thani | TH | MRT Purple and Pink; BTS Sukhumvit ext., Yellow; Green ext., SRT Red | **Country/sibling only** (national hosts and BMA refuse this machine) | `global_country_shortlist.md:2104` |
| Manila (with Quezon City, Makati, Pasig, Pasay, Mandaluyong, Marikina, San Juan, Caloocan, Parañaque, Taguig read) | PH | LRT-1, LRT-2, MRT-3 | DISCARDED | `city_master_list.md:292`; `global_country_shortlist.md:2101` |
| Antipolo | PH | LRT-2 east extension | **Country/sibling only** | — |
| Hanoi | VN | Metro 2A, 3 | BAND R | `city_master_list.md:163` |
| Ho Chi Minh City | VN | Metro Line 1 | DISCARDED | `city_master_list.md:390` |
| Jakarta | ID | MRT, LRT Jakarta | DISCARDED (national OSS register has no activity field) | `city_master_list.md:300` |
| Bekasi, Depok | ID | LRT Jabodebek | **Country only** (the same national OSS register) | — |
| Palembang | ID | Palembang LRT, 13 stations | **Country only** | — |
| Yangon | MM | Circular line (commuter) | Not in scope | — |

### Central Asia

| City | Country | System | Status | Evidence |
|---|---|---|---|---|
| Tashkent | UZ | Tashkent Metro | BAND R | `city_master_list.md:162` |
| Samarkand | UZ | Samarkand tram (2017) | **Country only** (Tashkent's national hosts refuse this machine) | — |
| Almaty | KZ | Almaty Metro, 11 stations (kn) | **NEVER RECORDED** (staging draft only) | `docs/decisions_drafts/staging.md:18` |
| Astana | KZ | Astana LRT, 18 stations, opened 2026-05-16 | **NEVER RECORDED** | — |
| Pavlodar, Oskemen, Temirtau | KZ | Soviet-era tram networks | **NEVER RECORDED** | — |
| Ashgabat | TM | Olympic-village monorail (not transit) | Not in scope | — |

### Middle East

| City | Country | System | Status | Evidence |
|---|---|---|---|---|
| Tehran, Mashhad, Isfahan, Shiraz, Tabriz, Karaj | IR | metros | COUNTRY RULED OUT (left out like Russia, owner 2026-09-28) | `city_master_list.md:406`; `global_country_shortlist.md:2113` |
| Baghdad | IQ | none | Not in scope | — |
| Tel Aviv | IL | Red Line (Dankal) | DISCARDED on the municipality's own terms | `city_master_list.md:294` |
| Jerusalem | IL | JLR Red Line (~23 stations) and Green Line L3 (opened 2026-08-21) | **NEVER RECORDED** (staging draft only) | `docs/decisions_drafts/staging.md:17` |
| Petah Tikva, Bat Yam | IL | Red Line termini | Named in passing only (never screened) | `city_master_list_evidence.md:710` |
| Bnei Brak, Ramat Gan | IL | Red Line (underground section) | **NEVER RECORDED** | — |
| Haifa | IL | Carmelit (funicular subway), Metronit (BRT) | Not in scope (funiculars are left out, Takamatsu precedent) | — |
| Riyadh | SA | Riyadh Metro, 6 lines | BAND R | `city_master_list.md:161` |
| Mecca | SA | Al Mashaaer Metro (Hajj season only) | **NEVER RECORDED** (fails frequency) | — |
| Dubai | AE | Metro Red and Green, Tram | BAND R | `city_master_list.md:158` |
| Abu Dhabi, Sharjah, Kuwait, Bahrain, Oman, Jordan, Lebanon | — | none | Not in scope | — |
| Doha | QA | Doha Metro, Msheireb tram | DISCARDED (MOCI counts only) | `city_master_list.md:282` |
| Lusail (Al Daayen), Al Rayyan | QA | Lusail Tram plus Red Line; Education City Tram plus Green Line | **Country only** (national portal enumerated; MOCI counts by municipality) | `global_country_shortlist.md:2105` |

### Africa

| City | Country | System | Status | Evidence |
|---|---|---|---|---|
| Algiers | DZ | Metro Line 1, tram | DISCARDED | `city_master_list.md:281` |
| Oran, Constantine, Sidi Bel Abbès, Ouargla, Sétif, Mostaganem | DZ | tramways (2013-2023) | **Country only** (CNRC paid lookup; ONS counts by wilaya) | `global_country_shortlist.md:2105` |
| Cairo | EG | Cairo Metro, East Nile Monorail (2026), Cairo LRT | DISCARDED | `city_master_list.md:307` |
| Giza | EG | Cairo Metro Lines 2 and 3 | **Sibling only** (Cairo Governorate and CAPMAS) | — |
| Alexandria | EG | Alexandria tram (Raml line closed for rebuild, kn) | **Sibling/country only** | — |
| New Cairo / New Administrative Capital | EG | East Nile Monorail (22 stations, 06:00-18:00 only); Cairo LRT | **Sibling only**; likely fails all-day frequency | — |
| Casablanca | MA | tramway | DISCARDED | `city_master_list.md:491` |
| Rabat-Salé | MA | tramway | DISCARDED | `city_master_list.md:492` |
| Tunis (Ariana, Ben Arous, Manouba suburbs on the same network) | TN | Métro léger | DISCARDED (national catalogue enumerated, which covers the suburbs) | `city_master_list.md:493` |
| Addis Ababa | ET | light rail | DISCARDED | `city_master_list.md:495` |
| Lagos | NG | Blue and Red Lines | DISCARDED | `city_master_list.md:494` |
| Abuja | NG | Abuja Light Rail (4 trips a day per line since 2024-05) | **NEVER RECORDED** (fails frequency) | — |
| Port Louis, Beau Bassin-Rose Hill, Quatre Bornes, Vacoas-Phoenix, Curepipe | MU | Metro Express light rail, 22 stations, every 8-10 min at peak, 06:00-19:00 | **NEVER RECORDED** | — |
| Johannesburg, Tshwane (Pretoria), Ekurhuleni | ZA | Gautrain (commuter-grade spacing) | **NEVER RECORDED** (likely fails the commuter-rail test; South Africa sits in the "single-feed tail" by country only) | `global_country_shortlist.md:1443` |
| Dakar | SN | TER Dakar (regional express) | **NEVER RECORDED** (likely fails the commuter-rail test) | — |
| Nairobi, Cape Town | KE, ZA | commuter only | Not in scope | — |
| Abidjan | CI | Metro Line 1 under construction | Not open | `global_country_shortlist.md:3235` |
| Réunion (CIREST) | FR | (Europe agent; recorded as school buses flagged tram) | DISCARDED pattern | `city_master_list.md:400-406` |

---

## Japan (separate, as briefed)

Japan was scoped systematically on 2026-10-02. The universe has 114 uncovered
municipalities: every designated and core city, every city of 200,000 or
more, and **every municipality with a subway, tram, monorail, AGT or Linimo
station**. That universe sits in an untracked scratchpad
(`C:\Users\dacek\AppData\Local\Temp\claude\...staging\dcee6a2e-515e-4cee-ba88-0643d5433468\scratchpad\japan_wave2\SCOPE.md`,
`universe_mhlw.csv`), not in the repository. Wave 2 briefed the top tier. The
remainder is summarised in `docs/handoff_staging_2026-09-30.md:155-175`.
Grouped by what the tracked files say:

**A. Built 20, Band A 9, Band B 5, Band R 3, discarded 3**: every city in
the master list (`city_master_list.md:43-177, 318, 478-479`).

**B. Named in the wave-2 remainder** (`handoff_staging_2026-09-30.md:155-175`).
These are recorded and need no action from this sweep: Maebashi, Takasaki,
Shizuoka, Fukuyama, Funabashi, Matsudo, Ichikawa, Kanazawa, Kurashiki,
Sagamihara, Naha (16 monorail groups; "not yet searched for a city list"),
Hachiōji, Saitama, Niigata, Tottori, Yamagata, Morioka, Yao, Kure, Mito,
Takatsuki, Kōfu, Chigasaki, Matsumoto, Miyazaki.

**C. Mentioned only as a neighbour's excluded stations, or in passing.**
No verdict of their own: Suita, Toyonaka, Moriguchi, Kadoma, Settsu (Osaka's
excluded stations, `excluded_categories.md:2903-2904`); Amagasaki
(Nishinomiya brief); Akashi, Fujisawa, Chōfu, Nishitōkyō, Machida
(`excluded_categories.md`); Uji (Kyoto brief); Okazaki, Nisshin (Toyota
brief); Ino, Nankoku (Kōchi brief); Imizu (with Takaoka); Ichihara (Chiba
brief); Nagakute (Toyota's Linimo row); Tokushima (Takamatsu brief).

**D. No hit at all in any tracked file** (only in the untracked SCOPE
universe). "mode" means the city has a subway, tram, monorail or AGT station.
Station groups are N02's:

| City | Groups | Why it is in scope | Note |
|---|---|---|---|
| Tachikawa | 12 | mode: Tama Monorail 7 | Tama cluster; Tokyo Metropolitan health centres license food here, so the source may be Tokyo's own open-data catalogue, not MHLW |
| Hino | 10 | mode: Tama Monorail 5 | Tama cluster |
| Tama | 7 | mode: monorail 1 | Tama cluster |
| Higashimurayama | 8 | mode: monorail 1 | Tama cluster |
| Higashiyamato | 4 | mode: monorail 3 | Tama cluster |
| Kawaguchi | 8 | core + mode: Saitama Rapid Railway (subway-type) 6 | 600k people; MHLW cover 0.05, so a city list is needed |
| Kamakura | 16 | mode: Enoden and Shonan Monorail 6 | Kanagawa Prefecture licenses food here |
| Urayasu | 7 | mode: Tozai Line 1, Disney Resort Line 4 | Chiba Prefecture lists (the handoff's untried route for Matsudo and Ichikawa) |
| Ibaraki (Osaka) | 10 | 200k+ and mode: Osaka Monorail 6 | |
| Minoh | 5 | mode: Kita-Osaka Kyūkō 2 (2024 extension) | |
| Urasoe | 3 | mode: Yui Rail 3 | Naha's add-on |
| Sakura | 11 | mode: Yamaman Yūkarigaoka AGT 6 | |
| Ina (Saitama) | 5 | mode: New Shuttle 5 | |
| Wakō | 1 | mode: subway 1 | too small |
| Toyokawa | 19 | mode: 5 class-21 stations | |
| Tokorozawa, Ageo | 10, 4 | 200k+; class "monorail_agt" 2 each (likely mis-classed) | |
| Gifu, Hirakata, Kashiwa, Kawagoe, Koshigaya, Amagasaki*, Asahikawa, Iwaki, Kōriyama, Akita, Aomori, Fukushima, Ōita, Matsue, Hachinohe, Nagaoka, Ichinomiya, Kasugai, Kakogawa, Takarazuka*, Neyagawa, Tsu, Fuji, Ōta, Yamato, Kasukabe, Yachiyo, Itami, Isesaki, Saga, Sōka, Tsukuba, Atsugi, Hiratsuka, Fuchū* | 1-33 | core or 200k+, JR and private rail only | Covered in tracked files only by the handoff's pattern line "most Tokyo, Saitama, Ōsaka and Hyōgo satellites" (too few stations); *=a stray mention exists |

---

## Ranked: NEVER RECORDED and country/sibling-only cities (non-Japan)

Promise reflects rail quality and a plausible business route. None of this
is a screen.

| Rank | City | Status | Rail (desk) | Frequent? | Business route (one-line guess) | Portal |
|---|---|---|---|---|---|---|
| 0 | **Daejeon, Gwangju, Gimhae** (Band R, not new) | R, re-check | 22 / 20 / 12 stations | yes | **SEMAS national storefront file, already cached** for Incheon and Gyeonggi; check the rows for 대전, 광주 and 김해 | cache: `data/korea/raw/sbiz_15083033.zip` |
| 1 | **Siheung, Paju, Pyeongtaek** (+ Gunpo, Osan, Gwangmyeong, Hanam, Guri) | sibling only | Siheung: Seohae plus Suin-Bundang (~8-10, kn); Paju: Gyeongui-Jungang plus GTX-A (~8); Pyeongtaek: Line 1 (~8) | Seohae and Line-1 outer sections are borderline (15-20 min, kn) | SEMAS, the same module; storefront counts unmeasured for these three | as above |
| 2 | **Almaty** | never | Almaty Metro, 11 stations (kn) | yes (kn) | Kazakhstan's Statistical Business Register (stat.gov.kz) holds name, OKED, address and status, the shape of Tbilisi's Geostat. Its search has moved behind a login; one xlsx extract is public. Also the data.egov.kz national portal | stat.gov.kz; data.egov.kz |
| 3 | **Astana** | never | Astana LRT, 18 stations, 22.4 km, opened 2026-05-16 | yes (65-75k riders a day) | as Almaty | as Almaty |
| 4 | **Macau** | noted, never screened | LRT, ~14 stations (kn) | yes (kn) | IAM licenses food and drink premises; data.gov.mo is the official portal; DSEC counts 4,930 licensed F&B establishments (2024). Hong Kong's precedent | data.gov.mo |
| 5 | **Jerusalem** | never | Red Line (~23) plus Green Line L3 (since 2026-08-21) | yes | Municipal business licensing; the city runs an open-data catalogue (datacity.jerusalem.muni.il). Whether it holds a licence list is unconfirmed. Watch for Tel Aviv-style terms and the IP refusal Israel showed in 2026-09 | datacity.jerusalem.muni.il |
| 6 | **Ahmedabad (+ Gandhinagar)** | country only | ~45 stations (kn) | yes (kn) | AMC trade licences / Gujarat Shops and Establishments. The national catalogue carries only Ahmedabad's 2015-19 statistics. A city host has never been asked | national: data.gov.in |
| 7 | **Pune + Pimpri-Chinchwad** | country only | ~30 stations (kn) | yes (kn) | PMC's open-data portal (kn, unconfirmed); PCMC is separate | (kn) opendata.punecorporation.org |
| 8 | **Noida, Gurugram, Ghaziabad, Faridabad, Greater Noida** | country/sibling | Delhi Metro, Aqua Line, Rapid Metro: tens of stations each | yes | Each city's own trade licence; Haryana and UP state portals. Delhi's MCD verdict covers only NCT | — |
| 9 | **Nagpur, Lucknow, Jaipur, Kanpur, Indore, Bhopal, Meerut, Agra** | country only | 37 / 21 / 11 / ~15 / 11 / 8 / 12 / ~7 | mostly yes; Indore and Bhopal ridership thin | Smart-city portals (kn); none known to publish premises | — |
| 10 | **Navi Mumbai, Mira-Bhayandar, Thane; Howrah, Bidhannagar** | sibling only | 11; 3 (since 2026-04); Line 4 pending; 2-6 each | yes | Separate municipal corporations from MCGM and KMC; never asked | — |
| 11 | **Petah Tikva, Ramat Gan, Bnei Brak, Bat Yam** | never / in passing | Red Line segments (~22 stations outside Tel Aviv, kn) | yes | Each municipality's own licensing department; open-data portals unknown | — |
| 12 | **Port Louis + 4 towns (Mauritius)** | never | Metro Express, 22 stations | 8-10 min at peak, 06:00-19:00 | Municipal trade licences; the national portal is data.govmu.org (kn). A regional scope like Lille's | data.govmu.org (kn) |
| 13 | **Lahore** | never | Orange Line, 26 stations | yes (kn) | Punjab Food Authority / Excise registrations; no known open list | — |
| 14 | **Dhaka** | never | MRT Line 6, ~16 stations | yes (kn) | DNCC and DSCC online trade licences; no known open list | — |
| 15 | **Petaling Jaya, Subang Jaya, Shah Alam, Kajang, Putrajaya** | country/sibling | LRT and MRT lines | yes | Selangor councils license premises; data.gov.my's premises table is a 3,916-row sample | data.gov.my |
| 16 | **Lusail, Al Rayyan** | country only | Lusail Tram plus Red Line; Education City Tram plus Green Line | yes | MOCI counts only (Doha's row) | data.gov.qa |
| 17 | **Pavlodar, Oskemen, Temirtau** | never | Soviet trams | Temirtau thin (kn) | as Almaty | as Almaty |
| 18 | **Oran, Constantine, Sétif, Sidi Bel Abbès, Ouargla, Mostaganem** | country only | one tram line each | ~10-15 min (kn) | CNRC paid; nothing better known | — |
| 19 | **Nonthaburi, Samut Prakan, Pathum Thani** | sibling/country | MRT Purple and Pink, BTS extensions | yes | Thai national hosts refuse this machine (Band R shape) | — |
| 20 | **Bekasi, Depok, Palembang** | country only | LRT Jabodebek; Palembang LRT 13 stations | Palembang thin (kn) | National OSS register has no activity field | — |
| 21 | **Giza, Alexandria, New Cairo / NAC** | sibling only | Metro Lines 2 and 3; tram; monorail (daytime only) | monorail fails all-day | Cairo's no-register verdict | — |
| 22 | **Samarkand** | country only | one tram line | ? | Uzbek hosts refuse this machine | — |
| 23 | **Antipolo** | sibling | LRT-2 terminus | yes | data.gov.ph empty | — |
| 24 | **Cheonan, Asan** | never | Line 1 outer section | probably not (kn) | SEMAS | — |
| — | Rail fails or infeasible | never | Abuja (4 trips a day), Mecca (Hajj season), Gautrain cities and Dakar TER (commuter-grade), Patna (20-min headway), Pyongyang, Chongjin and Wonsan (no data) | no | — | — |

## Lists for the counts

**Covered only by a country or sibling verdict (58):** Noida, Greater Noida,
Ghaziabad, Gurugram, Faridabad, Bahadurgarh, Thane, Mira-Bhayandar, Navi
Mumbai, Howrah, Bidhannagar, Ahmedabad, Gandhinagar, Pune, Pimpri-Chinchwad,
Nagpur, Lucknow, Jaipur, Kanpur, Agra, Bhopal, Indore, Patna, Meerut (24
India) · Siheung, Paju, Pyeongtaek, Gunpo, Osan, Yangju, Dongducheon, Icheon,
Gwangju (Gyeonggi), Yeoju (10 Korea) · Petaling Jaya, Subang Jaya, Shah
Alam, Kajang, Putrajaya (5 Malaysia) · Nonthaburi, Samut Prakan, Pathum Thani
(3) · Antipolo · Bekasi, Depok, Palembang (3) · Samarkand · Lusail, Al Rayyan
(2) · Oran, Constantine, Sidi Bel Abbès, Ouargla, Sétif, Mostaganem (6
Algeria) · Giza, Alexandria, New Cairo/NAC (3 Egypt).

**NEVER RECORDED, no verdict of any kind (22 rows):** Jerusalem, Bnei
Brak, Ramat Gan, Petah Tikva and Bat Yam (named in passing only), Almaty,
Astana, Pavlodar, Oskemen, Temirtau, Lahore, Dhaka, Mecca, Cheonan, Asan,
Pyongyang, Chongjin, Wonsan, Abuja, Port Louis (Mauritius, with four towns),
Johannesburg/Tshwane/Ekurhuleni (Gautrain, one row), Dakar.
Macau is "noted, never screened" (DECISIONS only).
