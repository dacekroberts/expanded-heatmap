# Closing note, 2026-11-06

The Global Transit-Business Atlas is finished as a site. This note is the
starting point for anyone who opens the project again.

## State at close

- **Master:** `bdfe5524`, live and checked after the owner's reboot on
  2026-11-06. Chicago, New York, Dallas and Seoul serve their committed maps
  in full; the site notice names the font, tile and code hosts; the Overview
  opener plays the new-name cut and follows the viewer's theme.
- **Scope:** 237 city maps, no new cities (maintenance since 2026-10-16).
  The 2026-11-03 audit (`docs/audit_2026-11-03.md`) is fully worked.
- **Backup:** `visuals/` and `data/_analysis/` are copied to the T7 at
  `F:\Portfolio\Backup\expanded-heatmap-2026-11-06\` (1,329 and 772 files,
  0 failed). Neither folder is in git. `visuals/` holds the cards, the
  generators and the six Motion films.

## Still open

- **Dated re-checks** in `docs/recheck_calendar.md` (parked while the owner
  was away). These are data checks, not site work.
- **Leftover file:** the copy of the first opener at the file host's bucket
  root (DECISIONS, 2026-10-14) is the owner's to delete.
- **Stale comment:** `scripts/check_personal_exposure.py` near line 448
  still describes New York's DCA names as before the 2026-11-04 rule.

## If the site moves to its own domain

Not decided (owner, 2026-11-06). What a move would touch:

- **The app address** `expanded-heatmap-daceroberts.streamlit.app`, named in
  `README.md`, `scripts/check_macro_attribution.mjs`,
  `scripts/review_lanes.py`, `.claude/agents/deploy-verify.md` and
  `docs/review_lane_kit.md`. Dated docs and handoffs keep the old address.
- **Printed on visuals:** the "Full credits" line on every card and in the
  Motion film reads the streamlit.app address. A move means regenerating the
  cards (`visuals-rebuild` skill) and a new Motion export.
- **The file host** (`files.dacekroberts.dev`, `PACK_HOST` in
  `pipeline/travel_packs.py`) is already on the owner's domain and need not
  move.
- **Paths:** Streamlit Cloud serves pages under `/~/+/`, which the poster's
  relative path depends on (`app/Overview.py`). Re-check it on any new host.
- **The privacy notice** (`app/components.py`, Notice 1) names the hosts a
  page contacts; a new host or proxy changes that sentence.
- **Opener films:** a replaced film takes a new `?v=` tag, because
  Cloudflare's edge kept the old file under the same URL (2026-11-06).
