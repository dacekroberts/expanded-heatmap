# DECISIONS drafts - Kansai-1 (`worktree-japan-kansai-1`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

Cities, in build order (`docs/build_plan_2026-10-07.md`): Toyonaka (page
222), Hirakata (223), Suita (224), Itami (225), Kakogawa (226), Amagasaki
(227), Uji (228); notices 169-175.

## Parked calls

None yet.

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
