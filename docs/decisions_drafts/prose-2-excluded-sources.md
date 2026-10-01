# DECISIONS drafts - prose pass agent 2 (`prose-2-excluded-sources`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-01 - The two reference pages show one country at a time (owner)

- **The owner's brief (option B)**: keep What Is Excluded and Where this data
  comes from as their own pages, but show one country's section at a time
  under a selector, with the all-city material where a reader expects it.
- **The selector is a region radio, then that region's countries** (owner,
  2026-10-01, chosen in session from two piloted forms). Both are horizontal
  `st.radio` rows labelled "<Name> (<n cities>)", the Overview region
  selector's control (cleanup's request).
  - Measured at 375 px: one radio of all 24 countries was **396 px** tall.
    The region row is **127 px**, and the tallest country row (Europe, 14
    countries) is **281 px**. The Overview's region radio is 319 px.
  - The regions are the macro map's, with a country's halves folded
    together: North America, Europe, South America, East Asia, Oceania.
    Oceania has one country, so it shows no second row.
- **Placement (owner)**: the selector directly under the title, then the
  country's section, then the page intro and the all-city material. Before
  this, the selector sat **1,473 px** down the page at 375, below the intro,
  so a reader arriving from a city page landed about two screens above their
  country.
- **Default (owner)**: United States, first in `cities.COUNTRY_ORDER` (the
  Cities dropdown's order). `?country=` with a `cities.py` country opens that
  country and its region; an unknown or missing value opens the default
  without an error.
- **The documents stay whole on disk; the split is made at render time**
  (`app/country_sections.py`). Splitting `excluded_categories.md` into files
  per country, as `data_sources/` was on 2026-09-27, was rejected:
  `check_scope_disclosure.py`, `check_provenance.py` (numbered notices),
  `check_barred_marks.py`, `check_stale_claims.py`, `check_stray_bullets.py`
  and `scripts/france_excluded_section.py` all read the single file.
  - **How a part gets a country:** a heading that names exactly one
    country's cities (or the country, or an alias such as SFMTA) is that
    country's. A heading naming none inherits its parent's country. One
    naming two countries stays shared. Inside the notices section, each
    numbered notice is judged by its title the same way.
  - **Anything unmatched stays shared, so a part can be misfiled but never
    dropped.** A new city's section lands under its country with no edit.
- **Nothing lost, measured**: both pages were captured before the change.
  After it, all 24 country views of each page were captured. Every line of
  the before text renders after, at least as many times: **0 lines lost** on
  either page (`data/_review/prose-2-excluded-sources/text_diff.md`). The
  only new lines are the selector labels and the heading "Stations left out
  in <country>".
- **The station table is per country**, under that heading. Its columns
  follow the site-wide totals, so every country shows the same columns. The
  site-wide total paragraph stays in the shared part.
- **Four paragraphs of `docs/data_sources.md` were moved back, verbatim**,
  so the split files each with its own notice.
  - The note that notice 7's heading "read NOT YET DISPLAYED" was moved back
    above notice 8, its place before INEGI was inserted (`0fa3e557`).
  - "**20 amended in the same change**" was moved under notice 20. It had
    drifted below notice 83.
  - "What has grown instead" was moved back after "Where this leaves the
    project", where `95edc72b` put it.
  - "Not required by anyone, but good practice ..." was moved to the head of
    the list, before notice 1. It is the one move with no earlier position to
    restore: its old place, after notice 8, would have filed it under Mexico.
- **Rejected**: a single 24-country radio (the owner's choice, on the height
  above), and a selectbox (cleanup: one kind of control across the site).
