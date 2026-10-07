# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-07 - Oradea's address layer accepted as a join target; Miskolc to R (owner, calls 219, 220)

- **Oradea's licence read:** SILENT. No reuse terms on harta.oradea.ro or oradea.ro; the WFS capabilities' Fees and AccessConstraints "none" are vendor defaults; the GIS portal's About box is the software's licence. Romania's Law 179/2022 (art. 3, 9(1), read through lege5.ro, the official text unreachable) makes public documents reusable, commercially or not, free of charge, short of a licence from the city; data.gov.ro timed out. Precedent: Bucharest's DSVSA (silent, accepted) and the Dallas and Snohomish address joins (join target, nothing displayed).
- **"219 yes":** the layer is accepted as a join target only, never drawn; credit by choice, e.g. "Address points: Primăria Municipiului Oradea (harta.oradea.ro)". One download of the layer (gmgml:NrAdm) is approved, and the owner's browser fetch of DSVSA Bihor's two lists. The single GetFeature did not finish in 590 s, so the layer is fetched in 36 BBOX tiles, one request at a time, into `data/oradea/raw/adrese_nradm_tiles_2026-10-07/`.
- **"220 R":** Miskolc to R on Lausanne's precedent (a register readable only through a paged search goes to R). Hungary now holds no candidate.

### 2026-10-07 - Seven Romanian cities and three Hungarian to Band R; Miskolc kept for one look (owner, calls 215c, 216)

- **RENNS checked in the owner's browser:** `geoportal.ancpi.ro` and `renns.ancpi.ro` answer DNS_PROBE_FINISHED_NXDOMAIN (the names no longer exist), `geoportal.gov.ro` ERR_CONNECTION_TIMED_OUT, as from here. So Timișoara, Iași, Arad, Galați, Ploiești, Craiova and Reșița go to R (215c), reopen condition RENNS reachable or the owner's request to ANCPI.
- **Hungary (216, "we can try miskolc, if fail band R. others can go to R now"):** the bulk-route probe found no API, export, open-data release or bulk extract (OKNYIR, Lechner, kozadatportal.hu, the cities' sites; NÉBIH's food search behind a CAPTCHA); Lechner takes requests for public data (the Trade Act §6/I(3) makes the register public). Debrecen, Szeged and Budapest to R, reopen on a Lechner extract or an OKNYIR export. Miskolc stays in D for one look at its GovCenter register (plain HTML, 200 rows a page, no licence stated); if it fails, R.
- **A precedent to weigh before Miskolc's look:** Lausanne went to R on 2026-10-04 because Vaud's licence register answers only through a paged search ("a bulk extract by request"), and Miskolc's own D row recorded "Paging a search is Lausanne's shape". Put to the owner before any work.
- **Master list:** candidates 69 (A 32, B 33, C 2, D 2: Oradea, Miskolc), R 89, 329 discarded.

### 2026-10-07 - Romania's placement settled: Cluj-Napoca to B, Oradea's address layer to a licence read, seven cities to R after the owner's RENNS check; Pune discarded (owner, calls 215, 218)

- **The address-source probe** (curl, catalogue and capabilities pages only): ANCPI's RENNS address points (INSPIRE AD, RO.ANCPI/AD.RENNS, every urban locality) exist in the INSPIRE record but `geoportal.ancpi.ro` and `renns.ancpi.ro` do not resolve and `geoportal.gov.ro` times out from here, as Bucharest's brief found; ANCPI's buildings likewise. Oradea runs an open WFS, `harta.oradea.ro` service "Adrese", layer `gmgml:NrAdm`, 34,237 address points with house numbers, no licence stated (its capabilities' "none" fields are vendor defaults). Nothing reachable for the other eight: Timișoara's catalogue holds no addresses, Cluj-Napoca's GIS lists only a sample service, Arad's sits behind a login, Ploiești, Galați and Reșița answered nothing usable; Overture and OpenAddresses do not cover them.
- **"215a yes, b yes, c R after allowing me to check RENNS if only inaccessible for you, 218 yes"** (owner, staging's chat):
  - **215a:** Cluj-Napoca D to B, food only, the unplaced share stated: OSM's address join plus the nearest same-side number tier (Palma's code, at most 6 numbers away) and the brief's three repairs place 71.6%. A tier point sits a median 2 house numbers (47 m) from its own address.
  - **215b:** a licence read of Oradea's address layer (running); if it clears, one download of the layer and the owner's browser fetch of DSVSA Bihor's lists go to the owner for approval.
  - **215c:** Timișoara, Iași, Arad, Galați, Ploiești, Craiova and Reșița go to R, reopen condition RENNS or a request to ANCPI, once the owner has checked whether RENNS opens in their own browser (unreachable from here may not mean unreachable everywhere). Their rows stay in D until then. Craiova's and Reșița's downloads are not needed.
  - **218:** Pune discarded (absence): dataset #434 "Commercial Establishments", fetched by the owner through the portal's form, is one sheet of 5 category totals, not premises; #409 "Restaurants" is from 2017. India now holds no candidate.
- **Master list:** candidates 79 (A 32, B 33, C 2, D 12), R 79, 329 discarded; counts by `check_master_list_counts.py --write`, discard evidence checked.
- **Housekeeping:** all 43 Romanian files still in the owner's Downloads are byte-identical to filed copies; the owner may delete them. A scratchpad script named `numbers.py` shadowed Python's standard library module and broke an import; renamed.

### 2026-10-07 - Konya to Band R; Hungary's OKNYIR caps every view at 200 rows (owner, call 217; call 216 pending a probe)

- **Konya (call 217, "217 yes"):** the owner's browser passed the portal's Cloudflare challenge and walked `acikveri.konya.bel.tr`: 232 datasets from 20 organizations, most last modified 2022-2023. The only business points are pharmacies (GeoJSON, 2022), banks and ATMs, none in the project's buckets; the Economy category holds tariffs, produce prices and one district's projects; a `ruhsat` search finds only a count of excavation permits. Moved D to R; reopen if the municipality publishes its workplace licences or a food-business list. Türkiye now holds no candidate (five cities in R). Master list: candidates 80 (D 14), R 79.
- **Hungary (call 216, pending):** in the owner's browser OKNYIR's shop register shows at most 200 rows per search, in the list and the map view alike, with no export; a record's detail page holds the shop's own address in separate postcode, street, street-type and house-number fields, and the trader's own residence or seat in a separate block, never used. Staging recommended R for the four cities; the owner asked first for a probe of bulk routes (OKNYIR and Lechner documentation, the cities' own published shop lists, national portals and NÉBIH), running.
- **Romania, call 215 (pending):** Arad, Galați and Ploiești's files are complete (18, 18 and 17). OSM address objects per city: Arad 15,671, Ploiești 12,295, Oradea 11,746, Timișoara 10,573, Galați 2,491, Reșița 136 (Craiova's count failed on every mirror). Arad's join places 39.7% (981 of 2,469 premises). Route 1, the nearest same-side number tier (Palma's code, at most 6 numbers away, a tie to the lower number, one site): Cluj-Napoca 60.2% to 68.3%, 71.6% with its three repairs; Timișoara 51.6% to 63.7%; Iași 43.9% to 59.9% (the brief's 61.0% skipped the one-site check); Arad 39.7% to 50.1%. A tier point sits a median 2 house numbers (47 to 76 m) from its own address. A probe of other address layers (ANCPI's INSPIRE addresses, RENNS, the cities' GIS portals, Overture, OpenAddresses, data.gov.ro) is running. Craiova, Reșița and Oradea's downloads are held until 215 is answered.
- **The 70% bar, swept at the owner's request:** no built page places under 70% overall (Bucharest 74.9% and Okayama 73.9% are the lowest); the bar is rule 5 of the owner's written bar for reduced-bucket pages (2026-09-29, "about 70% or more placed (Incheon's 71.3%)"), applied since to Japan's food lists, Macau and Romania, and not written in rule_history, category_rules or the address-join skill; Kure (69.4%, call 185) is the one city let through under it. Cities dropped or held for placement: Santa Cruz–La Laguna, Zaragoza, Ino, Tokushima, Saga, Miyazaki, Fuenlabrada, Wakayama (discarded); Macau and Kōfu (R); Shizuoka, Funabashi, Matsudo, Fuji and Kōchi narrowed to personal services. Cleanup found no statement of the bar, or of any placement threshold, on the published site; only each city's own placed share is shown, as a fact.

### 2026-10-07 - Band D's first three Romanian briefs: every one under the 70% placement bar; call 215 put to the owner

- **Briefs written** (owner: "write the briefs for those three now"; three agents, one city each, from the owner's saved DSVSA files, OSM by one Overpass query at a time across the session): `docs/build_briefs/timisoara.md`, `iasi.md`, `cluj_napoca.md`.
  - **Timișoara:** 4,925 kept premises in the city (food service 2,620, food shops 2,160, BUFET 145); OSM's address join places **51.6%** (OSM holds 11,268 address points in the city). Six running tram lines (SMTT: 1, 2, 4, 7, 8, 9), 68 stop names, median gap 336 m (halved rings). The city's CC BY transit dataset (9.3 MB) is a Step 0 download for the owner.
  - **Iași:** 3,063 premises (food shops 1,634, food service 1,429); placed **43.9%**, 61.0% with Incheon's nearest same-side tier (4,551 OSM addresses). Nine tram lines, 57 stops, median gap 399 m; six Copou stops closed for works. The two old files (2021, 2017) fail currency, at most 6 premises lost.
  - **Cluj-Napoca:** 5,626 premises (food shops 2,799, food service 2,721); placed **60.2%** with Bucharest's normaliser, 63.4% with three Cluj fixes (22,217 OSM addresses). Trams 100, 101, 102 read from CTP's timetables; 20 stations, median gap 475 m.
  - Each county numbers its files differently from Bucharest's, so the build maps files to roles per city.
- **Call 215, the placement bar:** the reduced-bucket bar is 70% placed, and Santa Cruz–La Laguna went to the discards at 57.7% (owner, 2026-09-30). All three fall under it; the Cluj agent proposed B with the gap disclosed, a departure from that precedent. Staging recommends Band C for all three, reopen condition a second address layer that reaches 70%, and an OSM address count for the six remaining Romanian cities before more browser acts.
- **Slips:** the Timișoara agent printed about 24 registration numbers and dates from a mislabelled column to its console; the Cluj agent printed about 30 premises addresses (street and number, no names) from file 26, whose address and category columns are swapped; the Iași agent printed DSVSA Iași's own letterhead (the office's address and phone). Nothing was stored or written to a brief. Staging ran `brief_check.py timisoara` twice without the session's Overpass lock while two agents held it in turn, so up to two queries may have overlapped theirs; both met a 504 or 500.

### 2026-10-07 - Calls 206 to 208 accepted; Regional-1's batch ready, calls 210 to 213 put to the owner

- **"206: accept, 207 accept", "208: acept"** (owner, staging's chat):
  - **206:** Yamagata §4's reimbursement, triggered by use and uncapped, accepted (Hong Kong's shape).
  - **207:** Matsumoto's city §6(5) and LinkData Art.18(4), both partly not fault-based and uncapped, accepted; the credit names CC BY 4.0 in the city's format with LinkData's CC BY 3.0 mark and attribution name.
  - **208:** Kawaguchi's 「データ利用のみ自由です」 read permissively: use without ownership, the page's CC BY 2.1 JP grant covering republication.
- **Regional-1 reported its batch** (branch worktree-japan-regional-1, head 9c8a7ddd, nothing pushed, zero drift, privacy 0 for all): Maebashi, Fukuyama, Ichinomiya, Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu, Mito and Morioka on pages 229 to 239 and notices 176 to 186, the block used. It ran fingerprint.py table and re-rendered with the marks.
- **Calls put to the owner:**
  - **210 (call 153 again): Fukushima's 2026 register months** (r0808riyou.csv, r0804-0807biyou.csv). Recommended approving and rebuilding to 2026-08-31 (Ichinomiya's call 128); without them the registers stand at 2026-03-31 beside food at 2026-08-31.
  - **211: Ōita's 2026 register months** (442011_beauty_salon_new, five CSVs; 442011_cleaning_new). Same recommendation.
  - **212: Ōita's own notification list** (442011_licensed_facility, 287,712 B). Recommended approving: a complete Food-shops layer instead of MHLW's partial one; a schema read and a re-render.
  - **213: Gifu's rings.** The measured median nearest-station gap is 545 m (the brief said 641 m), inside the 540-570 m band. Recommended standard rings: the median rests on three close pairs and every JR and private-rail Japanese city is on standard rings. Tradeoff: the rule's letter and Rennes's 541 m point to halved rings (ring share 30.7% against 15.3%).
