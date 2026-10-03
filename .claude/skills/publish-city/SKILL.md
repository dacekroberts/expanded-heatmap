---
name: publish-city
description: Take finished city work from a branch to the live site - the gate order, which checks catch what, when a full deploy-verify is required versus wasteful, and why landing app/ on master IS deploying. Use when a built city is ready to go public, when merging an app-touching branch to master, or when asked to publish or deploy. Not for building a city (add-city) and not for pipeline-only work, which never reaches the deployed app at all.
---

# Publishing a city

The deploy path is long and **two of its steps are invisible**:
landing `app/` on master *is* deploying, because Streamlit Cloud pulls master
automatically; and an "Updated app!" does **not** reload imported modules. Both
have cost real outages.

Written 2026-09-22, after a publish in which the gate worked and two things
still nearly went wrong for want of it — a full `deploy-verify` was almost
re-run out of reflex at ~186k tokens, and the agent correctly reported "no
reboot needed" for the three commits it was handed while the actual push
changed `app/components.py`.

**Deploys are batched (owner, 2026-09-27).** A finished `app/` change waits on
its branch until the owner calls "review time". Everything queued then lands in
one push, with one reboot and one live check. Only a broken live site or a
removal request goes out on its own. `deploy-verify` runs once per batch, at
review time; during the day a session checks its own `app/` change with at most
one quick browser render. The whole process is in
`docs/review_time.md`. Why: `docs/efficiency_review_2026-09-27.md`, change 2.

**Renderer changes batch the same way.** This covers `map_common.py`,
`theme.py`, `linecolour.py` and the shared blocks. Iterate on 3-5 sample maps
and re-render every city once, at review time, as part of that one push. Until
then `check_render_current.py` fails, so the pre-push hook holds the branch
back. Comment-only edits do not count. Of 14 full re-renders from 09-23 to
09-27, 12 would have fitted into three (finding 4).

---

## The order, and what each step can see that the others cannot

Run these in order. Each catches a class nothing else does.

| # | Step | Catches |
|---|---|---|
| 1 | `python scripts/check_no_fetch_in_steps.py` | a step that reaches the network, **including through a shared module** |
| 2 | `python pipeline/drift_check.py --jobs 2` (a heavy job: announce it, per `docs/session_roles.md`) | committed outputs that no longer regenerate |
| 3 | `python scripts/check_personal_exposure.py <city>`; record the verdict in DECISIONS and its row in `docs/privacy_verdicts.md` | a person's name at their address; a city published with no verdict (`check_privacy_verdicts.py`) |
| 4 | `python scripts/check_provenance.py`, `python scripts/check_inconsistency_list.py` and `python scripts/check_ring_shares.py` | a city whose sources were never recorded; notices vs `_NOTICES`; a city with no row in `docs/map_inconsistencies.md` (the internal evidence for the "Why the maps differ" page), or without its three summary fields in `app/cities.py` (`rail_extra`, `record_kind`, `categories`) or its in-ring share in `app/ring_shares.json` (`--write` after the final render), which that page's table is built from |
| 5 | `python scripts/brief_check.py <city>` | a brief's claims that stopped being true |
| 5a | **read the page and the city's doc sections against `docs/city_page_format.md`** (below) | a city's gap filed under a shared heading, wording that does not read well; `check_city_page_format.py` (in `check_all`) already fails a page out of order or a path in its text |
| 6 | **merge to your branch, commit** | — |
| 7 | `python scripts/check_deploy_imports.py` | an import that works locally and not on a clean clone under the lean venv |
| 8 | `deploy-verify` (scope below) | what the rendered page actually looks like |
| 9 | **merge to master, push** | this is the deploy |
| 10 | **REBOOT the app** — the owner's action | stale cached modules |
| 11 | **verify on the live URL**, not locally | everything the working tree cannot show |

### Three ordering rules that are not obvious

- **Step 7 must run on the commit you are about to push**, not on `HEAD` before
  your edits. `check_deploy_imports` clones a ref; running it before committing
  checks the wrong tree and says `PROBLEMS 0` about code you did not write.
