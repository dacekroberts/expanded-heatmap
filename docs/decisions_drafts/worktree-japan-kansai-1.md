# DECISIONS drafts - Kansai-1 (`worktree-japan-kansai-1`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

Cities, in build order (`docs/build_plan_2026-10-07.md`): Toyonaka (page
222), Hirakata (223), Suita (224), Itami (225), Kakogawa (226), Amagasaki
(227), Uji (228); notices 169-175.

## Parked calls

1. **ANSWERED (owner, call 205, 2026-10-07; the entry below). Suita: one operator's own name shown, because the name rule does not
   cross premises (a shared-code gap; Suita is parked, committed on the
   branch, nothing pushed).** `check_personal_exposure.py suita` prints 1 (of
   4,012 pins). The city's old-law list flags a street stall (露店, 市内一円, not
   a premises) whose trade name is its operator's own name; MHLW's
   notification at a fixed address in 泉町 carries the same trade name, and
   its 法人名 does not flag it, so the pin shows the name. Step 2 spreads the
   rule only to rows sharing the flagged row's block (Osaka's 2026-09-27 rule);
   a citywide stall has no block. *Recommend*: in `japan_step2`, withhold
   every row whose trade-name key matches any flagged row's key in the same
   city, as a foundation-style switch on for new cities (`name_city`), with a
   raising check that the privacy pass and step 2 agree; built cities stay
   unchanged until a review time re-renders them. Measured: the privacy
   check, which already matches by trade-name key across the whole city,
   prints 0 for the other six Kansai-1 cities, so the change would move only
   Suita's 1 pin among them; East-1 reports the same check printing 0 on
   all twelve of its cities (2026-10-07); built cities are not re-measured here. Tradeoff:
   a common trade name that is also some operator's own name elsewhere in the
   city would be withheld at every premises. Without it, Suita cannot publish.
   The shared change touches `japan_step2`, so East-1 and Regional-1 are told
   first.

## Proposals for review time (sentences no template covers)

- **Toyonaka, What Is Excluded, Stations:** "Senri-Chuo is one station: the
  Osaka Monorail's platform and Kita-Osaka Kyuko's, 257 m apart, share one
  ring."
- **Itami and Kakogawa, The businesses:** "From Hyōgo Prefecture's lists of
  … (all as of August 31, 2026), which cover the prefecture's towns and cities
  outside its five largest; each business is placed in <City> by its
  address." and the stated share (call 125's precedent, Ichinomiya's shape):
  "The prefecture publishes no count for <City> alone, so how complete the
  lists are here can only be estimated: they hold about 86% [Kakogawa 87%] of
  the restaurants a prefecture-wide comparison suggests." The notification
  bullet is Yokkaichi's approved sentence with "the prefecture" for "the
  city".
- **Itami, The lines:** "…and the Osaka Monorail's main line, which has one
  station in the city, at the airport."
- **Kakogawa, Reading the map** (the tiers disclosed, owner call 145): "Each
  address is matched to MLIT's address reference data: about 88% reach their
  street block, and about 12%, where only the district can be found, sit at
  the district's center."
- **Itami and Kakogawa, What Is Excluded:** the rows addressed outside the
  city and the 県下一円 permits; "The list names no hostess venue, so snack
  bars holding a restaurant permit stay in Food service."; the estimated share
  in **Counted**.

- **Hirakata, The businesses:** "The city's food list holds fixed premises
  only, so food trucks, stalls and vending machines are not on this map."
  (call 154: the exclusion named, no share).
- **Suita, The lines:** "Osaka Metro's Midosuji Line, which has one station in
  the city, is not drawn: Esaka keeps its rings through Kita-Osaka Kyuko, whose
  trains run on along the Midosuji Line." (call 165). **The businesses:** "The
  food lists hold the permits in term on March 31, 2026: a permit that has run
  out since is still counted, and one granted since is not." (Kyoto's
  upper-bound disclosure in words).
