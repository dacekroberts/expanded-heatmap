---
name: commercial-use-audit
description: Run the one-time commercial-use audit into docs/commercial_use_positions.md - one row per city, layer and source, the weakest source in use deciding the city's column (allowed, blacklisted, held) - cheaply - distinct sources counted and audited once, the standard licences settled from a table with no read, a first pass over the STORED licence texts whose every verdict carries a quoted sentence a script confirms, and a full licence-read only for the sources transit-globe wants. Use for the audit after the phase 2 landing and for a city added afterwards. Not for deciding whether THIS site may publish a source (read-licence, licence-read), and not legal advice.
---

# The commercial-use audit

Written by Cleanup, 2026-10-12. The rules are the owner's of 2026-10-11
(`DECISIONS.md`, "The portfolio review's handoff answered"); the method
below is the owner's ruling of 2026-10-12 (`DECISIONS.md`, "The search
rollout's cheap path and the commercial-use audit's method"). Lines marked
TO BUILD name a script that does not exist yet.

## What the audit answers, and for whom

One question per source: **may a third party use this data commercially**,
and on what condition. The answer serves the transit-globe project's
decisions only. This site stays non-commercial, so nothing here changes what
the site publishes, and no verdict here is a reason to add or remove a city.

The same pass answers public sharing of analytics and visuals pieces
(owner, 2026-10-11): which pieces could go public, with what notices and
which cities removed. Analytics supplies its pieces and the cities each uses.

## The rules (owner, 2026-10-11)

- **The unit is city, layer and source.** A per-city list with no source
  table put nine Japanese cities in two columns at once.
