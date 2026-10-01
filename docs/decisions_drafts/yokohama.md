# DECISIONS drafts - branch `yokohama` (Band B build session)

Kept here under the owner's rule of 2026-09-30 (relayed by the tram kit
session): build sessions keep their entries in their own drafts file, and the
cleanup session folds every drafts file into `DECISIONS.md` in one pass. Newest
first, each entry exactly as it should land.

### 2026-09-30 - A new category value, "Personal services only", for Yokohama (owner)

The site's "Why the maps differ" page reads each city's `categories` from
`app/cities.py`, from a closed vocabulary in `scripts/check_inconsistency_list.py`.
None of its values described Yokohama, whose page shows barbers, beauty salons and
laundries and no food: the nearest, "Food premises only", is the food-only case.
Asked, the owner chose **"Personal services only"** (recommended over a generic
"One category"), tiered `one_bucket` like "Food premises only". Added to `FIELDS`
and `TIER_OF` with a dated comment. `check_macro_facts.py` needed no change: table
B's pins cell `— / — / 6,540` is a single figure, which it already reads as one
bucket.

### 2026-09-30 - Yokohama built: personal services only, on the shared Japanese steps

**Built** on branch `yokohama` (from `origin/master`, `origin/macro-legend` merged
first), page 81, region East Asia, not in the default frame. Band B (owner,
2026-09-29): the first page not built on food, under the amended rule 1, and the
page says the city publishes no food list. Downloads and page prose under the
owner's pre-approval (2026-09-30). **7,843 storefronts**, 6,540 within the 0.6 mi
rings (83.4%), **140 stations on 20 lines**. `coverage` one_bucket, `categories`
"Personal services only" (entry above), `mode` metro, `record_kind` "Permit
registers", `rail_extra` "Suburban rail".

**Business leg.** The city's 環境衛生関係施設一覧 as of 2026-04-01: barbers 1,512,
beauty 5,091, laundries 1,293 (7,896 rows; the brief's figure, not the 17,408 of
2026-09, reproduced). The three zips are byte-identical to the city's copies of
2026-09-30. Each holds 18 ward CSVs (UTF-16 LE, TAB-separated); the shared
`japan_register.city_rows` reads only zipped `.xlsx`, so `config.source_rows` reads
the members city-locally (Kyoto's hook) and `fetch_sources.py` overrides only the
shared fetch's city part. **No shared join code changed**, so the Minato control
was not re-run. One city-local rule: the kind of premises is in 詳細業種, while
業種 repeats the register's name, so 詳細業種 is the type the taxonomy reads - that
is what catches 美容所(移動) (3 salons in vehicles) and 無店舗取次店 (20 pick-up
services with no shop). 24 rows have no fixed place (those, and 市内一円 laundries);
25 repeat registrations are shown once.

**One clock (the snapshot case).** The registers record no closures. The page
also publishes each month's new premises since (新規, 2026-04 to 2026-09: about
170 barbers, salons and laundries, 2% of the register) but no closures, so they are
not added: the register stays one snapshot, dated 2026-04-01, and the page says a
dot may have closed since. `bill` and the other five zips are not personal-services
storefronts.

**Placement.** The shared MLIT join: 7,712 at the block (98.0%), 156 at the
town-chōme centre, 4 unplaced (a building name holding 丁目, 六ッ川, 子安通り).

**Rail.** MLIT N02 on Japan's standing rule, cut at the city line. 20 lines: the
Blue Line (N02's 1号線 + 3号線) and Green Line; JR East's 東海道線 drawn as four
services, each a `route` (Tokyo's precedent) - the Keihin-Tohoku Line (with 根岸線
as the Negishi Line), the Tokaido, the Yokosuka (over the Hinkaku track via 新川崎)
and the Sotetsu-JR Link Line (羽沢横浜国大 to 武蔵小杉 on the freight track, checked:
17.6 km, 42 m from 鶴見, never near 横浜) - plus the Yokohama, Nambu and Tsurumi
lines; Keikyu Main and Zushi; Tokyu Toyoko, Den-en-toshi, Kodomonokuni and
Shin-yokohama; Minatomirai; Sotetsu Main, Izumino and Shin-yokohama; the Kanazawa
Seaside Line (N02 class 24, drawn as Kobe's Port Liner). The JR Nambu Line keeps
one station inside (矢向, 1 of 30), kept as cut on Kobe's JR Takarazuka Line
precedent. **140 stations** (the brief said 138): 大船's JR platform lies inside the
city line (Sakae ward), and a station counts when any platform is inside (Osaka's
太子橋今市, owner 2026-09-27). Gate 3 exact on seven lines (Blue 31, Green 10,
Seaside 14, Minatomirai 6, Kodomonokuni 3, Tokyu and Sotetsu Shin-yokohama 3 each).
Close pairs read and kept: Tsunashima / Shin-Tsunashima 145 m, the JR and Keikyu
Higashi-Kanagawa 164 m, the JR and Keikyu Shinkoyasu 171 m (separate stations). 41
stations beyond the line are excluded. Median gap 857 m: standard rings.

**Station names** follow the operators' signs, Tokyo's style (owner 2026-09-28):
one override, 大船 "Ōfuna" to "Ofuna" (the city's only macron), and one alias, N02's
鶴ヶ峰 for OSM's 鶴ケ峰. **Line colours** from `scripts/line_colour_search.py
yokohama`: all 20 clear 45 from the pins; closest pair within 500 m 18.0 (Blue /
Keihin-Tohoku), anywhere 12.4 (Kodomonokuni / Seaside Line, 17 km apart).

**Personal exposure: PASS.** `check_personal_exposure.py yokohama` (Japan pass):
the operator's own name shown as a trade name on 0 of 7,843 rows; person-like
name at a residential unit 0 of 6,540 pins. The name rule compared every row
(申請者氏名 filled on all 7,896, read in memory only): none is exactly the
operator's name; 4 trade names contain the operator's full name plus a business
word, which the owner's rule shows. 申請者役職 and 施設電話番号 are never read.

**Licence.** CC BY 4.0 (read 2026-09-30 by the `licence-read` agent): the city's
prescribed credit for a modified work, with an English gloss, in notice 69.
MLIT's credits as in Kobe's. **Macro label**: width 68.8 px (measured 2026-09-30,
controls reproduced); the dot sits 2 px from Tokyo's, so the pill goes right of it
and above Tokyo's, ("start", 12, -42), clear from dy -34 to -56; PROBLEMS 0 on the
combined tree.

**Left for others.** Regenerating `docs/japan_city_list.md` also moved Tokyo's
Taitō (5,779 to 4,830) and Meguro (2,022 to 1,999) food counts, drift unrelated
to Yokohama; only Yokohama's row was taken, and the drift is reported to the
cleanup session. The same table still shows Hiroshima in Band C; Hiroshima's
build updates it.
