# Handoff - the Czech tram batch (2026-09-30)

For a FRESH session in `.claude/worktrees/czech-kit` (branch
`worktree-czech-kit`), doing for Czechia's six T1 cities what the France kit
session did for France's twenty. **Delete a section when its item is done.**

The owner asked for it on 2026-09-30, the day the France kit was approved.
Builds were approved for France that day; **for Czechia, bring the open calls
below to the owner, and wait for the go before building.**

## Read first

1. `CLAUDE.md`, then `docs/session_roles.md` (the build role, the heavy-job
   rule, explicit-path staging).
2. **The France kit as the model**: `.claude/skills/france-tram-city/SKILL.md`,
   `scripts/scaffold_france_batch.py`, and one French brief
   (`docs/build_briefs/brest.md`). DECISIONS "The France batch kit" and "The
   France batch's eight calls approved" record how it was done and what the
   owner approved. Copy the method, not the French facts.
3. **The six Czech briefs**, written by staging on 2026-09-30, each passing
   `brief_check.py`: `docs/build_briefs/brno.md`, `ostrava.md`, `plzen.md`,
   `olomouc.md`, `liberec.md` and `most.md`. DECISIONS "The six Czech tram
   cities briefed" has their calls.
4. **Prague, the built Czech city**: `pipeline/prague/`,
   `pipeline/countries/czechia.py`, `czechia_register.py`,
   `pipeline/taxonomies/czech_nace2025.py`, `docs/data_sources/czechia.md`.
   Czechia is Mexico's shape, like France: one national register chain
   (ROS02 establishments, RES activity, the RÚIAN address join).
5. `docs/tram_city_list.md`, the Czech T1 rows, and `docs/ring_rules.md`.

## 1. A `czech-tram-city` skill (the per-country-skill rule)

Written from Prague's build and the six briefs, on the France skill's plan:
- the ROS02 + RES + RÚIAN chain and its traps (active judged against the
  file's own `DATPLAT`, dedupe on `ICP`, the 6.6% with no `PKODADM`, never
  RŽP via ARES);
- `czechia_register.ruian()`'s per-city coordinate control;
- the tram leg: Brno from KORDIS's own CC BY 4.0 feed at `kordis-jmk.cz`
  (geometry from OSM, since the feed has no shapes), and the other five from
  OSM through `osm-rail`. Plzeň's PMDP feed is at most a stop-name
  cross-check;
- the scope call (Liberec with Jablonec; Most + Litvínov jointly, because
  Most alone fails the stub test);
- the halved rings (median gaps 294-514 m);
- UTM per city (Ostrava is 34N, not 33N);
- the notices;
- a page-text template, drafted in chat for the owner's approval, as
  France's was;
- a sheet per city.

## 2. A batch scaffold - only if it pays

France's twenty justified `scripts/scaffold_france_batch.py`. For six cities,
five of them on OSM rail, `scaffold_city.py` six times may be enough. Decide
on the measurement (how much per-city config is the same), and say which in
DECISIONS. If a script is written: `--dry-run` first, and a real run behind
`--go`.

## 3. The briefs - refresh, then bring the calls to the owner

The briefs exist; re-run `python scripts/brief_check.py brno ostrava plzen
olomouc liberec most`. **The open calls, from the briefs (recommendations
theirs):**
- **Line colours** for the five OSM cities: OSM tags none, so a chosen
  palette (Le Havre's and Riga's precedent).
- **Ostrava's line 5**: 3 of its 10 stops in the city. Recommended left out,
  which costs two stops.
- **Liberec's scope**: with Jablonec recommended; Liberec alone passes at
  67%.
- **Brno's H4 and P1** (heritage and event services, no weekday trips):
  recommended out.
- `mode` tram and `coverage` full for each, as the briefs propose.

## Standing rules (same as the France kit)

- **Feeds are fetched at build, never cached across weeks.** `brief_check.py`
  refetches a GTFS older than 7 days since 2026-09-30.
- **One heavy job machine-wide**, announced to the other live sessions first
  (a Czech step 2 reads the national ROS02 file). The France build session
  runs in `.claude/worktrees/france-kit`.
- **Push docs, skills and scripts only**, with the push ritual in `CLAUDE.md`
  (fetch, merge, push `HEAD:master`) and commit messages written through a
  file. **Builds go on a separate branch**, because landing `app/` is
  deploying; `app/` waits for review time.
- Log judgment calls in `DECISIONS.md`; bring owner calls in chat with a
  recommendation.