- **The weakest source in use decides the city's column**: allowed,
  blacklisted or held. "Allowed if layer X is left out" is noted where true
  (Fukuoka's own list is CC BY; only its MHLW rows are non-commercial).
- **A source whose read never addressed commercial use is held**, never
  assumed allowed.
- **From the record first**, then one `licence-read` per source
  transit-globe wants. The review session's first draft is a starting point,
  not a source.
- **Every source that places a pin counts**, not only the registers: address
  references, parcel layers, geocoders, boundary files, rail geometry.
- A script confirms every `app/cities.py` city appears once.

## The verdict shapes

| Verdict | Means | Column |
|---|---|---|
| PERMITTED | The terms allow commercial use outright | allowed |
| PERMITTED, CONDITION | Allowed with a duty: attribution, share-alike, a notice, no alteration, a currency duty | allowed, condition named |
| FORBIDDEN | The terms exclude commercial use | blacklisted |
| SILENT | The terms read and say nothing on it, or nothing is recorded | held |
| NOT READ | No stored text and no recorded read of the point | held |

Each verdict carries: the source, the document it rests on (a file under
`docs/licenses/` or a dated entry in `docs/data_sources/<country>.md`), the
sentence quoted in its own language, and the date read.

## The cheap path

1. **Count the distinct sources first** (TO BUILD,
   `scripts/commercial_use_sources.py`): from `outputs/<city>/provenance.json`
   and the country files, one line per source with the cities and layers
   that use it. The audit's size is this count, not the city count: one
   national register or one portal licence covers every city on it. Report
   the count to the owner before reading anything.
2. **Settle the standard licences from the table below, with no read.** The
   table settles what a licence says. It does NOT settle whether a source is
   under it: the record must show that licence named on the dataset itself,
   not on the portal's footer (`read-licence`, the three corrections).
3. **First pass over the stored texts.** For each remaining source with a
   text under `docs/licenses/` or a recorded read: a verdict and the sentence
   it rests on. After the DeepSeek integration the cheaper model
   takes this pass, one request per source, the stored text in and JSON out
   (verdict, quoted sentence, the clause's heading). **A script confirms each
   quoted sentence occurs in the stored text**
   (`scripts/commercial_use_quote_check.py`, built 2026-10-12): exact, or
   after Unicode NFC and whitespace collapsing, or with whitespace removed
   (a PDF's line wraps inside a Japanese sentence), each reported as such; a
   quote that is not there, is under 12 characters, is cut out of a longer
   word, has no clause heading, or names a document off the hashed list in
   `docs/licenses/README.md` voids the verdict; so do two rows on one
   source. A recorded read under `docs/data_sources/` is NOT CHECKED, for a
   person. **The script proves the passage is in the file, not what it
   means**: MHLW's sentence that "use outside the purpose is forbidden" is
   about personal information, not commercial use. Every VERIFIED row
   prints 60 characters either side and its clause: read them all. **The
   first pass's prompt says**: copy characters exactly from the stored
   text (no straightened quotes), quote within one line of an .md or .html
   file, and give the heading the sentence sits under. No further
   normalisation is added (owner, 2026-10-12); a true quote that voids goes
   to Claude.
4. **Claude reads** every SILENT and every PERMITTED, CONDITION, and a
   sample of the PERMITTED (say one in five, and all of a language the model
   was not tried on).
5. **The owner decides** every FORBIDDEN and every unclear one, and any
   "allowed if layer X is left out".
6. **A full `licence-read`**, one source per call, only for a source
   transit-globe wants whose row is held.
7. **Write `docs/commercial_use_positions.md`**: the source table first, then
   the city table derived from it by script, never by hand. Is the file
   rendered anywhere public? It is not on a page today; keep it that way
   unless the owner says otherwise.

## The costly error

A wrong PERMITTED is the mistake that matters: another project would build
on it. So the cheaper model finds and quotes; it never gives the final
verdict on its own. Before it is used on a language, try it on sources whose
answer is already on record: MHLW's terms (non-commercial, Japan), a KOGL
Type 2 or 4 source (Korea), and one CC BY 4.0 portal as the easy case. A
miss on any of them means Claude reads that language in full.

## Standard licences: the commercial answer

Settled from the licence texts themselves; a version not listed is read.

| Licence | Commercial use | Condition |
|---|---|---|
| CC0 1.0, Public Domain Mark | Permitted | none |
| CC BY 4.0, CC BY 3.0, CC BY 2.1 JP | Permitted | attribution, changes indicated |
| CC BY-SA 4.0 | Permitted | attribution, share-alike on adaptations |
| CC BY-NC, CC BY-NC-SA, CC BY-NC-ND (any version) | Forbidden | |
| CC BY-ND | Permitted, but no adaptations may be shared | a derived map is an adaptation: treat as held and ask |
| ODbL 1.0 (OpenStreetMap) | Permitted | attribution; share-alike on a derived database; a produced work carries the notice |
| Open Government Licence, UK v3.0; Canada 2.0 and the provincial and municipal versions modelled on it | Permitted | attribution statement |
| Licence Ouverte / Etalab 2.0 (France) | Permitted | attribution with the date |
| Datenlizenz Deutschland, Namensnennung 2.0 | Permitted | attribution |
| Japan: 政府標準利用規約 2.0, 公共データ利用規約 (PDL) 1.0 | Permitted | attribution, edits stated |
| KOGL Type 1 (Korea) | Permitted | attribution |
| KOGL Type 2, Type 4 | Forbidden | |
| KOGL Type 3 | Permitted, no alteration | treat as held and ask, as CC BY-ND |

A portal's own terms, a "terms of use" page, an API agreement, or a licence
with a local rider is never settled from this table.

## Where the record already is

- `docs/licence_positions.md`: every source's position, ranked weakest to
  strongest, as of 170 cities; rows 1.6, 2.7, 2.8 and 2.10 are the four
  non-commercial sources it names. A starting index, to be brought to 237.
- `docs/derived_use_licensing.md`: derived material (statistics, cards).
- `docs/licenses/`: the stored texts, each hashed in `check_provenance.py`.
- `docs/data_sources.md` and `docs/data_sources/<country>.md`: each source's
  recorded terms and date; the required notices.
- Known stale in the first draft (measured 2026-10-11): it omits Washington
  D.C., San Diego and Belgium's sources other than KBO, and reads registers
  only.

## Guards

- Stored licence texts are public documents and may go to an outside model.
  Nothing from a business register may, and no API key enters the repository.
- This is a reading of the project's own record, not legal advice; the
  positions file says so at its top.
- A verdict is dated. A source re-read later gets a new row, never an edit
  to an old one (`decisions-entry`).
