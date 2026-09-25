---
name: cjk-text
description: Read, match and display Chinese, Japanese and Korean text in a city's data and on its map - console and file encodings on Windows, bilingual OSM names, choosing a language edition, normalising CJK text before any match or de-duplication, the privacy check's blindness to CJK names, and the font order that decides which glyph forms a reader sees. Use before and during any city whose data carries Han, kana or Hangul - Hong Kong, the Taiwanese cities, Seoul and the Japanese cities - alongside add-city and address-join. Not for Latin-script cities.
---

# Chinese, Japanese and Korean text - processing it and showing it

Distilled from **Hong Kong** (2026-09-24), the first city whose data carried
Chinese characters, and written before the cities queued behind it: **Taipei
(Regional), Taichung and Taoyuan** (Traditional Chinese, registers in Chinese
only), **Seoul** (Hangul) and the **Japanese cities** (kanji and kana). Each of
those will meet what Hong Kong met, usually harder, because Hong Kong's registers
come in an English edition and theirs do not.

Every item is labelled. **MEASURED** means Hong Kong hit it and the fix is in
its code. **TO CHECK** means a known trap in this family that Hong Kong did not
reach; measure it in the city that does, then move it up a label here.

## 1. Encodings on this machine - MEASURED

This project runs on Windows, where Python's default text encoding is the ANSI
code page (cp1252), not UTF-8. Three things followed from that in one build:

- **Printing a CJK name crashed a probe.** `print()` of MTR's station list raised
  `UnicodeEncodeError: 'charmap' codec can't encode characters`. A crash
  mid-probe looks like a data problem, and it is not one. Put
  `sys.stdout.reconfigure(encoding="utf-8")` at the top of any script that
  prints names, or run it with `PYTHONIOENCODING=utf-8`.
- **A console dump is not evidence about the bytes.** An ALS response piped
  through `python -m json.tool` showed its Chinese fields as mojibake
  (`ä¹\udc9d...`) because the pipe was decoded as cp1252. The data was
  fine. Judge an encoding from the file, opened with an explicit encoding, never
  from terminal output.
- **A BOM hides in the first header.** MTR's CSV begins with U+FEFF, so its first
  column read `﻿Line Code` and a lookup by `"Line Code"` failed. Read CSVs
  with `encoding="utf-8-sig"`; it strips a BOM when there is one and is harmless
  when there is not.

The rule underneath all three: **every `open`, `read_text`, `write_text`,
`read_csv` and `to_csv` names its encoding.** The pipeline already does; probes
are where it slips.

And one project rule bites harder here: a regex holding a Unicode escape
(`[㐀-鿿]`) contains backslashes, so it cannot go in a Bash heredoc or
`-c` string (`.claude/hooks/block_heredoc.py`). Write the probe to a file.

## 2. Names from OpenStreetMap - MEASURED

- **Hong Kong's convention is a bilingual `name`** (`荃灣 Tsuen Wan`) plus
  `name:en`. One MTR stop node had no `name:en`. The rule in
  `pipeline/hong_kong/step1_stations.py`: prefer `name:en`; failing that, take
  the Latin tail of `name` only when it matches CJK-then-Latin; failing that,
  STOP and name the node, never guess. Count the fallback, and print it
  (Hong Kong: 1 of 371).
- **Which tag carries the reader's name differs per country** - TO CHECK before
  step 1, on the city's own relations: Taiwan `name:en` / `name:zh`, Japan
  `name:en` / `name:ja-Latn` / `name:ja_rm`, Korea `name:en` / `name:ko-Latn`.
  Print the coverage of each before choosing.
- **Network tags are CJK strings** (`港鐵 MTR`, `輕鐵 Light Rail`). Match them
  exactly, keep them in the city's config (a UTF-8 source file), and print the
  relation table before matching - the osm-rail rule, unchanged.
- **When the operator's list and OSM disagree on a name, match on the ID.**
  Light Rail stop 250 is "Hoi Wong Road" to MTR and "Tuen Mun Swimming Pool" in
  OSM; both carry stop ID 250, and that is what made the rename provable rather
  than assumed. Record the alias with the ID that proves it.

## 3. Which language edition - MEASURED, and a decision

- **Bilingual publishers ship paired editions and paired fields.** FEHD
  publishes `_EN` and `_TC` XML files; its CSDI layers pair `NAME_EN`/`NAME_TC`,
  `ADDRESS_EN`/`ADDRESS_TC`, and the shop sign as `NSEARCH03_EN`/`_TC`. Choose
  the edition deliberately, say which on the page, and record why.
- **An English edition is still mixed-script.** Hong Kong used the English
  edition, and 7,159 of its in-ring tooltips contain Chinese anyway - shop signs
  such as `章記香港仔魚旦王` or `Harvest House 加賀屋 (Peace & Joyful)`. Plan for
  CJK on the map in every CJK city, whichever edition is read.
- **Taiwan's and Japan's registers are single-language** - the brief says so
  for Taiwan's national tax register. Their maps will show names in Chinese or
  Japanese only. That is correct; decide in the page text whether a reader
  needs to be told.
- **Join on an identifier, never on text.** Hong Kong's register and its point
  layer joined by licence number; the shop signs were identical on 99.7% of
  rows, which is high and still not a key.

## 4. Normalising before any match or de-duplication - partly MEASURED

