# Handoff - the remaining tram cities' kit (2026-09-30)

For a FRESH session in `.claude/worktrees/tram-kit` (branch
`worktree-tram-kit`): the France kit session's role, for the T1 tram cities
that are neither French nor Czech. **HOLD ON BUILDS** (owner, 2026-09-30):
no scaffolding, no pipeline step, nothing in `app/`. Write the kit, bring the
owner's calls with recommendations, say when it is done, and wait for the go.
**Delete a section when its item is done.**

## The ten cities (`docs/tram_city_list.md`, T1)

| City | Country | Built there already | Brief (staging's) |
|---|---|---|---|
| Odense | Denmark | Copenhagen, Aarhus (CVR, DAR) | none |
| Daugavpils | Latvia | Riga (two layers, VZD) | none |
| Liepāja | Latvia | Riga | none |
| Kansas City | United States | many (NAICS) | none |
| New Orleans | United States | many | none |
| Tucson | United States | many | none |
| Florence | Italy | Milan, Rome | none |
| Zurich | **Switzerland: new country** (`add-country` first) | nothing | `zurich.md`, from 2026-09-23, before T1 (staging refreshes it) |
| Göteborg | Sweden | Stockholm | `goteborg.md`, before T1 (staging refreshes it) |
| Den Haag | Netherlands | Amsterdam, Rotterdam (BAG) | none |

**The briefs are STAGING's** (owner, 2026-09-30: staging is writing them,
as it is the Czech six). Do not write or edit them here. Read them as they
land on `origin/master`, run `python scripts/brief_check.py <slug>`, and
when the kit needs a brief changed or finished, ask staging
(`ListAgents`, then `SendMessage`).

## Read first

1. `CLAUDE.md` and `docs/session_roles.md`.
2. **The France kit as the model of the role**:
   `.claude/skills/france-tram-city/SKILL.md`,
   `scripts/scaffold_france_batch.py`, `docs/build_briefs/brest.md`, and
   DECISIONS "The France batch kit" and "The France batch's eight calls
   approved". Copy the method: a skill written from what is built, live reads
   of every source, briefs whose checks pass, and calls put to the owner with
   a recommendation.
3. `docs/tram_city_list.md` (the ten rows, "Data currency", "The light-rail
   test") and `docs/ring_rules.md`.
4. The macro map's two keys (`mode`, `coverage`): the add-city skill on
   `origin/macro-legend` (or on master once it lands), and
   `docs/category_rules.md` for any category kept or dropped.

## 1. A `tram-city` skill - what every trams-only city shares

France and Czechia each get a country skill. These ten are one or two per
country, so write one cross-country skill instead. The per-country detail
goes in each brief, pointing at the country's built city (and `japan-city`,
`taiwan-city` and `brazil-city` stay the model for where a country skill
belongs).

What it should carry:
- the owner's trams-only calls (DECISIONS "Yes to trams-only maps");
- rings by the spacing rule (0.3 mi outer at about 550 m or less; Kansas
  City's ~560 m is measured at build);
- no stop thinning, except the street-stop filter where stops are
  one or two blocks apart (New Orleans, 161 m:
  `docs/sub_transit_line_filters.md`, Philadelphia's and San Francisco's);
- the light-rail test (`docs/tram_city_list.md`);
- rolling feeds, fetched at build and never cached across weeks;
- OSM rail through `osm-rail` where a feed is unlicensed or unreachable;
- the currency rule (the data date on the page: Kansas City, Göteborg);
- one-bucket and narrowed pages (`coverage`);
- a trams-only page-text template, drafted in chat for the owner's approval
  as France's was (`france-tram-city` section 6 is the model; the controls
  paragraph and heat caveat stay as on the built pages).

## 2. A scaffold script - only if it pays

Ten cities in seven countries have little shared config. `scaffold_city.py`
per city is probably enough. Decide on the measurement and record it in
DECISIONS.

## 3. The briefs - staging's; this session's part

Staging writes the ten briefs. This session:
- reads each brief as it lands and checks it against the skill;
- makes sure it states the proposed `mode` and `coverage` and the owner's
  calls with a recommendation, and asks staging for anything missing;
- collects the calls across the ten, so the owner can approve them in
  one sitting, as France's eight were approved.

What the briefs still have to settle, from `docs/tram_city_list.md`
(staging's to do, listed here so the skill covers them):
- **Kansas City**: RideKC's GTFS terms (unread); data frozen 2026-01-15,
  so the page gives the date (owner); `dba_name` is often a person.
- **New Orleans**: RTA's GTFS (unread); `ownername` goes through
  `check_personal_exposure.py`; the street-stop filter.
- **Tucson**: BUSLIC's "as is" terms; about 6,250 licences are
  individuals'.
- **Florence**: the Comune's four layers (a full read); GEST's GTFS.
- **Daugavpils and Liepāja**: VZD's `aw_eka.csv` (a new source row); rail
  from OSM.
- **Odense**: placement through DAR (owner, 2026-09-27).
- **Zurich**: `add-country` for Switzerland (LV95 `EPSG:2056`), and
  partial retail from alcohol-licensed shops (owner).
- **Göteborg**: the CSV, never the rowstore JSON; undated rows (owner).
- **Den Haag**: Amsterdam's precedent for the horeca layer (owner); never
  fetch `AANVRAGER`, `KVKNUMMER` or `RECHTSVORM`; RandstadRail E and the
  `mode`.

## Standing rules (as the France kit)

- **Hold on builds.** When the kit is done, say so and wait for the go.
- Feeds are rolling: fetch at build, never cache across weeks.
- **One heavy job machine-wide**, announced to the other live sessions first.
  The France builds run in `.claude/worktrees/france-kit`; the Czech kit is in
  `.claude/worktrees/czech-kit`.
- **Push docs, skills and scripts only**, with the push ritual in `CLAUDE.md`
  and commit messages written through a file.
- Log judgment calls in `DECISIONS.md`; bring owner calls in chat with a
  recommendation. Probe output goes to the session scratchpad.
