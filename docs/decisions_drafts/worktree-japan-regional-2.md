# Decisions drafts: Regional-2 (branch worktree-japan-regional-2)

The Regional-2 build session of the A and B build plan
(`docs/build_plan_2026-10-07.md`), phase 2: Shizuoka, Kanazawa, Okazaki,
Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure and Kurashiki, on
pages 258-267 and 306 and notices 205-214 and 216. Newest first; Cleanup folds
these into `DECISIONS.md`.

## For Cleanup, raised by the owner (2026-10-11)

- **Call 182's hook belongs in shared code (owner: "call 182 bring to the
  surface for cleanup").** Call 182 (owner, 2026-10-06) has the name rule
  read MHLW's 法人名 through the permit match and withhold the matching city
  trade names. Shared `japan_step2` has no permit-match mechanism, so
  Yamagata's builder implemented it in `pipeline/yamagata/config.py`'s
  `source_rows`: it reads MHLW's 法人名 in memory by permit number and grant
  date and carries only the yes or no answer on the city's row (Kyoto's
  `name_is_operator` key). It flags 3 rows where the brief counted 4, and a
  looser match finds no fourth. No built city has a twin of this hook. For
  Cleanup: review the hook, move the permit match into `japan_step2` (with
  the Minato control and a drift run of every Japanese city), say whether
  the fourth row matters, then delete the city-local copy. Yamagata's
  privacy pass prints 0 as built.

## Parked calls

Each city's own parked calls and proposals are under its entry below
("Parked calls", "Proposals"). The lead's, by city and letter:

- **Okazaki A: Meitetsu's red on two neighbouring maps.** Okazaki's Meitetsu
  Nagoya Main Line takes the registry's `#E80010`; Toyota's built map draws
  the Meitetsu Mikawa Line in the same `#E80010`, and the two lines come
  within 2 km of each other, so `check_line_identity.py` reports 1 problem
  (CIE76 0.0, under 10). Recommended: a `NEIGHBOUR_EXCEPTIONS` entry, as JR
  East's orange for the Musashino and Chuo lines: Meitetsu signs every line
  in the one red, and the two lines never share a map. Tradeoff: a reader
  moving from Toyota's map to Okazaki's sees one red for two lines. The
  alternative moves Toyota's Mikawa Line (a built map: Cleanup's, with a
  re-render). Nothing was changed; Okazaki is committed with the check
  failing on this one pair.
- **Kurashiki A: 83 vending-machine pins a missing shared rule leaves on the
  map.** Kurashiki's brief lists 自動販売形態 (the old-law vending form) as a
  shared-code item, but `japan_eigyo.FORM_RULES` does not hold it, so 83
  vending machines (67 on a café permit, 3 on a restaurant permit, 13 milk
  sellers) are on the map as built; What Is Excluded says so. Parked, not
  fixed city-locally. Recommended: add the form to `FORM_RULES` (vending is
  out everywhere), check by drift that no built city moves, re-run
  Kurashiki's steps 2 and 3 and re-record its baseline before the page
  lands. Tradeoff: a taxonomy change with a Japan-wide drift run; without it
  the page publishes 83 pins the owner's rule leaves out.
- **Kurashiki B: 特殊形態, 8 pins at fixed addresses.** The brief expected them
  set aside; no rule names the form and its meaning in the prefecture's old
  ordinance is unread. Recommended: read it before any rule; kept as built.
- **Tottori A: a shared rule that misses, worked around in the city's
  config.** The foundation's area-wide rule tests the prefecture-wide
  address before the city's name is cut, so Tottori's main spelling
  (鳥取県鳥取市鳥取県内, 226 rows, and three rarer forms) passes it: without a
  hook 208 stalls and vehicles land on the map at MHLW's point (2,448
  storefronts). The builder added a narrow `source_rows` normalisation in
  `pipeline/tottori/config.py` so the shared rule fires (237 set aside, 2,240
  storefronts), which is a city-local fix the plan says to park. Kept,
  because the alternative publishes stalls the owner's rule leaves out.
  Recommended: move the test in `japan_register.permits_from_rows` after the
  city cut, re-run the Minato control and every city screen, then delete
  Tottori's hook. Tradeoff: a shared-code change with a full drift run.
- **Okazaki B: one BODIK request carried the owner's email address.** The
  Okazaki builder's first `package_show` call (one metadata request to
  `data.bodik.jp`, 2026-10-11) went out with a hand-typed user-agent that
  included the owner's email address; every later request used the
  project's own string. It cannot be recalled. The builders' instructions
  now forbid anything personal in a header or URL. For the owner to know;
  no action recommended. **A second one, the same day:** Matsue's builder,
  launched before that instruction was added, sent one GET to
  `railway.ichibata.co.jp/operate/timetable/list/` (the gate 3 station list)
  with the same kind of user-agent. Two requests in all, to two hosts.

## Proposals for review time (sentences no template covers)

- **Shizuoka, the source bullet** (the owner asked for each list's date on
  the page, 2026-10-04): "From Shizuoka City's registers of barbers, beauty
  salons and laundries: the complete lists as of March 31, 2026 and the new
  premises listed each month since, to August 31, 2026 for barbers and
  September 30, 2026 for beauty salons and laundries."
- **Shizuoka, the food bullet** (Kōchi's sentence with Shizuoka's share):
  "Restaurants, cafés and shops are not on this map: the national list of
  food businesses gives an address for only about six in ten of Shizuoka's
  restaurants."
- **Shizuoka, the sightseeing bullet** fills the template's slot for a line
  rather than cable cars: "The Oigawa Railway's Ikawa Line, which is a
  sightseeing line, is not drawn."

## Downstream inputs this branch changes

- New cities (Visuals, Analytics): Shizuoka (`shizuoka`, notice 205; English
  station names from OpenStreetMap, rail from MLIT N02). Notice 205: caption
  only (CC BY 4.0 asks for attribution with the work, no placement named).
  No open terms question.
- `pipeline/line_registry.py`: `jr-central-tokaido-line` gains Shizuoka.

## Changes

### 2026-10-12 - The owner's answers applied on this branch (S16, S23, S24, S27); 特殊形態 read (S18)

- **"yes apply all, fetch approved for s18"** (owner, in the Regional-2
  chat, confirming staging's relay below).
- **S16, the Meitetsu exception:** `pipeline/line_registry.py` gains
  `NEIGHBOUR_EXCEPTIONS[{meitetsu-nagoya-main-line, meitetsu-mikawa-line}]`
  ("Meitetsu's own red for both lines") with its note. The check keys an
  exception on registry identities, so the Mikawa Line was registered as
  `meitetsu-mikawa-line` at the colour Toyota's map already draws
  (`#E80010`, `maps: {"toyota": "MM"}`); Toyota's config and map are
  untouched. `check_line_identity.py`: PROBLEMS 0, 7 pairs excepted.
- **S23, Kure's share:** "about three restaurants in five" became "about
  half (46%)", the Food service rows a reader sees (806 of e-Stat's 1,752
  restaurant permits, 46.0%), on the page, in What Is Excluded and in table
  B of `docs/map_inconsistencies.md`. The page sentence, for review time:
  "The map shows about half (46%) of the restaurants in the official count:
  the ministry's list holds permits granted since June 2021, vehicles and
  stalls are left out, and about three fixed restaurants in ten do not
  publish their address." The earlier 58.3% (1,022 addressed fixed permits)
  was the brief's figure and is no longer stated.
- **S24, gate 3 with no in-city count:** accepted for Aomori, Tottori,
  Yamagata and Kure. The note was already in each city's row of table A
  ("no line wholly inside: gate 3 has no in-city count"); nothing more was
  written.
- **S27, Yamagata's Zao Onsen rows:** the 10 placed rows stay, and What Is
  Excluded now says so: 23 premises there are unplaced while 10 others sit
  at the ministry's own coordinates, because the ministry's list holds the
  same premises.
- **S18, what 特殊形態 means (read 2026-10-12, one page):** Okayama City's
  page 「自動車や屋台等で調理を行う場合の営業許可について」
  (`https://www.city.okayama.jp/kurashi/0000038347.html`, dated 2024-05-23),
  which applies the prefecture's ordinance, describes 飲食店営業（特殊形態第1種）
  as 「自動車（キッチンカーを除く）、屋台等移動又は撤去を前提とする施設」, with
  tents as its example and 岡山県内一円 as its area: a facility meant to be
  moved or taken down. The prefecture's own ordinance text was not found
  (one attachment URL answered 404), so the old-law form is read from the
  current page's use of the same name: ASSERTED for the pre-2021 rows.
- **The 8 pins checked** (trade names and addresses, from the clean file):
  6 are concession stands at the Muscat Stadium (中庄 3250-1, floors 1 to 3)
  and 2 are one market stall on the plaza in front of 吉備真備 station, on a
  restaurant and a confectionery permit. None is an everyday shopfront.
- **A rule is needed, and it is Cleanup's to write (S14):** recommended that
  特殊形態 join `japan_eigyo.FORM_RULES` as a temporary form, beside 露天 and
  the vending form of S17, in the same change. It would take these 8 pins
  off Kurashiki's map (63 of the 71 old-law restaurant rows with the form
  are already out as area-wide). Tradeoff: stadium stands at a fixed address
  go with it, where the owner kept fixed-pitch yatai (屋台) in Fukuoka and
  Kure; the difference is that these open on event days only. Nothing was
  changed on the map; Kurashiki is re-run once after Cleanup's change.
- **S22, Kanazawa (relayed by staging, 2026-10-12; the owner: "s22 no
  share, yes read the frequency"):** the page states no share, as built.
  Staging read IR Ishikawa's whole-line timetable of 2026-03-14 and counted
  about three trains an hour each way (its record is in staging's drafts):
  no low-frequency stretch, nothing to change on Kanazawa's page.
- `check_all.py` after these changes: 49 of 51. The two left are the master
  list's built counts (staging, after landing) and Fuji's and Kurashiki's
  macro labels (Cleanup, call 198).

### 2026-10-12 - The owner's answers to S14 to S27, as staging relayed them (not yet applied on this branch)

- **Relayed by staging from its own chat, 2026-10-12; the owner's words:**
  "s14 cleanup, s15 accept, s16 exception and note, s17 yes, s19 yes, s20
  yes, s23 we can say about half(46%) if that's more accurate, s27 keep the
  10 and note the oddity. s18 read and check then write rule if needed. s21
  correct and keep. s22 should we state share and read quickly? s24 accept
  and note. s25 accept." Staging's record is the source; this entry is a
  copy of its relay, and nothing below was changed on this branch on the
  relay alone (the owner confirms in the Regional-2 chat first).
- **What each means for this branch:** S14, S17 and S19: the shared-code
  changes (自動販売形態 in `FORM_RULES`; the area-wide test after the city cut)
  are Cleanup's, then Kurashiki's steps 2 and 3 and baseline are re-run and
  Tottori's hook deleted, before those pages land. S16: a
  `NEIGHBOUR_EXCEPTIONS` entry for Meitetsu's Nagoya Main and Mikawa lines,
  with a note. S18: read what 特殊形態 means and check Kurashiki's 8 pins,
  then a rule if one is needed. S20: Tottori's Inbi Line accepted as drawn.
  S21: Matsumoto's 2026-10-01 edition kept. S22 (Kanazawa): open, the owner
  asked a question back. S23: Kure's "about three restaurants in five" may
  become "about half (46%)", the share of the Food service pins a reader
  sees (806 of 1,752). S24: gate 3 with no in-city count accepted for
  Aomori, Tottori, Yamagata and Kure, with a note. S25: Aomori's clause 6
  accepted. S27: Yamagata's 10 placed Zao Onsen rows kept, the oddity noted.

### 2026-10-12 - Fuji's notice credit checked by staging; the parked calls numbered

- **Fuji's parked call 1 is closed: notice 210 follows the portal's
  prescribed form.** Staging read Shizuoka Prefecture's terms page
  (`opendata.pref.shizuoka.jp/privacy.html`, §4) on 2026-10-12: the
  modified-use form is the one the notice was drafted in, and the terms
  allow the URL as a link on the licence name. One difference was corrected:
  the terms write 表示 4.0 国際 with a space after 表示, so the notice in
  `app/components.py`, item 210 in `docs/data_sources.md` and the licence row
  in `docs/data_sources/japan.md` now do too. Shizuoka City's notice 205 is
  under the city's own terms and was not changed. No map re-rendered (a
  notice is page text).
- **Staging's numbers for this batch's parked calls** (with the owner, none
  answered): Okazaki A S16; Kurashiki A S17 and B S18; Tottori A S19;
  Tottori's Inbi Line against call 180 S20; Matsumoto's edition S21;
  Kanazawa's notes S22; Kure's "three in five" S23; gate 3 with no in-city
  count S24; Aomori's clause 6 S25; the proposals S26 (review time);
  Yamagata's 10 placed Zao Onsen rows S27. Who makes the shared-code changes
  in S17 and S19 is S14 (staging recommended Cleanup).

### 2026-10-11 - Kurashiki built, the city's year-end food-permit list of March 31, 2026, food only

- **Kurashiki built (page 306, notice 216), Hiroshima's page shape (food
  only) on a source that is rows, not a file (a PDF read through
  `config.source_rows`, Kyoto's and Maebashi's hook): 4,904 storefronts
  (Food service 4,005, Food shops 899) around 21 stations on 6 lines, 53.2%
  of them in a ring (2,610: 2,281 and 329) on the standard rings.** Source:
  Kurashiki City's 食品営業許可一覧, the year-end list of permits in force
  (令和7年度末, 2026-03-31), `r07nenndinatu_2026-03-31.pdf`, 8,034,340 B, 243
  pages, CC BY 4.0 by the page's mark (read 2026-10-08 by staging). Built by
  a Regional-2 subagent; the brief passed 11 of 11 on 2026-10-11.
