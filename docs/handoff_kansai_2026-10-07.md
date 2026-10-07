# Handoff: Kansai-1 to Kansai-2 (2026-10-07)

Kansai-1 built its seven cities on branch `worktree-japan-kansai-1`
(worktree `.claude/worktrees/japan-kansai-1`), committed, nothing pushed; it
lands at the phase 1 review time. Kansai-2 builds Ibaraki (Osaka), Minoh,
Moriguchi, Kadoma, Neyagawa, Yao and Takatsuki, then Naha's one measurement if
BODIK answers (`docs/build_plan_2026-10-07.md`). Pages 251-257, notices
198-204.

## What Kansai-1 left you

- **Seven built configs on the same shapes as yours**
  (`pipeline/<slug>/config.py` on the branch): a full list rebuilt by permit
  number with closures (Toyonaka), a list kept whole plus monthly new permits
  (Hirakata), two food files by law read as one kind (Suita), a prefecture's
  lists cut by address (Itami, Kakogawa), a city's permit and notification
  lists (Amagasaki), MHLW's prefecture file cut by address (Uji).
- **Line colours your neighbours already use**, so shared lines agree across
  maps: the Osaka Monorail `#007890` (Toyonaka, Itami; Suita moved it one step
  to `#108098` beside the JR Kyoto Line), Kita-Osaka Kyuko `#E81820`, Hankyu
  Takarazuka `#C06038`, Hankyu Senri `#B88080`, Hankyu Kyoto `#885848`, JR
  Kyoto `#506878`, Osaka Higashi `#A088A0`, Keihan Main `#787858`, JR
  Gakkentoshi `#C000A8`. Start `line_colour_search.py` from these.
- **Licences read today** (in `docs/data_sources/japan.md` on the branch and
  sent to Staging): Toyonaka's BODIK datasets, Hirakata, Suita, Amagasaki,
  and Hyōgo Prefecture's 生活衛生課 catalogue. Osaka Prefecture's own lists
  were not read.

## Traps this batch measured

1. **Run `check_personal_exposure.py <city>` right after step 3, not at the
   end.** The name rule spreads only within one block; a trade name flagged
   on a citywide stall (市内一円, no block) still shows at another premises
   (Suita, parked call 1 in `docs/decisions_drafts/worktree-japan-kansai-1.md`).
   The check's Japan pass needed `rules = japan.city_rules(slug)` (fixed on
   all three phase 1 branches; it lands with them).
2. **An address cut by name** needs two exceptions measured, not assumed: an
   area licensed across several towns names your city mid-address (Kakogawa's
   「たつの市、高砂市、加古川市内一円」), and another town can hold your city's name
   as a village (伊根町字本庄宇治). Guard on the full municipality name
   (`宇治市`), and pass over rows that end 一円.
3. **Ring size is step 1's median**, among the in-city stations as step 1
   prints it, not the brief's count by N02 group: Uji measured 505 m (the
   brief 588 m) and takes the halved rings.
4. **One Japanese name, two stations read differently** (木幡: JR Kohata,
   Keihan Kowata): step 1 stops until `OSM_NAME_EN_TIES` settles one
   spelling; the operator suffix then tells them apart (Kyoto's 西院).
5. **OSM translates some names** (大阪空港 as "Osaka Airport"): romanize, as
   Fukuoka's 福岡空港.
6. **`check_provenance.py` reads every endpoint verbatim**: write each URL in
   full in the source row, never `…/file.csv`.
7. **`check_all.py` needs, per city**: four rows in
   `docs/map_inconsistencies.md` (tables A-D, after Shimonoseki's), then
   `check_macro_facts.py --write`, `check_ring_shares.py --write`,
   `rendered_surfaces.py --write`, `readme_cities.py`; `app/osm_notice.py`
   and notice 1's city tuple in `app/components.py`; `scripts/stress_overview.py`'s
   `BUILT_PREF`. Three failures are not yours: the fingerprint marks (the
   owner's key), macro labels (Cleanup's, call 198), the master list's count
   (Staging's).

## How the batch was run

- **The lead made every network call**: the brief checks through a wrapper
  that spaces each `data.bodik.jp` request 21 s (brief_check.py does not),
  and every Overpass query, one at a time. Overpass refused (504/429 on every
  mirror) about half the time today; a serial prefetch with 120 s between
  retries finished the six cities in about 30 minutes.
- **Three subagents built pipelines in parallel** (pipeline only, one
  `pipeline/<city>/` each, no shared file, no Overpass, no BODIK), from one
  common rules file; they matched their briefs exactly and returned page,
  doc and row drafts. The lead wrote every shared file.
- **Usage**: the batch took weekly usage from 51% to about 58%.

## Open owner calls that touch your cities

- Toyonaka's register months (call 151) are still open with the owner.
- Parked call 1 (the name rule across premises) is a shared change to
  `japan_step2`; if the owner approves it, it may land before your cities and
  change your step 2's withheld count.
