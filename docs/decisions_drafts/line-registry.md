# DECISIONS drafts - Line registry (`line-registry`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

## Landing checklist

1. Re-render the 34 maps whose line colours change (render-only; the branch
   committed configs and code, not maps): amagasaki fukuoka hakodate
   higashimurayama higashiosaka himeji hirakata hiroshima itami kagoshima
   kakogawa kasukabe kawasaki kitakyushu kobe kurume kyoto mito nara
   nishinomiya nishitokyo oita osaka otsu sakai soka suita tama tokorozawa
   tokyo toyonaka uji yokohama yokosuka. On this branch the run took 0.76 GB
   at `--jobs 3`, and every one of the 34 drifted in `heatmap.html` only
   (baseline, provenance and excluded stations identical). The neighbour
   rule's two Seibu moves fall on Tokorozawa, already in the list, so the
   full list stays these **34 maps**.
2. After it: `python scripts/check_line_identity.py --rendered` must print
   PROBLEMS 0 (it did on this branch before `git checkout -- outputs/`, the
   neighbour rule on), and `check_map_markup.py` PROBLEMS 0 (it did).
3. No `app/` file changes: the app imports no city config, so no reboot.
4. Downstream: Visuals hears that 34 Japanese maps changed line colours
   (cards that show a line legend for any of them).

## The neighbour rule: decided (owner, 2026-10-07, "i agree with your recommendations")

See the entry "The neighbour rule on" below. The call as it was put:

Built and OFF (`check_line_identity.py --neighbours`). It would flag two
DIFFERENT lines on two maps, within 2 km of each other, drawn within CIE76 10
of one colour. With the registry's colours it finds **8 pairs, 5 line
pairs**:

- JR Musashino Line / JR Chuo Line, both `#F05820` (Fuchu and
  Higashimurayama against Hino and Tachikawa; 4 pairs). JR East colours both
  orange itself.
- Seibu Seibuen Line (Higashimurayama) / Seibu Sayama Line (Tokorozawa), both
  `#9040C0`.
- Seibu Tamako Line (Higashimurayama) / Seibu Yamaguchi Line (Leo Liner,
  Tokorozawa), both `#A06030`, the case the owner named.
- Midosuji Line (Osaka, `#E4151E`) / Kita-Osaka Kyuko Namboku Line (Suita and
  Toyonaka, `#E81820`), CIE76 1.2; the two through-run as one service and
  share Midosuji red (2 pairs).

*Recommend:* switch it on for the three Seibu and Musashino pairs only if the
reading is "one map read beside the next"; the Midosuji pair and the
Musashino/Chuo pair carry the operators' own sameness, which the per-map rule
already respects (`linecolour.dark_label_colours`: "two lines the agency
itself coloured alike are left alike"). *Tradeoff:* on, three colours move
on two Tama-area maps and Osaka-area red splits; off, a reader comparing
Higashimurayama with Tokorozawa sees two Seibu branches in one colour.

## Entries

### 2026-10-07 - The neighbour rule on: different lines meeting on neighbouring maps differ by at least 10; two Seibu lines moved on Tokorozawa; two pairs excepted (owner)

- **Decided (owner): two DIFFERENT lines that meet on neighbouring maps differ
  by at least `linecolour.HARD_FLOOR` (CIE76 10).** "Neighbouring" is
  adjacency measured on the committed polylines: the two drawn lines come
  within 2 km of each other (`NEIGHBOUR_M`) on two different maps. No shared
  station or Japan view is required; maps of two countries never come that
  close. Colours are the configs' (the legend's where no config names the
  line), so the rule holds before a re-render.
- **Decided: the two Seibu pairs separated by moving Tokorozawa's two lines,
  not Higashimurayama's.** Each side's nearest feasible move cost the same
  (12.4 and 12.6), and both on Tokorozawa means one map changes, already in
  the re-render list. Hue kept, each the nearest colour reading 3:1 on both
  pages, 45 from the pins, 12 from every line on its map and on every map
  within 2 km:
  - Seibu Yamaguchi Line (Leo Liner) `#A06030` to `#C87848`: pins 46.1,
    nearest line Seibu Ikebukuro 27.9, 12.4 from Higashimurayama's Seibu
    Tamako Line; contrast 5.56 dark, 3.37 light.
  - Seibu Sayama Line `#9040C0` to `#B060E8`: pins 66.0, nearest line Seibu
    Shinjuku 56.9, 12.6 from Higashimurayama's Seibu Seibuen Line; contrast
    5.07 dark, 3.69 light.
  The two are 99.9 apart on their own map; dark-mode labels separate, 5 of 5;
  the render's `check_line_colours()` and `check_map_markup.py` passed.
