# DECISIONS drafts - Japan foundation (`worktree-japan-foundation`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-07 - The Japan foundation: every shared-code rule of the 58 Japanese briefs landed once, built maps unchanged

- **Landed in `pipeline/countries/japan_register.py`, `japan_step2.py`, `japan.py` and `pipeline/taxonomies/japan_eigyo.py`, in four groups, each followed by the Minato control (98.0 / 0.2 / 1.8 every time) and `drift_check.py` over the 34 built Japanese cities with `--jobs 3` (zero drift every time, about 3.5 min, peak 5.0 GB).** The checklist below names each rule's briefs. Group A's first run drifted Hiroshima's and Toyama's maps with every count unchanged: the circled-numeral strip ran in `_head`, which `xlsx_rows` applies to every CELL, so `㉕ そうざい製造業` lost its number. It moved to header cells only (`_header`), and both cities read zero drift.
- **Rules that touch no built map run everywhere** (a scan of the 34 built cities' raw rows found each trigger 0 times): 自動車以外 is no vehicle, the header circled numeral, the `NN:` and `?` type prefixes, 米殻類, the LinkData reader, the slash and Shōwa wareki forms, and the briefs' address, name, form and operator column spellings.
- **Rules that would move a built map are switches, `japan_register.WAVE5_RULES`.** A city outside `japan.BUILT_BEFORE_FOUNDATION` reads `ALL_RULES` by default, and `japan.py` refuses one that switches a rule off without a reason in `"rules_off"`. That includes the briefs' `"rules": WAVE2_RULES`, which predates the foundation. Rejected: one global switch per rule with each built city opted out by hand (34 entries to keep in step as rules are added).
- **Raising checks for the next city:** step 2 stops a new city whose source reads no address, no trade name, no food type, or an operator-like column `operator_cols()` does not compare (`config.NOT_OPERATOR` records one judged otherwise), and one whose permit term has no `config.TERM_AS_OF`. These are the traps Hirakata, Gifu, Tsu and Neyagawa found by hand.
- **Call 158, read with the earlier calls (precedent, process change 1):** a combined cell naming a public restaurant form stays Food service unless it names 給食 or 旅館. The vehicle, stall, hostess, entertainment, vending and mail-order exclusions also keep winning, each its own earlier owner call. Only the 仕出し and the deli and shop forms give way. On Fujisawa's cached lists that returns 70 catering and 30 deli rows (the brief: 69 and 27 on a 312-row filter; 316 here).
- **The owner's no-frequency-floor call (calls 46 and 86) added to the japan-city skill's standing calls** on Cleanup's relay of the owner's word; skill text only, no code (N02 has no timetable to check).
- **Each brief's figure reproduced on its cached file:** Uji 55.0% to 92.7% at the block (1,406 rows, exactly); Ichinomiya's barbers 82.3% to 93.3% (brief 93.0%); Takatsuki 19 unplaced to 3 (exactly); Okazaki 86.6% to 91.5% with O1 (92.7% in the brief with its city-local O2); Aomori 82.3% to 92.3%; Ōita's 301 withheld addresses and Aomori's 1,284 全域 rows exactly; Kure's 7 late starters (3 restaurants and 4 others); Tottori's four towns cut by address, 640 open rows (the brief: 644).

## The checklist (2026-10-07; every row landed except S30's optional items; the switches are named in `japan_register.WAVE5_RULES`)

Every "⚠️ Shared code" item in the Japanese briefs of `docs/build_plan_2026-10-07.md`'s
table (58 cities; Tama, Higashimurayama, Kasukabe, Toyonaka, Suita, Amagasaki,
Sagamihara, Urayasu, Sakura, Yachiyo, Ichihara, Ibaraki (Osaka), Minoh,
Moriguchi, Kadoma, Yao and Kanazawa name none), plus the owner's rules in
`docs/decisions_drafts/staging.md` (2026-10-06, calls 154-184), duplicates
merged. **Built** is what the 34 built Japanese cities' raw rows hold of the
rule's trigger (a scan, rows, 2026-10-07): zero means the rule is global;
anything else means a per-city switch, on for new cities and off for built ones.

| # | Rule | Briefs | Built | Where |
|---|---|---|---|---|
| S1 | 自動車以外 is not a vehicle (`自動車(?!以外)` in the vehicle test and the temporary words) | staging; Higashiyamato, Nishitōkyō, Fuchū (Tokyo), Chōfu, Tachikawa, Hino (1,063 rows across the Tama ledgers) | 0 | global |
| S2 | 露天 is a temporary word | staging; Kure | 3 (Hiroshima, Sakai, Takamatsu) | switch |
| S3 | 自動車 in a permit condition (許可条件) marks a vehicle | staging; Kure | 1,289 rows carry it (Tokyo, Hiroshima, Utsunomiya, Shimonoseki, Fukuoka, Kumamoto) | switch |
| S4 | An address of asterisks only is withheld by the publisher: counted apart, never parsed, out before de-duplication | staging; Kawaguchi (1,316), Ōita (301) | 1 (Fukuoka) | switch |
| S5 | 未選択 is no address | staging; Kure | 7 (Kagoshima, Okayama, Utsunomiya) | switch |
| S6 | An address of the city name alone is not a premises (call 162) | staging; Morioka (open call 3) | 1 (Tokyo) | switch |
| S7 | Area-wide addresses are not premises: 全域, 周辺, a prefecture-wide address (鳥取県内, 県内, 鳥取県東部, 鳥取県 alone), `<city>内` after a repeated city name | Takatsuki, Aomori, Kawaguchi (optional), Tottori | 全域 15, 周辺 108, 県内 763 | switch |
| S8 | A row addressed in another municipality is cut by its address, never by `CITY_BBOX` | Tottori, Ichinomiya, Ageo (Regional) | n/a (new-city check) | switch |
| S9 | 移動 in a personal-services address or name is not a premises | Maebashi | 9 | switch |
| S10 | Permits past their term are dropped (call 161); MHLW's lapsed permits | staging; Mito | yes (MHLW cities) | switch |
| S11 | A permit that starts after the as-of waits (call 172) | staging; Kure, Ageo (Regional), Sōka, Tokorozawa, Kasukabe | yes | switch |
| S12 | A combined 業態 cell naming a public restaurant form stays Food service unless it also names 給食 or 旅館 (call 158) | staging; Fujisawa (open call 1) | 3,386 combined cells | switch |
| S13 | Column spellings (ADDR, NAME, TYPE, FORM, OPERATOR) | Hirakata, Itami, Kakogawa, Maebashi, Fukuyama, Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu, Morioka, Koshigaya, Fujisawa, Funabashi, Matsudo, Ichikawa, Neyagawa, Shizuoka, Aomori, Matsue, Fuji, Matsumoto | TYPE: 245 (Matsuyama's クリーニング種別１); the rest 0 | global, TYPE switched |
| S14 | A header's leading circled numeral stripped (`①営業所名称`) | Itami, Kakogawa | 0 | global |
| S15 | A type's leading `NN:` code and a leading `?` (a circled number lost in cp932) stripped | Ageo (Regional), Sōka, Tokorozawa, Ōita | 0 | global |
| S16 | 米殻類販売 beside 米穀類販売 | Kawaguchi | 0 | global |
| S17 | `wareki_date` reads `R8/09/30`, `H01/08/18` and the Shōwa `S` | Maebashi; Ageo (Regional), Sōka, Gifu, Fuji, Koshigaya (optional) | slash 0; Shōwa 234 grant dates (Nara, Toyota) | global if drift is zero |
| S18 | `rebuilt_register`: two expiry spellings, rows with no end date kept (opt-in) | Fukuyama, Koshigaya, Iwaki | n/a (argument) | argument |
| S19 | A LinkData `.txt` reader in `city_rows` | Matsumoto | 0 | global |
| S20 | Every form column read (形態 beside 業態), 一般 skipped | Fukuyama, Itami, Kakogawa | n/a | switch |
| S21 | 字 left out after a short 大字 (`宇治妙楽` for MLIT's 宇治字妙楽) | Uji (a), Ichinomiya, Akita, Mito, Morioka, Matsumoto, Fukushima, Fuji (a) | join | switch |
| S22 | 小字 written in the address read as 字 | Takatsuki | join | switch |
| S23 | Spelling pairs: 蔵/藏, ノ/の, ッ/ツ, ケ/が, 之/の | Uji (b), Ichinomiya, Yamagata, Akita, Shizuoka, Ōita, Fuji (c), Matsumoto | join | switch |
| S24 | A town written with 町 that MLIT names bare (比奈町, 明磧) | Fuji (b), Ōita | join | switch |
| S25 | 大字 + 小字 丁目 (`康生通西4-5-6` for MLIT's 康生通字西4丁目) | Okazaki (O1) | join | switch |
| S26 | A 小字-centroid tier where MLIT lacks the number | Iwaki | join | switch |
| S27 | A 小字 written without its 大字, where it exists under one 大字 only | Fukushima, Aomori (浪岡), Yamagata (蔵王温泉) | join | switch |
| S28 | One page, several municipalities: a per-municipality ISJ ward key | Ageo (Regional) | n/a | new key |
| S29 | A city's own private-use glyphs, mapped before the join | Kawaguchi | n/a | per city table |
| S30 | Optional small spellings: 八雲村 → 八雲町, `―丁目` → `一丁目` (Matsue), a bracketed 字 (Gifu), 地割 (Morioka), 宮町 / 泉町 without 丁目 (Mito) | Matsue, Gifu, Morioka, Mito | join | switch |

City-local by their briefs, not shared: Okazaki's O2 (U+B743), Fujisawa's
laundry 種目, Matsue's repeated header row and mobile barber, Fuji's
monthly-file reading, Ichinomiya's and Fukushima's kind per file (`SOURCE_KIND`
exists).

S30 landed only Matsue's `―丁目` (in `spelling5`); Gifu's bracketed 字,
Morioka's 地割, Mito's 宮町 / 泉町 without 丁目, Matsue's 八雲村 and
Matsumoto's 湯の原 are each a few rows, optional in their briefs, and left
for a later city that needs them.

## Review-time re-render proposal (built maps, for the owner)

What each built city's step 2 gives with every WAVE5 rule switched on
(`write=False`, 2026-10-07), against its committed baseline. Nothing here is
applied: a built city stays on `WAVE2_RULES` until a review time re-renders
it. **The term rules (calls 161 and 172) are not in these figures:** no built
config pins a per-source as-of, so each city needs a `TERM_AS_OF` before they
can be measured.

| City | Storefronts | What moves |
|---|---|---|
| Toyota | 4,203 → 4,380 (+177) | unplaced 232 → 35 (the short-大字 字 rule, 145 at a 小字 centroid) |
| Kyoto | 32,370 → 32,389 (+19) | unplaced 426 → 407 |
| Nara | 4,801 → 4,820 (+19) | combined cells 79 (Food service +20), area-wide 19, the city name alone 1 |
| Tokyo | 61,317 → 61,297 (−20) | permit-condition vehicles 414 and area-wide 102 set aside (most already out), Retail −19 |
| Kobe | 27,259 → 27,277 (+18) | block 27,758 → 27,874, chōme 684 → 556 |
| Yokkaichi | 4,290 → 4,306 (+16) | combined cells 619 (Food service +8), unplaced 111 → 94 |
| Matsuyama | 9,329 → 9,337 (+8) | the type columns (クリーニング種別１), unplaced 41 → 33 |
| Toyama | 6,590 → 6,596 (+6) | unplaced 98 → 91 |
| Hiroshima | 13,691 → 13,686 (−5) | permit-condition vehicles 297 (most already out), combined cells 41 |
| Kurume | 3,067 → 3,071 (+4) | block 2,997 → 3,041 |
| Sakai, Nagasaki | +3 each | combined cells 73 / 8 |
| Utsunomiya, Takamatsu | −2 each | permit-condition vehicles 291 (Utsunomiya); area-wide 676 (Takamatsu, already out) |
| Fukui, Fukuoka, Kawasaki, Kitakyushu, Sapporo, Yokohama | ±1 | |
| Yokosuka | unchanged | names withheld 2 → 4 (the 法人名称 column) |
| Himeji, Kagoshima, Kumamoto, Nishinomiya, Ōtsu, Sasebo, Shimonoseki | unchanged | tiers only (Ōtsu's 646 area-wide rows were already out) |
| Hakodate, Hamamatsu, Higashiōsaka, Kōchi, Okayama, Osaka | unchanged | nothing |

*Recommend* re-rendering at the review time that lands the first A/B Japanese
cities: Toyota first (+177 placed, a real gain), then the rest in one batch,
each with a pinned `TERM_AS_OF`. Tradeoff: about 34 map re-renders and their
deploy-verify lane for changes mostly under 0.1% outside Toyota; leaving them
keeps built maps one rule set behind the new cities.

## Parked calls

None. Call 158's reading beside the earlier exclusions is a precedent
application (above), flagged here for the owner's review.
