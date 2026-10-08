# DECISIONS drafts - two-level region selector (`region-selector`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

The branch is cut from master `b24f66a2` and lands at review time; it is not
pushed before then. It touches `app/` only (`app/Overview.py`,
`app/cities.py`), so landing it IS deploying, and `app/cities.py` is a
module the app imports: **reboot the deployed app after the push.**

**Downstream inputs this branch changes**: `app/cities.py` gains two region
views, "Canada" and "Japan" (composites), and `REGIONS` grows from 33 to 35
entries. No map, output or taxonomy changes. Visuals' pieces that list the
region menu or count its views would need the new two-row shape.

## Landing checklist

- deploy-verify `scope: map-chrome` at review time, at 375 and 1200 px: the
  dropdowns at a phone width, the pills on a wide screen, `?region=Kansai`,
  a city page's region button, the "Canada" and "Japan" views.
- Reboot the deployed app after the push (`app/cities.py` changed).
- `python scripts/check_macro_labels.py`: PROBLEMS 0, 35 regions x 3 widths
  (measured on this branch).

## Proposals flagged for review time (UI text no template covers)

- The second row's label, "Closer view", and its first option, "All of
  Japan (64)" / "All of the United States (20)"; a half drops its parent's
  name under that parent ("West (7)", "East (13)").

## Open for the owner

- **Korea stays two first-row choices**, "Seoul Capital Area (13)" and
  "South Korea (5)". One "South Korea" choice with the capital area as a
  closer view would need a composite named for the whole country, and that
  name is already the leaf view of the five cities outside the capital
  area; renaming that view changes links, captions and the city list, so it
  is the owner's call.
- **The "Canada" view reverses part of 2026-09-22**, when one Canada view
  was rejected for leaving every city near an edge. It exists because the
  owner listed Canada in the first row with West and East beneath it; it
  competes for labels and is never the default.

---

### 2026-10-07 - The region menu becomes two rows: broad views, then closer views

**Decision.** The macro map's region selector is two rows. The first holds
the broad views, in `REGION_ORDER`'s geographic order: Global, United
States, Canada, Mexico, Europe West, Europe East, United Kingdom, South
America, East Asia, Japan, Seoul Capital Area, South Korea, Oceania, West
Asia (14). The second shows only when the chosen view has closer views, the
broad view first as "All of ...": the United States (West, East), Canada
(West, East), Japan (its 12 views with cities: Hokkaido, Tohoku, Kanto,
Saitama Prefecture, Tokyo Metropolis, Chubu, Kansai, Osaka Prefecture,
Hyogo Prefecture, Chugoku, Shikoku, Kyushu-Okinawa; Chiba Prefecture joins
when it has a city) and Europe West (France North, France South, Benelux,
Germany, Czechia). `?region=<any view>` opens with both rows set, and either
row keeps the URL current.

**Why.** The flat list of 33 views measured 665 px tall on a 375 px phone
(review lane 3), so the map began about 1,378 px down. Owner's decision,
2026-10-07.

**How it is built.**
- *Grouping, derived where it can be* (`app/cities.py`, `SUB_VIEWS`,
  `MENU_TOP`, `MENU_SUB`): a composite's closer views are its members
  (`REGION_MEMBERS`); Europe West's are written out, its country views less
  the United Kingdom, which the owner placed in the first row. Every other
  view is a first-row view, so a new region joins the first row with no
  edit. `cities.py` raises on a view named under two parents, a parent that
  is itself a closer view, or a name not in `REGION_ORDER`.
- *Two new views*, "Canada" (Canada West + Canada East) and "Japan" (every
  Japanese view), as composites on the United States' pattern, because the
  broad view stays selectable. By hand their labels failed
  `check_macro_labels.py` (Edmonton x Kitchener-Waterloo, 3 problems;
  Japan's anchors over nine neighbours' dots, 27), so both compete for
  labels (`COMPETING_REGIONS`, whose check now admits a composite other
  than Global): PROBLEMS 0, 35 regions x 3 widths, no member dot off the
  canvas in either. Captions: "Showing 7 cities in Canada." and "Showing 64
  cities in Japan."; the list beneath opens every member region, as the
  United States' does.
- *Widget, measured* (one local render, 2026-10-07): `st.pills` on a screen
  wider than 640 px (Streamlit's column breakpoint), `st.selectbox` at or
  below it; both are drawn and CSS shows one, each set from the URL before
  it is drawn. The URL is the state: a widget's callback writes
  `?region=`, so the page never reads a URL one click behind, and a pill
  clicked a second time (which clears it) keeps the view shown.
- *Heights*, the menu itself:

  | width | view | before (one radio) | pills | dropdowns (shipped at 375) |
  |---|---|---|---|---|
  | 375 px | Global | 665 px | not measured | 68 px |
  | 375 px | Japan / Kansai | 665 px | 568 px | 152 px |
  | 1200 px | Global | not measured | 96 px (shipped) | |
  | 1200 px | Japan | not measured | 208 px (shipped) | |

  At 375 px the map now starts 781 px down on Global and 865 px with two
  rows, against about 1,378 px before.

**Checked.** At 375 and 1200 px: choosing Japan then Kansai (URL
`?region=Japan`, then `?region=Kansai`; Kansai's caption and its one open
list section unchanged), a direct `/?region=Kansai` link (both rows set),
Global (the parameter dropped, the landing caption, no section open), and
Kyoto's in-map region button (back on Kansai with both rows set).
`check_macro_labels.py` PROBLEMS 0; `check_all.py` 50 of 50.