- **Uji:** the Tōzai bullet ("…which ends at Rokujizo, is not drawn: Rokujizo
  keeps its rings through the JR Nara Line."); the personal-services bullet
  ("Kyoto Prefecture publishes its lists … only as documents whose reuse needs
  its permission"); "each is placed in Uji by its address"; and the brief's
  open call 1 wording, "About one restaurant in seven in Kyoto Prefecture's
  filings (outside Kyoto City) chose not to publish its address in the
  national filing system, so some in Uji are not on this map. Where they are
  is not known." (the brief's recommendation; the share is measured
  prefecture-wide, never for Uji).
- **Amagasaki, What Is Excluded:** "The JR Tōzai Line keeps one station inside
  the city, Amagasaki (JR), and the Hankyu Itami Line one, Tsukaguchi
  (Hankyu); each is drawn as cut."

## Brief corrections (a brief to correct, never a check to relax)

- **Kakogawa:** "0 rows in any file contain 加古川市 anywhere else" holds for
  premises only: 3 vehicle notifications read 「たつの市、高砂市、加古川市内一円」.
  The cut passes over an area licensed across several towns (it is no premises
  in any of them) and still stops on any other mid-address mention; Itami's
  cut does the same.
- **Uji:** the guard on 宇治 alone stopped on 伊根町's 字本庄宇治 (3 rows); the
  brief's measured claim is about 宇治市, and the guard now tests that.
- **Toyonaka:** the June 2026 and later new-permit files drop the empty
  廃業年月日 column; the brief listed it for every month.

### 2026-10-07 - The name rule crosses premises (owner, calls 205 and 209); Toyonaka's register rebuilt to August (call 151)

- **Call 205 ("205 yes", relayed by Staging): `name_city`, a WAVE5_RULES switch in `japan_step2.run`**, after the block spread: a trade name the name rule flags on any row withholds every row of the city with the same trade-name key. On for new cities (ALL_RULES), off for the 34 built (WAVE2_RULES). Minato control unchanged (98.0% block). Suita's privacy check 1 → 0 (1 pin now shows its permit type). The other six Kansai-1 cities move nothing. East-1 and Regional-1 were told before the change; East-1's call 202 switch (`default_joined`) shares the frozenset's closing line, keep both at merge.
- **Measured read-only on the 34 built cities** (step 2 at `write=False`, the switch forced on): Osaka 6, Utsunomiya 3, Fukuoka 1, Kyoto 1, Sapporo 1, Yokkaichi 1 and Tokyo 1 rows withheld; the other 27 nothing. **`check_personal_exposure.py` prints the same 13 names on the six live maps** (Tokyo 0: its row is not on the map): the gap was already published. Reported to Staging at once; **call 209, owner: "fix now in cleanup"**. The switch alone, on origin/master 7611559f, is commit fe85a793 (local branch `kansai1-name-city`, not pushed) for Cleanup to land and switch on for the six; Kansai-1 left the built cities and master alone.
- **Call 151 ("151 yes"): Toyonaka's 生活衛生 register rebuilt to 2026-08-31.** The 14 monthly CSVs of 2026 fetched from BODIK (one package_show and 14 downloads, each at least 21 s after the last; no datastore_search_sql), rebuilt by 許可（登録）番号 (Maebashi's): 1,255 + 17 new − 90 closed = 1,182, every closure matching a register number and no new number already in it. Barbers 237 → 231, beauty salons 736 → 722, laundries 231 → 180 (the March closure list alone names 27 pick-up shops). The page now states one date. Storefronts 5,277 → 5,205.

### 2026-10-07 - Hirakata, Suita, Amagasaki and Uji built (Kansai-1, pages 223, 224, 227, 228; notices 170, 171, 174, 175)

