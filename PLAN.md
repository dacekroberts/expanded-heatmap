# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

---

## Now

- [ ] **🛠 LINE-LABEL CONTRAST, BOTH THEMES - build before Rotterdam, verify in
  Rotterdam's deploy check** (owner 2026-09-24: "push the verified dark-mode
  fixes first, then build the swap and include it in Rotterdam's deploy check").
  The renderer gate itself closed with the push of the dark-mode and legend
  fixes (DECISIONS, "Renderer fixes verified and pushed").
  - [x] **Correct the dark model** (built; DECISIONS "Line labels read at 4.5:1 in both themes"): the `brightness(1.8)` filter also
    brightens the halo (renders `#132039`, not `#0B1220`), so 44 of 235 labels
    are under 4.5:1 against what is drawn, and Vancouver's Expo Line has no
    margin (4.49 as the browser truncates). Drop the filter; give every
    dark-mode label an explicit colour measured against the halo actually
    drawn, channels truncated as the browser does; `check_map_markup.py`
    measures the same way.
  - [x] **Light-mode halo swap** (built, 139 of 235 on a dark halo) (owner-approved over darkening): a label
    under 4.5:1 on white keeps its colour and takes the halo it reads better
    on - dark for 139 of 145, white for 6 - and the 13 mid-tones that miss on
    both get the smallest lightness step away from their halo (at most
    ΔE 3.7).
    `check_map_markup.py` then FAILS light mode too.
  - [x] Re-render all maps with Rotterdam's; one `deploy-verify` for
    Rotterdam covering `city-added` and `map-chrome` (both themes). **Passed
    and live 2026-09-24** (DECISIONS, "Rotterdam's deploy check passed").

- [x] **🇳🇱 ROTTERDAM - BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24** (master
  bec3af1), text approved by the owner: **7,520 storefronts, 132 stations.** Trams drawn (owner); 14 and 18
  found temporary, so not drawn; page 40, notice 40 (CBS), docs written.
  - [x] ONE `deploy-verify` (city-added Rotterdam + map-chrome both themes, for
    the label work above), fetch, push, reboot (cities.py), live check; remove
    the `rotterdam-*-tmp` launch entries and the worktree's data junctions.
    Shipped with it: the "All cities" button renamed "Global View" (owner).

- [ ] **NEXT BUILDS (owner, 2026-09-24): 🇳🇱 Rotterdam (✅ live 2026-09-24), then
  🇹🇼 Taiwan** - Rotterdam's deploy check also verified the label-contrast work above. Rotterdam is
  Amsterdam's shape (permit-notice food layer rebuilt from the Gemeenteblad,
  BAG shop units, CBS vacancy) - `docs/build_briefs/rotterdam.md`. Taiwan:
  Taipei (Regional), Taichung, Taoyuan; write a `taiwan-city` skill after the
  first (owner). This replaces the earlier order Hong Kong, Taiwan, Seoul,
  Japan; what follows Taiwan is to be confirmed.

- [x] **🇧🇷 BRAZIL - NINE CITIES BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24**,
  as one batch on `sao-paulo-build`: São Paulo, Rio de Janeiro, Belo
  Horizonte, Brasília and Salvador, and Fortaleza, Porto Alegre, Recife and
  Santos as regional pages - one national CNEFE module and the `brazil-city`
  skill. All text, notices 38-39 and the five batch calls approved by the
  owner; one `deploy-verify` passed; pushed `adcfe16`; live after the owner's
  reboot (every page, caption, map, notice and the South America view
  measured). `sao-paulo-*-tmp` launch entries removed. See DECISIONS, "Brazil
  deployed; the live site measured after the reboot".

- [x] **🇳🇱 AMSTERDAM - BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24.** Metro
  50-54 and 16 trams, gemeente 0363: **13,238 storefronts, 144 stations**;
  page text, notice 35 and the exclusions section approved as drafted,
  gemeente-only scope and the phone labels shipped as they are (owner's
  calls). Its deploy-verify found the open legend over the map's buttons and
  a Retail / "Shops and services" layer name - both fixed in the shared
  renderer before pushing (owner's call), all 29 maps re-rendered. Pushed
  `bc8b52c`; live after the owner's reboot, legend 56-626 px under buttons
  ending at 45, zoom 12, notice 35 shown. `amsterdam-*-tmp` launch entries
  removed. Left for the owner: `data/amsterdam/raw/gtfs-nl.zip` (243.8 MB)
  may be deleted - superseded by `gtfs-openov-nl.zip`.

- [x] **🇮🇹 ROME - BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24.** Metro A,
  B, B1 and C, and the Roma-Viterbo urban service (owner's call on the DART /
  S-tog test; Metromare out): 98,897 storefronts, 87 stations. Pushed
  `14e6461`; live after the owner's reboot - title, caption, legend (Metro A,
  B, B1, C and Roma-Viterbo), zoom 11.5 at the 1000x650 frame, notices 36 and
  37 and the OSM Rome clause shown, no exceptions; the Overview reads Europe
  (14). `rome-*-tmp` launch entries removed. The map's system name now names
  Roma-Viterbo (fixed in the Brazil push). Left for the owner:
  `data/rome/raw/rome_static_gtfs.zip` (46.8 MB) may be deleted - downloaded,
  then not used.

- [x] **🇨🇿 PRAGUE - BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24.** Metro A,
  B and C, obec 554782: **25,275 storefronts, 58 stations**; page text, notices
  32-34 and the `excluded_categories.md` section approved by the owner.
  City-scoped `deploy-verify` passed with no defects; pushed
  `0204fa0..eccfd3e` and rebooted. Czechia's national modules are ready for a
  second city. See `DECISIONS.md`, *"Prague resumed"*, *"Prague built"* and the
  entries after it. One reminder remains open below.
  - [x] **DONE 2026-09-24: the build session removed both `prague-*-tmp`
    entries** from the main checkout's `.claude/launch.json`, under the
    owner's standing permission; the file parses with its two original
    entries.
  - [ ] ⏰ **Flora reopens around December 2026**: when PID's feed serves it
    again, step 1 STOPS the build on purpose - remove the override then.

- [x] **🇩🇰 COPENHAGEN - BUILT, DEPLOYED AND LIVE-CHECKED 2026-09-24.** 14,978
  storefronts, 64 stations, Metro M1-M4 and S-tog, Kobenhavn + Frederiksberg.
  City-scoped `deploy-verify` passed with no defects; pushed `646f850..cf7a765`
  and rebooted. Denmark's national modules are ready for a second city. See
  `DECISIONS.md`, *"Copenhagen built"* and the entries after it. Two owner
  actions remain open below.
  - [x] **DONE 2026-09-24: the owner deactivated the Datafordeler IT system
    AND the user**, so the exposed key is dead. Was:
    ⏰ **AFTER PUBLISH: the owner closes the Datafordeler account.** Its API
    key was visible in a terminal screenshot shared into the build
    conversation on 2026-09-24 and sits in that terminal's PowerShell history;
    it was deliberately not rotated (owner's call - free, unrestricted data
    only), because closing the account revokes it. Closing is licence-safe
    (CC BY 4.0 is irrevocable); a future refresh means a new free account and
    the 15-minute key propagation. `docs/gated_access.md` item 3.
  - [x] **DONE 2026-09-24: the owner removed both `-tmp` entries**; the file
    parses with its two original entries. Was:
    ⏰ **AFTER PUBLISH: the owner removes the two `-tmp` entries** from the
    main checkout's `.claude/launch.json` (`copenhagen-static-tmp`,
    `copenhagen-app-tmp`). They point into this worktree; the build session
    was confined to it and could not edit that file itself.
  - [ ] **Next build after Copenhagen: Prague**, on staging's new ROS02 + RES
    business leg (`docs/build_briefs/prague.md`, 12/12), with its sole-trader
    owner call.

