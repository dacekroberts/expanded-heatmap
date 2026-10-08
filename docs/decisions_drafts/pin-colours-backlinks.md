# DECISIONS drafts - pin colours and back links (`pin-colours-backlinks`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

The branch is cut from `japan-regions` (which carries `europe-split`) and
lands with them at review time; it is not pushed before then. Approved by
the owner on 2026-10-07: DECISIONS, "Four ideas assessed before the large
review", items 1 and 2.

**Downstream inputs this branch changes** (for the lander's
`downstream_changes.py` check): the shared map code
(`pipeline/map_common.py`), `pipeline/taxonomies/` (the shared palette and
fourteen modules), two city configs (Hiroshima, Osaka), and, once the
landing re-render runs, the `outputs/<city>/heatmap.html` of every city in
the list below. Visuals' cards show pins, so the landing note to Visuals
names the colour change.

## Landing checklist

- **Re-render EVERY map, render-only** (`python pipeline/drift_check.py
  --render-only`, never steps 1-2): the region button and the legend's
  clearance live in `pipeline/map_common.py`'s chrome, so every map
  changes, not only the 58 whose pins or menus move. Cleanup does this on
  the integration branch before pinning (206 maps with the 30 new Japanese
  ones; Cleanup, 2026-10-07). Measured on that branch's committed HTML: none
  of the 30 has a line within CIE76 10 of a pin it will draw (nearest to
  olive 15.8, Akita, Fukushima, Mito, Morioka), and none draws violet.
- deploy-verify `scope: map-chrome` at review time (the button row, both
  themes, a phone width).
- Downstream note to Visuals and Analytics: pins changed colour on 56
  maps, eight legends and fourteen menus changed wording, every map gained
  the region button.
- `check_provenance.py` fails on this branch only on
  `docs/city_master_list.md`'s counts (176 built against the list's 170,
  the new region rows), which Staging writes at landing.

## The owner's calls (2026-10-07, in this build's chat)

- City pages: the region link is a **button in the map**, beside "Global
  View" (recommended), over a Streamlit link above the title.
- Japan and Thessaloniki: the legend takes the menu's name, **"Food shops
  (no general retail is published)"** (recommended); the menu stays "Food
  shops".
- The eight wordings for the blue licensed slices: **approved as drafted**.
- Ottawa's one food layer: **stays magenta** (recommended).

### 2026-10-07 - The owner's calls on the pin colours and the back links: a region button in every map, eight legends naming their licensed slices, Japan's legend, Ottawa stays magenta (owner)

- **Decided (owner): a city page's region link is a button inside the map,
  beside "Global View".** The rejected option was a Streamlit link above
  the title, which would have needed no re-render but would not sit beside
  the button. The map reads the link and its words ("← Kansai") from a
  hidden link that `components.render_city_nav` renders from the city's
  `region` in `app/cities.py`, in a container of its own
  (`map-region-nav`) so the map's Cities menu never lists it. A region
  renamed or a city regrouped therefore needs no map re-rendered, and an
  older app or a map opened alone leaves the button hidden. Clicking it
  opens the Overview on that region (`?region=`). Every map re-renders once,
  at landing.
- **Decided: on a phone the button row wraps, rather than truncate a
  region's name.** Measured in a 343 px frame (a 375 px phone): Cities 78,
  Global View 94 and Dark mode 94 px already filled 278 of the 287 px
  available, so any fourth button wraps the row to two lines (72 px tall),
  even "← Kansai" (65 px); the longest names ("← Seoul Capital Area") are
  129 px. Labels already avoid the button row's live box. The open legend's
  cap assumed a fixed 56 px clearance, so it now follows the row: the
  button's script sets `--hm-actions-clear` to the row's bottom plus the
  same 16 px gap (98 px wrapped), and the cap falls back to 56 px. At
  desktop widths the row stays on one line (408 px of 854). Rejected:
  ellipsizing the region name, and an icon-only theme button, which would
  change every map's existing control to make room.
