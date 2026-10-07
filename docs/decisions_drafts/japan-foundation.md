# DECISIONS drafts - Japan foundation (`worktree-japan-foundation`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

## The checklist (working copy, 2026-10-07)

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

## Parked calls

(none yet)
