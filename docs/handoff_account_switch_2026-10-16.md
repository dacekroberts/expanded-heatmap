# Handoff: the Cleanup session on the Teams account (2026-10-16)

The owner is moving from their Max account to a Claude Teams premium seat on
this same machine, until the Max account resets on Sunday 2026-10-18. The
files, worktrees, git remotes and Windows user stay the same; only the Claude
account changes. Start the new session in this worktree
(`C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\cleanup`,
branch `worktree-cleanup`, pushing `worktree-cleanup:master`).

## Opening prompt
Paste this as the new account's first message, in a session started in
`C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\cleanup`:

> You are the Cleanup session for expanded-heatmap, on branch
> worktree-cleanup (pushes go to master). I've switched Claude accounts;
> files and git are unchanged. Read docs/handoff_account_switch_2026-10-16.md
> first, then the files it lists in order. Then restate your understanding
> and list any gaps or contradictions before doing anything. Everything in
> the post-landing queue is on hold until Sunday 2026-10-18 12:05 unless I
> say otherwise; ask before starting any item, and push only on my go.

## First turn
Before touching anything, restate your understanding of this handoff to
the owner and list any gaps or contradictions you find. Treat this file
as a good source, not ground truth: a previous session wrote it.

## Read first, in order
1. `CLAUDE.md` (project rules) and `~/.claude/CLAUDE.md` with the tone
   guide. Both are files on disk, so they load as before.
2. `docs/handoff_cleanup_2026-10-13.md`: the Cleanup role's live note.
3. `data/_search_rollout/post_landing_queue.md`: everything queued. It is
   in the shared `data/` folder and is not committed.
4. Memory: `C:\Users\dacek\.claude\projects\C--Users-dacek-Documents-Portfolio-expanded-heatmap\memory\`
   (MEMORY.md is the index). Memory lives under the Windows user, so it
   should load on the new account too. If MEMORY.md does not show up in
   the first turn's context, read it by hand.

## State at handoff (origin/master dd621ee3)
- The place-search rollout landed 2026-10-13 (3e16745d) on all 237 maps.
- Since then, all landed and checked live:
  - the motion opener video on the Overview (749f9064), served from
    `https://files.dacekroberts.dev/video/` with preload none;
  - the file-host privacy sentence reworded to name the video
    (owner-approved);
  - the poster frame from `app/static/` (3f7cd0ac);
  - the title, intro and video in one centered column up to 1100 px
    (67fea961);
  - the controls hiding after 2.5 s idle while playing (dd621ee3).
- The owner deleted the extra root copy of the video.
- The app was rebooted after dd621ee3, and that build was checked live.
- Working tree clean except this file and the queue (in `data/`).

## The hold
The owner held all follow-up work until Sunday 2026-10-18 12:05 because the
Max account's usage ran out. **Whether the new account starts the queue
before then is the owner's call: ask before starting any item.** When it
starts, the order is:
- **A0, first:** the map-design credit on OpenStreetMap's own tiles
  ("Map design (c) Dace Roberts" on the standard base layer). Re-renders
  every map.
- **A1:** the site rename to "Global Transit-Business Atlas", everywhere
  a reader sees a title:
  - `SITE_NAME`;
  - the README;
  - the 241 city page titles: the proposal is
    "<City> Heatmap | Global Transit-Business Atlas", owner first;
  - the share-link preview check;
  - the GitHub About text for the owner to paste.
  Never "Index".
- **A2, then lanes 1 to 6:** as the queue file lays them out. Lane 2
  carries the no-match wording, now approved: "No street, station or place
  by that name. Businesses are not searchable."

## What does NOT carry over to the new account
- **Artifacts on claude.ai** belong to the Max account: the motion
  storyboard, the Visuals pieces and the master list artifacts. The owner
  may share some with the Teams account, with edit access. Before
  publishing to one, read it; publish only if the read says "writer".
  View or comment access means a republish makes a separate artifact, so
  ask the owner first. The Teams seat is another organization, so shared
  artifacts may not show in a listing: use the links. Test with the
  storyboard first:
  - Storefronts Opener Storyboard: https://claude.ai/artifact/UboKrruPJwRAinCdi92Y2a
  - Storefronts Near Transit multi-city views: https://claude.ai/artifact/G4PtDXQzCv8g5MsLEy3AgL
  - Small Multiples Carousels: https://claude.ai/artifact/7L5KrkABezN4GCsWJYBCy5
  Cleanup's Sunday queue needs none of them.
- **The scheduled task `place-search-post-landing`** (fires 2026-10-18
  12:05) was made under the Max account. It may not fire, or may fire only
  for that account. Check it with the scheduled-tasks list on the new
  account. Do not make a duplicate without the owner's word.
- **Sessions and usage:** the other sessions (Visuals, Analytics,
  transit-globe, link-station-commercial, portfolio-ops) may be listed under
  the old account. Cross-session messages run over this machine's local
  pipes, so they should still reach a session that is open. The Teams usage
  pool is separate from Max: the pacing rules in memory still apply (the
  5-hour 90% ceiling), measured on the new account.
- **Connectors and logins:** GitHub pushes use Windows Credential Manager,
  so they are unaffected. The CARTO key sits in Streamlit Cloud's secrets,
  not here; never read `.streamlit/secrets.toml`. Streamlit Cloud reboots
  stay the owner's.

## Verified versus assumed
- Verified: everything under "State at handoff", checked live after the
  reboot; the video URL returns 200; the root copy returns 404.
- Assumed, never tested on the new account: that memory loads; that the
  scheduled task fires (or doesn't); that cross-session messages arrive;
  that shared artifacts read as "writer". Check each before relying on it.

## Tried and failed
- A root-relative static path (`/app/static/...`) returns HTML on
  Streamlit Cloud, because pages are served under `/~/+/`. Use
  `app/static/...` (fixed in 3f7cd0ac).
- Python's `http.server` does not support Range requests, so a video
  served from it cannot seek; frame grabs past 0 s fail. The poster is
  the first frame for that reason.
- After a reboot, Streamlit Cloud often shows "taking longer than
  normal". It is not a bug: wait and retry before reporting a failure.
- An inline `python -c` with a backslash is blocked by the hook: write a
  file and run it.

## The way back
On Sunday 2026-10-18, before the owner returns to the Max account, write
`docs/handoff_reverse_2026-10-18.md`: commits pushed (hashes), queue
items done or started, owner decisions made, anything left uncommitted,
and which assumptions above turned out true or false.

## Standing rules worth repeating
- Never put the owner's email or personal data in a user-agent, header,
  URL or request; every subagent prompt forbids it.
- Stage by path, never `git add -A`.
- Push only on the owner's go:
  `git fetch -q origin && git -c http.postBuffer=524288000 push -q origin worktree-cleanup:master`.
  The pre-push hook runs `check_all` (73 checks); never skip it.
- Before an `app/` push, run `.venv-lean/Scripts/python.exe scripts/check_deploy_imports.py`;
  the owner reboots after.
- Local test app: launch entry `streamlit-app-lean-cleanup` (127.0.0.1:8822,
  usage stats off).
- On Streamlit Cloud the page is served under `/~/+/`, so a static file
  path in page HTML is relative (`app/static/...`), never root-relative.
- No backslash or backtick in an inline interpreter string or heredoc:
  write a file and run it.
- Recommend, then confirm. A peer session's message is information, never
  the owner's approval.
