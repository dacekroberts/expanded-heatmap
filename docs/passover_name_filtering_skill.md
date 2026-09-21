---
name: business-name-privacy-check
description: Check whether a map or dataset built from a municipal business registry is about to publish individuals' personal names at their home addresses, and decide what to filter. Use before publishing any city-level business map, and after any change to the row-filtering or classification step. Portable: written to be dropped into another project's .claude/skills/.
---

# Are you about to publish someone's name at their home address?

A portable write-up of a check run on a four-city business-density map in
September 2026, and of what it found. **Copy this file into the other
project's `.claude/skills/` directory** and adapt the column names; the
reasoning and the traps transfer unchanged, because they come from how
municipal registries are shaped, not from any one codebase.

## Why this applies to a sibling project

If a project maps business points from a municipal business registry, it
inherits this risk from the **data**, not from the code. Three reasons it may
be worse there than in the project this came from:

1. **Registries are full of sole proprietors with no trade name.** Whatever
   the pipeline falls back to when the trade-name column is blank is likely a
   person's own name. This is a property of the registry.
2. **A single-city project concentrates the exposure.** Four cities dilute a
   bad one; one city does not. If that city has a high blank-trade-name rate,
   the whole map is affected.
3. **An older project may lack even accidental protections.** One city in the
   source project happened to exclude home-based licences for unrelated
   reasons and came out clean at 0.09%. That was luck, not design.

## The principle

**Publish public commercial information, not personal information.**

A trade name someone chose for their shop is commercial and deliberately
public; mapping it is the entire point. A registrant's own name at what looks
like their home is not, even though the registry holding it is public.

"It is in a public dataset" answers the *licence* question, not the
*publishing* question. A registry entry sits behind a search box; a map pin is
a precise coordinate, plotted, searchable and indexable. Re-publishing in a
more usable form is a different act from the registry's own listing, and it is
the act that needs justifying. Where the two conflict, the map loses the row.

## The check, in order

### 1. The authoritative measure: did the fallback fire?

Find the trade-name column and whatever the pipeline uses when it is blank.
Then join the **published** names back to the **raw** export. A name that can
only be explained by the fallback column is a registrant name on your map.

```python
import html, json, re
import pandas as pd

raw = pd.read_csv(RAW, dtype=str, low_memory=False)
trade = raw[TRADE_COL].fillna("").str.strip()      # e.g. dba_name
owner = raw[OWNER_COL].fillna("").str.strip()      # e.g. business_name / legal_name / ownership_name
fallback_only = set(owner[(trade == "") & (owner != "")].str.upper()) - set(trade[trade != ""].str.upper())

published = [...]                                   # the names your output actually shows
hits = [n for n in published if n.upper() in fallback_only]
print(f"{len(hits)} of {len(published)} published names can only be the {OWNER_COL} fallback")
```

**Trap that cost real time:** do not measure this on the *processed*
intermediate. A pipeline that renames the trade column and fills its blanks in
the same step leaves no trace — the blank count reads as zero and everything
looks fine. Only the raw export can tell you. Three of four cities read as
"clean" until the join went back to raw.

Reference numbers from the source project, blank trade name in raw: two
registries 0.0-0.2%, one 68.1%. The spread between registries is enormous, so
measure; do not assume.

### 2. The heuristic measure, and its false-positive floor

A regex for "looks like a person's name" (two or three capitalised words, no
corporate token, no digits or `&`) is useful but noisy. In the source project
it flagged **17-23% of pins in every city and in every category**, including
unambiguous storefronts: full-service restaurants, taverns, beauty salons.

That floor is **not exposure**. It is trade names that happen to read like
people ("Senor Sisig", "Shake Shack", "Maria Elena"). Reporting that number as
a privacy finding would have been wrong and alarmist.

**Use the heuristic only in combination with signal 3.** On its own it tells
you almost nothing.

### 3. The residential signal, and the suite/apartment confound

Check the address for a residential indicator. **Separate residential from
commercial indicators or the number is meaningless:**

```python
RESID = re.compile(r"\b(APT|APARTMENT|SPC|SPACE|TRLR|LOT)\b|\bUNIT\b")
COMM  = re.compile(r"\b(STE|SUITE|FL|FLOOR|BLDG|BUILDING|RM|ROOM)\b")
```

