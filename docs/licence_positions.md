# Notice positions, weakest to strongest

The owner's question was: "we should list our weakest to strongest notice positions to know what could potentially be flagged."

This document ranks the legal position on which each source is republished. It covers every source the 144 landed cities rely on (the cities in `app/cities.py` on worktree-staging, merged with master, on 2026-10-02). Sources include business registers, transit feeds, rail data, address and parcel joins, geocoders, boundaries, naming layers, page-text statistics and the basemaps.

**How it was made.** Everything here comes from the project's own record: `docs/data_sources.md`, `docs/data_sources/*.md`, `docs/licenses/`, `docs/privacy_verdicts.md`, `DECISIONS.md` with `docs/decisions/` and `docs/decisions_drafts/`, the build briefs, and `app/components.py` with `app/pages/` for what actually renders. No publisher's page was re-read on the web (0 of the 10 permitted spot checks were used), nothing was downloaded, and no tracked file was edited. Four extraction passes, split by country group, are kept in full as Appendices A to D; each entry there carries the full field set (quote with doc:line, who and when, what would flag it, safety net, strengthen). The tables below are the merged ranking.

**Notice numbers removed (staging, 2026-10-02).** The research cited the
numbered notices of `docs/data_sources.md`, and `check_provenance.py` found 87
of those citations pointing at the wrong publisher. The numbers are stripped
rather than guessed; the authoritative list is data_sources.md's "Notices
this project MUST display when published".

This is a reading of the project's own documents, not legal advice.

**Tiers**
- **1 Weakest:** the permission rests on a reading of silent, ambiguous or contradicting terms, or nothing is recorded at all.
- **2 Conditional:** the permission depends on a state the project must keep, such as staying non-commercial, an indemnity accepted, no alteration, share-alike, a currency duty, a grant that ends on breach, a live account, or an act owed.
- **3 Explicit open licence:** read and recorded, with the notice displayed.
- **4 Public domain or no copyright:** nothing owed.

**Sub-ranks** run within a tier, weakest first: a, then b, then c.

**One rule underlies every entry: the removal commitment** (`docs/data_sources.md:254-323`). A publisher's request, a business owner's request or a privacy concern is honoured first and argued never. It is cited once here.

---

## Update, 2026-10-02 (evening): eight licence reads move nine sources

The owner asked for the zero-reading entries to be read ("run the licence
reads"). One `licence-read` agent per source read them the same day; the
verdicts and the owner's calls are in `docs/decisions_drafts/staging.md`.
**This section supersedes the tier tables and the 15 weakest below wherever
they disagree.**

| Source | Was | Now | Verdict, and the owner's call |
|---|---|---|---|
| D.C. Basic Business License (DLCP) | 1.4 | **3** | CC BY 4.0 on the item (`85bf98d3…`); the District's CC0 default yields to it. Credit DLCP, link the licence, say modified. |
| DC Boundary (OCTO) | 1.4 / 1.24 | **3** | CC BY 4.0 on the item (`7241f6d5…`). Credit OCTO (DC GIS), say reprojected. |
| NTA national GTFS (Dublin) | 1.3 | **3** | CC BY 4.0 with the NTA's prescribed sentence. **Owner: "plain CC BY"**: the developer portal's Fair Usage Policy (an uncapped indemnity) is not accepted; the credit still meets its §7. |
| geo.api.gouv.fr (26 French cities) | 1.25 | **3** | ODbL on the source dataset, Licence Ouverte on IGN's ADMIN EXPRESS; unanswered since 2025-10-15. **Owner: show both credits.** |
| MassGIS municipalities (Boston) | 1.24 | **4** | "may be freely redistributed"; public records. Credit requested, not required. |
| LA County Planning boundaries (Los Angeles) | 1.24 | **2** | eGIS Terms of Use grant copy and publish; breach-only indemnity; auto-termination on breach; no endorsement. |
| SanGIS municipal boundaries (San Diego) | 1.24 | **2** | SanGIS End User Agreement: credit PROHIBITED at this scale, an uncapped indemnity and a general release (Civil Code §1542 waiver), **accepted by the owner 2026-10-02 for both SanGIS layers** (the boundaries and the parcels, 2.32; `data_sources.md`). SANDAG, which only hosts it, adds "should not be redistributed", read as deferring to SanGIS's terms. |
| CARTO basemap (Overview macro map only) | 1.23 | **1, weaker** | The Terms (2026-09-29) grant free use only with the project's own API key; the macro map loads keyless vector tiles (keyless raster is already watermarked). A key brings an uncapped indemnity, New York law and revocation at will. **Open with the owner**: request a key, switch the macro map to OpenStreetMap tiles (staging's recommendation), or drop its basemap. City maps use OpenStreetMap's own tiles and are unaffected. |

**Rows and credits landed 2026-10-03 (lane-app):** D.C.'s register and
boundary, notice 137; Dublin's NTA GTFS, notice 138, the Fair Usage Policy's
indemnity recorded as not accepted; geo.api.gouv.fr, notice 139, both credits,
on all 26 French pages; MassGIS, notice 140, the credit in its FAQ's words.
LA County's and SanGIS's boundaries have licence rows and no credit (SanGIS
forbids one at this scale). Each licence row is in its country file under
`docs/data_sources/`; `united-states.md` now names SanGIS, not SANDAG, as the
boundaries' and parcels' publisher. SFMTA's 2.16 was settled the same day
(below).

**Counts after the update:** tier 1 **24**, tier 2 **50**, tier 3 **47**,
tier 4 **23** (144 entries; the 1.24 boundary group split into its four
sources).

**The 15 weakest after the update:** 1 Philadelphia · 2 King County food ·
3 **CARTO** (keyless, outside its terms) · 4 Snohomish food · 5 Bellevue ·
6 Daegu · 7 Den Haag · 8 Bucharest · 9 CNEFE · 10 Milan ATM · 11 Paris IDFM
(2a, elevated) · 12 Miami-Dade · 13 Tucson · 14 Stockholm · 15 Kitchener–Waterloo ("No License Provided"). D.C., NTA and
SanGIS (its indemnity accepted 2026-10-02) leave the list.

---

## The 15 weakest (as first ranked; superseded by the update above)

| # | Source (publisher) | Cities | Tier | Why it is weak |
|---|---|---|---|---|
| 1 | L&I Business Licenses, OPA parcels, City Limits (City of Philadelphia) | Philadelphia | 1a | The dataset page incorporates Terms of Use that prohibit "republication ... and any modification whatsoever ... without the prior written permission" (`docs/data_sources/united-states.md:511-516`). The written request sent 2026-09-21 is unanswered, including after the 2026-09-28 follow-up. |
| 2 | Food inspections r878-4sxa, Address Points, city polygons (Public Health - Seattle & King County) | Seattle (Regional) | 1a | The dataset is declared Public Domain, but the live kingcounty.gov terms "forbid publishing without written permission", and the Open Data terms that granted reuse survive only in an archive from 2023 (`docs/data_sources.md:2957-2961`). The owner chose "option 1" on 2026-10-01. The displayed notice says "Data provided by permission of King County", a permission no one gave in writing. |
| 3 | National GTFS: Luas and DART geometry (National Transport Authority) | Dublin | 1a | **No licence reading anywhere.** No credit is rendered in `_NOTICES` or on `app/pages/19_Dublin_Heatmap.py`. The source was switched in mid-build on 2026-09-22 (`docs/decisions/2026-09-20.md:10441-10451`). |
| 4 | Basic Business License, all three buckets (D.C. DLCP, formerly DCRA) | Washington D.C. | 1a | **No licence row or reading** for D.C.'s only register (`docs/data_sources/united-states.md:20`). The DC Boundary layer (`:173`) has no reading either. |
| 5 | Food Service Establishments (2025) (Snohomish County) | Seattle (Regional) | 1b | The terms are SILENT, and the site's "All rights reserved" was read as a web-page footer. The owner took a "permissive read" on 2026-10-02 (`docs/data_sources.md:2989-2992`). |
| 6 | Business Licenses (All) (City of Bellevue) | Seattle (Regional) | 1b | The portal terms allow "own personal, non-commercial use", with all other rights reserved. The owner read the data's own narrower field as governing ("option 1", 2026-10-01; `docs/data_sources.md:3002-3009`). |
| 7 | 인허가데이터 (Daegu Metropolitan City, D-데이터허브) | Daegu | 1a | Every licence field is null, and the City's own copyright guide asks for consultation before unmarked material is used. That consultation was never made (`docs/data_sources/south-korea.md:198-227`). |
| 8 | Horecavergunningen (Gemeente Den Haag) | Den Haag | 1a | The layer is "SILENT and ambiguous", the site terms name database rights, and it sits on an internal ArcGIS account. The owner relied on Amsterdam's precedent on 2026-09-30 (`docs/data_sources.md:2457-2461`). |
| 9 | Registered food units (DSVSA București) | Bucharest | 1b | There is no terms page at all, and "Toate drepturile rezervate" was read as website-only. The files sit behind a bot challenge and were fetched by hand (`docs/data_sources/romania.md:13`; `docs/data_sources.md:2118-2123`). |
| 10 | CNEFE 2022 (IBGE) | 9 Brazilian cities | 1b | No IBGE licence document exists. The project relies on Decree 8.777 art. 4, and four restrictive readings are "NOT resolved in this project's favor" (`docs/data_sources/brazil.md:72-104`). The reader's working was not kept. |
| 11 | ATM metro layers and gtfs.zip (Comune di Milano / ATM) | Milan | 1b | The "cc-by" declaration was "NOT read to this project's standard", and the promised read was never recorded (`docs/build_briefs/milan.md:382-394`). The rail is not credited. |
| 12 | Paris GTFS under Licence Mobilités (Île-de-France Mobilités) | Paris | **2a, elevated** | The grant ends "de plein droit, sans préavis" on breach (Art. 11.1). Its Art. 5.8 discharge is "a public repository ... linked from the site" (`docs/data_sources.md:1329-1331`), and **no repository link was found in `app/`**. If that holds, the lapse may already have happened, and silently. |
| 13 | Local Business Tax, boundaries, Miami-Dade Transit GTFS (Miami-Dade County) | Miami (Regional) | 1c | Nothing grants reuse and nothing forbids it. The record still says both "closed" and "open" (`docs/data_sources/united-states.md:316` vs `:563`), and the footer disclosure no longer names Miami. |
| 14 | BUSLIC layer 3 (City of Tucson) | Tucson | 1c | The terms are SILENT. The owner read reuse as permitted despite two sibling City disclaimers that say "for your personal use" (`docs/data_sources/united-states.md:232`). |
| 15 | Livsmedelstillsyn (Stockholms stad) | Stockholm | 1c | The item is silent, and a harvester labels it "Begränsad". The decision went for the publisher's feed (`docs/data_sources/sweden.md:27-31`). The walled record is still unread. |

Next in line: the Kitchener–Waterloo zips ("No License Provided"), SEMAS (10 Korean cities), Busan's 제14조, Hiroshima's full list, Amsterdam's horeca layer, Palma's Catastro join, and Dallas's address points (silent, with an indemnity on top).

---

## Count per tier

| Tier | Entries | Of which unrecorded (no licence reading) |
|---|---|---|
| 1 Weakest | 28 | 8 rows (D.C. register, NTA, four US boundary layers, geo.api.gouv.fr, CARTO, the boundary group and the minor borrowings) |
| 2 Conditional | 48 | none |
| 3 Explicit open, notice shown | 44 | none |
| 4 Public domain | 22 | none |
| **Total** | **142** | |

The 142 entries are grouped: one entry per shared source (for example, MHLW across 12 cities, SIRENE across 26), with its city list. OpenStreetMap is a single entry.

---

## Full ranked list

**Abbreviations.**
- **DS** = `docs/data_sources.md`. Country files are named by country (for example `united-states.md`); all are under `docs/data_sources/`.
- **COMP** = `app/components.py`.
- **DEC** = `DECISIONS.md`.
- **ARCH** = `docs/decisions/2026-09-20.md`.
- **DRAFT** = `docs/decisions_drafts/staging.md`.

**In the Safety net column**, "removal" means the removal commitment applies and nothing more specific does.

### Tier 1 - permission rests on a reading, or on nothing recorded

| # | Source | Cities | Rests on (doc:line) | Decided | What would flag it | Safety net | Strengthen |
|---|---|---|---|---|---|---|---|
| 1.1 | Philadelphia L&I licences, OPA parcels (internal), City Limits | Philadelphia | ToU "strictly prohibited without the prior written permission"; reasoned web-page reading (united-states.md:511-525) | owner 2026-09-21 (ARCH:17108) | the City, on its own incorporated terms | `_UNSETTLED_TERMS` footer (COMP:2243-2262) commits to coming down on a restrictive answer; no registrant-name columns | chase the 2026-09-21 request, or get the City's written permission |
| 1.2 | King County food r878-4sxa, Address Points, city polygons | Seattle (Regional) | "the live site-wide kingcounty.gov terms forbid publishing without written permission" (DS:2957-2961; united-states.md:304, :182) | owner 2026-10-01, option 1 (DRAFT:630-641) | King County, under its live terms; the notice's words "by permission" | notice (COMP:2188); no USPS ZIP fields | King County's written confirmation; until then, consider rewording "by permission" |
| 1.3 | NTA national GTFS (Luas, DART) | Dublin | nothing recorded (ireland.md:110-122) | build 2026-09-22; never read | NTA, on attribution or modification terms | none specific; the map-corner OSM credit does not cover NTA | licence-read now and add a notice, or fall back to the cached OSM geometry |
| 1.4 | D.C. Basic Business License (DLCP) and DC Boundary | Washington D.C. | nothing recorded (united-states.md:20, :173) | build 2026-09-21; never read | the District, on any terms the portal carries | removal; `_NON_AFFILIATION` | licence-read; add rows and any notice |
| 1.5 | Snohomish County Food Service Establishments (2025) | Seattle (Regional) | "SILENT, read permissively"; "All rights reserved" read as a footer (DS:2989-2992; DRAFT:186-200) | owner 2026-10-02 | Snohomish County, under its site-wide reservation | notice (COMP:2198) says the list is not current, complete or official | written confirmation, or a catalogued copy with a stated licence |
| 1.6 | Bellevue Business Licenses (All) | Seattle (Regional) | the portal allows "own personal, non-commercial use"; the owner reads the data field as governing (united-states.md:303) | owner 2026-10-01, option 1 | Bellevue, under its portal terms; any commercial turn | notice (COMP:2203); legal name and UBI never fetched | Bellevue's written confirmation |
| 1.7 | Daegu 인허가데이터 (D-데이터허브) | Daegu | every licence null; the guide's 사전에 협의 (south-korea.md:198-221) | owner 2026-09-27 (DEC:12396) | Daegu City's copyright officer | notice (COMP:1326); "If Daegu objects, the page comes down" | the phone consultation (an owner act), or a switch to SEMAS |
| 1.8 | Den Haag Horecavergunningen | Den Haag | "SILENT and ambiguous"; database rights on the site (DS:2457-2461) | owner 2026-09-30, call C1 | the Gemeente, on its database right; an internal account | notice (COMP:2022); applicant fields refused at fetch | written confirmation, or Rotterdam's Gemeenteblad method |
| 1.9 | DSVSA București food units | Bucharest | "a website footer ... not the data" (DS:2118-2123; romania.md:13) | owner 2026-09-28/29 | DSVSA or ANSVSA, under the footer; the hand-fetch behind a bot wall | notice (COMP:1938) says no licence is stated; sole traders shown by category only | written permission from DSVSA, or a data.gov.ro listing |
| 1.10 | IBGE CNEFE 2022 | São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza, Porto Alegre, Recife, Santos | Decree 8.777 art. 4; four readings unresolved (brazil.md:72-104) | owner 2026-09-23, "the Philadelphia shape" (ARCH:6469) | IBGE's dissemination policy; LGPD | notice (COMP:1213); dwelling rule | written confirmation from IBGE |
| 1.11 | Milan ATM rail layers and gtfs.zip | Milan | "recorded as CC-BY but has NOT been read" (build_briefs/milan.md:382-394) | build 2026-09-22; the read was never done | ATM or the Comune; no rail credit | notice credits the registers only (COMP:896) | licence-read, then add the rail to notice |
| 1.12 | Miami-Dade LBT, boundaries, GTFS | Miami (Regional) | "nothing grants and nothing forbids" (united-states.md:316) | build 2026-09-21 (ARCH:17184) | the County, on the absence of a grant | removal; OWNERNAME and MAIL* never fetched | one written line from the County; fix the "open" / "closed" contradiction |
| 1.13 | Tucson BUSLIC | Tucson | SILENT, read as permitted, over the "personal use" disclaimers (united-states.md:232; DS:2422-2433) | owner 2026-09-30 (DEC:1446) | the City, citing its sibling disclaimers | notice (COMP:2001) | written confirmation |
| 1.14 | Stockholm Livsmedelstillsyn | Stockholm | "The blank license is a silence, not a refusal" (sweden.md:27-31) | build 2026-09-22; owner wording 2026-09-29 | the City; dataportal.se's "Begränsad" | notice (COMP:1924) | read the walled record via the Internet Archive, or ask the City |
| 1.15 | Kitchener–Waterloo Inspections.zip and Inspections_PS.zip | Kitchener–Waterloo (Regional) | "No License Provided"; the portal's sentence read as covering them (DS:2237-2244) | owner 2026-09-30 (DEC:3960) | the Region, on Esri's "request permission" label | notice (COMP:680) | the Region's written confirmation |
| 1.16 | SEMAS 상가(상권)정보 | Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang, Daejeon, Gwangju | 제한 없음, with the site policy read as homepage-only; 소상공인365 notices unread (DS:2141-2151) | owner 2026-09-29 (DEC:6853) | SEMAS | notice (COMP:1955) | read the notices from a Korean vantage point, or get SEMAS's OK |
| 1.17 | Busan LocalDataService | Busan | 제14조 read as covering platform-authored works only (south-korea.md:171-193) | owner 2026-09-27 | Busan's portal, under 제14조② | notice (COMP:1343) | written OK, or a host that declares 제한 없음 |
| 1.18 | Hiroshima full permit list (DataEye 5672) | Hiroshima | owner reads the dataset's PDL as covering a file with no entry of its own (japan.md:146) | owner 2026-09-24 | Hiroshima City, under its website's default terms | notice (COMP:1553) | ask DataEye to list the file |
| 1.19 | Amsterdam Horeca exploitatievergunningen | Amsterdam | live "Licentie: -"; a retired 2022 catalogue said CC BY (DS:1546-1549) | owner 2026-09-24 | the Gemeente | notice (COMP:1177), displayed as CC BY | written confirmation |
| 1.20 | Catastro INSPIRE addresses | Palma | CC BY 4.0 declared over a still-linked 2016 licence that restricts (build_briefs/palma.md:97-104) | owner 2026-09-29, call C | Catastro, reading the 2016 PDF | notice (COMP:846) | Catastro's confirmation that CC BY supersedes |
| 1.21 | Dallas Address Points | Dallas | "nothing grants it and nothing forbids it", plus an uncapped indemnity (DS:458-467) | owner 2026-09-30 | the City, under the indemnity | prose rule "never surveyed or exact"; the optional credit is not shown | Census geocoder instead, or add the optional credit |
| 1.22 | Snohomish Building Address Points | Seattle (Regional) | the food layer's permissive reading extended "on firmer ground" (DEC:15766-15774) | owner 2026-10-02 | Snohomish County (unlikely; nothing displayed) | removal | none beyond 1.5 |
| 1.23 | CARTO keyless basemap (Overview macro map) | Overview page | **no row in DS.** The keyless CDN "that policy no longer documents" (ARCH:17474-17486) | owner accepted the residual 2026-09-20 | CARTO, on fair use or keyless access; withdrawal leaves the basemap blank | "© CARTO" caption (COMP:2313) | the free CARTO key (PLAN.md:852) and a DS row |
| 1.24 | DC Boundary; LA County Planning city boundaries; MassGIS municipalities; SANDAG boundaries (terms "not read") | Washington D.C., Los Angeles, Boston, San Diego | no rows (united-states.md:167, 171, 173, 315) | builds 2026-09-18 to 09-21 | the publisher (low; scope only) | removal | licence-read each; add rows |
| 1.25 | geo.api.gouv.fr commune and EPCI contours | all 26 French cities | no licence on any row (france.md:117-166) | builds 2026-09-22 to 10-01 | an audit (the publisher is unlikely to object) | not drawn | licence-read and add a row |
| 1.26 | Municipal boundaries with no row of their own: Madrid término, Milan ds2841, Dublin Tailte, Montréal limites, Vancouver, Surrey, Calgary, Edmonton, Toronto | those cities | each has the same publisher as a displayed notice (spain.md:182; canada.md:85-93; ireland.md:174) | builds 2026-09-21/22 | low | the publisher's notice already shown | add one row each |
| 1.27 | GeoSampa estações (status only) | São Paulo | "AVOIDED, not answered": a fact read, never drawn (brazil.md:147-184) | owner 2026-09-23 | Metrô, only if its geometry were reproduced | geometry is OSM's | none while it stays OSM |
| 1.28 | Minor unread borrowings: GVB map colours and the bbga/Locatus vacancy figure (Amsterdam); Tokyo statistical yearbook counts (Tokyo); e-Stat 衛生行政報告例 (Kumamoto, Hakodate); Chitetsu's English names (Toyama); MTR's "Hoi Wong Road" (Hong Kong); NAP metadata API (Paris, French batch); Monterrey's operator PDF; TfGM's map (Manchester) | as listed | no licence reading for any (Appendix C flags A2-A4; Appendix D flags A1-A4; Appendix B flag A) | builds | Locatus (a commercial vendor) is the only one with a motive | each is a fact, a figure or a colour, not a dataset | read or replace each one: the CBS figure for Amsterdam, project colours for GVB |

### Tier 2 - conditional on a state the project must keep

