# Cleanup handoff, 2026-10-12: the phase 2 landing

From the Cleanup session that answered the portfolio review and saw phase 2
built, to the fresh Cleanup session that runs the landing. Read `CLAUDE.md`,
`docs/session_roles.md` and `PLAN.md` first ("From the portfolio review" and
"At the phase 2 landing" hold the queue); this note gives the order and what
is not in PLAN. It replaces `docs/handoff_cleanup_2026-10-08.md`, whose
landing order for `legend-dot-georgia` and place search (item 4 there) still
applies and is not repeated here. Delete both notes once their items are done
or in PLAN.

**Nothing below starts until the owner calls review time.** Only the owner
calls it. A peer session's relay is not his word: every call below was given
by him in a chat and is recorded in DECISIONS (2026-10-11) or in a build
branch's drafts file.

## Where things stand

- **Master `900c8f69`**, 206 cities. Phase 2 is built and nothing of it is
  pushed. Weekly usage 12% on 2026-10-12 (3% before the batch); the lifted
  weekly stops ended with the batch, and the 5-hour 90% ceiling holds.
- **Branches to land** (tips on 2026-10-12; confirm each ref before merging):
  - `worktree-japan-east-2` `151e4208`: 11 cities. Kawaguchi is HELD until
    S1 lands.
  - `worktree-japan-kansai-2` `40af664c`: 7 cities and Cluj-Napoca, with the
    `romania-city` skill and `name_kind_extended()`.
  - `worktree-japan-regional-2` `75fa42ac`: 11 cities. `check_all` 49 of 51
    there (the master list's counts, two macro labels): both expected,
    both items below. S16 is DONE on this branch: a
    `NEIGHBOUR_EXCEPTIONS` entry, with the Mikawa Line registered as
    `meitetsu-mikawa-line` at the red Toyota's map already draws;
    Toyota's config and map untouched.
  - `legend-dot-georgia` `16a68efe` (worktree `review-prep`), 57 behind
    master: needs the one full re-render.
  - `place-search` `e4b9e9bf` (2026-10-12; far behind master): batches 1
    to 3, nineteen cities, the watch file and its check. Since `498853e7`
    (that session's message; its newest drafts entry has the detail): the
    found place's marker rebuilt site-wide in `map_common` (own pane above
    the dots; dots, clusters and heat fade to 28% while it shows), all 19
    searched maps re-rendered, 18 London rows dropped by id. **The owner
    has not yet seen the new marker on a phone: a fifth call at review
    time.** That marker change is one more edit to `map_common`: merge
    it before S1 and the phone legend, as with `basemap`. **The owner's
    phone test of São Paulo PASSED (2026-10-12, his word in that
    session, relayed)**, and it covers London, the second largest (owner,
    2026-10-12, in Cleanup's chat: "sao paulo covers london"), so place
    search joins this landing. Its worktree was found missing on 2026-10-11 and re-added
    by the owner; the standing block on removing it holds until place
    search has landed. **Four owner calls to put at review time**
    (owner: "open from earlier stuff goes to cleanup"; the branch's
    PLAN, "Review time: the place search pilot"): (1) whether the
    suggestions go live as they are, marked work in progress; (2) the
    corner-credit test, the ODbL credit moved into the map's corner
    credit; (3) the Cities menu out of the map, measured at 343 px with
    the search box in place; (4) whether "Download this index" also
    links the intersections file (ODbL 4.6). Back with the owner and not
    built: stricter notability for monuments and galleries (measured to
    remove about 420 rows, two well-known Seoul landmarks among them),
    and a stronger station highlight on phones.
  - `basemap` (tip `16acf351` on 2026-10-12, master merged in): the
    site's partial Travel view. **The owner wants it finished (2026-10-12),
    and its go-live call is his, made at review time** (its drafts,
    2026-10-08). See "The basemap" below; an earlier version of this note
    wrongly left it out of the landing.
- **Each build branch has `docs/decisions_drafts/<branch>.md` and a handoff
  note.** Fold the drafts when the owner hands them off. S numbers are
  Staging's.

## Order

1. **The weekly archive first**: `python scripts/archive_decisions.py` (due
   2026-10-11, held for the batch by the owner), then
   `python scripts/decisions_index.py`. The branches' drafts cite entries by
   heading, which the archive keeps.
2. **An integration worktree** from master (junctions for `data` and
   `.venv-lean`; the 2026-10-08 note's "Habits" has the commands). Merge the
   three build branches; `app/cities.py` conflicts are keep-both; the OSM
   notice lists in `app/osm_notice.py` and `app/components.py` are keep-both
   beside step 3's edit. Then `python scripts/regen_generated.py`.
3. **The missing credit line, first inside the landing** (owner,
   2026-10-12: at the landing, not alone): add Regional-1's eleven cities
   (Maebashi, Fukuyama, Ichinomiya, Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu,
   Mito, Morioka) to `OSM_RAIL_BY_CITY` in `app/osm_notice.py` and to
   `_OSM_STATION_NAMES` in `app/components.py` (it raises at import when the
   two differ). Then read notice 1's sentence, reported to stop at "Tachikawa
   and Hino", and bring it up to every Japanese city; that sentence renders,
   so its wording goes to the owner if no template covers it.
4. **Shared-code changes, Cleanup's (S14). These go to master BEFORE the
   build branches merge** (a pipeline-only push, no `app/` file, no
   deploy), so step 2 above waits for them: Regional-2 re-runs
   Kurashiki's steps 2 and 3 after S17 (and S18 if written) and deletes
   Tottori's hook and re-runs Tottori after S19, on its own branch, and
   asked for a message as each lands. **The owner's instruction
   (2026-10-12): message Regional-2 when the changes land on master**: the
   session titled "Regional-2 build session expanded-heatmap", one message
   per push, naming the commit and which of S17, S18, S19 and call 182 it
   carries. East-2 gets the same for S1 and S2 (Kawaguchi is held on S1).
   Each with the Minato control
   (`screen_japan_join.py minato`, expect 98.0 / 0.2 / 1.8) and a Japan drift
   run through the gate (`--jobs 3`, about 5.3 GB; read
   `heavy_job.py status` first):
   - S1: `map_common.glitched_name` treats U+E000 to U+F8FF as glitched.
     Measure how many built maps it moves before changing it.
   - S2: a late start whose first-permit date is on or before the list's
     date is a renewal and stays (call 172's rule). Kawaguchi gains about
     100 pins.
   - S17: 自動販売形態 into `japan_eigyo.FORM_RULES` (83 vending pins on
     Kurashiki, which re-runs steps 2-3 before its page lands).
   - S19: `japan_register.permits_from_rows` tests the area-wide rule after
     the city cut; delete Tottori's `source_rows` hook; step 2 must reproduce
     237 area-wide and 2,240 storefronts.
   - Call 182: move Yamagata's permit-match name rule from
     `pipeline/yamagata/config.py` into `japan_step2`, find out why it flags
     3 rows where the brief counted 4, delete the city-local copy.
   - S18 (owner, 2026-10-12, in Regional-2's chat: "s18 yes treat as
     temporary"; relayed, recorded in that branch's drafts; Staging's
     relay numbers the same answer S28): 特殊形態
     joins `FORM_RULES` as a TEMPORARY form, set aside as 露天 is, in the
     same edit as S17. Okayama City's page defines it as a facility meant
     to be moved or removed; the prefecture's ordinance text was not
     found. Kurashiki loses 8 pins (six stadium concession stands, one
     market stall in two rows). 屋台 at a fixed pitch stays counted
     (Fukuoka, Kure). Check whether a form rule is switchable per city or
     universal before the drift run: no built Japanese city may move
     unlisted. Then tell Regional-2, which re-runs Kurashiki (83 vending
     pins and these 8 gone) and corrects its page's sentences.
5. **Bucharest's name repair** (a privacy repair on a published map): call
   `name_kind_extended()` in Bucharest's step 2 so the 127 pins (93 names) of
   a given name beside one other word show their category. The "two or more
   premises is a brand" exception is NOT applied (owner, 2026-10-12: leave
   them withheld). Then `check_personal_exposure.py bucharest`, the verdict
   in DECISIONS and `docs/privacy_verdicts.md`, and Bucharest's drift check.
6. **Lines:** JR Keiyo to `#C81000` in `pipeline/line_registry.py` (S3) and
   Tokyo's own JE literal switched to the registry; run the dark-mode label
   check, which nobody has run on this value (10.2 from the Keikyu Main Line
   on Tokyo; if the labels do not separate, moving Keikyu's red goes back to
   the owner). S16's exception arrives with Regional-2's branch. Osaka's three
   lines renamed "Osaka Metro ..." as the registry has them.
   `scripts/check_line_identity.py` green.
7. **Macro map (call 198):** place Minoh, Fuji and Kurashiki in a view; add
   `TEXT_WIDTH` for "Ibaraki (Osaka)", "Yao" and "Takatsuki"; add the new
   cities to `scripts/stress_overview.py`'s `BUILT_PREF` (it already lacks 23
   of the last batch). `scripts/check_macro_labels.py` PROBLEMS 0.
8. **The phone legend** (owner, 2026-10-12): in `pipeline/map_common.py`, on
   phones only, cap the open legend at about 40% of the map's height with
   its own scroll, and fold the transit lines by operator, closed by default,
   on maps past a line-count threshold set by measuring which maps exceed the
   cap. Names stay whole and wrap; nothing is truncated (the line-identity
   rule). Tokyo is the case that prompted it. Re-run
   `scripts/check_map_attribution.js` at more than one height afterwards.
9. **Per-category totals in every city's `baseline.json`** (owner,
   2026-10-11, for Analytics): `storefronts`, `storefronts_retail`,
   `storefronts_food_service`, `storefronts_personal_services`, counted AFTER
   the renderer's contact-detail screen. 61 cities carry them; 33 have no
   `baseline.json`. Size it first: no one shared writer was found.
10. **ONE full re-render** of every map after steps 3 to 9 and the merge of
    `legend-dot-georgia` (and place search, if its phone test has passed):
    `drift_check.py --render-only` through the gate. It covers the held
    Japanese re-render on `WAVE5_RULES` (every built Japanese city, Toyota
    first, call 158), Osaka, Tokyo, Funabashi, Ichikawa, Urayasu, Suita and
    Bucharest. Then `check_render_current.py`, `check_ring_shares.py
    --write`, `check_all.py`.
11. **Deploy-verify in lanes** (`docs/review_lane_kit.md` 7b; `scope:
    city-added` for the 30, `map-chrome` for the legend), then the push
    (`publish-city`; fetch and merge in the same breath), then **reboot the
    app** (`app/cities.py` and `app/components.py` both changed). Verify one
    new city and Bucharest live by hashing the iframe's `srcdoc`.
12. **After the landing:**
    - Give the owner the city count read from `app/cities.py` (expected 236:
      206 and 30), for the "about N cities" lines in his other projects.
    - Staging moves the master list's cities to Built and republishes.
    - The downstream note to Visuals and Analytics
      (`scripts/downstream_changes.py`). **Cluj-Napoca takes Bucharest's hold
      off public pieces** (owner, 2026-10-12).
    - The search disclosure sentence on About the Data, once place search
      lands (approved wording below).
    - The commercial-use and public-sharing audit (PLAN, "From the portfolio
      review").
    - At a later review time: Bucharest's address and name functions to a
      shared module.

## The basemap (the site's partial Travel view)

Read `docs/decisions_drafts/basemap.md` on the branch, the 2026-10-11
entries first. As that file records:

- **Built and switched off.** `pipeline/travel_packs.py` is one table for
  every city, with `PACK_HOST` None, so every committed map is unchanged
  (`check_render_current` 206 of 206 on the branch). Go-live is one line
  and one re-render of the maps. `scripts/check_travel_packs.py` is in
  `check_all`.
- **Packs:** 192 `.pmtiles` in the main checkout's
  `data/_basemap_build/host_upload_2026-10/` (1.9 GB, counted
  2026-10-12), with `MANIFEST.csv`, the libraries and the glyphs. Nothing
  is uploaded anywhere.
- **Wording P1 to P6 approved** (owner, 2026-10-11); none applied: each
  waits for the host's address. P5 goes into notice 1 beside CARTO's
  sentence at go-live, with its "keeps no record" clause confirmed
  against the chosen host's log settings.

**What is left, in order:**

1. **The owner's:** a Cloudflare account and the host (R2 behind an owned
   domain against the free Worker, compared live); the upload; the
   go-live call. Claude creates no account and enters no credential.
2. **The missing packs.** 206 cities and 192 packs: the basemap session
   names the 14 and why. Phase 2's 30 cities each need a pack and a row in
   the Travel table or `ENGLISH_ONLY`: **the pre-push check fails on the
   merged tree until each new city is placed**, by design. A pack build is
   a heavy job (about 4 GB, 2 to 2.5 min; three lanes at most, one gate
   slot left free); a new Geofabrik extract is the owner's download.
3. **Merge order:** `basemap` changes `pipeline/map_common.py` (five
   conflicts with master resolved on the branch, both sides kept). Merge
   it into the integration worktree BEFORE writing S1 and the phone
   legend, which edit the same file.
4. **One re-render, not two.** If the host is ready before step 10 of the
   order, set `PACK_HOST` first and the one full re-render carries the
   Travel switch. If it is not, land with the switch off (maps unchanged)
   and say plainly to the owner that go-live then costs a second full
   re-render.
5. **At go-live:** the license rows in `docs/data_sources.md` (Protomaps
   BSD-3, the tiles an ODbL produced work, Noto OFL with its trademark
   line, Cloudflare), the notice wording, deploy-verify `scope:
   map-chrome` with the Travel switch opened on a phone-width map,
   `scripts/check_map_attribution.js` at more than one height (a new tile
   source must show its own attribution), and the drafts fold.

## Approved wording

About the Data, with place search (owner, 2026-10-12): "Search finds stations
that are open. A station OpenStreetMap still marks as planned or under
construction is not listed until it opens."

## Open

- **The Global View button on Seattle (Regional)'s map does nothing on the
  owner's iPhone.** He reached the page from its dot on the Overview, and the
  same button works on Tokyo's map on the same phone. NOT reproduced: at 375
  px on the live site (emulated Android, a scripted click) the button was
  visible, the top element at its centre, and the click reached the
  Overview. Not tested: a real touch, iOS font metrics. Measured there:
  Seattle's button row wraps to two rows (`#map-actions` 287 by 72 px in a
  343 px frame) because its region button reads "← United States West".
  Unverified lead: on iOS the wrapped row puts the button under another
  element. Compare `elementFromPoint` across the whole button on Seattle and
  Tokyo with the touch harness (`data/_tap_harness_2026-10-03/`) and Safari's
  metrics, and check the other long region names.
