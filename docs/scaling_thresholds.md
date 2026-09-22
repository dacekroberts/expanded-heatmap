# What breaks as cities are added, and at roughly what count

Written 2026-09-21 at **7 built cities**, and **re-measured the same day at 9**
(adding Boston and Washington D.C.). These are reminders to act on as the
counts approach, not work to do now.

Each entry says what actually breaks, the number where it starts to hurt, and
what to do about it. Where a claim was measured or verified, that is stated;
where it is an estimate, it says so.

## Correction, 2026-09-21 — the headline number was wrong by about 3x

The first version of this file estimated **3–10 MB per city** and concluded
`outputs/` in git was "the real ceiling" at around **20 cities**. Both were
estimates, and measurement does not support either.

**Measured across all 9 cities:**

| City | Map HTML | | City | Map HTML |
|---|---|---|---|---|
| New York | **7.4 MB** | | Philadelphia | 1.1 MB |
| Los Angeles | 2.7 MB | | Washington D.C. | 0.7 MB |
| Chicago | 2.2 MB | | San Diego | 0.7 MB |
| San Francisco | 1.7 MB | | Boston | 0.5 MB |
| Miami | 1.2 MB | | | |

**`outputs/` total: 19 MB. Mean 2.1 MB per city, median 1.2 MB.** New York has
itself fallen from 10.3 MB to 7.4 MB, the coordinate-rounding lever having been
applied.

**History growth, measured:** 32 of 108 commits touch `outputs/` — about **3.5
outputs-commits per city**. Folium HTML is highly repetitive (coordinate
arrays, repeated JS) and zlib-compresses roughly 3–5x.

Projected at 50 cities: ~105 MB working tree, ~370 MB of raw blobs,
**~75–125 MB packed** — against GitHub's 1 GB soft limit, about 8x headroom.
**Storage is not the binding constraint**, and the sections below are corrected
accordingly.

## The thing that does not break: per-page rendering

**A 50-city site has the same per-page weight as a 7-city site.** Each city
page embeds exactly one city's pre-rendered map, so the cost is bounded by the
*largest* city, not by how many exist. New York is the ceiling at 10.3 MB
(44,361 pins); Los Angeles is 3.5 MB, San Francisco 2.4 MB.

This is worth stating explicitly because it is the intuitive worry and it is
the wrong one. Adding cities does not slow down any page a visitor loads.

## Page numbering — one myth and one real bug

**NOT a problem: sort order.** The obvious fear is that `app/pages/10_*.py`
sorts before `2_*.py`, breaking the sidebar at exactly ten cities. **It does
not.** Streamlit's `source_util.page_sort_key` applies `PAGE_FILENAME_REGEX`
and returns `(float(number), label)` — a numeric sort, not lexicographic.
Checked against the installed Streamlit in `.venv-lean` on 2026-09-21. No
zero-padding needed.

**REAL, and fixed 2026-09-21: the tenth city had no slot.** Different problem,
same number, and the first one masked it. The two info pages occupied
`10_About_the_Data.py` and `11_What_Is_Excluded.py`, while
`scaffold_city.py`'s `next_page_number()` globs `*_Heatmap.py` only — so with
nine cities built it would have generated `10_<Name>_Heatmap.py`, **straight
into the About page's slot.**

Fixed by renumbering the info pages to **90** and **91**, which leaves 10–89
free for cities and keeps them last in the sidebar where they belong.
`next_page_number()` needed no change, since it never counted them.
`app/components.py`'s `ABOUT_DATA_PAGE` and `EXCLUSIONS_PAGE` constants were
updated with it.

The lesson worth keeping: **"verified not a problem" was true of the question
asked and hid a real defect one layer down.** The sort was fine; the slot was
not.

## ~12–15 cities — the Overview macro map

The one page whose cost genuinely scales with city count, because it draws
every city at once. Markers already touch at phone width for Los Angeles and
San Diego, which is noted in `PLAN.md`, and the arithmetic showing the markers
**cannot** be displaced at a continental zoom is in `DECISIONS.md` — 1 px is
about 21.7 km there, so separating New York from Philadelphia would need
217 km.

**The owner's answer, decided 2026-09-21: open the macro map on a default
region rather than fitting the whole world, and make the global coverage
obvious in the UI.** Once the map spans continents, a single fitted view is
unreadable no matter how the markers are drawn — so the fix is to stop trying
to fit everything at once.

Two things that must come with it, or the feature costs more than it gains:

- **Signal the other regions explicitly.** A visitor landing on a
  region-scoped map must be able to see at a glance that other regions exist —
  otherwise the default silently hides most of the site. A region switcher plus
  a count ("9 more cities in Europe") is the minimum.
- **Do not make the default a per-visitor guess.** Geolocating the visitor
  adds a privacy surface this project has no reason to take on. A fixed
  default, changeable in one click, is simpler and defensible.

Cosmetic and solvable, and **it does not threaten the architecture** — which
is the whole reason it sits here rather than in `PLAN.md` as urgent work.

## ~150+ cities — `outputs/` committed to git — **CORRECTED, this is not the ceiling**

Originally recorded as "the real ceiling" at ~20 cities, on an estimate of
3–10 MB per city. **Measured, the mean is 2.1 MB**, and the projection above
puts 50 cities at ~75–125 MB packed against a 1 GB soft limit. The pressure is
real but it arrives far later than stated — on these figures, somewhere past
**150 cities**, which the research process will never reach.

The mitigations below stay recorded because they are still the right answers
*if* per-city size grows (a denser city than New York, or the opt-in all-city
layer being restored everywhere) — not because the limit is near.

