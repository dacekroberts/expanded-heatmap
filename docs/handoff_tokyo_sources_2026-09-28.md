# Handoff - Tokyo's missing wards: CLOSED 2026-09-28

The Tokyo sources research session (`worktree-tokyo-sources`) finished its
job the same day and passed back to the Japan build session ("Fukuoka
handoff"). The owner plans to pass everything from there to the Tokyo build
session. Delete this file once that session has read it.

## The result

**Every one of the 23 wards is settled: ON 8, OFF 15.** None of the 15
missing wards can join the map from its own publications. The build reads
the **Ward cards** section of `docs/build_briefs/tokyo.md`:
- one row per ward (food ON or OFF, the reason, the licence, and whether the
  ward has personal-services registers);
- a full card for each ward settled on 2026-09-28: Suginami, Katsushika,
  Bunkyō, Ōta, Kita and Arakawa.

The reasoning is in `DECISIONS.md`, 2026-09-28, "Tokyo's missing wards".

| Why OFF | Wards |
|---|---|
| released only on request (parked) | Chiyoda, Toshima, Nerima, Edogawa |
| PDF under site terms that bar reuse | Ōta (owner's call), Arakawa, Kita |
| nothing published at all | Bunkyō, Suginami, Katsushika |
| stale, partial or new permits only | Nakano, Shinagawa, Itabashi, Sumida, Adachi |

## Not done, and why

- **PDF extraction and the `pdf-register` skill**: no ward's licence permits
  reuse, so there was nothing to extract. Whoever writes the skill later must
  carry CLAUDE.md's [#memory] rule (no hand-written PDF or font decoder).
- **No new keys in `scripts/screen_japan_join.py`**: no new list to join.
- **No outreach drafted.** Each card's "route in" names the office. All
  routes are parked (owner: outreach is the last resort).

## Traps the build inherits

- **Dates that do not mean new data.** wagmap labels Nakano's file 2026/6/30,
  but its permits end 2023-06-27. Shinjuku's server re-stamped its 2023 CSV
  with Last-Modified 2026-08-31. Read a list's own permit dates.
- **Ward servers send a PDF or ZIP as a download.** Opened in the Browser
  pane, it lands at the checkout root, which happened twice here. Use HEAD
  and WebFetch.
- **WebFetch on a PDF or ZIP saves the binary** under the home directory, in
  the session's `tool-results` folder. `check_stray_downloads.py` does not see
  it.