- **Built by three subagents (Hirakata, Suita, Amagasaki; pipeline only, each in its own `pipeline/<city>/`) and the lead (Uji)**, every shared file edited by the lead, every Overpass query and BODIK call made by the lead one at a time (process change: the plan's "up to three subagents").
- **Hirakata: 4,607 storefronts, 12 stations.** The March 2026 food list kept whole plus the five monthly new-permit files (call 126), merged by `rebuilt_register` (3,221 permits, 2,560 restaurants, the brief's); `TERM_AS_OF` the list's own 2026-03-31, since the merge keeps the March list whole (a later date would drop the March permits ending April to August without their renewals, the brief's rejected 2,503). The registers with their five monthly files (call 155, 11 new premises, 59,835 B from the city's host). MHLW's notifications as the partial Food-shops layer (127b) with its own point (127c). Block 97.4%; 2 restaurants unplaced (a lot number with no town). Census 2.65, above the built range: no 業態 (konbini chains about 120, supermarkets 56 by trade-name word), and closures unseen between the twice-yearly lists; without the konbini and supermarket rows about 2.47, Toyonaka's and Aomori's level. Names withheld 1.
- **Suita: 4,012 storefronts, 15 stations; PARKED (call 1 above).** The two food lists of 2026-03-31 (revised and old law) as one food kind, `TERM_AS_OF` their own date (the upper bound disclosed, Kyoto's); the registers of 2026-08-31; MHLW's notifications. Every count is the brief's: 3,330 restaurants, Food service 2,430 rows / 2,301 pins, Retail 630 + 444, Personal services 849; 0 unplaced; census 2.26. Rail: the Midōsuji Line left out (call 165); Osaka's `BRANCHES["UK"]` copied so the Umekita track beyond the city line draws as the Osaka Higashi Line, as on Osaka's map (step 1 walked 3,507 m); JR's and Hankyu's 吹田 apart; gate 3 exact on Hankyu's Senri Line (7).
- **Amagasaki: 7,385 storefronts, 12 stations.** The permit list and the notification list (call 164) of 2026-08-31 and the three registers: every count is the brief's (Food service 3,946 rows, Retail 893 + 1,295, laundries 368 through the foundation's `type_cols5`, which reads クリーニング種別１); 116 premises in both food lists fold to one pin; 2 unplaced (the brief's 5: the foundation's rules placed 3); census 1.93. The JR Kobe Line needs no branch walk (Nishinomiya's precedent). MHLW a control, not a source (Kawasaki's).
- **Uji: 1,281 storefronts, 12 stations.** MHLW's Kyoto Prefecture file cut to Uji by address (2,498 rows, the brief's); Food service 782 and Retail 624 rows, the brief's; block 94.3% through the foundation's `aza_insert` and `spelling5` (the brief: 55.0% without them), MHLW's own point for 74, 6 unplaced; census 1.79. **Rings halved** by the spacing rule: step 1 measured a 505 m median gap among the 12 in-city stations (the brief's 588 m counted by N02 group, folding JR's and Keihan's 宇治 and 木幡 into one each); Hiroshima's edges. 木幡 settled as Kohata (Kyoto's 西院 tie; the operators read it Kohata and Kowata) with operator suffixes. The Tōzai Line left out (calls 54 and 92).
- **Station names, Hiroshima's style:** Hirakata 1 (御殿山), Suita 2 (the Monorail's two), Amagasaki 1 (-mae), Uji none beyond the tie.
- **Privacy:** Hirakata, Amagasaki and Uji print 0 (1, 2 and 2 pins show their permit type); Suita prints 1 and is parked.
- **Licences:** each read today (the entry below); Uji's is MHLW's, recorded.

### 2026-10-07 - Toyonaka, Itami and Kakogawa built (Kansai-1, pages 222, 225, 226; notices 169, 172, 173)