- **Decided (owner): eight Retail legends and menus name what their
  licensed slice holds; the pins stay retail blue.** Measured on each
  city's clean file: Philadelphia "Food shops, tire and precious-metal
  dealers" (food 88.5%, tire 5.3%, precious metal 4.8% of 1,529); Boston
  "Food, liquor and cannabis shops" (61.8, 33.2, 4.9% of 791); New York
  "Food, secondhand, electronics, tobacco shops" (50.0, 15.8, 10.3, 10.6%
  of 22,614; also products for the disabled 6.8% and stoop stands 4.7%),
  which supersedes the 2026-09-21 call to keep its legend broad; Buffalo
  "Food stores, used-car and secondhand dealers" (76.5, 15.0, 4.9% of 728);
  Toronto "Vape, secondhand, precious-metal, pawn shops" (45.6, 30.1, 11.2,
  6.0% of 814, and NO food: the brief had listed it as a mostly-food slice);
  Seoul, Daegu and Busan "Food, convenience and tobacco shops" (98-99%). At
  most 44 characters, the length the Japanese legend already shipped at.
  `layer_label = legend_label` in each of the six modules.
- **Decided (owner): the Japanese legend reads "Food shops (no general
  retail is published)"** (was "Food retail (...)"), so legend and menu
  ("Food shops") name the same olive meaning; Thessaloniki's module copies
  it. Ottawa's single food layer stays magenta with its "Restaurants and
  food shops" legend.
- **Verified:** Kyoto rendered with the button and shown in the lean app:
  at desktop one row ("← Kansai" 79 px), the hidden region link absent from
  the Cities menu and invisible on the page, and a click opened the
  Overview on Kansai; at 375 px the row wrapped to 72 px and the legend cap
  measured 528 px (650 - 24 - 98). Liepaja, Birmingham, Hiroshima and Osaka
  re-rendered with the new chrome. `check_map_markup.py` 0 problems
  (legends intact); `check_provenance.py`'s invariants and the legend clamp
  pass.

### 2026-10-07 - Back links beside "Global View": the reference pages return to the city or region the reader came from; the Overview opens on a region in its link (owner)

- **Decided: a reference page learns its reader's origin from `?from=`,**
  carried in every link into About the Data, What Is Excluded, Why the Maps
  Differ and Required Notices the way `?country=` already is: from a city
  page the city (its footer row and its two country links), from the
  Overview the region shown. Each of the four pages opens with "← Global
  View", then "← Back to <city or region>", then its links to the others,
  which forward the same origin; About the Data's in-page country links keep
  it too. A bookmark, an unknown name, or the Global region shows "← Global
  View" alone. One key serves cities and regions because no name is both
  (176 cities, 31 regions, 2026-10-07). Helpers in `app/components.py`
  (`back_origin`, `from_params`, `render_back_link`,
  `render_reference_nav`); `render_site_notices()` takes `origin=`.
  Rejected: `st.session_state` as the carrier, which a reload, a new tab or
  a shared link loses.
- **Decided: the Overview opens on `?region=` and writes the region shown
  back to the URL** (none for Global), so a reload or a shared link returns
  to it. The link is applied only when it changed since the page last wrote
  it, or when the radio has no state (Streamlit drops it when the reader
  leaves the page), the rule `select_country()` already follows: a click
  updates the radio before the rerun while the URL still holds the old
  region.
- **Verified with one local render (lean venv):** `/?region=Kansai` opened
  on Kansai with its footer links carrying `from=Kansai`; a click on
  Kyushu-Okinawa moved the URL and held; its "Why the maps differ" link
  showed "← Back to Kyushu-Okinawa", which reopened the Overview on that
  region; Kyoto's "Where this data comes from: Japan" opened
  `?country=Japan&from=Kyoto` with "← Back to Kyoto"; `/Required_Notices`
  with no origin showed "← Global View" alone. No exceptions.
  `check_deploy_imports.py` (clean clone at 4ed2137e) and
  `check_macro_labels.py` (31 regions x 3 widths): 0 problems.
- **Open: the city pages' link.** A city page shows no Streamlit "Global
  View" (map-only navigation); its "Global View" is a button inside the map,
  so a link beside it needs `pipeline/map_common.py` and every map
  re-rendered, which the assessment had not counted. Brought to the owner,
  who chose the button in the map (the entry above).

### 2026-10-07 - One pin colour per meaning: food shops olive, shops and services violet, a refuse-both guard, three line colours moved (owner)

