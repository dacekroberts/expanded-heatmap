---
name: regional-extension
description: Extend a BUILT city's map to the neighboring municipalities its lines already reach - the city alone proved at zero drift first, a REGIONAL switch, one register cut by municipality codes or one more publisher per municipality, the "(Regional)" rename on the same page, license rows and notices per added publisher, the single-station and too-few-stations calls, the add-ons that go to Band R, and the gates, deploy-verify scope and downstream note an extension owes. Use for every row in the master list's add-ons section (Mexico City + four municipios, the Korean four, the Greater Copenhagen Light Rail if the owner makes it an extension). Not for a first build of a city, even a multi-municipality one such as Seattle (Regional) or Liverpool (Regional) (that is add-city, with multi-source-city), and not for screening a city that has never been probed (add-city Step 0, screen-wave).
---

# Extending a built city to its neighbors

Drafted by the staging session from the repository record on 2026-10-04.
Distilled from the four extensions that landed on 2026-10-03 (Belo Horizonte +
Contagem, Rio + Duque de Caxias, Los Angeles + Long Beach, Vancouver (Regional)
+ Burnaby, New Westminster and Coquitlam), their deleted kit (`git show
4c59cb02:docs/handoff_extensions_2026-10-02.md`), and the regional pages built
whole (Miami, Monterrey, Seattle, Brussels). Read with `add-city`,
`multi-source-city` and `publish-city`, which this does not replace. Rules
marked *(inference)* are not stated in the record in so many words.

**Why it is its own job.** "A station in another city is a new project,
because it needs that city's own business data sourced and verified
separately" (the standing rule, as Miami's entry put it: `docs/decisions/2026-09-20.md`,
"Miami built, as the project's first REGIONAL city"). An extension also
changes a LIVE page, so the drift baseline moves on purpose and the work
lands only at review time (the kit, "These change LIVE pages").

## Step 0 - Is it an extension at all?

Answer these before any code. Each has a precedent; a departure goes to the
owner with the precedent it breaks.

1. **Its stations are on lines the built map already draws.** Berkeley was
   discarded because "San Francisco's map draws Muni only, so BART is no built
   map's satellite" (`docs/city_master_list.md:525`). Mexico City's extension
   keeps "the page's own lines"; the Tren Suburbano, El Insurgente and
   Mexicable stay out (`city_master_list.md:251`).
2. **The add-on must not give the page a bucket at a few stations only.**
   Vaughan: "Not a Toronto add-on either: it would give Toronto a retail
   bucket at two stations only" (`city_master_list.md:489`).