- **Decided (owner): two pairs left alike on purpose, in
  `line_registry.NEIGHBOUR_EXCEPTIONS` with their reasons:** JR Musashino /
  JR Chuo (`#F05820`, JR East's own orange for both; 4 map pairs) and
  Midosuji / Kita-Osaka Kyuko Namboku (`#E4151E` / `#E81820`, CIE76 1.2, one
  through service; 2 map pairs).
- **Decided: the rule is part of the gate.** `check_line_identity.py` check N
  fails any other pair; the `--neighbours` flag is gone. Result on this
  branch: PROBLEMS 0, 0 pairs, 6 excepted.

### 2026-10-07 - One colour per line on every map: a site-wide line registry, 48 lines made one colour on 34 maps, a check that fails a second colour (owner)

- **Decided (owner, hard line): a line drawn on more than one city's map has
  one colour on every map, distinct from the lines it meets on each map, even
  if other lines move to fit.** Before it, each Japanese city chose its colours
  alone (`scripts/line_colour_search.py`), so the JR Kobe Line was five
  colours on six maps and the JR Sanyo Line four on six.
- **Decided: identity is operator plus public line, never a display name.**
  Japan keys on MLIT N02's operator (`N02_004`, read through each config's
  `n02`, `route` and `BRANCHES`) and the line's public name; Korea, Taiwan and
  Brussels on their configs' line keys. Calls inside that rule: the JR
  Tokaido Line is two identities, JR East's (Kawasaki, Yokohama `#E07800`)
  and JR Central's (Gifu, Hamamatsu, Ichinomiya `#E86810`); the Tozai Lines of
  Kyoto, Sapporo and Tokyo, the Namboku Lines of Sapporo and Tokyo and the JR
  Takayama Lines of Gifu (JR Central) and Toyama (JR West) are different lines;
  the JR Sanyo Line is ONE identity although JR Kyushu runs Shimonoseki to
  Moji, because Shimonoseki's map draws both stretches over Kitakyushu's
  (6.3 km of shared track); through-services a map names differently are the
  line they run as: Yokohama's "JR Keihin-Tohoku / Negishi Line" is the JR
  Keihin-Tohoku Line, Tokyo's "JR Yokosuka / Sobu Rapid Line" the JR Yokosuka
  Line, and Tokyo's "JR Utsunomiya / Takasaki Line" one identity with
  Utsunomiya's JR Utsunomiya Line and Ageo's JR Takasaki Line (all three
  already `#E07800`). Rejected: N02's legal line as the key (it joins the JR
  Kobe and JR Sanyo Lines, which Himeji draws as two), and the display name
  alone (Tram 1 is fifteen different lines).
- **Found: 83 shared lines.** 71 Japanese (193 map entries on 57 maps), 11
  Korean (Seoul and its satellites, Busan with Gimhae; all already one
  colour), Taiwan's Airport MRT (Taipei, Taoyuan; one colour). Brussels
  (Regional) imports Brussels' `LINE_COLOURS`, so its 19 shared lines are one
  value already: an `INHERITED` record, not entries. A name and track scan of
  all 206 committed maps (same name over 500 m of shared track) found no
  other pair; every same-named pair elsewhere (Line 1, Tram 1, Linea 1,
  Metro A) is two networks.
- **Decided: `pipeline/line_registry.py` holds the 83, one entry each (name,
  operator, colour, `maps` = {city: config key}), with the colour's basis and
  margins in a comment.** Every config that draws one reads
  `line_registry.colour("<id>")` in place of its own value (73 configs); no
  step file, `map_common.py` or the renderer changed.
