# GTBA | Place search - retrospective (2026-10-16)

Written 2026-10-16 from the record; committed 2026-10-17 on the owner's word. It
covers place search, the in-map box that finds streets, intersections,
stations, lines, neighborhoods and landmarks from an OpenStreetMap index. It
runs from the Kyoto pilot (2026-10-07, b2e4a8a4) through the rollout to all
237 maps (landed 2026-10-13, 3e16745d), the post-landing batch (559bf919,
2026-10-16) and the final browser check the same day. The detail behind each
figure is in `DECISIONS.md` (2026-10-11 to 2026-10-16) and
`docs/decisions/2026-10-04.md` (2026-10-07 and 08), cited by entry title. The
rules themselves are in `docs/place_search_exclusions.md` and the
`place-search-city`, `place-street-lines` and `osm-extract` skills. A first
draft written on landing night (`data/_search_rollout/notes_drafts/retrospective.md`)
was the starting point; its figures were re-checked against the log, not
copied.

## The short answer

**It worked, and it reached every map six days after the pilot.** The final check opened
all 237 maps and found every drawn station and line by its own name: 13,010
stations and 1,275 lines, with six ranking warnings on phones (DECISIONS
2026-10-16, "The project closed to maintenance"). The search runs in the
reader's browser over a static per-city file, so no typed text reaches a
server, a log or a URL ("Four ideas assessed", 2026-10-07).

