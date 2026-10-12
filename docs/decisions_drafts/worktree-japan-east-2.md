# Drafts: East-2 (branch `worktree-japan-east-2`)

The A/B build plan's East-2 batch (`docs/build_plan_2026-10-07.md`): Koshigaya,
Sagamihara, Fujisawa (A); Kawaguchi, Funabashi, Matsudo, Ichikawa, Urayasu,
Sakura, Yachiyo, Ichihara (B). Pages 240-250, notices 187-197 in build order.
Newest entry first. Cleanup folds this file into `DECISIONS.md`.

## Downstream inputs this branch changes

- New cities (each with `outputs/<slug>/`, a `app/cities.py` entry, a notice
  and rows in `docs/data_sources/japan.md`): Koshigaya (187), Sagamihara
  (188), Fujisawa (189), Kawaguchi (190), Funabashi (191), Matsudo (192),
  Ichikawa (193), Urayasu (194), Sakura (195), Yachiyo (196), Ichihara (197).
- Station names in English are OpenStreetMap's for every city here; the rail
  is MLIT's N02.
- `pipeline/line_registry.py`: eleven new entries and the new maps joined to
  existing ones. **No registered colour changed and no built map's output
  changes**; Tokyo's, Yokohama's and Kasukabe's lines are registered in the
  colours they already draw.
- A new shared module, `pipeline/countries/chiba_pref.py`; no existing shared
  pipeline module changed.
