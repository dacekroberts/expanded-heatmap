# DECISIONS drafts - Regional-1 (`worktree-japan-regional-1`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

The batch (the A/B build plan, 2026-10-07): Maebashi, Fukuyama, Ichinomiya,
Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu, Mito, Morioka; pages 229-239,
notices 176-186.

## Parked calls

1. **Tsu (page 232, notice 179 held): Mie Prefecture's three BODIK lists
   (`240001_food_business_all`, `240001_barbar`, `240001_hair_dressing`) have
   no licence verdict.** The brief records CC BY 4.0 as stated and leaves the
   read to a `licence-read` agent; no read is recorded in staging's drafts,
   `docs/data_sources/japan.md` or `DECISIONS.md` (the wave-5 entry's eleven
   reads do not include Mie). *Recommend:* one licence read of the
   三重県オープンデータ利用規約 (`https://odcs.bodik.jp/240001/tos/`), one read
   for all three lists, by a session cleared to call BODIK's hosts; then
   build. What the brief quotes points to permitted with conditions (CC BY
   4.0, a resource's own licence prevailing, no logo, a fault-based cost
   clause, accepted for Japan 2026-09-24). *Tradeoff:* one read and a later
   build, against a page and notice whose credit and conditions are
   unverified. The scaffold stands as committed (efeaf016); nothing else was
   written. The brief's open call 1 (MHLW's notifications as a partial Food
   shops layer) needs no call: Iwaki's call 150 left 164 addressed retail
   rows out as too thin, and Tsu's are 159 (156 pins), so they stay out and
   MHLW's file stays the control.
   **Resolved 2026-10-07, the same day:** Staging's licence read found Mie's
   lists PERMITTED WITH CONDITIONS (CC BY 4.0 by 第１条; master's staging
   drafts, "Licence reads for the Japan builds"). Tsu is built after it.
2. **Fukushima (page 233, notice 180; built, not blocked): the registers'
   2026 monthly files** (`r0808riyou.csv`, `r0804biyou.csv` to
   `r0807biyou.csv`, 360-709 B each; the same page, publisher and terms;
   none for laundries; the brief's open call 3, staging's call 153). They
   are not approved and were not fetched, so the registers stand at
   2026-03-31 (`SOURCE_AS_OF`) while the food leg reaches 2026-08-31.
   *Recommend* approving them (Ichinomiya's call 128), then rebuilding the
   barber and beauty lists to 2026-08-31 in `config.source_rows`.
   *Tradeoff:* a handful of salons, a re-render and one more approval,
   against registers five months older than the food leg (stated on the
   page and in data_age).
3. **Ōita (page 236, notice 183; built, not blocked): the registers' 2026
   monthly files** (`442011_beauty_salon_new`, five CSVs of 240-713 B, and
   `442011_cleaning_new`; no barber set; the brief's open call 3). Not
   approved and not fetched, so the registers stand at 2026-03-31 while the
   food list is of 2026-09-01. *Recommend* approving them (Ichinomiya's call
   128), then reading each register plus its months as Ichinomiya's
   `source_rows`. *Tradeoff:* a few dozen salons (openings only; the city
   publishes no closures, so an upper bound) and one more approval, against
   registers five months older than the food leg (stated on the page and in
   data_age).
4. **Ōita: the city's own notification list** (`442011_licensed_facility`,
   すべての営業届出施設一覧 as of 2026-09-01, CSV 287,712 B, same publisher and
   licence; the brief's open call 2(a)). Not approved and not fetched; MHLW's
   opt-in notifications stand in by precedent. *Recommend* approving it at
   review time: the city's complete list would make the Food shops layer
   complete rather than partial. *Tradeoff:* one approval, a schema read and
   a re-render, against a Food shops layer the page calls partial.
5. **Gifu (page 237, notice 184; built, held for one call): the rings.** The
   median nearest-station gap is 545 m, inside the spacing rule's 540-570 m
   owner band (tram-city skill section 3; Ōtsu's and Uijeongbu's builds
   applied it). The brief's 641 m is the 7th of 12 gaps, not the median.
   In-ring share 30.7% on the standard rings (1,844 of 6,005), 15.3% on
   halved ones (916). *Recommend* the standard rings: the median rests on
   three close pairs (岐阜 / 名鉄岐阜 418 m, 加納 / 茶所 428 m, 長森 / 手力
   449 m); the other six stations are 641 m to 4.6 km from their nearest;
   every JR or private-rail Japanese city is on standard rings. *Tradeoff:*
   the rule's letter (about 550 m or less) and Rennes's 541 m (halved) point
   the other way, at half the ring share. The build stands on the standard
   rings; halved is two lines in `pipeline/gifu/config.py` and a step 3
   re-run.

## Proposals for review time (page sentences no template covers)

- **Maebashi** (page 229): "Barbers, beauty salons and laundries come from
  the city's registers, brought up to August 31, 2026 from its March list and
  its monthly lists of openings and closings." and "The laundry register
  lists 139 laundries, against 170 in the national count a year earlier. The
  city notes that some premises are left off at their operators' request."
  (the owner's call 14: build and state the share, citing the dataset's
  note as a stated cause, never the whole of the gap). The same two
  sentences in its What Is Excluded section, and "No Shinkansen station lies
  in the city." there. The notice (176) adds Hamamatsu's form for two lists
  and the sentence "No list is claimed to be complete or current; the
  ministry's holds only filings whose applicants agreed to publish them."
  (第３条).
- **Fukushima** (page 233): "From Fukushima City's list of food-business
  permits (as of March 31, 2026), with the new permits it listed each month
  to August 31, 2026, and its registers of barbers, beauty salons, laundries
  and coin laundries (as of March 31, 2026)." (the template's sentence with
  the months and Sapporo's coin laundries added), and "The JR Ou Line is
  infrequent inside the city: about 11 trains a day each way stop at
  Sasakino and Niwasaka." (call 86 asks for the stretch to be named; no
  approved form yet). In its What Is Excluded section: the Counted
  paragraph's month and upper-bound sentences (from Higashiōsaka's) and "The
  JR Ou Line runs about 11 trains a day each way inside the city; it is
  drawn (owner, 2026-10-06)." The notice (180) adds 新規食品営業許可施設一覧,
  the monthly files' own title, to the brief's five titles, and the
  processing sentence "this project added the new permits to the list".
  Also for review time (open call 4, precedent applied): of the 230 caterers
  left out, 161 also name a counter form (一般食堂 仕出し屋 …); a sentence
  saying so is not on the page.
- **Fukuyama** (page 230): "From Fukuyama City's list of food-business
  permits, brought up to August 31, 2026 from its March list and its monthly
  lists of new and renewed permits, and its registers of barbers, beauty
  salons and laundries (as of August 31, 2026)." (the template's first
  business bullet with Maebashi's proposed rebuild wording) and "Permits
  granted since June 2021 that the ministry's list no longer holds are left
  out as closed, and a few permits the ministry's list holds and the city's
  monthly lists do not are added." (calls 5c and 6). In its What Is Excluded
  section, the rebuild and the waiting-renewal wording under **Counted**, the
  145 permits left out as closed, and "The registers list 396 barbers, 1,238
  beauty salons and 173 laundries, against 405, 1,209 and 200 in the national
  count a year earlier." The notice (177) adds "rebuilt the city's food list
  to 31 August 2026 from its March list and its monthly new and renewed
  permits, left out permits granted since June 2021 that the ministry's list
  no longer holds" to Maebashi's processed-by sentence.