The obvious escape — build at deploy time instead of committing outputs — is
closed by two invariants at once: the deployed app never runs the pipeline,
and geopandas on Streamlit Cloud breaks the deploy (`requirements.txt` must
stay lean). So the fix has to be on the storage side:

- **Git LFS** for `outputs/**/*.html`, the most likely answer.
- **Periodic history pruning**, which rewrites history and is disruptive.
- Reducing per-city size first. New York's measured levers are already in
  `PLAN.md`: 5 dp coordinate rounding saves 1.4 MB, string indexing ~1.2 MB,
  dropping the opt-in all-city heat layer 2.0 MB.

Interacts with the open question of whether to make the repository private
(see `PLAN.md`): LFS bandwidth and storage quotas apply either way.

## ~20 cities — `drift_check.py` runtime — **ADDRESSED 2026-09-21**

The check re-ran *every* city's pipeline on any pipeline change, which is O(n)
on a gate the project runs constantly.

**Done:** `pipeline/drift_check.py` now takes `--changed` (and `--since REF`),
mapping changed files to the cities they can actually reach — a city directory
to that city, `taxonomies/<t>.py` to the cities whose config declares
`TAXONOMY_SYSTEM = "<t>"`, and anything else under `pipeline/` to every city.
It is deliberately conservative: a shared file still means the full sweep,
because a wrong "nothing to do" is invisible until a deploy shows stale
output. A filtered run prints a `PARTIAL:` line naming what it skipped.

**Still true:** the unfiltered sweep is what runs before a deploy and when
recording a baseline in `DECISIONS.md`, and *that* remains O(n). If it becomes
painful, the next step is running cities in parallel rather than in sequence.

## CORRECTION, 2026-09-21 — RAM is NOT a function of city count

The "~40 cities strains Streamlit's memory" line below was inherited from this
file's first version and **was never verified**. It is wrong, and the reason is
worth knowing because it also says what *would* make it right.

**Measured, by reading the app rather than estimating:**

- **There is no caching anywhere in `app/`.** No `@st.cache_data`, no
  `@st.cache_resource` (grepped). So nothing accumulates across page visits or
  sessions — each request reads what it needs and releases it.
- **No city map contains another city's data.** The "All cities" control is a
  navigation button, not a data layer. (The "all-city heat layer" noted for New
  York is *city-wide* extent versus the ring subset — not cross-city.)
- **`Overview.py` loads only `pd.DataFrame(CITIES)`** — the metadata list from
  `app/cities.py`. It reads no `outputs/` file, so the macro map costs one row
  per city, not one map per city.
- **Streamlit runs only the visited page's script.** The other cities' pages
  never execute.

**Therefore the per-request memory ceiling is the LARGEST SINGLE map, not the
sum.** That is **New York at 7.43 MB**, against a community-tier allowance
around 1 GB — roughly 0.7% of it. Adding cities does not move that number at
all; only making one city *bigger* does.

**What the old claim conflated:** it bundled RAM with sleep-after-inactivity
and the one-private-app limit. Neither of those is a count question either.

**So RAM is not a constraint at any city count this project can reach.** The
count-sensitive limits are the macro map (~12–15, cosmetic) and repo size
driving deploy clone time (~150+).

**THE GUARDRAIL THIS DEPENDS ON.** All of the above holds *only while nothing
loads cross-city data*. Two plausible features would break it and make count
matter immediately:

1. **A combined map** drawing several cities' pins at once.
2. **An Overview that reads each city's outputs** to show statistics — row
   counts, densities, a leaderboard — rather than the static metadata in
   `cities.py`.

Either would turn a bounded per-request cost into one that grows with the city
count, and **at that point the ~40 figure becomes worth re-deriving.** Until
then it is not a limit, and should not be planned around as one.

## 40+ cities — hosting

Streamlit Community Cloud's ~1 GB memory and sleep-after-inactivity behaviour,
plus the one-private-app limit if the repository goes private, start arguing
for a different story. The likely shape is vector tiles rather than per-city
static HTML with embedded pins — a much larger change than anything above, and
one that would revisit the pre-rendered-HTML invariant itself.

## The stated allowance

Agreed 2026-09-21, on the measurements above:

- **20–25 cities is the planning ceiling.** Nothing in the stack forces it —
  it is set by the Overview macro map and by research cost per city.
- **~40 cities is the architectural line.** Past it, Streamlit Community
  Cloud's ~1 GB memory, its sleep-on-inactivity behaviour and repo-clone time
  on deploy start arguing for vector tiles instead of per-city static HTML —
  which would revisit the pre-rendered-HTML invariant itself.
- **Storage is not a constraint at any count this project will reach.**

Ordered by when each actually bites:

| Where | What | Severity |
|---|---|---|
| **City #10** | Page-slot collision | **Fixed 2026-09-21** |
| **~12–15** | Overview macro map legibility | Cosmetic, solvable |
| **~40+** | Streamlit Cloud memory, sleep, deploy clone time | Architectural |
| **~150+** | GitHub 1 GB soft limit | Not reachable in practice |

## The constraint that actually binds

None of the above.

Seven cities took roughly four days of dense work, and the expensive part was
never rendering — it was Step 0 research, taxonomy modules, privacy checks and
licence review. A single agency's terms of use consumed a large part of one
session on 2026-09-21, and turned up a clause affecting an already-built city
(MTA's "You will not modify or delete any of the data").

**The website will comfortably outscale the research process.** So effort
aimed at "more cities" belongs in reducing the marginal cost per city —
`scripts/scaffold_city.py`, a country-level screen run once per country rather
than per city, and choosing countries where one licence read and one taxonomy
cover many cities. That argues for depth per country over breadth across
countries: five Canadian cities are cheaper than five countries with one city
each, because the portal licence, the privacy regime and often the
classification amortise across them.