**The trap:** a first pass lumped `STE` in with `APT` and reported jewellery
stores at 42% "residential". They were downtown suites in a jewellery-district
tower — commercial tenancies, entirely legitimate. Splitting the two dropped
that category to 6% and moved the real offender to the top of the list.

Then intersect: **person-like name AND residential indicator**. That
combination is the number to act on. In the source project it separated the
cities cleanly: 0.09% and 0.03% (fine) against 1.67% and 5.73% (act).

**Second trap:** one registry had its suite field essentially unpopulated (6
of 3,117 mapped rows carried any indicator). Its 0.03% was a *measurement
gap*, not a clean bill of health. If the address field cannot carry the signal,
say so rather than reporting a low number as safety.

### 4. Rank classifications by that intersection, do not guess

Group by the classification code and rank by the intersection count. This
finds categories you would not have guessed, and it is how the real problem
surfaced in the source project.

## What it found, and the fix that generalises

The largest exposure was not a privacy bug at all — it was a **definitional
one**, and the privacy harm was its symptom:

- The project's stated subject was *storefront* commercial density.
- Its retail bucket was a NAICS prefix match on `44` and `45`.
- **NAICS `454` is "Nonstore retailers"**: electronic shopping, mail-order,
  direct selling, vending-machine operators, fuel dealers. Non-storefront **by
  NAICS's own definition**, yet swept in by the `45` prefix. It was 10.1%,
  9.0% and 1.7% of three cities' pins, and `454390` (direct selling) was the
  single largest residential-exposure group left after the first fix.
- Similarly `812990` "All Other Personal Services" is a catch-all that a prior
  sample found **~90% non-storefront: home-based sole proprietors**. Excluding
  it in the worst city removed 30.7% of that city's rows and cut
  fallback-traceable personal names from 3,998 to 1,803.

**So: check whether your category filter's own definition already excludes what
you are publishing.** A broad prefix match is the usual culprit. Fixing the
definition fixes the privacy problem for free, and it is a much easier change
to justify than a privacy carve-out, because it makes the project *more*
correct about its own subject.

Codes worth looking at in any NAICS-based project: the `454` family (nonstore),
`812990` (all other personal services), `812930` (parking: a planned trip, not
a storefront — a data-quality question rather than a privacy one, ~4%
residential), `459999` (miscellaneous retail: a prior sample found ~70%
plausible storefronts, so probably keep). A local licence taxonomy has its own
equivalents; look for anything named "other", "limited", "general" or "misc".

## Deciding, and what not to do

Order the options by how much they cost the project:

1. **Fix the category definition** (exclude a definitionally non-storefront
   family). Cheapest to justify, improves correctness, usually the biggest win.
2. **Exclude a specific catch-all code**, with a sample recorded.
3. **Drop the owner/registrant fallback**: show the classification instead of a
   name for those rows. Loses real storefronts whose registry simply has no
   trade name.
4. **Remove names entirely.** Guts the map; a last resort.

Coordinate rounding is largely theatre here: 5 decimal places is about a metre,
and the address is already the exposure. Do not bother unless precision itself
is the concern.

**Be honest about the limits in whatever you write down.** The name test is a
regex; it cannot tell a sole proprietor legitimately trading under their own
name (a real shop) from a registrant sitting at home. The residential indicator
is a proxy, not proof. No row is individually verified, and nobody is
contacted. Record the numbers, the sample size, the date, and the decision —
then a later reader can re-judge it instead of trusting it.

**Also still open in the source project, and probably in yours:** the dataset
licences and terms of use were never read. That is a separate question from
this one. This check is about what is *appropriate* to publish; the licence
governs what is *permitted*. Do both.

## A reusable script

The source project's version is `scripts/check_personal_exposure.py`: it takes
a city slug, reads the rendered output plus the raw and processed data, and
prints the fallback-only count, the person-like count, their classifications
and the residential share — numbers, deliberately not a pass/fail, because the
judgment is per city. It is wired in as a pre-publish gate and re-run after any
change to row filtering or classification. Copy that shape: a check that
prints a verdict nobody reads is worse than one that prints numbers somebody
has to think about.