- **Ichinomiya** (page 231): "From Ichinomiya City's list of food-business
  permits and its registers of barbers, beauty salons and laundries, all as
  of March 31, 2026, with the new permits and registrations it has listed
  each month since, to August 31, 2026." and the coverage sentence the
  owner's call 125 asks for (Toyota's precedent with the reason named): "The
  city's food list leaves out vending-machine, vehicle, stall and temporary
  permits, entries containing personal information and operators who asked
  not to be listed, so it holds about two restaurants in three of the
  official count." The same facts in its What Is Excluded section, with
  "Another 124 sit at the center of their 小字 (a named part of a town)" (the
  foundation's 小字-centroid tier, new on a page). The notice (178) adds "The
  city's food list leaves some permits out by design, and the ministry's
  list holds only filings whose applicants agreed to publish them; neither is
  complete." (Sasebo's sentence with the city's half; the terms' 4(1)). The
  credit's titles were read from the city's catalogue, since staging's
  record names none: check them against the licence-read report.
- **Tsu** (page 232): "From Mie Prefecture's list of food-business permits
  and its registers of barbers and beauty salons (all as of August 31, 2026),
  which cover the prefecture outside Yokkaichi; the premises addressed in Tsu
  are shown." (the template's source sentence for a prefecture's lists), and
  "The JR Meisho Line is infrequent: about 8 trains a day each way stop at its
  12 stations in the city." (call 86, in Fukushima's form; the figure is from
  Japanese Wikipedia's account of the timetable, since JR Central's pages load
  by script: the one soft fact on the page). Two template sentences take the
  prefecture for the city: Kitakyushu's laundry sentence and the notification
  sentence. In its What Is Excluded section: the Hisai (久居) clause of
  Counted, and the Meisho Line's sentence. The notice (179) follows staging's
  credit form and adds "No list is claimed to be complete or current".
- **Akita** (page 235): "The JR Uetsu Line is infrequent at Katsurane: 3
  trains a weekday stop there toward Akita and 4 toward Sakata." (call 86;
  Fukushima's proposed form). In its What Is Excluded section: "The list's
  form of business does not mark snack bars, so they stay in Food service."
  (adapted from Higashiōsaka's approved sentence) and the Uetsu Line's
  Stations bullet. The notice (182) credits the three edition titles in the
  出典 form, since staging's read found no prescribed wording. Line names
  drop "Main" ("JR Ou Line", as Fukushima's), against the brief's table.
- **Ōita** (page 236): "About one restaurant in 20 in Ōita City's list has
  its address withheld by the city, which does not say why, and is not on
  this map. Where they are is not known." (Fukuoka's approved MHLW sentence
  with the city in the ministry's place and the reason stated as absent; the
  foundation's `asterisk` rule). In its What Is Excluded section: the
  withheld-entries bullet, "1 whose trade name the city masked" under **Names
  not shown**, and "No Shinkansen line reaches the city." The notice (183)
  adds "left out the entries whose address the city withholds" to
  Ichinomiya's processing sentence; the 記載例's 利用日 is the download date.
  **Line names:** Ōita uses "JR Hohi Main Line" (JR Kyushu's 豊肥本線, as
  Kurume's and Kagoshima's "Main Line" names), but Kumamoto's built config
  names the same line "JR Hohi Line": one consistency fix for review time.
  Akita and Fukushima drop "Main" for JR East's lines; the two conventions
  follow each operator's signs, which is worth the owner's look.
- **Gifu** (page 237): the coverage sentence the owner's call 125 asks for,
  in Ichinomiya's form with Gifu's reasons only: "The city's food lists leave
  out vending-machine, vehicle, stall and temporary businesses, so they hold
  about two restaurants in three of the official count." In its What Is
  Excluded section: the form-of-business sentence under **Counted** and the
  Takehana Line's stub sentence. The notice (184) adds the processing
  sentence and "The city's food lists leave out vending-machine, vehicle,
  stall and temporary businesses by design; no list is claimed to be
  complete or current". The credit is the portal terms' own form (3) for a
  modified work, read 2026-10-07 from the prefecture's terms page since
  staging's record names the form but not its wording: check it against the
  licence-read report.

## Shared-code findings for review time (not changed here)

- **`japan_register.rebuilt_register` ranks on the latest expiry alone**
  (Fukuyama): a renewal that starts after the as-of then hides the permit in
  force, and step 2's call-172 rule drops the premises (17 in Fukuyama, fixed
  city-locally in `config.rebuilt_food` by ranking only permits started by
  the as-of). Any city with renewal months is exposed; Higashiōsaka, built
  on it, is worth re-measuring. It also keeps only the first non-empty
  `FORM_COLS` value, so under `form_all` a 形態 beside a filled 業態 is lost
  (harmless in Fukuyama).
- **`japan_step2.own_coordinates_check`** prints and emits a chōme-tier
  median of 741,990 m on Fukuyama: 10 rows whose MHLW point lies in
  Fukushima or Tokyo, refused by `CITY_BBOX` and never used. Cosmetic, but
  the figure is in the baseline.
- **A full list kept whole plus new-permit months** cannot be one
  `rebuilt_register` source under calls 161 and 172 (one `TERM_AS_OF` per
  source): two sources of one `SOURCE_KIND` is the shape (Fukushima,
  Ichinomiya, Iwaki). A line for the japan-city skill.
- **`city_rows` trusts the file extension**: Ichinomiya's July beauty file is
  an XLSX named .csv, read city-locally by its magic bytes. Checking the
  bytes first in shared code would cover the next city.
- **`map_common.render_heatmap` anchors a line's label on its first
  segment** (Akita): the Oga Line's first N02 segment lies wholly outside the
  city, so its label lands at 出戸浜 in 潟上市, about 2 km past the city line.
  It places cleanly at desktop width; run `check_map_labels.js` at 375 and
  343 at review time. The fix is `LINE_LABEL_ENDS` or anchoring on all
  segments in shared code.
- **A yatai form moves a Retail notification to Food service** (Akita): one
  MHLW ⑬その他の食料・飲料販売業 row with 業態 屋台 becomes Food service through
  the shared yatai `FORM_RULES`, although a form is meant never to bring a
  row in. One pin; a taxonomy question, not Akita's.
- **`japan_register.wareki_date` reads no YYYYMMDD date** (Gifu): the permit
  list's 許可開始日 / 許可満了日 (20250620) read as None, so calls 161 and 172
  compared nothing and the foundation's TERM_AS_OF check (which fires only
  where a start or end reads) stayed silent. Fixed city-locally in
  `config.source_rows` (rewritten to YYYY-MM-DD); one late permit now waits.
  Any later city with 8-digit dates is exposed.