- **The PDF is read with `pdftotext -table` only** (xpdf 4.06), never a
  hand-written decoder. `fetch_sources.py city` writes the text beside the
  PDF (`r07nenndinatu_2026-03-31.table.txt`, 1,713,215 B, recorded in
  provenance with the tool and its sha256) and `config.pdf_rows()` reads it:
  each page's header gives the column offsets; the operator cell, the
  operator's phone cell and the address by offset; three dates and the
  permit number from the right by pattern; the form (6 values), the type and
  the premises' phone as whole tokens off the right of the trade-name cell.
  It stops on a page without a header, a line that is not a record, a cell
  overflowing the address column, or a record without a type. The whole
  extraction ran once through the gate (`heavy_job.py`, label "kurashiki
  pdf", admitted after a wait behind four basemap jobs). Step 2 reads the
  text and never runs pdftotext.
- **The reader reproduces the brief exactly:** 6,288 records on 242 pages,
  38 types, 6 forms (普通形態 970, 特殊形態 101, 自動販売形態 91,
  卸販売及び小売販売形態 48, 簡易形態 47, 移動販売形態 12, every one on a
  pre-2021 row), 飲食店営業 4,727 (867 old-law), 1,322 old-law rows, 13 blank
  operator cells, 11 blank and 66 ＊＊＊ trade names, 667 rows with 一円, no
  expiry before 2026-03-31, no grant after it.
- **Call 229, the same-number rule, as the brief and DECISIONS record it:**
  127 permit numbers carry one old-law and one new-law row; the old-law row
  goes (108 restaurants, 8 confectioners, 3 cafés, 2 delis, 2 fishmongers, 2
  butchers, 2 others), leaving 6,161 rows and **4,619 restaurant permits,
  99.3% of e-Stat's 4,653**. A number repeated in any other shape stops the
  build (none). The other 1,195 old-law rows stay: "pre-2021 rows dropped"
  was read as the old-law row of a pair, not every old-law row, since the
  brief's and DECISIONS' wording, the expected counts and call 230's ratio
  all keep them.
- **Step 2:** 4 rows set aside as area-wide (周辺 / 全域), 657 not a premises
  (一円: 608 restaurant permits, 19 fishmongers, 18 confectioners, 8 cafés, 2
  butchers, 2 milk sellers), 0 past term and 0 late starters against
  `TERM_AS_OF` 2026-03-31, 326 not a storefront (239 "no rule", 87 vending
  machines by type). Storefront rows 5,174 (Food service 4,099, Retail
  1,075); 270 repeat rows shown once; **4,904 pins**. The brief expected
  about 3,933 and 886 with two shared-code items it listed as landed first;
  they are not in shared code (parked calls 1 and 2), which is the whole
  difference: 83 pins carry 自動販売形態 (67 喫茶店営業, 13 乳類販売業, 3
  飲食店営業) and 8 carry 特殊形態 (6 飲食店営業, 1 喫茶店営業, 1 菓子製造業).
- **The join:** block 4,531 rows (87.6%), town-chōme 643 (12.4%), unplaced
  0; on the pins 87.8% and 12.2% (599). The brief's figures.
- **Position check (MHLW's file, read by no step):** on the 169 pins MHLW
  also holds with a point, a median 97 m; on the 128 block-tier pins a
  median 66 m, 85.9% within 250 m (the brief: 67 m, 83.5%), 1 over 1 km
  (松島, where MHLW's point is at 倉敷 station, 4.1 km from the address's
  block). The 41 town-chōme pins sit a median 288 m off, 8 over 1 km: five
  at 酒津 and one at 林 (large 大字, 1.2 to 1.6 km from the centroid) and one
  at 東塚1丁目 whose MHLW point lies 6.7 km away in 児島 (MHLW's point, not
  the join, is the outlier).
- **The name rule:** 6 trade names in the list are an operator's own name
  (the brief's 6); 4 pins show their permit type. 24 more pins the list
  masks with ＊＊＊ and 9 with a blank name show their permit type too
  (counted on `businesses_clean.csv`, the data the map embeds).
- **Factory share:** 27 of 638 菓子 / そうざい premises (4.2%); kept (owner,
  2026-09-24).
- **Economic Census control (`scripts/japan_census_control.py kurashiki`):**
  4,005 Food service pins against 1,405 establishments (2021), **2.85 per
  establishment**; about 2.80 once the vending and 特殊形態 pins go (the
  brief's 3,933). Accepted and recorded by the owner (call 230): the city
  has 3.31 in-force restaurant permits per census establishment (4,653 over
  1,405, the highest of the 14 cities the Kure brief read), so the excess is
  permits the census does not count as establishments, not a join defect;
  new-law rows carry no 業態, so snack bars, hotel restaurants and caterers
  stay in Food service, and no caterer count exists to disclose.
- **Rail:** step 1 reproduces the brief: 21 station groups (Mizushima Main
  Line 10, Sanyo 4, Seto-Ohashi 4, Ibara 3, Hakubi 1, Uno Minato 1; 倉敷 and
  茶屋町 on two lines each), the Shinkansen's 新倉敷 dropped, 14 stations
  beyond the line within 3 km listed (岡山市南区 5, 岡山市北区 1, 早島町 2,
  浅口市 2, 総社市 2, 玉野市 1, 矢掛町 1; 久々原 and 植松 fall outside, as the
  brief asked to check). Median nearest-station gap 1,523 m (the brief's):
  standard rings. One pair under 200 m, 倉敷 (JR) and 倉敷市 (Mizushima
  Rinkai), 150 m: two operators' stations, kept apart (Kobe's Tarumi
  precedent). Gate 3 exact on the Mizushima Main Line, 10 of 10.
- **One-station JR stubs drawn as cut** (standing call 3): the Hakubi Line
  (倉敷) and the Uno Minato Line (茶屋町). 本四備讃線's JR West and JR Shikoku
  records are one line, the JR Seto-Ohashi Line (the Sanyo Line's
  two-operator precedent).
- **Station names:** 37 OSM objects, 36 with `name:en`; 21 names read, none
  translated, no 丁目. Two overrides bring OSM's two macron spellings to the
  style of the other 19 and of Okayama's map: Kaminocho (Kaminochō), Nakasho
  (Nakashō). Kurashikishi and Kibinomakibi stand as OSM writes them, not
  checked against the operators' signs.
- **Line names:** Okayama's ("JR Sanyo Line", "JR Seto-Ohashi Line", "JR Uno
  Minato Line"), Fukuyama's ("Ibara Railway Ibara Line"), and two new ones:
  "JR Hakubi Line" and "Mizushima Rinkai Railway Mizushima Main Line".
- **Line colours:** the Sanyo Line `#007890` from the registry; the
  Seto-Ohashi `#00A0B8` and Uno Minato `#7098A8` are Okayama's and the Ibara
  Line `#28A800` Fukuyama's, as literals (no registry entry yet). New: the
  Mizushima Main Line `#0068B8` and the Hakubi Line `#A89078`
  (`line_colour_search.py`'s rule with the four held fixed, scratch
  `kurashiki/colours.py`; no yellow-green clears the pins by 45, so the
  Hakubi Line is tan). Against the pins (CIE76): 82.3, 75.2 (Sanyo), 77.8,
  45.1, 68.1, 45.7; none between 20 and 45. Closest pair within 500 m 19.0
  (Seto-Ohashi, Uno Minato, inherited), anywhere 15.8 (Sanyo, Seto-Ohashi,
  inherited, never near each other here); dark-mode labels 6 of 6.
- **Privacy verdict: publish.** `check_personal_exposure.py kurashiki`: the
  Japan pass prints 0 of 4,904. The name rule compares 営業者氏名 in memory
  only; the two phone columns are never handed to step 2. The PDF's text
  file holds everything the PDF does and stays in `data/kurashiki/raw/`
  (gitignored).
- **Not done:** JR West's train counts at 木見 and 上の町 (the brief's "read
  at build"; ASSERTED well above 11 a day, not read); the GSI sample (the
  brief leaves it to the owner); `check_map_view.js`, `TEXT_WIDTH`,
  `check_macro_labels.py`, drift, provenance (the lead's).
- Files: `pipeline/kurashiki/` (config, fetch_sources, three steps),
  `outputs/kurashiki/` (heatmap.html, excluded_stations.csv,
  provenance.json).

#### Parked calls

1. **自動販売形態 is not a vending form in shared code** (the brief's
   "⚠️ Shared code" item; `japan_eigyo.FORM_RULES` reads `自動販売機|自販機`).
   91 fixed old-law rows carry it; 83 pins are on the map as built (67 cafés
   and 3 restaurants in Food service, 13 milk sellers in Food shops), 30 of
   them in a ring. Recommend: add 自動販売形態 to the vending form rule
   (Minato control and every city screen first), then re-run Kurashiki's
   steps 2 and 3 and re-measure the hand-back counts. Tradeoff: until it
   lands the map shows 83 vending machines as cafés and dairy shops, which
   `excluded.md` discloses; a city-local filter in `source_rows` would hide a
   rule the next old-law list also needs.
2. **特殊形態** (Okayama Prefecture's old-law form; 101 rows, 92 of them
   area-wide already; 9 at a fixed address, 8 pins: 6 restaurants, 1 café, 1
   confectioner, all in a ring). Recommend: confirm its meaning in the
   prefecture's old 施行条例 before any rule, as the brief says; if it is
   temporary or mobile trading, a form rule drops the 8. Tradeoff: 8 pins
   that may be stalls stay on the map meanwhile.
3. **Kagawa in the "running on to" bullet.** The brief's bullet names
   Kagawa (the Seto-Ohashi Line crosses the bridge from 児島); no station of
   Kagawa is within 3 km, so `excluded_stations.csv` lists none there.
   Recommend keeping it (Aomori's Hiranai call). Tradeoff: the bullet names
   a place the list below does not.
4. **JR West's counts at 木見 and 上の町** were not read. Recommend one read
   of `timetable.jr-odekake.net` at review; tradeoff: a low-frequency
   stretch would need its bullet, though Seto-Ohashi locals are far above 11
   a day (ASSERTED).
5. **Station spellings Kurashikishi and Kibinomakibi** (OSM's, one word
   each) against the operators' signs. Recommend leaving OSM's unless a sign
   read says otherwise; tradeoff: none measured.

#### Proposals

Sentences adapted from an approved bullet of another page, none in the
japan-city template:

- "Kurashiki City publishes its lists of barbers and beauty salons under
  terms that do not allow reuse, and no list of laundries, so personal
  services are not on this map." (from Okayama's)
- "About 660 permits are registered for an area rather than an address,
  which are food trucks and stalls; they are not on this map." (from
  Aomori's)
- "The city publishes the list once a year and no closures in between, so a
  business that closed after March 2026 is still counted. The map shows an
  upper bound, and a dot means a permit on file, not a business open today."
  (from Kyoto's and Shizuoka's upper-bound bullets; it replaces the
  template's may-include-closed bullet)
- "About one dot in eight sits at a district's center." (call 145; 12.2% of
  pins)
- Notice 216's credit and processing sentence: "Source: Kurashiki City
  (倉敷市), 食品営業許可一覧, the food-business permits in force at March 31,
  2026 (page URL), CC BY 4.0. Edited and processed by this project, which
  read the list from the city's PDF, selected the storefront types, left out
  permits registered for an area rather than an address, showed a renewed
  permit and a premises with several permits once, placed each by its
  address, and counted them around stations. The list is published once a
  year and closures since its date are not shown, so it is not claimed to be
  complete or current, and it may include premises that have closed." (the
  licence read's example form, with Aomori's processing sentence)
- `excluded.md`'s sentence on the 83 vending-machine pins (it goes if parked
  call 1 lands).

#### Registry

- `jr-west-sanyo-line`: add `"kurashiki": "JS"` to `maps`.
- New entry needed, JR Seto-Ohashi Line (JR West and JR Shikoku, 本四備讃線),
  `#00A0B8`: maps `{"okayama": "JB", "kurashiki": "JB"}`.
- New entry needed, JR Uno Minato Line (JR West, 宇野線), `#7098A8`: maps
  `{"okayama": "JU", "kurashiki": "JU"}`.
- New entry needed, Ibara Railway Ibara Line (井原鉄道 井原線), `#28A800`:
  maps `{"fukuyama": "IB", "kurashiki": "IB"}`.
- Kurashiki's config holds the three as literals; swap each for
  `line_registry.colour(...)` when its entry lands.
- No entry: the JR Hakubi Line and the Mizushima Main Line are drawn by no
  other built map and by no other city of this batch.

#### Downstream

- Notice 216 (Kurashiki City, CC BY 4.0 by the page's mark): the page asks
  that the source and the fact of editing be stated wherever the edited data
  is published (「出典を明記し、編集・加工等した旨を記載して、公表してください」), so
  card face, in the short form Visuals uses for CC BY 4.0 city lists, with
  "edited"; the MLIT credits as for every Japanese card. No open terms
  question: no indemnity or reimbursement clause, no prescribed wording.

### 2026-10-11 - Kure built, the national food filings alone, food only

- **Kure built (page 267, notice 214), Kurume's and Tottori's shape (MHLW's
  open data alone, food only, the food share stated: call 185): 1,595
  storefronts (Food service 805, Food shops 790) around 13 stations on 1
  line, 58.6% of them in a ring (935: 536 and 399) on the standard rings.**
  Source: MHLW's `34202_food_business_all.csv`, 3,538 rows (許可 2,246, 届出
  1,286, 許可(廃業) 3, 届出(廃業) 3), latest permit 2026-08-28, PDL 1.0 as
  recorded. Built by a Regional-2 subagent; the brief passed 8 of 8 on
  2026-10-11.
- **Step 2, by rule (3,538 rows to 1,765 storefront rows):** 6 closed, 0 past
  term and 7 late starters (3 of them restaurants) against `TERM_AS_OF`
  2026-08-31; 41 vehicles by permit condition (`kyoka_joken`), 15 area-wide,
  1,143 with no address, 11 not a premises (一円); 550 not a storefront (228
  no rule, 145 institutional catering, 36 hostess venues, 36 vending, 30
  temporary or mobile of which 1 by 露天, 28 entertainment, 27 inside
  accommodation, 11 mail order, 9 caterers). 55 combined 業態 cells read as
  their restaurant form (call 158). 170 repeat rows shown once.
- **Against the brief's storefront rows (1,768: Food service 808, Retail
  960): 1,765 (806 and 959).** The three rows are the brief's three
  shared-code proposals, all in the foundation already and none
  re-implemented: 自動車 in 許可条件 (1 addressed restaurant), 露天 (1
  restaurant) and 未選択 (1 notification, which would have sat at the
  city-hall geocode). The brief's "not a premises 1,195" reads 1,210 here
  (41 + 15 + 1,143 + 11) because the permit-condition rule now sets 13
  vehicles and stalls aside before the form rules that used to take them
  (temporary or mobile 42 to 30), with the 自動車 and 未選択 rows. A scratch
  replay of the brief's order reproduces its figures (2,330 open addressed
  rows, 796 restaurants, 12 yatai, 562 not a storefront; the brief's list of
  555 leaves out 4 temporary rows by type and 3 vending rows by 業態).
- **The brief's restaurant figures reproduce:** 1,543 open restaurant
  permits in term (88.1% of e-Stat's 1,752), 487 with a blank address
  (31.6%), 9 一円, 26 一円 rows in all, 1,169 blank addresses in all
  (`scratchpad/kure/measure.py`). The fixed-premises measure (the brief's
  1,022 of 1,474, 69.3%; 58.3% of 1,752) was not rebuilt rule for rule: a
  scratch word list reads 1,015 of 1,465, the same 69.3%. The brief's
  figures are the ones quoted.
- **The join, and where the brief's tier table no longer describes the
  map.** Block 1,561 of 1,765 rows (88.4%; the brief 1,557 of 1,768, 88.1%).
  The brief's 207 town-chōme rows do not stay at the town's center: the
  shared `OWN_POINT_FALLBACK` (Fukuoka's call, MHLW's point for chōme-tier
  rows too) moves 177 of them, 2 小字-tier rows and 2 unplaced rows to
  MHLW's own point, and refuses it for 22 rows whose point is a default
  shared by three or more towns (the city-hall geocode among them), which
  stay at the town's center with 1 more. Unplaced 0. On the map: block 1,406
  (88.2%), MHLW's point 167 (10.5%; 134 of them on the islands), town center
  22 (1.4%, all on the islands). Within a ring: 922 block and 13 at MHLW's
  point, none at a town center. MHLW's point against the block point: median
  35 m, 95.8% within 250 m, 22 over 1 km (1,561 rows; the brief 34 m and
  96.1%). The page's placement bullet states these tiers (call 145), not
  the brief's "one in nine at its town's centroid"; see Proposals.
- **The food share (calls 125 and 185):** the page says "about three
  restaurants in five of the official count", the brief's sentence, on 1,022
  fixed, addressed permits of 1,752 (58.3%). See parked call 1 for what the
  Food service layer itself holds (806 rows, 46.0%).
- **The name rule:** the raw file holds 2 trade names that are an operator's
  own name (the brief measured 0 among storefront rows); neither is among
  the storefronts, so 0 names are withheld and 0 pins show a permit type for
  that reason. Call 205's city-wide pass matched 1 more row, not on the map.
  2 pins have a blank trade name in the filings (1 within a ring) and show
  their permit type through the renderer.
- **Factory share:** 24 of 192 菓子 / そうざい rows (12.5%) read as a factory
  or central kitchen; kept (owner, 2026-09-24). High against the built
  cities (Tottori 3.9%, Aomori 8.4%); not read further.
- **Caterers:** 9 rows left out by 業態 (仕出し), 3 of which also name a
  counter form (客席あり twice, 店頭販売 once); disclosed in What Is Excluded
  the way Fukushima's are.
- **Economic Census control (`scripts/japan_census_control.py kure`):** 805
  Food service pins against 848 establishments (2021), 0.95 per
  establishment, the brief's expected figure and below every built city
  (Tottori 1.79). The brief's reading stands and is a coverage reading:
  e-Stat's 1,752 in-force permits over 848 establishments is 2.07, the
  lowest of the cities read, the file holds 88% of permits and about three
  fixed restaurants in ten withhold their address. Not under the brief's
  0.9 trigger, and the in-force share (88.1%) has not moved, so nothing
  goes back to staging on that account.
- **Rail:** step 1 reproduces the brief: the Kure Line 13 of 28, 13 groups,
  no Shinkansen. 3 stations beyond the city line within 3 km are listed
  (小屋浦 and 水尻 in 坂町, 風早 in 東広島市). Median nearest-station gap 1,442
  m, minimum 1,170 m (the brief's): standard rings.
- **No low-frequency stretch (calls 46 and 86):** the fewest trains the
  brief read is 20 a day (安浦 toward 三原); nothing is named on the page.
- **Gate 3 has no in-city count (Aomori's and Tottori's shape):** the line
  runs on past the city line at both ends. `GATE3["lines"]` is empty.
- **Station names stand as OpenStreetMap writes them:** 20 objects, all
  with `name:en`; 13 names read (Kure-Portopia, Tenno, Karugahama, Yoshiura,
  Kawaraishi, Kure, Aki-Aga, Shin-Hiro, Hiro, Nigata, Aki-Kawajiri, Ato,
  Yasuura). No macron, no translation, no 丁目; no override, alias or tie.
- **Line name:** "JR Kure Line", as Hiroshima's map writes the same line.
- **Line colour:** `#D08000`, Hiroshima's colour for the same line (its key
  `JY`), written as a literal because `pipeline/line_registry.py` has no
  entry for the line yet. Against the pins (CIE76, step 3): 43.0 from Food
  shops olive, between 20 and 45, recorded in the config as an accepted
  trade (the colour is the line's own site-wide). One line, no pair.
- **Privacy verdict: publish.** `check_personal_exposure.py kure`: the Japan
  pass prints 0 of 1,595. The name rule compares 法人名 in memory only;
  法人番号, 法人住所 and 営業施設電話番号 are never selected.
- **Checks:** `check_no_em_dashes.py` OK, `check_no_fetch_in_steps.py` OK
  (2026-10-11). Not run, the lead's: drift, `check_all`,
  `check_provenance`, `check_scope_disclosure`. Not run at all: the opening
  view (`scripts/check_map_view.js`; the brief asks for the fit to be read
  against the station line, since the islands stretch the city south and
  east) and the Minato control (no shared code changed).
- **Overpass:** the first two tries failed on both mirrors (HTTP errors, a
  host problem); the third, after the back-off and with the lock held,
  returned 20 elements from overpass-api.de.
- Files: `pipeline/kure/` (config, fetch_sources, three steps),
  `outputs/kure/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **"About three restaurants in five" against the Food service layer.** The
   sentence (the brief's, call 185) counts restaurant PERMITS at a fixed,
   published address: 1,022 of 1,752, 58.3%. The Food service layer holds
   806 of those rows (46.0%), because the form rules class restaurant
   permits held by convenience stores as Food shops (127 rows by 業態) and
   leave out canteens, snack bars, entertainment venues, hotel
   restaurants and caterers. Recommend keeping the brief's sentence (it is
   the share the owner accepted, and Ichinomiya's and Tottori's shares count
   permits the same way). Tradeoff: "about half" is the nearer figure for
   the magenta pins a reader sees.
2. **The placement bullet (call 145).** The brief had the page say about one
   premises in nine sits at its town's centroid. As built, those rows sit at
   MHLW's own coordinates (167 pins, 10.5%) and only 22 at a town center.
   Recommend the bullet in the page block, which states both. Tradeoff: it
   is longer than Kurume's and Tottori's approved sentence ("where that
   fails, the dot sits at the ministry's own coordinates"), which could
   stand alone if the tiers are judged disclosed by What Is Excluded.
3. **MHLW's point on the islands.** 134 island pins rest on MHLW's own
   coordinates, checked only where a block point also exists (median 35 m,
   mostly mainland). None is within a ring, so no count is affected.
   Recommend accepting it (call 127c); the GSI sample
   (`scratchpad/gsi_sample.py kure`) would test it and was not run, since
   the brief does not ask for it.
4. **Gate 3 against the operator.** Recommend accepting Aomori's shape (no
   in-city count). Tradeoff: JR West's line page would confirm N02's 28
   whole-line records, but the brief names no such page.
5. **The opening view.** Not measured (above). Recommend the lead runs
   `scripts/check_map_view.js` on Kure with the batch.
6. **Mihara and Hiroshima on the page.** The "running on to" bullet names
   Saka and Higashihiroshima, the municipalities of the three stations in
   `excluded_stations.csv`; the line's ends (Kaitaichi in Kaita, and Mihara)
   are not named. Recommend leaving it as the list gives it. Tradeoff: a
   reader may know the line by its ends.

#### Proposals

Sentences adapted from an approved bullet of another page, or new:

- "Kure City publishes no list of barbers, beauty salons or laundries, so
  personal services are not on this map." (Aomori's, the city changed)
- "The ministry's list places about three restaurants in five of the
  official count: it holds permits granted since June 2021, leaves out
  vehicles and stalls, and about three fixed restaurants in ten do not
  publish their address." (the brief's proposed sentence for call 125, with
  "The ministry's list" for "MHLW's file", as the page's other bullets name
  it)
- "About three restaurants in ten in Kure chose not to publish their address
  in the national filing system and are not on this map. Where they are is
  not known." (the template's "About one restaurant in <n>", as three in
  ten: 487 of 1,543, 31.6%)
- "The rest are matched to MLIT's address reference data: about 88% reach
  their street block, and about 11%, most of them on the city's islands, sit
  at the ministry's own coordinates; 22 sit at their district's center."
  (Kakogawa's tier sentence joined to Kurume's; parked call 2)
- "One line is drawn, labeled on the map and in the legend: JR West's Kure
  Line." and "the line running on to Saka and Higashihiroshima is cut at the
  city line" are Soka's one-line forms, the names changed.
- What Is Excluded: "Street stalls at a fixed pitch (屋台, 12) count as Food
  service." (new; Fukuoka's yatai rule, which the brief applies here)

#### Registry

- **New entry needed: JR West's Kure Line** (`西日本旅客鉄道`, `呉線`), colour
  `#D08000`, `"maps": {"hiroshima": "JY", "kure": "JY"}`, name "JR Kure
  Line". Hiroshima draws its one in-city station (矢野) in that colour;
  Kure's config carries the same value as a literal with a comment to
  replace it by `line_registry.colour(...)` once the entry exists. An
  identity such as `jr-west-kure-line` fits the registry's naming.
- For the lead to weigh: Okayama's JR Tsuyama Line (`JT`) is also `#D08000`.
  The two lines never meet and the maps are not neighbours, but the registry
  will then hold one colour under two identities.
- No other city of this batch draws the Kure Line.

#### Downstream

- Notice 214 (MHLW, PDL 1.0; MLIT, PDL 1.0): as Kurume's and Tottori's
  cards. MHLW's terms ask for the 出典 line wherever the processed data is
  used and a link to the top page only, so the credit goes on the card face
  in the form Visuals already uses for the MHLW-only cities, with the MLIT
  credits as for every Japanese card. No open terms question beyond the
  recorded 免責 2)ウ point (non-commercial use).
- `jp_licence.md` is empty on purpose: MHLW's row is already in
  `docs/data_sources/japan.md` and no other publisher is used.
- Corrections for staging, from the brief (not owner questions): the master
  list's row reads 1,546 open (88.2%), 1,025 of 1,477 and "34-57 a day";
  the build confirms 1,543 (88.1%) and takes the brief's 1,022 of 1,474
  (69.3%) and 20-57.

### 2026-10-11 - Yamagata: the owner's three answers (the update list, call 182 to Cleanup, Zao Onsen)

- **"yamagata: let's add to the list of cities scheduled for updates"**
  (owner, in the Regional-2 chat): Yamagata stays built on the August 31,
  2026 list its brief measured, and the September edition the city published
  on 2026-10-10 is a scheduled update, not a rebuild now. Added to
  `docs/plan_detail/city_watch.md` ("Yamagata: the September food list")
  with a pointer in `PLAN.md`. Yamagata's parked call 1 is answered.
- **"call 182 bring to the surface for cleanup"** (owner): the config hook
  that implements call 182 is raised at the top of this file, under "For
  Cleanup", and goes in the batch report. Yamagata's parked call 3 is
  answered: Cleanup reviews it and moves it to shared code.
- **"zao onsen can be removed if buggy"** (owner): the 23 rows at 蔵王温泉
  whose 小字 addresses the shared join misses stay off the map, as built,
  and no shared-code change is owed for them; they are counted under Not
  placed in What Is Excluded. The 10 rows the point-donor match placed there
  stay: each sits at the ministry's own coordinates for the same premises,
  not at a guessed point. Yamagata's parked call 2 is answered. Nothing was
  re-run: the map already matches this answer.

### 2026-10-11 - Yamagata built, the city's food-permit list of August 31, 2026 with MHLW's notifications, food only

- **Yamagata built (page 266, notice 213), Hiroshima's page shape (food
  only) on Okazaki's mechanics (a complete city list, MHLW's notifications
  and points): 3,280 storefronts (Food service 2,264, Food shops 1,016)
  around 11 stations on 3 lines, 34.0% of them in a ring (1,114, step 3) on
  the standard rings.** Sources: Yamagata City's
  食品営業許可施設一覧（オープンデータ）, `062014_syokuhin_list_20260831.csv`,
  3,584 permits in term on 2026-08-31 (CC BY 4.0 through
  山形市オープンデータ利用規約, read 2026-10-07 by staging; clause 4 accepted
  by the owner, call 206), and MHLW's file for 06201 (5,287 rows: 1,925
  notifications read, 3,362 permits not added). Built by a Regional-2
  subagent.
