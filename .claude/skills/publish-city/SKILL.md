---
name: publish-city
description: Take finished city work from a branch to the live site - the gate order, which checks catch what, when a full deploy-verify is required versus wasteful, and why landing app/ on master IS deploying. Use when a built city is ready to go public, when merging an app-touching branch to master, or when asked to publish or deploy. Not for building a city (add-city) and not for pipeline-only work, which never reaches the deployed app at all.
---

# Publishing a city

The deploy path is now nine steps long and **two of them are invisible**:
landing `app/` on master *is* deploying, because Streamlit Cloud pulls master
automatically; and an "Updated app!" does **not** reload imported modules. Both
have cost real outages.

Written 2026-09-22, after a publish in which the gate worked and two things
still nearly went wrong for want of it — a full `deploy-verify` was almost
re-run out of reflex at ~186k tokens, and the agent correctly reported "no
reboot needed" for the three commits it was handed while the actual push
changed `app/components.py`.

---

## The order, and what each step can see that the others cannot

Run these in order. Each catches a class nothing else does.

| # | Step | Catches |
|---|---|---|
| 1 | `python scripts/check_no_fetch_in_steps.py` | a step that reaches the network, **including through a shared module** |
| 2 | `python pipeline/drift_check.py --jobs 4` | committed outputs that no longer regenerate |
| 3 | `python scripts/check_personal_exposure.py <city>` | a person's name at their address |
| 4 | `python scripts/check_provenance.py` and `python scripts/check_inconsistency_list.py` | a city whose sources were never recorded; notices vs `_NOTICES`; a city with no row in `docs/map_inconsistencies.md`, the cross-city "why maps differ" list the owner will publish |
| 5 | `python scripts/brief_check.py <city>` | a brief's claims that stopped being true |
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

- The region switcher and macro map still land where they should.
- The new city's page renders its map, its labels and its licence notices.
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
- [ ] `check_deploy_imports` run **on the commit being pushed**
- [ ] `deploy-verify` scope chosen deliberately and stated
- [ ] Reboot question computed from **the whole push's `app/` diff**
- [ ] Pushed to master; owner told plainly whether a reboot is required
- [ ] Live URL verified, **including one city not touched**
- [ ] `DECISIONS.md` and `PLAN.md` updated; publisher obligations carried forward