- **The label anchor's first segment, a second time** (Gifu): both JR lines'
  longest N02 segments lie wholly outside the city, so their labels landed
  about 12 km out and pulled the opening view south-east. Gifu's step 3
  orders each line's segments in-city-first (`in_city_first`) before
  `render_heatmap` (not a fork of it); all five labels now sit inside.
  Anchoring on all segments in shared code would cover Akita and the next
  city.
- **`rebuilt_register` folds live permits of a different 種目** (Iwaki): it
  keeps the latest-expiring permit per (address, trade name, type), which at
  11 Iwaki premises hid a live permit with another form (5 Food service
  pins). Where a list is a snapshot of permits in term, read it whole; keep
  the rebuild for lists that carry superseded permits. A line for the
  japan-city skill beside the two-sources note.

## Entries

### 2026-10-07 - Gifu built, the city's food permits and notifications of June 2025 and its barber and beauty registers of March 2025, from its CKAN packages

- **Gifu built (page 237, notice 184), Akita's shape (one standing food list
  of every permit in term on its date, nothing rebuilt) with Toyota's
  precedent for a list that leaves rows out by design, Yokkaichi's for the
  city's own notification list and Hamamatsu's for the registers: 6,005
  storefronts (Food service 3,272, Food shops 1,234, Personal services 1,499)
  around 12 stations on 5 lines, 30.7% of them in a ring (1,844) on the
  standard rings, which wait on the owner (parked call 5).** Sources: Gifu
  City's packages on Gifu Prefecture's CKAN, CC BY 2.0 (read 2026-10-06 by
  staging): c212016-072, the permit list (4,453 rows) and the notification
  list (1,093) as of 2025-06-01; c212016-075, the barber (362) and beauty
  (1,177) registers as of 2025-03-31. The city page's newer food list is not
  used (owner, 2026-10-06). Built by a subagent of the Regional-1 lead,
  integrated by the lead.
- **The brief's open calls, by precedent:** MHLW's 265 unmatched
  notifications stay out and its file is a control read by no step
  (Yokkaichi's and Toyama's precedent: the city's own complete notification
  list supplies the Food shops layer); no laundry list, so Personal services
  is barbers and beauty salons only, disclosed (Akita's and Tsu's).
- **The term dates:** the permit list writes 許可開始日 and 許可満了日 as
  YYYYMMDD, which the shared reader reads as no date; rewritten city-locally
  in `config.source_rows` (a shared-code finding). Past term 0; 1 菓子製造業
  permit starting 2025-06-20 waits (call 172), the brief's one.
- **Step 2:** storefront rows 6,590: Food service 3,382 (the brief exactly),
  Retail 1,673 (887 permits less the late starter, 787 notifications),
  Personal services 1,535 (4 beauty rows addressed 一円 are not a premises).
  Out by rule 490: 286 manufacturing and other non-counter types, 201
  institutional catering notifications, 3 mail order, the brief's figures
  exactly. The join: block 6,273, town-chōme 287, 小字 4, unplaced 26 (0.4%),
  against the brief's about 39: the foundation's `bracket_aza` places the 7
  鷺山(向井町) rows. 559 repeat rows shown once. On the map: 95.9% block, 4.0%
  town-chōme, 0.1% 小字. No 業態 column, so konbini, supermarkets, canteens,
  hotel restaurants and snack bars on a restaurant permit stay in Food
  service (R3).
- The 菓子 / そうざい factory share: 28 of 556 (5.0%), kept (owner,
  2026-09-24).
- **Food share stated on the page** (call 125, Ichinomiya's precedent): the
  permit list's 3,382 restaurants and cafes are 66.7% of e-Stat's 5,070 in
  force on 2025-03-31; the registers are 100.0% of e-Stat's counts.
- **Economic Census control: 1.51** (3,272 Food service pins against 2,165
  飲食店 establishments in 21201), the brief's figure, just under the built
  cities' 1.56-1.92: the list's left-out kinds are not census
  establishments either.
- **Privacy verdict: publish.** `check_personal_exposure.py gifu`: the Japan
  pass prints 0; 4 trade names in the raw files are an operator's own name,
  2 pins show their permit type.
- **Rail:** N02-25; 12 stations: Meitetsu Nagoya Main 3 of 60, Kakamigahara
  6 of 18, Takehana 1 of 9 (柳津, a one-station stub kept as cut, Kobe's
  standing call), JR Central Tokaido 2 of 89 and Takayama 2 of 36. 名鉄岐阜
  and 岐阜, 418 m apart, stay apart (Ichinomiya's precedent). Gate 3 exact on
  all five lines. 18 excluded: 各務原市 7, 羽島市 4, 一宮市 3 (Aichi's N03 through
  `N03_NEIGHBOR_PREFS`), 笠松町 2, 岐南町 1, 瑞穂市 1. No Shinkansen track
  crosses the city. The thinnest stretch runs 37 and 40 trains a weekday.
  **Median nearest-station gap 545 m, not the brief's 641 m**: inside the
  owner band, parked. English names: OSM's 30 objects; 3 cited overrides
  (Kano, Kiridoshi, Meitetsu-Gifu). Meitetsu's red split three ways, JR
  Central's orange two (closest pair within 500 m 18.1).
- **Labels:** both JR lines' labels landed about 12 km outside the city (the
  first-segment trap); step 3's `in_city_first` puts all five inside.
- **Slips:** an early header probe printed one food-list row in full to the
  agent's own console, including its operator's name; nothing was written
  anywhere, and later probes printed counts only. The agent read two other
  builds' commits by `git show` and ran one `git status` (read-only), and
  read the portal's top page and the prefecture's terms page (no data) for
  the credit's wording.

### 2026-10-07 - Ōita built, one complete food list with the city's withheld addresses counted apart, the registers of March 2026 and MHLW's notifications

- **Ōita built (page 236, notice 183), Matsuyama's shape (one complete city
  food list beside MHLW's file), Hamamatsu's for the registers and
  Ichinomiya's for MHLW's notifications: 6,219 storefronts (Food service
  2,902, Food shops 1,508, Personal services 1,809) around 17 stations on 3
  lines, 52.9% of them in a ring (3,290).** On the Japan foundation's rules.
  Sources: the city's BODIK food list of every permit in term on 2026-09-01
  (6,199 rows), its barber, beauty and laundry lists of 2026-03-31 (391,
  1,308, 186), and MHLW's file (its 1,517 notifications read). Built by a
  subagent of the Regional-1 lead, integrated by the lead.
- **The withheld addresses (open call 1), by the foundation's `asterisk`
  rule:** 301 rows whose address the city masks with asterisks are set aside
  before any de-duplication and counted (250 restaurants), the brief
  exactly. The city's pages give no reason (staging's licence read), so the
  page says so plainly (precedents: Maebashi's laundry share stated with its
  cause; Fukuoka's `ADDRESS_BY_CONSENT` sentence). Of the 269 masked trade
  names, 267 are on withheld rows; 1 at a visible address shows its permit
  type, and 1 more is a citywide vehicle.
- **MHLW (open call 2), by Ichinomiya's call 127 and the batch's rule that
  hundreds of rows make a layer (Iwaki's call 150 left 164 out):** its
  notifications as a partial Food shops layer, 802 addressed of 1,517, 426
  pins. Its 85 permits are not added (all in the city's list by number).
  MHLW's point against the block point: median 40 m, 93.2% within 250 m (the
  brief 40 m, 94.7%). `SUPERSEDES` dropped 92 city rows. The city's own
  notification list was not approved and not fetched (parked call 4).
- **Terms (calls 161 and 172):** `TERM_AS_OF` food 2026-09-01 (the file's
  date), MHLW 2026-08-31. Past term 0, late 0, as the brief measured.
- **The brief's figures reproduce:** Food service 2,990 and Retail 1,323
  before the join against the brief's 2,989 and 1,324 (one combined 業態 cell
  read as its restaurant form, call 158). Restaurants 5,053, 101.6% of
  e-Stat's 4,971. Hostess venues 968.
- **Step 2:** 9,601 rows read. Set aside 301 withheld and 2 area-wide (MHLW);
  no address published 715 (MHLW); not a premises 369 (346 大分市内一円
  vehicles, stalls and demonstration sales, 4 storeless laundry pick-ups, 19
  MHLW mobile filings). Out by rule 1,524: 968 snack bars and cabarets, 246
  manufacturing and other non-counter types, 116 vending, 98 canteens, 40
  temporary or mobile, 33 inside accommodation, 20 caterers, 3 mail order.
  Join of 6,690 storefront rows: block 5,888, town-chōme 552, 小字 6, MHLW's
  point 86, unplaced 158 (2.4%). 221 repeat permits shown once. On the map:
  90.2% block, 8.7% town-chōme, 1.1% MHLW's point, 0.1% 小字.
- The 菓子 / そうざい factory share: 25 of 873 (2.9%), kept (owner,
  2026-09-24).
- **Economic Census control:** 2,902 Food service pins against 1,723 飲食店
  establishments in 44201: 1.68 per establishment, the brief's estimate.
- **Privacy verdict: publish.** `check_personal_exposure.py oita`: the Japan
  pass prints 0; 8 trade names in the raw files are an operator's own name,
  4 pins show their permit type (3 by the name rule, 1 masked by the city).
  No asterisk mask reaches the map.
- **Rail:** N02-25, 17 stations: JR Kyushu's Nippo Main Line 8 of 113, Hohi
  Main Line 6 of 37, Kyudai Main Line 5 of 37 (大分 one group on all three).
  No Shinkansen in the prefecture. Median nearest-station gap 2,209 m:
  standard rings. 6 excluded: 別府市 2, 由布市 2, 臼杵市 1, 豊後大野市 1. Gate
  3: JR Kyushu's timetable station index (read once by plain GET,
  2026-10-07, a page outside the cached files) gives 8, 6 and 5, exact.
  English names: OSM's 34 objects; 9 cited overrides (macrons dropped;
  豊後国分 "Bungo-Kokubu" for OSM's misread "Bungo-Kobuku"). Colours with the
  built Kyushu cities' hues (closest pair 92.3). No frequency floor: the
  thinnest stretch runs 25 to 26 trains a weekday each way.