- **The brief check passed 5 of 7, and the two failures are the city's
  monthly refresh.** On 2026-10-10 the city replaced the August list with
  `062014_syokuhin_list_20260930.csv` (CSV 464.4 KB by the page); the August
  URL answers 404 and the page no longer links it. The build reads the
  cached August edition, the one the brief measured and the one that pairs
  with the cached MHLW file (grants to 2026-08-31). `SOURCE_LINKS` reads the
  current link from the page on a refresh (Akita's pattern); provenance
  records the August file's sha256. The brief's two checks need the new file
  name at the refresh (parked call 1).
- **Step 2 against the brief.** City rows 3,584, MHLW notifications 1,925.
  Set aside as area-wide 238 (県内一円: 237 city rows, 235 of them
  restaurants; 1 notification), not a premises 118 (山形県内一円: 38 city
  restaurant permits; 80 notifications): the brief's 275 city rows, 273
  restaurants. No address 782 (city 267, of which 265 carry no name either
  and 222 are restaurants; MHLW 515); the city's key is in
  `ADDRESS_BY_CONSENT` because the brief read these rows as the operator's
  opt-out. 2 closed notifications; 0 past term, 0 late starters. Not a
  storefront 741 (no rule 324, vending 230, institutional catering 110,
  temporary or mobile 68, mail order 9). Storefront rows 3,628: Food service
  2,330 and city Retail 535 (both the brief's exactly), MHLW Retail 763 (the
  brief's). 130 city rows dropped for MHLW's row of the same premises
  (`SUPERSEDES`, Okazaki's and Matsuyama's direction); 191 repeat permits
  shown once (the brief counted 61 inside the city's list; the rest are
  MHLW's). 菓子 / そうざい 311 rows, 23 factory-like (7.4%), kept.
- **The join (3,628 rows):** block 3,320 (91.5%; the brief 91.7% on the
  city's rows), MHLW's own point 222 (6.1%: 96 notifications through
  `OWN_POINT_FALLBACK`, 126 city rows through `POINT_DONORS`), town-chōme
  centre 56, 小字 centre 3, unplaced 27 (0.7%, all city rows: 24 Food
  service, 3 Retail). On the map's 3,280 pins: block 92.4%, MHLW's point
  5.9% (193), town-chōme 1.6% (54), 小字 0.1% (3). MHLW's notification points
  sit a median 46 m from the block point (94.5% within 250 m; 667 rows).
- **The unplaced 27 are the brief's 蔵王温泉 rows, and shared code does not
  yet place them** (23 of 27: 上ノ台 7, 上ノ代 5, 荒敷 3, 川前 3, 清水坂, 横倉外,
  大字上宝沢外, 川原, 中森; the other 4: 壇野前 2, 大字菅沢鬼越, 大字中野楯). The
  brief's "⚠️ Shared code" item (a rule cutting 蔵王温泉 at its 小字, the ノ /
  の fold) is in `japan_register.spelling5`'s comment for 上ノ台 but those
  rows still miss. `POINT_DONORS` matches on town and trade name, so it
  placed 10 of the brief's 40 unplaced where the brief's permit match placed
  35. Nothing was patched (parked call 2). None of the 27 is near a station:
  Zaō Onsen is about 12 km from 蔵王 station.
- **Call 182 (the name rule through the permit match) is built in the
  config, on Kyoto's mechanism.** The city's file has an empty 法人名 on every
  row, so the shared rule compares nothing for it. `config.source_rows`
  reads MHLW's 法人名 in memory for the permit of the same number (digits)
  and grant date and puts only the rule's ANSWER on the city row
  (`name_is_operator`, the key `japan_register.name_is_operator` already
  reads for Kyoto's rebuilt register); no name leaves the function. Matched:
  3,000 of 3,584 city rows. Flagged: **3** (2 restaurant permits, 1
  そうざい), where the brief read 4; a looser match (digits and type, or the
  trade-name key) finds no fourth (scratch `probe3.py`). 1 of the 3 is at a
  fixed address. MHLW's own rows: 19 flagged in the whole file, 16 of them
  notifications. On the map: 3 pins show their permit type (1 city row, 2
  notifications). This is a city-local hook with no exact twin in a built
  city: a shared-code finding for review time (parked call 3).
- **No 業態 borrow.** The brief left borrowing MHLW's 業態 through the same
  permit match to the build ("if the build wants FORM_RULES on the city's
  rows"). Not built: it changes which rows count, which is a call (parked
  call 4). The city's rows are classified by permit type alone, as Aomori's
  and Kobe's.
- **The share:** 2,770 restaurant permits against e-Stat's 2,789 in force on
  2025-03-31 (99.3%, the brief's); 2,275 at a fixed address (81.6%). No
  coverage sentence on the page; the withheld rows are disclosed instead
  (one restaurant permit in twelve, 222 of 2,770).
- **Census control (`japan_census_control.py yamagata`):** 2,264 Food
  service pins against 1,215 establishments in the 2021 Economic Census,
  1.86 per establishment (the brief's estimate exactly), inside the built
  cities' 1.56 to 1.92. A list with no 業態 column counts konbini,
  supermarkets and hotels holding 飲食店営業 as Food service, each permit
  holder a pin.
- **Rail:** step 1 reproduces the brief: 13 station records, 11 groups (Ou
  6, Senzan 5, Aterazawa 2; 北山形 one group, 63 m; 羽前千歳 one group), no
  Shinkansen record in the city. 7 stations beyond the line within 3 km are
  listed (上山市 2, 天童市 2, 中山町 2, 山辺町 1); none in Sendai (the Senzan
  Line's next station is over 3 km beyond the line). Median nearest-station
  gap 2,221 m (minimum 1,344 m), as the brief: standard rings. Ring counts:
  山形 813, 北山形 124, 羽前千歳 45, 面白山高原 0.
- **Gate 3 has no in-city count (Aomori's and Fukui's shape):** no line is
  wholly inside the city and the brief names no JR East station list, so
  none was fetched. `GATE3["lines"]` is empty.
- **Frequency:** nothing at about 11 trains a day or fewer (16 to 19 weekday
  departures each way on every line, the brief's read of 2026-10-06); no
  low-frequency bullet. The seven intermediate stations stay asserted.
- **Station names:** 20 OSM objects, 19 with `name:en` (the one without,
  天童南, is outside the city). 11 names read: none translated, no numeral.
  1 override, Omoshiroyama-Kogen for OSM's Omoshiroyama-Kōgen, so the city's
  names share one style with Zao, which OSM writes without a macron
  (Okazaki's and Hiroshima's style). The other 10 stand.
- **Line names:** "JR Ou Line" (the registry's), "JR Senzan Line", "JR
  Aterazawa Line" (no other config draws the last two).
- **Line colours:** the Ou Line takes `#E07800` from
  `pipeline/line_registry.py`; the Senzan Line is `#28A800` and the
  Aterazawa Line `#0098D8` (`line_colour_search.py yamagata`, 2026-10-11).
  Against the three pins (CIE76): 53.6, 45.6 and 70.6; closest pair 94.2;
  the dark-mode labels separate, 3 of 3. None between 20 and 45.
- **Privacy verdict: publish.** `check_personal_exposure.py yamagata`: the
  Japan pass prints 0 of 3,280; 19 trade names in the raw files are an
  operator's own name; 3 pins show their permit type. 0 bare personal names
  among the city's trade names. On the map's rows 1 published name is
  damaged and shows its permit type (`map_common.glitched_name`); 0 blank.
- **The notice's credit** uses the terms' prescribed form (2(3)) with the
  catalogue title of the edition read, 令和8年8月31日時点で営業中の
  食品営業許可施設一覧, as the licence read recorded it; the title changes
  with each month's edition.
- **Overpass:** the first names query failed on both mirrors (HTTP errors);
  retried once after more than 60 s under the session lock, 20 elements.
  Every request used the project's own user-agent (`japan_fetch`, and
  `osm.OVERPASS_USER_AGENT` for one GET of the dataset page to read its
  links).
- **Not run:** the GSI sample (the brief does not ask for it), drift, the
  provenance and scope checks (the lead's). `check_no_em_dashes.py` and
  `check_no_fetch_in_steps.py` OK. The ring total by a scratch buffer reads
  1,113 (Food service 821, Food shops 292) against step 3's 1,114; the
  bucket split in `map_inconsistencies` is the scratch one.
- Files: `pipeline/yamagata/` (config, fetch_sources, steps 1 to 3),
  `outputs/yamagata/` (heatmap.html, excluded_stations.csv,
  provenance.json).

#### Parked calls

1. **Which edition: August (built) or September (live since 2026-10-10).**
   *Recommend* landing August as built: it is what the brief measured, it
   pairs with the cached MHLW file, and every figure is checked against it.
   Tradeoff: the pinned URL is dead and a fresh checkout cannot re-fetch
   that edition; the September file (and a matching MHLW download) means a
   new file name, `FOOD_AS_OF` 2026-09-30, a re-measure of every figure and
   a corrected brief-checks block.
2. **蔵王温泉's 小字 addresses (23 unplaced rows) and the permit match for
   `POINT_DONORS`.** *Recommend* a shared-code look at review time: either
   the 小字 cut for 蔵王温泉上ノ台 / 上ノ代 / 荒敷 / 川前, or a donor match on the
   permit number where both files carry it (the brief: 35 of 40 placed).
   Tradeoff: every city screen and the Minato control re-run for about 25
   restaurants in a resort 12 km from the nearest station; no ring count
   moves.
3. **Call 182's hook lives in the city's config.** `source_rows` carries the
   name rule's answer from MHLW's 法人名 through the permit match (Kyoto's
   `name_is_operator` key). *Recommend* keeping it and, if a second city
   needs it (a city list with no operator column beside MHLW's file), moving
   it into `japan_step2` as a config key. Tradeoff: one more city-local
   hook until then; without it the 3 names would show.
4. **MHLW's 業態 for the city's rows through the same match.** *Recommend*
   not borrowing (built so): Aomori's, Kobe's and Okazaki's lists also have
   no 業態 and count konbini and hotels holding a restaurant permit as Food
   service, and the census ratio (1.86) is inside the built range. Tradeoff:
   about 2,300 of the 2,770 restaurant permits could be read by form
   (konbini to Food shops, hotel and school kitchens out), which would make
   Yamagata stricter than its neighbours.
5. **Sendai in the "running on to" bullet.** The bullet names Kaminoyama,
   Tendō, Sendai, Yamanobe and Nakayama; `excluded_stations.csv` has no
   Sendai station (the Senzan Line's next one is over 3 km beyond the line).
   *Recommend* keeping Sendai (it is where the line runs on to; Aomori's
   Hiranai is the same case). Tradeoff: the bullet names a city the list
   below does not.
6. **Gate 3 against JR East.** *Recommend* accepting Aomori's shape as
   built. Tradeoff: JR East's line pages would confirm N02's 105, 18 and 11
   whole-line totals, but the brief names none, so each is a fetch to
   approve.
7. **`coverage` in `cities_fields.txt`.** Written as Okazaki's ("narrowed",
   "No Personal services; Retail thin"), the same source shape; Aomori's
   food-only entry reads "one_bucket". *Recommend* the lead pick one for the
   batch's food-only pages with MHLW's layer.

#### Proposals

Sentences no template covers, each adapted from an approved bullet:

- Page: "Yamagata City's lists of barbers, beauty salons and laundries hold
  only premises opened since April 2019, so personal services are not on
  this map." (from Aomori's proposal; the reason is call 138's)
- Page: "From Yamagata City's list of food-business permits (as of August
  31, 2026)." (the template's sentence with the registers clause removed,
  as Hiroshima's and Okazaki's)
- Page: "About 270 restaurant permits are registered for the whole
  prefecture rather than an address, which are event stalls and food
  trucks; they are not on this map." (from Aomori's whole-city bullet)
- Page: "About one restaurant in twelve in Yamagata chose not to publish its
  name and address in the city's list and is not on this map. Where they
  are is not known." (Hiroshima's sentence, "in the national filing system"
  replaced: here the city's own list withholds them)
- Page: "The Shinkansen is not drawn (Yamagata appears as a JR Ou Line
  station)." (the template's form; the Yamagata Shinkansen has no station
  record of its own in N02)
- Notice 213, completeness sentence: "The city's list leaves out the name
  and address of permits whose operators did not agree to publish them, and
  the ministry's list holds only filings whose applicants agreed to publish
  them; neither is complete." (from Okazaki's)
- Notice 213, processing sentence: Okazaki's, with "left out permits
  registered across the prefecture rather than at an address," added.
- Excluded section: "267 permits the city's list publishes without an
  address, 265 of them without a name either, because the operator did not
  agree to publication: 222 of them are restaurant permits, about one
  restaurant permit in twelve. Where they are is not known."

#### Registry

- `jr-east-ou-line`: add `"yamagata": "OU"` to `maps`.
- The JR Senzan Line (`SZ`, `#28A800`) is new to the site. Sendai, the only
  other city it serves, is not built and not in this batch (it waits on the
  city's permission), so no entry was needed for `check_line_identity`; if
  the lead wants it registered ahead of Sendai: `jr-east-senzan-line`,
  "JR Senzan Line", JR East, `#28A800`, `maps: {"yamagata": "SZ"}`. Note the
  value equals Aomori's Tsugaru Line and the Aichi Loop Line (different
  lines on maps that do not meet).
- The JR Aterazawa Line (`AT`, `#0098D8`): no other built or batch city
  draws it; no entry.

#### Downstream

- Notice 213, Yamagata City (CC BY 4.0 through the city's terms): 2(3)
  prescribes a credit line naming the work, the city and the licence for a
  modified work; it does not say where the line must sit, so caption only
  is defensible, card face not required. The title in the credit is the
  August 2026 edition's and changes at a refresh. MHLW (PDL 1.0) and MLIT
  as on every Japanese card. Open terms question: none beyond clause 4,
  accepted (call 206); the terms are re-read before each refresh (clause 1).

### 2026-10-11 - Tottori built, the national food filings alone, food only

- **Tottori built (page 265, notice 212), Kurume's and Uji's shape (MHLW's
  open data alone, food only): 2,240 storefronts (Food service 1,500, Food
  shops 740) around 13 stations on 2 lines, 50.5% of them in a ring (1,131:
  895 and 236) on the standard rings.** Source: MHLW's
  `31201_food_business_all.csv`, 4,782 rows (許可 2,845, 届出 1,932,
  許可(廃業) 5), latest permit 2026-08-26, PDL 1.0 as recorded. Built by a
  Regional-2 subagent; the brief passed 7 of 7 on 2026-10-11.
- **Step 2, by rule (4,782 rows to 2,417 storefront rows):** 644 addressed in
  another municipality (the four towns the health center also licenses: the
  shared `other_muni` rule, by address, exactly the brief's 205 + 194 + 168 +
  77), 237 area-wide, 1 closed, 0 past term and 83 late starters against
  `TERM_AS_OF` 2026-08-31, 650 with no address, 111 not a premises (市内一円
  and the like), 639 not a storefront (335 no rule, 172 vending, 117
  institutional catering, 7 temporary or mobile, 6 mail order, 2 inside
  accommodation). 177 repeat rows shown once.
- **SHARED-CODE FINDING: the area-wide rule misses Tottori's dominant
  spelling.** The health center writes the prefecture-wide address AFTER the
  city's name (鳥取県鳥取市鳥取県内 226 rows, 鳥取県鳥取市鳥取県東部 4,
  鳥取県鳥取市鳥取県 3, 鳥取県鳥取市県内 3); `permits_from_rows` tests
  `PREF_WIDE` before the city is cut, so it read none of them. Measured
  without any city-local code: area-wide 1, 225 rows with no town placed at
  MHLW's own point, 2,448 storefronts, 208 of them stalls and vehicles (201,
  1, 3 and 3 by spelling). The owner's call is made (the area-wide rows are
  not premises; the brief), so the config's `source_rows` cuts the city's
  name from those four spellings only, which leaves the address the shared
  rule was written for; the rule and its count stay shared (237). Precedent
  for an address normalised in a city's own `source_rows`: Okazaki's `_BARA`.
  An unknown spelling of the kind stops the build. See parked call 1.
- **Against the brief's storefront rows (2,491: Food service 1,557, Retail
  934): 2,417 (1,509 and 908).** The difference is call 172: 84 raw rows (50
  of them 飲食店営業) carry a 許可開始日 in September 2026, after the file's last
  day, and are set aside (83 after the earlier rules). The brief counted
  them.
- **The join:** block 2,067 of 2,417 rows (85.5%; the brief 85.1%), MHLW's
  own point 350 (349 the join put at a town-chōme center, 1 it could not
  place), unplaced 0. On the map: block 1,925 (85.9%), MHLW's point 315
  (14.1%). MHLW's point against the block point: median 39 m, 95.7% within
  250 m, 8 over 1 km (2,067 rows; the brief 39 m and 96.1%). Every one of
  the 2,240 pins is inside the N03 city line (point in polygon, measured):
  no row of the four towns reached the fallback.
- **The food share (call 181):** the page says "about 8 in 10", with the
  note that it may understate, on the brief's 1,573 restaurant permits at a
  fixed address in the city (79.0% of e-Stat's 1,990). A looser regex of
  this build's own reproduces 2,065 open restaurant permits and splits them
  1,566 city, 184 towns, 281 area-wide, 34 blank; the brief's split is the
  one quoted. See parked call 3.
- **The name rule:** the raw file holds 148 trade names that are an
  operator's own name; none is among the storefronts (they sit in
  notifications of types outside every bucket, blank addresses and the four
  towns), so 0 names are withheld and 0 pins show a permit type. The brief
  expected 16 in a bucket; not read further (names are never printed). 0
  blank names on the rendered data.
- **Factory share:** 9 of 233 菓子 / そうざい rows (3.9%) read as a factory or
  central kitchen; kept (owner, 2026-09-24). No caterer (仕出し) form among
  the pins.
- **Economic Census control (`scripts/japan_census_control.py tottori`):**
  1,500 Food service pins against 837 establishments (2021), 1.79 per
  establishment (the brief 1.85 on 1,550 premises), inside the built
  cities' 1.56-1.92.
- **Rail:** step 1 reproduces the brief: San'in Line 8 of 161, Inbi Line 6
  of 19, 鳥取 one group (0 m), 13 stations, no Shinkansen. 5 stations beyond
  the city line within 3 km are listed (東郡家, 郡家 and 河原 in 八頭町, 大岩 in
  岩美町, 泊 in 湯梨浜町). Median nearest-station gap 2,924 m, minimum 1,237 m
  (the brief's): standard rings.
- **The Inbi Line draws as ONE continuous line, not the two pieces of call
  180.** Shared step 1 draws every N02 section within 3 km of the city line
  (`DRAW_BEYOND_M`), and the 八頭町 stretch between 津ノ井 and 国英 is 6.6 km
  of track never more than 1,671 m outside the line (measured against N03),
  so all of it is drawn, with its three stations unringed and listed. The
  brief's "gap of about 10 km" does not exist under the shared rule. Left as
  the shared step draws it; see parked call 2.
- **Low frequency (calls 46 and 86):** the Inbi Line's southern four
  stations see about 12 trains a day out of 鳥取 (the brief's count from JR
  West's timetable); drawn and named on the page.
- **Gate 3 has no in-city count (Aomori's and Fukui's shape):** both lines
  run on past the city line. `GATE3["lines"]` is empty.
- **Station names:** 26 OSM objects, all with `name:en`; 13 names read. Two
  overrides in Hiroshima's style (Shimonoseki's and Kurume's precedent):
  Hogi (OSM Hōgi) and Tottori-daigaku-mae (OSM Tottoridaigaku-Mae). No
  translation, no 丁目, no tie.
- **Line names:** "JR San'in Line" (the registry's, as Matsue and
  Shimonoseki) and "JR Inbi Line" (the brief's spelling; no other map draws
  the line).
- **Line colours:** the San'in Line takes `#E80010` from
  `pipeline/line_registry.py`; the Inbi Line is `#28A800`
  (`line_colour_search.py tottori`, 2026-10-11, from a green starting hue
  that is not claimed as the operator's). Against the pins (CIE76): 51.6 and
  45.6 (45.7 at render); the pair 134.7; the dark-mode labels separate, 2 of
  2. None between 20 and 45.
- **Privacy verdict: publish.** `check_personal_exposure.py tottori`: the
  Japan pass prints 0 of 2,240. The name rule compares 法人名 in memory only;
  法人番号, 法人住所 and 営業施設電話番号 are never selected.
- **Checks:** `check_no_em_dashes.py` OK, `check_no_fetch_in_steps.py` OK
  (2026-10-11). Not run, the lead's: drift, `check_all`, `check_provenance`.
- Files: `pipeline/tottori/` (config, fetch_sources, three steps),
  `outputs/tottori/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **The area-wide rule and an address written after the city's name
   (shared code).** Recommend: in `permits_from_rows`, test `PREF_WIDE`
   again once the city's name is cut (the `repeat_city` step already strips
   a second 鳥取県 but then only tests for the city), re-run the Minato
   control and every city screen, then delete Tottori's `source_rows` hook;
   step 2 must reproduce 237 area-wide and 2,240 storefronts. Tradeoff:
   until then the rule lives half in a city config, the pattern the
   foundation was built to end; without either, 208 stalls and vehicles sit
   on the map at MHLW's point.
2. **Call 180, the Inbi Line in two pieces.** The shared step draws it
   continuous across 八頭町 (6.6 km, inside the 3 km draw margin every
   Japanese map has), with one label. Recommend keeping it as drawn and
   wording the page as Kanazawa's Ishikawa Line and Sasebo's Matsuura
   Railway do (the page block does). Tradeoff: the owner answered call 180
   on the brief's picture of a 10 km gap; a literal two-piece drawing needs
   a clip at the city line in shared code or in this city's step 3, which no
   other map has, and would end the line at the city line here while every
   other line runs 3 km past it.
3. **"About 8 in 10" against the map's own count.** The approved figure
   rests on 1,573 restaurant permits; with call 172's September starters
   out, the map's Food service rows are 1,509 (75.8% of 1,990). Recommend
   keeping "about 8 in 10" (the permits exist and next month's file starts
   them). Tradeoff: "about 3 in 4" is the nearer round figure for what is
   drawn today.
4. **Chizu on the page.** The "running on to" bullet names Iwami, Yurihama,
   Yazu and Chizu; `excluded_stations.csv` lists none in Chizu (智頭 is over
   3 km beyond the line). Recommend keeping it, as Aomori's Hiranai.
   Tradeoff: the bullet names a town the list below does not.
5. **Gate 3 against the operator.** Recommend accepting Aomori's shape (no
   in-city count). Tradeoff: JR West's line pages would confirm N02's 161
   and 19 whole-line totals, but the brief names no such page.
6. **"Inbi" or "Imbi".** The config, map and page write "JR Inbi Line", the
   brief's spelling; the lead's note wrote "Imbi". Recommend "Inbi"
   (ASSERTED as JR West's own romanization, not read from a JR page in this
   build). One string in `config.LINES` if the other is wanted.

#### Proposals

Sentences adapted from an approved bullet of another page, or new:

- "The JR Inbi Line leaves the city between Tsunoi and Kunifusa to cross
  Yazu: its track there is drawn, its three stations there have no rings."
  (from Kanazawa's Ishikawa Line bullet; stands or falls with parked call 2)
- "The JR Inbi Line is infrequent south of Yazu: about 12 trains a day run
  from Tottori to Kunifusa, Takagari, Mochigase and Inaba-Yashiro." (from
  Aomori's Tsugaru Line bullet)
- "Neither Tottori City nor Tottori Prefecture publishes a list of barbers,
  beauty salons or laundries, so personal services are not on this map."
  (from Aomori's)
- "... so it holds about 8 in 10 of the restaurant permits in the official
  count. The true share may be higher, because the official count may
  include four neighboring towns." (Mito's share clause, then call 181's
  note; new)
- "The health center also licenses those four towns (Iwami, Yazu, Wakasa
  and Chizu); their filings are left out by address." (new)
- "About 350 permits and filings are registered for the whole city or
  prefecture rather than an address, which are event stalls and food trucks;
  they are not on this map." (from Aomori's; 237 + 111 = 348)
- "About one restaurant in 60 in the health center's filings chose not to
  publish its address in the national filing system and is not on this map.
  Where they are is not known." (the template's, "in the health center's
  filings" for "in Tottori": the 34 cannot be split from the towns)

#### Registry

- `jr-west-sanin-line`: add `"tottori": "SN"` to `maps`.
- No new entry: the JR Inbi Line is drawn by no other built map and by no
  other city of this batch. Its `#28A800` is also the Aichi Loop Line's and
  Aomori's Tsugaru Line's value, on maps far from this one.

#### Downstream

- Notice 212 (MHLW, PDL 1.0; MLIT, PDL 1.0): as Kurume's and Uji's cards.
  MHLW's terms ask for the 出典 line wherever the processed data is used
  and a link to the top page only, so the credit goes on the card face in
  the form Visuals already uses for the MHLW-only cities, with the MLIT
  credits as for every Japanese card. No open terms question beyond the
  recorded 免責 2)ウ point (non-commercial use).
- `jp_licence.md` is empty on purpose: MHLW's row is already in
  `docs/data_sources/japan.md` and no other publisher is used.

### 2026-10-11 - Matsumoto built, the city's barber, beauty-salon and laundry registers of October 1, 2026, personal services only

- **Matsumoto built (page 264, notice 211), Kōchi's page shape (personal
  services only) on Hamamatsu's source shape (one standing file per trade):
  975 storefronts (barbers 165, beauty salons 695, laundries 115) around 20
  stations on 3 lines, 46.8% of them in a ring (456) on the standard rings.**
  Source: Matsumoto City's 「松本市の生活衛生施設データ」, LinkData.org work
  `rdf1s8757i`, CC BY 4.0 under the city's terms and marked CC BY 3.0 on
  LinkData (read 2026-10-07 by staging; owner's call 207). Built by a
  Regional-2 subagent.
- **The brief passed 12 of 13; the failure is a brief to correct.** The
  register work's page no longer reads 「2026年7月1日現在」: LinkData replaced
  the three tables in place on 2026-10-08 and the page now reads
  「2026年10月1日現在」 (last update Oct 8, 2026). The brief foresaw it ("a
  later edition re-measured ... the build pins the work page's date"). **The
  build reads the 2026-10-01 edition**, fetched 2026-10-11 from the three
  URLs the brief names and saved under dated names
  (`matsumoto_barber_20261001.txt`, `..._beauty_...`, `..._cleaning_...`;
  16,476, 74,822 and 17,264 B) beside the Step 0 files of the 2026-07-01
  edition, which no step reads. The brief's check string and byte counts
  need the correction.
- **What moved between the editions** (by address and trade name): barbers
  168 to 165 (3 gone, none added), beauty salons 710 to 710 (9 gone, 9
  added), laundry rows 118 to 117 (2 gone, 1 added; pick-up counters 74 to
  73). The barber table's 検査確認日 is ISO now, not an Excel serial.
- **Against e-Stat FY2024 (2025-03-31):** barbers 165 of 172 (95.9%), beauty
  salons 709 of 686 (103.4%), laundries 116 of 125 (92.8%: general 43 of 43,
  pick-up counters 73 of 82). The brief's 97.7%, 103.5% and 93.6% were the
  July edition's.
- **Step 2:** 992 rows; 1 set aside as addressed in another municipality (the
  beauty row in 長野市 the brief flagged: the foundation's `other_muni` rule
  decides it, no city-local choice); 1 not a premises (無店舗取次店); 990
  storefront rows. Join: block 940 (94.9%), town-chōme center 45, 小字 center
  3, unplaced 2 (0.2%: 波田宮ノ久保 and 蟻々崎) where the brief left 9: the
  foundation's `aza_insert` and `no_dropped` rules place the rest. 13 repeat
  rows shown once (11 premises are in both the barber and the beauty
  register by address and name).
- **No shared-code change was needed.** The brief's items (a LinkData reader,
  営業者 in `OPERATOR_COLS`, the short-大字 rule, 湯の原 / 湯原) are all in
  shared code; the config has no `source_rows` hook and no `TERM_AS_OF` (the
  registers carry no permit term).
- **Food stays off (call 133, as approved).** The ledger and MHLW's file are
  read by no step and not credited. The Economic Census control
  (`scripts/japan_census_control.py matsumoto`) has no Food service pins to
  measure: 0 against 1,400 establishments, by design.
- **Rail:** step 1 reproduces the brief: Kamikochi Line 14 of 14, Shinonoi
  Line 4 of 15, Oito Line 4 of 33, 松本 one group (116 m), 20 stations, no
  Shinkansen. 7 stations beyond the city line within 3 km are listed (安曇野市
  5, 塩尻市 1, 筑北村 1). Median nearest-station gap 950 m (the brief: 1,021
  m): standard rings either way; closest pair 417 m.
- **Gate 3 exact on the Kamikochi Line (14).** Alpico Kotsu's timetable PDF
  of 2026-03-14 (call 176: counts only) was fetched once on 2026-10-11 with
  the project's user-agent into `data/matsumoto/raw/` (137,355 B) and read
  with `pdftotext`: 14 stations, AK01 to AK14, and 25 trains a day each way,
  so the brief's "about every 40 minutes" holds (it was ASSERTED there). No
  stretch is at or under about 11 trains a day (JR's thinnest is the Oito
  Line, 24 each way, the brief's reading; not re-read).
- **Station names:** 44 OSM objects, 43 with `name:en`; all 20 names read.
  One override: 北新・松本大学前 reads "Kitanii-Matsumotodaigakumae", the
  spelling of Alpico's own timetable, where OSM translates half of it
  ("Kitanii / Matsumoto Univ."). No macron, no 丁目, no tie.
- **Line names:** "Alpico Kotsu Kamikochi Line", "JR Shinonoi Line", "JR Oito
  Line". No other config draws any of the three.
- **Line colours** (`line_colour_search.py matsumoto`, 2026-10-11): `#0090D0`,
  `#E07800` and `#9050A0`. Against the pin colours (CIE76): 71.6, 53.6 and
  47.6; closest pair of lines 51.2; the dark-mode labels separate, 3 of 3.
  None between 20 and 45. The starting hues are the project's own guesses,
  not read from the operators.
- **The opening view fits the stations, not the city's 979 km²:** the
  rendered bounds run 36.174-36.288 N, 137.822-137.970 E. Not checked in a
  browser (`check_map_view.js` is the lead's, at review time).
- **Privacy verdict: publish.** `check_personal_exposure.py matsumoto`: the
  Japan pass prints 0 of 975; 0 names withheld, 0 masked, 0 blank on the
  rendered data. 営業者 is filled on 277 of 992 rows, every one with a
  company marker; it is compared in memory only.
- **The notice's credit** follows call 207: the city's format naming CC BY
  4.0, then LinkData's CC BY 3.0 mark and the attribution name. The download
  date in it is 2026-10-11.
- Files: `pipeline/matsumoto/` (config, fetch_sources, three steps),
  `outputs/matsumoto/` (heatmap.html, excluded_stations.csv,
  provenance.json).

#### Parked calls

1. **The newer edition.** Built on the 2026-10-01 tables rather than the
   Step 0 files. Recommend keeping it: the brief names these URLs and says a
   later edition is re-measured and pinned to the work page's date, and
   Shizuoka's build re-fetched newer files the same way. Tradeoff: the
   licence read (2026-10-07) predates the page's update of 2026-10-08; the
   licence mark on the work page and in each table's header is unchanged
   (`brief_check` still finds the CC BY 3.0 link; the headers were read by
   the fetch), but the terms were not re-read.
2. **The credit's title and URL.** The city's format reads 松本市の［タイトル］,
   and the work's title is itself 「松本市の生活衛生施設データ」, so the credit
   puts the title in 「」 to keep "松本市の" from doubling; the URL is the
   LinkData work page (where the data is), not the city's open-data page.
   Recommend both as written. Tradeoff: brackets the format does not show;
   the alternative URL is `https://www.city.matsumoto.nagano.jp/soshiki/5/4172.html`.
3. **The Chuo Line's through trains.** N02 files the track as 篠ノ井線 and
   the map labels it "JR Shinonoi Line"; JR East also files 村井, 平田 and
   南松本 under 中央本線. The brief left adding the Chuo Line to the legend
   text to the build "if OSM's route relations carry it"; no route relation
   was queried (one names query only). Recommend leaving the label as built;
   tradeoff: a reader who knows the service as the Chuo Line sees only
   Shinonoi. `jr-east-chuo-line` in the registry is not used here.
4. **Alpico's PDF sits outside `fetch_sources.py`.** It is a gate 3 read, not
   a pipeline input, fetched by a scratch script, so `provenance.json` does
   not record it (sha256 7273992e...6ddfcd, 137,355 B). Recommend leaving it
   so (Kōchi's and Shizuoka's gate 3 reads are not recorded either);
   tradeoff: the file is on disk in `data/matsumoto/raw/` with no record but
   this entry.
5. **`data_sources.md` row for the timetable.** If a gate 3 read needs a
   support-source row, the lead adds it; none drafted beyond the transit
   row's mention.

#### Proposals

Sentences adapted from an approved bullet of another page, none in the
japan-city template:

- "Restaurants, cafés and shops are not on this map: the national list of
  food businesses gives an address for only about one in three of
  Matsumoto's restaurants." (Shizuoka's and Kōchi's bullet; 35.4%)
- "From Matsumoto City's registers of barbers, beauty salons and laundries,
  as of October 1, 2026." (the template's source bullet, cut to registers)
- "The registers may include premises that have closed, so a dot is a
  premises on a register, not necessarily one open today." (the template's
  closed-premises bullet with Hamamatsu's ending)
- Notice 211's LinkData sentence: "Published on LinkData.org by 松本市　DX推進本部,
  where the data is marked CC BY 3.0 (http://creativecommons.org/licenses/by/3.0/deed.ja)."
  (new; call 207 sets its content, not its words)
- Notice 211's processing sentence: "(This map modifies Matsumoto City's
  registers of barbers, beauty salons and laundries as of October 1, 2026:
  this project selected the premises with a fixed place, placed each by its
  address, and counted them around stations.) The registers may include
  premises that have closed." (from Shizuoka's)
- In What Is Excluded: "Another 48 sit at their district's center, mostly
  rural addresses in the villages the city absorbed." The "mostly" is the
  brief's reading of the July edition's misses, not re-read on this one.

#### Registry

- No `maps` addition and no new entry needed for a built neighbor: no line
  in `pipeline/line_registry.py` is the Kamikochi, Shinonoi or Oito line,
  and no other built city or city of this batch draws one of them.
- JR's Chuo Line is not drawn here (N02 files no 中央線 inside the city), so
  `jr-east-chuo-line` takes no Matsumoto entry.
- `#E07800` (JR Shinonoi Line) is the same colour Aomori's JR Ou Line takes
  from the registry; the two lines are different and their maps do not meet.
  `check_line_identity.py` is the lead's to run.

#### Downstream

- Notice 211 (Matsumoto City; CC BY 4.0 by the city's terms, CC BY 3.0 as
  marked on LinkData): the city's terms prescribe the 出典 line wherever the
  edited data is used, and CC BY requires the credit with the work, so card
  face, in the prescribed form or the short form Visuals uses for CC BY city
  lists, naming 松本市 and both licence versions; the MLIT credits as for
  every Japanese card. Open terms question: no document says which CC BY
  version prevails (call 207 answered it by naming both); the download date
  in the credit must follow any refresh.

### 2026-10-11 - Fuji built, Shizuoka Prefecture's barber, beauty-salon and laundry registers of March 31, 2026 with their monthly new premises, personal services only

- **Fuji built (page 263, notice 210), Kōchi's page shape (personal
  services only) on Shizuoka's and Ichinomiya's source shape (a full list
  plus its months, call 126) with Kakogawa's prefecture-list cut by address:
  831 storefronts (barbers 209, beauty salons 531, laundries 91) around 17
  stations on 3 lines, 49.6% of them in a ring (412) on the standard
  rings.** Source: Shizuoka Prefecture's 理容所台帳, 美容所台帳 and
  クリーニング所台帳 (datasets 11261 to 11263 on `opendata.pref.shizuoka.jp`,
  author 衛生課), the lists of 2026-03-31 and the fifteen monthly files of
  April to August 2026, CC BY 4.0 by the portal's §4 (read 2026-10-06 by
  staging; §6 accepted, call 144). Built by a Regional-2 subagent; the brief
  passed 9 of 9 on 2026-10-11.
- **Step 2 reproduces the brief's rows.** Fuji's rows by address: barbers
  211 + 1 (August), beauty salons 534 + 5 (June 3, July 1, August 1),
  laundries 93 + 0 (31 general, 61 取次所, 1 無店舗取次所). 1 not a premises
  (the storeless agent), 0 past term and 0 late starters (no file carries a
  term, so no `TERM_AS_OF`), 843 storefront rows, 5 repeat rows shown once
  (the brief's 5 premises registered as barber and beauty salon under one
  name; 17 addresses hold both registers). `config.FUJI_ROWS` pins each
  file's Fuji count, so a replaced file stops the build.
- **The join is better than the brief's.** Block 815 of 843 (96.7%; the
  brief 809, 96.0%), town-chōme center 19, 小字 center 2, unplaced 7 (0.8%;
  the brief 11): the foundation's rules (the bare 町, the spelling pairs, the
  小字 center) place 比奈町, 神谷町 and 米の宮町, the brief's proposals (b)
  and (c). On the map: block 810, town center 19, 小字 center 2. By register:
  barbers 208 / 1 / 0, beauty salons 516 / 14 / 1, laundries 86 / 4 / 1. The
  7 left: 東比奈 2 (a town in neither MLIT file) and 5 written with a 通称
  after a two-character 大字 (岩渕上町, 厚原西, 大野新町, 伝法桜ヶ丘, 大渕城山),
  the brief's proposal (a), which is not in shared code (parked call 2).
- **GSI's address search on 150 block-tier rows** (`gsi_sample.py fuji 150
  静岡県`, 1 request a second): 150 answered, median 1 m, 146 within 100 m,
  149 within 250 m, the farthest 556 m.
- **No shared-code change was needed.** クリーニング所所在地 and
  クリーニング所名称 are in `ADDR_COLS` and `NAME_COLS` already, the S era in
  `wareki_date`. City-local, each with its precedent: the months read by
  header name (`city_rows`), 該当なし rows passed over by the address cut,
  July's beauty file pinned to resource 857854 (the one the dataset page
  links; 857848 stays on disk unread), the cut by address and never by
  富士保健所 (Kakogawa's `source_rows`).
- **The pinned URLs were not re-downloaded**: all 18 files were on disk from
  Step 0 (2026-10-06). Each pinned URL is a link on its dataset page as
  fetched 2026-10-11 (three page requests, 8 s apart), and the brief check
  fetched the beauty full list by its pinned URL.
- **Facility-named and factory-named premises are kept** (the brief's item):
  4 trade names read as a hospital or welfare facility (2 barbers, 1 beauty
  salon, 1 laundry), 2 general laundries carry リネン and 4 carry 工場 in the
  name. Sapporo's welfare-facility rule reads a type column, which these
  registers lack, and Funabashi kept its 工場 names; nothing was dropped by
  name.
- **No census control ran**: `japan_census_control.py` measures Food service
  pins, and this page has none. The brief's coverage figures stand as
  staging measured them (the jurisdiction's lists hold 97.1%, 99.6% and
  93.4% of e-Stat's FY2024 counts; the census estimate for Fuji reads about
  100%, 89% and 78%); not re-measured here.
- **Rail:** step 1 reproduces the brief: Tokaido Line 4 of 89, Minobu Line 5
  of 39, Gakunan Railway Line 10 of 10; 19 platform records, 17 stations (富士
  one group, 0 m; 吉原 one group, 142 m); the Shinkansen's 新富士 dropped. 7
  stations beyond the city line within 3 km are listed (富士宮市 4, 静岡市清水区
  2, 沼津市 1). Median nearest-station gap 1,024 m (the brief's exactly):
  standard rings. No stub, no low-frequency stretch.
- **Gate 3:** exact on the Gakunan Railway Line (10), from Gakunan's weekday
  timetable as staging read it (2026-10-06); the timetable page was checked
  by the brief check, the PDF not re-read. JR is cut at the city line.
- **Station names stand as OpenStreetMap writes them:** 27 objects, all with
  `name:en`; 17 names read, none translated, no macron, no 丁目. No
  override, alias or tie. Jatco-mae and Yoshiwara-honcho keep OSM's
  lower-case common word (Kakogawa's style).
- **Line names:** "JR Tokaido Line" (the registry's), "JR Minobu Line",
  "Gakunan Railway Line" (the brief's; the operator has one line).
- **Line colours:** the Tokaido Line takes `#E86810` from
  `pipeline/line_registry.py`. `line_colour_search.py` re-chooses every line,
  so its rule was run with that colour held fixed (scratch `fuji/colours.py`,
  2026-10-11): the Minobu Line `#B070B0`, the Gakunan Railway Line `#E83810`.
  Against the pins (CIE76): 62.6, 45.3 and 53.2 at the least; lines JT/GK
  21.1 (they share 吉原), JT/MN 89.0, MN/GK 88.8; 3:1 on both basemaps; the
  dark-mode labels separate, 3 of 3. None between 20 and 45 against a pin.
  Against Shizuoka's Shizuoka-Shimizu Line (`#0068B8`): 41.1 or more.
- **The opening view** is the stations' extent (the rendered `BOUNDS`,
  35.136 to 35.205 N, 138.619 to 138.752 E), not the 245 km² N03 polygon;
  `check_map_view.js` was not run by the builder.
- **Pin names:** 0 blank; 1 beauty salon's name carries a `?` where the
  published file lost a character, and the renderer shows its register type.
- **Privacy verdict: publish.** `check_personal_exposure.py fuji`: the Japan
  pass prints 0 of 831; 0 names withheld by the name rule (the brief's 0 and
  0). The name rule compares 開設者氏名 in memory only; the phone column is
  never selected.
- Files: `pipeline/fuji/` (config, fetch_sources, three steps),
  `outputs/fuji/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **The notice's credit wording.** Staging's read records "CC BY 4.0 by the
   portal's §4, the prescribed modified-use credit" and no record quotes the
   prescribed text. The notice, the numbered item and the licence row are
   drafted in the CC BY 4.0 改変 form Shizuoka City's terms prescribe (notice
   205), with 静岡県 as the author and the three dataset pages linked.
   Recommend: confirm the wording against staging's read (or one
   `licence-read` call on the portal's terms) before the page lands.
   Tradeoff: publishing the drafted form risks a credit that is not the
   portal's own words; the builder may not read terms.
2. **A two-character 大字 followed by a 通称** (the brief's proposal (a)): 5
   of the 7 unplaced rows (岩渕上町, 厚原西, 大野新町, 伝法桜ヶ丘, 大渕城山).
   `known_town`'s prefix match needs 3 characters. Recommend: leave as built
   (0.6% of rows) unless another city shows the same shape. Tradeoff: a
   shared rule allowing 2 characters where the 地番 then hits a block would
   place about 5 here, and needs the Minato control and every city screen
   re-run.
3. **The Tokaido and Gakunan colours are 21.1 apart** (orange and
   red-orange, sharing 吉原). It clears the search's 18. Recommend: keep.
   Tradeoff: a Gakunan colour farther from orange leaves the operator's red
   hue; the Tokaido colour is the registry's and cannot move.
4. **Facility-named premises (4) kept** on Sapporo's rule reading a type,
   not a name. Recommend: keep. Tradeoff: a salon inside a hospital or care
   home may not serve the public; dropping by name is the rule the owner
   rejected for 工場 / センター.
5. **The map view and macro label** (`check_map_view.js`,
   `check_macro_labels.py`, `TEXT_WIDTH` for "Fuji") are the lead's: not run
   here.

#### Proposals

Sentences adapted from an approved bullet of another page, or new:

- "The Shinkansen is not drawn, so Shin-Fuji, which only the Shinkansen
  serves, has no ring." (the template's Shinkansen bullet, with a new clause)
- "Restaurants, cafés and shops are not on this map: the national list of
  food businesses holds an address for at most about two in three of Fuji's
  restaurants." (from Shizuoka's and Kōchi's food bullet; the figure is the
  brief's "at most 67%")
- "From Shizuoka Prefecture's registers of barbers, beauty salons and
  laundries: the complete lists as of March 31, 2026 and the new premises
  listed each month since, to August 31, 2026." and "The prefecture lists
  new premises each month but not closures, so a premises that closed after
  March is still counted. The map shows an upper bound, and a dot is a
  premises on the lists, not necessarily one open today." (Shizuoka's, with
  the prefecture as publisher)
- "No official count exists for Fuji alone. The registers list 539 beauty
  salons and 92 laundries here, about nine in ten and about four in five of
  what the 2021 Economic Census suggests. Both shares are estimates, and the
  reason for the gap is not known." (the owner's call 186, the sentence
  itself for review time)
- "Names and types are shown in Japanese, as the prefecture records them."
  (the template's, with the prefecture)
- Notice 210's processing sentence: "(This map modifies Shizuoka
  Prefecture's registers of barbers, beauty salons and laundries as of March
  31, 2026 and its monthly lists of new premises to August 2026: this
  project selected the premises in Fuji with a fixed place, placed each by
  its address, and counted them around stations.) The registers may include
  premises that have closed." (from Shizuoka's)

#### Registry

- `jr-central-tokaido-line`: add `"fuji": "JT"` to `maps`.
- No new entry needed today: the JR Minobu Line (`#B070B0`) and the Gakunan
  Railway Line (`#E83810`) are drawn by no built map and by no other city of
  this batch. The Minobu Line runs on to Fujinomiya and Kōfu (Kōfu is in
  Band R); if either is built, the line needs an entry with Fuji's colour.

#### Downstream

- Notice 210 (Shizuoka Prefecture, CC BY 4.0 by the portal's terms): CC BY
  requires the credit wherever the modified work is used, so card face, in
  the prescribed form or the short form Visuals uses for CC BY 4.0 lists;
  the MLIT credits as for every Japanese card. Open terms questions: the
  credit's exact wording (parked call 1), and §6, which the liabilities
  review found read two ways (with Cleanup).

### 2026-10-11 - Matsue built, the city's barber, beauty-salon and laundry registers of August 31, 2026, personal services only

- **Matsue built (page 262, notice 209), Kōchi's page shape (personal
  services only) on one standing list per register: 919 premises (barbers
  262, beauty salons 551, laundries 106) around 16 stations on 3 lines, 32.5%
  of them in a ring (299) on the standard rings.** Source: Matsue City's
  three registers on Shimane Prefecture's portal, resources 76779, 76780 and
  76781 as of 2026-08-31, PDL 1.0 (read 2026-10-06 by staging). Built by a
  Regional-2 subagent; the brief passed 14 of 14 on 2026-10-11.
- **Step 2 reproduces the brief's rows:** 266 barbers (267 less the mobile
  barber), 574 beauty salons (575 less the repeated header) and 108
  laundries (27 クリーニング所, 81 取次所), 948 in all. 15 repeat rows shown
  once, each a premises in both the barber and the beauty register (the
  brief's 15). 0 not a premises, 0 set aside by a shared rule.
- **The join is slightly better than the brief's:** block 776 (81.9%; the
  brief 771, 81.3%), town or 大字 center 158 (16.7%; 161), unplaced 14 (1.5%;
  16). The foundation's rules place what the brief listed as one shared rule
  each (八雲村 through `town_aliases`, the dash written for 一 before 丁目) and
  three more rows reach a block. On the map: 763 pins at a block, 156 at a
  center, 90 of those in 鹿島町 23, 八束町 19, 美保関町 18, 島根町 17 and 八雲町
  13, where MLIT keys almost no block (call 145's disclosure, on the page per
  call 183). Unplaced by register: 4 barbers, 8 beauty salons, 2 laundries.
- **GSI cross-check (`gsi_sample.py matsue 150`, block-tier rows):** 150
  answered, 0 failed; median 1 m; 143 within 100 m, 148 within 250 m, max
  1,258 m. The script samples block-tier rows only, so the brief's
  "weighted to the centroid tier" was not done.
- **Two rows are left out in `config.source_rows`, as the brief prescribes
  (city-local):** the beauty file's repeated header row, and the one mobile
  barber (an address naming a service area and a depot in another
  prefecture; the test is a prefecture other than 島根県 in the address,
  never 市内). The counts dropped are pinned in `SOURCE_ROWS_DROPPED` and the
  build stops if a later edition differs. Column selection in `source_rows`
  is Kōchi's and Shizuoka's; a row filter there is Tsu's (its prefix cut).
  Shared-code findings: (a) without the header drop the shared `idou` rule
  would count the repeated header as a mobile salon, because its address
  cell is the column's own label, which contains 移動; (b) no shared test
  reads a mobile barber's "service area and depot" address.
- **No shared-code change was needed.** The brief's three column items (the
  two long address labels, 営業者の名称又は氏名, クリーニング所又は取次所の別)
  are in shared code already. No `TERM_AS_OF`: the registers carry no permit
  term (step 2 did not ask for one).
