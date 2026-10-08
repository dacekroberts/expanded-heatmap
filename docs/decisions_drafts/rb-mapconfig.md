# rb-mapconfig: line colours against the new pins, one name per line

Drafts for the fold. Branch `rb-mapconfig`, cut from
`review-batch-2026-10-07` for the large review.

### 2026-10-07 - One name per line across maps

- **Six cross-map name splits unified at their config source (owner,
  2026-10-07: the operator's full official name everywhere, unless a shorter
  official name is valid and used on every map involved).** Lane 4's survey of
  the 64 Japanese maps found them. Each changed in `pipeline/<city>/config.py`
  (`LINES[...]["name"]`), the page bullet, the city card blurb in
  `app/cities.py`, and the rows of `docs/data_sources/japan.md` and
  `docs/map_inconsistencies.md` that name the line:
  - 豊肥本線: Kumamoto "JR Hohi Line" to "JR Hohi Main Line", as Ōita
    (lane 4's P201 and P202 applied with it: "Kagoshima and Hohi main lines").
  - 函館本線: Hakodate "JR Hakodate Line" to "JR Hakodate Main Line", as
    Sapporo (name_ja 函館線 to 函館本線, which does not render).
  - 山陽電気鉄道 本線: Kobe "Sanyō Main Line" to "Sanyo Electric Main Line",
    as Himeji and Kakogawa. Checked to be the SAME line: all three draw N02's
    (山陽電気鉄道, 本線). JR West's Sanyo Main Line (N02 山陽線) is a
    different line, drawn as "JR Kobe Line" and "Wadamisaki Line" in Kobe and
    "JR Sanyo Line" in Himeji, and is untouched. The old Kobe name read as
    JR's line. Kobe's station suffix "Sanyō" stays: no station uses it.
  - おおさか東線: Osaka and Suita "Osaka Higashi Line" to "JR Osaka Higashi
    Line", as Higashiōsaka (the full form; the short one was not on every
    map). Both configs' Umekita branch label follows (step 1 log text only).
  - Osaka Metro 中央線: Osaka "Chūō Line" to "Osaka Metro Chuo Line", as
    Higashiōsaka (the full form; the macron by the rule below). Osaka's other
    Osaka Metro lines keep their unprefixed names, which no other map
    contradicts.
  - 天神大牟田線: Fukuoka "Nishitetsu Tenjin Ōmuta Line" to "Nishitetsu Tenjin
    Omuta Line", as Kurume. Macron rule, measured: 12 of the 298 distinct
    Japanese line names in the configs carry a macron, so the majority form is
    without. The same count settles Chuo and Sanyo.
- **JR Chuo left as it is.** Tachikawa and Hino draw "JR Chuo Line", Tokyo
  "JR Chuo Line (Rapid)". The owner answered East-1's call 203 "keep" ("rapid
  is a regional distinction for speed"); the 2026-10-07 rule is not read as
  overturning an answer given on this exact pair. For the owner to confirm.

### 2026-10-07 - Lines within 20 of the olive and violet pins recoloured

