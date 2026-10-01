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
> | **Built** | **76** across 23 countries *(Namyangju, a Gyeonggi satellite, 2026-09-30; Bergen, Aarhus, Buffalo, Sacramento and Houston, the light-rail cities from the tram list, 2026-09-29; Suwon and Bucheon, Gyeonggi satellites, 2026-09-29; Goyang, Seongnam and Yongin, the first Gyeonggi satellites, 2026-09-29; Incheon, South Korea's fourth, 2026-09-29; Bucharest, Romania's first, 2026-09-29; Stockholm, Sweden's first, 2026-09-29; Melbourne, Australia's second, 2026-09-28; Sydney, Australia's first, 2026-09-28; Newcastle (Regional), the United Kingdom's third, 2026-09-28; Glasgow, the United Kingdom's second, 2026-09-28; Buenos Aires, Argentina's first, 2026-09-28; Berlin, Germany's first, 2026-09-28; London, the United Kingdom's first, 2026-09-28; Tokyo, Japan's sixth and last, 2026-09-28; Kyoto, Japan's fifth, 2026-09-28; Fukuoka, Japan's fourth, 2026-09-28; Sapporo, Japan's third, 2026-09-28; Osaka, Japan's second, 2026-09-27; Kobe, Japan's first, 2026-09-27; Monterrey (Regional), Daegu and Busan, 2026-09-27; Seoul, Taichung, Taoyuan and Taipei (Regional), 2026-09-25; Riga, Hong Kong and Rotterdam, 2026-09-24; Toulouse, Lille (Regional) and Rennes, 2026-09-23; Oslo, Copenhagen, Prague, Amsterdam and Rome, 2026-09-24; Brazil's nine cities as one batch, 2026-09-24)* |
> | **Candidates** | **64**, all at least partially viable — A 1 · B 8 · C 0 · D 0 · R 18 · T 37 *(**Dallas from the discards to A 2026-09-30** (owner), on the Texas Comptroller's permit file; **The tram list's bucket-gap tier (T2) closed 2026-09-30** (owner): Zurich, Göteborg and Den Haag to T1, Utrecht to R, Santa Cruz–La Laguna, Rijswijk and Delft to the discards; **Bergen, Aarhus, Buffalo, Sacramento and Houston built 2026-09-29**, leaving A empty; **Baltimore from B to the discards 2026-09-29** on currency (owner); **Band C closed 2026-09-29** (owner): Singapore, Istanbul, Ankara, Perth and Ho Chi Minh City to the discards; **Minneapolis and Pittsburgh from C to B 2026-09-29** (owner), their worst lines' 42% accepted; **Ottawa and Palma from C to B 2026-09-29** on the post-reset measurements (owner's bar); **Yokohama from C to B 2026-09-29** on the amended rule 1, personal services only (owner); **Hiroshima, Kitchener–Waterloo and Baltimore from C to B 2026-09-29** on the Band C audit's reduced-bucket bar (owner); **Palma reopened** the same day, pending a placement check; **Incheon built 2026-09-29**, South Korea's fourth, leaving B; **Bucharest built 2026-09-29**, Romania's first, leaving B; **Stockholm built 2026-09-29**, Sweden's first, leaving B; **Santa Cruz–La Laguna to T2 2026-09-29 as food only (owner), after its stale retail and services directory failed currency the same day**; **Band T moved to its own file 2026-09-29** (owner), [`docs/tram_city_list.md`](tram_city_list.md), in tiers T1 and T2; **ten left T the same day** on a three-part light-rail test, owner's calls: Buffalo, Houston, Sacramento, Aarhus and Bergen to A, Ottawa, Minneapolis, Kitchener–Waterloo, Pittsburgh and Hiroshima to C; **Melbourne built 2026-09-28**, Australia's second, leaving B; **Sydney built 2026-09-28**, Australia's first, leaving B; **Newcastle (Regional) built 2026-09-28**, the United Kingdom's third, leaving B; **Glasgow built 2026-09-28**, the United Kingdom's second, leaving B; **Buenos Aires built 2026-09-28**, Argentina's first, leaving A empty; **Lisbon from D to R 2026-09-28** (owner): DGAE's accounts are for institutions only; the request is drafted; **Delhi from D to R 2026-09-28** (owner): no street address in MCD's licences, CAPTCHA restricted; **Ho Chi Minh City from D to C 2026-09-28** (owner): the CAPTCHA passed, the catalogue measured; **London and Berlin built 2026-09-28**, the United Kingdom's and Germany's first, leaving B; **Kaohsiung, Tallinn and Sendai from D to R 2026-09-28** (owner): R renamed "restricted or request only"; **Bands restructured 2026-09-28 (owner)**: N retooled as C (closer to a page); D split into D (the owner can act) and R (restricted); **Glasgow to B and Bengaluru to D 2026-09-28** from the transit-gap re-screen, owner's calls; **Tashkent, Hanoi and Ho Chi Minh City to D 2026-09-28** from the transit-gap re-screen, owner's calls; **Perth and Ankara to N 2026-09-28** from the transit-gap re-screen, owner's calls; **Sydney (City of Sydney) and Newcastle to B, Bangkok and Riyadh to D 2026-09-28** from the transit-gap re-screen, owner's calls; **Buenos Aires to A and Melbourne (City of Melbourne) to B 2026-09-28** from the transit-gap re-screen, owner's calls; Sydney queued for a re-probe; **Delhi to D 2026-09-28** from the transit-gap re-screen, owner's call: its current register sits behind a CAPTCHA and the state hosts refuse this machine; **Tokyo built 2026-09-28**, Japan's sixth and last, leaving A empty; **Berlin to B 2026-09-28** from the discards, owner's call: IHK Berlin's premises register, shops and food; **Istanbul to N 2026-09-28** from the transit-gap re-screen, owner's call: pharmacies and opticians only; **Dubai to D 2026-09-28** from the transit-gap re-screen, owner's call: its register's hosts refuse this machine; **London to B 2026-09-28** from the transit-gap re-screen, owner's call: food only on the FSA register; **Kyoto built 2026-09-28**, Japan's fifth, leaving A; **Fukuoka built 2026-09-28**, Japan's fourth, leaving A; **Sapporo built 2026-09-28**, Japan's third, leaving A; **Band C's last five given verdicts 2026-09-28 (owner)**: Band B reopened for the passed (Stockholm, Bucharest, Incheon, the Gyeonggi satellites), Band N created for no page (Singapore, Yokohama, Palma, Baltimore), Ottawa to T, Band C closed; **Osaka built 2026-09-27**, Japan's second, leaving A; **wave 2's US screen 2026-09-28**, owner's calls: New Orleans, Tucson, Houston, Sacramento, Buffalo, Pittsburgh and Minneapolis to T, Baltimore to C; **wave 2's second group 2026-09-28** (Spain, Italy), owner's calls: Florence and Santa Cruz–La Laguna (Regional) to T, Palma to C; **Kitchener–Waterloo (Regional) to T 2026-09-27 from wave 2's first group** (Canada, Brazil, Ireland), owner's call: T, not A, since ION has no metro; **Kobe built 2026-09-27**, Japan's first, leaving A; **Band T renamed "Contingent on trams" 2026-09-27 and five moved into it from C** (Zurich, Göteborg, Hiroshima, Utrecht, Den Haag), owner's call; **the 2026-09-27 second-city screens, owner's calls**: Daegu and Busan to A, reopened on their cities' own portals, and **both built the same day**, leaving A; **32 trams-only cities to T** (France 21, Czechia 6, Denmark 2, Latvia 2, Norway 1), edge networks tagged rather than promoted; Den Haag, Utrecht, Rijswijk, Delft, Incheon and the Gyeonggi satellites to C, whose caption widened to buckets with a measured gap; Daejeon, Gwangju and Gimhae to D; **Monterrey (Regional) to A 2026-09-27** and built the same day, Mexico's third city, screened on DENUE and OSM rail, its old rail-only negative obsolete; **Band T, trams only, created by the owner 2026-09-27, with the first-blocker rule made universal**; **Seoul, Taichung, Taoyuan and Taipei (Regional) built 2026-09-25**, leaving Band A; **the open gap emptied 2026-09-24 after a final re-probe, owner's calls**: Riga to A (tram rings, scoped vacancy disclosure), Yokohama to C (personal services only, no page for now), Lisbon, Helsinki and Tallinn to D, Vienna, Santiago and Nagoya to the discards; **Hong Kong, Rotterdam and Brazil's nine built 2026-09-24**, leaving Band A by being built; Kyoto from the open gap to A 2026-09-24 — its register rebuilt from the permit stream, owner's call; **Japan re-banded 2026-09-24 and the geocoding band closed** — Tokyo (8 wards), Osaka, Kobe, Sapporo and Fukuoka to A, Hiroshima to C, Sendai to D, Yokohama, Nagoya and Kyoto to the open gap; Rotterdam from the open gap to A; all owner's calls; Warsaw and Hyderabad to D 2026-09-24 from the open gap, owner's calls — each geo-blocked before measurement; Copenhagen, Prague, Amsterdam and Rome built 2026-09-24; Amsterdam to A 2026-09-24 — permits + BAG shop units, both licences read, owner's call; Amsterdam from the discards to C earlier the same night; Rome to A 2026-09-24 — SUAP premises joined to ANNCSU, owner's call with a build check; Prague back to A 2026-09-24 on open data — ROS02 establishments + RES; Kaohsiung moved from B to a reopened access-blocked band D 2026-09-23, owner's call; Brazil re-screened 2026-09-23: +7 cities, and São Paulo and Rio moved from B to A; Taipei (Regional), Taoyuan and Taichung moved from B to A the same evening; Rennes built; Prague paused to the open gap 2026-09-24)* |
> | **Open screening gap** | **0** — **emptied 2026-09-24** by a final re-probe of its last eight, each given a verdict (owner's calls) *(before that: Kyoto out again to A later the same day, on a rebuilt register; Yokohama, Nagoya and Kyoto in, Rotterdam out to A, 2026-09-24; ten left 2026-09-24 on the owner's calls after their re-probes: eight to the discards, Warsaw and Hyderabad to D)* |
> | **Discarded** | **100**, each naming its evidence *(**Dallas out to A and St. Louis in, 2026-09-30** (owner's wave-2 follow-ups); **Santa Cruz–La Laguna, Rijswijk and Delft 2026-09-30** from the tram list's T2 (owner): placement 57.7%, and no food source; **Baltimore 2026-09-29** from B, on currency (owner); **Singapore, Istanbul, Ankara, Perth and Ho Chi Minh City 2026-09-29** from Band C, closing it (owner); **Kolkata and Chennai 2026-09-28** from the transit-gap re-screen, owner's calls: per-licence lookups only; **Baku, Panama City and Caracas 2026-09-28** from the transit-gap re-screen, owner's calls; **Doha 2026-09-28** from the transit-gap re-screen, owner's call: the commerce register is counts only; **Algiers 2026-09-28** from the transit-gap re-screen, owner's call: no premises list at any level, after its "no urban rail" misfiling was corrected; **Mumbai 2026-09-28** from the transit-gap re-screen, owner's call: no storefront list on the city's or state's reachable hosts; **Munich, Frankfurt and Cologne 2026-09-28** from the transit-gap German screen, owner's call: no premises register on a full enumeration; **Berlin out to Band B** the same day; **Manila 2026-09-28** from the transit-gap re-screen, owner's call: no business list at any level; **sixteen from wave 2's US screen 2026-09-28**, owner's calls: Portland, Cleveland, Salt Lake City, Phoenix, Mesa, Honolulu, St. Paul, Oklahoma City, El Paso, Atlanta, Norfolk, Milwaukee, Detroit, Tampa, Cincinnati, Berkeley; **thirteen from wave 2's second group 2026-09-28**, owner's calls: Genoa, Palermo, Bergamo, Sassari, Padua, Venice-Mestre, Bologna, Vitoria-Gasteiz, Murcia, Granada, Jaén, Fuenlabrada, Zaragoza; **eleven from wave 2's first group 2026-09-27**, owner's calls: Laval, Longueuil, Brossard, Vaughan, Cork, Sobral, Juazeiro do Norte / Crato, Teresina, Maceió, João Pessoa, Natal; Denver, Dallas and Brampton 2026-09-27, whose discards were recorded only in the archived DECISIONS; San Jose, Fort Worth, Austin and Charlotte, moved in from the retired `docs/city_shortlist.md` 2026-09-27, with Kansas City, which went on to Band T the same day; Tainan, Hsinchu, Trondheim, Aubagne, Clermont-Ferrand and Saint-Louis from the 2026-09-27 second-city screens, on rail; Vienna, Santiago and Nagoya from the open gap 2026-09-24 after the final re-probe, owner's calls; Kuala Lumpur, Athens, Poznań, Bratislava, Hamburg, Naples, Lima and Messina from the open gap 2026-09-24, owner's calls after their re-probes; an audit moved 12 single-method rows to the open gap and Amsterdam to Band C, 2026-09-24; the evidence check moved 5 more the same night)* |
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

## Built — 76

| Country | Cities |
|---|---|
| **United States** (12) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. · Buffalo · Sacramento · Houston |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |
| **Mexico** (3) ✅ | **Mexico City** · **Guadalajara (Regional)** — built 2026-09-22, live in the app. · **Monterrey (Regional)** — **built 2026-09-27**, Mexico's third (`pages/47_Monterrey_Heatmap.py`; **58,565 storefronts, 38 stations**, Metrorrey Líneas 1–3 across four municipios): the national DENUE modules unchanged, the scope keyed on INEGI's municipio code, rail from OpenStreetMap with gate 3 exact (19 / 13 / 9) and Línea 3 in the operator's red; publishes with the next batch |
| **Europe** (24) ✅ | 🇩🇰 **Aarhus** — **built 2026-09-29**, Denmark's second (`pages/72_Aarhus_Heatmap.py`; **5,102 storefronts, 20 stations**, Letbane L2 on the city tramway, light rail, the kommune): Copenhagen's register and step 2 on the shared CVR/DAR cache, placed on OpenStreetMap's DAR address points (97.1%), a personal owner's or franchisee's premises shown by its address. · 🇳🇴 **Bergen** — **built 2026-09-29**, Norway's second (`pages/71_Bergen_Heatmap.py`; **3,597 storefronts, 33 stations**, Skyss Bybanen lines 1 and 2, light rail, the kommune): Oslo's register, step 2 and address join, a sole trader's premises shown by its address. · 🇷🇴 **Bucharest** — **built 2026-09-29**, Romania's first (`pages/64_Bucharest_Heatmap.py`; **15,593 storefronts, 64 stations**, Metrorex M1–M5, the municipality): DSVSA București's food registers (active rows, fetched by the owner in their browser), placed by joining each address to OpenStreetMap's address points in its own sector (74.9%, the unplaced quarter disclosed); sole traders and person-named companies by category. · 🇸🇪 **Stockholm** — **built 2026-09-29**, Sweden's first (`pages/63_Stockholm_Heatmap.py`; **5,218 storefronts, 82 stations**, the Tunnelbana's three lines, Stockholms kommun): the city's food inspection register, frozen at its 2025-10-21 inspections, one record per premises; food only, institutional kitchens out by name, 225 untyped premises classified from their name and flagged. · 🇩🇪 **Berlin** — **built 2026-09-28**, Germany's first (`pages/56_Berlin_Heatmap.py`; **60,313 storefronts, 275 stations**, U-Bahn U1–U9 and 16 S-Bahn lines, the Land of Berlin): IHK Berlin's membership register (WZ 2025), no names, Personal services partial (no crafts). · 🇬🇧 **Newcastle (Regional)** — **built 2026-09-28**, the United Kingdom's second (`pages/60_Newcastle_Heatmap.py`; **6,171 storefronts, 60 stations**, the Tyne and Wear Metro's Green and Yellow lines, the Sunderland branch included, the five Tyne and Wear districts): the Food Standards Agency's food hygiene register, food only, London's postcode-centroid tier (10%), rail from OpenStreetMap. · 🇬🇧 **Glasgow** — **built 2026-09-28**, the United Kingdom's second (`pages/59_Glasgow_Heatmap.py`; **4,708 storefronts, 15 stations**, the Glasgow Subway's one loop, Glasgow City): Food Standards Scotland's Food Hygiene Information Scheme, food only, from the FSA's open-data file, rail from OpenStreetMap; a flat address or a childminder never placed (owner). · 🇬🇧 **London** — **built 2026-09-28**, the United Kingdom's first (`pages/57_London_Heatmap.py`; **56,492 storefronts, 387 stations**, the Underground, DLR, Elizabeth line and six Overground lines, Greater London): the Food Standards Agency's food hygiene register, food only, rail from OpenStreetMap. · 🇱🇻 **Riga** — **built 2026-09-24**, Latvia's first (`pages/42_Riga_Heatmap.py`; **6,730 storefronts, 108 stations**, Rīgas satiksme's seven tram routes): food from the State Revenue Service's excise-licence register, joined to the city's own address points (96.8%), and shops and services from the cadastre's trade premise groups at their building footprints (99.4%); the vacancy disclosure scoped to the historic centre, and a Europe view that keeps its zoom with Riga a pan away on phones (owner). · 🇪🇸 **Madrid** · **Barcelona** · 🇮🇪 **Dublin (Regional)** · 🇮🇹 **Milan** · **Rome** · 🇫🇷 **Paris** · **Marseille** · **Toulouse** · **Lille (Regional)** · **Rennes** · 🇳🇴 **Oslo** · 🇩🇰 **Copenhagen** · 🇨🇿 **Prague** · 🇳🇱 **Amsterdam** · **Rotterdam** — **Rotterdam built 2026-09-24**, the Netherlands' second (`pages/40_Rotterdam_Heatmap.py`; **7,520 storefronts, 132 stations**, RET metro A–E and trams 1–8 and 11, gemeente only): Amsterdam's shape with the food layer REBUILT from the permit decisions Rotterdam publishes in its Gemeenteblad (1,939 premises), BAG shop units for the rest, and the metro and tram network measured on the timetable after a works period whose temporary trams 14 and 18 had looked like permanent lines. **Rome built 2026-09-24**, Italy's second (`pages/30_Rome_Heatmap.py`; **98,897 storefronts, 87 stations**, Metro A, B, B1 and C and the Roma–Viterbo urban service, comune only): Roma Capitale's SUAP premises register JOINED to ANNCSU house numbers at 95.7%, no names, and the food layer stated as an upper bound (2.67x OSM, no closing dates). **Amsterdam built 2026-09-24**, the Netherlands' first (`pages/29_Amsterdam_Heatmap.py`; **13,238 storefronts, 144 stations**, GVB metro 50–54 and 16 tram lines, gemeente only): the city's live hospitality-permit register for food, the BAG's shop-class units for everything else - one "Shops and services" category, because a building register cannot tell a hairdresser from a clothes shop - de-duplicated by address, and trams thinned with the sub-transit-line filters. **Prague built 2026-09-24**, Czechia's first (`pages/28_Prague_Heatmap.py`; **25,275 storefronts, 58 stations**, metro A, B and C): ROS02's establishments where they trade, the owner's activity from RES's CZ-NACE 2025, a RUIAN join for the point, and every natural person's or partnership's name replaced by its address - their premises at the owner's own seat left off. **Copenhagen built 2026-09-24**, Denmark's first (`pages/27_Copenhagen_Heatmap.py`; **14,978 storefronts, 64 stations**, Metro and S-tog, Copenhagen with Frederiksberg): CVR production units joined across six national files, coordinates JOINED to DAR, and every personally owned business shown by its address. **Oslo built 2026-09-24**, Norway's first city (`pages/26_Oslo_Heatmap.py`; **10,718 storefronts, 155 stations**, T-bane and trams, kommune only): an establishment register keyed on the PHYSICAL location address, coordinates JOINED to Kartverket's bulk address file, and every sole trader's name replaced by its address. the first four built and deployed 2026-09-22, Paris deployed 2026-09-23, **Marseille built and deployed the same day** (`pages/22_Marseille_Heatmap.py`; **18,177 storefronts, 66 stations**), **Toulouse** likewise (`pages/23_Toulouse_Heatmap.py`; **8,635 storefronts, 48 stations**), **Lille (Regional)** likewise (`pages/24_Lille_Heatmap.py`; **11,833 storefronts, 91 stations**) — **the first French city scoped regionally**, to the eleven communes its network serves, because the commune alone would have drawn the tram as a three-stop stub — and **Rennes built and deployed the same day** (`pages/25_Rennes_Heatmap.py`; **3,479 storefronts, 24 stations**), commune-only because its worst line keeps 11 of 15 stations, **which completes France at five cities**. **France is the first country here where the second city was materially cheaper than the first**: Marseille inherited the national register, the NAF taxonomy, the parquet cache and the Lambert-93 grid, and its own work was the scope measurement and the rail leg. That is Mexico's retrospective repeating, and the opposite of Spain's. **Toulouse made the third city cheaper again**: it downloaded nothing at all, because the 3 GB national parquet pair was already cached for the country, and its own work was one scope decision, one owner call, and a gate-3 run that matched the operator exactly on all four lines. It is also the first city anywhere here to draw a **non-rail mode** — the Téléo cable car — which was the owner's call after the brief's stated precedent for it turned out not to exist. **One macro-map region, not one per country**: Spain, Ireland and Italy were three regions holding four cities until they were collapsed the same day, which is what let France join without adding a sixth region. Spain is complete at two cities, Ireland at one, and Italy is a Milan-only country — so the countries are still the research unit, and only the MAP groups them. ⚠️ **France's own viability figure was corrected on the day Paris was built**: the recorded "50,156 storefronts, 92.5% of OSM" is not reproducible and the real ratio is about 1.78× — see `docs/build_briefs/paris.md`. France remains a build; `docs/global_country_shortlist.md`'s France row still carries the old number |
| **South America** (10) ✅ | 🇦🇷 **Buenos Aires** — **built 2026-09-28**, Argentina's first (`pages/58_Buenos_Aires_Heatmap.py`; **63,596 storefronts, 89 stations**, Subte Líneas A–E and H, the Ciudad Autónoma): the city's 2022–2024 land-use survey placed at its parcels' centres (99.8%), no names, stations and track from SBASE's own layers. · 🇧🇷 **São Paulo** · **Rio de Janeiro** · **Belo Horizonte** · **Brasília** · **Salvador** · **Fortaleza (Regional)** · **Porto Alegre (Regional)** · **Recife (Regional)** · **Santos (Regional)** — **built 2026-09-24 as one batch** (`pages/31`–`39`; **617,188 storefronts, 363 stations**), the first country built that way: every city to drafts, one review of all the text, one deploy check and one push. One national source, IBGE's CNEFE 2022 - the census's walk of every block, each establishment with the enumerator's description and a coordinate - read by a free-text classifier (`pipeline/taxonomies/brazil_cnefe.py`); unreadable descriptions dropped and disclosed, and only the category shown at an address that is also a home. Commuter lines went through the three-part rail test: São Paulo's CPTM Linha 9 and Rio's SuperVia Deodoro and Saracuruna drawn, the rest out. The macro map's **South America** region |
| **East Asia** (12) ✅ | 🇯🇵 **Tokyo** — **built 2026-09-28**, Japan's sixth and last (`pages/55_Tokyo_Heatmap.py`; **63,989 storefronts, 490 stations**, 52 lines across JR East, Tokyo Metro, Toei and eleven other operators, the 23 wards): each ward its own source - eight wards' own food lists, MHLW's filings for four, four wards' registers - JOINED to MLIT's address blocks (99.7% block); the fifteen wards with no usable list drawn as hollow stations, each ward's share of the official count on the page; JR East drawn as its nine services, and every line labelled by its operator's code (owner). · 🇯🇵 **Kyoto** — **built 2026-09-28**, Japan's fifth (`pages/54_Kyoto_Heatmap.py`; **32,355 storefronts, 117 stations**, the Kyoto Municipal Subway, JR West, Keihan, Hankyu, Kintetsu, the Randen and Eiden - 18 lines, city line only): a food register REBUILT from the 2021 list and every monthly list since, pinned at 2026-07-31 and disclosed as an upper bound (closures unseen), with the barber, beauty and laundry lists, JOINED to MLIT's address blocks (93.2% block) past Kyoto's street-corner addresses; the funiculars left out (owner). · 🇯🇵 **Fukuoka** — **built 2026-09-28**, Japan's fourth (`pages/53_Fukuoka_Heatmap.py`; **30,062 storefronts, 71 stations**, the Fukuoka City Subway's three lines, JR Kyushu and Nishitetsu, city line only): the first two-source Japanese city - the city's pre-2021 food list and MHLW's online filings, one pin where a premises is in both - with the barber, beauty and laundry registers, JOINED to MLIT's address blocks (98.1% block, MHLW's own point where the join misses); about one restaurant in five withheld its address (disclosed); Fukuoka's yatai counted (owner). · 🇯🇵 **Sapporo** — **built 2026-09-28**, Japan's third (`pages/52_Sapporo_Heatmap.py`; **28,674 storefronts, 95 stations**, the Sapporo Municipal Subway's three lines, the streetcar loop and JR Hokkaido, city line only): the city's food-permit list and its barber, beauty, laundry and coin-laundry registers JOINED to MLIT's address blocks (86.0% block, 13.9% at the block group on Sapporo's 条 grid, 0.1% unplaced), almost entirely as a config on the shared Japanese modules; station names in one style with block numbers as figures (owner). · 🇯🇵 **Osaka** — **built 2026-09-27**, Japan's second (`pages/51_Osaka_Heatmap.py`; **72,999 storefronts, 216 stations**, Osaka Metro's eight lines and the New Tram, JR West, Hankyu, Hanshin, Keihan, Kintetsu, Nankai and the Hankai tram - 34 lines, city line only): Kobe's shared steps with a config, the city's food-permit list and 生活衛生 registers JOINED to MLIT's address blocks (99.1% block, 13 unplaced), checked against the list's own coordinates at a median 38 m; the map with the most lines here, which took a measured colour search and a third label pass (owner). Publishes after Kobe. · 🇯🇵 **Kobe** — **built 2026-09-27**, Japan's first (`pages/50_Kobe_Heatmap.py`; **27,251 storefronts, 121 stations**, the subway, Port and Rokkō Liners, JR, Hankyu, Hanshin, Sanyō, Kobe Kōsoku and Kobe Electric, city line only): the city's food-permit list and 生活衛生 registers JOINED to MLIT's address blocks (97.3% block, 0.3% unplaced), rail from MLIT N02 collapsed on its station-group code, English station names from OSM, and a trade name that is the operator's own name shown by its permit type (owner). The shared Japanese steps (`pipeline/countries/japan_step1.py`, `japan_step2.py`) are for the cities after it. · 🇰🇷 **Busan** — **built 2026-09-27**, South Korea's third (`pages/49_Busan_Heatmap.py`; **89,798 storefronts, 110 stations**, Busan Metro Lines 1–4, Line 4 a monorail, and the Busan–Gimhae LRT): the same fourteen permit types through the city's keyless API, each pulled in full and never by state (which drops every permit since 2025-02), through Daegu's shared Korean module; frozen at 2026-04-15 and the rows agree; held for a batch publish. · 🇰🇷 **Daegu** — **built 2026-09-27**, South Korea's second (`pages/48_Daegu_Heatmap.py`; **67,212 storefronts, 86 stations**, Daegu Metro Lines 1–3, Line 3 a monorail): fourteen of the national permit registers from the city's own portal, read through a new shared Korean module that refuses the column renames Seoul's code would read as nothing; the rows end 2025-08-31 whatever the edition's label says (owner: build, date disclosed); held for a batch publish. · 🇹🇼 **Taipei (Regional)** — **built 2026-09-25**, Taiwan's third (`pages/46_Taipei_Heatmap.py`; **133,335 storefronts, 153 stations**, twelve metro and light-rail lines across Taipei and New Taipei): each city's own door plates through the shared step 2, the join's control reproduced (92.4%), and gate 3 exact on Taipei Metro's lines. · 🇹🇼 **Taoyuan** — **built 2026-09-25**, Taiwan's second (`pages/45_Taoyuan_Heatmap.py`; **45,014 storefronts, 15 stations**, the Airport MRT inside Taoyuan): Taichung's national modules and shared step 2, a TWD97 door-plate file reprojected, and stations from the national land-survey layer, whose own addresses say which city each is in. · 🇹🇼 **Taichung** — **built 2026-09-25**, Taiwan's first (`pages/44_Taichung_Heatmap.py`; **66,115 storefronts, 18 stations**, Taichung Metro's Green Line): the national business tax register joined to the city's door plates (92.2%), keyed by district because one street name recurs across districts; office-like company head offices dropped and unmarked sole proprietors shown by their line of business (owner's rules). The national modules and the `taiwan-city` skill came out of it. · 🇭🇰 **Hong Kong** — **built 2026-09-24** (`pages/41_Hong_Kong_Heatmap.py`; **21,135 storefronts, 141 stations**, MTR's eight urban lines and the Light Rail): FEHD's three licence registers, each licence at FEHD's own point from the same registers on the CSDI Portal - the brief's address geocode was never needed - and a map that is mostly restaurants, because Hong Kong licenses food and not general retail. Rail from OpenStreetMap, since MTR publishes no geometry; gate 3 exact against MTR's own station lists. The macro map's **East Asia** region, named for the Taiwanese, Korean and Japanese cities behind it |
| **Seoul Capital Area** (8) ✅ | 🇰🇷 **Namyangju** — **built 2026-09-30**, South Korea's tenth (`pages/83_Namyangju_Heatmap.py`; **18,344 storefronts, 17 stations**, Line 4, Line 8, and the Gyeongui–Jungang and Gyeongchun Lines): SEMAS's register, Incheon's module · 🇰🇷 **Bucheon** — **built 2026-09-29**, South Korea's ninth (`pages/70_Bucheon_Heatmap.py`; **22,512 storefronts, 14 stations**, Line 1, Line 7 and the Seohae Line): SEMAS's register, Incheon's module · 🇰🇷 **Suwon** — **built 2026-09-29**, South Korea's eighth (`pages/69_Suwon_Heatmap.py`; **33,433 storefronts, 14 stations**, Line 1, the Suin–Bundang and Shinbundang Lines): SEMAS's register, Incheon's module · 🇰🇷 **Yongin** — **built 2026-09-29**, South Korea's seventh (`pages/68_Yongin_Heatmap.py`; **23,481 storefronts, 24 stations**, the EverLine, the Suin–Bundang and Shinbundang Lines): SEMAS's national storefront register, Incheon's module · 🇰🇷 **Seongnam** — **built 2026-09-29**, South Korea's sixth (`pages/67_Seongnam_Heatmap.py`; **25,529 storefronts, 18 stations**, Line 8, the Suin–Bundang, Shinbundang and Gyeonggang Lines): SEMAS's register, Incheon's module · 🇰🇷 **Goyang** — **built 2026-09-29**, South Korea's fifth (`pages/66_Goyang_Heatmap.py`; **27,808 storefronts, 20 stations**, Line 3 and the Gyeongui–Jungang Line): SEMAS's register, Incheon's module · 🇰🇷 **Incheon** — **built 2026-09-29**, South Korea's fourth (`pages/65_Incheon_Heatmap.py`; **82,671 storefronts, 79 stations**, Incheon Lines 1 and 2, Line 1, Line 7 and the Suin–Bundang Line): SEMAS's national storefront register (상가(상권)정보, keyless, every storefront with a point), all three buckets - the national LOCALDATA API needs a Korean identity check. · 🇰🇷 **Seoul** — **built 2026-09-25**, South Korea's first (`pages/43_Seoul_Heatmap.py`; **239,410 storefronts, 308 stations**, Lines 1–9, Shinbundang, Ui LRT, Sillim and three Korail lines): seventeen of Seoul's citywide permit registers, each premises at its own building point or at another permit's at the same building (98% placed), one pin per premises with the five convenience-store chains matched by brand, and a Korean personal-name pass that withholds 138 names at home addresses. Rail from OpenStreetMap, since Korea's station dataset has no lines.. The macro map's own region since 2026-09-29 (owner): six cities within about 40 km, whose labels cannot share East Asia's zoom |
| **Oceania** (2) ✅ | 🇦🇺 **Sydney** — **built 2026-09-28**, Australia's first (`pages/61_Sydney_Heatmap.py`; **7,074 storefronts, 16 stations**, Sydney Trains' T1-T4, T8 and T9 and Sydney Metro M1, the City of Sydney LGA): the City's 2022 Floor Space and Employment Survey, all three buckets on ANZSIC classes, no names; light rail left out (owner). · 🇦🇺 **Melbourne** — **built 2026-09-28**, Australia's second (`pages/62_Melbourne_Heatmap.py`; **4,959 storefronts, 17 stations**, Metro Trains' six line groups, the City of Melbourne LGA): the City's 2024 Census of Land Use and Employment, all three buckets on ANZSIC classes, trading names; trams left out (owner). |

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

## Candidates — 64

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
| 🟢 **A** | **Ready to build.** Register measured, licence read, coordinates answered, rail answered — every remaining question is answerable inside the build | **1** *(Dallas from the discards 2026-09-30 (owner); + 47 built; Aarhus, Buffalo, Sacramento and Houston built 2026-09-29; Buffalo, Houston, Sacramento, Aarhus and Bergen from T 2026-09-29, light rail (owner); Buenos Aires built 2026-09-28; Tokyo built 2026-09-28; Kyoto built 2026-09-28; Fukuoka built 2026-09-28; Sapporo built 2026-09-28; Osaka built 2026-09-27; Kobe built 2026-09-27; corrected 2026-09-27 from a stale 10 + 28, then Monterrey added and built the same day; Daegu and Busan 2026-09-27, both built the same day; Buenos Aires 2026-09-28, from the transit-gap re-screen)* |
| 🔵 **B** | **Passed: narrower pages** (reopened by the owner 2026-09-28 for the cities that passed the Band C memo). Screening complete; the page shows one bucket, or all three with a measured gap, and says what is missing *(Stockholm and Bucharest passed 2026-09-27; Incheon and the Gyeonggi satellites 2026-09-28; London, Berlin, Melbourne, Sydney, Newcastle and Glasgow 2026-09-28, from the transit-gap re-screen; London, Berlin and Glasgow built the same day; Stockholm, Bucharest and Incheon built 2026-09-29. The letter's earlier band, geocoding at national scale, closed 2026-09-24; Hiroshima, Kitchener–Waterloo, Baltimore, Yokohama, Ottawa, Palma, Minneapolis and Pittsburgh passed 2026-09-29 on the reduced-bucket bar; Baltimore left for the discards the same day, on currency)* | **8** |
| 🟣 **C** | **Closer to a page** (Band N, "no page for now", retooled as C by the owner 2026-09-28, the letter having closed earlier that day). Screening complete; a page is not worth building on what is published today, but these are the likeliest to become buildable, and each row says what would change it *(Singapore, Yokohama, Palma, Baltimore, Istanbul, Perth, Ankara; Ho Chi Minh City from D, 2026-09-28; Ottawa, Minneapolis, Kitchener–Waterloo, Pittsburgh and Hiroshima from T 2026-09-29, each with a bucket gap and no verdict yet (owner); Hiroshima, Kitchener–Waterloo, Baltimore, Yokohama, Ottawa, Palma, Minneapolis and Pittsburgh to B 2026-09-29; **closed 2026-09-29**, its last five to the discards (owner))* | **0** |
| 🔴 **D** | **Blocked, but the owner can act alone** (retooled by the owner 2026-09-28). A CAPTCHA or a free account stands between us and the file, and the owner can clear it without waiting on anyone; each row names the act *(empty since 2026-09-28: Ho Chi Minh City to C, Delhi and Lisbon to R, once the owner had checked each)* | **0** |
| ⚫ **R** | **Restricted or request only** (created by the owner 2026-09-28; renamed the same day). The publisher answers only inside its country, or only to an identity this project cannot hold, or only on request (a permission, an order, a bureau's reply), so the push past the block is out of the owner's hands; no VPN, proxy or account. **Future request-only cities go here** *(geo-blocked: Warsaw, Hyderabad, Helsinki, Dubai, Bengaluru, Bangkok, Riyadh, Tashkent, Hanoi, Gimhae; residency walls: Daejeon, Gwangju; request only: Kaohsiung, Tallinn, Sendai; restricted CAPTCHA and no street address: Delhi, 2026-09-28; institutional accounts only: Lisbon, 2026-09-28; portal refuses this machine, and a browser: Utrecht, from the tram list 2026-09-30)* | **18** |
| 🟤 **T** | **Contingent on trams** (created by the owner 2026-09-27 as "trams only", renamed the same day). The build waits on the owner's yes to trams-only maps: the rail is trams or streetcars with no metro. **Listed in its own file since 2026-09-29**, [`docs/tram_city_list.md`](tram_city_list.md): T1 ready if trams are approved, T2 with a bucket gap as well. **Light rail left for A and C the same day** on a three-part test (owner). Riga (built 2026-09-24) is the precedent | **37** *(T2 closed 2026-09-30 (owner): Zurich, Göteborg and Den Haag to T1, Utrecht to R, Santa Cruz–La Laguna, Rijswijk and Delft to the discards; Santa Cruz–La Laguna to T2 2026-09-29 as food only (owner), after its stale retail and services directory failed currency the same day; ten to A and C 2026-09-29 (owner); Ottawa from Band C 2026-09-28; seven US cities from wave 2, owner 2026-09-28; Florence and Santa Cruz–La Laguna from wave 2, owner 2026-09-28; Kitchener–Waterloo from wave 2, owner 2026-09-27; Rijswijk and Delft from C as Den Haag add-ons, owner 2026-09-27; 32 from the 2026-09-27 second-city screens; Kansas City from the discards; five from Band C; all owner 2026-09-27)* |
| | **Candidates** | **64** *(Dallas to A 2026-09-30 (owner); T2's verdicts 2026-09-30 (owner): three to T1, Utrecht to R, three to the discards; Aarhus, Buffalo, Sacramento and Houston built 2026-09-29; Baltimore to the discards 2026-09-29; Band C's last five to the discards 2026-09-29; Incheon built 2026-09-29; Bucharest built 2026-09-29; Stockholm built 2026-09-29; Santa Cruz–La Laguna to T2 2026-09-29 as food only (owner), after its stale retail and services directory failed currency the same day; Band T to its own file and ten light-rail cities from T to A and C 2026-09-29 (owner); Melbourne built 2026-09-28; Sydney built 2026-09-28; Newcastle built 2026-09-28; Glasgow built 2026-09-28; Buenos Aires built 2026-09-28; Berlin built 2026-09-28; London built 2026-09-28; Glasgow to B and Bengaluru to D 2026-09-28 (owner); Tashkent, Hanoi and Ho Chi Minh City to D 2026-09-28 (owner); Perth and Ankara to N 2026-09-28 (owner); Sydney and Newcastle to B, Bangkok and Riyadh to D 2026-09-28 (owner); Buenos Aires to A and Melbourne to B 2026-09-28 (owner); Delhi to D 2026-09-28 (owner); Tokyo built 2026-09-28; Berlin from the discards to B 2026-09-28 (owner); Istanbul to N 2026-09-28 (owner); Dubai to D 2026-09-28 (owner); London to B 2026-09-28 (owner); Kyoto built 2026-09-28; Fukuoka built 2026-09-28; Sapporo built 2026-09-28; Band C's last five given verdicts 2026-09-28, and C closed (owner); Osaka built 2026-09-27; eight US cities from wave 2 2026-09-28; Florence, Santa Cruz–La Laguna and Palma from wave 2 2026-09-28; Kitchener–Waterloo from wave 2 2026-09-27; corrected 2026-09-27 from a stale 24 to 20, then Monterrey added; 43 more from the second-city screens the same day; Kansas City from the discards; Ottawa to C; Monterrey, Daegu and Busan built; Kobe built)* |
| *Open gap* | Unscreened — a row resting on an absence, so not a discard | *0 (emptied 2026-09-24)* |
| *Discarded* | Measured negative, evidence named | *100* |

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

## 🟢 Band A — ready to build (1 ready + 47 ✅ BUILT)

### ▲ 🇺🇸 Dallas — from the discards on the Comptroller's permit file (2026-09-30, owner's call)

**Queued for the Band B build session, last in its queue (owner, 2026-09-30).** Brief: `docs/build_briefs/dallas.md`, 4/4.

Discarded on 2026-09-21 because the city's certificates of occupancy stopped
in 2022. **The Texas Comptroller's Active Sales Tax Permit Holders file
(`jrea-zgmq`, public domain), Houston's register, replaces them.** The owner
approved the re-screen (2026-09-28) and the move (2026-09-30).

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Dallas** 🇺🇸 | DART light rail, Red, Blue, Green and Orange: **44 stations inside the city** (OSM relation 6571629, 1,018 km²), 1,397 m median gap, so standard rings. Worst line Orange, 17 of 30 inside (57%, over Toulouse's 52%). Purpose-built track, so frequency is disclosed, not gated. The Silver Line and the TRE are commuter rail, not drawn | `jrea-zgmq`, 44,760 outlets flagged DALLAS inside city limits, permits to 2026-09-26: **19,557 storefronts** once non-store retail (454, 4,350) and parking (812930, 256) leave: retail about 11,900, food 6,310, personal about 1,360. **Placed 90.0%** on a 300-row sample against the City's AddressPoints (395,893 main addresses, `services2.arcgis.com/rwnOSbfKSwyTBcwN`): exact 88.3%, same-side number 1.7%. **24.4% within 0.6 mi** of a station (a 400-row sample) | Houston's module and rules: never `taxpayer_name`, `taxpayer_address` or `taxpayer_number`; suppress `outlet_name` for sole owners; strip suites (38.6% carry one). **The AddressPoints layer, read 2026-09-30: SILENT on reuse, with an open-ended indemnity accepted by use; the owner accepted it (2026-09-30)** (`docs/data_sources.md`, "Dallas's indemnity"). Never call the pin locations surveyed or exact. The Dallas Streetcar and the M-Line trolley: an owner call at the build |

### ▲ Five light-rail cities from Band T — 2026-09-29 (owner's call)

**Light rail passes on precedent**: San Diego, Calgary and Edmonton were built
on light rail with no metro, and no tram decision was made for them. These
five passed the three-part light-rail test (track, frequency, spacing,
calibrated on those three; the test and its measurements are in
[`docs/tram_city_list.md`](tram_city_list.md)) and carry all three buckets.
Street trams stay on the tram list.

| City | Network | Business | Build-time calls |
|---|---|---|---|

▲ **🇦🇷 Buenos Aires joined 2026-09-28** from the large-transit gap's
never-screened list (owner's call). Network class: **METRO**. Argentina's
first city. **Built 2026-09-28** and its row moved to the Built table (its
screen's figures are in `docs/build_briefs/buenos-aires.md`); the rail came
from SBASE's own station and track layers, found at the build, not OSM.

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
| ✅ | ~~**Houston**~~ 🇺🇸 | The Texas Comptroller's Active Sales Tax Permit Holders (outlet columns and the organisation type only), placed by an address join to the City's Site Addresses (83.9%) and the Census geocoder (12.4%), scoped by TIGER's place polygon | **BUILT 2026-09-29** — `pages/75_Houston_Heatmap.py`, region *United States East*, **29,912 storefronts, 40 stations** (Red, Green and Purple from OSM, light rail). **7.4% in the rings**, stated on the page (owner); a person's permit shows its address, and one at a Residential point is left off (owner); Purple has 10 stations, not the brief's 13. See `docs/build_briefs/houston.md` |
| ✅ | ~~**Sacramento**~~ 🇺🇸 | The City's Business Operation Tax register (unexpired at the fetch date; never the owner, phone or mailing columns), placed by the Census geocoder (98.0%) and scoped by point-in-boundary | **BUILT 2026-09-29** — `pages/74_Sacramento_Heatmap.py`, region *United States West*, **3,335 storefronts, 37 stations** (Blue and Gold from OSM, light rail). The Green Line is suspended and not drawn (Township 9 closed for works); Dos Rios placed from Wikidata; three downtown couplets merged; person-like names shown by description (owner) |
| ✅ | ~~**Buffalo**~~ 🇺🇸 | New York's three-register shape: the City's Business Licenses (unexpired at the fetch date, since every row says Active), NYS food stores and NYS salon businesses, the State's rows scoped by point-in-boundary on the Census place polygon | **BUILT 2026-09-29** — `pages/73_Buffalo_Heatmap.py`, region *United States East*, **1,564 storefronts, 14 stations** (NFTA Metro Rail from OSM, light rail). The screen's ~1,670 became 1,564: 186 City grocers merged into the State's rows, caterers out (R1), 3 salons at an apartment out and 42 person-named salons shown by type (owner) |
| ✅ | ~~**Aarhus**~~ 🇩🇰 | Copenhagen's modules: CVR production units on the shared generation-505 cache, `969900` dropped on Aarhus's numbers, the Husnummer id joined to OpenStreetMap's `osak:identifier` points (**97.1%**) | **BUILT 2026-09-29** — `pages/72_Aarhus_Heatmap.py`, region *Europe*, **5,102 storefronts, 20 stations** (Letbane L2 on the city tramway, light rail; halved rings). The screen's 5,283 became 5,254 before placement, and 39 stations became the owner's 20: Odderbanen and Grenaabanen fail the 15-minute test on Midttrafik's timetables. A franchisee's own name with a store number now shows the address (owner) |
| ✅ | ~~**Bergen**~~ 🇳🇴 | Oslo's modules unchanged: the national sub-unit register (shared 2026-09-23 cache), the parent join and sole-trader rule, `96.990` dropped on Bergen's numbers, Kartverket's address join (**96.2%**) | **BUILT 2026-09-29** — `pages/71_Bergen_Heatmap.py`, region *Europe*, **3,597 storefronts, 33 stations** (Bybanen 1 and 2, light rail). Screening said "none" and that held: 3,615 became 3,597 because the shared filter now also excludes catering, and 34 stop places are 33 stations by name |
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

## 🔵 Band B — passed: narrower pages (8 cities; reopened 2026-09-28)

**Reopened by the owner 2026-09-28** for the cities that passed the Band C memo:
screening is complete, and the page will be narrower than the three-bucket
cities - one bucket, or all three with a measured gap - and says plainly what
is missing (Hong Kong's "mostly restaurants" and the Japanese cities' missing
retail are the precedent). **Band C closed the same day**, when its last five
got verdicts: Incheon and the Gyeonggi satellites to this band, Ottawa to T,
Palma and Baltimore to N. *(The letter's earlier band, geocoding at national
scale, closed 2026-09-24; this is a new condition under a free letter.)*

### ✅ Passed on the reduced-bucket bar (owner, 2026-09-29)

**The Band C audit's bar** (owner, 2026-09-29), drawn from the reduced-bucket
pages already built (Stockholm, Bucharest, London, Glasgow, Newcastle, Hong
Kong, Incheon):
1. **at least one full bucket at register quality** (amended 2026-09-29 from "food", owner, for Yokohama);
2. current under the one-clock rule;
3. a register of premises, not a curated guide, one sector or land use per
   property;
4. **size and in-ring share are disclosed on the page, never a gate** (owner:
   relaxed; Houston will map at about 7% in-ring);
5. about 70% or more placed (Incheon's 71.3%);
6. rail that passes (the light-rail test, not a stub).

The rows moved verbatim from Band C.

| City | Network | What is there | The gap | Notes |
|---|---|---|---|---|
| **Hiroshima** 🇯🇵 | **Not trams-contingent (measured 2026-09-29, MLIT N02 × N03)**: the Astram Line's 22 stations (an automated guideway, as Kobe's drawn Port Liner) and JR's 39 (Kabe 14, Sanyō 10, Geibi 14, Kure 1) inside the city, drawn under Japan's standing rule; Hiroden's streetcars besides | 7,479 + 5,195 restaurants on two lists, joined 96.0% / 95.0%; PDL 1.0 | **No personal-services list** (PDFs only); food retail only as MHLW's opt-in slice | A personal-services list, or the owner passing it as food only (B). Write-up below |
| **Kitchener–Waterloo (Regional)** 🇨🇦 | ION light rail, one line, **19 stops: Kitchener 11, Waterloo 8** (either city alone is a stub); every 10 min, 06:00–22:00 on weekdays; 99% mapped light rail. GTFS from the Region (GRT), Region of Waterloo Open Data Licence v2.0 (declared) | The Region's public-health inspection layers: food "General" **2,008** (2.0× OSM), personal services **about 636** (2.7×), points on 100%. Same licence, which requires the wording "Contains information provided by the Regional Municipality of Waterloo under licence" | **No retail**: grocery and convenience stores sit inside food with no field to split them. Neither city publishes a general licence register (all three hub catalogues enumerated) | A retail source, or the owner passing the gap (B). At build: filter by boundary polygon, not `SiteCity` (about 60 spellings); the personal-services layer holds home-based operators, so `check_personal_exposure.py` first |
| **Yokohama** 🇯🇵 | MLIT N02 (subway, JR and private railways) | Personal services, complete: **17,408 premises** (CC BY) | **No food list in any era**: a map without its ~29,000 restaurants would misread its stations (owner 2026-09-24) | The city publishing its food register, or MHLW's online system covering most permits. Write-up below **Passed to B 2026-09-29 (owner)** on the amended rule 1: the first page not built on food, stating that no food register is published. The block-level join's placement rate is still to measure **Measured 2026-09-29: the current register (2026-04-01, all 18 wards) holds 7,896 premises (beauty 5,091, barbers 1,512, cleaning 1,293), not the 17,408 recorded above**, whose source could not be traced. **Block-level join 97.8–98.7%, about 100% with town-chōme** (the shared japan_register join). Never load 申請者氏名 |
| **Ottawa** 🇨🇦 | O-Train Lines 1, 2 and 4: 25 stations (884 m), 19% in tunnel or on bridges; every 6–12 min (OC Transpo's GTFS, 2026-09-29) | Food-safety inspections: the one address-level commercial layer among 697 catalogue entries scanned 2026-09-21 (`docs/canada_retrospective.md`) | **Food only**: no retail or personal-services source | A second source, or the owner passing it as a one-bucket page (B) **Measured 2026-09-29: passed to B on the reduced-bucket bar.** Ottawa Public Health's inspection feed (`opendata.ottawa.ca/inspections/yelp_ottawa_healthscores_FoodSafety.zip`, feed date 2026-09-29): 12,961 businesses, **5,747 inspected since 2024-09-29**, about 7.2% of them institutional kitchens by name (schools, daycares, hospitals), so **~5,300 food premises**, 99.8% with coordinates. No type field: food shops (groceries, pharmacies) sit inside, to disclose as Kitchener–Waterloo's. The feed's licence is to read at build |
| **Palma** 🇪🇸 | Metro de Palma M1 (10 stations, all inside) and M2 (10 → 6); OSM tags both `light_rail` | The Consell de Mallorca's restaurant register: **4,375 food premises** (2.75× OSM), **13% with coordinates** | Food only, and an address join for 87% of rows, on a small metro (owner 2026-09-28) | **Reopened 2026-09-29 (owner)**: Glasgow's twin (4,375 food premises against Glasgow's 4,708; about 16 stations against 15), so it passes the reduced-bucket bar if an address join places about 70%: measure that first. Still no retail or personal-services source (none in the Balearic catalogue's 399 datasets; `smartoffice.palma.es` refused connections) **Measured 2026-09-29: passed to B.** 4,372 active (`Estat = Alta`), 581 (13.3%) with coordinates. The rest joined to Catastro's INSPIRE addresses for Palma (55,609 points; the licence to read at build): 61.0% of a 300-row sample on street + number after one normalisation pass (Catastro's type codes, Catalan particles), **66.2% placed overall; 73.4% with Incheon's nearest same-side number (within 6)**. 12.7% have no number (`S/N`). Never load `Explotador/s` (can name a person) |
| **Minneapolis** 🇺🇸 | METRO Blue and Green: 38 stations (659 m), 15% in tunnel or on bridges; every 12–15 min (Metro Transit's GTFS, 2026-09-29) | Food inspections (CC0 waiver, 47,959 violation rows 2023–26, lat/lon): restaurants, plus grocery as retail (owner 2026-09-28); an inspection table, so de-duplicate to premises | **No personal-services source and no licence register** | A personal-services source, or the owner passing the gap (B); the stub test to measure **Measured 2026-09-29: the data passes; the rail is the owner's call.** 2,916 facilities inspected 2023–26 (100% with coordinates): restaurants 1,544 (1,537 inspected in the last two years), caterers 36, grocery 448 and meat markets 90 as retail; institutions, food trucks and food shelves out. **Stub test (OSM)**: 19 stations inside the city; Blue keeps 12 of 20 (60%), **Green 10 of 24 (42%)**, its other half in St. Paul. The 38 recorded earlier was a bounding-box count. Toulouse's T1 (52%) is the lowest worst line built on a city-only scope **Passed to B 2026-09-29 (owner)**: the city-only scope, 19 stations, with the Green line's 42% accepted; St. Paul was re-checked the same day and has no register to widen it |
| **Pittsburgh** 🇺🇸 | The T, 3 lines, with a downtown subway: 30% in tunnel or on bridges; Red every 20 min, Blue and Silver part-day (PRT's GTFS, 2026-09-29), disclosed under the light-rail test's rule; **stub test unmeasured** (much of the network is suburban) | Allegheny County's Geocoded Food Facilities (CC0, 32,245 county-wide; `municipal` = Pittsburgh wards; x/y): food, plus grocery and convenience stores as retail (New York's precedent, owner 2026-09-28); the file last modified 2025-08-27 | **No personal-services source**; the city's own licences are signs, amusements and peddlers (729 active) | A personal-services source, or the owner passing the gap (B) **Measured 2026-09-29: the data passes; the rail is the owner's call.** WPRDC's Geocoded Food Facilities (as of 2025, CC0): 11,197 in the city's wards; **3,217 with status 1 and no closing date** (restaurants 1,633, convenience and packaged-food shops 453 as retail), 98% with x/y. Status 7 (3,855 with no closing date) is undocumented and may add more: read the data dictionary at build. **Stub test (OSM)**: 20 stations inside; Blue 13 of 24 (54%), Red 15 of 31 (48%), **Silver 13 of 31 (42%)** **Passed to B 2026-09-29 (owner)**: 20 stations, the Silver line's 42% accepted |

### ✅ Passed (owner, 2026-09-27): build as one-bucket pages

**Stockholm and Bucharest passed the Band C memo**: a food-only page beside
the three-bucket cities, saying plainly what is missing (Hong Kong's "mostly
restaurants" and the Japanese cities' missing retail are the precedent). They
stay in this band, apart from the cities still waiting on a verdict. Both
have a metro, so the deferred trams decision does not touch them.
**Stockholm was built 2026-09-29** and its row moved to the Built table (the
screen's figures are in `docs/build_briefs/stockholm.md`).

**Bucharest was built 2026-09-29** and its row moved to the Built table (the
screen's figures are in `docs/build_briefs/bucharest.md`).

| City | Network | The one bucket | What travels with it to the build |
|---|---|---|---|

### ✅ Passed from the transit-gap re-screen (owner, 2026-09-28): London food only, Berlin without hairdressers and laundries

**London was ruled out 2026-09-21 as a country, before food-only pages
passed.** Re-screened on `docs/global_transit_gap.md`'s order; the trail is the
United Kingdom row in the shortlist's Tier 4. **Berlin was a discard on two
keyword searches**; enumerating its catalogue found its chamber of commerce's
register, and the trail is the shortlist's Germany row. **London was built 2026-09-28** and its row moved to the Built table (its screen's figures are in `docs/build_briefs/london.md`); **Berlin was built the same day** and its row moved the same way (`docs/build_briefs/berlin.md`); **Glasgow was built the same day too** and its row moved the same way (`docs/build_briefs/glasgow.md`).

| City | Network | The one bucket | What travels with it to the build |
|---|---|---|---|

### ✅ Scoped to one municipality: Melbourne and Sydney (owner, 2026-09-28)

**Australia left "Countries ruled out" the same day**: "licensing is not
municipal" was ASSERTED and wrong (councils register food premises; none
publishes the register). Melbourne passes on the City of Melbourne's own
census; Sydney's first pass found only liquor licences, and **the re-probe
the owner asked for (the same day) found the City of Sydney's
establishment layer**, filed under a title no keyword search reaches.
**Sydney and Melbourne were built 2026-09-28** and their rows moved to the
Built table (their screens' figures are in `docs/build_briefs/sydney.md` and
`docs/build_briefs/melbourne.md`).

| City | Network | What is there | The narrowing, measured |
|---|---|---|---|

### ✅ A measured gap, disclosed (owner, 2026-09-28)

| City | Network | What is there | The gap, measured |
|---|---|---|---|
| **Gyeonggi satellites** 🇰🇷 (**Namyangju built 2026-09-30**; **Goyang, Seongnam and Yongin built 2026-09-29** on SEMAS's register, **Suwon and Bucheon the same day**. Uijeongbu, Yongin, Gimpo named; Seongnam, Goyang, Suwon, Bucheon, Ansan, Namyangju have more stations) | Uijeongbu METRO (Line 1, U Line: 21); Yongin METRO (EverLine: 25); Gimpo EDGE (Goldline only: 9) | `data.gg.go.kr`, 14 province-wide permit types over 31 시군, licence "commercial use and changes permitted". Province: retail 58,005, food 147,615, personal 54,206 | **The café file has no name, location or status**; takeaway food (즉석판매) has no status column; restaurants have X/Y but no address (a boundary join places them). The download page's "purpose of use" is answered honestly at build (owner) **Verdict (owner 2026-09-27): hold until Daegu and Busan are built.** **Verdict (owner 2026-09-28): PASS, to this band**, the café file's gap disclosed; the hold for Daegu and Busan lapsed when both were built. Which satellites to build is the brief's question, those with the most stations first (Suwon, Seongnam, Goyang, Bucheon). **Namyangju, Ansan and Uijeongbu briefed 2026-09-29** (owner's scope): 17, 13 and 20 stations, 54.9%, 64.3% and 85.3% in a ring. **Anyang briefed the same day** on its ring share (owner): 7 stations, 64.2%. Hwaseong (3 drawn stations), Gimpo (edge) and the smaller 시군 left out. All four go in the Seoul Capital Area view only (owner). The row closes when the four are built |

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

### Bucharest's screen (history: built 2026-09-29, see the Built table)

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

### Stockholm in full (history: built 2026-09-29, see the Built table)

*Zurich's write-up, which shared this section, moved to Band T with Zurich on 2026-09-27 (owner's call), and with Band T to `docs/tram_city_list.md` on 2026-09-29.*

**Stockholm** 🇸🇪 — **upgraded from D-c on 2026-09-22.** Screening is
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

## 🟣 Band C — closer to a page (0 cities; closed 2026-09-29; retooled from N by the owner 2026-09-28)

▼ **Closed 2026-09-29 (owner).** The Band C audit passed Hiroshima, Kitchener–Waterloo, Baltimore, Yokohama, Ottawa, Palma, Minneapolis and Pittsburgh to B, and sent Singapore, Istanbul, Ankara, Perth and Ho Chi Minh City to the discards, each with its reopen condition. The letter is free for reuse; the write-ups below are history.

**Retooled by the owner 2026-09-28** from Band N ("no page for now"): the same
seven cities, placed higher because they are the likeliest to become
buildable when the named source changes. The letter C had closed earlier the
same day; its old meaning (one bucket, or a measured gap) now lives in B.

**Created by the owner 2026-09-28.** Screening is complete, and the owner has
decided a page is not worth building on what is published today. The row stays
so that a change in the source can reopen it; each says what would.


### ▲ Three from Band T — 2026-09-29 (owner's call): a bucket gap, measurements to come (Hiroshima and Kitchener–Waterloo passed to B the same day)

Four passed the light-rail test (the test and its measurements are in
[`docs/tram_city_list.md`](tram_city_list.md)) and one was never
trams-contingent, so each now waits on its bucket gap, the first blocker after
trams. **Unlike the rows above, none has had a verdict yet**: the owner's call
on each gap sends it to B (a narrower page) or keeps it here.

| City | Network | What is there | Why no page yet | What would change it |
|---|---|---|---|---|

▼ **Yokohama 🇯🇵 (history: passed to Band B 2026-09-29 on the amended rule 1). Joined 2026-09-24 from the open gap (owner's call): personal services only, and
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

### Singapore's screen (history: to the discards 2026-09-29, see DISCARDED)

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

### Hiroshima's screen (history: passed to Band B 2026-09-29 on the reduced-bucket bar, see Band B)

| | |
|---|---|
| **The one bucket (food)** | Two lists that split by filing channel: the city's counter applications (**7,479** restaurants) and MHLW's open data for online filings (**5,195**, 66% addressed), overlapping by 1.2% at block level. **10.7 restaurants per 1,000 residents** (9.2 placeable), beside Sendai's 9.5 |
| **Joined** | own list **96.0%**, MHLW **95.0%** block; MHLW's own coordinates median **35 m** |
| **Why one bucket** | **no personal-services list**: new openings are published as PDFs only. Food retail exists only as MHLW's partial, opt-in notifications |
| **Licences** | both **PERMITTED WITH CONDITIONS**: the city's list under PDL 1.0 (the dataset-level declaration accepted for the full-list file, owner 2026-09-24) and MHLW's PDL 1.0 |
| **Brief** | `docs/build_briefs/hiroshima.md` (4/4). Hiroden's streetcars sit beside the Astram Line and JR, both drawable without them (2026-09-29) |

## 🔴 Band D — blocked, but the owner can act alone (0 cities; retooled 2026-09-28)

▼ **Empty since 2026-09-28.** The owner worked through every city here the same
evening: Ho Chi Minh City's CAPTCHA was passed and it moved to C; Delhi's CAPTCHA
would not load and its licences carry no street address, so R; Lisbon's account
turned out to be for institutions only, so R with a drafted request. The band
stays for the next city the owner can unblock alone.

**Retooled by the owner 2026-09-28**, when the hard blocks moved to Band R: every
city left here is unblocked by something the owner can do from here, which the
row's last column names (pass a CAPTCHA in a browser, register a free account).
Requests and orders went to R the same day. Bucharest's browser fetch (Band B) is
the precedent for a CAPTCHA: the owner fetches, the project never replays a
session.

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

*Kaohsiung's full record while it sat in Band B: see [city_master_list_evidence.md#band-d-kaohsiung](city_master_list_evidence.md#band-d-kaohsiung).*

*Closed bands (formerly G, B, D-c and D-d), kept in full: see [city_master_list_evidence.md#closed-bands](city_master_list_evidence.md#closed-bands).*

## ⚫ Band R — restricted or request only (18 cities; created 2026-09-28)

**Created by the owner 2026-09-28** from Band D's hard blocks. The publisher
answers only inside its country (ten geo-blocks), or only to an identity this
project cannot hold (Daejeon's and Gwangju's residency and CAPTCHA wall). The
project uses no VPN, proxy or account, so none of these moves from here; each
row says what would. **Renamed "restricted or request only" the same day (owner)**: Kaohsiung, Tallinn and Sendai moved in from D, because waiting on a bureau's reply also takes the push past the block out of the owner's hands, and **every future request-only city goes here**.

| City | Screened and passed | What blocks it — MEASURED | The way through |
|---|---|---|---|
| **Warsaw** 🇵🇱 | ⚠️ **NOT screened behind the block — a weaker shape than Kaohsiung's (owner's call 2026-09-24).** Nothing behind the block has been read. The city's own catalogue is the one place a premises register could be; every reachable route is negative (the city's 21 datasets on `dane.gov.pl`; the map portal's layers, markets and café terraces only; CEIDG is company-level; the alcohol-sales-points lead was Gdańsk's) | 🚧 **Geo-blocked to Poland**: `api.um.warszawa.pl` / `dane.um.warszawa.pl` answer only from Poland (2 of 2 probes) and time out from Germany and the US, while `mapa.um.warszawa.pl` answers everywhere; the API is also key-gated. **Not routed around** | **A read from inside Poland first** (the catalogue listing — does a premises dataset exist?), and only then a request to the city for access. An owner action. Nothing sent |
| **Hyderabad** 🇮🇳 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-24).** India's national catalogue was walked in full (288,011 titles: trade-licence counts, never premises); GHMC's archived URL names show trade-licence status and lookup forms, no bulk register named. Nothing behind the block has been read | 🚧 **Geo-blocked to India**: GHMC's own site answers 3 of 3 Globalping probes inside India (Mumbai, Bengaluru, Hyderabad) and returns 403 at its F5 edge to 9 of 9 from the US, Germany and Singapore, and from here; Telangana's portal (`data.telangana.gov.in`) the same. **Not routed around** | **A read from inside India first** (does GHMC publish a trade-licence register as a file?), then a request. An owner action. Nothing sent |
| **Helsinki** 🇫🇮 | ⚠️ **Reachable hosts all negative for retail and personal services** (2026-09-24): the city catalogue, enumerated through `data.europa.eu`'s copy (373 datasets, 6 Helsinki publishers, nonsense publisher 0); `kartta.hel.fi` WMS (485 layers) and WFS (terraces, parklets); HSY's WFS (397 layers, jobs grid only); `api.hel.fi` servicemap (public services, and its search is inert). Food exists in Oiva (national inspections, current) but only behind a search API, which is not used (above). The city's own food-control CSV is frozen at 2019 | 🚧 **Geo-blocked**: `hri.fi`, `avoindata.fi` and `avoindata.suomi.fi` answer 403 outside Finland and Germany. The bulk files behind them (the city catalogue; Valvira/LVV's alcohol-premises register, CC BY 4.0; any Oiva release) are unread | A read from inside Europe, by a person there (no proxy or VPN), of HRI's catalogue and of whether Oiva or the alcohol register is a bulk file. Then asking Ruokavirasto, the last resort |
| **Daejeon** 🇰🇷 | ⚠️ **NOT screened behind the block — Warsaw's shape (2026-09-27).** METRO: Line 1, 22 stations (the tram opens in 2028) | 🚫 **No city portal** (`data.daejeon.go.kr` fails DNS); the national register sits on data.go.kr behind the residency and CAPTCHA wall measured 2026-09-22 | A city-published register, or a national route without a CAPTCHA |
| **Gwangju** 🇰🇷 | ⚠️ **NOT screened behind the block — Warsaw's shape (2026-09-27).** METRO: Line 1, 20 stations (Line 2 under construction) | 🚫 **No city portal** (`data.gwangju.go.kr` fails DNS); the city's own open-data page points only to data.go.kr and the closed localdata.go.kr | As Daejeon |
| **Gimhae** 🇰🇷 | ⚠️ **NOT screened behind the block (2026-09-27).** EDGE, light rail only: the Busan–Gimhae LRT, 12 stations | 🚫 `data.gyeongnam.go.kr` and `www.gyeongnam.go.kr` both time out; no city portal found | A read from inside the country first. Its LRT also enters any Busan (Regional) scope |
| **Dubai** 🇦🇪 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** METRO: Red (two branches) and Green, 64 named stations in OSM, plus the tram. The 2026-09-21 record found the Department of Economy's licence register (`ded_license_master`, mainland Dubai without the free zones, an activity table beside it); whether its rows carry an address or coordinates, and its dataset licence, are unread. Dubai Municipality's building-entrance layer (`dm_dmgisnet_enterances-open`) could be the join file, on the same portal | 🚧 **Every host refuses this machine** (2026-09-28): `dubaipulse.gov.ae` times out on HTTPS and HTTP, `data.dubai` (the successor) returns a firewall "Request Rejected" on every path, `dubaidet.gov.ae` 403; the API wants a key (401). DMCC's free-zone directory forbids copying | A read from inside the UAE: the register's data dictionary and the open-data licence |
| **Bengaluru** 🇮🇳 | ⚠️ **NOT screened behind the block — Hyderabad's shape (owner's call 2026-09-28).** Namma Metro (kn) | 🚧 `bbmp.gov.in` and `site.bbmp.gov.in` time out at 21 s; `opendata.bbmp.gov.in` fails at once (2026-09-28). India's national catalogue carries counts only | A read from inside India |
| **Bangkok** 🇹🇭 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** MRT, BTS, Airport Rail Link (kn). Reachable sources fail: the Revenue Department's Bangkok VAT-registrant file (63 MB, no activity code, no coordinates, individuals' names at home addresses) and TAT's curated tourism restaurant list | 🚧 **The BMA's own portal refuses this machine**: `data.bangkok.go.th` (CKAN) resets TCP on HTTP and HTTPS; `bmagis` resets; `www`/`webportal.bangkok.go.th` serve a Cloudflare 403; `data.go.th` Cloudflare "Access Denied"; DBD (Incapsula 403) and the Thai FDA (403) likewise | A read of `data.bangkok.go.th`'s catalogue from an allowed network |
| **Riyadh** 🇸🇦 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** Riyadh Metro, 6 lines (kn). The reachable RCRC portal (35 datasets) has 2,658 retail-only points, 826 of them "extracted from Google Maps" | 🚧 **The national portal times out from here** (`open.data.gov.sa`, `od.data.gov.sa`, `data.gov.sa`, TCP connect 21–42 s), where the Ministry of Commerce and Riyadh Municipality publish; the municipality's geoportal times out; `rcrc.gov.sa` "Request Rejected" | A read of the national portal's commercial-licence datasets from an allowed network |
| **Tashkent** 🇺🇿 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** Tashkent Metro (kn) | 🚧 `data.egov.uz` refuses TCP 443 and 80 (other .uz hosts connect); `opendata.tashkent.uz` and `openmap.tashkent.uz` answer 403 "Your country is United States… not allowed"; the Statistics Committee's register redirects to the OneID login; `license.gov.uz`'s register API needs a Cloudflare Turnstile token; `soliq.uz` times out | A read from inside Uzbekistan |
| **Hanoi** 🇻🇳 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-28).** Hanoi Metro 2A and 3 (kn). The one reachable list is the city's opt-in "safe dining places" food list (no licence; its map served through a media contractor's key, not used) | 🚧 `hanoi.gov.vn` and `data.hanoi.gov.vn` time out (WebFetch ECONNREFUSED); `data.gov.vn` does not resolve; `dangkykinhdoanh.gov.vn` (a per-enterprise lookup) and `gdt.gov.vn` time out | A read from inside Vietnam |
| **Kaohsiung** 🇹🇼 | **72,550 storefronts** in the national tax register; OGDL v1 read and accepted (the same decision as Taiwan's other cities); the door-plate file exists in a **2026 edition** (`高雄市115年門牌坐標資料-TWD97`, updated 2026-06-25) with the same columns the three joined cities used (**92.7–95.5%**) | 🚧 **Geo-blocked to Taiwan**: `data.kcg.gov.tw` answers **HTTP 200 to 3 of 3 Taiwanese probes** (two networks) and times out from Japan and the US; `www.kcg.gov.tw` on the same network answers everywhere. The national catalogue lists **no other host** for any of 3,342 Kaohsiung datasets. **Not routed around** — no proxy, no VPN | **A request to 高雄市政府民政局** to publish the file on data.gov.tw or lift the filter for it — an owner action. Nothing sent |
| **Tallinn** 🇪🇪 | ⚠️ **A second layer is reachable, the first is not** (2026-09-24). Building-register use classes per building part come on a public WFS (`gsavalik.envir.ee`, `etak_ehr_hooned`; Maa- ja Ruumiamet, CC BY 4.0 equivalent): 2,077 commercial buildings; parts: food 1,496, retail 2,773 (0.79× OSM shops), personal services 342 plus 765 "other service". But these are registered use, not occupancy, with no names; 14% of lists are cut at 200 characters. It is not a premises register alone (Vienna's lesson). The city's GIS (1,173 layers) holds markets and malls only | 🚧 **Geo-blocked**: the food-handlers register `Toidukaitlejad.xml` (`avaandmed.agri.ee`, CC BY-SA 3.0) answers Estonia and Germany only. The public-view route is not used (above). The building register's full data needs an order carrying an e-mail (the owner's act, gated item 23). `www.tallinn.ee` is behind a Cloudflare challenge | A read of the food XML from inside the EU (no proxy or VPN), or the owner's EHR order. Then the Amsterdam shape: food register plus building-use layer, with a vacancy rate found and the trams-only call (5 lines; GTFS expired 2026-08-31, so OSM) |
| **Sendai** 🇯🇵 | ✅ **Screened and joined**: 12,627 permanent food premises, **95.1%** block, GSI check median 34 m; personal services 3,378 at 96.5% (`docs/build_briefs/sendai.md`, 4/4) | 🚫 **The city's permission**: its site terms default to 「無断で複製・転用することはできません」 and neither list page overrides it; the lists carry no per-file CC BY badge and are not in the city's 5,907-row open-data catalogue | **A written request to 健康福祉局生活衛生課**, drafted in formal Japanese for the owner to send (2026-09-24). Nothing sent yet |
| **Delhi** 🇮🇳 | ⚠️ **Partly screened (2026-09-28, owner's call).** Delhi Metro (kn). What is open is stale or partial: MCD's 2021-22 general trade licence list (366 KB XLSX, ~4,100 rows, former South DMC only, placed to colony, not street); NDMC's current health licences (453 in 2025, unit address, no trade type, central New Delhi only, mostly food). No reachable address or coordinate layer (NDMC's gate points carry no address) | 🚧 **The current register is behind a CAPTCHA**: MCD's `gtlLicenseDetail` / `htlLicenseDetail` (trade × 12 zones × year, Excel export) and FSSAI FoSCoS both need an image CAPTCHA. **Every Delhi-government host times out** (delhi.gov.in and its labour, food-safety, DES and health subdomains on one IP; `gsdl.org.in`; `edistrict`); Delhi Police licensing refuses HTTPS. Food moved to FSSAI in 2026 (MCD order) | A bulk export requested from MCD, or a read from inside India; then placement, which is unresolved ▼ **Owner's check 2026-09-28**: MCD's General Trade Licence search shows its columns without a query (Licensee, Application Number, Licence No, Establishment/Unit, Trade Description, Zone, Ward, Colony, Status, Submitted Date, Valid Upto): **no street address**, only zone/ward/colony; no "All" trade type; the CAPTCHA image does not load for the owner (likely restricted). MCD's site terms are a disclaimer only (no reuse clause; a GIGW copyright-policy page not yet found). Health Trade Licence columns unchecked (the screen reported an establishment address: the one food lead, by request to MCD). Moved to R (owner) |
| **Lisbon** 🇵🇹 | ⚠️ **The city side is negative on three methods** (2026-09-24): its catalogue as mirrored on `dados.gov.pt` (220 of 316 datasets link to its ArcGIS services, which answer); its ArcGIS services directory (102) and org (nonsense control 0); and the archive's index of the challenged CKAN (1,966 dataset names). What exists: kiosks (373, CC0), markets, the stale 2010 commercial census, and a 2020 COVID "Estamos Abertos" layer marked internal use | 🚫 **A free account**: DGAE's national *cadastro comercial* (`cadastro.dgae.gov.pt/api/estabelecimentos`) returns 401 logged out, and a CMS key in the app's JavaScript was NOT used. Row count, activity codes, coordinates and terms are all unmeasured | Register the account (the owner's act, `docs/gated_access.md` item 28), then measure. With activity codes, points and reusable terms, **Lisbon and Porto** both go to A. Without them, a discard ▼ **Owner's check 2026-09-28 — moved to R (request only)**: DGAE's public Mapa do Comércio, Serviços e Restauração shows, without login, each establishment's exploration type (Comércio / Serviços / Restauração), CAE, full address and coordinates (Lisbon-area clusters of ~6,700–11,000); no status field; sole traders under their own names. The export is account-only, and registration offers only Administração Pública Central, Município and Estrutura Associativa, so no individual account. Terms: a visitor privacy policy only (silent on reuse); not on dados.gov.pt. **The request to DGAE is drafted, not sent**: `docs/notifications/dgae-lisbon-porto-request.md`. Porto follows on the same answer |
| **Utrecht** 🇳🇱 (EDGE) | ⚠️ **Partly screened, from the tram list's T2 (owner, 2026-09-30).** Trams 20–22, 16 stops in the city (line 21 keeps 57%). What is reachable: the BAG's 3,461 shop units in use (1.73× OSM; Rotterdam's second layer), and a food layer rebuilt from Gemeenteblad notices, 822 premises (0.78× OSM) that cannot drop a closed business, since Utrecht's exploitation permits do not expire. An ArcGIS Online search (2026-09-30) found no Utrecht horeca layer | 🚧 **The city's portal refuses this machine**: `open.utrecht.nl` and `data.utrecht.nl` (its CKAN API included) answer nginx 403 to scripts, and the same 403 to a real browser (2026-09-30); `utrecht.dataplatform.nl` times out. Whether it answers from inside the Netherlands is untested | A read of the city's catalogue from an allowed network, for a current horeca register like Den Haag's or Amsterdam's |

## 🟤 Band T — contingent on trams (37 cities; on the tram list since 2026-09-29)

**Band T's cities live in their own file, [`docs/tram_city_list.md`](tram_city_list.md)**
(owner, 2026-09-29), sorted into tiers so they can be worked through apart
from the rest: **T1**, ready if trams-only maps are approved, and **T2**,
trams plus a bucket gap. They still count toward this file's candidate total,
and a city sits in ONE place across both files; `scripts/check_master_list_counts.py`
reads both and checks every count the tram list states.

**Ten left the band the same day (owner)**, on a three-part light-rail test
(track, frequency, spacing), calibrated on San Diego, Calgary and Edmonton,
which were built on light rail with no tram decision: five to Band A (all
three buckets) and five to Band C (a bucket gap), Hiroshima among them on a
different ground (its Astram Line and JR are drawable without trams). The test
and its measurements are in the tram list; street trams stay there.

**Every tram city's source was re-checked for currency the same day** (the
audit's Phase 2, the register's latest date rather than its description):
39 of 41 stand. **Santa Cruz–La Laguna moved to T2 as food only** (owner):
its retail and services directory failed, its food register is current,
and **Kansas City stays in T1 with its data date on the page** (owner):
its register froze on 2026-01-15, holding 2025's licences, Stockholm's
precedent.

**Created by the owner 2026-09-27** as "trams only", the same day the owner
ruled that trams count as rail for this project ("count trams"), and renamed
"Contingent on trams" the same evening. **The owner said yes to trams-only
maps on 2026-09-29**, after the audit (a preliminary yes for scoping came
first, the same day); T1 can now be briefed and built.

**T2 closed on 2026-09-30 (owner)**, each city read against Band B's
reduced-bucket bar:
- **Zurich and Göteborg** passed to T1.
- **Den Haag** went to T1 on a permit register the 2026-09-27 screen had
  missed. The city's own horeca permit layer gives it Rotterdam's shape.
- **Utrecht** went to Band R: its portal refuses this machine.
- **Santa Cruz–La Laguna, Rijswijk and Delft** went to the discards.

The measurements are in the tram list's T1 rows and in the rows here.


## DISCARDED — 100 cities, each naming its evidence

▼ **2026-09-30 — Santa Cruz–La Laguna, Rijswijk and Delft, from the tram list's T2** (owner's call, closing the tier): Santa Cruz–La Laguna's address join places 57.7%, under the reduced-bucket bar's 70%; Rijswijk and Delft have no food source, and the regional Den Haag scope they were kept for is no longer needed.

▼ **2026-09-29 — Baltimore, from Band B on currency** (owner's call: "dubious"): every row of its Restaurants layer carries a 2008 edit date, and the publisher says it has not been updated since 2022.

▼ **2026-09-29 — Band C's last five, closing the band** (owner's call): Singapore, Istanbul, Ankara, Perth and Ho Chi Minh City. The Band C audit passed eight cities to B on the reduced-bucket bar; these five fail it on what their publishers publish, so the band's condition (the likeliest to become buildable) described none of them. Each row keeps its reopen condition.

▼ **2026-09-28 — Mumbai, from the large-transit gap's re-screen** (owner's call). The city hosts were asked, as the gap file said; what answers is negative, and what times out (the state's Shops & Establishments system, MCGM's GIS servers) is application and planning systems rather than a register.

▼ **2026-09-28 — Munich, Frankfurt and Cologne, from the large-transit gap's German screen** (owner's call), each on a full enumeration of its catalogue and geoportal, and of its chamber of commerce. **Berlin left this table the same day for Band B** (owner): its chamber publishes a premises register (IHK Gewerbedaten) that the row's two keyword searches could not find.

▼ **2026-09-28 — Manila, from the large-transit gap's re-screen** (owner's call). Its old reason (the operator's feed types its lines as commuter rail) is obsolete, since OSM carries LRT-1, LRT-2 and MRT-3; the business side fails instead.

▼ **2026-09-28 — sixteen rows from wave 2's US screen** (owner's calls): Portland, Cleveland, Salt Lake City, Phoenix, Mesa, Honolulu, St. Paul, Oklahoma City and El Paso (no register); Atlanta (currency; its ground changed to terms 2026-09-29); Norfolk (a stream); Milwaukee, Detroit and Tampa (too thin, reversible); Cincinnati and Berkeley (rail). Tempe and St. Louis were not reached.

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
| **Algiers** 🇩🇿 | absence | read CNRC's Sidjilcom (a paid per-trader lookup, no bulk offer) · read ONS's register of natural-person businesses (2023-12-31: counts by wilaya × NAA section only) · read `wilaya-alger.dz`'s downloads (weapons forms) and `dcwalger.dz` (database error) · read the Ministry of Commerce's holiday duty rosters (personal names, no coordinates, no licence) | yes — `wilaya-alger.dz` and the Algiers Direction du Commerce | **No premises list at any level (2026-09-28).** First screened after the records' "no urban rail" misfiling was corrected (Algiers has a metro and a tramway). No `data.gov.dz` exists |
| **Doha** 🇶🇦 | absence | enumerated `www.data.gov.qa` (Opendatasoft, 1,889 datasets, 1,876 CC BY; none with geo features) · measured MOCI's active-certificate table (counts by municipality and activity: 121,409 in Doha) · enumerated GIS Qatar's public ArcGIS services (the Landmarks layer: 1,880 BUSINESS points nationwide, no licence, phone and email fields; QARS only as geocode locators) | yes — `www.data.gov.qa` and GIS Qatar | **No premises register (2026-09-28).** The commerce register is published only as counts; the one placeable layer is a curated gazetteer of about 800 relevant points nationwide, with no stated licence |
| **Baku** 🇦🇿 | absence | enumerated `opendata.az` (886 datasets; 20 terms searched; the Statistics Committee's 574 are counts and turnover) · read the Food Safety Agency's register page (food only, no coordinates, reCAPTCHA, "all rights reserved") · read the Baku City Executive Power's site (links only to opendata.az) | yes — `baku-ih.gov.az` | **No publishable premises list (2026-09-28).** The portal's "objects and places" layer is re-exported from OSM (a CC-BY label over ODbL data), and the metro-exit coordinates are stations only; the taxpayer search is a lookup |
| **Panama City** 🇵🇦 | absence | enumerated `datosabiertos.gob.pa` (5,753 packages, 114 orgs; MICI and MINSA hold 0 datasets) · read the Municipio de Panamá's 131 datasets (CC0, all aggregates) · search `datosabiertos.gob.pa` for aviso de operación, patente, restaurante, permiso sanitario, licores, barbería, lavandería | yes — the Municipio de Panamá's org on the national portal; `panamaemprende.gob.pa` timed out | **No premises list (2026-09-28).** The only business-name list is one bank's 723 card-terminal merchants, with province only |
| **Caracas** 🇻🇪 | absence | read `caracas.gob.ve` (site search and wp-json: nothing; no transparency page) · read INE (census tables and yearbooks only) · read Chacao's site (licence application guidance, no register) | yes — `caracas.gob.ve` and `chacao.gob.ve`; `datos.gob.ve`, SENIAT and `gobiernoenlinea.gob.ve` timed out; `sumat.gob.ve` and `datosabiertos.gob.ve` do not resolve | **No open-data portal and no premises list (2026-09-28).** Chacao's public map rates 1,549 buildings by inspection colour, not businesses; Sucre and Baruta not checked |
| **Mumbai** 🇮🇳 | absence | read `portal.mcgm.gov.in`'s licence pages (forms only) and its RTI proactive disclosures (nothing on licences) · enumerated MCGM's ArcGIS Online org (437 public items, 107 services; the one licence layer is 7,361 Section 394 trade licences, mostly hazardous goods and manufacturing, no licence text, personal names on 3,536 rows) · read FDA Maharashtra (counts only: 187,030 licences) and the state DES pages (no register) | yes — `portal.mcgm.gov.in` and MCGM's ArcGIS Online; MCGM's own GIS servers and `lms.mahaonline.gov.in` timed out from outside India and were left alone | **No storefront list on any reachable host (2026-09-28).** Health licences, trade licences and Shops & Establishments registrations exist only as application systems or counts; no eating-house list anywhere. The blocked hosts are the state's S&E application system and the Development Plan map servers, not a register |
| **Kolkata** 🇮🇳 | absence | read `www.kmcgov.in`'s Certificate of Enlistment pages (procedures, guidelines, forms, unit offices) · read its EODB dashboard (a services menu, no licence data) · read the homepage, departments page and site map (no open-data, GIS or 4(1)(b) link) | yes — `www.kmcgov.in`; `kmc.wb.gov.in` (KMC 2.0, the RTI portal) timed out and was left alone | **No published licence list (2026-09-28).** The only licence data is a per-certificate lookup ("View CE Information"), not queried |
| **Chennai** 🇮🇳 | absence | read `chennaicorporation.gov.in/gcc/`'s Trade Licence page (a status lookup, a login-only application, a fee PDF) · read its Profession Tax, Revenue Department and RTI pages (no list or counts) · read the Public Information Portal (projects, maps, architects; no business data) | yes — `chennaicorporation.gov.in`; `erp.chennaicorporation.gov.in` (the status lookup) timed out and was left alone | **No published licence list (2026-09-28).** Trade licences are a per-licence lookup; no state portal is linked |
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
| **Portland** 🇺🇸 | absence | enumerated the city's ArcGIS hub (354 items) · search (the only licence set is the defunct CivicApps one; Multnomah County's inspections are lookup-only) · measured Oregon's "Active Businesses - ALL" (`tckn-sxa6`, 561,388 principal places of business, no classification) | yes — its hub | **No classified premises register — 2026-09-28, wave 2; re-probed 2026-09-29, still negative.** The re-probe:<br>• **data.oregon.gov enumerated (537 datasets).** The only premises-shaped source is **OLCC's liquor licences** (`srxe-qkm2`, updated daily, no licence declared). It lists **~2,140** current alcohol-serving venues (full on-premises 1,540, limited on-premises 538, brewpubs 61) and **666** off-premises shops. Food venues without alcohol and non-alcohol retail are absent.<br>• **No personal-services register** anywhere: no salon or barber facility file on the state portal, the county's hub or Metro's.<br>• **The City's Buildings layer** carries a use class per building, not per premises: 874 Commercial Retail and 239 Commercial Restaurant among 249,102 buildings.<br>• `tckn-sxa6` is unchanged, with no classification. MAX and the Streetcar give 132 stops inside the city (MAX Blue keeps 22 of 47) |
| **Cleveland** 🇺🇸 | absence | enumerated the city's hub (188 items) · search (ArcGIS Online and the web) | yes — its hub | **No register — 2026-09-28, wave 2.** A METRO city (the Red Line) |
| **Salt Lake City** 🇺🇸 | absence | enumerated the city's hub (71 items; Utah's portal answers "decommissioned") · read slc.gov (monthly PDFs of new applicants only, "not provided in any other format") | yes — its hub and site | **No register — 2026-09-28, wave 2** |
| **Phoenix** 🇺🇸 | absence | enumerated the city's CKAN (145 packages) · search (ArcGIS Online) · read phoenix.gov (no general business licence, only sales-tax licences) | yes — its CKAN | **No register — 2026-09-28, wave 2** |
| **Mesa** 🇺🇸 | absence | enumerated the city's Socrata catalogue (304 datasets: monthly aggregate counts only) · search (ArcGIS Online) | yes — its catalogue | **No register — 2026-09-28, wave 2** |
| **Honolulu** 🇺🇸 | absence | enumerated `data.honolulu.gov` (72 datasets) · enumerated the city's hub (167 items) · read the state entity register (2022, mailing addresses only) | yes — both | **No premises register — 2026-09-28, wave 2.** Skyline is a METRO |
| **St. Paul** 🇺🇸 | absence | enumerated the city's hub (126 items: liquor licences only) · search (Socrata discovery and ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2; re-checked 2026-09-29 for a Minneapolis–St. Paul scope, still negative**: the city's Socrata portals are gone (404 on three domains), its one licence layer is 306 liquor licences, and no statewide or Ramsey County food list was found |
| **Oklahoma City** 🇺🇸 | absence | enumerated the city's hub (38 items: hotel-motel tax and TIF districts) · search (ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2.** The streetcar runs every 12–20 min, fare-free since 2026-08-07 |
| **El Paso** 🇺🇸 | absence | enumerated the city's hub (5 items; a 260-row corridor business survey with contact columns, not a register) · search (ArcGIS Online) | yes — its hub | **No register — 2026-09-28, wave 2.** The streetcar runs limited days and hours |
| **Atlanta** 🇺🇸 | terms | measured the Revenue Department's 2024 licences (`BusinessLicenses_2024_Revenue`, 19,297 rows, 14,591 for licence year 2024, NAICS, 99.3% inside the city limits, last edited 2024-08-15) · measured the 2019–22 layer (`GBL_WFL1`, 26,643 rows, last edited 2023-04-24) and the 2019–2023 yearly layers · read the item, service and metadata terms (all blank), the city's open-data hub (the item is not in its catalogue), Esri's terms (E204CW §2.4(c)) and O.C.G.A. § 48-13-15 | yes — the city's planning GIS account and its open-data hub | **Ruled out on terms, 2026-09-29 (owner's call); it was ruled out on currency on 2026-09-28, on the wrong layer.** The current layer is two years old and all three buckets are there (retail 2,944, food 2,141, personal 1,306), but it declares no licence, sits outside the city's open-data hub, and carries each business's reported revenue and employee count, which Georgia law makes confidential: an exposure, not a publication. **What would reopen it: a licensed City extract**, for example on the Atlanta Regional Commission's portal (unread), or the City on request, the last resort. A METRO city (MARTA, 23 of 38 stations inside) |
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
| **Fort Worth** 🇺🇸 | rail | measured the Certificates of Occupancy table (ArcGIS `CFW_Open_Data_Certificates_of_Occupancy_Table_view`, table 0: 72,065 rows, `JobUse` with 48 values) · search-level rail (TEXRail and the Trinity Railway Express; their GTFS not read) | yes | **The data is workable, the rail is not. Live-verified 2026-09-18.** The certificates run from about 2002 and are current through 2026. But 13,343 rows (about 19%) have no coordinates, the city and address fields are null on most rows, and a business that relocates appears more than once: it is a history of certificates, not a register. Revisit if the rail expands or a thin-network map becomes acceptable **Re-read 2026-09-30 (owner's wave-2 follow-up): the register is answered, the rail is not.** The Comptroller's permit file holds 22,352 outlets inside Fort Worth, about 11,800 of them storefronts once non-store retail and parking leave; its rail is still TEXRail and the TRE, commuter lines |
| **Austin** 🇺🇸 | rail | measured Capital Metro's GTFS (`r4v4-vz24`, data.texas.gov, 2026-08-26 to 2027-01-09): the Red Line (route 550, typed `route_type` 0) runs 1–2 trains an hour each way at its median stop, Wednesday 2026-10-07, 07–19h · measured the Comptroller's permit file (`jrea-zgmq`: 37,228 outlets inside Austin, about 12,700 storefronts once non-store retail and parking leave) · measured "Certificates Of Occupancy" (Socrata `f9mz-m6dy`, 291,759 rows: construction permits, no business name) | yes | **Rail fails — re-read 2026-09-30 (owner's wave-2 follow-up).** The register the 2026-09-18 row found missing exists in the Comptroller's file, so the ground moved from absence to rail: the Red Line is a converted freight railway, and the light-rail test gates converted railway at 15 minutes by day. **Reopens** with Project Connect's light rail |
| **Charlotte** 🇺🇸 | absence | read the city hub `data.charlottenc.gov` · read Mecklenburg County's GIS open-data page | yes | **No business or licence dataset. Live-verified 2026-09-18.** The city hub holds zoning, permit-review and planning layers, plus hand-curated point sets (grocery stores, pharmacies, medical facilities). The county page lists none. The rail is the LYNX Blue Line plus a streetcar (from memory, not checked) |
| **Denver** 🇺🇸 | measured | measured "Active Business Licenses" on the city's ArcGIS hub and on the Colorado Information Marketplace mirror (7 columns: `License_Num, License_Type, License_Sub_Type, License_Status, Entity_Name, Trade_Name, Expiration_Date`) · search the city's 347 catalogue datasets for an alternative | yes — the city's hub | **No address, no classification, no geometry — live-verified 2026-09-18** (`docs/decisions/2026-09-13.md`, "Ruled out Denver on live-verified data"). The "Business License Data Explorer" the first pass cited was Anaheim's. With San Jose, the case that made live verification a rule |
| **Singapore** 🇸🇬 | measured | measured NEA's Licensed Eating Establishments (36,687 rows, 2015-06-11 → **2016-09-06**) · measured the supermarket licences (478, 2016-06-26 only) · measured the current tobacco retailer (4,235, 2026-08-07) and pharmacy (243) lists | yes — data.gov.sg, the city-state's own catalogue | **Food register ten years stale — to the discards 2026-09-29 (owner), from Band C.** The current lists are one sector each, not a bucket. **Reopens** the moment NEA refreshes its eating-establishment register |
| **Istanbul** 🇹🇷 | absence | enumerated `data.ibb.gov.tr` (564 datasets, 557 public, titles, notes, tags and resources) · measured İBB's health-institutions dataset (5,806 pharmacies, 1,672 opticians, 1,208 medical-supply shops; frozen 2024-03, "subject to a fee and will not be updated") · search the central districts (Kadıköy counts only, Üsküdar 7 unrelated datasets; Beşiktaş, Şişli, Beyoğlu, Fatih and Bakırköy no open-data host) | yes — İBB's portal | **No premises register — to the discards 2026-09-29 (owner), from Band C.** Shops, restaurants and salons are licensed by the 39 districts. **Reopens** if a central district publishes its işyeri licence list in bulk, or İBB a premises-level register |
| **Ankara** 🇹🇷 | absence | enumerated ABB's Şeffaf Ankara portal (7,147 datasets) · read its POI layer (63,597 points: a curated restaurant guide of 1,013 and 225 butchers, no retail or salon category) · search Çankaya, Keçiören, Altındağ and Yenimahalle (application guides and lookup maps only) | yes — ABB's portal | **Istanbul's shape — to the discards 2026-09-29 (owner), from Band C.** **Reopens** if a central district publishes its işyeri licence list in bulk |
| **Perth** 🇦🇺 | absence | enumerated the City of Perth's ArcGIS org (370 items) · measured its Property Boundaries layer (`PRP_BND_PROPERTIES_PV`, 23,994 properties, 174 land uses: about 465 retail, 354 food, 17 personal services) · search WA's Land Use and Employment Survey (per LGA only) and liquor licences (a search form) | yes — the City's ArcGIS org | **Land use per property, not premises, on about 6 stations — to the discards 2026-09-29 (owner), from Band C.** **Reopens** with a per-establishment census like Sydney's or Melbourne's, or the LUES published per premises |
| **Ho Chi Minh City** 🇻🇳 | absence | enumerated the city portal's 112 datasets (behind a CAPTCHA the owner passed, 2026-09-28) · measured the Food Safety Department's certificate file (`DU DIEU KIEN DAT 2026.xlsx`, sha256 `1ef3a41d…`: 7,413 establishments certified 2026-01-05 to 2026-07-31, supervising-sector codes only) · read the enterprise register (685 MB, 2022-01, company-level) | yes — the city's portal | **Seven months of certificates, not the stock, with no placement route — to the discards 2026-09-29 (owner), from Band C.** 34% household businesses named for their owners; no open address layer. **Reopens** with the full certificate stock and a business-type field, a household-business register, or an open address layer |
| **Baltimore** 🇺🇸 | measured | enumerated Maryland's portal (1,531 items), the city's hub (693), iMAP (1,423) and 175 city map services: no premises register for retail or personal services (wave 2, 2026-09-28) · measured the city's Restaurants layer (ArcGIS `42f8856d647a41b89561e10fb60bc98a`, 1,327 rows, **`EDIT_DATE` 2008-06-22 on every row**; republished 2025-12-04; its own description: "has not been updated since 2022") · read the City Code's open-data ordinance (§ 9-8(b): permitted) | yes — the city's hub | **Currency — to the discards 2026-09-29 (owner), from Band B.** Read from its rows the list is 18 years old; at best (the publisher's note) 4, and it has no way to drop a closed restaurant. Passed to B the same day on the Band C audit's bar, which had not read the rows' dates. **Reopens** with a current food-licence or inspection register. Rail (SubwayLink 11, Light RailLink 16 inside) passes |
| **St. Louis** 🇺🇸 | measured | measured the Building Division's occupancy permits (`occupancy-permits.zip`, 1991 to date, daily; 10,635 applications 2021–2026, `CANCELDATE` for cancelled applications only, no closure of a business) · measured its Commercial Occupancy API (`stlcitypermits.com/API/Occupancy/GetCommercialOccupancyInspections`: a live queue of 60 pending applications; date filters ignored) · read the city's excise licences (2026-09-28: liquor only) | yes — `stlouis-mo.gov` | **A stream, not a register — to the discards 2026-09-30 (owner's wave-2 follow-up)**, Norfolk's precedent. Occupancy permits record a business arriving, never leaving, and do not expire, so the source cannot drop a closed business. **Reopens** with a business licence or inspection register |
| **Santa Cruz–La Laguna (Regional)** 🇪🇸 | measured | measured the Cabildo's hostelería register (`datos.tenerife.es`, CC BY declared, republished monthly, 2026-08-31: 3,658 restaurants in the two municipalities, addresses only, no row dates) · measured its join to Catastro's INSPIRE addresses for 38900 and 38023 (73,841 points, EPSG:32628): exact 1,756, nearest same-side number 356, **57.7% placed**; 753 rows (20.6%) carry no house number · measured the Cabildo's four retail and services layers (newest row 2023-11-13, median 2016-11) | yes — the Cabildo's portal and Santa Cruz's CKAN | **Placement fails — to the discards 2026-09-30 (owner), from the tram list's T2.** Under the reduced-bucket bar's 70%, and 79% at most even with every numbered row joined. Unmatched streets include names the city has since changed (General Franco), a sign the register's addresses are not revised. The tram passed (Metrotenerife L1 and L2, 25 stops, 509 m). **Reopens** if the Cabildo publishes coordinates, or a current register that has them |
| **Rijswijk** 🇳🇱 | absence | read `rijswijk.nl` (no open-data page: `/open-data` and `/opendata` 404; its search finds none) · search `data.overheid.nl` (4 datasets name Rijswijk, none published by the municipality) · search ArcGIS Online for its horeca and permit layers (one 2018 municipal-info layer) · measured the province's facility layers (`geoservices.zuid-holland.nl`, restaurants and cafés: OpenStreetMap re-processed by Kurtosis, not a register) | yes — `rijswijk.nl` | **No food source — to the discards 2026-09-30 (owner), from the tram list's T2.** Its only layer is the BAG's shop units, a use class per unit, which passes as Rotterdam's second layer but not alone (the reduced-bucket bar's rule 3). It was kept as an add-on to a Den Haag (Regional) scope, which Den Haag no longer needs: its own permit register covers the city alone. **Reopens** with a published horeca register |
| **Delft** 🇳🇱 | absence | enumerated the city's ArcGIS Online org `Delft_Open` (455 items, behind `data.delft.nl`): terrace maps, shopping areas and parking, no horeca or food register · measured the province's facility layers (OpenStreetMap re-processed, not a register) · search ArcGIS Online for its horeca and permit layers (none) | yes — `data.delft.nl` | **No food source — to the discards 2026-09-30 (owner), from the tram list's T2.** As Rijswijk: BAG shop units alone fail rule 3, and the Den Haag (Regional) scope it was kept for is no longer needed. **Reopens** with a published horeca register |

Plus the 2026-09-27 second-city screens' no-urban-rail set (Toulon; Nancy,
now a trolleybus; Metz, Nîmes, Amiens and Pau, bus rapid transit; Aalborg's
+BUS; Kristiansand's amusement-park tram; Carcassonne and Réunion's CIREST,
whose feeds flag school buses as tram), wave 2's (Limerick, Galway and
Waterford, one InterCity station each; Cuiabá, whose VLT never ran and is
being replaced by a BRT), and the earlier one (Winnipeg, Hamilton and Québec City
(re-checked 2026-09-27: both lines still under construction, Québec's to open
in 2033), Halifax,
Mississauga, ~30 single-feed countries) and access-not-data
(Russia, Ukraine; Iran and Belarus left out the same way 2026-09-28, owner,
for wartime concerns).

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
| 🇺🇸 United States | **12** | **6** — Dallas; Minneapolis, Pittsburgh; Kansas City, New Orleans, Tucson | A · B · T | **Dallas to A 2026-09-30** (owner) on the Comptroller's permit file; Fort Worth and Austin stay out on rail, St. Louis to the discards (a stream). **Buffalo, Sacramento and Houston built 2026-09-29.** **Light rail out of T 2026-09-29 (owner)**: Buffalo, Houston and Sacramento to A (Houston and Sacramento need an address join), Minneapolis and Pittsburgh to C (no personal services); Kansas City, New Orleans and Tucson stay on the tram list. Wave 2 (2026-09-28): Baltimore to C (food only); sixteen discards; Tempe and St. Louis not reached. **Queued**: a re-screen of Dallas, Fort Worth and Austin on the Texas Comptroller's permit file; Long Beach (for Los Angeles) and Arlington (for D.C.) as regional add-ons, each checked first |
| 🇨🇦 Canada | **5** | **2** — Ottawa, Kitchener–Waterloo | B | **Both light rail, out of T to C 2026-09-29 (owner)**, each on a bucket gap: Ottawa food only, **Kitchener–Waterloo (Regional)** food and personal, no retail. Vancouver's four SkyTrain suburbs are a rescope in PLAN, probes first. Brampton waits on the Hurontario LRT (revisit mid-2027; no opening date, construction to early 2028) |
| 🇲🇽 Mexico | **3** | **0** | — | Complete on the current screen: Monterrey (Regional) built 2026-09-27 and published with Daegu and Busan |
| 🇪🇸 Spain | **2** | **1** — Palma | B | **Santa Cruz–La Laguna to the discards 2026-09-30** (owner): its address join placed 57.7%. **Santa Cruz–La Laguna to T2 2026-09-29** (owner): food only on the Cabildo's current register; its retail and services directory (no update since 2023-11-13) is dropped. Wave 2 (2026-09-28): **Palma** to C (food only, 13% placed). Zaragoza discarded on placement; Alicante and Alcobendas not reached. Valencia, Bilbao, Málaga, Sevilla still measured out |
| 🇮🇪 Ireland | **1** | — | — | Complete: wave 2 (2026-09-27) found no second city. Dublin's map already covers all four Dublin councils; Cork, Limerick, Galway and Waterford have no urban rail. Re-screen Cork when Luas Cork opens |
| 🇮🇹 Italy | **2** | **1** — Florence | T | Milan and Rome, bespoke per city. Wave 2 (2026-09-28): **Florence** to T (the Comune's layers, coordinates on every row). Bologna discarded until its tram opens (spring 2027); Brescia, Catania and Cagliari not reached. Turin, Naples and Messina discarded |
| 🇫🇷 France | **5** | **21** | T | Every one trams-only; waits on the trams decision, on the tram list (T1). Lyon discarded |
| 🇨🇿 Czechia | **1** | **6** — Brno, Ostrava, Plzeň, Olomouc, Liberec, Most + Litvínov | T | Band T's decision; `czechia_register.ruian()`'s coordinate control is per city now |
| 🇩🇰 Denmark | **2** | **1** — Odense | T | **Aarhus built 2026-09-29** on Copenhagen's modules (to A the same day, light rail, owner), placed through OSM's DAR address points; Odense's tram on the tram list |
| 🇳🇴 Norway | **2** | — | — | **Bergen built 2026-09-29** on Oslo's modules (to A the same day, light rail, owner) |
| 🇱🇻 Latvia | **1** | **2** — Daugavpils, Liepāja | T | Band T's decision; VZD's address file needs its licence row |
| 🇳🇱 Netherlands | **2** | **2** — Den Haag, Utrecht | T · R | **T2's verdicts 2026-09-30 (owner)**: Den Haag to T1 on the city's own horeca permit layer (2,352 food premises) and the BAG, Rotterdam's shape; Utrecht to R (its portal answers 403 to this machine and a browser); Rijswijk and Delft to the discards (no food source) |
| 🇭🇰 Hong Kong | **1** | — | — | Built; the East Asia region |
| 🇰🇷 South Korea | **10** | **4** — Gyeonggi satellites; Daejeon, Gwangju, Gimhae | B · R | **Goyang, Seongnam and Yongin built 2026-09-29** on SEMAS's register, Incheon's module, **Suwon and Bucheon the same day**. **Daegu and Busan built 2026-09-27** on the shared Korean module; **Incheon built 2026-09-29** on SEMAS's national storefront register, which the Gyeonggi satellites also use (the LOCALDATA API needs a Korean identity check); the other three have no city portal |
| 🇹🇼 Taiwan | **3** | **1** — Kaohsiung | R | Its door-plate file is geo-blocked to Taiwan |
| 🇯🇵 Japan | **6** | **3** — Hiroshima; Yokohama; Sendai | B · R | **Kobe built 2026-09-27** on the shared Japanese steps, **Osaka the same day** on the `japan-city` skill, mostly as a config, **Sapporo 2026-09-28** likewise, **Fukuoka 2026-09-28**, the first on two food lists, and **Kyoto 2026-09-28** on a rebuilt register, and **Tokyo 2026-09-28**, the last, ward by ward. Hiroshima food only (C; its Astram Line and JR make it no longer a trams question, 2026-09-29), Yokohama personal services only, Sendai the city's permission |
| 🇧🇷 Brazil | **9** | — | — | Built 2026-09-24 as one batch. Wave 2 (2026-09-27) found no new city: six discards on frequency; **Contagem joins Belo Horizonte and Duque de Caxias joins Rio** as regional add-ons (owner; PLAN). Watch Salvador's VLT (trial running) and Teresina's 15-minute service |
| 🇸🇪 Sweden | **1** | **1** — Göteborg | T | **Stockholm built 2026-09-29** on its frozen food inspection register. **Göteborg to T1 2026-09-30** (owner): all active food businesses (2,167 food service, 906 food shops as retail), undated rows disclosed |
| 🇨🇭 Switzerland | — | **1** — Zurich | T | **Zurich to T1 2026-09-30** (owner): 2,325 food premises, plus 1,028 shops licensed to sell alcohol as a partial retail layer |
| 🇷🇴 Romania | **1** | — | — | **Bucharest built 2026-09-29**: DSVSA's food registers, fetched by the owner in their browser, placed by an OSM address join (74.9%) |
| 🇦🇷 Argentina | **1** | — | — | Buenos Aires built 2026-09-28: the city's land-use survey joined to its parcels (99.8%), CC BY 2.5 AR |
| 🇦🇺 Australia | **2** | — | — | Melbourne and Sydney each on its own council's establishment census, one LGA each (2026-09-28, owner); Sydney's found on a re-probe, and Sydney and Melbourne built 2026-09-28. Perth to N: property land-use codes only |
| 🇹🇷 Türkiye | — | — | — | Pharmacies and opticians only on İBB's portal (2026-09-28, owner); the districts, which license shops and restaurants, publish no lists |
| 🇹🇭 Thailand | — | **1** — Bangkok | R | The BMA's portal and GIS refuse this machine; national hosts too (2026-09-28, owner) |
| 🇸🇦 Saudi Arabia | — | **1** — Riyadh | R | The national open-data portal times out from here (2026-09-28, owner) |
| 🇶🇦 Qatar | — | — | — | Doha discarded 2026-09-28 (the commerce register is counts only) |
| 🇺🇿 Uzbekistan | — | **1** — Tashkent | R | Every host refuses this machine or needs a login or CAPTCHA (2026-09-28, owner) |
| 🇻🇳 Vietnam | — | **1** — Hanoi | R | Hanoi's hosts time out; HCMC's catalogue is CAPTCHA-walled (2026-09-28, owner) |
| 🇦🇿 Azerbaijan | — | — | — | Baku discarded 2026-09-28 (counts only; the food register is CAPTCHA-gated) |
| 🇵🇦 Panama | — | — | — | Panama City discarded 2026-09-28 (the municipality publishes aggregates only) |
| 🇻🇪 Venezuela | — | — | — | Caracas discarded 2026-09-28 (no open-data portal) |
| 🇦🇪 United Arab Emirates | — | **1** — Dubai | R | Every host of the licence register refuses this machine (2026-09-28); a read from inside the UAE first |
| 🇵🇭 Philippines | — | — | — | Manila discarded 2026-09-28 (no business list at any level) |
| 🇬🇧 United Kingdom | **3** | — | — | London built 2026-09-28, food only; Glasgow (FHIS) and Newcastle (Regional) built the same day. Food only on the FSA register (London re-screened 2026-09-28, Newcastle the same day, owner); the VOA list's terms bar publishing. Glasgow the same day (FHIS) |
| 🇸🇬 Singapore | — | — | — | Its food register is a 2016 snapshot; the owner's verdict is no page (2026-09-27) |
| 🇵🇱 Poland | — | **1** — Warsaw | R | Geo-blocked before measurement; a read from inside Poland first |
| 🇮🇳 India | — | **3** — Hyderabad, Delhi, Bengaluru | R | Hyderabad geo-blocked before measurement; Delhi's current register behind a CAPTCHA and its state hosts blocked (2026-09-28). Mumbai discarded 2026-09-28; Kochi discarded; Bengaluru's BBMP hosts time out (2026-09-28). Kolkata and Chennai discarded 2026-09-28 (per-licence lookups only) |
| 🇵🇹 Portugal | — | **1** — Lisbon | R | DGAE's register is public on its map (three buckets, address, coordinates), but bulk access is for institutions only; the request is drafted, not sent (2026-09-28). Porto would follow |
| 🇫🇮 Finland | — | **1** — Helsinki | R | Geo-blocked; a read from inside Europe |
| 🇪🇪 Estonia | — | **1** — Tallinn | R | Food register geo-blocked; the EHR order |
| 🇩🇪 Germany | **1** | — | — | Berlin built 2026-09-28 on IHK Berlin's per-premises register: shops, food and personal services without hairdressers and laundries. No second city: Munich, Frankfurt and Cologne discarded the same day (no premises register); Hamburg discarded on currency |
| 🇦🇹 Austria | — | — | — | Vienna discarded (no premises register at any level). **The Linz lead is closed (2026-09-27)**: its "Gewerbeberechtigungen" (CC BY 4.0, from the central trade register) is annual AGGREGATE counts by trade type, about 200 bytes a year, and ends in 2014. No premises and no addresses. A premises register for Linz is still unprobed on the city's own host |
| 🇪🇬 Egypt | — | — | — | Cairo discarded (no register at any level) |
| 🇨🇱 Chile | — | — | — | Santiago discarded (coverage fails downtown) |
| **Total** | **76** | **64** | | A 1 · B 8 · C 0 · D 0 · R 18 · T 37 (T on the tram list). Checked against the band tables by `scripts/check_master_list_counts.py` |

---

*The 2026-09-22 tier view, retained as evidence and not current (Tiers 1-6, the former Tier 5): see [city_master_list_evidence.md#tier-view-2026-09-22](city_master_list_evidence.md#tier-view-2026-09-22).*

## Countries ruled out

*▼ **2026-09-24 — eight countries left this list** with the discard audit:
Germany, Austria, the Netherlands, Greece, Portugal, Poland, Latvia and
Slovakia each rested on one national-level method, and their cities are in
the open gap (the Netherlands' Amsterdam now in Band A). A country is not ruled
out by its national portal's first page.*

🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)* · 🇨🇳 **China** *(accounts, terms and
mapping law; 2026-09-28, owner)*

*🇨🇳 **China joined this list on 2026-09-28** (owner), from a feasibility gate
rather than fourteen city screens. Shanghai's platform is behind an anti-bot
challenge; Beijing's and Shenzhen's downloads need real-name accounts, and
Shenzhen's terms forbid passing on any data. **Hangzhou is a narrow opening,
noted**: its food-business licence list (54,100 rows, premises addresses, no
coordinates) is keyless under terms that allow republishing, but the terms
oblige a filing (备案) that needs a real-name Zhejiang account, and no open
address or coordinate file exists to place it. **The legal barriers stay high
for any Chinese city**: publishing map data of China is regulated (map review,
GCJ-02 coordinates), and the geocoders' terms forbid this use.*

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

## Five rules this list is maintained by

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
1. **Access (D or R)**: can the data be reached at all?
2. **Trams (T)**: does the build need a yes on trams-only maps?
3. **Buckets (C)**: does it yield two or more, without a measured gap?

So:
- Tallinn sits in R, tagged "trams only".
- A trams-only city sits in T whatever its buckets, on the tram list
  (`docs/tram_city_list.md`), with any gap noted beside it: tier T2 holds
  Zurich, Göteborg, Utrecht and Den Haag, and Rijswijk and Delft as Den Haag
  add-ons.
- **Light rail is not a trams question** (owner, 2026-09-29): a city that
  passes the tram list's three-part light-rail test goes to the band of its
  next blocker, as Buffalo went to A and Ottawa to C.

A city is never listed in two bands. The same rule governs the Japan list
(`scripts/japan_ward_table.py`) and every chat republish.

**A source must be current: one clock for every kind of source (owner,
2026-09-29).** It replaces the same day's three clocks (five years for a
census, 18 months for a register), which were fitted to earlier calls rather
than derived; a register frozen at a date is a snapshot as of that date, just
as a census is.
1. **It must be able to drop closed businesses**: a complete snapshot (a
   census, a survey, a register kept up to its last update), a validity year,
   a closure field, or an expiry window. A source that only records openings
   fails at any age: Dallas's certificates of occupancy (issued on move-in,
   never withdrawn) and Santa Cruz–La Laguna's retail and services directory
   (rows aged in place, no closure field, median last update 2016-11).
2. **Its age is the date it last showed what was open, read in the rows**,
   never the catalogue's description or its re-stamp: Stockholm's layer read
   "daily" while frozen, and Tenerife's catalogue was re-stamped 2026-05-31
   with no row changed. For a validity-year source, the latest year held in
   full. Look for a newer layer from the same publisher before dating a
   city: Atlanta's 2019–22 layer hid its 2024 one.
3. **The ceiling is five years, and the date is on the page.** Five is what
   the site already publishes: Brazil's census and Barcelona's and Sydney's
   surveys are 2022 fieldwork, up for re-check in 2027. Density ages more
   slowly than any one pin, since a closed storefront often reopens as
   another business. Stockholm (2025-10), Kansas City (2025's licences) and
   Atlanta (2024's) pass; Hamburg's 2016 survey fails.

**A frozen part may sit beside a current whole**, its date on the page:
Tokyo's Koto, Chuo and Shinjuku lists end 2022-11 to 2023-01, with current
national filings layered on (owner's call at build). Published cities are
measured against this rule by a date check; none leaves the site on it
without the owner's call.

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