- **Food left out** (owner, call 96): no food source is read by any step.
  No census control (no food leg).
- **Rail:** step 1 reproduces the brief: San'in Line 7 of 161, Kisuki Line 2
  of 18, Kita-Matsue Line 8 of 22, 宍道 one group (0 m), 16 stations. 5
  stations beyond the city line within 3 km are listed (一畑口, 伊野灘 and 荘原
  in 出雲市, 荒島 in 安来市, 加茂中 in 雲南市). Median nearest-station gap
  1,718 m (the brief's exactly), minimum 1,197 m: standard rings.
- **Gate 3 exact on the Kita-Matsue Line (8):** Ichibata's timetable list
  page numbers the line's stations 01 to 22 (N02 also 22), and 15 津ノ森 to
  22 松江しんじ湖温泉 are the eight inside. The operator's list does not say
  where the city line falls; that is N03's. JR has no in-city count (both
  lines run on); the brief's timetable reads stand.
- **The Kisuki Line** is drawn as cut (2 stations) and named on the page as
  infrequent with its counts (call 86): 10 trains a weekday toward Kisuki,
  11 toward Shinji (the brief's read of JR West's timetables, 2026-10-06;
  not re-read).
- **Station names stand as OpenStreetMap writes them:** 41 objects, 40 with
  `name:en`; 16 names read, none translated, no macron, no 丁目. No
  override, alias or tie. "Matsue English Garden-Mae" and
  "Matsue-Shinjiko-Onsen" keep OSM's hyphens and capitals.