- **Decided: a bucket's pin colour follows what it MEANS in its taxonomy,
  not its name.** Measured on this branch's 176 maps (the colour agent's
  `evaluate.py`, re-run 2026-10-07): retail blue was drawn for general
  retail, for food shops only (50 maps: the 30 Japanese food registers,
  Thessaloniki, the ten UK FSA cities, Antwerp, Ghent, Stockholm,
  Goteborg, Bucharest, Hong Kong, Minneapolis, Pittsburgh,
  Kitchener-Waterloo) and for shops and services together (6: Amsterdam,
  Rotterdam, Den Haag, Riga, Liepaja, Daugavpils). Food shops are now olive
  #737a00, shops and services violet #7e57c2; Retail blue, Food service
  magenta and Personal services green are unchanged. The bucket keeps its
  name in every count; a taxonomy states its meaning in `PIN_MEANINGS`
  (`{"Retail": "Food shops"}`), and `pipeline/taxonomies/__init__.py`'s
  `MEANING_COLOURS` and `pin_colours()` swap the colour in. Fourteen
  modules declare one. Every measured value is in the `MEANING_COLOURS`
  comment. Rejected: a fourth bucket, which would have changed every
  count, macro fact and continuity check for a colour.
- **Decided: the renderer refuses a map that draws violet beside blue.**
  Violet sits CIEDE2000 3.1 from Retail blue under deuteranopia (7.7
  under protanopia). `map_common.REFUSED_TOGETHER` and
  `_refuse_colours_together()` raise, naming the recorded backup: teal
  #37786e for Shops and services site-wide, with a dark outline ring on
  that layer (weakest pair Retail under tritanopia, 11.0). The ring is
  built and unused: `add_pin_layer(outline=...)`, fed by
  `MEANING_OUTLINES` (empty); with no outline every map's markup is byte
  for byte as before (tested in the session: the default stroke string is
  unchanged, a set outline changes only `color` and `weight`).
- **Decided: `check_line_colours()` compares a map's lines only with the
  pin colours that map draws**, so it now runs after the pin layers are
  built. Paris's #6E6E00 (6.6 from olive) and Ostrava's #688008 (8.1)
  would otherwise fail on a colour neither map shows. The line-against-line
  half still runs when no pins are drawn. Its printout names a bucket by
  its layer name ("vs Food shops", not "vs Retail").
- **Decided: three line colours moved off olive, by the smallest step that
  clears it by 12** (two points over the hard floor), under each city's own
  search rules: 3:1 on both map pages, CIE76 45 from the other pins the map
  draws, 18 from lines within 500 m (Osaka: from every line, its own rule)
  and 10 from every line. Hiroshima's Ujina Line #607808 (8.6 from olive)
  to #587808, a shade darker (moved 3.6); its Miyajima Line #788028 (9.6)
  to #788430 (moved 3.0); Osaka's Uemachi Line #8A8A24 (8.0) to #9C9830
  (moved 5.9; nearest line Nankai Koya 18.1). Two of the three are a
  touch LIGHTER, not darker as first proposed: darkening Ujina and
  Miyajima ran into the Eba Line (#586818) and the 3:1 floor on the dark
  page, and darkening Uemachi needed a move of 11.9 to clear olive. The
  Ujina search first returned a move of 18.8, because it held the line 45
  from Personal services green, which Hiroshima does not draw; measured
  against the drawn pins only, 3.6. Hiroshima's closest pair is now 10.2
  (Hakushima / Miyajima; was 10.6, Ujina / Miyajima), within 500 m still
  19.4. Nine of Hiroshima's twelve lines and twelve of Osaka's 34 sit
  below 45 from olive, recorded in each config as a trade. Every other
  food-shop map's lines clear olive's hard floor.
- **Decided: the layer menus say what the legends say.** `layer_label =
  legend_label` added to fsa_businesstype (10 cities), romania_dsvsa
  (Bucharest), minneapolis_inspection, pittsburgh_inspection,
  kitchener_waterloo_inspection (both its renamed layers), and to
  ottawa_inspection and palma_restauracio for their food layers. Berlin's
  "Personal services (partial)" legend beside a "Personal services" menu is
  left: the qualifier is a coverage note, not a different name. Zurich's
  "Licensed shops" (petrol stations and shops licensed under its
  Gastwirtschaft register) stays blue: not food shops only.
- **Decided: Madrid's map step reads the shared palette.** It carried its
  own copy of the three colours for its early line check; it now takes
  `pin_colours()` of its taxonomy, so a palette change cannot leave it
  behind. `scripts/line_colour_search.py` likewise searches against the
  city's own pin colours (olive included for a food-shop taxonomy).
- **Verified on the branch, outputs not landed in full:** render-only for
  Liepaja (violet), Birmingham (olive, menu "Food shops"), Hiroshima and
  Osaka (olive, moved lines) and Paris (no drift; its churn reverted).
  Normalized diffs show only pin colours, the menu name and the moved line
  colours. `check_map_markup.py`: 176 maps, 1,020 labels, 0 problems.
  `check_no_em_dashes.py` OK. The full re-render waits for landing.