| # | Source | Cities | The condition (doc:line) | Decided | What would flag it | Safety net | Strengthen |
|---|---|---|---|---|---|---|---|
| 2.1 | IDFM GTFS, Licence Mobilités | Paris | ends without notice on breach; Art. 5.4, 5.7 and 5.8 duties (DS:288-297, 1299-1352) | owner 2026-09-22 | IDFM, or an automatic lapse; the L.1115-5 declaration is unresolved | notice (COMP:926); the snapshot date on the page; archive-not-delete | **link the repository from the site**; the NAP community upload |
| 2.2 | Cens de locals 2022 (Ajuntament de Barcelona) | Barcelona | "may not be altered" read narrowly; a notification owed and **never sent** (DS:333, 1142-1162) | owner 2026-09-22 | the Ajuntament | notice (COMP:822) | deliver the notification and record it |
| 2.3 | WMATA rail GTFS | Washington D.C. | the API agreement ends with the account (§9(i)); an accuracy clause (united-states.md:369-407) | owner 2026-09-21/22 | WMATA revoking the key; the public repo read as "sharing" | gate item; `_AS_RECORDED` | WMATA's written OK on the public outputs |
| 2.4 | FEHD via DATA.GOV.HK, and the CSDI points | Hong Kong | an uncapped, one-way indemnity, "directly or indirectly" (DS:335, 353-410) | owner 2026-09-22 and 09-24 | any third-party infringement claim | notice (COMP:1255); three conditions | none short of dropping the source |
| 2.5 | GOIB / Consell de Mallorca restaurant register | Palma | an uncapped indemnity, plus Barcelona's no-alteration reading (DS:437-448) | owner 2026-09-29 | GOIB or the Consell | notice (COMP:846) | send GOIB the courtesy note it urges |
| 2.6 | LA Metro rail GTFS | Los Angeles | no modification; terminable "for any reason" (united-states.md:343, 426-448) | owner 2026-09-21 | LA Metro, on modification or marks | notice (COMP:445) | Metro's clarification, or OSM rail |
| 2.7 | City of Seattle Business Locations | Seattle (Regional) | no commercial use (united-states.md:302) | owner 2026-10-01 | the City, on any monetization | notice (COMP:2206) | none while the site stays non-commercial |
| 2.8 | WA Liquor and Cannabis Board Off Premise list | Seattle (Regional) | RCW 42.56.070(8), non-commercial; the Board's accuracy note (DS:2971-2984) | owner 2026-10-02 | the Board | notice (COMP:2192) | re-check the Board's note at each refresh |
| 2.9 | Fukui City lists, CC BY-SA | Fukui | share-alike on the outputs; §4's open-ended prohibitions (japan.md:150) | owner 2026-10-01/02 | Fukui City; a reuser | notice (COMP:1632); LICENSE:62-71 | keep the LICENSE section and the notice together |
| 2.10 | MHLW 食品衛生申請等システム | Fukuoka, Tokyo (4 wards), Hiroshima, Matsuyama, Toyama, Kumamoto, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Kagoshima, Okayama | 免責 2) ウ OPEN; fine only while non-commercial (japan.md:128) | owner 2026-09-24 and 10-01 | MHLW, if the site turned commercial | "not complete" in each notice | MHLW's written answer |
| 2.11 | MLIT N03 行政区域 | all 20 Japanese cities | permitted only while never drawn, under the Survey Act (japan.md:127) | 2026-09-24 | GSI or MLIT, if an outline were drawn | the rule in `pipeline/countries/japan.py` | render the 出典 with its URL and licence link |
| 2.12 | Matsuyama and Sakai lists (弁償 clauses) | Matsuyama, Sakai | breach-triggered repayment of the city's costs; Sakai's monthly files rest on the owner's reading (japan.md:147, 154) | owner 2026-09-24 and 10-02 | either city, after a breach | notices | ask Sakai to catalogue its monthly files |
| 2.13 | Sacramento Business Operation Tax | Sacramento | an uncapped indemnity, "even if ... groundless" (DS:420-435) | owner 2026-09-29 | a claim the City passes on | owner, phone and mail fields never fetched | none |
| 2.14 | WPRDC Allegheny food facilities | Pittsburgh | CC0, but the Data Use Agreement adds an indemnity and a duty to report Non-Public Information (united-states.md:229) | owner 2026-09-30 (DEC:4374) | WPRDC | no person column | none |
| 2.15 | MTA NYCT subway and SIR GTFS | New York | "will not modify"; no accuracy claims (united-states.md:345-448) | build 2026-09-21; the row still says "open decision" | MTA | `_AS_RECORDED` | close the stale row |
| 2.16 | SFMTA Muni GTFS | San Francisco | a revocable licence; a §5 indemnity; clause 4's disclaimer goes in "any use agreement" (the site has none) or is displayed (united-states.md, the GTFS table) | licence check 2026-09-21; re-read 2026-10-03 | SFMTA | notice 3, verbatim: clause 12's two paragraphs and clause 4's disclaimer, displayed on the cautious reading (2026-10-03) | none needed |
| 2.17 | MTS Trolley GTFS | San Diego | marks "may not be used in association with GTFS Data", yet the official colours and names are used (united-states.md:611-617) | owner 2026-09-21 | MTS | `_NON_AFFILIATION` | the project's own palette for San Diego |
| 2.18 | OpenStreetMap: rail, boundaries, names, address points; OSM tiles on every city map | about 80 cities, all maps | ODbL §4.3 credit shown; §4.6 "provided the repo is LINKED from the site" (ARCH:8101-8105); the Tile Usage Policy is best-effort | owner and builds, from 2026-09-20 | OSMF, on share-alike for the committed station CSVs, or a tile block | map-corner credit; footer line (COMP:2310-2314); notice (COMP:750) | link the repository; add an ODbL notice to the station CSVs (brazil.md:177-179 says one exists; **none was found in `outputs/`**) |
| 2.19 | Chicago Business Licenses and boundary | Chicago | "terminate any and all display ... for any reason"; indemnity not recorded as accepted (united-states.md:297) | 2026-09-21 | the City | notice, verbatim (COMP:430) | record the indemnity acceptance |
| 2.20 | Tisséo GTFS (ODbL) | Toulouse | §4.4 open on the station CSV; §4.6 needs the repository link (DS:1361-1401) | 2026-09-23 / 09-29 | Tisséo, or an ODbL enforcer | notice (COMP:953) | an ODbL notice on the CSV; the repository link; the PLAN.md:159 check |
| 2.21 | STAR GTFS (ODbL) | Rennes | as 2.20 (DS:1403-1429) | 2026-09-23 | STAR | notice (COMP:972) | as 2.20 |
| 2.22 | Angers Loire Métropole GTFS (ODbL plus a marks bar) | Angers | held only while the page carries no mark (DS:2325-2347) | owner 2026-09-30 | the Métropole, on any brand surface | notice (COMP:1014) | the Métropole's consent; the repository link |
| 2.23 | CRTM M4/M10 layers | Madrid | "siempre actualizada": the date must be shown, re-render on edit (spain.md:115-153) | owner 2026-09-22 and 09-27 | CRTM, after an edit to the layers | notice, verbatim (COMP:519); max_age check | keep the max_age check green |
| 2.24 | STM métro geometry (CC BY 4.0) | Montréal | the portal requires a statement of modifications; **the notice omits it** (canada.md:118) | build 2026-09-21 | STM or the Ville | notice (COMP:586), incomplete | add the changes sentence and the licence link |
| 2.25 | TransLink SkyTrain GTFS | Vancouver (Regional) | "limited, revocable"; a duty to identify the user on request (canada.md:117) | 2026-09-21 | TransLink | notice, verbatim Legend (COMP:533) | none |
| 2.26 | Edmonton licences, ETS GTFS, boundary | Edmonton | cancellable "at any time"; a pass-through duty with no further restrictions (DS:879-897) | 2026-09-21 | the City | notice (COMP:657); LICENSE excludes outputs/ | none |
| 2.27 | KCMO Business License Holders | Kansas City | Public Domain by ordinance, but the portal's indemnity was read as binding nothing (DS:2403-2415) | owner 2026-09-30 | the City | notice (COMP:1989) | check for Finance-department terms before each republish |
| 2.28 | CTA GTFS | Chicago | purpose-limited grant (united-states.md:449-454) | owner 2026-09-21 | CTA | optional credit (COMP:452) | none |
| 2.29 | MBTA GTFS | Boston | revocable "at any time without notice" (united-states.md:346) | 2026-09-21 | MassDOT | notice (COMP:449) | none |
| 2.30 | SEPTA GTFS | Philadelphia | revocable; a fee is possible; indemnity not recorded as accepted (united-states.md:347) | 2026-09-21 | SEPTA | `_NON_AFFILIATION` | record the indemnity |
| 2.31 | San Diego Business Tax Certificates | San Diego | derivative work permitted; indemnity not recorded as accepted (united-states.md:236, 287-290) | 2026-09-21 | a claim passed on | privacy verdict | record the indemnity |
| 2.32 | SanGIS tax parcels (internal) | San Diego | no redistribution; a credit is PROHIBITED at this scale (united-states.md:245-270) | 2026-09-22 | a reviewer who **adds** a credit | nothing reaches outputs/ | none |
| 2.33 | LA County Assessor parcels (internal) | Los Angeles | voided automatically on violation (united-states.md:239) | 2026-09-22 | the County | three fields only | none |
| 2.34 | TaM, M réso / SMMAG, LiA GTFS (ODbL) | Montpellier, Grenoble, Le Havre | pure-extract station tables; §4.6 via the repository (DEC:6306-6370) | owner 2026-09-29 | each authority, on share-alike | notices (COMP:987-1002) | the repository link |
| 2.35 | SIRENE plus geolocation (INSEE, Licence Ouverte 2.0) | all 26 French cities | perpetual licence, with a **standing duty to honour the latest opt-out**; no refresh cadence (licenses/france-licence-ouverte-2.0.md:93-104) | 2026-09-23 | a person who opted out; INSEE | "Source : Insee" on every page (check M) | set a refresh cadence (needs the NAF 2025 mapping) |
| 2.36 | OGL - Vancouver: licences, parcels, tax report, local areas | Vancouver (Regional) | terminates automatically on breach (DS:766-776) | 2026-09-21 | the City, on the notice's wording | notice, verbatim (COMP:463) | keep the en dash and "Licence" |
| 2.37 | OGL - Surrey: directory, boundaries | Vancouver (Regional) | as 2.36 (DS:778-785) | 2026-09-21 | Surrey | notice (COMP:467) | none |
| 2.37a | OGL - Burnaby (the BC licence v2.0): Business Licences | Vancouver (Regional) | auto-termination; Personal Information exempt, read cautiously (canada.md, Burnaby rows) | 2026-10-03; the cautious reading owner 2026-10-03 | the City | notice 130, verbatim BC wording, credited "City of Burnaby" | keep the en dash and "Licence" |
| 2.37b | OGL - City of New Westminster v1.0: licences (residents), address points | Vancouver (Regional) | as 2.37a | 2026-10-03; the cautious reading owner 2026-10-03 | the City | notice 131, verbatim ("licenced", hyphen) | none |
| 2.37c | OGL - Coquitlam v1.0: business licences | Vancouver (Regional) | as 2.37a | 2026-10-03; the cautious reading owner 2026-10-03 | the City | notice 132, verbatim, with "© City of Coquitlam" | none |
| 2.38 | OGL - Calgary: licences, CTrain GTFS, boundary | Calgary | as 2.36 (DS:859-869) | 2026-09-21 | the City | notice (COMP:617) | none |
| 2.39 | OGL - Toronto: MLS, TTC GTFS, address repository, boundary | Toronto | datasets say "License not specified"; site OGL applies; auto-termination (canada.md:122) | 2026-09-21 | the City | notice (COMP:653) | none |
| 2.40 | OGL - British Columbia: ABMS naming layer | Vancouver (Regional) | auto-termination; API terms changeable (canada.md:110) | 2026-09-22 | the Province | notice (COMP:555) | none |
| 2.41 | FIA 營業(稅籍)登記 (OGDL v1) | Taichung, Taoyuan, Taipei (Regional) | without the 顯名聲明, "視為自始未取得" (never licensed) (taiwan.md:41-57) | owner 2026-09-23 | the FIA; a sole proprietor under the PDPA | notice (COMP:1362) | keep the statement exact |
| 2.42 | Door-plate files (four bureaus) | Taichung, Taoyuan, Taipei (Regional) | OGDL attribution reaches derivatives; Taoyuan's undefined "interests" FAQ (DS:1666-1671) | owner 2026-09-25 | any bureau, if the statement lapses; Taoyuan | notices | none, short of a written OK from Taoyuan |
| 2.43 | Taiwan MRT station tables | Taichung, Taoyuan, Taipei (Regional) | OGDL v1; Taipei Metro's liability declaration (DS:1679-1682) | owner 2026-09-25 | an operator | notices | none |
| 2.44 | Rio IPP / DATA.RIO MetrôRio layers | Rio de Janeiro | CC BY 4.0, plus SIURB's fault-based damages clause (brazil.md:125-145) | owner 2026-09-23 | IPP | notice (COMP:1227) | re-check for "sem alteração" before each republish |
| 2.45 | Tokyo catalogue wards (Chūō, Minato, Shinjuku, Kōtō, Taitō, Shibuya registers) | Tokyo | CC BY with a fault-based cost clause and a date-of-use element (japan.md:129) | owner 2026-09-24 | a ward or the Metropolitan Government | notice (COMP:1514) | none |
| 2.46 | Wards on their own terms (Taitō, Setagaya, Meguro) | Tokyo | cost clauses; Taitō's site policy bars copying, but its licence page names the list (japan.md:131-133) | owner 2026-09-24 | Taitō | notice | none |
| 2.47 | Shibuya food list | Tokyo | terms "may change without notice ... re-read them before each republish" (japan.md:130) | 2026-09-24 | Shibuya | notice | make the re-read a gate item |
| 2.48 | City lists, CC BY with a fault-based cost clause | Sapporo, Fukuoka, Toyama, Kumamoto, Nagasaki, Kitakyushu, Kagoshima | the country-wide acceptance (japan.md:144-175) | owner 2026-09-24 | a city, after a lapse or a currency claim | notices | none |

### Tier 3 - explicit open licence, read, notice displayed

| # | Source | Cities | Licence (doc:line) | Decided | Residual | Safety net |
|---|---|---|---|---|---|---|
| 3.1 | Ville de Montréal locaux-commerciaux and boundary | Montréal | CC BY 4.0; site "tous droits réservés" read as web-only (DS:812-857) | 2026-09-21 | no licence link | notice (COMP:578) |
| 3.2 | City of Sydney FES 2022 | Sydney | CC BY 4.0; website terms read as not incorporated (DS:2061-2064) | 2026-09-28 | the City's website terms | notice (COMP:1900) |
| 3.3 | Geostat Statistical Business Register | Tbilisi | "without restriction ... without prior permission" (georgia.md:60) | 2026-10-01/02 | Georgia's personal-data law is unread | notice (COMP:2212) |
| 3.4 | Tailte Éireann valuation register | Dublin | CC BY 4.0; three attribution strings, one chosen (DS:1186-1224) | 2026-09-22 | no licence link | notice (COMP:876) |
| 3.5 | Ayuntamiento de Madrid Censo de locales | Madrid | CC BY 4.0, plus conditions binding by use (spain.md:220-261) | 2026-09-22 | the update date must be kept current | notice (COMP:497) |
| 3.6 | INEGI DENUE | Mexico City, Guadalajara, Monterrey | Términos de Libre Uso §1(f)-(h) (DS:574-604) | 2026-09-22 | the notice must grow with each city | notice (COMP:731) |
| 3.7 | Comune di Milano six registers | Milan | CC BY 4.0 (DS:1240-1247) | 2026-09-22 | no licence link | notice (COMP:896) |
| 3.8 | Waterloo inspection layers and boundaries | Kitchener–Waterloo (Regional) | the Region's OGL (canada.md:109) | 2026-09-30 | the cited URL returns 404 | notice |
| 3.9 | Ottawa OPH feed and wards | Ottawa | OGL - Ottawa (canada.md:111) | 2026-09-29 | the feed is due to retire | notice (COMP:1973) |
| 3.10 | REM GTFS | Montréal | CC BY 4.0, bundled (canada.md:119) | 2026-09-27 | none | notice (COMP:598) |
| 3.11 | VBB GTFS | Berlin | CC BY 4.0 (DS:1882-1893) | 2026-09-28 | none | notice (COMP:1804) |
| 3.12 | Roma Capitale SUAP; ANNCSU | Rome | CC BY 4.0 (DS:1558-1574) | 2026-09-24 | none | notices (COMP:1191-1201) |
| 3.13 | Comune di Firenze layers | Florence | CC BY 4.0 (DS:2441-2451) | 2026-09-30 | none | notice (COMP:2009) |
| 3.14 | GCBA Usos del Suelo, Parcelas, Subte | Buenos Aires | CC BY 2.5 AR / 4.0 (DS:1957-1976) | 2026-09-28 | none | notice (COMP:1844) |
| 3.15 | City of Melbourne CLUE 2024 | Melbourne | CC BY 4.0 (DS:2073-2088) | 2026-09-28 | the page does not mention OSM | notice (COMP:1912) |
| 3.16 | FSA FHRS | London, Newcastle, Manchester, Birmingham, Sheffield, Nottingham, Blackpool | OGL v3; name and address treated as personal data (DS:1918-1922) | 2026-09-28; the UK six 2026-10-02 | sole traders | seven FSA notices |
| 3.17 | FSS FHIS | Glasgow, Edinburgh | OGL v3 (DS:1995-1999) | 2026-09-28; 2026-10-02 | home bakers | notices |
| 3.18 | OS Code-Point Open | eight UK cities | OGL v3; three statements (DS:1934-1951) | 2026-09-28 | the OS style guide was not read (owner: skip) | eight OS notices |
| 3.19 | DfT NaPTAN (gate 3 only) | six UK cities | OGL v3 (DS:2509-2524) | 2026-10-02 | none | notice (COMP:2057) |
| 3.20 | French LO 2.0 tram feeds, taken from the NAP's declaration | Le Mans, Besançon, Avignon, Tours, Dijon, Reims, Orléans, Mulhouse, Brest, Saint-Étienne, Nice, Strasbourg, Nantes, Valenciennes | "not read one by one" (build_briefs/le_mans.md:66) | 2026-09-30 | operator mark or colour claims; the credit is inside the provenance guard | page credits |
| 3.21 | Marseille Référentiel GTFS (Métropole AMP) | Marseille | LO 2.0 (licenses/france-licence-ouverte-2.0.md:162-167) | 2026-09-23 | the credit is inside the provenance guard | page credit |
| 3.22 | MEL WFS layers | Lille (Regional) | LO 2.0; the retrieval date stands in for the update date | 2026-09-23 | the date element | page caption |
| 3.23 | Atoumod Normandie aggregate | Caen, Rouen (Regional) | LO 2.0 (build_briefs/caen.md:76-99) | 2026-09-30 | the page shows the NAP window, not last_modified | page credits |
| 3.24 | TBM GTFS (Bordeaux Métropole) | Bordeaux (Regional) | LO 1.0 (DEC:6327) | 2026-09-29 | none | page credit |
| 3.25 | Entur GTFS (NLOD) | Oslo, Bergen | NLOD; Ruter's app agreement read as app-only (DS:1459-1477) | owner 2026-09-24 | Ruter | notice, with the logo |
| 3.26 | KORDIS IDS JMK GTFS | Brno | CC BY 4.0; the web footer's BY-NC-SA read as web-only (DS:2352-2357) | owner 2026-09-30 | KORDIS | notice |
| 3.27 | PMDP GTFS (gate 3 only) | Plzeň | the record contradicts itself, and both readings permit (DS:2366-2379) | 2026-09-30 | notice framing still awaits owner review | notice |
| 3.28 | Brønnøysundregistrene | Oslo, Bergen | NLOD (DS:1431-1444) | 2026-09-24 | sole traders | notice |
| 3.29 | Kartverket addresses and boundaries | Oslo, Bergen | CC BY 4.0 (DS:1446-1457) | 2026-09-24 | none | notice |
| 3.30 | CVR via Datafordeler | Copenhagen, Aarhus, Odense | CC BY 4.0; closing the account is safe (DS:336-338, 1479-1490) | owner 2026-09-24 | none | notice |
| 3.31 | DAR (Klimadatastyrelsen) | Copenhagen, Aarhus, Odense | CC BY 4.0 (DS:1492-1503) | 2026-09-24 | none | notice |
| 3.32 | ČSÚ RES | seven Czech cities | CC BY 4.0 (DS:1505-1517) | 2026-09-24 | natural persons | notice |
| 3.33 | ČÚZK RÚIAN | seven Czech cities | CC BY 4.0, "ČÚZK, [rok]" (DS:1519-1530) | 2026-09-24 | none | notice |
| 3.34 | ROPID PID GTFS | Prague | CC BY (DS:1532-1542) | 2026-09-24 | none | notice |
| 3.35 | VZD cadastre and address register | Riga, Liepāja, Daugavpils | CC BY 4.0 (DS:1624-1630) | 2026-09-24 and 09-30 | none | notice |
| 3.36 | GEO RIGA layers | Riga | CC BY 4.0 (DS:1632-1639) | 2026-09-24 | the outline must not be called the city boundary | notice |
| 3.37 | CBS Monitor Leegstand | Rotterdam, Den Haag | CC BY 4.0 (DS:1601-1611) | 2026-09-24 and 09-30 | none | notice |
| 3.38 | NYS Retail Food, Appearance Enhancement | New York, Buffalo | OPEN-NY: "you may use it as you wish" (united-states.md:296) | 2026-09-21 | a stop in writing on breach | name columns never selected |
| 3.39 | NYC DOHMH, DCWP, boroughs | New York | Local Law 11 (united-states.md:299; DS:539-553) | 2026-09-21 | DoITT's source, version and modifications | About and Excluded pages |
| 3.40 | MLIT 位置参照情報 | all 20 Japanese cities | PDL 1.0 (japan.md:125) | 2026-09-24 | **the level names are missing from the notice** | the 出典 line in each notice |
| 3.41 | MLIT N02 鉄道 | all 20 Japanese cities | PDL 1.0 (japan.md:126-127) | 2026-09-21 | URL and processor "Check at build", never closed | the credit in each notice |
| 3.42 | Seoul 인허가 (KOGL Type 1) | Seoul | KOGL 1 (south-korea.md:108-141) | 2026-09-22 to 09-25 | none | notice (COMP:1307) |
| 3.43 | City lists, CC BY with no cost clause | Osaka, Kyoto, Yokohama, Utsunomiya, Kōchi | japan.md:142-160 | 2026-09-24 to 10-02 | none | notices |
| 3.44 | City lists, CC BY 2.1 JP | Kobe, Hakodate | japan.md:143, 155 | 2026-09-24; 2026-10-02 | none | notices |

### Tier 4 - public domain or no copyright

| # | Source | Cities | Basis (doc:line) | Note |
|---|---|---|---|---|
| 4.1 | SF registered businesses, assessor rolls, county polygons | San Francisco | PDDL (united-states.md:225-238) | privacy only |
| 4.2 | LA Listing of Active Businesses | Los Angeles | CC0 (united-states.md:235) | privacy only |
| 4.3 | Boston food, licensing board, cannabis | Boston | PDDL (united-states.md:237) | none |
| 4.4 | Minneapolis food inspections | Minneapolis | CC0 (united-states.md:228) | none |
| 4.5 | New Orleans occupational licences | New Orleans | CC0, re-checked at each fetch (united-states.md:233) | none |
| 4.6 | Texas Comptroller sales-tax permits | Houston, Dallas | "public domain ... as permitted by law" (united-states.md:226) | re-read before each republish |
| 4.7 | Open Data Buffalo licences | Buffalo | public domain (united-states.md:301) | never call the pins official records |
| 4.8 | COHGIS Site Addresses | Houston | public domain, though sibling items say "All rights reserved" (united-states.md:227) | low |
| 4.9 | Census TIGERweb | ten US cities | federal work (united-states.md:300) | none |
| 4.10 | Census batch geocoder | Los Angeles, New York, Washington D.C., Sacramento, Houston, Dallas | federal work; **terms page not read** (united-states.md:313) | read it |
| 4.11 | 2022 NAICS titles | Kansas City | federal work | none |
| 4.12 | Wikidata (Dos Rios) | Sacramento | CC0 | none |
| 4.13 | Stadt Zürich Gastwirtschaftsbetriebe | Zurich | CC0; the Reglement was read only in summary (switzerland.md:39-52) | none |
| 4.14 | IHK Berlin Gewerbedaten; ALKIS | Berlin | CC0 / dl-de/zero (germany.md:16, 28) | none |
| 4.15 | Göteborg Livsmedelsverksamheter | Göteborg | CC0, on the distribution node only (sweden.md:33-40) | the fetch exits if CC0 is dropped |
| 4.16 | OVapi national GTFS | Amsterdam, Rotterdam | CC0 LICENSE.TXT (netherlands.md:24, 30) | no marks |
| 4.17 | ROS02 (DIA) | seven Czech cities | no copyright, no database right (build_briefs/prague.md:228-240) | natural persons |
| 4.18 | BAG verblijfsobjecten | Amsterdam, Rotterdam, Den Haag | Public Domain Mark (netherlands.md:14-18) | none |
| 4.19 | KOOP Gemeenteblad notices | Rotterdam | Auteurswet art. 11, CC0 (DS:1608) | none |
| 4.20 | VID excise register | Riga, Liepāja, Daugavpils | CC0 (DS:1638) | none |
| 4.21 | Rīgas satiksme GTFS | Riga | CC0 (latvia.md:26) | none |
| 4.22 | IPEDF ESTACOES_METRO (status only) | Brasília | public domain (brazil.md:32) | none |

---

## Flags

### A. Sources in use with no licence row (CLAUDE.md requires one)

1. **D.C. Basic Business License** (the whole D.C. register) and **DC Boundary**. Only endpoint rows exist (`united-states.md:20, :173`).
2. **NTA national GTFS (Dublin rail).** Nothing is recorded anywhere, and no credit is rendered. This is the most serious item.
3. **CARTO basemap** (the Overview macro map). The record has no row, and it relies on a keyless CDN that CARTO's policy "no longer documents" (`docs/decisions/2026-09-20.md:17474-17486`). The page shows "© CARTO".
4. **Boundary and naming layers with no row of their own:**
   - **United States:** LA County Planning boundaries (`united-states.md:167`); MassGIS municipalities for Boston (`:171`); SANDAG boundaries for San Diego, marked "Terms not read" (`:315`).
   - **France:** geo.api.gouv.fr contours and EPCI layers for all 26 French cities (`france.md:117-166`).
   - **Same publisher as an existing notice:** Madrid, Milan ds2841, Dublin, Montréal, Vancouver, Surrey, Calgary, Edmonton and Toronto.
5. **A row exists but no licence is recorded on it:**
   - The Census geocoder, "Terms page not read" (`united-states.md:313`).
   - The NAP metadata API that supplies Paris's notice-24 dates (`france.md:76`).
   - Milan's ATM rail layers, declared but never read.
6. **Facts, figures and names published from unread sources:**
   - Tokyo statistical yearbook counts (`app/pages/55_Tokyo_Heatmap.py:92-97`).
   - The e-Stat figure on Kumamoto's page (`164_Kumamoto_Heatmap.py:78`).
   - The bbga/Locatus vacancy figure for Amsterdam (`29_Amsterdam_Heatmap.py:103-105`).
   - Chitetsu's 23 English stop names for Toyama.
   - MTR's "Hoi Wong Road".
   - GVB's map colours.
   - Monterrey's operator PDF.
   - TfGM's network map for Manchester.

### B. Notices the docs require that the rendered pages may not display

These come from a read-only search of `app/components.py` `_NOTICES` and `app/pages/*`.

1. **The public repository is not linked from the site.** Searches of `app/` for `github`, `repositor` and `expanded-heatmap` found no link. Two families of licence rely on that link:
   - IDFM's Licence Mobilités Art. 5.8 (Paris). That grant ends by its own terms on breach.
   - ODbL §4.6 for Tisséo, STAR, TaM, M réso, LiA and Angers, and for OpenStreetMap-derived station files.

   The record makes the link a condition: "an unlinked repo is not an offer" (`docs/decisions/2026-09-20.md:8101-8105`; `DS:1329-1331, 1378-1381, 1417-1418`). Streamlit Community Cloud may show a GitHub icon in its toolbar for public apps, but this was not verified and the record does not claim it. **Verify on the live site, or add a link.**
