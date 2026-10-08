# DECISIONS drafts - two-level region selector (`region-selector`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

The branch is cut from master `b24f66a2` and lands at review time; it is not
pushed before then. It touches `app/` (`app/Overview.py`, `app/cities.py`,
`app/country_sections.py`), so landing it IS deploying, and `app/cities.py`
is a module the app imports: **reboot the deployed app after the push.**

**Downstream inputs this branch changes**: `app/cities.py` gains three region
views, "Canada", "Japan" and "South Korea" (composites); the five-city view
once named "South Korea" is renamed "South Korea outside the capital area";
`REGIONS` grows from 33 to 36 entries. The tag on the five Korean cities
outside the capital area changes, so Visuals or Analytics code keyed on the
old view name needs the new one. No map, output or taxonomy changes.

## Landing checklist

- deploy-verify `scope: map-chrome` at review time, at 375 and 1200 px: the
  dropdowns at a phone width, the pills on a wide screen, `?region=Kansai`,
  a city page's region button, the "Canada", "Japan" and "South Korea"
  views.
- Reboot the deployed app after the push (`app/cities.py` changed).
- `python scripts/check_macro_labels.py`: PROBLEMS 0, 36 regions x 3 widths
  (measured on this branch).

## For the owner at review time

- **Daegu's region button reads "South Korea outside the capital area"**,
  the view's full name, as every city's button reads its view's name. At
  375 px it is 227 px wide and wraps the map's button row onto a third line
  (108 px tall); the legend's clearance follows the row, as it does for any
  fourth button. A shorter button label would be a new, per-view name.

---

### 2026-10-07 - South Korea becomes one first-row view, like Japan

**Decision.** The region menu's first row has one "South Korea" view
covering all 18 Korean cities, a composite of the Seoul Capital Area and the
five cities outside it. Its second row: "All of South Korea (18)", "Seoul
Capital Area (13)", "Outside the capital area (5)". The five-city view once
named "South Korea" is renamed "South Korea outside the capital area", a name
that stands alone in a caption ("Showing 5 cities in South Korea outside the
capital area."); the menu drops its parent's name, as "United States West"
reads "West". Owner, 2026-10-07 ("i agree with your recommendations", on the
recommendations of the entry below). The same call approves the "Closer
view" label and the "All of ..." option names, and keeps the whole-country
Canada and Japan views.

**Why.** It fixes review lane 3's O3: the old name captioned 5 cities as
"in South Korea" when the site has 18, and one country took two first-row
choices.

**How it is built.**
- The five cities' `region` tag, `REGION_ORDER`, `COUNTRY_VIEWS`, East
  Asia's `REGION_LABELS_ALSO` and `country_sections.REGION_GROUP` take the
  new name; `_CAPTION_NAME` maps both Korean views to "South Korea", so East
  Asia's caption reads "with the main cities of Japan and South Korea
  labeled too" (it named the Seoul Capital Area and South Korea before).
- The composite competes for labels: by hand, Seoul's pill covered
  Uijeongbu's dot at every width (3 problems); competing, PROBLEMS 0 over 36
  regions.
- Links: `?region=South Korea` from before (a back link's `?from=`, a
  bookmark) now opens the whole country, which holds the five cities it used
  to open. The in-map region button reads the app's link, so no map is
  re-rendered: Daegu's opens `?region=South Korea outside the capital area`.
- Renamed where the build path reads it too: the `korea-city` skill's
  region rule, `scripts/stress_overview.py`'s anchor in `COUNTRY_VIEWS`, and
  the master list's built-table row (`check_provenance.py` keys rows by view
  name).

**Checked.** One local render, 375 and 1200 px: `?region=South Korea` (both
rows set, "Showing 18 cities in South Korea.", both Korean list sections
open; 152 px of dropdowns at 375, 172 px of pills at 1200), the "Outside the
capital area" pill (the five-city view, its caption and list section), and
Daegu's in-map region button (back on that view, both rows set).
`check_macro_labels.py` PROBLEMS 0; `check_all.py` 50 of 50;
`check_deploy_imports.py` PROBLEMS 0 from the commit.

---

### 2026-10-07 - The region menu becomes two rows: broad views, then closer views

**Decision.** The macro map's region selector is two rows. The first holds
the broad views, in `REGION_ORDER`'s geographic order: Global, United
States, Canada, Mexico, Europe West, Europe East, United Kingdom, South
America, East Asia, Japan, Seoul Capital Area, South Korea, Oceania, West
Asia (14; 13 since South Korea became one view, the entry above). The
second shows only when the chosen view has closer views, the
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