- The licence row cites the 大分市オープンデータ利用規約 by title and date only:
  staging's record gives no URL.

### 2026-10-07 - Akita built, the city's full food list of October 2026, its barber and beauty registers and MHLW's notifications

- **Akita built (page 235, notice 182): 4,961 storefronts (Food service
  2,727, Food shops 997, Personal services 1,237) around 12 stations on 3
  lines, 32.7% of them in a ring (1,622).** The city's 食品営業許可施設一覧 is
  one XLSX of every permit in term on 2026-10-01 (4,041 rows), so nothing is
  rebuilt; the registers are one file per kind (理容所台帳 420, 美容所台帳 850,
  as of 2026-08-31); no laundry list exists. All CC BY 4.0, read 2026-10-07
  by staging (no prescribed wording, no cost clause; the use-report request
  is not a condition). No `"rules"` key. Built by a subagent of the
  Regional-1 lead, integrated by the lead.
- **The food file is renamed monthly:** `SOURCE_LINKS` reads the current
  `r\d{6}.xlsx` link from the page at a re-fetch (Kawasaki's and Ōtsu's
  precedent). `TERM_AS_OF` is 2026-10-01, the title's date. Past term 0;
  starting after the as-of 0.
- **MHLW's notifications in, as a partial Food-shops layer** (the brief's open
  call 1), by staging's precedent of 2026-10-06 naming Akita and Ichinomiya's
  shape (call 127): 1,227 届出 rows, 248 without a published address, 429
  pins (428 Retail, 1 Food service read as a yatai). MHLW's 245 permits not
  added. `OWN_POINT_FALLBACK` places 34 notification rows the join misses.
  `SUPERSEDES` keeps the MHLW row and drops 67 city rows.
- **The brief's food figures reproduce exactly** on the food list alone (not
  a premises 345, temporary or mobile by 業態 16, 仕出し 16, vending 1, no rule
  179; Food service 2,764 and Retail 720 storefront rows; 147 repeat permits;
  2 names withheld). With the foundation's 字 rules the food join rose from
  95.0% to 95.8% at the block and unplaced food rows fell from about 35 to 7.
- **Step 2, all sources:** 6,538 rows read. Not a premises 436; set aside 6
  (4 MHLW area-wide, 1 MHLW city-name-only, 1 mobile salon); closed 2. Out by
  rule 600. On the map: 95.9% block, 1.9% 小字, 1.7% town-chōme, 0.5% MHLW's
  point; 10 unplaced (4 in 御所野堤台3丁目, which MLIT's files lack). MHLW's
  points a median 56 m from the block point, 86.7% within 250 m; one point
  546 km off refused by the bbox guard.
- The 菓子 / そうざい factory share: 20 of 455 (4.4%), kept (owner,
  2026-09-24).
- **Economic Census control: 2.13** (2,727 Food service pins against 1,283
  飲食店 establishments in 05201), above the built cities' 1.56-1.92 (the
  brief predicted 2.11). The city's 業態名 carries no hostess-venue marker, so
  snack bars stay in Food service (`docs/category_rules.md` R3; Higashiōsaka's
  precedent). Built cities with a marker drop 14-16% of their restaurant
  permits that way (Fukushima 277 of 1,930, Maebashi 407 of 2,481); at that
  share Akita's ratio would be 1.79-1.82.
- **Privacy verdict: publish.** `check_personal_exposure.py akita`: the Japan
  pass prints 0; 15 distinct trade names in the raw files are an operator's
  own name, 2 pins show their permit type. The registers have no operator
  column, so only the sign test applies there (0 names).
