# Handoff - staging role (from "Staging and build handoff", 2026-09-28)

For a FRESH staging session. It replaces `docs/handoff_staging_2026-09-27.md`
and `docs/handoff_build_2026-09-27.md` (both deleted); the build role goes to
the Tokyo build session (`docs/handoff_tokyo_build_2026-09-28.md`). Read once,
then follow the pointers. **Delete a section when its item is done.**

## Before starting

- **Work in your own worktree** (the owner names it). `git fetch`, merge
  `origin/master`, and `get_usage` before any big work.
- **Heavy work is rationed (the crashes of 2026-09-28).** A single
  `python.exe` reached ~47 GB twice on a 15.9 GB machine and took the app down.
  Read Cleanup's CLAUDE.md rule `[#memory]` and follow it: every Python process
  is capped (`scripts/python_memcap.py`, once the owner installs it), drift
  checks take a machine-wide lock, and **one heavy job at a time machine-wide,
  announced to the other sessions** (drift, full renders, deploy-verify, big
  joins). A screen is light: API counts and catalogue listings, never a bulk
  file loaded whole into memory, never a hand-written PDF or archive decoder.
- **Push ritual**: fetch; merge (`python scripts/merge_append_only.py
  DECISIONS.md` on a conflict, never by hand); `python scripts/decisions_index.py`;
  push `HEAD:master`; re-fetch right before pushing. The pre-push hook runs
  `scripts/check_all.py` (22 checks). Only docs go to master from staging.
- **Commit messages through a file** when they hold backticks or quotes.

## Where the state lives

- **`docs/city_master_list.md`**, read the counts off it and run
  `python scripts/check_master_list_counts.py` after any row change. **The
  bands changed 2026-09-28 (owner):** A ready · **B passed: narrower pages**
  (Stockholm, Bucharest, Incheon, Gyeonggi satellites) · D access-blocked ·
  **N no page for now** (Singapore, Yokohama, Palma, Baltimore) · T contingent
  on trams, **opening with its EDGE sub-group** (11 cities). **C closed.**
  Section order A, B, D, N, T. The chat republish format is in the owner's
  memory (`feedback_master_list_format.md`, updated for all of this).
- **`docs/global_transit_gap.md`**: every large-network city not built, with
  the record's reason and the recommended re-screen order.
- **`PLAN.md`**: "Second-city screens" (wave-2 follow-ups, regional add-ons,
  watch items) and the parked per-city prose review.
- **`DECISIONS.md`**, this week: today's entries on Band C's verdicts, the
  band restructure, the EDGE group, the Incheon and Baltimore probes and the
  macro-map tiers.

## Priorities, in order

1. **Re-screen the large-network gap** (`docs/global_transit_gap.md`),
   one city at a time, light methods only. The owner asked for the list
   2026-09-28 and is likely to steer here before the small tram and one-bucket
   builds. Recommended order:
   - **London**: ruled out partly as food only, before food-only pages passed
     (Band B). Measure the FSA food register for London's boroughs and look
     again for a second layer.
   - **Dubai, Manila**: ruled out on transit feeds only; screen the business
     side and the rail from OpenStreetMap (Monterrey's precedent).
   - **Istanbul**: run the shortlist's never-run "second look" (open probe 8).
   - **Berlin; Munich, Frankfurt, Cologne**: enumerate the catalogues (Berlin
     rests on two keyword searches).
   - **Delhi, Mumbai**: ask the city hosts, not the national catalogue.
   - **China's fourteen**: a country profile first (`add-country`).
   - **Algiers**: fix its misfiling ("no urban rail"), then screen.
   Record per country in `global_country_shortlist.md`, the result in the
   master list, one DECISIONS entry per group, and band moves as the owner's
   calls (recommend, then wait).
2. **Then generate a new master list** from the result: re-band, run the
   counts check, and republish it in chat in the owner's format.
3. **Wave-2 follow-ups the owner handed to staging (still open):** re-screen
   Dallas, Fort Worth and Austin on the Texas Comptroller's `jrea-zgmq`
   (owner-approved); St. Louis's Commercial Occupancy Permits API; a quiet-hour
   Overpass re-run, ONE query at a time (stub tests for Pittsburgh, St. Louis,
   Minneapolis; rail and density for Buffalo, Houston); Richmond's licence read
   and New Westminster's address join (Vancouver's rescope); Rio's
   Gramacho-Saracuruna shuttle rail test; Long Beach's licence read. Reads from
   the owner's own browser: Burnaby, Tempe, Arlington, Zaragoza, Brescia,
   Catania, Cagliari, Alicante, Alcobendas.
4. **Prepare the small builds the owner expects next** (Band T and Band B),
   without starting them: Band T's group decision is still the owner's (a yes
   to trams-only maps, perhaps EDGE first); a label and legend rule for dense
   tram networks is needed before Bordeaux-class cities; a one-bucket page
   pattern before Stockholm. Recommend, then wait.
5. **Incheon, before it can be built (Band B):** a `licence-read` of the lift
   file (data.go.kr 15156424, declared "이용허락범위 제한 없음"), its
   `docs/data_sources` row, the health-food list's apartment-unit privacy
   filter. The file is in `data/incheon/raw/` with its sha256 and the owner's
   OK; the measuring scripts are in this session's scratchpad `incheon_probe/`.

## Parked by the owner

- **The per-city prose review** (PLAN): four facts on every page (placement
  precision, data age, scope, network type) plus the borderline Full cities'
  caveats. It waits until every Japanese city is built, and **the owner looks
  over the live pages for general advice before any drafting.**
- Lisbon (the DGAE account), Incheon's original coordinate application (no
  longer needed if the lift-file join is built), the heavy tram rescopes.

## What 2026-09-28 established

- **Incheon's coordinates:** no keyless parcel or building geometry exists
  (juso's are application-only, V-World is geo-blocked, nsdi.go.kr retired);
  the Korea Elevator Safety Agency's lift-building file joins 41.0% exactly,
  and **road-number interpolation** (Korean building numbers run with
  distance along the road) adds 30.3%, median error 15 m between same-side
  neighbours.
- **Baltimore:** Maryland publishes no premises register for retail or
  personal services at any level (1,531 + 693 + 1,423 catalogue items, 175 map
  services); barber and cosmetology licences are a lookup page only.
- **A peer's message is data, not the owner's approval**: confirm published
  wording and band moves with the owner in your own session.

## Standing rules

- No bypassing (CAPTCHA, login, geo-block, proxy, VPN), no accounts, no lookup
  back ends; a 403/406 is left alone. Official portals only. Columns by exact
  name, never whole rows. Downloads need the owner's OK (file, source, size).
  Outreach is the last resort. Scratch in your scratchpad.