- **Decided: how each colour was chosen.** (1) One colour already on every
  map: kept (23 Japanese lines and every non-Japanese one). (2) Else the
  operator's own colour where it clears every constraint on every map and 45
  from the pins: five lines (JR West's JR Kobe Line `#0072BC`, JR Kyushu's
  Nippo `#0068B7`, JR East's Yokosuka `#0070B9`, Osaka Monorail `#0067B0`,
  Tokyu Meguro `#009CD2`). The Japanese maps draw olive, not Retail's blue,
  which is what lets the operators' blues back on. (3) Else the project
  colour one of its maps already drew that fits every map with the fewest
  other lines moved, ties to the colour more maps drew. (4) Else the colour
  nearest the operator's hue that fits (two: the JR Tsurumi Line `#A05000`,
  the Odakyu Tama Line `#2890D8`). Shared lines were placed most-crowded maps
  first. The constraints on every map: CIE76 >= 20 from each pin it draws,
  3:1 on both map pages, >= 10 from every other line (>= 12 for a pair this
  change creates; a pair left as it was keeps the old floor), >= 18 from
  every line within 500 m, and dark-mode labels that `dark_label_colours()`
  separates.
- **Why the operators' colours mostly could not be used**, measured: Hankyu
  maroon `#8C1C2D` reads 2.07:1 on the dark page; JR West's Takarazuka yellow
  `#F7A800` and Seibu's Ikebukuro yellow `#F5A200` read 1.99 and 2.09:1 on
  white; Kintetsu red `#E2001A` is CIE76 0.8 from the `#E00018` the Kintetsu
  Nagoya and Nara Lines already drew, so only one Kintetsu line per map can
  hold it; Hanshin blue `#0062B3` is 9.0 from the JR Kobe Line's blue it runs
  beside; the JR Kyoto Line shares the JR Kobe Line's operator blue and
  meets it at Osaka; Tokyu Toyoko `#DA0442` is 22.6 from Food service, under
  the 45 a new colour was held to.
- **Every shared line took one colour.** None had to stay split.

The 48 lines whose colour changed on at least one map (margins over every map
that draws the line; "lines beside it" = within 500 m):