- **Every drawn line within CIE76 20 of Food shops olive (#737a00) or Shops
  and services violet (#7e57c2) on a map that draws it was recoloured: 32
  legend rows, 27 distinct line colours, 21 maps (owner, 2026-10-07).** Found
  by reading each committed map's legend (pin rows and line rows). Each line
  took the colour nearest its operator's hue (the config's `hue`, else its
  drawn colour) on a 4-step sRGB cube, holding: 3:1 on both map pages; CIE76
  >= 20 from every pin its maps draw; >= 18 from every other line those maps
  draw (stricter than the search's 18-within-500 m, so no spatial read was
  needed); the LCh hue within 20 degrees of the operator's, or a stated
  yellow band for the yellow lines. The margin: the highest of 45, 40, 35,
  30, 25, 20 whose best colour costs at most 7 (pull units) more than the
  floor's. Lines in one city went in order, each seeing the ones already
  moved; a line drawn on several maps took one colour clearing all of them.
  `scripts/line_colour_search.py` was not run: it recolours every line in a
  city, and the brief was to move only these. Old and new (CIE76 to the
  nearer of olive / violet, then to any pin where lower):
  - Bucharest M4 #608000 (11.6) to #247810 (30.0); M1 #989800 (15.7) to
    #B48C00 (25.8), a dark gold.
  - Kyoto Karasuma #608000 (11.6) to #387C04 (25.4); Keihan Main #586818
    (15.8) to #506C30 (25.6); Keihan Keishin #909040 (16.0) to #949054
    (25.2), Kyoto and Otsu one colour.
  - Hiroshima, toward Hiroden's #00A650: Yokogawa #889828 (11.8) to #08A850
    (46.0); Ujina #587808 (12.1) to #089860 (46.8); Miyajima #788430 (12.1)
    to #0C7C24 (35.4); Eba #586818 (15.8) to #247038 (36.9); Hakushima
    #989848 (18.1) to #60A450 (30.9).
  - Hankai Line, Osaka #516C00 (12.6) and Sakai #689000 (17.4), to #449418
    (30.3), now one colour; Osaka's Uemachi #9C9830 (13.3) to #7C9C48 (20.4);
    Nagahori Tsurumi-ryokuchi #7E9F1E (18.2) to #7CA014 (20.1).
  - Kawasaki JR Nambu Branch #909800 (14.9) to #B88C3C (27.6), an ochre in
    the 80-100 degree band from JR's #FFD400.
  - Tokyo Toei Shinjuku #889800 (15.0) to #78A03C (20.1); Chiyoda #586818
    (15.8) to #007034 (olive 39.4, green pin 25.3).
  - Sheffield Yellow #989800 (15.7) to #B48C00 (25.8), yellow kept: lane 4's
    whole-city search at 45 gave #28A800, a green, refused.
  - JR East's green, #586818 (15.8) on Akita's Oga, Fukushima's and
    Morioka's Tohoku and Mito's Suigun lines, to #007430 on all four (olive
    38.0, green pin 25.2).
  - London District #586818 (15.8) to #00A064 (48.0); Nottingham Line 1
    #586818 (15.8) to #008854 (45.1); Sapporo Streetcar #586818 (15.8) to
    #506C30 (25.6).
  - JR Takarazuka, Kobe #9F9504 (16.3), Amagasaki and Itami #A09808 (16.7),
    to #A8903C (20.1) on all three, a mustard in the 87-111 degree band;
    Kobe's Hokushin #7A9C1C (17.5) to #6CA424 (25.6).
  - Riga Tram 8 #9467bd (violet 14.0) to #b480cc (25.0); Rotterdam Tram 1
    #3f5ebe (violet 19.5) to #306ccc (25.2).
- **Every moved line clears 20; none fell short.** The four at the floor
  (Toei Shinjuku 20.1, the Nagahori 20.1, JR Takarazuka 20.1, the Uemachi
  20.4) sit in crowded yellow-green and ochre families where the 18-line
  separation leaves no wider colour in their hue. Closest pairs and
  dark-label separation held in every affected city (Hiroshima's closest
  pair now 18.0, Yokogawa / Miyajima, was 10.2).
- **Gaps between 20 and 45 recorded as an accepted trade in each affected
  config**, with the count and the nearest line, as Hiroshima's and Osaka's
  were. The UK configs' "every line >= 45 from every pin" is corrected to the
  truth: London (Circle 23.2, Lioness 43.0, Bakerloo 43.5, Suffragette 44.4),
  Sheffield (Yellow 25.8), Edinburgh (28.1), Manchester (Yellow 36.3),
  Newcastle (Yellow 32.5, Green 44.4); Nottingham, Glasgow, Birmingham,
  Blackpool and Liverpool hold 45. Other configs whose "clears CIE76 45 from
  every pin" predates the olive and violet pins, with no line under 20, are
  left as written: the claim describes the search's rule at its run date.
- **Nishinomiya's JR Takarazuka Line stays #C88800**, a different colour from
  Kobe's group for the same line, as before this change: #C88800 sits 7.6
  from Kobe's Shintetsu Ao Line, under the hard floor, so the group cannot
  take it. For the owner.
- `docs/data_sources/united-kingdom.md`'s Sheffield row names the new yellow.
  Maps re-rendered and checked on the branch, then reset: the batch
  re-renders every map after the merge.