- **`upper()` does nothing to Han, kana or Hangul.** Hong Kong's de-duplication
  key was `upper().strip()` of shop sign and address, which is enough for the
  English edition (2 duplicates found). For CJK text, normalise first with
  `unicodedata.normalize("NFKC", s)`. It folds full-width Latin and digits
  (`ＡＢＣ１２３` to `ABC123`), full-width parentheses (`（）`) and the
  ideographic space (U+3000). TO CHECK: how much of Taiwan's and Japan's text is
  full-width - count before and after normalising.
- **Addresses insert units a join does not expect.** Taipei's brief measured
  its register inserting `里` and `鄰` between district and street, so the first
  join matched nothing; it matches on district + street + number. Japanese
  addresses carry `丁目`, `番地` and `号`, often with kanji numerals (`一丁目`)
  - TO CHECK against the city's address file. See `address-join`.
- **A CJK regex range must reach the supplementary planes.** Hong Kong's step 1
  uses `[㐀-鿿]` (CJK Extension A and the unified block), which is
  enough to spot a bilingual name. It is NOT enough to test "is this
  character Chinese": Hong Kong's HKSCS characters and many Cantonese ones sit
  above U+FFFF (`𨋢`, lift, is U+282E2). Use
  `[㐀-鿿豈-﫿\U00020000-\U0003134f]` for Han, add
  `぀-ヿ` for kana and `가-힯ᄀ-ᇿ㄰-㆏` for
  Hangul. Python's `re` has no `\p{Han}`.
- **Publishers write placeholders, not blanks.** 308 FEHD licences carry
  `No Record` or `(no record found)` in the shop-sign field; they show as
  "No shop sign on the licence". TO CHECK in each CJK register: the Chinese-,
  Japanese- or Korean-language placeholder, which a Latin pattern will not see.

## 5. The privacy check cannot read these scripts - MEASURED

`scripts/check_personal_exposure.py` is built on Latin-script heuristics, and in
Hong Kong it misread in both directions:

- **Its person-name heuristic flagged 14.7% of pins, and every one was a trade
  name.** It reads two capitalised words as a name: `KWOK YIN`,
  `Wealthy Garden`, `INANIWA YOSUKE`.
- **Its residence test counts `UNIT` as residential.** In Hong Kong, UNIT is how
  commercial space is numbered. All 144 "person-like name at a residential unit"
  hits were mall and office units (`SHOP UNIT LG19, LG/F, THE SOUTHSIDE`).
- **It cannot see a CJK personal name at all.** A Chinese name is two to four
  characters and a Korean one usually three syllables, with no capitals, no
  comma and no space. So on a Chinese-only, Korean or Japanese register its
  **zero is not a finding.**

Until the check has a CJK-aware pass (Seoul's brief already asks for one, and it
belongs in the check rather than here), do what Hong Kong did. Find out whether
the register carries a person's name at all - FEHD's carries the shop sign and
no licensee, which settled Hong Kong structurally. Then read a sample of the
flagged pins in the original script, decide, and record the verdict in
`DECISIONS.md`.

## 6. Display on the map - MEASURED

- **No missing glyphs.** `FONT_STACK` in `pipeline/theme.py` carries Japanese,
  Korean, Traditional and Simplified Chinese faces after the Latin ones, and
  Hong Kong's tooltips rendered Chinese on a real hover with no empty boxes.
  Keep the Latin faces first, as that file's comment explains: browsers fall
  through per glyph, and a CJK face first would restyle every Latin name.
- **But the CJK faces are in Japanese-first order, so Chinese renders in
  Japanese forms.** Han unification gives Chinese and Japanese the same code
  points with different regional glyph standards (`骨` and `直` are the classic
  pairs). A Japanese face draws Hong Kong's shop signs in Japanese shapes, and
  Cantonese characters it lacks (`嘅`, `冇`, `啲`) drop to the next face, so one
  sign can mix two typefaces. It is legible and it is wrong for a Chinese reader.
  **Handed to the Cleanup session 2026-09-24**; the likely fix is a per-map
  language (`zh-HK`, `zh-TW`, `ko`, `ja`) that sets the map's `lang` and orders
  the CJK faces for it. **Before building a CJK city, check whether that has
  landed.** If it has not, Taiwan renders in Japanese forms too; Japan is
  unaffected, and Korean Hangul is unaffected (the Japanese faces lack it) apart
  from any Hanja.
- **Tooltip metrics.** A CJK face changes line height and width; the Hong Kong
  deploy check saw no overflow, but a Chinese-only or Japanese-only register
  puts CJK in every tooltip, so look again.
- **City names on the macro map are English** ("Hong Kong", "Taipei
  (Regional)"). Measure each label's width in the live app's frame with five
  known widths reproduced, as `scripts/check_macro_labels.py` requires.
- **Page text.** Space Grotesk has no CJK. If a page quotes a name in its own
  script, check it in the rendered page.

## Checklist for a CJK city

- [ ] Probes print UTF-8, CSVs are read with `utf-8-sig`, and encodings are never
      judged from console output
- [ ] OSM name-tag coverage printed per tag before choosing; any fallback rule
      counted; unmatched nodes stop the step
- [ ] Operator/OSM name disagreements resolved by an ID, recorded with it
- [ ] Language edition chosen and stated; joins made on identifiers
- [ ] NFKC before every text key; full-width share counted; placeholders found
      in the register's own language
- [ ] Privacy: does the register carry a person's name at all? A sample read in
      the original script, with the verdict recorded - the heuristic's zero is
      not one
- [ ] Font order: has the per-map language landed? If not, say what the reader
      sees
- [ ] Tooltips with CJK hovered in the rendered map, in both themes
