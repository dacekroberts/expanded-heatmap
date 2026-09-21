# What breaks as cities are added, and at roughly what count

Written 2026-09-21 at **7 built cities** (San Diego, San Francisco, Los
Angeles, Chicago, New York, Philadelphia, Miami), when the question came up of
how far this could go — Canadian cities, then other countries. These are
reminders to act on as the counts approach, not work to do now.

Each entry says what actually breaks, the number where it starts to hurt, and
what to do about it. Where a claim was measured or verified, that is stated;
where it is an estimate, it says so.

## The thing that does not break: per-page rendering

**A 50-city site has the same per-page weight as a 7-city site.** Each city
page embeds exactly one city's pre-rendered map, so the cost is bounded by the
*largest* city, not by how many exist. New York is the ceiling at 10.3 MB
(44,361 pins); Los Angeles is 3.5 MB, San Francisco 2.4 MB.

This is worth stating explicitly because it is the intuitive worry and it is
the wrong one. Adding cities does not slow down any page a visitor loads.

## Verified NOT a problem: page-number ordering

The obvious fear is that `app/pages/10_*.py` sorts before `2_*.py`, breaking
the sidebar at exactly ten cities. **It does not.** Streamlit's
`source_util.page_sort_key` applies `PAGE_FILENAME_REGEX` and returns
`(float(number), label)` — a numeric sort, not lexicographic. Checked against
the installed Streamlit in `.venv-lean` on 2026-09-21.

Recorded here so it is not raised again. No zero-padding needed.

## ~10 cities — the Overview macro map

The one page whose cost genuinely scales with city count, because it draws
every city at once. Markers already touch at phone width for Los Angeles and
San Diego, which is noted in `PLAN.md`.

**What to do:** cluster or group nearby markers, and consider showing each
city's mapped extent or a one-line summary in the tooltip rather than a bare
pin. Cosmetic and solvable; it does not threaten the architecture.

## ~20 cities — `outputs/` committed to git

**This is the real ceiling.** At 3–10 MB per city, 50 cities is 150–500 MB
*before history*, and every re-render commits a fresh multi-megabyte HTML blob
that diffs terribly. Twenty cities with a few re-renders each puts the
repository in the high hundreds of megabytes.

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

## 40+ cities — hosting

Streamlit Community Cloud's ~1 GB memory and sleep-after-inactivity behaviour,
plus the one-private-app limit if the repository goes private, start arguing
for a different story. The likely shape is vector tiles rather than per-city
static HTML with embedded pins — a much larger change than anything above, and
one that would revisit the pre-rendered-HTML invariant itself.

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