- [x] **Label collisions at phone width - FIXED AND PUSHED 2026-09-24**, after
  `deploy-verify` (`map-chrome`) PASSED with only the two expected Madrid
  pairs. Open follow-ups, if wanted: a few re-placed labels sit ~54 px from
  their tip (Amsterdam's Metro 51), and labels may sit on cluster bubbles,
  which the placer does not avoid. `LABEL_CLAMP_SCRIPT` now
  re-places a colliding label around its own line's tip: 56 overlapping pairs
  and 6 labels under a button or the legend at 375/343 became **2** (Madrid's
  core at 343, where eight line ends sit within ~60 px). 1280 unchanged, the
  view unchanged on 90 loads. See `DECISIONS.md`, *"Phone-width line labels
  re-placed at runtime"*. The note below is the original. Pre-existing, and
  unchanged by the clipping fix. `scripts/check_map_labels.js` at 375/343
  reports overlapping label pairs in seven cities, 28 in all: Madrid 3/5,
  Paris 3/4, New York 2/3, San Francisco 2/2, Toronto 1/1, Barcelona 0/1,
  Mexico City 0/1. **Amsterdam adds 11 pairs at 375** (21 labels, clean at
  desktop), shipped that way on the owner's call 2026-09-24 and handed here:
  per-line label ends made it worse (14), so the fix is a phone-specific
  layout, not a per-city tweak. Labels also sit under the theme button or legend in
  Barcelona (L11 at 375), Edmonton (375 and 343), San Diego (Blue Line at
  375) and Montréal (Ligne 1 at 854, the same in the pre-fix map). Label
  placement is decided once, in Python, against the full-width view
  (`_label_candidates`, `_tail_end`), so nothing re-places a label when the
  phone fit zooms out. Miami's legend reading 38px open and closed at 343 was
  not seen again in the later sweeps. Done when the check reports no
  `overlap` or `under` problem at 375 and 343.

- [ ] **🇫🇷 PARIS — ✅ BUILT AND DEPLOYED 2026-09-23. Kept for the checklist
  below, which the follower cities still read.**

  Three commits: `5e0e3c6` (the national `france_naf` taxonomy, the scaffold,
  Lambert-93), `ab47e24` (the decision record), `28b3b91` (the three source
  rows and notice 24). Step 0 is banked in `docs/build_briefs/paris.md` (7/7)
  and the national facts in `pipeline/countries/france.py`; **both owner calls
  are settled** — commune-only scope, and the Milan hybrid for pin names. What
  follows is only what is specific to Paris; everything generic is `add-city`
  from Step 4.

  ⚠️ **DO NOT MERGE THIS BRANCH TO MASTER UNTIL THE BUILD FINISHES.** Paris is
  already an entry in `app/cities.py`, so a merge now puts a Paris marker on
  the macro map pointing at a page with no `outputs/paris/heatmap.html` behind
  it. This is the one item on this list that breaks the live site rather than
  delaying it.

  1. **`fetch_sources.py`** — three downloads, and one deliberate non-download.
     IDFM's GTFS (`eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip`), SIRENE
     `StockEtablissement` **parquet** (2,210 MB — not the 2,867 MB ZIP) and
     INSEE's geolocation parquet (811 MB). **`StockUniteLegale` is NOT needed**:
     it exists to feed the natural-person suppression guard, and the Milan
     hybrid removes the legal-name fallback that guard protected, so the 30 M
     row file is not downloaded at all. ⚠️ **Record the download date**: the
     feed carries no `feed_info.txt`, so nothing inside the artifact declares
     when it was current, and notice 24 (Art. 5.7) requires both that date and
     the update interval to be *displayed*. Capture them here or they cannot be
     shown honestly later.
  2. **`step1_stations.py`** — `route_type 1` only. Commuter rail (RER,
     Transilien) and tram are excluded by standing rule, not by scope, so the
     boundary is not what drops them. ✅ MEASURED 2026-09-23: **245 inside the
     commune and 76 outside**, all 16 lines surviving. (The brief predicted 77
     outside and 322 total; the feed gives 76 and 321. The inside count
     reproduced exactly.) The 76 go to
     `outputs/paris/excluded_stations.csv`, which
     `app/pages/21_Paris_Heatmap.py` **already cites** — `check_provenance.py`
     stays red until it exists. Naming the commune each excluded station sits
     in needs a multi-commune layer, so this is **Los Angeles' step 1 shape,
     not San Diego's**; `geo.api.gouv.fr` can resolve the names.
  3. **`step2_clean_businesses.py`** — the traps are all measured, and each one
     fails silently rather than loudly:
     - active is the **letter `A`**, never the label `Actif` (which returns
       zero rows for all six French cities — keep Paris as the control);
     - `codeCommuneEtablissement` prefix **`751`**;
     - `statutDiffusionEtablissement == "O"` (13.4% masked at source);
     - join geolocation on `siret`, and **read the per-row `epsg` column**
       rather than hard-coding 2154 — the DOM values are real;
     - drop `qualite_xy` **class 33**, which is commune-centroid grade and must
       not be drawn as a street address;
     - name = `enseigne1Etablissement` or `denominationUsuelleEtablissement`,
       **else the address** (42.9% carry either; Paris is the worst-named of
       France's six cities).
  4. **Two measurements this build owes, both currently unmeasured.** The
     market-stall codes `47.81Z/47.82Z/47.89Z` are excluded in `france_naf.py`
     on reasoning whose supporting share **nobody has counted** — count it, and
     if it is large, re-take the call rather than leaving the footnote. And
     sample the five `CATCH_ALL_CODES`, `96.09Z` first at **8.6%** of bucket
     rows, then put the verdict in `pipeline/paris/config.py` as an exclusion
     list. The national module deliberately does not make either call.
  5. **`step3_map.py`** — 16 `LINE_SHAPES`, each with the name riders use
     (M1–M14 plus 3bis and 7bis, which are separate lines and not variants).
     ⚠️ **IDFM's network plans are CC BY-NC-ND 3.0 France**: redraw from
     `shapes.txt` only, and use no IDFM schematic as a source or an overlay.
     `label_focus` is the commune polygon.
  6. **Checks, in order.** Add Paris to `scripts/check_personal_exposure.py`'s
     `REGISTRIES` and run it; `drift_check.py paris`; `check_provenance.py`
     (two failures are currently **correct** and must clear by being *fixed*,
     not relaxed — the missing CSV, and `city_master_list.md` still saying
     `Built - 20`, which becomes true to bump only once Paris really is built);
     **measure** Paris's macro-map label width in a real browser with Space
     Grotesk loaded and add it to `check_macro_labels.py` (it refuses a guessed
     width); `check_deploy_imports.py --ref paris-build`; then `deploy-verify`
     with scope `city-added`, and a **reboot** after the push.
  7. **Page prose carries two obligations no other city's does.** Notice 24
     needs the snapshot date and update interval *displayed*, and Art. 5.7's
     duty is the inverse of MTA's — it requires **exhaustivité**, so the page
     must state what was excluded (commuter rail, tram, the 77 out-of-commune
     stations) rather than leave it implicit. Art. 5.4(a) also prescribes the
     **linking**, which `render_site_notices()` has never had to do.

  **Still open, none of it blocking:** whether `enseigne1` or
  `denominationUsuelle` wins when both are present (cosmetic now that neither
  path reaches a person's name); whether the annual *déclaration de conformité*
  applies to a static density map (L. 1115-5 — worth asking
  `donnees-mobilite@autorite-transports.fr` rather than assuming, because it
  creates a *recurring* duty); and IDFM's own licences page contradicting the
  NAP by calling its *tracés* Licence Ouverte, where **the stricter reading was
  adopted deliberately** and would change this city's notice if ever relied on.


- [ ] **🇫🇷 Validate the SIRENE storefront filter against OSM in the FIRST
  non-Paris French city built — not in all five, and not skipped.**

  Measured 2026-09-22: **geolocation is confirmed for all six French cities**
  (Paris 99.98%, Lyon 99.97%, Marseille 99.91%, Rennes 99.90%, Toulouse
  99.85%, Lille 99.71%), so there is no geocoding leg anywhere in France.
  **What is still Paris-only is the composition check** — that the storefront
  filter selects the *right rows*, not merely rows that have coordinates.

  ⚠️ **THE ORIGINAL COMPARISON IS SUPERSEDED. Re-run it, do not inherit it.**
  This item read "**50,156 against OSM's 54,198** (92.5%), and **10,595 against
  10,642** on restaurants alone" and called that the comparison that turned
  France from a rejection into a build. **The SIRENE side of it cannot be
  reproduced.** It was attributed to an employee filter, and measured
  2026-09-23 over all 149,166 Paris bucket rows, `trancheEffectifs` is `NN` on
  **77.3%** of them — so every banded row together is 33,918 and no predicate
  on that column reaches 50,156.

  Re-established from scratch 2026-09-23, same commune, this project's own
  Overpass helper:

  | | OSM | SIRENE | ratio |
  |---|---|---|---|
  | Total | **48,973** | **87,164** | **1.78×** |
  | `amenity=restaurant` vs NAF `56.10A` | **9,058** | **16,280** | 1.80× |

  The **OSM side reproduces** (48,973 against the recorded 54,198, and 9,058
  against 10,642 — my tag set is slightly narrower). The **SIRENE side does
  not**: 16,280 against a recorded 10,595, on the one definition where the two
  schemes mean the same thing.

  **What this does and does not overturn.** France remains a build — register,
  join, coverage and licence are untouched. What falls is the *claim* that
  SIRENE lands at 92.5% of OSM; it is about 1.78× of it. The residual is
  disclosed on the city page rather than filtered away, because tuning until
  the number matched OSM is what produced 50,156.
  ⚠️ `docs/global_country_shortlist.md`'s France row still rests on the old
  figure and needs the same correction.

  **Why this is a checklist item and not a paragraph:** the two halves are
  easy to conflate, and the geolocation half is now so clean that it invites
  treating the whole country as settled. It is not. Run the OSM comparison on
  whichever city is built after Paris — **now genuinely a second data point
  rather than a confirmation**, since the first one turned out to be wrong.

  Storefront layers, for sizing the comparison: **Paris 87,164 (measured)**;
  Marseille 8,065, Lyon 7,354, Toulouse 4,833, Lille 3,272, Rennes 2,089 —
  ⚠️ **the five follower figures are scaled from the same superseded basis as
  50,156 and should be treated as ordering hints only.** **Rennes and Lille are
  an order of magnitude below Paris** — a separate scope call about whether a
  ~2,000-point city earns a page, not a data problem.


- [x] **Region switcher on the macro map — DONE 2026-09-22 (`2121ada`).**

The macro map opens on the United States and re-centres on any other region,
which is what `docs/scaling_thresholds.md` required before a city outside North
America. `app/cities.py` carries the region model (`f80d04b`); `app/Overview.py`
carries the radio, the region-aware caption and the fix.

**The fix was `st.session_state.pop("macro_map", None)` on a region change.**
`st.pydeck_chart(on_select="rerun")` persists the viewer's view under its widget
key and restores it on rerun, ignoring `initial_view_state`. A per-region key
was tried and rejected: Streamlit restores the previous key's state when the
viewer switches back.

**The constraint held and was measured:** zoom 1.4525 in both regions, centre
34.067N to 48.599N. Re-fitting on Canada's cities would give 1.5048 and
invalidate all fourteen pixel `label_offset` values.

**Keep this warning for anyone editing the macro map's view:** that same
persistence makes a changed `initial_view_state` invisible in a browser session
that has already rendered the page, across server restarts included. Test in a
fresh session (a new query string is enough) or you will debug correct code.

- [x] **`deploy-verify` on the switcher — steps 1, 2, 3, 6, 7, 8, 9, run
2026-09-22.** No named scope fitted: the change is the Streamlit macro map plus
an import under `app/`, where `map-chrome` covers overlays inside the per-city
rendered map HTML and says the app is usually not needed. Passed: lean-venv
start with no import error, all 14 cities in the DOM, the real click path
through a name pill to a city page in BOTH regions (`st.switch_page` survives
the new widget), caption flipping, zoom pinned, attribution present, dark mode
inverting the basemap with the radio still legible. The only console errors
were two `ERR_CONNECTION_REFUSED` on `/_stcore/health`, bracketed by `200 OK`
either side — the stop/start gap, not the running server.

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375px — in the
Canada region as well as the US one.** Found during the run above. NOT a
regression: `fit_view` is byte-identical to the pre-switcher commit and frames
`IN_DEFAULT_VIEW` (US only), so Vancouver was never in the fitted box. But the
switcher makes it newly user-facing, because it now invites a viewer to look at
Canada and Canada still does not frame its own westernmost city. This is the
direct cost of RE-CENTRE-NEVER-RE-ZOOM: centring on Canada's midpoint leaves a
long label 25 degrees west of centre.
Options, in increasing cost: shorten the label to "Vancouver"; give that city a
right-side anchor; or set `REGIONS[i]["zoom"]` for Canada, which exists for
exactly this and costs a re-measure of that region's `label_offset` values.
Desktop is unaffected — the label is fully visible there.


- [ ] **Next city** - pick from the list below. Start with the `add-city`
  Step 0, then `scripts/scaffold_city.py` (the `scaffold-city` skill). That
  build is also the first real test of the scaffold: record in `DECISIONS.md`
  whether it saved effort (estimated at about 10%) and fix any template that
  needed rewriting.
  **Vancouver has a build brief ready** - `docs/build_briefs/vancouver.md`
  banks Step 0's answers (all three endpoints with their traps, EPSG:32610,
  the rejected address join against the spatial one that works, both required
  notices with exact wording), so that build starts at the scaffold command
  rather than at Step 0. **One of its seven open questions is an owner
  decision rather than a build one:** `businesstradename` is blank on 63% of
  rows, and restricted to the categories this project maps, 16.94% of
  displayed names match the person pattern - the storefront filter makes it
  worse, not better. What a pin displays on that fallback wants settling
  before the map renders, not after.
  - [x] **DONE 2026-09-21 — two clause families added to `read-licence`**
    (step 6's third adjacent category, and a new step 6b). Landed once
    Vancouver was built, and timely: **Montréal is one of the two worked
    examples**, and its build had just started.
    Original item, kept until its `DECISIONS.md` entry exists:
    **After the Vancouver build lands: add two clause families to the
    `read-licence` skill.** Deferred deliberately so the skill settles first
    (it was written 2026-09-21). Both recur and both were found by the global
    country screen. **(a) Licences that require disclosing TRANSFORMATION, not
    just crediting the source** - INEGI demands you "notificar al usuario final
    de cualquier análisis o transformación que haga a la información", and
    Montréal requires stating whether modifications were made *or
    interpretations drawn*. This project always triggers these (ring density,
    bucketing, storefront filtering), so a bare source credit does not comply.
    **(b) Registers that do the privacy work upstream** - France masks
    non-diffusible records including geolocation, Edmonton publishes
    `<REDACTED FOR PRIVACY>` on 9.3% of rows, Austria's GISA strips personal
    data before release. Worth checking before building a residence filter,
    because the work may already be done. Evidence for both is in
    `docs/global_country_shortlist.md`.

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20; see
  `DECISIONS.md` and `docs/navigation_sidebar_and_city_links.md`). The
  Overview's fallback link list is kept (decided 2026-09-21). The hop-between-cities
  gap is closed with a "Cities" dropdown on each city map (2026-09-21). Open: the
  final go/no-go. To revert, set `MAP_ONLY_NAV = False` in
  `app/cities.py`.
- [ ] **Midnight slate theme: the Streamlit page AND the map palette, as one
  change.** No longer deferred - the blocker was the assumption that an
  explicit theme forces the site dark-only, and separate
  `[theme.light]`/`[theme.dark]` blocks keep the toggle (tested). Decided
  2026-09-21 to stay on Streamlit rather than go static; see `DECISIONS.md` for
  why, and for the measurement showing a map-chrome reskin alone is not worth
  doing (it is ~15% of a city page's pixels; the tiles are filtered and the
  data colours are fixed, so no `--dm-*` variable touches them).
  **Everything needed to build it - palette, both value sets, the traps, the
  verification checklist - is in `docs/theming.md`.**
  - [x] `.streamlit/config.toml` with both light and dark blocks; the chooser
    Streamlit had been suppressing is back (System / Light / Dark).
  - [x] The map's `--dm-*` values swapped to slate, the macro map's duplicate
    copy removed, and everything sourced from the new `pipeline/theme.py`.
    `scripts/check_theme_sync.py` guards the one unavoidable TOML duplicate.
  - [x] **Two theme controls reconciled (option A, 2026-09-21).** With no
    stored choice a map follows the page it is embedded in; an explicit click
    wins from then on; a standalone map follows the OS preference. Verified
    all three: ambient-dark page gives a dark map (`storedTheme: null`), a
    click stores `light`, and that survives a reload on a dark page. Options B
    (our button drives the page, overriding Streamlit's widget CSS by hand)
    and C (remove the in-map button when embedded) were rejected - see
    `DECISIONS.md`.
  - [ ] Sweep the remaining hardcoded colours in `app/` now that a dark page
    exists: `Overview.py` still has literal `white` and
    `#1c2b2a` (lines ~90, ~139) for the macro map's markers and labels. Check
    contrast numerically against `#0B1220`, not by eye - a 1.01:1 label looks
    like empty space rather than a bug.
  - [x] Reconciled the two overlapping handoffs into `docs/theming.md`
    (2026-09-21). Both originals are in git history.

## Next cities, in ease order

- [x] **Philadelphia - built 2026-09-21.** The WKB parsing this item predicted
  was never needed (the Carto SQL API evaluates `ST_X`/`ST_Y` server-side), and
  `phl_licensetype` is filled from the full 50-type pull. What it left behind:
  - Two open licence questions, both to settle before the public deploy:
    SEPTA's trademark/commercial clause, and the "City of Philadelphia
    License", which reserves all database rights while granting nothing
    explicitly. See `docs/data_sources.md`.
  - Personal services is **absent**, not thin - the only such city. Stated on
    the city page and in `docs/excluded_categories.md`.
  - Regional Rail (52 well-spaced in-city stations, no thinning needed) is the
    obvious later addition if the commuter-rail exclusion is revisited.
  - The Girard Avenue Trolley's label uses SEPTA's own `#FFD700`, which is the
    lowest-contrast of the four over the orange heat wash. Cosmetic; swap for a
    darker gold if it reads badly on a real screen.
- [x] **Boston - BUILT 2026-09-21.** 3,164 premises, 2,410 within a ring
  across 57 in-city stations; see `DECISIONS.md`. What it left behind:
  - **MassDOT's acknowledgement notice is now ACTIVE**, not conditional, which
    takes the mandatory-notice count from four to five. The city page carries
    "Rail alignment data provided by MassDOT/MBTA"; the site-level placement is
    part of the same job as the other four.
  - **The residence check is blind here and the 0.00% reading is a measurement
    gap, not a clean result.** Boston's addresses carry no unit designators at
    all, so there is nothing for it to read - the same shape as San Diego's old
    0.03%, which became 2.80% once a parcel join replaced address text. What
    limits the real exposure is that a food-service or package-store licence
    requires commercial premises. The ISD table's `property_id` IS Boston's
    assessing parcel id, so a parcel join against the city's Property
    Assessment data (ODC-PDDL) is available if that is ever not enough.
  - `Business Inventory` stays recorded as available and deliberately unused;
    revisit only if the city extends that survey city-wide.
  - Regional Rail (52 well-spaced in-city stations) is the obvious later
    addition if the commuter-rail exclusion is ever revisited - the same
    follow-up Philadelphia has.
- [x] **Washington D.C. - BUILT 2026-09-21** as the ninth city; see
  `DECISIONS.md`. 5,230 premises, 3,860 within a ring across the 40 in-District
  stations - the highest ring coverage in the project at 73.8%. The first
  non-NAICS registry here to cover all three buckets on its own. Follow-ups it
  leaves behind:
  - **Three Step 0 findings recorded in this file were wrong, and the
    corrections are the useful part.** (a) "Trade name is missing on 49% of
    storefront rows ... the Los Angeles trap at half LA's severity" was
    measured before the category exclusions; on the rows that reach the map the
    gap is **26.9%**, 85.6% of those carry a company-shaped `ENTITYNAME`, and
    the residual is **14 pins / 0.36%**. (b) "`MAR_ID` should recover the rest"
    was wrong - the 452 rows with no coordinates are the **same rows** that
    lack `MAR_ID`, because they are what the District's own geocoder failed on,
    so a Census geocoding step was needed after all (it recovered 387). (c) The
    catch-all count was 14,770 for `General Business`; scoped to active and
    in-District it is **11,074**. The lesson is the one this file keeps
    relearning: a Step 0 percentage measured on the wrong denominator is worse
    than no percentage.
  - **`Delicatessen` is ambiguous in the source and stays ambiguous.** D.C.
    issues it to sandwich shops and to corner shops alike, so ~180 premises
    could honestly read as Food service or Retail. Recoverable only by
    classifying trade names, which is a project of its own - the same shape as
    Miami's `SERVICE BUSINESS`. Stated on the city page rather than hidden.
  - **A parcel-based residence rule is available and unused.** `SSL` is on
    **91.1%** of mapped rows - better coverage than Miami's `FOLIO` at 45.7%
    and comparable to what Philadelphia joins against. D.C.'s addresses carry
    almost no unit designators, so the address-text residence check reports
    0.00% and that is a measurement gap, exactly as in Boston. The structural
    signal that partly replaces it is `ENTITYTYPE`: 14 pins are a sole
    proprietorship with a person-like displayed name. Do the parcel join if
    that ever stops being enough.
  - **The feed expires in ten days and the key is not in the repo**, so this
    city cannot be rebuilt from a clean checkout without `WMATA_API_KEY` set
    and a fresh download. `outputs/washington_dc/` is committed, so the app
    does not care; `drift_check.py` does, and will report a missing raw input
    rather than drift. Worth deciding whether the drift check should say so
    more clearly for key-gated cities.
  - **The Silver Line is harder to trace in LIGHT mode than the other five**,
    and that is accepted rather than engineered around. See `config.py`'s
    `LINE_NAMES` comment for the measurements in both modes and the two
    alternatives that were rejected.
- [x] **Miami - BUILT 2026-09-21** as the project's first regional city; see
  `DECISIONS.md`. 3,775 within-ring pins across 42 stations in six
  municipalities. Follow-ups it left behind:
  - **Its licence position is not established** - Miami-Dade's `licenseInfo` is
    purely an accuracy disclaimer and says nothing about reuse, and its GTFS has
    no `feed_info.txt` and no developer terms were found. Same shape as the
    Philadelphia and NYC questions. Settle before the public deploy.
  - **`SERVICE BUSINESS` (28,010 rows) is excluded and contains some genuine
    repair shops**, so the map undercounts small repair and service premises.
    Recoverable only by classifying free-text `OCCDESC` - a project of its own.
  - A **parcel-based residence rule is available but unused**: `FOLIO` is on
    100% of City of Miami rows and only 45.7% of the regional set, so it would
    apply to half the map. Revisit if the coverage improves.
  - Ring coverage is 12.6%, the lowest here, because the business set is
    county-wide while the rail is one line plus a loop. Consider whether the
    all-businesses toggle should be scoped to station municipalities.
- [ ] **New Orleans - DEFERRED POST-DEPLOY by the owner (2026-09-21),
  alongside Seattle.** The pre-deploy city scope is the nine that are
  built; this and Seattle's multi-municipality build come after. Findings
  kept so returning costs nothing. Screened 2026-09-21, needs a real
  Step 0.** `iqay-p646`
  "Active Occupational Licenses", 16,396 rows, and the **cleanest licence of
  any candidate: CC0 1.0, explicitly declared**. Has `businesstype`,
  `businessaddress`, `the_geom`. Two sibling datasets exist (`abc4-h3u3`, an
  application-workflow file that also carries `naics`, `category` and an
  `ishome` flag; `hjcd-grvu`, 37,902 rows) - pick one deliberately rather than
  merging them. Rail is streetcar-only, which is a **scope** question for the
  owner, not a data one. Privacy flags: `ownername` and `businessphone`
  columns, and the name fields are inverted on some rows (blank `businessname`
  with the trade name sitting in `ownername`) - Boston's trap again.
- [ ] **Seattle - deferred by the owner 2026-09-21, and scoped as the project's
  first MULTI-MUNICIPALITY city.** Do not re-probe the Seattle registry itself;
  the findings are in `docs/city_shortlist.md`. On that evidence Seattle's own
  data is the best-equipped of any candidate - an official nightly export,
  **active-only by construction**, 54,604 rows with real NAICS (no new taxonomy
  module), a trade name, and point geometry (no geocoding step). It is on
  ArcGIS rather than Socrata, which is why earlier screens missed it.

  **The owner's intent (2026-09-21): full line coverage, not just the city.**
  This is deliberately the first test of merging several jurisdictions'
  business data into one map, and it **supersedes the standing rule that
  stations in another city are a new project rather than a config change** -
  for Seattle specifically, by the owner's decision. The named jurisdictions
  are Seattle, Shoreline, Lynnwood, Tukwila, Federal Way, Bellevue and
  Redmond. What to check before scoping the work:
  - **The station list is wider than seven jurisdictions.** Link also stops in
    **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
    the 2 Line; if Federal Way is in scope then the extension also runs through
    **Des Moines** and **Kent**. So plan for roughly ten to twelve, and settle
    the list from the real GTFS stop set against a Washington municipal
    boundary layer rather than from memory - the same discipline that caught
    16 Trolley stations in San Diego and 54 in Los Angeles.
  - **Each jurisdiction is an independent Step 0**, with its own registry,
    schema, classification, coordinate quality, licence and privacy profile.
    Seattle's own data says nothing about Lynnwood's. Expect some to have no
    usable registry at all, and decide up front what the map does where data is
    missing - a gap in coverage is the failure mode that made Boston's
    `Business Inventory` unusable, and it would appear here as whole
    suburbs reading as empty rather than as unsurveyed.
  - **The architecture already supports the taxonomy side.** Taxonomy plurality
    means each jurisdiction can carry its own module mapping into the shared
    three buckets, and `map_common.py` never names a taxonomy, so the map layer
    needs no fork. If several use NAICS (likely in Washington), they share
    `naics` and the merge is mostly plumbing.
  - **What genuinely does not exist yet** is multi-polygon scope: `CITY_KEEP`
    and the boundary filter assume one city. A multi-jurisdiction build needs a
    boundary *set*, per-jurisdiction row provenance on every business (so the
    map can say which registry a pin came from, and so a single city's data
    going stale is visible), and a cross-registry dedup rule for businesses
    licensed in more than one jurisdiction.
  - **Naming stays neutral**: this would be a region, and the project is never
    named after a city - so the page name needs deciding too ("Link light rail"
    rather than "Seattle" may be the honest label if it spans twelve cities).
- [ ] San Jose, Denver, Austin, Charlotte, Fort Worth, **Dallas, Houston**:
  ruled out. Dallas was ruled out 2026-09-21 on **currency** - its
  certificate-of-occupancy feed froze on 2022-11-15 and the dashboard this plan
  pointed to is not a dataset at all (HTTP 403, 0 columns). See
  `docs/city_shortlist.md`.
- [ ] **Fifteen further rail cities were screened shallowly and nothing
  surfaced - that is NOT a disqualification.** Atlanta, Baltimore, Portland OR,
  Phoenix, Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve of those
  returned HTTP 404 from Socrata's discovery API, which means "not a Socrata
  domain", and the ArcGIS pass searched titles only. **Seattle proves the
  point**: it came back "no matching datasets" on Socrata and has a 54,604-row
  official layer on ArcGIS. Any of these needs a proper per-portal check before
  being written off.

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

Ten cities; JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Deferred downloads are listed by domain in the
evidence section.

- [x] **A. Address file** — MLIT 位置参照情報 (block + town-chōme) per
  municipality. The Address Base Registry MOVED (`dataset.address-br.digital.go.jp`,
  plus an official geocoder) — not needed at these rates.
- [x] **B. Minato control join** — 99.8% of fixed premises at block level.
- [x] **C. Privacy** — individuals' names withheld at source (Minato: 12 of 5,721).
- [x] **D. Coverage** — Tokyo: **8 wards** with full, current food lists
  after the wards' own sites were read (2026-09-24); Chiyoda and Toshima are on
  request only and Bunkyō publishes none. The other nine cities: measured.
  MHLW's national open data is an opt-in slice that completes only Fukuoka and
  Hiroshima.
- [x] **E. Downloads (Tokyo)** — 60 files, 12.2 MB, in bounds.
- [x] **F. Join** — Tokyo 99.1–100%, Osaka 99.1%, Kobe 96.5%, Sapporo 84.5% (+15.2%
  chōme), Fukuoka 98.1% / 96.7%, Sendai 95.1%, Hiroshima 95.9% / 94.7%; independent
  checks median 22–43 m.
  - [ ] Like-for-like control against the Economic Census per-ward 飲食店 count
    (the owner's chosen control) — at build.
- [x] **G. Buckets** — food everywhere published; personal services from the
  生活衛生 registers; food retail only where 届出 are published (a disclosed
  partial bucket, owner). No general retail.
- [x] **Owner: scope** — Tokyo is 8 wards now, with the missing wards named on
  the page; the owner requests Chiyoda's ledger in parallel.
- [x] **Owner: band** — re-banded 2026-09-24 and the geocoding band closed.
  Tokyo, Osaka, Kobe, Sapporo and Fukuoka to A; Hiroshima to C; Sendai to D
  (permission); Yokohama, Nagoya and Kyoto to the open gap.
- [x] **Licences** — all read, each PERMITTED WITH CONDITIONS; the cost clauses
  were accepted. See each brief.
- [ ] **Rail** — MLIT N02 with JR and private lines; decide intercity-only
  services (Shinkansen, limited-express-only). **Owner, once for all five.**

### ▶ Handoff to main — the Band A candidates, 2026-09-24

**All 20 Band A cities are buildable**: each has a brief whose checks pass live
and its licences read. The items below are what should be settled BEFORE
main starts a city. Everything else is a decision inside the build, which the
brief names.

- [~] **Japan (Tokyo, Osaka, Kobe, Sapporo, Fukuoka) — shared code first
  (staging, started 2026-09-24).** Five cities run on one join. Lift
  `scripts/screen_japan_join.py` into `pipeline/japan_join.py`, and write a
  shared taxonomy for 営業の種類 in `pipeline/taxonomies/`, as Brazil's CNEFE
  module was written before its second build.
  - [x] **Stage 1 (2026-09-24): the join core MOVED unchanged** into
    `pipeline/countries/japan_register.py` (20 definitions). The script now
    imports it and keeps only the measurement. Identical output on all 24
    city and ward keys, with Minato at 99.8%.
  - [x] **Stage 2 (2026-09-24)**: `pipeline/countries/japan.py` (N02 without
    the Shinkansen, N03 city lines, ISJ templates, ward codes and EPSG,
    `stub_test()`) and `pipeline/taxonomies/japan_eigyo.py`, registered as
    `japan_eigyo`: 19 ordered rules with import-time checks. Over 229,504 fixed
    premises in ten lists: Food service 76.4%, food-only Retail 18.2%, out 5.3%.
    Every one of the 125 fall-through values is manufacturing, processing or
    the 0.04% catch-all. **Main can now start Osaka**
    (`add-city`, `pipeline/osaka/`), reading the join, the facts and the
    taxonomy from the shared modules.
  - [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many are gelato
    counters) is OUT for now, since the owner's call named 菓子 and そうざい.
- [x] **Kyoto → Band A (owner, 2026-09-24), in this order, after a /compact:**
  all five steps done 2026-09-24. Brief checks pass 8/8.
  1. [x] **Done 2026-09-24.** Kyoto food 92.7% block, 6.0% chōme, 1.3% none;
     personal services 94.4% / 4.1% / 1.6%. Minato stays at 99.8%. Two changes
     from the text below, both measured: the private-use codes sit in a
     Kyoto-only table, and C's prefix match on a 大字 that has 小字 looks the
     地番 up under that 小字 or leaves the row unplaced. Kobe, Sapporo, Sendai,
     Fukuoka and Hiroshima briefs updated. See DECISIONS.
     Add the rebuild's rules A–D to `pipeline/countries/japan_register.py`.
     The rule text is in `scratchpad/japan_run/kyoto/result.json`.
     - A: strip the street-intersection part (上る/下る/入る), Kyoto only.
     - B: character variants in `VARIANTS` (祇/祗 and Kyoto's private-use
       characters, 藪/薮, 壷/壺, 桧/檜, 篭/籠, 竃/竈, 竜/龍, 渕/淵, 祓/秡; 鍛治→鍛冶,
       廻リ→廻り; expand ゝ).
     - C: a known-town fallback, where the longest known town in the ward
       ends or starts the parsed town.
     - D: same-named twin towns in 上京, 中京 and 下京 are left unplaced.
     
     B and C apply to every city. Capture a before/after of all 24 keys plus
     Kyoto (`scratchpad/japan_run/baseline_all.py`), keep Minato at 99.8%,
     and update any brief whose number moves.
  2. [x] **Done 2026-09-24.** The stitch moved into the pipeline as
     `japan_register.kyoto_permit_stream(raw_dir, as_of)`, so the screen and
     the build run one copy. The build must pin `as_of` and never use today.
     The screen's `kyoto` and `kyoto-life` keys read 28,459 / 5,828 fixed
     premises at 92.7% / 94.4% block. `xlrd` was added for the 2021 `.xls`.
     **Stub test passes.** Karasuma keeps 15 of 15 stations and Tōzai 16 of 17.
     Randen, Eizan, Keihan Ōtō and Hankyū Arashiyama keep all of theirs. JR and
     the private railways are cut at the line.
     ✅ **Owner, 2026-09-24:** Keihan Keishin passes (3 of 7 stations is half
     a line, not a stub). The two funiculars (Eizan cable, Kurama-dera) are
     drawn. The Sagano scenic line is left out as a tourist line. The brief
     carries all three.
     Add a `kyoto` entry to `scripts/screen_japan_join.py` (the stitched list,
     `data/kyoto/raw/isj`), and put Kyoto's ward codes (26101–26111) and
     EPSG:32653 in `japan.py`. Run the stub test.
  3. [x] **Done 2026-09-24: PERMITTED WITH CONDITIONS** (CC BY 4.0, applied
     by the portal's terms, 第3版). The notice names 京都市オープンデータ and
     says the data was processed. Nothing is owed to the City. Fetch only
     from the portal. Recorded in the brief and in `data_sources.md`.
     `licence-read` on data.city.kyoto.lg.jp (CC BY 4.0 declared).
  4. [x] **Done 2026-09-24**: `docs/build_briefs/kyoto.md`, checks 8/8.
     Write `docs/build_briefs/kyoto.md` with a checks block. It must disclose
     a rebuilt register (the 2021 list plus monthly permits within their
     term), closures unknown (an upper bound), and vehicles excluded.
  5. [x] **Done 2026-09-24**: A 21, gap 8.
     Move Kyoto's master-list row from the open gap to Band A. **Osaka is the recommended
  first build**: the cleanest list, 99.1% block, 38 m against the city's own
  coordinates.
- [ ] **Japan's licence reads, consolidated into `docs/data_sources.md`
  (2026-09-24).** The consolidation found gaps:
  - [x] **N03** (the city line), read 2026-09-24. CC BY 4.0, permitted for
    picking stations and anchoring labels. ⛔ **Never drawn.** Showing its
    boundaries as a map may need GSI's approval under the Survey Act, and
    that question is open. The maps never draw a boundary, so nothing is
    blocked. The rule is in `japan.city_boundary()` and every Japanese brief.
  - [x] **Four Tokyo wards whose terms were never read**: Shibuya (its ArcGIS
    site), Taitō, Setagaya and Meguro (BODIK). **Read 2026-09-24 (owner):
    all PERMITTED WITH CONDITIONS, CC BY 4.0, nothing owed.** Their cost
    clauses are within the Japan-wide acceptance, and Shibuya has none. Each
    needs its own credit. Found on the way: Meguro's 生活衛生 registers on BODIK.
    **Downloaded and joined the same day (owner)**: 1,412 premises at 100.0%
    block, so Tokyo's personal services now total 16,299.
  - [x] **The fault-based cost clauses: ✅ ACCEPTED by the owner
    2026-09-24 for every Japanese source**, as for Taiwan. That covers
    Fukuoka 第４条, Hiroshima 第3条 and MHLW 免責 1) エ, beside Tokyo's and
    Sapporo's, and later sources of the same class. Anything broader comes
    back to the owner.
- [x] **Kyoto's place in the Japanese build order (owner, 2026-09-24): after
  Fukuoka, before Tokyo**, which stays last. Kyoto is the first rebuilt
  register in Japan, so it benefits from the join being settled on four
  cities first.
- [ ] **Kyoto, at build**: pin `as_of` to the fetch date. Before publishing,
  measure same-address successors and the factory share of 菓子 and そうざい
  (brief, "Still unknown").
- [~] **Japan — three owner calls that recur in all five briefs.**
  1. [x] **The Shinkansen does NOT count** (owner, 2026-09-24): it is
     long-distance travel between cities.
  2. [x] **City line only, with the stub test** (owner, 2026-09-24): only
     stations inside each city get rings, matching the city-only permit lists.
     Stage 2 measures each line's stations inside and outside (N02 against
     MLIT's N03 boundaries), and any urban line the city line cuts to a stub
     goes back to the owner (the Rennes and Lille test). Neighbours are a
     later, case-by-case upgrade.
  3. [x] **菓子製造業 and そうざい製造業 COUNT** (owner, 2026-09-24): bakeries,
     confectioners and delis are counter shops. They join the Retail bucket
     with the other food-retail permit types.
  - [ ] Stage 2 carries 1 and 3 into the taxonomy and the five briefs' open
    items.
- [ ] **premises-taxonomy skill** — add the São Paulo session's sampling
  lesson (CNEFE rules v2): words chosen from a sample of unmatched rows rescued
  14.7% of that sample but 3.5% of all rows. **Measure a rule's yield on a
  FRESH sample**, never the one it was chosen from.
- [x] **Japanese build order (owner, 2026-09-24): Osaka → Kobe → Sapporo →
  Fukuoka → Kyoto → Tokyo LAST.** (Kyoto was added later the same day, owner.) The stub test cleared the first four: every urban
  line keeps 80–100% of its stations inside the city line. Tokyo failed, with
  Chiyoda missing from the centre of its 8 wards. Tokyo goes last as the
  densest, and it benefits most from a Japan skill written off the first four.
- [ ] **Tokyo — the missing wards as a planned project, before its build.**
  Chiyoda alone lifts urban station coverage from 45% to 56%; Chiyoda,
  Toshima and Bunkyō reach 67%; all 23 wards reach 98% (`tokyo.md`).
  Routes: request Chiyoda's ledger (owner, gated item 22); extract Ōta's,
  Kita's and Arakawa's PDF lists; Shinagawa's and Itabashi's partial files;
  requests to Toshima, Nerima and Edogawa.
  - [x] ⚠️ **Tokyo's food lists measured against an official count
    (2026-09-24)**: Tokyo's statistical yearbook, table 19-8. Only Shibuya is
    essentially complete (98%). The others: Shinjuku 83% (2023), Taitō 71% and
    Setagaya 63% (opt-outs left out), Meguro 46%, Minato 30%
    (consent-filtered), Chūō 12% and Kōtō 9% (never updated). The ward probes
    found no open file that fills any gap. `tokyo.md` has the table.
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32). Not sent, and not the next step.
    The next step is the own-time probe round below.
  - [x] **The own-time probe round, 2026-09-24**:
    - MHLW's slice adds at most about +3%.
    - OSM holds 8–10% of Shibuya's register: not viable.
    - Shinjuku's PDF list is NOT PERMITTED or ambiguous, so Shinjuku stays on
      its 2023 CSV.
    - Two COVID-era Tokyo lists would lift Chūō, Kōtō and Minato to about
      50–60%, but they ask not to be used beyond COVID measures.
    - `tokyo.md` has the table.
  - [x] **Owner decisions for Tokyo (2026-09-24):**
    1. **The COVID-era lists are NOT used.** Honour the stated purpose and
       the shops' limited consent.
    2. **Tokyo ships all 8 food wards, each ward's share of the official
       count disclosed** on the page (Shibuya 101% down to Kōtō 9%).
    3. **MHLW's slice is added** to the four partial wards at build (PDL 1.0,
       already accepted), de-duplicated by address and name.
    **Drafted 2026-09-24** in formal Japanese, one per ward:
    `docs/notifications/tokyo-{chuo,koto,minato,shinjuku}-request.md`. Each
    asks for open publication first. Before sending, confirm each ward's
    address, which is not verified in any of the four.
  - [x] **Meguro's 52% explained (2026-09-24): its lists hold first permits
    only.** Every revised-law row is 新規 (2,495 of 2,495), and so is every row
    of seven monthly 「新規、更新、届出」 lists. Restaurant permits run flat at
    about 290 a year, while Tokyo's revised-law count grew by 27,419 in FY2024
    as old-law holders moved across. Premises that moved from an old-law
    permit are in neither list. No overlap between the halves, and the ward's
    page carries no opt-out wording. **Coverage will shrink** as the
    remaining 1,087 old-law permits expire (584 in 2026). No own-time fix, so
    it ships disclosed.
  - [ ] **Licence reads** for two side finds: Chūō's complete
    personal-services lists (August 2026) and Shinjuku's (June 2026, PDF).
  - [x] **The designated cities against the same kind of count** (MHLW's
    衛生行政報告例, FY2024, old law + revised law): Kobe 101%, Sapporo 100%,
    Fukuoka 101%, Kyoto 93%, Hiroshima 99%, Sendai 101%. These lists are
    complete. `docs/japan_city_list.md` now measures every city this way.
- [x] **Osaka's 67% probed (2026-09-24): the official count is most likely
  inflated, not the list short.** Its old-law count exceeds what can exist by
  about 12,000. The list is even across wards against the Economic Census,
  and every file since 2023 reads 69–76%. The build is NOT blocked. The page
  carries the disclosure drafted in `osaka.md`.
- [ ] Optional, and ours to do: e-Stat 衛生行政報告例 tables 1-2 and 3-2
  (permits issued and closed per city) would settle Osaka's residual: 20–35%
  of each year's permit numbers are unexplained.
- [ ] **Fukuoka** — agree the wording that discloses the ~20% of restaurants
  with no published address. BODIK is flaky, so `fetch_sources.py` retries.
- [x] **No pre-build items**: Seoul (its brief is deliberately partial, and
  geocoding the rest of 一般飲食店 is build work), Hong Kong, the nine Brazilian
  cities (São Paulo is already with main), the three Taiwanese cities, and
  Rotterdam (its build-time calls are in its brief).

**Not ready for main:**
- **Band C (6)** — one owner decision moves all six: does a single-bucket page
  belong beside three-bucket cities?
- **Band D (4)** — each waits on an owner act or on access: Sendai's request
  (drafted), Kaohsiung's request, and reads from inside Poland and India.
- **The open gap (8)** — re-probes, not builds.

**Owner's outside actions** are tracked in `docs/gated_access.md`, the list of
every key, account and letter:
- [ ] Item 21: send Sendai's request (`docs/notifications/sendai-permission-request.md`).
- [ ] Item 22: request Chiyoda's ledger.
- [ ] Item 23: place the Tallinn building-register orders (two reports).
- Items 25–27 (Hiroshima, MHLW, Osaka) are optional confirmations, not gates.

### Brief-ready, not started — ordered checklists, 2026-09-23

**These five have a brief with passing checks and no item here until now.**
Each list is in build order and every line is a measurement, not a template
step. Briefs: `docs/build_briefs/<city>.md`. Run
`python scripts/brief_check.py <city>` first — a brief caches Step 0's
mistakes as confidently as its findings.

- [ ] **Paris** 🇫🇷 — brief 7/7, **both owner calls settled**
  (commune-only; Milan-hybrid pins). Country facts in
  `pipeline/countries/france.py`; **five more French cities inherit them, so a
  correction belongs there, not in the city.**
  1. Fetch the **parquet**, not the zip — 2,210 MB vs 2,867 MB, and columnar,
     so step 2 reads ten columns of fifty-four.
  2. Match the resource title **with its trailing ` -`**, or
     `StockEtablissementHistorique` matches too. **Never `StockUniteLegale`** —
     30,020,346 legal units keyed on `siren`, the registered-office map.
  3. Filter `codeCommuneEtablissement` prefix **`751`**, active =
     **`"A"`, not `"Actif"`** — the label returned zero rows for all six
     cities. **Run Paris first as a control against 149,166** (re-measured
     2026-09-23 over the whole file; the brief's 148,633 was 0.36% lower, a
     month's churn rather than an error).
  4. Join the geolocation parquet on `siret`. **Read the `epsg` COLUMN** — it
     is per row; 2154 here, 2975/5490/2972 overseas.
  5. **Exclude distance selling: `47.91A`, `47.91B`, `47.99A`, `47.99B` —
     15.5% of bucket rows, no storefront.**
  6. Taxonomy keys at **sous-classe** (catch-all 19.3%; *groupe* would be
     49.4%). `96.09Z` alone is 8.6%.
  7. Pins: **premises name where it exists, address otherwise.** **Do NOT
     build the legal-name join** — settled 2026-09-22.
  8. Rail: **IDFM's own feed only**. **Record the download date in
     `fetch_sources.py`** — there is no `feed_info.txt`, and Licence
     Mobilités Art. 5.7 requires the date and update interval on the page.
  9. Notices: Art. 5.4 text **with both hyperlinks**, plus snapshot date and
     update interval. Region **`Europe`**.
  10. Open: whether the annual *déclaration de conformité* applies — a
      **recurring** obligation, so ask rather than assume.

- [ ] **Hong Kong** 🇭🇰 — brief 7/7, **indemnity ACCEPTED
  2026-09-22** with three binding conditions.
  1. Three XML registers from `fehd.gov.hk/english/licensing/license/text/`.
     100% fill on `SS`, `ADR`, `TYPE`, `DIST`, `EXPDATE`.
  2. **Filter out the 14,263 non-storefronts**: `FF` Food Factory (11,566),
     `TP` Swimming Pool (1,440), `FG`, `FE`, `FC`, `FM`, `TU`, `TF`, `TO`,
     `TS`. **35,808 → ~21,545.**
  3. Taxonomy: **flat, 20 types, catch-all 0%**, and `TYPE_CODE` ships inside
     the download. No level to choose — no module work beyond the mapping.
  4. Geocode via ALS. **Budget ~35,000 lookups**: addresses are 1,799 distinct
     of 1,800, so unlike Singapore they do **not** collapse. ~2.5 h at the
     measured 3.9 req/s.
  5. **Set a Score threshold** — 21.1% of hits score 50–75. Decide what
     happens below it.
  6. **`check_personal_exposure.py`, catch-alls excluded** — indemnity
     condition 2, a risk control rather than a formality.
  7. Notices: **source + Government IP acknowledgement + DATA.GOV.HK**, all
     three, exactly.
  8. ⚠️ **Needs a NEW map region** — owner/app call. It is not Europe.
  9. Open: whether `EXPDATE` should filter; the `INFO` field's 6-code lookup.

- [ ] **Prague** 🇨🇿 — brief 5/5, **both licences read
  2026-09-23**, nothing licence-shaped blocks it.
  1. ⚠️ **Take the RÚIAN URL from the ATOM service**, not a hard-coded
     path: `atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_554782`.
     It sidesteps the VDP application's ban on automated extraction **and**
     fixes the `20260831` path, which goes stale on the 1st of every month.
  2. Stream RES, `OKRESLAU == "CZ0100"`, active = `DDATZAN` empty.
     `FIRMA` is **100%** — a name on every row, unlike Milan or Paris.
  3. Join `KODADM` → coordinates (99.8%). **`EPSG:5513` with (X, Y) as
     published** — the wrong orderings land in Germany and the Arctic
     **without erroring**.
  4. ⚠️ **Taxonomy must match on PREFIX** — CZ-NACE is ragged: 4.4% at 2
     chars, 31.4% at 3, 6.2% at 4, 57.9% at 5. **No level can be keyed.** This
     has no precedent here; the four existing local taxonomies all had uniform
     depth.
  5. Rail: **OSM, 85 relations, all named** — the Golemio key is **not**
     needed. **Assign colours to the 24 without one**; every drawn line needs a
     label and a legend entry.
  6. Notices — **five obligations across two publishers**, and **two are
     transformation disclosures**: ČÚZK's literal **`ČÚZK, 2026`** + a link to
     its conditions + *"popis úpravy"*; ČSÚ's licence link + derived-data
     marking. They may share one sentence only if it names both.
  7. Open: whether to apply the `KATPO` employee filter (85,022 → 38,575);
     scope beyond `CZ0100`.

- [ ] **Oslo** 🇳🇴 — brief 3/3, **both licences read** (NLOD +
  CC BY 4.0).
  1. ⚠️ **Take the bulk file, and filter
     `beliggenhetsadresse.kommunenummer` LOCALLY.** The API's
     `?kommunenummer=0301` does **not** constrain the address you read — the
     misses were Bergen, Copenhagen, Paris and Malmö — and it stops paging
     past ~10,000 sorted by name, so it **cannot** settle scope.
     **138,896 in Oslo; 13,458 in the buckets.**
  2. Read `adresse` as a **LIST**; skip `c/o`, `postboks`, `pb`.
  3. Geocode two-stage: exact `adressetekst`, then plain `sok` (**97.8%**).
     ⚠️ **NEVER `fuzzy=true`** — it returned `Karenslyst allé 8B` as
     `allé 1B`, a different building.
  4. Taxonomy: **uniform 5-char depth**, so a level CAN be keyed — but
     **run `taxonomy_catchall` first**; it has not been computed. `96990` is
     the visible residual at 6.0%.
  5. ⚠️ **Rail is UNMEASURED** — probe Entur vs OSM. Three Overpass
     endpoints errored, so Oslo's station count is **missing, not zero**.
  6. Notices: **NLOD and CC BY 4.0 are different licences — two attribution
     lines, not one credit.**
  7. Open: whether `navn` is a trade name or a legal name — the question that
     caught Milan and Paris.

- [ ] **Marseille · Toulouse · Lille · Rennes** 🇫🇷 — **NOT
  brief-ready; country-ready.** No brief file exists for any of them. They
  inherit France's register, join and privacy handling, but **three things do
  NOT transfer from Paris.**
  1. **Their GTFS licences differ from Paris's and from each other.**
     ✅ **ODbL READ 2026-09-23** for Toulouse and Rennes — **PERMITTED WITH
     CONDITIONS**, written up at `docs/licenses/odbl-toulouse-rennes.md`.
     §4.5(b) settles the map: making a Produced Work **does not create a
     Derivative Database**. But **§4.6 fires on a Produced Work *from* a
     Derivative Database**, and the map is produced from the committed station
     CSV — **already satisfied by the public repo**, which is literally *"the
     method of making the alterations"*, **provided it is LINKED from the
     site**. §4.3 prescribes a safe-harbour notice per database.
     ✅ **Both publishers' CGU READ 2026-09-23 and BOTH ARE CLEAN** — no
     indemnity, and the marks clause is **Opendatasoft's own with the data
     expressly excluded**, so **naming Tisséo and STAR is not barred**. The
     express extraction bar is conditional on acting *outside* a licence, and
     this project is inside one. ⚠️ They answered plain curl — **the earlier
     Cloudflare challenge was path-specific, not a wall.**
     ⚠️ **Still open**: whether the station CSV is itself a Derivative
     Database under §4.4. **Unlike Paris there is NO publisher gloss** —
     Licence Mobilités had the NAP's published interpretation; ODbL has none.
     **Cheap discharge: put an ODbL notice on the station CSV.**
     ✅ **Marseille and Lille are `lov2` — Licence Ouverte 2.0 READ 2026-09-23**,
     **PERMITTED WITH CONDITIONS**, write-up at `docs/licenses/france-licence-ouverte-2.0.md`.
     **No share-alike, no revocation, no indemnity.** Attribution is **name +
     date of last update, PER SOURCE** — and the date-of-last-update duty is
     **LO 2.0's own**, so the three sightings (Licence Mobilités 5.7, Grand Lyon
     6.1, MEL) are ONE duty restated, not three inventions.
     ⚠️ **`Source : Insee` is prescribed VERBATIM** — the only fixed string
     in the five. ⚠️ **Render no publisher's logo.**
     ⚠️ **A STANDING refresh duty**: `statutDiffusion` changes as people
     exercise opposition, so a committed `outputs/` snapshot can contain
     someone who has since opted out. **Needs a stated refresh cadence.**
     ⚠️ **ODC-BY is named compatible; ODbL is NOT.** Do not read it as
     covering Toulouse or Rennes.
  2. ⚠️ **Scope does not transfer.** Paris went commune-only on a
     *measurement* — all 16 métro lines survived the boundary. Nothing
     guarantees that repeats: **Lille's commune is small against MEL**, whose
     métro serves Villeneuve-d'Ascq, Roubaix and Tourcoing. One
     boundary-vs-network measurement each.
  3. **The NAF catch-all (19.3%) and the 15.5% distance-selling exclusion were
     measured on PARIS rows only**, and per-city row counts are scaled
     estimates from a 3.9% sample, not build numbers.

  **Feeds VERIFIED 2026-09-23** — they had been identified, never downloaded:

  | City | Size | `shapes.txt` | `feed_info.txt` | Rail |
  |---|---|---|---|---|
  | Marseille | 34.0 MB | ✅ | ✅ end **2026-12-31** | 2 subway, 4 tram, 6 ferry |
  | Toulouse | 12.0 MB | ✅ | ❌ | 2 subway, 1 tram, **1 gondola** |
  | **Lille** | 9.2 MB | ❌ **MISSING** | ❌ | 2 subway, 1 tram |
  | Rennes | 13.4 MB | ✅ | ✅ end **2026-10-18** | 2 subway |

  4a. **Lille geometry — PROBED 2026-09-23. Tram is first-party; métro is
     NOT, and must come from OSM.**
     The portal is **geOrchestra, not Opendatasoft** —
     `opendata.lillemetropole.fr` serves an HTML app and
     `data.lillemetropole.fr` returns **404 JSON whose body names its own
     platform** (`georchestraStylesheet`, `logoUrl: /public/logo-mel.jpg`).
     So `/api/datasets/1.0/search` and `/api/explore/v2.1` are the wrong shape
     entirely. **Read the error body before guessing another path.**
     The working surface is **WFS**:
     `data.lillemetropole.fr/geoserver/wfs?service=WFS&request=GetCapabilities&version=2.0.0`

     | Mode | Layer | Verdict |
     |---|---|---|
     | **Tram** | `mel_mobilite_et_transport:tramway_lignes` — *"Tracés des lignes de tramway du réseau Ilévia"* | ✅ **4 LineString features**, lines **R** (Lille↔Roubaix) and **T** (Lille↔Tourcoing), with `nom`, `ligne`, `exploitant` |
     | **Métro** | — | ❌ **NO LINE GEOMETRY ANYWHERE ON THE PORTAL.** Only `stations_metro` and `dsp_ilevia:entree_sortie_metro`, both **points** |
     | Bus | `dsp_ilevia:ilevia_traceslignes` | 424 LineStrings — not needed |

     ⚠️ **A near-miss worth keeping.** `ilevia_traceslignes` is titled
     *"Tracés des lignes de **bus**"* and its `ligne` values include **`L1`**,
     which reads exactly like Métro Ligne 1. **It is not.** Its `type_ligne`
     values are `Urbaine`, `Suburbaine`, `Scolaire` and `Ligne de nuit` — all
     bus categories — and **`L1` is *Liane 1*, ilévia's high-frequency BUS
     brand.** The title was honest; the line code was the trap. **One field
     check disproved it.**

     🎁 **Bonus, and it solves a separate problem**: `dsp_ilevia:couleurs_lignes`
     exists, and `ilevia_traceslignes` carries `rgbhex_fond`, `rgbhex_texte`
     and `color`. Lille's GTFS `routes.txt` may not carry colours; **this is a
     first-party source for them**, and every drawn line needs a legend entry.

     **So Lille's rail geometry is a HYBRID or an OSM job** — an owner call:
     tram from MEL's WFS (first-party, named, with `exploitant`) and métro from
     **OSM** via `osm-rail`; or both from OSM for consistency. ✅ **MEL's WFS licence READ 2026-09-23: `Licence Ouverte v2.0 (Etalab)`**,
     from the ISO19139 `gmd:otherConstraints`. **PERMITTED WITH CONDITIONS** —
     its `gmd:useLimitation` requires *"mentionner la source (a minima le nom
     du producteur) **et la date de sa dernière mise à jour**"*. ⚠️ The WFS
     service-level `AccessConstraints: NONE` is **OGC boilerplate and was NOT
     taken** — the dataset records say `otherRestrictions`, which is INSPIRE's
     code for *see otherConstraints*, not for *no restrictions*. **Third time a
     date-of-last-update duty has appeared in France**, after Licence
     Mobilités Art. 5.7 and Grand Lyon CGU 6.1.

  3b. ⚠️ **OWNER DECISION — Lille's GTFS is served from
     `media.ilevia.fr`, and ilévia's Mentions légales §5 bars "pas de
     modification ni altération d'aucune sorte" and commercial use of "les
     contenus des Services en ligne".** *Services en ligne* is a **defined
     term** — ilévia's websites and apps — and the GTFS is **MEL's `lov2`
     publication**, so this is likely the **SEPTA pattern**: a web-contents
     notice mistaken for a data licence. But the host is ilévia's.
     ⚠️ **The obvious mitigation FAILS**: the PAN's stable
     `data.gouv.fr/api/1/datasets/r/c9e5dd3f-…` URL **302s to
     `media.ilevia.fr`** — a redirect, not a mirror. **Third "no modification"
     bar this project has met**, after LA Metro and Philadelphia.
     **Cheap close: email `opendata@lillemetropole.fr`.**
  4. ⚠️ **LILLE HAS NO `shapes.txt`.** Line geometry **cannot be drawn from
     its feed**, and this project's invariant requires every drawn line to
     carry real geometry plus a label plus a legend entry. Either reconstruct
     polylines from stop sequences or take Lille's geometry from **OSM**
     (`osm-rail`). **Decide before starting Lille** — it is the one follower
     with a structural rail problem.
  5. **Marseille and Rennes SELF-ATTEST** (`feed_end_date` 2026-12-31 and
     2026-10-18). **Toulouse and Lille do not** — same as Paris, so
     `fetch_sources.py` must record the download date for those two.
  6. **Toulouse carries `route_type 6`** — an aerial lift, the Téléo cable
     car. Paris draws a funicular, so a gondola is a **judgment call**, not an
     automatic include. Marseille's **17 `route_type 2`** are TER regional
     rail and are excluded by the standing commuter-rail rule.
  7. ✅ **OSM composition validation RUN 2026-09-23 on Marseille, and the
     filter HOLDS.** First the employee rule had to be **recovered**, because
     it was never written down: the `trancheEffectifsEtablissement`
     distribution shows **dropping `NN` (not reported) leaves 31.8% of Paris**
     against the recorded 50,156/148,633 = **33.7%** — within sampling
     variance. Applying the same rule: **Marseille ≈ 6,800 against OSM's
     6,340 = ≈107%**, where Paris was **92.5%**.
     **Both near parity, so the filter is not systematically wrong.** The
     swing is informative rather than alarming: **it measures OSM's
     completeness as much as SIRENE's** — Paris is densely mapped so OSM
     overshoots, Marseille less so.
     ⚠️ **The original Paris query was never recorded**, so today's OSM side
     is a reconstruction (`shop=*` plus food `amenity` values) and the
     comparison is **indicative, not an exact reproduction**. **Write the query
     down this time** — four more cities are meant to reuse it.

- [ ] **Göteborg** 🇸🇪 — promoted into Band D 2026-09-23. **One
  measurement away from being comparable to Stockholm.**
  1. ⚠️ **Get `Livsmedelsverksamheter`'s row count.** Its DCAT node exposes
     **no `accessURL`** and `resource/18` returns RDF, so the file was not
     reached. **Until this is taken, Stockholm's measured 8,146 is the stronger
     number** and "better data than Stockholm" stays structural, not measured.
  2. `Restauranger med serveringstillstånd` is **1,043 rows, CC ZERO**, with
     `Namn` and **`Besöksadress`** kept distinct from `Fakturaadress`.
  3. Then: **the one-bucket scope decision, which now covers Stockholm, Zurich
     AND Göteborg** — one call, three cities.

## Structure

- [x] **Re-render `outputs/dublin/heatmap.html` so the Use tooltip drops the
  `-` placeholder — DONE 2026-09-23 (`383687a`), without anyone setting out to
  do it.** A session re-rendering every city to fix map widths re-rendered
  Dublin with the fix in place. Measured on the committed map at each commit:
  `eb1b68d` (the original build) 88.9% of 7,595 pins carry the placeholder;
  `383687a` and every commit since, **0%**. That is also the first end-to-end
  proof the fix works through the real render path - the note below verified
  the function against extracted values, never an actual render. It sat open
  here for a day after it was done, which is the argument for closing an item
  by measuring the output rather than by remembering who was going to do it.
  Original note, kept as it was:

  The code fix landed 2026-09-22
  (`dublin_uses.display_value()`, used by `map_common.py`) and is verified
  against every value in the committed map: **88.9% of 7,595 pins improve and
  none is left with an empty Use line**. But the rendered map is committed
  output, and this worktree has no `data/dublin/raw/`, so the live site still
  shows "Use: -, SHOP". Needs a session holding Dublin's cache: run step 3
  and `drift_check.py dublin`, expecting a diff ONLY in the tooltip strings.
  If the cache is gone, `pipeline/dublin/fetch_sources.py` will rebuild it -
  but that is a re-fetch, so report what changed upstream rather than letting
  it ride in with the tooltip fix.

- [x] ~~**Collapse the European macro-map regions into one "Europe"**~~ -
  **done 2026-09-22, the same day the problem appeared.** `app/cities.py` gave
  every European country its own `region` - Spain (Madrid, Barcelona), then
  Ireland (Dublin) and Italy (Milan) - three regions holding four cities, and
  growing by one entry per country while the map it indexes stayed the same
  size. Collapsed on the owner's call **before France's six cities could make
  it five**, which is why it stopped being "not urgent".

  Done as one change: `REGION_ORDER` loses the three country entries and gains
  `Europe`, and all four cities are retagged. **No `label_offset` moved.**
  `scripts/check_macro_labels.py` scores every city in every region at three
  widths and reports **PROBLEMS 0** across the new 7-region layout - and one
  fewer clipped label than before (11, from 12), because collapsing three
  narrow frames into one wider one moves labels away from a canvas edge rather
  than toward it.

  ⚠️ **Two label widths had to be MEASURED first**, and neither city had done
  it: `TEXT_WIDTH` carried no Dublin and no Milan, so the checker would have
  refused regardless of this change. Measured in a real browser at
  `600 14px "Space Grotesk"` - **Dublin 42.8 px, Milan 36.3 px** - with the
  method validated by reproducing five existing entries (Barcelona 67.9,
  Madrid 47.2, Boston 48.4, Toronto 52.4, Washington D.C. 110.3) exactly.

  **Revisit the single-region decision on a measurement, not a feeling.**
  Europe's four cities span Dublin to Milan, about 1,700 km, and frame together
  at a zoom where each is still distinguishable; North America is split because
  its countries are 3,300 km wide. A city far enough east or south to force the
  frame open is what changes it, and `check_macro_labels.py` is what says so.

- [x] ~~Move GUADALAJARA's and MADRID's fetching out of their step files~~ -
  **done 2026-09-22; all three exceptions are closed.** Mexico City first as
  the worked pattern, Madrid by its own session on the unmerged
  `spain-app-wiring` branch, Guadalajara last -
  `pipeline/guadalajara/fetch_sources.py`, which took the three Overpass
  queries with it because each one's comment is addressed to whoever edits
  the query, and that is no longer the step. Proved both ways: zero drift
  with the cache present, and step 1 and step 2 both exiting 1 with "Run
  pipeline/guadalajara/fetch_sources.py first" with `data/guadalajara/raw/`
  moved aside. **Guadalajara's two-pass retry was kept rather than unified
  with Mexico City's single pass** - neither has been measured against the
  other, and a refactor is a bad moment to quietly change a retry policy. At
  the `spain-app-wiring` merge the two sessions' Guadalajara fetchers were
  resolved in the BRANCH's favour, because that one goes through the shared
  `pipeline/osm.py` (which rejects a `remark` and a partial 200, not only an
  empty one, and still retries twice) while master's repeated the logic in the
  city; its two step files were taken from MASTER, so both Mexican cities name
  the reader `read_cached`. **The rule is now a check rather than a
  convention:** `scripts/check_no_fetch_in_steps.py`. Madrid was listed there
  under `KNOWN_GAPS` until `spain-app-wiring` landed, and the check fails on a
  gap that has silently been fixed, so landing the branch forced both entries
  out - which is what that failure mode is for.

  The original finding: move the fetching into a `fetch_*.py`, as the other
  fourteen cities do.
  Demonstrated 2026-09-22: `python pipeline/drift_check.py` in a worktree with
  no `data/<city>/raw/` **fetched over the network for all three** - a 39 MB
  DENUE zip, a Madrid census CSV, Overpass responses and CRTM layers - and
  then reported zero drift. Toronto, by contrast, stopped with "no
  data/<city>/raw/ - nothing to run against", which is the correct behaviour.
  The calls are cache-guarded, so this is invisible on a machine that already
  has the data. **It changes what a passing drift check means:** for those
  three it asks "does the current upstream still produce the committed output"
  rather than "does the committed code". Build-session work - each city's
  context is needed.
- [x] ~~Wire Toronto's `STATIONS_COLLAPSED_EXPECTED`~~ - **done 2026-09-22,
  and it was a mis-wiring rather than a missing check.** Step 1 compared the
  COLLAPSED count (110) against `IN_CITY_STATIONS_EXPECTED` (108), printing a
  NOTE every run while the right constant sat unread. Both now guard what they
  name, an in-city check was added after the boundary filter, and the docstring
  no longer claims `excluded_stations.csv` is empty (it has two rows). Verified
  by running step 1: 234 -> 110 -> 108, two excluded, zero NOTEs.
- [x] ~~Write `scripts/check_stale_claims.py`~~ - **done 2026-09-22.**
  Reports and always exits 0. On its first real run it found three notices in
  the deploy gate marked NOT YET DISPLAYED - Chicago, SFMTA and LA Metro - that
  were all in `_NOTICES` and had been displayed for some time, so the list that
  gates the public deploy was understating this project's compliance. Tuning
  history is in the module docstring and the sweep skill: digits matched 1,012
  measurements, undetermined counts 265 mostly-correct scoped facts, and
  requiring a determiner cut it to 74. **Known blind spot:** category A matches
  on built CITY names, so agency names miss - two of the three notices above
  were found by a follow-up grep rather than by the tool.

- [x] ~~Fill in the remaining local taxonomy skeleton (`phl_licensetype`)~~ -
  **done 2026-09-21** from the full `SELECT DISTINCT licensetype` pull; all 50
  active types carry an explicit verdict. No taxonomy skeletons remain.
  (`nyc_dca` was retired rather than filled - see `DECISIONS.md`, 2026-09-21.)
  The check this item asked for paid off twice: New York needed four sources,
  and Philadelphia turned out to have **no source at all** for one bucket.
- [ ] **Close the residence blind spot in `check_personal_exposure.py`.** It
  detects a home only by an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at
  a detached house reads as clean - which is why Philadelphia scores 0.00%.
  **Tested both candidate signals against Philadelphia's property register on
  2026-09-21, and the results corrected this item** (see `DECISIONS.md`):
  - **Mailing address == premises does NOT work. Do not build it.** It matches
    41.9% of mapped pins, because a shop's mailing address is normally its own
    premises. No discriminating power at all.
  - **Parcel land use works, but only combined with owner-occupancy.** Joining
    `opa_account_num` to `opa_properties_public` succeeds on 94% of licences
    and is a real signal - but "residential parcel" alone flags 7.95% of pins,
    including **147 thirty-plus-seat restaurants on `APARTMENTS > 4 UNITS`
    parcels**. In a dense city, shops sit in residential buildings; land use
    alone would delete hundreds of real storefronts.
  - **The best signal was one not listed here: a homestead exemption**, which
    Philadelphia grants only on an owner's primary residence. Also over-fires
    alone (162 of its 189 hits are `MIXED USE`, the rowhouse-with-a-shop where
    the owner lives upstairs), so it needs pairing too.
  - **Usable rule: a person-like name AND an Individual entity AND (a purely
    residential parcel OR a homestead exemption)** - 33 pins, 0.39%. The
    corrected exposure for Philadelphia is ~0.2-0.5%, not the 0.00% the unit
    test reported.
  - **Done for Philadelphia 2026-09-21.** The parcel join is folded into the
    existing Carto query rather than being a separate download, step 2 removes
    the 8 pins that are a person-like name at a purely residential parcel, and
    `check_personal_exposure.py` reports the land-use and owner-occupancy
    signals. The homestead exemption is reported but **not** filtered on - it
    over-fires on mixed-use rowhouses.
  - **All six cities checked 2026-09-21. Three are settled; three are scoped
    work for the pre-deploy batch.** Per-city status:
    - [x] **Philadelphia** - parcel join built, 8 pins filtered.
    - [x] **New York** - measured via `bbl` -> PLUTO (`64uk-42ks`), a key join
      because DOHMH and DCWP both carry a BBL. **0.02%** (10 pins of 62,444 on
      a One & Two Family lot with a person-like name). **No filter needed**, and
      it confirmed that only 1 of the 161 surname-first DCWP names is on a
      residential lot.
    - [x] **Chicago** - nothing to do: `business_activity` marks home-based
      businesses and the taxonomy already drops all of them (zero reach the
      map). Verified, not assumed.
    - [ ] **San Diego - filter BUILT and applied 2026-09-21, but its number is
      a floor.** It removes 42 pins (0.37%), against San Francisco's 1.19% and
      Los Angeles' 2.05%, and the gap is a method artifact rather than a fact
      about the city. This city's coordinates sit systematically 5-15 m from
      their own parcel (exact point-in-parcel matched 1 of 30 sampled pins; a
      25 m buffer matched 30 of 30) because they are placed at the street
      frontage and SanGIS parcels exclude road right-of-way. So 2,227 of 2,454
      lookups fall back to the buffer, where the conservative "every parcel
      within 25 m" test quietly clears any home with a rental next door.
      **RESOLVED 2026-09-21 - and the bulk-download advice this item used to
      give is wrong; do not follow it.** Paginating the layer costs ~26 s per
      2,000-row page, because `orderByFields` sorts 664,662 rows and
      `resultOffset` deep-pages through them: about two hours, abandoned at
      2.7%. The working method is `pipeline/san_diego/fetch_parcels.py` -
      **one buffered query per point with `returnCentroid=true`** (this layer
      supports centroid-only responses), picking the nearest centroid locally.
      That gives true nearest semantics in 2,463 requests rather than ~5,000.
      - **Rate limit, measured:** SANDAG's gateway sustains roughly 2
        requests/second for a run this long. ~7 req/s completed once; slightly
        faster was refused after ~500. Defaults are now 1 worker at 0.4 s,
        about 20 minutes. A refusal aborts and writes nothing.
      Original Step 0 notes, all still valid:
      Better placed than expected: it has all three signals after all.
      - Layer: `https://geo.sandag.org/server/rest/services/Hosted/Parcels/
        FeatureServer/0` - **one countywide layer, 1,089,758 polygons**, so the
        geographically split `Parcels_South`/`_North`/`_East` siblings are not
        needed.
      - **`ownerocc`** is an owner-occupancy flag (`'Y'` on 472,498 parcels,
        null otherwise) - the occupancy signal this city was thought to lack.
      - Land use is `asr_landuse` (numeric) with **no coded-value domain**, so
        the codes were verified empirically rather than guessed:
        **`11` = single-family detached** (571,236 parcels, `nucleus_use_cd`
        110/111, `unitqty` 1, mostly `ownerocc='Y'`) and **`17` = condominium**
        (199,972, `nucleus_use_cd` 171). Use **11 only**; exclude 17 for the
        same reason as San Francisco's Multi-Family and New York's
        multi-family lots.
      - Also available: `apn`, `unitqty`, `situs_community`,
        `nucleus_use_cd` (225 types, more granular if ever needed).
      - The registry adds a fourth condition for free: `ownership_type='SOLE'`
        (24,974 rows), the same kind of structural signal as Philadelphia's
        `legalentitytype`. Requiring person-like name + SOLE + `asr_landuse=11`
        + `ownerocc='Y'` makes this the most conservative of the three filters.
      - Use the buffered-point approach from Los Angeles
        (`fetch_parcel_residence.py`): an exact point-in-parcel test misses
        pins whose coordinates sit on a street centreline.
    - [ ] **San Francisco - MEASURED 2026-09-21, and it is the real one: 217
      pins (1.19%) to remove.** A person-like name on a Single Family
      Residential parcel that claims a homeowner's exemption. Mostly home
      caterers and home beauty/nail/pet-care businesses (NAICS 722320, 812112,
      812910, 812199). **This is required pre-deploy work, not optional** - it
      is 27x Philadelphia's 8 pins and the largest exposure in the project.
      Method that works, so it need not be rediscovered:
      - Source: "Assessor Historical Secured Property Tax Rolls"
        (`wv5m-vpq2`, PDDL), `closed_roll_year = '2025'`, selecting
        `use_definition`, `number_of_units`, `homeowner_exemption_value` and
        **`the_geom`**.
      - **Use the domain `data.sf.gov`.** `data.sfgov.org` returns 403 on
        `/resource/` while `/api/views/` works, which makes the data look
        unavailable.
      - **Join spatially, not by address.** `the_geom` is a point, so a
        nearest-parcel join in EPSG:32610 with a 40 m tolerance matches 93.4%
        at a median 1.4 m. An address join reaches only 43.8%, because
        `property_location` is a fixed-width composite
        (`'0000 2801 LEAVENWORTH         ST0000'`) and because stripping
        direction words breaks "North Point" and "South Van Ness".
      - Exclude **Multi-Family Residential** from the residential set (5,733
        pins - ground-floor retail in residential buildings).
      - Do NOT use the Land Use layer `fdfd-xptc` - it is **[ARCHIVED]**.
    - [ ] **Los Angeles - MEASURED 2026-09-21 and the largest of the three:
      ~1,000-2,000 pins.** The earlier note here was wrong: the MapServer layer
      `public.gis.lacounty.gov/public/rest/services/LACounty_Cache/
      LACounty_Parcel/MapServer/0` **does** carry `UseType`, `UseDescription`,
      `Roll_HomeOwnersExemp`, `Units1` and `Bedrooms1` - 92 fields - so no
      second dataset is needed. Method:
      - Query point-in-parcel per pin with `returnGeometry=false`; a batched
        multipoint query returns polygons and is far too slow.
      - A 400-point sample put 7.2% of person-like pins on a Residential parcel
        with a homeowner's exemption (13.6% of the 53.2% that matched).
      - **Expect a ~47% non-match** and investigate it before filtering: the ~9%
        of LA coordinates recovered by Census geocoding sit on street
        centrelines, outside any parcel. Filtering only matched rows would be
        the same partial-coverage mistake San Francisco's address join nearly
        caused.
    - **Carry the mixed-use lesson into each.** New York's largest land-use
      category is Mixed Residential & Commercial at 20,257 pins, ahead of
      Commercial & Office. Counting mixed use as residential would delete a
      third of that map.
- [x] **Record each data source's licence and terms of use** - done
  2026-09-21 in `docs/data_sources.md`, covering all 8 registries, all 5 GTFS
  feeds, the boundary layers and the basemap. Permissive terms were NOT the
  default they were expected to be. What came out of it:
  - [ ] **Display the required notices before publishing.** Chicago, SFMTA and
    LA Metro each require specific text; OSM's is already satisfied. Exact
    wording is in that file under "Notices this project MUST display when
    published". Part of the same app job as surfacing the two doc pages, and
    it **blocks the public deploy** - publishing without them breaches terms
    this project has now read.
  - [x] **Store the transit licence texts locally** - done 2026-09-21. All six
    are in `docs/licenses/` with source URLs, retrieval dates and SHA-256 in
    that directory's `README.md`. The stated position (unaltered,
    non-commercial, for compliance) is in `DECISIONS.md`.
  - [ ] **DECIDE: does this project satisfy MTA's "You will not modify or
    delete any of the data"?** Found 2026-09-21 while storing the texts, and it
    **blocks the public deploy** because New York is already built. The terms at
    `mta.info/developers/terms-and-conditions` were never read - `data_sources.md`
    recorded the landing page's "Our data feeds are free to use" instead - and
    they are substantive. Three clauses to weigh:
    - **"You will not modify or delete any of the data."** Same shape as LA
      Metro's clause, which the owner decided 2026-09-21 this project does not
      breach because it draws `shapes.txt` geometry unaltered. The argument is
      *stronger* here: MTA's very next sentence says "You may, however, create
      an app that uses some but not all of the data", which is exactly the
      29-services-drawn-as-11-trunk-lines choice. Likely the same verdict, but
      it needs to be stated rather than assumed.
    - **"You will not state or imply that the data is accurate, complete, or
      timely."** Check the New York page's prose against this before deploying.
    - **"You will not state or imply in any manner that your app is licensed by
      MTA."** Satisfied by construction, but note it when writing the notice.
    Also confirm the non-MTA-server requirement, which this project satisfies
    trivially: `outputs/` is committed and the app never fetches from MTA.
  - [x] **NYC Open Data's reuse position** - resolved 2026-09-21 from the
    primary source. Local Law 11 of 2012 "requires that data sets must be
    available without registration requirement, license requirement, or usage
    restrictions", so the absent licence field is compliance rather than an
    omission. One condition attaches (identify source, version and
    modifications when republishing), which this project already satisfies in
    substance via `data_sources.md` and `excluded_categories.md`.
  - [x] **LA Metro's "modification" clause and CTA's purpose limitation** -
    both decided 2026-09-21 by the project owner; reasoning recorded in
    `docs/data_sources.md` and `DECISIONS.md`.