3. **One station is enough for an add-on, never for a page.** Uiwang's one
   station is "a potential Anyang (Regional) add-on" (`city_master_list.md:674`);
   Naucalpan's one "follows Anyang + Uiwang" (`docs/decisions_drafts/staging.md`,
   "Mexico City (Regional) marked"). As standalone pages the same counts are
   discards: Longueuil ("one métro station is not a map", line 487),
   Putrajaya, Antipolo (Uiwang's precedent, lines 705, 718), Brossard and
   Berkeley at three (lines 488, 525). Station counts alone are no precedent:
   Takarazuka was built on 11 (line 357).
4. **The added publisher's terms must be ones the project accepts.** Richmond
   (BC) went to Band R on site terms of "research purposes and private use
   only" (line 198); Arlington followed as D.C.'s add-on, "like richmond", on
   "non commercial, personal use only" (line 199; `docs/decisions/2026-09-27.md`,
   "Arlington left out of Washington D.C."). An R add-on is left out and the
   built page ships without it (Vancouver extended without Richmond). Its way
   through is a written question, the owner's to send; nothing is drafted
   (outreach is the last resort).
5. **Extension or a page of its own: the owner's call.** Gimhae became its own
   page because "a Busan regional map would change a live page"
   (`staging.md`, the 2026-10-03 Belgium-and-Korea entry); Yangsan and
   Gyeongsan sit in Band C as "a page of its own, or Busan (Regional)"
   (`city_master_list.md:139-140`). Brussels kept the commune on page 196 and
   built Brussels (Regional) as page 201 with its own pipeline, saying which
   storefronts neither page's rings count (`DECISIONS.md`, "Brussels
   (Regional) built"). Recommend, with the tradeoff; wait for a yes.

## Step 1 - The city alone, at zero drift, first

**The built city must prove zero drift before any extension** (owner,
2026-10-04, from Mexico City's probe: `staging.md`, "Mexico City (Regional)
marked", call 1; `city_master_list.md:249` for the Korean four, "as the
2026-10-03 extensions did"). Mexico City's probe found eight Metro stations
dropped and two kept twice; the repair landed first (`DECISIONS.md`, "Mexico
City's station repair landed").

- **Add a `REGIONAL` switch to `pipeline/<slug>/config.py`, commit it OFF, and
  run the drift check.** False must reproduce the city-alone build byte for
  byte (`pipeline/belo_horizonte/config.py:13-18`,
  `pipeline/los_angeles/config.py:13-21`). Belo Horizonte's off commit was
  8ca5d522, Los Angeles' b27d6ad7.
- **A city with no `baseline.json` figures gets a first baseline first**, with
  `--update-baseline`, outputs unchanged (Vancouver: `2026-09-27.md`,
  "Vancouver (Regional) extended").
- **The drift check is a heavy job**: `scripts/heavy_job.py run ...`, `--jobs 3`
  at most. The extensions measured 0.31 to 0.44 GB per city.
- **Regional processed files go to `data/<slug>/processed/regional/`** from the
  first run (`DATA_PROCESSED` in both configs above). `data/` is one junction
  shared by every worktree; Belo Horizonte's first scope-on run wrote into
  `processed/` and failed `check_macro_facts` for every session until it was
  restored (`2026-09-27.md`, "Belo Horizonte (Regional)"). Fold back on landing.

## Step 2 - One register cut by code, or one publisher per municipality

Two shapes, and the record treats them very differently:

| Shape | Precedents | What it costs |
|---|---|---|
| **One register, cut to the added municipalities by official code** | Monterrey's `MUNICIPIOS` / `MUNIDS` (`pipeline/monterrey/config.py:88-102`); Belo Horizonte's `SCOPE_CODES` (IBGE); Copenhagen's `KOMMUNER` (`pipeline/copenhagen/config.py:59`); Anyang on `korea_sbiz`'s `sigungu_codes` | No new license row or notice: "CNEFE and OSM are the city's own, so no licence row and no notice" (Belo Horizonte). A brief claim for the new file (`contagem-cnefe-file-live`) |
| **A new publisher per municipality** | Vancouver + Surrey, then Burnaby, New Westminster, Coquitlam; Los Angeles + Long Beach; Seattle's five sources | A license read, a row, usually a notice, a taxonomy branch and a privacy pass per publisher (`multi-source-city`) |

- **Key on codes, never names.** Monterrey's names exist only to be ASSERTED
  against the register's own column, so a wrong code fails loudly. Gwangju's
  2026 merger is why `korea_sbiz` now cuts by 시군구코드 (`DECISIONS.md`,
  "korea_sbiz: a 시군구코드 filter"). Check the codes at build.
- **Disjoint publishers need no cross-source dedup**; record that, since a
  missing dedup step looks like a forgotten one (`2026-09-20.md`, "Vancouver
  is built at REGIONAL scope"). Dedup stays per source.
- **The taxonomy dispatches on `source`**; the built city's rows must classify
  exactly as before (`TAXONOMY_SYSTEM = "los_angeles" if REGIONAL else "naics"`,
  `pipeline/los_angeles/config.py:172`). Give every new category value a
  verdict from `docs/category_rules.md`, each with its reason.
- **A municipality whose sources fall short is disclosed, not padded.**
  Seattle's places with no published register carry county food only, said
  in its own section and in `docs/map_inconsistencies.md` ("Personal services
  thin").
- **Widen the sanity box, not the fetch box, when only the polygon grows**
  (Belo Horizonte: Contagem reaches -44.162).
- **A download is pre-permitted only once a brief names it.** Entidad 15's
  two DENUE ZIPs wait "until a brief names it" (owner, `staging.md`).

## Step 3 - Licenses, notices and personal data, per added publisher

- **One `licence-read` agent per new source**, before the build reads it.
  Record the registry row and license row in `docs/data_sources/<country>.md`
  under the city's new name (Long Beach: `docs/data_sources/united-states.md:19,243`).
- **Claim notice numbers** in `docs/session_roles.md`'s numbers sentence before
  writing one (the extensions held 129-136 and released 133-136 unused). A
  notice "displayed by choice" carries a no-endorsement sentence where the
  terms bar implied endorsement (Long Beach's 129, Seattle's 113).
- **Carry affirmative obligations forward** (`read-licence` step 6c;
  `publish-city`, "What must be recorded"). Long Beach's breach-only
  indemnity needed the owner's acceptance before the build (the kit).
- **Never fetch a new publisher's personal fields.** Long Beach's `FULLNAME`
  and Burnaby's, New Westminster's and Coquitlam's name, mailing, phone and
  e-mail fields were never requested, and both fetch and step 2 raise if one
  arrives. A row with no trade name shows its street address or business
  type, never a person's name.
- **Re-run `scripts/check_personal_exposure.py <slug>` on the extended city**
  and record the verdict (drafts file, then `docs/privacy_verdicts.md`). The
  OGL variants' personal-information exemption was read cautiously and
  recorded, with no pin removed (`2026-09-27.md`, "the OGL
  personal-information exemption read cautiously").

## Step 4 - Switch it on and account for every change

Run steps 1-3 of the pipeline with `REGIONAL = True`, then the drift check.
**Confirm every change it reports is the extension's**, then re-record the
baseline deliberately (the kit, "For each extension", step 4). Record what
moved: stations kept and excluded, storefronts per source and bucket, in-ring
count and share, scope area. Belo Horizonte's share fell 18.4% to 16.0%, so
its page's "one in six" changed with it.

- **Stations in the added municipalities move from `excluded_stations.csv` to
  kept;** the rest stay listed with their municipality (property E of
  `scripts/check_scope_disclosure.py` reads the file's shape through
  `app/station_scope.py`).
- `python scripts/check_ring_shares.py --write` touches only this city's row.

## Step 5 - The page stays; the name gains "(Regional)"

- **Same page file, same slug; only the display name changes.** "Belo
  Horizonte becomes 'Belo Horizonte (Regional)'; the page file and slug stay"
  (`2026-09-27.md`). The slug is derived from the page path
  (`app/station_scope.py`, `slug()`), and renaming a page that a cached module
  names breaks every page until the reboot (`publish-city`). The extensions
  took no new pages. A city already "(Regional)" keeps its name (Vancouver).
- **Why the label:** "a map spanning six municipalities cannot honestly be
  called Miami" (`2026-09-20.md`); `app/cities.py:304-307` carries Vancouver's
  version. Copenhagen covers Frederiksberg unlabeled, a listed inconsistency
  (`docs/map_inconsistencies.md`, theme 5).
- **In `app/cities.py`:** `name`, then `blurb`, `data_age` (Long Beach's fetch
  date), `placement` (New Westminster's address join) and any summary field
  the new sources change; `record_kind` stays the majority source's. The
  pipeline config's `NAME` follows the switch. `render_city_nav` and
  `render_city_title` on the page take the new name (`check_deploy_imports`).
- **Re-score the macro label**: "(Regional)" widens the pill. Measure it in a
  real browser, then `scripts/check_macro_labels.py` at 375, 768 and 1200;
  a clip no side avoids is flagged for the owner (Los Angeles, 43% at 375 px).
- **Page text in the format of `docs/city_page_format.md`**, not the text being
  replaced. A new sentence no template covers is a proposal in the drafts file.
- **What Is Excluded:** the city's `### <Name> (Regional) - ...` section names
  the new municipality, its exclusions with counts, what is missing, what is
  shown but not named, and a **Stations.** line ("The A Line's eight stations
  in Long Beach are drawn and ringed": `docs/excluded_categories.md:218-236`).
  *(inference)* Rename the city's existing headings to the new name, since
  `app/country_sections.py` files a section by the name as `app/cities.py`
  gives it.
- **Also:** `docs/map_inconsistencies.md` (the city's rows, and theme 5's
  "Labelled (Regional)" list), `app/macro_facts.json`, `docs/ring_rules.md`,
  README, the master list's Built row (the add-on leaves the add-ons section),
  `docs/project_context.md` (no counts).

## Step 6 - Gates, review time, downstream

The kit's order, per city: personal exposure and its verdict row; provenance
(`check_provenance.py` names the city OK; every new URL constant verbatim in
the docs, every new notice in bijection with `_NOTICES`); scope disclosure;
inconsistency rows and `cities.py` fields; the master list; macro facts and
label; the drafts entry; commit; the drift check with the deliberate baseline
update; merge master, `check_all.py`, push at 0 behind. **Never to master
before the owner's review time.**

- **Reboot: yes.** `app/cities.py` changes with every extension (`publish-city`).
- **deploy-verify:** at review time, once for the batch. *(inference)* Scope
  `city-added`, naming the extended cities: one city's output and the code
  that produced it changed, which is `publish-city`'s case for a narrow scope.
- **Downstream:** an extension always counts (`outputs/<city>/`, the registry,
  notices, macro facts, ring shares: `docs/session_roles.md`, "Downstream
  sessions"). The drafts file names the inputs changed and, per new notice,
  card face or caption only, plus any open terms question. Cleanup sends the
  note once per review time.

## The queue, 2026-10-04

| Extension | Shape | Still needs |
|---|---|---|
| **Mexico City (Regional)** + Ecatepec (Línea B, 5), Nezahualcóyotl (B, 3), La Paz (A, 2), Naucalpan (Línea 2's Cuatro Caminos, 1) | One register: DENUE over entidades 09 and 15, cut by `MUNIDS` | Marked, not scheduled. The station repair landed (`DECISIONS.md`, 2026-10-04); a zero-drift run of the city alone on it. A brief naming entidad 15's two ZIPs (50.6 and 30.2 MB) before the download; the country module assumes one ZIP per entidad. Codes checked at build. Ecatepec's ring share will be low. No new license row expected *(inference, Belo Horizonte's precedent)* |
| **Anyang (Regional)** + Gunpo (6) and Uiwang (1) | One register: SEMAS, a longer `sigungu_codes` list | Marked, not scheduled. The code filter landed. `korea-city`, `cjk-text` |
| **Seoul (Regional)** + Gwacheon (5), Gwangmyeong (2), Hanam (4), Guri (4) | Two sources: LOCALDATA and SEMAS (Long Beach's shape) | Marked, not scheduled. `multi-source-city`, `korea-city`; SEMAS's notice 68 reaches the page *(inference, check N)* |
| **Busan (Regional)** + Yangsan (5); **Daegu (Regional)** + Gyeongsan (5) | Two sources, as Seoul | The owner's call first: a page of its own or the extension (Band C until chosen) |
| **Greater Copenhagen Light Rail** (about 10 municipalities, Lyngby-Taarbæk to Ishøj) | One register: CVR and DAR by kommune code | Unscreened; first in the held queue (`city_master_list.md:361`). Frequency and the page's shape are open; Copenhagen's map does not draw the Letbane today (`docs/commuter_rail_list.md:18`). Screen first, then Step 0 above |

Off the queue: Arlington (VA) and Richmond (BC), Band R.
