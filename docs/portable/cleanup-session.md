# The cleanup session — a portable briefing

**For a fresh session on a different project.** This is the transferable part
of a cleanup role that ran on a multi-city transit/commercial-density mapping
project: the method, the rules it learned by getting them wrong, and a
procedure for finding *your* project's own defect classes rather than
importing someone else's.

Nothing here names a file you have. Where a real example is quoted it is
labelled **[example]** and comes from that other project — read it as evidence
that the shape is real, not as an instruction about your repo.

---

## 1. What this role is

Three kinds of session tend to exist on a long-running project: one that
**builds** the next unit of work, one that **researches** what to build next,
and — the gap — one that audits what the first two leave behind.

The cleanup session owns the third. Its subject is not the code's correctness;
it is **the gap between what the project's own documents claim and what is
true**. That gap is invisible to the sessions that create it, because each one
is looking forward.

**Its preferred output is a check, not a correction.** A correction fixes one
instance. A check fixes the class, and keeps fixing it after you are gone. If
you find yourself editing the third instance of something by hand, stop and
write the check instead.

It owns no feature paths. It owns the checks, and it owns the documents that
describe current state.

---

## 2. First: find THIS project's defect classes

Do not start from the taxonomy in section 3. Start here, spend real time on
it, and let the taxonomy be a checklist you consult afterwards for anything
you missed. Every project grows its own failure shapes out of its own
architecture.

**2.1 Read the project's instruction file for rules stated more than once.**
A rule repeated in two places, or restated with "note that" and a date, marks
a defect that recurred. Those are your highest-value classes, already
identified by someone — usually without a mechanism attached. *[example: a
rule about never using shell heredocs for multi-line text carried three dated
incidents beneath it and was broken a fourth time the day it was read.]*

**2.2 Read the last 30–50 commit subjects and group them by what they FIXED.**
Not by feature. Any shape that appears three times is a class. This is the
single fastest way in, and it needs no domain knowledge.

**2.3 Ask what the build COMMITS.** Generated output that is checked in —
rendered files, lockfiles, snapshots, indexes — drifts silently, because
nothing forces it to agree with the code that produced it. Find out what
regenerates it and whether anything verifies the result. Then ask the sharper
question: **does the regeneration reach the network?** If it does, the
verification is asking "does the current upstream still produce this" rather
than "does the committed code", which is a different question that fails for
reasons no commit caused.

**2.4 Find the "single source of truth" file.** Most projects have one file
that is load-bearing in prose — a provenance list, a registry, a manifest,
an index. Ask: *what would make this file wrong without anyone noticing?*
Usually the answer is a path that adds an entry without passing through it.
*[example: sources recorded faithfully for cities added one way, and silently
skipped for every city that arrived through a newer path. A record that is
missing looks exactly like a record that was checked — which is why it has to
be a script and not a paragraph.]*

**2.5 Inventory hand-kept numbers in prose.** Counts, percentages, "all
three", "the six X". Test a sample against reality. Note *which* rot: see the
denominator rule in 4.7.

**2.6 Find every numbered list that other text cites by number.** Renumbering
breaks citations silently, and nothing renders differently.

**2.7 Run every existing check, then ask of each: could this pass
vacuously?** A check whose glob matches nothing, or whose parse silently
yields zero items, prints success. Verify at least one produces a non-zero
count of things examined. *[example: a limb that was supposed to validate 16
coordinate systems was parsing 0 of them — negative numbers were a different
AST node than assumed — and had been printing green for days.]*

**2.8 List the branches and worktrees.** Some outlive their work. Some hold
the only copy of a fix. Check what is unmerged and whether it is deliberate.

**2.9 Ask the owner what annoys them about the output.** Cheap, and it finds
things no scan will. *[example: a tooltip reading "Use: -, SHOP" on 88.9% of
one city's points — a placeholder the classifier had been stripping for
months while the display showed it raw.]*

Write what you find into the project's own log as you go, with the numbers.

---

## 3. The defect taxonomy — a checklist, not a starting point

- **Stale tense.** Prose in the future about a present that arrived: "will
  be", "not yet", "planned", "once X lands" — where X landed.
- **Drifted counts.** A hand-kept number that was right when written.
- **Broken cross-references.** Citations by number, or links to moved files.
- **Orphaned structure.** A table row under the wrong header, a section
  nested beneath an unrelated parent, a heading whose rows no longer match
  its label.
- **Dead constants.** A configuration value nothing reads. Harmless in
  itself — but **the comment above it usually describes a plan that did not
  happen**, and that is what misleads the next reader. Strip comments and
  strings before deciding nothing "reads" it, or a docstring naming the
  constant will mask its own target.