- **Line names:** "JR San'in Line" (as Shimonoseki's map writes the same
  line; the brief's "San'in Main Line" not used), "JR Kisuki Line",
  "Ichibata Electric Railway Kita-Matsue Line" (the brief's).
- **Line colours** (`line_colour_search.py matsue`, 2026-10-11): San'in
  `#E80010`, Kisuki `#A05000`, Kita-Matsue `#E07800`. Against the pins
  (CIE76): 51.6, 45.2 and 53.6; closest pair within 500 m 46.3 (San'in,
  Kisuki); closest anywhere 24.4 (Kisuki, Kita-Matsue, which never meet);
  dark-mode labels 3 of 3. None between 20 and 45. The Kisuki Line's
  starting hue was moved from a yellow-orange to a dark gold after the first
  run put it 10.8 from the Kita-Matsue Line's orange.
- **The opening view** is baked from the stations' extent (35.380 to 35.481
  N, 132.909 to 133.149 E, zoom 12.25), not the N03 polygon. Not checked in
  a browser (`check_map_view.js`), and the Kisuki Line's label on its short
  stretch was not looked at: both are for the lead's render.
- **Privacy verdict: publish.** `check_personal_exposure.py matsue`: the
  Japan pass prints 0 of 919. 0 trade names flagged in the raw files by the
  name rule or the sign rule (the brief's 0). 営業者の名称又は氏名 is compared
  in memory only; 代表者の役職及び氏名, 営業者所在地, the phone and the postcode
  are never selected.
- **A request that carried the owner's email address.** One GET to
  `railway.ichibata.co.jp/operate/timetable/list/` (the gate 3 list page,
  2026-10-11) went out with a hand-typed user-agent that included the
  owner's email address. It cannot be recalled. Every other hand-made
  request (three resource pages on `shimane-opendata.jp`) used a string with
  nothing personal in it; the pipeline's fetches use the project's own.
- Files: `pipeline/matsue/` (config, fetch_sources, three steps),
  `outputs/matsue/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **Salons inside a hospital or care facility.** The brief asked for the
   facility-named rows to be read against Sapporo's welfare-facility rule.
   That rule reads a register TYPE (厚生施設理容所); Matsue's files carry no
   such type, so nothing is set aside and the rows are on the map: by trade
   name, 2 barbers and 1 beauty salon inside a hospital and 1 laundry at a
   disability-support facility (the brief counted 5; a name search finds
   these 4 clearly, with a sheltered-workshop laundry and a hospital-branch
   barber as possible others). Recommend keeping them as built. Tradeoff: up
   to about 5 pins for premises that may not be open to the public, against
   a name test, which the owner rejected for factories (real shops are
   called …センター) and which would be a new shared rule.
2. **The mobile-barber test and the header drop live in the city's config.**
   Recommend moving both to shared code at the next foundation pass (a
   repeated header row dropped by `city_rows`; an address naming another
   prefecture set aside for a register). Tradeoff: a shared change needs the
   Minato control and every city screen; the config version is pinned by a
   count check and affects Matsue alone.
3. **GSI sample weighted to the centroid tier.** The brief asked for it; the
   scratch script samples block rows only. Recommend accepting the block
   sample (median 1 m) with the tiers disclosed. Tradeoff: the 156 center
   pins' distance from their true lot stays unmeasured (it is what call 145
   discloses).
4. **Whether a closed premises leaves the monthly list** is unmeasured (one
   month read; a second month needs the owner's approval, the brief). The
   page keeps "may include premises that have closed".
5. **Kyoto's JR Sagano Line is N02's 山陰線 too** (JR West). If the registry
   treats a line a map names differently as the same line, a San'in entry
   would reach Kyoto's map (a built map: Cleanup's). Recommend an entry for
   the JR San'in Line as named (Shimonoseki, Matsue, Tottori) and a
   `NOT_SAME` or exception record for Kyoto's Sagano Line, 300 km away.
   Nothing was changed.

#### Proposals

Sentences adapted from an approved bullet of another page, or new:

- "The JR Kisuki Line is infrequent: 10 trains a weekday run toward Kisuki
  and 11 toward Shinji." (from Aomori's Tsugaru Line bullet)
- "Restaurants, cafés and shops are not on this map: Matsue City's own list
  of food businesses is not open data, and the national list holds only
  about 2% of the city's restaurants." (from Kōchi's and Shizuoka's food
  bullet; the reason is new)
- "From Matsue City's registers of barbers, beauty salons and laundries (as
  of August 31, 2026)." and "The registers may include premises that have
  closed, so a dot is a premises on the registers, not necessarily one open
  today." (the template's source and closed-premises bullets, reworded for
  registers; Kōchi's upper-bound sentence does not fit, since each month's
  list is complete)
- "MLIT's data holds almost no street blocks in the rural towns that joined
  the city in 2005 (Kashima, Shimane, Mihonoseki, Yakumo and Yatsuka), so
  the 90 premises there sit at the center of a district that can be large."
  (new; call 145's disclosure made specific. "can be large" rests on the
  brief's reading, not a measurement of this build.)
- Notice 209's processing sentence: "Processed by this project, which took
  Matsue City's registers of barbers, beauty salons and laundries as of
  August 31, 2026, showed a premises in two registers once, placed each by
  its address, and counted them around stations. The registers may include
  premises that have closed." (from Nishinomiya's)

#### Registry

- **New entry needed: JR West's San'in Line** (operator 西日本旅客鉄道, N02
  山陰線, public name "JR San'in Line"), colour `#E80010`, `maps`:
  `"shimonoseki": "JN"`, `"matsue": "SN"`, and Tottori's key when it is
  built. Shimonoseki already draws it in `#E80010`, and Matsue's own colour
  search chose the same value, so no map changes colour. Matsue's config
  holds the literal `#E80010` with a comment; switch it to
  `line_registry.colour(<id>)` when the entry exists.
- No entry for the JR Kisuki Line or the Ichibata Kita-Matsue Line: no other
  built map or city of this batch draws them.

#### Downstream

- Notice 209 (Matsue City, PDL 1.0 on Shimane's portal): PDL 1.0 asks for
  the source to be stated wherever the content is used, and that it was
  processed, so card face, in the short form Visuals uses for PDL 1.0 city
  lists (Nishinomiya's), with the MLIT credits as for every Japanese card.
  Link the portal (`shimane-opendata.jp`), never `city.matsue.lg.jp`. No
  open terms question beyond the fault-based cost clause (§3), accepted for
  Japan.

### 2026-10-11 - Kanazawa built, the city's food-permit snapshot of April 2024 kept whole, food only

- **Kanazawa built (page 259, notice 206), Hiroshima's one-bucket page on
  Toyama's complete-own-list shape with Hamamatsu's own-point fallback: 7,388
  storefronts (Food service 5,819, Food shops 1,569) around 21 stations on 3
  lines, 38.4% of them in a ring (2,837) on the standard rings.** One source:
  the city catalogue's 食品衛生関係営業許可施設一覧
  (`172014-syokuhineisei-kyokashisetsu`, cc-by with no version, read
  2026-10-05 by staging: permitted with conditions, clause 5 accepted), the
  Step 0 file as cached (8,842 rows, 2,756,283 B). Built by a Regional-2
  subagent; the brief passed 13 of 13 (`brief_check.py kanazawa`, 2026-10-11),
  so the record's 2024-07-16 date and 8,842 rows stand: no new edition.
- **The snapshot is kept whole and pinned to 2024-04-01** (owner's calls 36
  to 38, 2026-10-05): `FOOD_AS_OF` and `TERM_AS_OF` are the newest 許可年月日.
  Measured at the build: all 8,842 grant, start and expiry dates read; none
  starts after the as-of, none ends before it (earliest expiry 2024-04-15),
  so calls 161 and 172 drop 0. By 2026-10-11, 3,360 of the 7,844 storefront
  rows (42.8%) had passed their 許可満了日 (Food service 2,395 of 5,839,
  Retail 965 of 2,005), and 2,713 of the 6,478 restaurant permits (41.9%):
  the brief's figures exactly.
- **Step 2 against the brief.** Storefront rows 7,844 (Food service 5,839,
  Retail 2,005), as the brief. The 998 rows out are the brief's 998, split
  differently by the foundation's rules: 350 area-wide addresses (一円, 市内),
  1 city name alone and 42 not a premises (the brief: 323 not a premises), and
  605 out by rule (the brief: 675; 70 of its 73 temporary or mobile rows are
  now set aside by address): no rule 439, inside accommodation 75, vending
  56, event catering 32, temporary 3. The 業態 column holds one form a row,
  so no caterer also names a counter form (call 158 changed 0 cells). 455
  repeat rows dropped. 菓子 / そうざい pins 1,225, factory-like 54 (4.4%),
  kept.
- **The join: block 7,218 (92.0%; the brief 91.8%), the city's own point 624
  (444 from the town-chōme tier, 114 from the foundation's 小字 tier, 66 from
  no match), 1 at a town centre, 1 unplaced** (下本多町, an address MLIT does
  not hold). `OWN_POINT_FALLBACK = {"food"}` on Hamamatsu's and Fukuyama's
  precedent; the datum guard passes (block-tier rows a median 33 m from
  MLIT's point, 96.6% within 250 m, 93 over 1 km). `shared_points` found 7
  default points and refused 2 rows on them (the brief expected 7 refused
  rows: the foundation's rules placed the other 5 at the block), so the two
  rows are the town-centre one and the unplaced one. 7,388 pins against the
  brief's 7,389 (the unplaced row). 4 pins at the city's own point lie 1 to
  28 m outside the N03 city line (the census control's "2 outside every
  ward" are the Food service two); they are inside `CITY_BBOX` and kept.
- **`config.source_rows` keeps the premises and name-rule columns only**
  (Shizuoka's precedent), so 営業所電話番号, 営業所名称カナ, 備考 and 画像 never
  reach step 2; the licence read says 画像 is never read (it is empty on all
  8,842 rows).
- **`OFFICIAL_SHARES = True`** (the brief lists it): step 2 writes
  `outputs/kanazawa/official_shares.json`, 6,478 of 6,438, 100.6%, against
  e-Stat's FY2024 count (2025-03-31), a year after the snapshot. The
  like-for-like count is FY2023's 6,420 (100.9%), which the shared reader
  does not hold; the page states neither share.
- **Census control (`japan_census_control.py kanazawa`): 5,817 Food service
  pins against 2,664 establishments, 2.18**, above the built cities' 1.56 to
  1.92 and equal to the brief's prediction. The list is not over-counting:
  the official permit stock itself is 2.41 per establishment (6,420 over
  2,664), and the snapshot reproduces it at 100.9%. Kanazawa licenses bars,
  snack bars and small counters as restaurants (飲食店営業（４） alone is 957
  pins) that the census counts under other industries or not at all, and R3
  keeps them in Food service (Akita's 2.13 has the same cause).
- **Rail:** step 1 reproduces the brief: Asanogawa 10 of 12, Ishikawa 7 of
  17 in two runs, IR Ishikawa 4 of 19; gate 3 exact on all three (the
  operators' pages, re-read by `brief_check.py` 2026-10-11); 15 stations
  beyond the city line listed (白山市 8, 野々市市 4, 内灘町 2, 津幡町 1); the
  Shinkansen's 金沢 dropped by the shared step. Two close pairs kept apart
  (北鉄金沢 / 金沢 135 m, 新西金沢 / 西金沢 140 m; trap 1). `mode` metro by the
  owner's rule (no JR station inside).
- **Frequency, read at the build from the timetable PDFs the brief names
  (fetched to the scratchpad from the operators' hosts, 2026-10-11):**
  Hokutetsu's weekday PDFs dated 2026-04-29 list 36 trains each way on the
  Asanogawa Line (trains 102 to 172) and 27 on the Ishikawa Line (402 to
  454), a little under the station pages' 37 and 29. IR Ishikawa's
  `20260314kanazawa1.pdf` and `kanazawa2.pdf` are connection tables to the
  Shinkansen, not departure lists: IR's frequency stays ASSERTED (the former
  JR Hokuriku Main Line, several trains an hour). Nothing is near 11 trains
  a day, so no stretch is named as low-frequency.
- **Station names (a judgment call, on precedent):** OSM gave all 21 (39
  objects, all with `name:en`). Four overrides bring them to one hyphenated
  style: Hokutetsu-Kanazawa (OSM "Hokutetsu Kanazawa"; the operator's own
  timetable writes the hyphen; Gifu's Meitetsu-Gifu), Nishi-Kanazawa (OSM
  "Nishi Kanazawa"; IR Ishikawa's form, beside OSM's own Higashi-Kanazawa),
  Shin-Nishi-Kanazawa (OSM "Shin Nishi Kanazawa") and Nukajutaku-mae (OSM
  "Nukajutakumae"; Hokutetsu's timetable writes Nukajūtaku-mae). Hokutetsu's
  timetable writes "Shin-nishikanazawa"; the map keeps the form that matches
  Nishi-Kanazawa 140 m away. OSM's Nishi-izumi, Shijima, Kagatsume and
  Waridashi stand. No translated name, no numeral before 丁目.
- **Line names and colours:** "Hokutetsu Asanogawa Line", "Hokutetsu
  Ishikawa Line" (the Hokuriku Railroad's own short name, as Toyama's
  "Chitetsu") and "IR Ishikawa Railway Line" (Toyama's "Ainokaze Toyama
  Railway Line"). No other map draws any of the three and no city of this
  batch is in Ishikawa, so none is in `pipeline/line_registry.py`. Colours
  from `line_colour_search.py kanazawa` (2026-10-11): `#E07800`, `#E86800`,
  `#0098E0`; against the pins 53.6, 63.7 and 75.4 (CIE76; none between 20
  and 45). The two Hokutetsu oranges are 11.3 apart: they never come within
  500 m, the search's city-wide floor is 10 (Toyama's Main and Kamidaki
  lines, 10.2).
- **The credit's title** (the brief left it to the build): the dataset
  page's heading, 「食品衛生関係営業許可施設一覧」, not `package_show`'s
  「金沢市 食品衛生関係営業許可施設一覧」: it is what a reader following the URL
  sees, and the form names 金沢市 next to it. The form is the licence read's,
  as recorded, with no 出典： prefix; the terms were not re-read at the build.
- **Privacy verdict: publish.** `check_personal_exposure.py kanazawa`: the
  Japan pass prints 0 of 7,388; 5 trade names are withheld and 5 pins show
  their permit type (the brief's 3 flagged rows plus version 2's bare
  personal names). The name rule compares 法人名 in memory only. No operator
  name was printed, stored or quoted by the build.
- **Checks:** `check_no_em_dashes.py` OK; `check_no_fetch_in_steps.py` OK.
  Not run by the subagent: `drift_check.py`, `check_all.py`,
  `check_provenance.py`.
- Files: `pipeline/kanazawa/` (config, fetch_sources, steps 1 to 3),
  `outputs/kanazawa/` (heatmap.html, excluded_stations.csv, provenance.json,
  official_shares.json), `data/kanazawa/raw/osm_station_names.json`.

#### Parked calls (Kanazawa)

- **Rings: the median nearest-station gap is 561 m, inside the 540 to 570 m
  band.** Built on the standard rings (38.4% in a ring). Recommendation:
  standard, on call 213 (Gifu, 545 m, standard: every JR and private-rail
  Japanese city is on them) and because 561 m is above the rule's 550 m.
  Tradeoff: Hokutetsu's stations are close (the Asanogawa Line's ten span
  about 5 km), so their 0.6 mi rings merge along each line; halved rings
  would separate them and roughly halve the in-ring share.
- **`OFFICIAL_SHARES` writes a share the page does not state.** The brief
  lists the switch; the shared reader compares the 2024 snapshot with the
  FY2024 count (100.6%), not FY2023's like-for-like 6,420 (100.9%).
  Recommendation: keep the file as a drift-checked measurement and state no
  share on the page. Tradeoff: switching it off loses the baseline line that
  would flag a changed file.
- **IR Ishikawa's frequency is not measured.** The PDF the brief names is a
  connection table. Recommendation: leave it; no floor applies and the line
  is the former JR main line. Tradeoff: one more fetch (a station timetable
  PDF the brief does not name) would turn ASSERTED into MEASURED.

#### Proposals (Kanazawa)

Sentences no template covers, for review time:

- Page, The lines: "The Hokutetsu Ishikawa Line leaves the city between
  Shin-Nishi-Kanazawa and Magae to cross Nonoichi: its track there is drawn,
  its three stations there have no rings."
- Page, The businesses: "Kanazawa City's lists of barbers, beauty salons and
  laundries are not open data, so personal services are not on this map."
  (Hiroshima's sentence with Kanazawa's reason.)
- Page, The businesses: "From Kanazawa City's list of food-business permits
  (as of April 2024). The city has not updated its open list since." (the
  template's source sentence plus one.)
- Page, The businesses (the owner sent it to review time, 2026-10-05): "About
  four in ten of these permits have reached their expiry date since April
  2024; renewals are not in the list." (42.8% on 2026-10-11.)
- Page, Reading the map: "Each address is matched to MLIT's address reference
  data, which places most at their street block; where only the district can
  be found, the dot sits at the city's own coordinates for the premises."
  (Hamamatsu's sentence without "The registers give an address but no
  location", which is not true of a list with coordinates on every row.)
- Notice 206: "Processed by this project, which selected the storefront
  types, left out permits registered for the whole city rather than an
  address, showed a premises with several permits once, placed each by its
  address or the city's own coordinates, and counted them around stations.
  The list is a snapshot of the permits in term in April 2024: it is not
  claimed to be complete, accurate or current, and it may include premises
  that have closed."
- What Is Excluded, Counted: "It has not been updated since: 3,360 of the
  7,844 rows on this map's layers (43%) had reached their expiry date by
  October 2026, and renewals are not in the list, so a premises that renewed
  and one that closed look the same."

#### Registry (Kanazawa)

- No `line_registry` change: none of the three lines is drawn by another
  map, built or in this batch. If Hakusan, Nonoichi or a Toyama-side city is
  ever built, the IR Ishikawa Railway Line (`#0098E0`) and the Hokutetsu
  Ishikawa Line (`#E86800`) would need entries.
- `app/components.py`'s `_OSM_STATION_NAMES` needs "Kanazawa" (English
  station names from OSM), as Shizuoka's.

#### Shared-code findings (Kanazawa)

- None blocking. `scripts/screen_japan_join.py` has no Kanazawa entry (the
  brief asks for one at the build); it is a shared file, so not added.
- The brief's `japan.CITIES` line carries `"rules": WAVE2_RULES` and its
  region "Japan East"; both predate the foundation and the retag (the entry
  and the scaffold are already right).
- The master list's Kanazawa row still reads "5,412 restaurants, 84%"; the
  build confirms 6,478 and 100.9% (staging's edit).

#### Downstream (Kanazawa)

- Notice 206, Kanazawa City: the terms' 2(2) asks for the name, the source,
  the URL and that it was processed wherever the data is used, so a card
  that shows the map carries the credit; the licence read records no
  face-or-caption rule. Recommendation: caption, as the other cc-by Japanese
  cities' cards. Open terms question: none recorded (clause 5 accepted).
- MLIT (位置参照情報, N02): as every Japanese card.
- The map is a 2024 snapshot: any card or count for Kanazawa should carry
  "as of April 2024".

### 2026-10-11 - Okazaki built, the city's food-permit list with MHLW's notifications, food only

- **Okazaki built (page 260, notice 207), Hiroshima's page shape (food only)
  on Ichinomiya's mechanics (a city list, MHLW's notifications and points):
  3,614 storefronts (Food service 2,711, Food shops 903) around 16 stations
  on 3 lines, 50.5% of them in a ring (1,825: Food service 1,456, Food shops
  369) on the standard rings.** Sources: Okazaki City's
  食品等営業許可・届出一覧 on BODIK (organization 232025; CC BY 4.0 under the
  city's terms, read 2026-10-07 by staging, clause 5(5) accepted by the
  owner, call 214), 4,022 rows in term on 2026-08-31, and MHLW's file for
  23202 (799 rows: 673 notifications, 126 permits). Built by a Regional-2
  subagent; the brief passed 6 of 6.
- **The brief's two hooks, one already shared.** The brief asks for
  Hiroshima's hook carrying 許可条件 into 業態 to take the 210 kitchen cars
  out. The foundation's `kyoka_joken` rule already reads 自動車 in 許可条件
  (step 2: "set aside, vehicle (permit condition): 210"), so no hook was
  written. O1 (大字 + 小字 + 丁目) is the shared `koaza_chome` rule. O2 is
  city-local as the brief says: `config.source_rows` reads U+B743 as ばら in
  戸崎町字<U+B743>山 only (20 addresses; every city row at ばら山, 24, now reaches a block,
  where the brief counted 17 of the 20 at the district tier and 3 unplaced). Precedent
  for a cell rewritten in a city's own `source_rows`: Gifu's term dates.
  The brief's "2 trade names" with the code point were not found in 施設名称
  (0 of 4,022); none is on the map.
- **Step 2 against the brief.** Rows 4,022 and 673. Set aside: 210 vehicles,
  1 area-wide address, 2 not a premises, 29 permits starting 2026-09-01
  (call 172: 21 restaurants, 4 菓子, 2 食肉販売, 2 魚介類販売), 324 MHLW
  notifications with no address. Not a storefront 274 (no rule 151, vending
  105, institutional catering 10, temporary or mobile 6, mail order 2).
  Storefront rows 3,855: Food service 2,794 (the brief's 2,815 less the 21
  late restaurants), Retail 1,061 (the brief's 819 less 8 late, plus 250
  MHLW notifications). 38 city rows dropped for MHLW's row of the same
  premises; 164 repeat permits shown once. 0 names withheld. 菓子 / そうざい
  539 rows, 19 factory-like (3.5%), kept.
- **The join (3,855 rows):** block 3,562 (92.4%; the brief 92.7% on the
  city's rows alone), 小字 centre 127 (3.3%), town-chōme centre 84 (2.2%),
  MHLW's own point 43 (1.1%: 30 MHLW rows, 13 city rows through
  `POINT_DONORS`), unplaced 39 (1.0%). The brief's as-is 87.1% is not where
  the build ended, so call 145's tier disclosure is met by the excluded
  section's Not placed paragraph rather than a page bullet.
- **Call 178 (舞木町字金森) applied:** 51 pins at the site (46 city, 5 MHLW;
  40 restaurants): 36 at the 小字's centre (the foundation's
  `koaza_centroid`, finer than the town centre the brief expected) and 15 at
  MHLW's point; all 51 lie 756 to 797 m from 名電山中, inside its outer ring.
- **Call 179 (the new towns south of JR 岡崎) applied:** 32 city rows at
  針崎西 16, 岡崎駅前 11, 若松西 4 and 柱西 1, and 3 at two 土地区画整理 areas,
  stay unplaced (35 of the 39); 8 rows there take MHLW's point (7 MHLW, 1
  city). The other 4 unplaced: 鹿勝川町地内 2 and 久右ヱ門町 2.
- **The share (call 125, Ichinomiya's precedent):** 3,023 restaurant permits
  of e-Stat's 3,755 in force (80.5%, `japan_official.restaurants`), stated on
  the page as about four in five.
- **Census control (`japan_census_control.py okazaki`):** 2,711 Food service
  pins against 1,257 establishments in the 2021 Economic Census, 2.16 per
  establishment (the brief estimated 2.10; Akita 2.11, Aomori 2.33). High
  because the list has no 業態 column: convenience stores (174 by trade-name
  word in the brief), supermarkets (100), hotels and food-court counters
  holding 飲食店営業 stay in Food service, each permit holder a pin, and the
  restaurant stock grew from 3,466 to 3,755 between FY2021 and FY2024.
- **Rail:** step 1 reproduces the brief: 17 station records, 16 groups
  (Meitetsu 9, Aichi Loop 6, JR 2; 岡崎 one group), 9 stations beyond the line
  listed (Toyota 4, Anjō 2, Toyokawa 2, Kōta 1). Median nearest-station gap
  1,741 m, as the brief: standard rings. 中岡崎 and 岡崎公園前 168 m apart,
  kept apart. Gate 3 exact on Meitetsu's 9 (its Nagoya Main Line station
  list, 名電長沢 / 本宿 ... 宇頭 / 新安城) and the Aichi Loop's 6 (its station
  index), both read 2026-10-11 by plain GET. JR Central's timetable was not
  read: JR's 2 are not gated and its frequency stays as the brief asserted.
- **Station names:** 3 overrides in Hiroshima's style (Okazaki-koen-mae for
  OSM's Okazakikōen-mae, Uto for Utō, Meiden-Yamanaka for Meiden Yamanaka,
  Toyota's Mikawa-Yatsuhashi precedent); OSM's other 13 stand, Kitanomasuzuka
  among them (the operator's own sign was not read).
- **Line colours:** Meitetsu's Nagoya Main Line `#E80010` and JR's Tokaido
  Line `#E86810` from `line_registry`; the Aichi Loop Line `#28A800`,
  Toyota's value, repeated as a literal because the registry has no entry.
  Against the pins (step 3): 51.6, 62.6 and 45.7, all over 45. Between
  lines: 31.4 (Main, Tokaido), 105.3 and 134.7.
- **Privacy verdict: publish.** `check_personal_exposure.py okazaki`: the
  Japan pass prints 0 of 3,614; 2 trade names in the raw files are an
  operator's own name (MHLW's file, by the brief) and neither is on the map;
  no pin shows its permit type. Blank or damaged pin names on the rendered
  map: 0.
- **Not run:** the GSI sample (the brief does not ask for it), drift, the
  provenance and scope checks (the lead's). `check_no_em_dashes.py` and
  `check_no_fetch_in_steps.py` OK.
- **One request went out with the wrong user-agent.** The `package_show`
  call for the dataset id (2026-10-11, under the BODIK lock, 20 s held)
  carried a hand-typed user-agent that included the owner's email address
  instead of the project's own string. Nothing else was sent; later requests
  used `osm.OVERPASS_USER_AGENT`.
- Files: `pipeline/okazaki/` (config, fetch_sources, steps 1 to 3),
  `outputs/okazaki/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **The registry has no Aichi Loop Line.** Toyota draws it (`AK`,
   `#28A800`) and Okazaki now does. *Recommend* a registry entry
   `aichi-loop-railway-aichi-loop-line` at `#28A800` with `maps: {"toyota":
   "AK", "okazaki": "AK"}`, and both configs reading it. Tradeoff: none for
   the maps (same colour); until then `check_line_identity.py` may flag the
   literal.
2. **U+B743 as a `gaiji` entry instead of the city-local rewrite.**
   `japan.CITIES["okazaki"]["gaiji"] = {0xB743: "ばら"}` would do the same
   through shared code and reach trade names too. *Recommend* leaving the
   city-local rewrite (address only, as the brief decided); tradeoff: one
   more `source_rows` normalisation outside the shared reader.
3. **久右ヱ門町 / 久右ｪ門町 (2 rows unplaced) and 宮石町字六ﾂ田 (17 rows at the
   district tier):** half-width and old kana the shared join does not fold
   for this town. *Recommend* a shared-code look at review time (a
   half-width kana fold); tradeoff: every city screen re-run for 19 rows.
4. **JR Central's frequency is still asserted.** The brief asks for a read
   at build; it needs the station index and PDFs the brief does not name.
   *Recommend* accepting it unread: the Tokaido main line here is nowhere
   near 11 trains a day. Tradeoff: one figure in the record rests on common
   knowledge.
5. **Kitanomasuzuka** stands as OSM writes it; the Aichi Loop Railway's own
   sign may hyphenate it. *Recommend* reading the operator's English station
   page at review time; tradeoff: a possible one-name override and re-render.

#### Proposals

- Page, source bullet: "From Okazaki City's list of food-business permits
  (as of August 31, 2026)." (the template's sentence with the registers
  clause removed, as Hiroshima's)
- Page, coverage bullet: "The city's list holds about four restaurant
  permits in five of the official count, and kitchen cars, which it lists at
  a base address, are left out."
- Notice, completeness sentence: "The city's list holds about four
  restaurant permits in five of the official count, and the ministry's list
  holds only filings whose applicants agreed to publish them; neither is
  complete."
- Excluded section: "Restaurants the city's list does not hold: it has 3,023
  restaurant permits, against 3,755 in the national count a year earlier
  (about four in five). The city does not say why."

#### Registry

- `meitetsu-nagoya-main-line`: add `"okazaki": "NH"` to `maps`.
- `jr-central-tokaido-line`: add `"okazaki": "TK"` to `maps`.
- New entry needed (parked call 1): the Aichi Loop Line, `#28A800`, `maps`
  `{"toyota": "AK", "okazaki": "AK"}`. No other line of this batch's cities
  was checked against it.

#### Downstream

- Notice 207, Okazaki City: the terms' form (4(2)) is a credit line naming
  the work, the city and the licence; it does not say where it must sit, so
  caption only is defensible, card face not required. MHLW (PDL 1.0) and
  MLIT as on every Japanese card. Open terms question: none beyond clause
  5(5), accepted (call 214).

### 2026-10-11 - Aomori built, the city's food-permit list of August 31, 2026, food only

- **Aomori built (page 261, notice 208), Hiroshima's page shape (food only)
  on Akita's source shape (one standing list, nothing rebuilt): 3,528
  storefronts (Food service 2,891, Food shops 637) around 18 stations on 3
  lines, 34.9% of them in a ring (1,231: 964 and 267) on the standard
  rings.** Source: Aomori City's 食品営業許可施設一覧（オープンデータ）,
  `r0808zendate.csv`, 5,289 permits in term on 2026-08-31, CC BY 4.0 through
  青森市オープンデータ利用規約 (read 2026-10-07 by staging). Built by a
  Regional-2 subagent; the brief passed 8 of 8 on 2026-10-11.
- **Step 2 reproduces the brief.** 1,284 rows set aside as area-wide (青森市全域:
  1,271 restaurant permits, 12 fishmongers, 1 confectioner; the foundation's
  rule, not re-implemented), 9 not a premises (青森県内一円), 301 out by "no
  rule" (manufacturing), 0 past term and 0 late starters against
  `TERM_AS_OF` 2026-08-31. Storefront rows 3,695 (Food service 2,946, Retail
  749, the brief's exactly). 164 repeat rows shown once.
- **The join is better than the brief's on unplaced rows.** Block 3,515
  (95.1%, the brief's), 小字 center 121 (3.3%), town-chōme center 56 (1.5%),
  unplaced 3 (0.1%, all restaurants) where the brief left 29: the
  foundation's 大字 and 小字 rules place the 浪岡大字…字… rows the brief read
  as misses. The 3 left: two in 浪岡 and 卸町6丁目.
- **No shared-code change was needed.** The brief's four items (施設の所在地１,
  施設の名称、屋号, 営業許可業種, 全域) are all in shared code already; the
  config has no `source_rows` hook.
- **MHLW stays a control (the brief's open call 1, built on its
  recommendation):** read by no step, not credited; 119 of its 120 permits
  are in the city's list. Gifu's and Toyama's precedent.
- **The name rule flags 3 trade names in the raw file and 1 pin shows its
  permit type**, where the brief measured 0. Not read further (the names are
  never printed); the brief's measure predates the foundation's switches.
  0 blank names on the rendered data.
- **Factory share:** 37 of 439 菓子 / そうざい premises (8.4%) read as a
  factory or central kitchen; kept (owner, 2026-09-24).
- **Economic Census control (`scripts/japan_census_control.py aomori`):**
  2,891 Food service pins against 1,235 establishments (2021), 2.34 per
  establishment (the brief estimated 2.33), above the built range of
  1.56-1.92 and at Toyonaka's and Hirakata's level. The brief's reading
  stands: the list has no 業態 column, so konbini (133 by trade-name word),
  supermarkets (45), kitchens (75) and hotels (71) holding 飲食店営業 count
  as Food service, and 83 addresses hold five or more restaurant permits
  (本町's bar buildings); about 2.07 without them (the brief's estimate, not
  re-measured). Closures the city was not told of stay in the list.
- **Rail:** step 1 reproduces the brief: Ou Line 6 of 105, Tsugaru Line 7 of
  18, Aoimori Railway Line 7 of 27, 青森 one group (0 m), 18 stations, the
  Shinkansen's 新青森 dropped. 2 stations beyond the city line within 3 km
  are listed (蓬田 in 蓬田村, 北常盤 in 藤崎町). Median nearest-station gap
  1,819 m (the brief: 1,844 m): standard rings either way.
- **Gate 3 has no in-city count (Fukui's shape):** no line is wholly inside
  the city and neither operator's station list is named in the brief, so
  none was fetched. `GATE3["lines"]` is empty.
- **Station names stand as OpenStreetMap writes them:** 31 objects, all with
  `name:en`; 18 names read, none translated, no macron, no 丁目. No
  override, alias or tie.
- **Line names:** "JR Ou Line" (the registry's), "JR Tsugaru Line", "Aoimori
  Railway Line" (the operator's own name for its one line).
- **Line colours:** the Ou Line takes `#E07800` from
  `pipeline/line_registry.py`; the Tsugaru Line is `#28A800` and the Aoimori
  Railway Line `#0098E0` (`line_colour_search.py aomori`, 2026-10-11).
  Against the pins (CIE76): 53.6, 45.6 and 75.4; closest pair 94.2; the
  dark-mode labels separate, 3 of 3. None between 20 and 45.
- **Privacy verdict: publish.** `check_personal_exposure.py aomori`: the
  Japan pass prints 0 of 3,528. The name rule compares 申請者氏名 and
  代表者氏名 in memory only; the applicant's address columns and the phone
  column are never selected.
- **The notice's credit** uses the terms' prescribed form (3(2)) with the
  dataset page's own title, 食品営業許可施設一覧（オープンデータ） (a judgment
  call the licence read left to the build: the page whose URL the credit
  carries names itself so; the portal's 青森市における食品営業許可施設一覧 is
  the alternative).
- Files: `pipeline/aomori/` (config, fetch_sources, three steps),
  `outputs/aomori/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **Gate 3 against the operators.** Recommend: accept Fukui's shape (no
   in-city count) as built. Tradeoff: a read of JR East's line pages and the
   Aoimori Railway's station list would confirm N02's 18 and 27 whole-line
   totals, but the brief names neither page, so each is a fetch to approve.
2. **MHLW beside the list (the brief's open call 1).** Built control-only,
   the brief's recommendation. Tradeoff: the Food shops layer is permits
   only; adding MHLW's 454 notifications (248 addressed) would add a thin
   partial layer and MHLW's credit to the notice.
3. **Hiranai on the page.** The "running on to" bullet names Yomogita,
   Fujisaki and Hiranai; `excluded_stations.csv` lists only the first two
   (the Aoimori Railway's next station, in 平内町, is over 3 km beyond the
   line). Recommend keeping Hiranai (it is where the line runs on to);
   tradeoff: the bullet names a town the list below does not.
4. **The credit's title** (above): recommend the dataset page's title.

#### Proposals

Sentences adapted from an approved bullet of another page, none in the
japan-city template:

- "The JR Tsugaru Line is infrequent: 9 trains a weekday run toward Kanita
  and 8 toward Aomori." (from Akita's Uetsu Line bullet)
- "Aomori City publishes no list of barbers, beauty salons or laundries, so
  personal services are not on this map." (from Akita's laundries bullet and
  Hiroshima's)
- "About 1,300 permits are registered for the whole city rather than an
  address, which are event stalls and food trucks; they are not on this
  map." (new)
- Notice 208's processing sentence: "(This map modifies Aomori City's list
  of food-business permits as of August 31, 2026: this project selected the
  storefront types, left out permits registered for the whole city rather
  than an address, showed a premises with several permits once, placed each
  by its address, and counted them around stations.) The list is not claimed
  to be complete or current, and it may include premises that have closed."
  (from Gifu's)

#### Registry

- `jr-east-ou-line`: add `"aomori": "OU"` to `maps`.
- No new entry: the JR Tsugaru Line and the Aoimori Railway Line are drawn
  by no other built map and by no other city of this batch.

#### Downstream

- Notice 208 (Aomori City, CC BY 4.0 through the city's terms): the terms
  prescribe a credit wherever the modified work is used, so card face, in
  the prescribed form or the short form Visuals uses for CC BY 4.0 city
  lists; the MLIT credits as for every Japanese card. Open terms question:
  clause 6's bar on acts that "harm or defame the city or others" is
  undefined (raised the way Taoyuan's was); nothing in the map engages it.

### 2026-10-11 - Shizuoka built, the city's barber, beauty-salon and laundry registers with their monthly new permits, personal services only

- **Shizuoka built (page 258, notice 205), Kōchi's shape (full lists plus
  monthly openings) on Hamamatsu's three-ward precedent: 2,752 storefronts,
  all Personal services, around 24 stations on 2 lines, 44.2% of them in a
  ring (1,216) on the standard rings.** Sources: Shizuoka City's three BODIK
  datasets (organization 221007), CC BY 4.0 under the city's terms (read
  2026-10-05 by staging, the barber list the same day; calls 10, 11, 39 and
  40): each full list as of 2026-03-31 (686 barbers, 1,752 beauty salons, 306
  laundry rows) and 41 monthly rows since. Food stays off (owner,
  2026-10-04). Built by the Regional-2 lead; the brief passed 10 of 10.
- **The brief's dates moved forward.** BODIK gained R8.9 files for beauty
  salons (3 rows) and laundries (1 row) on 2026-10-06, after the brief; the
  brief says to fetch the newest monthly files at build and re-pin each date.
  Beauty salons and laundries are as of 2026-09-30, barbers 2026-08-31 (no
  barber file for R8.9). Three BODIK downloads on 2026-10-11, 21 s apart: the
  barber full list (re-fetched under the owner's approval of call 39, as the
  brief says) and the two September files; three `package_show` calls before
  them, 21 s apart.
- **Two laundry vehicles the brief did not see.** Step 2 sets aside 2 rows of
  the laundry list whose address ends 県内全域 after a vehicle's plate number:
  mobile laundry vehicles, caught by the foundation's area-wide rule. With the
  1 無店舗 row out, laundries are 306 premises (the brief counted 307 before
  the September row, vehicles included).
- **Step 2:** rows 689, 1,787 and 309; storefront rows 2,782. The join: block
  2,713 (97.5%), town-chōme 68 (2.4%), unplaced 1 (三保宮方, a beauty salon;
  MLIT has no 宮方 under 三保). The foundation's ッ / ツ rule placed the 3
  七ッ新屋 rows the brief left unplaced. 29 repeat rows shown once, so 2,752
  pins (the brief expected 2,750 before the September files). The name rule
  flags 0 rows.
- **Independent check (GSI's address search, 150 block-tier rows, 1 request a
  second, 2026-10-11):** 150 answered; median 26 m from MLIT's block point,
  148 within 100 m, all within 250 m.
- **Rail:** step 1 reproduces the brief: 15 of 15 on the Shizuoka-Shimizu
  Line (gate 3 exact), 10 of 89 on JR's Tokaido Line, 草薙 one group (176 m),
  the Ikawa Line left out by `LEFT_OUT_LINES` (owner, 2026-10-04), 2 stations
  beyond the city line listed (富士, 富士川, both in Fuji). The median
  nearest-station gap is 610 m, where the brief read 624 m: standard rings
  either way (the halving threshold is about 550 m).
- **Station names stand as OpenStreetMap writes them (a judgment call, on the
  operator's own signs):** "Pref. Art Museum" and "Pref. Sports Park" are the
  Shizuoka Railway's own English names for 県立美術館前 and 県総合運動場, not
  OSM's translation, so Fukuoka's trap does not apply; "Shin-shizuoka" and
  "Shin-shimizu" keep OSM's lowercase beside JR's "Shin-Kambara" (Maebashi's
  precedent: OSM's spellings stand). No override, alias or tie.
- **Line colours:** JR Central's Tokaido Line takes `#E86810` from
  `pipeline/line_registry.py` (the registry's `maps` gains Shizuoka); the
  Shizuoka-Shimizu Line is `#0068B8`, `line_colour_search.py`'s nearest to the
  operator's blue. Against the Personal services pin: 88.5 and 106.4 (CIE76);
  `check_line_identity.py` PROBLEMS 0.
- **Line names:** "Shizuoka-Shimizu Line" (the operator's own name for its
  one line, as "Jomo Line" in Maebashi) and "JR Tokaido Line" (the registry's
  name).
- **Privacy verdict: publish.** `check_personal_exposure.py shizuoka`: the
  Japan pass prints 0 of 2,752; no trade name in the raw files is an
  operator's own name. The name rule compares 開設者氏名, 開設者法人, 営業者氏名
  and 法人代表者 in memory only; the operators' own addresses and the phone
  column are never selected.
- **No Economic Census control was run:** the control measures restaurants
  (industry 76) and this page has no food leg. The brief's census ratios for
  the registers (1.22, 1.57 and 1.12 per establishment) stand as measured at
  Step 0.
- **The notice's credit form** follows the licence read's "CC BY 4.0 改変
  form" in Hamamatsu's wording (the three register titles, 静岡市, the CC BY
  4.0 deed, the three dataset pages linked). The city's own terms were not
  re-read at the build.
- Files: `pipeline/shizuoka/`, `outputs/shizuoka/`,
  `app/pages/258_Shizuoka_Heatmap.py`, `app/cities.py`, `app/components.py`
  (notice 205, `_OSM_STATION_NAMES`), `pipeline/countries/japan.py` (the
  batch's eleven `CITIES` entries), `pipeline/line_registry.py`,
  `scripts/check_personal_exposure.py` (the batch's eleven entries), the
  docs rows.