- **Toyonaka: 5,277 storefronts, 10 stations.** The food list rebuilt BY PERMIT NUMBER (the brief's method, Maebashi's and Sakai's): the full list of 2026-03-31 (4,369 permits), plus the new permits of April to August 2026 (339; a number seen again replaces the earlier row), less 252 permits the closure files name (of 277 closure numbers; a closure applies only where it falls on or after that permit's grant), kept while 許可満了日 is on or after 2026-08-31 (130 dropped): **4,318, exactly the brief's.** The 生活衛生 register split by 業種 (barbers 237, beauty 736, laundries 231 with the bracketed kind as the type, so linen supply goes out by `japan_eigyo`'s rule; lodging, public baths and 興行場 out). MHLW's notifications as the partial Food-shops layer (1,367 rows; 488 without a published address), its own point where the join misses (89). Food service 2,957, Retail 1,127, Personal services 1,193 pins; block 96.9% of storefront rows, 4 unplaced. Names withheld 2; factory share 16 of 418 (3.8%), kept. Census control 2.27 (the brief's; no 業態, so konbini and canteens holding 飲食店営業 stay in Food service, Kobe's and Osaka's lists' way). Rail: 千里中央 joined (`GROUP_JOIN`, 257 m: staging applied Kawasaki's and Tokyo's precedent, 2026-10-06), 10 stations, 11 excluded beyond the line, median gap 1,102 m: standard rings; 79% of storefronts within a ring.
- **Itami: 2,383 storefronts, 6 stations; Kakogawa: 3,701 storefronts, 8 stations.** Hyōgo Prefecture's five lists cut BY ADDRESS (Tsu's shape: a row that begins 伊丹市 / 加古川市 once 兵庫県 is cut; an area licensed across several towns passed over; any other mid-address mention stops the build). The notifications are the Food-shops layer (owner, call 164). Itami: Food service 1,333, Retail 704, Personal services 454 rows, the brief's exactly; block 95.7%, 1 unplaced; census 2.17 (the brief's). Kakogawa: 1,970, 1,093, 787 rows, the brief's; block 87.8%, town center 11.9%, 11 unplaced (the tiers disclosed, call 145); census 2.16. The (4) その他 catch-all (40-42% of restaurants) stays in Food service: the list names no hostess venue (R3 applies only where a register names them). Rail: Itami's Osaka Monorail drawn cut at 大阪空港 (owner, call 163; the brief's "left out" predated it), JR and Hankyu 伊丹 kept apart with operator suffixes; Kakogawa's 宝殿 is Takasago's (38 m beyond the line).
- **Station names, Hiroshima's style:** Toyonaka 4 overrides (macrons; 柴原阪大前 as Shibahara-handai-mae); Itami 2 (新伊丹 hyphenated; 大阪空港, which OSM translates, romanized as Osaka-kuko, Fukuoka's 福岡空港 precedent); Kakogawa 1.
- **Line colours** from `line_colour_search.py`, starting from Osaka's, Kobe's and Himeji's colours where those maps draw the same line, so neighbouring maps agree.
- **Privacy:** `check_personal_exposure.py` prints 0 for each (Japan pass): Toyonaka 2 pins show their permit type (5 operator matches in the raw rows), Itami 1 (6), Kakogawa 2 (16, most of them unbucketed notifications).
- **The privacy check's Japan pass read a new city with no rules** (`frozenset(CITIES[slug].get("rules", ()))`, empty for an ALL_RULES city): fixed to `japan.city_rules(slug)`, the same one-line fix East-1 and Regional-1 made (coordinated, 2026-10-07).

### 2026-10-07 - Kansai-1's licence reads: five sources, all usable; two precedents applied (licence-read agents)