2. **No ODbL notice on any committed station CSV.** The record says "the committed station file carries an ODbL notice" (`brazil.md:177-179`). A search of `outputs/` finds ODbL text only in five `provenance.json` files: Angers, Grenoble, Le Havre, Montpellier and Tbilisi. It is not in any `excluded_stations.csv`, which leaves the Toulouse and Rennes §4.4 question open (`DS:1394-1401, 1427-1429`).
3. **NTA (Dublin)** has no credit at all.
4. **Milan's rail** is not credited. Notice names only the registers (COMP:896).
5. **STM (notice, COMP:586)** lacks the statement of modifications or interpretations that the portal requires: "a bare credit does not satisfy it" (`canada.md:118`).
6. **SFMTA "Must also display liability disclaimers"** (`united-states.md:342`) is not rendered. The stored clause ties it to a "use agreement", so it may not apply, but the record says it is required. **Closed 2026-10-03:** displayed on the cautious reading, verbatim, in notice 3 with clause 12's second paragraph.
7. **MLIT, all 20 Japanese cities:**
   - The 位置参照情報 notice omits the level names 街区レベル and 大字・町丁目レベル that `japan.md:125` requires.
   - The N03 credit has no URL and no CC BY link (`japan.md:127`).
   - The N02 credit has no URL and no processor ("Check at build", never closed).
8. **Credits rendered only if `provenance.json` parses.** This affects every French operator credit, Paris's Art. 5.7 snapshot date and interval (the only city page with that duty), and Lille's MEL credit. The Insee line was moved out of that guard for exactly this reason; these were not.
9. **The last-update date under Licence Ouverte 2.0.** Caen and Rouen show the NAP window instead of the resource's `last_modified`, which the brief specified (`build_briefs/caen.md:76, 99`). Eleven other no-feed_info cities use the same substitute.
10. **The CC BY 4.0 licence link** is named but not linked in the Ville de Montréal, STM, Tailte and Milan notices. Confidence is lower here: those entries do not say a link is required.
11. **The OpenStreetMap rail-geometry notice (COMP:750-801) omits many OSM cities:**
    - Buenos Aires, Sydney, Melbourne and Tbilisi.
    - All nine UK cities, and Seattle.
    - Montpellier, Strasbourg, Le Havre, Caen and Rouen.
    - Stockholm and Bucharest.

    The map-corner credit and the footer's OSM line still cover attribution. Melbourne's page has no OSM mention at all.
12. **Disclosure consistency, not a missing notice.**
    - The footer's `_UNSETTLED_TERMS` (COMP:2243) says "One city rests on terms that are unresolved", meaning Philadelphia. The removal commitment says it "has exactly one live subject" (`DS:266`).
    - Since then, Seattle (Regional) has come to rest on two "option 1" readings and one SILENT reading, and Daegu, IBGE, Den Haag, Bucharest and Stockholm rest on owner readings too. Miami was dropped from the footer while its record still calls it open in two places.
    - King County's notice asserts "Data provided by permission of King County" on the strength of terms that survive only in an archive.

### C. Positions recorded as pending or "owed" that a landed city now relies on

1. **Philadelphia:** the request sent 2026-09-21 is unanswered, including after the 2026-09-28 follow-up. The next step is the owner's call (`docs/notifications/philadelphia-permission-request.md:3-6`).
2. **Barcelona:** the notification owed under the terms is "draft, NOT YET SENT" (`docs/notifications/barcelona-city-council.md:1`; `DS:333`).
3. **Milan:** the rail "read-licence job before the deploy gate" was never done (`build_briefs/milan.md:382-384`).
4. **Paris:**
   - The L.1115-5 declaration is "APPLICABILITY UNRESOLVED" (`docs/gated_access.md:47`).
   - The Art. 5.6(b) NAP upload was not made, because the owner declined the account (`DEC:6306-6309`).
5. **Toulouse and Rennes:** the ODbL §4.4 question on the station CSVs is OPEN. The PLAN.md:159 check on whether the mean-coordinate fallback fired is open too.
6. **SIRENE (26 cities):** the standing duty to honour opt-outs has no refresh cadence, and a refresh is blocked until NAF 2025 is mapped (`docs/recheck_calendar.md:55`).
7. **IBGE (9 cities):** four readings are unresolved. **SEMAS (10 cities):** the 소상공인365 notices are unread. **Daegu:** the consultation was never made.
8. **MHLW (12 cities):** 免責 2) ウ is "OPEN (minor)" and holds only while the site stays non-commercial. **MLIT N02:** "Check at build" is still open. **MLIT N03:** holds only while no outline is drawn.
9. **Stockholm:** the walled record is unread. **Amsterdam:** the bbga licence is unknown, and the API key becomes mandatory on an unset date. **Zurich:** the Reglement was read only in summary. **UK:** the OS style guide was skipped (owner).
10. **Indemnities read but never recorded as accepted:** San Diego's portal, Chicago, SEPTA and SFMTA §5 (the last only in the stored copy). Sacramento, Dallas, Pittsburgh, Hong Kong and Palma each have an acceptance entry.
11. **Other open items in the US record:**
    - MTA's row still reads "An open decision ... see PLAN.md", but PLAN.md has no such item.
    - Miami-Dade is recorded as both closed and open.
    - Agency branding (official colours and names, with MTS's flat bar) is recorded as an open question.
12. **Recurring acts the record owes:**
    - WMATA: re-confirm the account before each deploy.
    - KCMO: check for Finance-department terms before each republish.
    - Liquor Board: check its accuracy note at each refresh.
    - Shibuya: re-read the terms before each republish. No record of the latest re-read was found.
13. **Pending owner reviews:** Plzeň's notice framing (`DS:2376-2377`). Geostat's wording is approved (`DEC:15982`), but a comment still says "flagged for review" (COMP:2211).
14. **Stale pointers:** the twelve batch Japanese cities and the UK six cite `docs/decisions_drafts/japan-batch.md` and `uk-six.md`. Neither file is in the tree, and their entries are now in `DECISIONS.md`. Separately, the Japan batch notices say they "land with the Japan batch at review time", so those twelve cities assume the notices ship with their pages.

---

## Appendices: the field-by-field entries from the four extraction passes

Each appendix is one country group's extraction, kept as written. Their tiers match the merged ranking above, except for three things added in the merge:
- **D.C. register:** promoted to Tier 1.
- **CARTO and OpenStreetMap:** entries added.
- **Paris (IDFM):** elevated, because of the missing repository link.


---

## Appendix A - United States

## US - notice positions, weakest to strongest

Group: United States (19 landed cities). Sources: the project's own record only.
Abbreviations: US = docs/data_sources/united-states.md; DS = docs/data_sources.md;
DEC = DECISIONS.md; ARCH = docs/decisions/2026-09-20.md; DRAFT =
docs/decisions_drafts/staging.md; COMP = app/components.py.

OSM (handled centrally): rail from OSM in Buffalo, Sacramento, Houston,
Minneapolis, Pittsburgh, Dallas, Kansas City, Tucson, New Orleans, Seattle
(Regional) (COMP:767-776 names all but Seattle; Seattle's page caption says
"Rail: OpenStreetMap", app/pages/174_Seattle_Heatmap.py:54-55). Boundary from
OSM: Sacramento (US:178). One station coordinate from OSM via Nominatim:
Philadelphia's 11th St (US:27). Basemap: all 19.

---

### TIER 1 - permission rests on a reading

#### US-PHL-LI - L&I Business Licenses (City of Philadelphia, Carto)
- Cities: Philadelphia
- Role: register
- Tier: 1 (1a) - the incorporated Terms of Use, read literally, prohibit it; written request unanswered
- Rests on: "Distribution or republication in any other form ... and any modification whatsoever, are strictly prohibited without the prior written permission of the City" (US:511-516); reasoned reading only (US:517-525)
- Decided by / when: owner (2026-09-21): ask, stay up on the reasoned position (ARCH:17108; US:544-551)
- What would flag it: the City (maps@phila.gov / LIGISTEAM) on its own terms; the City's catalogue links straight to those terms (US:530-534)
- Safety net: footer disclosure _UNSETTLED_TERMS (COMP:2243-2262) with a commitment to come down on a restrictive answer; registrant-name columns never selected (US:25); privacy verdict publish (docs/privacy_verdicts.md:28)
- Strengthen: the City's written permission; chase the 2026-09-21 request (owner's call open, PLAN.md:837)

#### US-KC-FOOD - Food Establishment Inspection Data r878-4sxa, plus Address Points and city polygons (Public Health - Seattle & King County / King County GIS)
- Cities: Seattle (Regional)
- Role: register (food, all King County cities); address join (food placed by parcel; Liquor Board premises; Pinehurst); boundary (city polygons scope every source)
- Tier: 1 (1a) - dataset says Public Domain, but the live site-wide terms forbid publishing without written permission; the granting Open Data terms are a 404
- Rests on: "the live site-wide kingcounty.gov terms forbid publishing without written permission. The owner reads the dataset's declaration and the data terms as governing" (US:304); polygons "read as permitted with the food inspections" (US:182)
- Decided by / when: owner (2026-10-01, "option 1", "defensible") (DRAFT:630-641; DS:2957)
- What would flag it: King County, on its live terms; note the displayed legend "Data provided by permission of King County" rests on archived terms, so a reader could call it a claim of permission never given
- Safety net: notice (COMP:2188-2191, adds "Not endorsed by King County"); page credit (app/pages/174_Seattle_Heatmap.py:48-50); no USPS-derived address fields (US:49); removal rule; privacy verdict publish (docs/privacy_verdicts.md:165)
- Strengthen: written confirmation from King County, or a live copy of the Open Data terms

#### US-PHL-OPA - OPA Property Assessments (City of Philadelphia, Carto)
- Cities: Philadelphia
- Role: address join (residence check only)
- Tier: 1 (1b) - same City of Philadelphia License and incorporated terms as the licences; nothing from it is published
- Rests on: "Same 'City of Philadelphia License' as the license data" (US:63-64); only two derived values selected, never published (US:59-63)
- Decided by / when: build session (2026-09-21), under the owner's Philadelphia decision (ARCH:17108)
- What would flag it: the City, as for US-PHL-LI (internal use is the weakest target)
- Safety net: as US-PHL-LI; no owner name, mailing address or exemption amount downloaded (US:26)
- Strengthen: same written permission

#### US-BELLEVUE - Business Licenses (All) (City of Bellevue)
- Cities: Seattle (Regional)
- Role: register
- Tier: 1 (1b) - portal Terms of Use allow only "own personal, non-commercial use", all other rights reserved; the data field is narrower
- Rests on: "The owner reads the data's own field as governing it: a free, non-commercial map falls outside its one prohibition" (US:303)
- Decided by / when: owner (2026-10-01, option 1) (DRAFT:625-641; DS:3002)
- What would flag it: City of Bellevue on the portal terms; any move to commercial use breaks even the narrow reading
- Safety net: notice (COMP:2203-2205); page credit (174_Seattle:54); legal name, UBI, mailing never requested (US:47); removal "takes the layer down first" (DS:3009)
- Strengthen: written confirmation from Bellevue

#### US-SNOCO-FOOD - Food Service Establishments (2025) (Snohomish County)
- Cities: Seattle (Regional) (Lynnwood, Mountlake Terrace)
- Role: register
- Tier: 1 (1b) - item SILENT; published by Public Works Solid Waste, not in the open-data catalogue; website "All rights reserved" read as a page footer
- Rests on: "SILENT, read permissively ... website's 'All rights reserved' as a web-page footer" (US:305; DRAFT:193-200)
- Decided by / when: owner (2026-10-02, "permissive read") (DRAFT:186-200; DS:2989)
- What would flag it: Snohomish County on its site-wide reservation
- Safety net: notice with "not a current, complete or official record" (COMP:2198-2202); page credit (174_Seattle:50-51); removal rule
- Strengthen: written confirmation, or a catalogue-listed copy with a stated licence

#### US-PHL-LIMITS - City Limits boundary (City of Philadelphia, Planning and Development)
- Cities: Philadelphia
- Role: boundary
- Tier: 1 (1c) - same incorporated terms, but the dataset itself states "Usage: Public use; Free"
- Rests on: "the boundary dataset ... states 'Usage: Public use; Free'" (US:298, US:535-541)
- Decided by / when: owner (2026-09-21) (ARCH:17108)
- What would flag it: the City, as above (least likely target)
- Safety net: _UNSETTLED_TERMS names "city limits" (COMP:2245)
- Strengthen: none beyond the pending request

#### US-MIAMI - Local Business Tax, municipal boundaries, Miami-Dade Transit GTFS (Miami-Dade County ITD)
- Cities: Miami (Regional)
- Role: register; boundary (naming); rail
- Tier: 1 (1c) - nothing grants and nothing forbids; three County documents read to silence; GTFS has no feed_info and no developer terms
- Rests on: "a definitive absence of restriction from the County's own authoritative pages ... No enquiry to the County is needed" (US:316; ARCH:17184-17197)
- Decided by / when: build session reading (2026-09-21), owner disclosure decision same day (ARCH:17415)
- What would flag it: Miami-Dade County, on absence of a grant (copyright in the register)
- Safety net: removal rule; project's own line colours, no County branding (US:573-576); OWNERNAME and MAIL* never downloaded (US:28); privacy verdict publish (docs/privacy_verdicts.md:29). No longer named in the footer (_UNSETTLED_TERMS says "One city", COMP:2244)
- Strengthen: a one-line written confirmation from the County, or restore the footer disclosure

#### US-TUCSON - BUSLIC layer 3 (City of Tucson)
- Cities: Tucson
- Role: register
- Tier: 1 (1c) - licenseInfo is an accuracy disclaimer only; sibling City disclaimers say "personal use", read as not incorporated
- Rests on: "SILENT, read as permitted by the owner ... over two sibling City disclaimers ... 'for your personal use'" (US:232; DS:2422-2427)
- Decided by / when: owner (2026-09-30) (DEC:1446)
- What would flag it: City of Tucson citing its sibling disclaimers; A.R.S. 39-121.03 if the project became commercial (DS:2433)
- Safety net: notice (COMP:2001-2003); page quotes "should not be considered a complete listing" (app/pages/134_Tucson_Heatmap.py:92); sole-proprietor names withheld (US:56); privacy verdict publish (docs/privacy_verdicts.md:102)
- Strengthen: written confirmation from the City

#### US-DAL-AP - Address Points (City of Dallas Development Services GIS)
- Cities: Dallas
- Role: address join
- Tier: 1 (1c) - silent on reuse, and an open-ended indemnity accepted on top; nothing from it is displayed
- Rests on: "Reuse: nothing grants it and nothing forbids it" and "indemnify, defend, and hold harmless The City of Dallas" (DS:458-463)
- Decided by / when: owner (2026-09-30) (DEC:3707; DS:464)
- What would flag it: the City (claims under the indemnity); a pin described as exact
- Safety net: prose rule "approximate, not surveyed" (app/pages/86_Dallas_Heatmap.py:90-91); only address fields read (US:42); optional credit not displayed
- Strengthen: swap to the Census geocoder (offered, unmeasured, DS:465), or add the optional credit

#### US-SNOCO-AP - Building Address Points (Snohomish County SnocoGIS / E911)
- Cities: Seattle (Regional)
- Role: address join
- Tier: 1 (1c) - SILENT, but in the County's open-data catalogue with the County disclaimer as its licence field
- Rests on: "The owner's permissive reading of the sibling food layer extends to it on firmer ground" (DEC:15766-15774; US:306)
- Decided by / when: licence-read agent and owner extension (2026-10-02)
- What would flag it: Snohomish County (unlikely; no point displayed)
- Safety net: placement never described as exact (US:306); removal rule
- Strengthen: none needed beyond the food layer's

---

### TIER 2 - conditional on a state the project must keep

#### US-WMATA - Rail GTFS Static (WMATA, keyed API)
- Cities: Washington D.C.
- Role: rail
- Tier: 2 (2a) - API agreement: grant ends with the account; third-party redistribution barred; accuracy clause; delete-and-certify on termination
- Rests on: §9(i) "all rights and licenses granted to you will terminate immediately" (US:369-375); account must stay live (US:401-407)
- Decided by / when: owner (2026-09-21, account re-established; re-confirmed 2026-09-22) (ARCH:16075; docs/gated_access.md:24)
- What would flag it: WMATA revoking the key, or reading committed outputs/ on a public GitHub repo as "sharing ... with any other person" (US:348)
- Safety net: gate item (DS:736-746); _AS_RECORDED for §6 (COMP:2265-2274); _NON_AFFILIATION (COMP:2225-2230); key never stored
- Strengthen: written WMATA confirmation that the public repo's outputs are "within your Application"

