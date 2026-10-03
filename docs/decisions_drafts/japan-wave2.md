# DECISIONS drafts - Japan wave 2 (`japan-wave2-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Japan wave 2: the shared-code pass, gated so no built city moves

- **Every wave-2 brief's shared-code item landed in one pass, and the new
  join rules are switched on per city: the fourteen wave-2 cities opt in
  (`japan.CITIES[...]["rules"] = japan_register.WAVE2_RULES`), the 20 built
  Japanese cities do not.** Measured first with every rule global: the rules
  moved nine built cities, mostly for the better (unplaced rows: Fukuoka
  92 -> 29, Hiroshima 152 -> 7, Kumamoto 62 -> 14, Matsuyama 84 -> 63;
  Kōchi 13 rows chōme -> block), and Fukuoka's "福岡市内" rows (3) became
  "not a premises". The kit requires the built cities' drift checks to stay
  clean, and a built city's output changes only at a review time that
  re-renders it, so each rule is named and opt-in: `oaza` (a 大字 dropped on
  both sides: Yokkaichi, Shimonoseki), `aza_letter` (字甲 read as 甲:
  Takamatsu), `kou_bare` (Himeji's 甲 / 乙 / 丙 地番, the bare town's number
  where MLIT gives it one place, its centroid where the number's rows lie
  over 500 m apart), `chome_missing` (Toyota's 浄水町1-5丁目 at the 大字
  centroid), `machi` (Nara's 宝来町一丁目 / 宝来1丁目 and 北京終 / 北京終町),
  `citywide` (Kurume's 「久留米市内」 rows are not premises) and `form_cols`
  (業態 read from 業態, Yokosuka's 詳細業種 or Sasebo's 種目). Turning them
  on for the built cities is a separate, measured option for review time.
- **Unconditional (they moved no built city):** column spellings
  (`ADDR_COLS` +6, `NAME_COLS` +5, `TYPE_COLS` + 営業種目 and 区分,
  `OPERATOR_COLS` +11); `wareki_date` reads Sasebo's `R 8. 5.31`;
  `japan_eigyo` reads Kawasaki's 飲食店（sub-type） with its carve-outs
  (給食施設, 学校給食炊飯, まあじゃん屋等, 短期営業), takes そうざい店 and a
  leading そうざい屋 to Retail (the そう菜店 precedent), reads Nara's old-law
  restaurant sub-types (軽飲食, 一般食堂, 居酒屋 and ten more; the first
  listed decides a combination) and 簡易菓子製造業; `rebuilt_register()`
  (Higashiōsaka's full list plus months: 7,067 rows read, 6,709 after
  de-duplication, 6,521 in term on 2026-08-31, the brief's figures exactly);
  `japan_step2.datum_guard()` stops `OWN_POINT_FALLBACK` on a publisher whose
  points sit a median over 200 m from the block point (Higashiōsaka's Tokyo
  Datum, 448 m); `japan_fetch.current_url()` reads a renamed file's current
  link from its page (`SOURCE_LINKS`: Kawasaki, Ōtsu) or a CKAN resource's
  current URL (`SOURCE_RESOURCES`: Yokosuka, Toyota);
  `japan_step1.n03_municipalities()` also reads `config.N03_NEIGHBOR_PREFS`'
  N03 files, so a station beyond the prefecture line is named, not filed as
  "another prefecture" (Kawasaki's 27 in Tokyo; opt-in, so Kitakyushu's
  Shimonoseki row is unchanged).
- **Proven:** `drift_check.py` on the 20 built Japanese cities, run through
  the heavy-job gate on this code: **zero drift**, every baseline unchanged
  (measured peak 4.54 GB). A step-2 snapshot of the same 20 cities, old code
  against new, was byte-identical too.
- **Two kit items held at the built cities' reading, a cross-city call for
  the owner at review time:** `複合型そうざい製造業` stays out (the import-time
  pin) and a deli by its 業態 alone (総菜屋, 惣菜店, そうざい屋 as the form of a
  restaurant permit) stays Food service. Counting them moved eight built
  cities (Kobe 8, Kyoto 6, Osaka 12, Sapporo 10, Sakai 12 and 4, Kagoshima 2,
  Okayama 1, Fukui 1; about 55 pins). The wave-2 rows they touch: Himeji 3,
  Kawasaki 6, Yokosuka 5 and its 総菜屋 29, Sasebo's 飲食店惣菜 5.
- **Nara's ケ/ヶ fix needed nothing new**: `VARIANTS` already reads ヶ as ケ;
  the brief's examples (杉ケ中町, 秋篠梅ケ丘町) are towns MLIT's file lacks.
- **The Minato control reproduces** (block 98.0 / chōme 0.2 / none 1.8), and
  each wave-2 city's tiers on fixed premises in a bucket
  (`screen_japan_join.py <slug> --bucketed`, new) match or beat its brief:
  Kawasaki 98.7 / 1.3 / 0.0, Yokosuka 96.5 / 3.4 / 0.1, Himeji 81.6 / 18.3 /
  0.2 (brief 79.4 / 17.9 / 2.7 before its rule), Nishinomiya 99.0 / 1.0 /
  0.0, Takamatsu 88.7 / 11.1 / 0.2, Toyota 78.5 / 16.2 / 5.3, Yokkaichi
  88.8 / 8.9 / 2.4, Ōtsu 94.7 / 5.3 / 0.0, Nara 89.2 (old-law) and 89.5
  (registers, brief 88.6), Hamamatsu 94.9 / 5.1 / 0.0, Higashiōsaka 99.6 /
  0.4 / 0.0, Kurume 87.5, Sasebo 88.5 (MHLW) and 90.5 (old law), Shimonoseki
  88.1 / 11.3 / 0.6.