| Line (identity) | Old colours (maps) | New | Basis | Margins over every map |
|---|---|---|---|---|
| Hankyu Itami Line (`hankyu-itami-line`) | `#A04820` amagasaki; `#C06038` itami | `#A04820` | project, kept from a map | pins >= 45.2, lines >= 21.4, lines beside it >= 21.4 |
| Hankyu Kobe Line (`hankyu-kobe-line`) | `#C87858` amagasaki; `#A36D66` kobe; `#985030` nishinomiya; `#C9785D` osaka | `#C9785D` | project, kept from a map | pins >= 45.0, lines >= 16.4, lines beside it >= 18.0 |
| Hankyu Kyoto Line (`hankyu-kyoto-line`) | `#905848` kyoto; `#87544B` osaka; `#885848` suita | `#87544B` | project, kept from a map | pins >= 45.9, lines >= 18.0, lines beside it >= 18.0 |
| Hankyu Senri Line (`hankyu-senri-line`) | `#BA7E7B` osaka; `#B88080` suita | `#BA7E7B` | project, kept from a map | pins >= 45.8, lines >= 18.0, lines beside it >= 18.0 |
| Hankyu Takarazuka Line (`hankyu-takarazuka-line`) | `#B7572D` osaka; `#C06038` toyonaka | `#B7572D` | project, kept from a map | pins >= 45.4, lines >= 18.1, lines beside it >= 18.2 |
| Hanshin Main Line (`hanshin-main-line`) | `#807878` amagasaki; `#3A6588` kobe; `#007890` nishinomiya; `#817B7B` osaka | `#3A6588` | project, kept from a map | pins >= 65.0, lines >= 16.8, lines beside it >= 19.6 |
| Hanshin Namba Line (`hanshin-namba-line`) | `#486860` amagasaki; `#4E665A` osaka | `#4E665A` | project, kept from a map | pins >= 45.7, lines >= 18.3, lines beside it >= 25.3 |
| JR Fukuhoku Yutaka Line (`jr-kyushu-fukuhoku-yutaka-line`) | `#F86000` fukuoka; `#A04820` kitakyushu | `#A04820` | project, kept from a map | pins >= 45.2, lines >= 18.3, lines beside it >= 18.3 |
| JR Gakkentoshi Line (`jr-west-gakkentoshi-line`) | `#C000A8` higashiosaka, hirakata; `#C303A8` osaka | `#C000A8` | project, kept from a map | pins >= 46.0, lines >= 19.9, lines beside it >= 19.9 |
| JR Hakodate Main Line (`jr-hokkaido-hakodate-main-line`) | `#28A800` hakodate; `#70A000` sapporo | `#70A000` | project, kept from a map | pins >= 24.5, lines >= 18.9, lines beside it >= 18.9 |
| JR Hanwa Line (`jr-west-hanwa-line`) | `#CF8400` osaka; `#B87808` sakai | `#CF8400` | project, kept from a map | pins >= 41.1, lines >= 18.0, lines beside it >= 18.0 |
| JR Hohi Main Line (`jr-kyushu-hohi-main-line`) | `#F05030` kumamoto; `#E80010` oita | `#F05030` | project, kept from a map | pins >= 46.3, lines >= 18.1, lines beside it >= 18.1 |
| JR Joban Line (`jr-east-joban-line`) | `#20A800` iwaki, tokyo; `#08A0C0` mito | `#20A800` | project, kept from a map | pins >= 45.7, lines >= 18.8, lines beside it >= 18.8 |
| JR Kagoshima Main Line (`jr-kyushu-kagoshima-main-line`) | `#E80010` fukuoka, kagoshima, kitakyushu, kumamoto; `#F05030` kurume | `#E80010` | project, kept from a map | pins >= 51.6, lines >= 18.1, lines beside it >= 18.1 |
| JR Keihin-Tohoku Line (`jr-east-keihin-tohoku-line`) | `#08A0C0` kawasaki, tokyo; `#207888` yokohama | `#08A0C0` | project, kept from a map | pins >= 50.6, lines >= 13.6, lines beside it >= 19.1 |
| JR Kobe Line (`jr-west-kobe-line`) | `#785870` amagasaki; `#08A0C0` himeji, kakogawa; `#0D51F2` kobe; `#7090A0` nishinomiya; `#755A75` osaka | `#0072BC` | operator | pins >= 82.7, lines >= 19.1, lines beside it >= 19.1 |
| JR Kosei Line (`jr-west-kosei-line`) | `#7098A8` kyoto; `#08A0C0` otsu | `#7098A8` | project, kept from a map | pins >= 49.6, lines >= 18.8, lines beside it >= 18.8 |
| JR Kyoto Line (`jr-west-kyoto-line`) | `#08A0C0` kyoto; `#4E6375` osaka; `#506878` suita | `#08A0C0` | project, kept from a map | pins >= 50.6, lines >= 17.5, lines beside it >= 18.8 |
| JR Nippo Main Line (`jr-kyushu-nippo-main-line`) | `#007890` kagoshima, oita; `#486878` kitakyushu | `#0068B7` | operator | pins >= 82.3, lines >= 37.2, lines beside it >= 40.4 |
| JR Osaka Higashi Line (`jr-west-osaka-higashi-line`) | `#A088A0` higashiosaka, suita; `#A28DA8` osaka | `#A088A0` | project, kept from a map | pins >= 57.3, lines >= 18.8, lines beside it >= 22.5 |
| JR Sanyo Line (`jr-west-sanyo-line`) | `#007890` fukuyama, okayama, shimonoseki; `#406878` himeji; `#E80010` hiroshima; `#808080` kitakyushu | `#007890` | project, kept from a map | pins >= 51.4, lines >= 15.8, lines beside it >= 18.8 |
| JR Takarazuka Line (`jr-west-takarazuka-line`) | `#A8903C` amagasaki, itami, kobe; `#C88800` nishinomiya | `#A8903C` | project, kept from a map | pins >= 20.1, lines >= 19.5, lines beside it >= 35.2 |
| JR Tsurumi Line (`jr-east-tsurumi-line`) | `#C08800` kawasaki; `#909800` yokohama | `#A05000` | searched near the operator hue | pins >= 45.2, lines >= 15.2, lines beside it >= 24.4 |
| JR Tōzai Line (`jr-west-tozai-line`) | `#F820C0` amagasaki; `#FF21C0` osaka | `#FF21C0` | project, kept from a map | pins >= 45.1, lines >= 19.9, lines beside it >= 19.9 |
| JR Yamatoji Line (`jr-west-yamatoji-line`) | `#20A800` nara; `#12A500` osaka | `#12A500` | project, kept from a map | pins >= 45.0, lines >= 18.1, lines beside it >= 18.1 |
| JR Yokosuka Line (`jr-east-yokosuka-line`) | `#406878` kawasaki; `#9888A0` tokyo; `#586878` yokohama; `#08A0C0` yokosuka | `#0070B9` | operator | pins >= 82.5, lines >= 12.7, lines beside it >= 23.4 |
| Keihan Main Line (`keihan-main-line`) | `#787858` hirakata; `#506C30` kyoto; `#7B7B5A` osaka | `#7B7B5A` | project, kept from a map | pins >= 37.3, lines >= 16.4, lines beside it >= 18.0 |
| Keikyu Main Line (`keikyu-main-line`) | `#E81820` kawasaki, yokohama, yokosuka; `#C80008` tokyo | `#E81820` | project, kept from a map | pins >= 45.5, lines >= 13.3, lines beside it >= 18.1 |
| Keio Line (`keio-line`) | `#B030D0` chofu, fuchu_tokyo, hino, tama; `#E060D0` tokyo | `#B030D0` | project, kept from a map | pins >= 64.6, lines >= 16.6, lines beside it >= 29.8 |
| Kintetsu Kyoto Line (`kintetsu-kyoto-line`) | `#E80010` kyoto, uji; `#F85838` nara | `#F85838` | project, kept from a map | pins >= 46.4, lines >= 12.2, lines beside it >= 18.2 |
| Kintetsu Osaka Line (`kintetsu-osaka-line`) | `#B83008` higashiosaka; `#B43009` osaka; `#F85838` tsu | `#F85838` | project, kept from a map | pins >= 46.4, lines >= 16.5, lines beside it >= 18.3 |
| Midōsuji Line (`osaka-metro-midosuji-line`) | `#E4151E` osaka; `#E81820` sakai | `#E4151E` | project, kept from a map | pins >= 45.1, lines >= 16.5, lines beside it >= 18.0 |
| Nankai Kōya Line (`nankai-koya-line`) | `#B18D06` osaka; `#B09000` sakai | `#B09000` | project, kept from a map | pins >= 23.2, lines >= 20.5, lines beside it >= 20.5 |
| Nankai Main Line (`nankai-main-line`) | `#9F6900` osaka; `#E07800` sakai | `#9F6900` | project, kept from a map | pins >= 30.4, lines >= 18.0, lines beside it >= 18.0 |
| Nishitetsu Tenjin Omuta Line (`nishitetsu-tenjin-omuta-line`) | `#688090` fukuoka; `#E80010` kurume | `#688090` | project, kept from a map | pins >= 54.0, lines >= 18.3, lines beside it >= 83.7 |
| Odakyu Odawara Line (`odakyu-odawara-line`) | `#588898` kawasaki; `#687888` tokyo | `#687888` | project, kept from a map | pins >= 56.4, lines >= 10.3, lines beside it >= 19.6 |
| Odakyu Tama Line (`odakyu-tama-line`) | `#686878` kawasaki; `#08A0C0` tama | `#2890D8` | searched near the operator hue | pins >= 77.0, lines >= 12.7, lines beside it >= 35.1 |
| Osaka Metro Chuo Line (`osaka-metro-chuo-line`) | `#606828` higashiosaka; `#5D662A` osaka | `#5D662A` | project, kept from a map | pins >= 23.3, lines >= 18.5, lines beside it >= 28.3 |
| Osaka Monorail Main Line (`osaka-monorail-main-line`) | `#007890` itami, toyonaka; `#108098` suita | `#0067B0` | operator | pins >= 81.9, lines >= 37.6, lines beside it >= 37.6 |
| Sanyo Electric Main Line (`sanyo-electric-main-line`) | `#D01810` himeji, kakogawa; `#D01911` kobe | `#D01810` | project, kept from a map | pins >= 45.4, lines >= 18.9, lines beside it >= 18.9 |
| Seibu Haijima Line (`seibu-haijima-line`) | `#805878` higashimurayama; `#08A0C0` higashiyamato, tachikawa | `#08A0C0` | project, kept from a map | pins >= 50.6, lines >= 48.5, lines beside it >= 48.5 |
| Seibu Ikebukuro Line (`seibu-ikebukuro-line`) | `#D08000` nishitokyo, tokorozawa; `#E86800` tokyo | `#D08000` | project, kept from a map | pins >= 43.0, lines >= 11.0, lines beside it >= 22.5 |
| Seibu Shinjuku Line (`seibu-shinjuku-line`) | `#08A0C0` higashimurayama, nishitokyo, tokorozawa; `#906888` tokyo | `#906888` | project, kept from a map | pins >= 48.3, lines >= 12.1, lines beside it >= 23.7 |
| Tobu Skytree Line (`tobu-skytree-line`) | `#08A0C0` kasukabe, soka; `#007890` tokyo | `#007890` | project, kept from a map | pins >= 51.4, lines >= 10.2, lines beside it >= 32.1 |
| Tokyu Den-en-toshi Line (`tokyu-den-en-toshi-line`) | `#207078` kawasaki; `#789090` tokyo; `#486860` yokohama | `#789090` | project, kept from a map | pins >= 45.7, lines >= 10.1, lines beside it >= 18.6 |
| Tokyu Meguro Line (`tokyu-meguro-line`) | `#0088A0` kawasaki; `#8890A0` tokyo | `#009CD2` | operator | pins >= 64.2, lines >= 13.6, lines beside it >= 23.4 |
| Tokyu Oimachi Line (`tokyu-oimachi-line`) | `#D87830` kawasaki; `#D07020` tokyo | `#D07020` | project, kept from a map | pins >= 49.2, lines >= 11.8, lines beside it >= 18.3 |
| Tokyu Toyoko Line (`tokyu-toyoko-line`) | `#C80808` kawasaki; `#E84028` tokyo; `#C03008` yokohama | `#C03008` | project, kept from a map | pins >= 46.7, lines >= 14.6, lines beside it >= 18.3 |