- [x] ~~**Find San Francisco's boundary-layer endpoint.**~~ **Found - it was
  recorded all along, and this item was stale.** `wamw-vt4s` is in
  `pipeline/san_francisco/config.py` with a full comment block and in
  `docs/data_sources.md` in three places, all added 2026-09-21. But re-checking
  it 2026-09-21 found the recorded command **does not work**, so San Francisco
  still could not be rebuilt - the item was closed by identifying the dataset,
  never by running the command end to end:
  - **`data.sfgov.org` now 301-redirects**, and the documented `curl -sG` has
    no `-L`. It writes a **654-byte HTML redirect stub** into
    `sf_county_boundary.geojson` and exits 0. The failure surfaces much later
    as a confusing geopandas parse error.
  - **Fixed 2026-09-21** to `data.sf.gov`, which returns 200 and reproduces the
    stored file byte-for-byte (38,822 bytes, sha256 `ecf625b5…`). Changed in
    `config.py` (`COUNTY_BOUNDARY_URL` and its comment) and in
    `docs/data_sources.md`.
  - **The general lesson, now true twice for this city:** use `data.sf.gov`,
    not `data.sfgov.org`. The assessor roll hits the same host with a different
    symptom (403 on `/resource/`, recorded in `docs/data_sources.md`). Treat it
    as one rule for San Francisco rather than two separate gotchas.
  - **Worth generalising:** an endpoint recorded but never re-run is not
    verified. Consider a smoke check that re-fetches every recorded endpoint
    and asserts a plausible content type, rather than trusting the rows.