#### US-LAMETRO - LA Metro Rail GTFS (LACMTA)
- Cities: Los Angeles
- Role: rail
- Tier: 2 (2a) - no-modification clause, terminable "at any time and for any reason" with removal of all references
- Rests on: "not change, tamper ... or otherwise modify"; owner: "this project does not modify it" after shapes emitted unrounded (US:343, US:426-448)
- Decided by / when: owner (2026-09-21)
- What would flag it: LA Metro on modification (stations are averaged, not Metro's), or its trademark; terms also speak of a "registration form" the record does not mention (docs/licenses/la-metro-terms-conditions.html)
- Safety net: notice "LA Metro" (COMP:445-448); _NON_AFFILIATION
- Strengthen: written clarification from Metro, or OSM rail (the Buffalo/Houston precedent)

#### US-SEA-REG - Business Locations (Active) (City of Seattle, FAS via data.seattle.gov)
- Cities: Seattle (Regional)
- Role: register
- Tier: 2 (2a) - permitted, but no commercial purpose for data configurable as a list of individuals
- Rests on: "data that can be 'configured as a list of individuals' may not be used 'for a commercial purpose'" (US:302)
- Decided by / when: licence-read + owner "no commercial, nothing sold" (2026-10-01) (DRAFT:616-624)
- What would flag it: City of Seattle if the project took ads, a paid tier or client use
- Safety net: notice (COMP:2206-2208); contact, phone, mailing, legal name never requested (US:46)
- Strengthen: none needed while non-commercial

#### US-LCB - Off Premise licensee list (Washington State Liquor and Cannabis Board)
- Cities: Seattle (Regional)
- Role: register (alcohol retail outside Seattle and Bellevue)
- Tier: 2 (2a) - no licence; RCW 42.56.070(8) non-commercial condition; an accuracy note the page must carry while the Board does
- Rests on: "records received through the Public Records Act may not be used for commercial purposes" (US:307; DRAFT:229-251)
- Decided by / when: licence-read + owner "yes non-commercial" (2026-10-02)
- What would flag it: the Board, on commercial use or a claim of completeness
- Safety net: notice with date and the Board's note (COMP:2192-2197); page caption (174_Seattle:51-54); Licensee, ID, phone, mailing never read (US:52)
- Strengthen: none needed; re-check the note at each refresh (DS:2982)

#### US-SAC-REG - Business Operation Tax Information (City of Sacramento)
- Cities: Sacramento
- Role: register
- Tier: 2 (2b) - City Open Data Terms grant use, with an uncapped indemnity accepted
- Rests on: "indemnify, defend at his/her sole cost ... even if the claim may be groundless, false or fraudulent" (DS:425-427)
- Decided by / when: owner (2026-09-29) (DS:430; DEC:5900)
- What would flag it: a third party's claim the City passes on
- Safety net: owner, phone, mail columns never requested (US:36); 525 person names shown by description; privacy verdict publish (docs/privacy_verdicts.md:96); removal rule
- Strengthen: none needed

#### US-WPRDC - Geocoded Food Facilities (Allegheny County Health Department via WPRDC)
- Cities: Pittsburgh
- Role: register
- Tier: 2 (2b) - CC0 data, but WPRDC's DUA binds by use: uncapped indemnity accepted, notify duty on Non-Public Information
- Rests on: "an uncapped indemnity of the University of Pittsburgh, UCSUR, the City and the County ... accepted by the owner" (US:229)
- Decided by / when: owner (2026-09-30) (DEC:4374-4380)
- What would flag it: WPRDC if Non-Public Information surfaced and was not reported
- Safety net: file has no person column; privacy verdict publish (docs/privacy_verdicts.md:130); courtesy credit on page caption (app/pages/78_Pittsburgh_Heatmap.py:47)
- Strengthen: none needed

#### US-MTA - NYCT subway + SIR GTFS (MTA)
- Cities: New York
- Role: rail
- Tier: 2 (2b) - "You will not modify or delete any of the data"; no accuracy claims; terminable without notice
- Rests on: feed 6 dp throughout, "so that clause was never engaged" (US:446-448); SIR drawn in a lighter blue (ARCH:19682)
- Decided by / when: build session (2026-09-21); row still says "An open decision ... see PLAN.md" (US:345)
- What would flag it: MTA on modification or an accuracy implication; logos need an application (US:591)
- Safety net: _AS_RECORDED (COMP:2268-2274); New York page avoids accuracy words (app/pages/5_New_York_Heatmap.py:9); _NON_AFFILIATION
- Strengthen: close the stale "open decision" text

#### US-SFMTA - Muni Metro GTFS (SFMTA)
- Cities: San Francisco
- Role: rail
- Tier: 2 (2b) - "revocable license"; required verbatim credit displayed; stored copy also carries a §5 indemnity and §10 "only Licensor shall have the right to alter ... the Data" not recorded in the row
- Rests on: "Reproduced with permission granted by the City and County of San Francisco ..." (DS:518-523)
- Decided by / when: licence check (2026-09-21)
- What would flag it: SFMTA revoking
- Safety net: notice 3 verbatim, with clause 12's "as is" paragraph and clause 4's disclaimer since 2026-10-03; own palette, no Muni branding (US:595-596)
- Strengthen: none needed. Clause 4 reads "display or include this disclaimer in any use agreement"; the site has no use agreement, so the disclaimer is displayed (the cautious reading, 2026-10-03)

#### US-MTS - MTS Trolley GTFS (San Diego MTS)
- Cities: San Diego
- Role: rail
- Tier: 2 (2b) - revocable grant; trademarks "may not be used in association with GTFS Data" while official colours and names are kept
- Rests on: owner kept official colours and names, recorded as open (US:611-617); the tightest marks clause (DS:674-678)
- Decided by / when: owner (2026-09-21)
- What would flag it: MTS on line names/colours beside its data
- Safety net: _NON_AFFILIATION (COMP:2219-2230); no logos
- Strengthen: switch San Diego to its own palette (one setting)

#### US-CHI - Business Licenses r5kz-chrr and Boundaries - City qqq8-j68g (City of Chicago)
- Cities: Chicago
- Role: register; boundary
- Tier: 2 (2b) - reuse contemplated; City may end use "for any reason"; indemnity; verbatim notice required
- Rests on: "may require a user of this data to terminate any and all display ... for any reason" (US:297)
- Decided by / when: licence check (2026-09-21)
- What would flag it: the City terminating; indemnity not recorded as accepted
- Safety net: notice verbatim site-wide (COMP:430-438); privacy verdict publish (docs/privacy_verdicts.md:26)
- Strengthen: record the indemnity acceptance

#### US-KCMO - Business License Holders kkhs-93m4 (City of Kansas City, Missouri)
- Cities: Kansas City
- Role: register
- Tier: 2 (2c) - Public Domain by ordinance; the portal terms' open indemnity read as binding nothing; worst case an indemnity
- Rests on: KCMO Code s.2-2134(a) "no restrictions or requirements placed on use" overrides the undated terms (DS:2403-2411)
- Decided by / when: owner (2026-09-30) (DEC:1566-1581)
- What would flag it: the City invoking its terms page indemnity
- Safety net: notice verbatim (COMP:1984-1997); fetch stops if the licence leaves Public Domain (US:54); privacy verdict publish (docs/privacy_verdicts.md:101)
- Strengthen: check Finance-department terms before a republish (DS:2415)

#### US-CTA - CTA GTFS (Chicago Transit Authority)
- Cities: Chicago
- Role: rail
- Tier: 2 (2c) - grant purpose-limited to assisting riders or promoting transit
- Rests on: "Decided: the project falls within that purpose" (US:449-454)
- Decided by / when: owner (2026-09-21)
- What would flag it: CTA disputing purpose
- Safety net: optional credit displayed (COMP:452-454); _NON_AFFILIATION
- Strengthen: none needed

#### US-MBTA - MBTA GTFS (MassDOT)
- Cities: Boston
- Role: rail
- Tier: 2 (2c) - express grant, but revocable and alterable "at any time without notice"; acknowledgement required and shown
- Rests on: §3.1 "non-exclusive, limited, and revocable rights to use, reproduce, and redistribute" (US:346)
- Decided by / when: licence check (2026-09-21)
- What would flag it: MassDOT revoking
- Safety net: notice (COMP:449-451); page line (app/pages/8_Boston_Heatmap.py:90); local copy kept
- Strengthen: none needed

#### US-SEPTA - SEPTA Metro GTFS (SEPTA)
- Cities: Philadelphia
- Role: rail
- Tier: 2 (2c) - revocable grant, fee may be instituted, indemnification required; trademark clause covers only the Logo
- Rests on: "limited and revocable right to use, reproduce and redistribute the datasets" (US:347); Trademark Notice claims only "The SEPTA Logo" (US:475-500)
- Decided by / when: licence check (2026-09-21)
- What would flag it: SEPTA revoking or charging
- Safety net: no logo; _NON_AFFILIATION; nothing required to display
- Strengthen: none needed

#### US-SD-REG - Business Tax Certificates (City of San Diego, seshat.datasd.org)
- Cities: San Diego
- Role: register
- Tier: 2 (2c) - portal terms permit "Derivative Work"; user indemnifies the city
- Rests on: derivative work "based in any way or to any extent on the Data" (US:236); indemnity noted (US:287-290)
- Decided by / when: licence check (2026-09-21); no owner acceptance of the indemnity recorded
- What would flag it: third-party claim passed on
- Safety net: privacy verdict publish (docs/privacy_verdicts.md:23); parcel residence check (US:14)
- Strengthen: record the indemnity acceptance

#### US-SANGIS - SanGIS/SANDAG tax parcels
- Cities: San Diego
- Role: address join (residence check)
- Tier: 2 (2c) - End User Agreement; no alteration as SanGIS product; credit PROHIBITED at this scale
- Rests on: "SanGIS shall not be attributed as the source of the data when representing the data at scales below 1:24,000" (US:245-261)
- Decided by / when: licence read (2026-09-22)
- What would flag it: a reviewer ADDING a SanGIS credit would breach it
- Safety net: nothing from the layer reaches outputs/ (US:268-270); deliberately no notice
- Strengthen: none needed

#### US-LAC-PARCEL - LA County Assessor parcels (LA County Enterprise GIS)
- Cities: Los Angeles
- Role: address join (residence check)
- Tier: 2 (2c) - explicit grant incl. publish and adapt; "Automatically voided on violation"
- Rests on: "license to copy, publish, distribute and/or transmit the Data, to adapt the Data and to exploit the Data" (US:239)
- Decided by / when: licence read (2026-09-22)
- What would flag it: implying County endorsement
- Safety net: three fields only, owner names absent by law (US:18); no endorsement implied
- Strengthen: none needed

---

### TIER 3 - explicit open position, nothing restrictive in force

#### US-NYS - Retail Food Stores 9a8c-vfzj, Appearance Enhancement & Barber Business y3u4-jbgh (data.ny.gov)
- Cities: New York, Buffalo
- Role: register
- Tier: 3 (3a) - OPEN-NY terms: no attribution, no pre-approval; State may require a stop in writing on breach
- Rests on: "So long as you are not doing anything malicious with NYS data, you may use it as you wish" (US:296)
- Decided by / when: licence check (2026-09-21)
- What would flag it: the State, only on a breach
- Safety net: license_holder_name never selected (US:23, US:35)
- Strengthen: none needed

#### US-NYC - DOHMH 43nn-pn8j, DCWP w7w3-xahh, Borough Boundaries gthc-hcne (City of New York)
- Cities: New York
- Role: register; boundary
- Tier: 3 (3b) - Local Law 11 of 2012 forbids licence requirements or usage restrictions; one conditional identification duty
- Rests on: "without registration requirement, license requirement, or usage restrictions" (US:299; DS:539-553)
- Decided by / when: licence check (2026-09-21)
- What would flag it: DoITT requiring source/version/modifications identification
- Safety net: source, version and modifications on the About and What Is Excluded pages (DS:549-553)
- Strengthen: none needed

---

### TIER 4 - public domain / no copyright

#### US-SF - Registered Business Locations g8m3-pdis, Assessor rolls wv5m-vpq2, Bay Area County Polygons wamw-vt4s (City and County of San Francisco)
- Cities: San Francisco
- Role: register; address join; boundary
- Tier: 4 (4a) - ODC PDDL 1.0
- Rests on: "Open Data Commons PDDL 1.0" (US:225, US:234, US:238)
- Decided by / when: licence check (2026-09-21)
- What would flag it: none on licence; privacy (practitioner licences left out, DEC:13652)
- Safety net: privacy verdict publish (docs/privacy_verdicts.md:24)
- Strengthen: none needed

#### US-LA - Listing of Active Businesses 6rrh-rzua (City of Los Angeles, Office of Finance)
- Cities: Los Angeles
- Role: register
- Tier: 4 (4a) - CC0 1.0
- Rests on: "CC0 1.0 Universal" (US:235)
- Decided by / when: licence check (2026-09-21)
- What would flag it: privacy only
- Safety net: Kansas City's rule; verdict publish (docs/privacy_verdicts.md:25)
- Strengthen: none needed

#### US-BOS - Food inspections, Licensing Board, Cannabis licences (+ property layers) (City of Boston, data.boston.gov)
- Cities: Boston
- Role: register
- Tier: 4 (4a) - ODC PDDL per dataset
- Rests on: "declared per-dataset in CKAN's license_id as odc-pddl" (US:237)
- Decided by / when: licence check (2026-09-21)
- What would flag it: none
- Safety net: owner/applicant/phone columns not selected (US:29-31)
- Strengthen: none needed

#### US-MPLS - Food Inspections (City of Minneapolis)
- Cities: Minneapolis
- Role: register
- Tier: 4 (4a) - CC0 1.0 waiver on the item
- Rests on: "City of Minneapolis has waived all copyright and related or neighboring rights" (US:228)
- Decided by / when: licence-read (2026-09-30)
- What would flag it: none
- Safety net: inspector free text never requested (US:44)
- Strengthen: none needed

#### US-NOLA - Active Occupational Licenses iqay-p646 (City of New Orleans)
- Cities: New Orleans
- Role: register
- Tier: 4 (4a) - CC0 1.0, re-checked on every fetch
- Rests on: "fetch stops if the license is no longer CC0" (US:57, US:233)
- Decided by / when: build session (2026-09-30)
- What would flag it: none
- Safety net: ownername, phone never requested (US:57)
- Strengthen: none needed

#### US-TX - Active Sales Tax Permit Holders jrea-zgmq (Texas Comptroller)
- Cities: Houston, Dallas
- Role: register
- Tier: 4 (4b) - Comptroller's policy: "public domain ... as permitted by law"; no seals or marks
- Rests on: "Information on CPA's sites is public domain and may be copied and used as permitted by law" (US:226)
- Decided by / when: licence-read (2026-09-29) (DEC:5223)
- What would flag it: none; re-read the policy before a republish
- Safety net: taxpayer name, address and SSN-derived number never requested (US:39-40)
- Strengthen: none needed

#### US-BUF - Business Licenses qcyy-feh8 (Open Data Buffalo)
- Cities: Buffalo
- Role: register
- Tier: 4 (4b) - portal FAQ: public domain, "no restrictions on the use"
- Rests on: "All data available on the portal is licensed in the public domain" (US:301)
- Decided by / when: licence read (2026-09-29)
- What would flag it: none; MUST NOT call them official records (app/pages/73_Buffalo_Heatmap.py:53-54)
- Safety net: privacy verdict publish (docs/privacy_verdicts.md:95)
- Strengthen: none needed

#### US-COHGIS - Site Addresses (City of Houston Planning & Development)
- Cities: Houston
- Role: address join
- Tier: 4 (4c) - public domain on the Hub, with a "(c) HITS-GIS. All rights reserved" tension on sibling items
- Rests on: "COHGIS data is in the public domain and may be copied without permission" (US:41, US:227)
- Decided by / when: build brief read (2026-09-29)
- What would flag it: HITS-GIS (low)
- Safety net: courtesy credit not displayed; nothing required
- Strengthen: none needed

#### US-TIGER - TIGERweb Incorporated Places, States, County Subdivisions (US Census Bureau)
- Cities: Washington D.C. (states naming), Buffalo, Houston, Minneapolis, Pittsburgh, Dallas, Kansas City, Tucson, New Orleans, Seattle (Regional) (Lynnwood, Mountlake Terrace)
- Role: boundary; naming
- Tier: 4 (4a) - US federal work
- Rests on: "A US federal government work, so not copyrightable" (US:300; US:176-187)
- Decided by / when: licence check (2026-09-21)
- What would flag it: implying Census endorsement
- Safety net: _NON_AFFILIATION
- Strengthen: none needed

#### US-CENSUS-GEO - Census Bureau batch geocoder (US Census Bureau)
- Cities: Los Angeles, New York, Washington D.C., Sacramento, Houston, Dallas
- Role: geocoder
- Tier: 4 (4c) - federal work, but its terms page is recorded as NOT read
- Rests on: "Terms page not read. A US federal government work" (US:313)
- Decided by / when: none recorded
- What would flag it: none expected
- Safety net: only street, city, state, ZIP sent (US:37)
- Strengthen: read the terms page (DS:687-689)

#### US-NAICS - 2022 NAICS titles (US Census Bureau)
- Cities: Kansas City
- Role: naming (title-to-code map)
- Tier: 4 (4a) - US federal work
- Rests on: "A US federal government work, public domain" (US:55)
- Decided by / when: build session (2026-09-30)
- What would flag it: none
- Safety net: none needed
- Strengthen: none needed

#### US-WIKIDATA - Q107175168 Dos Rios station (Wikidata)
- Cities: Sacramento
- Role: rail (one station coordinate)
- Tier: 4 (4a) - CC0 1.0
- Rests on: "CC0 1.0 (Wikidata's structured data): nothing to display" (US:38)
- Decided by / when: owner (2026-09-29)
- What would flag it: none
- Safety net: retires itself when OSM maps the station
- Strengthen: none needed

#### Not landed / not used (for completeness)
- Long Beach (MapsLB, breach-only indemnity accepted, DEC:4344): LA + Long Beach is probed, not built.
- NFTA, SacRT, METRO Houston, RideKC, Sound Transit, Metro Transit, PRT, DART, Sun Link, RTA GTFS: none fetched for a landed map; OSM instead (US:150-159).

---

### FLAGS

#### A. Sources in use with NO licence row in docs/data_sources*.md
1. **D.C. Basic Business License** (DCRA/DLCP FeatureServer, US:20): the whole D.C. register has no licence row anywhere (grep for DCRA/DLCP/opendata.dc.gov finds only US:20 and US:173).
2. **DC Boundary**, layer 10 (US:173): no licence row.
3. **LA County Planning incorporated-city boundaries** (US:167): no licence row; the Assessor parcels' Enterprise GIS grant (US:239) is a different host and must not be extended by proximity (the rule at US:279-281).
4. **MassGIS Massachusetts Municipalities** (US:171): Boston's actual boundary and naming layer has no licence row; the PDDL row at US:237 covers "city boundary" on data.boston.gov, which is the outline recorded as NOT used (US:172).

#### B. Notices required by the docs that could not be found rendered
1. **SFMTA liability disclaimers**: US:342 records "Must also display liability disclaimers". _NOTICES carries only the permission sentence (COMP:439-444); nothing in app/pages/2_San_Francisco_Heatmap.py. Searched COMP and the SF page for "disclaim", "as is", "SFMTA". The stored clause (docs/licenses/sfmta-transit-data-license-agreement.html) says "display or include this disclaimer in any use agreement", so it may not bite, but the record says it is required. **Closed 2026-10-03:** displayed on the cautious reading, verbatim, in notice 3 with clause 12's second paragraph.
2. Nothing else missing: Chicago (COMP:430), KCMO (COMP:1989), Tucson (COMP:2001), King County incl. "Data provided by permission of King County" (COMP:2188), LCB date and note (COMP:2192), Snohomish (COMP:2198), Bellevue (COMP:2203), LA Metro (COMP:445), MassDOT (COMP:449) all render.

#### C. Positions recorded as pending / unresolved that a landed city relies on
1. **Philadelphia written request** sent 2026-09-21, followed up 2026-09-28, **no reply**; next step (wait, chase, call) is the owner's open call (PLAN.md:829-842; docs/gated_access.md:25; docs/recheck_calendar.md:138). No reply is recorded anywhere as of 2026-10-02.
2. **Census geocoder terms "not read"** (US:313; DS:687-689) - six landed cities.
3. **San Diego municipal boundaries (SANDAG): "Terms not read"**, scoping San Diego since 2026-09-18 (US:315), flagged higher priority than the geocoder.
4. **MTA "An open decision, not a settled one - see PLAN.md"** (US:345), but PLAN.md carries no MTA item and US:446-448 says the clause was "never engaged". Stale either way.
5. **Miami-Dade recorded both ways**: closed by reading (US:316; ARCH:17184) but "Open question" (US:563) and "all still open" (DS:661-668); the footer no longer names Miami (COMP:2244), while its code comment still says "Two cities' sources" (COMP:2232).
6. **Agency branding (route colours and names)**: the owner's decision was to "keep the official colours and record this as an open question" (US:611-617; DS:669-682). San Diego, Los Angeles, Chicago, New York, Washington D.C. rely on it; MTS's clause is a flat prohibition.
7. **Indemnities in read terms with no acceptance recorded**: San Diego portal (US:287-290), Chicago (US:297), SEPTA (US:347), and SFMTA §5 (stored copy only, not in the US:342 row). Unlike Sacramento, Dallas, Pittsburgh (and Hong Kong), none has an owner acceptance entry.
8. **WMATA account**: a standing gate, last confirmed 2026-09-22 (docs/recheck_calendar.md:137); must be re-confirmed before every deploy.
9. **Recurring "MUST DO"s**: KCMO Finance-department terms before a republish (DS:2415); LCB data-transfer note at each refresh (DS:2982).

---

## Appendix B - Canada, Mexico, Spain, Ireland, Italy, Argentina, Australia, Germany, Switzerland, Georgia, United Kingdom

## AMER_EU1 - notice positions, weakest to strongest

Scope: Canada (Vancouver (Regional) with Surrey, Montréal, Calgary, Edmonton, Toronto,
Ottawa, Kitchener-Waterloo (Regional)); Mexico (Mexico City, Guadalajara (Regional),
Monterrey (Regional)); Spain (Madrid, Barcelona, Palma); Ireland (Dublin); Italy (Milan,
Rome, Florence); Argentina (Buenos Aires); Australia (Sydney, Melbourne); Germany (Berlin);
Switzerland (Zurich); Georgia (Tbilisi); United Kingdom (London, Glasgow, Newcastle,
Manchester, Birmingham, Edinburgh, Sheffield, Nottingham, Blackpool).
Read from the repository at 2a0dbf6f (worktree-staging = origin/master). Nothing fetched or edited.

The removal commitment (docs/data_sources.md:302-319) is the safety net for every entry;
it is cited once here and not repeated.

**OpenStreetMap (handled centrally):** rail and/or boundaries from OSM in Mexico City,
Guadalajara, Monterrey, Barcelona, Palma, Rome, Florence, Zurich (plus Gemeinde naming),
Kitchener-Waterloo (rail only), Ottawa (rail only), Buenos Aires (station names, cross-check,
boundary), Sydney, Melbourne, London, Glasgow, Newcastle, Manchester, Birmingham, Edinburgh,
Sheffield, Nottingham, Blackpool, Tbilisi; cross-check only in Dublin and Berlin. Note for the
central handler: the "OpenStreetMap (rail geometry)" notice (app/components.py:750-801) does
not list Buenos Aires, Sydney, Melbourne, Tbilisi or the nine UK cities; their pages credit
OSM in page text, except Melbourne (app/pages/62_Melbourne_Heatmap.py has no OSM mention).

---

### Tier 1 - weakest

#### NTA-GTFS - National GTFS, rail for Dublin (National Transport Authority / Transport for Ireland)
- Cities: Dublin
- Role: rail (Luas Red, Luas Green, DART geometry and stations)
- Tier: 1 (1a) - no licence position recorded anywhere; the drawn rail rests on nothing read
- Rests on: nothing. The row names only endpoint, currency and trim (docs/data_sources/ireland.md:110-122, :168); a repo-wide grep for NTA/Transport for Ireland near licence/terms/CC BY/attribution finds no reading
- Decided by / when: build session 2026-09-22 switched OSM to the NTA feed mid-build (docs/decisions/2026-09-20.md:10441-10451); licence never read
- What would flag it: the NTA, if its terms require attribution or restrict modification; a reviewer finding drawn geometry with no source credit
- Safety net: none specific; no notice in _NOTICES and no credit on app/pages/19_Dublin_Heatmap.py; OSM cross-check (notice) could replace it
- Strengthen: run licence-read on the NTA GTFS terms now, add a notice; fallback is OSM geometry, already cached as the cross-check

#### MIL-ATM - ATM metro layers ds535/ds539/ds533 and gtfs.zip (Comune di Milano portal / ATM)
- Cities: Milan
- Role: rail (stations, alignments, route colours)
- Tier: 1 (1b) - a CKAN "cc-by" declaration recorded as a citation, explicitly "not read to this project's standard"
- Rests on: "The rail sources' licence is recorded as CC-BY but has NOT been read ... a separate read-licence job before the deploy gate" (docs/build_briefs/milan.md:382-384, :392-394); docs/data_sources.md:1236-1238 still says only "declare"
- Decided by / when: build session 2026-09-22; the promised read is not recorded as done
- What would flag it: ATM or the Comune if the GTFS carries other terms (the portal mixes cc-by, other-at, cc-zero: docs/data_sources.md:1271-1273); missing CC BY attribution/modification statement for the rail
- Safety net: notice (app/components.py:896-904) says "Contains data from the Comune di Milano" but names only the six registers; the page says only "in ATM's own colors" (app/pages/20_Milan_Heatmap.py:52)
- Strengthen: read the ds535/ds539/gtfs.zip terms (licence-read), then add the rail to notice with a modification sentence

#### KW-TABLES - Inspections.zip and Inspections_PS.zip bulk tables (Region of Waterloo Public Health)
- Cities: Kitchener-Waterloo (Regional)
- Role: register (the SUBCATEGORY typing behind every pin's category)
- Tier: 1 (1b) - item pages name no licence; owner read a portal sentence as covering them
- Rests on: Hub shows "No License Provided / Request permission to use"; owner: portal says "By downloading the data on the portal, you are agreeing to the Open Data License" (docs/data_sources.md:2237-2244; canada.md:109)
- Decided by / when: owner, 2026-09-30 (DECISIONS.md:3960)
- What would flag it: the Region, on the Esri "request permission" label
- Safety net: notice "Region of Waterloo (Kitchener-Waterloo)" (app/components.py:680-692) displayed by choice; "Any objection from the Region is honoured" (docs/data_sources.md:2243-2244); SiteTelephone never fetched; privacy verdict publish (docs/privacy_verdicts.md:131)
- Strengthen: written confirmation from the Region's open-data contact that the portal licence covers the zips

#### CAT-PALMA - INSPIRE Addresses, Palma 07040 (Dirección General del Catastro)
- Cities: Palma
- Role: address join (places the ~87% of premises without a register coordinate)
- Tier: 1 (1c) - owner's permissive reading over an older licence PDF still linked, which restricts
- Rests on: 2016 "Licencia de Acceso y Uso" "bars distributing 'información original' untransformed, and asks the reuser to bear third-party claims"; CC BY 4.0 is "the dated, current declaration" (docs/build_briefs/palma.md:97-104; spain.md:201-204)
- Decided by / when: owner, 2026-09-29 (DECISIONS.md:5347-5349, call C)
- What would flag it: Catastro, reading the 2016 PDF as still governing (each pin sits on Catastro's exact coordinate)
- Safety net: notice (app/components.py:846-860) names Catastro as author and owner, CC BY 4.0 linked, join and access date stated; the address layer is never published; privacy verdict publish (docs/privacy_verdicts.md:132)
- Strengthen: ask Catastro to confirm CC BY 4.0 supersedes the 2016 PDF, or record that the HVD regulation makes it so

### Tier 2 - conditional on a state the project must keep

#### BCN-CENS - Cens de locals en planta baixa, 2022 (Ajuntament de Barcelona)
- Cities: Barcelona
- Role: register
- Tier: 2 (2a) - act owed and undelivered, plus a "may not be altered" clause read against its letter; borderline tier 1
- Rests on: Art. 8 "content ... may not be altered" read as barring misrepresentation, not analysis (docs/data_sources.md:1142-1162); notification "not yet sent" (docs/data_sources.md:333, :1094-1112; docs/notifications/barcelona-city-council.md:1, :58-63)
- Decided by / when: owner, 2026-09-22 (publish on disclosed position); live terms read by the owner 2026-09-22 (docs/data_sources.md:1114-1117)
- What would flag it: the Ajuntament, on alteration or on never having been informed
- Safety net: notice "Ajuntament de Barcelona" (app/components.py:822-835) prescribed credit, modifications itemised, notification status stated; Referencia_Cadastral never requested; "If the Council reads it the other way, Barcelona comes down" (docs/data_sources.md:1160-1162); privacy verdict publish (docs/privacy_verdicts.md:40)
- Strengthen: retry the notification channel (atencioenlinia) and record delivery; no deadline, but every day undelivered is the exposure

#### GOIB-PALMA - Registre d'Establiments de Restauració i Entreteniment de Mallorca (Consell de Mallorca on the GOIB catalogue)
- Cities: Palma
- Role: register
- Tier: 2 (2a) - uncapped indemnity accepted, plus "no alteration" on Barcelona's reading
- Rests on: reuser "accepta indemnitzar ... pel mer ús, reproducció, modificació o distribució", no cap (docs/data_sources.md:437-448); call A extends Barcelona's reading (DECISIONS.md:5342-5343)
- Decided by / when: owner, 2026-09-29 (DECISIONS.md:5341-5349)
- What would flag it: GOIB or the Consell (alteration; any third-party claim triggers the indemnity)
- Safety net: notice (app/components.py:846-860) carries every GOIB element (credit, author, title, licence link, URI, update date, modified); Explotador/s never read; GOIB's "urged" courtesy notification not done (docs/data_sources.md:2274-2275)
- Strengthen: send GOIB the urged courtesy note; it costs nothing and narrows the alteration reading

#### STM - Métro GTFS / geometry (Société de transport de Montréal, on the Ville's portal)
- Cities: Montréal
- Role: rail
- Tier: 2 (2b) - CC BY 4.0, but the displayed notice omits the required modification/interpretation statement, so it drops a tier
- Rests on: portal condition "préciser si des modifications ont été effectuées ou si des interprétations en ont été tirées ... a bare credit does not satisfy it" (docs/data_sources/canada.md:118)
- Decided by / when: build session 2026-09-21
- What would flag it: STM or the Ville; CC BY 4.0 §3(a)(1)(B) and the portal's broader clause
- Safety net: notice (app/components.py:586-590) credits STM and names CC BY 4.0 (no link, no modification sentence)
- Strengthen: add one sentence of changes (lines redrawn, off-island stations removed) and the licence link, as the REM notice beside it does

#### CRTM - M4_Red and M10_Red feature services (Consorcio Regional de Transportes de Madrid)
- Cities: Madrid
- Role: rail (Metro and Metro Ligero ML1)
- Tier: 2 (2b) - currency clause the page must honour, prescribed wording, share-alike on the data, access monitoring
- Rests on: "garantizar que la información mostrada ... esté siempre actualizada" read as a misrepresentation rule, met by stating CRTM's 5 June 2026 date (docs/data_sources/spain.md:115-153, :298-329)
- Decided by / when: owner decision 2026-09-22 (spain.md:115); ML1 amendment owner 2026-09-27
- What would flag it: CRTM, if layers are edited after 5 June 2026 and the map still shows the old network; CRTM may block a reuser whose fetching degrades its systems
- Safety net: notice "Powered by CRTM - www.crtm.es" verbatim, datos explotados disclosed, date stated (app/components.py:519-532); brief_check arcgis_layer max_age_days watches edit dates (spain.md:146-148)
- Strengthen: none needed beyond keeping the max_age check green and re-rendering when CRTM edits

#### TRANSLINK - SkyTrain static GTFS (TransLink)
- Cities: Vancouver (Regional)
- Role: rail
- Tier: 2 (2b) - "limited, revocable" licence; duty to identify on request; commercial-use terms may be imposed
- Rests on: "limited, revocable and non-exclusive license to use, reproduce, and redistribute"; "must provide TransLink sufficient information ... to identify you" read as a duty to answer, not a precondition (docs/data_sources/canada.md:117)
- Decided by / when: build session, recorded as a stated position 2026-09-21 (docs/decisions/2026-09-20.md:17339)
- What would flag it: TransLink revoking, or asking who uses the data and getting no answer
- Safety net: notice Legend verbatim (app/components.py:533-537); no TransLink marks; both term texts stored in docs/licenses/
- Strengthen: none needed; keep a reply ready if TransLink asks

#### EDMONTON - Business Licences, ETS GTFS, Corporate Boundary (City of Edmonton Open Data Terms of Use)
- Cities: Edmonton
- Role: register, rail, boundary
- Tier: 2 (2b) - City may cancel access "at any time for any reason"; pass-through duty with no further restrictions
- Rests on: distributing "in original or modified form" requires the Terms URL and binding recipients "without introducing any further restrictions" (docs/data_sources.md:879-897; canada.md:121)
- Decided by / when: build session 2026-09-21 (corrected from "nothing owed" the same day)
- What would flag it: the City, if the repo LICENSE ever restricted outputs/ or the URL were dropped
- Safety net: notice "City of Edmonton" with the URL, changes and no-endorsement (app/components.py:657-667); repo LICENSE disclaims MIT over outputs/; PDF stored (docs/licenses/edmonton-open-data-terms-of-use.pdf); privacy verdict publish (docs/privacy_verdicts.md:35)
- Strengthen: none needed; keep outputs/ outside the MIT grant

#### OGL-VANCOUVER - Business Licences, Property Parcel Polygons, Property Tax Report, local-area-boundary (City of Vancouver)
- Cities: Vancouver (Regional)
- Role: register; parcel join (residence check, internal only); boundary
- Tier: 2 (2c) - explicit OGL, but terminates automatically on breach
- Rests on: "if you fail to comply with any of them, the rights granted ... will end automatically" (docs/data_sources.md:766-776)
- Decided by / when: build session 2026-09-21
- What would flag it: the City, on a missing or altered verbatim notice
- Safety net: notice verbatim (app/components.py:463-466); no owner or mailing field downloaded (canada.md:19); privacy verdict publish (docs/privacy_verdicts.md:32)
- Strengthen: none needed; keep the en dash and "Licence" exact

#### OGL-SURREY - Surrey Business Directory and City Boundaries (City of Surrey)
- Cities: Vancouver (Regional)
- Role: register, boundary
- Tier: 2 (2c) - OGL - City of Surrey, terminates automatically on breach
- Rests on: "The same OGL template, with Surrey's own wording ... also terminates automatically on breach" (docs/data_sources.md:778-785)
- Decided by / when: build session 2026-09-21
- What would flag it: the City, on a wrong-template notice (hyphen and "License")
- Safety net: notice verbatim (app/components.py:467-470); Home Occupation dropped, PhoneNumber dropped and asserted absent (canada.md:20)
- Strengthen: none needed

#### OGL-CALGARY - Business Licences, CTrain GTFS, City Boundary (City of Calgary)
- Cities: Calgary
- Role: register, rail, boundary
- Tier: 2 (2c) - one OGL covers all three; terminates automatically on breach
- Rests on: "worldwide, royalty-free, perpetual ... including for commercial purposes"; "Terminates automatically on breach" (docs/data_sources/canada.md:120; docs/data_sources.md:859-869)
- Decided by / when: build session 2026-09-21
- What would flag it: the City, on notice wording
- Safety net: notice verbatim (app/components.py:617-620); licence stored docs/licenses/calgary-open-government-licence.txt; privacy verdict publish (docs/privacy_verdicts.md:34)
- Strengthen: none needed

#### OGL-TORONTO - MLS register, TTC GTFS, One Address Repository, Regional Municipal Boundary (City of Toronto)
- Cities: Toronto
- Role: register, rail, geocoder (address join), boundary
- Tier: 2 (2c) - datasets say "License not specified"; OGL captured from open.toronto.ca; terminates automatically
- Rests on: "Both declare 'License not specified' at dataset level ... captured from open.toronto.ca/open-data-licence/" (docs/data_sources/canada.md:122; data_sources.md:913-924); address repository "same license as the business data" (canada.md:17)
- Decided by / when: build session 2026-09-21
- What would flag it: the City, on notice wording; Client Name / phone columns never read (canada.md:47-48)
- Safety net: notice verbatim (app/components.py:653-656); privacy verdict publish (docs/privacy_verdicts.md:36)
- Strengthen: none needed

#### OGL-BC - ABMS municipalities WFS, naming layer (Province of British Columbia)
- Cities: Vancouver (Regional)
- Role: naming (names the 30 out-of-scope SkyTrain stations)
- Tier: 2 (2c) - OGL-BC terminates automatically; API terms make credentials revocable and terms changeable without notice
- Rests on: OGL-BC v2.0 "Terminates automatically on breach"; API Terms add "no new notice"; two sibling layers are "Access Only" (docs/data_sources/canada.md:110; data_sources.md:953-1003)
- Decided by / when: build session 2026-09-22
- What would flag it: the Province, on wording, or if the build ever drifted to an Access Only sibling
- Safety net: notice verbatim (app/components.py:555-558); licence stored docs/licenses/bc-open-government-licence.txt
- Strengthen: none needed

### Tier 3 - explicit open licence, read, notice displayed

#### MTL-VILLE - locaux-commerciaux 2025 and agglomeration boundary (Ville de Montréal)
- Cities: Montréal
- Role: register, boundary
- Tier: 3 (3a) - CC BY 4.0 with a broader interpretation clause; site "tous droits réservés" read as web-only
- Rests on: montreal.ca mentions-légales "written entirely in web-page language ... contains no data language at all" (docs/data_sources.md:846-857); interpretation clause (:812-831)
- Decided by / when: build session 2026-09-21
- What would flag it: the Ville, reading the site terms as reaching data; no licence URI in the notice
- Safety net: notice states modifications and interpretations, no endorsement (app/components.py:578-585); no registrant-name column; privacy verdict publish (docs/privacy_verdicts.md:33)
- Strengthen: add the CC BY 4.0 link to notice

#### SYDNEY-FES - Floor Space and Employment Survey 2022 (City of Sydney)
- Cities: Sydney
- Role: register
- Tier: 3 (3a) - CC BY 4.0 on the item; main website terms bar republishing, read as not incorporated
- Rests on: website terms "bar republishing its content without written authorisation; the read judged them written for that site's pages" (docs/data_sources.md:2061-2064)
- Decided by / when: licence-read 2026-09-28; owner "noted, not a blocker" 2026-09-28
- What would flag it: the City, reading its website terms as covering the data hub
- Safety net: notice with licence, dataset link, modification, warranty disclaimer (app/components.py:1900-1907); no names or addresses; privacy publish-structural (docs/privacy_verdicts.md:83)
- Strengthen: none needed

#### GEOSTAT - Statistical Business Register (National Statistics Office of Georgia)
- Cities: Tbilisi
- Role: register
- Tier: 3 (3a) - explicit grant; app footer "© All rights reserved" read as the site's; no personal-data carve-out
- Rests on: "for any purpose, including commercial and non-commercial use, without restriction ... without prior permission" (docs/data_sources/georgia.md:60; data_sources.md:3025-3034); footer read as site-only (docs/georgia_step0_endpoints.md:174-176)
- Decided by / when: licence-read 2026-10-01, re-read 2026-10-02; notice approved by owner 2026-10-02 (DECISIONS.md:15982)
- What would flag it: an individual entrepreneur, or a company named for a person (148 shown); Georgian data-protection law is not recorded as read
- Safety net: notice (app/components.py:2212-2216) and page caption (app/pages/175_Tbilisi_Heatmap.py:46-49); personal numbers and IE names never written to disk; privacy verdict publish (docs/privacy_verdicts.md:166)
- Strengthen: record a reading of Georgia's personal-data law for named companies

#### FSA-FHRS - Food Hygiene Rating Scheme open data (Food Standards Agency, with the councils)
- Cities: London, Newcastle (Regional), Manchester (Regional), Birmingham (Regional), Sheffield, Nottingham (Regional), Blackpool (Regional)
- Role: register
- Tier: 3 (3a) - OGL v3; the FSA's privacy notice treats name and address as personal data the OGL does not license
- Rests on: "the FSA's privacy notice treats a business's name and address as personal data and the OGL does not license it" (docs/data_sources.md:1918-1922)
- Decided by / when: licence-read 2026-09-28; owner wording and personal-data rule 2026-09-28; UK six by notice precedent 2026-10-02
- What would flag it: a sole trader shown by name; the FSA on "FHRS" name or ratings shown
- Safety net: notices (app/components.py:1815, 1875, 2032, 2067, 2114, 2137, 2160); flat and childminder rules, private addresses never placed, no ratings; verdicts publish (docs/privacy_verdicts.md:79, 82, 147-152)
- Strengthen: none needed

#### FSS-FHIS - Food Hygiene Information Scheme (Food Standards Scotland, via the FSA files)
- Cities: Glasgow, Edinburgh
- Role: register
- Tier: 3 (3a) - OGL v3 (FSS states v3); same personal-data caveat
- Rests on: "FSS's FHIS privacy notice counts the operator's name and address as personal information" (docs/data_sources.md:1995-1999)
- Decided by / when: licence-read 2026-09-28; owner 2026-09-28; Edinburgh 2026-10-02
- What would flag it: home bakers at a flat (Glasgow's 185 now withheld); "FHRS" misnaming
- Safety net: notices (app/components.py:1862, 2090); verdicts publish (docs/privacy_verdicts.md:81, 149)
- Strengthen: none needed

#### TAILTE - Rateable valuation register (Tailte Éireann)
- Cities: Dublin
- Role: register
- Tier: 3 (3b) - CC BY 4.0 under Circular 12/2016; three live attribution strings, Circular chosen as a disclosed position
- Rests on: "No document ranks them ... Recorded as a disclosed position" (docs/data_sources.md:1186-1193); Eircode dropped (:1209-1224)
- Decided by / when: licence-read 2026-09-22; Eircode owner 2026-09-22
- What would flag it: Tailte on wording; GeoDirectory if Eircodes ever returned
- Safety net: notice with modification and warranty sentences (app/components.py:876-885); no name column; publish-structural (docs/privacy_verdicts.md:41)
- Strengthen: add the CC BY 4.0 link

#### MADRID-CENSO - Censo de locales (Ayuntamiento de Madrid)
- Cities: Madrid
- Role: register
- Tier: 3 (3b) - CC BY 4.0 plus general conditions binding by use (date, no distortion, no re-identification)
- Rests on: "obligan a cualquier persona y/o empresa que reutilice datos por el mero hecho de hacer uso" (docs/data_sources/spain.md:220-261)
- Decided by / when: build session 2026-09-22
- What would flag it: the Ayuntamiento under Ley 37/2007 art. 11 sanctions (re-identification, distortion)
- Safety net: notice with prescribed form and date (app/components.py:497-508); no registrant column; verdict publish (docs/privacy_verdicts.md:39)
- Strengthen: none needed

#### INEGI-DENUE - DENUE, entidades 09, 14, 19 (INEGI)
- Cities: Mexico City, Guadalajara (Regional), Monterrey (Regional)
- Role: register
- Tier: 3 (3b) - Términos de Libre Uso; attribution form plus disclosure-of-transformation duty
- Rests on: §1(g) "notificar al usuario final de cualquier análisis o transformación" (docs/data_sources.md:574-604)
- Decided by / when: build session 2026-09-22 (terms stored docs/licenses/inegi-terminos-libre-uso-informacion.pdf)
- What would flag it: INEGI if a city were not named in the notice (it must grow per city)
- Safety net: notice "INEGI" names all three cities (app/components.py:731-743); edition date in data_age; personal columns never read; verdicts publish (docs/privacy_verdicts.md:37, 38, 71)
- Strengthen: none needed

#### MILANO-REG - Six premises registers (Comune di Milano)
- Cities: Milan
- Role: register
- Tier: 3 (3b) - CC BY 4.0, version found only in DCAT-AP_IT
- Rests on: CKAN "no version at all"; three sources give 4.0 (docs/data_sources.md:1240-1247)
- Decided by / when: licence-read 2026-09-22
- What would flag it: the Comune if the version changed (brief_check http_contains watches the .ttl)
- Safety net: notice (app/components.py:896-904); no name column; verdict publish (docs/privacy_verdicts.md:42)
- Strengthen: add the licence link

#### WATERLOO-OGL - Inspection layers 17/18 and Cities and Towns (Region of Waterloo)
- Cities: Kitchener-Waterloo (Regional)
- Role: register (points), boundary
- Tier: 3 (3b) - layers' licenseInfo names the Region's licence; heading v2.0, body v1.0; cited URL 404s
- Rests on: docs/data_sources/canada.md:109; data_sources.md:2227-2236
- Decided by / when: licence-read 2026-09-30
- What would flag it: the Region on misrepresentation (ratings); MFIPPA
- Safety net: notice verbatim credit (app/components.py:680-692); no results shown
- Strengthen: none needed

#### OTTAWA-OGL - OPH food-safety feed and Wards 2022-2026 (City of Ottawa / Ottawa Public Health)
- Cities: Ottawa
- Role: register, boundary
- Tier: 3 (3b) - OGL - City of Ottawa v2.0; feed due to be retired, rights attach to version accessed
- Rests on: docs/data_sources/canada.md:111; data_sources.md:2209-2221
- Decided by / when: read 2026-09-29 (staging brief); build DECISIONS.md:4798
- What would flag it: the City on wording; feed retirement (cached)
- Safety net: notice verbatim and linked (app/components.py:1973-1983); phone never read; verdict publish (docs/privacy_verdicts.md:128)
- Strengthen: none needed

#### REM - REM GTFS (Réseau express métropolitain)
- Cities: Montréal
- Role: rail
- Tier: 3 (3c) - CC BY 4.0 from the legal code bundled in the zip; no licensor named
- Rests on: docs/data_sources/canada.md:119
- Decided by / when: licence-read 2026-09-27; wording owner 2026-09-27
- What would flag it: REM on credit; licence changes in a later feed version
- Safety net: notice with link and modifications (app/components.py:598-607)
- Strengthen: none needed

#### VBB - VBB GTFS (Verkehrsverbund Berlin-Brandenburg)
- Cities: Berlin
- Role: rail
- Tier: 3 (3c) - CC BY 4.0 per VBB's dataset page
- Rests on: docs/data_sources.md:1882-1893
- Decided by / when: licence-read 2026-09-28; owner wording 2026-09-28
- What would flag it: VBB on logos or official status
- Safety net: notice (app/components.py:1804-1811)
- Strengthen: none needed

#### ROMA-SUAP and ANNCSU - SUAP register (Roma Capitale); ANNCSU civic numbers (Agenzia delle Entrate, ISTAT)
- Cities: Rome
- Role: register; address join
- Tier: 3 (3c) - CC BY 4.0 each
- Rests on: docs/data_sources.md:1558-1574; italy.md:14-15
- Decided by / when: licence-read 2026-09-24; owner wording 2026-09-24
- What would flag it: none recorded
- Safety net: notices (app/components.py:1191-1207); publish-structural (docs/privacy_verdicts.md:52)
- Strengthen: none needed

#### FIRENZE - Four activity layers (Comune di Firenze)
- Cities: Florence
- Role: register
- Tier: 3 (3c) - CC BY 4.0 on every dataset and the Note legali
- Rests on: docs/data_sources.md:2441-2451
- Decided by / when: brief licence read 2026-09-30
- What would flag it: none recorded
- Safety net: notice (app/components.py:2009-2017); page caption (app/pages/136_Florence_Heatmap.py:49); publish-structural (docs/privacy_verdicts.md:104)
- Strengthen: none needed

#### GCBA - Usos del Suelo survey, Parcelas, Subte: Estaciones (Gobierno de la Ciudad de Buenos Aires)
- Cities: Buenos Aires
- Role: register; parcel join; rail
- Tier: 3 (3c) - CC BY 2.5 AR (Parcelas resources 4.0); one credit satisfies both
- Rests on: docs/data_sources.md:1957-1976
- Decided by / when: licence-read 2026-09-28; owner 2026-09-28
- What would flag it: none recorded
- Safety net: notice with titles, URIs, licence, changes (app/components.py:1844-1857); publish-structural (docs/privacy_verdicts.md:80)
- Strengthen: none needed

#### MELBOURNE-CLUE - CLUE 2024 (City of Melbourne)
- Cities: Melbourne
- Role: register
- Tier: 3 (3c) - CC BY 4.0
- Rests on: docs/data_sources.md:2073-2088
- Decided by / when: licence-read 2026-09-28
- What would flag it: trading names that are a person's own
- Safety net: notice (app/components.py:1912-1918); verdict publish (docs/privacy_verdicts.md:84)
- Strengthen: none needed

#### OS-CPO - Code-Point Open postcode centroids (Ordnance Survey, Royal Mail, ONS)
- Cities: London, Newcastle, Manchester, Birmingham, Edinburgh, Sheffield, Nottingham, Blackpool
- Role: address join (postcode-centroid placement)
- Tier: 3 (3c) - OGL v3, three statements verbatim
- Rests on: docs/data_sources.md:1934-1951
- Decided by / when: licence-read 2026-09-28; owner 2026-09-28
- What would flag it: OS on "Code-Point" mark use
- Safety net: notices (app/components.py:1831, 1887, 2044, 2079, 2103, 2126, 2149, 2172); README credits
- Strengthen: none needed

#### NAPTAN - NaPTAN access nodes, ATCO 940 (Department for Transport)
- Cities: Manchester, Birmingham, Edinburgh, Sheffield, Nottingham, Blackpool
- Role: rail (gate-3 count only, nothing drawn)
- Tier: 3 (3c) - OGL v3; credit displayed on the cautious reading
- Rests on: docs/data_sources.md:2509-2524
- Decided by / when: licence-read 2026-10-02; owner 2026-10-02
- What would flag it: none realistic
- Safety net: notice (app/components.py:2057-2064)
- Strengthen: none needed

### Tier 4 - strongest

#### ZURICH-GASTRO - Gastwirtschaftsbetriebe (Stadt Zürich)
- Cities: Zurich
- Role: register
- Tier: 4 (4a) - CC0; the Reglement it rests on read only via the legal notice's summary
- Rests on: CKAN license_id cc-zero; "Quelle: Stadt Zürich recommended, not required" (docs/data_sources/switzerland.md:39-52)
- Decided by / when: build session 2026-09-30 (DECISIONS.md:928)
- What would flag it: a person-named trade name (12 show the address instead)
- Safety net: courtesy caption (app/pages/139_Zurich_Heatmap.py:57); fetch exits on a licence other than cc-zero; verdict publish (docs/privacy_verdicts.md:107)
- Strengthen: none needed

#### IHK-BERLIN and ALKIS - Gewerbedaten (IHK Berlin); ALKIS Landesgrenze (SenStadt)
- Cities: Berlin
- Role: register; boundary
- Tier: 4 (4b) - CC0 1.0 (CSV) / dl-de/zero-2.0
- Rests on: docs/data_sources/germany.md:16, :28; data_sources.md:1894-1897
- Decided by / when: licence-read 2026-09-28; owner courtesy credit 2026-09-28
- What would flag it: nothing owed
- Safety net: "Business data: IHK Berlin (CC0)." (app/pages/56_Berlin_Heatmap.py:62); publish-structural (docs/privacy_verdicts.md:78)
- Strengthen: none needed

---

### FLAGS

#### A. Sources in use with no licence row in docs/data_sources*.md
- **NTA national GTFS (Dublin rail)**: nothing anywhere (grep for NTA/Transport for Ireland near licence/terms returns nothing). Most serious item in this group.
- **Milan ATM rail layers and gtfs.zip**: declared only, never read (docs/build_briefs/milan.md:382-394).
- **Boundary layers with no licence of their own** (same publisher as a displayed notice, so low risk): Madrid Término municipal (geoportal.madrid.es, spain.md:182); Milan ds2841 (CC-BY only in docs/build_briefs/milan.md:305); Dublin Tailte statutory boundaries (ireland.md:174); Montréal limites administratives (CC-BY only in docs/canada_step0_endpoints.md:225); Vancouver local-area-boundary; Surrey City Boundaries FeatureServer; Calgary erra-cqp9; Edmonton qqvh-dp5m; Toronto Regional Municipal Boundary (canada.md:85-93).
- **Vancouver parcels and tax report**: OGL-Vancouver only in docs/build_briefs/vancouver.md:159; internal use, nothing published.
- **Reference-only (not republished)**: Monterrey operator map PDF, used for gate 3 and Línea 3's colour, "nl.gob.mx's site terms are unread" (mexico.md:50); TfGM's network map, which sets Manchester's line names, order and routing (united-kingdom.md:40); SITEUR, westmidlandsmetro.com, thetram.net, edinburghtrams.com and Wikipedia station counts.

#### B. Required notices not found rendered
- **NTA**: no credit in _NOTICES or on app/pages/19_Dublin_Heatmap.py (searched "NTA", "National Transport", "Transport for Ireland").
- **STM notice** (app/components.py:586-590) has no modification/interpretation sentence, though docs/data_sources/canada.md:118 says "a bare credit does not satisfy it".
- **Milan rail**: docs/data_sources.md:1236-1238 counts the ATM layers under CC BY 4.0, but notice (app/components.py:896-904) credits only "six of the Comune's own registers" and app/pages/20_Milan_Heatmap.py names no rail source.
- **CC BY 4.0 licence URI** (§3(a)(1)(C)) named but not linked in Ville de Montréal (578), STM (586), Tailte (876) and Milan (896); the later notices (Rome, Sydney, REM, Florence) link it. Lower confidence: the docs for 12, 22 and 23 do not say a link is required.

#### C. Pending positions a landed city relies on
- **Milan rail licence**: the "separate read-licence job before the deploy gate" (docs/build_briefs/milan.md:382-384) was never recorded as done.
- **Barcelona notification**: "not yet sent" since 2026-09-22 (docs/data_sources.md:333; docs/notifications/barcelona-city-council.md:58-63).
- **Monterrey**: nl.gob.mx's terms are unread (mexico.md:50); low stakes, since only a colour and a count are used.
- **Zurich**: the Reglement über offene Verwaltungsdaten was "not read beyond the legal notice's summary" (switzerland.md:51-52).
- **London and the UK six**: OS's third-party style guide not read, owner said skip (docs/data_sources.md:1949).
- **Stale pointers, not legal gaps**:
  - Privacy rows (docs/privacy_verdicts.md:147-152) and notice entries (docs/data_sources.md:2487 and siblings) cite docs/decisions_drafts/uk-six.md, which is no longer in the tree. The entries now sit at DECISIONS.md:14281 onward.
  - app/components.py:2211 still says Geostat's wording is "flagged for review", though the owner approved it (DECISIONS.md:15982).
  - docs/data_sources/spain.md:346-379 still describes Barcelona's terms as read only from the Archive. The live read of 2026-09-22 is recorded at docs/data_sources.md:1114.

#### Consistency note for cross-group ordering
The project's own record ranks the Canadian municipal OGLs at tier 2 because they "terminate automatically on breach".

- **UK sources**: the record never says whether OGL v3 does the same. That covers FSA, FSS, OS and NaPTAN (grep: no match). The Canadian OGLs descend from it, so verify before giving the UK sources a tier other than the Canadian ones.
- **Ottawa and Waterloo**: their records are silent on termination as well.

---

## Appendix C - France, Norway, Romania, Sweden, Denmark, Czechia, Netherlands, Latvia

## EU2 - notice positions (France, Norway, Romania, Sweden, Denmark, Czechia, Netherlands, Latvia)

Read-only, from the project's own record (2026-10-02). Entries ordered weakest first.
_NOTICES line numbers are the tuple's title line in app/components.py.

OpenStreetMap (central, no entries here): rail geometry for Lille (metro lines), Montpellier, Strasbourg, Le Havre, Caen, Rouen (Regional), Brno (geometry), Plzen, Olomouc, Ostrava, Liberec (Regional), Most (Regional), Stockholm, Goteborg, Copenhagen, Aarhus, Odense, Bucharest, Den Haag, Liepaja, Daugavpils; line colours for Oslo and Bergen; boundaries for Bucharest (plus its six sectors), Stockholm (plus naming), Goteborg (plus Molndal naming), Copenhagen, Aarhus, Odense, Prague, Brno, Plzen, Olomouc, Ostrava, Liberec, Most, Amsterdam, Rotterdam, Den Haag, Liepaja, Daugavpils; address joins for Bucharest (address points) and Aarhus/Odense (osak:identifier points); gate-3 counts for most French tram cities.

---

### Tier 1

#### NL-DH - Horecavergunningen layer (Gemeente Den Haag)
- Cities: Den Haag
- Role: register (food service)
- Tier: 1a - silent layer; the city's own site terms name database rights, and the owner proceeds on a precedent
- Rests on: "SILENT and ambiguous; the owner proceeds on Amsterdam's precedent"; Databankenwet art. 8(2) vs "denhaag.nl's site terms name database rights" (docs/data_sources.md:2457-2461; docs/data_sources/netherlands.md:17)
- Decided by / when: owner (2026-09-30, call C1)
- What would flag it: Gemeente Den Haag, on its reserved database right; the layer sits on an internal ArcGIS account (GemeenteDenHaagIntern) and was last edited 2025-05-23
- Safety net: notice "Gemeente Den Haag" (app/components.py:2022), page states the 2025-05-23 edit and "not a complete or current record"; AANVRAGER/KVKNUMMER/RECHTSVORM never requested, fetch stops if one arrives; privacy PASS (docs/privacy_verdicts.md:106); removal rule
- Strengthen: written confirmation from the Gemeente, or swap to Rotterdam's Gemeenteblad-notice method (KOOP, Auteurswet art. 11)

#### RO-DSVSA - Registered food units lists (DSVSA Bucuresti / ANSVSA)
- Cities: Bucharest
- Role: register (food only)
- Tier: 1b - no terms page at all; an "all rights reserved" footer read as website-only
- Rests on: "Toate drepturile rezervate is a website footer, which governs site content, not the data (the New York situation)" (docs/data_sources.md:2118-2123; docs/data_sources/romania.md:13 "License SILENT")
- Decided by / when: owner (2026-09-28/29; notice wording 2026-09-29)
- What would flag it: DSVSA or ANSVSA, on the footer's reservation; both hosts serve a "Verifying your browser" challenge to scripts, and the owner fetched the 17 files by hand in a browser (romania.md:13)
- Safety net: notice (displayed by choice; app/components.py:1938) credits DSVSA, says no licence is stated, lists changes, disclaims endorsement; sole traders shown by category only; no address reaches the map; privacy publish (docs/privacy_verdicts.md:86); removal rule
- Strengthen: written permission from DSVSA Bucuresti, or a data.gov.ro listing if one appears

#### SE-STO - Livsmedelstillsyn food-inspection register (Stockholms stad, miljoforvaltningen)
- Cities: Stockholm
- Role: register (food only)
- Tier: 1c - silent item; a harvester says "Begransad" (restricted), the publisher's own feed says public
- Rests on: "A contradiction between a catalog and its publisher is decided for the publisher. The blank license is a silence, not a refusal" (docs/data_sources/sweden.md:27-31)
- Decided by / when: build session reading 2026-09-22; owner notice wording 2026-09-29
- What would flag it: Stockholms stad, or anyone reading dataportal.se's "Atkomstrattigheter: Begransad"; the layer is also frozen (inspections to 2025-10-21)
- Safety net: notice (by choice; app/components.py:1924) claims no licence, states changes, disclaims official status; inspection text never read; privacy publish (docs/privacy_verdicts.md:85); brief_check re-reads the Hub DCAT feed; removal rule
- Strengthen: read the walled dataportalen.stockholm.se record via the Internet Archive (docs/gated_access.md:75), or ask the miljoforvaltningen

#### NL-AMS - Horeca exploitatievergunningen (Gemeente Amsterdam)
- Cities: Amsterdam
- Role: register (food service)
- Tier: 1d - live dataset silent ("Licentie: -"); a retired 2022 catalogue said CC BY; displayed as CC BY by choice
- Rests on: "Displayed as CC BY 4.0 on the owner's choice of 2026-09-24, which satisfies both readings" (docs/data_sources.md:1546-1549; netherlands.md:13)
- Decided by / when: owner (2026-09-24)
- What would flag it: Gemeente Amsterdam; also the city API is to require a key on an unset date (registering is the owner's act)
- Safety net: notice (app/components.py:1177) credits, links CC BY 4.0, states changes, "not the official permit record"; privacy publish (docs/privacy_verdicts.md:51); removal rule
- Strengthen: written confirmation of the licence from the Gemeente (data.amsterdam.nl)

#### FR-GEO - Commune contours and EPCI commune layers (geo.api.gouv.fr)
- Cities: all 26 French cities (scope polygon for each; EPCI or region layer names excluded stations; scope for the five Regional cities)
- Role: boundary and naming
- Tier: 1d (unrecorded) - no licence is recorded for this source anywhere; weak on paper only
- Rests on: nothing recorded; the naming rows say "Same publisher and license as the contour" (docs/data_sources/france.md:118, :123), and the contour rows (france.md:117, 119-166) state no licence
- Decided by / when: build sessions (2026-09-22 to 2026-10-01); never read
- What would flag it: a consistency sweep or check_provenance-style audit (an unread source in use); the publisher objecting is unlikely
- Safety net: not displayed; boundaries are not drawn as data (scope and labels only); removal rule
- Strengthen: run read-licence on geo.api.gouv.fr (and its underlying geometry source) and add a licence row to france.md

#### NL-GVBMAP - GVB network map PDF, colour source (GVB)
- Cities: Amsterdam
- Role: naming/styling (tram line colours read off line badges)
- Tier: 1d (unrecorded) - colours lifted from an agency map whose terms were never read
- Rests on: "Tram colours from GVB's own map (GVB_railnetwerk_31aug_2026.pdf ...), downloaded with the owner's permission" (docs/decisions/2026-09-20.md:3663-3665; netherlands.md:24)
- Decided by / when: build session with owner's permission to download (2026-09-24)
- What would flag it: GVB, on its map or brand (OVapi README: must not imply the site represents GVB; CC0 s4: no GVB marks)
- Safety net: page says "in GVB's own colors" (app/pages/29_Amsterdam_Heatmap.py:71); five lines shifted in lightness; no logo; removal rule (colours are one setting to change)
- Strengthen: read GVB's map terms, or switch to project colours (Riga's precedent)

#### NL-BBGA - Shop-vacancy statistic, bbga indicator BHLOCVKPLEEGSTAND_P (Gemeente Amsterdam, source Locatus)
- Cities: Amsterdam
- Role: page text (quoted figure "about one Amsterdam shop unit in twenty stood empty")
- Tier: 1d (unrecorded) - licence never read; a single quoted figure, not republished data
- Rests on: "The bbga licence - the vacancy figure is quoted, not republished" (docs/build_briefs/amsterdam.md:151; netherlands.md:14)
- Decided by / when: build session (2026-09-24)
- What would flag it: Locatus (a commercial data vendor) or the Gemeente
- Safety net: attributed in page text "by the city's own statistics" (app/pages/29_Amsterdam_Heatmap.py:103-105); removal rule
- Strengthen: read bbga's terms, or replace with the CBS Landelijke Monitor Leegstand figure already licensed for Rotterdam and Den Haag (notice)

---

### Tier 2

#### FR-IDFM - Paris GTFS under Licence Mobilites (Ile-de-France Mobilites)
- Cities: Paris
- Role: rail (Metro 16 lines, trams T3a/T3b)
- Tier: 2a - revocable grant that ends "de plein droit, sans preavis" on breach, and one recorded discharge condition (repository linked from the site) is not visibly met
- Rests on: Art. 3.1 grants "l'affichage public"; "ACCEPTED, and Paris is built on it ... if the grant lapses, Paris is archived" (docs/data_sources.md:288-297, 1299-1352)
- Decided by / when: owner (2026-09-22); licence-read agent (2026-09-22)
- What would flag it: IDFM (or automatic lapse) on Art. 5.4 linking, Art. 5.7 date/update interval, Art. 5.8 supply of modifications; the regulator on L.1115-5 annual declaration (unresolved)
- Safety net: notice verbatim with both prescribed hyperlinks (app/components.py:926); Art. 5.7 snapshot date and "feed valid to" on the page (app/pages/21_Paris_Heatmap.py:46-56); stricter reading adopted over IDFM's own "Licence Ouverte" page (data_sources.md:1354-1359); no IDFM plan used (CC BY-NC-ND); archive-not-delete posture
- Strengthen: link the public repository from the site (Art. 5.8); upload the station table as a ressource communautaire (data_sources.md:1332-1339); ask the regulator about L.1115-5

#### FR-TIS - Reseau urbain Tisseo GTFS, ODbL 1.0 (Tisseo / Toulouse Metropole)
- Cities: Toulouse
- Role: rail (Metro A-B, Tram T1, Teleo)
- Tier: 2b - share-alike licence with an OPEN s4.4 question on the committed station CSV, and s4.6 discharged only "provided it stays linked"
- Rests on: "Contains information from Reseau urbain Tisseo ... ODbL"; "OPEN - the station CSV under s4.4" (docs/data_sources.md:1361-1401; docs/licenses/odbl-toulouse-rennes.md)
- Decided by / when: build session / licence read (2026-09-23); NAP Conditions Particulieres correction (2026-09-29, DECISIONS.md:6357-6370)
- What would flag it: Tisseo / Toulouse Metropole or an ODbL enforcer, on share-alike of the station CSV (and the unverified mean-coordinate fallback, which the NAP files under "ajout de coordonnees")
- Safety net: notice verbatim s4.3 (app/components.py:953); page credit with dataset date (app/pages/23_Toulouse_Heatmap.py:54-57); CGU read clean (no indemnity, marks clause excludes data); removal rule
- Strengthen: put the ODbL notice on outputs/toulouse station CSVs; resolve PLAN.md:159 (fallback check); link the repository from the site

#### FR-STAR - Reseau urbain STAR GTFS, ODbL 1.0 (STAR / Keolis Rennes)
- Cities: Rennes
- Role: rail (Metro a and b)
- Tier: 2b - same shape as Tisseo: s4.4 OPEN on the station CSV, s4.6 relies on a repository link
- Rests on: "OPEN - the station CSV under s4.4, exactly as for Tisseo" (docs/data_sources.md:1403-1429)
- Decided by / when: build session / licence read (2026-09-23)
- What would flag it: STAR / Rennes Metropole or an ODbL enforcer, as Tisseo
- Safety net: notice verbatim (app/components.py:972); page credit with feed window (app/pages/25_Rennes_Heatmap.py:59-61); automated re-read of STAR's CGU (star-cgu-still-clean); removal rule
- Strengthen: as Tisseo (CSV notice, PLAN.md:159 fallback check, repository link)

#### FR-ANG - Angers Loire Metropole network GTFS, ODbL 1.0 (Angers Loire Metropole)
- Cities: Angers
- Role: rail (Tram A, B, C; stations and geometry)
- Tier: 2b - ODbL plus a marks bar ("any other mark" without prior agreement) held off only by keeping the page mark-free
- Rests on: "Built MARK-FREE ... ODbL s2.3(c) leaves marks outside the licence"; the notice names the database by producer and NAP id (docs/data_sources.md:2325-2347; DECISIONS.md:6347-6356)
- Decided by / when: owner (2026-09-30)
- What would flag it: Angers Loire Metropole, if any surface (page, macro map, caption, notice, feed_publisher_name) shows the network brand, or if it reads "Tram A/B/C" labelling as use of a mark
- Safety net: notice (app/components.py:1014); page credit "Transit data (c) Angers Loire Metropole" (app/pages/120_Angers_Heatmap.py:62); pure-extract station table; "If the Metropole objects, the removal rule applies"
- Strengthen: seek the Metropole's consent (reCAPTCHA form; outreach is the last resort); link the repository from the site

#### FR-TAM / FR-MRESO / FR-LIA - Batch ODbL feeds (Montpellier Mediterranee Metropole/TaM; SMMAG "M"/TAG; Le Havre Seine Metropole/LiA)
- Cities: Montpellier (stations only), Grenoble (Regional) (stations and geometry), Le Havre (stations only)
- Role: rail
- Tier: 2c - ODbL kept clean by a state the project must hold (pure-extract station tables; s4.6 via a linked repository)
- Rests on: "Conditions Particulieres ... so the maps owe only the s4.3 notice"; "The pure-extract rule for every French ODbL feed (owner)" (DECISIONS.md:6306-6315, 6357-6370; docs/data_sources.md:2158-2204)
- Decided by / when: licence-read agent (2026-09-29); owner (pure-extract rule 2026-09-29)
- What would flag it: each Metropole/SMMAG on share-alike if a station is renamed, merged or re-coordinated; LiA's site terms claim its colour scheme (colours are the project's own)
- Safety net: notices/70/71 verbatim s4.3 (app/components.py:987, :994, :1002); page credits (e.g. app/pages/111_Montpellier_Heatmap.py:62); no TaM logo; privacy PASS (docs/privacy_verdicts.md:119-126); removal rule
- Strengthen: link the repository from the site; optionally the ODbL notice on each station CSV

#### FR-SIRENE - SIRENE StockEtablissement + INSEE geolocation file, Licence Ouverte 2.0 (INSEE)
- Cities: all 26 (Paris, Marseille, Toulouse, Lille (Regional), Rennes, Le Mans, Besancon, Avignon, Tours, Dijon, Reims, Orleans, Mulhouse, Brest, Saint-Etienne, Nice, Montpellier, Strasbourg, Le Havre, Caen, Rouen (Regional), Bordeaux (Regional), Nantes (Regional), Grenoble (Regional), Valenciennes (Regional), Angers)
- Role: register (all three buckets) and coordinate join
- Tier: 2c - the licence is tier 3 (perpetual, no revocation) and its prescribed credit is displayed, but INSEE adds a STANDING duty to honour each natural person's latest opt-out, with no refresh cadence set
- Rests on: Source : Insee "sous la forme" verbatim; "il est ainsi de votre responsabilite de tenir compte du statut de diffusion le plus recent" (docs/licenses/france-licence-ouverte-2.0.md:56-59, :93-104; france.md:13)
- Decided by / when: licence-read (2026-09-23); build sessions per city (2026-09-22 to 2026-10-01)
- What would flag it: a natural person who opted out after the 2026-09 snapshot, or INSEE, on a stale committed outputs/ snapshot; refresh is also blocked until a NAF 2025 mapping exists (docs/recheck_calendar.md:55)
- Safety net: "Business data: Source : Insee, SIRENE ... and its geolocation file" on every French page, outside the provenance block, enforced by check M of check_provenance.py (e.g. app/pages/21_Paris_Heatmap.py:72, app/pages/100_Le_Mans_Heatmap.py:75); masked rows (statutDiffusion != O) carry no location; StockUniteLegale never mapped; no INSEE logo; privacy publish/PASS for all 26 (docs/privacy_verdicts.md:43-47, 108-127, 140); removal rule
- Strengthen: state a refresh cadence (and do the NAF 2025 mapping so a refresh is possible)

---

### Tier 3

#### FR-LO2 - Tram/metro GTFS feeds declared lov2 on the NAP, not read one by one (each Metropole/AOM)
- Cities: Le Mans (SETRAM), Besancon (Ginko), Avignon (Orizo), Tours (Fil Bleu), Dijon (Divia), Reims (Grand Reims Mobilites), Orleans (TAO), Mulhouse (Solea), Brest (Bibus), Saint-Etienne (STAS), Nice (Lignes d'Azur), Strasbourg (CTS, stations only), Nantes (Regional) (Naolib), Valenciennes (Regional) (Transvilles)
- Role: rail
- Tier: 3c - open licence displayed, but accepted from the NAP's declaration without reading each operator's own terms (LiA's showed a colour claim)
- Rests on: "The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text" (docs/build_briefs/le_mans.md:66; france.md:77-96)
- Decided by / when: build session (France batch kit, 2026-09-30)
- What would flag it: an operator whose site terms claim its line colours or marks; a publisher on the "date of last update" element (several feeds have no feed_info, so the page shows the NAP window and snapshot date)
- Safety net: per-page "Transit data (c) <producer>, via transport.data.gouv.fr, from the feed published for X to Y; snapshot taken Z" (e.g. app/pages/100_Le_Mans_Heatmap.py:62-65), but only when provenance.json exists; no logos; removal rule
- Strengthen: a batch read of each operator's site terms for marks/colour claims; render the credit outside the provenance guard

#### FR-RTM - Marseille GTFS, Referentiel complet (Metropole Aix-Marseille-Provence; exporter Mecatran)
- Cities: Marseille
- Role: rail (Metro 1-2, Tram 1-3)
- Tier: 3c - lov2; read, with the Concedant question (Metropole vs Mecatran) settled for the Metropole
- Rests on: "The Concedant is the body that granted the licence - the Metropole. Naming Mecatran alone would be wrong" (docs/licenses/france-licence-ouverte-2.0.md:162-167; france.md:98)
- Decided by / when: licence-read (2026-09-23)
- What would flag it: the Metropole, if the credit's naming or the date element were read as inadequate (page names RTM "via the Metropole Aix-Marseille-Provence feed")
- Safety net: page credit with snapshot and feed end date (app/pages/22_Marseille_Heatmap.py:51-56, inside the provenance guard); removal rule
- Strengthen: none needed beyond moving the credit outside the provenance guard

#### FR-MEL - MEL WFS layers (stations_metro, tramway_arrets, tramway_lignes, dsp_ilevia:couleurs_lignes) (Metropole Europeenne de Lille, Ilevia co-producer)
- Cities: Lille (Regional)
- Role: rail (stations, tram routes, line colours)
- Tier: 3b - lov2 read layer by layer; the date-of-last-update duty is met with the retrieval date, because the layer has none
- Rests on: "MEL publishes no update date for these layers, so this is the date they were read" (app/pages/24_Lille_Heatmap.py:45-61; france-licence-ouverte-2.0.md:63-65, :188-191, :227-232)
- Decided by / when: licence-read (2026-09-23); build session (2026-09-23)
- What would flag it: MEL or Ilevia on the date element; MEL's institutional site's "Tous droits reserves" (read as web-page-only, a different host); Ilevia's GTFS host carve-out is moot because no GTFS is read
- Safety net: page caption naming MEL and Ilevia, Licence Ouverte 2.0, retrieval date (24_Lille:56-61); five layers each checked individually against MEL's mixed catalogue; removal rule
- Strengthen: none needed (optionally ask opendata@lillemetropole.fr for an update date)

#### FR-ATOU - Agregat des reseaux urbains et interurbains de Normandie, lov2 (Syndicat mixte Atoumod)
- Cities: Caen (stations), Rouen (Regional) (stations)
- Role: rail
- Tier: 3b - lov2, Concedant read (Atoumod, not the Region or Cityway)
- Rests on: "The aggregate's Concedant is Syndicat mixte Atoumod (the licence read 2026-09-30)" (docs/build_briefs/caen.md:76, :99; france.md:91-92)
- Decided by / when: build session licence read (2026-09-30)
- What would flag it: Atoumod on the date element: the brief asked for the resource's last_modified date, the page shows the NAP window and snapshot date
- Safety net: "Transit data (c) Syndicat mixte Atoumod (Twisto/Astuce)" (app/pages/114_Caen_Heatmap.py:62-65; app/pages/115_Rouen_Heatmap.py:62); line geometry is OSM's; removal rule
- Strengthen: show the resource's last_modified date as the brief specified

#### FR-BDX - TBM GTFS, Licence Ouverte 1.0 (Bordeaux Metropole)
- Cities: Bordeaux (Regional)
- Role: rail (Tram A-F)
- Tier: 3b - fr-lo, read by licence-read; credit Bordeaux Metropole with the feed's own date
- Rests on: "Credit Bordeaux Metropole as producer (not TBM, Keolis or ... Mecatran) with the feed's own last-update date" (DECISIONS.md:6327-6332; france.md:93)
- Decided by / when: licence-read agent (2026-09-29)
- What would flag it: Bordeaux Metropole; infotbm.com's marks claim (nothing taken from it)
- Safety net: page credit "Transit data (c) Bordeaux Metropole" with the feed window (app/pages/116_Bordeaux_Heatmap.py:62-65); removal rule
- Strengthen: none needed

#### FR-NAPMETA - transport.data.gouv.fr NAP metadata API (DINUM/NAP)
- Cities: Paris (load-bearing for notice's dates); the French tram batch's "NAP's reading" windows
- Role: support (feed validity dates displayed on pages)
- Tier: 3c - facts (dates) from the national portal; no licence recorded on its row
- Rests on: "Not a feed, and it is here because notice makes it load-bearing" (docs/data_sources/france.md:76)
- Decided by / when: build session (2026-09-23)
- What would flag it: unlikely; an audit for an unrecorded licence
- Safety net: only dates are shown; removal rule
- Strengthen: add the NAP's terms to the row

#### NO-ENT - Ruter and Skyss GTFS via Entur, NLOD 2.0 (Entur AS)
- Cities: Oslo, Bergen
- Role: rail (T-bane, trams, Bybanen)
- Tier: 3b - NLOD with Entur's specified credit and logo displayed; Ruter's app agreement (bars copying Ruter's data) read as governing the app only
- Rests on: "Entur should be credited as the source with the text: Data made available by Entur + (logo)"; Ruter's agreement "read as governing the app, and recorded rather than buried" (docs/data_sources.md:1459-1477; norway.md:22)
- Decided by / when: owner (logo, 2026-09-24)
- What would flag it: Ruter on its APP agreement; Entur if the logo or credit drifts from its rules
- Safety net: notice (app/components.py:1062); credit and unaltered logo on each page (app/pages/26_Oslo_Heatmap.py:62-70; app/pages/71_Bergen_Heatmap.py:66-74); no endorsement use; removal rule
- Strengthen: none needed

#### CZ-KOR - IDS JMK GTFS (KORDIS JMK, data from KORDIS JMK and DPMB)
- Cities: Brno
- Role: rail (tram stops)
- Tier: 3b - CC BY 4.0 under KORDIS's own grant; idsjmk.cz's BY-NC-SA footer read as covering web pages only
- Rests on: "idsjmk.cz's BY-NC-SA footer covers only its web pages" (docs/data_sources.md:2352-2357; czechia.md:27)
- Decided by / when: owner (fetch host and wording, 2026-09-30)
- What would flag it: KORDIS or the City of Brno, if the NC-SA footer were read as reaching the feed
- Safety net: notice, approved word for word (app/components.py:1149); no logos; privacy publish (docs/privacy_verdicts.md:141); removal rule
- Strengthen: none needed

#### CZ-PMDP - PMDP GTFS, gate 3 only (PMDP, via opendata.plzen.eu)
- Cities: Plzen
- Role: reference (per-line stop counts; nothing drawn)
- Tier: 3b - record contradicts itself (CC BY vs no-rights), both permit; credited on the stricter reading
- Rests on: "PMDP's GTFS record contradicts itself ... and either permits use" (docs/data_sources.md:2366-2379; czechia.md:28)
- Decided by / when: build session read (2026-09-30); framing sentence flagged for owner review
- What would flag it: unlikely; PMDP or the City of Plzen
- Safety net: notice (app/components.py:1165); no arms or logo; removal rule
- Strengthen: owner reviews the notice's framing sentence

#### NO-BRREG - Enhetsregisteret sub-units and units, NLOD 2.0 (Bronnoysundregistrene)
- Cities: Oslo, Bergen
- Role: register
- Tier: 3a - NLOD with s5's default sentence displayed and changes stated
- Rests on: "Contains data under the Norwegian licence for Open Government data (NLOD) distributed by Bronnoysundregistrene" (docs/data_sources.md:1431-1444)
- Decided by / when: build session (2026-09-24)
- What would flag it: a sole trader (ENK) whose premises appears; the CSV carries e-mail and phone, never loaded
- Safety net: notice (app/components.py:1030); ENK names replaced by address; contact columns asserted absent; privacy publish (docs/privacy_verdicts.md:48, :93); removal rule
- Strengthen: none needed

#### NO-KV - Matrikkelen Adresse and kommune boundaries, CC BY 4.0 (Kartverket)
- Cities: Oslo, Bergen
- Role: address join and boundary/naming
- Tier: 3a - CC BY 4.0, prescribed "(c) Kartverket" and SSR credit displayed
- Rests on: "Kartverket's terms ... prescribe (c) Kartverket and a link"; stricter reading over the API's "no conditions apply" (docs/data_sources.md:1446-1457)
- Decided by / when: build session (2026-09-24)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1045); address file never shown
- Strengthen: none needed

#### DK-CVR - CVR production units via Datafordeler, CC BY 4.0 (Erhvervsstyrelsen)
- Cities: Copenhagen, Aarhus, Odense
- Role: register
- Tier: 3a - CC BY 4.0 attaching to the data; prescribed name displayed; account closure licence-safe
- Rests on: "Du skal kreditere Det Centrale Virksomhedsregister (CVR) pa et passende sted" (docs/data_sources.md:1479-1490, :336-338)
- Decided by / when: owner (wording 2026-09-24; widenings 2026-09-29, 2026-09-30)
- What would flag it: a personally owned business owner (address shown instead of name); CVRPerson never requested; coNavn never loaded
- Safety net: notice (app/components.py:1080); privacy publish (docs/privacy_verdicts.md:49, :94, :98); removal rule
- Strengthen: none needed

#### DK-DAR - Danmarks Adresseregister via Datafordeler, CC BY 4.0 (Klimadatastyrelsen)
- Cities: Copenhagen (full chain), Aarhus and Odense (Adresse/Husnummer only; point from OSM)
- Role: address join
- Tier: 3a - CC BY 4.0, credit form left to the reuser
- Rests on: "free to fetch, share and adapt, with credit to Klimadatastyrelsen" (docs/data_sources.md:1492-1503)
- Decided by / when: licence-read agent (2026-09-24); owner (wording, widenings)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1097), naming OSM's copies for Aarhus and Odense
- Strengthen: none needed

#### CZ-RES - Registr ekonomickych subjektu, CC BY 4.0 with CSU data conditions (Cesky statisticky urad)
- Cities: Prague, Brno, Plzen, Olomouc, Ostrava, Liberec (Regional), Most (Regional)
- Role: register (activity, legal form, name)
- Tier: 3a - CC BY 4.0, conditions linked, derived data marked
- Rests on: "v pripade sireni dat CSU vznika povinnost uvest podminky teto licence" (docs/data_sources.md:1505-1517)
- Decided by / when: owner (wording 2026-09-24; titles widened 2026-09-30)
- What would flag it: a natural person (ÚOOÚ's 2019 fine concerned RŽP, not RES); natural persons at their own seat are excluded
- Safety net: notice (app/components.py:1113); FORMA guard; privacy publish (docs/privacy_verdicts.md:50, 141-146); removal rule
- Strengthen: none needed

#### CZ-RUIAN - RUIAN address exports via INSPIRE ATOM, CC BY 4.0 (CUZK)
- Cities: Prague, Brno, Plzen, Olomouc, Ostrava, Liberec (Regional), Most (Regional)
- Role: address join
- Tier: 3a - CC BY 4.0 with the prescribed "CUZK, 2026" credit; the VDP app's automated-extraction ban sidestepped via ATOM
- Rests on: "The credit FORMAT is prescribed: CUZK, [rok]" (docs/data_sources.md:1519-1530; docs/build_briefs/prague.md:378)
- Decided by / when: owner (wording 2026-09-24)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1125)
- Strengthen: none needed

#### CZ-ROPID - PID GTFS (ROPID)
- Cities: Prague
- Role: rail (Metro A, B, C)
- Tier: 3a - CC BY, author and changes named; logos need consent and are not used
- Rests on: "je nutne uvest autora a pripadne provedene zmeny" (docs/data_sources.md:1532-1542)
- Decided by / when: owner (wording 2026-09-24); Flora added while closed (owner)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1136)
- Strengthen: none needed

#### LV-VZD - Cadastre premise groups and cadastral maps; State Address Register aw_eka.csv, CC BY 4.0 (Valsts zemes dienests)
- Cities: Riga, Liepaja, Daugavpils
- Role: register (shops and services) and address join
- Tier: 3a - CC BY 4.0 under VZD's data-use rules, changes described, VZD's source wording for the address register
- Rests on: "credit the source, link the licence, and describe the changes made" (docs/data_sources.md:1624-1630; latvia.md:43)
- Decided by / when: licence-read (2026-09-24, 2026-09-30); owner (wording)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1273); address file not shown; privacy (docs/privacy_verdicts.md:64, :99, :100)
- Strengthen: none needed

#### LV-GEORIGA - Address points, neighbourhoods, degrading buildings, CC BY 4.0 (Rigas valstspilsetas pasvaldiba, GEO RIGA)
- Cities: Riga
- Role: address join and boundary
- Tier: 3a - CC BY 4.0; the merged outline is never called the city boundary
- Rests on: "MUST NOT SAY that the merged neighbourhood outline is Riga's administrative boundary" (docs/data_sources.md:1632-1639; latvia.md:34, :42)
- Decided by / when: owner (wording 2026-09-24)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1292)
- Strengthen: none needed

#### NL-CBS - Landelijke Monitor Leegstand 2025 table 1, CC BY 4.0 (CBS)
- Cities: Rotterdam, Den Haag
- Role: page text (vacancy figures)
- Tier: 3a - CC BY 4.0, recalculation stated
- Rests on: "credit CBS, link the licence, and say when a figure is recalculated" (docs/data_sources.md:1601-1611)
- Decided by / when: owner (2026-09-24; Den Haag 2026-09-30)
- What would flag it: unlikely
- Safety net: notice (app/components.py:1240)
- Strengthen: none needed

---

### Tier 4

#### SE-GBG - Livsmedelsverksamheter CSV distribution, CC0 1.0 (Goteborgs Stad)
- Cities: Goteborg
- Role: register (food only)
- Tier: 4b - CC0, but only on the distribution node; the dataset node is silent
- Rests on: "dcterms:license ... CC0 is on the CSV DISTRIBUTION's node ... not the dataset's" (docs/data_sources/sweden.md:33-40)
- Decided by / when: build session (2026-10-01)
- What would flag it: a change to the distribution's licence (fetch_sources.py exits if CC0 stops being named)
- Safety net: courtesy credit with CC0 on the page (app/pages/137_Goteborg_Heatmap.py:55); privacy PASS (docs/privacy_verdicts.md:105)
- Strengthen: none needed

#### NL-OVAPI - National GTFS gtfs-openov-nl.zip, CC0 (OVapi; GVB and RET data)
- Cities: Amsterdam, Rotterdam
- Role: rail (GVB metro and trams; RET metro and trams)
- Tier: 4b - CC0 via the producer's LICENSE.TXT; the sibling file's weaker README was avoided rather than answered
- Rests on: "These works are available under CC0 1.0 Universal ... Choosing it AVOIDS the README question" (netherlands.md:24, :30)
- Decided by / when: build session (2026-09-24)
- What would flag it: GVB/RET on marks or implied representation (README; CC0 s4)
- Safety net: no marks; snapshot window on pages (app/pages/29_Amsterdam_Heatmap.py:54-57)
- Strengthen: none needed

#### CZ-ROS02 - ROS02 active establishments (Digitalni a informacni agentura)
- Cities: Prague, Brno, Plzen, Olomouc, Ostrava, Liberec (Regional), Most (Regional)
- Role: register (location)
- Tier: 4a - podminky-uziti declares no authorial work, no database right, no personal data; narrowMatch CC0
- Rests on: "Data ... je tak mozne bez omezeni vytezovat, zuzitkovat a opetovne uzivat" (docs/build_briefs/prague.md:228-240; czechia.md:13)
- Decided by / when: build session read (2026-09-24)
- What would flag it: ÚOOÚ on natural persons (its 2019 fine was RŽP-based; RŽP not used)
- Safety net: natural persons shown by address, at-own-seat excluded; privacy publish (docs/privacy_verdicts.md:50, 141-146)
- Strengthen: none needed

#### NL-BAG - BAG verblijfsobjecten (winkelfunctie), Public Domain Mark (Kadaster, via the city API or PDOK)
- Cities: Amsterdam, Rotterdam, Den Haag
- Role: register (shops and services)
- Tier: 4a - Public Domain Mark; only national BAG fields read (the city's BAG-plus additions carry no licence)
- Rests on: "License Public Domain Mark (Kadaster; PDOK: no conditions) - PERMITTED, nothing to display" (netherlands.md:14, :16, :18)
- Decided by / when: build session (2026-09-24)
- What would flag it: nobody on licence; units also registered as dwellings are left off (privacy)
- Safety net: page credit (app/pages/138_Den_Haag_Heatmap.py:53)
- Strengthen: none needed

#### NL-KOOP - Gemeenteblad exploitation-permit notices (KOOP, official publications)
- Cities: Rotterdam
- Role: register (food service, rebuilt from notices)
- Tier: 4a - official publications (Auteurswet art. 11), CC0 declared
- Rests on: "KOOP's notices (Auteurswet art. 11, CC0 declared) ... need no notice" (docs/data_sources.md:1608-1609; netherlands.md:15)
- Decided by / when: build session (2026-09-24)
- What would flag it: a named person in a notice title (titles never read into a pin)
- Safety net: no names shown; privacy publish-structural (docs/privacy_verdicts.md:62)
- Strengthen: none needed

#### LV-VID - Excise-licence register, CC0 (VID, State Revenue Service)
- Cities: Riga, Liepaja, Daugavpils
- Role: register (food service)
- Tier: 4a - CC0
- Rests on: "The VID excise register and Rigas satiksme's GTFS are CC0 (read 2026-09-24)" (docs/data_sources.md:1638-1639)
- Decided by / when: build session read (2026-09-24)
- What would flag it: a licence holder (holder column never read)
- Safety net: kind and street address only, unit number dropped; privacy (docs/privacy_verdicts.md:64, :99, :100)
- Strengthen: none needed

#### LV-RS - Monthly tram GTFS, CC0 (Rigas satiksme)
- Cities: Riga
- Role: rail (trams 1, 5, 7, 8, 10, 11, 14)
- Tier: 4a - CC0 on the dataset and the operator's own page
- Rests on: "CC0 (dataset, and Rigas satiksme's own open-data page, read 2026-09-24)" (latvia.md:26)
- Decided by / when: build session (2026-09-24)
- What would flag it: nobody
- Safety net: page date credit (app/pages/42_Riga_Heatmap.py:55); colours the project's own
- Strengthen: none needed

---

### FLAGS

#### A. Sources in use with NO licence row in docs/data_sources*.md
1. **geo.api.gouv.fr** commune contours and EPCI/region commune layers - scope and naming for all 26 French cities. No licence on any row (docs/data_sources/france.md:117-166); the naming rows defer to "Same publisher and license as the contour" (:118, :123), which has none.
2. **GVB network map PDF** (`GVB_railnetwerk_31aug_2026.pdf`) - Amsterdam's tram colours (netherlands.md:24; docs/decisions/2026-09-20.md:3663-3665). Terms never read.
3. **bbga / Locatus vacancy indicator** - quoted on Amsterdam's page (app/pages/29_Amsterdam_Heatmap.py:103-105); "The bbga licence" still listed unknown (docs/build_briefs/amsterdam.md:151).
4. **transport.data.gouv.fr NAP metadata API** - has a row (france.md:76) but no licence; it supplies Paris's notice-24 dates.
5. Read-only references with no licence rows (nothing published from them): IDOS per-stop timetables (czechia.md:29-32), Midttrafik timetable PDFs (denmark.md:29), RET map PDFs (netherlands.md:30), DSB's page and Wikipedia gate-3 counts (several), fr.wikipedia for Reims (france.md:82), Tisseo's arrets-itineraire and STAR's tco layers (france.md:99-100), Nominatim spot-check for Bucharest (romania.md:14). Rejseplanen's GTFS was downloaded by an audit script despite the Copenhagen decline (DECISIONS.md:6287-6297); no owner ruling is recorded, and nothing published uses it.

#### B. Required notices or conditions not found rendered
1. **Public repository not linked from the site.** The record discharges ODbL s4.6 (Tisseo, STAR, TaM, M reso, LiA, Angers) and Licence Mobilites Art. 5.8 (IDFM) only "provided it stays linked from the site" (docs/data_sources.md:1330-1331, :1378-1381, :1417-1418; docs/decisions/2026-09-20.md:8101-8105: "an unlinked repo is not an offer"). Searched app/ for `github`, `gitlab`, `repositor`, `expanded-heatmap` and `git`: no link to the repository. For IDFM this is a condition of a grant that ends automatically on breach (Art. 11.1). The About page renders data_sources.md (the method in prose), but the record does not claim that as the discharge.
2. **LO 2.0 "date of last update" for Caen and Rouen.** The brief requires the resource's `last_modified` date (docs/build_briefs/caen.md:76, :99). The pages show the NAP window and snapshot date instead (app/pages/114_Caen_Heatmap.py:59-65; 115_Rouen same template). The other no-feed_info lov2 cities (Avignon, Tours, Dijon, Mulhouse, Saint-Etienne, Strasbourg, Le Havre, Nantes, Grenoble, Valenciennes, Montpellier) use the same NAP-window substitute. Arguable, but not what the brief says.
3. **Operator credits depend on provenance.json.** Every French transit credit, Paris's Art. 5.7 date (app/pages/21_Paris_Heatmap.py:46-56) and Lille's MEL credit (24_Lille:51-64) render only if provenance.json exists and parses. The Insee line was moved out of that guard for this reason (check M); the operator credits were not. Entur's credit is outside the guard, with its logo.
4. **OpenStreetMap rail-geometry enumeration** (app/components.py:750-801) does not name Montpellier, Strasbourg, Le Havre, Caen or Rouen line geometry, Stockholm's Tunnelbana and boundaries, or Bucharest's metro, boundary, sectors and address points. The record relies on notice's map-corner credit for these (docs/data_sources.md:2112-2113, :2135-2136, :2169-2171). For the central OSM owner to decide.

#### C. Pending or unresolved positions a landed city relies on
1. **Paris - L.1115-5 annual declaration:** "APPLICABILITY UNRESOLVED" (docs/gated_access.md:47; DECISIONS.md:6371-6375; Legifrance was CAPTCHA-walled, so the article was never read).
2. **Paris - Art. 5.6(b) re-share on the NAP:** recorded as "one upload moots the argument" (docs/data_sources.md:1332-1339). Not done: the owner declined a data.gouv.fr account for the ODbL feeds (DECISIONS.md:6306-6309), so Paris rests on the NAP's "Non" example.
3. **Toulouse, Rennes - ODbL s4.4 on the station CSV:** "OPEN" (docs/data_sources.md:1394-1401, :1427-1429). Whether the mean-coordinate fallback fired, breaking the pure-extract rule, is an open PLAN item (PLAN.md:159-164; DECISIONS.md:6316-6320).
4. **SIRENE (26 cities) - standing opt-out refresh duty:** no cadence set (docs/licenses/france-licence-ouverte-2.0.md:93-104; docs/decisions/2026-09-20.md:8027-8033). No refresh is possible until NAF 2025 is mapped (docs/recheck_calendar.md:55).
5. **Stockholm:** the walled dataportalen.stockholm.se record and any city-wide policy are "Still unread" (docs/gated_access.md:75).
6. **Amsterdam:** the bbga licence is still unknown (docs/build_briefs/amsterdam.md:151). The API key becomes mandatory on an unset date and is the owner's to register (docs/data_sources.md:1555-1556).
7. **Plzen - PMDP notice:** "the sentence around it is the build's own wording, flagged for the owner's review" (docs/data_sources.md:2376-2377).

---

## Appendix D - Brazil, Hong Kong, South Korea, Taiwan, Japan

## ASIA_BR - notice positions (Brazil, Hong Kong, South Korea, Taiwan, Japan)

Read-only extraction from the staging worktree at 2a0dbf6f (2026-10-02). Paths are
repo-relative. "Removal rule" = docs/data_sources.md:254-317 (commitment: removal
requests honoured, not argued).

**OpenStreetMap (handled centrally):** Brazil - rail for São Paulo, Belo Horizonte,
Brasília, Salvador, Fortaleza, Porto Alegre, Recife, Santos, and Rio's VLT and SuperVia;
municipal boundaries for all nine. Hong Kong - all rail and the SAR boundary. South Korea -
all rail, station English names and boundaries for all 13 cities. Taiwan - Taichung's and
Taoyuan's route geometry; all of Taipei (Regional)'s rail and names. Japan - English
station names for all 20 cities (names only; geometry is MLIT's).

### Order, weakest first

1a Daegu D-데이터허브 · 1b IBGE CNEFE · 1c SEMAS · 1c Busan LocalDataService · 1c Hiroshima
full list · 1c GeoSampa (status only) · 2a Hong Kong FEHD/DATA.GOV.HK/CSDI · 2b MLIT N03 ·
2b Fukui · 2b MHLW open data · 2b Matsuyama + Sakai · 2b Taoyuan door plates (inside TW-DOOR)
· 2c FIA register · 2c Taiwan door plates · 2c Taiwan rail tables · 2c Rio IPP · 2c Tokyo
catalogue wards · 2c Tokyo own-terms wards · 2c Shibuya · 2c Japan CC BY + fault-cost group ·
3a MLIT 位置参照情報 · 3a MLIT N02 · 3b Seoul KOGL 1 · 3b Japan CC BY no-cost group · 3b
Japan CC BY 2.1 JP group · 4 IPEDF (status only)

---

#### KR-DAEGU - 인허가데이터 monthly files (Daegu Metropolitan City, D-데이터허브; origin 한국지역정보개발원)
- Cities: Daegu
- Role: register
- Tier: 1 (1a) - dataset pages declare no licence at all; the City's own copyright guide asks for prior consultation before using unmarked material, read as not reaching these files.
- Rests on: "every license field in the embedded JSON is null"; guide: 공공누리가 부착되지 않은 자료 ... 사전에 협의한 이후에 이용 - docs/data_sources/south-korea.md:198-221; notice text docs/data_sources.md:1685-1695
- Decided by / when: licence-read agent 2026-09-27; owner accepted the disclosed reasoned position 2026-09-27 (DECISIONS.md:12396)
- What would flag it: Daegu City (copyright 관리책임관), on the ground that unmarked material needed consultation first; the national route (file.localdata.go.kr) that would have avoided it 403ed.
- Safety net: "If Daegu objects, the page comes down" (south-korea.md:226); notice "Daegu Metropolitan City" app/components.py:1326; phone column 소재지전화 never read; privacy verdict docs/privacy_verdicts.md:69 (0 of 67,212).
- Strengthen: the consultation by phone (053-803-3770/3785, owner act), or swap to SEMAS's national file as the satellites did.

#### BR-CNEFE - Cadastro Nacional de Endereços para Fins Estatísticos 2022 (IBGE)
- Cities: São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza (Regional), Porto Alegre (Regional), Recife (Regional), Santos (Regional)
- Role: register (and its own coordinate leg)
- Tier: 1 (1b) - no IBGE licence document exists; the grant is federal law, and four restrictive readings were found and NOT resolved in the project's favour.
- Rests on: Decree 8.777/2016 art. 4 "de livre utilização ... pela sociedade"; Lei 14.129 art. 29; readings A-D (2009 IBGE email, União-only waiver, Lei 5.534 secrecy, not on dados.gov.br) - docs/data_sources/brazil.md:72-104
- Decided by / when: licence-read 2026-09-23 (working not kept in the repo, brazil.md:69-70); owner decided to proceed on the law, "the Philadelphia shape", 2026-09-23 (docs/decisions/2026-09-20.md:6469)
- What would flag it: IBGE (dissemination policy not contemplating third-party sites; © IBGE on its PDFs); an individual under LGPD (art. 29's proviso makes privacy a licence condition).
- Safety net: notice "IBGE (Brazil)" app/components.py:1213 (IBGE's own Fonte form, changes, no endorsement); description text never shown at an address that is also a dwelling (brazil.md:112-119); privacy verdicts docs/privacy_verdicts.md:53-61; removal rule.
- Strengthen: written confirmation from IBGE that third-party republication with citation is fine (the 2009 thread's second reply suggests it would be).

#### KR-SEMAS - 상가(상권)정보, data.go.kr 15083033 (Small Enterprise and Market Service, 소상공인시장진흥공단)
- Cities: Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang, Daejeon, Gwangju
- Role: register (with its own WGS84 point)
- Tier: 1 (1c) - the dataset carries the publisher's own "이용허락범위 제한 없음", but SEMAS's site copyright policy (consult before using non-KOGL material) is read as homepage-only, and the 소상공인365 notices the listing cites are unread.
- Rests on: "declares 이용허락범위 제한 없음 in the page, Schema.org and DCAT ... SEMAS's website copyright policy asks for a consultation ... read as covering the homepage's content" - docs/data_sources.md:2141-2151
- Decided by / when: licence-read agent 2026-09-29; owner, "as for Daegu", 2026-09-29 (DECISIONS.md:6853-6858)
- What would flag it: SEMAS, on its copyright policy or on terms in the unread 소상공인365 notices; data.go.kr FAQ 186's no-distortion rule if counts were presented as SEMAS's.
- Safety net: notice app/components.py:1955 (credit, licence label, counts stated as the project's, no endorsement); privacy verdicts docs/privacy_verdicts.md:87-92, 135-138; removal rule ("Any objection is honoured", data_sources.md:2150).
- Strengthen: read the 소상공인365 notices from a Korean vantage point, or a written OK from SEMAS.

#### KR-BUSAN - LocalDataService Open API, 구군 인허가포털 (Busan Metropolitan City, Big-데이터웨이브; source 행정안전부)
- Cities: Busan
- Role: register
- Tier: 1 (1c) - an explicit portal policy grants free use including commercial, but the portal terms' 제14조 (platform-authored IP, no republication without consent) is read as not reaching API output; machine metadata is unreliable.
- Rests on: "영리 목적의 이용을 포함한 자유로운 활용이 보장됩니다"; 제14조 "Read as covering only works the platform itself authored ... restrictive reading ... recorded, not adopted" - docs/data_sources/south-korea.md:171-193
- Decided by / when: licence-read agent 2026-09-27; owner accepted the 제14조 reading 2026-09-27 (DECISIONS.md:12396)
- What would flag it: Busan's platform, claiming the API output as its own IP under 제14조②; terms are silent on caching a frozen feed.
- Safety net: notice app/components.py:1343 (Ministry as source, Big-데이터웨이브 linked, frozen date, no endorsement); `sitetel` refused at load (data_sources.md:1706); privacy verdict docs/privacy_verdicts.md:70; "Any objection from Busan is honoured" (south-korea.md:193).
- Strengthen: a written OK from Busan's portal, or source the same Ministry records from a host declaring 제한 없음.

#### JP-HIROSHIMA - 【窓口申請】食品営業許可施設一覧（市内全て） (Hiroshima City, via DataEye 5672)
- Cities: Hiroshima
- Role: register
- Tier: 1 (1c) - PDL 1.0 is declared on a DataEye dataset, but the full-list file has no entry of its own; that the dataset licence covers it is the owner's reading (the website terms give way only to a "special provision").
- Rests on: "Whether that dataset-level license covers the full-list file, which has no entry of its own, was the one open point: the owner accepted the permitting reading" - docs/data_sources/japan.md:146
- Decided by / when: owner 2026-09-24 (japan.md:146); fault-based 第3条 cost clause accepted country-wide 2026-09-24 (docs/decisions/2026-09-20.md:2366)
- What would flag it: Hiroshima City, saying the full list is under its website's default terms, not the dataset's PDL.
- Safety net: notice app/components.py:1553 (DataEye's 出典 pattern, processed by this project, no endorsement); privacy verdict docs/privacy_verdicts.md:134; removal rule.
- Strengthen: ask the city (or DataEye) to list the full-list file under dataset 5672, or a written note that PDL covers it.

#### BR-GEOSAMPA - estacao_metro / estacao_trem WFS (Prefeitura de São Paulo, GeoSampa) - status only
- Cities: São Paulo
- Role: rail (which lines operate and the gate-3 count; never drawn)
- Tier: 1 (1c) - the declared CC BY-SA 4.0 may not reach these layers (author is the State's Metrô, "License Not Specified"); the question was avoided by reading only a fact, not answered.
- Rests on: "the question is AVOIDED, not answered ... GeoSampa is used only to decide WHICH lines operate - a fact read from it" - docs/data_sources/brazil.md:147-184
- Decided by / when: licence-read agent 2026-09-23; owner 2026-09-23 (docs/decisions/2026-09-20.md:5922)
- What would flag it: Metrô or the Prefeitura only if the project reproduced geometry; low exposure as used.
- Safety net: geometry drawn from OSM (notice); no GeoSampa notice rendered, none claimed owed; removal rule.
- Strengthen: none needed while geometry stays OSM's; email geosampa@prefeitura.sp.gov.br first if the build ever wants its geometry (brazil.md:183-184).

#### HK-FEHD - FEHD licence registers via DATA.GOV.HK, and FEHD's points on the CSDI Portal (HKSAR Government / FEHD)
- Cities: Hong Kong
- Role: register (DATA.GOV.HK XML) and placement (CSDI points, joined by licence number)
- Tier: 2 (2a) - permissive grant, but an uncapped indemnity for claims arising "directly or indirectly", no notice-and-defend, paired with a non-infringement disclaimer; CSDI's terms carry the same.
- Rests on: "you shall indemnify the Government ... which in any case arise directly or indirectly in relation to your use" - docs/data_sources.md:335, 359-387; CSDI extension :404-410
- Decided by / when: owner 2026-09-22 (DATA.GOV.HK, docs/decisions/2026-09-20.md:9454) and 2026-09-24 (CSDI, with the switch from ALS)
- What would flag it: any third party alleging infringement of their rights against the Government over the republished data; the Government could pass costs on without telling the project.
- Safety net: notice app/components.py:1255 (source, IP acknowledgement, attribution to Government, FEHD, DATA.GOV.HK and CSDI); registers carry shop sign only, no licensee name; privacy verdict docs/privacy_verdicts.md:63; removal rule named as the escalation cut-off (data_sources.md:382-384).
- Strengthen: none available short of dropping the source; keep the three conditions (data_sources.md:389-402) exact.

#### JP-N03 - 国土数値情報 行政区域 N03-2025 (MLIT; geometry derived from GSI's 数値地図)
- Cities: all 20 Japanese cities (Kobe, Osaka, Sapporo, Fukuoka, Kyoto, Tokyo, Yokohama, Hiroshima, Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Hakodate, Kagoshima, Okayama, Kōchi)
- Role: boundary (picks stations, anchors labels; never drawn)
- Tier: 2 (2b) - CC BY 4.0, but permitted only while no N03 outline is ever drawn: reproducing the boundaries needs GSI approval under the Survey Act, ambiguous and "not resolved in this project's favor".
- Rests on: 原典表示 says reproduction needs GSI's approval; "The verdict holds only while that stays true" - docs/data_sources/japan.md:127
- Decided by / when: licence read 2026-09-24; recorded as NEVER DRAWN 2026-09-24 (docs/decisions/2026-09-20.md:2379-2398)
- What would flag it: GSI / MLIT, if a map drew a city outline (or arguably if picking stations were read as reproduction).
- Safety net: rule in `pipeline/countries/japan.py` (japan.md:127) and every brief; rendered as "stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; not drawn)" e.g. app/components.py:1419-1420.
- Strengthen: render the MLIT 出典 form with its URL and the CC BY 4.0 link (see Flags B); GSI application or MLIT question only if an outline is ever wanted.

#### JP-FUKUI - 食品衛生法に基づく営業許可施設一覧 and 環境衛生関係施設一覧 (Fukui City)
- Cities: Fukui
- Role: register
- Tier: 2 (2b) - CC BY-SA (site default, no version), so share-alike binds the project's own output; the site policy's §4 open-ended prohibited acts were accepted knowingly.
- Rests on: 「…基本ライセンスは…CC－BY－SA（表示－継承）とします。」; "§4's open-ended prohibited acts accepted knowingly (owner, 2026-10-01; Taoyuan's pattern)" - docs/build_briefs/fukui.md:182-200; docs/data_sources/japan.md:150
- Decided by / when: licence-read agent 2026-10-01; owner took the BY-SA 4.0 offer 2026-10-01 (docs/decisions_drafts/staging.md:535); notice and LICENSE wording accepted at the owner's batch calls 2026-10-02 (DECISIONS.md:15620-15627)
- What would flag it: Fukui City, under §4's undefined prohibited acts; a reuser if `outputs/fukui/` were not actually offered under BY-SA.
- Safety net: notice app/components.py:1632 (city, titles, URLs, CC BY-SA, processed, BY-SA 4.0 offer); LICENSE:62-71; privacy verdict docs/privacy_verdicts.md:156.
- Strengthen: keep the LICENSE section and notice together on every republish; none needed beyond that.

#### JP-MHLW - 食品衛生申請等システム open data (Ministry of Health, Labour and Welfare)
- Cities: Fukuoka, Tokyo (Chūō, Minato, Shinjuku, Kōtō slices), Hiroshima, Matsuyama, Toyama (points only), Kumamoto, Nagasaki, Utsunomiya, Kitakyushu, Sakai (notifications only), Kagoshima, Okayama (sole source). Fukui: count control only, not used.
- Role: register (and its own point where the block join misses)
- Tier: 2 (2b) - PDL 1.0 via the site terms, but 免責 2) ウ "could be read as barring commercial reuse", held OPEN and fine only while the site stays non-commercial; fault-based 免責 1) エ accepted.
- Rests on: "OPEN (minor): 免責 2) ウ could be read as barring commercial reuse. That is fine while the site is non-commercial" - docs/data_sources/japan.md:128; terms archived docs/licenses/mhlw-food-sanitation-system-terms-2020.pdf
- Decided by / when: read 2026-09-24 (docs/decisions/2026-09-20.md:3228, 2764); cost clause accepted by owner 2026-09-24 (:2366); owner's non-commercial confirmation 2026-10-01 (docs/decisions_drafts/staging.md:622-624)
- What would flag it: MHLW, if the project became commercial, or if pages claimed completeness or accuracy; applicants who consented to publication for MHLW's purposes.
- Safety net: "processed by this project ... holds only filings whose applicants agreed ... not complete" in every user's notice (e.g. app/components.py:1476-1480, 1771-1779); top page linked only; 法人名/法人住所/phones never selected; default-point guard (DECISIONS.md:15630).
- Strengthen: keep the site non-commercial; a written MHLW answer on 2) ウ would close it.

#### JP-BREACH-REPAY - city lists whose terms add 弁償 (repay the city's costs) (Matsuyama City; Sakai City)
- Cities: Matsuyama (five lists, 松山市オープンデータ); Sakai (standing list plus monthly new-permit and closure files)
- Role: register
- Tier: 2 (2b) - CC BY 4.0 with breach-triggered cost clauses that go furthest of any Japanese source (repay the city's own costs); Matsuyama adds a public-order/national-security use bar; Sakai's monthly files rest on the owner's reading that the page's open-data paragraph covers them.
- Rests on: Matsuyama 第5条 "the furthest any Japanese source has gone, still breach-triggered" (docs/data_sources/japan.md:147); Sakai 5 and 8 "本市への弁償", monthly files "covered by that page's own open-data paragraph (owner, 2026-10-02)" (japan.md:154)
- Decided by / when: read 2026-10-02 (staging/batch session); covered by the owner's 2026-09-24 country-wide fault-based acceptance; Sakai monthly-file reading owner 2026-10-02
- What would flag it: either city after a breach of attribution or a prohibited use; Sakai on whether the un-catalogued monthly files are open data.
- Safety net: notices app/components.py:1572, 1717 in each city's prescribed modified-work form; privacy verdicts docs/privacy_verdicts.md:153, 160; 営業者住所 never selected (Sakai).
- Strengthen: none needed beyond exact notices; Sakai could be asked to catalogue its monthly files.

#### TW-FIA - 全國營業(稅籍)登記資料集, data.gov.tw 9400 (財政部財政資訊中心 / Fiscal Information Agency)
- Cities: Taichung, Taoyuan, Taipei (Regional)
- Role: register
- Tier: 2 (2c) - OGDL v1, whose attribution statement is load-bearing (failing it means never licensed at all), with a fault-based §六(三) liability clause and the FIA's own PDPA and "not the register" conditions.
- Rests on: §三(二) "視為自始未取得開放資料之授權"; FIA §二(二) personal data under the PDPA; "Do not present the filtered, geolocated points as the register" - docs/data_sources/taiwan.md:41-42, 52-57
- Decided by / when: licence-read agent 2026-09-23; owner accepted §六(三) for all Taiwan 2026-09-23 (taiwan.md:57); name rule owner 2026-09-23 (taiwan.md:67)
- What would flag it: FIA, or a sole proprietor under PDPA 第51條 if an owner's name were shown (FIA itself refused to publish names, 2026-08-14).
- Safety net: notice app/components.py:1362 (prescribed 顯名聲明, licence link, "This map is not the register", no endorsement); names only when a trade name (taiwan.md:67-72); privacy verdicts docs/privacy_verdicts.md:66-68.
- Strengthen: none needed; keep the 顯名聲明 exact (it is the licence).

#### TW-DOOR - door-plate files (臺中市政府數位發展局; 桃園市政府民政局; 臺北市政府民政局; 新北市政府民政局)
- Cities: Taichung, Taoyuan, Taipei (Regional) (Taipei and New Taipei)
- Role: address join (coordinates only; plates never shown)
- Tier: 2 (2c; Taoyuan 2b) - OGDL v1 with the load-bearing attribution reaching derivatives; Taoyuan's portal FAQ adds that reuse must not mislead or "intentionally or unintentionally jeopardise the City Government's interests", undefined.
- Rests on: "covers derivatives, so the published coordinates carry it though the door-plate table is never published" (docs/data_sources/taiwan.md:41); Taoyuan FAQ 有誤導社會大眾、有意或無意侵害本府利益之虞 (docs/data_sources.md:1666-1671)
- Decided by / when: licence-read agent 2026-09-23 and 2026-09-25; Taoyuan FAQ accepted by owner 2026-09-25
- What would flag it: any of the four bureaus if the 顯名聲明 lapsed (licence void ab initio); Taoyuan on its open-ended "interests" clause.
- Safety net: notices app/components.py:1374, 1386, 1399 (one statement per publisher, licence link, plates not shown, no endorsement); removal rule.
- Strengthen: none needed; for Taoyuan, nothing short of a written OK resolves the FAQ's undefined terms.

#### TW-RAIL - station tables (臺中捷運股份有限公司 144164; 內政部國土測繪中心 捷運車站 73233; 桃園捷運公司 128390; 臺北大眾捷運股份有限公司 131326)
- Cities: Taichung (stations and names), Taoyuan (station points; operator list for gate 3), Taipei (Regional) (operator list for gate 3)
- Role: rail / naming
- Tier: 2 (2c) - OGDL v1 throughout (load-bearing attribution, §六(三)); Taipei Metro's own declaration adds civil and criminal liability for malicious alteration.
- Rests on: "OGDL v1 (license: "1")" rows docs/data_sources/taiwan.md:45, 47, 48, 50; Taipei Metro declaration docs/data_sources.md:1679-1682
- Decided by / when: licence-read agent 2026-09-25; Taipei Metro declaration accepted by owner 2026-09-25
- What would flag it: an operator if its 顯名聲明 were missing, or if the map implied endorsement or used its marks.
- Safety net: notices app/components.py:1374-1407; no operator colours or logos used (colours from OSM or the project).
- Strengthen: none needed.

#### BR-RIO-IPP - Transporte_publico MapServer layers 19 and 18, MetrôRio stations and lines (Prefeitura do Rio / Instituto Pereira Passos, DATA.RIO)
- Cities: Rio de Janeiro
- Role: rail
- Tier: 2 (2c) - CC BY 4.0 at service level, plus the SIURB terms' fault-based liability clause, accepted though it may not even bind non-login users.
- Rests on: "This work is licensed under a Creative Commons Attribution 4.0"; SIURB §6 iv "todos e quaisquer danos, diretos ou indiretos", fault-based - docs/data_sources/brazil.md:125, 135-145
- Decided by / when: licence-read agent 2026-09-23; owner accepted SIURB 2026-09-23 (docs/decisions/2026-09-20.md:5922)
- What would flag it: IPP, for damage caused through use, or if the "sem alteração" clause were later attached to these items (it is item-by-item, brazil.md:128-133).
- Safety net: notice app/components.py:1227 (creator, licence link, data link, modified statement); VLT layer 9 not used.
- Strengthen: none needed; re-check the four items for "sem alteração" before a republish.

#### JP-TOKYO-CAT - ward files on the Tokyo Open Data catalogue (Chūō, Minato, Shinjuku, Kōtō food; Minato, Taitō, Shibuya 生活衛生 registers)
- Cities: Tokyo
- Role: register
- Tier: 2 (2c) - CC BY 4.0 under Tokyo Open Data Terms with the §6 / Chūō §5 fault-based cost clause and a date-of-use notice element.
- Rests on: "Tokyo Open Data Terms §2 ... catalog declares CC-BY-4.0 on every package used ... One combined notice: ... date of use" - docs/data_sources/japan.md:129
- Decided by / when: read 2026-09-24; cost clause accepted by owner 2026-09-24 (japan.md:129; docs/decisions/2026-09-20.md:2366)
- What would flag it: a ward or the Tokyo Metropolitan Government if a credit or the date of use were missing (`check_provenance.py` refuses a roster file without a credit, data_sources.md:1860-1862).
- Safety net: notice app/components.py:1514 built from pipeline/tokyo/credits.py; privacy verdict docs/privacy_verdicts.md:77.
- Strengthen: none needed.

#### JP-TOKYO-OWN - wards on their own terms (Taitō food list; Setagaya food list; Meguro food lists and registers on BODIK)
- Cities: Tokyo
- Role: register
- Tier: 2 (2c) - CC BY 4.0 by each ward's own licence page or terms, each with a cost clause in the accepted fault-based class (Tokyo §6 for Taitō, Setagaya §4, Meguro 第8項); Taitō's site policy bars copying but its licence page names this list.
- Rests on: Taitō "the ward's license page ... puts everything on its オープンデータ一覧 under CC BY 4.0, and this list is on it"; Setagaya §2; Meguro odcs.bodik.jp/131105/tos/ - docs/data_sources/japan.md:131-133
- Decided by / when: read 2026-09-24 (docs/decisions/2026-09-20.md:2331); cost clauses accepted by owner 2026-09-24
- What would flag it: Taitō, reading its site-wide no-copying policy over its licence page; any ward on a missing element of its prescribed credit.
- Safety net: notice app/components.py:1514 via pipeline/tokyo/credits.py:95-101 (Taitō's four elements, Setagaya's §2 form, Meguro's catalogue link); wards mask individual operators at source.
- Strengthen: none needed.

#### JP-SHIBUYA - 131130_food_businesses_list.csv on the ward's ArcGIS site (Shibuya City)
- Cities: Tokyo
- Role: register
- Tier: 2 (2c) - 渋谷区オープンデータ利用規約 (政府標準利用規約 2.0 base, CC BY 4.0 compatible), no cost clause, but terms "may change without notice, so re-read them before each republish" - an act owed every republish.
- Rests on: "§1 grants copying, transmission and adaptation, commercial use included ... The terms may change without notice, so re-read them before each republish" - docs/data_sources/japan.md:130
- Decided by / when: read 2026-09-24
- What would flag it: Shibuya, if its terms changed and a republish went out unread.
- Safety net: notice (§2 pattern), app/components.py:1514; removal contact div-smartcity@shibuya.tokyo (japan.md:130).
- Strengthen: make the re-read a gate item for any Tokyo republish.

#### JP-CCBY-COST - city lists, CC BY 4.0 (Kumamoto: PDL 1.0 / CC BY 4.0) with a fault-based cost clause (Sapporo, Fukuoka, Toyama, Kumamoto, Nagasaki, Kitakyushu, Kagoshima city governments)
- Cities: Sapporo, Fukuoka, Toyama, Kumamoto, Nagasaki, Kitakyushu, Kagoshima
- Role: register
- Tier: 2 (2c) - explicit open licence, each with a breach-triggered cost clause the owner accepted country-wide.
- Rests on: Sapporo 第9条3, Fukuoka 第４条, Toyama 第４条４, Kumamoto "the fault-based class", Nagasaki 第5条, Kitakyushu 第3条, Kagoshima 5(2)/5(3) - docs/data_sources/japan.md:144, 145, 148, 149, 151, 153, 156; acceptance japan.md:163-175
- Decided by / when: Sapporo/Fukuoka read 2026-09-24 (Fukuoka from web-archive copies, re-read 2026-09-28, data_sources.md:1784-1786); the other five read 2026-10-02; owner's country-wide acceptance 2026-09-24 (docs/decisions/2026-09-20.md:2366)
- What would flag it: a city after a credit lapse or a completeness/currency claim (Fukuoka 第４条); Nagasaki's lists are a 2023 snapshot, which the page must not present as current.
- Safety net: notices at app/components.py:1449, 1466, 1592, 1613, 1650, 1692, 1754; "may include premises that have closed"; privacy verdicts docs/privacy_verdicts.md:74-75, 154-155, 157, 159, 162; Sapporo fetched from ckan.pf-sapporo.jp only.
- Strengthen: none needed.

#### MLIT-ISJ - 位置参照情報 block (24.0a) and town-chōme (19.0b) (MLIT)
- Cities: all 20 Japanese cities
- Role: address join (never drawn)
- Tier: 3 (3a) - PDL 1.0, read; but the required notice is rendered only in part (the level names are missing).
- Rests on: "PDL 1.0 allows adaptation and 「商用利用も可能です」 ... MUST DISPLAY ... naming 街区レベル and 大字・町丁目レベル位置参照情報" - docs/data_sources/japan.md:125
- Decided by / when: read 2026-09-24 (japan.md:125)
- What would flag it: MLIT, on an incomplete credit or if placements were presented as MLIT's own.
- Safety net: 出典 and 加工して作成 lines in every Japanese notice (e.g. app/components.py:1418-1419, 1794); "did not make and do not endorse".
- Strengthen: add 街区レベル・大字・町丁目レベル to the shared credit string (see Flags B).

#### MLIT-N02 - 国土数値情報 鉄道データ N02-24 / N02-25 (MLIT)
- Cities: all 20 Japanese cities (N02-25 for Hiroshima and the twelve batch cities)
- Role: rail
- Tier: 3 (3a) - PDL 1.0, read; the credit lacks the URL and processor MLIT's current examples add, recorded as "Check at build" and not closed.
- Rests on: "PDL 1.0, read 2026-09-21 | 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成" (docs/data_sources/japan.md:126); "the N02 credit above lacks [URL and processor]. Check at build" (japan.md:127)
- Decided by / when: read 2026-09-21; gap noted 2026-09-24 (docs/decisions/2026-09-20.md:2399-2401)
- What would flag it: MLIT, on credit form; low.
- Safety net: credit in every Japanese notice (e.g. app/components.py:1419); line colours are the project's.
- Strengthen: add the KsjTmplt-N02 URL and "this project processed" to the shared credit.

#### KR-SEOUL - seventeen 인허가 정보 datasets (Seoul Metropolitan Government, Seoul Open Data Plaza)
- Cities: Seoul
- Role: register
- Tier: 3 (3b) - KOGL Type 1, `제3저작권자: 없음` on every dataset, read from kogl.or.kr; all three duties (linked attribution, no endorsement, describe the statistical change) displayed.
- Rests on: "공공누리 1유형 : 출처표시 (상업적 이용 및 변경 가능) ... 제3저작권자 = 없음" - docs/data_sources/south-korea.md:108-141
- Decided by / when: read 2026-09-22 and 2026-09-24 (build sessions; docs/decisions/2026-09-20.md:15267); notice approved by owner 2026-09-25
- What would flag it: Seoul, on KOGL's moral-rights clause if counts were presented as Seoul's figures.
- Safety net: notice app/components.py:1307; no 대표자/성명 column exists; 138 names withheld; privacy verdict docs/privacy_verdicts.md:65.
- Strengthen: none needed.

#### JP-CCBY-NOCOST - city lists, CC BY 4.0 (Utsunomiya: CC BY / PDL 1.0) with no cost clause (Osaka, Kyoto, Yokohama, Utsunomiya, Kōchi city governments)
- Cities: Osaka, Kyoto, Yokohama, Utsunomiya, Kōchi
- Role: register
- Tier: 3 (3b) - explicit open licence on the source page or portal, nothing owed beyond the credit. Osaka's food CSV rests on the CC BY sentence of the page that links it (owner-accepted).
- Rests on: Osaka 「CC-BY4.0で提供いたします。」 (japan.md:142); Kyoto "Nothing is owed to the City" (:159); Yokohama dataset page + open-data terms (:160); Utsunomiya "Cost: none stated" (:152); Kōchi "Cost: none (第7 limits the city's own liability only)" (:158) - docs/data_sources/japan.md
- Decided by / when: Osaka/Kyoto read 2026-09-24; Yokohama licence-read agent 2026-09-30 (rendered URL placement accepted by owner, call B5); Utsunomiya/Kōchi read 2026-10-02
- What would flag it: a city if a pin were called "currently operating" or the map looked like the city's work; Kyoto if fetched from www.city.kyoto.lg.jp instead of the portal.
- Safety net: notices at app/components.py:1430, 1492, 1532, 1670, 1786; privacy verdicts docs/privacy_verdicts.md:73, 76, 133, 158, 164.
- Strengthen: none needed.

#### JP-CCBY21 - city lists, CC BY 2.1 JP (City of Kobe; Hakodate City)
- Cities: Kobe, Hakodate
- Role: register
- Tier: 3 (3b) - CC BY 2.1 JP declared (badge on each CSV / list page); no cost clause; credit removed if the city asks (art. 5).
- Rests on: Kobe "CC BY 2.1 JP, from the badge on each CSV" (japan.md:143); Hakodate 「このページの本文とデータは クリエイティブ・コモンズ 表示 2.1 日本ライセンス」 (japan.md:155) - docs/data_sources/japan.md
- Decided by / when: Kobe read 2026-09-24, notice approved by owner 2026-09-27; Hakodate read 2026-10-02
- What would flag it: either city on "currently operating" claims (Kobe's page warns closed premises remain).
- Safety net: notices app/components.py:1414, 1740 (出典 form, © line, licence link); sublicensing bar met by LICENSE (japan.md:143); privacy verdicts docs/privacy_verdicts.md:72, 161.
- Strengthen: none needed.

#### BR-IPEDF - geonode:ESTACOES_METRO (IPEDF, Distrito Federal) - status only
- Cities: Brasília
- Role: rail (status check only; not drawn)
- Tier: 4 - recorded as public domain.
- Rests on: "IPEDF geonode:ESTACOES_METRO (public domain) read for status only" - docs/data_sources/brazil.md:32
- Decided by / when: read 2026-09-24 (docs/decisions/2026-09-20.md:4428)
- What would flag it: nothing realistic.
- Safety net: not reproduced.
- Strengthen: none needed.

#### Used but not published (no position needed; listed for completeness)
- Hong Kong ALS (cross-check, ~2,000 lookups cached; "an unresolved reading under which no terms grant use at all - moot for an unpublished check", docs/data_sources/hong-kong.md:33); MTR's station lists (gate 3, "no license declared", hong-kong.md:21 - but see Flags A); TDX not used (taiwan.md:43).
- Gate-3 references: pt.wikipedia (BH, Brasília), Korean Wikipedia (Daegu, Busan), English Wikipedia infoboxes (Gyeonggi satellites, Incheon), Recife's ODbL station file and EMTU's CPGSTM layers (cross-checks, brazil.md:36-37).
- Rejected or not used: Shinjuku/Chūō/Arakawa/Ōta/Kita PDF lists, Tokyo COVID lists, Sendai, Okayama's and Nagasaki's own current pages, CNPJ (japan.md:134-140, 157, 161; brazil.md:186-192).

---

### FLAGS

#### A. Sources in use with NO licence row in docs/data_sources*.md
1. **Tokyo statistical yearbook, table 19-8 (飲食店営業, FY2024)** - its per-ward official counts are PUBLISHED in the Tokyo page's table (app/pages/55_Tokyo_Heatmap.py:92-97, from outputs/tokyo/official_shares.json). Grep for "yearbook" / 東京都統計年鑑 finds no row in docs/data_sources.md or docs/data_sources/japan.md.
2. **e-Stat 衛生行政報告例 FY2024 (MHLW statistics)** - has a "measurement, never drawn" row for Hakodate (docs/data_sources/japan.md:53) but no licence verdict; it is also the source of Kumamoto's published "about three in four of the restaurants licensed" (app/pages/164_Kumamoto_Heatmap.py:78; source named in outputs/kumamoto/official_shares.json). Hakodate's brief asks only for a provenance credit (docs/build_briefs/hakodate.md:200).
3. **Chitetsu's English line map** (chitetsu.co.jp/english/img/trams/trams-linemap.gif) - 23 published Toyama tram-stop English names (pipeline/toyama/config.py:148-153; DECISIONS.md:15175). Named in japan.md:70 but with no licence row or verdict. Smaller one-off name borrowings with no row: Nagasaki 八千代町 from the operator's stop table, Osaka's two operator-signed names, Sakai's two (japan.md:62, 73, 76).
4. **MTR station lists** - recorded "not published" (hong-kong.md:21), yet Light Rail stop 250's displayed name "Hoi Wong Road" was taken from MTR's list over OSM's. One name; no licence declared on the list.

#### B. Required notices not found rendered as the docs require
1. **MLIT 位置参照情報 level names** - japan.md:125 requires naming 街区レベル and 大字・町丁目レベル位置参照情報; every rendered Japanese notice gives only 「出典：位置参照情報ダウンロードサービス（国土交通省）（URL）を加工して作成」 (e.g. app/components.py:1418, 1436, 1794). Searched _NOTICES for 街区 and 町丁目: not present.
2. **MLIT N03 credit** - japan.md:127 lists 出典 with the KsjTmplt-N03-2025 URL, 「…をもとに[作成者名]作成」 and "the license link if relying on CC BY"; rendered as plain "stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; not drawn)" with no URL and no licence link (e.g. app/components.py:1420, 1777). The doc calls MLIT's wording "examples, not fixed", so the missing licence link is the firmer gap.
3. **MLIT N02 URL and processor** - japan.md:127 / docs/decisions/2026-09-20.md:2399-2401 note MLIT's current examples add a URL and the processor; rendered N02 credit has neither (e.g. app/components.py:1419).
4. Everything else checked was found rendered: IBGE (:1213), IPP (:1227), FEHD/CSDI (:1255), Seoul KOGL with link (:1307), Daegu (:1326), Busan (:1343), FIA and three Taiwan 顯名聲明 (:1362-1407), SEMAS (:1955), all 20 Japanese city credits in their prescribed forms (:1414-1798), Tokyo's per-ward elements (pipeline/tokyo/credits.py:95-101), Fukui's BY-SA offer (LICENSE:62-71).

#### C. Positions recorded as pending / unresolved that a landed city relies on
1. **IBGE CNEFE**: four restrictive readings "NOT resolved in this project's favor" (docs/data_sources/brazil.md:95-97); the licence reader's full working "was not kept in the repository" (brazil.md:69-70). Nine cities.
2. **SEMAS**: "The 소상공인365 notices the listing cites are unread (IP-blocked from here)" (docs/data_sources.md:2151). Ten cities.
3. **MHLW 免責 2) ウ**: "OPEN (minor)", fine only while non-commercial (docs/data_sources/japan.md:128). Twelve Japanese cities, Okayama wholly.
4. **MLIT N02 credit**: "Check at build" (japan.md:127), not closed (B3). Twenty cities.
5. **MLIT N03**: drawing "not resolved in this project's favor"; the verdict holds only while nothing is drawn (japan.md:127). Twenty cities.
6. **Daegu**: the consultation "stays available as an owner act, not a prerequisite" (docs/data_sources/south-korea.md:227) - never made.
7. **Busan 제14조** and **Taoyuan FAQ**: restrictive / undefined readings "recorded, not adopted" (south-korea.md:191-193; docs/data_sources.md:1666-1671).
8. **Shibuya**: "re-read them before each republish" (japan.md:130) - a recurring act; no record found of the latest re-read.
9. **Stale pointer**: the twelve batch cities' privacy verdicts and MUST-DO lines cite `docs/decisions_drafts/japan-batch.md` (docs/privacy_verdicts.md:153-164; docs/data_sources.md:2732, 2753, 2775, 2795, 2814, 2836, 2855, 2875, 2894, 2914, 2932, 2951), which does not exist in this tree; the entries are already folded into DECISIONS.md:15048-15536.
10. **Japan batch notices** say "lands with the Japan batch at review time" (docs/data_sources.md:2715 ff.); the owner's landing steps are queued for review time (DECISIONS.md:15620-15629), so the positions above for those twelve cities assume those notices ship in the same push.

Side note (not licence): Daegu's notice says records run "to 2025-09-02" (app/components.py:1331; docs/data_sources.md:1692) while the registry row says rows end 2025-08-31 (docs/data_sources/south-korea.md:14; DECISIONS.md:12109).
