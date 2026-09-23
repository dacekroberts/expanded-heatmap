---
name: premises-taxonomy
description: Build a city's classification module when its register uses a local taxonomy rather than NAICS - choosing which LEVEL of a multi-level scheme to key on, finding the catch-alls, and deciding whether a catch-all can be dispatched or must be dropped. Use when add-city Step 1 finds a non-NAICS classification, when scaffold-city has written an empty taxonomy skeleton, or when a bucket's counts look wrong after step 2. Not for a NAICS city (naics.py is complete) and not for choosing a city (add-city Step 0).
---

# Building a city's own taxonomy

Distilled from the first four cities that needed one — Chicago, Edmonton,
Madrid and Barcelona — plus the two national schemes, SCIAN and NAICS. More
have needed one since (Dublin's `dublin_uses`, Milan's `milan_source`); the
four are where the method came from, not the whole list. Read `add-city`
Step 1 first: this is that step when the answer is "the city has its own
system", which is most non-US cities and several US ones.

**The deciding measurement is the same every time and gets skipped every
time.** It is not "what do the values mean". It is:

> **What fraction of rows lands in a catch-all, at each level of the scheme?**

Everything else in this file follows from asking that first.

---

## Step 1 — Find out how many levels there are, before reading any values

A local taxonomy is usually a **hierarchy**, and the register publishes several
levels as separate columns. Barcelona's census publishes **four**. Madrid's
publishes **three**. A scheme with one level is the easy case and you can skip
to Step 3.

List the columns and their distinct counts. The shape gives it away: a column
with 15 values and a column with 75 values in the same file are two levels of
one thing, not two different facts.

## Step 2 — Measure the catch-all share at EVERY level, and key where it is smallest

**This is the step this skill exists for.** Run it before writing any of the
module:

```bash
python scripts/brief_check.py <city>    # with a taxonomy_catchall entry
```

The `taxonomy_catchall` check kind takes the level you intend to key on, the
catch-all value(s), and a `compare` list of the other levels, and reports the
share at each. Declare it in the city's brief so the decision is evidence on
the record rather than a choice someone made silently.

**Barcelona and Madrid keyed at opposite ends of identically-shaped taxonomies
and both were right**, which is why there is no default to inherit:

| | Level keyed | Catch-all share there | One level up |
|---|---|---|---|
| **Barcelona** | `Nom_Activitat` — the **finest** of four | **2.6%** | 35.1% at `Nom_Grup_Activitat` |
| **Madrid** | nearer the **top** of three | workable | — |

Barcelona's group level puts **20,693 of 58,908 active rows into `Altres`**.
Keying there would have thrown away a third of the city and looked fine, because
a third of a map being "other" is invisible once it is a colour.

**A share over about 5% at your chosen level is a reason to go a level deeper,
not a threshold to raise.** That is written into the check's failure message
deliberately.

### The cost of getting it wrong is asymmetric

Keying **too coarse** loses rows silently into a catch-all. Keying **too fine**
costs you enumeration work — Barcelona's 75 values each needed an explicit
home — and nothing else. When in doubt, go finer.

## Step 3 — Find the catch-alls by name, not by inspection

They are always there and they are usually obvious once you look:

| City / scheme | Catch-all |
|---|---|
| Barcelona | `Altres` |
| Chicago | `Limited Business License`, `Regulated Business License` |
| NAICS | `812990`, `812930`, `459999` |
| SCIAN | `469` (nonstore's exact twin) |
| Washington D.C. | `General Business` |

**A catch-all that is small is not therefore harmless.** Check what it *means*
before deciding, which is the next step.

## Step 4 — Ask whether the catch-all means ONE thing or several

This decides whether you can dispatch it or must drop it.

Barcelona's `Altres` is only 1,545 rows (2.6%) — and it means **five different
things depending on its parent**:

| Parent | Rows | Really is |
|---|---|---|
| `Quotidià alimentari` | 625 | food retail |
| `Comerç al detall /Engròs` | 458 | **retail or wholesale, no detail at all** |
| sector `Altres` | 323 | genuinely other |
| `Serveis` | 115 | services |
| restaurants group | 24 | food service |

`taxonomy_catchall`'s `parent_column` reports exactly this breakdown, so you do
not have to go looking.

**Where a parent settles it, dispatch** — `EXTRA_COLUMNS` in the taxonomy
module, the mechanism Chicago built for classifying `Limited Business License`
by a second field and Barcelona reused wholesale.

**Where it does not, drop the rows and say why.** Barcelona's 458 are excluded,
not assigned to Retail, on the reasoning that **"it is in a sector whose name
contains retail" is not evidence about a premises** — and that sector explicitly
mixes in wholesale. Dropping 458 rows you cannot classify is honest; assigning
them to the biggest bucket is a guess wearing a number's clothes.

## Step 5 — Check for accommodation hiding inside food service. It is a pattern

**Three countries, three times.** Assume it is there:

- **SCIAN 72** includes **721 accommodation** — 999 hotels. Counting the
  two-digit prefix reported 58,167 food-service units; the real figure is
  **57,168**, and the headline bucket share moved 73.07% → **64.1%**.
- **Barcelona's** `Restaurants, bars i hotels` group holds **10,722 rows of
  which 720 are `serveis d'allotjament`** — the group's own name says so, in
  Catalan, and it is still easy to miss.
- The same shape lurks in any scheme that groups by *sector served* rather than
  by *what the premises is*.

**Search the value list for the words**, in the register's own language:
`allotjament`, `alojamiento`, `hotel`, `hostal`, `pensió`/`pensión`, `fonda`,
`hébergement`, `accommodation`, `lodging`. Then check what bucket they would
land in.

Hotels are not storefronts for this project's purpose. A hotel beside a station
is not the same claim as a shop beside a station.

## Step 6 — When a taxonomy has levels, the levels are evidence

**Use the publisher's own hierarchy to settle a bucket call before reaching for
a reading of the words.** Two Barcelona calls were about to go the other way and
the hierarchy decided both:

- `Plats preparats (no degustació)` sits under `Quotidià alimentari`, **beside
  the butcher and the greengrocer** — so it is food *retail*, not a restaurant.
- `Fotografia` sits under `Comerç al detall` — so it is the camera shop, not the
  portrait studio.

Neither reading came from translating the Catalan. Both came from where the
publisher filed the value, which is a statement by the people who collected the
data.

## Step 7 — Enumerate every value with an explicit home, and prove it

- Pull the **full** `SELECT DISTINCT <column>` with counts, restricted to the
  rows step 2 actually keeps (the active/open filter). Distinct values across
  the whole file include ones that never survive filtering, and padding a
  mapping with them wastes review attention.
- Give **every** value a home: a bucket, or `None` with a reason.
- `classify()` **raising on an unknown value is the design**, not a rough edge.
  It is what would have turned "SCIAN is basically NAICS" from a silently
  half-empty map into a loud failure on the first run.
- **Put import-time assertions in the module** for the facts that were expensive
  to learn. Barcelona's assert the accommodation carve-out and the nan-safety of
  its normaliser. An assertion beside the mapping is read by everyone who edits
  the mapping; a comment in `DECISIONS.md` is not.

### Two traps that are not about meaning at all

- **`pd.DataFrame` fills a missing key with `float('nan')`, and `nan` is
  truthy.** A scalar-safe normaliser —
  `value.strip().upper() if isinstance(value, str) else ""` — is not fussiness.
- **Normalise for joins, never for display.** Keep the register's own string
  alongside; it is what the tooltip should show, and it is what a reader
  checking your work searches for.

## Step 8 — Record what the choice was, not just what it was

In `DECISIONS.md`: the level chosen, **the catch-all share at each level that
decided it**, the catch-all's parent breakdown, and any rows dropped with the
count. The numbers are the reasoning — "we keyed on the finest level" is not
checkable and "35% versus 2.6%" is.

## Checklist

- [ ] Every level of the scheme identified, with distinct counts
- [ ] **Catch-all share measured at each level**, via `taxonomy_catchall`
- [ ] Keyed where the share is smallest; a `>5%` share justified or re-keyed
- [ ] Catch-all's parent breakdown examined — dispatched, or dropped with a stated reason
- [ ] **Accommodation searched for by name** in the register's own language
- [ ] Publisher's hierarchy used to settle ambiguous values, not a translation
- [ ] Every surviving distinct value has an explicit home; `classify()` raises otherwise
- [ ] Import-time assertions for the expensive findings
- [ ] The check declared in the city's brief so the decision re-runs
- [ ] `DECISIONS.md` carries the shares that decided the level