## Before deploying

- [ ] **The narrow-width re-fit race is NOT fully fixed, and it is visible on
  the live site.** Seen 2026-09-22 on the deployed app at an 820px viewport
  (map container 778px): **Madrid** rendered showing Toledo to Guadalajara with
  all thirteen line labels collapsed into an unreadable clump, and **Chicago**
  rendered showing Madison, Milwaukee and Kalamazoo with its seven labels in
  one cluster. Both persisted more than ten seconds, through a scroll and a
  re-screenshot, so neither was a frame caught mid-layout.

  **It is intermittent and pre-existing, which is why it needs a check rather
  than a look.** On reload at the same width both measured their correct baked
  views - Madrid `zoom 11.25` at `40.4010,-3.6708`, Chicago `zoom 11` at
  `41.8711,-87.7554`, container `778x650` in both - and rendered correctly.
  Chicago is what rules out the 2026-09-22 label change as the cause: it was
  built long before, its `heatmap.html` is byte-identical to the version that
  passed the last full `deploy-verify`, and it fails the same way.

  This is the race already documented in `pipeline/map_common.py`'s `apply()`
  ("It is a RACE, so it is intermittent and not specific to a city"). The
  2026-09-21 fix added the `else if (HOME)` branch, which repairs the case
  where the map ends up at a narrow-width zoom **at full width**. What is still
  open is the narrow case: when the container is under 1000px the function
  re-fits `BOUNDS` every pass, and a pass that measures a transient width bakes
  a zoom that no later pass necessarily corrects - `apply()` returns early once
  the container width already equals its target, before it fits anything.

  **That mechanism is a hypothesis, not a measurement** - the reproduction was
  observed twice and did not reproduce on demand afterwards. Do not fix it from
  the hypothesis: instrument `apply()` to record each pass's measured width and
  resulting zoom, reproduce with that instrumentation, and only then change the
  branch. `HOME` is captured before the first `apply()`, so the correct zoom is
  in hand throughout and the repair is likely to be small.

  Anything changed here is baked into all eighteen `outputs/*/heatmap.html`, so
  it costs a re-render and re-commit of every city plus a full `deploy-verify`.
  Worth doing as its own change, not folded into a city build.

