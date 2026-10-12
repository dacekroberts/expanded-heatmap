# Commercial-use positions

Audit of 2026-10-12, by Cleanup, with the owner's rulings of the same day.
**This is a reading of licence terms and of this project's own record, not
legal advice.** It is not rendered on any public page of the site; keep it
that way unless the owner says otherwise.

## What this file answers

One question per source: **may a third party use this data commercially,
and on what condition.** The answer serves the transit-globe project's
decisions. This site stays non-commercial, so nothing here changes what the
site publishes, and no row is a reason to add or remove a city.

- The unit is a licence position: one licence document or recorded position,
  with the sources and cities under it. Method and verdict shapes:
  `.claude/skills/commercial-use-audit/SKILL.md`.
- **The weakest source in use decides a city's column.** Every source that
  places a pin counts: registers, address and parcel layers, geocoders,
  boundary files, rail geometry.
- A source whose terms never address commercial use is held, never assumed
  allowed.
- Each row's quoted sentence, where it was settled from and the reason are
  in `docs/commercial_use_reads_2026-10-12.md`, under the same Id. That file
  also lists what could not be read.
- A verdict is dated. A source re-read later gets a new row, never an edit
  to an old one: the new row's Id is the old Id plus "+1" (EW-13+1 replaces
  EW-13), and only the newest row of an Id counts toward the city table.

## Summary

Derived by `scripts/commercial_use_cities.py`; do not edit between the marks.

<!-- summary:start -->
237 cities: 2 blacklisted, 36 held, 45 allowed if left out, 154 allowed.

- **Blacklisted** (2): Philadelphia, Seattle (Regional).
- **Held** (36): Chicago, Miami (Regional), São Paulo, Rio de Janeiro (Regional), Belo Horizonte (Regional), Brasília, Salvador, Fortaleza (Regional), Porto Alegre (Regional), Recife (Regional), Santos (Regional), Daegu, Stockholm, Bucharest, Sacramento, Tucson, Dallas, Okayama, Kurume, Shimonoseki, Brussels (Regional), Tacoma, Higashiyamato, Nishitōkyō, Tama, Higashimurayama, Fuchū (Tokyo), Chōfu, Tachikawa, Hino, Uji, Yao, Takatsuki, Cluj-Napoca, Tottori, Kure.
- **Allowed if left out** (45): San Diego, San Francisco, Los Angeles (Regional), New York, Boston, Washington D.C., Vancouver (Regional), Paris, Amsterdam, Monterrey (Regional), Fukuoka, Tokyo, Den Haag, Palma, Hiroshima, Matsuyama, Toyama, Kumamoto, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Kagoshima, Takamatsu, Ōtsu, Nara, Sasebo, Ageo (Regional), Sōka, Tokorozawa, Kasukabe, Toyonaka, Hirakata, Suita, Maebashi, Fukuyama, Ichinomiya, Akita, Ōita, Mito, Morioka, Okazaki, Yamagata, Koshigaya, Fujisawa.
<!-- summary:end -->

The columns: **allowed** (every source permits commercial use, almost always
with attribution; read the Condition cells), **allowed if left out** (allowed
once the named layer is dropped or replaced), **held** (a source in use is
silent, not established, or held by the owner's ruling, and the map does not
stand without it), **blacklisted** (a source in use forbids commercial use
and the map does not stand without it).

## The owner's rulings, 2026-10-12

| Source | Ruling | Row |
|---|---|---|
| Japan's health ministry food list (MHLW) | Held. Eight cities have no other register and are held outright; the rest stand without its rows | JA-G5 |
| Tokyo's Tama ledgers | Held, and stated: permitted only on a reading of the Tokyo catalogue's section 3 that the owner does not rest on. The eight cities on the ledgers have no other register | JA-G7 |
| French municipal boundaries (geo.api.gouv.fr) | Permitted, recorded under the stricter ODbL condition | EW-8 |
| Daegu's own datasets | Held, with the national route noted | AN-4 |
| Brazil's address file (IBGE CNEFE) | Held | AU-P7 |
| Philadelphia's register, limits and assessment data | Blacklisted | HC-44 |
| Busan's datasets | Permitted with condition, the art. 14(2) doubt noted | AN-3 |
| Korea's small-business register (SEMAS) | Permitted with condition, both doubts noted | AN-5 |
| Geneva's register (SITG) | Permitted with condition; no resale, a paid data tier being the exposed case | EW-24 |
| Palma: the Balearic register | Permitted with condition | EW-18 |
| Palma: the national cadastre's addresses | Held; Palma is allowed if that address layer is replaced | EW-28 |
| Paris: the timetable feed | Held for the feed; the station and line reference layers are permitted | EW-7 |
| Brussels (Regional): the company register (KBO) | Allowed only under the app's own registration; held as a hand-on from this project | EW-27 |
| Hong Kong | Permitted, the uncapped indemnity stated prominently. The owner's rider: if an app design would make every user accept that indemnity site-wide, hold Hong Kong instead. As read, the indemnity binds the party that reproduces the data (the app's operator), not the app's users | AN-7, AN-8, AN-9 |
| New York City's three datasets; the US Census files | Permitted and flagged: no sentence names commercial use | HC-23, HC-25, HC-26, AU-P10, AU-S4 |
| Thessaloniki, after its full read the same day | Allowed with condition, the harvester-default doubt noted. Replaces the "held, confirmed" in the next line for Thessaloniki only | EW-13+1 |
| Thessaloniki, Stockholm, Bucharest, Cluj-Napoca, Miami, Chicago, Tucson, Sacramento, Tacoma, Dallas | Held, confirmed | EW-13, AN-25, AN-28, AN-29, HC-45, HC-44a, HC-48, AU-P22, AU-P16, AU-P23, AU-P15 |

Not ruled one by one, and recorded as the reads left them: Seattle
(Regional), where two layers forbid commercial use (AU-P18, AU-S1) and the
rest are held, so the rule puts it in the blacklisted column; the cities
whose only weak source is a rail feed, a permit register or one local list
(the "allowed if left out" column); the Saitama 生活衛生 page, where two
passes disagreed and the weaker reading stands (JL-L36b); the national
boundary file (JA-G4).

## What the reads corrected in this project's record

To be carried into the country files under `docs/data_sources/`.

- MHLW's clause is about commercial reuse (免責 2) ウ), not personal data.
- MLIT's N02 rail file is CC BY 4.0 on its own pages; the record says PDL
  1.0. Either permits.
- MLIT's N03 page does not say that users need the survey agency's approval;
  that was this project's inference. It matters only if a boundary is drawn.
- e-Stat's terms say 「商用利用も可能です」.
- Palma's "no alteration" line is about the information's content, not
  derived maps.
- San Diego's Business Tax Certificates page now links PDDL.
- MTR's station lists carry no licence field, but DATA.GOV.HK's terms reach
  every dataset on the portal.
- King County's open-data terms are at data.kingcounty.gov/terms and are
  silent on commercial use.
- 13 of the 16 sources with no licence on record have one on the publisher's
  page today (rows marked "none recorded").
- Stale pointers: line references in the korea-city skill and
  `docs/licence_positions.md`; `docs/licenses/README.md` says no French or
  Brazilian city is built; Monterrey's map PDF has no source row; the Census
  geocoder's rows disagree.

## Source table