ALREADY ONE COLOUR (23, kept, now registered): Hankai Line `#449418` (osaka, sakai); Ise Railway Ise Line `#9840A0` (tsu, yokkaichi); JR Biwako Line `#406878` (kyoto, otsu); JR Chuo Line `#F05820` (hino, tachikawa, tokyo); JR Kyudai Main Line `#30A800` (kurume, oita); JR Musashino Line `#F05820` (fuchu_tokyo, higashimurayama, tokorozawa); JR Nambu Line `#B09000` (fuchu_tokyo, kawasaki, tachikawa, yokohama); JR Nara Line `#A87840` (kyoto, uji); JR Ou Line `#E07800` (akita, fukushima); JR Tohoku Line `#007430` (fukushima, morioka); JR Tokaido Line `#E07800` (kawasaki, yokohama); JR Tokaido Line `#E86810` (gifu, hamamatsu, ichinomiya); JR Utsunomiya / Takasaki Line `#E07800` (ageo_regional, tokyo, utsunomiya); JR Yosan Line `#08A0C0` (matsuyama, takamatsu); Keihan Keishin Line `#949054` (kyoto, otsu); Keihan Uji Line `#20A800` (kyoto, uji); Keio Sagamihara Line `#F000B8` (chofu, kawasaki, tama); Kintetsu Nagoya Line `#E00018` (tsu, yokkaichi); Kintetsu Nara Line `#E00018` (higashiosaka, nara); Kita-Osaka Kyuko Namboku Line `#E81820` (suita, toyonaka); Meitetsu Nagoya Main Line `#E80010` (gifu, ichinomiya); Sotetsu-JR Link Line `#805878` (kawasaki, yokohama); Tama Toshi Monorail `#E07800` (higashiyamato, hino, tachikawa).