- **Rail:** N02-25, 12 stations: JR Ou 8, Uetsu 5, Oga 1 (秋田 one group for
  Ou and Uetsu, 追分 for Ou and Oga). Gate 3 exact against JR East's station
  timetables. 2 excluded, both in 潟上市. The Akita Shinkansen runs over the Ou
  Line's track and is not counted. The Oga Line is a one-station JR stub kept
  as cut (Kobe's JR Takarazuka Line). The Uetsu Line at 桂根 (3 and 4 trains a
  weekday) is drawn and named (calls 46 and 86). OSM's 12 English names stand
  with no override. Colours from `line_colour_search.py` (Ou keeps
  Fukushima's orange; closest pair 61.6). Median station gap 3,093 m:
  standard rings.

### 2026-10-07 - Tsu built, Mie Prefecture's lists cut to the city by address

- **Tsu built (page 232, notice 179), Yokkaichi's shape with Uji's one
  difference: 3,234 storefronts (Food service 1,760, Food shops 559, Personal
  services 915) around 33 stations on 5 lines, 45.5% of them in a ring
  (1,472).** Built after staging's licence read the same day (PERMITTED WITH
  CONDITIONS, CC BY 4.0 by the 三重県オープンデータ利用規約 第１条), which
  unparked it (parked call 1). Sources: Mie Prefecture's three BODIK lists as
  of 2026-08-31 (food 18,680 rows, barbers 1,523, beauty 3,853; the
  prefecture except Yokkaichi). No laundry list exists: a disclosed gap. Built
  by a subagent of the Regional-1 lead, integrated by the lead.
- **The cut by address** (`config.source_rows`): an address beginning 津市
  once the prefecture is dropped, or 久居; a row naming 津市 elsewhere stops
  the build (none). Food 2,924 and barbers 251, the brief exactly; beauty 705,
  the brief's 701 plus 4 rows written under Hisai City (三重県久居市明神町,
  三重県久居中町 ...), merged wholly into Tsu in 2006, whose towns MLIT keys as
  Tsu's 久居…町: read as Tsu's on Matsue's 八雲村 precedent (an old place name
  read as the current one). The shared `other_muni` rule alone is not the
  cut: it would keep the prefecture's 196 unaddressed food rows, 10 register
  rows addressed 三重県一円 and 2 rows under old district names (多気郡,
  志摩郡). MHLW's file is a control, read by no step.
- **The brief's open call 1 needs no call:** MHLW's 159 Tsu retail
  notifications stay out as too thin, as Iwaki's 164 did (call 150).
- **Step 2:** 3,880 Tsu rows; no vehicle, stall or 一円 row; combined 業態
  cells read as their restaurant form 423 (call 158). Out by rule 440: 144
  manufacturing and other non-counter types, 119 canteens, 78 caterers, 66
  snack bars and cabarets, 33 inside accommodation, the brief's figures
  exactly. Storefront rows 3,440: Food service 1,806 and Retail 678 (the
  brief exactly), Personal services 956 (the brief's 952 plus the 4 Hisai
  rows). The join: block 2,708, town-chōme 642, 小字 centre 25, unplaced 65
  (1.9%); the foundation's 小字 rules lifted the brief's figures. 141 repeat
  permits shown once. On the map: 80.3% block, 18.9% town-chōme, 0.7% 小字.
  The brief's digit-space-digit pre-step (9 + 2 rows) is not written, being
  shared code for a few rows. One Hisai row (久居市明神町) may stay coarse:
  `"town_aliases": {"久居市": "久居"}` in its `japan.CITIES` entry would place
  it, for review time.
- The 菓子 / そうざい factory share: 27 of 449 (6.0%), kept (owner,
  2026-09-24).
- **Economic Census control: 2.02** (1,760 Food service pins against 872
  飲食店 establishments in 24201), above the built cities' 1.56-1.92
  (Yokkaichi 1.79). The catch-all form 飲食店営業（その他） holds 673 of Tsu's
  1,815 restaurant and cafe rows (37%, against Yokkaichi's 17%): counters the
  census files under a shop's main trade, plus five years of openings since
  2021; closures cannot be read (no status or expiry column). No page
  sentence proposed.
- **Privacy verdict: publish.** `check_personal_exposure.py tsu`: the Japan
  pass prints 0. One beauty row's trade name is its operator's own name; it
  is not placed, so no pin is withheld.
- **Rail:** N02-25; 33 stations: Kintetsu Nagoya 10 of 44, Kintetsu Osaka 5
  of 49, JR Kisei 4 of 41, JR Meisho 12 of 15, Ise Railway 4 of 10 (津 one
  group on three operators, spread 45 m). Median nearest-station gap 1,432 m:
  standard rings. 9 excluded: 鈴鹿市 5, 亀山市 2, 伊賀市 1, 松阪市 1. No line
  wholly inside, so no gate 3. English names: OSM's 67 objects, 1 cited
  override (伊勢大井 Ise-Oi). 川合高岡 and 一志, 179 m apart, stay separate.
  Colours from `line_colour_search.py` (the Ise Railway's blue goes purple,
  as in Yokkaichi). The JR Meisho Line, about 8 trains a day each way, drawn
  and named (calls 46 and 86).
- **Resource URLs** use the package name, since the brief truncates the
  package ids and no BODIK call was made; CKAN resolves names as ids. A
  future re-fetch should confirm one.

### 2026-10-07 - Ichinomiya built, the March food list kept whole with the months since, and the registers with their 2026 months

- **Ichinomiya built (page 231, notice 178), Fukuyama's shape (a city's own
  full food list plus the months since) with Toyota's precedent for a list
  that leaves rows out by design and Matsuyama's for MHLW's notifications:
  4,025 storefronts (Food service 2,001, Food shops 706, Personal services
  1,318) around 19 stations on 3 lines, 46.9% of them in a ring (1,887).** On
  the Japan foundation's rules (no `"rules"` key). Sources: the city's food
  list of permits in term on 2026-03-31 (2,815 rows) and its five monthly
  lists to 2026-08-31 (193), its barber, beauty and laundry lists of
  2026-03-31 (300, 819, 242) and the 2026 monthly beauty and laundry lists
  (13 and 1 rows; approved, call 128, fetched 2026-10-07, 12,264 B), and
  MHLW's notifications (995 rows). Built by a subagent of the Regional-1
  lead, integrated by the lead.
- **Merge (a) (owner, call 126) as two sources, not one rebuilt register.**
  The brief's `rebuilt_register(as_of=2026-03-31)` predates the term rules: a
  rebuilt source takes one `TERM_AS_OF`, and at 2026-03-31 call 172 would
  drop nearly every monthly permit, at 2026-08-31 call 161 would drop the 240
  old-law permits past their expiry that the owner's merge keeps. So the
  March list is source `food` (`TERM_AS_OF` 2026-03-31: past term 0) and the
  months source `food_new` of the same kind (`SOURCE_KIND`; `TERM_AS_OF`
  2026-08-31), and one pin per premises and bucket shows a renewal once. No
  shared code changed.
- **Late starters (call 172):** 62 monthly permits start after 2026-08-31: 29
  renew a premises the March list already holds (nothing lost), 33 wait.
  Against the brief's 2,898 permit keys and 2,228 restaurants (67.7%), the
  build holds 2,867 and 2,207 (67.0%); the 31 keys are those late starters.
  "About two restaurants in three" stands.