One row per licence position. `Verdict` is the verdict after the owner's
ruling, with the read's own verdict in brackets where they differ. `Stands
without it` names the cities whose map still stands if the source is dropped
or replaced. The Id's letters name the pass that read it (JA and JL Japan,
EW western Europe, AN Asia and the north, AU the Americas and the United
Kingdom, HC the hand count).

### Japan, cities A to K, and Japan's national layers

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| JA-G1 | OpenStreetMap | ALL | PERMITTED, CONDITION | allowed | Also read as JL-S1, EW-1, AN-1, AU-P1, HC-5. | ODbL 1.0: attribution; share-alike on a derived database; a produced work carries the notice | ODbL 1.0 |   |
| JA-G2 | MLIT 位置参照情報 (街区 24.0a, 大字・町丁目 19.0b) | Kobe; Osaka; Sapporo; Fukuoka; Kyoto; Tokyo; Yokohama; Matsuyama; Toyama; Kumamoto; Fukui; Nagasaki; Utsunomiya; Kitakyushu; Sakai; Hakodate; Kagoshima; Okayama; Kōchi; Kawasaki; Yokosuka; Himeji; Nishinomiya; Takamatsu; Toyota; Yokkaichi; Ōtsu; Nara; Hamamatsu; Higashiōsaka; Kurume; Sasebo; Shimonoseki; Higashiyamato; Nishitōkyō; Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino; Sōka; Tokorozawa; Kasukabe; Toyonaka; Hirakata; Suita; Itami; Kakogawa; Amagasaki; Uji; Maebashi; Fukuyama; Ichinomiya; Tsu; Fukushima; Iwaki; Akita; Ōita; Gifu; Mito; Morioka; Ibaraki (Osaka); Minoh; Moriguchi; Kadoma; Neyagawa; Yao; Takatsuki; Shizuoka; Kanazawa; Okazaki; Aomori; Matsue; Fuji; Matsumoto; Tottori; Yamagata; Kure; Kurashiki; Naha; Koshigaya; Sagamihara; Fujisawa; Kawaguchi; Funabashi; Matsudo; Ichikawa; Urayasu; Sakura; Yachiyo; Ichihara | PERMITTED, CONDITION | allowed | Also read as JL-N3, HC-14. | PDL 1.0: source credit, edits stated, never presented as MLIT's own | 国土数値情報ダウンロードサイト 利用規約, in force 2026-03-23, `https://nlftp.mlit.go.jp/ksj/other/agreement.html`; MLIT's FAQ `https://nlftp.mlit.go.jp/ksj/other/faq.html` |   |
| JA-G3 | MLIT N02 鉄道データ (N02-24, N02-25) | Kobe; Osaka; Sapporo; Fukuoka; Kyoto; Tokyo; Yokohama; Hiroshima; Matsuyama; Toyama; Kumamoto; Fukui; Nagasaki; Utsunomiya; Kitakyushu; Sakai; Hakodate; Kagoshima; Okayama; Kōchi; Kawasaki; Yokosuka; Himeji; Nishinomiya; Takamatsu; Toyota; Yokkaichi; Ōtsu; Nara; Hamamatsu; Higashiōsaka; Kurume; Sasebo; Shimonoseki; Higashiyamato; Nishitōkyō; Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino; Sōka; Tokorozawa; Kasukabe; Toyonaka; Hirakata; Suita; Itami; Kakogawa; Amagasaki; Uji; Maebashi; Fukuyama; Ichinomiya; Tsu; Fukushima; Iwaki; Akita; Ōita; Gifu; Mito; Morioka; Ibaraki (Osaka); Minoh; Moriguchi; Kadoma; Neyagawa; Yao; Takatsuki; Shizuoka; Kanazawa; Okazaki; Aomori; Matsue; Fuji; Matsumoto; Tottori; Yamagata; Kure; Kurashiki; Naha; Koshigaya; Sagamihara; Fujisawa; Kawaguchi; Funabashi; Matsudo; Ichikawa; Urayasu; Sakura; Yachiyo; Ichihara | PERMITTED, CONDITION | allowed | Also read as JL-N3, HC-15. | CC BY 4.0 (the page's own label): attribution, changes indicated. The site terms would give PDL 1.0 with the same duties | The N02 dataset pages, `https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2024.html` and `...-N02-2025.html`, field 「このデータの使用許諾条件」 |   |
| JA-G4 | MLIT N03 行政区域 (N03-2025) | Kobe; Osaka; Sapporo; Fukuoka; Kyoto; Tokyo; Yokohama; Hiroshima; Matsuyama; Toyama; Kumamoto; Fukui; Nagasaki; Utsunomiya; Kitakyushu; Sakai; Hakodate; Kagoshima; Okayama; Kōchi; Kawasaki; Yokosuka; Himeji; Nishinomiya; Takamatsu; Toyota; Yokkaichi; Ōtsu; Nara; Hamamatsu; Higashiōsaka; Kurume; Sasebo; Shimonoseki; Higashiyamato; Nishitōkyō; Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino; Sōka; Tokorozawa; Kasukabe; Toyonaka; Hirakata; Suita; Itami; Kakogawa; Amagasaki; Uji; Maebashi; Fukuyama; Ichinomiya; Tsu; Fukushima; Iwaki; Akita; Ōita; Gifu; Mito; Morioka; Ibaraki (Osaka); Minoh; Moriguchi; Kadoma; Neyagawa; Yao; Takatsuki; Shizuoka; Kanazawa; Okazaki; Aomori; Matsue; Fuji; Matsumoto; Tottori; Yamagata; Kure; Kurashiki; Naha; Koshigaya; Sagamihara; Fujisawa; Kawaguchi; Funabashi; Matsudo; Ichikawa; Urayasu; Sakura; Yachiyo; Ichihara | PERMITTED, CONDITION (read: a split) | allowed | Read as a split: commercial use is allowed under CC BY 4.0 for the use made (choosing stations by municipality); reproducing the boundary geometry is NOT ESTABLISHED. No map draws it, so it decides no city. Re-read before any boundary is drawn. Also read as JL-N4, HC-12. | For the use made: CC BY 4.0 attribution, changes indicated. For the geometry: a Survey Act question that the licence does not answer | N03-2025 page, `https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2025.html`; MLIT site terms 1.3 (same URL as G2); GSI 承認申請Q&A Q1-24, `https://www.gsi.go.jp/LAW/2930-qa.html` (linked from MLIT's terms 1.2 through `2930-index.html`) |   |
| JA-G5 | MHLW 食品衛生申請等システム | Fukuoka; Tokyo; Hiroshima; Matsuyama; Toyama; Kumamoto; Nagasaki; Utsunomiya; Kitakyushu; Sakai; Kagoshima; Okayama; Takamatsu; Nara; Kurume; Sasebo; Shimonoseki; Higashiyamato; Nishitōkyō; Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino; Toyonaka; Hirakata; Suita; Uji; Maebashi; Fukuyama; Ichinomiya; Akita; Ōita; Mito; Morioka; Yao; Takatsuki; Okazaki; Tottori; Yamagata; Kure; Koshigaya; Fujisawa | HELD | held | Held (owner, 2026-10-12): the terms page applies PDL 1.0, and its disclaimer 2) ウ has the user agree not to reuse the information for profit. Also read as JL-N2, HC-51. | none while held | i2fas.mhlw.go.jp/termsofuse.htm, sections 2 and 3; the PDL 1.0 text at digital.go.jp | Fukuoka, Tokyo, Hiroshima, Matsuyama, Toyama, Kumamoto, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Kagoshima, Takamatsu, Nara, Sasebo, Higashiyamato, Nishitōkyō, Tama, Higashimurayama, Fuchū (Tokyo), Chōfu, Tachikawa, Hino, Toyonaka, Hirakata, Suita, Maebashi, Fukuyama, Ichinomiya, Akita, Ōita, Mito, Morioka, Okazaki, Yamagata, Koshigaya, Fujisawa = the MHLW rows |
| JA-G6 | e-Stat (衛生行政報告例 第10表 and 第11表; 2021 Economic Census) | Matsuyama; Toyama; Kumamoto; Fukui; Nagasaki; Utsunomiya; Kitakyushu; Sakai; Hakodate; Kagoshima; Okayama; Kōchi; Kawasaki; Yokosuka; Himeji; Nishinomiya; Takamatsu; Toyota; Yokkaichi; Ōtsu; Nara; Hamamatsu; Higashiōsaka; Kurume; Sasebo; Shimonoseki; Higashiyamato; Nishitōkyō; Sōka; Tokorozawa; Kasukabe; Minoh; Kadoma; Neyagawa; Yao; Takatsuki; Shizuoka; Kanazawa; Okazaki; Aomori; Matsue; Fuji; Matsumoto; Tottori; Yamagata; Kure; Kurashiki; Naha; Koshigaya; Sagamihara; Fujisawa; Kawaguchi | PERMITTED, CONDITION | allowed | Also read as JL-N1. | 政府標準利用規約 2.0 form: source credit, edits stated, never presented as the state's own | 政府統計の総合窓口（e-Stat）利用規約, `https://www.e-stat.go.jp/terms-of-use` |   |
| JA-G7 | Tokyo Tama ledgers (食品関係営業台帳, 環境衛生施設台帳) | Higashiyamato; Nishitōkyō; Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino | HELD (read: PERMITTED, CONDITION) | held | Held (owner, 2026-10-12): permitted only if the Tokyo catalogue's terms (section 3) override the host site's personal and non-profit policy; the owner does not rest on that reading. If section 3 is not accepted the answer is FORBIDDEN. Also read as JL-L39, HC-11. | none while held | Tokyo Open Data Terms, section 3; the host site's policy (see the reads file) |   |
| JA-G8 | Akita City | Akita | PERMITTED, CONDITION | allowed |   | CC BY 4.0: attribution, changes indicated | Mark on each XLSX (`jp.md:510`) |   |
| JA-G9 | Amagasaki City | Amagasaki | PERMITTED, CONDITION | allowed |   | CC BY 4.0; the terms' §6 bars on harm and defamation | Each dataset page and 尼崎市オープンデータ利用規約 §2 (`jp.md:504`) |   |
| JA-G10 | Aomori City | Aomori | PERMITTED, CONDITION | allowed |   | CC BY 4.0; the terms' credit form | Dataset page (`jp.md:517`) |   |
| JA-G11 | Fujisawa City | Fujisawa | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' 3(3) credit | 藤沢市オープンデータライブラリ, `https://www.city.fujisawa.kanagawa.jp/kyoso/shise/kekaku/kakushu/datalibrary.html`, and its 利用規約 (`.../documents/13230/riyoukiyaku20250401.pdf`) 3(2) |   |
| JA-G12 | Fukui City | Fukui | PERMITTED, CONDITION | allowed |   | **Share-alike**: CC BY-SA, version not named by the city. Attribution, and an adaptation shared only under the same licence | 福井市サイトポリシー 1 著作権, `https://www.city.fukui.lg.jp/sisei/kohou/hp/site-p.html` |   |
| JA-G13 | Fukushima City | Fukushima | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP: the terms' 2(3) credit; the terms' cost clauses 3 and 4 | 福島市オープンデータ利用規約 ２(２), `https://www.city.fukushima.fukushima.jp/material/files/group/7/opendatariyokiyaku_2.pdf` |   |
| JA-G14 | Hakodate City | Hakodate | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP | Statement on the list page (`jp.md:474`) |   |
| JA-G15 | Hamamatsu City | Hamamatsu | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP: the terms' credit form | 浜松市オープンデータ利用規約 第1条, `https://www.city.hamamatsu.shizuoka.jp/koho2/opendata/kiyaku.html`; the portal top (`.../api/odpf/opendata/v1?m=top`) |   |
| JA-G16 | Himeji City | Himeji | PERMITTED, CONDITION | allowed |   | CC BY 4.0 | Each dataset's `license_id: CC-BY-4.0` (`jp.md:480`) |   |
| JA-G17 | Hirakata City | Hirakata | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP: the pages' credit form | 利用条件 printed on both dataset pages (`jp.md:499`) |   |
| JA-G18 | Hiroshima City | Hiroshima | PERMITTED, CONDITION | allowed |   | Attribution, edits stated (CC BY mark on the city page, version not shown; PDL 1.0 on the catalogue) | The city page (`https://www.city.hiroshima.lg.jp/business/shokuhin-eisei/1051268/1051957.html`); the city's オープンデータの取組の推進に関する基本方針 (`.../shisei/gyosei/1021856/1006054/1027540/1018955.html`); catalogue resource `https://hiroshima-opendata.dataeye.jp/resources/25502` |   |
| JA-G19 | Ichinomiya City | Ichinomiya | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' credit form | Mark on each CSV (`jp.md:508`) |   |
| JA-G20 | Iwaki City | Iwaki | PERMITTED, CONDITION | allowed |   | CC BY 4.0 (the general open-data page's 2.1 JP has the same duties) | The two dataset pages |   |
| JA-G21 | Kagoshima City | Kagoshima | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' prescribed credit | 鹿児島市オープンデータ利用規約 １, `https://www.city.kagoshima.lg.jp/ict/documents/riyoukiyaku.pdf` |   |
| JA-G22 | Kawaguchi City | Kawaguchi | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP; the page's own rider (no use that infringes human rights or threatens safety) | The open-data page, `https://www.city.kawaguchi.lg.jp/shiseijoho/ict_johoka/2/12182.html` |   |
| JA-G23 | Kawasaki City | Kawasaki | PERMITTED, CONDITION | allowed |   | CC BY (2.1 JP by the terms, 4.0 by the page badge): credit naming both | Both dataset pages; 川崎市オープンデータ利用規約 §2 (`jp.md:478`) |   |
| JA-G24 | Kobe City | Kobe | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP | Badge on each CSV (`jp.md:462`) |   |
| JA-G25 | Kōchi City | Kōchi | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' processed-use credit | The page's 【オープンデータ利用ルール】 (`jp.md:477`) |   |
| JA-G26 | Koshigaya City | Koshigaya | PERMITTED, CONDITION | allowed |   | PDL 1.0: the portal's processed-use credit | Saitama portal resources `https://opendata.pref.saitama.lg.jp/resources/2715` and `.../resources/6312` (datasets 530 and 2004, creator the city's own 生活衛生課) |   |
| JA-G27 | Kumamoto City | Kumamoto | PERMITTED, CONDITION | allowed |   | PDL 1.0 (restaurant list); CC BY 4.0 (the three lists; BODIK says PDL 1.0): one credit meets both | The four dataset pages; catalogue terms `https://odcs.bodik.jp/431001/tos/` |   |
| JA-G28 | Kurashiki City | Kurashiki | PERMITTED, CONDITION | allowed |   | CC BY 4.0: source and a statement of editing | Page 1004977 (`jp.md:524`, read 2026-10-08) |   |
| JA-G29 | Kanazawa City | Kanazawa | PERMITTED, CONDITION | allowed |   | CC BY, version not given: the terms' 2(2) four-item credit | Dataset record, `https://catalog-data.city.kanazawa.ishikawa.jp/dataset/172014-syokuhineisei-kyokashisetsu`; 金沢市オープンデータ利用規約 2(1), `https://portal-data.city.kanazawa.ishikawa.jp/pdf/opendata_rule.pdf` |   |
| JA-G30 | Funabashi City | Funabashi | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' credit form | Each dataset's `cc-by-40-intl` (`jp.md:496`) |   |
| JA-G31 | Osaka Prefecture | Ibaraki (Osaka); Kadoma | PERMITTED, CONDITION | allowed |   | CC BY 4.0 | Both dataset pages (`jp.md:502`) |   |
| JA-G32 | Kitakyushu City | Kitakyushu | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' 第6条 credit | 北九州市オープンデータ利用規約 第1条, `https://odcs.bodik.jp/401005/tos/`; the three dataset pages |   |
| JA-G33 | Fukuoka City | Fukuoka | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' 第７条 credit | Fukuoka's terms 第１条, `https://odcs.bodik.jp/401307/tos/`; the four dataset pages on `data.bodik.jp` (`401307_insyokuteneigyoutoueigyoukyokasisetuitiran`, `401307_riyousyo_kensakakuninzumi`, `401307_biyousyo_kensakakuninzumi`, `401307_cleaning`) |   |
| JA-G34 | Higashiōsaka City | Higashiōsaka | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' credit form | Dataset `license_id: cc-by-40-intl` (`jp.md:488`) |   |
| JA-G35 | Fukuyama City | Fukuyama | PERMITTED, CONDITION | allowed |   | Attribution, edits stated (CC BY, versionless, on the records; PDL 1.0 by the terms) | Both dataset pages; catalogue terms `https://data.city.fukuyama.hiroshima.jp/terms` |   |
| JA-G36 | Kyoto City | Kyoto | PERMITTED, CONDITION | allowed |   | CC BY 4.0; the portal's name in the credit | Every resource page (`jp.md:526`) |   |
| JA-G37 | Gifu City (on Gifu Prefecture's catalogue) | Gifu | PERMITTED, CONDITION | allowed |   | CC BY 2.0: attribution, licence notice kept; the catalogue terms' credit form | Both dataset pages (`https://gifu-opendata.pref.gifu.lg.jp/dataset/c212016-072`, `.../c212016-075`); CC BY 2.0 legal code, `https://creativecommons.org/licenses/by/2.0/legalcode`, section 3 |   |
| JA-G38 | Chiba Prefecture | Ichikawa; Ichihara | PERMITTED, CONDITION | allowed |   | PDL 1.0: processed-use credit; cite the open-data site only | Every resource records `pdl` (`jp.md:497`) |   |
| JA-G39 | Shizuoka Prefecture | Fuji | PERMITTED, CONDITION | allowed |   | CC BY 4.0: the terms' modified-use credit | Portal terms, `https://opendata.pref.shizuoka.jp/privacy.html`; the dataset pages |   |
| JA-G40 | Saitama Prefecture | Ageo (Regional); Kasukabe | PERMITTED, CONDITION | allowed | Covers the food layers only here. The two passes disagreed on the 生活衛生 page (a0706); the weaker reading is recorded once, in row JL-L36b. | PDL 1.0: the portal terms' §1.1 processed-use credit | GIS catalogue page, `https://portal-pref-saitama.hub.arcgis.com/pages/opendatacatalog` (rendered in a browser; the page is script-built); portal terms `https://opendata.pref.saitama.lg.jp/pages/terms`; portal resource `https://opendata.pref.saitama.lg.jp/resources/5028` (dataset 1343) |   |
| JA-G41 | Hyōgo Prefecture | Itami; Kakogawa | PERMITTED, CONDITION | allowed |   | CC BY 4.0 by the catalogue terms (the register files' own icon reads CC BY 2.1 JP): the terms' 3(3) credit | Catalogue terms 3(3), `https://web.pref.hyogo.lg.jp/kk26/johoseisaku/documents/kiyaku_opendata.pdf`; the catalogue, `https://web.pref.hyogo.lg.jp/opendata/index.php`; the register page |   |

### Japan, cities L to Z

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| JL-L01 | Tokyo catalogue, ward packages | Tokyo | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; Tokyo terms §2(1)イ: say it was modified, never as if Tokyo or a ward made it | Tokyo Open Data Terms §2, §3; each package's `license_id` |   |
| JL-L02 | Shibuya ward terms | Tokyo | PERMITTED, CONDITION | allowed |   | Attribution in the terms' form (「…を加工して作成」); terms change without notice | The ward's open-data site statement; 渋谷区オープンデータ利用規約 (recorded read 2026-09-24, jp.md:449); item `licenseInfo` |   |
| JL-L03 | Taitō ward licence page | Tokyo | PERMITTED, CONDITION | allowed |   | The ward's four credit elements (台東区; CC-BY表示4.0国際; the no-warranty sentence; the source URL) | Ward licence page `opd.html`; Tokyo catalogue entry `t131067d3100000006`; stored `docs/licenses/taito-opendata-guideline.pdf.txt` |   |
| JL-L04 | Setagaya ward terms | Tokyo | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the ward's §2 form | CC BY 4.0 badge on each file (jp.md:451) |   |
| JL-L05 | Meguro BODIK | Tokyo | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; catalogue link labelled (第9項) | `cc-by-40-intl` on every package (jp.md:452) |   |
| JL-L06 | Osaka City pages | Osaka | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution (「…を加工して作成」) | Each source page's own notice |   |
| JL-L07 | Matsuyama | Matsuyama | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the site's form; 第5条 repayment on the user's own breach | Open-data site's CC licence section |   |
| JL-L08 | Mito dataset label | Mito | PERMITTED, CONDITION | allowed |   | Attribution, licence credited as the city writes it ("CC-BY", no version) | The dataset page's licence row |   |
| JL-L09 | Morioka | Morioka | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; CSVs only (the page's XLSX and PDF are not open); §4 repayment on breach | Both dataset pages state 表示4.0国際 (jp.md:515) |   |
| JL-L10 | Nara | Nara | PERMITTED, CONDITION | allowed |   | CC BY 2.1 JP attribution | Each page (jp.md:486) |   |
| JL-L11a | Ōtsu registers (BODIK) | Ōtsu | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the ４(2) form; ６ and ８ fault-based | 大津市オープンデータ利用規約 １, ４(1); package `license_id: cc-by` |   |
| JL-L11b | Ōtsu food list (city site) | Ōtsu | NOT ESTABLISHED | held |   | (if permitted: as L11a) | Same terms, ２; the catalogue entry; the city's copyright page | Ōtsu = the city-site food list |
| JL-L12 | Sakai | Sakai | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the 3-3 form; 5 and 8 fault-based | 堺市オープンデータ利用規約 3-2; the list page's own open-data paragraph; BODIK `cc-by-40-intl` on the standing list (record) |   |
| JL-L13 | Suita | Suita | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; §5 bars harm or defamation of the city or others (undefined) | Page marks both sections CC BY 4.0 (jp.md:500) |   |
| JL-L14 | Yamagata | Yamagata | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; clause 4: the user repays the city's costs arising from use, uncapped, not fault-based | Dataset page (jp.md:523) |   |
| JL-L15 | Yokohama | Yokohama | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the city's form | Dataset page declares CC BY 4.0 (jp.md:527) |   |
| JL-L16 | Maebashi | Maebashi | PERMITTED, CONDITION | allowed |   | Attribution naming CC BY 4.0 (food) and both CC BY 2.1 JP and 4.0 (registers); remove the credit if the city asks (2.1 JP 第5条) | Package `license_id`; 前橋市オープンデータ利用規約 第１条 |   |
| JL-L17 | Yokosuka | Yokosuka | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; fetch from the catalogue only | `cc-by-40-intl` on both (jp.md:479) |   |
| JL-L18 | Shizuoka City | Shizuoka | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution | 静岡市 open-data terms on BODIK; package `license_id: cc-by` |   |
| JL-L19 | Okazaki | Okazaki | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; 5(5): claims arising from use settled at the user's cost, uncapped, not purely fault-based | `cc-by-40-intl`; 岡崎市 terms 3(2) (jp.md:518) |   |
| JL-L20 | Toyota | Toyota | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the 3(2) form; 4(6) and 5 | `license_id` on both packages; catalogue terms 3(2) |   |
| JL-L21 | Mie Prefecture | Tsu | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution | `cc-by-40-intl` on each (jp.md:509) |   |
| JL-L22 | Yokkaichi | Yokkaichi | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution | `cc-by-40-intl` on each (jp.md:484) |   |
| JL-L23 | Osaka Prefecture | Minoh; Moriguchi | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution | Both dataset pages state CC BY 4.0 (jp.md:502) |   |
| JL-L24 | Toyonaka | Toyonaka | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution | `cc-by-40-intl` on both (jp.md:498) |   |
| JL-L25 | Neyagawa | Neyagawa | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the terms' 記載例 | All three packages marked CC BY 4.0 (jp.md:503) |   |
| JL-L26 | Nagasaki | Nagasaki | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; BODIK copies only (the city's own current list is not permitted and not used) | `cc-by-40-intl` on each (jp.md:470) |   |
| JL-L27 | Sasebo | Sasebo | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, 第3条(2)(イ) form | `cc-by-40-intl` (jp.md:489) |   |
| JL-L28 | Ōita | Ōita | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, the §1 form with the date of use | `cc-by-40-intl` on each (jp.md:511) |   |
| JL-L29 | Naha | Naha | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; BODIK copies only; 第5項 costs | Each package declares CC BY 4.0 (jp.md:525) |   |
| JL-L30 | Matsumoto | Matsumoto | PERMITTED, CONDITION | allowed |   | Attribution naming CC BY 4.0 (city terms) and CC BY 3.0 (table headers); §6(5) and LinkData Art.18(4): claims arising from use at the user's cost, uncapped, partly not fault-based | 松本市オープンデータ利用規約; each table's `#license` header (jp.md:522) |   |
| JL-L31 | Toyama | Toyama | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution, 第１条２(2) form | Portal terms 第１条１; package `license_id: cc-by`, extra `ライセンス: CC-BY` |   |
| JL-L32 | Sagamihara | Sagamihara | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; no framing of the catalogue; re-read the terms before each refresh | The city's open-data page for the catalogue; 相模原市オープンデータ利用規約 3(2) (recorded read 2026-10-04) |   |
| JL-L33 | Nishinomiya | Nishinomiya | PERMITTED, CONDITION | allowed |   | PDL 1.0: 出典 line, and a separate line saying who processed it | 西宮市オープンデータ利用規約 第2.0版, １ |   |
| JL-L34 | Chiba Prefecture | Matsudo; Urayasu; Sakura; Yachiyo | PERMITTED, CONDITION | allowed |   | PDL 1.0 credit; cite and fetch from the open-data site only | Every resource records `pdl` (jp.md:497) |   |
| JL-L35 | Takamatsu | Takamatsu | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution; 第４条(3) fault-based | 高松市オープンデータ利用規約 第１条; package `license_id: cc-by` |   |
| JL-L36a | Saitama food (GIS catalogue) | Sōka; Tokorozawa | PERMITTED, CONDITION | allowed |   | PDL 1.0 credit, the portal's §1.1 form | The GIS catalogue's adoption of the portal terms (recorded read 2026-10-06, jp.md:491); portal terms |   |
| JL-L36b | Saitama 生活衛生 page | Ageo (Regional); Sōka; Tokorozawa; Kasukabe | NOT ESTABLISHED | held | The Japan A to K pass read the same page as permitted (the prefecture registered it on its portal under PDL 1.0); this pass found the site's no-republication policy unanswered. The weaker reading stands for all four cities. | (if permitted: PDL 1.0 credit) | Portal resource 5028; the prefecture site's 著作権 page | Sōka, Tokorozawa, Ageo (Regional), Kasukabe = the prefecture's 生活衛生 list |
| JL-L37 | Shimane portal (Matsue) | Matsue | PERMITTED, CONDITION | allowed |   | PDL 1.0 credit; link the portal, never the city's site | Each resource page states PDL1.0 (jp.md:520) |   |
| JL-L38 | Utsunomiya | Utsunomiya | PERMITTED, CONDITION | allowed |   | One credit meeting both: 「…（宇都宮市）（URL）を加工して作成」, who processed it, the licence | Package `license_id: cc-by`; portal terms |   |

### France, Belgium, the Netherlands, Germany, Italy, Spain, Switzerland, Greece

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| EW-2 | ODbL 1.0 declared on France's NAP, under the NAP's Conditions Particulières | Toulouse; Rennes; Montpellier; Le Havre; Grenoble (Regional) | PERMITTED, CONDITION | allowed |   | The ODbL §4.3 notice naming the database; share-alike only on a derived database of the same nature, granularity, time span and area, which must then be re-shared ON THE NAP in the original format (correcting or adding stop coordinates or names is filed under "Oui"); §4.6 offer of the method | The NAP's ODbL page, `https://doc.transport.data.gouv.fr/le-point-d-acces-national/cadre-juridique/conditions-dutilisation-des-donnees/licence-odbl`; `lic/odbl-toulouse-rennes.md:115-129` |   |
| EW-3 | The same, plus Angers Loire Métropole's own terms | Angers | PERMITTED, CONDITION | allowed | ODbL applies, but the network's marks may not be used without agreement; no condition at all if the tram is drawn from OpenStreetMap. | Row 2's conditions AND the network's marks "and any other mark" of the service not used or mentioned in anything built from the data without the Métropole's prior agreement | As row 2; the Métropole's terms as recorded at `ds.md:2606-2628` and `docs/decisions/2026-09-27.md:13597-13606` |   |
| EW-4 | Licence Ouverte 2.0 (`lov2`) | Marseille; Lille (Regional); Le Mans; Besançon; Avignon; Tours; Dijon; Reims; Orléans; Mulhouse; Brest; Saint-Étienne; Nice; Strasbourg; Caen; Rouen (Regional); Nantes (Regional); Valenciennes (Regional) | PERMITTED, CONDITION | allowed |   | Attribution: the source (at least the Concédant's name) and the date of last update, per source; no official character, no endorsement, nothing misleading; no logos | Licence Ouverte 2.0; `lic/france-licence-ouverte-2.0.md:17-19,37-39` |   |
| EW-5 | Licence Ouverte 2.0 plus INSEE's standing duty | Paris; Marseille; Toulouse; Lille (Regional); Rennes; Le Mans; Besançon; Avignon; Tours; Dijon; Reims; Orléans; Mulhouse; Brest; Saint-Étienne; Nice; Montpellier; Strasbourg; Le Havre; Caen; Rouen (Regional); Bordeaux (Regional); Nantes (Regional); Grenoble (Regional); Valenciennes (Regional); Angers | PERMITTED, CONDITION | allowed |   | « Source : Insee » verbatim, with the date of last update; AND a standing duty to follow each natural person's latest diffusion status (opt-outs), which no notice discharges: a refresh duty for whoever holds a copy; do not mislead as to interpretation; no INSEE marks | Licence Ouverte 2.0 and INSEE's conditions on the SIRENE dataset; `lic/france-licence-ouverte-2.0.md:17-19,56-58,95-99` |   |
| EW-6 | Licence Ouverte 1.0 (`fr-lo`) | Bordeaux (Regional) | PERMITTED, CONDITION | allowed |   | Attribution: the source (at least the Producteur's name) and the date of its last update; nothing misleading | Licence Ouverte, "Version de Octobre 2011", `https://www.data.gouv.fr/pages/legal/licences/etalab-1.0`; the NAP's dataset page, which today shows "Licence Ouverte — version 1.0" (`https://transport.data.gouv.fr/datasets/67f5bad303325228295b7dff`) |   |
| EW-7 | Licence Mobilités | Paris | HELD (single-source read) | held | Held for the feed (owner, 2026-10-12): three licences are declared for it and the Licence Mobilités text was not re-read. IDFM's station and line reference layers are PERMITTED, CONDITION under Licence Ouverte 2.0 (attribution, source and last-update date). | none while held | IDFM's licence pages; the dataset's metadata on the national access point; PRIM's summary | Paris = the timetable feed, with rail redrawn from IDFM's reference layers (Licence Ouverte 2.0) or OpenStreetMap |
| EW-8 | geo.api.gouv.fr, licence unclear | Paris; Marseille; Toulouse; Lille (Regional); Rennes; Le Mans; Besançon; Avignon; Tours; Dijon; Reims; Orléans; Mulhouse; Brest; Saint-Étienne; Nice; Montpellier; Strasbourg; Le Havre; Caen; Rouen (Regional); Bordeaux (Regional); Nantes (Regional); Grenoble (Regional); Valenciennes (Regional); Angers | PERMITTED, CONDITION | allowed | Recorded under the stricter ODbL (owner, 2026-10-12): Licence Ouverte 2.0 upstream, odc-odbl declared on the intermediate dataset, none stated by the API. | attribution; share-alike on a derived database made public | the data.gouv.fr dataset record; IGN's Licence Ouverte 2.0; the api-geo build script |   |
| EW-9 | CC BY 4.0 named on the dataset | Rome; Florence; Charleroi; Liège | PERMITTED, CONDITION | allowed |   | Attribution, licence link, changes indicated; LoGIC: SPW's citation verbatim and the downloaded GeoPackage only, never the map service | CC BY 4.0; `ds.md:3832-3845` (in the zip and on the Metawal record), `it.md:14` (resource `license_type` `A21_CCBY40`), `ds.md:2718-2732` (every dataset and distribution) |   |
| EW-10 | CC BY 4.0, with CC0 recorded for Brussels | Brussels (Regional) | PERMITTED, CONDITION | allowed |   | Attribution (the stricter of the two recorded licences) | BOSA's BeST page, `https://opendata.bosa.be/index.nl.html`; `ds.md:3915-3928` |   |
| EW-11 | CC BY 4.0 on VBB's page, unversioned `cc-by` on Berlin's CKAN | Berlin | PERMITTED, CONDITION | allowed |   | Attribution ("VBB Verkehrsverbund Berlin-Brandenburg GmbH"), licence link, changes stated, VBB's disclaimer kept; no logos or line signets | VBB's own dataset page, `https://unternehmen.vbb.de/digitale-services/datensaetze/` |   |
| EW-12 | CC BY 4.0 known from the national catalogue | Rome | PERMITTED, CONDITION | allowed |   | Attribution to the Agenzia delle Entrate (and ISTAT), licence link, changes indicated | dati.gov.it's record of the dataset, holder "Agenzia delle Entrate", the Lazio distribution, `https://www.dati.gov.it/opendata/api/3/action/package_show?id=stradari-ed-indirizzari-regionali-e-nazionali-da-anncsu` |   |
| EW-13 | CC BY 4.0 set by a harvester default | Thessaloniki | NOT ESTABLISHED | held | Held; confirmed by the owner, 2026-10-12. | Reading A: attribution, licence link, changes stated. Reading B: no modification or redistribution at all | data.gov.gr's record, `https://data.gov.gr/dataset/gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton`; `gr.md:30-41`; `docs/build_briefs/thessaloniki.md:205-217` |   |
| EW-13+1 | Thessaloniki's Ενεργές Άδειες Καταστημάτων: the national record's CC BY 4.0 (full read, replaces EW-13) | Thessaloniki | PERMITTED, CONDITION | allowed | Allowed with condition (owner, 2026-10-12, on the full read of the same day). The no-redistribution clause is clause 3 of the City's map application splash and is about the Portal's content and source code, not the open-data terms. Doubt noted: the CC BY stamp is the harvest source's default, applied to all 131 of the City's layers and not always matching the City's own labels; the layer is absent from the City's own portal, so the City's CC BY default reaches it by inference; the splash's preamble can be read as covering all the department's geodata. Not read: Ministerial Decision 11654 ΕΞ 2026 art. 8(3); one City PDF whose text does not extract. | Credit to the City, title, licence link, changes stated; no implied endorsement; no misleading alteration (terms art. 3.3); not presented as official or complete | data.gov.gr package record `gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton`, field `rights`; data.gov.gr Όροι Χρήσης v1.0 (May 2026), art. 3.2; opendata.thessaloniki.gr About; `maps.thessaloniki.gr/public/config.json`, clause 3 |   |
| EW-14 | CC BY 4.0, level unclear in the record | Brussels | PERMITTED, CONDITION | allowed |   | Attribution to the publisher and hub.brussels with the listed contributors, licence link, changes stated; no City logo or "BXL" mark (portal terms 3.1) | The dataset's own metadata, `https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/commerces-recenses-par-hubbrussels-vbx` |   |
| EW-15 | FAVV-AFSCA's own open-data terms (recorded as CC BY 4.0) | Antwerp; Ghent | PERMITTED, CONDITION | allowed |   | The source and the date of last update cited; nothing misleading, no implied link or endorsement; the permission is revoked automatically while a condition is unmet; no deep link to the agency's site (record) | The agency's open-data page, `https://favv-afsca.be/nl/open-data` |   |
| EW-16 | Belgian Mobility Company portal Terms of Use, art. 3: CC BY 4.0 | Brussels; Antwerp; Ghent; Charleroi; Liège; Brussels (Regional) | PERMITTED, CONDITION | allowed |   | "Source: [PTO Name] – Open Data – [Date of dataset update]" (art. 4), re-dated at each refresh; the modified-data line; access is acceptance of the terms; nothing taken from the operators' own websites | The portal's Terms of Use, `https://data.belgianmobility.io/en/terms.html` |   |
| EW-17 | "Creative Commons Namensnennung (CC-BY)", no version | Bremen | PERMITTED, CONDITION | allowed |   | Attribution („Quellenvermerk: Kommunalverbund Niedersachsen/Bremen e.V.“), the licence title as written and linked, changes stated; the public "reduziert" file only | The dataset's ISO record (`otherConstraints`) and GovData's resource, as recorded at `ds.md:3987-4015`, `de.md:18` |   |
| EW-18 | `cc-by` plus GOIB's terms (CC BY 3.0 ES) | Palma | PERMITTED, CONDITION (single-source read) | allowed | Permitted with condition (owner, 2026-10-12): source line with the date of last update, modifications identified, no suggestion of endorsement, an uncapped indemnity for mere use, unilateral cancellation. The no-alteration line is about the information's content, not derived maps. Not established: whether the terms bind a dataset authored by the Consell de Mallorca. | source line with the date of last update; modifications identified; no suggestion of endorsement; an uncapped indemnity | the Balearic open-data catalogue's terms (Llicència aplicable als conjunts de dades); the dataset's cc-by tag |   |
| EW-19 | CC0 1.0 | Amsterdam; Rotterdam; Berlin; Zurich; Brussels; Brussels (Regional) | PERMITTED | allowed |   | none (no marks: CC0 releases no trademark) | CC0 1.0. B2: the dataset's metadata, `https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/limites-administratives-des-communes-en-region-de-bruxelles-capitale`; N6: the producer's `LICENSE.TXT` (`nl.md:24`); D1: `de.md:16`, `ds.md:2175-2178`; C1: the dataset's CKAN record (`ch.md:44-46`) |   |
| EW-20 | "Auteurswet art. 11, CC0 declared" | Rotterdam | PERMITTED | allowed |   | none; unless a publication itself says otherwise | KOOP's dataset record on data.overheid.nl, `https://data.overheid.nl/dataset/officiele-bekendmakingen`; KOOP's help page, `https://www.overheid.nl/help/officiele-bekendmakingen/bestanden-en-hergebruik` |   |
| EW-21 | Public Domain Mark | Amsterdam; Rotterdam; Den Haag | PERMITTED | allowed |   | none | Kadaster's BAG page, `https://www.kadaster.nl/zakelijk/registraties/basisregistraties/bag` |   |
| EW-22 | Datenlizenz Deutschland – Zero – Version 2.0 | Berlin; Gelsenkirchen | PERMITTED | allowed |   | none | The licence text, `https://www.govdata.de/dl-de/zero-2-0`; D3: the WFS capabilities, `https://gdi.berlin.de/services/wfs/alkis_land?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities`; D4: `docs/build_briefs/gelsenkirchen.md:152-156` |   |
| EW-23 | Modellicentie voor gratis hergebruik v1.0 (Flanders) | Antwerp; Ghent | PERMITTED, CONDITION | allowed |   | A source credit as the licensor specifies: „publieke KBO gegevens, verrijkt met adressen uit het Vlaamse Adressenregister.“ with the extract date | The licence text, `https://www.vlaanderen.be/digitaal-vlaanderen/onze-diensten-en-platformen/open-data/voorwaarden-voor-het-hergebruik-van-overheidsinformatie/modellicentie-gratis-hergebruik`; `ds.md:3820-3830`; `docs/build_briefs/antwerp.md:333-336` |   |
| EW-24 | SITG conditions, Level A | Geneva (Regional) | PERMITTED, CONDITION (single-source read) | allowed | Permitted with condition (owner, 2026-10-12): no resale (RIRT art. 62(4), undefined; a paid data tier is the exposed case); source line with the extraction date; the conditions passed on to anyone given access; own indemnity to the State; no re-identification by crossing sources. | no resale; source line with the extraction date; conditions passed on; own indemnity; no re-identification | SITG conditions of 19 May 2026 (CU 4.1.1, 5.3.1, 5.4.2, 5.5.1, 7.2.1); RIRT (J 1 05.01) art. 62(4) |   |
| EW-25 | SILENT, displayed as CC BY 4.0 on the owner's choice | Amsterdam | SILENT | held |   | none can be named | The dataset's own page, `https://api.data.amsterdam.nl/v1/docs/datasets/horeca.html`; `ds.md:1825-1837` | Amsterdam = the permit register |
| EW-26 | SILENT and ambiguous | Den Haag | SILENT | held |   | none can be named | The layer's and the service's own metadata, `https://services7.arcgis.com/b8OtZx5E96LVMxxJ/arcgis/rest/services/Horeca_nieuw/FeatureServer/2?f=json`; `ds.md:2734-2748` | Den Haag = the permit layer |
| EW-27 | KBO Open Data's terms of reuse | Brussels (Regional) | HELD (single-source read) | held | Allowed only under the app's own registration (owner, 2026-10-12): the KBO licence is free and allows commercial reuse, but it is personal and not assignable, so the data is held as a hand-on from this project. Conditions on the app's own licence: declared purpose, no direct marketing with personal data, source and update date shown, ends after a year with no download. | none while held as a hand-on | the KBO Open Data licence (arts. 1.2, 2.2, 2.3, 2.6 to 2.9, 10.5, 11); Royal Decree of 18 July 2008 |   |
| EW-28 | CC BY 4.0 DG Catastro, over a still-linked 2016 licence | Palma | HELD (read: PERMITTED, CONDITION) | held | Held (owner, 2026-10-12): the separate read of 2026-10-12 found the 2016 licence allows use of transformed cadastral information but not distribution of the original, and the feed's rights line disagrees with the 2013 metadata. That read is weaker than this pass's and stands. | none while held | the 2016 Catastro licence; the ATOM feed's rights line; the 2013 service metadata | Palma = the Catastro address layer, replaced by another geocoder |

### Korea, Taiwan, Hong Kong, Czechia, Latvia, Georgia, the Nordic countries, Romania

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| AN-2 | KOGL Type 1 (Seoul, 17 datasets) | Seoul | PERMITTED, CONDITION | allowed |   | Attribution (source shown) | each dataset page's 이용허락범위 field; `kr.md:87`, `kr.md:124-128` |   |
| AN-3 | Busan Big-데이터웨이브 policy (9 operations) | Busan | PERMITTED, CONDITION (single-source read) | allowed | Permitted with condition (owner, 2026-10-12): source credit and good-faith use; the portal policy page grants free use including for profit. Doubt noted: terms of use art. 14(2) bars commercial use, without consent, of information whose rights belong to the platform, and does not say whether API output is that. | source credit; good-faith use | data.busan.go.kr publicDataPolicy.do; the portal's terms of use, art. 14(2); Public Data Act arts. 1 and 3 |   |
| AN-4 | Daegu D-데이터허브 (9 datasets) | Daegu | HELD | held | Held (owner, 2026-10-12): the City's pages declare no licence. National route noted: data.go.kr listings 15045016, 15006730 and 15096283 state no restriction. | none while held | data.daegu.go.kr openData.do; Public Data Act art. 3(4); the City's copyright guide on daegu.go.kr |   |
| AN-5 | SEMAS 15083033, "이용허락범위 제한 없음" | Incheon; Goyang; Seongnam; Yongin; Suwon; Bucheon; Namyangju; Ansan; Uijeongbu; Anyang (Regional); Daejeon; Gwangju; Gimhae; Gimpo; Siheung | PERMITTED, CONDITION (single-source read) | allowed | Permitted with condition (owner, 2026-10-12): both national listings state no restriction on use; data.go.kr FAQ 210 allows commercial apps. Noted: SEMAS's own copyright policy asks for consultation for unmarked material, and the API listing names the tax service and card companies as sources with no third-party-rights declaration. | source credit; facts kept, nothing falsified or distorted | data.go.kr listings 15083033 and 15012005; data.go.kr FAQ 210 and 186; Public Data Act art. 3(4) and 3(5) |   |
| AN-6 | Taiwan OGDL v1 (政府資料開放授權條款-第1版), ten datasets | Taichung; Taoyuan; Taipei (Regional) | PERMITTED, CONDITION | allowed |   | (a) The annex's attribution statement (顯名聲明) on the data AND on every derivative; without it the licence never existed. (b) Fault-based liability to the agency, §六(三). (c) No patent or trademark. (d) Riders, from the record only: FIA (cite the source; public personal data still under the Personal Data Protection Act; do not present filtered points as the register); Taoyuan portal FAQ (below); Taipei Metro's declaration (no logo, no endorsement, liability for malicious alteration) | The licence text, `https://data.gov.tw/license`, fetched today; each dataset's 授權方式 field on data.gov.tw, fetched today for 9400, 168887, 131326, 157689, 128390 and 128388; `tw.md:39-57`; `ds.md:1922-1964` |   |
| AN-7 | DATA.GOV.HK Terms of Use (FEHD registers) | Hong Kong | PERMITTED, CONDITION | allowed | Permitted, the condition stated prominently (owner, 2026-10-12): an uncapped, one-way indemnity. It binds the party that reproduces the data (the app's operator, once), not the app's users. The owner's rider: if an app design would make every user accept it, hold Hong Kong instead. | Identify the source; acknowledge the Government's and the organisation's IP; attribute the Government, FEHD and DATA.GOV.HK; **an uncapped, one-way indemnity** for third-party infringement claims arising "directly or indirectly", with no notice-and-defend clause; terms revisable without notice | `https://data.gov.hk/en/terms-and-conditions`, fetched today; `ds.md:519-594`; notice 41 |   |
| AN-8 | CSDI Portal terms (FEHD's points) | Hong Kong | PERMITTED, CONDITION | allowed | As AN-7: the same uncapped indemnity, on the operator. | Identify "the Government and the CSDI Portal" as the source; acknowledge IP; the same uncapped indemnity; exclusive Hong Kong jurisdiction | `https://portal.csdi.gov.hk/csdi-webpage/doc/TNC`, fetched today; `ds.md:588-594` |   |
| AN-9 | MTR station lists ("no license declared" in the record) | Hong Kong | PERMITTED, CONDITION | allowed | As AN-7. A change from the record (no licence declared): the portal's terms reach it. Used for a count and one stop name only. | As row 7: source, IP acknowledgement (owner named on the page: MTR Corporation Limited), attribution, the uncapped indemnity | `https://data.gov.hk/en-data/dataset/mtr-data-routes-fares-barrier-free-facilities` and the portal terms, both fetched today |   |
| AN-10 | ČSÚ conditions page: CC BY 4.0 with further data conditions (RES, and the CZ-NACE codebooks) | Prague; Brno; Plzeň; Olomouc; Ostrava; Liberec (Regional); Most (Regional) | PERMITTED, CONDITION | allowed |   | CC BY 4.0 attribution and changes; state the conditions, best by a link to the page; mark modified or derived data and never present it as unchanged official statistics | `https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu`, fetched today; `ds.md:1786-1798` (notice 32) |   |
| AN-11 | ČÚZK spatial-data conditions: CC BY 4.0 (RÚIAN) | Prague; Brno; Plzeň; Olomouc; Ostrava; Liberec (Regional); Most (Regional) | PERMITTED, CONDITION | allowed |   | Credit "ČÚZK, [rok]"; a link to the conditions; a description of any modification; data spread only with its metadata. Fetch through the ATOM service: the VDP APPLICATION's terms ban automated extraction (`docs/build_briefs/prague.md:325-335`), and whether that reaches the static file URLs was never decided | `https://www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx`, fetched today; `ds.md:1800-1811` (notice 33) |   |
| AN-12 | ROS02 `podmínky-užití` declaration (no copyright, no database right, no personal data) | Prague; Brno; Plzeň; Olomouc; Ostrava; Liberec (Regional); Most (Regional) | PERMITTED | allowed |   | none | `docs/build_briefs/prague.md:226-240` (read 2026-09-24); `cz.md:13` |   |
| AN-14 | KORDIS JMK's own grant: CC BY 4.0 (BY-NC-SA in the site footer) | Brno | PERMITTED, CONDITION | allowed |   | Attribution (KORDIS JMK and DPMB as the feed credits them), licence link, changes | `https://www.idsjmk.cz/a/kontakty.html`, fetched today; `ds.md:2630-2645` (notice 78) |   |
| AN-15 | PMDP GTFS record, self-contradictory | Plzeň | PERMITTED, CONDITION | allowed |   | Name the author and any changes (CC BY 4.0) | `https://opendata.plzen.eu/public/opendata/detail/187` and its catalogue record `.../public/opendata/dataset/187`, both fetched today; `ds.md:2647-2660` (notice 79) |   |
| AN-16 | VZD data-use rules: CC BY 4.0 (premise groups, three cadastral maps, address register) | Riga; Liepāja; Daugavpils | PERMITTED, CONDITION | allowed |   | Credit the source; link the licence; describe the changes made; never suggest VZD approved the changes or the product | `https://www.vzd.gov.lv/lv/par-datu-izmantosanas-noteikumiem`, fetched today; the three data.gov.lv dataset pages, fetched today; `ds.md:1905-1911` (notice 42) |   |
| AN-17 | GEO RĪGA: CC BY 4.0 (addresses, degraded buildings, neighbourhoods) | Riga | PERMITTED, CONDITION | allowed |   | Attribution, licence link, changes; do not call the merged neighbourhood outline Riga's administrative boundary | each dataset's licence field; `ds.md:1913-1919` (notice 43); one page fetched today, `https://data.gov.lv/dati/lv/dataset/rigas-ielas-un-adreses` |   |
| AN-18 | CC0 (VID excise-licence register) | Riga; Liepāja; Daugavpils | PERMITTED | allowed |   | none | `https://data.gov.lv/dati/lv/dataset/specialas-atlaujas-licences-un-izzinas-darbibam-ar-akcizes-precem`, fetched today |   |
| AN-19 | CC0 (Rīgas satiksme GTFS) | Riga | PERMITTED | allowed |   | none | `https://data.gov.lv/dati/lv/dataset/marsrutu-saraksti-rigas-satiksme-sabiedriskajam-transportam`, fetched today; `lv.md:26` |   |
| AN-20 | Geostat Terms of Use | Tbilisi | PERMITTED, CONDITION | allowed |   | Name Geostat as the source; third-party material, logos and trademarks are outside the grant | `docs/licenses/geostat-terms-of-use.html.txt`, lines 179 and 185 |   |
| AN-21 | NLOD (Brønnøysundregistrene, Enhetsregisteret) | Oslo; Bergen | PERMITTED, CONDITION | allowed |   | Name the licensor and refer to the licence (§5); say when the data was changed; not misleading; no use of the licensor's name to market a product (§6); **no sublicensing** | NLOD 2.0, `https://data.norge.no/nlod/no/2.0`, fetched today; the API documentation, `https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html`, fetched today; `ds.md:1712-1725` (notice 27) |   |
| AN-22 | NLOD (Entur, Ruter and Skyss GTFS) | Oslo; Bergen | PERMITTED, CONDITION | allowed |   | Credit "Data made available by Entur" with the logo; no distorted or misrepresentative presentation; NLOD's own duties as row 21 | `https://developer.entur.org/pages-intro-setup-and-access/` and `https://developer.entur.org/stops-and-timetable-data/`, both fetched today; `ds.md:1740-1758` (notice 29) |   |
| AN-23 | Kartverket terms: CC BY 4.0 (addresses, kommune boundaries) | Oslo; Bergen | PERMITTED, CONDITION | allowed |   | "© Kartverket" wherever the product or an extract is used, with a link where possible; changes indicated | `https://www.kartverket.no/api-og-data/vilkar-for-bruk`, fetched today; `ds.md:1727-1738` (notice 28) |   |
| AN-24 | CC0 1.0 (Göteborgs Stad, on the distribution node) | Göteborg | PERMITTED | allowed |   | none | the distribution node's metadata, `https://catalog.goteborg.se/store/6/metadata/57479`, fetched today; `se.md:33-40` |   |
| AN-25 | Stockholms stad, Livsmedelstillsyn | Stockholm | SILENT | held | Held; confirmed by the owner, 2026-10-12. | - | the publisher's Hub DCAT feed, `https://open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, fetched today; `se.md:17-31`; `ds.md:2372-2394` (notice 66) |   |
| AN-26 | CVR through Datafordeler: CC BY 4.0 (from `audit_hand_count.md`, S3) | Copenhagen (Regional); Aarhus; Odense | PERMITTED, CONDITION | allowed |   | Credit Det Centrale Virksomhedsregister (CVR) in a fitting place; CC BY 4.0's licence link and changes. Access needs a Datafordeler account and key | `https://datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/`, fetched today (no challenge was served); `ds.md:1760-1771` (notice 30) |   |
| AN-27 | DAR through Datafordeler: CC BY 4.0 (S4) | Copenhagen (Regional); Aarhus; Odense | PERMITTED, CONDITION | allowed |   | Credit Klimadatastyrelsen in a fitting place; licence link and changes | `https://datafordeler.dk/vejledning/brugervilkaar/danmarks-adresseregister-dar/`, fetched today; `ds.md:1773-1784` (notice 31) |   |
| AN-28 | DSVSA București, lists of registered food units | Bucharest | SILENT | held | Held; confirmed by the owner, 2026-10-12. Also read as HC-46. | - | `ds.md:2396-2405` (notice 67), read in the browser 2026-09-23 |   |
| AN-29 | DSVSA Cluj, two lists of registered units | Cluj-Napoca | SILENT | held | Held; confirmed by the owner, 2026-10-12. Also read as HC-46. | - | `ds.md:5199-5231` (notice 215), read in the browser 2026-10-11 |   |

### United Kingdom, Brazil, Australia, Argentina, and the Americas with a provenance file

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| AU-P2a | OGL v3, FSA food hygiene data | London; Glasgow; Newcastle (Regional); Manchester (Regional); Birmingham (Regional); Edinburgh; Sheffield; Nottingham (Regional); Blackpool (Regional); Liverpool (Regional) | PERMITTED, CONDITION | allowed |   | OGL attribution statement and link. Outside the grant: personal data (the record: the FSA treats a sole trader's name and address as personal data), the FSA logo, "the FHRS name" and imagery. A rating, if shown, must be current | FSA terms page |   |
| AU-P2b | OGL v3, OS Code-Point Open | London; Newcastle (Regional); Manchester (Regional); Birmingham (Regional); Edinburgh; Sheffield; Nottingham (Regional); Blackpool (Regional); Liverpool (Regional) | PERMITTED, CONDITION | allowed |   | The three prescribed statements (Ordnance Survey, Royal Mail, National Statistics); no endorsement; "Code-Point" is a registered mark outside the licence | The licence file in the zip, as recorded (`ds.md` notice 59; `uk.md:16`) |   |
| AU-P2c | OGL v3.0, DfT NaPTAN | Manchester (Regional); Birmingham (Regional); Edinburgh; Sheffield; Nottingham (Regional); Blackpool (Regional); Liverpool (Regional) | PERMITTED, CONDITION | allowed |   | OGL attribution statement and link; no endorsement | DfT NaPTAN terms page |   |
| AU-P3 | OGL, City of Ottawa v2.0 | Ottawa | PERMITTED, CONDITION | allowed |   | The prescribed statement, linked; no official status or endorsement; personal information outside the grant | Both items' `licenseInfo`, as recorded (`ca.md:118`, notice 72) |   |
| AU-P4 | Region of Waterloo Open Data Licence | Kitchener–Waterloo (Regional) | PERMITTED, CONDITION | allowed |   | Credit optional, wording prescribed if given; no official status or endorsement; personal information outside the grant | Region of Waterloo open-data page (the licence text is on it) |   |
| AU-P5 | CC BY 4.0 | Rio de Janeiro (Regional); Sydney; Melbourne; Mendoza | PERMITTED, CONDITION | allowed |   | Attribution, licence link, changes indicated | The dataset's own licence field in each case, as recorded |   |
| AU-P6 | CC0 1.0 | New Orleans; Minneapolis; Pittsburgh | PERMITTED | allowed |   | none | The dataset's own licence field in each case, as recorded (`us.md:234,235,240`) |   |
| AU-P6-add | WPRDC Data Use Agreement (rider) | Pittsburgh | PERMITTED, CONDITION | allowed |   | Uncapped indemnity, accepted by use; a duty to notify WPRDC and stop on finding non-public information | `us.md:235` |   |
| AU-P7 | IBGE CNEFE, no licence document | São Paulo; Rio de Janeiro (Regional); Belo Horizonte (Regional); Brasília; Salvador; Fortaleza (Regional); Porto Alegre (Regional); Recife (Regional); Santos (Regional) | HELD (single-source read) | held | Held (owner, 2026-10-12): permitted with a source credit by statute only (Decreto 8.777/2016 art. 4; Lei 14.129/2021 art. 29); IBGE's own terms are silent, and the copyright and statistical-secrecy readings stay open. | none while held | Decreto 8.777/2016 art. 4 and Lei 14.129/2021 art. 29 (planalto.gov.br); IBGE's own pages |   |
| AU-P8 | "Public Domain (PD)", IPEDF | Brasília | PERMITTED | allowed |   | none | The layers' own item pages, API field and ISO record, as recorded (`docs/build_briefs/brasilia.md:54-58`), with Decreto 38.354/2017 art. 4 |   |
| AU-P9 | GeoSampa, CC BY-SA 4.0 declared | São Paulo | NOT ESTABLISHED | held |   | If covered: attribution and share-alike on adaptations | `br.md:147-184` | São Paulo = GeoSampa (a status and a count only) |
| AU-P10 | US federal work (Census Bureau) | Buffalo; Houston; Kansas City; Tucson; New Orleans; Minneapolis; Pittsburgh; Dallas; Seattle (Regional); Tacoma | PERMITTED | allowed | Permitted and flagged (owner, 2026-10-12): a federal work; no sentence names commercial use. | No use of the Bureau's name to imply endorsement | 17 U.S.C. 105 (no copyright in a work of the United States Government), as the record states it (`us.md:314`) |   |
| AU-P11 | Open Data Buffalo, public domain by the portal FAQ | Buffalo | PERMITTED | allowed |   | none | Portal FAQ and 2017 Open Data Policy, as recorded (`us.md:315`) |   |
| AU-P12 | OPEN-NY Terms of Use | New York; Buffalo | PERMITTED, CONDITION | allowed |   | Lawful use; the State may impose terms on specific content and may require a user in breach to stop | OPEN-NY Terms of Use, last modified 2013-03-08 |   |
| AU-P13 | Texas Comptroller, "Public Domain" and the CPA policy | Houston; Dallas | PERMITTED, CONDITION | allowed |   | No pictures, official symbols or service-marked names and logos; "as permitted by law" | The dataset's own licence field and the CPA Privacy and Security Policy |   |
| AU-P14 | COHGIS Site Addresses | Houston | PERMITTED | allowed |   | none (citation "appreciated") | COHGIS Hub statement, as recorded (`docs/build_briefs/houston.md:96-101`) |   |
| AU-P15 | City of Dallas Address Points | Dallas | SILENT | held | Held; confirmed by the owner, 2026-10-12. These points place every pin, so there is nothing to leave out. | Open-ended indemnity under the City's GIS disclaimer | The item's `licenseInfo` and the City's GIS Data Disclaimer |   |
| AU-P16 | City of Sacramento Open Data Terms of Use | Sacramento | SILENT | held | Held; confirmed by the owner, 2026-10-12. | Uncapped indemnity, accepted by use | `docs/build_briefs/sacramento.md:134-146`; `ds.md:604-619` |   |
| AU-P17 | City of Seattle Open Data Terms of Use | Seattle (Regional) | NOT ESTABLISHED | held |   |   | Seattle Open Data Terms of Use (the portal's Data Policy page) |   |
| AU-P18 | City of Bellevue, data field and portal terms | Seattle (Regional) | FORBIDDEN | blacklisted |   | (lifted only by Bellevue's express written authorization) | The item's own `licenseInfo`; and the site Terms of Use |   |
| AU-P19 | King County food inspections | Seattle (Regional) | NOT ESTABLISHED | held |   | If the portal terms govern: the legend "data provided by permission of King County"; no marks; uncapped indemnity; revocable | The portal's own Terms of Use (last updated 2015-03-03), against the site-wide kingcounty.gov terms |   |
| AU-P20 | Snohomish County Food Service Establishments (2025) | Seattle (Regional) | SILENT | held |   |   | The item (empty fields); the County's GIS terms on its Maps and GIS page |   |
| AU-P21 | KCMO Business License Holders | Kansas City | PERMITTED, CONDITION | allowed |   | The portal's prescribed disclaimer on any derivative application; an open-ended indemnity from "any user of the data", if the portal terms bind; no City marks | The dataset's own licence field, with KCMO Code 2-2134(a) as recorded; the portal's Data Terms of Use beside it |   |
| AU-P22 | City of Tucson BUSLIC | Tucson | SILENT | held | Held; confirmed by the owner, 2026-10-12. | A.R.S. 39-121.03 applies to a commercial purpose | The item's `licenseInfo`; A.R.S. 39-121.03 |   |
| AU-P23 | City of Tacoma | Tacoma | SILENT | held | Held; confirmed by the owner, 2026-10-12. | The City's disclaimer displayed with any application; revocable for any reason | City of Tacoma Data Disclaimer; Resolution 39378 (2016) as recorded |   |
| AU-S1 | Washington State Liquor and Cannabis Board, Off Premise list | Seattle (Regional) | FORBIDDEN | blacklisted |   |   | The Board's lists page; RCW 42.56.070(8) |   |
| AU-S2 | Snohomish County Building Address Points | Seattle (Regional) | SILENT | held |   | Hold-harmless for errors in the data | The item's own `licenseInfo` |   |
| AU-S3 | King County Address Points (`ADDRESS_POINT_642`) and city polygons (`CITY_KC_AREA_446`) | Seattle (Regional) | NOT ESTABLISHED | held |   | No sale of the information without a written agreement | King County GIS Center terms, which both items' `licenseInfo` link |   |
| AU-S4 | US Census Bureau batch geocoder | Sacramento; Houston; Dallas | PERMITTED | allowed | Permitted and flagged (owner, 2026-10-12): no terms page for the geocoder was read. | as P10 | as P10; `us.md:327` still says "Terms page not read" |   |
| AU-S5 | Wikidata item Q107175168 | Sacramento | PERMITTED | allowed |   | none | CC0 1.0 (Wikidata structured data), `us.md:39` |   |
| AU-S6 | Metro Linha 17-Ouro page | São Paulo | SILENT | held |   |   | none recorded (`br.md:29`) | São Paulo = the Metro page (a status and a count only) |

### The 34 cities counted by hand (North America, Mexico, Spain, Ireland, Milan, Denmark, Sapporo, the Tama cities)

| Id | Source or position | Cities | Verdict | Column | Ruling or note | Condition | Rests on | Stands without it |
|---|---|---|---|---|---|---|---|---|
| HC-1 | CC0 1.0 on the dataset | Los Angeles (Regional) | PERMITTED | allowed |   | none | Socrata metadata, `licenseId: CC0_10` |   |
| HC-2 | ODC PDDL 1.0 on the dataset (not in the table: text read) | San Francisco; Boston | PERMITTED | allowed |   | none | PDDL 1.0 legal text, s.3.3(a) |   |
| HC-3 | MassGIS, public records | Boston | PERMITTED | allowed |   | none required; never present the outline as an authoritative boundary | `us.md:250`, read 2026-10-02, FAQ re-read 2026-10-03 |   |
| HC-4 | OPEN-NY Terms of Use | New York | PERMITTED | allowed |   | lawful, non-malicious use; the State may require a stop in writing on breach | OPEN-NY Terms of Use (data.ny.gov `77gx-ii52`, last modified 2013-03-08) |   |
| HC-6 | CC BY 4.0 named on the dataset or in the register's own terms | Washington D.C.; Montréal; Dublin; Copenhagen (Regional); Sapporo; Aarhus; Odense | PERMITTED, CONDITION | allowed |   | attribution, changes indicated; NTA's prescribed sentence; CVR and Klimadatastyrelsen named | `us.md:248-249`; `ds.md:1445-1453`, `3670-3681`, `1762-1781`; `jp.md:463`; `ca.md:126` |   |
| HC-7 | CC BY 4.0, CKAN id with no version | Milan | PERMITTED, CONDITION | allowed |   | attribution, changes indicated | `ds.md:1514-1528` |   |
| HC-8 | CC BY 4.0 plus the Ayuntamiento's general conditions | Madrid | PERMITTED, CONDITION | allowed |   | source and last-update date cited; meaning not distorted; no endorsement; metadata kept | `lic/madrid-condiciones-generales-reutilizacion.txt:38` |   |
| HC-9 | CC BY 4.0 plus the Open Data BCN terms | Barcelona | PERMITTED, CONDITION | allowed |   | cite the Council; inform the Council of every project; Article 8's "content may not be altered" stands as a disclosed position | `lic/barcelona-condicions-us-live.txt:98-99` |   |
| HC-10 | CC BY 4.0 plus the Ville de Montréal's licence page | Montréal | PERMITTED, CONDITION | allowed |   | credit (STM for the feed); say whether modified or interpreted; no endorsement; no attempt to identify a person, business or organisation | `lic/montreal-licence-donnees-ouvertes.txt:59-60` |   |
| HC-13 | CC BY 2.5 AR on the dataset (not in the table: text read) | Buenos Aires | PERMITTED, CONDITION | allowed |   | credit GCBA / BA Data and each author unit, title, URI, licence URI, how changed | CC BY 2.5 AR legal code s.3; deed |   |
| HC-16 | Open Government Licence, municipal and provincial versions | Vancouver (Regional); Calgary; Toronto | PERMITTED, CONDITION | allowed |   | each publisher's attribution statement, verbatim; no Personal Information; no official status or endorsement; ends automatically on breach | `lic/calgary-...txt:25-27`, `lic/toronto-...txt:29-31`, `lic/vancouver-...txt:28-30`, `lic/surrey-...txt:28-30`, `lic/bc-...txt:80`; `ca.md:115-117` for Burnaby, New Westminster, Coquitlam |   |
| HC-17 | Edmonton Open Data Terms of Use v2.1 | Edmonton | PERMITTED, CONDITION | allowed |   | pass on the Terms or their URL to anyone given the data, with no added restriction; indemnity; no endorsement; the City may cancel at any time | `lic/edmonton-open-data-terms-of-use.pdf.txt:9` |   |
| HC-18 | INEGI Términos de Libre Uso | Mexico City (Regional); Guadalajara (Regional); Monterrey (Regional) | PERMITTED, CONDITION | allowed |   | "Fuente: INEGI, ..." credit; tell the end user of any analysis or transformation; no official stance or endorsement | `lic/inegi-terminos-libre-uso-informacion.pdf.txt:9` |   |
| HC-19 | LA County Enterprise GIS Terms of Use | Los Angeles (Regional) | PERMITTED, CONDITION | allowed |   | no suggestion of County endorsement; voided on breach; breach-only indemnity; boundary never called legal | `us.md:247,251` (read 2026-09-22 and 2026-10-02) |   |
| HC-20 | MapsLB Terms of Use | Los Angeles (Regional) | PERMITTED, CONDITION | allowed |   | no endorsement; ends on breach; breach-only indemnity | `us.md:243` (read 2026-10-03) |   |
| HC-21 | CRTM licencia de uso | Madrid | PERMITTED, CONDITION | allowed |   | "Powered by CRTM" with the link; raw or worked stated; kept up to date; no bad-faith alteration; no endorsement | `lic/crtm-licencia-de-uso.txt:230` |   |
| HC-22 | TransLink GTFS static terms | Vancouver (Regional) | PERMITTED, CONDITION | allowed |   | the "Route and arrival data" legend; identify yourself and say whether the use is commercial, if asked; **TransLink may impose further terms or a fee on a commercial user who charges end users**; indemnity; revocable | `lic/translink-gtfs-static-terms-of-use.txt:77-80` |   |
| HC-23 | NYC Open Data Law, no licence | New York | PERMITTED, CONDITION | allowed | Permitted and flagged (owner, 2026-10-12): the sentence is general (no restrictions on use) and does not name commercial use. | DoITT may require source, version and modifications to be identified | NYC Open Data FAQ; `us.md:313` |   |
| HC-24 | San Diego: PDDL on the dataset page, plus the portal's Terms of Use | San Diego | PERMITTED, CONDITION | allowed |   | the portal terms bind by use: indemnify and defend the City | the dataset page's "License: View License" link to `opendefinition.org/licenses/odc-pddl/`; PDDL text as position 2; portal terms `https://data.sandiego.gov/help/guides/terms/` |   |
| HC-25 | US Census Bureau, a federal work | Washington D.C. | PERMITTED, CONDITION | allowed | Permitted and flagged (owner, 2026-10-12): a federal work; no sentence names commercial use. | no endorsement implied; "TIGER/Line" not in a commercial product's name; the API notice | TIGER/Line technical documentation 2025 ch.1 §1.2; Census API Terms of Service |   |
| HC-26 | US Census batch geocoder (none recorded) | Los Angeles (Regional); New York; Washington D.C. | PERMITTED, CONDITION | allowed | Permitted and flagged (owner, 2026-10-12): none recorded; a federal work. | as position 25 | the same two documents; the developer page for geocoding services links the same Terms of Service |   |
| HC-27 | Calgary City Boundary (none recorded) | Calgary | PERMITTED, CONDITION | allowed |   | as position 16, Calgary's statement | dataset metadata: `licenseId: SEE_TERMS_OF_USE`, attribution "The City of Calgary" |   |
| HC-28 | Edmonton Corporate Boundary (none recorded) | Edmonton | PERMITTED, CONDITION | allowed |   | as position 17 | dataset metadata: `licenseId: SEE_TERMS_OF_USE` |   |
| HC-29 | Toronto Regional Municipal Boundary (none recorded) | Toronto | PERMITTED, CONDITION | allowed |   | as position 16, Toronto's statement | `package_show`: `license_id: open-government-licence-toronto` |   |
| HC-30 | Vancouver parcel polygons, tax report, local-area boundary (none recorded) | Vancouver (Regional) | PERMITTED, CONDITION | allowed |   | as position 16, Vancouver's statement | each dataset's metadata: `"license": "Open Government Licence - Vancouver"` |   |
| HC-31 | Montréal Limites administratives (none recorded) | Montréal | PERMITTED, CONDITION | allowed |   | as position 10 | `package_show`: `license_id: cc-by`, "Creative Commons Attribution 4.0 International" |   |
| HC-32 | Tailte statutory boundaries (none recorded) | Dublin | PERMITTED, CONDITION | allowed |   | attribution, changes indicated; the item says reference use only | the ArcGIS item's `licenseInfo` |   |
| HC-33 | Madrid Término municipal (none recorded) | Madrid | PERMITTED, CONDITION | allowed |   | as position 8 | datos.madrid.es dataset `300498-0-termino-municipal-madrid`: `license_id: cc-by`, "Creative Commons Attribution 4.0 International (CC BY 4.0)"; one of its resources is the exact geoportal zip the build reads |   |
| HC-34 | Milan GTFS (none recorded) | Milan | PERMITTED, CONDITION | allowed |   | attribution, changes indicated | dataset `ds929-orari-del-trasporto-pubblico-locale-nel-comune-di-milano-in-formato-gtfs`: `license_id: cc-by`, resource `license_type` `.../licences/A21_CCBY40` |   |
| HC-35 | Milan Confini Amministrativi (none recorded) | Milan | PERMITTED, CONDITION | allowed |   | attribution, changes indicated | `package_show`: `license_id: cc-by`, resources' `license_type` `.../licences/A21_CCBY40` |   |
| HC-36 | Tokyo statistical yearbook FY2024 (none recorded) | Tama; Higashimurayama; Fuchū (Tokyo); Chōfu; Tachikawa; Hino | PERMITTED, CONDITION | allowed |   | the Tokyo catalogue's credit; edits stated | Tokyo catalogue entry 「東京都統計年鑑 令和6年 19A 医療・衛生」: `license_id: CC-BY-4.0`, resources `tn24qv190700.csv` and `tn24qv190800.csv` |   |
| HC-37 | MassDOT Developers License Agreement | Boston | SILENT | held |   |   | `lic/mbta-massdot-develop-license-agreement.pdf.txt:25` | Boston = the MBTA feed, with rail from OpenStreetMap |
| HC-38 | LA Metro developer Terms & Conditions | Los Angeles (Regional) | SILENT | held |   |   | `lic/la-metro-terms-conditions.html.txt:37,47,51` | Los Angeles (Regional) = the LA Metro feed, with rail from OpenStreetMap |
| HC-39 | MTA terms and conditions for data feeds | New York | SILENT | held |   |   | `lic/mta-terms-and-conditions.txt:60-62` | New York = the MTA feed, with rail from OpenStreetMap |
| HC-40 | SFMTA Transit Data License Agreement | San Francisco | SILENT | held |   |   | `lic/sfmta-transit-data-license-agreement.html.txt:84` | San Francisco = the SFMTA feed, with rail from OpenStreetMap |
| HC-41 | WMATA Transit Data terms | Washington D.C. | SILENT | held |   |   | `lic/wmata-transit-data-terms-of-use.html.txt:97,109` | Washington D.C. = the WMATA feed, with rail from OpenStreetMap |
| HC-42 | MTS Developer License Agreement | San Diego | SILENT | held |   |   | MTS terms page | San Diego = the MTS feed, with rail from OpenStreetMap |
| HC-43 | SanGIS GIS Data End User Use Agreement | San Diego | SILENT | held |   |   | the parcel item's `licenseInfo` | San Diego = both SanGIS layers |
| HC-44a | Chicago Data Terms of Use | Chicago | SILENT | held | Held; confirmed by the owner, 2026-10-12. |   | Data Terms of Use, "USE OF DATA" |   |
| HC-45 | Miami-Dade County, disclaimer and no grant | Miami (Regional) | SILENT | held | Held; confirmed by the owner, 2026-10-12. |   | `us.md:329` (established by reading, 2026-09-21) |   |
| HC-47 | Metrorrey network map PDF (none recorded) | Monterrey (Regional) | SILENT | held |   |   | nl.gob.mx home page footer | Monterrey (Regional) = the operator's map PDF |
| HC-44 | "City of Philadelphia License" plus the City's Terms of Use | Philadelphia | FORBIDDEN (read: NOT ESTABLISHED) | blacklisted | Blacklisted (owner, 2026-10-12). The read's verdict was NOT ESTABLISHED with neither reading permitting: the City's Terms say commercial use is prohibited without the City's prior written permission, and each dataset page binds the reader to them. |   | each OpenDataPhilly dataset page; `https://www.phila.gov/terms-of-use/` |   |
| HC-48 | CTA Developer License Agreement | Chicago | NOT ESTABLISHED | held |   |   | `lic/cta-developer-license-agreement.html.txt:431,455,513` |   |
| HC-49 | SEPTA License Agreement | Philadelphia | NOT ESTABLISHED | held |   |   | `lic/septa-license-agreement.html.txt:213,215` |   |
| HC-50 | Surrey City Boundaries (none recorded) | Vancouver (Regional) | NOT ESTABLISHED | held |   |   | the item and Surrey's open-data site | Vancouver (Regional) = Surrey's boundary file |

## City table

Derived from the source table by `scripts/commercial_use_cities.py --write`;
never edit it by hand. `Decided by` names the rows that hold or blacklist the
city; `Stands if left out` names what would have to be dropped or replaced.

<!-- city-table:start -->
| City | Country | Column | Decided by | Stands if left out | Rows |
|---|---|---|---|---|---|
| Buenos Aires | Argentina | allowed |   |   | 2 |
| Mendoza | Argentina | allowed |   |   | 2 |
| Melbourne | Australia | allowed |   |   | 2 |
| Sydney | Australia | allowed |   |   | 2 |
| Antwerp | Belgium | allowed |   |   | 4 |
| Brussels | Belgium | allowed |   |   | 4 |
| Brussels (Regional) | Belgium | held | EW-27 |   | 5 |
| Charleroi | Belgium | allowed |   |   | 3 |
| Ghent | Belgium | allowed |   |   | 4 |
| Liège | Belgium | allowed |   |   | 3 |
| Belo Horizonte (Regional) | Brazil | held | AU-P7 |   | 2 |
| Brasília | Brazil | held | AU-P7 |   | 3 |
| Fortaleza (Regional) | Brazil | held | AU-P7 |   | 2 |
| Porto Alegre (Regional) | Brazil | held | AU-P7 |   | 2 |
| Recife (Regional) | Brazil | held | AU-P7 |   | 2 |
| Rio de Janeiro (Regional) | Brazil | held | AU-P7 |   | 3 |
| Salvador | Brazil | held | AU-P7 |   | 2 |
| Santos (Regional) | Brazil | held | AU-P7 |   | 2 |
| São Paulo | Brazil | held | AU-P7 | GeoSampa (a status and a count only) (AU-P9); the Metro page (a status and a count only) (AU-S6) | 4 |
| Calgary | Canada | allowed |   |   | 3 |
| Edmonton | Canada | allowed |   |   | 3 |
| Kitchener–Waterloo (Regional) | Canada | allowed |   |   | 2 |
| Montréal | Canada | allowed |   |   | 4 |
| Ottawa | Canada | allowed |   |   | 2 |
| Toronto | Canada | allowed |   |   | 3 |
| Vancouver (Regional) | Canada | allowed if left out |   | Surrey's boundary file (HC-50) | 5 |
| Brno | Czechia | allowed |   |   | 5 |
| Liberec (Regional) | Czechia | allowed |   |   | 4 |
| Most (Regional) | Czechia | allowed |   |   | 4 |
| Olomouc | Czechia | allowed |   |   | 4 |
| Ostrava | Czechia | allowed |   |   | 4 |
| Plzeň | Czechia | allowed |   |   | 5 |
| Prague | Czechia | allowed |   |   | 4 |
| Aarhus | Denmark | allowed |   |   | 4 |
| Copenhagen (Regional) | Denmark | allowed |   |   | 4 |
| Odense | Denmark | allowed |   |   | 4 |
| Angers | France | allowed |   |   | 4 |
| Avignon | France | allowed |   |   | 4 |
| Besançon | France | allowed |   |   | 4 |
| Bordeaux (Regional) | France | allowed |   |   | 4 |
| Brest | France | allowed |   |   | 4 |
| Caen | France | allowed |   |   | 4 |
| Dijon | France | allowed |   |   | 4 |
| Grenoble (Regional) | France | allowed |   |   | 4 |
| Le Havre | France | allowed |   |   | 4 |
| Le Mans | France | allowed |   |   | 4 |
| Lille (Regional) | France | allowed |   |   | 4 |
| Marseille | France | allowed |   |   | 4 |
| Montpellier | France | allowed |   |   | 4 |
| Mulhouse | France | allowed |   |   | 4 |
| Nantes (Regional) | France | allowed |   |   | 4 |
| Nice | France | allowed |   |   | 4 |
| Orléans | France | allowed |   |   | 4 |
| Paris | France | allowed if left out |   | the timetable feed, with rail redrawn from IDFM's reference layers (Licence Ouverte 2.0) or OpenStreetMap (EW-7) | 4 |
| Reims | France | allowed |   |   | 4 |
| Rennes | France | allowed |   |   | 4 |
| Rouen (Regional) | France | allowed |   |   | 4 |
| Saint-Étienne | France | allowed |   |   | 4 |
| Strasbourg | France | allowed |   |   | 4 |
| Toulouse | France | allowed |   |   | 4 |
| Tours | France | allowed |   |   | 4 |
| Valenciennes (Regional) | France | allowed |   |   | 4 |
| Tbilisi | Georgia | allowed |   |   | 2 |
| Berlin | Germany | allowed |   |   | 4 |
| Bremen | Germany | allowed |   |   | 2 |
| Gelsenkirchen | Germany | allowed |   |   | 2 |
| Thessaloniki | Greece | allowed |   |   | 2 |
| Hong Kong | Hong Kong | allowed |   |   | 4 |
| Dublin | Ireland | allowed |   |   | 3 |
| Florence | Italy | allowed |   |   | 2 |
| Milan | Italy | allowed |   |   | 4 |
| Rome | Italy | allowed |   |   | 3 |
| Ageo (Regional) | Japan | allowed if left out |   | the prefecture's 生活衛生 list (JL-L36b) | 3 |
| Akita | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Amagasaki | Japan | allowed |   |   | 5 |
| Aomori | Japan | allowed |   |   | 6 |
| Chōfu | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Fuchū (Tokyo) | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Fuji | Japan | allowed |   |   | 6 |
| Fujisawa | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Fukui | Japan | allowed |   |   | 6 |
| Fukuoka | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Fukushima | Japan | allowed |   |   | 5 |
| Fukuyama | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Funabashi | Japan | allowed |   |   | 5 |
| Gifu | Japan | allowed |   |   | 5 |
| Hakodate | Japan | allowed |   |   | 6 |
| Hamamatsu | Japan | allowed |   |   | 6 |
| Higashimurayama | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Higashiyamato | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Higashiōsaka | Japan | allowed |   |   | 6 |
| Himeji | Japan | allowed |   |   | 6 |
| Hino | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Hirakata | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Hiroshima | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 5 |
| Ibaraki (Osaka) | Japan | allowed |   |   | 5 |
| Ichihara | Japan | allowed |   |   | 5 |
| Ichikawa | Japan | allowed |   |   | 5 |
| Ichinomiya | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Itami | Japan | allowed |   |   | 5 |
| Iwaki | Japan | allowed |   |   | 5 |
| Kadoma | Japan | allowed |   |   | 6 |
| Kagoshima | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Kakogawa | Japan | allowed |   |   | 5 |
| Kanazawa | Japan | allowed |   |   | 6 |
| Kasukabe | Japan | allowed if left out |   | the prefecture's 生活衛生 list (JL-L36b) | 7 |
| Kawaguchi | Japan | allowed |   |   | 6 |
| Kawasaki | Japan | allowed |   |   | 6 |
| Kitakyushu | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Kobe | Japan | allowed |   |   | 5 |
| Koshigaya | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Kumamoto | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Kurashiki | Japan | allowed |   |   | 6 |
| Kure | Japan | held | JA-G5 |   | 6 |
| Kurume | Japan | held | JA-G5 |   | 6 |
| Kyoto | Japan | allowed |   |   | 5 |
| Kōchi | Japan | allowed |   |   | 6 |
| Maebashi | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Matsudo | Japan | allowed |   |   | 5 |
| Matsue | Japan | allowed |   |   | 6 |
| Matsumoto | Japan | allowed |   |   | 6 |
| Matsuyama | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Minoh | Japan | allowed |   |   | 6 |
| Mito | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Moriguchi | Japan | allowed |   |   | 5 |
| Morioka | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Nagasaki | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Naha | Japan | allowed |   |   | 6 |
| Nara | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Neyagawa | Japan | allowed |   |   | 6 |
| Nishinomiya | Japan | allowed |   |   | 6 |
| Nishitōkyō | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Okayama | Japan | held | JA-G5 |   | 6 |
| Okazaki | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Osaka | Japan | allowed |   |   | 5 |
| Sagamihara | Japan | allowed |   |   | 6 |
| Sakai | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Sakura | Japan | allowed |   |   | 5 |
| Sapporo | Japan | allowed |   |   | 5 |
| Sasebo | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Shimonoseki | Japan | held | JA-G5 |   | 6 |
| Shizuoka | Japan | allowed |   |   | 6 |
| Suita | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Sōka | Japan | allowed if left out |   | the prefecture's 生活衛生 list (JL-L36b) | 7 |
| Tachikawa | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Takamatsu | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Takatsuki | Japan | held | JA-G5 |   | 6 |
| Tama | Japan | held | JA-G7 | the MHLW rows (JA-G5) | 7 |
| Tokorozawa | Japan | allowed if left out |   | the prefecture's 生活衛生 list (JL-L36b) | 7 |
| Tokyo | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 10 |
| Tottori | Japan | held | JA-G5 |   | 6 |
| Toyama | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Toyonaka | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Toyota | Japan | allowed |   |   | 6 |
| Tsu | Japan | allowed |   |   | 5 |
| Uji | Japan | held | JA-G5 |   | 5 |
| Urayasu | Japan | allowed |   |   | 5 |
| Utsunomiya | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Yachiyo | Japan | allowed |   |   | 5 |
| Yamagata | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 7 |
| Yao | Japan | held | JA-G5 |   | 6 |
| Yokkaichi | Japan | allowed |   |   | 6 |
| Yokohama | Japan | allowed |   |   | 5 |
| Yokosuka | Japan | allowed |   |   | 6 |
| Ōita | Japan | allowed if left out |   | the MHLW rows (JA-G5) | 6 |
| Ōtsu | Japan | allowed if left out |   | the city-site food list (JL-L11b) | 7 |
| Daugavpils | Latvia | allowed |   |   | 3 |
| Liepāja | Latvia | allowed |   |   | 3 |
| Riga | Latvia | allowed |   |   | 5 |
| Guadalajara (Regional) | Mexico | allowed |   |   | 2 |
| Mexico City (Regional) | Mexico | allowed |   |   | 2 |
| Monterrey (Regional) | Mexico | allowed if left out |   | the operator's map PDF (HC-47) | 3 |
| Amsterdam | Netherlands | allowed if left out |   | the permit register (EW-25) | 4 |
| Den Haag | Netherlands | allowed if left out |   | the permit layer (EW-26) | 3 |
| Rotterdam | Netherlands | allowed |   |   | 4 |
| Bergen | Norway | allowed |   |   | 4 |
| Oslo | Norway | allowed |   |   | 4 |
| Bucharest | Romania | held | AN-28 |   | 2 |
| Cluj-Napoca | Romania | held | AN-29 |   | 2 |
| Ansan | South Korea | allowed |   |   | 2 |
| Anyang (Regional) | South Korea | allowed |   |   | 2 |
| Bucheon | South Korea | allowed |   |   | 2 |
| Busan | South Korea | allowed |   |   | 2 |
| Daegu | South Korea | held | AN-4 |   | 2 |
| Daejeon | South Korea | allowed |   |   | 2 |
| Gimhae | South Korea | allowed |   |   | 2 |
| Gimpo | South Korea | allowed |   |   | 2 |
| Goyang | South Korea | allowed |   |   | 2 |
| Gwangju | South Korea | allowed |   |   | 2 |
| Incheon | South Korea | allowed |   |   | 2 |
| Namyangju | South Korea | allowed |   |   | 2 |
| Seongnam | South Korea | allowed |   |   | 2 |
| Seoul | South Korea | allowed |   |   | 2 |
| Siheung | South Korea | allowed |   |   | 2 |
| Suwon | South Korea | allowed |   |   | 2 |
| Uijeongbu | South Korea | allowed |   |   | 2 |
| Yongin | South Korea | allowed |   |   | 2 |
| Barcelona | Spain | allowed |   |   | 2 |
| Madrid | Spain | allowed |   |   | 4 |
| Palma | Spain | allowed if left out |   | the Catastro address layer, replaced by another geocoder (EW-28) | 3 |
| Göteborg | Sweden | allowed |   |   | 2 |
| Stockholm | Sweden | held | AN-25 |   | 2 |
| Geneva (Regional) | Switzerland | allowed |   |   | 2 |
| Zurich | Switzerland | allowed |   |   | 2 |
| Taichung | Taiwan | allowed |   |   | 2 |
| Taipei (Regional) | Taiwan | allowed |   |   | 2 |
| Taoyuan | Taiwan | allowed |   |   | 2 |
| Birmingham (Regional) | United Kingdom | allowed |   |   | 4 |
| Blackpool (Regional) | United Kingdom | allowed |   |   | 4 |
| Edinburgh | United Kingdom | allowed |   |   | 4 |
| Glasgow | United Kingdom | allowed |   |   | 2 |
| Liverpool (Regional) | United Kingdom | allowed |   |   | 4 |
| London | United Kingdom | allowed |   |   | 3 |
| Manchester (Regional) | United Kingdom | allowed |   |   | 4 |
| Newcastle (Regional) | United Kingdom | allowed |   |   | 3 |
| Nottingham (Regional) | United Kingdom | allowed |   |   | 4 |
| Sheffield | United Kingdom | allowed |   |   | 4 |
| Boston | United States | allowed if left out |   | the MBTA feed, with rail from OpenStreetMap (HC-37) | 4 |
| Buffalo | United States | allowed |   |   | 4 |
| Chicago | United States | held | HC-44a, HC-48 |   | 3 |
| Dallas | United States | held | AU-P15 |   | 5 |
| Houston | United States | allowed |   |   | 5 |
| Kansas City | United States | allowed |   |   | 3 |
| Los Angeles (Regional) | United States | allowed if left out |   | the LA Metro feed, with rail from OpenStreetMap (HC-38) | 6 |
| Miami (Regional) | United States | held | HC-45 |   | 2 |
| Minneapolis | United States | allowed |   |   | 3 |
| New Orleans | United States | allowed |   |   | 3 |
| New York | United States | allowed if left out |   | the MTA feed, with rail from OpenStreetMap (HC-39) | 6 |
| Philadelphia | United States | blacklisted | HC-44, HC-49 |   | 3 |
| Pittsburgh | United States | allowed |   |   | 4 |
| Sacramento | United States | held | AU-P16 |   | 4 |
| San Diego | United States | allowed if left out |   | the MTS feed, with rail from OpenStreetMap (HC-42); both SanGIS layers (HC-43) | 4 |
| San Francisco | United States | allowed if left out |   | the SFMTA feed, with rail from OpenStreetMap (HC-40) | 3 |
| Seattle (Regional) | United States | blacklisted | AU-P17, AU-P18, AU-P19, AU-P20, AU-S1, AU-S2, AU-S3 |   | 9 |
| Tacoma | United States | held | AU-P23 |   | 3 |
| Tucson | United States | held | AU-P22 |   | 3 |
| Washington D.C. | United States | allowed if left out |   | the WMATA feed, with rail from OpenStreetMap (HC-41) | 5 |
<!-- city-table:end -->