| Map | Unshared line | Old | New | Pins | Nearest line | Nearest beside it |
|---|---|---|---|---|---|---|
| hiroshima | JR Kabe Line | `#007890` | `#506870` | 53.3 | JR Sanyo Line 18.8 | 18.8 |
| kyoto | Tōzai Line | `#E85820` | `#D84810` | 52.3 | Kintetsu Kyoto Line 12.2 | 46.5 |
| nishinomiya | Hanshin Mukogawa Line | `#586878` | `#788898` | 55.0 | Hanshin Main Line 20.1 | 20.1 |
| nishinomiya | Hankyu Imazu Line | `#D08068` | `#905848` | 45.7 | Hankyu Kobe Line 19.5 | 19.5 |
| nishinomiya | Hankyu Koyo Line | `#D06840` | `#D87040` | 49.1 | Hankyu Kobe Line 18.0 | 18.0 |
| osaka | Yotsubashi Line | `#00A2C3` | `#4898D0` | 67.8 | JR Kyoto Line 18.8 | 18.8 |
| osaka | Kintetsu Namba Line | `#FC5D3F` | `#B83008` | 45.7 | Kintetsu Osaka Line 18.7 | 18.7 |
| tokyo | Marunouchi Line | `#E81020` | `#F80008` | 58.4 | Keikyu Main Line 13.3 | 23.5 |
| tokyo | Tokyu Setagaya Line | `#C08800` | `#D86008` | 60.2 | JR Utsunomiya / Takasaki Line 12.2 | 83.5 |
| tokyo | Seibu Toshima Line | `#D08000` | `#F86800` | 67.0 | JR Chuo Line (Rapid) 12.5 | 27.1 |
| tokyo | Keikyu Airport Line | `#F81808` | `#F84800` | 61.9 | JR Chuo Line (Rapid) 12.0 | 19.1 |
| tokyo | Tsukuba Express | `#B83008` | `#A04820` | 45.2 | Fukutoshin Line 13.7 | 20.2 |
| yokohama | Blue Line | `#08A0C0` | `#007088` | 53.2 | Tokyu Kodomonokuni Line 13.4 | 19.1 |
| yokohama | Tokyu Kodomonokuni Line | `#688898` | `#486878` | 55.7 | Blue Line 13.4 | 18.6 |