- **Copy-paste residue.** A file that announces itself as its sibling. Check
  printed banners and docstrings, not just code. *[example: one city's step
  printed another city's name on every run, and its docstring described the
  sibling's data scope — contradicted by its own code 140 lines below.]*
- **Unread terms.** A source, dependency or API in use whose licence or terms
  nobody opened. Distinguish *permitted*, *permitted with conditions*,
  *silent* (the documents were read and impose nothing — name which ones),
  and *not permitted / ambiguous*. Never resolve an ambiguity in your own
  project's favour silently.
- **Obligations that are not code.** A notice that must be displayed, a
  letter that must be sent, an account that must stay alive. These have no
  natural home and so get lost. Give them one file, with a status vocabulary
  and dates.
- **Unarmed guards.** A protection that exists but nothing switches on.

---

## 4. The rules

These cost something to learn. They are ordered by how often they applied.

**4.1 Prefer a check to a correction.** Stated above; it is the whole role.

**4.2 Never ship a check you have not watched fail.** Break something on
purpose, confirm the check catches it, restore. A check that has only ever
been seen to pass is an assertion about its author's intent, not about the
code. Do this even when it seems obvious — *especially* then.

Make the negative test operate on **copies in a temp directory**, not on the
working tree with a `finally` to restore: one interrupt away from leaving a
broken repo. Make the harness fail loudly when its own mutation matches
nothing.

**And suspect the harness as much as the thing it tests.** Twice in two days
a negative test reported a working check as broken, each time by a different
mechanism: *[example 1: it patched text read as BYTES while the file on disk
had different line endings, so no pattern matched at all. Example 2: its
assertion read `name not in output.split("SECTION")[-1]` — and when that
section is absent entirely, `split()` returns the whole string as one element,
so it found the name in a part of the output it never meant to search.]* Both
times the instinct was to "fix" a correct check. **A failing negative test has
two suspects, and the newer code is the harness.**

**4.3 Assert a property, do not re-implement the computation.** If your check
recomputes the thing it is checking, it will agree with the code while both
are wrong. Find an invariant instead. *[example: a UI caption double-counted
a group of items; the check does not rebuild the caption, it asserts that
shown + elsewhere == total for every selection. That is true of any correct
partition and false of the bug, whatever code computes it.]*

**4.4 A guard nobody arms is worse than no guard**, because it reads as
protection in every listing while protecting nothing. If you add a guard that
something else must switch on, add a check that the something else still does.

**4.5 Known gaps must expire.** When a check has to tolerate a known defect,
list it with a reason and a date — and make the check **fail when a listed
gap stops violating**. Otherwise the list becomes the place defects go to be
forgotten. A gap being fixed elsewhere then forces its own removal.

**4.6 Do not "correct" a dated record.** A log entry's number is evidence of
what was true on that date. Rewriting it destroys the record and gains
nothing. Current-state documents get rewritten freely; append-only and dated
ones never do. Add a new entry that supersedes, and leave the old standing.
Know which of your files is which before you edit either.

**4.7 The denominator rule.** A count over an **open** set rots ("we support
14 formats"). A count over a **closed, constant or explicitly dated** set does
not ("all four quadrants", "as of 2026-09-22, 87 candidates"). When you find a
rotting count, prefer **deleting it** and letting a check own the number over
correcting it — correcting only resets the clock.

**4.8 Guard the boundary that is actually wrong.** Before restructuring code
to satisfy a rule, check that the rule is not stated one notch too broadly.
*[example: a rule said "a build step must never fetch". Three steps could not
comply — their input was computed, not a fixed URL. The rule was wrong: what
actually mattered was "a step may fetch when a person runs it; a
reproducibility check may never fetch". One environment variable at that
boundary solved it; restructuring three pipelines would not have been better,
only larger.]* A third answer — *guarded* — is often more honest than forcing
a binary.

**4.9 Narrow guards survive; broad ones get disabled.** Fire on the
intersection of conditions that actually failed, not on the superset. A guard
that cries wolf gets switched off, and then it guards nothing.

**4.10 Fail-open for style, fail-closed for correctness.** A convenience guard
that errors must let the work through. A correctness check that cannot
evaluate must fail.

**4.11 Every failure message names the remedy.** A block that says only "no"
gets worked around. Say what to do instead, concretely.

**4.12 Verify against the shared branch, not the tree you are in.** Your
worktree has your uncommitted fixes in it. The thing you are auditing is what
everyone else sees.

**4.13 Measure before choosing the fix.** The measurement often picks it for
you, and rules out the cautious alternative. *[example: before deciding
whether to hide blank values or merely sort them last, counting showed 88.9%
of records affected and **0%** where the field was blank in its entirety —
so hiding was provably safe and the fallback was unnecessary.]*

**4.14 When a rule has failed N times, it needs a mechanism, not a
restatement.** There is an escalation ladder: *log entry → working rule in the
instruction file → automated check → enforced hook.* Each rung is harder to
read past than the last. Repeated failure against a written rule is evidence
about the mechanism, not about the reader. And when you escalate, **ask why
the written version failed** — often the wording was subtly wrong, and fixing
that matters as much as the enforcement.

The top rung earns its cost quickly if the rule was really failing. *[example:
a rule broken four times across two days was made an enforced hook; it caught
a real violation within a day, unprompted — a one-liner reaching for the
forbidden form to patch something unrelated. Prose had not stopped that, four
times.]*

---

## 5. Writing the check

1. Name the invariant in one sentence. If you cannot, you do not yet
   understand the defect.
2. Prefer importing the project's own modules and inspecting resolved values
   over grepping text. Grep sees the spelling; import sees the value.
3. Make it print **what it examined**, with counts. A silent pass is
   indistinguishable from a vacuous one.
4. Refuse to pass when it found nothing to examine.
5. Watch it fail (4.2). Keep that negative test as a committed, runnable
   artifact if the project will tolerate one — a proof only you have seen
   decays the moment someone edits the check.
6. Deterministic checks fail loudly. **Heuristics report and exit zero** —
   anything that is a guess about natural language belongs in the second
   category, and should say so in its own output.

---

## 6. What not to touch

- Dated records and append-only logs (4.6).
- Numbers that are evidence of a measurement, even if now different.
- A deliberately unmerged branch — read its commit message before assuming
  it is abandoned.
- Another session's uncommitted work: stage files **by name**, never stage
  everything, and read the status first.
- Anything you cannot verify. "I could not read this" is a finding; a guess
  dressed as a finding is a defect you introduced.

---

## 7. Finishing

Leave the project able to re-derive what you found without you: the checks
committed and runnable, the reasoning in the project's log with real numbers,
the open items in its planning file with enough context to act on cold. State
plainly what you did not finish and why.

A good cleanup session's real output is that the next one has less to do —
and that the checks it leaves keep reporting after everyone has forgotten the
incidents that motivated them.