- **"210 yes, 211 yes, 212 yes, 213 standard rings"** (owner, staging's chat): Fukushima's and Ōita's 2026 register months and Ōita's own notification list are approved downloads from the publishers' hosts, so the registers rebuild to 2026-08-31 and Ōita's Food-shops layer comes from the city's list; Gifu keeps standard rings (median gap 545 m, inside the 540-570 m band; three close pairs, every JR and private-rail Japanese city on standard rings).
- **"214 accept, update the indemnity page"** (owner, staging's chat): Okazaki's 5(5), triggered by use and uncapped, accepted (Toyota's 4(6) and Yamagata's §4 shape). The private liabilities page is brought up to date with the 2026-10-07 reads.
- **The liabilities page updated** (https://claude.ai/artifact/FMZrsssfiCtydpHroo1V16, version 2): 82 clauses (68 accepted, 7 pending, 7 declined), adding the 2026-10-07 reads: four class-1 clauses (Yamagata §4, Matsumoto §6(5), LinkData Art.18(4), Okazaki 5(5)), six fault-based reimbursements, four own-cost clauses and Hirakata's hold-harmless; Iwaki's pending row closed (no clause).
- **Phase 2 waits until after the next review time lands on the site** (owner: "i want to wait for after next review lands on the site"); the owner has ideas for Cleanup to weigh first. Phase 2 holds 28 cities (East-2 11, Kansai-2 7, Regional-2 10), every licence read done; Kurashiki and Naha (Band C) stay unbuilt, outside the phases.
- **Band D, the first three Romanian cities' files complete** (the owner's browser acts, filed by staging into data/<slug>/raw and raw/non-animal): Timișoara 9 and 9, Iași 9 and 9, Cluj-Napoca 9 and 8. The DSVSA hosts timed out on the owner's home connection after the first batch; the owner fetched the last ten files over phone data. Staging had advised waiting rather than changing network, since a block met by changing address would be a bypass; the hosts gave timeouts, not a refusal page, and the owner made the call. Recorded for review time. The checklist page (version 5) marks the three as saved.
- **Regional-1 applied 210 to 213** (clean at b43ad80c, nothing pushed): Fukushima's five month files and Ōita's six hold new premises only (no closures published), so the registers are an upper bound, as the pages say (Fukushima 3,343 storefronts; Ōita's personal services 1,809 to 1,836). Ōita's own notification list supplies its Food-shops layer (Gifu's and Yokkaichi's precedent), MHLW now a points donor only (Toyama's): 6,406 storefronts, 6 names withheld, 349 withheld addresses counted apart. Gifu unchanged. One shared-code word: 届出者氏名 added to japan_register.OPERATOR_COLS_WAVE5 (new cities only; in no other city's raw files); keep both sides at merge (Kansai-1 adds name_city on the same module; its session was unreachable, so this entry carries the note to review time). BODIK: 3 package_show calls and 7 downloads, 22 s apart.
- **For review time:** eight shared-code findings worked around city by city (rebuilt_register's expiry ranking, which may affect Higashiōsaka; wareki_date and YYYYMMDD; city_rows trusting the extension; map_common anchoring line labels outside the city, Akita unfixed; SOURCE_LINKS; an oaza_cut fallback; the yatai FORM_RULES); "JR Hohi Main Line" against Kumamoto's "JR Hohi Line"; Morioka's terms re-read before publishing. Slips disclosed in its drafts: four terms or catalogue pages read for credit wording, one operator's name printed to an agent's console once, a few read-only git commands.

### 2026-10-07 - Thirteen operators' own names live on six published Japanese maps: fixed at once in Cleanup (owner, call 209)

- **Found by Kansai-1** while building call 205: `check_personal_exposure.py`'s Japan pass on the built cities' current files prints Osaka 6, Utsunomiya 3, Fukuoka 1, Kyoto 1, Sapporo 1, Yokkaichi 1 (Tokyo 0). Each is a trade name the name rule flags on one row that also shows at another premises; step 2 spread the rule only within one block. Staging did not re-run the check, which would print the names.
- **The fix is call 205's switch** (`name_city`): read-only on all 34 built cities it withholds exactly those 13, plus 1 Tokyo row not on its map; the other 27 move nothing.
- **"fix now in cleanup"** (owner, staging's chat), over taking the six layers down first: Cleanup takes Kansai-1's switch commit alone, adds `name_city` to the six cities' rules, re-runs steps 2 and 3, checks each at 0, drift-checks the six and Tokyo, records the verdicts and pushes outside review time; a reboot only if the push's app/ diff calls for one.
- **Live on master at bcd9e08f (Cleanup):** Kansai-1's fe85a793 taken alone, `name_city` added to the six; names withheld before and after: Osaka 29 to 35, Utsunomiya 5 to 8, Fukuoka 7 to 8, Kyoto 22 to 23, Sapporo 4 to 5, Yokkaichi 6 to 7. The privacy pass prints 0 for the six and Tokyo; zero drift beyond the withheld counts; no app/ change, no reboot; the deployed Yokkaichi map's hash matches the pushed file. Cleanup's DECISIONS entry "Call 209: the Japanese name rule crosses premises on six live maps..." is the record. app/ring_shares.json's map_blob for the six was left stale; Cleanup regenerates it.
- **The branches after the answers:** Kansai-1 clean at 3ddead26, all seven cities ready (Suita's check 0; Toyonaka's registers rebuilt to 2026-08-31 under call 151, storefronts 5,277 to 5,205). East-1 clean at 79b2581b: distinct colours in six cities; the two-town reason fixed; call 202 as a WAVE5 switch `default_joined` (Kasukabe's mall shops placed, 2,840 storefronts), which would add pins to five built cities if switched on there (Okayama 13, Fukuoka 4, Hiroshima 2, Shimonoseki 2, Kurume 1), for a review-time re-render; call 201's label kept on the owner's sign-off in East-1's chat (e7103294). All of East-1's calls are answered.

### 2026-10-07 - Calls 204, 205 and 151 approved; phase 2 held until the 60% check-in, its licence reads run now (owner)

- **"204 yes, 205 yes, 151 yes, hold on phase 2 do license reads now"** (owner, staging's chat):
  - **204:** East-1's shared code (tokyo_tama.py, saitama_pref.py, the yearbook's Tama rows and table 19-7, SHARE_DATES and REGISTER_SHARES) is accepted as precedent from Tokyo's official_shares.
  - **205:** Kansai-1 adds a japan_step2 switch, on for new cities, withholding every row whose trade-name key matches a flagged row in the same city; built cities unchanged until a re-render. Suita publishes with it.
  - **151:** Toyonaka's 14 sanitation month files (2026-01 to 2026-08) are approved: 14 BODIK calls, at least 20 s apart, so the registers rebuild to 2026-08-31.
  - **Phase 2** (East-2, Kansai-2, Regional-2) waits for the 60% weekly check-in. Staging runs the eight pending reads now: Osaka Prefecture's BODIK barber and beauty lists (Ibaraki, Kadoma, Minoh, Moriguchi), Neyagawa, Kawaguchi, Fujisawa, Okazaki, Aomori, Matsumoto, Yamagata.

### 2026-10-07 - Kansai-1's batch: six cities ready, Suita parked on call 205; call 151 put again (owner)

- **Kansai-1 reported its batch** (branch worktree-japan-kansai-1, tip 8c260435, nothing pushed, zero drift, 92 of 92 brief checks): Toyonaka, Hirakata, Itami, Kakogawa, Amagasaki and Uji ready on pages 222, 223 and 225 to 228 and notices 169, 170 and 172 to 175; Suita (page 224, notice 171) parked.
- **Call 205, the name rule across premises (Suita):** the city's old-law list flags a citywide street stall whose trade name is its operator's own name, and MHLW shows the same trade name at a fixed address, so the privacy check prints 1. Step 2 spreads the rule only within one block. Recommended a japan_step2 switch, on for new cities, withholding every row whose trade-name key matches a flagged row in the same city; it moves nothing among the other six. Tradeoff: a common trade name that is someone's own name elsewhere is withheld citywide. Suita cannot publish without it.
- **Call 151 put again:** Toyonaka's 14 sanitation month files (2026-01 to 2026-08) were never answered, so Kansai-1 built the registers to about 2025-12-31 beside the food list's 2026-08-31, two dates on the page (Fukuoka's precedent). Recommendation unchanged: approve them (14 BODIK calls). Calls 152 and 153 (Fukushima) are Regional-1's and it has not parked them.
- **Precedents Kansai-1 applied, flagged for review time:** Hyōgo's food XLSX on Ōtsu's precedent; Amagasaki's and Suita's undefined harm and defamation bars raised as Taoyuan's were; Hirakata's credit without hyperlinks; Uji's halved rings (505 m median gap); 木幡 as Kohata (Kyoto's 西院 tie); 大阪空港 as Osaka-kuko (Fukuoka's 福岡空港). About fifteen untemplated sentences wait as proposals in its drafts file.

### 2026-10-07 - East-1's batch ready: twelve cities, calls 199 to 204 put to the owner

- **East-1 reported its batch done** (branch worktree-japan-east-1, nothing pushed, zero drift): Higashiyamato, Nishitōkyō, Tama, Higashimurayama, Ageo (Regional), Sōka, Tokorozawa, Kasukabe, Fuchū (Tokyo), Chōfu, Tachikawa and Hino, on pages 210 to 221 and notices 157 to 168, the whole block used. Privacy passes are 0 for every city. check_all fails only the master list's built counts (staging's, after landing) and check_macro_labels on the new cities (Cleanup's, call 198).
- **Calls put to the owner** (East-1's drafts file holds the full text):
  - **199, line colours where one operator colour covers several lines** (Higashimurayama's five Seibu lines, the New Shuttle, Tobu's Urban Park Line): recommended distinct seeds, or Seibu's per-line colours if read.
  - **200, Ageo (Regional)'s excluded-station reason** reads "outside 上尾市" though the page covers Ageo and Ina: recommended naming both towns from the config's municipalities in shared japan_step1, before landing; no built city moves.
  - **201, the Leo Liner's label** "Seibu Yamaguchi Line (Leo Liner)": recommended keeping it.
  - **202, own_point_fallback refuses a publisher point** when one premises' address is written several ways (Kasukabe's AEON Mall, 3 rows unplaced): recommended counting towns over joined rows only, then a drift check of the built cities.
  - **203, "JR Chuo Line"** (Tachikawa, Hino) beside Tokyo's "JR Chuo Line (Rapid)": recommended keeping it.
  - **204, East-1 added shared code the briefs assumed existed** (tokyo_tama.py and saitama_pref.py new; the yearbook's Tama rows and table 19-7 in japan_official; SHARE_DATES and REGISTER_SHARES in japan_step2), treating Tokyo's official_shares as precedent rather than parking it. All 34 built Japanese cities' step 2 reproduces byte for byte. Recommended accepting the reading.
- **Answers to 199 to 203, given by the owner in East-1's own chat** (as East-1 reported them; East-1's drafts file is the record): 199 distinct colours; 200 fix the two-town reason; 201 shown to the owner, kept on their sign-off; 202 "sounds good, we can note if need be"; 203 keep ("rapid is a regional distinction for speed"). East-1 applies them on its branch, the shared fixes each checked read-only against the 34 built cities. Call 204 stays open.

### 2026-10-07 - Licence reads for the Japan builds (staging, licence-read agents): Morioka, Akita, Tsu, Iwaki, Ōita, Mito

The A and B briefs left 23 reads pending. Regional-1's six run from staging (Tsu, Iwaki, Akita, Ōita, Mito, Morioka); Kansai-1 runs its own five (Toyonaka, Hirakata, Suita, Hyōgo Prefecture's catalogue for Itami and Kakogawa, Amagasaki) and sends the verdicts here. Each verdict below is the agent's, read 2026-10-07 by plain GET; no data file was downloaded. Build sessions write their own `docs/data_sources/japan.md` rows from these at build.

- **Morioka: PERMITTED WITH CONDITIONS.** CC BY 4.0 through 盛岡市オープンデータ利用規約 (terms PDF, undated, `/_res/projects/default_project/_page_/001/024/522/opendateriyokiyaku.pdf`), which binds on use.
  - **Must display** (§2(2)ア, イ): a 出典 line and a separate processing line. The prescribed example's site URL is dead since the city's 2026-10-01 renewal, so the credit cites `https://www.city.morioka.iwate.jp/shisei/johokokai/opendata/index.html`. Suggested: 出典：盛岡市オープンデータサイト（that URL）, the four list titles, クリエイティブ・コモンズ・ライセンス表示 4.0 国際 (linked), and 「…（盛岡市ホームページ）を加工して作成」.
  - **Must not:** present processed data as the city's (§2(2)イ); imply endorsement.
  - **Clauses:** §3(2) own cost, and §4 reimbursement for costs from the user's own breach or infringement. Both are fault-based, the class the owner accepted for Japanese sources on 2026-09-24.
  - **Scope:** on the registers page only the CSVs are open (「データの一部」; the XLSX and PDF fall under the site's copyright page). On the food page every file is open. The build reads CSVs, as its brief says.
  - **Re-read before publishing:** the terms change without notice.
- **Akita: PERMITTED WITH CONDITIONS.** CC BY 4.0 on each dataset page (catalogue code op_cc_1). The city's 利用にあたって page allows free use and adaptation and adds nothing more restrictive.
  - **Must display:** CC BY 4.0's attribution, a modification notice and the licence link. No wording is prescribed; credit the edition titles actually used (the food file is renamed monthly).
  - **Must not:** imply endorsement.
  - **Clauses:** no indemnity, reimbursement or own-cost clause; the city's 免責事項 limits only its own liability.
  - **A request, not a condition:** the city asks users to report their use, through a form needing the owner's name and email. It does not block publication. Noted for the owner; nothing sent.
  - **Personal data:** the city's policy says data holding personal information is not made open, which sits oddly with the food list's 申請者名 column; the name rule already withholds those names.
- **Tsu (Mie Prefecture on BODIK): PERMITTED WITH CONDITIONS.** CC BY 4.0 by 三重県オープンデータ利用規約 第１条; no resource sets its own licence. 第４条's own-cost sentence is fault-based (the 2026-09-24 class). The terms are accepted by use and change without notice. BODIK has no user terms of its own.
  - **Credit:** the proposed form satisfies CC BY. The read suggests linking the three dataset pages, naming 医療保健部食品安全課, and stating the date as 2026年8月末時点, matching the monthly file used.
  - **Must not:** use the prefecture's logo alone (第３条); imply endorsement; claim completeness.
  - **Scope note for What Is Excluded:** the list omits vehicles, vending, stalls and temporary businesses, and 四日市市.
  - **Tsu is unparked.**
- **Iwaki: PERMITTED WITH CONDITIONS.** Both pages grant free use and modification and link CC BY 4.0. The food page's 「4.0日本」 names a licence that does not exist (4.0 has no ports; the linked deed is 表示 4.0 国際). The city's general open-data page still says CC BY 2.1 JP for its whole list, the food list included.
  - **Applied:** the dataset page's own, more specific and newer CC BY 4.0, credited as "CC BY 4.0" with the general page's statement noted beside the source entry. Both readings permit the use and differ only in the licence link.
  - **Clauses and acts:** no indemnity or cost clause. The showcase invitation is not a duty.
- **Ōita (BODIK): PERMITTED WITH CONDITIONS.** 大分市オープンデータ利用規約 (令和5年3月15日), compatible with CC BY 4.0, which every dataset declares.
  - **Must display (§1):** a credit in its 記載例 form, 「○○データ」（大分市）（URL）（利用日）, with 「…を加工して作成」 and the CC BY 4.0 link.
  - **Must not:** present the data as the city's; use logos (§3); imply endorsement.
  - **Clauses:** no indemnity or cost clause.
  - **Open for the build:** the city masks 301 rows, and neither page says why.
- **Mito: PERMITTED WITH CONDITIONS, on Bremen's precedent (call 196).** The dataset page says 「ライセンス CC-BY」 and 「コピーライト 水戸市役所」, with no version and no link; none of the city's 85 open-data pages names a version, and no open-data 利用規約 exists. The site-wide 著作権 section reserves copying of web pages; the dataset's own CC-BY label is the permission (the New York, Fukui and Bremen reading).
  - **Applied (change 1, precedent decides):** accepted on the permissive reading. Unlike Bremen, nothing points to 4.0, so the credit states the licence as the city does, "CC-BY, no version given". It also gives the copyright line 水戸市役所, the title 生活衛生関係施設一覧, a link to `https://www.city.mito.lg.jp/site/open-data/4496.html`, and a modification statement, which covers every CC BY version.
  - **Clauses:** no indemnity or cost clause.
  - **Must not:** use the city banner as a logo; imply endorsement; say "currently operating".
- **All six of Regional-1's reads are in;** Regional-1 is told.
- **From Kansai-1's reads (its drafts file holds the detail):**
  - **Hyōgo Prefecture's registers** (barber, beauty, laundry; Itami and Kakogawa): PERMITTED WITH CONDITIONS. CC BY 4.0 by the catalogue terms 3(3), which 2(1) puts above the site's copyright page; the 2.1 JP icon on the list page looks stale.
  - **Hyōgo's food permit and notification XLSX:** AMBIGUOUS. The catalogue lists only the HTML page (CC BY), not the files. Kansai-1 applies Ōtsu's precedent (owner, 2026-10-02) and flags it for review.
  - **Hyōgo's credit** takes the modified-work form 「この地図は、以下の著作物を改変して利用しています。[タイトル]、兵庫県」. No cost clause.
  - **Amagasaki:** PERMITTED WITH CONDITIONS. CC BY 4.0 on each op_data page (/op_data/1000922/1001025 to 1001028) and 尼崎市オープンデータ利用規約 §2. §3 requires the source and a modification statement; §6 bars presenting the edited data as the city's. §6 and §7 are fault-based cost clauses (the 2026-09-24 class); the use report (§5) is voluntary. The brief's page 1023309 is only an encoding note.
  - **Hirakata:** PERMITTED WITH CONDITIONS under CC BY 2.1 JP (the 利用条件 on pages 0000023479 and 0000025284).
    - Must display the prescribed adaptation form 「この[作品名等]は以下の著作物を改変して利用しています。[データのタイトル]、枚方市、クリエイティブ・コモンズ・ライセンス 表示 2.1」 with the licence URI.
    - The hold-harmless clause is fault-based. The credit must be removed if the city asks (CC 2.1 JP 第5条).
    - The site's linking policy asks for an enquiry before deep links, so Kansai-1 cites titles without hyperlinking the city's pages (flagged for review).
  - **Suita:** PERMITTED WITH CONDITIONS under CC BY 4.0 (吹田市オープンデータ利用規約, 2019-03-27, accepted by use).
    - Must display (2(3), prescribed): 「この地図は以下の著作物を改変して利用しています。【タイトル】、吹田市、クリエイティブ・コモンズ・ライセンス表示 4.0（URL）」.
    - Must not (§5): present edited data as the city's; use the logo.
    - Fault-based cost clauses. Links to data pages need no contact (§3).
  - **Toyonaka (BODIK):** PERMITTED WITH CONDITIONS under CC BY 4.0 (豊中市オープンデータ利用規約, ２(1)); ２(2) gives an example credit only, so CC BY 4.0's change statement applies. No cost or indemnity clause binds the user. That completes Kansai-1's five reads.
- **Phase 2's reads (staging, licence-read agents, 2026-10-07, plain GET, no data file):**
  - **Aomori: PERMITTED WITH CONDITIONS.** CC BY 4.0 through 青森市オープンデータ利用規約 (accepted by use, clause 1; terms PDF riyokiyaku.pdf, undated; dataset page /shisei/jouhokoukai/opendata/1006170/1006184.html, updated 2026-09-15). The site policy's reproduction bar covers the city's web pages, not this data.
    - Must display (3(2), prescribed): 「この地図は以下の著作物を改変して利用しています。［タイトル］、青森市、クリエイティブ・コモンズ・ライセンス表示 4.0 国際（https://creativecommons.org/licenses/by/4.0/deed.ja）、［当該ページの URL］」. The build chooses the title: the page's 食品営業許可施設一覧（オープンデータ） or the portal's 青森市における食品営業許可施設一覧.
    - Must not (6): present edited data as the city's; act in a way that harms or defames the city or others, or might (undefined, raised the way Taoyuan's was). The usage report (5) is voluntary.
    - Liability 6, 7(1), 7(2): fault-based, uncapped; Aomori District Court. The standing Japanese class.
  - **Yamagata: PERMITTED WITH CONDITIONS, subject to call 206.** CC BY 4.0 through 山形市オープンデータ利用規約 §2(2) (terms PDF /_res/common/opendeta/1000082/opendeta_riyou.pdf, Last-Modified 2021-09-29; accepted by use per the dataset page 1012802.html). The site policy's 著作権 clause covers web pages, not this data.
    - Must display (§2(3), prescribed): 「この地図は以下の著作物を改変して利用しています。［タイトル］、山形市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際（https://creativecommons.org/licenses/by/4.0/deed.ja）」, the URL as text or a link. The catalogue title changes each month (令和8年8月31日時点で営業中の食品営業許可施設一覧).
    - Must do: re-read the terms before each refresh (§1, changes without notice). No notification.
    - Liability: §3 fault-based, uncapped. **§4 is not fault-based**: the user reimburses the city's costs, damages included, arising from 「利用者によるサービスの利用やサービスの接続」 as well as from a breach. Uncapped; Yamagata District Court. The Hong Kong shape (accepted, owner 2026-09-22 and 09-24), put to the owner as call 206.
  - **Fujisawa: PERMITTED WITH CONDITIONS.** CC BY 4.0 through the open-data terms (riyoukiyaku20250401.pdf, 156,986 B, Last-Modified 2025-04-10, §3(2)). Library page 13230 lists both dataset pages (food 28905, 2026-09-18; barbers, beauty and laundry 32931, 2026-09-29) and binds by use; neither dataset page has a licence line.
    - The site policy (page 1196, 2023-04-01) bars unauthorised use of 文書・画像等 on the site. Read as covering the city's web pages, the open-data terms governing what the library lists: Koshigaya's and Hiroshima's shape (call 142), applied as precedent; both readings recorded.
    - Must display (§3(3), prescribed): 「この地図は以下の著作物を改変して利用しています。［タイトル］、藤沢市、クリエイティブ・コモンズ・ライセンス 表示 4.0（http://creativecommons.org/licenses/by/4.0/）」, the URL as text or a link; titles 「食品衛生法に基づく営業許可施設情報」 and 「理容所・美容所・クリーニング所」.
    - Must do: re-check the terms before each refresh (§1). Page 1196 asks for a notice to the city when a site links its pages, with no channel given; the build cites titles without hyperlinking city pages (Hirakata's precedent).
    - Liability: §4(3) and §5 breach-based, uncapped (the 2026-09-24 class).
  - **Matsumoto: PERMITTED WITH CONDITIONS, subject to call 207.** The city's terms (13394.pdf, 2018-10-01, accepted by use §1) grant use 「誰でも自由に利用（複製、加工、商用利用等）」 and cover both LinkData works (rdf1s8757i, rdf1s8748i), which LinkData marks CC BY 3.0 with the attribution name 松本市　DX推進本部; LinkData's terms (in force 2012-03-06) Art.11.2 make that mark binding on its host. No document says which version wins.
    - Must display (city §2(2), the city's format): 「出典：松本市の［タイトル］（クリエイティブ・コモンズ・ライセンス表示4.0国際、［URL］、［ダウンロード日］ダウンロード）、松本市を編集・加工して作成」, plus the attribution name and a line that LinkData marks the data CC BY 3.0 (both versions named; owner to confirm, call 207).
    - Must not: imply endorsement by the city or LinkData (CC BY 3.0 §4(b), LinkData Art.14.2); harm the author's honour (14.1); keep the contributor's name if asked to remove it (14.3).
    - Liability: **city §6(5) is not fault-based**: the user settles 「全ての苦情や請求」 arising from use at its own cost, uncapped, no express indemnity. **LinkData Art.18(4) is partly not fault-based**: the user settles claims arising from a breach or from the content, and repays LinkData's 「一切の損害、損失及び費用」, uncapped. Art.21(3) fault-based. Courts: Nagano, Tokyo. Put to the owner as call 207.
  - **Kawaguchi: PERMITTED WITH CONDITIONS, subject to call 208.** The open-data page (12182.html, updated 2026-10-07, now listing data to R8年8月) grants 「クリエイティブコモンズ「表示」（CC BY）」 and links **CC BY 2.1 JP**, not 4.0; its 第3条 grants reproduction, adaptation and 公衆送信. The site terms (4467.html, 2024-04-02) cover web text and images and route permission to each page's department, whose page this grant is; not incorporated into the data.
    - The page's 「データ利用者はデータ利用のみ自由です。」 sits beside 「所有権…は放棄しません」: read as use without ownership, the CC BY grant covering redistribution; read narrowly, only use is free. Put to the owner as call 208.
    - Must display (no prescribed form; 2.1 JP 第5条): the licence URI, 川口市, the title 食品等営業許可・届出一覧, that the data was used and changed, notices intact. The city's credit removed if it asks.
    - Must not: use that 「人権侵害を行ったり、安全を脅かす」 (the personal-name rule covers it); added terms; accuracy claims.
    - Liability: the city's exclusions only; 2.1 JP 第6条 fault-based. No indemnity or cost owed by the user.
  - **Osaka Prefecture's barber and beauty lists (Ibaraki, Kadoma, Minoh, Moriguchi): PERMITTED WITH CONDITIONS.** CC BY 4.0 by 大阪府オープンデータ利用規約 第1条 (https://odcs.bodik.jp/270008/tos/, accepted by use, changes without notice; 第5条 puts it above other sites' terms). Both dataset pages state CC BY 4.0 with no exception. The prefecture's site policy (use.html) covers its web pages only.
    - Must display (no prescribed form; CC BY 4.0 §3(a)): 大阪府, the titles 「理容所届出施設一覧」「美容所届出施設一覧」, the licence link, a modification statement.
    - Must do: clear third parties' rights (第2条; trade names are facts, none found); ask before using the logo (第3条). The list page says the lists lag and the full list renews twice a year, so the page never calls them current. Linking prefecture pages asks for a notice to the page's 作成所属: cite titles without hyperlinking them (Hirakata's precedent).
    - Liability: 第4条 ¶3 breach- or infringement-based, uncapped, settled at the user's cost, not an indemnity; Osaka District Court.
    - Rate: three bodik.jp requests, all 200; the second came about 30 s after the first, inside the 20 s rule but under the 60 s spacing staging set.
  - **Neyagawa (barbers, beauty salons, laundries: 272159_barber, _hair_dressing, _cleaning): PERMITTED WITH CONDITIONS.** CC BY 4.0 by 寝屋川市オープンデータ利用規約 (page 16048, 2021-07-01, accepted by use; compatible with CC BY 4.0) and BODIK's terms 第1条 (odcs.bodik.jp/272159/tos/); all three packages `cc-by-40-intl`. The site's 著作権・リンク page covers web pages only.
    - Must display (item 1, the city's 記載例): 「「理容所確認施設一覧」「美容所確認施設一覧」「クリーニング所確認施設一覧」（寝屋川市）（［ページURL］）を加工して作成」, the edit stated apart from the credit.
    - Must not: present edited data as the city's; claim completeness or accuracy (BODIK 第4条); use the logo alone without asking (第3条).
    - Liability: BODIK 第4条 ¶3 fault-based, uncapped (the standing Japanese class); Osaka District Court. Three bodik.jp requests, 65 s and 66 s apart.
  - **Okazaki: PERMITTED WITH CONDITIONS, subject to call 214.** CC BY 4.0 (package_show `cc-by-40-intl`) under 岡崎市オープンデータ利用規約 (in force 2015-12-01, opendata-kiyaku.pdf, accepted by use 2(1), changes without notice 2(2)); 3(2): 「データの利用に当たり本市の承諾及び利用料は不要です。」 BODIK's tos page defers to the city's terms. The site policy (about/1006234.html) covers web pages only.
    - Must display (4(2)): 「この地図は、以下の著作物を改変して利用しています。食品等営業許可・届出一覧、岡崎市、クリエイティブ・コモンズ・ライセンス 表示４.０国際（http://creativecommons.org/licenses/by/4.0/legalcode.ja）」, the URL as text or a link on the licence name.
    - Must not: harm others' rights or safety (3(3)); unlawful use or use against public order (3(4)).
    - Liability: **5(5) is not purely fault-based**: complaints and claims arising from 「データの利用、データへの接続、本規約違反若しくは第三者の権利侵害」 are settled at the user's cost, uncapped (Toyota's accepted 4(6) shape; Yamagata's §4, call 206). 6 本市への補償 breach-triggered, uncapped. Nagoya District Court. Put to the owner as call 214.
    - Slip: the agent opened the terms PDF in the in-app browser, which saved opendata-kiyaku.pdf (136 KB) into the main checkout's root; staging moved it to its scratchpad. A terms document, not data. Three bodik.jp requests, 97 s and 72 s apart.

### 2026-10-07 - Call 197 built on Cleanup's europe-split branch; the macro map's region views are Cleanup's (owner, call 198)

- **Call 197 built** (Cleanup, branch europe-split, off Abroad's tip, not pushed; DECISIONS on master 69d32b6d):
  - the owner's answers in Cleanup's session: Benelux replaces the Belgium view; the top cities are Sydney, Brussels and Taipei (Regional);
  - the landing view labels 24 of 27 countries' top cities (was 20); Brussels, Copenhagen and Zurich have no room at world zoom and are labelled in Europe West;
  - every city is labelled in at least one view, and check_macro_labels fails if either goal breaks.
  It lands at review time after Abroad's batch, with a reboot and a map-chrome deploy-verify. Staging writes the master list's Built rows then (176; Europe 21; Seoul Capital Area 13; Benelux 9; Germany 3).
- **Japan's region views (call 198, "198 yes, cleanup builds them"):** with call 197's every-city test, about 27 of the planned Japanese cities would be labelled in no view until Japan's eight regions plus Osaka Prefecture (2026-10-04) exist. Three Japan sessions build in parallel, so Cleanup builds the views on its own branch at the phase 1 review time. Build sessions leave region tables alone and report any label-check failure. The plan says so; East-1 and Regional-1 are told.

### 2026-10-07 - Bremen's licence accepted on the permissive reading; Europe West anchors; every city labelled somewhere, every country's top city on the landing view (owner)

- **Bremen (call 196):** the 2024 report (124 pages; downloaded on the owner's yes in the Abroad session, call 191) names no licence, no CC version and no reuse terms. The owner said yes, in the Abroad session, to accepting the unversioned "CC BY" on the permissive reading. Bremen is credited to CC BY 4.0's terms (the Kommunalverbund Niedersachsen/Bremen as publisher, the survey named, the source linked), the version recorded as unstated and assumed to be 4.0; the publisher uses cc-by/4.0 on its six boundary sets. Outreach stays the last resort.
- **The Europe split (call 195) with a Germany view (call 194).** Cleanup measured both on Abroad's tip:
  - the split alone leaves Europe West's 12 label problems;
  - the split plus a Germany view (Berlin, Gelsenkirchen, Bremen), with competition in both Europe halves, comes to 0 problems with every name labelled.
  Cleanup builds both on one branch, landing at review time after Abroad's batch. Abroad leaves the region tables alone.
- **East Asia's Seoul pattern for Europe West (owner):** "berlin, prague, brussels, antwerp etc. should be visible on global but the remaining smaller cities can be omitted for country-views". REGION_LABELS_ALSO gives Europe West the Czechia, Belgium and Germany anchors; the smaller cities are label_tier "minor". Cleanup measures which anchors fit before building.
- **A site-wide label rule (owner):** "the goal is to have all dots visible in at least one regional view, and to feature every nation's top 1, maybe 2 cities at least in global view". Call 197, "197 sounds good":
  - "top" is the largest by city population;
  - one city per country is guaranteed a label on the landing view, ahead of the competition;
  - a second is labelled only where the competition clears it;
  - check_macro_labels tests that every city is labelled in at least one view and that each country's anchor is labelled on the landing view;
  - many-city countries take the Seoul pattern.
  Cleanup builds it with the split branch. It is an app/ change, landing at review time. On the tradeoff, the owner: "the europe concerns are null if the result is the biggest cities people would expect to see are the ones displayed. The competition is still relevant but just at a lower order of magnitude" (mid-sized cities fading below the anchors is accepted).

### 2026-10-07 - Phase 0: the Japan foundation landed; Abroad's batch ready; calls 191 to 195; Europe East to land with Thessaloniki (owner)

- **The Japan foundation landed** (7ab440f9; the five address fixes the owner asked for, "do the address fixes", in 521d28fc). Pipeline and the japan-city skill only, with Minato 98.0 / 0.2 / 1.8 and zero drift on the 34 built Japanese cities after every group. The new rules are on for new cities only. The review-time re-render proposal (Toyota +177 storefronts, other built cities under about 20) is in `docs/decisions_drafts/japan-foundation.md`. Matsue's 八雲村 fold is a config key, now in its brief.
- **Abroad's batch is ready on its branch**, nothing pushed: Gimpo, Siheung, Geneva (Regional), Thessaloniki, Gelsenkirchen, Bremen, Anyang (Regional), Mexico City (Regional). Pages 202 and 300-304 and notices 154-156 are recorded in `docs/session_roles.md`. Copenhagen (Regional) is not built: it waits for the owner to set the Datafordeler key or fetch the address-point files.
- **Calls (owner, 2026-10-07):**
  - 191: Bremen's 2024 report PDF (3,643,392 B), "download approved", for the licence terms only.
  - 192: Nezahualcóyotl's 398 rows outside OSM's polygon, "continue drop, state on page".
  - 193: Gelsenkirchen's U11, "keep it tram mode".
  - 194: a Germany view, approved only "if we are waiting a while longer for europe east/west".
  - 195: Greece in Europe East, "yes and we should message cleanup to land the europe east region with the greek city".
- **The trigger for the split moves:** it was to be made by the first Romanian city to land (all in Band D); the owner asks for it now, with Thessaloniki. Staging asked Cleanup to make it and re-run the stress test with Abroad's cities. Gelsenkirchen, Bremen, Rotterdam and Den Haag all fall in Europe West, so the 12 overlaps may stay; if they do, the Germany view follows (194). Abroad holds the Germany view until then.

### 2026-10-07 - Builds resume: the A and B waves planned, four process changes, weekly check-ins at every ten percent (owner)

- **The owner lifted the build pause** set on 2026-10-04 ("pause lifted, approve 1-4, write the session prompts, we can start phase 0 after that"). Band D waits until the owner can give it attention ("those I will act on when i can devote full attention here"). Seoul, Busan and Daegu (Regional) still wait for SEMAS's social-post scope (call 71).
- **The plan:** `docs/build_plan_2026-10-07.md`, on staging's measurements.
  - Japanese steps 2-3 take 0.2-1.2 min and under 0.7 GB; the Japan drift check takes 2-3.4 min at 5.3 GB.
  - The last Japan batches did 12 and 14 cities in about 3 h of active time each, against 4.6 h and 9.3 h of wall time.
  - 39 of 58 Japanese briefs flag shared-code changes, so a **Japan foundation session lands every shared rule once, before any Japanese city**. A rule that would change a built map is switched per city, default off for built cities, and goes to review time as a re-render proposal.
  - An Abroad session runs alongside it: Gimpo, Siheung, Geneva, Thessaloniki, Gelsenkirchen, Bremen, and the Anyang, Mexico City and Copenhagen (Regional) extensions.
  - Then six Japan sessions of about 12 cities each, grouped by shared source (East: the Tama ledgers, the Saitama layers, Chiba; Kansai: BODIK, called by one session only; Regional), three at a time.
- **The four changes (owner, "approve 1-4"):**
  1. Precedent decides: a question answered by a brief, a skill, `docs/category_rules.md` or a numbered owner call is applied and logged.
  2. Unattended mode: parked calls go in the branch's drafts file and reach the owner through Staging as one numbered list per wave.
  3. One review time per phase.
  4. Build sessions never edit `docs/city_master_list.md`; Staging moves rows after each landing.
  For Cleanup to fold into `docs/session_roles.md` and CLAUDE.md as it sees fit.
- **Usage check-ins (owner):** "pause and check in with me (here or in cleanup) before continuing when weekly usage hits a multiple of ten." The weekly read 42% on 2026-10-07, so the next stop is 50%. Every session checks `get_usage` between cities and stops at a crossing; all sessions share one pool. Cleanup told.

### 2026-10-06 - Review-time page-text proposal: the Japan rail exception explained on Why the maps differ (owner, call 190)

- **The gap, found on the owner's question** ("do we have a JR explanation piece anywhere on the site to justify the japan-only distinction?"): the site states the distinction but never justifies it. `app/pages/Why_the_Maps_Differ.py` (the "Suburban trains appear on only a few maps" paragraph) ends "The Japanese maps draw their JR and private railways as well."; What Is Excluded points there; no Japanese city page gives the reason. The rule has also widened since that sentence was written: no frequency floor for JR or private lines (call 46), and stretches with about 11 trains a day or fewer are drawn and named (call 86).
- **Approved for review time (owner: "190 yes, log it for review time")**: replace that last sentence with:

  > Japan is the exception: its JR and private railways are drawn on every Japanese map, whatever their frequency. Most Japanese cities have no subway, and these railways are their rapid-transit network. Their stations sit close together through built-up areas, and each city's shopping streets grew up around them. Where a line runs only a few trains a day inside the city, the city's page says so.

- **For whoever lands it:**
  - It is an `app/` change, so it lands at review time, with `check_deploy_imports.py` and a deploy-verify `map-chrome` scope or a quick render of the page. American spelling throughout. The claims are structural, never ridership (out of scope, hard line).
  - The fourth sentence holds for pages built under call 86. Shimonoseki's earlier page cuts its 8-to-10-trains-a-day stretch instead of naming it. Before landing, check whether any built Japanese page has an undisclosed low-frequency stretch, then either soften the sentence or add a note to that page.
- Staging changed no `app/` file.

### 2026-10-06 - Wave 5, the last briefs: calls 154 to 184, the one-station rule applied as written, Saitama's old-law list added (owner)

- **Hirakata, Mito, Fujisawa (calls 154-160):** Hirakata keeps no food-share sentence and stays in A (154), its registers' five monthly XLSX files approved (155); Mito leaves out 偕楽園, a seasonal station (156, the Sagano and Mojikō Retro precedents), and states its food share in two figures together (157); Fujisawa drops MHLW's 6 August closures (159), and the city's yearly report was approved as one file (160; the 統計年報's health chapter holds no food table).
- **Shared-code rules for the build (owner):** combined-form restaurant cells stay in Food service unless the cell names 給食 or 旅館 (158); permits past their term are dropped (161); an address of the city name alone is not a premises ("city name alone seems like we can exclude (also confusing)", 162); a permit that starts after the as-of waits until it is in term (172). The briefs also name 自動車以外 as not a vehicle, and an asterisk-only address as withheld. Each needs the Minato control at build.
- **The one-station rule (calls 163, 165, 167):** Itami's 大阪空港 is drawn cut, since no other line serves it ("draw it cut"); Suita's Esaka keeps its ring through Kita-Osaka Kyuko, so the Midōsuji Line is left out ("apply as written"; call 92's premise did not hold). Kadoma's 門真南 (the Nagahori Tsurumi-ryokuchi Line) is drawn cut, and the Osaka Monorail at 門真市 is left out, since Keihan keeps its ring ("apply rule as written"). The master list's call-116 wording is corrected. Hyōgo's notification lists are the Food-shops layer for Itami and Kakogawa, as Amagasaki's city list is for Amagasaki (164, Yokkaichi's precedent).
- **Floors and names (166, 168, 170):** Minoh's 294 measured premises are the floor ("Minoh's page"), so Moriguchi (375) and Kadoma (339) are built; Ibaraki's page is "Ibaraki (Osaka)"; Higashiyamato's `mode` is `metro`.
- **Tama and Saitama (169, 171-173):** MHLW's rows that the Tama ledgers lack are added for all four Tama cities (the Tokyo wards' precedent; the stated share excludes them). Saitama's R8.3.31 old-law list joins the food source for Ageo (Regional), Sōka, Tokorozawa and Kasukabe, disclosed as an upper bound (171, "yes and disclose"). Rows that start after the as-of are dropped (172). There is no food-share sentence; the withholding note is given with no number (173).
- **Approvals (174, 176, 184):** Fuji's Shizuoka Prefecture lists (datasets 11261-11263) approved for download, and its brief is under way; Alpico's timetable PDF for Matsumoto and Ichibata's eight for Matsue approved for gate 3, counts only.
- **Fujisawa's food share (175, "okay to fetch if low cost, otherwise we can leave estimate and state as such"):** the health centre's 令和7年度実施結果 PDF (797,085 B) was fetched. Its Japanese text has no Unicode mapping and no renderer or OCR is installed, so no count can be read. The 5.4 MB plan was not fetched. The page states the census estimate as an estimate.
- **Kawaguchi, Okazaki, Tottori, Yamagata, Matsue (177-183):**
  - Kawaguchi builds on the CSV as published, with June's stoppage named (177).
  - Okazaki keeps the 47 permits at 舞木町字金森 (178). Its new towns south of JR 岡崎 stay unplaced, disclosed with the tiers (179; the owner wrote "okay with closure", read as disclosure).
  - Tottori's Inbi Line is drawn cut in two pieces (180). Its food share is stated as "about 8 in 10", with a note that the figure may understate (181).
  - Yamagata withholds the 4 city trade names that match an individual's 法人名 (182).
  - Matsue builds with its tiers disclosed (183).
- **Kure (call 185, "185 yes, B with share stated"):** 69.4% of fixed premises carry a real address (1,025 of 1,477), taken as about 70% on call 139's bar; moved from C to B, food only, the share stated. Its brief re-read it as 69.3% (1,022 of 1,474) once call 172 set aside 3 permits that start after the as-of and the permit condition marked 8 vehicles or stalls; staging logs it, the call stands.
- **The last four Tama cities (calls 187, 188, "187 and 188: B sounds good"):** measured from cached files by Tama's own method, which reproduced Tama's brief exactly. Restaurants at the yearbook's date: Chōfu 68.0%, Tachikawa 63.6%, Hino 61.2%, Fuchū 57.6% (raw 70.7-85.2%), against 71.6-75.2% for the four Tama cities in A. Retail is near complete, and personal services 52-89%. All four go from C to B, all three buckets, with the food share stated at the yearbook's date; Kure's 58.3% of the in-force count (its brief, after call 172) is the precedent, and Fuchū sits 0.7 points under it, the lowest food share on any page. Call 169's MHLW rows apply. Bands now A 32, B 32, C 2, D 16, R 77. The final group of about 93 has no city left in C; Kurashiki and Naha (third wave) remain.
- **Tokyo's yearbook table 19-7 (call 189, "fetch at once"):** 6,876 B from the statistics bureau's own host, the publisher of table 19-8. Against the official FY2024 counts, the eight Tama cities' registers hold barbers 84-98%, beauty 86-93% and laundry 83-98% at the yearbook's date (86-102% counting every row), against census-scaled estimates that had read laundry as low as 43%; Tachikawa's 501 beauty salons are 448 of 504 at the date (88.9%). The official shares supersede the estimates in all eight briefs and rows, and the page states the share at the yearbook's date, as the food share (calls 187-188); it is a lower bound, since 確認年月日 renews on a change of operator.
- **Fuji's brief (call 174):** 19 files, 862,513 B, from the portal's own host; the portal answered HTTP 429 once and the agent retried a single time after more than 60 s. Its coverage sentence: call 186, "186 yes, state both as estimates" (beauty about nine in ten, laundries about four in five).
- **Slips:**
  - The Matsue brief agent printed rows holding personal data to its own console once. The Yao agent listed business addresses on its console and ran a grep with backslashes (within the hook's rule). Nothing was stored.
  - The Tokorozawa agent fetched an 11.3 MB file beyond its conditional approval; it was kept for the owner to confirm. The Fujisawa agent fetched the monorail operator's timetable PDF without it being named; counts only.
  - Staging's own HEAD requests for Fujisawa's two PDFs carried the owner's email address in the user-agent string instead of the project's. The fetch itself used the project's user agent.
### 2026-10-06 - Wave 5, the briefs: calls 142 to 153, Ireland's indemnity kept declined, a private list of every liability clause (owner)

- **Licence calls (owner, 2026-10-06):** Koshigaya's PDL record for its exact pages relied on over the site's copyright page (call 142, Hiroshima's shape); Saitama Prefecture's 2024 PDL record for its 生活衛生 page relied on likewise (143); Shizuoka Prefecture's portal §6 accepted for Fuji (144: its reimbursement sentence is fault-based, its own-cost sentence Fukushima's class); Kakogawa built with its block-join tiers disclosed (145, 86.5% block); Copenhagen (Regional) keeps Gentofte, Ballerup and Rudersdal out of the business filter and reads the S-tog test per line (146); the downloads for the remaining A and B briefs approved (147).
- **Ireland (call 148, "i meant 148 yes"):** the NTA developer portal's uncapped indemnity stays unaccepted; Dublin's feed is a plain CC BY download and the portal policy binds only API-key and realtime use.
- **Iwaki (calls 149, 150):** its monthly files merge as Ichinomiya's (the full list whole plus the months); MHLW's 164 addressed notifications left out as too thin. Precedents applied without new calls: MHLW's notifications as partial food shops where they run to hundreds of rows (Akita, Toyonaka); Toyonaka's two 千里中央 groups joined (Kawasaki's and Tokyo's precedent); public baths out (no built Japanese city carries them); Fukushima's shared catering rule kept. Open: Toyonaka's and Fukushima's monthly register files (151, 153) and Fukushima's MHLW as control only (152).
- **The owner asked for "an internal list of all accepted indemnities/liabilities so far"**: compiled from the records (67 clauses: 52 accepted, 8 pending, 7 declined; class 1, no fault needed, 9 accepted) and published as a private page, https://claude.ai/artifact/FMZrsssfiCtydpHroo1V16. Found while compiling: Fukushima §4's quoted text is triggered by the user's breach or infringement (fault-based, uncapped in amount) although it was accepted as uncapped; Shizuoka Prefecture §6 was read as purely fault-based on 2026-10-05 and as two sentences on 2026-10-06; PDL 1.0 §1.6 is read differently in Fukuyama's and Utsunomiya's records; `docs/licence_positions.md` predates the CARTO and SanGIS acceptances. Each is for Cleanup and review time; staging changed no licence record.
- **Briefs on master (20):** Uji, Sakura, Yachiyo, Urayasu, Ichihara (block shares 93.2-99.1% measured with MLIT's files), Ichinomiya, Tsu, Aomori, Ōita, Iwaki, Akita, Toyonaka, Fukushima, and the extensions (Seoul, Anyang, Busan, Daegu and Mexico City (Regional), Copenhagen (Regional)). Corrections made from the briefs: Sakura's beauty count 256; Aomori's thin line is JR East's Tsugaru Line, not the Tsugaru Railway; Gifu's dataset ids; the J4 probe's JR East counter skipped marked departures (Akita's Oga Line read 11 a day for 18; Fukushima's 11 re-counted and held).
- **Slips:** the Fukushima and Ichinomiya brief agents each printed trade names or building names from monthly files to their own consoles once; nothing was stored.

### 2026-10-06 - Wave 5, second half: calls 95 to 141, the Japanese pre-verdicts converted, eleven licence reads (owner)

- **Bands (owner, 2026-10-06), after the first entry's:**
  - **A:** Ōita; Gifu (on Gifu City's own CKAN packages c212016-072 and -075, CC BY 2.0; the city page's newer edition needs permission, noted); Tokorozawa, Kasukabe, Sōka and **Ageo (Regional) with Ina** (call 102: Ina too thin alone); Koshigaya; Higashiyamato, Nishitōkyō, Tama and Higashimurayama on Tokyo's Tama ledgers (call 109: the skew disclosed); Hirakata, Fujisawa; Amagasaki, Suita, Itami, Kakogawa (call 118: 101-106% with old-law permits); Mito (6 station groups, one under the smallest built page); Morioka; Ichinomiya kept in A with its food share (67.7%) stated (call 125).
  - **B:** Matsue (personal services; PDL 1.0 read); Kawaguchi (food only; the personal-services PDFs need the city's permission, noted, call 104); Neyagawa; Moriguchi and Kadoma (counted first: under Minoh's roughly 350 premises they come back as too thin); Fuji (personal services, a licence read); Matsumoto (the ledger fill measured at the brief); Tottori, Yamagata, Yao, Takatsuki (food only).
  - **C:** Kure (one measurement); Fuchū, Tachikawa, Hino, Chōfu stay.
  - **D:** Oradea, from C (its 2022 files carry no activity column, call 120).
  - **R:** Kawagoe, Asahikawa (call 111), Kamakura, Yamato, Kōfu, Atsugi, Kasugai, Nagakute, Nisshin.
  - **Discards:** Tokushima, Saga, Miyazaki on coverage; Chigasaki (3 station groups), Wakō and Hiratsuka (one each) on rail. **The owner asked (call 130) whether a page with fewer than 3 station groups had been published**: staging measured the master list's built rows, whose fewest stated stations are 7 (Anyang, Mendoza), with Brossard and Berkeley discarded at 3 and Uiwang and Putrajaya at 1; the owner: "if it follows our current precedents discard".
  - **Add-on:** Naha (Regional) + Urasoe, only once Naha is built (call 100).
- **Rules applied, owner's words:** Sakura's mode is `metro` ("i think metro is safe due to it having significant presence", call 121); Urayasu's monorail is labelled the Disney Resort Line (call 122); Ichihara's 81% laundries built and stated (call 123), its half-width address column fixed city-locally (call 124); Ichinomiya merges the March list whole plus the months, MHLW's extra permits out, its notifications in as partial food shops, its points where the join misses, the registers' monthly CSVs approved (calls 126-128). Yamagata's partial personal-services lists stay out (call 138).
- **Licences read (licence-read agents, 2026-10-06):** Ichinomiya PERMITTED WITH CONDITIONS (CC BY 4.0 plus the city's terms; prescribed credit); Kyoto Prefecture's personal-services PDFs NOT PERMITTED without permission (Uji food only, call 107); Tokyo's Tama ledgers PERMITTED WITH CONDITIONS through the catalogue route, relied on (call 108, Taitō's precedent); Fukushima PERMITTED WITH CONDITIONS, **its uncapped §4 reimbursement clause accepted** (call 110, Hong Kong's and SanGIS's precedent); Asahikawa NOT PERMITTED (Chūō's precedent); Matsue PERMITTED WITH CONDITIONS (PDL 1.0 on the newest resources, CC BY on older ones; a fault-based cost clause); Koshigaya PERMITTED WITH CONDITIONS (PDL 1.0 on the portal records for the exact pages; the site's copyright page differs: Hiroshima's shape, an owner acknowledgement pending); Saitama Prefecture: food layers PERMITTED WITH CONDITIONS (the GIS catalogue applies the portal's PDL terms), the 生活衛生 files AMBIGUOUS (a 2024 PDL record for the page against the site's copyright page: an owner call pending); Gifu PERMITTED WITH CONDITIONS on the CKAN packages, the city page's edition NOT PERMITTED without permission.
- **The owner on Ireland** (asked with call 110, "should we accept ireland's as well?"): staging recommended leaving the NTA developer portal's uncapped indemnity unaccepted, since Dublin's feed is a plain CC BY download and the portal policy governs API keys and the realtime service only; the owner's answer is pending.
- **Slips:** two licence-read agents fetched data they were not approved to fetch (Ichinomiya's four CSVs, approved for the brief but not for the read; two Kyoto Prefecture PDFs, not approved at all); a third read headers by Range request (Tokyo's ledgers, Fukushima's CSVs); all copies were deleted from the scratchpad and later reads were told terms only. The Fuji measurement fetched MLIT's two small address files for 22210 without them being named (kept, owner to confirm). The Ichinomiya brief agent printed building and unit names from the monthly food files to its own console once; nothing was stored. Cleanup's call 94 closed: the probes' backslash commands were within the hook's rule, CLAUDE.md now says so.

### 2026-10-06 - Wave 5: the ranked queue and the pre-verdicts screened; Japan's lines carry no frequency floor (owner)

- **The owner released NEXT items 2 onward** ("We can start on the next items, i
  want to get a bunch of briefs ready for build time"). Staging ran 18 city-probe
  agents and two brief agents, curl only, no data downloads, no names; calls 46
  to 93 went to the owner in numbered groups.
- **Japan's frequency floor (call 46, "46 yes").** No 15-minute floor applies to
  JR or private lines in Japan, on Maebashi's approved brief (the Jōmō line every
  30 minutes) and Fukuyama's (never less than hourly); the japan-city screening
  section had said the call rests on frequency, and now agrees. **Call 86** (the
  owner: "check my call on 46 and manage accordingly, note these 11> trains
  though"): stretches with about 11 trains a day or fewer are drawn and named in
  each brief, not left out; Shimonoseki's built cut (8 to 10 trains a day)
  predates this and is not reopened. Cleanup told.
- **Bands (owner, 2026-10-06):**
  - **A:** Ichinomiya, Tsu, Uji (food only, its own page, Gimhae's precedent),
    Fukushima (a licence read first), Iwaki, Akita, Toyonaka (99.8% of
    restaurants in force).
  - **B:** Okazaki and Aomori (food only); Urayasu, Sakura, Yachiyo and Ichihara
    (personal services, Matsudo's shape; the Kominato line drawn); Ibaraki and
    Minoh (barbers and beauty only, thinner than any page published, measured
    against Hakodate's 1,077 and Kōchi's 1,406 storefronts).
  - **C:** Oradea (the city's own 2022 lists); Asahikawa (a licence read
    decides); eight Tama cities on the Tokyo Metropolitan Government's monthly
    ledgers (one download approved to measure them); Amagasaki, Suita, Itami,
    Kakogawa (files approved to measure).
  - **D:** Arad, Galați, Ploiești, Craiova and Reșița on Timișoara's DSVSA act.
  - **R:** Imizu, Isesaki, Ōta, Tsukuba, Toyokawa, Kōriyama, Machida; Espoo,
    Tampere; Almada, Seixal, Vila Nova de Gaia, Matosinhos, Maia; Pavlodar,
    Oskemen; Samarkand.
  - **Open gaps:** Perugia (the Minimetrò counted as rail, Téléo's precedent),
    Faridabad, Howrah.
  - **Discards, 61:** the rail pre-verdicts less Reșița; Brăila and
    Hódmezővásárhely; Ino, Nankoku, Hachinohe, Nagaoka, Akashi, Settsu ("too
    thin", unless a thinner city is published: none is); Adana, Memphis,
    Thane, Mira-Bhayandar, Ghaziabad; the Aburrá towns, Santo Domingo's two,
    San Miguelito, Bidhannagar, Giza, New Cairo, Abuja; Gauteng's three
    (vendor POI layers count as absence; not in the commuter-rail tier);
    Temirtau, Vantaa; eight German, Austrian and Dutch towns on absence and
    Nieuwegein; Strausberg, Woltersdorf and Schöneiche on rail.
  - **Commuter-rail tier** gains Toluca's four (data buildable) and Trenton,
    Oceanside, Escondido, Vicente López, San Isidro, Tigre, Cádiz, Chiclana,
    San Fernando, Dakar, Thane and Vantaa (data open or blocked).
  - **Potentials, not now:** Amsterdam + Amstelveen (Gemeenteblad notices,
    "let's revisit"); Strausberg, Woltersdorf and Schöneiche ("mark the three
    on rail as potentials to allow through but not now").
- **One-station stubs, two exceptions (calls 54, 92):** the Tōzai at 浦安
  (Urayasu) and the Midōsuji at Esaka (Suita) are drawn cut, because no other
  line keeps the station's ring, which the one-station rule of 2026-10-06
  assumes. The Maihama Resort Line counts as rail (call 53).
- **Extensions (calls 68 to 72):** Mexico City (Regional) keeps Naucalpan (Línea
  2 ends at Cuatro Caminos, it is not cut), takes boundaries from OSM matched on
  INEGI codes, and the two State of México files (81 MB) are approved. Busan +
  Yangsan and Daegu + Gyeongsan are extensions, not pages (Yangsan and Gyeongsan
  leave Band C); SEMAS's retail step at the city line is built and disclosed;
  Anyang (Regional) builds first, Seoul, Busan and Daegu after the owner rules
  on SEMAS's social-post scope; the Gwangmyeong shuttle station stays.
- **Housekeeping:** Navi Mumbai was on the low-odds list though discarded on
  2026-10-04; Noida's row names `greaternoidaauthority.in` (the old domain
  redirects to a shop); every county DSVSA host now answers 403 to scripts;
  Chiba's beauty workbook repeats 印旛 as 海匝 (Matsudo's and Ichikawa's
  controls corrected to 92.3%); Akashi's outreach option noted, not sent.
- **Probe slips:** the Mie/Aichi probe retried Aichi Prefecture once with a
  cookie jar after an Imperva challenge (no disguise, no success); two probes
  ran Bash commands with backslash escapes (Gauteng, Hyōgo), which the hook
  allows by design outside heredocs (Cleanup, call 94: the gap is CLAUDE.md's
  stricter wording, put to the owner). Staging's own call 60 said "eighteen"
  rail discards where the rows were sixteen plus Tigre's three.
- **Open:** call 66 (the Copenhagen Light Rail), the western Japanese group's
  calls, Fuji's food measurement, two probe groups running.

### 2026-10-06 - The Japanese name rule's version 2 landed; staging's bare-name count re-run: 0 shown

- **Cleanup landed version 2 on master** (47452fa8, 2030af23; the owner:
  "Land now"; DECISIONS 2026-10-06 "The Japanese name rule's version 2"):
  `japan_register.bare_personal_name()` with staging's 166-surname list,
  the strict spaced form only, applied first in `name_is_operator`.
- **Staging re-ran its own count on the merged master**, not taking the
  peer's figure: the strict spaced form matches **0 of 432,489 shown rows**
  in the built Japanese cities, as expected. The loose unspaced shape (484)
  stays unused, as the owner decided: it catches shop names such as a
  surname run into a trade word.
- **No separate sweep needed** (the open question in the entry below): the
  rule itself is the sweep, and the re-run confirms it.

### 2026-10-06 - Toei Shinjuku left out, the Tōzai drawn cut; bare personal names measured; the Japanese name rule's version 2 (owner)

- **The owner: "confirm, record toei shinjuku out, note on page. 44 note
  this and determine if we need a sweep. 45: sounds good note the version
  change here"**, after "the tozai 3 and 2 stations seem more reasonable".
- **Calls 31 and 41, the subway stubs.** **The Tōzai Line is drawn cut at
  the city line** in Ichikawa (3 of 23) and Funabashi (2 of 23), on Sakai's
  (the Midōsuji, 3 of 20) and Higashiōsaka's (the Chūō Line, 2 of 12)
  precedent. **The Toei Shinjuku Line is left out of Ichikawa**
  (`LEFT_OUT_LINES`): one station, 本八幡, its terminus; 本八幡 keeps its
  ring through JR's Sōbu Line (in N02 its station group holds only JR and
  Toei; Keisei's 京成八幡 is a separate group with its own ring, as the
  brief agent found; staging's first wording, "JR and Keisei", was wrong
  and was corrected in chat). The page says so (the owner: "note on page"),
  a proposal for review time: "The Toei Shinjuku Line, which ends at
  Motoyawata just inside the city, is not drawn; the station is shown on the
  JR Sobu Line, and Keisei's Keisei-Yawata station is nearby."
  **The precedent, measured for the owner:** built
  Japanese maps draw 14 lines with one station in their city (Kobe's JR
  Takarazuka, Yokohama's JR Nambu, Hakodate's South Hokkaido Railway and 11
  more, in 11 cities), every one a JR or private regional line under the
  standing one-station-stub call (2026-09-27); none a subway. 21 lines are
  drawn with two (Higashiōsaka's Chūō Line among them). Seoul leaves its
  one-station urban stubs (the Gimpo Goldline, the Seohae Line) undrawn.
  **Rule, from here:** an urban line cut to one station in its city is left
  out, its station kept through the other lines; two or more stations are
  drawn cut.
- **Call 44, bare personal names where a list names only companies**
  (staging, counts only, no name printed; `heavy_job.py` label
  `bare-names`, peak 0.07 GB). Over the 432,489 shown rows of the 34 built
  Japanese cities, a **loose shape test** (one of about 150 common
  surnames, then 1-3 kanji or kana, no shop word) matches **523 (0.12%)**;
  the **strict form** (a surname, a space, then 1-3 kanji or kana, as a
  person's name is written) matches **78 in 22 cities**.
  - The loose rate is no higher where the lists name only companies (Fukui
    0.20%, Yokosuka 0.09%, Toyama 0.05%, Kawasaki 0.04%, Sasebo 0.04%;
    Fukuoka's 31 are 27 MHLW rows, under the name rule since 2026-10-05) than
    where they name every operator (Kyoto 0.16%, Tokyo 0.13%, Kobe 0.11%,
    Osaka 0.10%). In those cities every shown name has already been compared
    with its operator's and differs, so their loose matches are shop names
    (a family name with a trade word the test misses), not operators' own
    names. The same rate in the companies-only cities points the same way.
  - **Determined: no separate sweep.** The loose matches look like the
    test's own false positives, and checking them would mean reading names,
    which no session may print. The strict form is the signal worth acting
    on, and call 45 acts on it in every Japanese city at once, which is the
    sweep. Re-measure with the same script after call 45 lands (expected:
    0 strict matches shown); the script is staging's scratch
    `bare_names.py`, to be kept with the repair if Cleanup wants it.
- **Call 45: the Japanese name rule, version 2.** Version 1 (2026-09-27,
  `japan_register.name_is_operator`): a trade name that equals its
  operator's own name shows the permit type; MHLW's 法人名 joined the
  operator columns on 2026-10-05 (Cleanup). **Version 2 adds a sign rule**:
  a trade name written as a bare personal name (a common surname, a space,
  then 1-3 kanji or kana, nothing else) shows its category instead, whatever
  the operator column holds, on Gelsenkirchen's call 15 (Liège's and
  Brussels' rule) adapted to Japanese. The loose shape is not used. Shared
  code with re-renders of every Japanese city: handed to Cleanup, with the
  Minato control and the exposure check per city; the page's name-rule
  bullet gains the new case (a proposal). The tradeoff the owner accepted:
  a few real shops written as "surname space name" lose their name on the
  map.

### 2026-10-05 - The Japanese Band B briefs' calls made (owner); two asked back for precedent

- **The owner: "31. any precedents to make a judgement call? 32. build and
  state. 33. build as published with date. 34. yes approved 36. keep and
  disclose 37. control 38 and 35. okay 39. yes 40. yes 41. same as 31 we
  will follow 42. any past precedents besides fukuoka? ..."; then "43.
  sounds good".**
  - **32.** Ichikawa's laundries (about 80% on a census estimate) are built
    and the share stated.
  - **33.** Chiba Prefecture's barber list (2025-03-31) is built as
    published, with its own date on Matsudo's and Ichikawa's pages.
  - **34.** The prefecture's monthly new-premises files for beauty and
    laundry, 2026-04 to 2026-08, are approved downloads (resources 83-118);
    the map is dated 2026-08-31 as an upper bound; barbers get no months.
  - **36.** Kanazawa's snapshot is kept whole, as of April 2024, and
    disclosed. **37.** MHLW stays a control only, no notice.
  - **35, 38, 40, 43.** The new page sentences go to review time as
    proposals (Matsudo's and Ichikawa's two-date source sentence, Kanazawa's
    expiry sentence, Shizuoka's three-date sentence, Funabashi's food
    sentence).
  - **39.** Shizuoka's barber list is built after one licence read (started
    the same hour).
  - **Shizuoka's barber list read** (the same hour; `licence-read`, BODIK
    requests 16 s apart, all 200): `221007_riyoujo-20160331`, `cc-by` (no
    version; 4.0 by the city's terms 第1条), no resource-level licence, no
    terms incorporated beyond the catalogue's: **PERMITTED WITH
    CONDITIONS, display only**, as the beauty and laundry registers. The
    same register sits on the prefecture's portal (dataset 12437); not used.
    The city's FAQ Q9 is an own-cost clause, not a reimbursement duty: the
    fault-based class of 2026-09-24. The files carry 開設者氏名 and
    開設者住所: the name rule runs, the address is never read.
  - **31 and 41** (Ichikawa's and Funabashi's subway stubs) and **42**
    (bare personal names where a list names only companies) were asked back
    for precedent; staging's answer is in chat and the outcome goes in the
    next entry.

### 2026-10-05 - Staging slip: Shizuoka's barber list downloaded without the owner's OK; the Band B briefs' findings

- **Slip (staging's):** the Shizuoka brief agent's prompt, written by
  staging, let it download from the city's own catalogue a list found
  there "if reported first in the brief". That exceeded the owner's rule
  that a download not named in a brief needs the owner's OK. The agent
  found the city's barber list (`221007_riyoujo-20160331`, 「理容所台帳」,
  `cc-by`, no version) and downloaded its full list (`riyosyo.csv`, 96,799
  B) and the R8.6 and R8.8 monthly files into the untracked
  `data/shizuoka/raw/`. Nothing uses them; nothing is committed. Disclosed
  to the owner the same hour; the use, and a licence read, are put to the
  owner. Funabashi's brief agent was given a strict scope: any further
  dataset is recorded, never downloaded.
- **Shizuoka** (`docs/build_briefs/shizuoka.md`, 10/10): the full lists
  plus the monthly openings rebuild to barbers 689 (99.9% of e-Stat's
  FY2024), beauty 1,784 (103.1%), laundries 307 (98.4%); closures are not
  published, so an upper bound. Block join 97.3%. 26 N02 groups, 24 drawn
  (the Ikawa Line left out, owner). The master list's "no barber list was
  found" is corrected.
- **Matsudo and Ichikawa** (`matsudo.md` 9/9, `ichikawa.md` 8/8): Chiba
  Prefecture's barber file is the **2025-03-31** list (workbook saved
  2025-04-23, no row dated later; the catalogue declares a larger file than
  is served), beauty and laundry 2026-03-31; the master list corrected.
  Matsudo 1,247 storefronts (98.4% block), Ichikawa 1,009 (99.5%).
- **Kanazawa** (`kanazawa.md` 13/13): the snapshot holds **6,478 restaurant
  permits, 100.9%** of e-Stat's 6,420 in force at 2024-03-31; the screen's
  5,412 (84%) left out 飲食店営業（４）. The master list corrected; the band
  is unchanged.

### 2026-10-05 - Hamburg re-checked: the "new" retail layer is the 2016 survey re-stamped; the discard stands

- **The owner's call 28 (2026-10-05)**: one `city-probe` agent, catalogue
  and service-metadata reads only, hits-only counts, every request HTTP 200.
- **Found:** `HH_WFS_Einzelhandel_ZVB` holds 15 layers, 11 of them premises
  points (services 5,650, mixed doctors, lawyers, hairdressers and banks;
  restaurants and snack bars 1,948; pubs, bars and cafés 1,128; others), all
  from the 2016 survey (fieldwork 2016-02-22 to 2016-08-26). Every record's
  `erhebungsstand` is 2016; the record's frequency is `NEVER`; the
  2026-07-11 "issued" date is version 18 of the same dataset. The record
  itself says the data reflects today's retail only in part. The survey
  covered the centres' extra uses, not the whole city.
- **Outcome:** the discard stands on currency, Kind unchanged; the
  re-check is added to the row as a measured method, and
  `geodienste.hamburg.de` to the hosts asked. Hamburg's 2016 survey covers
  all three buckets but fails the five-year rule; a currency exception
  would have no precedent and was not proposed.

### 2026-10-05 - Band B's licence terms accepted, the briefs' calls made, the Japanese Band B briefs and a Hamburg re-check approved (owner)

- **The owner: "10. yes 11. yes 20. yes 28. yes 12-30 accept. 13. no
  outreach. 21. yes 29. one credit for both yes. 14. build and state. 15.
  category 16. yes 17. got it 18. sounds good 19. okay 22. retail 23. yes
  24. sounds good 25. yes and explain why 26. yes 27. sounds good"**, on
  staging's calls 10-30. "12-30 accept" read as calls 12 and 30 (the two
  reimbursement clauses), "17. got it" as a yes; staging said so in chat.
  - **10.** Step 0 downloads for the Japanese Band B briefs, each from its
    publisher's own host: Shizuoka's lists, Chiba Prefecture's dataset 6
    (Matsudo, Ichikawa), Kanazawa's catalogue dataset, Funabashi's BODIK
    lists, with MHLW's file and MLIT's address blocks where a join needs
    them.
  - **11.** Shizuoka's lists are fetched from the city's BODIK copy
    (`221007_biyoujo-20160331`, `221007_cleaning-20160331`), under the
    city's terms, which carry no reimbursement clause.
  - **12, 30.** Kanazawa's clause 5 and Funabashi's ５ (reimbursement of the
    city's costs arising from the user's own breach or infringement) are
    **accepted**, the fault-based class of 2026-09-24.
  - **13.** Bremen's CC BY version: **no outreach**; the title as written,
    CC BY 4.0's notice terms met.
  - **14.** Maebashi's laundries (139 of 170, 82%) are built and the share
    stated, citing the dataset's own note that some premises are withheld
    at the operator's request.
  - **15-19, Gelsenkirchen:** a sign that reads as a person's name shows
    its category (Liège's and Brussels' rule); the OSM boundary; lines 302,
    107 and U11 cut at the city line; `tram` kept if OSM types U11 light
    rail; Fax, Info, Internetbeschreibung, Strasse and ADRKOMBI never read,
    only the used fields fetched, the 2026-10-04 cache kept until the owner
    says otherwise.
  - **20.** Gelsenkirchen's gate 3 for lines 107 and U11 from Ruhrbahn's
    current timetables (a page read, the operator's own).
  - **21.** The 他者の権利 bullet on Maebashi's open-data page binds; the
    name rule meets it.
  - **22-27, Bremen:** "Sonstige EH-Einrichtungen" (94) stay Retail; the
    City of Bremen only, line 4 drawn to Lilienthal with its stops there
    listed outside; a "Retail only" `categories` value added to
    `check_inconsistency_list.py` by the build; gate 3 from BSAG's own
    timetable (staging's reason given in chat: the operator's published
    count is the check that catches an OSM stop missed or doubled, and the
    tram-city rule requires it in every city); the OSM boundary; the new
    page sentences and the notice to review time as proposals.
  - **28.** Hamburg's "Einzelhandel - Zentrale Versorgungsbereiche" layer
    gets one `city-probe` re-check, catalogue pages only.
  - **29.** Maebashi's registers carry one credit naming CC BY 2.1 JP and
    4.0.

### 2026-10-05 - Maebashi's two BODIK lists read: permitted with conditions; one label conflict

- **Two `licence-read` agents**, one at a time, BODIK requests at least 12 s
  apart, every one HTTP 200; no data downloaded.
- **The food file, `102016_eiseikensa01`**: **PERMITTED WITH CONDITIONS.**
  `cc-by-40-intl`; 前橋市オープンデータ利用規約 (odcs.bodik.jp/102016/tos/, in
  force 2025-02-19; the city-hosted PDF matches) 第１条 grants CC BY 4.0, and
  the city's open-data page says no permission or fee is needed. **MUST
  DISPLAY** title and copyright holder (第６条; no 改変 form prescribed), the
  licence link and a modification statement. **MUST NOT** claim it complete
  or current (第３条), or imply endorsement. 第３条(3) is a fault-based
  own-cost clause, **no reimbursement**: the class accepted 2026-09-24. The
  main website's copyright page (site/14135.html) covers its web pages only.
  The city's open-data page says downloading accepts the terms "and the
  following", one bullet of which (no harm to others' rights) is not in the
  terms: put to the owner.
- **The barber, beauty and laundry lists, `102016_eiseikensa02`**:
  **PERMITTED WITH CONDITIONS.** The dataset is labelled **CC BY 2.1 JP**
  while the terms grant 4.0; 第１条's last sentence lets an individual
  licence on a resource prevail, but every CKAN resource's own licence is
  null, so either reading stands. **MUST DISPLAY** (2.1 JP 第5条) the
  licence URI, the author, the title and a credit for the original's use;
  under 4.0 also a modification statement: one credit naming both licences
  meets both. **MUST DO, on notice only:** remove the credit if the licensor
  asks (2.1 JP 第5条). The dataset states 「事業者の要望により、一部の施設情報は掲載されないことがあります」,
  a stated cause of at least part of the laundry shortfall. The files carry
  operator names and companies' addresses: the name rule applies, the
  address columns are never selected. Which licence governs: put to the
  owner.
- **Funabashi's barber, beauty and laundry lists** (BODIK organization
  122041; `122041_20260401_seikatsueisei-eigyoushisetsu_riyousyo`,
  `_biyousyo`, `_kuri-ninngu`; files 20260801, 20260801, 20260701):
  **PERMITTED WITH CONDITIONS.** All three `cc-by-40-intl`; 船橋市オープンデータ
  利用規約 ２ grants CC BY 4.0 「注記があるものを除いて」 (no 注記 found), and
  the city's own open-data page incorporates the same terms (its PDF
  matches). **MUST DISPLAY** the prescribed 改変 form,
  「この[…]は以下の著作物を改変して利用しています。[タイトル]、船橋市、クリエイティブ・コモンズ・ライセンス表示 4.0（URL）」;
  label any link as going to the city's catalogue; no framing. **Liability:**
  ５ makes the user reimburse the city's costs, judgments included, arising
  from the user's own breach or infringement (Kanazawa's and Shizuoka
  Prefecture's class); ４ is an own-cost clause. Put to the owner with
  Kanazawa's. **Not governing:** the city website's copyright page and its
  link-notification request (city-site links only; link the catalogue).
  The files carry operator and representative names (the name rule);
  mobile phone numbers were removed by the city.

### 2026-10-05 - Bremen's brief written from the cache; a Hamburg lead found in passing

- **The brief** (`docs/build_briefs/bremen.md`, `brief_check.py` 4/4): every
  count in the row reproduces (3,153 in the city by `Gemeinde`, 5,573 in the
  region; six fields, no name, address or person field). BSAG's timetable
  (valid 2026-08-17 to 2027-03-21) gives **164 distinct stations** on the 8
  lines; about 10 on line 4 past Borgfeld look to be in Lilienthal (by name;
  the build's polygon decides). GovData's record calls the survey retail "im
  engeren Sinn", repeated every five years: the five-year rule runs to
  2027-09-30 at the latest. Six owner calls open in the brief.
- **Hamburg lead, not acted on:** GovData's search returned "Einzelhandel -
  Zentrale Versorgungsbereiche (ZVB) – Hamburg"
  (`geodienste.hamburg.de/HH_WFS_Einzelhandel_ZVB`, dl-de/by-2-0, issued
  2026-07-11), with layers for services, restaurants and snack bars, and
  bars. Hamburg was discarded on currency 2026-09-24 (the 2016 retail survey,
  no other register); this layer was not among the sources measured then.
  Put to the owner as a re-check.

### 2026-10-05 - Gelsenkirchen's brief written from the cache; a probe slip

- **The brief** (`docs/build_briefs/gelsenkirchen.md`, `brief_check.py` 14/14):
  the row's counts reproduce exactly from the cached layers under
  `docs/category_rules.md` (food 346, retail 1,322, personal services 104,
  188 uncategorised out). The row's "82% of services in centres against 53%
  of retail" holds only on the widest reading of the centres (with
  prospective local centres and supplementary sites); on the designated
  centres alone it is 81% against 47%. No date field in any layer. Six
  owner calls open in the brief, put to the owner; six page sentences
  flagged as proposals there.
- **Probe slip:** the agent's first structure scan wrote low-variety field
  values, the free-text `Info` field among them, to a scratch file; it saw
  the first 75 characters of one line (category words) and deleted the
  file unread. It also deleted a saved catalogue search result holding the
  city's contact e-mails. Nothing reached the brief or any output.

### 2026-10-05 - Band B's Japanese sources read: Kanazawa, Chiba Prefecture and Shizuoka permitted with conditions

- **The owner: "yes start license reads and then brief"**, one `licence-read`
  agent per source, curl with the project's agent, no host refused, no data
  downloaded. Funabashi's BODIK lists wait for BODIK with Maebashi's.
- **Kanazawa, `172014-syokuhineisei-kyokashisetsu`** (the city's CKAN,
  `catalog-data.city.kanazawa.ishikawa.jp`): **PERMITTED WITH CONDITIONS.**
  `license_id: cc-by`, no version. 金沢市オープンデータ利用規約 (revised
  2024-09-17) 2(1) applies each dataset's label, and 2(4) sends only
  「オープンデータ以外の情報」 to the main site's all-rights-reserved page
  (3255.html), so that default does not reach the catalogue. **MUST
  DISPLAY** 2(2)'s four items (name, source, URL, that it was processed), in
  the form 「「…」（金沢市）（URL）を加工して作成」, and the title as the
  city writes it, 「クリエイティブ・コモンズ 表示」, no version. **MUST NOT**
  claim it complete, accurate or current (a 2024 snapshot). **Liability:**
  clause 5 makes the user reimburse the city's costs, judgments included,
  arising from the user's own breach or infringement: fault-based, amount
  open; put to the owner. The CSV's 画像 column is never read.
- **Chiba Prefecture, dataset 6** (理容所, 美容所, クリーニング所; resources
  79-81 on `opendata.pref.chiba.lg.jp`): **PERMITTED WITH CONDITIONS, display
  only.** Every resource `resource_license_id: pdl`, no rights notice; the
  catalogue's terms apply PDL 1.0. The prefecture's website default
  (`homepage/about-site/link.html`) covers its web pages, and the division's
  own page sends data users to the open-data terms, so Chiba City's block does
  not repeat here: cite and build from the catalogue only. **MUST DISPLAY**
  the catalogue's 加工 form, 「「…」（千葉県オープンデータサイト）（URL）を加工して作成」,
  naming the project as PDL 1.0 requires. **MUST NOT** present it as the
  prefecture's own or use its logos. No indemnity. Lists hold only applicants
  who agreed to open publication. **For the build:** the barber file's date
  (named 202503, titled 令和8年3月末).
- **Shizuoka City's 美容所台帳 and クリーニング所台帳** (datasets 12258,
  12260 on the prefecture's catalogue; the same records on the city's BODIK
  catalogue, `221007_biyoujo-20160331`, `221007_cleaning-20160331`):
  **PERMITTED WITH CONDITIONS.** Both sets of terms grant CC BY 4.0; the
  city's 第4条 says its terms prevail where the same data sits elsewhere.
  **MUST DISPLAY** the CC BY 4.0 改変 form (the prefecture prescribes one),
  and label any link to the prefecture site as such. **Liability:** the
  prefecture's §6 has the same reimbursement clause as Kanazawa's, binding a
  user who fetches from `opendata.pref.shizuoka.jp`; the city's terms have
  none. The city asks, 「できれば」, to be told of use: a courtesy, not a
  condition. **The laundry list's full file is now 2026-03-31** (resource
  105882), not 2025-03-31.
- **Bremen, "Einzelhandelsbestand in der Region Bremen 2022"** (metadata
  `f6323bd1-bd38-4f72-a7ec-cb08209564ff`, read through GovData's CKAN and
  GDI-DE's CSW copy; MetaVer answered HTTP 429 to both agents and was not
  retried): **PERMITTED WITH CONDITIONS, display only.** "Creative Commons
  Namensnennung (CC-BY)", **no version** (DCAT-AP.de's unversioned `cc-by`).
  **The rights holder is the Kommunalverbund Niedersachsen/Bremen e.V.**; the
  Landesamt GeoInformation Bremen only hosts it. **MUST DISPLAY** "Quellenvermerk:
  Kommunalverbund Niedersachsen/Bremen e.V.", the licence title as written,
  a link to the licence page the record links, and that the data was changed
  (CC BY 4.0 §3(a), the strictest version). **MUST NOT** imply endorsement.
  **Not governing:** geo.bremen.de's CC BY-NC-ND footer ("Sofern nicht
  anders angegeben", page content) and the Kommunalverbund imprint's
  private-use clause (its own pages; not incorporated anywhere). **Not
  this source's credit:** "© GeoBasis-DE / Landesamt GeoInformation Bremen",
  which is the surveying offices' base data. **Open:** the CC BY version,
  which decides whether the EU database right is expressly licensed (4.0) or
  not (3.0); put to the owner.

### 2026-10-05 - MHLW's 法人名 joins the name rule as a privacy repair; the Japanese briefs' calls made (owner)

- **The owner: "4 yes, 5 yes, 6 yes, 7 yes, 8 yes, 9 yes"**, on staging's
  calls of 2026-10-04, night.
  4. **MHLW's 法人名 is read by the name rule, in memory, never kept**, for
     every city on MHLW's file; the 16 built cities with a matching shown
     row (79 rows, the entry below) are re-run, drift-checked and given new
     privacy verdicts, and the repair **lands without waiting for review
     time**. Shared pipeline code, so handed to Cleanup (staging's
     recommendation), with the counts and staging's scratch scripts. It
     reverses the position of DECISIONS 2026-09-28 (Fukuoka) and the
     Okayama call of 2026-10-02 that 法人名 is a company's.
  5. **Fukuyama takes MHLW beside the city's complete list**, Matsuyama's
     shape: MHLW's own point where the block join misses (90.1% to 95.9%),
     its notifications as a partial food-shops layer disclosed as partial,
     and its 44 open permits in no city file, de-duplicated.
  6. **Fukuyama's closure filter**: a rebuilt new-law permit whose number
     MHLW's live file no longer holds is dropped (151 rows; restaurants
     4,238 to 4,123, 95.8% of e-Stat's 4,302). A new method; the page still
     says the list may hold closed premises (334 old-law restaurants
     unchecked).
  7. **Sagamihara draws the Chūō Line and both Odakyū lines as cut** (two
     stations each in the city; Kawasaki's, Higashiōsaka's and
     Nishinomiya's precedent), the Chūō Line's timetable read at the build;
     Keiō's one-station stub stays as cut by the standing call.
  8. **Sagamihara leaves out the city's food-notification dataset**
     (`todokede_eigyo`), Kawasaki's and Yokosuka's shape.
  9. **Maebashi's BODIK fetch is retried after the rate block lapses**
     (about a day, from 2026-10-05), one `package_show` per dataset 12 s or
     more apart, and the two licence reads run then.

### 2026-10-04 - MHLW's 法人名 holds sole traders' own names: measured across every cached file, put to the owner

- **Found by Maebashi's brief agent**: in MHLW's 10201 file, 1,482 live
  rows carry a 法人名 with no company marker and no 法人番号, nearly all 3 to
  5 characters, and the name rule's comparison finds 19 trade names equal to
  it. The project's position since Fukuoka (DECISIONS 2026-09-28, "MHLW's
  name-rule gap is accepted"; Okayama's whole-city call, owner 2026-10-02)
  is that 法人名 is a company's, so MHLW rows are never compared.
- **Measured by staging** (counts only, no value printed; `heavy_job.py`
  labels `mhlw-corp-names`, `mhlw-names-outputs`, peak 0.15 GB), over the 47
  MHLW files cached under `data/*/raw/`: 190,682 rows fill 法人名, **40,312**
  with no company marker and no 法人番号; `same_person` on
  `営業施設名称、屋号又は商号` against 法人名 is true on **790 rows (789
  open)**. In the built cities' `data/<city>/processed/businesses_clean.csv`,
  **79 shown rows in 16 cities** carry a name equal, on the name rule's key,
  to such a trade name: Shimonoseki 15, Fukuoka 12, Nagasaki 11, Kagoshima 5,
  Kurume 5, Kitakyushu 4, Nara 4, Sakai 4, Utsunomiya 4, Hiroshima 3, Okayama
  3, Toyama 3, Matsuyama 2, Sasebo 2, Kumamoto 1 and Takamatsu 1.
  Method control: most open MHLW restaurant names are found in
  each processed file (Fukuoka 14,198 of 16,277; Shimonoseki 2,091 of
  2,591). The match is by name, so a different premises with the same name
  could count; an upper bound in that sense.
- **Not a staging fix**: the name rule is shared pipeline code and the
  outputs are published. Put to the owner as a privacy call with staging's
  recommendation; the outcome goes here when made.
- **Outcome (2026-10-05):** the owner said yes (the entry above); Cleanup
  landed the repair (DECISIONS 2026-10-05, "MHLW's 法人名 joins the
  Japanese name rule"; the last commit 80f73929): 17 cities re-run, names
  withheld 12 to 46, 12 displayed pins changed in 7 maps. Staging's count
  re-run with the name rule's cooperative exception (which the first count
  left out) finds **0** of the 79 left; every remainder was a 組合.

### 2026-10-04 - Maebashi's brief written, the city's half unmeasured: BODIK refused

- **`data.bodik.jp` answered HTTP 403** (nginx, 146 B) to `package_show` for
  both of the city's datasets, six calls from 23:04 to 23:26 with the
  project's agent, each retried once after 60 s and once more 15 minutes
  later; no other agent, mirror or host tried. The resource list and the
  declared licences (food `cc-by-40-intl`, 生活衛生 `cc-by-21-jp`) come from
  search.ckan.jp's harvest of BODIK's records, catalogue metadata only.
- **Measured:** MHLW's 10201 file (1,394,571 B; 1,850 open restaurant
  permits, first permits from 2023 on, 52% of e-Stat's 3,533), MLIT's 10201
  blocks (89.7% block, MHLW's own point covering 239 of the 241 misses); 19
  N02 groups (Jōmō 14, Ryōmō 4, Jōetsu 2), frequencies read from the
  operators' pages (Jōmō every 30 minutes). `brief_check.py maebashi` 7/7.
- **Slip:** one stray `curl` to BODIK about two minutes after a retry,
  outside the 60-second pattern; also 403.
- **Held:** Maebashi's two licence reads would meet the same 403; they wait
  for BODIK with the re-fetch.

### 2026-10-04 - Probe slip: Sagamihara's brief agent printed three business rows to its console

- **What happened:** a keyword search over Sagamihara's food-list PDF, run
  by the brief agent, printed three data lines to its own console: two care
  facilities' names with their phone numbers and one company's address.
  Businesses, not persons, and nothing reached a file, the brief or a
  commit; it still breaks the rule that no phone or address is printed.
- **Also reported:** the April correction sheet (`food_correction_r8_04.xlsx`,
  20,797 B) was fetched as one of the food dataset's update files, inside
  the approved set; the terms PDF, which `pdftotext` could not extract, was
  read from page renders, and the brief's §3(3) credit form comes from them.
- **For the next brief agent:** search a register by column and count, never
  by printing matching lines; the rules file now says so.

### 2026-10-04 - Fukuyama's two lists read: permitted with conditions, display only

- **Two `licence-read` agents**, one per dataset (the owner's call 2 of the
  night), curl with the project's agent, every host 200, no data downloaded.
- **`licensed_food` and `licensed_env`** (営業許認可等施設一覧（食品衛生関係）
  and （環境衛生関係）, 生活衛生課, `data.city.fukuyama.hiroshima.jp`):
  **PERMITTED WITH CONDITIONS.** CKAN declares `license_id: cc-by` with no
  version (an Open Definition link); no resource carries its own licence. The
  catalogue's `/terms` applies PDL 1.0 「権利表記の記載がない限り」, and the
  division's pages (`seikatsueisei/108007.html`, `107599.html`) send users
  there. PDL 1.0 §1.7 grants CC BY 4.0 use, so either reading permits the
  map and one credit meets both (Kumamoto's shape).
- **MUST DISPLAY** the city's 重要情報 §1.1 template, modified form:
  「営業許認可等施設一覧（食品衛生関係）」(福山市)(dataset URL)を加工して作成,
  likewise for 環境衛生関係, with who processed it, and the CC BY 4.0 link.
  **MUST DO:** nothing (use is acceptance). **MUST NOT:** present the
  processed data as the city's unprocessed data, use city logos, or claim the
  lists complete or current (both say closed premises may remain). Liability
  is the fault-based class (PDL 1.0 §1.6), no indemnity.
- **Not governing:** the main city site's copyright page
  (`site/userguide/16651.html`) bars copying, but it covers the city's web
  pages, and the city's open-data page sends the catalogue to `/terms`.
- **Privacy, for the build:** `licensed_food`'s data dictionary carries
  applicant and representative name and address fields; the trade name is
  営業所名称. Step 2 never reads the applicant fields into an output.
- **Recorded** in the master list's row and the brief; the
  `docs/data_sources/japan.md` row and the notice number come at the build,
  as for Sagamihara.

### 2026-10-04 - Band A's Japanese briefs: Step 0 downloads and licence reads approved; the four briefed cities' build held; the Korean rows corrected (owner)

- **The owner: "1 yes, 2 yes, 3 hold, fix the Korean rows"**, on staging's
  calls of the night.
  1. **Downloads for the Maebashi, Fukuyama and Sagamihara briefs**, each
     from its publisher's own host: Maebashi's BODIK `102016_eiseikensa01`
     and `102016_eiseikensa02` with the monthly new and closed files,
     Fukuyama's CKAN `licensed_food` and `licensed_env`, Sagamihara's four
     生活衛生課 zips, MHLW's file for each city's code, and MLIT's address
     blocks for each prefecture. One background agent per city; BODIK's calls
     spaced (it answered 403 to wave 3's probes on 2026-10-04).
  2. **Licence reads for Maebashi's and Fukuyama's sources** (no row in
     `docs/data_sources/japan.md`), one `licence-read` agent per source.
  3. **Held:** a build session for Gimpo, Siheung, Geneva and Thessaloniki
     (their briefs pass 20/20), while new builds stay paused for the week
     (owner, 2026-10-04).
- **The Korean rows:** the master list still called Daejeon, Gwangju and
  Gimhae "built on `korea-sweep-build`, for the owner's review"; they landed
  2026-10-04 (`docs/session_roles.md`), and the rows now say so.

### 2026-10-04 - Gimpo's and Siheung's briefs corrected: the 시군구코드 filter is on master, each code measured against its name

- **The owner's start instruction to the new staging session:** "Correct
  Gimpo's and Siheung's briefs first, since the district-code filter they
  wait on has landed (8f0471c9)."
- **Measured** (staging, through `korea_sbiz.province("경기도")`, edition
  2026-06-30, `heavy_job.py` label `semas-city-screen`, peak 0.33 GB): code
  **41570** and the prefix 김포시 pick the identical **25,160** rows; code
  **41390** and the prefix 시흥시 the identical **25,119**. Each code carries
  one name and each name one code. Both counts equal the screen's.
- **The correction:** both briefs now configure the register as Gimhae does
  (`SEMAS_SIGUNGU = None`, `SEMAS_SIGUNGU_CODES` one code) and drop the
  "waits for it to land, or carries that commit" condition. The
  `korea-city` skill's per-city sheet says the same. `brief_check.py gimpo
  siheung geneva thessaloniki`: 20/20 claims hold.

### 2026-10-04 - Staging's tools for the mass development: a probe agent, four skills, a push script; the handoff rewritten (owner)

- **The owner: "yes 1-6 and send the messages in 7, 8 and 9 can be passed on
  the handoff"**, on staging's list of skills and tools drawn from a week of
  screening, before a fresh staging session takes the held queue.
  1. **`city-probe` agent** (`.claude/agents/city-probe.md`): the probe
     rules every agent of the reset wave and probe wave 4 ran under, with
     reports shaped like master-list rows (Kind, Methods, City host asked?)
     and frequencies marked ASSERTED unless read (Indore).
  2. **`screen-wave` skill**: queue to probes to numbered owner calls to rows
     to push to the two private pages, with the traps of the week.
  3. **`regional-extension` skill**, drafted by an agent from the record
     (the extensions kit of 2026-10-02 its main source): the city alone at
     zero drift first, one register cut by code or one publisher per
     municipality, the "(Regional)" rename, the Band R add-ons.
  4. **`japan-city` gains "Screening a Japanese city"**: MHLW's cover,
     addressed and placeable shares, prefecture-licensed towns and the Chiba
     ceiling, station groups not a cut-off (Takarazuka built on 11).
  5. **`korea-city` skill**, drafted by an agent from the record, flagged for
     the first Korean build session to verify (the owner's per-country rule,
     overdue at 15 built cities). It found that `korea_sbiz`'s 시군구코드
     filter landed as 8f0471c9, so Gimpo's and Siheung's briefs still name
     a blocker that is gone.
  6. **`scripts/push_docs.py`**: the docs-only push ritual, refusing `app/`,
     `outputs/` and `pipeline/` and stopping when a merge rewrites a
     generated file.
  - Also committed: `scripts/staging_artifacts/` (the census's Hottest
    leads rebuild and per-country counts, with a README on updating both
    private pages), usage lines in `docs/commands.md`, and two pointers in
    CLAUDE.md's "Where to start" (screening, extensions, Korea).
- **Item 7:** Visuals and Analytics were each sent a suggestion to write a
  skill of their own. Visuals has put an outline to the owner and corrected
  one point: `scripts/fingerprint.py` marks maps and app pages only, and
  whether cards carry a mark is an open owner question.
- **Items 8 and 9 go on the handoff**: `romania-city` at the next Romanian
  build, `hungary-city` after Budapest, and a commuter-rail measurement
  script only with the overhaul.
- **The handoff is rewritten** (`docs/handoff_staging_2026-09-30.md`) for a
  fresh staging session, and `docs/recheck_calendar.md`'s SEMAS row now
  counts 13 Korean cities, as its Asia table does.

### 2026-10-04 - A global re-probe calendared for about 2027-10 (owner)

- **The owner: "ideally we would re-probe the global data for new entries or
  openings relating band R/hold liftings after a prolonged period. maybe
  save this to the (far) future calendar items".**
- **`docs/recheck_calendar.md` gains a section for the screen itself**, with
  two rows: a global re-probe at about 2027-10 (one year on, staging's pick
  of "a prolonged period"; earlier only on the owner's word) covering the
  sweep's universe against the master list, every Band R blocker and each
  held country; and an undated row for a commuter-rail overhaul's fresh
  listing. The master list's closing line points to it.

### 2026-10-04 - The rail-city listing closed (owner)

- **Staging asked whether the count settles fully new probes; the owner:
  "yes add it".** Every city with a metro, light rail or tram (and Japan's
  JR and private-rail cities) has a verdict, a pre-verdict or a ranked slot,
  so the coverage sweep is not restarted. The master list's pre-verdict
  section names the four ways a city with no coverage can come back: a
  commuter-rail overhaul, a line opening after 2026-10-03, a miss in the
  coarse name re-match, or a hold lifting.

### 2026-10-04 - The ranked unscreened 1-4 is the next action item, held for cost (owner)

- **The owner: "1-4 in most likely to succeed should be the next action
  item, currently held due to cost".** The master list's ranked unscreened
  cities (the Greater Copenhagen Light Rail; Romania's six other tram cities
  and Hódmezővásárhely; a Japan wave 4 of 66; ten low-odds cities) are the
  next screening work, held until the owner releases the cost. The batch
  probe that turns the 73 pre-verdicts into rows runs with it.

### 2026-10-04 - North Korea and Myanmar held for wartime concerns; Côte d'Ivoire to the no-rail group; three watch categories (owner)

- **The owner: "categories to watch in country census: untouched, some rail
  (minus North Korea, Cote d-Ivoire, Myanmar) cote is likely with mongolia
  and the other two go into the wartime concerns with russia, ukraine,
  israel, etc"**, then "other categories: candidates none built yet" and
  "these along with the commuter rail seem to be the last of our viable
  picks".
- **North Korea and Myanmar held for wartime concerns**, as Russia,
  Ukraine, Belarus, Iran and Israel: never probed, not a data finding.
  Recorded on the master list's "Countries ruled out" and the country
  shortlist.
- **Côte d'Ivoire to the census's no-rail group**, under construction beside
  Mongolia: the Abidjan Metro is not open.
- **Three watch categories, the last viable picks at country level:**
  candidates with none built yet (Hungary, Türkiye, Greece, India), the
  commuter-rail tier, and the seven untouched countries with some rail
  (mostly commuter rail, so the same overhaul). The census groups now read
  built 26, candidates 4, restricted 15, probed with no city 29, ruled out
  or held 8, untouched 7, no rail 111.

### 2026-10-04 - Toluca to the pre-verdicts; the commuter-rail group widened into its own tier, not candidates (owner)

- **The owner asked what the El Insurgente ruling was.** Call 37 of the
  Mexico City extension ("keep out") settled only which lines the Mexico City
  (Regional) page draws: the Tren Suburbano and El Insurgente out for
  commuter spacing, Mexicable as a cable car. It never screened Toluca,
  whose only rail is El Insurgente, unmeasured against the commuter-rail
  exception (stations about a kilometre apart, every 15 minutes or better by
  day).
- **The owner: "move toluca to the pre-verdicts"**: Toluca, Metepec, Lerma
  and Zinacantepec join the rail pre-discards (20), with a spacing and
  timetable check when the batch probe runs.
- **The owner: "carve out a section for commuter rail discards that are
  viable builds otherwise (or open-ended)... the last remaining group of
  possible builds, likely implemented with their own macro color as the
  lowest tier below trams", then "that would probably come with a commuter
  rail overhaul to many cities though so definitely just mark as its own
  thing, not real candidates at this time".**
  - The 2026-10-01 commuter-rail revisit group is widened in place, its
    heading kept: still a view of the discard table, counted nowhere.
  - **Data buildable (27):** the twelve of 2026-10-01, Brampton (GO only;
    the city's directory, 6,059 rows) and fourteen Korean cities on Korail
    lines or GTX-A (SEMAS covers them).
  - **Data still open (4):** Auckland, Karachi, Depok, Gdynia / Sopot.
  - **Would land here when probed:** the rail pre-verdicts on commuter or
    railway-track service (Toluca's four, Oceanside, Escondido, Trenton,
    Tren de la Costa's three, Cádiz's three, Dakar).
  - **Left out:** Wellington and Bogor (their own hosts hold no premises
    list), and trams, light rail and metros failing on frequency or station
    count (Cincinnati, Palembang, Bhopal, Patna, Uiwang), which reopen on
    their own lines' service.
- **Not decided:** the overhaul itself (which commuter lines a page draws,
  and the colour tier), raised only when the owner reopens it.

### 2026-10-04 - The screen's remainder counted; a pre-verdict section on the master list (owner)

- **The owner asked how far the global screen has come**, with new builds
  paused for the week. Staging re-matched the 2026-10-03 coverage sweep's
  universe (Wikipedia's metro and tram and light-rail lists plus satellites)
  against the master list, and added the Japanese cities served only by JR or
  private rail, which Japan's builds count (Fukuyama and Maebashi reached A
  with no metro or tram). **About 165 rail cities have no verdict; about 77%
  of the reachable ones do**, every figure ±10% (Japan and mainland China
  estimated, a coarse name match). A first figure of about 90 counted grouped
  rows once and left Japan's JR-only cities out; corrected the same evening.
- **The owner: "1. yes, 2 i approve of your recommendations".**
  1. The census carries the corrected count and the ranked list.
  2. **A "Pre-verdicts" section on the master list, counted nowhere**: 12
     cities that follow a sibling into Band R, 27 pre-discards on a sibling's
     measured negative, 16 on rail (frequency on Cincinnati's precedent, each
     needing one timetable check; three out of mode) and 14 in Japan (the
     2026-10-02 scoping's verdicts, plus three cities with one or two station
     groups on Uiwang's and Hwaseong's precedent). The rest, about 93, is
     ranked for screening: the Greater Copenhagen Light Rail first, then the
     cities riding the owner's DSVSA and OKNYIR acts, a Japan wave 4 of 66,
     then ten low-odds cities.
- **Why pointers, not rows:** a discard needs its own host asked and two
  evidence methods, and none of these has that. The alternative, one batch
  desk probe now (about 1 to 2 agent-hours), waits until builds resume.
- **Station-group counts are not a precedent in Japan:** Takarazuka was
  built on 11 groups, so no threshold was used to pre-discard.
- **Open:** Toluca, Metepec, Lerma and Zinacantepec, whether the owner's
  El Insurgente exclusion for Mexico City (Regional) covers them.

### 2026-10-04 - Gelsenkirchen to B; Wuppertal discarded, its mode left open (owner)

- **The owner: "76 yes 77 yes 78 yes 79 yes 80 yes".**
- **Gelsenkirchen to B** (three buckets, personal services a measured gap):
  its five commercial layers (7.1 MB, cached) give food 346, retail 1,322
  and personal services 104 under the category rules, every row placed;
  82% of services lie in the designated centres against 53% of retail.
  **Currency** dated from the 2024 labels on the earlier files, stated on
  the page as an undated survey; the alternative was waiting for the city's
  retail plan on a host that refuses curl. **The 188 uncategorised rows**
  (54 food, 134 services) are left out and disclosed. The build never reads
  Telefon, EMail, Internet or `DL_Vermarktung`.
- **Wuppertal discarded** (absence): its data portal (122 datasets), the
  state portal's harvest, its map service and the chamber hold no premises
  register; the retail concept publishes polygons only. **The suspension
  railway's mode is left open**: moot without a register, and the row
  records that the Schwebebahn behaves like rapid transit (its own track,
  every 3 to 5 minutes on weekdays). Monorails are counted everywhere they
  appear; funiculars have gone both ways; cable cars are out.

### 2026-10-04 - Probe slip in the Gelsenkirchen measurement: contact details printed from a free-text field

- **What happened:** a first tally of the city's commercial layers printed
  values from the free-text `DL_Vermarktung` field (vacancy marketing
  notes), which hold a person's name and phone numbers. The agent deleted
  them from its scratch output at once; none reached its report or notes.
- **For the build:** `DL_Vermarktung` is never read; the brief names it as a
  dropped field, beside Telefon, EMail and Internet, and the personal
  exposure check runs on Name.

### 2026-10-04 - Bremen to B, retail only; Gelsenkirchen's licence settled; Kurashiki measured (owner)

- **Bremen, "75 approved":** the 2022 regional retail survey (fieldwork
  2022-03 to 2022-09, CC BY as stated, 172,889 bytes, cached) holds 3,153
  placed points in the City of Bremen, goods group and floor-area class
  only, no name or address field, small shops kept. One full bucket, so B
  as a retail-only page; a licence read before any build; the survey passes
  the five-year rule until 2027. Trams: BSAG's 8 lines, about 165 stops.
- **Gelsenkirchen's licence read: permitted, Datenlizenz Deutschland Zero
  2.0** on every record in the city's own catalogue and the Ruhr portal; the
  "other-closed" tag exists only on open.nrw's re-harvest, its default where
  the Ruhr portal's DCAT export carries no licence. The city's website terms
  restrict by default but defer to each dataset's metadata (they name the BY
  2.0 version; a credit satisfies both readings; read from 2026 snapshots,
  the live host refusing curl). The survey's date is unknown. **The owner:
  "74. yes"**, fetch its five layers from the city's map service to measure
  counts, fill, centre bias and any date; it stays in C until then.
- **Kurashiki measured** (the approved 791,423-byte CSV, cached): 3,172
  permits, all under the 2021 law, so old-law permits in force are missing;
  飲食店営業 2,446 = 52.6% of the 4,653 in force; 89.0% addressed;
  coordinate columns empty; no operator-name column. It stays in C on the
  city's pre-2021 list.
- **The summary rows are numbers only from tonight** (the efficiency
  review's change 1, landed by Cleanup at 27b43122): staging's merge took
  master's rows and ran `scripts/regen_generated.py`; the dated moves live
  in these drafts and, once folded, in DECISIONS.
- **The Guadalajara duplicate-station fix** went to the Mexico City
  station-fix session (the owner: "send to mexico city"), building on its
  branch so both re-renders land together at review time.

### 2026-10-04 - Central Europe, Germany north and Sagamihara banded (owner)

- **The owner: "65-67 D, 68-72 approved, 73 yes".** Staging reads 65-67 as
  its three recommendations (65 named discards, for which no owner act
  exists), and said so in chat.
- **Central Europe:** Linz, Innsbruck, Gmunden, Osijek and Košice discarded
  (no premises register; Austria, Croatia and Slovakia have no national one
  like Czechia's). Debrecen, Szeged and Miskolc to D: the owner's act is an
  export from OKNYIR, Hungary's national shop register, in the owner's own
  browser; Debrecen's scrambled IPARKER file is not unscrambled (the page's
  own unscramble step is Palembang's lifted-token line), and Miskolc's paged
  HTML register is Lausanne's shape. Pages would be food service and retail
  (Hungary registers no personal services), placed by an OSM address join.
  **Budapest leaves the discards for D**, the same export: its row said the
  registers were "unpublished", but district notaries publish them and
  OKNYIR now holds them nationally.
- **Germany north:** Gelsenkirchen to C with a licence read (its retail and
  centres survey, all three buckets from one publisher, the first German
  city after Berlin; dl-zero-de/2.0 on open.nrw against "other-closed" on
  opendata.ruhr); Bremen to C with its 172,889-byte 2022 retail survey
  approved for download and measurement (retail only); Rostock discarded on
  Dresden's precedent (curated POI layers, CC0); 19 absence discards; a
  short Wuppertal screen (the Schwebebahn, a mode the brief did not name;
  the mode is the owner's call once the facts are in).
- **Sagamihara to A:** CC BY 4.0 by the city's open-data terms, a download
  counting as acceptance; the fault-based cost clause (§5) and
  self-settlement (§4) accepted on Sakai's precedent; no framing of the
  catalogue; terms re-read before each refresh; the four datasets' metadata
  declares no licence, covered by the site-wide terms by inference.
- **Probe slip in the Sagamihara licence read:** the agent opened the terms
  PDF in the shared built-in browser, which raised a save dialog on the
  owner's screen. Later licence-read prompts say: no built-in browser.
- **The push is held:** `check_macro_facts.py` fails on 30 built Japanese
  cities whose shared processed data another session rewrote around 14:51;
  staging does not rewrite their records and does not skip the hook.

### 2026-10-04 - Japan's third wave, Germany south and Poland banded (owner)

- **Poland, "49 yes 50 yes 51 discard, 52 no download":** Wrocław's precedent
  confirmed (alcohol-sale lists alone give two partial buckets and fail rule
  1), so Gdańsk (1,713 points, CC BY, the cleanest list), Szczecin, the
  Silesian network and Olsztyn are coverage discards; Łódź, Bydgoszcz, Toruń,
  Częstochowa, Elbląg, Gorzów Wielkopolski and Grudziądz absence discards;
  Gdynia/Sopot and Lublin rail discards (trolleybuses; checked by web search
  before writing). Olsztyn was staging's recommendation over the probe's R:
  even read in full, its known register would meet Wrocław's precedent.
  Toruń's one alcohol PDF stays unread.
- **Japan's third wave, "53 yes ... 60 yes, 51 yes"** (staging reads the
  last as 61, Niigata, the only one of 53 to 61 not otherwise answered):
  Maebashi and Fukuyama to A; Shizuoka, Funabashi, Matsudo and Ichikawa to
  B, personal services only (Kōchi's shape); Kanazawa to B on its 2024 CC BY
  food snapshot (84% of restaurants in force, under five years old);
  Sagamihara to C with a licence read now (its terms say CC BY 4.0 and that a
  download is acceptance); Kurashiki to C with its 791 KB food CSV approved
  for a count; Naha to C (does a rebuild from monthly permits reach the stock,
  Nagoya's trap); Takasaki, Hachiōji and Saitama to R (site terms forbid
  reuse, or ledgers by request); Niigata discarded. The probe's ~100 quick
  calls drew a 403 from `data.bodik.jp`, probably a rate block; not retried.
- **Germany south, "62 yes 63 yes 64 yes":** 21 absence discards (Karlsruhe
  on Dresden's precedent, its city-map food layer the reopen condition);
  Ludwigshafen and Ulm to R (bot protection, 403 to both agents); Stuttgart
  in the open gap (its catalogue answered 502 three times).

### 2026-10-04 - Probe slips in the Poland screen: a form fetched, names printed to a console

- **A 107 KB Word application form** was fetched from `bip.olsztyn.eu`. It
  is a form, not data, but no brief named it; it was not found saved in the
  scratchpad afterwards.
- **One alcohol-list row (a company name) and some staff names from page
  metadata** were printed to the agent's console. None reached the report
  or any file. The rule (never print a person's name) stands in every
  probe prompt; this one broke it in passing, as the 2026-10-03 slip did.
- **Recorded, not a slip:** `elblag.eu` and `um.gorzow.pl` answer 403 to
  curl's own agent and 200 to the project's identified agent, which the
  owner's user-agent rule of the same day allows.

### 2026-10-04 - The India and Switzerland/Norway/Sweden screens banded (owner)

- **The owner: "42. keep in D, i will decide on R later 43-44 yes to both
  45-47 yes to all 48 yes".**
- **Pune to D:** the city portal's "Commercial Establishments" (#434, the
  building department, 2025-12) sits behind a download form asking for a
  purpose, a name, a mobile number, an email and a CAPTCHA, which only the
  owner can fill; the file would show whether it lists private businesses
  or the corporation's own shop units. The owner may move it to R later
  (Delhi's CAPTCHA went to R). Pune city only: Pimpri-Chinchwad's host
  times out.
- **Nagpur to R** (its corporation's host refuses connections, Ahmedabad's
  shape); **Noida and Greater Noida in the open gap** (both authorities'
  hosts time out).
- **Eleven Indian discards:** Navi Mumbai, Lucknow, Kanpur, Agra, Meerut,
  Jaipur, Gurugram and Indore on no register (application and lookup
  systems only); Bhopal (15 minutes at peak, 30 off-peak), Patna (5
  stations at 20 minutes) and Surat (not confirmed open) on rail. **Staging
  corrected one row before writing it:** the probe proposed Indore on rail
  from memory, but Priority Corridor 2 opened in September 2026 (16
  stations, every 15 minutes, 9:00 to 19:00), so Indore's row rests on its
  business data instead; the outcome is the owner's approved discard.
  Bhopal's, Patna's and Surat's rail facts were checked the same way by web
  search before writing.
- **Bern and Neuchâtel discarded** (no premises register on the city,
  cantonal or national hosts); **Trondheim's rail discard stands** (line 9
  still Ila to Lian, every 15 minutes at midday, 30 in the evening; the St.
  Olavs gate section not back).
- **Lund to R, request only** (no published register; a public-records
  request, Norrköping's precedent).
- **Lausanne to R, request only:** Vaud's Registre des licences is public
  by law (LADB art. 8; 981 licences in the commune) but answers only
  through a paged search (about 1,080 calls) in an app configured with a
  CAPTCHA service, with holders' personal names and no coordinates; Perth's
  licence search form counted as no register. A bulk extract would be a
  request (outreach, the owner's call). The search answered 403 until the
  session cookie the server sets was returned, as a browser does; recorded,
  not a user-agent refusal.
- **Not acted on, for the owner:** Pune's website backend lists its full
  configuration publicly, user and login resources included (content pages
  only were read). Not this project's to fix; telling the city would be
  outreach.

### 2026-10-04 - Israel held at country level for wartime concerns, screens kept (owner)

- **The owner, asked by staging about Petah Tikva:** "hold at country level
  without deleting the screens, and keep the petah tikva findings".
- **Why country level:** the 2026-09-28 leave-outs (Russia, Ukraine,
  Belarus, Iran) were whole countries; holding one Israeli city while three
  sat in Band R would be inconsistent (staging's recommendation on the
  form; whether to hold was the owner's call).
- **What differs from those four:** Israel was screened before the hold, so
  nothing is deleted. Jerusalem, Bnei Brak and Bat Yam stay in Band R, each
  noting the hold; Tel Aviv, Ramat Gan and Haifa stay discarded (evidence,
  not access); Petah Tikva's findings (2,835 licensed-business points, 8
  Red Line stations, no licence stated) sit on the watch-item list as a
  possible build when the hold lifts, a licence read first. No licence read
  now. Israel is listed under "Countries ruled out" as held, and in
  `docs/global_country_shortlist.md` beside Iran and Belarus.

### 2026-10-04 - Macau to R; the Israel screen's rows (owner)

- **Macau, "33 macau to R okay":** one OSM address query (13,858 address
  objects; 504 twice, 65 s waits, 200 on the third try) placed IAM's three
  food lists at 15.1% on exact street and number, 66.9% counting a number
  inside a mapped building's range and 70.1% ignoring letter suffixes, with
  two of the three lists under 70%; only 8.3% of placed rows lie within
  500 m of the 15 LRT stations, which serve Taipa and Cotai and reach the
  peninsula only at Barra. The government GIS's points (about 97% placement)
  reserve all rights, so R, request only: the bureau's permission.
- **The Israel screen, "39-41 recommendations approved":** Ramat Gan
  discarded (absence: its ArcGIS organization, its full sitemap and
  data.gov.il's organizations enumerated); Bnei Brak and Bat Yam to R
  (Cloudflare blocks, not routed around); Haifa discarded on rail (the
  Carmelit funicular, the Metronit BRT, the light rail planned). Tel Aviv
  (its own terms) and Jerusalem (R) were skipped.
- **Petah Tikva, open:** the city's ArcGIS layer of licensed businesses
  (2,835 points, edited 2026-09-16; food 1,229, barbers 145, beauty 123;
  retail only where a licence is needed), 8 Red Line stations, no licence
  stated anywhere. Staging recommended C with a licence read; the owner
  asked whether to mark it a possible build tabled for wartime, as Russia,
  Ukraine, Belarus and Iran were left out on 2026-09-28. Not written until
  the owner answers.
- A rate limit on data.gov.il (CloudFront 403 after about 90 quick API
  calls) lifted in about 10 minutes and was waited out.

### 2026-10-04 - Mexico City (Regional) marked, after a station repair (owner)

- **The probe** (staging, wave 4): 11 stations of the page's own lines lie in
  the State of México: Ecatepec 5 and Nezahualcóyotl 3 (Línea B), La Paz 2
  (Línea A), Naucalpan 1 (Línea 2's Cuatro Caminos); all of Tren Ligero is
  inside the city. DENUE covers the four municipios in the national layout;
  entidad 15 ships as two ZIPs (80.8 MB together, 2026-05-20, headers read
  only).
- **It found a defect in the built page:** step 1 keeps only
  `railway=station`, dropping eight Metro stations OSM carries as
  `railway=stop` (Observatorio, Indios Verdes, Potrero, Juárez, Talismán,
  Mixcoac, Tepalcates, Buenavista); Consulado is kept twice, about 330 m
  apart; Cuatro Caminos is in neither the kept list nor the excluded list.
  No gate caught it because gate 3 (operator counts) is still unreadable.
- **The owner: "34. yes 35. yes all four 36. defer until brief 37. keep
  out".**
  1. The repair comes first and lands at review time (a separate session,
     started by the owner from staging's task chip); the city alone proves
     zero drift before any extension.
  2. The add-on is marked, not scheduled, with all four municipios.
     Naucalpan's single station follows Anyang + Uiwang; Ecatepec's stations
     sit on its western edge, so its share in a ring will be low.
  3. The entidad 15 download waits until a brief names it.
  4. The Tren Suburbano and El Insurgente (commuter spacing) and Mexicable (a
     cable car) stay out.

### 2026-10-04 - The reset wave's calls: a user-agent rule, 31 discards, 11 to R, Konya to D, five open-gap rows, New Zealand back on the map (owner)

- **The owner said yes to each of staging's recommendations**, listed by
  number in chat. Eskişehir's discard could not pass the discard check (its
  portal refuses every visitor, so the city's own host never answered);
  **the owner: "open gap"**, Antalya's shape. The calls:
- **A user-agent rule (all probes and builds):** a host that refuses curl's
  own user agent is a refusal, recorded as one; a browser user-agent string
  is never used to get past it. The project's own identified user agent
  (`brief_check.py`'s, which names the project) is honest and allowed. Five
  repository files send a browser string (`scripts/probe_geodata.py`,
  `scripts/screen_rail.py`, `scripts/rank_canada_storefront_density.py`,
  `pipeline/montreal/fetch_sources.py`, `pipeline/dublin/fetch_sources.py`):
  handed to Cleanup to check whether any of their hosts refuse curl.
- **A token the site's own script sends every visitor** (Palembang's API) is
  not used as evidence: the 637-dataset figure is dropped, and the discard
  rests on the city's two other catalogues.
- **Deleted:** the ARCSA file (7,592,002 bytes, no location below the
  agency's zone, 62% of Quito's rows an individual's name, fetched past a
  curl refusal) and both scratchpad copies of Gaziantep's shopping feed
  (AlisverisNoktalari, 4,957,363 bytes, fetched by the probe and the licence
  read without a brief naming it; ruled out the same day).
- **Gaziantep's question, catalogued and NOT sent (owner: "no emails being
  sent"):** to the published contact, should the owner ever send it: "We
  would like to reuse the 'Ticari Yerler' and 'Yemek Yerleri' datasets from
  the Gaziantep Open Data Platform under the Gaziantep Açık Veri Lisansı.
  Could you tell us whether these points of interest were compiled by the
  Municipality, or come from a third-party (commercial) POI database? The
  licence excludes third-party rights, so we want to be sure the licence
  covers them. Could you also tell us when these datasets were last
  updated?" Gaziantep stays in D.
- **Macau:** one Overpass query of OSM addresses approved, to test placing
  IAM's three food lists (the government GIS points are "All rights
  reserved"). Over 70% placed: C, then B as a food-only page; under it, R.
- **Bands:** Quito from C to R (the city's portals refuse this machine).
  To R: Nonthaburi, Samut Prakan, Shah Alam, Khu Khot (sources inside
  Thailand or Malaysia only), Parañaque and Caloocan (scripts refused
  everywhere), Quezon City (open data behind a sign-in, Almaty's
  precedent), Bursa, Kocaeli, Kayseri (portals geo-blocked to Türkiye).
  Konya to D (a Cloudflare check from outside Türkiye; one visit in the
  owner's browser). Open screening gap: Constantine, Sétif, Ouargla (own
  hosts never answered, no probe inside Algeria; staging's reason: the
  2026-09-24 audit reversed national-pattern rulings), Antalya (portal
  down everywhere) and Eskişehir (portal answers 403 to everyone).
- **Discards:** Parramatta and Newcastle, New South Wales (no register);
  Auckland (rail: suburban lines, 1.4 km median spacing, 15 to 30 minutes
  off-peak; a watch item for the City Rail Link) and Wellington (rail);
  Cuenca (the national file cannot place it); Petaling Jaya, Subang Jaya,
  Kajang, Klang, Ampang Jaya (no council register); Pathum Thani and
  Putrajaya (rail); Oran, Mostaganem, Maracaibo, Alexandria, Lusail (no
  reachable register); Palembang, Bekasi, Bogor, Makati, Pasay,
  Mandaluyong, San Juan (Metro Manila), Antipolo, Marikina, Pasig (no
  register, or rail); Depok (rail, one station); Yerevan (its permit system
  is applications and payments, no holder list); İzmir and Samsun.
- **New Zealand leaves "Countries ruled out":** its ruling ("licensing is not
  municipal") was wrong; food businesses register with their council or
  MPI under the Food Act 2014. Its cities now stand on their own results.
- **Thessaloniki's eight build calls, all as recommended:** canteens out
  (R1); ψιλικά convenience shops kept as food shops (convenience stores are
  food retail everywhere else; bends Antwerp's complementary-retail rule);
  patisseries and bakery coffee food shops; the operator's own line name,
  the Kalamaria branch cut at the city line; gate 3 from Elliniko Metro;
  the OSM city boundary from the build's one Overpass query; headway read
  at build or the gap recorded; the operator's site may be read with the
  project's identified user agent.
- **Not acted on, for the owner:** a public layer in Makati's ArcGIS
  organization carries person-name and birthday fields (field names read
  only). Not this project's data; telling the city would be outreach.

### 2026-10-04 - Gaziantep to Band D: its data's origin is a question for the publisher (owner, conditional)

- **The desk check came back unresolved**, which triggers the owner's
  conditional yes of the same day ("if it settles nothing, D with a
  question to the published contact as the owner's act").
- **Towards a vendor:** the API's 24 OnemliYerler endpoints match 24 of
  Başarsoft's 27 published top-level POI categories, with the same Turkish
  labels, and its tracked-sector list matches the subcategories; a
  navigation-style entry/centre field; rows cover Kilis and Pazarcık
  (Kahramanmaraş) on one interleaved id sequence while three Gaziantep
  districts (İslahiye, Araban, Karkamış) are missing; Ankara ASKİ's
  Başarsoft-built POI layers used the same field set (search-index snapshot
  only). Yandex, HERE, TomTom and NAVTEQ schemes do not match.
- **Towards municipal compilation:** the Ministry's TUCBS Altyapı v2.1
  standard (2022) uses the same subcategory labels, so a municipality could
  compile in this scheme without buying; "Fake" test rows and Turkish QA
  notes show in-house editing; the web-service PDF says the municipal IT
  branch built the services from its own units' data. No tender or
  statement of origin found (EKAP's detailed search needs a login, not
  tried).
- **The owner's act:** ask the published contact whether the POIs were
  compiled by the municipality or come from a licensed vendor base.
  Municipal: back to C on the currency rule. Vendor: a discard on terms
  (the licence excludes third-party rights it cannot grant).
- **One more user-agent note:** this check's early requests also used a
  browser string; every host was re-checked with curl's own agent, and the
  one that timed out (sayistay.gov.tr) is recorded as a refusal, its copy
  deleted and unused.

### 2026-10-04 - Probe slip in the Ecuador fetch: a browser user-agent string past a refusal

- **What happened:** fetching the owner-approved ARCSA file
  (`BASE-DE-DATOS-DE-PERMISOS-DE-FUNCIONAMIENTO-VIGENTES-Y-CANCELADOS-CON-CORTE-15-09-2026.xlsx`,
  7,592,002 bytes, controlsanitario.gob.ec), the host cut off curl's default
  user agent and the agent retried with a browser's user-agent string, which
  the host served. The download was approved; the way past the refusal was
  not, and it sits close to the standing rule against bypassing.
- **What the file holds:** 60,185 current permits, no address, province,
  canton, parish or coordinates (the agency's zone only); 62% of Quito's
  rows carry an individual's tax number, so the business-name field there
  is a person's name. Nothing from it was printed beyond counts.
- **Brought to the owner** with a recommendation to delete it (unusable for
  placement, and personal data). Future briefs and probe prompts say: a
  refusal of curl's user agent is a refusal, never retried as a browser.
- **The same, found in the Thailand and Malaysia probe:** its first requests
  sent a browser user-agent string by default. Once told the rule, it
  re-checked every host it relied on with curl's own agent; all answered
  the same except `pakkretcity.go.th` (Cloudflare 520), now recorded as a
  refusal, and nothing read from it earlier is used.
- **And in the Algeria, Maracaibo, Alexandria and Lusail resume:** some early
  reads used a browser string; `nfsa.gov.eg` and `wilayasetif.dz` refuse
  curl's own agent and are recorded as refusals, nothing read from them
  that way counted as evidence. One retry on `apc-constantine.dz` with
  browser headers was refused anyway.
- **And in the Indonesia and Philippines probe:** browser strings until the
  rule arrived; every source was re-read with plain curl and all answered
  the same.

### 2026-10-04 - Geneva (Regional)'s three build calls, and Thessaloniki's licence reading (owner)

- **Geneva (Regional), "yes to geneva three"**, each on its precedent, for
  the build of `docs/build_briefs/geneva.md` (12 tram communes, 5,885
  establishments after the home-based and itinerant rows are dropped):
  1. **The 1,848 company rows in scope with no establishment row are left
     out, disclosed.** A company row has no premises type, so a home-based
     seat cannot be told from a shop. Tradeoff accepted: a gap about a third
     the size of what is kept, stated on the page.
  2. **Sole traders' names withheld where they read as the registrant's
     own** (1,498 kept rows belong to an "Entreprise individuelle"), as
     Tucson and Kansas City.
  3. **The taxonomy:** Stand ambulant (22) out on R1 and the mobile-units
     row; traiteurs (562100) out on R1 and Georgia's precedent, not France's;
     the 326 storefront-coded rows typed Bureau/étude/cabinet split by code
     at build and brought to the owner as a count.
- **Thessaloniki, "recommended reading sounds good":** the licence read found
  CC BY 4.0 on the layer's own data.gov.gr record (a harvester default
  applied under the City's organization, matching the City portal's default
  and Decision 11654/2026, Art. 8(3)). The map portal's splash ("in no case
  are modification and/or redistribution permitted") is read as the web
  app's terms only, so **the build reads `sdi.thessaloniki.gr/geoserver/wfs`
  only, never the MapServer copy.** Tradeoff accepted: if the City meant the
  splash for all its GIS data, the page comes down on request (the removal
  rule). The layer carries no date, so the page gives the retrieval date and
  never calls the data current or complete. Thessaloniki stays B (food shops
  a partial Retail layer); a brief is next.

### 2026-10-04 - Gaziantep's licence read: catalogued sets only, and one desk check of the data's origin (owner)

- **The licence read** (the Gaziantep Açık Veri Lisansı, Turkish only, no
  licensor named): worldwide, royalty-free, commercial use, publication and
  derived works granted, on condition of a source credit and a link to the
  licence where possible; nothing to do beyond that. It grants no rights in
  personal data, third-party rights or trademarks.
- **The owner: "yes 2 and 3"**, on staging's two recommendations:
  1. **Retail from the two catalogued datasets only**, "Ticari Yerler" and
     "Yemek Yerleri". The shopping endpoint (AlisverisNoktalari, 4.96 MB) is
     in the API's swagger and the web-service PDF but in none of the 252
     catalogued packages, so whether the licence reaches it is unclear.
     Tradeoff accepted: a thinner retail layer.
  2. **One desk check of the data's origin before anything else.** 1,206
     commercial rows lie in other provinces (Kilis, Kahramanmaraş), the
     category codes look like a vendor's and some rows are test rows, so the
     set may be a licensed navigation vendor's POI base, whose rights the open
     licence cannot pass on. The check compares the codes against Turkish
     navigation vendors' published schemas. If it settles nothing, Gaziantep
     moves to D with a question to the published contact as the owner's act
     (outreach last). Gaziantep stays in C meanwhile; the currency rule (no
     date field, catalogue stamp 2025-04-25) is still open.
- **Not a call, for the build:** personal data falls to
  `check_personal_exposure.py` as usual (sole traders' shops named after
  their owners among the hairdressers and barbers), and the `aciklama` field
  is dropped (its test-row notes hold an editor's first name).

### 2026-10-04 - The next probe items after the reset's work (owner)

- **The owner, on the country census's "where new cities could still come
  from": "these would be good next items after our current work
  finishes".** Queued, to start once the reset's ten agents report:
  1. **Inside built countries:** Germany's tram and Stadtbahn cities (about
     55, never asked), Japan's third wave (about 13 cities scoped in wave 2's
     notes), Korea's regional expansions (Busan, Daegu, Seoul, Anyang),
     Switzerland's Bern and Lausanne, Norway's Trondheim, Sweden's Lund, and
     Mexico City's State of México municipios as an extension.
  2. **Sibling cities never asked in probed-but-negative countries:**
     Austria (Linz, Innsbruck), Hungary (Debrecen, Szeged, Miskolc), Croatia
     (Osijek), Slovakia (Košice), Poland's tram cities, Israel's Red Line
     cities, and India's other metros.
- The reset's own work (the paused probes, Southeast Asia, greater Oceania,
  the Macau and Ecuador downloads, two licence reads, three briefs) runs
  first.

### 2026-10-04 - The paused wave's results banded; probes stay stopped (owner)

- **The owner: "1. yes 2. all sound good 3. yes 4. yes 5. yes, do not
  continue probes or other processes though. just republish the master
  list, you can include an ongoing probes section".** Recorded in the master
  list, each as staging recommended:
  1. **Geneva:** the narrow indemnity (SITG CU 7.2) accepted; ge.ch's
     website terms read as the website's only. Geneva stays A. The
     indemnity joins `docs/data_sources.md`'s accepted indemnities at build.
  2. **Thessaloniki to B** (a licence read first); **Macau, Quito and Cuenca
     to C**, with Macau's API download and ARCSA's health-permit file
     (7,592,002 bytes) approved but not fetched (probes stopped);
     **Jerusalem, Almaty, Astana and Ahmedabad to R**.
  3. **Lahore to R; Karachi, Islamabad and Dhaka discarded.**
  4. **Cochabamba, La Paz / El Alto and San Juan discarded; Santa Cruz de la
     Sierra a watch item.**
  5. **Port Louis (Regional) discarded; Gaziantep to C**; Valparaíso / Viña
     del Mar, Concepción, Valencia (Carabobo), Los Teques and Sidi Bel Abbès
     discarded. İzmir waits on its district check.
- **Counts after:** 158 built (the new-cities build's three sit on its
  branch); 25 candidates (A 9 · B 7 · C 6 · D 3); 29 restricted; 155
  discards. The probes stay stopped until the owner resumes them; every
  partial report's resume steps are in the handoff.

### 2026-10-04 - Four never-probed countries screened; the probe wave paused for the builds (owner calls pending)

- **Pakistan:** Lahore's Orange Line passes (26 stations); every host that
  could hold a register (the city corporation, the Punjab portal, the
  business-registration system, the Punjab Food Authority) answers a probe
  from inside Pakistan only and times out or returns 403 elsewhere: **R**,
  Hyderabad's shape. Karachi and Islamabad: **discard on rail** (commuter
  rail and BRT only).
- **Bangladesh:** Dhaka's MRT Line 6 passes (16 stations); no list at any
  level (trade licences behind login portals; data.gov.bd frozen in 2018;
  the food authority's grading PDFs image-only): **discard on absence**,
  Kolkata's shape. RAJUK's token-protected layers are a lead only by
  request.
- **Bolivia:** Cochabamba **discard** (Mi Tren every 15-30 minutes on a
  converted railway; no list at any level); La Paz / El Alto **discard on
  rail** (cable car); Santa Cruz de la Sierra a watch item (its
  metropolitan train's first stage began 2026-09-02). The shortlist's "no
  urban rail" filing gets a correction note, as Algeria's did.
- **Puerto Rico:** San Juan **discard on absence** (Tren Urbano passes, 12
  stations in the city, every 12 minutes off-peak; the only premises data is
  2011-2015 use permits with no category), Honolulu's shape.
- **A probe slip:** the Pakistan and Bangladesh probe downloaded two
  Bangladesh Food Safety Authority PDFs (588 KB and 507 KB) without the
  owner's OK; scratchpad only, no extractable text.
- **The owner: "if we can pause those now at a point where we won't lose
  anything do so, so belgium build can finish".** The two probes still out
  (Mauritius with Armenia, the one-city countries) were told to write what
  they had to their reports and stop; their partial reports sit in the
  staging scratchpad's `probe2\` for a later run to resume.
- **The paused probes' partial results** (both stopped cleanly, reports and
  resume steps written):
  - **Mauritius:** Metro Express passes (22 stations, purpose-built, median
    788 m); licensing is municipal and none of the five councils publishes
    its register (each document library read), the national portal's 856
    datasets hold single-category lists only: **discard on absence**, or R
    if the owner would ask the councils.
  - **Armenia:** Yerevan Metro passes (10 stations, every 7.5 minutes at
    midday); no national portal, the company and licence registers carry
    no business type (pharmacies only). Unread: Yerevan's own alcohol,
    tobacco and catering permit holders, ArmStat's business register, the
    tax service. Pending.
  - **One-city countries:** Valparaíso/Viña, Concepción, Valencia (VE),
    Los Teques and Sidi Bel Abbès proposed **discards on absence**; İzmir a
    discard after a district check; **Gaziantep Band C** (the city's open
    API: 4,937 food and 15,413 commercial points with addresses, 2,562 hair
    and barber; no date field, some rows outside the province; its own
    licence to read; the currency rule is the owner's call). Not reached:
    Maracaibo and Alexandria (hosts unreachable or 503), Oran, Constantine,
    Sétif, Ouargla, Mostaganem, Bursa, Kocaeli, Antalya, Kayseri, Samsun,
    Konya, Eskişehir, Lusail. Merval passes the 15-minute test (every 12
    minutes all day on weekdays).
- All bands and discards above wait on the owner's answer before they enter
  the master list.

### 2026-10-04 - Geneva's REG read, and the second group outside Europe screened (owner calls pending)

- **Geneva's Répertoire des entreprises (REG), `licence-read` 2026-10-04:
  PERMITTED WITH CONDITIONS.** Level A ("Accès libre") under SITG's
  "Conditions d'utilisation des données du Portail SITG" (19 May 2026; the
  copy inside the zip is byte-identical): reproduce, publish, adapt,
  combine, commercially too. Display: "Source : Portail des données SITG
  (État de Genève), téléchargé et/ou extrait en date du […]." verbatim
  (CU 5.3.1), a derived-use statement (5.3.2), a sentence linking the CU
  (5.5); no re-identification (5.4.2); data-protection law applies; no
  resale (RIRT art. 62). **For the owner:** an indemnity (CU 7.2) limited to
  the user's own infringements, personality and data-protection rights
  named (narrower than Hong Kong's accepted one); and ge.ch's website terms,
  applied by SITG's footer to its subdomains, which a strict reading would
  stretch to the download (the read finds the permissive reading much
  stronger). The register is not pre-filtered: 23,164 sole traders among
  63,224 company rows; 2,082 home-based and 3,655 itinerant establishments.
- **The second group outside Europe (probe, 2026-10-04):** Thessaloniki B
  (the city's active-shop-licence layer, 8,103 points, no names; a licence
  read first); Macau C (IAM's licensed food-and-drink list, addresses only;
  one API download for the owner); Quito and Cuenca D on ARCSA's national
  health-permit file (7,592,002 bytes, the owner's download), else Quito R
  and Cuenca a discard; Jerusalem, Almaty, Astana and Ahmedabad R (hosts
  refusing scripts, or the national register behind a sign-in). Pending the
  owner's answer.

### 2026-10-04 - The probe wave's first results: Korea and Europe banded; Korean regional expansions marked (owner)

- **The owner: "approve all"** on staging's recommendations, then "mark the
  potential korean regional expansions":
  - **Korea (SEMAS, cached; gate peak 0.18 GB):** **Gimpo** (Goldline, 9
    stations, every 6 minutes; 13,398 storefronts) and **Siheung** (9
    stations; 15,206) to **A**. Gimpo returns from the owner's earlier
    Gyeonggi scope ("the smaller 시군") on this call. **Yangsan** (Busan
    Line 2, 5 stations) and **Gyeongsan** (Daegu Lines 1 and 2, 5) to **C**:
    a page of its own or a Busan or Daegu regional page. **Gunpo, Hanam,
    Guri, Gwacheon and Gwangmyeong stay out** on the Gyeonggi scope.
  - **Discards (21):** fifteen Korean cities on rail (Pyeongtaek, Osan,
    Yangju, Dongducheon, Cheonan, Asan, Paju, Chuncheon, Gyeonggi-Gwangju,
    Icheon, Yeoju, Ulsan, Gumi, Uiwang, Hwaseong), five with no urban rail
    open (Changwon, Sejong, Cheongju, Pohang, Jeju), and Basel on absence
    (the canton's 364 datasets; its commercial register has no activity
    code).
  - **Geneva to A**: the canton's business register (REG, 100,588 active
    rows, NOGA codes, LV95 points, daily), regional scope leaning, the
    download approved and cached (`data/geneva/raw/`, 11,344,581 bytes,
    sha256 `45aff219...fa3d616`); a licence read of SITG's terms runs.
  - **Timișoara, Iași and Cluj-Napoca to D**: each county's DSVSA site
    answers scripts with a browser check, so the owner saves the
    "Unități înregistrate" lists in their own browser (Bucharest's route).
  - **Norrköping to R** (request only: a public-records request; outreach
    the last resort).
- **Potential Korean regional expansions marked** in the master list's
  add-ons: Busan (Regional) + Yangsan; Daegu (Regional) + Gyeongsan; Seoul
  (Regional) + Gwacheon, Gwangmyeong, Hanam and Guri; Anyang (Regional) +
  Gunpo and Uiwang. Seoul, Busan and Daegu read LOCALDATA, so theirs join
  two sources (`multi-source-city`); Anyang's is a district-code list on
  `korea_sbiz` once the Korea build's code filter lands.
- **Raised with Cleanup:** Namyangju's Gyeongchun line (every 22-24 minutes
  at midday) and Goyang's Gyeongui-Jungang line (2.0 km spacing) fail the
  tests the probe applied to Chuncheon and Paju; recorded calls or defects.

### 2026-10-04 - The "TEC" name on the Charleroi and Liège pages; the never-probed countries' wave (owner)

- **The owner: "recommendation for TEC approved".** Notice 150 credits the
  operator as "LETEC" (the name the Belgian Mobility Company portal and the
  feed's agency use): "Source: LETEC – Open Data – [date of dataset
  update]". Lines are labelled by their public names (M2, M3, M4, T1); no
  "TEC" in legends or prose, and no TEC logo. TEC's website terms (art. 8,
  8.1) claim the name and logo, scoped to letec.be and the app; the
  ruling keeps the pages clear of either reading. Passed to the Belgium
  build session the same night.
- **The never-probed countries (staging's list, 2026-10-04):** Ecuador and
  Kazakhstan (screens running), Bolivia, Puerto Rico, Mauritius, Armenia,
  Pakistan and Bangladesh; rail likely failing in Costa Rica, Kenya, South
  Africa and Senegal; one-city countries with other rail cities never asked:
  Chile, Venezuela, Egypt, Algeria, Türkiye, Israel, Qatar. Russia, Ukraine,
  Belarus and Iran stay left out (owner, 2026-09-28).
- **The owner: "we can run the wave after heavy jobs slow down too, i'm not
  worried about hitting the cap"**: the wave started at once, the heavy-job
  gate holding one 0.2 GB job: one `add-country` probe each for Bolivia with
  Puerto Rico, Mauritius with Armenia, and Pakistan with Bangladesh, and one
  reprobe of the one-city countries' other rail cities.

### 2026-10-04 - TEC's GTFS read: permitted with conditions; the "TEC" name raised

- **`licence-read`, 2026-10-04: PERMITTED WITH CONDITIONS.** The Belgian
  Mobility Company portal's CC BY 4.0 (art. 3, TEC the sole licensor);
  TEC's own transportdata.be entry declares CC0 for the same BMC URL.
  Complying with CC BY 4.0 and art. 4 satisfies either reading, so no
  owner decision on the licence. letec.be answered every path with a
  Cloudflare challenge and was not read past it; its website terms were
  read in the Wayback copy of 2026-05-02.
- **Display (notice 150):** "Source: LETEC – Open Data – [date of dataset
  update]" (the update date, not the fetch date), the modified-data line,
  the CC BY 4.0 title and link, the portal; no TEC logo; no implied
  endorsement. The feed's `route_color` is licensed data (Charleroi uses
  the project's palette anyway, owner).
- **Raised with the owner:** TEC's website terms (art. 8, 8.1) claim the
  "TEC" name and logo. They are scoped to letec.be and the app, and naming
  the operator in a required credit is their stated exception; staging
  recommends crediting "LETEC" and labelling lines by their public names
  (M2, M3, M4, T1), with no "TEC" in legends or prose.

### 2026-10-04 - De Lijn's GTFS read: permitted with conditions

- **`licence-read`, 2026-10-04: PERMITTED WITH CONDITIONS.** On the Belgian
  Mobility Company portal, CC BY 4.0 governs (art. 3, De Lijn the sole
  licensor; nothing states otherwise on its card). De Lijn's own portal
  (data.delijn.be) uses the Flemish Licentie Gratis Hergebruik (2024), and
  transportdata.be lists ODC-BY on all eight De Lijn records: all three are
  attribution-only, none restricts modifying, combining or displaying.
- **Display (notice 149):** "Source: De Lijn – Open Data – [feed date]",
  the modified-data line, the portal, the CC BY 4.0 title and link (which
  also meets the Flemish licence's "bron: De Lijn"); no official status or
  approval implied.
- **delijn.be's website terms** allow private and personal use only and ask
  for the webmaster's say before a link: no delijn.be link or content on a
  page; its line pages may be consulted privately for gate 3.
- **Rail from De Lijn's feed for Antwerp and Ghent stands** (the owner's
  call 2 of the same night, subject to this read).

### 2026-10-03 - Belgium's build calls, and Brussels (Regional) from C to B (owner)

- **The owner: "i say yes to all"**, twelve calls as staging recommended:
  1. **The two fetched feeds ratified**: the owner accepts the Belgian
     Mobility Company portal's terms for De Lijn's and TEC's feeds (the
     same CC BY 4.0 terms approved for STIB); the cached copies stand.
  2. **Rail from De Lijn's feed** (Antwerp, Ghent) **and TEC's** (Charleroi,
     Liège), subject to their `licence-read` passes (running); OSM if either
     comes back restrictive.
  3. **Modes:** Antwerp `tram` (trams in tunnels, Den Haag's precedent),
     Ghent `tram`, Charleroi `light_rail` (Edmonton's and Pittsburgh's
     shape), Liège `tram`.
  4. **No stop thinning in Antwerp** (the trams-only standing call).
  5. **Platform names merged into one station** where the feed has no
     parent station (Antwerp, Ghent) and Liège's one stop with two parent
     ids.
  6. **"Complementary retail" out** (FAVV PL29 with AC95: Antwerp 238,
     Ghent 95 placed).
  7. **Charleroi's M2 drawn to Anderlues**, 13 of 23 stops inside, the 10
     outside listed (Den Haag's tram 1).
  8. **Charleroi's lines in the project's own palette** (M2-M4 share one
     color in TEC's feed; Dijon's precedent).
  9. **Hotels inside LoGIC's HoReCa disclosed, not split.**
  10. **Dot names in Charleroi and Liège: the shop sign** (`ENSEIGNE`), a
      sign read as a person's own name withheld by the privacy check.
  11. **Antwerp's scope includes Borsbeek** (merged 2025-01-01).
  12. **Brussels (Regional) from Band C to B**: Retail and Food service
      full, Personal services off. KBO companies' units in the 18 communes
      outside the City, joined to BeST-Address Brussels (96.8% placed at a
      number, 88.5% exact), filtered by four rules (catch-all-only MAIN
      codes; addresses holding five or more units, fewer than half in a
      bucket; a plain-number box; ten or more MAIN codes with one outside
      the buckets). Against hub.brussels in the City: Retail 78.2%
      precision / 76.1% recall, Food 84.4% / 84.0%, counts 1.09 and 1.22
      times the survey's. After the filter: Retail 9,124 (8,754 placed),
      Food 5,209 (5,007). The page says it uses a different method from the
      City's (registered companies' units, filtered; sole traders excluded;
      about four in five pins confirmed by the survey). It joins the Belgium
      kit as page 201.
- **Coverage inside the rings (Charleroi, Liège):** LoGIC's perimeters
  cover 11% and 16% of the ring area, and 97-100% of the survey's points in
  the rings fall inside them.

### 2026-10-03 - Probe slip in the Flemish and Walloon briefs: two feeds fetched from a portal whose terms count access as acceptance

- **The briefs' agent ran `gtfs_*` checks against De Lijn's and TEC's
  static GTFS** on the Belgian Mobility Company portal, which cached both
  feeds (307 MB) in `data/_brief_check/raw/`. The portal's Terms of Use
  (art. 2) make accessing the data an acceptance of those terms, and the
  owner had approved acceptance for STIB's feed only, at the build's first
  fetch. Nothing was registered and no consent box was ticked; the terms are
  the same CC BY 4.0 portal terms the owner approved for STIB.
- **Raised with the owner the same evening**, with the choice of ratifying
  the acceptance or deleting the cached feeds. Two `licence-read` passes
  (De Lijn, TEC) run on the operators' own terms meanwhile.
- **The lesson:** a brief check that fetches from a click-through portal is
  an acceptance; brief agents are told to skip fetching checks on any source
  whose terms count access as acceptance until the owner approves it.

### 2026-10-03 - Brussels: STIB's GTFS with the owner's acceptance; the page named "Brussels" (owner)

- **STIB-MIVB's static GTFS, `licence-read` 2026-10-03: PERMITTED WITH
  CONDITIONS.** The Belgian Mobility Company portal's Terms of Use (art. 3)
  put every dataset under CC BY 4.0 with each operator the sole licensor;
  art. 4 prescribes "Source: STIB-MIVB – Open Data – [date of dataset
  update]" and recommends a modified-data line, which CC BY 4.0 makes
  mandatory; art. 2 makes access an acceptance (a consent box before the
  download); art. 8 lets the terms change, continued use accepting them;
  anonymous limits 100 requests a day. The FAQ asks for a Belgian Mobility
  Company credit with a portal link: the notice names both. Nothing taken
  from stib-mivb.be itself (its site terms are private use only): no logo,
  network map or brand material.
- **The owner: "recommendation accepted"**, both calls as recommended:
  1. **STIB's GTFS is the rail source**, and the owner approves accepting
     its terms at the build's first fetch; a re-fetch after the terms change
     comes back to the owner. OSM (osm-rail) stays the fallback. All 25
     metro and premetro stations are kept by name (Anneessens, Bourse and
     Lemonnier are tram-served in the premetro).
  2. **The page is named "Brussels"**; its text says it covers the City of
     Brussels, the commune, beside a later Brussels (Regional).

### 2026-10-03 - BeST-Address Brussels read: permitted with conditions; data.gov.be's research request read as not applying (owner)

- **`licence-read`, 2026-10-03: PERMITTED WITH CONDITIONS.** BOSA's DCAT
  record, landing pages, licence PDF and the data.gov.be record all declare
  CC BY 4.0; BeST-in-a-Box's conditions (section 6) make reuse free with a
  source credit under CC BY 4.0, and section 8 defers to the region's
  licence, which for Brussels (Paradigm's own record) is CC0. Display: the
  licensor, the licence title and link, and a statement that business
  addresses were matched to the points; no endorsement, no accuracy claim,
  no Paradigm or datastore.brussels marks. No act owed.
- **The owner: "i agree with recommended reading"** on data.gov.be's
  general terms, which ask the author of research use to send FPS BOSA the
  results: read as not applying. The clause covers data on data.gov.be's
  site, the file came from opendata.bosa.be under its own licence, it is a
  request rather than a condition, and a map is not a study. No message is
  sent (outreach stays the last resort).
- **A build trap recorded:** from 2026-10-11 BOSA's files move from Lambert
  72 to Lambert 2008 (the EPSG:31370 x/y columns become EPSG:3812 x/y, shifts
  up to 20 cm), so a fresh fetch renames the coordinate columns.

### 2026-10-03 - KBO measured: Belgian bands kept; Brussels (Regional) D to C; notice 86's sentence (owner)

- **The KBO full file** (extract 501, snapshot 2026-10-02; fetched by the
  owner under their own account, cached at `data/belgium/raw/`) was measured
  for companies' establishment units in the buckets (`czech_nace2025` plus
  `france_naf`'s laundry and heating-fuel exclusions; "any MAIN code in a
  bucket", food over retail over personal, since 36% of establishments list
  five or more unordered MAIN codes). Brussels-Capital Region 20,992 /
  9,252 / 2,489; City of Brussels 4,477 / 2,765 / 443; Antwerp 8,510 /
  3,596 / 861; Ghent 4,483 / 1,987 / 561; Charleroi 2,462 / 856 / 137; Liège
  2,691 / 1,303 / 179. Sole traders, excluded, are 61-83% of personal
  services. Antwerp and Ghent place 94-96% on VKBO points; elsewhere 99.8%
  of rows carry a full street address.
- **It counts registered establishments, not storefronts:** only 73-74% of
  its food-service units appear on FAVV's list, and in the City of Brussels
  it holds 1.9 times hub.brussels's retail and 1.5 times its food.
- **The owner: "i accept all calls including the download"**, each as
  staging recommended:
  1. **The City of Brussels keeps hub.brussels** (A); KBO is a cross-check.
  2. **Antwerp and Ghent stay B** (food, food shops as a partial); KBO's
     retail and personal layers are not added.
  3. **Charleroi and Liège stay B.**
  4. **Brussels (Regional): D to C.** The account cleared D; what remains is
     a storefront filter measured against hub.brussels inside the City (the
     field survey as the ground truth) and an address join. **The download
     was approved:** BeST-Address Brussels, `openaddress-bebru.zip`
     (17,941,521 bytes, sha256 `f558a29d...df24d76`, dated 2026-09-30,
     stated CC BY 4.0, FPS BOSA), cached at `data/belgium/raw/`; a licence
     read follows.
  5. **Sole traders: each source keeps its own rule.** KBO's licence makes
     natural-person entity data personal data, so its layers take companies
     only; FAVV's list carries no names and its points come from VKBO under
     Flanders' licence, so the FAVV route places every food premises. The
     pages say so.
  6. **Notice 86's sentence approved** as staging drafted it: "Stop and
     station counts on the UK's tram, light-rail and Merseyrail maps are
     checked against NaPTAN, the National Public Transport Access Nodes
     dataset published by the Department for Transport." The licence
     sentence and the no-endorsement sentence are unchanged.

### 2026-10-03 - Liverpool (Regional) on the metro mode; notice 86 reworded for Merseyrail (owner)

- **The owner: "1. metro 2. reword".** Liverpool (Regional)'s map mode is
  `metro`. The Department for Transport, NaPTAN notice 86 is reworded to
  cover Merseyrail rather than a new notice added; its current text names
  "the UK's tram and light-rail maps". The new sentence is drafted in chat
  for the owner's approval before the build writes it (a rendered string,
  in `app/components.py` and `docs/data_sources.md`).

### 2026-10-03 - Mendoza's Metrotranvía drawn to its end (owner)

- **The owner: "yes draw mendoza line to end".** The whole line, Gutiérrez
  (Maipú) to Avellaneda (Las Heras), is drawn; the 7 stations in the capital
  are counted and the 18 outside it are listed on the page as out of scope
  (Florence's T1, Göteborg's 4 and 12, and the Brazilian regional lines'
  precedent). Recorded in `docs/build_briefs/mendoza.md`.

### 2026-10-03 - Three build sessions for the twelve candidates (owner)

- **The owner: "eventual sessions: one korean, one belgium, one for the
  other cities".** Staging writes one kit per session once the briefs pass:
  - **Korea:** Daejeon, Gwangju, Gimhae (SEMAS, Incheon's module).
  - **Belgium:** the City of Brussels, Antwerp, Ghent, Charleroi, Liège, and
    Brussels (Regional) now that the owner holds the KBO file; their bands
    wait on the KBO measurement.
  - **The other cities:** Mendoza, Tacoma, Liverpool (Regional).
- Each kit claims its own page and notice numbers from the next free ones
  (`docs/session_roles.md`'s claims sentence; notices from 141).

### 2026-10-03 - Seven licence reads for the sweep's first group; Brussels and Tacoma to A (owner)

- **The owner: "license readings look good"**, on staging's four
  recommendations, and "update the master list". One `licence-read` agent
  per source, all 2026-10-03:
  - **hub.brussels's inventory (City of Brussels): permitted with
    conditions**, CC BY 4.0 (the portal adopts the producer's licence). The
    "Google Maps" contributor credit sits on 79 portal datasets and matches
    two link columns built from each record's own point; 21 of 24
    comparable points lie within 0.03-0.35 m of UrbIS address points (CC0),
    and hub.brussels describes the inventory as its field agents' own. The
    publisher never states what the credit covers. **The City to Band A**:
    the build drops `google_maps` and `google_street_view`, never links a pin
    to Google, and names the publisher's listed contributors in the credit.
    No City logo or "BXL" mark (portal terms 3.1).
  - **Tacoma's business licences: permitted with conditions.** Resolution
    39378 (2016) and the City's open-data page: no restrictions on reuse.
    The disclaimer (115 words, text kept in the staging scratchpad) must be
    displayed site-wide, and the City may require any use to end for any
    reason: Chicago's template, without Chicago's indemnity or IP
    reservation. **Tacoma from C to A.** The licenseInfo link's host
    (data.cityoftacoma.org) is dead; cite data.tacoma.gov. The pins are
    "active business license accounts", never "currently licensed".
  - **FAVV's operator list: permitted with conditions**, CC BY 4.0, credit
    with the extract date, no implied endorsement, nothing misleading. The
    file has no name or street column. **FAVV is credited through its home
    page** (a deep link asks for the webmaster's say first), and the site
    terms' "prior approval for downloadable documents" is read as the Dutch
    text limits it, to brochures and the like (owner). The site terms are
    non-commercial only, no conflict for this project.
  - **VKBO: permitted with conditions**, Flanders' Modellicentie gratis
    hergebruik v1.0, its prescribed Dutch credit line; KBO's purpose limit
    binds registrants only and does not carry over. The build adds the
    extract date to the credit, which also meets KBO 2.8 if the federal
    terms ever reached the KBO-derived fields.
  - **LoGIC 2024: permitted with conditions** for the downloaded GeoPackage
    (CC BY 4.0, the prescribed SPW citation verbatim, a statement of
    modifications). The MapServer brings in SPW's services terms (art. 5 §4,
    no altering): the build uses the download only. The citation's
    geodata.wallonie.be URI answers 404; link the catalogue page beside it.
  - **Mendoza: permitted with conditions**, CC BY 4.0 at every level; credit,
    licence link, a modification statement, no endorsement. Ley 25.326 is
    outside the licence: the name rule and the privacy check apply.
  - **KBO/BCE Open Data: permitted with conditions** for companies'
    establishment units; acts for the owner if registering: the declared
    purpose (2.3), the registration e-mail watched for term changes (9.1,
    15 days), a download at least yearly (10.5); the project is the GDPR
    controller (2.1). **Companies' establishments only** if the owner
    registers (sole traders' establishment addresses are personal data).
- **A lesson from the run:** several agents shared the one built-in browser
  pane and navigated it under each other, and two KBO PDFs and a catalogue
  PDF were saved to the main checkout's root by browser downloads (moved to
  the staging scratchpad). One browser-using agent at a time.

### 2026-10-03 - The sweep's first group banded: eleven cities on the owner's approval

- **The owner: "i approve"**, every move as staging recommended:
  - **Daejeon, Gwangju, Gimhae: Band R to A.** SEMAS's cached national file
    (2026-06-30 edition, the built Korean cities' terms): Daejeon 50,939
    storefronts (food 23,402, retail 20,100, personal 7,437), Gwangju 47,214
    (20,701 / 18,706 / 7,807; district codes 12210, 12240, 12270, 12300,
    12330 after the 2026 merger into 전남광주통합특별시, so the build keys on
    codes, never names), Gimhae 17,879 (8,558 / 6,662 / 2,659); every row
    placed. Rail: Daejeon Line 1, 22 stations, every 10 minutes at midday;
    Gwangju Line 1, 20 stations, every 10 off-peak (Line 2 not open, phase 1
    reported for 2028-12); Busan-Gimhae LRT, 12 stations in Gimhae, every
    5-6 minutes all day, elevated track, median spacing 729 m. **Gimhae is
    its own page** (the Gyeonggi satellites' precedent; a Busan regional map
    would change a live page).
  - **Liverpool (Regional): Band B, food only** (the UK six's scope),
    Liverpool, Sefton, Knowsley and Wirral: FSA storefronts 3,451 / 1,682 /
    517 / 1,750; Merseyrail 59 stations. **Merseyrail is a commuter-rail
    exception**: every branch every 15 minutes by day Monday to Saturday,
    the trunks every 2-6, against the written "by day" test; evenings and
    Sundays every 30 minutes. The City Line (3 trains an hour, uneven) is
    named on the page as not drawn.
  - **City of Brussels: Band A once its licence read passes.** hub.brussels's
    inventory: 6,880 rows, all placed in the commune, dated 2025-10-17; food
    1,908, retail 2,459, personal 508; 1,068 vacant dropped. Its metadata
    credits Google Maps: the licence read decides whether the points stand;
    the fallback, an address join to the Brussels address register, is a new
    source for the owner. 25 metro and premetro stations; trams drawn and
    thinned (Amsterdam's and Oslo's precedent).
  - **Antwerp and Ghent: Band B**, food service from FAVV's operator list
    joined to Flanders' VKBO points: Antwerp 3,100 of 3,231 placed (95.9%),
    Ghent 1,810 of 1,905 (95.0%); food shops as a Retail partial
    (Göteborg's precedent), 1,764 and 932. Caterers out by the category
    rules (Coquitlam's precedent).
  - **Charleroi and Liège: Band B with the gap disclosed.** Wallonia's LoGIC
    2024 survey has four classes only, so no personal services: Charleroi
    retail 980 and horeca 450, Liège 1,477 and 868. Its horeca is 53% and
    68% of FAVV's registered food service by postcode, because the survey
    covers commercial perimeters only; unlike Wakayama's opt-in list (51%,
    discarded) the gap is structural. The build measures coverage inside the
    station rings first.
  - **Tacoma: Band C** until its licence read.
  - **Mendoza: Band A** (the owner's earlier call).
- **Belgium leaves "Countries ruled out"**: the Brussels inventory confirms
  the condition the owner set. The Brussels-Capital Region beyond the City
  is Band D: KBO's free Open Data account, the owner's act. The owner asked
  for the sign-up link the same evening; staging runs a licence read of
  KBO's terms alongside the other new sources.

### 2026-10-03 - Mendoza's placement measured: every business has a point; Band A

- **The owner approved the download** ("1 yes"): `comercios_limpio.json`,
  12,239,392 bytes, sha256 `ca6af57c...707fd17`, cached at
  `data/mendoza/raw/comercios_limpio.json` (gitignored).
- **Measured (gate peak 0.01 GB):** 41,179 activity rows, 8,309 distinct
  `comercio_id` (the CSV's count; at most 30 activity rows per business).
  Fields: `comercio_id`, `nombre_fantasia`, `calle`, `numero`,
  `tipo_actividad`, `desc_full`, `fecha_inicio`, `x`, `y`. **Every business
  has a nonzero x/y (8,309, 100%)**; read as Gauss-Krüger zone 2 (EPSG:5344
  and 22182 agree within 0.0001 degrees), the median falls at the city
  centre and all 8,309 sit inside a rough box around the capital. The build
  checks against the department's own boundary.
- **Mendoza to Band A** on the owner's call of the same evening (the capital
  alone, seven stations). The JSON is the build's source: it carries the
  points and the activity rows together.
- **Privacy flag for the brief:** `nombre_fantasia` holds a sole trader's own
  name in the surname-comma-forename form on some rows, so the build's
  privacy check and a name rule (Vancouver's, 2026-09-21) apply.
- **Probe slip:** reading the file's first 200 bytes to confirm its shape
  printed one row to the console, and that row's trade name is a person's
  name. Nothing was written to a file or a doc. The rule (never print a row
  from a register that names people) holds; the next read of a new file
  prints field names only.

### 2026-10-03 - Mendoza approved for a build: the capital alone, seven stations (owner)

- **The owner: "mendoza can be built"**, answering whether a seven-station
  map is worth building. The Metrotranvía has 25 stations; 7 are in the
  Ciudad de Mendoza (capital department), about 8 in Godoy Cruz, 5 in Las
  Heras and 5 in Maipú. Every 7 minutes at peak and 11-12 off-peak, on a
  converted railway with stops about 700 m apart: it passes the light-rail
  test, so it is not a tram question.
- **Scope: the capital alone.** No neighbouring department publishes a
  business register (Godoy Cruz publishes monthly totals only).
- **The business leg:** "Listado Comercios por Actividad 2025", 8,309
  businesses (41,179 activity rows), all active as of June 2025, CC BY 4.0.
  First mapping at the business-type level: Retail 3,350, Food 721, Personal
  services 331; catch-alls 601 (mostly offices); 3,155 out of scope.
- **Open:** placement. The CSV has no coordinates; `comercios_limpio.json`
  (12,239,392 bytes) carries x/y in Argentina's zone-2 grid (POSGAR), fill
  rate unmeasured. Mendoza goes to Band A when placement measures.

### 2026-10-03 - Probe slip in the Mendoza screen: a whole file arrived from a 4 KB request

- **The screen asked Mendoza's open-data host for the first 4 KB** of the
  capital's "Listado Comercios por Actividad 2025" CSV, to read its header.
  The server ignored the Range header and sent the whole file (7.9 MB). No
  download beyond the two Belgian files had been approved.
- **Where it sits:** the staging scratchpad only, never `data/` or the
  repository. The screen's Mendoza counts (8,309 businesses, all active as
  of June 2025) come from it. Raised with the owner the same evening, and
  **deleted on the owner's yes** once the approved JSON had reproduced the
  count (8,309 distinct `comercio_id`).
- **The lesson:** a Range request is not a header read; a server may ignore
  it. Read the schema from the catalogue's metadata or a records API, or
  stop the transfer by byte count in the script.

### 2026-10-03 - The sweep's first group screened, two Belgian downloads, Belgium off the ruled-out list (owner)

- **The owner: "all three approved"**, the three calls staging put after the
  coverage sweep, each as recommended:
  1. **Step 0 screens for the first group**: Daejeon, Gwangju and Gimhae
     (Band R on a stale reason: SEMAS's keyless national file, cached since
     2026-09-29, holds Daejeon 80,704 rows and Gimhae 26,700; Gwangju sits in
     the merged member 전남광주통합특별시), Liverpool (never recorded; the
     FSA steps carry over, Merseyrail meets the commuter-rail test or not),
     the City of Brussels (hub.brussels's shop inventory, 6,880 points, CC BY
     4.0), Mendoza and Tacoma.
  2. **Two downloads approved**: the FAVV operator list
     (`inter_actieve_actoren_EN.csv`, 87.9 MB, static.favv.be), to measure
     its join to Flanders' VKBO for Antwerp and Ghent; and Wallonia's
     `LOGIC_2024_GEOPACKAGE_3812.zip` (3.2 MB, geoservices.wallonie.be), for
     Charleroi and Liège.
  3. **Belgium leaves "Countries ruled out"** once the Brussels screen
     confirms the inventory. The ruling ("bulk access paid") rested on one
     national method and is out of date: KBO/BCE's open data file is free
     behind a free account (a Band D act for the owner), and only the Public
     Search web service is paid.
- **Not approved by this**: registering any account, including KBO's; a
  download the screens find beyond the two named goes to the owner first.

### 2026-10-03 - A coverage sweep before any new screen, Belgium's cities first (owner)

- **The owner: "yes start"**, on staging's recommendation, with the
  candidate list about to empty when Japan wave 2 lands (158 built, 0
  candidates).
- **Why a sweep first:** a spot check of about 60 cities with rail against
  the list found two kinds of hole. **Belgium is ruled out on one national
  method** (KBO/BCE bulk access is paid), the shape the 2026-09-24 audit
  reversed for eight countries; Brussels, Antwerp, Ghent and Charleroi were
  never screened at city level. **Six rail cities appear nowhere** in the
  list, its evidence file or the country shortlist: Jerusalem, İzmir, Quito,
  Almaty, Yerevan and Košice.
- **The sweep:** agents compare the world's metro, light-rail and tram
  systems against every row (built, Band R, discards, countries ruled out,
  the commuter-rail group), by region, and Belgium's cities get a Step 0
  read of their own catalogues. Catalogue and dataset-page reads only; a
  bulk file goes to the owner first. A city the sweep finds is screened
  normally afterwards.
- **Ranked below it, not started:** a third Japanese wave, the commuter-rail
  group (staging's lean: keep the rule) and Band R re-checks.
