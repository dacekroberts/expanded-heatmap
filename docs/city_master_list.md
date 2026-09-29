# Global city master list — CURRENT STATE

**This is the operative list: which cities this project could build next, and
what is stopping each one.** It is rewritten as things change, like
`docs/project_context.md` and unlike `DECISIONS.md`.

**The evidence lives in [`docs/global_country_shortlist.md`](global_country_shortlist.md)** —
87 countries screened, every probe logged, every negative with the measurement
behind it. That file is the trail; this file is the answer. When they disagree,
the trail wins and this file is stale.

**Drift-corrected 2026-09-23**, after Marseille was built: counts, the band
table, Marseille's row, Hong Kong's geocode rate, Göteborg's row count, Cairo
(moved out of the discards onto the open screening gap, by this file's own
rule) and the by-country view, which had stopped being current a day earlier.

Last reordered **2026-09-22**, after the browser sweep — Tier 5 closed
(7 negatives, no survivors), Tier 6 reached for the first time, and three
food-authority probes run. **Stockholm** and **Bucharest** were promoted out
of the band that used to read *"never actually reached"*; five cities moved to
discarded on measurement.

**The method that produced all of it:** open the portal in a real browser
*before* concluding anything about it, then enumerate providers rather than
search keywords. Both are written up in `.claude/skills/add-country/`
(§3 and §2) and `add-city` Step 0.

---