- [x] **Madrid and Barcelona are LIVE - rebooted and verified 2026-09-22.**
  They landed on master at `6dcb295`, the owner rebooted (not "Update": the
  push changed `app/cities.py` and `app/components.py`, both imported by
  `app/Overview.py`, and Streamlit Cloud leaves imported modules cached, which
  is what kept the site down for over three hours earlier the same day; the
  reboot requirement is the ninth entry on the deploy gate in
  `docs/data_sources.md`, which is a different numbering from the required
  notices).

  Confirmed on <https://expanded-heatmap-daceroberts.streamlit.app>, not
  locally: the region switcher now reads **Spain (2)** alongside Mexico (2),
  Canada and the three United States bands, and the macro map still opens on
  the United States. Madrid's page renders all thirteen line labels with the
  circular Línea 6 standing clear, Barcelona's all sixteen including both
  funiculars; both carry a full legend and the `© OpenStreetMap contributors`
  attribution.

- [ ] **Send the Barcelona notification AFTER the site is publicly reachable,
  not before.** Drafted in English and Catalan at
  `docs/notifications/barcelona-city-council.md`, unsent, with its two
  preconditions stated in the file. It is a courtesy notification to the
  Ajuntament de Barcelona about the `cens de locals` reuse, and the draft is
  written to be sent by the owner rather than by a session - sending anything
  on the owner's behalf needs their explicit go-ahead each time.