- **Decided (as the owner allows): 14 unshared lines on 7 maps moved so the
  shared colours fit, hue kept where it could be.** Each city's config
  records its own moves with these margins. Tokyo swapped two Seibu oranges
  (its Ikebukuro Line takes the `#D08000` Nishitokyo and Tokorozawa drew, its
  Toshima Line moves to `#F86800`) and its Tokyu Setagaya Line left yellow
  for orange `#D86008`: Tokyo's yellows (Chuo-Sobu `#B09000`, Yurakucho
  `#A89060`) leave no other room. The Seibu Ikebukuro Line is held at its
  orange by hand (`FORCE` in the search): the search's alternative was
  salmon `#D08068` on all three maps, off the operator's hue.

- **Trades, recorded:** eight shared lines sit between 20 and 45 from a pin,
  each a project colour some map already drew and now drawn on every map of
  the line: JR Takarazuka `#A8903C` 20.1 (owner-accepted 2026-10-07), Nankai
  Koya `#B09000` 23.2, Osaka Metro Chuo `#5D662A` 23.3, JR Hakodate Main
  `#70A000` 24.5 (Sapporo's; Hakodate drew `#28A800`), Nankai Main `#9F6900`
  30.4, Keihan Main `#7B7B5A` 37.3, JR Hanwa `#CF8400` 41.1, Seibu Ikebukuro
  `#D08000` 43.0. Pairs this change created under 12.5 (none within 500 m of
  each other): on Tokyo, JR Utsunomiya / Takasaki and Seibu Ikebukuro 11.0
  (11.3 before), JR Chuo and Keikyu Airport 12.0, JR Utsunomiya / Takasaki
  and Tokyu Setagaya 12.2, Tokyu Oimachi and Tokyu Setagaya 12.4; on
  Kawasaki, JR Tokaido and Tokyu Oimachi 12.0; on Kyoto, Kintetsu Kyoto and
  Tozai 12.2.
- **Decided: `scripts/check_line_identity.py`, in `check_all.py`.** It fails
  when a registered line's config colour differs from its entry, when an
  inherited page's line differs from its parent's, and when two maps draw what
  looks like one line (the same name, a line code allowed, over 500 m of
  shared track; or one Japanese operator's line under one public name in two
  configs) with no entry joining them or `NOT_SAME` parting them.
  `--rendered` also compares the committed legends (off in the gate: a config
  change reaches a map at its next render). `--neighbours` turns on the
  neighbour rule. Verified: PROBLEMS 0 on this branch (83 lines, 73 maps, 187
  same-name shared-track pairs, all joined); with the 34 maps re-rendered,
  `--rendered` PROBLEMS 0, `check_map_markup.py` PROBLEMS 0, every render's
  `check_line_colours()` passed, `check_all.py` 51 of 51. A negative control
  (one member dropped from the JR Kobe Line and from Line 4, one colour
  changed) failed it with 92 problems.
- **Fixed in passing:** Kobe's config carried a dead duplicate of its
  station-scope block (a second `LINES = {` holding the two funiculars and a
  repeated `COLLAPSE_MAX_SPREAD_M`), overwritten at import since 2026-09-27;
  removed, since the registry edit has to find the real `LINES`.
