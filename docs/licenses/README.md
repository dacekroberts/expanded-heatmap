# Stored licence texts

Local copies of the licence and terms documents this project relies on. Every
transit agency here reserves the right to alter or revoke its terms **without
notice**, so a URL alone does not preserve what was actually agreed to. The
clauses quoted in [`../data_sources.md`](../data_sources.md) are checkable
against these files.

**Position on storing them** (decided 2026-09-21, recorded in
[`../../DECISIONS.md`](../../DECISIONS.md)): each file is kept **unaltered,
non-commercially, for compliance reference**. These are the agencies' own
copyrighted documents, not this project's, and nothing here is republished —
the repository is the archive, not a distribution channel. Save fetched files
as-is; do not transcribe, reformat or trim them.

| File | Agency / row in `data_sources.md` | Source URL | Retrieved |
|---|---|---|---|
| `mbta-massdot-develop-license-agreement.pdf` | **MBTA / MassDOT** (Boston) | `https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf` | 2026-09-21 |
| `sfmta-transit-data-license-agreement.html` | **SFMTA** (San Francisco) | `https://www.sfmta.com/reports/gtfs-transit-data` | 2026-09-21 |
| `la-metro-terms-conditions.html` | **LA Metro** (Los Angeles) | `https://developer.metro.net/terms-conditions/` | 2026-09-21 |
| `cta-developer-license-agreement.html` | **CTA** (Chicago) | `https://www.transitchicago.com/developers/terms/` | 2026-09-21 |
| `mta-terms-and-conditions.txt` | **MTA** (New York) | `https://new.mta.info/developers/terms-and-conditions` | 2026-09-21 |
| `septa-license-agreement.html` | **SEPTA** (Philadelphia) | `https://wwww.septa.org/license-agreement/` | 2026-09-21 |
| `wmata-transit-data-terms-of-use.html` | **WMATA** (Washington D.C.) — *not yet a row; D.C. is unbuilt* | `https://developer.wmata.com/license` | 2026-09-21 |

## SHA-256, as retrieved

```
03171dc15145af12c15781d121df4bac9713d025d57b919ae4798bdfb7acb473  cta-developer-license-agreement.html
aaf555af500679ae73f72d5495896ed27f9bf51c75f922c08a24bdc13b2860ac  la-metro-terms-conditions.html
e791e24e86b9e974de060c3b238abfc392260cad54ccc0d2d3d4f0a61846b91a  mbta-massdot-develop-license-agreement.pdf
6aa68ab9d19242d275fda71f36e2cb3165d23d545eb5494a9bea9597439ae746  mta-terms-and-conditions.txt
f7c07583af9880189c1df55fac2349378dc659016b7ce927dbd3f2900c3c220a  septa-license-agreement.html
ad6db26b111e58813aa41747c4b958d844befc664609cc7e2147b955a12c04b8  sfmta-transit-data-license-agreement.html
9df073bf2819a257e44cd9ad7961cac9d418c7fc4e100a625c8e4605dff516d3  wmata-transit-data-terms-of-use.html
```

Re-fetch and compare to detect a changed agreement. The HTML files are whole
pages, so an unrelated site redesign changes the hash without changing the
terms — a hash mismatch means *read it again*, not *the terms changed*.

## Two files are not raw fetches, and why

- **`mta-terms-and-conditions.txt`** is a rendered-text capture. `mta.info`
  returns HTTP 403 to curl even with full browser headers, so the page was read
  in the browser pane and its text copied unaltered. The file says so at the
  top.
- **`mbta-massdot-develop-license-agreement.pdf`** is the raw PDF, but reaching
  it needed the browser: `mass.gov` also 403s automated fetches.

## Retrieval gotchas worth keeping

- **SEPTA's host really is `wwww.septa.org`, with four w's.** It is not a typo
  in their repo README, as `data_sources.md` previously recorded — SEPTA serves
  both `www` and `wwww`, each returning 200 independently with no redirect.
- **SFMTA's licence page is `/reports/gtfs-transit-data`.** The plausible
  `/reports-documents/gtfs-transit-data` is a 404. The agreement text sits
  inline on the page above the download link; there is no separate document.
- **MTA's landing page is not its terms.** `mta.info/developers` carries the
  "Our data feeds are free to use" line; the actual obligations are at
  `/developers/terms-and-conditions`, and they are substantive.