- [x] **Sweep every city page for "accurate, complete, or timely" claims** -
  DONE 2026-09-21. Two real hits, both on the New York page (the MTA city):
  it called its restaurant coverage "close to fully covered", and said Retail
  was "less complete ... than in the other cities", which implied the other
  eight WERE complete. Both reworded, and a note in that page's docstring
  says why. Everything else was clean: the only "accurate" left in a
  rendered map is a pharmacy called Accurate Pharmacy, and the remaining
  matches are code comments. A positive statement now appears site-wide via
  `components.render_site_notices()` - every map is "a snapshot of a public
  register as it stood on the retrieval date". Original item:
- [x] (reference) The rule this implements:
  **Two** transit licences now forbid it in nearly identical words - MTA's
  "You will not state or imply that the data you provide through your
  Application is accurate, complete, or timely" and WMATA §6's - so this is a
  cross-city prose rule, not a per-city footnote. New York and **Washington
  D.C.** are both built and affected today. Check the city pages, the Overview
  and the map legends, and prefer "as recorded by <agency> on <date>" phrasings over
  anything implying completeness. Both texts are in `docs/licenses/`.
- [x] **Agency branding - DECIDED 2026-09-21 by the owner: keep the official
  route colours AND the real line names, and state non-affiliation plainly.**
  What those clauses actually prohibit is stating or implying affiliation,
  sponsorship or endorsement, which `components._NON_AFFILIATION` now does
  head-on on every page; nothing in the project reproduces a logo, wordmark
  or route-bullet artwork, and for WMATA the colour IS the line's name. No
  re-render was needed. Original item:
- [x] (reference) **The branding question: official route colours, AND the
  line names beside them.** Now **six** of the nine built cities, since D.C.
  draws WMATA's six published `route_color` values - and WMATA's is the clause
  that names "confusingly similar variants", which also rules out the obvious
  workaround of shifting a colour slightly. Full detail and the clause wording per agency are
  in `docs/data_sources.md` (item 5c, and the table under the GTFS notes).
  Recorded here because it is a permission question, not implementation work,
  and it was previously visible only in the provenance doc.
  - **It affects five of the seven built cities**, not the two first assumed:
    San Diego (MTS), Los Angeles (LA Metro), Chicago (CTA), New York (MTA) and
    Philadelphia (SEPTA). San Francisco and Miami are out of scope - both
    already draw this project's own palette.
  - **Start with MTS, not MTA.** MTS's is the tightest wording in the project -
    its trademarks "may not be used in association with GTFS Data", a flat
    prohibition rather than an application process - while MTA's merely needs a
    free application. The first agency found is not the strictest.
  - **Two halves, and only one is cheap.** Colours are a free choice: each
    city's values live in one dict, and the project has already departed from an
    official palette twice on its own initiative (San Francisco throughout,
    Staten Island Railway for contrast). **Line names are not** - a standing
    invariant requires every drawn line to carry its real public name on the map
    and in the legend, so an answer covering names as well as colours is a
    materially harder change than a palette swap. Know that before asking.
  - Nothing in the project reproduces a logo, wordmark or route-bullet artwork,
    which is the part every one of these clauses most clearly covers.
