# Review time

How approvals and deploys are batched (owner, 2026-09-27). This is change 2 of
`docs/efficiency_review_2026-09-27.md`, with renderer batching (finding 4)
added the same day. **Review time happens only when the owner calls it**, never
on a schedule; sessions remind the owner once work has built up.

## What waits for review time

1. **The owner's approvals.** Wording that gets published, map labels,
   renderer or look-and-feel choices, and any judgment call a session would
   otherwise stop and ask about. Sessions queue these and carry on with other
   work.
2. **Landing `app/` changes on master.** This is the deploy, since Streamlit
   Cloud pulls master automatically.
3. **Full re-renders of all 46 maps** after a change to the shared map code
   (`pipeline/map_common.py`, `pipeline/theme.py`, `pipeline/linecolour.py`,
   the shared blocks). Sessions try changes on 3-5 sample maps in the
   meantime. `check_render_current.py` fails until the full render, so the
   pre-push hook keeps the branch off master; comment-only edits do not count.
4. **The pre-deploy checks that come with a deploy:** `check_deploy_imports`,
   `deploy-verify`, the reboot, and the live-site check. These run once for the
   whole batch rather than once per change. **`deploy-verify` belongs to review
   time** (owner, 2026-09-27): during the day, a session checks its own `app/`
   change with at most one quick browser render, never `deploy-verify`.

## What does not wait

- **Building cities on branches**: pipeline steps, drift checks, commits,
  research, licence reads, briefs.
- **Pushing changes that don't touch `app/`** to master, such as docs and
  scripts. These don't deploy anything.
- **A broken live site, or a removal request.** These go out immediately, as
  their own deploy. A removal request is honoured first under the CLAUDE.md
  invariant.

## What happens at review time

1. Each session presents its queue, each item with a recommendation. The owner
   decides.
2. The approved `app/` work is merged, and all maps are re-rendered once if the
   shared map code changed.
3. `check_deploy_imports`, then **one** `deploy-verify` run for the batch. Its
   scope matches what changed; `full` is kept for large batches.
4. One push, **one reboot**, one live check. The `publish-city` skill has the
   gate in order.

## Reminders

A session reminds the owner once, at the end of a reply, when any of these is
true:

- 5 or more items are queued
- 3 or more `app/` commits are waiting to land
- an item has waited more than 24 hours
- a session is blocked on queued items

It reminds once per threshold crossed, not on every turn.

## What this changes in how we work

- **The owner is interrupted less often** but sees a bigger batch each time.
- **`deploy-verify` runs about once per batch instead of once per change.**
  This is where most of the savings come from, since a full run is about 186k
  tokens.
- **The live site changes in steps rather than continuously.** An approved fix
  isn't live until the batch lands, unless it's fixing a break.
- **The risk is batching more changes into one deploy.** If something breaks,
  there's more to search through. The single `deploy-verify` before the push is
  what guards against that.