- **Steps 1–5 are cheap and 8 is not.** Never reorder so that the expensive one
  runs first and finds something the cheap one would have.
- **`git checkout -- outputs/` after step 2** if it reports zero drift but
  leaves files modified. On Windows the regenerated files come back CRLF and
  Folium assigns fresh element ids every render, so committing that churn
  rewrites files the deployed app reads for no change at all.

---

## Step 5a: the page against the format

Every city page is published in one format (owner, 2026-10-01;
`docs/city_page_format.md` is the spec). Open the city's page file and read
it top to bottom:

- [ ] `render_city_nav("<Name>")`, then `render_city_title("<Name>")`: the
  name alone, as in `app/cities.py`, over the shared subtitle. No `st.title`
  of the page's own, no "<City> Heatmap" heading.
- [ ] **The map directly after the title**, nothing between:
  `st.iframe(HEATMAP_HTML, width=1000, height=650)`.
- [ ] The captions directly under the map: the data dates
  (`render_data_age`, or the city's provenance caption) and any credit its
  sources prescribe word for word.
- [ ] Short bullets under bold headings (**The lines**, **The businesses**,
  a third only where needed); no intro paragraph above the map, no prose
  paragraphs, no controls paragraph of the city's own, no TODO left.
- [ ] Stations left out are "listed below", never a file path. No
  repository path or file name, script, check or skill name, decision log or
  build brief anywhere in page text.
- [ ] Then, in order: `render_map_help(...)`, `render_excluded_stations(...)`,
  `render_country_links(...)`, and `render_site_notices()` last, inline,
  never behind an expander.
- [ ] Reader-facing text in US spelling, except the notices, license titles,
  quotes, a register's own category names and official names (spec section 4).
- [ ] In `docs/excluded_categories.md` and `docs/data_sources/<country>.md`,
  every heading for the city names it; its gaps and limits sit in its own
  section, not the shared "What is missing rather than excluded" or "Honest
  limits"; process notes are absent or between `<!-- internal -->` markers.
- [ ] Any sentence no approved template covers is flagged as a proposal in
  the drafts file, for the owner at review time.

**The checks that read page text, and what each one sees:**

| Check | Reads | Fails (or reports) |
|---|---|---|
| `check_city_page_format.py` | every `app/pages/*_Heatmap.py`, as code | the title not first, anything between the title and the map, `render_site_notices()` not last, map help, the stations list or the country links missing; a repository path, script, check or the decision log named in rendered text |
| `check_deploy_imports.py` | every `app/pages/*_Heatmap.py` | no `render_site_notices()`; no `render_city_nav`, or its name not the `cities.py` name; a `page_title` not starting with the city's name |
| `check_scope_disclosure.py` (property F) | the city's page and `docs/excluded_categories.md` | a city whose stations are thinned by spacing and which says so in neither ("thinned", "one stop per half mile") |
| `check_provenance.py` J | page prose and the docs | an `outputs/...` file named there that is not committed (the format names none on a page) |
| `check_provenance.py` M | the pages of a country whose licence prescribes its credit | the credit missing as a literal in an `st.*` call, or only inside an `if`/`try` (« Source : Insee » on French pages) |
| `check_stray_bullets.py` | the docs the app renders | a wrapped spaced dash the app would draw as a bullet |
| `check_stale_claims.py --only E` | `app/Overview.py`, `app/pages/*.py` and the rendered docs | reports "the only", "no other", "every other" claims; never fails |
| `rendered_surfaces.py --check` | every page under `app/` | `docs/rendered_surfaces.md` stale: run `--write` after adding a page |

None of them checks the bullets, the spelling or the process notes on the
reference docs (`check_internal_markers.py` checks only the markers): that is
the read-through above.

---

## Choosing the `deploy-verify` scope — the expensive decision

A full sweep is **~186k tokens and ~27 minutes**. The rule reads "full before
any real deploy", and read literally that is wrong often enough to matter.

**`full` is for a BATCH of unverified work.** Several cities, or a chrome
change touching every page, or a backlog nobody has checked piece by piece.

**A narrow scope is correct after repairing something a full sweep just
found.** That case is specific and recognisable: a full sweep passed everything
except one defect, you fixed that defect, and `drift_check` says the other
cities' outputs are **byte-identical to the ones it already passed**. Re-running
full re-examines identical files. Measured 2026-09-22: `map-chrome` cost ~106k
against ~186k and caught the thing that mattered.

**Ask: what changed since the last full sweep?** If the answer is "one city's
output and the code that produced it", scope narrowly and say so in the report.
If you cannot answer, run full.

**And state the scope explicitly every time.** An unstated scope now runs
`map-chrome`, so silence no longer buys the expensive run by accident — but it
also no longer buys the thorough one, which is the point.

---

## The reboot, which is the step everyone skips

**Streamlit Cloud's "Updated app!" re-runs the entry script and leaves imported
modules cached.** The live site stayed down over three hours on 2026-09-22
across five pulls for exactly this.

**You need a reboot if the push changed any module `app/Overview.py` imports** —
in practice `app/cities.py` (changes with *every* city) or `app/components.py`
(changes whenever a notice does). A new page file under `app/pages/` alone does
not.

**Renaming or removing a page that a cached module names breaks EVERY page
until the reboot**, not just that page. On 2026-10-02 the info pages lost
their numbers. The cached `components.py` still linked
`pages/201_What_Is_Excluded.py`, and every city page and the Overview raised
`StreamlitPageNotFoundError` in the footer until the owner rebooted. Push such
a change only when the owner can reboot straight away, and check one city
page live after.

**`deploy-verify` cannot tell you this and will sometimes say the opposite in
good faith.** It judges the diff it is handed. Hand it three commits that touch
only `pipeline/` and it will correctly report that no reboot is triggered —
while the *push* you are about to make also carries the branch's earlier
`components.py` change. **Compute the reboot question from the whole push**
(`git diff --stat <deployed-ref> <new-ref> -- app/`), never from the last few
commits.

**No session can reach the Streamlit Cloud console.** This is the owner's
action. Say so plainly and do not report the city as live until they confirm.

---

## Verify on the live site, and look at something you did not change

Not locally. The working tree cannot show you a cached module, a CDN, or a
process that never restarted.

- The region switcher and macro map still land where they should, and the
  new city's dot shows the colour of its `mode` and the fill of its
  `coverage` that the owner approved (the two-key legend, 2026-09-30).
- The new city's page renders in the page format's order: title and
  subtitle, the map, its captions, the bullets, "Using the map", the stations
  left out, the two country links, and the site notices last. Its map draws
  its labels and the OSM credit.
- **One city you did not touch.** This is the highest-value minute in the whole
  process: on 2026-09-22 the new city rendered wrong at a narrow viewport and so
  did **Chicago**, untouched for weeks, which is what proved the fault was a
  pre-existing intermittent race rather than the change just shipped. Without
  that second data point the obvious conclusion would have been wrong and a good
  fix would have been reverted.

---

## What must be recorded before calling it done

- `DECISIONS.md`: the publish, the verification evidence, and any position taken
  rather than resolved.
- `PLAN.md`: the reboot and any owner action, ticked or added.
- Any **affirmative obligation** owed to a publisher (`read-licence` step 6c) —
  these survive the deploy and are the likeliest thing to be forgotten once the
  site is up, precisely because everything else finished.

## Checklist

- [ ] Steps 1–5 green, with `git checkout -- outputs/` after the drift check
- [ ] Step 5a: the page and the city's doc sections read against
  `docs/city_page_format.md`
- [ ] `check_deploy_imports` run **on the commit being pushed**
- [ ] `deploy-verify` scope chosen deliberately and stated
- [ ] Reboot question computed from **the whole push's `app/` diff**
- [ ] Pushed to master; owner told plainly whether a reboot is required
- [ ] Live URL verified, **including one city not touched**
- [ ] `python scripts/downstream_changes.py <old master> <pushed>` run, and its
  output sent to the Visuals and Analytics sessions unless it says "nothing
  downstream" (`docs/session_roles.md`, "Downstream sessions")
- [ ] `DECISIONS.md` and `PLAN.md` updated; publisher obligations carried forward