- Per notice, for Visuals: **all eleven are caption only** (PDL 1.0, CC BY
  4.0 and CC BY 2.1 JP name no placement beyond being stated with the work;
  the same reading as Kasukabe's 164). **No open terms question on any.
  Kawaguchi is held off cards and public pieces until its parked call B (the
  glyphs) is settled.**

## The owner's answers to the parked calls (2026-10-11, in the East-2 session)

Asked as five numbered calls in the batch report; the owner's words in quotes.

1. **Kawaguchi B, the private-use glyphs: "accepted."** The recommendation
   stands: `map_common.glitched_name` treats a private-use code point
   (U+E000-U+F8FF) as glitched, so such a pin shows its permit type. A shared
   renderer change, not made on this branch (the recommendation named it
   Cleanup's, with other maps measured first); Kawaguchi stays held until it
   lands and its map is re-rendered.
2. **Kawaguchi A, late starters that are renewals: "shared rule accepted."**
   A late start whose first-permit date is on or before the list's as-of is a
   renewal and stays. A shared `japan_step2` / `japan_register` change with
   the Minato control and a drift check over the Japanese cities, not made on
   this branch; Kawaguchi's counts rise by about 100 pins when it lands (5,212
   as built, 5,312 measured with the rule off), and its page, notice and docs
   figures are re-read then.
3. **Funabashi A, Keiyo against Musashino: "show me a visual."** Shown in
   chat (today's #F86040 beside the recommended #D01010, each next to the
   Musashino Line's #F05820, on the light and dark pages). No decision yet.
4. **The two station names: "note internally."** Urayasu's "Bay Side Station"
   and Sakura's "Chikucenter" stay as OpenStreetMap spells them; noted here,
   nothing on a page.
5. **Kawaguchi C, the line's name: "check image"**, with a screenshot of the
   line's Wikipedia entry: the line is the Saitama Rapid Railway Line
   (埼玉高速鉄道線), and "Saitama Stadium Line" (埼玉スタジアム線) the nickname
   adopted on 2015-11-27. Read as: label it by its formal name, which is also
   the project's line-name rule and N02's. **Renamed "Saitama Rapid Railway
   Line"** in the config, the page, the blurb and the docs rows; steps 1 and 3
   re-run (East-2's reading of the answer, to be corrected if the owner meant
   the nickname).

## Parked calls

- **Kawaguchi A: late starters that are renewals (call 172 against this
  list's shape).** The shared `late_start` rule drops 142 rows whose term
  starts after their list's as-of. All 131 in the March list carry a first
  permit and a latest grant date on or before 2026-03-31 and a term starting
  April to June 2026: renewals already granted, 112 of them restaurants at
  premises the list holds. With the rule off (measured in scratch, nothing
  written) the map holds 5,312 pins against 5,212 as built: 100 pins, 91 of
  them Food service. *Recommendation:* a shared rule that a late start whose
  first-permit date (初回許可（届出）年月日) is on or before the as-of is a
  renewal and stays (Cleanup's or a foundation change; the saitama_pref
  module already treats a late new-law permit as the renewal of an old-law
  twin). *Alternative:* `"rules_off": {"late_start": why}` for Kawaguchi
  alone, which also keeps the 41 monthly rows that may not be open yet.
  *Tradeoff of leaving it:* about 90 operating restaurants are missing. Built
  with the shared rule as it stands.
- **Kawaguchi B: three trade names carry a private-use glyph the map shows
  as an empty box** (U+E218, U+F223, U+E315, once each; the fourth, U+E4AA, is
  read as 塚 by the city's gaiji table). `map_common.glitched_name` does not
  flag a private-use code point, so the name renders as published; one pin
  is inside a ring. The owner's line is no glitched pin names live, so
  **Kawaguchi does not land until this is settled.** *Recommendation:*
  `glitched_name` treats U+E000-U+F8FF as glitched, so such a pin shows its
  permit type (a shared renderer change, Cleanup's; other maps change only
  where they hold such a name, to be measured first). *Alternative:* extend
  Kawaguchi's gaiji table once each character is read from evidence; a guess
  today. `businesses_clean.csv`'s address column also keeps the raw address
  (104 pins with a private-use code point); the map never renders it, noted
  for place search.
- **Funabashi A (for Cleanup): the JR Keiyo Line (#F86040, Tokyo's) sits
  11.8 from the JR Musashino Line (#F05820, registered) where they share
  track into 西船橋**, under the 18 asked of lines within 500 m and over the
  hard floor of 10, so the render passes. Both are another map's colour, so
  neither moved. *Recommendation:* Cleanup re-colours the Keiyo Line toward
  JR's red (#D01010 fits Funabashi: 45.2 from the Food service pin, 18.8 from
  Musashino), re-checked against Tokyo's other 51 lines. *Tradeoff:* it moves
  a built city's line; leaving it keeps two near-identical oranges side by
  side on Funabashi's and Ichikawa's maps.
- **Station names left as OpenStreetMap spells them, where the brief
  expected another spelling and no operator source is named:** Urayasu's "Bay
  Side Station" (the brief expected "Bayside Station") and its four monorail
  names ending in "Station"; Sakura's "Chikucenter" (the brief expected "Chiku
  Center"; Yamaman's page gives Japanese only). An override needs a cited
  operator spelling. *Recommendation:* the owner or Cleanup names the source
  (the operators' English signage) and the two overrides go in at review
  time; each is one config line and a re-run of steps 1 and 3. *Tradeoff of
  leaving them:* two labels that read oddly. Hyphen case also varies as OSM
  has it (Yachiyo-midorigaoka beside Toyo-Katsutadai), as on Tokyo's map.
- **Kawaguchi C: the Saitama Railway's line name.** The brief reads the
  operator's own public name, "Saitama Stadium Line" (埼玉スタジアム線, the
  line's adopted name); N02 files it as 埼玉高速鉄道線. Built as "Saitama
  Stadium Line"; confirm the label. It is new to the site (#3060B8) and not
  registered: no map in this batch or already built draws it (Tokyo leaves
  its one station out).

## Applied by precedent (named for the batch report)

- **Koshigaya, the brief's three weighed calls**, each applied as the brief
  recommends on the precedent it names: (1) no food-share sentence on the
  page, the city's withholding note stated with no number (call 125 as read
  for Hirakata, call 154; Kasukabe's call 173 wording); (2) the missing July
  2026 list: the food page re-read at build (brief check, 2026-10-11: still
  no July file), the months stated as April, May, June and August (calls
  126-127: MHLW's permits are not added in its place); (3) MHLW's
  notifications left out, since the city's own list publishes notifications
  (127b answered lists that have none).

- **Fujisawa:** one open MHLW permit (a restaurant granted 2026-08-21) is in
  no city file and is not added (call 127 (a), Ichinomiya's: MHLW's permits
  are not added; the city's next list should carry it). The Blue Line left
  out and the Sotetsu stub and Monorail drawn cut (calls 54 and 92, the
  standing stub call). The census ratio 1.97 is reported as measured.
- **Kawaguchi:** built on the CSV as published (call 177); MHLW left out
  whole (calls 126-127); the Musashino stub kept as cut.

## Proposed wording (no template covers these; for review time)

- **Fujisawa** (page 242): "From Fujisawa City's lists of food-business
  permits and of barbers, beauty salons and laundries, all as of June 30,
  2026, with the new food permits it listed for July and August 2026."; the
  estimate call 175 asks for: "No official count of Fujisawa's restaurants is
  published. Measured against the 2021 census of restaurants at the rates of
  four other Kanagawa cities, the list is estimated to hold between 88% and
  101% of them."; "Yokohama's Blue Line subway, which has only its terminus,
  Shonandai, in the city, is not drawn; Shonandai appears as a station of the
  Odakyu and Sotetsu lines." The notice (189) adds "left out permits the
  ministry's list records as closed". What Is Excluded carries "a caterer
  that also names a restaurant form is counted as a restaurant" (call 158).
- **Kawaguchi** (page 243): "From Kawaguchi City's list of food-business
  permits and notifications (as of March 31, 2026, with the new premises it
  listed for April, May and July 2026; the list has no entries for June).";
  "Kawaguchi City's lists of barbers, beauty salons and laundries are not
  open data, so personal services are not on this map."; "The city withholds
  the address of about one entry in six in its list, and those are not on
  this map. Where they are is not known." (Hiroshima's sentence; 1,316 of
  8,364); "Where the city masks a trade name, or a trade name is its
  operator's own name, the dot shows its permit type instead."; "JR's
  Utsunomiya, Takasaki and Shonan-Shinjuku line trains pass through the city
  without stopping and are not drawn."

- **Koshigaya** (page 240): "From Koshigaya City's list of food-business
  permits and notifications (as of March 31, 2026, with the new and renewed
  permits it listed for April, May, June and August 2026; the city published
  no list for July) and its lists of barbers, beauty salons and laundries (as
  of October 2, 2026)."; "The city leaves out some premises at their
  operators' request, so the food list is not complete." (Kasukabe's sentence
  with the city as publisher); "Minami-Koshigaya (JR) and Shin-koshigaya
  (Tobu) are separate stations a short walk apart, so their rings overlap.";
  the Reading-the-map placement bullet in Ichinomiya's form with the
  ministry named in full. The notice (187) adds "The city leaves out some
  premises at their operators' request, and no list for July 2026 was
  published." The same facts in its What Is Excluded section.
- **The credit's titles (187)** are the portal datasets' own (【越谷市】食品営業
  許可・届出一覧, 【越谷市】営業施設一覧) with the creator section the licence
  record names; check them against the licence-read report at review time.

## Shared-state findings for review time (not changed here)

- **Two operator-column spellings are not in `japan_register.OPERATOR_COLS`:
  開設者名称 (Sagamihara's barber and beauty lists) and 営業者名称 (its laundry
  list).** They hold company names only (496 values, every one with a
  company marker); Sagamihara records both in `config.NOT_OPERATOR` behind a
  guard that stops the build if a value ever lacks a marker. Adding them to
  the shared tuple needs the Minato control and changes nothing measured (0
  flags either way).
- Yokohama's config holds literals for three lines East-2 registered
  (`sotetsu-izumino-line`, `jr-east-yokohama-line`) where a registered line
  should read `line_registry.colour()`; the values are equal and the check
  passes. A built city's config, left for Cleanup.

- `app/components.py`'s `_OSM_STATION_NAMES` and notice 1's sentence do not
  name Regional-1's eleven cities, and the sentence does not name Kansai-1's
  seven; `app/osm_notice.py` names Kansai-1's but not Regional-1's. East-2's
  cities are added to all three as East-1's were. Cleanup's to reconcile.

## Entries

### 2026-10-11 - Ichihara built on the Chiba module, personal services only, the Kominato line drawn with its rural stretch named

- **Ichihara built (page 250, notice 197), personal services only (Band B),
  Matsudo's shape on `chiba_pref.py`: 708 storefronts (beauty salons 416,
  barbers 216, laundries 76) around 20 stations on 3 lines, 42.2% of them in
  a ring (299).** Brief check 13/13. Built by a subagent of the East-2 lead,
  integrated by the lead. Sheet 市原, rows 218 / 423 / 76 (the sheet's
  half-width header read through the module's alias).
- **Step 2:** 717 storefront rows: 669 block, 42 town centre, 6 unplaced
  (0.8%); 3 repeat rows dropped; names withheld 8 (the sign rule). On the map
  94.1% block, 5.9% at a district's centre, many of them rural 大字 with no
  block points; a GSI sample only returns the same centroids, so no
  independent distance exists for that tier. Built and disclosed (the
  brief's recommendation on its open call 1).
- **The laundry share (owner, call 123, Ichikawa's shape):** 76 against about
  94 scaled from the 2021 Economic Census, about four in five, stated on the
  page.
- **Privacy verdict: publish.** `check_personal_exposure.py ichihara`: the
  Japan pass prints 0; 8 pins show their register type.
- **Rail:** N02-25; 20 stations: the Kominato Railway Line 17 of 18, the JR
  Uchibo Line 3, the Keisei Chihara Line 1 (a private stub kept as cut). 五井
  one group for JR and the Kominato. Median gap 1,789 m: standard rings. Gate
  3: Kominato 17, the railway's own pages. 4 excluded (Chiba City 3, Otaki
  1). One alias: N02's 姉ヶ崎 is OSM's 姉ケ崎.
- **The low-frequency stretch (calls 46 and 86):** south of 上総牛久 the
  Kominato Railway runs 10 trains a weekday each way (9 to 養老渓谷, 1 turning
  at 里見), counted by train number from the railway's timetable of
  2026-03-14; the brief's 11 to 12 included specified-day trains. Drawn, and
  named on the page as "about ten trains a day each way" with the no-floor
  reason. The count was read by hand from a table with merged cells.
- **Colours, all this map's alone:** Kominato #F86040, JR Uchibo #00A0D0,
  Keisei Chihara #2860B0. The Kominato's value equals the registry's JR Keiyo
  Line; the two are about 20 km apart and never neighbours, so the checks
  pass. Its hue is a seed, free to move if the owner wants them apart.
- **The opening view** needs `scripts/check_map_view.js` (a large city whose
  stations run 30 km north to south): run with the batch's map checks.
- **Visuals:** notice 197 caption only. No open terms question.

### 2026-10-11 - Urayasu, Sakura and Yachiyo built on the Chiba module, personal services only

Each is Matsudo's shape on `chiba_pref.py` (sheet and address cut, barbers of
2025-03-31, beauty salons and laundries to 2026-08-31), built by a subagent of
the East-2 lead and integrated by the lead; each brief's checks hold (11/11,
12/12, 11/11); each privacy pass prints 0; no census control (no Food service
layer); notices caption only, no open terms question.

- **Urayasu (page 247, notice 194): 326 storefronts (beauty salons 192,
  barbers 76, laundries 58) around 7 stations on 3 lines, 77.6% in a ring
  (253).** Sheet 市川, rows 76 / 195 / 58. 329 storefront rows: 326 block, 3
  town centre, 0 unplaced (the brief, on the wave-2 rules alone, left 2
  unplaced); 3 repeat rows dropped; no name withheld. Rail: the Disney Resort
  Line (the monorail loop, 4 of 4; owner's label, call 122; #7850A0, a violet
  seed, this map's alone), JR Keiyo 2 (`jr-east-keiyo-line`), Tozai 1 at 浦安
  (`tokyo-metro-tozai-line`), drawn cut because no other line serves the
  station (calls 54 and 92). `N03_NEIGHBOR_PREFS = ("13",)`. Maihama and
  Resort Gateway Station, 161 m apart, kept apart. Gate 3: Disney 4, Tozai 1.
  6 excluded (Ichikawa 3, Edogawa 3). OSM's one object without name:en is a
  park ride, not a station.
- **Sakura (page 248, notice 195): 444 storefronts (beauty salons 250,
  barbers 116, laundries 78) around 11 stations on 4 lines, 72.5% in a ring
  (322).** Sheet 印旛, rows 117 / 256 / 79 (one April row already listed; 1
  無店舗 agent not a premises). 451 storefront rows: 429 block, 20 town
  centre, 2 unplaced (0.4%); 5 repeat rows dropped; no name withheld. `mode`
  metro (owner, call 121). Rail: Keisei Main 5 (`keisei-main-line`), the
  Yamaman Yukarigaoka Line (an automated guideway loop, 6 of 6, drawn once;
  #0068B8), and JR East's Sobu Main Line (#C06808) and Narita Line (#20A800),
  one station each at 佐倉, JR stubs kept as cut. Gate 3: Yamaman 6, its own
  station page. 9 excluded (Shisui 4, Yachiyo 2, Yachimata 2, Yotsukaido 1).
  One tie (ユーカリが丘 without a macron). The three new lines are this map's
  alone.
- **Yachiyo (page 249, notice 196): 549 storefronts (beauty salons 350,
  barbers 129, laundries 70) around 7 stations on 2 lines, 80.3% in a ring
  (441).** Sheet 習志野, rows 130 / 353 / 77 (7 無店舗 agents not premises).
  553 storefront rows: 539 block, 12 town centre, 2 unplaced (0.4%); 2 repeat
  rows dropped; 1 name withheld. Rail: the Toyo Rapid Railway Line 4 and
  Keisei Main 3; 勝田台 and 東葉勝田台, 149 m apart, kept apart. Gate 3: Toyo
  Rapid 4. 6 excluded (Sakura 2, Narashino 2, Funabashi 2).
- **Registry:** Urayasu, Sakura and Yachiyo joined `jr-east-keiyo-line`,
  `tokyo-metro-tozai-line` and `keisei-main-line`; new
  `toyo-rapid-railway-line` #20A800 (Funabashi and Yachiyo).
- **Against the briefs:** each brief's pin count did not subtract unplaced
  rows, and each join was measured on the wave-2 rules alone; the foundation's
  rules place a few more at the block (Sakura 4, Yachiyo 5).
- **Three lines share the value #20A800** (the registry's JR Joban, the Toyo
  Rapid Railway Line, Sakura's JR Narita Line). None meets another on any
  map or within 2 km of a neighbouring one, so the checks pass; a later map
  that draws two of them together would move one.

### 2026-10-11 - Ichikawa built on the Chiba module, personal services only, seven lines all from the registry

- **Ichikawa built (page 246, notice 193), personal services only (Band B),
  Matsudo's shape on `chiba_pref.py`: 1,017 storefronts (beauty salons 646,
  barbers 223, laundries 148) around 15 stations on 7 lines, 78.5% of them in
  a ring (798).** Brief check 12/12. Built by a subagent of the East-2 lead,
  integrated by the lead. Sheet 市川, rows 223 / 646 / 148 as the module and
  the brief agree; no 無店舗 row.
- **Step 2:** 1,017 storefront rows: 1,012 block, 5 town centre, 0 unplaced;
  no repeat rows. Names withheld 4 (the sign rule).
- **The laundry share (owner, call 32):** stated on the page as the brief
  words it, 148 against about 186 scaled from the 2021 Economic Census, about
  four in five, the reason not known.
- **Privacy verdict: publish.** `check_personal_exposure.py ichikawa`: the
  Japan pass prints 0; 4 pins show their register type.
- **Rail:** N02-25; 15 stations: Keisei Main 5, JR Chuo-Sobu 2 and Yokosuka /
  Sobu Rapid 1 (N02's 総武線 as two routes), JR Musashino 1 (a JR stub kept
  as cut), JR Keiyo 2 (drawn whole, as Funabashi's), Tozai 3 (drawn cut,
  call 31), Hokuso 2. **The Toei Shinjuku Line is left out** (1 of 21 inside,
  本八幡; owner, 2026-10-06), its station kept through JR.
  `N03_NEIGHBOR_PREFS = ("13",)`. Gate 3 exact for the Tozai (3, Tokyo
  Metro's numbering). Median gap 1,305 m (the brief's "closest pair 216 m" is
  341 m by step 1). 26 excluded. One tie: 本八幡 reads "Moto-Yawata", JR's
  spelling, since the pin sits on JR's line and Toei's is left out.
- **Registry:** every line joins an existing entry (`keisei-main-line`,
  `jr-east-chuo-sobu-line`, `jr-east-yokosuka-line`, `jr-east-musashino-line`,
  `jr-east-keiyo-line`, `tokyo-metro-tozai-line`, `hokuso-line`); no colour
  of its own. The Musashino / Keiyo pair is 11.8 apart here too (Funabashi A).
- **Visuals:** notice 193 caption only. No open terms question.

### 2026-10-11 - Chiba Prefecture's shared leg (`chiba_pref.py`) written with Matsudo; Matsudo built, personal services only

- **One module for the six Chiba pages** (Matsudo, Ichikawa, Urayasu, Sakura,
  Yachiyo, Ichihara), on `saitama_pref.py`'s precedent (the japan-city skill:
  what a second city would also need goes in the shared module):
  `pipeline/countries/chiba_pref.py` reads Chiba Prefecture's
  環境衛生関係施設一覧 (dataset 6, PDL 1.0) from a shared cache
  `data/chiba_pref/raw/` (the thirteen Step 0 workbooks, copied from
  `data/matsudo/raw/`, byte-identical by SHA-256 to the copies in three other
  city folders; nothing downloaded) and cuts each page out by health-center
  sheet and address. A new file; no existing shared file changed, so no
  Minato control was owed.
- **What it encodes:** the barber file as published, dated 2025-03-31 (owner,
  call 33); beauty salons and laundries as the 2026-03-31 lists plus the
  months' openings to 2026-08-31, an upper bound (call 34); one header
  spelling per sheet through aliases (the 印旛 barber sheet's own column
  order, the half-width header of 市原, months writing 施設名称), raising on
  an unknown header; a 「…新規なし」 sheet read as empty; a month row dropped
  only where both its number and its address repeat a listed row (Sakura's
  April case); the beauty workbook's 海匝 sheet, a copy of 印旛, never read;
  phones, titles and second address and name columns never leave the reader;
  `fetch` never overwrites a file on disk.
- **Proved for all six:** the module's row counts equal every brief's, 18 of
  18 (Ichikawa 223 / 646 / 148, Urayasu 76 / 195 / 58, Sakura 117 / 256 / 79,
  Yachiyo 130 / 353 / 77, Ichihara 218 / 423 / 76); each city's config
  asserts its own (`EXPECTED_ROWS`).
- **Matsudo built (page 245, notice 192), personal services only (Band B):
  1,253 storefronts (beauty salons 766, barbers 304, laundries 183) around
  20 stations on 7 lines, 79.8% of them in a ring (1,000).** Brief check
  13/13. Built by a subagent of the East-2 lead, integrated by the lead.
- **Step 2:** 2 無店舗 laundry agents not premises (クリーニング種別１, read by
  the foundation); 1,262 storefront rows: 1,241 block, 19 town centre, 2
  unplaced (0.2%: a district MLIT's files do not hold); 7 repeat rows
  dropped. Names withheld 5, all by the sign rule. The brief's "1,255 pins"
  did not subtract the 2 unplaced rows.
- **No official count for the city alone** (e-Stat counts the prefecture's
  jurisdiction as one); prefecture-wide the barber list is 99.6% of the
  official count on the same date. No census control: no Food service layer.
- **Privacy verdict: publish.** `check_personal_exposure.py matsudo`: the
  Japan pass prints 0; 5 pins show their register type.
- **Rail:** N02-25; 20 stations: Keisei Matsudo 8, JR Joban 5 (one line, as
  Tokyo's, Mito's and Iwaki's), JR Musashino 3, Hokuso 4, Ryutetsu Nagareyama
  3, the Keisei Narita Sky Access Line 1 (N02's 成田空港線, its own line over
  the Hokuso track, a stub kept as cut) and the Tobu Urban Park Line 1 (a
  stub kept as cut). `N03_NEIGHBOR_PREFS = ("13", "11")`. Two close pairs kept
  apart as N02 keeps them (Yabashira / Shin-Yahashira 93 m, Koya /
  Shin-Matsudo 196 m). Gate 3 exact for Ryutetsu (3); the cut lines have no
  independent in-city count read. 26 excluded. No override.
- **Registry:** joined `jr-east-joban-line`, `jr-east-musashino-line`,
  `hokuso-line`, `tobu-urban-park-line`; new `keisei-matsudo-line` #E060D0
  (Funabashi and Matsudo). This map's alone: Ryutetsu #3060B8, Sky Access
  #D87800.
- **Visuals:** notice 192 caption only (PDL 1.0 names no placement). No open
  terms question. The five Chiba pages after it carry the same notice.

### 2026-10-11 - Funabashi built, personal services only, ten lines; six lines Tokyo and Kasukabe draw registered

- **Funabashi built (page 244, notice 191), personal services only (Band B),
  Yokohama's and Kōchi's shape: 1,473 storefronts (beauty salons 957, barbers
  314, laundries 202) around 30 stations on 10 lines, 83.8% of them in a ring
  (1,234).** On the Japan foundation's rules. Brief check 5/5 (2026-10-11).
  Built by a subagent of the East-2 lead, integrated by the lead. The three
  registers were on disk from Step 0; no BODIK data request was made at
  build. The terms page (odcs.bodik.jp/122041/tos/) was re-read once by the
  lead, as the brief asks: the modified-use form, CC BY 4.0, the link clause
  and the no-completeness clause all stand.
- **Step 2:** 4 rows addressed in another municipality and 1 giving the city
  name alone set aside by the shared rules (the brief's `source_rows` filter
  not needed); 1,493 storefront rows, 1,490 block, 3 town centre, 0
  unplaced; 20 repeat rows dropped. The kind (業態) is copied into the type
  in `source_rows` (Amagasaki's route). Names withheld 6 (the sign rule; the
  brief's operator comparison alone found 0).
- **One laundry address holds 15 rows** under three trade names, each with a
  company marker; kept as 3 pins (one pin per address and name). Nothing
  marks them storeless.
- **Official shares (e-Stat FY2024):** barbers 94.9%, beauty salons 100.5%,
  laundries 97.3% of rows (202 premises, 91.8%). No census control: no Food
  service layer.
- **Privacy verdict: publish.** `check_personal_exposure.py funabashi`: the
  Japan pass prints 0; 6 raw flags, 6 pins show their register type.
- **Rail:** N02-25; 30 stations on ten drawn lines: Keisei Main 7, Keisei
  Matsudo 9, JR Chuo-Sobu 4 and JR Yokosuka / Sobu Rapid 1 (N02's 総武線 as
  two routes, Tokyo's form), JR Musashino 2, JR Keiyo 2, Tozai 2 (drawn cut,
  owner's call 41), Toyo Rapid Railway 5, Tobu Urban Park 4, Hokuso 1 (a
  private stub kept as cut). Gate 3 exact where an operator's count was read
  (Toyo Rapid 5, Hokuso 1, Tozai 2 from the station numbering; Tokyo Metro's
  page answered 403); JR East, Keisei and Tobu are cut lines with no
  independent in-city count read. Median gap 729 m: standard rings. 25
  excluded: Ichikawa 8, Narashino 7, Kamagaya 5, Yachiyo 2, Shiroi 2, Chiba
  City (Mihama Ward) 1. No override.
- **Registry:** joined `jr-east-musashino-line` and `jr-east-yokosuka-line`;
  **six new entries, each in the colour a built map already draws:**
  `keisei-main-line` #785868, `jr-east-chuo-sobu-line` #B09000,
  `jr-east-keiyo-line` #F86040, `tokyo-metro-tozai-line` #6890A0 and
  `hokuso-line` #787878 (Tokyo's), `tobu-urban-park-line` #60A000
  (Kasukabe's). Tokyo's and Kasukabe's configs still hold the literals. New
  on this map: Keisei Matsudo Line #E060D0 (registered with Matsudo) and the
  Toyo Rapid Railway Line #20A800 (18.8 from the Tobu Urban Park Line within
  500 m; the same value as the registry's JR Joban, which it never meets).
- **Line names follow Tokyo's map** ("Tozai Line", "JR Yokosuka / Sobu Rapid
  Line"), so one line reads the same on every map.
- **Slips (subagent):** two reads of operators' station pages outside the
  brief's named URLs, for gate 3 (toyokosoku.co.jp, used; keisei.co.jp, not
  used), saved to scratch only; the rendered map opened once in the browser
  pane as a file for a label measurement.
- **Visuals:** notice 191 caption only. No open terms question.

### 2026-10-11 - Sagamihara built, the food, barber and beauty lists rebuilt to August 2026 from zipped registers; two lines registered

- **Sagamihara built (page 241, notice 188), Sakai's shape (a register
  rebuilt by permit number with the city's own closures): 5,539 storefronts
  (Food service 2,881, Food shops 894, Personal services 1,764) around 16
  stations on 6 lines, 60.3% of them in a ring (3,339).** On the Japan
  foundation's rules; three wards, so not wardless. Brief check 17/17
  (2026-10-11). Built by a subagent of the East-2 lead, integrated by the
  lead. Every file was on disk from Step 0 (2026-10-04).
- **Zipped registers:** each source is a zip of CSVs, read by the config's
  own `file_rows` (a file-format hook; `city_rows` reads XLSX members only).
  Food: year-end 5,563 fixed + 447 new - 442 closed (of 461 closure numbers)
  = 5,568; 19 past term; 5,549 in term on 2026-08-31. Vehicle permits are the
  city's own list (592 in term), counted for the share and never placed.
  Barbers 468 + 2 = 470; beauty 1,082 + 11 - 8 = 1,085; laundries 237
  (2026-03-31, no months).
- **A closure removes one row, the earliest inspected, not every row of its
  key:** one beauty salon changed hands (a new registration in June, the old
  operator's closure in July, same address and name); removing by key would
  have dropped the live salon. Hence 1,085 against the brief's 1,080.
- **Withheld premises (`ADDRESS_BY_CONSENT`):** 611 food rows carry no
  address or name at the operator's request. The page says "about one
  restaurant in nine", the brief's measure (3,763 of 4,231 fixed restaurant
  permits publish an address, stalls out of the denominator); with the 36
  stall-form rows kept in, it is 504 of 4,267 (one in 8.5). Both round to the
  sentence used.
- **Step 2:** not a premises 299 (297 一円 food rows, 2 mobile salons); 6
  無店舗 laundry agents set aside; late start 1; out by rule 665 (197
  institutional catering, 173 hostess venues, 163 manufacturing types, 41
  entertainment venues, 36 inside accommodation, 28 vending, 25 caterers of
  which 4 also name a counter form, 2 temporary, 1 mail order); 37 combined
  業態 cells read as their restaurant form (call 158). Of 5,759 storefront
  rows: 5,649 block, 110 town centre, 0 unplaced. 220 repeat rows dropped.
  Names withheld 2. Factory share 30 of 486 (6.2%), kept.
- **Official shares:** restaurants 5,150 permits in term (vehicles included)
  of 5,100, 101.0%; barbers 98.5%; beauty 101.1%; laundries 99.6%.
- **Economic Census control:** 2,881 pins against 1,850 establishments, 1.56
  (緑区 1.71, 中央区 1.51, 南区 1.52), the bottom of the built range, as
  expected with one restaurant in nine withheld.
- **Privacy verdict: publish.** `check_personal_exposure.py sagamihara`: the
  Japan pass prints 0; 5 raw flags, 2 pins show their permit type.
- **Rail:** N02-25; 16 stations: JR Sagami 7, JR Yokohama 5, JR Chuo 2,
  Odakyu Odawara 2, Odakyu Enoshima 2, Keio Sagamihara 1 (a private stub kept
  as cut); the Chuo and both Odakyu lines drawn as cut (owner, 2026-10-05).
  `N03_NEIGHBOR_PREFS = ("13", "19")`. Gate 3 exact on all six. Median gap
  1,452 m (the brief's 1,542 corrected). 14 excluded: Machida 5, Yamato 3,
  Zama 3, Hachioji 2, Uenohara 1. No override.
- **Registry:** joined `jr-east-chuo-line`, `odakyu-odawara-line` and
  `keio-sagamihara-line`; **new entries** `jr-east-yokohama-line` (#68A008,
  the colour Yokohama already draws; 26.3 from olive Food shops, an accepted
  trade recorded in the config, as it is on Yokohama's map) and
  `odakyu-enoshima-line` (#5080B8, Fujisawa's choice, measured on both maps:
  pins 72.3, 24.0 from the Odawara Line at 相模大野; Sagamihara's own first
  choice #1888D0 dropped for it). The JR Sagami Line (#008090) is this map's
  alone. Yokohama's config still holds its literals for both new entries.
- **The line name "JR Chuo Line"** follows the registry (Hino's and
  Tachikawa's); the brief wanted "Chuo Main Line", and East-1's parked call 5
  covers the name site-wide.
- **Visuals:** notice 188 caption only (CC BY 4.0 names no placement). No
  open terms question.

### 2026-10-11 - Fujisawa built, the June lists kept whole with the months since, MHLW's notifications, five lines

- **Fujisawa built (page 242, notice 189), Ichinomiya's shape: 4,947
  storefronts (Food service 2,938, Food shops 866, Personal services 1,143)
  around 17 stations on 5 lines, 77.2% of them in a ring (3,821).** On the
  Japan foundation's rules. Brief check 18/18 (2026-10-11). Built by a
  subagent of the East-2 lead, integrated by the lead. Every file was on disk
  from Step 0.
- **Sources:** the city's food list of 2026-06-30 in two files (companies
  2,629 rows, individual operators 1,897), kept whole less 6 permits MHLW's
  file records as closed in August 2026 (call 159, a read-only filter in
  `source_rows`, Fukuyama's shape; 6 of 6 found); the July and August lists
  (109 rows) as `food_new`; the barber, beauty and laundry lists of
  2026-06-30 (203, 821, 142); MHLW's notifications only (989 rows read, 387
  with no published address), `SUPERSEDES` over the city rows (49),
  `OWN_POINT_FALLBACK` (14) and `POINT_DONORS` (9). June's monthly files are
  all in the full list by permit number and are not read.
- **The individual operators' file goes through the name rule** (the owner's
  answer): it carries no operator column, so only the sign test runs there
  (0 bare personal names); the page carries Kawasaki's bullet, as the brief
  prescribes.
- **Step 2:** not a premises 504 (一円 addresses; 2 無店舗 laundry agents, the
  laundry 種目 passed as the type); out by rule 711 (308 institutional
  catering, 158 non-counter types, 103 vending, 55 hostess venues, 40
  caterers, none of which also names a counter form since call 158 returns
  those to Food service (242 combined cells read as their restaurant form),
  32 inside accommodation, 11 temporary, 4 mail order). Of 5,172 storefront
  rows: 5,099 block, 50 town centre, 23 own point, 0 unplaced. 176 repeat
  rows dropped. Names withheld 3. Factory share 13 of 411 (3.2%), kept.
- **Economic Census control:** 2,938 pins against 1,495 establishments,
  1.97, just above the built cities' 1.56-1.92 (the brief estimated 1.90
  before call 158 returned about 100 rows). Reported, not tuned.
- **The food share (call 175):** no official count exists; the page states
  the brief's census estimate as an estimate (88% to 101% at four Kanagawa
  cities' rates). Registers against the city's own 2025-03-31 counts: 102.0%,
  104.3%, 94.7%.
- **Privacy verdict: publish.** `check_personal_exposure.py fujisawa`: the
  Japan pass prints 0; 2 raw trade names are an operator's own name, 3 pins
  show their permit type.
- **Rail:** N02-25; 17 stations: Odakyu Enoshima Line 9, Enoden 6, JR
  Tokaido 2, Shonan Monorail 2 (drawn cut, 2 of 8), Sotetsu Izumino 1 (a
  private stub kept as cut). Yokohama's Blue Line, 1 of 17 inside (湘南台), is
  left out, its station kept through Odakyu and Sotetsu (calls 54 and 92).
  `SPACING_MIN_M = 90` under Shonan-Enoshima / Enoshima, 96 m apart, separate
  N02 groups. Gate 3 exact on all five. 17 excluded: Kamakura 10, Yokohama's
  Izumi Ward 4, Yamato 2, Chigasaki 1. One cited override (辻堂, Tsujido).
- **Colours and the registry:** JR Tokaido from `jr-east-tokaido-line`;
  the Sotetsu Izumino Line registered as `sotetsu-izumino-line` in the colour
  Yokohama already draws (#6048E0; Yokohama's config still holds the literal,
  which the check accepts: Cleanup's to switch); the Odakyu Enoshima Line is
  registered with Sagamihara (below, its entry). Enoden #486860 (45.0 from
  the Personal services pin) and the Monorail #F01000 are this map's alone.
- **The fetch pins each edition's URL** rather than following the page's
  links: the files are renamed each edition and the registers' timestamp
  names cannot be told apart by href. A refresh edits `SOURCE_FILES`; the
  brief's first two checks fail when the pages move on.
- **Visuals:** notice 189 caption only (CC BY 4.0 and PDL 1.0 name no
  placement). No open terms question.

### 2026-10-11 - Kawaguchi built, food only, the March list kept whole with the new premises to July; two parked calls hold its landing

- **Kawaguchi built (page 243, notice 190), food only (Band B; the
  personal-services PDFs are not open data, call 104), Ichinomiya's merge:
  5,212 storefronts (Food service 3,299, Food shops 1,913) around 8 stations
  on 3 lines, 56.4% of them in a ring (2,939).** On the Japan foundation's
  rules. Built by a subagent of the East-2 lead, integrated by the lead.
- **Brief check 11/12:** the live CSV now carries an R0808 edition (the page
  was updated 2026-10-07). Built on the file on disk, the 2026-08-19 edition
  the brief measured (call 177: the CSV as published, June's gap named);
  `config.source_rows` stops unless the file holds exactly R0803 8,034, R0804
  112, R0805 104 and R0807 114 rows, so a re-download cannot be read
  silently. The newer edition is a refresh for after landing, under a new
  file name (the shared data/ rule).
- **One CSV, two sources:** `food` (R0803, `TERM_AS_OF` 2026-03-31) and
  `food_new` (the months, 2026-07-31), split by Source.Name in a read-only
  `source_rows`.
- **Step 2:** address withheld by the city 1,316; area-wide 10; another
  municipality 9; late start 142 (parked call A); not a premises 436; out by
  rule 790 (302 institutional catering, 243 vending, 232 manufacturing and
  other non-counter types, 11 mail order, 2 temporary). Of 5,661 storefront
  rows: 5,598 block, 57 town centre, 6 unplaced (0.1%). 443 repeat rows
  dropped. Masked trade names 1,350; names withheld by the name rule 8.
  Factory share 47 of 350 (13.4%), kept. Against the brief's 5,283 pins: 100
  fewer from late_start, about 25 more Retail from 米殻類販売業 now classified.
- **Gaiji:** the three address code points are in `japan.CITIES` (塚, 蓮,
  樋); 139 raw address rows carry one. Three trade names keep an unread
  private-use glyph (parked call B).
- **Economic Census control:** 3,299 pins against 1,384 establishments,
  2.38, above the built cities' 1.56-1.92; the brief's reading stands (the
  official count is itself 3.08 per establishment, and the March list is
  100.5% of e-Stat's 4,259 restaurants).
- **Privacy verdict: publish, once call B is settled.**
  `check_personal_exposure.py kawaguchi`: the Japan pass prints 0; 16 raw
  trade names are an operator's own name, 8 pins show their permit type.
- **Rail:** N02-25; 8 stations: the Saitama Stadium Line 6 of 8, JR
  Keihin-Tohoku 2 (a route over 東北線 from 赤羽 to 蕨, Tokyo's and Kawasaki's
  JK form), JR Musashino 1 (a JR stub kept as cut, standing call 3). 東川口 one
  group for two lines. `N03_NEIGHBOR_PREFS = ("13",)`. Gate 3 exact. 8
  excluded. English names from OSM, no override. Colours: JK and JM from the
  registry, SR #3060B8 from the colour search (77.8 from the nearest pin,
  49.1 from JK).
- **Visuals:** notice 190 caption only (CC BY 2.1 JP names no placement).
  **Open terms question: none**, but the city is held off cards and public
  pieces until parked call B is settled.

### 2026-10-11 - Koshigaya built, the March food list kept whole with the months since, and the October registers

- **Koshigaya built (page 240, notice 187), Ichinomiya's shape (a city's own
  full food list kept whole plus the months since, owner call 126) with
  Toyama's point-donor use of MHLW's file: 4,092 storefronts (Food service
  1,988, Food shops 1,114, Personal services 990) around 8 stations on 2
  lines, 71.7% of them in a ring (2,934).** On the Japan foundation's rules
  (no `"rules"` key). The brief's checks: 16/16 (2026-10-11). Sources: the
  city's food list of permits in term and notifications on 2026-03-31 (4,567
  rows) and its monthly lists of April, May, June and August 2026 (235 rows),
  and its barber, beauty and laundry lists of 2026-10-02 (225, 645, 124).
  Every file was on disk from Step 0 (2026-10-06); the build fetched only the
  OSM station names (one Overpass query; overpass-api.de answered 504, the
  kumi mirror answered).
- **Merge (a) as two sources, not one rebuilt register** (Ichinomiya's
  finding, applied): the March list is source `food` (`TERM_AS_OF`
  2026-03-31: 1 permit past its term) and the months source `food_new` of the
  same kind (`TERM_AS_OF` 2026-08-31: 0 late starters). The months carry
  renewals as well as new permits; one pin per premises and bucket shows a
  renewed premises once (294 repeat rows dropped). The brief's
  `rebuilt_register` worry (rows with no end date dropped) does not arise:
  the list is read whole, so the 1,472 notifications reach step 2. No shared
  code changed; 代表者名（法人） and 代表者_氏名 were already in
  `OPERATOR_COLS` (the foundation).
- **MHLW (calls 126-127):** nothing of it is drawn. `POINT_DONORS` gave its
  own point to 18 city rows the block join left at a town centre (15 pins).
- **Step 2:** of 4,394 storefront rows, 4,244 at the block, 124 at a town
  centre, 18 at MHLW's point, 8 unplaced (0.2%). On the map: 96.7% block,
  3.0% town centre, 0.4% MHLW's point. Not a premises 382 (vehicles, stalls,
  市内一円, storeless). Out by rule 1,019: 291 institutional catering, 254
  vending, 215 manufacturing and other non-counter types, 181 hostess venues
  (種目 カフェバーキャバレー, out whole on Tokyo's precedent, owner 2026-09-29;
  the brief measured 177), 60 caterers (種目 is one value per row, so none
  also names a counter form), 18 inside accommodation. Kept by 種目: 151
  konbini holding a restaurant permit, 79 department stores and
  supermarkets, 37 delis (Retail).
- Against the brief: Food service 1,988 (the brief 1,977 before the foundation's
  rules); Retail 1,114 pins from 1,314 rows (the brief's 1,288 counted rows
  before one pin per premises).
- The 菓子 / そうざい factory share: 19 of 214 (8.9%), kept (owner,
  2026-09-24).
- **Economic Census control:** 1,988 Food service pins against 1,095 飲食店
  establishments in 11222: 1.82 per establishment, inside the built cities'
  1.56-1.92 (the brief's 1.80).
- **Privacy verdict: publish.** `check_personal_exposure.py koshigaya`: the
  Japan pass prints 0; 7 trade names in the raw files are an operator's own
  name, 1 pin shows its permit type.
- **Rail:** N02-25; 8 stations, 8 groups: the Tobu Skytree Line 6 of 55
  (伊勢崎線), JR East's Musashino Line 2 of 27, both main lines cut at the
  line. 南越谷 (JR) and 新越谷 (Tobu), 132 m apart, are separate N02 groups of
  different names and stay apart (trap 1); `SPACING_MIN_M = 100` lets gate 1
  read them as two stations (Tama's precedent). Median nearest-station gap
  1,295 m: standard rings. 9 excluded: 草加市 3, 春日部市 2, 吉川市 2, 三郷市 1,
  川口市 1. Gate 3 exact (6 and 2). English names: OSM's 14 objects, no
  override (Shin-koshigaya and Kita-koshigaya as Tobu signs them).
- **Colours:** both lines are registry lines (`tobu-skytree-line` #007890,
  `jr-east-musashino-line` #F05820): 51.4 and 54.7 from the nearest pin, over
  45. `check_line_identity.py`: PROBLEMS 0.
- **Region:** `Saitama Prefecture` (the view Sōka and Kasukabe are in);
  `label_tier: "minor"`. No region table touched (call 198).
