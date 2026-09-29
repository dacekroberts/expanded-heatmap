# 🟤 Tram city list — 41 cities (split from the master list 2026-09-29)

**Band T of [`docs/city_master_list.md`](city_master_list.md), in a file of its
own** (owner, 2026-09-29), so the tram cities can be sorted and worked through
apart from the rest. They still count toward the master list's candidate
total, and a city sits in ONE place across the two files:
`scripts/check_master_list_counts.py` reads both.

**What goes here**: a city whose build waits on the owner's yes to trams-only
maps. Its rail is trams or streetcars with no metro, and it passes the rest of
screening, or passes with a bucket gap (T2). A city blocked on access first
stays in D or R (Tallinn); a city whose rail passes the light-rail test below
belongs in the master list's bands, not here.

**The owner's framing (2026-09-29): a preliminary yes, for scoping and
filtering this list only.** Nothing is built, and no city leaves for Band A or
B, until the owner's final call on trams-only maps. **Riga** (built
2026-09-24 on seven tram routes, stops thinned by a 0.5-mile spacing filter)
is the live precedent; Amsterdam (16 tram lines beside the metro), Rotterdam,
Oslo and Dublin (Luas) also draw trams.

| Tier | What these cities ARE | Cities |
|---|---|---|
| 🟤 **T1** | **Ready if trams-only maps are approved.** All three buckets, access open, rail measured; grouped by country pipeline, which is how the build cost falls | **35** |
| 🟤 **T2** | **Trams plus a bucket gap.** Two yeses needed: trams-only maps, and a verdict on the gap (the owner's Band B / C call) | **6** |
| **Total** | | **41** |

**EDGE** (light rail partly built to metro standard, the owner's tag
2026-09-27) is now a flag on a row, not a group: the rest of the EDGE group
passed the light-rail test and left for A and C on 2026-09-29. Nice and Rouen
(tunnels) keep it; Den Haag and Utrecht (RandstadRail, sneltram) keep it.

---

## The light-rail test — how a city leaves this list (owner, 2026-09-29)

San Diego, Calgary and Edmonton are built on light rail with no metro, and no
tram decision was ever made for them. So **light rail passes on precedent, and
only street trams wait on the trams decision.** A city is light rail when it
passes three parts, read against those three precedents rather than against a
fixed line:

1. **Track** — how much of the route is in tunnel or on bridges, and whether
   OSM maps the rest as `light_rail` or `tram` (mappers tag the kind of
   system, not where the track runs, so this cannot separate street-running
   light rail from reserved track; Houston's street-running line reads 94%
   light rail).
2. **Frequency** — every 15 minutes or better by day. **A gate only where the
   track is converted railway** (Aarhus's L1); **on purpose-built track a
   slower timetable is disclosed on the page, not disqualifying** (Buffalo's
   flat 20 minutes; owner, 2026-09-29).
3. **Spacing** — the median gap to the nearest stop in scope, about 550 m or
   more. **Supporting evidence, not the gate**: it moves with the scope (ION
   reads 558 m in Kitchener, 749 m in Waterloo), with how platforms are named
   (Ottawa read 10 m until platforms within 150 m were merged), and a street
   tram can clear it (Dublin's Luas, 575 m).

Measured 2026-09-29 (OSM route relations for track and spacing; each
operator's GTFS for frequency, worst daytime hour at the median stop):

| City | Tunnel or bridge | Mapped light rail / tram | Frequency, by day | Spacing | Verdict |
|---|---|---|---|---|---|
| *San Diego (precedent)* | 13% | 87% / 0% | — | 851 m | built |
| *Calgary (precedent)* | 13% | 87% / 0% | — | 1,020 m | built |
| *Edmonton (precedent)* | 23% | 72% / 5% | — | 631 m | built |
| *Riga (tram control)* | 2% | 0% / 98% | — | 360 m | built, trams |
| Buffalo | **80%** | 20% / 0% | 20 min, flat 06–23 | 609 m | light rail → A |
| Ottawa | 19% | 81% / 0% | 6–12 min | 884 m | light rail → C |
| Sacramento | 6% | 94% / 0% | unread (the feed host's certificate has expired) | 763 m | light rail → A |
| Minneapolis | 15% | 85% / 0% | 12–15 min | 659 m | light rail → C |
| Houston | 6% | 94% / 0% | 6–12 min | 651 m | light rail → A |
| Kitchener–Waterloo | 1% | 99% / 0% | 10 min (screen read) | 558–749 m | light rail → C |
| Aarhus | 3% | 97% / 0% | L2 15 min; **L1 30 min on converted railway** | 666 m | light rail on its new tramway → A |
| Bergen | **40%** | 58% / 3% | 7–8 min | 622 m | light rail → A |
| Pittsburgh | 30% | 70% / 0% | Red 20 min; Blue, Silver part-day | 437 m (suburban street stops in the box) | light rail (the Buffalo rule) → C |
| Santa Cruz–La Laguna | 4% | 0% / **96.5%** | L1 5–6 min, L2 10–12 (Metrotenerife) | 510–549 m | **tram — stays here** |

**Hiroshima left as well, on a different ground**: MLIT's N02 × N03 puts the
Astram Line (22 stations, an automated guideway like Kobe's drawn Port Liner)
and JR (39) inside the city, drawn under Japan's standing rule, so trams were
never its first blocker.

**Stop spacing of the cities that stay** (nearest-neighbour median, in scope;
the screens' OSM caches, 2026-09-29): Odense 440 m, Ostrava 430, Liberec 349,
Brno 337, Florence 322, Olomouc 309, Liepāja 309, Plzeň 306, Daugavpils 281,
Tucson 266, New Orleans 161. Riga 360 and Amsterdam 390 for comparison.

**Commuter rail checked, and none of it changes a tier** (the rail test,
`docs/commuter_rail_list.md`): Zurich's S-Bahn fails on coverage (row below);
Den Haag's NS Sprinters all stand within 178 m of a tram stop and RET metro E
keeps 4 of its 23 stops in the city (a stub); Utrecht's Sprinters are 2.2 km
apart; Brno's and Ostrava's trains 2.0 and 2.4 km; Göteborg has 4 train
stations in the city.

---

## 🟤 T1 — ready if trams-only maps are approved (35 cities)

**Every one passed all three buckets on a national or city register this
project has already built on** (the 2026-09-27 second-city screens and wave 2;
scratch in `second_cities/<country>/`), so each costs its rail leg, a scope
measurement and its licence reads. **Stores near stations** is storefronts
within 966 m of a station, the screen's measure. French builds use France's
own config (a 483 m outer ring, Lambert-93), so the build recounts.
**Build-time calls are listed per row** and put when each brief is written.

**🇫🇷 France (21)** — SIRENE through the built cities' step-2 chain, which
reproduced Rennes (3,479) and Toulouse (8,635) exactly as the control. Most
feeds are Licence Ouverte 2.0; Montpellier, Grenoble, Angers and Le Havre
ODbL. **Mode flags are unreliable** (Reims' feed types its tram as metro), so
the mode is decided per city. TER is excluded in every built French city.

| City | Network | Stations in the commune / total (worst line) | R / F / P (× OSM) | Stores near stations | Build-time calls |
|---|---|---|---|---|---|
| **Montpellier** | Tram 1–5 | 87 / 112 (line 2: 54%) | 2,484 / 2,622 / 1,193 (1.93×) | 6,179 | 54% matches Toulouse's T1 precedent |
| **Nice** (EDGE: L2 in a 6.4 km tunnel) | Tram L1–L3, plus a route "B" (Aéroport T2 – CADAM, 6 stations) not yet identified | 47 / 47 (every line whole) | 4,230 / 3,544 / 2,372 (2.85×; personal 6.4×) | **9,379** | Personal services lean on beauty (96.02B, 1,026 over 810 hairdressers): a composition and personal-exposure item |
| **Strasbourg** | Tram A–F (short Rotonde and Halles tunnels) | 66 / 94, plus 3 in Kehl, Germany (B: 52%) | 2,385 / 2,244 / 1,020 (2.11×) | 5,482 | Commune or regional |
| **Bordeaux** | Tram A–F | 53 / 135 (A: 35%) | 3,167 / 3,018 / 1,224 (1.84×) | 6,889; **10,754 over 14 communes** | **Regional scope** (Lille-style); TBM's Licence Ouverte **1.0** never read |
| **Nantes** | Tram 1–3 | 56 / 84 (line 3: 48%) | 2,105 / 1,844 / 852 (1.39×) | 4,341; 5,383 regional | Commune or regional (48% is just under Toulouse's line) |
| **Grenoble** | Tram A–E | 36 / 81 (C and D: 36%) | 1,541 / 1,601 / 598 (1.51×) | 3,716; 5,455 over 12 communes | **Regional scope** |
| **Rouen** (EDGE: the "métro", a light rail with a central tunnel) | 2 branches | 10 / 31 (32%) | 1,505 / 1,190 / 512 (1.73×) | 2,868; 3,634 over 5 communes | **Regional scope**; Astuce's own host timed out, so rail from the Normandie regional feed |
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
Prague. `czechia_register.ruian()`'s coordinate control is per city now.

| City | Rail (stations in the town) | Spacing | R / F / P; restaurants × OSM | Build-time calls |
|---|---|---|---|---|
| **Brno** | 11 lines, **146 stations**; line 2 keeps 21 of 23. IDS JMK GTFS, CC BY 4.0 | 337 m | 2,520 / 2,126 / 2,583 = **7,229**; 1.61× (Prague 1.59–1.63×) | The strongest trams-only find anywhere |
| **Ostrava** | 96 stations; **line 5 is a stub (10 → 3)**. No GTFS, rail from OSM | 430 m | 1,309 / 1,101 / 1,561 = 3,971; 2.23× | Line 5 |
| **Plzeň** | Lines 1, 2 and 4: 53 stations, all inside | 306 m | 1,225 / 863 / 1,425 = 3,513; 1.99× | PMDP's GTFS licence contradicts itself (CC BY against a CC0-like record): read it, or take OSM |
| **Olomouc** | Lines 1–7: 36 stations | 309 m | 811 / 620 / 815 = 2,246; 1.80× | DPMO's GTFS declares no licence: OSM, or a read |
| **Liberec** | 34 stations alone (line 11 keeps 21 → 15); 41 with Jablonec, every line whole. DPMLJ's GTFS resets the connection, so OSM | 349 m | 1,880 alone; **2,498 with Jablonec**; 2.45× | With Jablonec or without |
| **Most + Litvínov** | Joint scope 27 stations, every line whole. **Most alone fails the stub test** (lines keep 6 of 18, 9 of 21, 12 of 24) | — | 429 / 267 / 334 = 1,030; 3.71× | Joint scope is required; low value |

**🇩🇰 Denmark (1), 🇱🇻 Latvia (2)**

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Odense** 🇩🇰 | Letbane, one line, 24 stops in OSM against the operator's 26 (440 m); every 7.5 min | 1,629 / 649 / 612 = **2,890** | Placement through OSM's DAR address points (98.4%, the owner's call 2026-09-27) |
| **Daugavpils** 🇱🇻 | Routes 1–5, **38 stop names**, all inside (281 m); route 1 every 10 min, the others about hourly | Riga's two layers: food 98 (95.9% placed), shops and services 722 (100%); 81.5% within 483 m | Rail from OSM (the GTFS declares no licence); VZD's address file `aw_eka.csv` (CC BY 4.0) is a new source needing its own `data_sources.md` row |
| **Liepāja** 🇱🇻 | One line, **18 stop names** (309 m), about every 7 min | Food 131 (93.9%), shops and services 583 (100%); 69.7% within 483 m | As Daugavpils |

**🇺🇸 United States (3)** — Kansas City moved here from the discards on
2026-09-27 (owner: "Kansas City trams okay"); New Orleans and Tucson from wave
2's US screen (owner, 2026-09-28).

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Kansas City** 🇺🇸 | The KC Streetcar, **one line**. **Measured 2026-09-27 from OSM** (relations 7825409/7825410, Riverfront–UMKC with the Main Street extension): **18 stops, all inside Kansas City, Missouri**, about 9.6 km at a mean 0.56 km. It passes the stub test; OSM carries no colour. **Frequency read 2026-09-27 from RideKC's GTFS** (`gtfs_8_27_26.zip`, valid 2026-07-12 to 2026-10-03; route 601 "KC Streetcar", `route_type` 0; terms declared "free for anyone to use", not read): **every ~10 min all day, seven days a week**, 05:15 to past midnight | "KCMO Business License Holders" (Socrata `kkhs-93m4`): **15,895 rows**, geocoded, all three buckets in readable categories (Beauty Salons 662, Barber Shops 146, Clothing Retailers 192, Supermarkets 154); explicitly PUBLIC_DOMAIN | Pick a colour (OSM has none); `dba_name` is often a person ("HARRIS GREGORY J") - a privacy filter; `business_type` mixes fee codes ("Flat Rate 16", "Misc Rate 129") with activities |
| **New Orleans** 🇺🇸 | RTA streetcars 12, 47, 48 and 2: **110 unique stop names, all inside the city** (161 m, the densest on this list); no line cut. Frequency search-level only (~10 min, varies by line): read RTA's GTFS at build | "Active Occupational Licenses" (Socrata `iqay-p646`, **CC0**, 16,481 rows, updated 2026-09-26, points on 100%): **~2,411 / 1,934 / 1,057** (3.4× / 1.9× / 20× OSM) | A small text taxonomy (NAICS-style descriptions, no codes); drop "Special Events-Other (Vendor)" (1,258) and "Home Based-Office Use Only" (357); `ownername` - `check_personal_exposure.py`; thin 110 street stops (Philadelphia's and San Francisco's filter) |
| **Tucson** 🇺🇸 | Sun Link, **21 stops, all inside** (266 m); every 10 min on weekdays 07–18, 20 in evenings and at weekends | The city's BUSLIC layer (`gis.tucsonaz.gov`, 34,764 active of 93,483, updated 2026-09-22), NAICS, active and not home-based: **4,056 / 2,011 / 1,245** (2.7× / 2.2× / 6.3×), points; terms an "as is" disclaimer, no licence named | A licence read; about 6,250 active licences are individuals' (privacy check); `naics.py` fits unchanged; the daytime-only 10-minute service disclosed |

**🇮🇹 Italy (1), 🇪🇸 Spain (1)** — joined 2026-09-28 from wave 2's second
group (owner's calls). Both with coordinates on every row.

| City | Network | Business | Build-time calls |
|---|---|---|---|
| **Florence** 🇮🇹 | Tramvia T1 and T2: **39 stations inside the comune** (322 m); T1 keeps 22 of 26 (4 in Scandicci), T2 20 of 20. GEST's GTFS in the Regione Toscana feed, declared CC BY 4.0. T3 under construction (due end of 2026) | The Comune's layers on dati.toscana.it, declared CC BY 4.0: commercio in sede fissa, pubblici esercizi, attività estetiche, tintolavanderie. **7,355 / 3,024 / 1,673** (2.49× / 1.45× / 4.62× OSM) after dropping private clubs, internal shops, e-commerce, vending, farmers; **coordinates on 100%**, rows carry only an id and a type code (no names) | **639 food rows are exempt categories** (464 "non soggetta a requisiti comunali", 175 art. 53): Milan's *fuori piano* question (without them food is 2,385, 1.14×); Scandicci's 4 stops; a full licence read; 3,424 rows share a point |
| **Santa Cruz–La Laguna (Regional)** 🇪🇸 | Metrotenerife L1 and L2. **Either municipality alone is a stub** (Santa Cruz keeps L1 11/21, L2 1/6; La Laguna L1 10/21, L2 5/6); **together 21/21 and 6/6**. **96.5% of its track mapped as tram** (510–549 m); L1 every 5–6 min, L2 10–12 (Metrotenerife's timetable page, 2026-09-29) | The Cabildo de Tenerife's georeferenced layers (`datos.tenerife.es`, publisher L03380011), declared `cc-by`: **3,786 / 2,528 / 494** (3.1× / 2.6× / 4.0× OSM, which is thin on the island); **coordinates on 100%** | **Currency first**: the rows are a directory created about 2016, updated 2015–2022 (Dallas was discarded on a four-year-old snapshot). The Cabildo's hostelería register (updated 2026-08-31) is current but addresses only. A taxonomy on about 60 `actividad_tipo` strings; phone and e-mail columns never read |

---

## 🟤 T2 — trams plus a bucket gap (6 cities)

Each needs two yeses: trams-only maps, and a verdict on its gap. Zurich,
Göteborg, Utrecht and Den Haag moved in from Band C on 2026-09-27 (owner's
call), Rijswijk and Delft after them as Den Haag add-ons.

| City | Network | What is there | The gap, measured |
|---|---|---|---|
| **Zurich** 🇨🇭 | 18 tram refs, all coloured, plus the Forchbahn (S18); no metro. **The S-Bahn fails the rail test on coverage (2026-09-29)**: 23 stations in the city, 707 m apart, 6–28 trains an hour each way on the trunk (each line alone every 20–30 min), but 21 of 23 stand within 800 m of a tram stop and the other two (Affoltern, Leimbach) run every 20–30 min, Seoul's AREX case. Trams only; the S-Bahn is named on the page as excluded | `Gastwirtschaftsbetriebe`, 3,488 food premises, CC0 | **Food only**: no second register in 1,128 catalogue names; STATENT is aggregate |
| **Göteborg** 🇸🇪 | **Measured 2026-09-27 (OSM)**: 13 tram lines (1–13, Göteborgs Spårvägar), **127 distinct stops inside Göteborgs Stad**; lines 4 and 12 run on into Mölndal. Each line has its own OSM colour except 11 ("black"); the heritage Lisebergslinjen is out. No metro; 4 train stations in the city (1.3–1.8 km apart), not a network | `Livsmedelsverksamheter`, 5,063 active food businesses, CC0, daily | **Food only**: `handel`, `butik`, `företag` and `frisör` all return 0 on a filtering search |
| **Den Haag** 🇳🇱 (EDGE) | 14 HTM lines plus RandstadRail E: 172 stop places; worst line tram 1, 20 of 37 (a regional scope makes every line 94–100% whole). RET metro E keeps 4 of 23 stops in the city | BAG shop units 6,560 (1.75× OSM) | **No current food source**: the city's register froze at the end of 2020, and its Gemeenteblad carries 321 applications and no decisions |
| **Utrecht** 🇳🇱 (EDGE) | Trams 20–22: 16 stops (line 21 keeps 57%); 32 with Nieuwegein and IJsselstein | BAG shop units 3,461 (1.73×) | **Food partial**: rebuilt from Gemeenteblad notices, 822 premises (0.78× OSM), no expiry rule. **What would move it**: the owner accepting a disclosed partial food layer. `open.utrecht.nl` answered 403 and was left alone, so "no register" there is unmeasured |
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
| **Rail** | **Trams, no metro — measured 2026-09-27** (13 lines, 127 stops, OSM), and **no commuter network** (2026-09-29: 4 train stations in the city). *(This row read "INHERITED, not measured" until 2026-09-29.)* Better data on a weaker map — the trade Toronto lost on |

**Göteborg does NOT displace Stockholm, and now that is measured**: **5,063
against 8,146**. Its advantages are structural — businesses rather than
inspections (no dedupe), CC0 rather than SILENT — and they are real, but the
count settles the size question in Stockholm's favour.

#### Zurich in full

**▲ Zurich** 🇨🇭 — **moved out of the one-probe-each band on 2026-09-22, and
it is the same decision as Stockholm's.** It sat in the probe band while its
open item was described as "no second bucket found". That is now **measured
absent**, which is an answer rather than a question:

✅ **RAIL COUNTED 2026-09-23 — ZURICH HAS NO METRO, AND THAT IS NOT A BLOCKER.** Zero `route=subway` relations inside the Stadt boundary (OSM rel 1682248); its network is **42 tram relations across 18 refs, all named and ALL COLOURED**, plus **4 `light_rail`, ref S18** (the Forchbahn). ⚠️ **An earlier version of this row said Zurich therefore had "no drawable network at all". That was WRONG** — asserted from prose, corrected against the code. **`route_type 0` is DRAWN in at least seven built cities**: San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin. **Every tram EXCLUSION is a city that also has a metro**, where the trams are a dense street-running overlay. **Zurich has no metro for a tram to overlay, so its trams ARE the rapid-transit system**, and all 42 carrying a colour removes Milan's invented-palette objection. **The live question is the Muni Metro SPACING test** — are stops one or two blocks apart, needing `docs/sub_transit_line_filters.md`? **A cost, not a disqualification.**

**The S-Bahn, measured 2026-09-29** (OSM stations; transport.opendata.ch
stationboards, Tuesday 2026-10-06 at 07, 11, 18 and 21h): 23 stations in the
city at a 707 m median spacing. The trunk is metro-grade (Hauptbahnhof 18–22
S-trains an hour each way, Hardbrücke 10–20, Stadelhofen 8–22, Oerlikon
8–14), the branches are not (the Sihltal S4 and Uetliberg S10 every 20
minutes, Affoltern, Seebach and Wipkingen every 30). **It fails on coverage**:
21 of 23 stations stand within 800 m of one of 415 tram and Forchbahn stop
nodes, most at interchanges within 100 m. An S-Bahn-only Zurich would be about
8 stations; a map with both would add up to 16 line labels for about two
stations' worth of new rings.

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
city, exactly Stockholm's shape.**

---

## Revisit if trams-only maps are approved (discards, not candidates)

Discarded in `docs/city_master_list.md` on the owner's calls, and **not**
reopened by trams alone: each row names what actually blocks it. Kept here so
that a yes to trams-only maps sends someone to look (owner, 2026-09-29).

| Discarded city | Rail | Business | What actually blocks it |
|---|---|---|---|
| **Aubagne** 🇫🇷 | One tram line, 7 stations, 2.5 km | SIRENE, all three buckets, the French chain built | **Size**: 526 storefronts within 966 m, under a sixth of Rennes. The cheapest page here if "too thin" is relaxed |
| **Trondheim** 🇳🇴 | Tram line 9, 16 stations | Oslo's modules, all three buckets, 2,510 placed | **Reach**: 3.7% of storefronts within 483 m; 21.7% once the St. Olavs gate section returns — re-measure then |
| **Tampa** 🇺🇸 | TECO streetcar, 11 stations, every 15 min | Food only, addresses only, licence unread | Thin and unplaced |
| **Cincinnati** 🇺🇸 | Connector streetcar, every 20–25 min | Food only | Fails frequency; one bucket |
| **Detroit** 🇺🇸 | QLine streetcar every 15 min, **plus the People Mover** (an automated elevated loop, 13 stations, never counted; Kobe's Port Liner is the same kind of line, and it is drawn) | Food only (4,830 restaurants) | Thin, one bucket; with the People Mover it is a real downtown network |
| **Milwaukee** 🇺🇸 | The Hop, 13 stops | 1,702 restaurants, 1,072 food dealers (grocers: retail under New York's rule?) | Thin, one or two buckets |

Bologna (the Linea Rossa, spring 2027) and Brampton (the Hurontario LRT,
early 2028) wait on rail that has not opened, with revisit dates in their own
discard rows; neither is a trams question.

---

## Notes carried from the master list

**Denmark's placement (owner's call 2026-09-27): OSM's imported DAR address
points**, whose `osak:identifier` is the DAR Husnummer id (95% of central
Copenhagen's are in OSM, median 0.03 m from DAR's own point). They place 97.0%
of Aarhus rows and 98.4% of Odense's, keyless, under ODbL. The owner reopens the
Datafordeler account only if a build proves it needs one.

**Not candidates of their own**: every Dutch and Danish suburb on a built or
listed network (Zoetermeer, Leidschendam-Voorburg, Amstelveen, Nieuwegein,
Schiedam, Lyngby-Taarbæk) is a regional add-on, because each keeps only a stub
of its lines inside its own boundary.