- [ ] **Settle the three "what does silence mean?" licence questions** -
  still open with the publishers, but **no longer a deploy blocker as of
  2026-09-21.** The owner's decision was to disclose the gap on the site
  rather than wait on third parties: `components._UNSETTLED_TERMS` names
  Miami-Dade and Philadelphia in the footer of every page, says plainly
  that nothing found in either forbids what is displayed, and commits to
  removing a city **without waiting to be asked** if its publisher states
  a position that does not permit this use. That is a BROADER trigger than
  the standing commitment, which fires on a publisher asking, and the same
  wording is now in `docs/data_sources.md` and `docs/excluded_categories.md`
  so all three agree. What remains is the underlying enquiry:
  - [ ] Ask Miami-Dade County directly - it is the only one of the three
    with **no document to read**, so this cannot be resolved by reading.
  - [ ] SEPTA: whether line names and official colours count as trademarks
    being "used", and whether a portfolio site is "commercial or
    profit-making". Overlaps the branding decision, which the owner settled
    on 2026-09-21 by keeping both and stating non-affiliation.
  - [ ] The City of Philadelphia License's rights reservation.
  - **Miami-Dade is the weakest paperwork in the project and should go first.**
    Its business registry and boundary layer carry an `licenseInfo` that is
    purely an accuracy disclaimer, and its GTFS ships **no `feed_info.txt` at
    all** with no locatable developer terms. It is also the only one of the
    three where **no agency document exists to read**, so settling it likely
    means asking the County rather than reading anything - which makes it the
    longest lead time, not the smallest job.
  - **SEPTA's trademark clause** - whether line names and official colours
    count as trademarks being "used", and whether a portfolio site is
    "commercial or profit-making". Overlaps the branding item above.
  - **The "City of Philadelphia License"** reserves all database rights while
    granting nothing explicitly and requiring no notice. Same shape as the NYC
    question with the opposite paperwork: NYC is *forbidden* from imposing a
    licence, Philadelphia has imposed one that says only "we keep our rights".
  - **THAT CLAIM WAS TESTED ON 2026-09-21 AND IS NO LONGER TRUE OF ALL
    THREE.** It read: "nothing found in any of the three forbids what this
    project does ... questions about the absence of permission, not about a
    prohibition". Reading the documents settled two of the three and made the
    third worse than silence:
    - **SEPTA: RESOLVED, and it was never really a silence question.** Its
      licence expressly grants "a non-exclusive, non-assignable,
      non-transferable, limited and revocable right to **use, reproduce and
      redistribute** the datasets". The trademark sentence carves out
      "SEPTA's trademarks and copyrighted materials", not the data - and
      SEPTA's own Trademark Notice claims exactly one thing: "**The SEPTA Logo**
      is a registered trademark". Line names and route colours are not claimed
      anywhere in it, and this project reproduces no logo. The
      "informational and non-commercial purposes only" wording sits in the
      Copyright Notice's *Web Contents and Materials* section, governing
      documents and graphics from septa.org - the same site-footer-versus-
      dataset distinction NYC already taught. Nothing to ask anyone.
    - **Miami-Dade: RESOLVED by reading, not by asking**, which corrects this
      file's claim that "no agency document exists to read". One does:
      `opendata.miamidade.gov/pages/terms-of-use`, the Open Data Hub's own
      designated Terms of Use. Its entire substance is the accuracy
      disclaimer. Three documents now read - the dataset `licenseInfo`, that
      Terms of Use page, and the county-wide "Liability Disclaimer and User
      Agreement" - and **not one of them says anything about reuse,
      redistribution, modification or attribution.** That is a definitive
      absence of restriction from the County's own authoritative pages, which
      is a stronger position than an unexamined gap.
    - **Philadelphia: NOT resolved, and sharper than recorded.** See below.
  - [x] SEPTA - settled 2026-09-21, no action needed.
  - [x] Miami-Dade - settled 2026-09-21 by reading the County's own Terms of
    Use. No enquiry to the County is needed after all.
  - [ ] **Philadelphia - the one real question, and it is a PROHIBITION rather
    than a silence.** The dataset page says "Browsing City data on this site
    constitutes acceptance of the license, **the City's terms of use** and
    your agreement to be bound by them", which incorporates
    `phila.gov/terms-of-use` by reference. Those terms grant permission only
    "to residents and citizens of the City of Philadelphia to copy
    electronically and to print single pages from the Website ... exactly as
    presented ... without any addition or modification", and then state:
    "**Distribution or republication in any other form or for any other
    purpose, including any commercial purpose or use, and any modification
    whatsoever, are strictly prohibited without the prior written permission
    of the City.**" A separate sentence adds "Commercial use is prohibited
    without the prior written permission of the City."
    Read literally and applied to the datasets, that does not permit this
    project's Philadelphia map, which filters and redraws what it publishes.
    Read as what it appears to be - terms drafted for web pages ("print single
    pages", "exactly as presented on the Website"), sitting beside a
    dataset-specific licence that contains no such prohibition, under an Open
    Data Program established by executive order in 2012 whose purpose is
    public reuse, and beside a City boundary dataset marked "Usage: Public
    use; Free" - it does. **This project has NOT resolved it in its own
    favour.** **DECIDED 2026-09-21: ask for written permission, and keep the
    map live under a reasoned position while that is outstanding** - the
    dataset licence governs, the Terms of Use are web-page terms, and the
    footer discloses the question either way. See `DECISIONS.md` for the
    position and for what makes it a position rather than a conclusion.
    - [x] **Request SENT 2026-09-21** by the owner, to **`maps@phila.gov`**
      (the City's own Open Data Program contact) copying
      **`LIGISTEAM@phila.gov`** (the Business Licenses custodian). Text kept at
      `docs/notifications/philadelphia-permission-request.md`. An earlier
      draft addressed
      the custodian alone - the right address for the wrong desk, since a
      dataset maintainer cannot speak to what the City's terms cover.
    - [ ] **Follow up on 2026-09-28** (one week), at the owner's request. No
      reply as of 2026-09-21. If still silent: wait, chase once, or ring the Open
      Data Program. **Silence is not consent** - the interim position holds on
      the reasoned reading and the disclosure, not on the absence of an
      objection, and it does not strengthen with time. Sending it is the owner's to do. **Nothing in this project may
      claim a request is outstanding until it has actually been sent**, and
      silence must never harden into a claim that permission was given.
    - [ ] On a reply, follow the branch already written into that file: on
      permission the footer clause loses its only live subject and comes out
      entirely; on refusal Philadelphia comes off the site, and the remaining
      eastern cities' macro-map label offsets need re-checking at 854 and
      1200 px, because removing a marker moves `fit_view`'s bounds.
- [x] **Repo visibility - DECIDED 2026-09-21: it stays PUBLIC**, accepting a
  real but unlikely residual. Nothing found in any licence forbids what the
  project displays, the browsable code is much of a portfolio's value, and
  the standing commitment (a removal request is honoured, not argued) is
  the answer if a revocation ever comes. The reasoning against, kept
  because it is still true:
  Raised 2026-09-21 on survivability grounds, not compliance alone: four
  transit licences (WMATA §9, LA Metro, SEPTA, MassDOT) are revocable without
  notice and carry removal obligations, and **a public repo cannot be
  un-published** - forks and history survive deletion, so a revocation could
  not be complied with in good faith. Private keeps the deployed map as the
  only distribution surface, which is the "within your Application" scope each
  licence actually grants. **Verified it does not block deployment:** Streamlit
  Community Cloud supports private repos on the free tier, though it needs the
  broader `repo` OAuth scope plus a deploy key, and the one-private-app limit
  should be checked against "app from a private repo" specifically, since that
  likely means restricted *viewers* rather than a private source. **No middle
  path** - `outputs/` must stay committed, because the deployed app never runs
  the pipeline. Cost: the code stops being browsable, which matters for a
  portfolio piece. Interacts with the `outputs/`-in-git ceiling in
  `docs/scaling_thresholds.md`, since Git LFS quotas apply either way.
- [x] **Tile provider - DECIDED 2026-09-21: change nothing, and the research
  reversed the original recommendation.** Both policies were read rather
  than assumed:
  - **OSM raster** (the nine city maps) is keyless, has no stated volume
    cap, and explicitly permits "normal interactive viewing by a human".
    Its requirements are attribution (already in every map corner), a valid
    User-Agent and Referer - and the policy itself notes "modern browsers,
    with default settings, already satisfy these technical requirements".
    It forbids prefetch, bulk download and offline use, none of which this
    project does. Best-effort, no SLA, may be blocked without notice.
  - **Carto** (the macro map only) is the one with a wall: free to a fair
    use limit of **5 million tile requests a month**, and "all you need is
    an API key" - so a key is now expected, with non-commercial projects
    "usually just get a higher limit" and commercial use needing an
    Enterprise licence.
  So moving the city maps onto Carto - the earlier recommendation - would
  have moved nine maps from the keyless, quota-free service onto the metered
  one. Reversed. **Residual risk, accepted:** the macro map uses Carto's
  keyless CDN, which that policy no longer documents. If it is withdrawn the
  macro basemap goes blank while the markers, name pills, clicks and the
  text-link list all keep working. `pydeck` 0.9.3 does accept
  `api_keys={"carto": ...}` (env `CARTO_API_KEY`), so requesting the free
  key is a one-minute owner task if that degradation is ever unwelcome -
  it needs the owner's own account, so it is not something this project can
  do on their behalf.
  - [ ] Optional: request a free Carto API key and set `CARTO_API_KEY` in
    the Streamlit Cloud secrets.
- [x] **Streamlit Cloud main-file path - SETTLED 2026-09-21.** The entry
  point was `app/Overview_&_Introduction.py`; an `&` in a path that Cloud
  fixes permanently at app creation is a live hazard in URLs and shells, so
  it is now **`app/Overview.py`**. Renamed with `git mv` and every reference
  updated - `components.OVERVIEW_PAGE`, all eleven page docstrings,
  `pipeline/theme.py`, `scripts/scaffold_city.py` (it generates new pages,
  so it had to follow), `.claude/launch.json`, the deploy-verify agent,
  CLAUDE.md, README and project_context. `DECISIONS.md` and
  `docs/passover_opus5.md` keep the old name: they are history.
- [x] **Project name - DECIDED 2026-09-21: "Storefronts Near Transit".**
  The owner kept `expanded-heatmap` as the repository and directory name and
  took the new name as the site title only, so nothing about the checkout,
  the remote or any path changes. It lives in `components.SITE_NAME` and
  feeds the Overview title and every page's browser tab.
- [x] `README.md` - revised 2026-09-21: the new name, all nine cities, the
  snapshot-not-a-census caveat, the non-affiliation statement, and D.C.'s
  API key and ten-day feed window.
  - [x] **Code licence: MIT, added 2026-09-21** (`LICENSE`), with an
    explicit scope section stating what it does NOT cover. A bare MIT file
    at the repo root would have purported to license the 19 MB of
    third-party-derived content in `outputs/` - redrawn GTFS geometry and
    register-derived business records - which this project cannot
    sublicense: WMATA prohibits third-party redistribution and LA Metro
    forbids modifying its data. The carve-out points at
    `docs/data_sources.md` for terms and `docs/excluded_categories.md` for
    the modifications half that some of those terms require a re-publisher
    to state. The copyright line reads `dacekroberts`, the identity this
    project commits under - change it if a legal name is wanted.
  - [x] **Deployed URL - LIVE 2026-09-21:**
    <https://expanded-heatmap-daceroberts.streamlit.app>, in `README.md`.
    Note the subdomain carries the REPOSITORY name while the site is titled
    "Storefronts Near Transit". Unlike the main-file path, a Streamlit Cloud
    app's URL CAN be changed later from the app's settings, so this is
    reversible if the mismatch ever grates.

## Data quality follow-ups

- [x] Los Angeles map size: **3.5 MB** after the 2026-09-21 exclusions (was
  5.8), against 2.4 MB for San Francisco. Largely resolved; revisit only if a
  deploy shows it is still slow.
- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- [x] **Surface `docs/excluded_categories.md` AND `docs/data_sources.md` in
  the app - DONE 2026-09-21**, as `pages/10_About_the_Data.py` and
  `pages/11_What_Is_Excluded.py`, each rendering its document as committed
  rather than a hand-maintained web copy that would drift. Both are linked
  from the footer on every page, which is also where the required notices
  now render. Original item:
- [x] (reference) Surface both docs, together (a page each, or one "About the data" section, linked from
  every city page). Deliberately paired and deferred as one job (2026-09-21):
  both are external necessities for a live site rather than development work,
  both are already written to be published as-is, and surfacing the exclusions
  without the provenance would be half an answer. **Blocks the public deploy:**
  the legends were left broad, so "Retail - NAICS Code: 44/45" overstates what
  the maps contain until the exclusions page is reachable from them.
- [ ] **Carry into the mandatory `full` `deploy-verify` run before deploy:** the
  three fixes made after the 2026-09-21 scoped `map-chrome` run (legend
  breakpoint dead on a wide load, container ~15px short, fit bounds excluding
  label anchors) are verified by screenshot on four cities but not by an agent
  pass. Confirmed 2026-09-21 to batch them into that run rather than spend
  another scoped one - which is the batching the scope policy encourages.
- [x] **Phone-width city pages** - largely fixed 2026-09-21. The map keeps its
  fixed 1000px layout for initialisation (which is what dodges the Leaflet.heat
  `IndexSizeError`) and is resized to the frame immediately afterwards, then
  re-fitted to the station bounds. At 375px: New York went from 1 of 11 line
  labels visible to **9 of 11 fully visible, 0 off-screen**, Chicago from 0 of 7
  to 6 of 7, and the horizontal scroll inside the iframe is gone. Desktop is
  unchanged (11 of 11, original view). What remains:
  - [ ] **Label placement is still computed for a 1000x650 canvas**, so at phone
    width labels can crowd each other and the cluster badges, and one or two
    clip at an edge (New York: "Lexington Av (4/5/6)" right, "Staten Island
    Railway" left). Laying them out correctly for a phone needs a **second
    render at phone dimensions** - a per-city phone HTML plus viewport
    selection in the page. That roughly doubles `outputs/` and render time, so
    it is worth doing only if phone traffic matters. Not started. **Blocks the public deploy:** the legends were deliberately left
  broad (2026-09-21), so "Retail - NAICS Code: 44/45" overstates what the map
  now contains until this page is reachable from it.
- [ ] **Run `python scripts/check_personal_exposure.py` before publishing any
  city**, and after any change to a city's step 2 or taxonomy. It is a
  pre-publish gate in `CLAUDE.md` and `add-city` Step 7.

## Later / maybe

- [ ] **Cluster split/merge animation back, per city, by a lag threshold.**
  Turned off for every city on 2026-09-23 (`render_heatmap(animate_clusters=
  False)`); the owner asked for it to be recorded for re-implementation. The
  switch already exists per city. What is missing is the rule: the owner's
  suggestion is a measured ms threshold - e.g. animate only where a +/- click
  settles under some figure with the animation on. Toulouse settled in 588 ms
  with it and 299 without, Paris 647 and 366, so the threshold has to be
  chosen against a harness run, not guessed: `scripts/profile_zoom.mjs`
  produced those figures and runs any city (`button+1` is the case).

- [ ] Macro map at scale: with ~10+ cities, consider grouping nearby cities,
  and showing each city's mapped extent or a one-line summary in the tooltip.
  **Both halves were done on 2026-09-21.** The labels got per-city pixel
  `label_offset`s in `cities.py` (11 collisions to 0), and the markers were
  shrunk from radius 6 with a 2 px ring to radius 4 with a 1 px ring - outer
  diameter 16 px to 10 px - which separates New York/Boston and New York/D.C.
  outright and cuts the worst overlap, New York/Philadelphia, from 10 px to
  4 px. Radius 3 was tried and rejected as too faint.
  **What cannot be fixed, with the arithmetic so nobody retries it:** at the
  fitted zoom 1 px is about 21.7 km at New York's latitude, so displacing New
  York enough to clear Philadelphia would take **217 km** and put its dot west
  of Pittsburgh. The separations are also width-independent, because `fit_view`
  pins the zoom to a 320 px reference and spends extra width as margin. The
  residual touching is cosmetic only: the name pills are pickable, so clicking
  never depends on hitting a dot.
  - **Known issue, accepted rather than fixed:** scrolling the page with the
    cursor over the macro map zooms the MAP instead of scrolling the page, and
    that view then persists across reloads via the widget key. The fix is to
    lock the controller, which the owner declined on 2026-09-21 because
    non-US cities would then need continent-specific maps and extra pages.
  - Its label offsets are in PIXELS and the map zooms, so any new city in the
    eastern cluster needs its offset checked at 854 and 1200 px AND at a
    zoomed-in level - see `cities.py`'s docstring for the measurements.
  **`docs/scaling_thresholds.md` holds the full list of what breaks at what
  city count** (written 2026-09-21 at 7 cities): this macro map at ~10, the
  committed `outputs/` in git at ~20 — the real ceiling — and hosting at 40+.
  Two entries there are already settled: `drift_check.py` went incremental on
  2026-09-21, and page-number ordering was verified *not* to be a problem
  (Streamlit sorts the prefix numerically), so neither needs re-raising.

- [~] Non-US cities. **Canada is screened and ready to build - see
  `docs/canada_step0_endpoints.md` and the 2026-09-21 `DECISIONS.md` entry.**
  Six viable cities, Step 0 complete on all three legs, licences and privacy
  documented in `docs/licenses/`. Ranked by sites per in-city station:
  **Vancouver 861** (densest measured anywhere in this project), **Surrey 549**
  (a regional pair with Vancouver - it has no rail of its own), **Montreal
  252**, **Edmonton 153**, **Calgary 103**, **Toronto 41** (a two-bucket city,
  Boston's shape, weakest despite being largest). Decided already: Montreal at
  agglomeration scope; TransLink needs no prior contact. Build-time work that
  remains, per city rather than in general:
  - **Taxonomy modules.** Calgary 173 real categories, Surrey 210, Vancouver
    93, Edmonton 67, Toronto 72 - and **three of the six store several
    categories per row**, with a different delimiter each (Calgary `,\n`,
    Edmonton `;`, Surrey `\n`). Splitting is not optional and a multi-licence
    premises needs a dispatch rule, as Boston's `FT+RF` did.
  - **Montreal:** decide `SCIAN` (NAICS, 99.6%) versus the 10-value `USAGE1`.
    Keying off SCIAN may need **no new taxonomy module at all**.
  - **Vancouver: DONE, and the filter turned out to be empty.** The two-hop
    join works (99.9% point-in-parcel, 99.7% to a zoning class), but the
    conjunction it was built for - residential zoning AND a substituted
    personal name - leaves **1 row**, and that row is a false positive (a real
    corner grocery). The predicted ~232/0.78% was measured across all mappable
    rows rather than the storefront set. Zoning alone is NOT usable: the 146
    residentially-zoned storefronts are Vancouver's legal non-conforming corner
    shops and neighbourhood restaurants. Also: Vancouver DOES have a structural
    name signal, contrary to the brief - the registry parenthesises a sole
    proprietor's own name.
  - **Toronto:** geocode against the City's own 525,440-point address
    repository (71.4% on exact match, no normalisation) rather than any
    external geocoder.
  Beyond Canada, the EU/UK remain unscreened - NACE, and a national CRS such
  as EPSG:27700 for the UK.
- [x] ~~**Korea: register for a `data.go.kr` API key** (owner action).~~
  **CANCELLED 2026-09-22 - do not attempt this. It is not possible, and it is
  not needed.**
  - **Not possible:** every `data.go.kr` member type requires a Korean resident
    ID (내국인) or a Korean business number, and Seoul's 외국인회원 route is for
    foreigners *residing in* Korea. This is a **residency** wall, not a
    registration one, so the WMATA precedent does not apply. The old item read
    "Free" and "This is WMATA's gate, already cleared once" - both wrong. A
    **401 says the endpoint wants a key; it says nothing about who is allowed to
    hold one.**
  - **Not needed:** `data.seoul.go.kr` serves the same shape of data with **no
    account**, via the SHEET CSV export (`ssUserId=SAMPLE_VIEW` is the
    logged-out identity the page itself sends). **Eight datasets, 197,276 active
    premises, EPSG:5174 coordinates, `영업상태명` for active filtering, cp949,
    refreshed daily.** `infId`s and per-file measurements are in
    `docs/data_sources.md`; the download mechanism is in
    `docs/global_country_shortlist.md`.
  - **Licence differs from what this item claimed.** Not `제한 없음` but
    **공공누리 제1유형 (KOGL Type 1)**: attribution required - including a
    **hyperlink** where one is possible online - no implied endorsement, and a
    moral-rights clause meaning the per-station counts must be described as this
    project's derivation. One notice covers all of Seoul.
  - **Scope shrank: Seoul only, not six cities.** Korea licenses at the 자치구,
    so registers are published per district; Seoul aggregates and no other
    Korean city does. Busan has 4 of 16 districts and its national-portal
    download ids are stale behind a CAPTCHA rate limiter; Daegu's route works
    but 중구 - the downtown where all three metro lines converge - publishes no
    premises register at all.
  - [x] ~~**Korea has no line geometry yet.**~~ Resolved: dataset `15013203`
    (전국도시철도노선정보표준데이터) is the line standard dataset, alongside
    `15013205` for stations.
  - [ ] **Still open, and build work rather than screening:** a **partial**
    geocoding fallback for `OA-16094` 일반음식점 only - it is the one file below
    97% on coordinates, at **90.7%**, so ~11,000 active restaurants have a road
    address (99.2%) but no point. And a **Korean-aware pass in
    `scripts/check_personal_exposure.py`**: no file carries a proprietor-name
    column, but salon trade names routinely contain a personal name (`김은미장`)
    and ~30% of `사업장명` are a bare 2-4 hangul token.

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