- **Brief checks first:** `brief_check.py` over the seven briefs, every data.bodik.jp request spaced 21 s through a wrapper (Kansai-1 is the only BODIK session): 92 of 92 claims hold.
- **Hyōgo Prefecture's 生活衛生課 lists (Itami, Kakogawa): the three registers PERMITTED WITH CONDITIONS.** Each XLSX has its own row in the prefecture's catalogue (`web.pref.hyogo.lg.jp/opendata/index.php`) with a CC BY licence; the catalogue terms (`kiyaku_opendata.pdf`) 3(3) license the works 「CCライセンス表示4.0国際」 unless noted, and 2(1) put them above the website's copyright page. The list page's own icon reads CC BY 2.1 JP, which also sits beside the 4.0 terms PDF itself (a stale site-wide icon); both are attribution-only. **MUST DISPLAY** the modified-work form, 「この地図は、以下の著作物を改変して利用しています。[タイトル]、兵庫県」, and CC BY 4.0's licence link and statement of change. **MUST NOT** present the edited data as the prefecture's (3(3)②), imply endorsement. No cost or indemnity clause; Japanese law, Kobe District Court.
- **Hyōgo's two food XLSX: AMBIGUOUS on the read, accepted on Ōtsu's precedent.** The catalogue lists only the page 食品関係営業施設リストの閲覧 (CC BY, format html, 「食品衛生法に係る営業許可施設及び営業届出施設の一覧です。」), not the files; the page holds nothing but the links to the two lists. Ōtsu's food list was catalogued the same way (the city's page under `cc-by`, its only content the list) and was accepted as CC BY 4.0 (owner, 2026-10-02). Precedent applied (process change 1); flagged for the owner at review time. Rejected: parking Itami and Kakogawa for an e-mail to the publisher (seikatsueiseika@pref.hyogo.lg.jp), which the precedent already answers.
- **Amagasaki City's food permit and notification lists and its three registers: PERMITTED WITH CONDITIONS.** Each op_data page (`/op_data/1000922/1001025` to `1001028`) states CC BY 4.0, and 尼崎市オープンデータ利用規約 (`/opendata/1000081/1000084.html`) §2 grants it unless a dataset says otherwise; use is acceptance (§1). The page the brief named (`1023309`) is only a character-encoding note. **MUST DISPLAY** (§3) the source and that it was modified; no wording prescribed. **MUST NOT** (§6) present edited data as the city's, or harm or defame the city or others. Cost: §6 and §7, damages and complaint costs from the user's own breach or infringement, the fault-based class accepted for all of Japan (2026-09-24). §5's use report is optional. The site's 著作権 page conflicts on its face; the open-data terms are the specific instrument for the catalogue (New York's specific-over-general shape), applied and flagged at review.
- **Hirakata City's food list and barber, beauty and laundry lists: PERMITTED WITH CONDITIONS, CC BY 2.1 JP.** The 利用条件 is printed on both dataset pages (`0000023479`, `0000025284`), scoped to 「本ページ」: free use and adaptation, derivative works allowed, a statement that the city's data is used. **MUST DISPLAY** the prescribed adaptation form, 「この地図は以下の著作物を改変して利用しています。[データのタイトル]、枚方市、クリエイティブ・コモンズ・ライセンス 表示 2.1」, and the licence URI (CC BY 2.1 JP 第5条); remove the credit if the city asks. The hold-harmless (caution 2: complaints from the user's breach or infringement settled at the user's cost) is the fault-based class. The site's 著作権 page covers web content and is conditioned on 「無断で」, which the pages' grant answers. **The site's linking policy** (`0000010379`) asks for an enquiry before a deep link and a notice of a top-page link: the credit cites the titles and the licence link and does not hyperlink the city's pages (MHLW's top-page-only precedent, applied more strictly), so neither arises; flagged at review time.
- **Suita City 衛生管理課's two food lists and its barber, beauty and laundry registers: PERMITTED WITH CONDITIONS, CC BY 4.0.** The dataset page marks both sections CC BY 4.0; 吹田市オープンデータ利用規約 (`opendata_kiyaku.pdf`, in force 2019-03-27) applies by use, and the terms page's scope rule makes a page's CC mark govern over the site's 著作権 page. **MUST DISPLAY** the prescribed modified-use form (2(3)), 「この地図は以下の著作物を改変して利用しています。【タイトル】、吹田市、クリエイティブ・コモンズ・ライセンス表示 4.0（https://creativecommons.org/licenses/by/4.0/deed.ja）」. **MUST NOT** (§5) present edited data as the city's, harm or defame the city or others, use its logo. The damages and claims clauses are fault-based. Links to data pages need no permission or contact (terms §3; the site's link page asks a courtesy notice, which the specific terms answer). The catalogue's own licence field for the five files was not seen (a form search).
- **Toyonaka City's BODIK datasets (`272035_food_business`, `272035_sanitation_business`): PERMITTED WITH CONDITIONS, CC BY 4.0.** 豊中市オープンデータ利用規約 (`https://odcs.bodik.jp/272035/tos/`, the same text as the city's PDF) １ allows any use, ２(1) applies CC BY 4.0; both packages record `cc-by-40-intl`. **MUST DISPLAY** a credit (２(2) gives an example, not a form: 「豊中市オープンデータ, 豊中市, クリエイティブ・コモンズ ライセンス表示 4.0 国際」 and the licence link) with the dataset titles and CC BY 4.0's statement of change. **MUST NOT** imply endorsement (CC BY 4.0 §2(a)(6)). No cost or indemnity clause; no governing law or precedence clause; the city's 著作権 page covers its web pages, and its open-data page carves the data out under CC. Four BODIK requests, each at least 23 s after the last.
- **The undefined harm and defamation bars** (Amagasaki §6, Suita §5) are recorded and flagged for the owner at review time (Taoyuan's undefined conditions were raised the same way); the build goes ahead on them, since nothing in a storefront map meets them while no operator's own name is shown.