**It cost more in owner rulings and rule churn than in code.** On 2026-10-13
alone, 242 commits name search or place in their subject (a `git log` grep,
which also catches a few unrelated commits). That day saw at least six
numbered rule passes plus the station and landmark fixes of `search-rules-8`
(`docs/place_search_exclusions.md`, section headings). Each pass meant
rebuilding every built index. The landing night ended with usage exhausted
and every follow-up held to 2026-10-18 ("the rollout lands on every map in
one push", 2026-10-13).

**Two things mattered most:**

- **The extract route replaced Overpass for bulk fetches.** The night run on
  regional extracts fetched 154 cities and built 151 in 2.3 hours with no
  Overpass request (`data/_search_rollout/extract_2026-10-13.md`). The
  Overpass run before it fetched 0 cities in 1.3 hours
  (`night_2026-10-13.md`).
- **Eye reads found what the rules missed, and the misses were classes.**
  Readers dropped 1.7% of the 137,106 station, landmark and place rows they
  read in 146 cities ("the extract run's full reads", 2026-10-13). Most drops
  pointed at a rule fault, which then cost another pass over every city.

## Timeline

| Date | Step | Source |
|---|---|---|
| 10-07 | Four ideas assessed; place search judged viable, browser-only | "Four ideas assessed" |
| 10-07 | Kyoto pilot: 11,836 places, 1.04 MB index (270 KB gzipped); 47 of 50 test queries found first or second | "Place search piloted on Kyoto" |
| 10-07 | Stations and lines read from the map itself; index URL hashed; languages measured, never written | three entries of 10-07 |
| 10-08 | Sample of one city per region begins: Seattle, Chicago, Vancouver, Sydney; owner's iPhone test passes on Seattle | "sample, first batch" |
| 10-08 | Intersections moved to a second file: Seattle's first open 563 KB to 227 KB gzipped | same entry |
| 10-08 | Batches 2a (five Latin-script cities) and 2b (four, three new scripts) | 2a and 2b entries |
| 10-09, 10 | No search commits | `git log` |
| 10-11 | Batch 3, the size tests; São Paulo largest at 1,229 KB gzipped; phone test passes | "Batch 3, the size tests" |
| 10-11 | `place-search-city` skill, `place-read` agent and index drift check built | same entry |
| 10-12 | The 19 searched cities land with phase 2; the deployed box never loaded its index until a street was typed live | "never loaded its index" |
| 10-12 | Scope rule and outline; wave 1 scaffolded (34 cities); one-query-per-mirror pilot carries 0 of 4 | "defined area"; "wave 1: the scaffold" |
| 10-13 | Extract route proved and landed; street lines landed (4d7cf5f9) | extract entries; "rulings on keep against drop" |
| 10-13 | Outside-model pilot fails its trust line; full reads run instead | "the outside model fails" |
| 10-13 | Four slices land in one push: 20 + 34 + 32 + 151 maps; 183 maps rendered twice | "lands on every map in one push" |
| 10-16 | Post-landing batch, 15 calls approved at once; all 237 maps re-rendered | "post-landing batch"; 559bf919 |
| 10-16 | `check_map_search.js` over 237 maps: 13,010 stations, 1,275 lines found | "closed to maintenance" |

Commit times are local and measure cadence, not effort. Lanes ran in
parallel, so one hour of the log can hold several sessions' work.

## What was built

The search is one shared script and one shared index builder; a city adds a
config block and a two-line step. The pieces, as they stand on master:

- **The index builder**, `pipeline/place_index.py` (6,681 lines today). It
  turns three OpenStreetMap caches into an index, an intersections file, a
  street lines file, a summary and an id side file for the travel app.
- **The browser script**, `_PLACE_SEARCH_TEMPLATE` in
  `pipeline/map_common.py` (lines 2275 to 3452, about 1,180 lines). Own
  matching code, chosen because whitespace tokenizers cannot find 烏丸 inside
  四条烏丸 (Kyoto pilot entry).
- **Two fetch routes.** `place_index_fetch.py` asks Overpass;
  `osm_extract.py` (2,154 lines) and `place_extract_fetch.py` (987 lines)
  answer the same queries from Geofabrik extracts on this machine.
- **The checks.** `check_place_search.py` (rules lettered A to J),
  `check_place_scope.py` (with rule D, e5345211), `check_place_index_drift.py`,
  `check_place_unopened.py` and the browser script `check_map_search.js`.
- **The record.** Three skills (730, 167 and 325 lines), the `place-read`
  agent, `docs/place_search_exclusions.md` (312 lines) and an internal watch
  file of stations OpenStreetMap marks as not yet open.

**The files are smaller than projected.** On 2026-10-12 the site-wide size
was projected at roughly 475 MB by extrapolation from 19 cities ("the cheap
path", 2026-10-12). Measured for this draft (`du -sb`, 2026-10-16), all of
`app/static/places/` is 227.7 MB, street lines and intersections included.
Why the projection was high is not recorded.

## What went well, and why

**Privacy was designed in, not repaired.** The box has no form, sends no
credentials or referrer, and turns off cloud spellcheck (Kyoto pilot entry).
Homes were held out by rule from the first batch, and graves and plaques to
private people from 2026-10-13. Named private people found by readers were dropped by id,
each id checked against its cached name.

**Measuring on a phone settled the size question cheaply.** Batch 1 put
iPhone memory and repository size to the owner as top-line risks (10-08).
The lossless file split was built at once. The largest index, São Paulo's,
then passed the owner's phone test on 10-11, so the reserve cut to side-street
intersections was never needed.

**The extract route turned an outage into a non-event.** It matched Overpass
element for element on Tbilisi. On Seattle, Brussels and Kyoto it differed
only by five boundary ways and a few edits made after the Overpass date
("Place search from regional extracts", 2026-10-13). No
element Overpass returned was missing. Its proof stated what it did not show,
including that no multi-region read was compared with an Overpass answer.

**Offline rebuilds made rule passes cheap per run.** Every index rebuilds
from caches on disk, so a rule change cost minutes of machine time, not a
refetch. The drift check (built 10-11) rebuilt 14 cities in 78 s and caught
any index left on old rules.

**The outside model was tested before it was trusted.** The trust line, one
miss in twenty of a full read's drops, was agreed first (2026-10-13, "16
known works kept by id"). Scored on five full reads, the model caught 67% of
drops and was right on 21% of its flags. So it failed, and the cost of
finding that out was about 22 dollars ("the outside model fails").

**Model tiers were chosen by measured recall.** On three cities' known drops,
a Sonnet-tier reader found 43 of 77 dropped ids and a Haiku-tier reader 32
("the top model reads places and landmarks", 2026-10-13). So the top model
kept the place and landmark rows, and Sonnet took the street screen.

## What went wrong or was expensive

**Rules were found by reading, so they changed after cities were built.**
Each batch's eye reads turned up a new class: homes on heritage registers,
bare type words, denomination-only church names, museum exhibits. Each became
a rule, and each rule changed every built index. The protocol held (measure
on every built city, report every changed row), but it multiplied work as
cities grew from 19 to 237.

**Re-renders repeated.** On 2026-10-11 the 19 searched maps were re-rendered
at least seven times, once per phone-check refinement (seven entries of that
date). At the landing, 183 maps were rendered a second time. They had been
rendered before another branch's search-script change reached them ("lands
on every map in one push"). Render-once held per branch, not across branches.

**The live site failed in a way no local test could see.** From the phase 2
landing until the owner typed a London street, the deployed box answered
with stations and lines only ("never loaded its index", 2026-10-12). Streamlit
Cloud serves the app under a path prefix, and every local app sits at the
root. All 19 searched maps were affected. The fix added a check and a skill
rule: type a street into the deployed box after any push.

**Dropping by id had side effects.** A same-named neighbor of a dropped
object could take its row, the "twins." One rollout commit dropped 222 twins
in 47 cities (b598b71c), and the final group found 34 more, 30 of them in
Taipei. The kept-id list had the opposite fault: a kept id could fail to
become a row. Both were fixed or turned into reports only on 10-16 ("post-
landing batch", lane 3).

**Overpass was the bottleneck until it was bypassed.** The one-query-per-
mirror pilot carried 0 of 4 cities ("wave 1: the scaffold", 2026-10-12).
overpass-api.de stopped answering for over two hours that night. A second
mirror served data three to four months old, now refused by a 7-day guard.
On 10-13 every public Overpass server stopped answering at once ("Buffalo's
and Miami's areas found without Overpass").

**Several statements to the owner were asserted, not measured.** "Every
merged square stays findable" was wrong: 15 of 43 returned only as alternate
names. The 334 "leak-word streets" were mostly landmarks and junctions.
Estimates of "about 20" and "six" rows became 83 and 32 when measured.
"A handful" of lost characters in Japanese names was 1,029 in 30 cities
(entries of 2026-10-12 and 13). Each was corrected the same day, but each
first reached the owner as fact.

**The outside model added a step that full reads then repeated.** Its first
reads cost about 22 dollars across three groups. On wave 1, three Claude
lanes checked its 1,977 flags and confirmed 13% as drops ("the outside
model's flags measured", 2026-10-13). Names alone, without tags, let it find
descriptions standing in for names and little else.

**Readers' tokens were the largest cost on record.** Five batch 3 reads and a
research agent took about 800,000 tokens. The five pilot full reads took
about 900,000 (entries of 10-11 and 10-13). The 24 reader lanes of the
extract run are not costed in the log.

**A scope fault slipped through every check.** Mendoza indexed its whole
province, 522 km out at the farthest row, because the check counted stations
per area and never area size (rule D entry, 2026-10-13). Rule D now fails an
index reaching more than 25 km past its stations without a dated reason.

## What the checks prove, and what they do not

**Proved, on all 237 maps as of 2026-10-16:**

- Every drawn station and line is returned by its own name as its own kind
  (`check_map_search.js`). The six warnings are ranking on phones: five in New
  York, where more than four stations share a name, and Toronto's Bathurst
  stop. They are open in PLAN.md, "Known faults."
- Each map carries its index's current hash, and each index whose cache is
  on disk rebuilds byte for byte from it (`check_place_search.py`, the index
  drift check).
- No index reaches more than 25 km past its stations without a recorded
  reason (rule D).
**Sampled, not proved on every map:** the OpenStreetMap credit and the
legend clamp were checked on three maps at three viewports after the
2026-10-16 render (559bf919). Before the landing, all 151 extract-run maps
were checked at two heights.

**Not proved:**

- **That an index holds only places.** The reads are the evidence, and no
  reader used the network. Every claim that a house is open, a church closed
  or a site private rests on cached tags ("wave 1: the last fifteen cities").
- **How much the reads missed.** Recall was measured only for lower model
  tiers against the top model's drops. The top model's own misses are
  unmeasured.
- **Streets in full.** Readers screened streets by pattern. The street
  coverage figure counts names, not geometry, and falls when names are
  dropped on purpose ("rulings on the fifteen held classes").
- **Phone performance beyond two tests.** Seattle and São Paulo passed on the
  owner's phone. No other city was tested on a phone.
- **Places never fetched.** Famous places with no matching tag, such as
  Yokohama Landmark Tower and Casa Rosada, are absent and wait for a wider
  fetch ("the extract run's full reads").

## Lessons

Per CLAUDE.md, a lesson belongs where the next run must pass through it. Each
line is a proposal for the owner, with its status where the record shows it.

1. **Run a sample wide enough to surface every class before building at
   scale.** One city per region found most classes, but the full reads of 146
   cities still found new ones. A next project should read a larger sample
   in full, then freeze the rules, then build the rest once.
2. **Test the deployed artifact, not only the local one.** A local app at the
   root hid a path fault for every live map. The deployed-box step is now in
   the skill; the lesson is general to any hosted page.
3. **Render once, after the last shared-code commit across all branches.**
   Render-once per branch still cost 183 second renders. Freeze the shared
   script before any branch renders.
4. **Make side effects of manual fixes part of the build.** Twins and unkept
   ids were found lane by lane. A build that reports both on every run
   removes the rounds (partly done, lane 3, 2026-10-16).
5. **Measure before telling the owner.** Four corrected statements in two
   days are a habit, not an accident. A count relayed to the owner should
   name the file and command that made it.
6. **Agree the trust line before piloting an outside model.** It worked
   here: 22 dollars bought a clear no. Keep the line and the scoring method
   written down for the next delegation.
7. **Prefer local extracts for bulk OpenStreetMap work.** Use Overpass for
   light lookups when it is healthy. The `osm-extract` skill is written so
   other projects can lift it.
8. **Budget usage before a fan-out.** The landing night ran reader lanes,
   landing agents and deploy-verify agents on one pool until it ran out.
   UNVERIFIED: the record holds no usage figure for that night.
9. **Check reach, not only presence.** A scope check that counts stations
   per area cannot see an area that is too large. Rule D now measures
   distance (e5345211).

## What the record does not show

The log records owner rulings, counts and commits, not hours of session time,
so the true cost in tokens is known for a few reads only. Nothing on record
measures how readers use the search: there is no logging by design, so
whether the feature is used at all is unknown. The 227.7 MB size is this
draft's own measurement and is not in any decisions entry. Why the
2026-10-12 size projection ran high is not explained. The six phone-ranking
warnings, the held worship-branch tag on Japanese maps, the wider fetch for
missing landmarks and the after-rollout audit of typos and closures (owner,
2026-10-11) were all open when this was written.