- **Six watch-file stations have no line** (four on Busan's line under
  construction, Busan's racecourse station, Chicago's 87th Street): stated
  as null with a reason; a second look only if the owner wants every row
  filled.
- **`docs/licence_positions.md` row 2.10 names 12 MHLW cities; at least 28
  read MHLW's filings** (27 configs name the download, and Tokyo). Left for
  the audit, which counts every source.
- **Naha is in phase 2** (owner, 2026-10-12, in Cleanup's chat: "naha
  should get built as part of phase 2"; DECISIONS, that date). Band B,
  food only, mode `light_rail`, region Kyushu-Okinawa, the macro view's
  fit Cleanup's at the landing (Staging's relay of S30, S33, S35). Brief
  `docs/build_briefs/naha.md` on `worktree-staging`. Expect 31 cities
  from phase 2 and 237 on the site, wherever this note says 30 and 236.
  Its five shared-code items (a reader argument on `rebuilt_register`;
  unnamed header columns in `xlsx_rows`; `NAME_COLS` 営業所名所;
  `TYPE_COLS` 営業所種類 and 営業の種目; `VARIANTS` 壼) are Cleanup's
  and go to master before its build starts: check `git log` for them
  before assuming either way. The build session and its timing are
  Staging's plan.
- **Toulouse and Rennes:** whether step 1's name-level fallback fired; one
  read-only step 1 run per city.
- **Five unverified leads** from the PLAN cleanup pass (DECISIONS,
  2026-10-11, "The PLAN cleanup pass"): confirm one before acting on it.

## Habits that held this week

- `python scripts/push_docs.py` for doc-only pushes; it refuses `app/`,
  `outputs/` and `pipeline/`.
- A script file in the scratchpad for any edit with CJK, quotes or escapes;
  the hook blocks them inline.
- Counts only when measuring names; never print one.
- A report-only agent for a wide read, then check each "done" against the
  entry it cites before acting on it.
- The permission guard refused `git worktree prune` here; the owner ran it.