- **MHLW (call 127):** its 129 permits not added; its notifications as a
  partial Food-shops layer, 471 addressed of 992 open (the brief exactly),
  263 pins; its point where the block join misses by the shared
  `POINT_DONORS` (ward, town and trade name, not the permit number the brief
  matched on: no shared code keys by number): 9 city rows took it.
  `OWN_POINT_FALLBACK` placed 37 notification rows; 2 default points refused
  for 10 rows; MHLW's point against the block point a median 29 m, 94.3%
  within 250 m (the brief 26 m, 95.3%). 47 city rows dropped for an MHLW row
  of the same premises and bucket (`SUPERSEDES`, Matsuyama's).
- **A trap: July's beauty file (`biyou_20260731.csv`) is an XLSX workbook
  under a .csv name**, read city-locally by its magic bytes
  (`config.file_rows`). June's file has no 代表者氏名 column, so the months
  require 施設名称, 施設住所 and 申請者氏名 only.
- **Step 2:** of 4,302 storefront rows, 4,002 at the block, 131 at a 小字
  centroid, 68 at a town centre, 46 at MHLW's point, 55 unplaced (1.3%; 43
  barbers, beauty salons and laundries). On the map: 94.6% block, 3.1% 小字,
  1.6% chōme, 0.7% MHLW's point. Set aside: 7 area-wide addresses (MHLW), 5
  addressed in another municipality (the brief's five), 2 mobile salons.
  Closed 3; past term 0; late 62; no address published 521; not a premises
  5. Out by rule 471: 130 manufacturing and other non-counter types, 114
  snack bars and cabarets, 103 canteens, 61 vending, 43 caterers, 10
  temporary or mobile, 9 inside accommodation, 1 mail order. 175 repeat
  permits shown once.
- The 菓子 / そうざい factory share: 30 of 348 (8.6%), kept (owner,
  2026-09-24).
- **Economic Census control:** 2,001 Food service pins against 1,434 飲食店
  establishments in 23203: 1.40 per establishment, below the built cities'
  1.56-1.92, as expected for a list that holds two restaurants in three (the
  brief's 1.37; Kurume's 1.37 is the precedent for reporting it with that
  reason).
- **Privacy verdict: publish.** `check_personal_exposure.py ichinomiya`: the
  Japan pass prints 0; 2 trade names in the raw files are an operator's own
  name, 1 pin shows its permit type (the brief's one beauty salon).
- **Rail:** N02-25; 19 stations: Meitetsu's Bisai Line 10 of 22, Nagoya Main
  Line 8 of 60 (名鉄一宮 one group on both), JR Central's Tokaido Line 2 of 89
  (a main line cut at the line, Kurume's precedent). 名鉄一宮 and 尾張一宮, 38 m
  apart, are separate N02 groups of different names and stay apart. Median
  nearest-station gap 935 m: standard rings. 9 excluded: 稲沢市 7, Gifu
  Prefecture 2 (岐南, 笠松). Gate 3: Meitetsu's station index gives 8 and 10
  in-city stations, exact. English names: OSM's 38 objects; 2 cited overrides
  (妙興寺 Myokoji, 奥町 Okucho, macrons dropped). Colours: Meitetsu's red
  splits into red (Main) and red-orange (Bisai), 18.1 apart (Toyota's split).
  No frequency floor: the thinnest stretch runs 38 trains a weekday.
- **The credit's wording:** staging's record names the verdict but not the
  titles, so the titles were read from the city's own catalogue (2026-10-07)
  and the form from the terms' 3(2)(イ) (one read of the terms page, no data).
- **Ring share:** step 3 and the map's layer menu give 1,887; the lead's
  scratch count 1,884. The page uses the map's.

### 2026-10-07 - Fukuyama built, the food list rebuilt to August 2026 and checked for closures against MHLW's live file

- **Fukuyama built (page 230, notice 177), Higashiōsaka's rebuilt food
  register plus Matsuyama's MHLW beside a complete city list: 6,365
  storefronts (Food service 2,926, Food shops 1,665, Personal services 1,774)
  around 18 stations on 3 lines, 43.1% of them in a ring (2,745).** On the
  Japan foundation's rules (no `"rules"` key). Sources: the city's CKAN food
  list of 2026-03-31 (5,880 rows) and its five monthly files since (434
  filled rows), rebuilt to 2026-08-31; the seven earlier months read for
  their permit numbers only; MHLW's file (8,573 rows); the barber/beauty
  (1,634) and laundry (173) registers as of 2026-08-31. Built by a subagent
  of the Regional-1 lead, integrated by the lead.
- **The rebuild reproduces the brief exactly**: 6,314 rows read, 5,942 after
  de-duplication, **5,738 in term, 4,238 restaurants**. It is city-local
  (`config.rebuilt_food`), because `japan_register.rebuilt_register` returns
  no permit number (the closure filter and MHLW's point key on it) and keeps
  only the first form column (業態 before 形態); a check stops the build if
  its in-term set ever differs from the shared function's.
- **A renewal that starts after the as-of waits; the permit it replaces
  stands** (call 172, applied to the rebuild). Ranked on the latest expiry
  alone, 19 renewals in the August file that start on 2026-09-01 won their
  premises, and step 2's call-172 rule then dropped them, so 17 premises
  whose permit ran to 2026-08-31 left the map. The rebuild now ranks only
  permits started by 2026-08-31: in force 5,736 (4,237 restaurants), 17 with
  a waiting renewal; the 2 with no earlier permit wait. No direct precedent:
  for review time.
- **The closure filter (owner, 2026-10-05, call 6)**: 151 new-law permits
  MHLW no longer holds, the brief exactly (115 restaurants). Read at build: 7
  premises had been renewed in MHLW's file alone under a new number starting
  2026-09-01, so the filter would have dropped an open premises whose renewal
  call 172 then makes wait. A permit MHLW renewed for the same premises and
  type under a number no city file lists is therefore not a closure (6 after
  the rebuild; precedent: the waiting renewal above). **145 left out as
  closed (109 restaurants); the register keeps 4,128 restaurants, 96.0% of
  e-Stat's 4,302** (the brief 4,123, 95.8%). For review time.
- **MHLW beside the city's list (owner, 2026-10-05, call 5)**: its 3,282
  notifications (1,854 addressed) and 7 closed ones, and its 44 open permits
  in no city file (34 restaurants; 10 start 2026-09-01 and wait, 15 are
  institutional kitchens) through `config.mhlw_rows`: 836 Food shops pins and
  6 Food service pins. Its point by permit number rides on 3,468 rebuilt
  city rows (`OWN_POINT_FALLBACK` = food and MHLW; call 5a says "by permit
  number", so not Matsuyama's `POINT_DONORS` name match). `SUPERSEDES` drops
  395 city rows for an MHLW row at the same premises and bucket (mostly
  supermarkets and konbini holding a city permit and filing a notification).
- **Step 2:** 7,269 storefront rows; on the map 90.3% block (5,746), 4.8%
  MHLW's point (303), 5.0% town-chōme or 大字 centre (316); 27 unplaced
  (0.4%), most in 水呑町三新田 (MLIT's files lack it). MHLW's point against the
  block point: median 39 m, 95.6% within 250 m (3,559 rows; the brief 38 m /
  96.2%). Set aside: 178 area-wide addresses (広島県内 vehicles), 1 in another
  municipality. Not a premises 102; no address published 1,429 (MHLW; no
  restaurant); closed 7; starting after the as-of 10 (MHLW). Out by rule
  1,735: 540 manufacturing and other non-counter types, 421 canteens, 274
  snack bars and cabarets, 216 vending, 123 karaoke and amusement venues, 74
  temporary or mobile, 53 inside accommodation, 26 caterers, 8 mail order.
  482 repeat permits shown once.
- **Registers**: barbers 396, beauty 1,238 (one file split by 種類),
  laundries 173 (3 empty rows dropped as no premises); shares of e-Stat
  FY2024 97.8%, 102.4%, 86.5%. No laundry sentence on the page beyond the
  counts in What Is Excluded: the dataset gives no cause (Maebashi's was the
  owner's call 14 for its own note).
- The 菓子 / そうざい factory share: 52 of 601 (8.7%), kept (owner,
  2026-09-24).
- **Rail**: N02-25, the brief's stub test reproduced (Sanyo 5 of 131, Fukuen
  12 of 27, Ibara 3 of 15), 18 stations (福山 and 神辺 shared), median gap
  1,479 m: standard rings. 7 excluded (Fuchu 4, Ibara 2, Onomichi 1). OSM
  `name:en` for all 18 (27 objects; one query under the session's Overpass
  lock, overpass-api.de 504, kumi answered); 1 override (備後本庄
  Bingo-Honjo, OSM's macron). No gate 3: no line wholly inside (Fukui's
  form). No frequency floor (calls 46 and 86); JR at least hourly. Colours
  from `line_colour_search.py` (Sanyo teal, Fukuen red-orange, Ibara green;
  closest pair 92.7).
- **Economic Census control:** 2,926 Food service pins against 1,737 飲食店
  establishments in 34207: 1.68 per establishment, the brief's estimate,
  inside the built cities' 1.56-1.92.
- **Privacy verdict: publish.** `check_personal_exposure.py fukuyama`: the
  Japan pass prints 0; 35 trade names in the raw files are an operator's own
  name, 6 pins show their permit type.

### 2026-10-07 - Fukushima built, the full food list kept whole with five months of new permits, all three buckets from the city's own lists

- **Fukushima built (page 233, notice 180): 3,335 storefronts (Food service
  1,653, Food shops 621, Personal services 1,061) around 22 stations on 4
  lines, 60.4% of them in a ring (2,013).** Fukuyama's shape (a city's full
  food list plus the months since) with Ichinomiya's answered merge. All
  three buckets come from the city's own CSVs on its 食品営業許可施設、
  生活衛生関係施設一覧 page (CC BY 2.1 JP by the 福島市オープンデータ利用規約;
  the uncapped ４ accepted, call 110). No `"rules"` key (`ALL_RULES`).
  `brief_check.py` 18/18 (2026-10-07). Built by a subagent of the
  Regional-1 lead, integrated by the lead.
- **The merge (the brief's open call 1), by precedent: Ichinomiya's call 125
  and Iwaki's 149.** The list of permits in term on 2026-03-31 is kept whole,
  and the five monthly lists of new permits (April to August) are added.
  They are read as two sources, `food` and `food_new` (`SOURCE_KIND`), each
  through `rebuilt_register`, and each permit's term is read against its own
  file's date (`TERM_AS_OF` 2026-03-31 and 2026-08-31). One source rebuilt
  from all six files has only one as-of: 2026-03-31 would hold back the 89
  new permits as late starters (call 172), and 2026-08-31 would drop the 98
  permits expiring in May and July (call 161), which the months never
  republish.
- **The brief's figures reproduce:** one rebuild of all six files gives
  3,769 rows, 2,883 restaurant permits (101.3% of e-Stat's 2,846), Food
  service 1,658 and Retail 772. The two sources give 3,776 rows (3,689 +
  87); the 7 extra rows are new permits at a premises already in the full
  list (4 Food service, 1 Retail, 2 snack bars), and one pin per premises
  folds them. Permits past their term 0; starting after the as-of 0. City
  config only; the foundation's checklist names Fukushima's kind per file
  as city-local.
- **MHLW's file stays a control** (open call 2, staging's call 152), by
  Iwaki's call 150 and Tsu's precedent: a thin notifications layer stays
  out. Its 44 permits are all in the city's files, and it has 144 fixed
  Retail notifications. Not in `SOURCE_FILES`, not on the notice; a
  "(control)" row in `docs/data_sources/japan.md`.
- **Caterers (open call 4):** the shared `FORM_RULES` as written
  (`docs/category_rules.md`; Sasebo's and Kanazawa's 仕出し precedent). 230
  restaurant permits go out as 仕出し, 161 of them also naming a counter
  form.
- **The registers' monthly files** (open call 3, staging's 153) were not
  fetched; the registers stand at 2026-03-31 (parked call 2, not blocking).
- **Step 2:** 4,869 rows read (food 3,689, months 87, barbers 278, beauty
  638, laundries 125, coin laundries 52). Not a premises 162 (145 food
  permits with no address, the festival stalls among them, and 17 storeless
  laundry pick-ups). Out by rule 1,196: 277 snack bars and cabarets, 230
  caterers, 229 manufacturing and other non-counter types, 186 vehicles
  (種目 自動車による営業, four spellings), 161 canteens, 106 inside
  accommodation, 7 vending. Join, 3,511 storefront rows: block 3,176,
  town-chōme 150, 小字 centroid 178 (the foundation's `koaza_centroid`),
  unplaced 7 (0.2%; the brief's 40 came before the foundation's 字 rules).
  One pin per premises: 169 repeat rows. On the map: 90.9% block, 4.3%
  town-chōme, 4.9% 小字. Registers against e-Stat FY2024: barbers 278 of
  282, beauty salons 638 of 630, laundries 108 of 117, as the brief says.
- **The 菓子 / そうざい factory share:** 18 of 553 (3.3%), kept (owner,
  2026-09-24).
- **Economic Census control:** 1,653 Food service pins against 1,030 飲食店
  establishments in 07201 (2021, table 9-1A, industry 76): 1.60 per
  establishment, inside the built cities' 1.56-1.92. The brief's 1,226
  establishments and its 1.35 estimate do not reproduce from
  `japan_census_control.py`.
- **Privacy verdict: publish.** `check_personal_exposure.py fukushima`: the
  Japan pass prints 0; 4 trade names in the raw files are an operator's own
  name, 2 pins show their permit type. 営業者氏名 / 営業者氏名漢字 and 開設者氏名
  are read in memory only; the operators' own addresses and phones are never
  selected.
- **Rail:** N02-25, 22 stations: the Iizaka Line 12 of 12, the Abukuma
  Express 5 of 24, JR Tohoku 5 of 155, JR Ou 3 of 105 (福島 one group on all
  four, spread 36 m). The Tohoku Shinkansen dropped; the Yamagata
  Shinkansen stops at neither 笹木野 nor 庭坂. 5 excluded: 伊達市 3, 二本松市
  1, Yamagata Prefecture 1 (板谷). Gate 3: Fukushima Kotsu's timetable page
  lists 12 stations, exact. English names: OSM's 32 objects, 3 cited
  overrides (Bijutsukan-toshokan-mae; Iizaka-onsen, as Hakodate's
  Yunokawa-onsen; Ioji-mae for OSM's Iohji-mae). Line names follow JR
  East's 福島 timetable index and ii-den.jp, with no macrons. Colours from
  `line_colour_search.py` (the Abukuma blue goes teal, Maebashi's; the
  Tohoku green olive; closest pair 45.4). Median station spacing 862 m:
  standard rings. No frequency floor (calls 46 and 86): the Ou Line from 福島
  to 庭坂, about 11 trains a day each way, drawn and named.
- **A slip:** staging's record did not quote the terms' ２(３) credit form,
  so the build fetched the terms PDF the brief names
  (`opendatariyokiyaku_2.pdf`, 133,265 B, HTTP 200, the city's host) into
  the scratchpad and read the form only; the verdict was not re-read. A
  terms page, not data, but not named for fetching at the build.
- **For the next city with a full list plus new-permit months:** under the
  foundation's term rules (calls 161 and 172) it cannot be one
  `rebuilt_register` source, since `TERM_AS_OF` takes one date per source;
  two sources by `SOURCE_KIND` is the shape (Ichinomiya's and Iwaki's too).
  Proposed for the japan-city skill at review time.
- **Not done here, by rule:** no region view, label tier or label offset
  (owner, call 198); `screen_japan_join.py` has no Fukushima entry;
  `city_master_list.md`'s built counts are Staging's.

### 2026-10-07 - Maebashi built, two food lists split by date and registers rebuilt to August 2026

- **Maebashi built (page 229, notice 176), Fukuoka's and Utsunomiya's
  two-source food shape plus its 生活衛生 registers: 4,696 storefronts (Food
  service 2,074, Food shops 1,362, Personal services 1,260) around 19
  stations on 3 lines, 40.5% of them in a ring (1,901).** The first city on
  the Japan foundation's rules (no `"rules"` key; `japan.city_rules` gives
  `ALL_RULES`). Sources: MHLW's filings (4,133 rows, every permit first
  granted from 2023 and the notifications), the city's food file from its
  former system (2,117 rows, as of 2026-06-30, granted 2019-10 to
  2023-03-31; the newest edition at build, `brief_check.py` 9/9), and the
  registers rebuilt by `config.source_rows`: the 2026-03-31 base zip plus
  five months of new and closed zips, keyed on 整理番号, every closure
  matched (barbers 310, beauty 830, laundries 139: the brief exactly). The
  rebuild stops the build on a closure that matches nothing, a repeated or a
  blank key, so it is exact, never an upper bound. A city `source_rows`, as
  the build prompt says for a zipped register; no shared code changed for it.
- **Terms (calls 161 and 172):** `TERM_AS_OF` MHLW 2026-08-31 (the month its
  file covers; newest permit 2026-08-28), the food file 2026-06-30 (its own
  date; its 179 rows expiring 2026-09-30 are in term then). Past term 0;
  starting after the as-of 1.
- **Step 2:** of 5,078 storefront rows, 4,628 at the block, 237 at MHLW's own
  point (all from chōme), 211 at a town centre, 2 unplaced (a barber at
  駒形町東高島 and a laundry at 駒形町増田境, addresses MLIT's files do not
  hold). On the map: 91.7% block, 4.4% MHLW's point, 3.9% town centre.
  MHLW's point against the block point: median 42 m, 92.4% within 250 m
  (2,100 rows), the brief exactly. 149 of the city's rows dropped for an MHLW
  row (`SUPERSEDES`: the brief's 18 counted restaurant permits only; the key
  is per premises and bucket, so the co-located Retail rows and konbini
  permits it lists go too, as the one-pin rule would fold them), 231 repeat
  permits shown once. Set aside: 3 mobile salons (`idou`, the brief's three),
  2 area-wide addresses. Closed 16; no address published 635 (MHLW; 38 of
  1,850 open restaurant permits, "one in 50", the brief's figure); not a
  premises 328. Out by rule 1,466: 409 manufacturing and other non-counter
  types (the brief's 299 + 110 exactly), 407 snack bars and cabarets by
  業態, 299 canteens, 187 temporary or mobile, 78 vending, 49 inside
  accommodation, 30 caterers, 7 mail order.
- The 菓子 / そうざい factory share: 34 of 541 (6.3%), kept (owner,
  2026-09-24).
- **Economic Census control:** 2,074 Food service pins against 1,299 飲食店
  establishments in 10201: 1.60 per establishment, inside the built cities'
  1.56-1.92 (the brief predicted 1.62 before de-duplication).
- **Privacy verdict: publish.** `check_personal_exposure.py maebashi`: the
  Japan pass prints 0; 19 trade names in the raw files are an operator's own
  name, 3 pins show their permit type. The name rule compares MHLW's 法人名,
  the food file's 営業者名 and the registers' 開設者氏名 / 営業者氏名 and their
  representatives, in memory only.
- **The privacy check's Japan pass corrected** (`scripts/check_personal_exposure.py`):
  it read a city's rules as `CITIES[slug].get("rules", ())`, so a city built
  after the foundation (no `"rules"` key) was checked with no rules while
  step 2 reads `ALL_RULES`; on Maebashi it counted 10 names step 2's rules do
  not flag (26 names against 19). Now `japan.city_rules(slug)`, which returns
  `WAVE2_RULES` for every built city, so their verdicts stand (Sasebo
  re-run: 0). East-1 made the identical one-line change on its branch.
- **Rail:** N02-25; 19 stations: the Jomo Line 14 of 23, JR Ryomo 4 of 19, JR
  Joetsu 2 of 39 (新前橋 one group on both JR lines). No Shinkansen station
  in the city; JR's Agatsuma Line has no in-city station of its own and is
  not drawn. Median nearest-station gap 1,000 m: standard rings. 6 excluded:
  桐生市 2, 高崎市 2, 伊勢崎市 1, 渋川市 1. Gate 3: the Jomo Electric
  Railway's timetable index gives 14 in-city stations, exact. English names:
  OSM's 35 objects, 1 cited override (心臓血管センター, "Shinzo-kekkan
  Center"). Colours from `line_colour_search.py` (the Jomo blue goes teal,
  Sasebo's; Ryomo yellow to ochre; closest pair 61.3). No frequency floor
  (calls 46 and 86): the Jomo Line every 30 minutes, nothing under hourly.
- **Not done here, by rule:** no region view, label tier or label offset
  (owner, call 198: Cleanup builds the Japan views), so the scaffold's
  default offset stands and Maebashi has no `label_tier`; `screen_japan_join.py`
  has no Maebashi entry (step 2 measures the join); `city_master_list.md`'s
  built counts are Staging's (the plan's change 4), so `check_provenance.py`
  fails on them until Staging moves the batch.
