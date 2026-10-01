# DECISIONS drafts - prose pass agent 3 (`prose-3-city-list`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-01 - The Overview's city list follows the region selector (owner)

- **The problem**: the list under the macro map was every city's link and
  blurb in one run, 124 cities long - dozens of phone screens.
- **The owner's direction**: one control, not two. The map's existing region
  selector drives the list.
- **Built**:
  - one closed section (`st.expander`) per leaf region, labelled like the
    selector, e.g. "Europe (26)";
  - the selected view's regions come first and open (United States opens
    its West and East halves);
  - every other region follows closed, in `REGION_ORDER` - the partition
    `cities.elsewhere_counts()` counts. So every view still lists all 124
    cities, and the caption "the list below, which always has all of them"
    stays true, unchanged.
- **The owner's three calls (2026-10-01), each the recommended option**:
  - Global opens no section: 13 closed sections, about one phone screen.
    Rejected: opening the United States to match the map's frame, and
    opening everything (today's length).
  - Each row keeps its link and blurb and adds the map tooltip's facts
    (mode, tier, storefront count; data age, placed by). A touch screen has
    no hover, so on a phone the list is the only place these show. Cost:
    Europe open measures 5,691 px at 375 against about half that blurb-only.
  - A small grey country label groups the cities where a region spans
    several countries.
- **Layout**: three cities to a row (`st.columns(3)`), which Streamlit stacks
  below 640 px. Europe open at 1200 went from 4,472 px in one column to
  3,258 px.
- **Unchanged**: the map, its layers, the label competition, the selector's
  behaviour, every caption. No new dependency, no new module, no new prose
  (every label is existing tooltip text or a region or country name).
- **Checks**:
  - `check_macro_labels.py`: PROBLEMS 0, caption arithmetic true in all 15
    regions;
  - `check_all.py`: 35 of 35;
  - `check_deploy_imports.py --ref HEAD`: clean.
