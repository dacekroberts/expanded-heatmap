# Large-transit cities not built - the gap, and why (2026-09-28)

**What this is.** Every city in the world with an expansive rapid-transit
network (roughly 50+ stations or several lines) that this project has not
built, with the reason the record gives. Compiled 2026-09-28 at the owner's
request, from `docs/city_master_list.md` (Built, every band, DISCARDED,
"Countries ruled out", "Current by country"), `docs/global_country_shortlist.md`
and `docs/city_master_list_evidence.md`, checked against a list of the world's
largest systems. It is the starting list for the **re-screens** in the staging
handoff; the master list stays the operative list, and this file is not
counted by `check_master_list_counts.py`.

**Why now.** With the 2026-09-28 review batch (Sapporo, Fukuoka, Kyoto) live,
every city within the original candidate specs is built or banded; what is
left is trams-only (Band T), one-bucket (Band B), access-blocked (D), no page
(N), or Tokyo (A). The large networks below are the ones the specs, or an old
negative, kept out.

"(kn)" marks a network size from general knowledge, not from the record; a
"subway 35" in the record counts route relations in a feed, not stations.

## Discarded (28) - `docs/city_master_list.md`, DISCARDED

| City | Country | Network | Why not covered (the record's words, short) |
|---|---|---|---|
| Doha | QA | Doha Metro, 3 lines (kn) | The commerce register is counts only (screened 2026-09-28, owner) |
| Algiers | DZ | 1 metro line + trams (kn) | No premises list at any level (screened 2026-09-28, owner); its "no urban rail" misfiling corrected |
| Mumbai | IN | Metro 1, 2A, 7, 3; Monorail (kn) | No storefront list on the city's or state's reachable hosts (screened 2026-09-28, owner) |
| Munich, Frankfurt, Cologne | DE | 96 / 86 / ~230 stops (kn) | No premises register on a full enumeration of each catalogue, geoportal and chamber (screened 2026-09-28, owner) |
| Manila | PH | LRT-1, LRT-2, MRT-3 | No business list at any level (re-screened 2026-09-28, owner); the old commuter-rail reason is obsolete |
| Kuala Lumpur | MY | 14 relations | "No register at any level, on three methods" |
| Santiago | CL | L1-L6, L4A | "Coverage fails downtown": 4 central comunas publish no list |
| Valencia | ES | metro + tram | "No premises register", 290 packages read |
| Portland | US | 132 stops in the city | "No classified premises register" |
| Vienna | AT | U-Bahn + 185 tram relations | "No premises register at any level", re-probed twice |
| Nagoya | JP | 102 stations | "No list, and none can be rebuilt" (monthly files hold about half the permits) |
| Hamburg | DE | U-Bahn 4 lines | Currency: its only register is a 2016 retail survey |
| Cairo | EG | 3 lines (kn) | "No register at any level" |
| Athens | GR | 3 lines | No premises register; the national list is from 2018, no addresses |
| Dallas | US | DART ~65 stations (kn) | Currency: the register ends in 2022. **A re-screen on the Texas Comptroller's permit file is already queued** |
| Jakarta | ID | 9 relations | "No activity field" |
| Denver | US | RTD ~50+ stations (kn) | "No address, no classification, no geometry" |
| Budapest | HU | 4 metro lines + trams | "Both routes closed" (the food authority's lookup is behind a CAPTCHA) |
| Sofia | BG | 4 metro relations + trams | "Sofia's 76 datasets include none" |
| Lyon | FR | 4 metro lines + trams | Terms: account required, indemnity, ban on operators' marks |
| Naples | IT | 3 lines + trams | No premises register |
| Atlanta | US | MARTA 38 stations (kn) | Currency: licences stop 2019-22 |
| Tel Aviv | IL | "realistically 1" line | Municipal terms forbid building a database from the data |
| Lima | PE | 4 relations | Coverage: 1 of Línea 1's 9 districts publishes |
| Medellín | CO | 6 relations | "Three closed doors" |
| Honolulu | US | Skyline (small) | No premises register |

## Country ruled out (22) - "Countries ruled out" and the shortlist

| City | Country | Network | Why not covered |
|---|---|---|---|
| Shanghai, Beijing, Guangzhou, Shenzhen, Chengdu, Wuhan, Hangzhou, Chongqing, Nanjing, Xi'an, Tianjin, Suzhou, Zhengzhou, Qingdao | CN | ~150-500 stations each (kn) | **Ruled out 2026-09-28 (owner), high legal barriers**: anti-bot (Shanghai), real-name accounts (Beijing, Shenzhen), terms forbidding redistribution (Shenzhen), no open coordinates, regulated map publishing. Hangzhou's food-licence list is a narrow opening, blocked by a real-name filing duty and placement |
| Moscow, St Petersburg | RU | 250+ / 72 stations (kn) | Excluded: sanctions and access |
| Tehran, Minsk | IR, BY | ~150 / ~37 stations (kn) | Left out like Russia, for wartime concerns (owner, 2026-09-28); not screened |
| Glasgow | UK | 15 stations (kn) | Recorded as "NNDR carries no category"; **wrong** (London's re-screen, 2026-09-28): the VOA list has a description and is ruled out by its terms. The FSA food register is untested for either city |
| Brussels | BE | 69 stations (kn) | Bulk access paid |
| Kyiv | UA | 52 stations (kn) | Excluded for now: active war |
| Auckland | NZ | commuter 5 | Commuter only; licensing not municipal |

## In a band, not built (23)

| City | Country | Network | Band and blocker |
|---|---|---|---|
| Buenos Aires | AR | Subte A–E, H | A - the land-use survey joined to parcels at 99.8%, CC BY 2.5 AR read (2026-09-28, owner) |
| Sydney (City of Sydney) | AU | Sydney Trains and Metro in the LGA | B - the City's FES establishment layer, found on a re-probe (2026-09-28, owner) |
| Newcastle | UK | Tyne and Wear Metro, ~60 stations | B - food only on the FSA register (2026-09-28, owner) |
| Bangkok | TH | MRT, BTS, ARL | D - the BMA's portal refuses this machine (2026-09-28, owner) |
| Riyadh | SA | Riyadh Metro, 6 lines | D - the national open-data portal times out from here (2026-09-28, owner) |
| Perth | AU | Transperth, ~80 stations | N - property land-use codes only, City of Perth (2026-09-28, owner) |
| Ankara | TR | Ankaray, M1–M4 | N - Istanbul's shape: the districts publish no licence lists (2026-09-28, owner) |
| Melbourne (City of Melbourne) | AU | City Loop, Metro Tunnel, CBD trams | B - CLUE covers the City of Melbourne only (2026-09-28, owner) |
| Delhi | IN | Delhi Metro, ~290 stations (kn) | D - the current register behind a CAPTCHA; every Delhi-government host refuses this machine (screened 2026-09-28, owner) |
| Berlin | DE | U-Bahn 9 lines, ~175 stations (kn); S-Bahn | B - IHK Berlin's per-premises register; hairdressers and laundries missing (from the discards 2026-09-28, owner) |
| Istanbul | TR | M1A–M11, 177 stations; T1–T5 | N - pharmacies and opticians only; the districts publish no licence lists (re-screened 2026-09-28, owner) |
| Dubai | AE | Metro Red and Green, 64 stations; tram | D - every host of its licence register refuses this machine (re-screened 2026-09-28, owner) |
| London | UK | 272 stations (kn) | B - food only on the FSA register (re-screened 2026-09-28, owner); no second layer covers central London |
| Stockholm | SE | T-bana, 92 stations | B - passed, food only |
| Singapore | SG | MRT 21 relations | N - the food register is a 2016 snapshot |
| Kaohsiung | TW | ~75 stations (kn) | D - geo-blocked to Taiwan |
| Bucharest | RO | M1-M5, 64 stations | B - food only; the file downloads only in a browser |
| Incheon | KR | 64 stations | B - placed 71.3% by the lift-building join and road interpolation |
| Hyderabad | IN | 6 relations | D - geo-blocked, nothing read behind it |
| Lisbon | PT | 10 subway relations | D - a free account on the national register |
| Helsinki | FI | metro + trams | D - geo-blocked |
| Yokohama | JP | 43 stations | N - no food list in any era |
| Warsaw | PL | 2 lines (kn) | D - geo-blocked |

## Never screened (9)

| Cities | Country | Network (kn) | Why not covered |
|---|---|---|---|
| Bengaluru, Kolkata, Chennai | IN | ~40-80 each | Only India's national catalogue was read (counts, not premises); the city hosts were never asked. Delhi and Mumbai were asked 2026-09-28 (D, discarded) |
| Caracas, Tashkent, Baku | various | ~27-57 stations | No record |
| Panama City, Hanoi, Ho Chi Minh City | PA, VN | ~14-30 stations | No record (small networks) |

## The weakest or oldest reasons among the biggest networks

Recommended first for re-screening (the staging handoff's priority 1):

1. ~~**London**~~ - **done 2026-09-28: Band B, food only** (owner). See the
   master list's Band B and the shortlist's United Kingdom row.
2. ~~**Dubai and Manila**~~ - **done 2026-09-28** (owner): Dubai to Band D
   (blocked before measurement), Manila discarded (no business list).
3. ~~**Istanbul**~~ - **done 2026-09-28: Band N** (owner), pharmacies and
   opticians only.
4. ~~**Berlin**, **Munich, Frankfurt, Cologne**~~ - **done 2026-09-28**
   (owner): the three discarded; Berlin to Band B on its chamber's register.
5. ~~**Delhi and Mumbai**~~ - **done 2026-09-28** (owner): Delhi to Band D
   (a CAPTCHA and geo-blocks), Mumbai discarded. Tokyo was built the same day
   and left the band table.
6. ~~**China's fourteen**~~ - **done 2026-09-28**: ruled out as a country
   (owner), Hangzhou's opening noted.
7. ~~**Algiers**~~ - **done 2026-09-28**: misfiling corrected, then
   discarded (owner). **Buenos Aires** probed the same day (never-screened
   list): see DECISIONS.