> ## ✅ Settled state — 2026-09-22
>
> **Every candidate on this list has a measured business leg, a named next
> step, and no unexamined route.** Nothing here is carried on a guess, a
> search result, or a host that was never asked properly.
>
> | | |
> |---|---|
> | **Built** | **55** across 17 countries *(Tokyo, Japan's sixth and last, 2026-09-28; Kyoto, Japan's fifth, 2026-09-28; Fukuoka, Japan's fourth, 2026-09-28; Sapporo, Japan's third, 2026-09-28; Osaka, Japan's second, 2026-09-27; Kobe, Japan's first, 2026-09-27; Monterrey (Regional), Daegu and Busan, 2026-09-27; Seoul, Taichung, Taoyuan and Taipei (Regional), 2026-09-25; Riga, Hong Kong and Rotterdam, 2026-09-24; Toulouse, Lille (Regional) and Rennes, 2026-09-23; Oslo, Copenhagen, Prague, Amsterdam and Rome, 2026-09-24; Brazil's nine cities as one batch, 2026-09-24)* |
> | **Candidates** | **74**, all at least partially viable — A 0 · B 6 · C 0 (closed) · D 12 · N 5 · T 51 *(**Delhi to D 2026-09-28** from the transit-gap re-screen, owner's call: its current register sits behind a CAPTCHA and the state hosts refuse this machine; **Tokyo built 2026-09-28**, Japan's sixth and last, leaving A empty; **Berlin to B 2026-09-28** from the discards, owner's call: IHK Berlin's premises register, shops and food; **Istanbul to N 2026-09-28** from the transit-gap re-screen, owner's call: pharmacies and opticians only; **Dubai to D 2026-09-28** from the transit-gap re-screen, owner's call: its register's hosts refuse this machine; **London to B 2026-09-28** from the transit-gap re-screen, owner's call: food only on the FSA register; **Kyoto built 2026-09-28**, Japan's fifth, leaving A; **Fukuoka built 2026-09-28**, Japan's fourth, leaving A; **Sapporo built 2026-09-28**, Japan's third, leaving A; **Band C's last five given verdicts 2026-09-28 (owner)**: Band B reopened for the passed (Stockholm, Bucharest, Incheon, the Gyeonggi satellites), Band N created for no page (Singapore, Yokohama, Palma, Baltimore), Ottawa to T, Band C closed; **Osaka built 2026-09-27**, Japan's second, leaving A; **wave 2's US screen 2026-09-28**, owner's calls: New Orleans, Tucson, Houston, Sacramento, Buffalo, Pittsburgh and Minneapolis to T, Baltimore to C; **wave 2's second group 2026-09-28** (Spain, Italy), owner's calls: Florence and Santa Cruz–La Laguna (Regional) to T, Palma to C; **Kitchener–Waterloo (Regional) to T 2026-09-27 from wave 2's first group** (Canada, Brazil, Ireland), owner's call: T, not A, since ION has no metro; **Kobe built 2026-09-27**, Japan's first, leaving A; **Band T renamed "Contingent on trams" 2026-09-27 and five moved into it from C** (Zurich, Göteborg, Hiroshima, Utrecht, Den Haag), owner's call; **the 2026-09-27 second-city screens, owner's calls**: Daegu and Busan to A, reopened on their cities' own portals, and **both built the same day**, leaving A; **32 trams-only cities to T** (France 21, Czechia 6, Denmark 2, Latvia 2, Norway 1), edge networks tagged rather than promoted; Den Haag, Utrecht, Rijswijk, Delft, Incheon and the Gyeonggi satellites to C, whose caption widened to buckets with a measured gap; Daejeon, Gwangju and Gimhae to D; **Monterrey (Regional) to A 2026-09-27** and built the same day, Mexico's third city, screened on DENUE and OSM rail, its old rail-only negative obsolete; **Band T, trams only, created by the owner 2026-09-27, with the first-blocker rule made universal**; **Seoul, Taichung, Taoyuan and Taipei (Regional) built 2026-09-25**, leaving Band A; **the open gap emptied 2026-09-24 after a final re-probe, owner's calls**: Riga to A (tram rings, scoped vacancy disclosure), Yokohama to C (personal services only, no page for now), Lisbon, Helsinki and Tallinn to D, Vienna, Santiago and Nagoya to the discards; **Hong Kong, Rotterdam and Brazil's nine built 2026-09-24**, leaving Band A by being built; Kyoto from the open gap to A 2026-09-24 — its register rebuilt from the permit stream, owner's call; **Japan re-banded 2026-09-24 and the geocoding band closed** — Tokyo (8 wards), Osaka, Kobe, Sapporo and Fukuoka to A, Hiroshima to C, Sendai to D, Yokohama, Nagoya and Kyoto to the open gap; Rotterdam from the open gap to A; all owner's calls; Warsaw and Hyderabad to D 2026-09-24 from the open gap, owner's calls — each geo-blocked before measurement; Copenhagen, Prague, Amsterdam and Rome built 2026-09-24; Amsterdam to A 2026-09-24 — permits + BAG shop units, both licences read, owner's call; Amsterdam from the discards to C earlier the same night; Rome to A 2026-09-24 — SUAP premises joined to ANNCSU, owner's call with a build check; Prague back to A 2026-09-24 on open data — ROS02 establishments + RES; Kaohsiung moved from B to a reopened access-blocked band D 2026-09-23, owner's call; Brazil re-screened 2026-09-23: +7 cities, and São Paulo and Rio moved from B to A; Taipei (Regional), Taoyuan and Taichung moved from B to A the same evening; Rennes built; Prague paused to the open gap 2026-09-24)* |
> | **Open screening gap** | **0** — **emptied 2026-09-24** by a final re-probe of its last eight, each given a verdict (owner's calls) *(before that: Kyoto out again to A later the same day, on a rebuilt register; Yokohama, Nagoya and Kyoto in, Rotterdam out to A, 2026-09-24; ten left 2026-09-24 on the owner's calls after their re-probes: eight to the discards, Warsaw and Hyderabad to D)* |
> | **Discarded** | **84**, each naming its evidence *(**Mumbai 2026-09-28** from the transit-gap re-screen, owner's call: no storefront list on the city's or state's reachable hosts; **Munich, Frankfurt and Cologne 2026-09-28** from the transit-gap German screen, owner's call: no premises register on a full enumeration; **Berlin out to Band B** the same day; **Manila 2026-09-28** from the transit-gap re-screen, owner's call: no business list at any level; **sixteen from wave 2's US screen 2026-09-28**, owner's calls: Portland, Cleveland, Salt Lake City, Phoenix, Mesa, Honolulu, St. Paul, Oklahoma City, El Paso, Atlanta, Norfolk, Milwaukee, Detroit, Tampa, Cincinnati, Berkeley; **thirteen from wave 2's second group 2026-09-28**, owner's calls: Genoa, Palermo, Bergamo, Sassari, Padua, Venice-Mestre, Bologna, Vitoria-Gasteiz, Murcia, Granada, Jaén, Fuenlabrada, Zaragoza; **eleven from wave 2's first group 2026-09-27**, owner's calls: Laval, Longueuil, Brossard, Vaughan, Cork, Sobral, Juazeiro do Norte / Crato, Teresina, Maceió, João Pessoa, Natal; Denver, Dallas and Brampton 2026-09-27, whose discards were recorded only in the archived DECISIONS; San Jose, Fort Worth, Austin and Charlotte, moved in from the retired `docs/city_shortlist.md` 2026-09-27, with Kansas City, which went on to Band T the same day; Tainan, Hsinchu, Trondheim, Aubagne, Clermont-Ferrand and Saint-Louis from the 2026-09-27 second-city screens, on rail; Vienna, Santiago and Nagoya from the open gap 2026-09-24 after the final re-probe, owner's calls; Kuala Lumpur, Athens, Poznań, Bratislava, Hamburg, Naples, Lima and Messina from the open gap 2026-09-24, owner's calls after their re-probes; an audit moved 12 single-method rows to the open gap and Amsterdam to Band C, 2026-09-24; the evidence check moved 5 more the same night)* |
>
> *Counts corrected 2026-09-23. This box had read 20 / 33 / 30 since
> 2026-09-22 while the sections below moved on — **the hand-kept summary is
> the first thing to drift, which is why the band sections are the ones to
> trust.***
>
> **What this day changed.** Four bands closed because their condition stopped
> being true of their members. **Seven cities were reached by going to a
> different HOST rather than a different network** — Sofia, Sevilla, Tel Aviv,
> Tallinn, Prague, Dublin and Hong Kong — and *unreachable* turned out to mean
> *not yet asked properly* in every single case.
>
> **Three recorded negatives turned out to be statements about a SEARCH rather
> than about the data**: Stockholm's register is called `Tillsynsverksamheter`,
> a word no query contained; Zurich's catalogue was matched over 938 of 1,128
> names; Hong Kong's bulk export was on `data.gov.hk` the whole time and the
> dataset list had never been requested. **Each cost one HTTP call to
> disprove.** India was then swept in full — 288,011 titles — specifically so
> it would not become the fourth.
>
> **This claim is dated because it will stop being true.** The next probe, the
> next build, or the next licence read changes it, and the counts in the table
> below are the ones to trust over any prose that repeats them.

## Built — 55

| Country | Cities |
|---|---|
| **United States** (9) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |
| **Mexico** (3) ✅ | **Mexico City** · **Guadalajara (Regional)** — built 2026-09-22, live in the app. · **Monterrey (Regional)** — **built 2026-09-27**, Mexico's third (`pages/47_Monterrey_Heatmap.py`; **58,565 storefronts, 38 stations**, Metrorrey Líneas 1–3 across four municipios): the national DENUE modules unchanged, the scope keyed on INEGI's municipio code, rail from OpenStreetMap with gate 3 exact (19 / 13 / 9) and Línea 3 in the operator's red; publishes with the next batch |
| **Europe** (16) ✅ | 🇱🇻 **Riga** — **built 2026-09-24**, Latvia's first (`pages/42_Riga_Heatmap.py`; **6,730 storefronts, 108 stations**, Rīgas satiksme's seven tram routes): food from the State Revenue Service's excise-licence register, joined to the city's own address points (96.8%), and shops and services from the cadastre's trade premise groups at their building footprints (99.4%); the vacancy disclosure scoped to the historic centre, and a Europe view that keeps its zoom with Riga a pan away on phones (owner). · 🇪🇸 **Madrid** · **Barcelona** · 🇮🇪 **Dublin (Regional)** · 🇮🇹 **Milan** · **Rome** · 🇫🇷 **Paris** · **Marseille** · **Toulouse** · **Lille (Regional)** · **Rennes** · 🇳🇴 **Oslo** · 🇩🇰 **Copenhagen** · 🇨🇿 **Prague** · 🇳🇱 **Amsterdam** · **Rotterdam** — **Rotterdam built 2026-09-24**, the Netherlands' second (`pages/40_Rotterdam_Heatmap.py`; **7,520 storefronts, 132 stations**, RET metro A–E and trams 1–8 and 11, gemeente only): Amsterdam's shape with the food layer REBUILT from the permit decisions Rotterdam publishes in its Gemeenteblad (1,939 premises), BAG shop units for the rest, and the metro and tram network measured on the timetable after a works period whose temporary trams 14 and 18 had looked like permanent lines. **Rome built 2026-09-24**, Italy's second (`pages/30_Rome_Heatmap.py`; **98,897 storefronts, 87 stations**, Metro A, B, B1 and C and the Roma–Viterbo urban service, comune only): Roma Capitale's SUAP premises register JOINED to ANNCSU house numbers at 95.7%, no names, and the food layer stated as an upper bound (2.67x OSM, no closing dates). **Amsterdam built 2026-09-24**, the Netherlands' first (`pages/29_Amsterdam_Heatmap.py`; **13,238 storefronts, 144 stations**, GVB metro 50–54 and 16 tram lines, gemeente only): the city's live hospitality-permit register for food, the BAG's shop-class units for everything else - one "Shops and services" category, because a building register cannot tell a hairdresser from a clothes shop - de-duplicated by address, and trams thinned with the sub-transit-line filters. **Prague built 2026-09-24**, Czechia's first (`pages/28_Prague_Heatmap.py`; **25,275 storefronts, 58 stations**, metro A, B and C): ROS02's establishments where they trade, the owner's activity from RES's CZ-NACE 2025, a RUIAN join for the point, and every natural person's or partnership's name replaced by its address - their premises at the owner's own seat left off. **Copenhagen built 2026-09-24**, Denmark's first (`pages/27_Copenhagen_Heatmap.py`; **14,978 storefronts, 64 stations**, Metro and S-tog, Copenhagen with Frederiksberg): CVR production units joined across six national files, coordinates JOINED to DAR, and every personally owned business shown by its address. **Oslo built 2026-09-24**, Norway's first city (`pages/26_Oslo_Heatmap.py`; **10,718 storefronts, 155 stations**, T-bane and trams, kommune only): an establishment register keyed on the PHYSICAL location address, coordinates JOINED to Kartverket's bulk address file, and every sole trader's name replaced by its address. the first four built and deployed 2026-09-22, Paris deployed 2026-09-23, **Marseille built and deployed the same day** (`pages/22_Marseille_Heatmap.py`; **18,177 storefronts, 66 stations**), **Toulouse** likewise (`pages/23_Toulouse_Heatmap.py`; **8,635 storefronts, 48 stations**), **Lille (Regional)** likewise (`pages/24_Lille_Heatmap.py`; **11,833 storefronts, 91 stations**) — **the first French city scoped regionally**, to the eleven communes its network serves, because the commune alone would have drawn the tram as a three-stop stub — and **Rennes built and deployed the same day** (`pages/25_Rennes_Heatmap.py`; **3,479 storefronts, 24 stations**), commune-only because its worst line keeps 11 of 15 stations, **which completes France at five cities**. **France is the first country here where the second city was materially cheaper than the first**: Marseille inherited the national register, the NAF taxonomy, the parquet cache and the Lambert-93 grid, and its own work was the scope measurement and the rail leg. That is Mexico's retrospective repeating, and the opposite of Spain's. **Toulouse made the third city cheaper again**: it downloaded nothing at all, because the 3 GB national parquet pair was already cached for the country, and its own work was one scope decision, one owner call, and a gate-3 run that matched the operator exactly on all four lines. It is also the first city anywhere here to draw a **non-rail mode** — the Téléo cable car — which was the owner's call after the brief's stated precedent for it turned out not to exist. **One macro-map region, not one per country**: Spain, Ireland and Italy were three regions holding four cities until they were collapsed the same day, which is what let France join without adding a sixth region. Spain is complete at two cities, Ireland at one, and Italy is a Milan-only country — so the countries are still the research unit, and only the MAP groups them. ⚠️ **France's own viability figure was corrected on the day Paris was built**: the recorded "50,156 storefronts, 92.5% of OSM" is not reproducible and the real ratio is about 1.78× — see `docs/build_briefs/paris.md`. France remains a build; `docs/global_country_shortlist.md`'s France row still carries the old number |
| **South America** (9) ✅ | 🇧🇷 **São Paulo** · **Rio de Janeiro** · **Belo Horizonte** · **Brasília** · **Salvador** · **Fortaleza (Regional)** · **Porto Alegre (Regional)** · **Recife (Regional)** · **Santos (Regional)** — **built 2026-09-24 as one batch** (`pages/31`–`39`; **617,188 storefronts, 363 stations**), the first country built that way: every city to drafts, one review of all the text, one deploy check and one push. One national source, IBGE's CNEFE 2022 - the census's walk of every block, each establishment with the enumerator's description and a coordinate - read by a free-text classifier (`pipeline/taxonomies/brazil_cnefe.py`); unreadable descriptions dropped and disclosed, and only the category shown at an address that is also a home. Commuter lines went through the three-part rail test: São Paulo's CPTM Linha 9 and Rio's SuperVia Deodoro and Saracuruna drawn, the rest out. The macro map's **South America** region |
| **East Asia** (13) ✅ | 🇯🇵 **Tokyo** — **built 2026-09-28**, Japan's sixth and last (`pages/55_Tokyo_Heatmap.py`; **63,989 storefronts, 490 stations**, 52 lines across JR East, Tokyo Metro, Toei and eleven other operators, the 23 wards): each ward its own source - eight wards' own food lists, MHLW's filings for four, four wards' registers - JOINED to MLIT's address blocks (99.7% block); the fifteen wards with no usable list drawn as hollow stations, each ward's share of the official count on the page; JR East drawn as its nine services, and every line labelled by its operator's code (owner). · 🇯🇵 **Kyoto** — **built 2026-09-28**, Japan's fifth (`pages/54_Kyoto_Heatmap.py`; **32,355 storefronts, 117 stations**, the Kyoto Municipal Subway, JR West, Keihan, Hankyu, Kintetsu, the Randen and Eiden - 18 lines, city line only): a food register REBUILT from the 2021 list and every monthly list since, pinned at 2026-07-31 and disclosed as an upper bound (closures unseen), with the barber, beauty and laundry lists, JOINED to MLIT's address blocks (93.2% block) past Kyoto's street-corner addresses; the funiculars left out (owner). · 🇯🇵 **Fukuoka** — **built 2026-09-28**, Japan's fourth (`pages/53_Fukuoka_Heatmap.py`; **30,062 storefronts, 71 stations**, the Fukuoka City Subway's three lines, JR Kyushu and Nishitetsu, city line only): the first two-source Japanese city - the city's pre-2021 food list and MHLW's online filings, one pin where a premises is in both - with the barber, beauty and laundry registers, JOINED to MLIT's address blocks (98.1% block, MHLW's own point where the join misses); about one restaurant in five withheld its address (disclosed); Fukuoka's yatai counted (owner). · 🇯🇵 **Sapporo** — **built 2026-09-28**, Japan's third (`pages/52_Sapporo_Heatmap.py`; **28,674 storefronts, 95 stations**, the Sapporo Municipal Subway's three lines, the streetcar loop and JR Hokkaido, city line only): the city's food-permit list and its barber, beauty, laundry and coin-laundry registers JOINED to MLIT's address blocks (86.0% block, 13.9% at the block group on Sapporo's 条 grid, 0.1% unplaced), almost entirely as a config on the shared Japanese modules; station names in one style with block numbers as figures (owner). · 🇯🇵 **Osaka** — **built 2026-09-27**, Japan's second (`pages/51_Osaka_Heatmap.py`; **72,999 storefronts, 216 stations**, Osaka Metro's eight lines and the New Tram, JR West, Hankyu, Hanshin, Keihan, Kintetsu, Nankai and the Hankai tram - 34 lines, city line only): Kobe's shared steps with a config, the city's food-permit list and 生活衛生 registers JOINED to MLIT's address blocks (99.1% block, 13 unplaced), checked against the list's own coordinates at a median 38 m; the map with the most lines here, which took a measured colour search and a third label pass (owner). Publishes after Kobe. · 🇯🇵 **Kobe** — **built 2026-09-27**, Japan's first (`pages/50_Kobe_Heatmap.py`; **27,251 storefronts, 121 stations**, the subway, Port and Rokkō Liners, JR, Hankyu, Hanshin, Sanyō, Kobe Kōsoku and Kobe Electric, city line only): the city's food-permit list and 生活衛生 registers JOINED to MLIT's address blocks (97.3% block, 0.3% unplaced), rail from MLIT N02 collapsed on its station-group code, English station names from OSM, and a trade name that is the operator's own name shown by its permit type (owner). The shared Japanese steps (`pipeline/countries/japan_step1.py`, `japan_step2.py`) are for the cities after it. · 🇰🇷 **Busan** — **built 2026-09-27**, South Korea's third (`pages/49_Busan_Heatmap.py`; **89,798 storefronts, 110 stations**, Busan Metro Lines 1–4, Line 4 a monorail, and the Busan–Gimhae LRT): the same fourteen permit types through the city's keyless API, each pulled in full and never by state (which drops every permit since 2025-02), through Daegu's shared Korean module; frozen at 2026-04-15 and the rows agree; held for a batch publish. · 🇰🇷 **Daegu** — **built 2026-09-27**, South Korea's second (`pages/48_Daegu_Heatmap.py`; **67,212 storefronts, 86 stations**, Daegu Metro Lines 1–3, Line 3 a monorail): fourteen of the national permit registers from the city's own portal, read through a new shared Korean module that refuses the column renames Seoul's code would read as nothing; the rows end 2025-08-31 whatever the edition's label says (owner: build, date disclosed); held for a batch publish. · 🇹🇼 **Taipei (Regional)** — **built 2026-09-25**, Taiwan's third (`pages/46_Taipei_Heatmap.py`; **133,335 storefronts, 153 stations**, twelve metro and light-rail lines across Taipei and New Taipei): each city's own door plates through the shared step 2, the join's control reproduced (92.4%), and gate 3 exact on Taipei Metro's lines. · 🇹🇼 **Taoyuan** — **built 2026-09-25**, Taiwan's second (`pages/45_Taoyuan_Heatmap.py`; **45,014 storefronts, 15 stations**, the Airport MRT inside Taoyuan): Taichung's national modules and shared step 2, a TWD97 door-plate file reprojected, and stations from the national land-survey layer, whose own addresses say which city each is in. · 🇹🇼 **Taichung** — **built 2026-09-25**, Taiwan's first (`pages/44_Taichung_Heatmap.py`; **66,115 storefronts, 18 stations**, Taichung Metro's Green Line): the national business tax register joined to the city's door plates (92.2%), keyed by district because one street name recurs across districts; office-like company head offices dropped and unmarked sole proprietors shown by their line of business (owner's rules). The national modules and the `taiwan-city` skill came out of it. · 🇰🇷 **Seoul** — **built 2026-09-25**, South Korea's first (`pages/43_Seoul_Heatmap.py`; **239,410 storefronts, 308 stations**, Lines 1–9, Shinbundang, Ui LRT, Sillim and three Korail lines): seventeen of Seoul's citywide permit registers, each premises at its own building point or at another permit's at the same building (98% placed), one pin per premises with the five convenience-store chains matched by brand, and a Korean personal-name pass that withholds 138 names at home addresses. Rail from OpenStreetMap, since Korea's station dataset has no lines. · 🇭🇰 **Hong Kong** — **built 2026-09-24** (`pages/41_Hong_Kong_Heatmap.py`; **21,135 storefronts, 141 stations**, MTR's eight urban lines and the Light Rail): FEHD's three licence registers, each licence at FEHD's own point from the same registers on the CSDI Portal - the brief's address geocode was never needed - and a map that is mostly restaurants, because Hong Kong licenses food and not general retail. Rail from OpenStreetMap, since MTR publishes no geometry; gate 3 exact against MTR's own station lists. The macro map's **East Asia** region, named for the Taiwanese, Korean and Japanese cities behind it |

✅ **Mexico is the first country built outside North America's anglophone
pair**, and the first where the rail leg came from **OpenStreetMap** rather
than an agency feed — the per-city exception approved for CDMX, which
validated at 195/195 stops exact.

✅ **Spain is the first country in EUROPE**, and the first where the two cities
did not generalise to each other in any leg. Different rail sources (Madrid
takes CRTM's own ArcGIS layers, Barcelona OpenStreetMap), different projected
CRS (25830 against 25831), different taxonomy LEVELS of similar four-level
schemes — Madrid keys on its division, Barcelona on its finest level, and each
for a measured reason. Both carry the same accommodation trap and it bites at a
different depth in each. Barcelona is also the first source in the project to
impose an obligation that is **an act rather than a notice**: its terms require
the City Council to be informed of every derived project.

## Candidates — 74

Re-tiered 2026-09-22 after the browser sweep closed Tier 5 and reached Tier 6.
**Eight cities moved to discarded on measurement** and **two were upgraded**.

**Four of those were sitting in Band D as "unreachable", and all four were
reached by going to a different HOST rather than a different network** —
Sofia via `data.europa.eu`, Sevilla and Tel Aviv via the ArcGIS service host
behind a walled portal, Tallinn via a bulk export its catalogue entry named.
Three then measured negative and **one, Tel Aviv, is now the strongest
unbuilt candidate outside Band A.** *Unreachable* turned out to mean *not yet
asked properly* in every single case.

**Re-banded 2026-09-22 so that every caption names the kind of work that
unblocks its cities**, after an audit found five rows whose text named a
blocker their band did not. Band D dissolved: its two live sub-tiers were
about different things and were siblings only because both arrived through
the same screen.

**The one-bucket band (now D) was added the same day** for a state the scheme
could not express: a city whose screening is **complete and successful** but
which yields only one bucket. Those two were sitting in "a decision to make"
beside a city waiting on a licence read, which conflated *we have not looked
yet* with *we looked at everything and this is what is there*.

| Band | What these cities ARE | Cities |
|---|---|---|
| 🟢 **A** | **Ready to build.** Register measured, licence read, coordinates answered, rail answered — every remaining question is answerable inside the build | **0** *(+ 41 built; Tokyo built 2026-09-28; Kyoto built 2026-09-28; Fukuoka built 2026-09-28; Sapporo built 2026-09-28; Osaka built 2026-09-27; Kobe built 2026-09-27; corrected 2026-09-27 from a stale 10 + 28, then Monterrey added and built the same day; Daegu and Busan 2026-09-27, both built the same day)* |
| 🔵 **B** | **Passed: narrower pages** (reopened by the owner 2026-09-28 for the cities that passed the Band C memo). Screening complete; the page shows one bucket, or all three with a measured gap, and says what is missing *(Stockholm and Bucharest passed 2026-09-27; Incheon and the Gyeonggi satellites 2026-09-28; London and Berlin 2026-09-28, from the transit-gap re-screen. The letter's earlier band, geocoding at national scale, closed 2026-09-24)* | **6** |
| ~~🟣 **C**~~ | ~~**One bucket only, or buckets with a measured gap**~~ **CLOSED 2026-09-28**: its last five got verdicts (owner): Incheon and the Gyeonggi satellites to B, Ottawa to T, Palma and Baltimore to N; Stockholm and Bucharest had passed 2026-09-27 and moved to B | **0** |
| 🔴 **D** | **Access blocked by the publisher.** Screening complete, the file exists and is measured; the publisher's own access control is the only thing stopping it, so it is unblocked by ASKING, not by probing *(Warsaw and Hyderabad, 2026-09-24: blocked before measurement — a read from inside the country first; Sendai, 2026-09-24: the city's permission; Lisbon, Helsinki and Tallinn, 2026-09-24: a free account, and two geo-blocks; Tallinn also trams only; Daejeon, Gwangju and Gimhae, 2026-09-27: no city portal, and the national one behind a residency and CAPTCHA wall; Dubai, 2026-09-28: every host of its register refuses this machine; Delhi, 2026-09-28: the current register behind a CAPTCHA)* | **12** |
| ⚪ **N** | **No page for now** (created by the owner 2026-09-28). Screening complete; a page is not worth building on what is published, and the row stays so a change in the source can reopen it *(Singapore, verdict 2026-09-27; Yokohama, 2026-09-24; Palma and Baltimore, 2026-09-28; Istanbul, 2026-09-28, from the transit-gap re-screen)* | **5** |
| 🟤 **T** | **Contingent on trams** (created by the owner 2026-09-27 as "trams only", renamed the same day). The build waits on the owner's yes to trams-only maps: the rail is trams, streetcars or street-running light rail with no metro. Most passed screening on two or more buckets; five also carry a Band C gap (moved from C, owner 2026-09-27). It waits on one decision about the group, deferred until the full tram list and the second-wave screens. Riga (built 2026-09-24) is the precedent. **Edge networks** (light rail partly built to metro standard) stay here tagged EDGE, owner's call 2026-09-27 | **51** *(Ottawa from Band C 2026-09-28; seven US cities from wave 2, owner 2026-09-28; Florence and Santa Cruz–La Laguna from wave 2, owner 2026-09-28; Kitchener–Waterloo from wave 2, owner 2026-09-27; Rijswijk and Delft from C as Den Haag add-ons, owner 2026-09-27; 32 from the 2026-09-27 second-city screens; Kansas City from the discards; five from Band C; all owner 2026-09-27)* |
| | **Candidates** | **74** *(Delhi to D 2026-09-28 (owner); Tokyo built 2026-09-28; Berlin from the discards to B 2026-09-28 (owner); Istanbul to N 2026-09-28 (owner); Dubai to D 2026-09-28 (owner); London to B 2026-09-28 (owner); Kyoto built 2026-09-28; Fukuoka built 2026-09-28; Sapporo built 2026-09-28; Band C's last five given verdicts 2026-09-28, and C closed (owner); Osaka built 2026-09-27; eight US cities from wave 2 2026-09-28; Florence, Santa Cruz–La Laguna and Palma from wave 2 2026-09-28; Kitchener–Waterloo from wave 2 2026-09-27; corrected 2026-09-27 from a stale 24 to 20, then Monterrey added; 43 more from the second-city screens the same day; Kansas City from the discards; Ottawa to C; Monterrey, Daegu and Busan built; Kobe built)* |
| *Open gap* | Unscreened — a row resting on an absence, so not a discard | *0 (emptied 2026-09-24)* |
| *Discarded* | Measured negative, evidence named | *84* |

*Band A's caption briefly said "brief written" (2026-09-23, morning). That was
wrong by `CLAUDE.md`'s own rule — **a brief is a cache, not a prerequisite** —
and it was removed the same day, when nine Brazilian cities met every other
condition without one.*

⚠️ **This table read A 9 / B 10 / C 12 / D 2 until 2026-09-23** — the
pre-renumber counts, left standing under two renumbers that each updated the
section headings below and not this summary. **The headings were right; the
table summarising them was not.**

**Renumbered 2026-09-22 to close the gaps left by four band closures.** The
live set is now contiguous, and **the closed bands have lost their letters
rather than keeping them** — a closed band's letter was never the interesting
part of it, the condition that stopped being true is.

| Old letter | Now | Why it changed |
|---|---|---|
| A | **A** | unchanged |
| **C** | **B** → *(2026-09-23: absorbed into A)* | Hong Kong, Prague, Taiwan ×4, Bucharest, Singapore, Oslo, Copenhagen |
| **E** | **C** → **B** *(2026-09-23)* | Brazil ×2, Japan ×10 |
| **F** | **D** → **C** *(2026-09-23)* | Stockholm, Zurich |
| B | *(closed)* | **awaiting permission** — Tel Aviv, discarded on terms |
| D | *(closed)* | **coordinates and unfinished screening** — Bucharest finished its screening |
| G | *(closed)* → **D** *(2026-09-23, reopened)* | **access blocked** — Hong Kong left upward, Hyderabad and Kochi measured out; **the condition came back true of Kaohsiung**, so it is a live band again under the next free letter |

**Rule this renumber established: a LETTER is for a heading, a CONDITION is
for a sentence.** Prose that says *"moved to the coordinates band"* survives
any renumber; prose that says *"moved to Band C"* does not, and four such
sentences went stale the moment the letters shifted. They have been rewritten
to name conditions.

**Renumbered again 2026-09-23, and this time a band closed by SUCCEEDING.**
The coordinates band existed to hold cities whose coordinate route was
unmeasured. All four of its last members ended up with the route measured AND
a brief written, so the condition stopped being true of every one of them and
the band was absorbed into **A** rather than re-captioned. `C` and `D` moved
up to `B` and `C` behind it.

⚠️ **Several sentences written on 2026-09-23 named LETTERS and went
stale within hours of being written** — including two in the Bucharest and
Singapore sections added that same day. They have been rewritten to name
conditions. **The rule above is easy to agree with and easy to break in the
next paragraph.**

⚠️ **`DECISIONS.md` is append-only and names bands by their letter at the time
of writing.** Those entries remain true of the moment they describe; this
table is how a reader resolves them. **Nothing in the log was edited.**

**Re-banded 2026-09-22 so each caption describes what its cities ARE**, not
how they were found. The previous Band C had grown to 21 cities whose only
shared property was "needs coordinates" — while the **cost** of that step
ranges from Prague's RÚIAN lookup to Japan's chōme/ban/gō. That is the
largest single ranking fact in this list, and one band was hiding it.

**Band D held Bucharest alone** while its business leg was unfinished. On
2026-09-22 it finished — **rail counted (12 relations, M1–M5), licence read
(SILENT), Romania's catalogue enumerated (4,693 datasets, no second
bucket)** — so the city moved to C and the band closed. **A band whose
condition stops being true of its last member should close, not be
re-captioned around the occupant.**

**A caption names a blocker, never a date or a status.** `D-a` was briefly
captioned *"all four PROBED 2026-09-22"*, which reads as progress and is
unauditable — Rio's misfiling was caught only because the sub-tier beside it
still declared what it was *for*.

✅ **Guadalajara and Mexico City left Band A by being built**, not by being
ruled out. Their rows are kept below, marked, because a built city's Band A
entry is the only place the screening promise and the delivered build sit
side by side.

**Net: the screen got smaller and more honest.** Nothing was lost that was
ever measured as viable — the five drops were all cities whose business leg
had never been tested, and testing it is what removed them.

**Two cities were promoted the same day**, both by the same method and both
out of the band that used to read "never actually reached": **Stockholm** to B
and **Bucharest** to C. The tier that looked deadest produced the two best new
results in the sweep.

---

## 🟢 Band A — ready to build (0 ready + 41 ✅ BUILT)

▲ **🇰🇷 Daegu and Busan joined 2026-09-27**, Korea's second and third cities, from
the East Asia second-city screen (scratch in `second_cities/korea/`). Network
class: **METRO** for both. **Their 2026-09-22 closures were findings about a
ROUTE**: the per-district data.go.kr files covered 4 of 9 and 4 of 16
districts. Each city's own portal republishes the national licence register
(LOCALDATA) citywide, keyless, with coordinates, in Seoul's schema, so
`korea_localdata` carries over.

| City | Rail | Business (the city's own portal) | Before the build |
|---|---|---|---|
| **Daegu** | Lines 1–3 (Line 3 a monorail), **86 stops** in the city, from OSM (Korea's station dataset lacks Daegu Metro). 대경선 (Korail, 3 stops at 4.08 km) not drawn (owner) | `data.daegu.go.kr` monthly permit files, 2026-08 edition (195 files in 36 group datasets, four id blocks; each page lists six files at a time), EPSG:5174 points, all 9 districts including 중구. Before de-duplication: food **38,893**, personal **12,548**, retail **18,737**, the same permit types as Seoul's. Points on 95.9–100% | ✅ **BUILT 2026-09-27** (`pages/48_Daegu_Heatmap.py`; **67,212 storefronts, 86 stations**), held for a batch publish. The build found the 2026-08 edition's rows **end 2025-08-31** (owner: build, the real date on the page) and the health-food file's addresses masked with * by the publisher. Licence: a disclosed reasoned position (owner). Brief: `docs/build_briefs/daegu.md`, 11/11 |
| **Busan** | Lines 1–4 (Line 4 a monorail) and the Busan–Gimhae LRT: **110 stations** in the city. 동해선 (Korail, 16 stops at 2.29 km) not drawn (owner) | The city's keyless `LocalDataService` Open API, one operation per permit group, all 16 구·군. Before de-duplication: food **53,596**, personal **16,697**, retail **23,039**, the same types as Seoul's. Points on 94.4–99.5%. **Pull without `state` and by `opnSvcId`**: a `state=01` pull loses the 8,804 open premises permitted after 2025-01 | ✅ **BUILT 2026-09-27** (`pages/49_Busan_Heatmap.py`; **89,798 storefronts, 110 stations**), its own branch stacked on Daegu's, held for a batch publish. Every type pulled in full by `opnSvcId`, never by `state`. **The feed is frozen at 2026-04-15**, and the rows agree; the date is on the page ("Busan snapshot ok"). Licence: PERMITTED WITH CONDITIONS (a credit). Brief: `docs/build_briefs/busan.md`, 8/8 |

✅ **🇲🇽 Monterrey (Regional) — BUILT 2026-09-27** (`pages/47_Monterrey_Heatmap.py`;
**58,565 storefronts, 38 stations**), Mexico's third city, held for a batch publish
(`docs/build_briefs/monterrey.md`, 5/5). Network class: **METRO**. The build refined
three screen figures: 58,565 storefronts after a polygon location test (the screen's
bbox clipped southern Monterrey), Línea 3's red read from the operator's PDF as
`#FF1646`, and OSM already naming the Línea 1 station Arena Monterrey.
- **Why now**: it was ruled out on 2026-09-22 only because Nuevo León publishes
  no Metrorrey data. OSM rail has since been approved and built with, which
  makes that negative obsolete.
- **Business**: DENUE 05_2026 (the same edition, licence and privacy position
  as CDMX and Guadalajara). **58,587 storefronts** (Retail 37,869 · Food 12,639
  · Personal 8,079) across Monterrey, San Nicolás de los Garza, Guadalupe and
  General Escobedo; coordinates **100%**; food **13.5× OSM** (Guadalajara
  13.8×).
- **Rail**: Metrorrey Líneas 1, 2 and 3 from OSM, **38 stations**. Gate 3
  matches the operator's map exactly (19 / 13 / 9). Líneas 4 and 6 are under
  construction and not drawn.
- ✅ **The owner's three calls, decided 2026-09-27**: OSM as the rail ground;
  the four-municipio "(Regional)" scope; and Línea 3 in the operator's red.
  **Nothing blocks the build.**

✅ **Riga BUILT 2026-09-24** (6,730 storefronts, 108 stations). ▲ **Riga 🇱🇻 joined 2026-09-24 from the open gap (owner's call)**, the eleventh. Amsterdam's
two-layer shape:
- **Food**: the State Revenue Service's excise-licence register, 1,596 premises, 96.2% joined to
  Riga's address points, CC0.
- **Shops**: the cadastre's class-1230 premise groups, 4,816 named shops, 99.5% on building
  outlines, CC BY 4.0.
- **Rail**: all 7 Rīgas satiksme tram routes (GTFS, CC0; 125 stations, every one inside the city;
  5–10 minute headways on routes 1, 7 and 11). Colours come from the operator's route maps,
  because OSM and the GTFS give every route the same red. The rings hold 78.5% of the shops and
  82.6% of the food premises. All five Vivi suburban corridors are out on frequency (15–30
  minutes at best).
- **The page carries the scoped vacancy disclosure**: 20.4% of 2,324 centre premises (2024), 15%
  in the Old Town (2025), and not measured elsewhere, about 62% of in-ring shops. Quote the
  municipal report's own definitions: its headline is 73% occupied.
- ✅ **Brief written 2026-09-24**: `docs/build_briefs/riga.md` (4/4). **Builds next, before
  Taiwan** (owner's call, 2026-09-24): a small build that fits the week's remaining budget.
- ⚠️ **Its licences are NOT yet read**: the excise register and the Rīgas satiksme GTFS (both
  declared CC0 on `data.gov.lv`), the VZD cadastre (declared CC BY 4.0), and the address points.
  None has a row in `docs/data_sources.md`, so Band A's "licence read" condition is not met
  yet. Corrected 2026-09-24, the same evening it moved here. Run the reads before the build.

**The ten:** ~~Seoul~~ ✅ **built 2026-09-25** · ~~Hong Kong~~ ✅ **built 2026-09-24** — **each with a brief** in `docs/build_briefs/` — ✅ ~~nine
Brazilian cities~~ **built 2026-09-24** (below) — **three Taiwanese cities**: ~~Taipei (Regional)~~ ✅ **built 2026-09-25** ·
~~Taichung~~ ✅ **built 2026-09-25** · ~~Taoyuan~~ ✅ **built 2026-09-25** — ▲ **and seven more on 2026-09-24**: **six Japanese cities**, Tokyo (8 wards) (7/7) ·
Osaka · Kobe · Sapporo · Fukuoka (4/4 each) · Kyoto (8/8), and ~~Rotterdam~~ ✅ **built 2026-09-24**. ✅ **Every Band A city has a brief** (Riga's written 2026-09-24), and
every brief's checks pass live *(Fukuoka's BODIK host is flaky — re-run before correcting)*.

### ▲▲ Taiwan — three cities, one tax register, a door-plate JOIN (2026-09-23)

*Taiwan's screening write-up, around this table: see [city_master_list_evidence.md#band-a-taiwan](city_master_list_evidence.md#band-a-taiwan).*

| City | Storefronts | **Joined** | Rail — keyless agency data |
|---|---|---|---|
| **Taipei (Regional)** — Taipei + New Taipei | **152,839** (76,519 + 76,320) | **93.9%** (92.4% · **95.5%**) | Taipei's network map (GeoJSON line geometry, `RouteName`) and station points; Taipei Metro's station tables |
| **Taichung** | **73,227** | **92.7%** | Taichung Metro Green Line stations (lat/lon); lines from OSM |
| **Taoyuan** | **49,282** | **94.0%** | Taoyuan Metro network XML; the national `捷運車站` layer (the railway bureau's own airport-MRT file is behind an Incapsula challenge — not worked around) |

### ▲▲ Brazil — nine cities, one census file, no geocoder (2026-09-23)

✅ **ALL NINE BUILT 2026-09-24, as one batch** - see the Built table above and
`DECISIONS.md`. The screening figures below are the screen's, kept beside the
build as the promise it was measured against; the built counts differ because
the build added the rules-version-2 fallback, placement and scope.

*Brazil's screening write-up, and the Band A notes that sat beside the built-cities table: see [city_master_list_evidence.md#band-a-brazil](city_master_list_evidence.md#band-a-brazil).*

| City | Mapped storefronts | Retail / Food / Personal | Dropped as unclassifiable | Enumerator's own coordinate | Rail (OSM) — what the build must settle |
|---|---|---|---|---|---|
| **São Paulo** | **216,037** | 108,265 / 66,467 / 41,305 | 19.7% — **13% periphery → 31% Pinheiros** | 98.5% | GeoSampa WFS, 94 stations / 6 lines, EPSG:31983 |
| **Rio de Janeiro** | **105,350** | 50,423 / 35,509 / 19,418 | 20.0% — 15% → **36% Barra da Tijuca** | 95.1% | 20 relations, all named and coloured |
| **Salvador** | **52,258** | 25,890 / 17,186 / 9,182 | 21.6% — 15% → 29% | 97.3% | L1 + L2, **0 of 4 relations coloured** — colours from the operator. No public agency layer (SEMOB's folder is token-gated). **20 of 21 stations in the city** |
| **Fortaleza (Regional)** | **62,792** (city 49,503) | 29,239 / 11,470 / 8,794 | 25.9% — 20% → **43% Meireles** | 98.5% | Sul (metro) + Oeste, Parangaba–Mucuripe (light rail), all coloured. No agency layer reachable (Metrofor's certificate expired). 31 of 41 stations in the city — **regional, decided 2026-09-23**: + Caucaia, Maracanaú, Pacatuba |
| **Belo Horizonte** | **44,923** | 22,518 / 13,127 / 9,278 | 22.8% — 22% → 30% | 98.8% | L1 + **Linha 2, opened 2026-07-03 with two stations — OSM lists exactly those two**. Agency lines (2022, pre-L2), no agency stations |
| **Brasília** | **35,824** | 19,706 / 9,164 / 6,954 | 26.7% — 16% → **48% Asa Sul** | 99.9% | Metrô-DF Verde + Laranja, coloured. **Agency stations + lines with status** (IPEDF GeoServer; **public domain, READ 2026-09-24**, backed by DF decree 38.354/2017) |
| **Recife (Regional)** | **43,518** (city 25,212) | 14,968 / 5,622 / 4,622 | 29.2% — 19% → 32% | 99.0% | Centro 1 & 2 + Sul, coloured; plus a diesel VLT to Cabo. **CBTU file: 36 stations + lines** (ODbL, READ 2026-09-24 — as a cross-check it carries no obligations). 19 of 36 stations in the city — **regional, decided 2026-09-23**: + Jaboatão, Cabo, Camaragibe |
| **Porto Alegre (Regional)** | **35,688** (city 18,798) | 10,576 / 4,599 / 3,623 | 27.9% — 23% → 40% | 98.1% | Trensurb, coloured. No agency layer. Only 7 of 23 stations in the city — **regional, decided 2026-09-23**: + the Trensurb corridor to Novo Hamburgo |
| **Santos (Regional)** | **11,691** (city 6,021) | 3,322 / 1,769 / 930 | 25.0% | 98.1% | VLT L1 + L2, coloured; tourist tram excluded. Stops layer of unconfirmed ownership. 17 of 25 stops in Santos — **regional, decided 2026-09-23**: + São Vicente |

**Not carried forward:** Teresina, Maceió, João Pessoa and Natal have rail in
OSM, but it is single diesel lines or CBTU suburban trains tagged
`light_rail` — the commuter shape this project excludes everywhere. **Not
downloaded, not discarded:** ASSERTED from the rail screen, and one download
each settles it. **Cuiabá** returned 0 relations (its VLT was abandoned) and
**Curitiba**, the negative control, returned only a tourist train.
▼ **2026-09-27 (wave 2): all four measured on frequency and discarded** (rows
in DISCARDED), with Sobral and the VLT do Cariri. **Contagem joins Belo
Horizonte and Duque de Caxias joins Rio** as regional add-ons (owner's call;
PLAN).

Ordered by how little stands in the way. **Built cities keep their row**,
struck through and marked ✅, so the band still shows what screening promised
and whether it held.

| # | City | Business leg | What remains |
|---|---|---|---|
| ✅ | ~~**Guadalajara**~~ 🇲🇽 | DENUE, SCIAN = NAICS, INEGI licence cleared | **BUILT 2026-09-22** — `pages/16_Guadalajara_Heatmap.py`, region *Mexico*. Screening said "nothing outstanding" and that held |
| ✅ | ~~**Monterrey (Regional)**~~ 🇲🇽 | DENUE (the same national edition), SCIAN = NAICS, INEGI licence cleared; four municipios keyed on INEGI's municipio code | **BUILT 2026-09-27** — `pages/47_Monterrey_Heatmap.py`, region *Mexico*, **58,565 storefronts, 38 stations**. Screening said the build would need only its rail leg and scope, and that held |
| ✅ | ~~**Madrid**~~ 🇪🇸 | **53,355 clean storefront rows** — retail 36,224 · food 18,194 · personal 9,974 (from 225,660 join rows → 159,787 open → filtered). Three-level taxonomy on `division`, EPSG:25830, CC BY 4.0 | **BUILT 2026-09-22** — `pages/17_Madrid_Heatmap.py`, region *Spain*. Rail from **CRTM's feature layers**: 13 lines, 293 station-line records, 49 stations excluded, 0 filter disagreements. Screening said the rail leg was the open question and CRTM answered it |
| ✅ | ~~**Dublin**~~ 🇮🇪 ▲▲ **REGIONAL** | **38,265 rateable rows across FOUR local authorities → 13,945 storefront** (Dublin City alone: 19,810 → **8,016**). **13 use categories region-wide, 12 in Dublin City.** **99.87% carry `Xitm`/`Yitm`** — Irish TM, already in metres; 51 of 38,265 missing, **46 of them pubs**. Per-row `Category` **and** `Uses`, plus `ValuationReport[].FloorUse`. `Eircode`. **CC BY 4.0, no key** | **No geocoding leg.** Build is the **Vancouver + Surrey shape** — four authorities, not one city. Rail: the three drawn lines (**Luas Red, Luas Green, DART**) all already carry an OSM colour; Commuter and InterCity are **dropped**. ⚠️ **36% of its storefronts are near no rail of any kind** — a scope fact to state on the page, not a defect. Brief: `docs/build_briefs/dublin.md`, **6/6**  — **✅ BUILT 2026-09-22** — the regional shape (four local authorities) held |
| ✅ | ~~**Seoul**~~ 🇰🇷 | **17 citywide permit registers**, all 25 gu, EPSG:5174, KOGL Type 1 on all 17: about **157,000 food, 53,000 retail and 40,000 personal-services premises** | ✅ **STEP 0 COMPLETE 2026-09-24** (`docs/build_briefs/seoul.md`, 4/4 checks). Nine retail and bar registers were found by an OA-id sweep. Restaurant coordinates go from 90.7% to **97.7%** by borrowing points from the register's own rows at the same building (control: median 0 m). The Korean exposure check is sized at 113 premises. Rail: 369 stations, 3 light-rail lines; the earlier "0" was a failed query. ✅ **Owner's four calls decided 2026-09-24**: the buckets (karaoke bars in Food service), 경의·중앙, 수인·분당 and 경춘 drawn, stations inside Seoul only, and the East Asia region Hong Kong creates. **Ready to build** — **✅ BUILT 2026-09-25** (`pages/43_Seoul_Heatmap.py`, region *East Asia*) |
| ✅ | ~~**Milan**~~ 🇮🇹 | **Three layers, one per bucket — the bucket comes from WHICH LAYER a row is in, not from a code.** `ds49` **28,131** retail · `ds59` **3,799** food service · `ds62` **5,732** personal services. All three **CC-BY**, all updated **2026-08-31**, all with `LONG_X_4326`/`LAT_Y_4326` | **Schemas captured 2026-09-22 — and the fill rates correct this row's old claim.** Coordinates are excellent (99.1% / 92.2% / 98.8%) and location is complete (`Ubicazione` 100%). **But the columns that were cited as making this the richest source in the screen are mostly EMPTY**: `insegna` **17.6%** on retail and **9.1%** on food, `codice_ateco` **7.1%**, and `ds62` has **no name field at all**. `settore_merceologico` is 99.5% but binary — *alimentare / non alimentare*; `tipologia` is 100% and single-valued. **Owner decision: a map where ~82% of retail pins carry no trade name.** Not a blocker — bucketing works by layer, and fewer published names is a privacy asset — but it is a choice, not a detail — **✅ BUILT 2026-09-22** |
| ✅ | ~~**Mexico City**~~ 🇲🇽 | Same DENUE. **Rail from OSM** — 195/195 stops exact, 6,468 geometry points | **BUILT 2026-09-22** — `pages/15_Mexico_City_Heatmap.py`. The ODbL share-alike decision was taken during the build; see `DECISIONS.md` |
| ✅ | ~~**Paris**~~ 🇫🇷 | SIRENE établissement-level, **Licence Ouverte 2.0**, **99.96% already geolocated**. Built storefronts **87,164** from **149,166** active bucket rows | **BUILT 2026-09-23 — the 21st city, and the first in France.** 🚨 **Its screening figures did NOT survive the build.** This row read *"50,156 rows vs OSM's 54,198, and on one class 10,595 vs 10,642"*, attributed to an **employee filter**. **There is no employee filter**: `trancheEffectifs` is `NN` on 77.3% of rows and only 1,425 record `00`, so SIRENE codes a sole trader as `NN` — that band holds every owner-run shop, and the largest cut the column can make falls **16,000 short** of 50,156. Re-established: **87,164 SIRENE vs 48,973 OSM = 1.78×**; on restaurants the **OSM side reproduced** (9,058 vs a recorded 10,642) and the **SIRENE side did not** (16,280 vs a recorded 10,595). **When one side of a comparison reproduces and the other does not, the non-reproducing side is where the tuning happened.** France remains a build; the 92.5% claim does not |
| ✅ | ~~**Marseille**~~ 🇫🇷 | The same SIRENE, estimated at **25,430** bucket rows | **BUILT 2026-09-23 — the 22nd city, and France's second.** `pages/22_Marseille_Heatmap.py`. **18,177 storefronts, 66 stations.** Scope was **measured rather than inherited from Paris**: all five RTM lines sit 100% inside commune 13055, so the commune costs it nothing; Aubagne's tram excludes itself by having zero stations inside; ferries dropped by owner's decision and recorded as revisitable. See `DECISIONS.md`, *"Marseille built, and a region now labels only its own cities"* |
| ✅ | ~~**Toulouse**~~ 🇫🇷 | The same SIRENE | **BUILT 2026-09-23 — the 23rd city and the third French one. 8,635 storefronts, 48 stations**, 64.3% of storefronts within a station ring, 0 person-like names at a residential unit. See `DECISIONS.md`, *"Toulouse built: 8,635 storefronts, 48 stations, and the first non-rail mode"* |
| ✅ | ~~**Lille (Regional)**~~ 🇫🇷 ▲▲ **REGIONAL** | The same SIRENE, estimated at **8,076** bucket rows for the commune alone | **BUILT 2026-09-23 — the 24th city, France's fourth, and its first regional one.** `pages/24_Lille_Heatmap.py`. **11,833 storefronts, 91 stations**, eleven communes. Both owner calls in the brief dissolved: métro geometry from OSM, everything else first-party from MEL, and ilévia's GTFS never read. See `DECISIONS.md` |
| ✅ | ~~**Rennes**~~ 🇫🇷 | The same SIRENE, estimated at **4,833** bucket rows (measured at the build: **5,451**, so the estimate was the floor it said it was) | **BUILT 2026-09-23 — the 25th city and France's fifth and last.** `pages/25_Rennes_Heatmap.py`. **3,479 storefronts, 24 stations**, 68.0% of storefronts within a station ring, 0 person-like names at a residential unit. **The brief's "the métro is city-contained" was half wrong**: Métro b keeps 11 of 15 stations inside commune 35238 and loses both termini; commune-only by owner's call, since its worst line survives better than Toulouse's T1. See `DECISIONS.md` |
| ✅ | ~~**Oslo**~~ 🇳🇴 | Enhetsregisteret SUB-UNITS on `beliggenhetsadresse`, measured at the brief's **13,458** bucket rows exactly | **BUILT 2026-09-24 — the 26th city and Norway's first.** `pages/26_Oslo_Heatmap.py`. **10,718 storefronts, 155 stations**, 75.6% within a ring, 0 sole-trader names shown. **Three brief claims corrected at the build**: the register is SN2025 (NACE Rev. 2.1) not SN2007; coordinates are a JOIN on Kartverket's bulk address file (96.8%) not a geocode; OSM's relations are too partial for gate 3. Kommune only, trams drawn, ferries excluded - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Copenhagen**~~ 🇩🇰 | CVR PRODUCTION UNITS on `beliggenhedsadresse`, measured at the brief's **14,887** Kobenhavn bucket rows exactly | **BUILT 2026-09-24 — the 27th city and Denmark's first.** `pages/27_Copenhagen_Heatmap.py`. **14,978 storefronts, 64 stations** (Kobenhavn and Frederiksberg), 94.5% within a ring, 4 person-like names at a residential unit (0.03%). **Three brief claims corrected at the build**: the codes are DB25 (NACE Rev. 2.1) not DB07; DAWA closes 1 October 2026, so coordinates join DAR on Datafordeler; the Letbane is open. Frederiksberg in, S-tog drawn, sole traders and partnerships shown by address, 969900 excluded, rail from OSM rather than Rejseplanen's GTFS - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Prague**~~ 🇨🇿 | ROS02 ESTABLISHMENTS where they trade, with the owner's activity from RES - measured at the build as 27,327 in the buckets against the brief's 27,065 on the older NACE column | **BUILT 2026-09-24 — the 28th city and Czechia's first.** `pages/28_Prague_Heatmap.py`. **25,275 storefronts, 58 stations**, 69.8% within a ring, restaurant control 1.59x OSM like-for-like, 1 person-like name at a residential unit (0.01%). Keyed on RES's `NACE2025` (NACE Rev. 2.1), matched on PREFIX for its ragged depth; metro from PID's own GTFS with Flora added while closed. Natural persons and partnerships shown by address, and a natural person's premises at their own seat left off - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Amsterdam**~~ 🇳🇱 | Two layers from the city's own API: the live hospitality-permit register (the brief's 4,092) and the BAG's shop-class units in use (the brief's 10,898) | **BUILT 2026-09-24 — the 29th city and the Netherlands' first.** `pages/29_Amsterdam_Heatmap.py`. **13,238 storefronts (3,583 permits, 9,655 shop units), 144 stations**, 95.5% within a ring. Metro 50–54 and 16 tram lines (owner's call), from OVapi's CC0 national GTFS; stations are each line's REGULAR route, trams thinned by the sub-transit-line filters; gate 3 exact on the metro. Tram colours read from GVB's own map. Gemeente only though tram 6 keeps 5 of its 16 stops, and shipped with 11 line-label overlaps at phone width, the phone layout handed to the cleanup role - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Rome**~~ 🇮🇹 | SUAP premises (the brief's 95,493 joined) placed on ANNCSU house numbers | **BUILT 2026-09-24 — the 30th city and Italy's second.** `pages/30_Rome_Heatmap.py`. **98,897 storefronts, 87 stations**, 53.5% within a ring, no names in the register at all. Rail from OpenStreetMap (the agency GTFS is ambiguous); the Roma–Viterbo urban service DRAWN and Metromare left out, measured against the DART / S-tog test; the food layer's 2.67x over OSM stated rather than cut - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Barcelona**~~ 🇪🇸 | **58,908 active premises** (2022 census — the 2024 one is geographically incomplete), 0.00% bad coordinates, CC-BY-4.0. Build brief, 9/9 | **BUILT 2026-09-22** — `pages/18_Barcelona_Heatmap.py`. All four owner decisions were settled before the build: census year **2022**, drawn scope **16 lines** (14 metro refs + funiculars FM and FV, decided on the operators' own `network` tag), mall and market interiors **kept**, and the brief's OSM breakdown corrected to tram 20 / funicular 6. ⚠️ **The duty to notify the Council is still OUTSTANDING** — see `docs/gated_access.md` item 2 |

### ▲ 🇮🇹 Rome — a premises register joined to Italy's house-number archive (2026-09-24)

*Rome's screening write-up, around this table: see [city_master_list_evidence.md#band-a-rome](city_master_list_evidence.md#band-a-rome).*

| City | Storefront establishments | **Joined** (civic level) | Rail | Licences |
|---|---|---|---|---|
| **Rome** | **95,493** — retail 65,107 · food 19,223 · personal 11,163 (+ food and personal trades inside the *Laboratorio* catch-all) | **95.7%** (92.0% exact), every municipio ≥ 90.9%, 0.2% unmatched | OSM Metro A, B/B1, C (+ Metromare, owner's call); **exclude the phantom Metro D**; Roma Mobilità GTFS live | SUAP and ANNCSU both **CC BY 4.0**, READ — credit, link, state the modification |

*Amsterdam's screening write-up (its row is in the built-cities table above): see [city_master_list_evidence.md#band-a-amsterdam](city_master_list_evidence.md#band-a-amsterdam).*

### ▲▲ 🇯🇵 Japan — six cities, a block-level JOIN, not a geocoder (2026-09-24)

**Moved here from the geocoding band on 2026-09-24 (owner's calls), which then
closed.** Japan's coordinate step was a JOIN: the permit lists spell the
address, and MLIT's 位置参照情報 publishes a point per block (街区).
`scripts/screen_japan_join.py` measures it, with Minato as the control at
**99.8%** re-run after every rule. Rail for every city is MLIT N02, **JR and the
private railways included** (owner). **No general retail anywhere**: Japan's
ceiling, stated on each page. The food control is the Economic Census's 飲食店
count, not OSM (owner).

| City | Food premises (fixed) | **Joined** (block) | Independent check | Personal services | Licences (all READ) |
|---|---|---|---|---|---|
| ✅ ~~**Tokyo (8 wards)**~~ | **≈59,400** permit rows — Chūō, Minato, Shinjuku (2023, disclosed), Kōtō, Shibuya, Taitō, Setagaya, Meguro. ⚠️ **Against Tokyo's yearbook count, only Shibuya's list is essentially complete (98%)** (measured 2026-09-24). The others hold 9–84%: consent-filtered exports, opt-outs, and snapshots never updated. Filling them takes requests to the wards (`gated_access.md` 29–32) | **99.1–100%** | the wards' own coordinates, median **22–43 m** | 生活衛生 registers, 11 wards (16,299; Meguro's 1,412 added 2026-09-24) | Tokyo Open Data Terms / ward CC BY 4.0; §6 cost clause accepted — **BUILT 2026-09-28** (63,989 storefronts, 490 stations, 293 of them hollow) |
| ✅ ~~**Osaka**~~ | **61,752**. ⚠️ **67% of the official restaurant count** (MHLW 衛生行政報告例, FY2024: 54,289 of 81,418), where the other designated cities read 93–101%. **About two-thirds of the gap is expired permits still in the official count** (probed 2026-09-24): the old-law count exceeds what can exist by about 12,000, and the list is even across wards against the Economic Census. **The other third is undetermined**: e-Stat's flow tables show about 9,000 revised-law restaurant permits that the city counts as live and has never listed, some of them short-lived event stalls. The page discloses it; the build is not blocked | **99.1%** | the city's own (mislabelled) coordinates, median **38 m** | 15,775 | CC BY 4.0 / 政府標準利用規約 2.0 — **BUILT 2026-09-27** (72,999 storefronts, 216 stations) |
| ✅ ~~**Kobe**~~ | **24,761** | **97.1%** | — | 4,993 | CC BY 2.1 JP — **BUILT 2026-09-27** (27,251 storefronts, 121 stations) |
| ✅ ~~**Sapporo**~~ | **24,257** | **84.7%** + 15.2% chōme | — | 5,993 | CC BY 4.0; 第9条3 accepted — **BUILT 2026-09-28** (28,674 storefronts, 95 stations) |
| ✅ ~~**Fukuoka**~~ | 3,231 (own list, pre-2021) + **21,088** restaurants from MHLW | **98.1% / 96.8%** | MHLW's own coordinates, median **36 m** | 5,846 (99.2%) | BODIK CC BY 4.0 + MHLW PDL 1.0 — **BUILT 2026-09-28** (30,062 storefronts, 71 stations) |
| ✅ ~~**Kyoto**~~ ▲ | **22,259** restaurants, a register **rebuilt** from the permit stream (an upper bound: closures unseen) | **92.7%** | GSI on the stripped address, 0–1 m (12 of 12) | 5,828 (94.4%) | CC BY 4.0 (京都市オープンデータ) — **BUILT 2026-09-28** (32,355 storefronts, 117 stations) |

- **Tokyo**: 🚩 the owner requests **Chiyoda's** ledger (即時公開請求, a CD-R for
  ¥100) to fill the centre. Until then the page names the wards with no
  published list, Chiyoda, Toshima and Bunkyō among them. Nakano (stale) and
  the partial Shinagawa and Itabashi lists stay off (owner).
- **Fukuoka**: ⚠️ about **20% of restaurants withheld their address** in MHLW's
  per-field consent, so the page discloses an undercount. The two sources
  overlap by 1.3% (measured at block level).
- **The other five**: Hiroshima to the one-bucket band (no personal-services
  list), Sendai to the access-blocked band (the city's permission), and
  Yokohama and Nagoya to the open gap (no current food list). Kyoto went there
  too, and came back the same day on a rebuilt register.
- **Kyoto** ▲ *from the open gap 2026-09-24 (owner's call)*: no full list since
  the 2021 reform, so the register is **rebuilt**: the 2021-03-31 list plus
  every monthly list, kept while each permit's term runs
  (`japan_register.kyoto_permit_stream`, Rotterdam's method). 15.5 restaurants
  per 1,000, inside the yardstick. ⚠️ Closures are invisible, so the count is
  an upper bound and the page says so. Rail (owner): Keihan Keishin passes the
  stub test, the two funiculars are drawn, the Sagano scenic line is out.
- Briefs: `docs/build_briefs/{tokyo,osaka,kobe,sapporo,fukuoka,kyoto}.md`.
- **Every Japanese city, ward by ward: `docs/japan_city_list.md`**, generated by
  `python scripts/japan_ward_table.py --write`. It is republished on its own
  (owner, 2026-09-24).

### ▲ 🇳🇱 Rotterdam — Amsterdam's shape, the food layer rebuilt (2026-09-24)

✅ **BUILT 2026-09-24** - 1,939 rebuilt permit premises (the brief's 1,937) and 5,581 BAG shop units, 132 stations. See the Built table and `DECISIONS.md`.

*Rotterdam's screening write-up and its open-gap row: see [city_master_list_evidence.md#band-a-rotterdam](city_master_list_evidence.md#band-a-rotterdam).*

### ▲ Four cities joined this band 2026-09-23, when the coordinates band closed

*The coordinates band's write-up, around this table: see [city_master_list_evidence.md#band-a-four-cities](city_master_list_evidence.md#band-a-four-cities).*

| Cities | Country | The coordinate step — MEASURED | Rate |
|---|---|---|---|
| **Prague** ▲▲ *(1)* | 🇨🇿 | ▶ **BACK IN THIS BAND 2026-09-24, on a new business leg**: paused the same day because RES is a seat register, then answered with **ROS02** — open-data *active establishments* with RÚIAN codes — joined to RES for activity. **27,065** storefront establishments, **restaurant control 1.63x** like-for-like (the paused 8.02x compared all of NACE 5610 with OSM restaurants alone; like-for-like, RES's seats read 4.48x). ROS02's terms **PERMITTED**, nothing to display. ARES/RŽP rejected on a 2019 ÚOOÚ GDPR fine, not on § 60(6), which Parliament narrowed. One owner call at build: sole traders (1,429 at their own seat). Brief: `docs/build_briefs/prague.md`. **The coordinate step, as measured before:** **A JOIN, confirmed.** RÚIAN's Praha export is **3.4 MB zipped, keyless** (`vdp.cuzk.gov.cz`; the old `cuzk.cz` redirects rather than dying) and holds **134,627 addresses, every one a unique `Kód ADM`, 99.99% carrying coordinates**. Measured on **6,000 active Praha rows** in CZ-NACE 47/56/96 streamed from RES | **99.8%** — 99.9% carry a code, 100.0% of those resolve |
| **Copenhagen** *(1)* | 🇩🇰 | **A JOIN, confirmed — and the account gate was on the wrong leg.** DAWA (`api.dataforsyningen.dk`) is **keyless**; the `distribution.virk.dk` 401 gates the BUSINESS register only. The whole city downloads as CSV: **85,351 access addresses, 100% with WGS84**, joinable on `vejnavn` + `husnr`. ⚠️ **Frederiksberg (0147) is a separate kommune entirely surrounded by Copenhagen** — scope to 0101 alone and the map has a hole in its middle; its 9,584 addresses come from the same call | **100%** of addresses carry coordinates ✅ **BRIEF WRITTEN 2026-09-23, 4/4 — `docs/build_briefs/copenhagen.md`.** **14,887 storefront rows** (retail 6,689 / food 5,163 / personal 3,035) at **100.0% named**, measured from the real 2.00 GB download rather than from metadata. **96.9% carry a DAR address UUID**, so coordinates are a JOIN. ⚠️ **Four files joined on `CVREnhedsId`** — `Produktionsenhed` alone is almost empty. 🚨 **`v/` marks a sole trader: 7.2%, a FLOOR**; `coNavn` is a second exposure at 26.0%. ⚠️ **Rail: M1–M4 only** — this list's "tram 4" was WRONG, Copenhagen has no tram |
| **Hong Kong** ▲▲▲ *(1)* | 🇭🇰 | ✅ **BUILT 2026-09-24 WITHOUT THE GEOCODE** - FEHD publishes the same registers with its own point per licence on the CSDI Portal, found by the ALS licence read; 21,137 of 21,165 placed, and the ALS hits this build would have accepted sit a median 12 m from FEHD's. Recorded as found: **A GEOCODE, confirmed keyless.** The government **Address Lookup Service** (`als.gov.hk/lookup`) answers without a key and returns **lat/long AND HK1980 Grid easting/northing AND a confidence `Score`** (76.15, 88.75, 97.69 on three test premises). ✅ **INDEMNITY ACCEPTED by the owner 2026-09-22** — the project's only uncapped liability, priced deliberately. Three conditions bind the build: display source + Government IP acknowledgement + DATA.GOV.HK attribution exactly; run `check_personal_exposure.py` and exclude catch-alls; the dated record in `data_sources.md`. ⚠️ Re-reading the live clause corrected this project's OWN earlier quote twice: it arises **directly or indirectly**, and there is **no notice-and-defend right** | ✅ **100.0% — RE-MEASURED 2026-09-23 on 200 random register rows, as a TWO-STAGE lookup.** This cell read *"per-row rate not yet measured"* for a day after the brief measured it. **Brief 8/8 — `docs/build_briefs/hong-kong.md`** |
| **Oslo** *(1)* | 🇳🇴 | **A GEOCODE, keyless — with two traps.** Kartverket (`ws.geonorge.no/adresser`) answers and returns `representasjonspunkt`. ⚠️ **`fuzzy=true` MUST NOT BE USED**: it "rescued" `Karenslyst allé 8B` as **`allé 1B`** — a different building — and turned `7-Eleven` into `Ellen Gleditsch' vei 7`. It returns plausible coordinates for the wrong place. ⚠️ The API caps at **10,000 rows** (offset 9,900 works, 15,000 returns nothing), so it cannot enumerate the city | **97.8%** via two stages: exact `adressetekst`, then plain `sok`. Never fuzzy |

*Closed Band B (Japan's geocoding band, closed 2026-09-24): see [city_master_list_evidence.md#closed-band-b](city_master_list_evidence.md#closed-band-b).*

*Open screening gap: empty since 2026-09-24, and a new row resting on an absence re-opens it here. Its rows and the 2026-09-23 sweep: see [city_master_list_evidence.md#open-screening-gap](city_master_list_evidence.md#open-screening-gap).*

## 🔵 Band B — passed: narrower pages (6 cities; reopened 2026-09-28)

**Reopened by the owner 2026-09-28** for the cities that passed the Band C memo:
screening is complete, and the page will be narrower than the three-bucket
cities - one bucket, or all three with a measured gap - and says plainly what
is missing (Hong Kong's "mostly restaurants" and the Japanese cities' missing
retail are the precedent). **Band C closed the same day**, when its last five
got verdicts: Incheon and the Gyeonggi satellites to this band, Ottawa to T,
Palma and Baltimore to N. *(The letter's earlier band, geocoding at national
scale, closed 2026-09-24; this is a new condition under a free letter.)*

### ✅ Passed (owner, 2026-09-27): build as one-bucket pages

**Stockholm and Bucharest passed the Band C memo**: a food-only page beside
the three-bucket cities, saying plainly what is missing (Hong Kong's "mostly
restaurants" and the Japanese cities' missing retail are the precedent). They
stay in this band, apart from the cities still waiting on a verdict. Both
have a metro, so the deferred trams decision does not touch them.

| City | Network | The one bucket | What travels with it to the build |
|---|---|---|---|
| **Stockholm** 🇸🇪 | T-bana: 8 subway refs in the kommune, all named and coloured | `Tillsynsverksamheter - Livsmedel`: 8,146 distinct food premises, WGS84, daily | Licence SILENT (the publisher's own feed says `accessLevel: public`), disclosed. Write-up below |
| **Bucharest** 🇷🇴 | Metro M1–M5 (13 relations; `Extensie M4` has no ref or colour) | DSVSA: 31,299 food rows | **The memo's two conditions**: the file downloads only in a browser that passed the site's challenge, so the owner fetches it (never a replayed cookie); licence SILENT, disclosed. Write-up below |

### ✅ Passed from the transit-gap re-screen (owner, 2026-09-28): London food only, Berlin without hairdressers and laundries

**London was ruled out 2026-09-21 as a country, before food-only pages
passed.** Re-screened on `docs/global_transit_gap.md`'s order; the trail is the
United Kingdom row in the shortlist's Tier 4. **Berlin was a discard on two
keyword searches**; enumerating its catalogue found its chamber of commerce's
register, and the trail is the shortlist's Germany row.

| City | Network | The one bucket | What travels with it to the build |
|---|---|---|---|
| **London** 🇬🇧 (Greater London, 33 authorities) | Underground, Overground, DLR, Elizabeth line and Tramlink (kn); how much to draw is a rail-shape decision at the build | FSA food-hygiene register, keyless API: **81,633** premises; food storefronts 40,585 (restaurants and cafés 27,279, takeaways 9,441, pubs and bars 3,865), food retail 19,088; **80.2%** with coordinates in a 3,300-row sample, 2 with no address; half the sampled ratings 2024-04 or later in every authority | **No second layer covers central London**: the VOA rating list's terms are "NDR purposes only"; borough NNDR lists with a description in 4 of 33 (Camden, Islington, Barnet, Hounslow), none downtown; special-treatment registers lookup-only. **Before the build**: a `licence-read` of the FSA register; placement for the ~20% without coordinates (postcode centroids, with their own `data_sources` row); the personal-exposure check (mobile and home caterers); the rail shape. **Brief**: `docs/build_briefs/london.md` (4/4, 2026-09-28) |
| **Berlin** 🇩🇪 | U-Bahn (9 lines) and S-Bahn (kn); how much of the S-Bahn ring and trams to draw is the build's rail-shape decision | **IHK Berlin's Gewerbedaten**: **367,575 per-premises points** at their addresses (WFS `gdi.berlin.de/services/wfs/gewerbedaten`; CSV 126 MB), WZ/NACE codes, no names, monthly (last 2026-09-28), CC0 / dl-de/zero-2.0. Retail 51,233, food 20,771. Four station boxes (600 m): food **1.18–1.47× OSM**, shops **1.18–1.40× OSM** | **Personal services partial**: hairdressers (9621, 180 city-wide) and laundries (9610, 215) are crafts-chamber members, not IHK, disclosed; beauty (9622, 1,792) and spa/sauna (9623, 1,595) are present, beside a 9699 catch-all of 10,170 *(corrected 2026-09-28: the probe's 0–5 per box keyed on NACE Rev. 2 codes; `nace_id` is NACE Rev. 2.1 / WZ 2025)*. Registered offices stack at arcade and courtyard addresses (65% of storefront entries at Hackescher Markt share an address with 10+), without inflating the storefront ratios. **Before the build**: a `licence-read`; a taxonomy module keyed on NACE Rev. 2.1 / WZ 2025 classes (restaurants 5611, hair 9621, beauty 9622; 5610 and 9602 do not exist), with IHK's 5–6-digit `ihk_branch_id` for finer splits; the personal-exposure check (46–59% of storefront entries report 0 employees); the rail shape |

### ✅ A measured gap, disclosed (owner, 2026-09-28)

| City | Network | What is there | The gap, measured |
|---|---|---|---|
| **Incheon** 🇰🇷 | METRO: Incheon Lines 1–2 (59 distinct), Line 7 (5) | `data.incheon.go.kr` active-only lists, keyless, all 10 districts: restaurants 33,256, cafés 10,156, salons and baths 9,493, health-food 7,467 | **No coordinates** (addresses only, a 2026-01 snapshot), and retail only as health-food. An operator-name column (`업자명`) must be dropped. **What would move it**: an address join through Korea's official address database (juso.go.kr), unprobed **Verdict (owner 2026-09-27): probe the address join first.** ▼ **Probed 2026-09-27: no keyless route.** juso.go.kr's keyless monthly files (건물DB, 주소DB, 도로명주소) carry **no coordinates** (their schema guides read); the file that does, **위치정보요약DB** (entrance X/Y, EPSG:5179 family, per 시도), is **application-only**: Korean phone or i-PIN identity check, a purpose statement and a review (도로명주소법 시행령 제46조), and the site's code refuses overseas IPs. data.go.kr 15050410 says the same. OSM `addr:*` places only **7.8% of restaurants exactly (11.1% of cafés)**, OSM's gaps not the parser's. **What would move it now: the owner's application for 위치정보요약DB, or the unprobed two-hop (건물DB → parcel id → a keyless parcel-centroid file, if one exists).** The health-food list holds apartment-unit addresses: a privacy filter at build **Verdict (owner 2026-09-28): PASS, to this band.** ▼ **Placed by a JOIN, measured 2026-09-28**: the Korea Elevator Safety Agency's lift-building coordinates (data.go.kr 15156424, keyless CSV, 36.4 MB, declared "이용허락범위 제한 없음"; 17,235 Incheon buildings, road-name address + WGS84), keyed on district + road + building number, plus **road-number interpolation** between the two nearest listed buildings on the same road (Korean building numbers run with distance along the road): **71.3% of the 33,256 restaurants** (41.0% exact, 30.3% interpolated). Leave-one-out on 2,000 listed buildings: median error **15 m** between same-side neighbours, 52 m either side. Extrapolated pins (11.4%; median 74 m, 90th percentile 526 m) are dropped; about 16% are unplaced, disclosed. **Before the build**: that file's licence read and a `data_sources` row; the health-food list's apartment-unit filter; a 법정동 mapping for the 2026-07-01 district reorganisation on any refresh (both files use the old names) |
| **Gyeonggi satellites** 🇰🇷 (Uijeongbu, Yongin, Gimpo named; Seongnam, Goyang, Suwon, Bucheon, Ansan, Namyangju have more stations) | Uijeongbu METRO (Line 1, U Line: 21); Yongin METRO (EverLine: 25); Gimpo EDGE (Goldline only: 9) | `data.gg.go.kr`, 14 province-wide permit types over 31 시군, licence "commercial use and changes permitted". Province: retail 58,005, food 147,615, personal 54,206 | **The café file has no name, location or status**; takeaway food (즉석판매) has no status column; restaurants have X/Y but no address (a boundary join places them). The download page's "purpose of use" is answered honestly at build (owner) **Verdict (owner 2026-09-27): hold until Daegu and Busan are built.** **Verdict (owner 2026-09-28): PASS, to this band**, the café file's gap disclosed; the hold for Daegu and Busan lapsed when both were built. Which satellites to build is the brief's question, those with the most stations first (Suwon, Seongnam, Goyang, Bucheon) |

*The Band C write-up below is history: it was written when Stockholm, Zurich
and Göteborg were one-bucket cities awaiting the memo.*

**Screening is COMPLETE for all five, and all five passed.** Each has a real
premises-level register with coordinates, current data and a usable licence.
What none of them has is a **second bucket** — and the owner's bar is that two
is acceptable and one is not. **Göteborg joined Stockholm and Zurich here on
2026-09-23**, probed to the same depth, which is why this caption no longer
says "both".

**▶ A second source in a different shape is still open for each** — a
building register's use class gave Amsterdam its shop layer on 2026-09-24,
which is how it left this band. `reprobe-city` Step 4 names the per-country
targets (ASSERTED, unprobed).

**This is not "we could not find a second register".** All these negatives were
re-established on 2026-09-22 by **enumerating the whole catalogue** rather
than searching it, because the original negatives rested on keyword searches
and that is the method that has failed this project most often — Stockholm's
own food register is called *Tillsynsverksamheter*, "supervision activities",
which matches neither `restaurang` nor `livsmedel`.

| | Stockholm 🇸🇪 | Zurich 🇨🇭 |
|---|---|---|
| **Catalogue enumerated** | **309 datasets** (Entryscape, by resource-URI prefix) | **1,128 dataset names** (CKAN `package_list`) |
| **The one register** | `Tillsynsverksamheter - Livsmedel` — **8,146 distinct premises** from 289,742 inspection rows, 100% trade names, 96.9% addresses, daily from Ecos 2 | `Gastwirtschaftsbetriebe` — licensed by the city police's *Bewilligung Gastro* unit |
| **Licence** | **SILENT** — the publisher's own feed says `accessLevel: public` on all 109 of its datasets | ✅ **CC0** |
| **What a second bucket would have been** | `Salutorg`, `Torghandelsplats` — **polygons**, *"i form av ytor"*: zones where trading is permitted, not traders | `geo_bauernhofladen` — **not shops**: *"Betriebszentren von Haupterwerbslandwirten"*, farmers' operating centres |
| **Everything else that matched** | 3 × social care (`Daglig verksamhet`), 1 utility service area | `standorte` of counting stations, contaminated sites, historic cinemas, tram ticket offices |

**Why neither is discarded.** Nothing here is unresolved or unreachable —
the work is done and the answer is *one bucket*. That is a **product
judgement**, not a data defect, and it can change: a second source may
appear, or a food-density page may become worth shipping. **A discard would
throw away two complete screenings to record a preference.**

**Both countries are structurally one-bucket, which is why no further probe
helps.** Sweden has **no general business licence** at all, so retail and
personal services have no municipal source to find; Switzerland's national
**STATENT is aggregate**. This is the Hong Kong distinction inverted — there
the register exists and we cannot reach it; here we have reached everything
and only one register exists.

**If one is ever taken, take Stockholm first on size, and Göteborg or Zurich
first on licence** — Stockholm's **8,146** premises against Göteborg's
**5,063** and Zurich's **3,488**; Göteborg and Zurich are both CC0 against
Stockholm's silence. *(Updated 2026-09-23, when Göteborg joined this band and
all three were measured.)* **One owner decision moves all three**: does a
food-density page belong in a project whose other cities carry three buckets?


---

*▲ **Amsterdam left this band on 2026-09-24 for Band A** — the BAG gave it a
second layer. Its section is there.*

### 🇷🇴 Bucharest — moved here from the coordinates band 2026-09-23

**Nothing about Bucharest got worse. The band it was in was measuring the
wrong thing.** The band it sat in described a **measured coordinate route**, and Bucharest's is
genuinely measured. This band describes the **one-bucket ceiling**, and
Bucharest has one. **Where both are true, the ceiling is what is actually
stopping the city** — which is what these bands exist to say.

⚠️ **This project had already recorded the finding and left the row
where it was.** The 2026-09-22 entry that closed Bucharest's screening states
that **Romania's national catalogue holds no second bucket**: 4,693 datasets
enumerated from the Internet Archive, and the only commercial register in them
is ~40 dated snapshots of ONRC's **company** register. **It has been in the
wrong band since its own screening finished.**

| | |
|---|---|
| **The one bucket** | **DSVSA** — the sanitary-veterinary authority, so its **31,299 rows are FOOD**. `bucuresti.dsvsa.ro` |
| **Licence** | **SILENT**, and established rather than assumed — no terms page exists at all; the footer's *"Toate drepturile rezervate"* is a **website** footer, the New York situation |
| **Coordinates** | **OSM fallback, re-measured 2026-09-23: 146,228 addressed objects** in relation 377733 (132,478 nodes + 13,750 ways), within 112 of the earlier figure |
| **Rail** ✅ | **RE-COUNTED 2026-09-23: 13 subway route relations, 13 named, 12 coloured**, refs M1–M5, and **64 station nodes** against the *"~63 claimed, unverified"* this list carried |
| ⚠️ **The 13th relation** | **`Extensie M4` carries NO `ref` and NO `colour`.** A build keying on `ref` silently drops it; a build keying on relation count draws a line it cannot label |
| ⚠️ **Fetch is browser-assisted by necessity** | Plain curl against the XLSX returns **503 with the challenge interstitial**; the same URL **inside the browser that legitimately passed the challenge** returns 200 and real `PK` magic bytes. Never a replayed clearance cookie |
| ⚠️ **Primary portal still dead** | `data.gov.ro` resolves to 85.120.75.35 and **blackholes on 443 and 80**, now **two days running** — which weakens the original "outage, not refusal" reading. Its catalogue was read from the Internet Archive instead |

**Bucharest is the strongest-RAILED city in this band** — a real five-line
metro against Zurich's and Göteborg's trams (Stockholm has a metro too) — and the
weakest on access. **The opposite trade from Göteborg**, which has the best
licence and the weakest map.

### Stockholm in full

*Zurich's write-up, which shared this section, moved to Band T with Zurich on 2026-09-27 (owner's call).*

**▲ Stockholm** 🇸🇪 — **upgraded from D-c on 2026-09-22.** Screening is
DONE: a public ArcGIS FeatureServer carrying **8,146 distinct food premises**
with WGS84 points, 100% trade names and 96.9% addresses, updated daily. It
carried two questions; **the licence one was answered on 2026-09-22 — SILENT,
see item 2** — so **one remains, and it is an owner decision rather than a
probe**. ⚠️ **Item 2's text went stale the day it was answered and sat
contradicting this very sentence until 2026-09-23**, so a reader arriving at
the list saw "one remains" above a list of two. It is struck through rather
than deleted, because the superseded reasoning is what makes the resolution
legible:

✅ **RAIL COUNTED 2026-09-23, and this list's figure was wrong.** It carried *"metro 7, tram 21"*. Measured inside **Stockholms kommun** (OSM rel 398021): **subway 15 relations / 8 refs**, all named and all coloured; **tram 6 relations / 4 refs**, only **4 of 6 coloured**; **light_rail 6** (refs 21, 30, 31); **92 rail station nodes**. ⚠️ **One subway relation and one tram relation carry NO `ref`** — a `ref`-keyed build drops them silently. ⚠️ The boundary lookup matched nothing on `name=Stockholm` because the kommun is **`Stockholms kommun`**, and widening it returned **two US "Stockholm Township" relations at the same admin_level**.

1. **Scope.** It is **one bucket** — food. Stockholms stad has 291 datasets
   and exactly one commercial register; `restaurang` and `företag` both
   return **0** inside its own catalogue, and Sweden has no general business
   licence. A Stockholm page would be a food-density map.
2. ~~**Licence.**~~ ✅ **RESOLVED 2026-09-22 — SILENT, and this item
   was left standing after its own intro said it was answered.** The
   superseded text read: *"`dataportal.se` says `Åtkomsträttigheter:
   Begränsad`; the ArcGIS item says `access: public`... ambiguous in a way
   that matters, so it needs the publisher asked."* **It does not.**
   `dataportal.se` is a **HARVESTER, not the publisher** — `read-licence`
   step 5 — and the miljöförvaltning's **own** Hub DCAT feed
   (`open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109
   datasets**) declares **`accessLevel: public` on all 109**, with `license`
   **CC0 on 8** and blank on the rest. **Step 5 decides a contradiction in
   favour of the publisher, and the publisher says public.** 💡 **And
   the blank is meaningful precisely BECAUSE 8 of 109 carry CC0**: a missing
   licence field can mean *"no mechanism"* or *"declined to license"*, and here
   the mechanism is demonstrably in use.

---

## 🔴 Band D — access blocked by the publisher (12 cities)

▼ **Delhi joined 2026-09-28** from the large-transit gap's re-screen (owner's
call): the municipal corporation's current licence register is behind a
CAPTCHA (Daejeon's wall), and every Delhi-government host refuses this machine
(Hyderabad's shape).

▼ **Dubai joined 2026-09-28** from the large-transit gap's re-screen (owner's
call), in Warsaw's weaker form (blocked before measurement). Its old reason,
"no agency feed", is obsolete: OpenStreetMap carries the Metro and the tram.

▼ **Daejeon, Gwangju and Gimhae joined 2026-09-27** from the East Asia
second-city screen, in Warsaw's weaker form (blocked before measurement).
**Kaohsiung's geo-block was re-measured the same day and stands**: `data`,
`openapi`, `api`, `kcgdg` and `sports.kcg.gov.tw` all time out on TCP while
`www` answers in 0.17 s, and today's national catalogue (52,434 datasets) still
lists only those hosts for the 2026 door-plate file.

▼ **Lisbon, Helsinki and Tallinn joined 2026-09-24 from the open gap (owner's calls)**, after a
final re-probe. **Lisbon** waits on a free account. **Helsinki and Tallinn** are in Warsaw's
weaker form: each one's bulk file sits behind a geo-block.

**The rejected route, recorded so nobody takes it.** The re-probe reached both through the back
ends of public lookup pages:
- **Oiva's search API**: 3,424 Helsinki premises, pulled in 217 queries to get past a 300-result
  cap. No licence is declared for per-premises results.
- **Tallinn's food-register public view**: 5,131 premises, pulled by sending back the page's
  own session token. Its responses carried operators' ID codes and birth dates, which were
  dropped.

The owner declined to rely on either (2026-09-24), and the harvested files were deleted. **A
lookup page's back end is not a substitute for a geo-blocked bulk file.**

**Reopened 2026-09-23 (owner's call) for a condition the other bands cannot
say**: screening is COMPLETE and passed, the file exists and is measured, and
the one thing stopping the city is **the publisher's own access control**.
▼ **Sendai joined 2026-09-24 in the full form** (screened, joined, only permission missing). ▼ **Warsaw and Hyderabad joined 2026-09-24 in a weaker form (owner's calls)**: blocked BEFORE
anything was measured, so the first step is a read from inside the country, and only then asking.
**What unblocks it is asking, not probing** — which is the difference from
the closed band below, whose members were *not yet reached properly* and all
left it once they were.

| City | Screened and passed | What blocks it — MEASURED | The way through |
|---|---|---|---|
| **Kaohsiung** 🇹🇼 | **72,550 storefronts** in the national tax register; OGDL v1 read and accepted (the same decision as Taiwan's other cities); the door-plate file exists in a **2026 edition** (`高雄市115年門牌坐標資料-TWD97`, updated 2026-06-25) with the same columns the three joined cities used (**92.7–95.5%**) | 🚧 **Geo-blocked to Taiwan**: `data.kcg.gov.tw` answers **HTTP 200 to 3 of 3 Taiwanese probes** (two networks) and times out from Japan and the US; `www.kcg.gov.tw` on the same network answers everywhere. The national catalogue lists **no other host** for any of 3,342 Kaohsiung datasets. **Not routed around** — no proxy, no VPN | **A request to 高雄市政府民政局** to publish the file on data.gov.tw or lift the filter for it — an owner action. Nothing sent |
| **Warsaw** 🇵🇱 | ⚠️ **NOT screened behind the block — a weaker shape than Kaohsiung's (owner's call 2026-09-24).** Nothing behind the block has been read. The city's own catalogue is the one place a premises register could be; every reachable route is negative (the city's 21 datasets on `dane.gov.pl`; the map portal's layers, markets and café terraces only; CEIDG is company-level; the alcohol-sales-points lead was Gdańsk's) | 🚧 **Geo-blocked to Poland**: `api.um.warszawa.pl` / `dane.um.warszawa.pl` answer only from Poland (2 of 2 probes) and time out from Germany and the US, while `mapa.um.warszawa.pl` answers everywhere; the API is also key-gated. **Not routed around** | **A read from inside Poland first** (the catalogue listing — does a premises dataset exist?), and only then a request to the city for access. An owner action. Nothing sent |
| **Hyderabad** 🇮🇳 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-24).** India's national catalogue was walked in full (288,011 titles: trade-licence counts, never premises); GHMC's archived URL names show trade-licence status and lookup forms, no bulk register named. Nothing behind the block has been read | 🚧 **Geo-blocked to India**: GHMC's own site answers 3 of 3 Globalping probes inside India (Mumbai, Bengaluru, Hyderabad) and returns 403 at its F5 edge to 9 of 9 from the US, Germany and Singapore, and from here; Telangana's portal (`data.telangana.gov.in`) the same. **Not routed around** | **A read from inside India first** (does GHMC publish a trade-licence register as a file?), then a request. An owner action. Nothing sent |
| **Lisbon** 🇵🇹 | ⚠️ **The city side is negative on three methods** (2026-09-24): its catalogue as mirrored on `dados.gov.pt` (220 of 316 datasets link to its ArcGIS services, which answer); its ArcGIS services directory (102) and org (nonsense control 0); and the archive's index of the challenged CKAN (1,966 dataset names). What exists: kiosks (373, CC0), markets, the stale 2010 commercial census, and a 2020 COVID "Estamos Abertos" layer marked internal use | 🚫 **A free account**: DGAE's national *cadastro comercial* (`cadastro.dgae.gov.pt/api/estabelecimentos`) returns 401 logged out, and a CMS key in the app's JavaScript was NOT used. Row count, activity codes, coordinates and terms are all unmeasured | Register the account (the owner's act, `docs/gated_access.md` item 28), then measure. With activity codes, points and reusable terms, **Lisbon and Porto** both go to A. Without them, a discard |
| **Helsinki** 🇫🇮 | ⚠️ **Reachable hosts all negative for retail and personal services** (2026-09-24): the city catalogue, enumerated through `data.europa.eu`'s copy (373 datasets, 6 Helsinki publishers, nonsense publisher 0); `kartta.hel.fi` WMS (485 layers) and WFS (terraces, parklets); HSY's WFS (397 layers, jobs grid only); `api.hel.fi` servicemap (public services, and its search is inert). Food exists in Oiva (national inspections, current) but only behind a search API, which is not used (above). The city's own food-control CSV is frozen at 2019 | 🚧 **Geo-blocked**: `hri.fi`, `avoindata.fi` and `avoindata.suomi.fi` answer 403 outside Finland and Germany. The bulk files behind them (the city catalogue; Valvira/LVV's alcohol-premises register, CC BY 4.0; any Oiva release) are unread | A read from inside Europe, by a person there (no proxy or VPN), of HRI's catalogue and of whether Oiva or the alcohol register is a bulk file. Then asking Ruokavirasto, the last resort |
| **Tallinn** 🇪🇪 | ⚠️ **A second layer is reachable, the first is not** (2026-09-24). Building-register use classes per building part come on a public WFS (`gsavalik.envir.ee`, `etak_ehr_hooned`; Maa- ja Ruumiamet, CC BY 4.0 equivalent): 2,077 commercial buildings; parts: food 1,496, retail 2,773 (0.79× OSM shops), personal services 342 plus 765 "other service". But these are registered use, not occupancy, with no names; 14% of lists are cut at 200 characters. It is not a premises register alone (Vienna's lesson). The city's GIS (1,173 layers) holds markets and malls only | 🚧 **Geo-blocked**: the food-handlers register `Toidukaitlejad.xml` (`avaandmed.agri.ee`, CC BY-SA 3.0) answers Estonia and Germany only. The public-view route is not used (above). The building register's full data needs an order carrying an e-mail (the owner's act, gated item 23). `www.tallinn.ee` is behind a Cloudflare challenge | A read of the food XML from inside the EU (no proxy or VPN), or the owner's EHR order. Then the Amsterdam shape: food register plus building-use layer, with a vacancy rate found and the trams-only call (5 lines; GTFS expired 2026-08-31, so OSM) |
| **Sendai** 🇯🇵 | ✅ **Screened and joined**: 12,627 permanent food premises, **95.1%** block, GSI check median 34 m; personal services 3,378 at 96.5% (`docs/build_briefs/sendai.md`, 4/4) | 🚫 **The city's permission**: its site terms default to 「無断で複製・転用することはできません」 and neither list page overrides it; the lists carry no per-file CC BY badge and are not in the city's 5,907-row open-data catalogue | **A written request to 健康福祉局生活衛生課**, drafted in formal Japanese for the owner to send (2026-09-24). Nothing sent yet |
| **Daejeon** 🇰🇷 | ⚠️ **NOT screened behind the block — Warsaw's shape (2026-09-27).** METRO: Line 1, 22 stations (the tram opens in 2028) | 🚫 **No city portal** (`data.daejeon.go.kr` fails DNS); the national register sits on data.go.kr behind the residency and CAPTCHA wall measured 2026-09-22 | A city-published register, or a national route without a CAPTCHA |
| **Gwangju** 🇰🇷 | ⚠️ **NOT screened behind the block — Warsaw's shape (2026-09-27).** METRO: Line 1, 20 stations (Line 2 under construction) | 🚫 **No city portal** (`data.gwangju.go.kr` fails DNS); the city's own open-data page points only to data.go.kr and the closed localdata.go.kr | As Daejeon |
| **Gimhae** 🇰🇷 | ⚠️ **NOT screened behind the block (2026-09-27).** EDGE, light rail only: the Busan–Gimhae LRT, 12 stations | 🚫 `data.gyeongnam.go.kr` and `www.gyeongnam.go.kr` both time out; no city portal found | A read from inside the country first. Its LRT also enters any Busan (Regional) scope |
| **Dubai** 🇦🇪 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** METRO: Red (two branches) and Green, 64 named stations in OSM, plus the tram. The 2026-09-21 record found the Department of Economy's licence register (`ded_license_master`, mainland Dubai without the free zones, an activity table beside it); whether its rows carry an address or coordinates, and its dataset licence, are unread. Dubai Municipality's building-entrance layer (`dm_dmgisnet_enterances-open`) could be the join file, on the same portal | 🚧 **Every host refuses this machine** (2026-09-28): `dubaipulse.gov.ae` times out on HTTPS and HTTP, `data.dubai` (the successor) returns a firewall "Request Rejected" on every path, `dubaidet.gov.ae` 403; the API wants a key (401). DMCC's free-zone directory forbids copying | A read from inside the UAE: the register's data dictionary and the open-data licence |
| **Delhi** 🇮🇳 | ⚠️ **Partly screened (2026-09-28, owner's call).** Delhi Metro (kn). What is open is stale or partial: MCD's 2021-22 general trade licence list (366 KB XLSX, ~4,100 rows, former South DMC only, placed to colony, not street); NDMC's current health licences (453 in 2025, unit address, no trade type, central New Delhi only, mostly food). No reachable address or coordinate layer (NDMC's gate points carry no address) | 🚧 **The current register is behind a CAPTCHA**: MCD's `gtlLicenseDetail` / `htlLicenseDetail` (trade × 12 zones × year, Excel export) and FSSAI FoSCoS both need an image CAPTCHA. **Every Delhi-government host times out** (delhi.gov.in and its labour, food-safety, DES and health subdomains on one IP; `gsdl.org.in`; `edistrict`); Delhi Police licensing refuses HTTPS. Food moved to FSSAI in 2026 (MCD order) | A bulk export requested from MCD, or a read from inside India; then placement, which is unresolved |

*Kaohsiung's full record while it sat in Band B: see [city_master_list_evidence.md#band-d-kaohsiung](city_master_list_evidence.md#band-d-kaohsiung).*

*Closed bands (formerly G, B, D-c and D-d), kept in full: see [city_master_list_evidence.md#closed-bands](city_master_list_evidence.md#closed-bands).*

## ⚪ Band N — no page for now (5 cities; created 2026-09-28)

**Created by the owner 2026-09-28.** Screening is complete, and the owner has
decided a page is not worth building on what is published today. The row stays
so that a change in the source can reopen it; each says what would.

| City | Network | What is there | Why no page | What would change it |
|---|---|---|---|---|
| **Singapore** 🇸🇬 | MRT 21 relations (the Jurong Regional Line uncoloured) | Four NEA / HSA registers; current only for tobacco retailers (4,235) and pharmacies | The eating-establishment register is a **2016 snapshot** (owner 2026-09-27) | NEA refreshing the register: it returns to the buildable bands at once. Write-up below |
| **Yokohama** 🇯🇵 | MLIT N02 (subway, JR and private railways) | Personal services, complete: **17,408 premises** (CC BY) | **No food list in any era**: a map without its ~29,000 restaurants would misread its stations (owner 2026-09-24) | The city publishing its food register, or MHLW's online system covering most permits. Write-up below |
| **Palma** 🇪🇸 | Metro de Palma M1 (10 stations, all inside) and M2 (10 → 6); OSM tags both `light_rail` | The Consell de Mallorca's restaurant register: **4,375 food premises** (2.75× OSM), **13% with coordinates** | Food only, and an address join for 87% of rows, on a small metro (owner 2026-09-28) | A retail or personal-services source (none in the Balearic catalogue's 399 datasets; the city's `smartoffice.palma.es` refused connections) |
| **Baltimore** 🇺🇸 | METRO: Metro SubwayLink **11 stations** and Light RailLink **16 stops** inside the city (OSM, measured 2026-09-28) | The city's "Restaurants" layer: **1,327 points** (2025-12); 311 package-goods liquor licences and 46 grocery stores, too thin to be a bucket | Food only: **no Maryland or city premises register for retail or personal services** in 1,531 state, 693 city and 1,423 iMAP catalogue items and 175 map services (probe 2026-09-28); barber and cosmetology licences are a name-search page only (owner 2026-09-28) | Maryland's Labor Department publishing shop and salon permits in bulk, or a decoder for the city's DHCD parcel use codes |
| **Istanbul** 🇹🇷 | METRO: M1A–M11, 177 named stations in OSM, every line with ref and colour; trams T1–T5 (156 stops); funiculars F2, F3; Marmaray (tagged train) a build question | İBB's health-institutions dataset (557 public datasets on `data.ibb.gov.tr` searched): **5,806 pharmacies, 1,672 opticians, 1,208 medical-supply shops**, lat/lon and full address; İBB's only licence dataset is aggregate counts per district and sector | **Pharmacies and opticians only**, frozen at 2024-03 with a note that the data "is subject to a fee and will not be updated", and pharmacy names are often the pharmacist's own. Shops, restaurants and salons are licensed by the 39 districts: Kadıköy publishes counts only, Üsküdar 7 unrelated datasets, and Beşiktaş, Şişli, Beyoğlu, Fatih and Bakırköy no open-data host. No open address layer (owner 2026-09-28) | A central district publishing its işyeri licence list in bulk, or İBB a premises-level licence register |

▼ **Yokohama 🇯🇵 joined 2026-09-24 from the open gap (owner's call): personal services only, and
no page for now.**
- **Personal services**: complete, 17,408 premises as of 2026-04-01, declared CC BY (barbers
  3,380, beauty 11,062, cleaning 2,966). Also a pharmacy list (1,719) and a drug-store list (611),
  whose licence page is unread.
- **Food: none in any era.** Four places were checked:
  - the city's catalogue, listed in full (649 packages);
  - the web archive of the catalogue and the food-safety pages;
  - a live crawl of all 18 ward sites;
  - the prefecture, which holds no Yokohama permits.
  MHLW's opt-in slice is 9.9% of the official 29,358.
- **Why no page**: a map without its roughly 29,000 restaurants would read its stations as
  emptier than Tokyo's or Osaka's, because of what is published, not what is there.
- **What would change it**: the city publishing its food register (only by request, the last
  resort), or MHLW's online system covering most permits as they renew online.

### 🇸🇬 Singapore — moved here from the coordinates band 2026-09-23

**Verdict (owner, 2026-09-27): no page.** The food register is a 2016 snapshot; it stays in this band in case NEA refreshes it.

**Two buckets on paper, ONE on current data.** Four keyless premises registers
exist and the licence permits everything this project does — but **the big
one is a 2016 snapshot.**

| Register | Coverage | Rows | |
|---|---|---|---|
| **NEA Licensed Eating Establishments** | 2015-06-11 → **2016-09-06** | **36,687** | ⛔ **TEN YEARS STALE** |
| **List of Supermarket Licences** | **2016-06-26 only — a single day** | 478 | ⛔ stale |
| **Licensed Tobacco Retailers** | updated **2026-08-07** | **4,235** | ✅ current |
| **Listing of Licensed Pharmacies** | updated **2026-08-07** | **243** | ✅ current |

**The ROWS confirm the metadata rather than merely repeating it**, which is
what makes this solid rather than a metadata artefact: the only dated column in
the eating-establishments file, `suspension_start_date`, returns **2016-02-21**
and **2016-04-13**, while tobacco's `ValidPeriod` returns **2025 / 2026 /
2027**. **Two files a decade apart in the data itself.**

⚠️ **`lastUpdatedAt` says 2024-06-06 for both stale files and it is a
METADATA TOUCH, not a data refresh.** Reading that field alone would have
recorded Singapore as two years old rather than ten. **`coverageEnd` is the
honest field and the rows are the honest check.**

**So the current position is ~4,478 rows, all RETAIL** — comparable to
Göteborg's volume and narrower than Stockholm's. **This is Turin's shape,
four years worse**: Turin sits in the open screening gap for a series that
stops in 2019, *"six years stale against a project mapping CURRENT density."*

✅ **The licence is NOT the problem and was read in full 2026-09-23** —
**Singapore Open Data Licence v1.0, PERMITTED WITH CONDITIONS.** Grant is
*"worldwide, perpetual, royalty-free"* covering *"modify and adapt ... or any
derived analyses"*, commercially. ⚠️ **It carries an INDEMNITY of
Hong Kong's class and wider** — its third limb reaches *"any claim made by
a third party in connection with the third party's Use of ... any derived
analyses or applications which you have provided"*, and it **survives
termination**. **That decision is HELD, not taken**: there is no reason to
accept an open-ended liability for a city whose main register is from 2016.

🚨 **`Listing of Licensed Pharmacies` carries `Pharmacistincharge`, a
named individual on all 243 rows**, and the licence expressly grants **no
rights over** *"any personal data in the dataset"* — so publishing it would
be outside the licence, not merely against project policy.

⚠️ **Provenance decides the terms: take these ONLY from
`data.gov.sg`.** HSA's and NEA's own site terms restrict commercial reuse of
their sites' contents, and both HSA datasets point at HSA's InfoSearch page.
**The same rows from the agency's own site would carry different terms.**

**Rail was counted 2026-09-23 and carries three traps** — recorded because
they would each have surfaced mid-build: **MRT 21 relations, 21 named, only 16
coloured** (the **`JRL` Jurong Regional Line has NO colour** across all 5 of its
relations — Bucharest's `Extensie M4` in a second city, the same day); **only
ONE of three LRT lines** appears under `route=light_rail`, Sengkang, so Bukit
Panjang and Punggol are tagged some other way; and **the station counts do not
reconcile** — MRT 54 + LRT 13 against 90 rail stations total, so 23 are
tagged as neither and the naive query undercounts badly.

**Reinstatement is cheap and well-defined: if NEA refreshes the eating-
establishment register, Singapore returns to the buildable band immediately.** Everything
else about it is already done — licence read, geocode measured at 98.8%,
rail counted, registers enumerated. **It is parked on ONE fact.**

## 🟤 Band T — contingent on trams (51 cities; created 2026-09-27, renamed the same day)

**Created by the owner on 2026-09-27** as "trams only", the same day the owner
ruled that trams count as rail for this project ("count trams"), and **renamed
"Contingent on trams" the same evening (owner's call)**, when five cities moved
in from Band C.
- **What goes here**: a city whose build waits on the owner's yes to
  trams-only maps: its rail network is trams, streetcars or street-running
  light rail with **no metro**. Access must be usable (a trams-only city that
  is access-blocked, Tallinn, stays in D).
  - **Most members** passed screening on two or more buckets, and the trams
    decision is their only open question.
  - **Five also carry a Band C gap** (the group below): the trams decision is
    the one that gates them first, so they wait here, tagged with the gap.
- **It waits on one decision about the group**, not on a probe: does a
  trams-only map belong beside metro cities? **Riga**, built 2026-09-24 on
  seven tram routes, is the precedent. **Deferred by the owner 2026-09-27**
  until the full tram list exists and the second-wave screens are done
  (PLAN).
- **Edge cases are flagged per city, not sorted silently**:
  - light rail built partly to metro standard (The Hague's RandstadRail,
    Utrecht's sneltram, Bergen's Bybanen, Aarhus's Letbane on former regional
    track);
  - Rouen's light rail with a centre tunnel;
  - Hiroshima's Astram Line, an elevated automated line beside the
    streetcars.

### EDGE — light rail built partly to metro standard (11 cities; grouped 2026-09-28)

**Grouped by the owner 2026-09-28**, so that the trams decision can take this
slice first. EDGE (the owner's call, 2026-09-27) marks light rail that runs in
tunnels, on its own right-of-way or on converted railway: between a tram and a
metro, tagged rather than promoted to Band A. Each row keeps its country flag
and its build-time call, and the country groups below point here. **Six also
carry a bucket gap** (Hiroshima, Utrecht, Den Haag, Kitchener–Waterloo, Ottawa,
Pittsburgh), named in the last column. Two EDGE cities sit elsewhere, placed by
their first blocker: Gimhae in Band D, Gimpo in Band B's Gyeonggi entry.
Ordered roughly from the most metro-like (Buffalo, mostly underground) to the
least.

| City | Network | Business | Gap, or build-time calls |
|---|---|---|---|
| **Buffalo** 🇺🇸 (EDGE: mostly underground, surface-running in the downtown transit mall) | Metro Rail, one line, **about 13 stations, all in the city** (from knowledge, not measured). **In T, not A (owner's call)**: the edge rule that kept Nice here | New York's multi-source pattern: the city's Business Licenses (`qcyy-feh8`, public domain, 12,131 active, lat/lon) + NYS retail food (`9a8c-vfzj`) + NYS salons (`y3u4-jbgh`), NYS licences already read: **~900 / ~1,500 / 374** | Scope the NYS rows by point-in-boundary; drop elevator and fuel-device certificates; the rail and OSM density to measure |
| **Ottawa** 🇨🇦 (EDGE: O-Train Line 1 is grade-separated light rail with a downtown tunnel) | O-Train light rail, 6 routes (stations unmeasured) | Food-safety inspections only: the one address-level commercial layer among 697 catalogue entries scanned 2026-09-21 (`docs/canada_retrospective.md`) | **Food only** (a bucket gap): no retail or personal-services source. **Moved from Band C 2026-09-28 (owner)**: light rail with no metro, so trams are its first blocker, as for Kitchener–Waterloo |
| **Nice** 🇫🇷 (EDGE: L2 in a 6.4 km tunnel) | Tram L1–L3, plus a route "B" (Aéroport T2 – CADAM, 6 stations) not yet identified; stations in the commune / total: 47 / 47 (every line whole) | SIRENE, R / F / P 4,230 / 3,544 / 2,372 (2.85×; personal 6.4×); stores near stations 9,379 | None on scope. Personal services lean on beauty (96.02B, 1,026 over 810 hairdressers): a composition and personal-exposure item |
| **Rouen** 🇫🇷 (EDGE: the "métro", a light rail with a central tunnel) | 2 branches; stations in the commune / total: 10 / 31 (32%) | SIRENE, R / F / P 1,505 / 1,190 / 512 (1.73×); stores near stations 2,868; 3,634 over 5 communes | **Regional scope**; Astuce's own host timed out, so rail from the Normandie regional feed |
| **Den Haag** 🇳🇱 (EDGE) | 14 HTM lines plus RandstadRail E: 172 stop places; worst line tram 1, 20 of 37 (a regional scope makes every line 94–100% whole) | BAG shop units 6,560 (1.75× OSM) | **Gap:** **No current food source**: the city's register froze at the end of 2020, and its Gemeenteblad carries 321 applications and no decisions |
| **Utrecht** 🇳🇱 (EDGE) | Trams 20–22: 16 stops (line 21 keeps 57%); 32 with Nieuwegein and IJsselstein | BAG shop units 3,461 (1.73×) | **Gap:** **Food partial**: rebuilt from Gemeenteblad notices, 822 premises (0.78× OSM), no expiry rule. **What would move it**: the owner accepting a disclosed partial food layer, to Band T. `open.utrecht.nl` answered 403 and was left alone, so "no register" there is unmeasured |
| **Bergen** 🇳🇴 (EDGE: Bybanen street-runs in the centre, segregated beyond) | Lines 1 and 2, **34 stations, all inside the kommune**; 5- and 7-minute headways. Skyss GTFS, NLOD (read for Oslo) | Oslo's modules unchanged: 2,195 / 658 / 762 = **3,615** placed; join **96.2%** | **None** — the cheapest non-French build |
| **Aarhus** 🇩🇰 (EDGE: 19 of its 39 stations are on converted single-track regional railway at 2 an hour) | Letbane L1 and L2, **39 stations in the kommune**; L1 keeps 19 → 11 | CVR production units: 3,122 / 1,220 / 941 = **5,283** | All 39 stations or the 20 on new tramway (the screen leans to 39, headway disclosed); one OSM colour for both lines; ~44% personally owned (Copenhagen 39%) |
| **Kitchener–Waterloo (Regional)** 🇨🇦 (EDGE: ION runs in reserved lanes and off-road corridors, at grade, with a tunnel and bridges) | ION light rail, one line, **19 stops: Kitchener 11, Waterloo 8**. Either city alone is a stub; the pair keeps every stop. Every 10 min, 06:00–22:00 on weekdays. GTFS from the Region (GRT), Region of Waterloo Open Data Licence v2.0 (declared) | The Region's public-health inspection layers: food "General" **2,008** (2.0× OSM), personal services **about 636** (2.7×), points on 100%. **No retail**: grocery and convenience stores sit inside food with no field to split them. Same licence, which requires the wording "Contains information provided by the Regional Municipality of Waterloo under licence" | The regional pair as the scope; filter by boundary polygon, not `SiteCity` (about 60 spellings); the personal-services layer holds home-based operators, so `check_personal_exposure.py` first; the grocery share of food. Neither city publishes a general licence register (all three hub catalogues enumerated) |
| **Pittsburgh** 🇺🇸 (EDGE: the T, with a downtown subway) | The T, 3 lines; **stub test unmeasured** (much of the network is suburban) | Allegheny County's Geocoded Food Facilities (CC0, 32,245 county-wide; `municipal` = Pittsburgh wards; x/y): food, plus grocery and convenience stores as retail (New York's precedent, owner 2026-09-28) | **No personal-services source** (a Band C gap); the city's own licences are signs, amusements and peddlers (729 active); the food file last modified 2025-08-27 |
| **Hiroshima** 🇯🇵 | Hiroden streetcars, plus the Astram Line (EDGE) | 7,479 + 5,195 restaurants on two lists, joined 96.0% / 95.0%; PDL 1.0 | **Gap:** **No personal-services list** (PDFs only); food retail only as MHLW's opt-in slice |

### ▲ Five moved from Band C 2026-09-27 (owner's call): contingent on trams, with a bucket gap as well

*Hiroshima, Utrecht and Den Haag, three of the seven below when they moved, are EDGE networks and are in the EDGE group above, with their gaps.*

Each needs two yeses: trams-only maps (this band) and the Band C memo's
verdict for its gap. Rows as they stood in Band C; the write-ups follow,
verbatim.

| City | Network | What is there | The gap, measured |
|---|---|---|---|
| **Zurich** 🇨🇭 | 18 tram refs, all coloured, plus the Forchbahn (S18); no metro | `Gastwirtschaftsbetriebe`, 3,488 food premises, CC0 | **Food only**: no second register in 1,128 catalogue names; STATENT is aggregate |
| **Göteborg** 🇸🇪 | **Measured 2026-09-27 (OSM)**: 13 tram lines (1–13, Göteborgs Spårvägar), **127 distinct stops inside Göteborgs Stad**; lines 4 and 12 run on into Mölndal. Each line has its own OSM colour except 11 ("black"); the heritage Lisebergslinjen is out. No metro | `Livsmedelsverksamheter`, 5,063 active food businesses, CC0, daily | **Food only**: `handel`, `butik`, `företag` and `frisör` all return 0 on a filtering search |
| **Rijswijk** 🇳🇱 | Trams-only, 17 stop places | BAG shop units | No food source. **A Den Haag add-on** (owner 2026-09-27): a candidate for a Den Haag (Regional) scope, not a page of its own |
| **Delft** 🇳🇱 | Trams-only, 12 stop places | BAG shop units | No food source. **A Den Haag add-on** (owner 2026-09-27): a candidate for a Den Haag (Regional) scope, not a page of its own |

### 🇸🇪 Göteborg — promoted into this band 2026-09-23

**It was never ruled out. It was never PLACED.** The master list named it
twice — *"Unprobed candidate"*, *"Better data, weaker map"* — and put it in no
band, which is how a candidate disappears without anyone deciding to drop it.
Probed to the same depth as Stockholm and Zurich on 2026-09-23.

| | |
|---|---|
| **Catalogue** | **EntryStore**, `catalog.goteborg.se/store/search?type=solr` — the same platform as Stockholm's. Three guessed CKAN bases returned a 662-byte HTML shell first: **a wrong endpoint, not a verdict** |
| **The one bucket** | ✅ **FOOD ONLY, and the control proves it.** `livsmedel` → 1, `restaurang` → 6, but **`handel` → 0, `butik` → 0, `företag` → 0, `detaljhandel` → 0, `frisör` → 0.** The search filters, so these are real absences |
| **`Restauranger med serveringstillstånd`** | **1,043 rows**, **CC ZERO**. Carries `Namn` (trade name) and **`Besöksadress`** — the *visiting* address, kept distinct from `Fakturaadress`, the invoice address. **That is the location split done right**, the same distinction that made Norway pass |
| **`Livsmedelsverksamheter`** | *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from **289,742** inspection rows. `accrualPeriodicity: DAILY` |
| ✅ **Row count MEASURED 2026-09-23: 5,063** | The `accessURL` **was on the DISTRIBUTION, not the dataset** — in DCAT the property you want is on the child, and the licence (**CC0 1.0**) was there too. ⚠️ **Take the CSV** (`utf-8-sig`, `;`): the rowstore JSON returns **4,786** — it drops the 279 blank-`typ` rows, swaps x and y, and BOM-mangles `namn`. Brief **2/2 — `docs/build_briefs/goteborg.md`** |
| **Rail** | **Trams, no metro — INHERITED, not measured.** It comes from the same screen that gave Copenhagen a tram it does not have and Stockholm 21 trams against a measured 6. **Verify before building.** Better data on a weaker map — the trade Toronto lost on |

**Göteborg does NOT displace Stockholm, and now that is measured**: **5,063
against 8,146**. Its advantages are structural — businesses rather than
inspections (no dedupe), CC0 rather than SILENT — and they are real, but the
count settles the size question in Stockholm's favour. *(This paragraph read
"the count that would settle it has not been taken" until 2026-09-23.)*

### 🇯🇵 Hiroshima — moved here from the Japan band 2026-09-24 (owner's call)

| | |
|---|---|
| **The one bucket (food)** | Two lists that split by filing channel: the city's counter applications (**7,479** restaurants) and MHLW's open data for online filings (**5,195**, 66% addressed), overlapping by 1.2% at block level. **10.7 restaurants per 1,000 residents** (9.2 placeable), beside Sendai's 9.5 |
| **Joined** | own list **96.0%**, MHLW **95.0%** block; MHLW's own coordinates median **35 m** |
| **Why one bucket** | **no personal-services list**: new openings are published as PDFs only. Food retail exists only as MHLW's partial, opt-in notifications |
| **Licences** | both **PERMITTED WITH CONDITIONS**: the city's list under PDL 1.0 (the dataset-level declaration accepted for the full-list file, owner 2026-09-24) and MHLW's PDL 1.0 |
| **Brief** | `docs/build_briefs/hiroshima.md` (4/4). Hiroden's streetcars are the network's backbone, and whether trams count is the owner's call |

#### Zurich in full

**▲ Zurich** 🇨🇭 — **moved here on 2026-09-22 out of the one-probe-each
band, and it is the same decision as Stockholm's.** It sat in the probe band while its open item
was described as "no second bucket found". That is now **measured absent**,
which is an answer rather than a question:

✅ **RAIL COUNTED 2026-09-23 — ZURICH HAS NO METRO, AND THAT IS NOT A BLOCKER.** Zero `route=subway` relations inside the Stadt boundary (OSM rel 1682248); its network is **42 tram relations across 18 refs, all named and ALL COLOURED**, plus **4 `light_rail`, ref S18** (the Forchbahn). ⚠️ **An earlier version of this row said Zurich therefore had "no drawable network at all". That was WRONG** — asserted from prose, corrected against the code. **`route_type 0` is DRAWN in at least seven built cities**: San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin. **Every tram EXCLUSION is a city that also has a metro**, where the trams are a dense street-running overlay — Milan's config calls its own exclusion *"a costed extension, not a discard"* and *"reversible"*. **Zurich has no metro for a tram to overlay, so its trams ARE the rapid-transit system**, and all 42 carrying a colour removes Milan's invented-palette objection. **The live question is the Muni Metro SPACING test** — are stops one or two blocks apart, needing `docs/sub_transit_line_filters.md`? **A cost, not a disqualification.**

| Term searched on `data.stadt-zuerich.ch` | Hits | What they actually are |
|---|---|---|
| `zzqqxxnonsense` **(control)** | **0** | the filter is real |
| `detailhandel` | **1** | a **traffic count** |
| `verkauf` | 12 | tram ticket offices, apartment sale prices |
| `laden` | 31 | a farm shop, population surveys, tariffs |
| `gewerbe` | 28 | zoning land, 3D roof models |
| `firmen` | 16 | **every one a `Firmenbefragung`** — a company *survey*, 2005–2025 |

Only **`Gastwirtschaftsbetriebe`** is a register: premises-level, GeoJSON,
food. The national STATENT is aggregate. **So Zurich is a one-bucket food
city, exactly Stockholm's shape**, and the question it now carries is the
same one — *does a food-density page belong in a project whose other cities
carry three buckets?* **Answer it once and two cities move together.**


▼ **32 cities joined 2026-09-27 from the second-city screens** (scratch in
`second_cities/<country>/`). **Every one passed all three buckets on a
national register this project has already built on**, so each costs its rail
leg, a scope measurement and its licence reads. **None has a metro**: every
French metro city is built (or is Lyon, discarded). **Stores near stations** is
storefronts within 966 m of a station, the screen's measure. French builds use
France's own config (a 483 m outer ring, Lambert-93), so the build recounts.
**Build-time calls are listed per row** and put when each brief is written, not
before.

*Nice and Rouen (EDGE) are in the EDGE group above.*

**🇫🇷 France (19)** — SIRENE through the built cities' step-2 chain, which
reproduced Rennes (3,479) and Toulouse (8,635) exactly as the control. Most
feeds are Licence Ouverte 2.0; Montpellier, Grenoble, Angers and Le Havre
ODbL. **Mode flags are unreliable** (Reims' feed types its tram as metro), so
the mode is decided per city.

| City | Network | Stations in the commune / total (worst line) | R / F / P (× OSM) | Stores near stations | Build-time calls |
|---|---|---|---|---|---|
| **Montpellier** | Tram 1–5 | 87 / 112 (line 2: 54%) | 2,484 / 2,622 / 1,193 (1.93×) | 6,179 | 54% matches Toulouse's T1 precedent |
| **Strasbourg** | Tram A–F (short Rotonde and Halles tunnels) | 66 / 94, plus 3 in Kehl, Germany (B: 52%) | 2,385 / 2,244 / 1,020 (2.11×) | 5,482 | Commune or regional |
| **Bordeaux** | Tram A–F | 53 / 135 (A: 35%) | 3,167 / 3,018 / 1,224 (1.84×) | 6,889; **10,754 over 14 communes** | **Regional scope** (Lille-style); TBM's Licence Ouverte **1.0** never read |
| **Nantes** | Tram 1–3 | 56 / 84 (line 3: 48%) | 2,105 / 1,844 / 852 (1.39×) | 4,341; 5,383 regional | Commune or regional (48% is just under Toulouse's line) |
| **Grenoble** | Tram A–E | 36 / 81 (C and D: 36%) | 1,541 / 1,601 / 598 (1.51×) | 3,716; 5,455 over 12 communes | **Regional scope** |
| Saint-Étienne | T1–T3 | 35 / 40 (81%) | 1,333 / 1,164 / 531 (1.71×) | 2,523 | — |
| Angers | A–C | 36 / 42 (76%) | 1,183 / 876 / 493 (1.48×) | 2,380 | — |
| Dijon | T1–T2 | 28 / 34 (82%) | 1,192 / 968 / 532 (1.50×) | 2,358 | — |
| Tours | A | 22 / 29 (76%) | 1,244 / 925 / 492 (1.52×) | 2,335 | — |
| Le Havre | A, B (Jenner tunnel) | 22 / 23 | 1,027 / 880 / 552 (1.95×) | 2,143 | Line C is in OSM only, not in service |
| Mulhouse | Tram 1–3 | 28 / 29 | 969 / 748 / 456 (3.66×, OSM thin) | 2,121 | The tram-train fails the rail test (30-minute midday headway) |
| Reims | 1 line, 2 branches | 22 / 24 | 1,167 / 927 / 598 (2.25×) | 1,947 | The feed types it `route_type` 1; it is a tram |
| Caen | T1–T3 (a real tram since 2019) | 29 / 38 (76%) | 986 / 833 / 420 (1.47×) | 1,881 | No feed of its own: the Normandie regional feed, agency Twisto |
| Brest | A, B | 39 / 41 | 952 / 679 / 360 (1.47×) | 1,845 | The feed ends 2026-12-20 |
| Besançon | T1, T2 | 29 / 31 | 1,012 / 676 / 369 (1.56×) | 1,794 | — |
| Orléans | A, B | 32 / 51 (B: 60%) | 901 / 619 / 351 (1.41×) | 1,772; 2,452 regional | Commune or regional |
| Le Mans | T1, T2 | 35 / 35 | 901 / 632 / 484 (1.54×) | 1,763 | Use the `gtfs_setram_lmm_auto` resource; `flex` has no tram |
| Avignon | T1 | 10 / 10 | 1,146 / 896 / 408 (1.86×) | 1,684 | Small |
| Valenciennes | T1, T2 | 12 / 48 (T2: 24%) | 514 / 412 / 192 (2.02×) | 1,027; 1,984 over 13 communes in 2 EPCIs | **Regional scope**; low interest |

**🇨🇿 Czechia (6)** — ROS02 establishments, RES activity and the RÚIAN join, as
Prague. **Before any of them: `czechia_register.ruian()` hard-codes a Prague
address as its coordinate check** and exits for every other town (sent to
Cleanup 2026-09-27).

| City | Rail (stations in the town) | R / F / P; restaurants × OSM | Build-time calls |
|---|---|---|---|
| **Brno** | 11 lines, **146 stations**; line 2 keeps 21 of 23. IDS JMK GTFS, CC BY 4.0 | 2,520 / 2,126 / 2,583 = **7,229**; 1.61× (Prague 1.59–1.63×) | The strongest trams-only find anywhere |
| **Ostrava** | 96 stations; **line 5 is a stub (10 → 3)**. No GTFS, rail from OSM | 1,309 / 1,101 / 1,561 = 3,971; 2.23× | Line 5 |
| **Plzeň** | Lines 1, 2 and 4: 53 stations, all inside | 1,225 / 863 / 1,425 = 3,513; 1.99× | PMDP's GTFS licence contradicts itself (CC BY against a CC0-like record): read it, or take OSM |
| **Olomouc** | Lines 1–7: 36 stations | 811 / 620 / 815 = 2,246; 1.80× | DPMO's GTFS declares no licence: OSM, or a read |
| **Liberec** | 34 stations alone (line 11 keeps 21 → 15); 41 with Jablonec, every line whole. DPMLJ's GTFS resets the connection, so OSM | 1,880 alone; **2,498 with Jablonec**; 2.45× | With Jablonec or without |
| **Most + Litvínov** | Joint scope 27 stations, every line whole. **Most alone fails the stub test** (lines keep 6 of 18, 9 of 21, 12 of 24) | 429 / 267 / 334 = 1,030; 3.71× | Joint scope is required; low value |

*Bergen (Norway) and Aarhus (EDGE) are in the EDGE group above.*

**🇩🇰 Denmark (1), 🇱🇻 Latvia (2)**

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Odense** 🇩🇰 | Letbane, one line, 24 stops in OSM against the operator's 26; every 7.5 min | 1,629 / 649 / 612 = **2,890** | — |
| **Daugavpils** 🇱🇻 | Routes 1–5, **38 stop names**, all inside; route 1 every 10 min, the others about hourly | Riga's two layers: food 98 (95.9% placed), shops and services 722 (100%); 81.5% within 483 m | Rail from OSM (the GTFS declares no licence); VZD's address file `aw_eka.csv` (CC BY 4.0) is a new source needing its own `data_sources.md` row |
| **Liepāja** 🇱🇻 | One line, **18 stop names**, about every 7 min | Food 131 (93.9%), shops and services 583 (100%); 69.7% within 483 m | As Daugavpils |

*Buffalo and Pittsburgh (EDGE) are in the EDGE group above.*

**🇺🇸 United States (6)** — Kansas City moved here from DISCARDED on 2026-09-27
(owner's call: "Kansas City trams okay"; discarded 2026-09-21 for "too little
rail", before the owner ruled that trams count). **Seven joined 2026-09-28 from
wave 2's US screen (owner's calls)**: New Orleans and Tucson on three buckets;
Houston and Sacramento with an address join to do (trams are their first
blocker); Buffalo as EDGE; Pittsburgh and Minneapolis with a Band C gap (no
personal services).

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Kansas City** 🇺🇸 | The KC Streetcar, **one line**. **Measured 2026-09-27 from OSM** (relations 7825409/7825410, Riverfront–UMKC with the Main Street extension): **18 stops, all inside Kansas City, Missouri**, about 9.6 km at a mean 0.56 km. It passes the stub test; OSM carries no colour. **Frequency read 2026-09-27 from RideKC's GTFS** (`gtfs_8_27_26.zip`, valid 2026-07-12 to 2026-10-03; route 601 "KC Streetcar", `route_type` 0; terms declared "free for anyone to use", not read): **every ~10 min all day, seven days a week**, 05:15 to past midnight, at River Market; both extensions in the feed. kcstreetcar.org's schedule page agrees (10-minute headways) | "KCMO Business License Holders" (Socrata `kkhs-93m4`): **15,895 rows**, geocoded, all three buckets in readable categories (Beauty Salons 662, Barber Shops 146, Clothing Retailers 192, Supermarkets 154); explicitly PUBLIC_DOMAIN | Pick a colour (OSM has none); `dba_name` is often a person ("HARRIS GREGORY J") - a privacy filter; `business_type` mixes fee codes ("Flat Rate 16", "Misc Rate 129") with activities |
| **New Orleans** 🇺🇸 | RTA streetcars 12, 47, 48 and 2: **110 unique stop names, all inside the city**; no line cut. Frequency search-level only (~10 min, varies by line): read RTA's GTFS at build | "Active Occupational Licenses" (Socrata `iqay-p646`, **CC0**, 16,481 rows, updated 2026-09-26, points on 100%): **~2,411 / 1,934 / 1,057** (3.4× / 1.9× / 20× OSM) | A small text taxonomy (NAICS-style descriptions, no codes); drop "Special Events-Other (Vendor)" (1,258) and "Home Based-Office Use Only" (357); `ownername` - `check_personal_exposure.py`; thin 110 street stops (Philadelphia's and San Francisco's filter) |
| **Tucson** 🇺🇸 | Sun Link, **21 stops, all inside**; every 10 min on weekdays 07–18, 20 in evenings and at weekends | The city's BUSLIC layer (`gis.tucsonaz.gov`, 34,764 active of 93,483, updated 2026-09-22), NAICS, active and not home-based: **4,056 / 2,011 / 1,245** (2.7× / 2.2× / 6.3×), points; terms an "as is" disclaimer, no licence named | A licence read; about 6,250 active licences are individuals' (privacy check); `naics.py` fits unchanged; the daytime-only 10-minute service disclosed |
| **Houston** 🇺🇸 | METRORail Red, Green and Purple, all inside the city (**from knowledge, not measured**: Overpass failed during the screen) | **The Texas Comptroller's "Active Sales Tax Permit Holders"** (`jrea-zgmq`, public domain, updated 2026-09-26; a NEW source): 79,097 outlets flagged inside city limits, `outlet_naics_code`: **28,368 / 11,870 / 2,057** | **Addresses only: an address join** (`address-join`); online and home sellers inflate retail, salons appear only if they sell taxable goods; 14,879 sole owners (privacy); rail and OSM density to measure. The Comptroller's `3kx8-uryv` (with out-of-business dates) is the alternative |
| **Sacramento** 🇺🇸 | SacRT light rail: **41 stations inside** (Blue 30 → 28, Gold 30 → 18, Green 9 → 9; OSM) | Business Operation Tax (the city's item `f4ee567a…`, 13,385 active in the city, 148 local descriptions): **~1,300 / ~1,010 / ~950** (1.7× / 1.1× / 6×; 241 independent stylists) | **Addresses only: an address join**; no licence declared; 5,724 rows with Location_City "ON FILE"; exclude `Principal_Owner_*`, `Primary_Phone_number`, `Mail_*` |
| **Minneapolis** 🇺🇸 | METRO Blue and Green (from knowledge, not measured) | Food inspections (CC0 waiver, 47,959 violation rows 2023–26, lat/lon): restaurants, plus grocery as retail (owner 2026-09-28) | **No personal-services source and no licence register** (a Band C gap); an inspection table, so de-duplicate to premises; the stub test to measure |

*🇨🇦 Canada: Kitchener–Waterloo (Regional) (joined 2026-09-27 from wave 2) and Ottawa (moved in from Band C 2026-09-28) are both EDGE, and both are in the EDGE group above.*

**🇮🇹 Italy (1), 🇪🇸 Spain (1)** — joined 2026-09-28 from wave 2's second group
(owner's calls). Both trams-only, both with coordinates on every row.

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Florence** 🇮🇹 | Tramvia T1 and T2: **39 stations inside the comune**; T1 keeps 22 of 26 (4 in Scandicci), T2 20 of 20. GEST's GTFS in the Regione Toscana feed, declared CC BY 4.0. T3 under construction (due end of 2026) | The Comune's layers on dati.toscana.it, declared CC BY 4.0: commercio in sede fissa, pubblici esercizi, attività estetiche, tintolavanderie. **7,355 / 3,024 / 1,673** (2.49× / 1.45× / 4.62× OSM) after dropping private clubs, internal shops, e-commerce, vending, farmers; **coordinates on 100%**, rows carry only an id and a type code (no names) | **639 food rows are exempt categories** (464 "non soggetta a requisiti comunali", 175 art. 53): Milan's *fuori piano* question (without them food is 2,385, 1.14×); Scandicci's 4 stops; a full licence read; 3,424 rows share a point |
| **Santa Cruz–La Laguna (Regional)** 🇪🇸 | Metrotenerife L1 and L2. **Either municipality alone is a stub** (Santa Cruz keeps L1 11/21, L2 1/6; La Laguna L1 10/21, L2 5/6); **together 21/21 and 6/6** | The Cabildo de Tenerife's georeferenced layers (`datos.tenerife.es`, publisher L03380011), declared `cc-by`: **3,786 / 2,528 / 494** (3.1× / 2.6× / 4.0× OSM, which is thin on the island); **coordinates on 100%** | **Currency first**: the rows are a directory created about 2016, updated 2015–2022 (Dallas was discarded on a four-year-old snapshot). The Cabildo's hostelería register (updated 2026-08-31) is current but addresses only. A taxonomy on about 60 `actividad_tipo` strings; phone and e-mail columns never read |

**Denmark's placement (owner's call 2026-09-27): OSM's imported DAR address
points**, whose `osak:identifier` is the DAR Husnummer id (95% of central
Copenhagen's are in OSM, median 0.03 m from DAR's own point). They place 97.0%
of Aarhus rows and 98.4% of Odense's, keyless, under ODbL. The owner reopens the
Datafordeler account only if a build proves it needs one.

**Not candidates of their own**: every Dutch and Danish suburb on a built or
listed network (Zoetermeer, Leidschendam-Voorburg, Amstelveen, Nieuwegein,
Schiedam, Lyngby-Taarbæk) is a regional add-on, because each keeps only a stub
of its lines inside its own boundary.

## DISCARDED — 84 cities, each naming its evidence

▼ **2026-09-28 — Mumbai, from the large-transit gap's re-screen** (owner's call). The city hosts were asked, as the gap file said; what answers is negative, and what times out (the state's Shops & Establishments system, MCGM's GIS servers) is application and planning systems rather than a register.

▼ **2026-09-28 — Munich, Frankfurt and Cologne, from the large-transit gap's German screen** (owner's call), each on a full enumeration of its catalogue and geoportal, and of its chamber of commerce. **Berlin left this table the same day for Band B** (owner): its chamber publishes a premises register (IHK Gewerbedaten) that the row's two keyword searches could not find.

▼ **2026-09-28 — Manila, from the large-transit gap's re-screen** (owner's call). Its old reason (the operator's feed types its lines as commuter rail) is obsolete, since OSM carries LRT-1, LRT-2 and MRT-3; the business side fails instead.

▼ **2026-09-28 — sixteen rows from wave 2's US screen** (owner's calls): Portland, Cleveland, Salt Lake City, Phoenix, Mesa, Honolulu, St. Paul, Oklahoma City and El Paso (no register); Atlanta (currency); Norfolk (a stream); Milwaukee, Detroit and Tampa (too thin, reversible); Cincinnati and Berkeley (rail). Tempe and St. Louis were not reached.

▼ **2026-09-28 — thirteen rows from wave 2's second group** (Spain, Italy; owner's calls): Genoa, Palermo, Bergamo, Sassari, Padua, Venice-Mestre, Bologna (revisit spring 2027), Vitoria-Gasteiz, Murcia, Granada, Jaén, Fuenlabrada and Zaragoza. Five more were not reached (the note below the tables).

▼ **2026-09-27 — eleven rows from wave 2's first group** (Canada, Brazil, Ireland; owner's calls): Laval, Longueuil, Brossard, Vaughan, Cork, Sobral, Juazeiro do Norte / Crato, Teresina, Maceió, João Pessoa and Natal. The four Brazilian cities "not carried forward" on 2026-09-23 are now measured on frequency.

▼ **2026-09-24 (evening) — the open gap's last three discards, on the owner's calls after a final re-probe**: Vienna (absence, now on the city's own hosts twice over), Santiago (coverage: four central comunas publish no current list) and Nagoya (the published permit stream carries only half the permits issued, so no rebuild can work).

▼ **2026-09-24 (morning) — five rows arrived from the open gap on the owner's calls**, each after its re-probe: Kuala Lumpur, Athens, Poznań and Bratislava on two-method negatives with the city's own host asked, and Hamburg on currency. Vienna, whose negative would also pass, stays in the gap by the owner's choice. **Naples, Lima and Messina followed later the same morning**, after the last re-probe batch.

▼ **2026-09-24 — thirteen rows left this table on an audit.** Every row was read
against the probe log and sorted by the kind of evidence behind it. **Twelve
rested on ONE method** — a national portal only, the city's own host never
asked, or the top hits of one search — which `add-country` says is an
ASSERTED negative, not a finding; they are in the open screening gap as a
re-probe queue (owner's call). **Amsterdam** went further: its own API
carries a current hospitality register, and it is in Band C. The 21 left
each rest on two methods, a measured register, or its terms.

▼ **Five of those 21 left the same night** (owner's call), when the columns
below were added and the check read them: Hyderabad, Naples, Santiago, Lima
and Messina. **The audit had sorted on the rows' wording again** — the very
failure it named — and the columns are what caught it.

**Every row carries its evidence as columns since 2026-09-24**, and
`scripts/check_discard_evidence.py` reads them. *Kind* says what the discard
claims; *Methods* lists each probe by its shape (`search`, `enumerated`,
`measured`, `read`, or `blocked`, which counts for nothing). An **absence** or
**coverage** row — one resting on something NOT being found — needs the city's
own host asked and two methods, or one that read the whole catalogue or
measured a register. A one-search negative cannot be added here without the
check refusing it. **Turin** and **Cairo**, the last two rows, came from the
open screening gap on 2026-09-24, each measured by two methods.

▼ **Cairo left this table on 2026-09-23** for the open screening gap. Its row
read *"No open-data infrastructure"*, which rests on one probe of one national
host, and the file's own sweep had already recorded it as unprobed. **A discard
row has to survive being read against the probe log; that one did not.**


▼ **Lisbon and Warsaw — added here by the 2026-09-23 sweep — left on
2026-09-24** with ten other single-method rows: see the note above the
open screening gap's table.

| City | Kind | Methods | City host asked? | Why |
|---|---|---|---|---|
| **Mumbai** 🇮🇳 | absence | read `portal.mcgm.gov.in`'s licence pages (forms only) and its RTI proactive disclosures (nothing on licences) · enumerated MCGM's ArcGIS Online org (437 public items, 107 services; the one licence layer is 7,361 Section 394 trade licences, mostly hazardous goods and manufacturing, no licence text, personal names on 3,536 rows) · read FDA Maharashtra (counts only: 187,030 licences) and the state DES pages (no register) | yes — `portal.mcgm.gov.in` and MCGM's ArcGIS Online; MCGM's own GIS servers and `lms.mahaonline.gov.in` timed out from outside India and were left alone | **No storefront list on any reachable host (2026-09-28).** Health licences, trade licences and Shops & Establishments registrations exist only as application systems or counts; no eating-house list anywhere. The blocked hosts are the state's S&E application system and the Development Plan map servers, not a register |
| **Munich** 🇩🇪 | absence | enumerated `opendata.muenchen.de` (337 datasets, read title by title) · enumerated the geoportal's WFS/WMS workspaces (mor, rku, soz, baut, baug, kvr, rbs, gsm_wfs, gsm, plan) · search GovData and `open.bydata.de` for Gewerbedaten and IHK | yes — `opendata.muenchen.de` and `geoportal.muenchen.de` | **No premises register, and no coordinates to join to (2026-09-28, never screened before).** Only aggregate trade counts, 54 markets and tourist sights; the gastronomy and retail layers are planning graphics in a WMS. The address file (4.1 MB) carries no coordinates, and Bavaria publishes building outlines but no house coordinates. IHK München sells addresses by order form; no open business data |
| **Frankfurt** 🇩🇪 | absence | enumerated `offenedaten.frankfurt.de` through its search endpoint (303 entries) · enumerated `geodatenkatalog.frankfurt.de` (555 records) · search GovData and GitHub for Gewerbedaten and IHK | yes — both city hosts | **No premises register (2026-09-28, never screened before).** Trade de-registrations by year and district only; the points-of-interest WFS is restricted to the city administration (INSPIRE Art. 13(1)(a)). House coordinates are open (dl-by-de/2.0), so a register would place; none exists. No IHK Frankfurt open data |
| **Cologne** 🇩🇪 | absence | enumerated `offenedaten-koeln.de` (DKAN metastore, 503 datasets) · enumerated the geoportal's ArcGIS services (85 in 15 folders; the secured folder refused and was left alone) · search open.nrw and GitHub for Gewerbedaten and IHK | yes — both city hosts | **No premises register (2026-09-28, never screened before).** Trade registrations by district 1995–2015, a 59-club nightlife register, weekly markets; the only named food source is the NRW tourism feed, a curated selection rather than a register. Addresses are open (161,591 points, dl-zero). IHK Köln has lookup databases only |
| **Manila** 🇵🇭 | absence | enumerated `data.gov.ph` in the browser (175 datasets from 17 agencies, none on businesses or permits) · read the portals of Makati, Quezon City, Pasig, Pasay, Mandaluyong, Marikina and San Juan (no business list; Makati an aggregate count, Quezon City's dashboards login-only) · read DTI's BNRS and the FDA verification portal (lookup only) | yes — seven of the cities on the lines; `manila.gov.ph`, Taguig, Caloocan and Parañaque answered 403 and were left alone | **No business list at any level (2026-09-28).** Permits are issued by each city's BPLO and none of the cities on LRT-1, LRT-2 and MRT-3 publishes them; FOI requests for business lists are redirected to the BPLO; PSA's establishment list is released only as aggregates; the national registers are lookups. No open address file to join to either (NAMRIA's footprints carry no addresses, under restrictive terms) |
| **Lyon** 🇫🇷 | terms | measured the data (~18,082 bucket rows) · read Grand Lyon's CGU · measured its National Access Point feed (dead since 2022-04-14) | yes — `data.grandlyon.com`, behind an account | **DISCARDED 2026-09-23 on FOUR independent blockers, not one.** Its DATA is fine — ~18,082 bucket rows, **51.4% named**, better than Paris — which is why this is a discard on terms and access rather than on data. **(1)** An account on `data.grandlyon.com` is required before any download, and this project does not create accounts. **(2)** Grand Lyon CGU **9.4** is an open-ended indemnity. **(3)** CGU **6.2** bars the producers' *signes distinctifs* *« associés ou non à l'utilisation des données »* — which collides with the invariant that every drawn line carries its real public name, Lyon's being **TCL**. **(4)** Its National Access Point feed is **DEAD since 2022-04-14** (0% availability) while the source portal is current, so even with the account the rail must come from behind it. ⚠️ **Toulouse's and Rennes' CGU were read 2026-09-23 and are CLEAN** — Opendatasoft template, no indemnity, marks clause excluding the data — so **Lyon's clauses are Grand Lyon's own, not a French pattern.** **Reinstatement template in `DECISIONS.md`, 2026-09-23** |
| **Tel Aviv** 🇮🇱 | terms | measured the register (22,176 rows) · read the municipal Terms of Use | yes | **DISCARDED ON TERMS, NOT ON DATA — owner's decision 2026-09-22.** The data is the strongest of any unbuilt city: **22,176 licensed businesses** with activity *and* location, **EPSG:2039 already in metres**, refreshed within two days. **The municipal Terms forbid it** — no copying, distributing or publishing, **no using the content to create a database**, extending to other websites and to non-commercial use, and requiring **explicit prior written consent**; the open-data portal's footer reads *all rights reserved*. The only remedy was a written request, made **in advance and against explicit prohibitions** — judged not worth the effort against its likelihood. **Not a data negative**, and the full measurement is retained below |
| **Kochi** 🇮🇳 | absence | enumerated the national catalogue · read K-SMART and Sanchaya (one licence at a time, no bulk export) · search `?t=establishment` (staff posts) | yes — K-SMART, which issues the Corporation's licences | **Same national sweep, same result** — India publishes trade-licence **counts**, never premises. Kerala's own route is transactional: K-SMART and Sanchaya renew licences one at a time with no bulk export, and the `?t=establishment` lead was a **false friend** — in Indian government usage *establishment* means **staff posts**, and that search returns 6,526 orders about staffing |
| **Sofia** 🇧🇬 | absence | enumerated `data.europa.eu`'s harvest of `data.egov.bg` (11,635 datasets) · blocked `data.egov.bg` (403 aimed at us) | yes — Столична община's own 76 datasets, read in full; `www.sofia.bg` not read | **11,635 Bulgarian datasets enumerated via `data.europa.eu`'s SPARQL endpoint, around a 403 aimed at us.** 141 municipal premises registers exist nationally; **Sofia's 76 datasets include none.** Its registers are all small towns — Sofia is Bulgaria's only metro city |
| **Sevilla** 🇪🇸 | absence | read the dead portal's last Archive capture · enumerated the city's ArcGIS org (1,260 items) | yes | **1,260 public ArcGIS items / 413 Feature Services enumerated** from org `hcmP7kr0Cx3AcTJk` after the dead portal's last Archive capture named its successor. **Rail is solved** (`METRO_Estacion` 21, `METRO_Linea` 20, no account). **No premises register**: `Locales` is 150 *vacant municipally-owned units*, the rest are property holdings and facility layers |
| **Bogotá** 🇨🇴 | rail | read its OSM relation (no ref, no colour) · measured the TransMilenio hub (153 BRT stations) | yes | **Fails on rail** — one unnamed-ref, zero-colour relation; its only mass transit is BRT |
| **Medellín** 🇨🇴 ↓ | measured | measured RUES (6,369,877 rows, no location column) · read the chamber's comuna×CIIU crosstabs · read the city's ArcGIS Hub (credential wall) | yes — behind a credential wall | **Three closed doors.** The city's ArcGIS Hub is **credential-walled**; the chamber of commerce publishes comuna×CIIU **crosstabs**; RUES has **6,369,877** premises rows and **no address, municipality or city column at all** |
| **Jakarta** 🇮🇩 ↓ | measured | measured the OSS register (53,827 rows, 9 columns, checked against the portal's component list) | yes | **No activity field.** The live OSS register has 53,827 rows and full street addresses across **exactly 9 columns**; the two that look like classification are legal form and business size |
| **Valencia** 🇪🇸 ↓ | absence | enumerated `opendata.vlci.valencia.es` (290 packages) | yes | **No premises register.** `opendata.vlci.valencia.es` is CKAN with **290 packages**, read in full. The only commercial-adjacent names are container locations, noise-monitoring stations and *zones d'activitats* — zoning polygons, not businesses |
| **Málaga** 🇪🇸 ↓ | absence | enumerated `datosabiertos.malaga.eu` (1,377 packages) | yes | **Business parks and facility layers only.** `datosabiertos.malaga.eu` is CKAN with **1,377 packages**. `empresas-y-sectores` is explicitly *"empresas que se encuentran en **parques empresariales**"*; `centros-comerciales` and `mercados` are `equipamientos` layers — a handful of malls and municipal markets. Licence is CC **BY-SA** |
| **Budapest** 🇭🇺 ↓ | absence | read `kozadat.hu` (an inventory search tool) · read Nébih's FELIR (CAPTCHA-gated lookup) and its two establishment PDFs · read `budapest.hu` (two data-ish links) | yes — `budapest.hu`; `opendata.` and `adatportal.budapest.hu` do not resolve | **Both routes closed.** Portal: `kozadat.hu` is a search tool over data inventories, not a data portal. Food authority: Nébih's FELIR is **CAPTCHA-gated** and is a one-customer lookup, not a register; its *Approved Establishments* holding is **two PDFs of processing plants** — slaughterhouses, dairies, egg packers, cold stores. Retail and catering are only *registered*, by county offices, unpublished |
| **Zagreb** 🇭🇷 ↓ | absence | enumerated `data.gov.hr` (3,889 packages; Grad Zagreb's 210) | yes — Grad Zagreb's own publisher account, read in full | **210 datasets, one commercial, and it is a grant list.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not `/api/3/...` — 3,889 packages once found. **Grad Zagreb** publishes 210 of them; the only commercial one is *Lista za dodjelu potpora … obrtničke djelatnosti*, a grants register. Croatia devolves to municipalities and the only business databases belong to villages — `baza-poduzetnika-i-obrtnika` is **Grad Ivanec** (pop. 13,000) and carries `adresu sjedišta`, the **registered office** |
| **Bilbao** 🇪🇸 ↓ | absence | read the city's portal (344 datasets, no search) · enumerated `datos.gob.es` publisher `A16003011` (600 datasets) | yes | **Aggregate barometers only.** Its own portal holds 344 datasets behind a paginated list with **no search** (its one form control is a sort order). Enumerated instead via `datos.gob.es`: **600 datasets** under publisher `A16003011`, whose entire commercial holding is *"Barómetro del comercio minorista"* — retail-trade survey aggregates by employment stratum, sector and territory |
| **Turin** 🇮🇹 | absence | search `aperto.comune.torino.it` (control 0) · search `dati.gov.it` (control 0) | yes | **Stale, and nothing replaced it.** The city's CKAN (`aperto.comune.torino.it`, nonsense control 0) holds *"Attività commerciali presenti 2019"* as its newest premises stock; every later commerce dataset is the statistical yearbook (aggregate). Italy's national catalogue (`dati.gov.it`, control 0) finds for Turin only animal-food processing plants, a regional summary and a 2009 survey. A map of 2019 premises is not a map of current density |
| **Cairo** 🇪🇬 | absence | read `cairo.gov.eg` · read CAPMAS (HTML only) | yes | **No register at any level.** The Governorate's own site (`cairo.gov.eg`, reached 2026-09-24) has no open-data section: a services portal, a population dashboard, a government-services map, and a **tourism guide of ~220 restaurants and ~50 malls** — a curated list for a city of 10 million, the Kuala Lumpur coverage trap. Nationally, CAPMAS serves HTML only |
| **Kuala Lumpur** 🇲🇾 | absence | enumerated DBKL's open-data page (10 datasets) · enumerated DBKL's ArcGIS server (two folders token-gated; `Hosted/LESEN_AKTIF` is 102 rows beside 42 CCTV points and 73 lamps) · enumerated `data.gov.my` (292 datasets, none from a local authority) · measured DOSM's `lookup_premise` (372 KL rows) | yes — DBKL's open-data page and ArcGIS server | **No register at any level, on three methods — moved here 2026-09-24 (owner's call) after its re-probe.** DBKL's licensing register exists only internally; the one public licence layer is a 102-row dashboard mock-up, and DOSM's premises table is a price-survey frame (the coverage trap `add-country` names) |
| **Athens** 🇬🇷 | absence | enumerated the city's CKAN `opendata.cityofathens.gr` (464 datasets, nonsense control 0) · enumerated its GeoServer (60 layers) · enumerated `data.gov.gr` (22,591 datasets) · blocked `geodata.gov.gr` (times out from GR and DE) · blocked `www.cityofathens.gr` (a Cloudflare challenge, not bypassed) | yes — its CKAN and GeoServer | **No premises register on the city's hosts or nationally — moved here 2026-09-24 (owner's call) after its re-probe.** The national business-notification list is 72,378 rows from 2018 with no address and no municipality |
| **Poznań** 🇵🇱 | absence | enumerated the city portal `www.poznan.pl/opendata` (66 datasets; GraphQL, read-only POST queries; nonsense control 0) · enumerated the city's 35 datasets on `dane.gov.pl` · enumerated its feature server (35 layers), map POIs (156 categories) and GIS portal (30 services) | yes — the city portal and its GIS | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** Alcohol permits are published only as aggregates (e.g. 840 category-A food-service permits). Side find, kept: the city portal carries a **tram GTFS modified 2026-09-18** |
| **Bratislava** 🇸🇰 | absence | enumerated the city's ArcGIS Hub `data.bratislava.sk` (680 items) · enumerated its ArcGIS Online org (2,093 items) · enumerated the geoportal server (724 of 1,023 services opened; 299 judged by name) · enumerated `data.slovensko.sk` over SPARQL (22,559 datasets) | yes — its Hub, ArcGIS org and geoportal | **No premises, food-service or opening-hours register — moved here 2026-09-24 (owner's call) after its re-probe.** The only use-class layer is a national 1.7M-point address layer whose category is the building's and partly OSM-sourced |
| **Hamburg** 🇩🇪 | absence | measured the city's 2016 retail survey (`api.hamburg.de/datasets/v1/einzelhandel`, 9,916 points, 1.17× OSM retail) · enumerated the transparency portal (521 map-service titles read) · enumerated the city API (411 datasets) | yes — `api.hamburg.de` and the transparency portal | **Stale, one bucket, and nothing replaced it — discarded on currency 2026-09-24 (owner's call).** A ten-year-old retail survey would misstate today's high streets; no food or personal-services register exists in either catalogue, and ALKIS building functions are whole buildings. Turin's shape. **Germany is again a two-city negative** (Berlin, Hamburg), each on its own hosts |
| **Naples** 🇮🇹 | absence | enumerated the city's CKAN `dati.comune.napoli.it` (37 datasets, nonsense control 0) · enumerated `dati.gov.it` for the Comune (36), the Città Metropolitana (96), Regione Campania (368) and every Napoli hit (182) · read the SUAP (on the national impresainungiorno platform; publishes no register) | yes — its CKAN and its SUAP | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** Commerce appears only as 2014 counts per procedure and district; the national catalogue's only premises lists are pharmacies, parafarmacie and historic shops; the SUAP's only lists are 2018–2019 outdoor-seating concessions. Italy's cadastral shop category is not open data, so there is no second layer. **Italy stays a Milan-and-Rome country** |
| **Lima** 🇵🇪 | coverage | enumerated `www.datosabiertos.gob.pe`'s 78 licence datasets (1 of Línea 1's 9 districts publishes: La Victoria) · read five districts' own sites (Villa El Salvador, Villa María del Triunfo, San Juan de Miraflores, San Borja, El Agustino — forms, procedure pages, login-only systems) · search gob.pe per district · blocked the Municipalidad Metropolitana, Surco and San Juan de Lurigancho (answer from Peru only) | yes — five districts' own sites | **Coverage fails on measurement — moved here 2026-09-24 (owner's call) after its re-probe.** Licensing is per district; five of Línea 1's districts, including the whole southern arm, are confirmed to publish nothing, so the line cannot be covered even if the three geo-blocked districts publish |
| **Messina** 🇮🇹 | absence | enumerated the city's catalogue (113 datasets) · enumerated `dati.gov.it` (113 for the Comune, 140 text hits) · measured the chamber's business list (18,467 rows, head offices only, 2022) | yes — its catalogue; the licensing office is behind SPID login | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** The chamber's list is company-level with no local units; SCIA/DIA is a 2021 flow with no activity field; a 1,531-point POI sample is not a register |
| **Vienna** 🇦🇹 | absence | enumerated the city's WFS (377 layers; the market layers are 550 unnamed stand outlines, and the only business list is 9 opt-in takeaways) · enumerated `data.gv.at` through its hub API (Stadt Wien 781 datasets; nonsense control 0) · read the national registers (GISA strips street addresses; Statistik Austria's company-to-activity file has no address; AGWR allows no public access to individual records) | yes — `data.wien.gv.at` and the city's map service, twice | **No premises register at any level.** The only premises rows on the city's hosts are outdoor-seating permits (no name, no activity, 0.42× OSM food) and market stands; the building use class is whole-building (0.19× OSM shops). The company register would give registered offices, not shops, and needs a ministry token. Re-probed twice (2026-09-24); the owner had held it in the gap after the first |
| **Santiago** 🇨🇱 | coverage | enumerated `datos.gob.cl` (272 publishers: 5 Metro comunas publish patentes) · measured Providencia's register (74,712 rows) · enumerated the comuna's GIS server (15 services; no licence or activity layer) · read `documentos.munistgo.cl` (scanned alcohol decrees only) · read the web archive's index of `transparencia.munistgo.cl` (no licence list after 2014) · blocked `transparencia.munistgo.cl` (403 to everyone) · read Las Condes, Ñuñoa, Estación Central, Macul, Maipú, Puente Alto and San Ramón's own sites | yes — every central comuna's own site | **Coverage fails downtown: Daegu's shape.** About 6 of ~33 Metro comunas publish a current list, and the four the network converges on (Santiago, Las Condes, Ñuñoa, Estación Central) publish none. The fix would take at least four transparency requests, each the owner's act and the last resort |
| **Nagoya** 🇯🇵 | absence | enumerated BODIK's food package and its full history (137 events, 61 resources: rolling 12 months of new permits) · read the web archive of the city's permit page (15 captures, 2019–2025: no standing list ever) · measured a Kyoto-style stitch against e-Stat's permits issued (new files carry 44–49% of issued, against Kyoto's 98–102%) | yes — the city's page and its catalogue | **No list, and none can be rebuilt.** The city never published a standing register, and its monthly files omit renewals, so a complete stream would reach at most about 54% of the official count, all opened since 2021. The recovered files reach 20.9%. Personal services: beauty salons only |
| **Tainan** 🇹🇼 | rail | enumerated OSM's route relations for Taiwan (subway, light rail, tram, monorail: none in Tainan) · read the Blue Line's OSM state (under construction) | no | **No urban rail — 2026-09-27, second-city screen.** Its 53,581 storefronts would pass. The claim that its TRA locals fail the rail test's frequency is ASSERTED (TDX needs a key), so a future timetable read is what could reopen it |
| **Hsinchu** 🇹🇼 | rail | enumerated OSM's route relations for Taiwan (none in Hsinchu; the LRT is only planned) · read the Neiwan and Liujia locals' service (about every 30–60 min) | no | **No urban rail — 2026-09-27, second-city screen.** 12,638 storefronts in the city; the TRA locals fail the rail test on frequency |
| **Trondheim** 🇳🇴 | rail | measured AtB's current GTFS (Sep 2026 – Feb 2027: line 9 runs Ila–Lian only, 16 stations) · measured ring coverage against the placed register | yes — AtB's own feed | **The one line reaches too little — 2026-09-27, second-city screen.** Only **3.7%** of its 2,510 placed storefronts lie within 483 m (9.5% within 966 m). With the St. Olavs gate section restored: 19 stations, 21.7% and 35.6% — the day that section returns is the day to re-measure |
| **Aubagne** 🇫🇷 | rail | measured AMP Agglobus's GTFS (one line, 7 stations, about 2.5 km) · measured ring coverage (526 storefronts within 966 m) | yes — the operator's feed | **Too thin — 2026-09-27, a judgement and reversible.** Less than a sixth of Rennes (3,479), the smallest French build. The line is not cut short; the Val'Tram extension is in OSM only, untagged |
| **Clermont-Ferrand** 🇫🇷 | rail | read T2C's GTFS (`route_type` 0) · read OSM's ways (`railway=tram`, no guidance tag) | yes — the operator's feed | **A rubber-tyred guided bus (Translohr), not rail — 2026-09-27.** Both sources call it a tram and neither can tell; the mode is known, not read, which is why the row says so. 2,565 storefronts near its 30 stations would otherwise pass |
| **Saint-Louis** 🇫🇷 | rail | measured Distribus's GTFS · read OSM route membership (4 of Basel BVB tram 3's 26 stops are in France) | yes — the local feed | **The short end of a Swiss line — 2026-09-27.** 274 storefronts near 4 stops. Annemasse (Geneva 17: 1 stop in the town), Leymen (Basel 10: 1 stop) and Sarreguemines (Saarbahn S1: 1 stop) are the same shape and never reached a row |
| **Brampton** 🇨🇦 | rail | measured the agencies' own `routes.txt` (no urban rail reaches Brampton; only GO commuter rail, excluded everywhere) · measured the city's business directory (6,059 rows, X/Y on 100%, `NAICS_DETAIL` on 97.3%) | yes — the city's directory | **Blocked on rail, not on data — recorded 2026-09-21 (`docs/canada_retrospective.md`; row added 2026-09-27).** Its data is better than most US cities'. Miami's regional precedent does not rescue it: Metrorail runs into Hialeah, but TTC Line 2 ends at Kipling inside Toronto. **Revisit mid-2027 for the Hurontario LRT**, asking "has an opening date been announced?" rather than "is it open?" (▼ wave 2, 2026-09-27: the Hazel McCallion Line has no opening date; Metrolinx expects construction to finish in early 2028) |
| **Laval** 🇨🇦 | absence | enumerated the city's Données Québec organisation (130 packages; the nearest is a layer of large shopping centres) · search (no other source) · measured OSM rail (métro line 2 keeps 3 of 31 stops inside the city; the REM 2) | yes — its Données Québec organisation | **No business register — 2026-09-27, wave 2.** Its 5 stations stay excluded from Montréal's map. Québec's *Registre des entreprises* (addresses and CAE codes, no coordinates) is CC BY-NC-SA 4.0 and **stays unused (owner, 2026-09-27: non-commercial)** |
| **Longueuil** 🇨🇦 | rail | measured OSM (the Yellow line keeps 1 of its 3 stations inside the city) · read its GeoHub (61 items: a *Répertoire des commerces*, CC BY 4.0, 159,824 rows duplicated about 10–21 times, a 2022-07 snapshot) | yes — its GeoHub | **One station — 2026-09-27, wave 2.** A register exists, but one métro station is not a map |
| **Brossard** 🇨🇦 | rail | measured OSM (3 REM stations: Panama, Du Quartier, Brossard) · enumerated Données Québec's organisations (none for Brossard) · search (only the bciti app's map, an app and not a file) | no | **Three stations at the end of the REM's south branch, and no register — 2026-09-27, wave 2** |
| **Vaughan** 🇨🇦 | rail | measured OSM (TTC Line 1: 2 stations, Vaughan Metropolitan Centre and Highway 407, both already in Toronto's excluded stations) · measured the York Region Business Directory 2024 (retail 1,893 / food 833 / personal 551, points; York Region Open Data Licence) | no | **Two stations — 2026-09-27, wave 2.** Not a Toronto add-on either: it would give Toronto a retail bucket at two stations only |
| **Cork** 🇮🇪 | rail | measured the NTA's national GTFS (803 routes: the only `route_type` 0 are Dublin's two Luas lines, and none is 1) · read TII's Luas Cork status (preliminary design; no Railway Order before the end of 2028) · measured the Mallow–Cobh/Midleton suburban line (13–17 min by day at Kent, but Kent is its only stop inside the city) | no | **No urban rail — 2026-09-27, wave 2.** The suburban line cannot pass the rail test with one stop in the city. Tailte Éireann's valuation register answers for Cork City Council, so the business leg would not block a re-screen when Luas Cork opens |
| **Sobral** 🇧🇷 | rail | measured OSM (2 VLT lines, 12 stations, all inside) · read the timetable (Diário do Nordeste, 2021: about every 48 min) · measured CNEFE (2,375 / 1,187 / 571, 99.8% placed) | no | **A diesel VLT every ~48 min — 2026-09-27, wave 2.** Fortaleza's Parangaba–Mucuripe precedent (same operator and vehicles, every 40 min), which the owner kept out under the trams rule the same day |
| **Juazeiro do Norte / Crato** 🇧🇷 | rail | measured OSM (VLT do Cariri: 9 stops, 5 in Juazeiro, 4 in Crato) · search (every 45 min at peak, 90 min midday, weekdays 06–19) | no | **A diesel VLT every 45–90 min — 2026-09-27, wave 2** |
| **Teresina** 🇧🇷 | rail | measured OSM (2026-09-23: one diesel line, 13 stations) · read the service during works (Cidade Verde, 2026-05-10: 2 peak departures each way) | no | **Two peak trips each way during works — 2026-09-27, wave 2.** "15-minute intervals" is the target after a modernisation still unfinished on 2026-09-11: re-screen when all-day 15-minute service starts |
| **Maceió** 🇧🇷 | rail | measured OSM (2026-09-23: 2 lines, 15 open stations; the Blue line runs on into Satuba and Rio Largo) · read pt.wikipedia's system article (20 min at best, about 1,150 riders a day) | no | **Suburban trains, every 20 min at best — 2026-09-27, wave 2** |
| **João Pessoa** 🇧🇷 | rail | measured OSM (2026-09-23: 1 line, 13 stations over 4 municípios) · read pt.wikipedia's system article (28 trips a day) | no | **Suburban, 28 trips a day — 2026-09-27, wave 2** |
| **Natal** 🇧🇷 | rail | measured OSM (2026-09-23: 2 lines, 80 km) · read pt.wikipedia's system article (24 trips a day in total) | no | **Suburban, 24 trips a day — 2026-09-27, wave 2** |
| **Genoa** 🇮🇹 | absence | enumerated the city's catalogue (163 packages; nonsense control 0) · enumerated `dati.gov.it` (158) · read the geoportal's layer list (766 WMS layers: commercial-plan zones and historic shops only) | yes — its catalogue and geoportal | **No premises register — 2026-09-28, wave 2.** Only 2013–2016 aggregate counts. Its one metro line was never measured, since the data fails first |
| **Palermo** 🇮🇹 | absence | enumerated its `dati.gov.it` publisher (1,681 packages: noise complaints and tourism statistics) · read the city portal's dataset archive · search | yes — its portal | **No premises register — 2026-09-28, wave 2.** Four tram lines, never measured |
| **Bergamo** 🇮🇹 | absence | enumerated the Lombardy catalogue's Bergamo datasets (44) · read the city's own list of geographic data · search | yes — its data list | **No premises register — 2026-09-28, wave 2.** The TEB tram (EDGE, on an old railway bed) never measured |
| **Sassari** 🇮🇹 | absence | enumerated its `dati.gov.it` publisher (23 packages) · read the city's own dataset page (empty) | yes — its dataset page | **No premises register — 2026-09-28, wave 2** |
| **Padua** 🇮🇹 | rail | read the mode (a Translohr, a rubber-tyred guided bus) · read OSM, which tags it tram | no | **A guided bus, not rail — 2026-09-28, wave 2.** Clermont-Ferrand's rule |
| **Venice-Mestre** 🇮🇹 | rail | read the mode (a Translohr) · read OSM, which tags it tram | no | **A guided bus, not rail — 2026-09-28, wave 2.** Clermont-Ferrand's rule |
| **Bologna** 🇮🇹 | rail | read the tram's status (Linea Rossa: service expected spring 2027; federMobilita 2026-09-11, the first CAF vehicle in testing) · read the Marconi Express (a cable-driven people mover) and the SFM (commuter frequency) · measured the SUAP lists on the city's portal (CC BY 4.0: 33,757 commercio, 18,710 somministrazioni, 5,891 servizi alla persona) | yes — its portal | **Blocked on rail, not on data — 2026-09-28, wave 2 (owner: discard for now).** Its register is among the best screened anywhere. **Revisit when the Linea Rossa opens (spring 2027)**, as Brampton's row does |
| **Vitoria-Gasteiz** 🇪🇸 | absence | enumerated the city's catalogue (200 datasets; the nearest is an IAE density grid in 100 m cells) · enumerated its `datos.gob.es` publisher (197) | yes — its catalogue | **No premises register — 2026-09-28, wave 2.** Euskotren's tram never measured |
| **Murcia** 🇪🇸 | absence | enumerated the city's catalogue (187 datasets, 2022–2023; "Actividades comerciales … por tipo" is an aggregate) · enumerated the regional CKAN (979; IAE for Molina de Segura only) · read `datos.gob.es` (no Murcia publisher) | yes — its catalogue | **No premises register — 2026-09-28, wave 2** |
| **Granada** 🇪🇸 | absence | enumerated the city's CKAN (6 packages: tourist licences and terraces) · enumerated the Andalucía catalogue (582; the IECA directory places only establishments of 50+ employees) · read `datos.gob.es` (no publisher) | yes — its CKAN | **No premises register — 2026-09-28, wave 2.** The Metro de Granada light rail never measured |
| **Jaén** 🇪🇸 | rail | read the tram's status (driver training daily since 2026-08-18; "autumn 2026", no date: Junta de Andalucía press note and local press, 2026-08-17) · enumerated the Andalucía catalogue (no premises register) | no | **Not in revenue service, and no register — 2026-09-28, wave 2** |
| **Fuenlabrada** 🇪🇸 | measured | measured `actividad-comercial-por-tipologia-y-localizacion` (`odc-by`, July 2026: retail 2,993, food 1,009, personal 527) · read its `DOMICILIO ACTIVIDAD` column (street names only, no house numbers; 40% blank) | yes — its portal | **Cannot be placed — 2026-09-28, wave 2.** A real register on MetroSur L12 (5 stations) whose addresses stop at the street |
| **Zaragoza** 🇪🇸 | measured | measured Aragón's Registro de actividades comerciales (`opendata.aragon.es` 324, CC BY 4.0, 21,072 Zaragoza rows: IAE code and street, no coordinates, no closure field) · measured Aragón's tourism restaurant register (67: 1,466 cafés and restaurants, no bars) · blocked `zaragoza.es` (connection refused on 80 and 443) | blocked | **Placement fails — 2026-09-28, wave 2 (owner's call).** Only about 36% of addresses carry a house number (61% a bare street), retail at 5.0× OSM likely counts closed shops, and food has no bars. Tram L1's 32 stops are all inside. **What would reopen it: the city's own layer, read in the owner's browser** |
| **Portland** 🇺🇸 | absence | enumerated the city's ArcGIS hub (354 items) · search (the only licence set is the defunct CivicApps one; Multnomah County's inspections are lookup-only) · measured Oregon's "Active Businesses - ALL" (`tckn-sxa6`, 561,388 principal places of business, no classification) | yes — its hub | **No classified premises register — 2026-09-28, wave 2.** MAX and the Streetcar give 132 stops inside the city (MAX Blue keeps 22 of 47) |
| **Cleveland** 🇺🇸 | absence | enumerated the city's hub (188 items) · search (ArcGIS Online and the web) | yes — its hub | **No register — 2026-09-28, wave 2.** A METRO city (the Red Line) |
| **Salt Lake City** 🇺🇸 | absence | enumerated the city's hub (71 items; Utah's portal answers "decommissioned") · read slc.gov (monthly PDFs of new applicants only, "not provided in any other format") | yes — its hub and site | **No register — 2026-09-28, wave 2** |
| **Phoenix** 🇺🇸 | absence | enumerated the city's CKAN (145 packages) · search (ArcGIS Online) · read phoenix.gov (no general business licence, only sales-tax licences) | yes — its CKAN | **No register — 2026-09-28, wave 2** |
| **Mesa** 🇺🇸 | absence | enumerated the city's Socrata catalogue (304 datasets: monthly aggregate counts only) · search (ArcGIS Online) | yes — its catalogue | **No register — 2026-09-28, wave 2** |
| **Honolulu** 🇺🇸 | absence | enumerated `data.honolulu.gov` (72 datasets) · enumerated the city's hub (167 items) · read the state entity register (2022, mailing addresses only) | yes — both | **No premises register — 2026-09-28, wave 2.** Skyline is a METRO |
| **St. Paul** 🇺🇸 | absence | enumerated the city's hub (126 items: liquor licences only) · search (Socrata discovery and ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2** |
| **Oklahoma City** 🇺🇸 | absence | enumerated the city's hub (38 items: hotel-motel tax and TIF districts) · search (ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2.** The streetcar runs every 12–20 min, fare-free since 2026-08-07 |
| **El Paso** 🇺🇸 | absence | enumerated the city's hub (5 items; a 260-row corridor business survey with contact columns, not a register) · search (ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2.** The streetcar runs limited days and hours |
| **Atlanta** 🇺🇸 | measured | measured the Revenue Department's licences (26,643 rows, licence years 2019–22, last edited 2023-04-24; points) · read the same organisation's 2026 NAICS layer (508 rows, Main Street districts only) | yes — the city's GIS organisation | **Stopped publishing: ruled out on currency, 2026-09-28 (owner's call), Dallas's precedent.** A current register exists but is not published whole; the fuller one would come only by asking the city, the last resort. A METRO city (MARTA) |
| **Norfolk** 🇺🇸 | measured | measured `dpi6-sct5` (10,240 rows, 7,338 with coordinates: ~905 / 403 / 508) · read its own description (new licences since 2019-01-01, no renewals, no closures) | yes — its portal | **A stream, not a register — 2026-09-28 (owner's call).** Nagoya's defect: food sits below OSM's (0.9×). The Tide (EDGE, 11 stations) would pass |
| **Milwaukee** 🇺🇸 | measured | measured the city's active food licences (`milwaukeemaps.milwaukee.gov`: 1,702 restaurants, 1,072 food dealers; points) · measured OSM rail (The Hop M and L: 13 unique stops, all inside) | yes — its map service | **Too thin — 2026-09-28, a judgement and reversible (owner's call), Aubagne's shape.** One short streetcar, food only |
| **Detroit** 🇺🇸 | measured | measured Restaurant Establishments (4,830 "Open", schools included; points) · read the city's licence layer (1,520 regulatory licences only) · read the QLine's service (one line, every 15 min; the People Mover not counted) | yes — its portal | **Too thin — 2026-09-28, a judgement and reversible (owner's call).** One streetcar line, food only |
| **Tampa** 🇺🇸 | measured | enumerated the city's hub (10 items; no register) · measured Florida DBPR's food file (~2,255 fixed premises with a Tampa postal city, addresses only; a new source, licence unread) · read the TECO Line's service (11 stations, every 15 min) | yes — its hub | **Too thin — 2026-09-28, a judgement and reversible (owner's call).** Food only, unplaced, on one short line. The state cosmetology file held licensees, not salons, and was deleted (owner) |
| **Cincinnati** 🇺🇸 | rail | search (the Connector every 20–25 min; SORTA's GTFS not read) · measured the city's Food Safety Program (2,334 licences inspected in the last year, public domain; the "Business Licenses" are peddler and chauffeur permits) | yes — its portal | **Fails the rail test on frequency — 2026-09-28, wave 2.** Food only as well; SORTA's GTFS is what would reopen it |
| **Berkeley** 🇺🇸 | rail | measured OSM (BART: 3 stations) · measured the city's Business Licenses (13,710 rows, NAICS, no coordinates) | yes — its portal | **Three stations, Brossard's shape — 2026-09-28, wave 2.** San Francisco's map draws Muni only, so BART is no built map's satellite |

▼ **2026-09-27: United States rows, moved here from
`docs/city_shortlist.md` when that file was retired** (San Jose, Fort Worth,
Austin, Charlotte; Kansas City moved on to Band T, owner's call), **plus
Denver and Dallas, whose discards were recorded only in the archived
DECISIONS** (rows added the same day). They were screened on 2026-09-18 to
2026-09-21, before this table had evidence columns. Each
method is written as it was recorded at the time. Where the record does not
say a whole catalogue was read, the method is marked `search`. The fuller
record is in `docs/decisions/2026-09-13.md` (2026-09-18, "Live check of
Dallas, Austin, Charlotte and Fort Worth"), `docs/decisions/2026-09-20.md`
and `docs/us_build_retrospective_addendum.md`.

| City | Kind | Methods | City host asked? | Why |
|---|---|---|---|---|
| **San Jose** 🇺🇸 | absence | search the city's CKAN `data.sanjoseca.gov` · search its ArcGIS hub `gisdata-csj.opendata.arcgis.com` | yes — both official portals | **No bulk business-tax dataset on either official portal. Live-verified 2026-09-18.** The only source found, `opendatasanjose.com`, is a third-party lookup tool with no export. With Denver, this is the case that made live verification a rule. Revisit only if a new source appears |
| **Fort Worth** 🇺🇸 | rail | measured the Certificates of Occupancy table (ArcGIS `CFW_Open_Data_Certificates_of_Occupancy_Table_view`, table 0: 72,065 rows, `JobUse` with 48 values) · search-level rail (TEXRail and the Trinity Railway Express; their GTFS not read) | yes | **The data is workable, the rail is not. Live-verified 2026-09-18.** The certificates run from about 2002 and are current through 2026. But 13,343 rows (about 19%) have no coordinates, the city and address fields are null on most rows, and a business that relocates appears more than once: it is a history of certificates, not a register. Revisit if the rail expands or a thin-network map becomes acceptable |
| **Austin** 🇺🇸 | absence | measured "Certificates Of Occupancy" (Socrata `f9mz-m6dy`, 291,759 rows) · search the city's Socrata for business sets (Active Credit Access Business Licenses `3buj-7jze`, 64 rows; vendor lists) | yes | **No business register. Live-verified 2026-09-18.** The dataset titled "Certificates Of Occupancy" is construction permits with a yes/no flag: no business name and no classification. The business sets found are small. The rail is one MetroRail line (from memory, not checked) |
| **Charlotte** 🇺🇸 | absence | read the city hub `data.charlottenc.gov` · read Mecklenburg County's GIS open-data page | yes | **No business or licence dataset. Live-verified 2026-09-18.** The city hub holds zoning, permit-review and planning layers, plus hand-curated point sets (grocery stores, pharmacies, medical facilities). The county page lists none. The rail is the LYNX Blue Line plus a streetcar (from memory, not checked) |
| **Denver** 🇺🇸 | measured | measured "Active Business Licenses" on the city's ArcGIS hub and on the Colorado Information Marketplace mirror (7 columns: `License_Num, License_Type, License_Sub_Type, License_Status, Entity_Name, Trade_Name, Expiration_Date`) · search the city's 347 catalogue datasets for an alternative | yes — the city's hub | **No address, no classification, no geometry — live-verified 2026-09-18** (`docs/decisions/2026-09-13.md`, "Ruled out Denver on live-verified data"). The "Business License Data Explorer" the first pass cited was Anaheim's. With San Jose, the case that made live verification a rule |
| **Dallas** 🇺🇸 | measured | measured `9qet-qt9e` (certificates of occupancy, PDDL, 23,731 rows, issued 2018-01-02 to 2022-11-15, last changed 2022-11-16) · read `ync5-xnfn` (a dashboard, not a dataset: HTTP 403, 0 columns) · measured `dri5-wcct` (food, 2016–2024, no licence, no business name) · enumerated the domain's 1,087 assets | yes — `dallasopendata.com` | **Stopped publishing: ruled out on currency, 2026-09-21** (`docs/decisions/2026-09-20.md`, "Dallas ruled out, on currency rather than schema"). Texas has no general city business licence, so the certificate of occupancy is Dallas's register, and it ends in 2022. A four-year-old snapshot cannot be disclosed away on a page |

Plus the 2026-09-27 second-city screens' no-urban-rail set (Toulon; Nancy,
now a trolleybus; Metz, Nîmes, Amiens and Pau, bus rapid transit; Aalborg's
+BUS; Kristiansand's amusement-park tram; Carcassonne and Réunion's CIREST,
whose feeds flag school buses as tram), wave 2's (Limerick, Galway and
Waterford, one InterCity station each; Cuiabá, whose VLT never ran and is
being replaced by a BRT), and the earlier one (Winnipeg, Hamilton and Québec City
(re-checked 2026-09-27: both lines still under construction, Québec's to open
in 2033), Halifax,
Mississauga, ~30 single-feed countries) and access-not-data
(Russia, Ukraine).

**Not reached (wave 2, 2026-09-28; owner's call: no row).** Each city's own
host refused or never answered, so a discard row would rest on no city-host
evidence, and the check above refuses one. Each waits on a read from the
owner's own browser: **Brescia** 🇮🇹 and **Catania** 🇮🇹 (both METRO;
`dati.comune.brescia.it` refused or timed out, `opendata.comune.catania.it`
timed out and `etnaopen` answered 403), **Cagliari** 🇮🇹 (a JavaScript portal
with no API), **Alicante** 🇪🇸 (refused; search shows only 2017–2021 IAE tax
files) and **Alcobendas** 🇪🇸 (a "Directorio de comercios" behind an Akamai
403; a Madrid L10 suburb). **The US (2026-09-28)**: **Tempe** 🇺🇸 (its
"General Business License List" answers 403 to scripts; Valley Metro Rail and
the Tempe Streetcar) and **St. Louis** 🇺🇸 (excise only so far; the Building
Division's Commercial Occupancy Permits API is live but untested, a probe
rather than a browser read). **US suburbs of built maps, no rows**: Newark,
Jersey City, Hoboken, Camden, Evanston, Pasadena, Santa Monica, Alexandria and
Oakland (no register found on two methods each); Cambridge and Somerville
(food only, so no Boston add-on); Hialeah and Coral Gables are already on
Miami (Regional). **Suburbs with no register** (wave 2, no rows):
Milan's (Sesto San Giovanni, Cologno Monzese, Rho/Pero, Assago; 21 metro
stations stay excluded from Milan's map), Madrid's (Getafe, Móstoles,
Leganés, Alcorcón, Parla, Rivas, Coslada, Boadilla, Pozuelo, San Sebastián de
los Reyes, Arganda) and Barcelona's (L'Hospitalet, Badalona, Santa Coloma,
Cornellà, Sant Adrià, El Prat, Esplugues: the Diputació's census returns 0
rows for each against a control of 323). Rome's one station outside the
comune (Pantano) needs no row.

⚠️ **Ottawa is NOT a no-rail city** (corrected 2026-09-27): it has 6 light-rail
routes (O-Train) and was ruled out on DATA on 2026-09-21. 697 catalogue
entries were scanned, and the only address-level commercial data is
food-safety inspections (`docs/canada_retrospective.md`). **That is Band C's
shape today (food only, like Stockholm), not a discard.** The owner placed it
in Band C on 2026-09-27; its row is there, not here.

~~**Houston** was ruled out beside Dallas "for the same structural reason (zero
results)" on 2026-09-21. That is one search, which cannot carry a row here, so
it sits with the search-level screen-outs.~~ ▼ **In Band T since 2026-09-28**,
on the Texas Comptroller's statewide sales-tax permit file, which the earlier
searches never found. **The same file bears on Dallas, Fort Worth and Austin**
(their rows above): a re-screen on it is queued (owner, 2026-09-28; PLAN).
Oklahoma City and El Paso now have measured rows above. There is also the 2026-09-18 US
screen's rail set, which was **search-level and never live-verified**: San
Antonio and Columbus (no
rail), Oklahoma City and El Paso (a streetcar only, so trams-only in shape
if a data screen ever passed), Nashville (one commuter line), Indianapolis
(bus rapid transit only), Jacksonville (a 2.5-mile people mover) and Las
Vegas (a short private monorail).

~~**Germany is a country-level negative**, on two cities measured independently
at two different portal hosts.~~ ▼ **Not any more (2026-09-24)**: Hamburg's row
rested on one search term and is back in the open gap; Berlin's stands.
▼ **Berlin's did not stand (2026-09-28)**: enumerating its catalogue found IHK
Berlin's per-premises register, and Berlin is in Band B (owner).
▼ **Hamburg returned the same day (morning), owner's call**: re-probed on two
methods, and discarded on currency, not on one search.

**The five added on 2026-09-22 each failed differently**, which is the useful
part: coverage (Santiago, Lima), sampling (Kuala Lumpur), no location column
(Medellín), no activity column (Jakarta). Four distinct ways for a
premises-shaped table to be unusable, and **not one of them is visible from a
dataset title**.

---

---

# BY COUNTRY — for country-by-country implementation

## ✅ Current by country — 2026-09-27

**Rebuilt 2026-09-27 from the band tables above** (the 2026-09-23 version
showed 30 built, Brazil as candidates and Japan in Band B). **The bands are
the source; this table is a view of them.** When they disagree, the bands win
and this table is stale. The Tier sections this table once replaced are in
the evidence file.

| Country | Built | Candidates | Bands | What stands between it and the next city |
|---|---|---|---|---|
| 🇺🇸 United States | **9** | **9** — Kansas City, New Orleans, Tucson, Houston, Sacramento, Buffalo, Pittsburgh, Minneapolis; Baltimore | T · N | Wave 2 (2026-09-28): seven to T (Houston and Sacramento need an address join; Pittsburgh and Minneapolis have no personal services), Baltimore to C (food only); sixteen discards; Tempe and St. Louis not reached. **Queued**: a re-screen of Dallas, Fort Worth and Austin on the Texas Comptroller's permit file; Long Beach (for Los Angeles) and Arlington (for D.C.) as regional add-ons, each checked first |
| 🇨🇦 Canada | **5** | **2** — Ottawa, Kitchener–Waterloo | T | Ottawa is food only, placed in Band C by the owner 2026-09-27 and moved to T 2026-09-28 (light rail, no metro); the Band C memo. **Kitchener–Waterloo (Regional)** joined T from wave 2 (ION light rail; food and personal, no retail). Vancouver's four SkyTrain suburbs are a rescope in PLAN, probes first. Brampton waits on the Hurontario LRT (revisit mid-2027; no opening date, construction to early 2028) |
| 🇲🇽 Mexico | **3** | **0** | — | Complete on the current screen: Monterrey (Regional) built 2026-09-27 and published with Daegu and Busan |
| 🇪🇸 Spain | **2** | **2** — Santa Cruz–La Laguna (Regional), Palma | T · N | Wave 2 (2026-09-28): **Santa Cruz–La Laguna** to T (the Cabildo's layers; currency first), **Palma** to C (food only, 13% placed). Zaragoza discarded on placement; Alicante and Alcobendas not reached. Valencia, Bilbao, Málaga, Sevilla still measured out |
| 🇮🇪 Ireland | **1** | — | — | Complete: wave 2 (2026-09-27) found no second city. Dublin's map already covers all four Dublin councils; Cork, Limerick, Galway and Waterford have no urban rail. Re-screen Cork when Luas Cork opens |
| 🇮🇹 Italy | **2** | **1** — Florence | T | Milan and Rome, bespoke per city. Wave 2 (2026-09-28): **Florence** to T (the Comune's layers, coordinates on every row). Bologna discarded until its tram opens (spring 2027); Brescia, Catania and Cagliari not reached. Turin, Naples and Messina discarded |
| 🇫🇷 France | **5** | **21** | T | Every one trams-only; waits on Band T's group decision. Lyon discarded |
| 🇨🇿 Czechia | **1** | **6** — Brno, Ostrava, Plzeň, Olomouc, Liberec, Most + Litvínov | T | Band T's decision; `czechia_register.ruian()`'s coordinate control is per city now |
| 🇩🇰 Denmark | **1** | **2** — Aarhus, Odense | T | Band T's decision; placement through OSM's DAR address points |
| 🇳🇴 Norway | **1** | **1** — Bergen | T | Band T's decision; Oslo's modules unchanged, no other calls |
| 🇱🇻 Latvia | **1** | **2** — Daugavpils, Liepāja | T | Band T's decision; VZD's address file needs its licence row |
| 🇳🇱 Netherlands | **2** | **4** — Den Haag, Utrecht, Rijswijk, Delft | T | Band T's decision; Rijswijk and Delft as Den Haag add-ons. No current food register in any of the four (Utrecht's is partial) |
| 🇭🇰 Hong Kong | **1** | — | — | Built; the East Asia region |
| 🇰🇷 South Korea | **3** | **5** — Incheon, Gyeonggi satellites; Daejeon, Gwangju, Gimhae | B · D | **Daegu and Busan built 2026-09-27** on the shared Korean module. Incheon needs an address join; Gyeonggi's café file is unusable; the other three have no city portal |
| 🇹🇼 Taiwan | **3** | **1** — Kaohsiung | D | Its door-plate file is geo-blocked to Taiwan |
| 🇯🇵 Japan | **6** | **3** — Hiroshima; Yokohama; Sendai | T · N · D | **Kobe built 2026-09-27** on the shared Japanese steps, **Osaka the same day** on the `japan-city` skill, mostly as a config, **Sapporo 2026-09-28** likewise, **Fukuoka 2026-09-28**, the first on two food lists, and **Kyoto 2026-09-28** on a rebuilt register, and **Tokyo 2026-09-28**, the last, ward by ward. Hiroshima food only and on streetcars (T), Yokohama personal services only, Sendai the city's permission |
| 🇧🇷 Brazil | **9** | — | — | Built 2026-09-24 as one batch. Wave 2 (2026-09-27) found no new city: six discards on frequency; **Contagem joins Belo Horizonte and Duque de Caxias joins Rio** as regional add-ons (owner; PLAN). Watch Salvador's VLT (trial running) and Teresina's 15-minute service |
| 🇸🇪 Sweden | — | **2** — Stockholm, Göteborg | B · T | Food only; the Band C memo. Göteborg is also trams only, so it waits in T |
| 🇨🇭 Switzerland | — | **1** — Zurich | T | Trams only and food only: Band T's decision, then the Band C memo |
| 🇷🇴 Romania | — | **1** — Bucharest | B | Food only, plus a browser-assisted fetch |
| 🇹🇷 Türkiye | — | **1** — Istanbul | N | Pharmacies and opticians only on İBB's portal (2026-09-28, owner); the districts, which license shops and restaurants, publish no lists |
| 🇦🇪 United Arab Emirates | — | **1** — Dubai | D | Every host of the licence register refuses this machine (2026-09-28); a read from inside the UAE first |
| 🇵🇭 Philippines | — | — | — | Manila discarded 2026-09-28 (no business list at any level) |
| 🇬🇧 United Kingdom | — | **1** — London | B | Food only on the FSA register (re-screened 2026-09-28, owner); the VOA list's terms bar publishing. Newcastle and Glasgow not re-screened |
| 🇸🇬 Singapore | — | **1** | N | Its food register is a 2016 snapshot; the owner's verdict is no page (2026-09-27) |
| 🇵🇱 Poland | — | **1** — Warsaw | D | Geo-blocked before measurement; a read from inside Poland first |
| 🇮🇳 India | — | **2** — Hyderabad, Delhi | D | Hyderabad geo-blocked before measurement; Delhi's current register behind a CAPTCHA and its state hosts blocked (2026-09-28). Mumbai discarded 2026-09-28; Kochi discarded |
| 🇵🇹 Portugal | — | **1** — Lisbon | D | The DGAE account (the owner is checking it); Porto would follow |
| 🇫🇮 Finland | — | **1** — Helsinki | D | Geo-blocked; a read from inside Europe |
| 🇪🇪 Estonia | — | **1** — Tallinn | D | Food register geo-blocked; the EHR order |
| 🇩🇪 Germany | — | **1** — Berlin | B | Berlin on IHK Berlin's per-premises register: shops, food and personal services without hairdressers and laundries (2026-09-28, owner; corrected the same day). Munich, Frankfurt and Cologne discarded the same day (no premises register); Hamburg discarded on currency |
| 🇦🇹 Austria | — | — | — | Vienna discarded (no premises register at any level). **The Linz lead is closed (2026-09-27)**: its "Gewerbeberechtigungen" (CC BY 4.0, from the central trade register) is annual AGGREGATE counts by trade type, about 200 bytes a year, and ends in 2014. No premises and no addresses. A premises register for Linz is still unprobed on the city's own host |
| 🇪🇬 Egypt | — | — | — | Cairo discarded (no register at any level) |
| 🇨🇱 Chile | — | — | — | Santiago discarded (coverage fails downtown) |
| **Total** | **55** | **74** | | A 0 · B 6 · D 12 · N 5 · T 51. Checked against the band tables by `scripts/check_master_list_counts.py` |

---

*The 2026-09-22 tier view, retained as evidence and not current (Tiers 1-6, the former Tier 5): see [city_master_list_evidence.md#tier-view-2026-09-22](city_master_list_evidence.md#tier-view-2026-09-22).*

## Countries ruled out

*▼ **2026-09-24 — eight countries left this list** with the discard audit:
Germany, Austria, the Netherlands, Greece, Portugal, Poland, Latvia and
Slovakia each rested on one national-level method, and their cities are in
the open gap (the Netherlands' Amsterdam now in Band A). A country is not ruled
out by its national portal's first page.*

🇦🇺 **Australia**, 🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)*

*🇦🇪 **Dubai left this list on 2026-09-28** for Band D: "no agency feed" is
obsolete now rail comes from OpenStreetMap, and its register's hosts refuse
this machine.*

*🇬🇧 **The UK left this list on 2026-09-28** with London (Band B, food
only): its reason, "NNDR is a tax register with no category", was wrong - the
rating list has a description and is ruled out by its terms instead.*

*🇪🇬 **Egypt left this list on 2026-09-23** with Cairo: one probe of CAPMAS is
not a country ruling. See the open screening gap.*

## The order, as decided

> **Current position, 2026-09-23.** Mexico, Spain, Ireland and Italy's Milan
> are built; France is **complete at five** (Paris, Marseille, Toulouse, Lille, Rennes).
> **The seventeen Band A cities are build-ready now**, nine of them Brazilian
> and three Taiwanese. **Brazil was
> picked to go first in the geocoding band and turned out to need no geocoder**
> (IBGE's census address file carries every establishment's coordinate), so
> **Taiwan was next in that band — and its first probe found the same thing**:
> every city publishes a keyless door-plate coordinate file, and Taipei's tax
> register joins to it at 92.5%. **Japan stays last**, and is the one country
> left whose address file has not been looked for. The numbered order below is the 2026-09-22 plan, kept because its
> reasoning (lift shared geocoding machinery into `pipeline/`, let Japan
> inherit it) still holds even though the country it named first changed.

1. ✅ **Mexico** — **DONE, 2026-09-22.** Two cities from one source, as
   predicted. It was also the project's first country outside anglophone North
   America and its first OSM-sourced rail leg, so it proved two things the
   screen had only asserted.
2. ▶ **Spain — NEXT, and it is exactly two cities.** Madrid and Barcelona are
   ready now, each with a build brief whose claims re-run green. The "other
   three likely rather than speculative" line was wrong: Valencia, Bilbao and
   Málaga were probed on 2026-09-22 and are measured negatives, and Sevilla is
   unreachable. **Plan Spain as two cities, not six.**
3. **Korea** and **Italy** — one city each, nothing to discover, both with
   named build work rather than open questions.
4. **Taiwan** — the first geocoding build, chosen because it is the cheapest:
   keyless geocoder, systematic addresses, four cities. **Lift the shared parts
   into `pipeline/` here**, not later.
5. **Norway**, **Denmark**, **Brazil** — the rest of Tier 3, in rising
   difficulty.
6. ⏸ **Japan** — **last, by decision.** Ten cities, and by then the geocoding
   machinery is built.

**France no longer sits outside this order awaiting a decision** — it was
made on 2026-09-22 and, after one reversal, went **in favour**. The employee
filter yields a defensible storefront layer, validated against OpenStreetMap,
and SIRENE arrives geolocated. That makes France **six cities on one national
integration with no geocoding leg** — on cities-per-unit-of-work, the
strongest unbuilt country in this screen. It belongs in the order, and where
it goes is the owner's call.

Tier 4's four probes (**Czechia** strongest) are cheap enough to run alongside
any of the above rather than competing with them.

**Sweden sits outside the numbered order too**, for the opposite reason to
France: its work is not architecture but a **scope call** — whether a
one-bucket, food-only city page belongs in this project at all. Settle that and
Stockholm is close to ready; leave it unsettled and there is nothing to build.
**Hong Kong is the one closed country worth reopening**, since its register is
known to exist and only the bulk route is missing.

---

## Four rules this list is maintained by

**A row reading "not reached", "unprobed" or a regional pattern is not a
discard.** Eleven cities were once sitting in the discard list on exactly those
grounds, against evidence in the same document. Every discard row above names
the finding that disqualified it, so a contradiction is visible rather than
inferable.

**A country ruling needs two cities measured, not one asserted onto a region.**
Germany no longer qualifies (2026-09-24): Hamburg's row rested on one search
term and is back in the open gap, leaving Berlin alone. Italy does not fail
merely because Naples did — Milan is built and Rome is in Band A.

**A discard states its kind, its methods and whether the city's own host was
asked, as columns — and `python scripts/check_discard_evidence.py` decides
whether that is enough.** Run it whenever the discard table changes. A
failing row moves to the open gap; the rule is not relaxed to keep it.

**A city sits in the band of its FIRST blocker, with every other blocker
noted beside it (owner, 2026-09-27; universal across every master list).**
Blockers are taken in this order (**amended by the owner 2026-09-27 evening**,
when Band T became "Contingent on trams": trams now come before buckets):
1. **Access (D)**: can the data be reached at all?
2. **Trams (T)**: does the build need a yes on trams-only maps?
3. **Buckets (C)**: does it yield two or more, without a measured gap?

So:
- Tallinn sits in D, tagged "trams only".
- A trams-only city sits in T whatever its buckets, with any Band C gap
  noted beside it: Zurich, Göteborg, Hiroshima, Utrecht and Den Haag moved
  there from C on 2026-09-27.
- **The one open exception**: Rijswijk and Delft are trams-only and still in
  C, pending the owner's word. The Band C memo recommends no page of their
  own (they are Den Haag regional add-ons).

A city is never listed in two bands. The same rule governs the Japan list
(`scripts/japan_ward_table.py`) and every chat republish.

## Before building any city on this list

**Check `docs/commuter_rail_list.md`** — which cities have commuter rail, the
two built maps that draw it (Dublin's DART, Copenhagen's S-tog), and the
candidates whose build must decide it (Japan, Seoul, Hong Kong, São Paulo).

- `docs/build_briefs/<city>.md` if one exists, then
  `python scripts/brief_check.py <city>` — a brief caches Step 0's mistakes as
  confidently as its findings.
- **A city outside every existing region needs one added.** `app/cities.py`
  raises on a city whose region is not a leaf of `REGION_ORDER`. **Europe is
  already ONE region**, so a new European country (Czechia, Denmark, Norway,
  Sweden, Switzerland, Romania) does not add one; **Seoul, Hong Kong, Brazil,
  Taiwan, Japan and Singapore each would**, and `check_macro_labels.py` is the
  measurement for whether a region frames its cities. *(This bullet said
  `REGION_ORDER` was still `["United States", "Canada"]` until 2026-09-23 — it
  now holds seven entries.)*
- `add-country` first for any country this project has never built in — every
  candidate country except France.
