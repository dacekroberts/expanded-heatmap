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

- Re-render on master, in the same sitting as the push, every map whose
  pins or menus move: 50 food-shop maps (antwerp, birmingham, blackpool,
  bucharest, edinburgh, fukui, fukuoka, ghent, glasgow, goteborg,
  higashiosaka, himeji, hiroshima, hong_kong, kagoshima, kawasaki,
  kitakyushu, kitchener_waterloo, kobe, kumamoto, kurume, kyoto, liverpool,
  london, manchester, matsuyama, minneapolis, nagasaki, nara, newcastle,
  nishinomiya, nottingham, okayama, osaka, otsu, pittsburgh, sakai,
  sapporo, sasebo, sheffield, shimonoseki, stockholm, takamatsu,
  thessaloniki, tokyo, toyama, toyota, utsunomiya, yokkaichi, yokosuka), 6
  shops-and-services maps (amsterdam, daugavpils, den_haag, liepaja, riga,
  rotterdam), ottawa and palma (menus), plus any city whose legend wording
  the owner approves below. `python pipeline/drift_check.py --render-only
  <cities>`, never steps 1-2.
- Downstream note to Visuals and Analytics (pins changed colour).

## Open for the owner

- **Legend wording for the licensed retail slices that stay blue** (owner:
  they stay blue; wording to the owner before it renders). Drafted in chat
  2026-10-07; not built.
- **The Japanese legend/menu pair** (and Thessaloniki's, which copies it):
  legend "Food retail (no general retail is published)", menu "Food
  shops". Drafted in chat; not built.
- **Ottawa's one food layer**: recommended to stay magenta with its
  "Restaurants and food shops" legend. Not changed.

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
  re-rendered, which the assessment had not counted. Brought to the owner.

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
