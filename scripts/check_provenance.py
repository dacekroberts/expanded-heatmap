"""Fail when a built city's provenance is not actually recorded.

    python scripts/check_provenance.py [--strict]

WHY THIS EXISTS, AND WHY IT IS A SCRIPT RATHER THAN A PARAGRAPH
---------------------------------------------------------------
`CLAUDE.md` calls `docs/data_sources.md` the only way a build can be
reproduced, and `add-city` Step 0.4 makes recording a source a build
requirement. Both were followed, and both were followed for the US cities
only. Twice:

  - **Canada, 2026-09-21.** Six municipalities built. Their NOTICES went into
    `data_sources.md` the same day, correctly. Their ENDPOINTS did not reach
    the three provenance tables at all, their FEEDS never reached the GTFS
    licence table, and one publisher - the Province of British Columbia, whose
    layer names 30 stations - was never read. Found 2026-09-22, a day later.
  - **Mexico, 2026-09-22.** Mexico City and Guadalajara built. Same omission,
    caught by this script on the day it was written rather than by a reader.

Each time the gap was invisible in exactly the way that matters: **a city whose
provenance is unrecorded looks identical to a city that was checked.** A prose
rule cannot tell those apart. This can.

The thing both misses have in common is that the country was PROFILED before
any of its cities was built, so a whole country's sources arrived through
`add-country` - which writes `docs/<country>_step0_endpoints.md` - and the
per-city step that would have copied them into `data_sources.md` was never the
step anyone was on. So the check is deliberately keyed on the BUILT CITY, not
on the country file.

WHAT IT CHECKS
--------------
  A. Every city in `app/cities.py` has at least one row naming it in each of
     the three provenance tables.
  B. Every URL constant that a city's `pipeline/<slug>/config.py` actually
     resolves to appears verbatim in `data_sources.md`. This is the strongest
     check here and the one that catches a source nobody thought of as a
     source - a naming layer, a parcel join, a geocoder.
  C. `app/components.py`'s `_NOTICES` and `data_sources.md`'s numbered notices
     are in bijection. A required string displayed but unexplained, or
     explained but not displayed, both fail.
  D. Notice numbers are unique and contiguous from 1. They were neither: the
     list carried two item 8s and two item 15s from 2026-09-21 to 2026-09-22,
     because each country's block was appended without renumbering.
  K. Three of `CLAUDE.md`'s invariants that a new city could break silently:

     - **the basemap attribution is on every rendered map, and nothing is
       parked on top of it.** ODbL requires it to stay visible; nothing
       verified it, and it is the one obligation here that is breached by
       OMISSION rather than by a wrong string. Since 2026-09-23 this also
       requires the legend's `bottom` to be clamped against the map's own
       height, because "in the file" and "on the screen" turned out to be
       different questions - the legend covered the credit in every city at
       any viewport taller than the map.
     - **each city's `CRS_PROJECTED` matches its own longitude.** The invariant
       is that the projected CRS is derived per city and NEVER copied, and a
       copied one is invisible: distances come out wrong by a few per cent
       rather than erroring.
     - **each city's map step calls `render_heatmap()` and builds no
       `folium.Map` of its own**, so the shared renderer is not forked.

  J. Every `outputs/...` file NAMED in a page's prose or in the docs exists and
     is committed. These are not files the app opens - it reads one
     `heatmap.html` per city through an iframe - they are **promises to a
     reader**: "the stations excluded are listed in
     `outputs/montreal/excluded_stations.csv`". `outputs/` is committed and
     `data/` is not, so a city added in a hurry can cite a file that never
     leaves the machine it was built on, and nothing about the page looks
     wrong. Clean when written, 17 paths; it exists for the seventeenth city.

  I. Every markdown table in the provenance docs actually renders: no row
     orphaned from its header by intervening prose, and no row whose cell
     count differs from its header's. **Markdown fails silently here** - an
     orphaned row renders as literal pipe-delimited text and looks fine in a
     diff - and it has happened twice: Edmonton's and Toronto's rows were
     orphaned in two tables at once, and Philadelphia's OPA row carried five
     cells against a six-cell header. This check was written inline six times
     during one sweep before being committed, which is the usual sign.

  H. Every relative markdown link in the docs resolves. `vancouver.md` linked
     `[session_roles.md](session_roles.md)` from inside `docs/build_briefs/`,
     which pointed at a sibling that never existed - it needed `../`. Fenced
     code is stripped first, because Overpass QL (`["network"="<Net>"](bbox)`)
     reads exactly like a markdown link and is not one.

  G. Every stored licence in `docs/licenses/` has a SHA-256 listed in that
     directory's README, and it MATCHES. This is a compliance artefact, not
     housekeeping: the hashes exist so the clauses quoted in `data_sources.md`
     are checkable against the text that was actually agreed to, and a stale
     one silently ends that. Two were stale on 2026-09-22 because
     `.gitattributes` sets `* text=auto eol=lf` and git rewrote CRLF to LF
     after the hash was taken - so the recorded digests described bytes that
     existed nowhere. Two more files had no hash at all.

  F. Every `notice N` / `item N` citation of the notices list still points at
     the notice it MEANT. A range check cannot do this: renumbering on
     2026-09-22 moved Edmonton from item 14 to 15, and
     `docs/build_briefs/edmonton.md` went on saying "item 14 carries it" - a
     citation that still RESOLVED, to Calgary. So the check compares the cited
     notice's subject against the subjects named around the citation, and
     fails when the neighbourhood is talking about a different notice's
     subject than the one it cites.

  E. `docs/city_master_list.md`'s built counts match `app/cities.py` - the
     total and the per-country figures. That file is the one place `CLAUDE.md`
     says to READ COUNTS OFF, so its numbers are load-bearing in a way no other
     document's are. A sweep on 2026-09-22 verified them by hand and they were
     right to the entry; this makes that verification repeatable instead of
     annual. **A count in a file whose job is to carry counts gets checked; a
     count anywhere else gets deleted** - which is why this lives here and not
     in `check_stale_claims.py`.

KNOWN_GAPS below is a list of DEFECTS, not exemptions. Entries are dated, the
report prints them loudly, and a stale entry - one naming a city that is now
recorded - fails the check, so the list can only shrink. `--strict` ignores it
entirely and is what CI should run once the list is empty.
"""

import argparse
import ast
import importlib
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

DATA_SOURCES = ROOT / "docs" / "data_sources.md"
CITIES_PY = ROOT / "app" / "cities.py"
COMPONENTS_PY = ROOT / "app" / "components.py"
MASTER_LIST = ROOT / "docs" / "city_master_list.md"
LICENCE_DIR = ROOT / "docs" / "licenses"

# Files whose `item N` citations are checked. DECISIONS.md is excluded for the
# usual reason - it records what a citation said on a date.
CITATION_GLOBS = ("docs/**/*.md", ".claude/**/*.md", "CLAUDE.md", "PLAN.md")
CITATION_SKIP = {"DECISIONS.md"}
# The sweep skill quotes the broken citation as a teaching example, and
# check_provenance's own docstring does the same.
CITATION_SKIP_PATHS = {
    ".claude/skills/consistency-sweep/SKILL.md",
    "scripts/check_provenance.py",
}
# "item N" IS AMBIGUOUS and the first version of this check ignored that. At
# least three numbered namespaces exist: the notices list, the deploy-gate list
# under "What closing this fully requires", and `global_country_shortlist.md`'s
# own "#### Item N" probe sweep. Reporting all of them against the notices list
# produced thirteen "unverifiable" notes, every one of which was a citation of
# a DIFFERENT list - noise that would have taught people to skip the section.
#
# So only two forms are treated as notices citations:
#   - "notice N", which is unambiguous; and
#   - "item N" where the surrounding text also says "notice" or names
#     data_sources.md, which is how a cross-file citation of that list reads.
# Anything else is left alone rather than guessed at.
CITATION_RE = re.compile(r"\b(?:item|notice)s?\s+(\d{1,2})\b", re.I)
NOTICE_WORD_RE = re.compile(r"notice|data_sources", re.I)

# A DOCUMENT THAT DECLARES ITSELF SUPERSEDED IS A TRAIL, NOT A CLAIM, and its
# citations point at the list AS IT WAS. Checking them is the same mistake as
# checking DECISIONS.md, which is skipped two constants above for exactly this
# reason: "it records what a citation said on a date."
#
# Found 2026-09-23 via canada-required-notices.md, whose header reads
# "SUPERSEDED 2026-09-22 ... Where this file and those disagree, those win."
# It cites "Items 9, 10, 14, 16" against the phrase "Four municipal OGLs"
# without naming the four cities, so the subject test could not confirm item 9
# was Vancouver's and reported it unverifiable. The citation is correct; it is
# simply written about a numbering this file no longer governs. Naming the
# cities to satisfy the check would have edited a historical trail to please a
# script - the correction runs the wrong way round.
SUPERSEDED_RE = re.compile(r"^\W*\*{0,2}SUPERSEDED\b", re.I | re.M)
SUPERSEDED_SCAN_CHARS = 600


def declares_itself_superseded(text):
    """Does this document say, up front, that it no longer governs?"""
    return bool(SUPERSEDED_RE.search(text[:SUPERSEDED_SCAN_CHARS]))

# Defects awaiting work, each with the date it was recorded. NOT an allowlist:
# a city here is one whose provenance is missing and known to be missing. Delete
# the entry when the rows land - leaving it stale fails the check.
KNOWN_GAPS = {}

# Slug for a city whose pipeline package is not named after its display name.
SLUG_OVERRIDES = {
    "Vancouver (Regional)": "vancouver",
    "Guadalajara (Regional)": "guadalajara",
    "Miami (Regional)": "miami",
    "Washington D.C.": "washington_dc",
    "Montréal": "montreal",
    "Mexico City": "mexico_city",
}

# A city's rows may name it differently from its page title - Vancouver's are
# filed under "Vancouver" and "Surrey" because the build spans two
# municipalities. Map display name -> the names any of which satisfies a table.
TABLE_ALIASES = {
    "Vancouver (Regional)": ("Vancouver", "Surrey"),
    "Guadalajara (Regional)": ("Guadalajara",),
    "Miami (Regional)": ("Miami",),
    "Washington D.C.": ("Washington D.C.",),
}

# A notice's heading in app/components.py is the publisher's full legal name;
# data_sources.md numbers it by the short name the rest of the file uses. Both
# spellings are deliberate, so the bijection is checked through this map rather
# than by loosening the match until everything passes.
NOTICE_ALIASES = {
    "San Francisco Municipal Transportation Agency": "SFMTA",
    "Chicago Transit Authority": "CTA",
    "OpenStreetMap (Mexican rail)": "OpenStreetMap",
}

# `app/cities.py` splits big countries into regions ("Canada West"); the master
# list groups by country. Strip the direction word to get from one to the other.
REGION_DIRECTIONS = (" West", " East", " North", " South", " Central")

TABLES = (
    ("## Business registries", "business registries"),
    ("## Transit feeds", "transit feeds"),
    ("## Boundary layers", "boundary layers"),
)

# URLs that are deliberately not in data_sources.md, with the reason. Keep this
# tiny; the default answer to "this URL is not recorded" is to record it.
URL_EXEMPT = {
    # Documentation pointers inside config comments, not fetched by the build.
    "https://github.com/dacekroberts/expanded-heatmap",
}


def read(path):
    return path.read_text(encoding="utf-8")


def section(text, heading, headings):
    """Return the slice of `text` under `heading`, up to the next heading."""
    start = text.index(heading)
    later = [text.index(h) for h in headings if text.index(h) > start]
    return text[start:min(later)] if later else text[start:]


def city_names():
    """Parse app/cities.py without importing streamlit."""
    tree = ast.parse(read(CITIES_PY))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "CITIES" for t in node.targets
        ):
            return [
                next(
                    v.value
                    for k, v in zip(d.keys, d.values)
                    if getattr(k, "value", None) == "name"
                )
                for d in node.value.elts
            ]
    sys.exit("check_provenance: could not find CITIES in app/cities.py")


def resolved_urls(slug):
    """Import a city's config and collect every http(s) URL it resolves to.

    Importing rather than grepping is the point: Vancouver builds four of its
    endpoints from an `_ODS` prefix via f-strings, so the literal never appears
    in the file and a grep would report them absent.
    """
    try:
        mod = importlib.import_module(f"pipeline.{slug}.config")
    except Exception as exc:                                  # noqa: BLE001
        return None, f"could not import pipeline.{slug}.config: {exc}"
    urls = set()

    def walk(value):
        if isinstance(value, str):
            if value.startswith("http"):
                urls.add(value)
        elif isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, (list, tuple, set, frozenset)):
            for v in value:
                walk(v)

    for name in dir(mod):
        if not name.startswith("_"):
            walk(getattr(mod, name))
    return urls, None


def notice_headings(doc):
    """(number, heading) for each numbered notice in data_sources.md."""
    sec = doc[doc.index("## Notices this project MUST display when published"):]
    out = []
    for m in re.finditer(r"^\*\*(\d+)\.\s+(.+?)\s+—", sec, re.M):
        out.append((int(m.group(1)), m.group(2).strip().strip("*")))
    return out


def displayed_notices():
    """Headings in app/components.py's _NOTICES, read as source, not imported."""
    src = read(COMPONENTS_PY)
    start = src.index("_NOTICES")
    end = src.index("def ", start)
    return re.findall(r'^\s{4}\("([^"]+)"', src[start:end], re.M)


# 326xx WGS84 UTM north, 258xx ETRS89 UTM, 269xx NAD83 UTM, 327xx WGS84 south.
UTM_FAMILIES = (326, 327, 258, 269)

# A national grid is admitted where the country publishes its data in one and a
# UTM zone would mean transforming OUT of the CRS the publisher measured in.
# This is not a relaxation: each entry still has to contain the city's own
# longitude, so a copied CRS fails here exactly as it does for UTM. What it
# stops asserting is that "projected metres" must always mean "UTM", which was
# only ever true of the cities built so far.
#
# Add an entry only with the evidence that the SOURCES ship in it - not because
# a national grid exists. Ireland qualifies because both Tailte Eireann's
# valuation register (Xitm/Yitm) and its boundary layer (wkid 2157) are already
# EPSG:2157, and Dublin sits within a quarter-degree of UTM zone 29's eastern
# edge, where that zone's distortion is worst.
NATIONAL_GRIDS = {
    2157: ("Irish Transverse Mercator", -11.0, -5.0),   # Ireland
    # METROPOLITAN France only. The domain is deliberately tight: SIRENE's
    # geolocation file carries a PER-ROW `epsg` column holding 2154 alongside
    # 2975 (Réunion), 5490 (Antilles) and 2972 (Guyane), so a French build that
    # hard-codes 2154 works in Paris and puts every pin in the sea in
    # Fort-de-France - without raising. These bounds are what raises.
    2154: ("Lambert-93", -5.5, 10.0),                   # France (métropole)
}


def check_invariants(names, lons):
    """K: three CLAUDE.md invariants a new city could break silently."""
    problems = []

    # 1. ODbL: the basemap credit must be on every rendered map - PRESENT,
    #    LINKED, and NOT UNDERNEATH THE LEGEND.
    #
    #    The third clause was added 2026-09-23. Until then this checked only
    #    that the credit was in the file, and it was: in every city, at every
    #    viewport taller than the map, the legend covered it completely. The
    #    file said "visible" and the render said otherwise, which is the exact
    #    shape of failure the rest of this script exists to catch.
    #
    #    Layout cannot be measured by reading HTML, so this does not try. What
    #    it checks is that the MECHANISM is present: the legend is
    #    position:fixed against the viewport's bottom edge while the credit is
    #    absolutely positioned against the MAP's, so the legend's `bottom` has
    #    to be clamped against the map's own height or the two collide as soon
    #    as the frame is taller than the map. Both numbers are read out of the
    #    same committed file, so this compares the map that shipped against the
    #    clamp that shipped with it. The real measurement is
    #    scripts/check_map_attribution.js, which hit-tests a rendered map at
    #    several viewport heights - but that one needs a browser and an agent,
    #    and CLAUDE.md says to skip deploy-verify for pipeline-only work.
    #    pipeline/map_common.py IS pipeline-only work, so without this half the
    #    only check that sees the regression is the one the rules say not to
    #    run.
    #
    #    A LOOP OVER NOTHING PASSES ALL THREE CLAUSES. Clause 3 below is
    #    anchored to `names` - a city with no map script fails - but this one
    #    had no anchor, so a renamed map file or a moved outputs/ would have
    #    reported every map credited, linked and clear having read none. Found
    #    2026-09-23 when the third clause was handed over; the same hole was
    #    closed that day in check_scope_disclosure.py, and is the one
    #    check_no_fetch_in_steps_selftest.py calls "a glob that matches nothing".
    maps = sorted(ROOT.glob("outputs/*/heatmap.html"))
    if not maps:
        problems.append(
            "outputs/*/heatmap.html matched NO files, so the basemap-credit "
            "clauses examined nothing and would otherwise pass. If the maps "
            "moved or were renamed, point this glob at them")
    for html in maps:
        text = html.read_text(encoding="utf-8", errors="replace")
        rel = html.relative_to(ROOT).as_posix()
        if "OpenStreetMap" not in text:
            problems.append(f"{rel}: no OpenStreetMap attribution - ODbL "
                            f"requires it to stay visible")
        elif "openstreetmap.org/copyright" not in text.lower():
            problems.append(f"{rel}: attribution present but not linked to "
                            f"the OSM copyright page")

        map_h = re.search(r"#map_\w+\s*\{[^}]*?height:\s*([\d.]+)px", text)
        legend_bottom = re.search(
            r'class="map-legend"[^>]*style="[^"]*?bottom:\s*([^;]+);', text, re.S)
        if not map_h or not legend_bottom:
            problems.append(
                f"{rel}: cannot find the map's height and the legend's bottom "
                f"offset, so the basemap credit's clearance is unverifiable. "
                f"If the legend or the map container was restructured, update "
                f"this check with it - do not delete it")
        else:
            want = f"max(24px, calc(100vh - {int(float(map_h.group(1))) - 24}px))"
            got = " ".join(legend_bottom.group(1).split())
            if got != want:
                problems.append(
                    f"{rel}: the legend's bottom is '{got}', not '{want}'. The "
                    f"legend is fixed to the VIEWPORT's bottom edge and the "
                    f"OSM credit sits at the MAP's, so an unclamped offset "
                    f"puts the credit under the legend at every frame taller "
                    f"than the map - measured 5/5 covered at 1024x768 on "
                    f"2026-09-23. See _LEGEND_BOTTOM_CSS in "
                    f"pipeline/map_common.py, and re-render this city")

    # 2. The projected CRS is derived per city, never copied.
    for name in names:
        slug = SLUG_OVERRIDES.get(name, name.lower().replace(" ", "_"))
        cfg = ROOT / "pipeline" / slug / "config.py"
        lon = lons.get(name)
        if not cfg.exists() or lon is None:
            continue
        m = re.search(r"CRS_PROJECTED\s*=\s*[\"']EPSG:(\d+)[\"']", read(cfg))
        if not m:
            continue
        epsg = int(m.group(1))
        family, zone = divmod(epsg, 100)
        implied = int((lon + 180) // 6) + 1
        if epsg in NATIONAL_GRIDS:
            grid, west, east = NATIONAL_GRIDS[epsg]
            if not west <= lon <= east:
                problems.append(
                    f"{slug}: CRS_PROJECTED EPSG:{epsg} is {grid}, whose "
                    f"domain is {west} to {east}, but longitude {lon:.2f} is "
                    f"outside it - a national grid is still per-city")
        elif family not in UTM_FAMILIES:
            problems.append(f"{slug}: CRS_PROJECTED EPSG:{epsg} is not a UTM "
                            f"zone and not a documented national grid - the "
                            f"invariant is per-city projected metres")
        elif zone != implied:
            problems.append(
                f"{slug}: CRS_PROJECTED EPSG:{epsg} is UTM zone {zone}, but "
                f"longitude {lon:.2f} implies zone {implied} - a copied CRS "
                f"does not error, it just measures wrong")

    # 3. The shared renderer is not forked.
    steps = sorted(ROOT.glob("pipeline/*/step[34]_map.py"))
    seen = {s.parent.name for s in steps}
    for s in steps:
        text = read(s)
        rel = s.relative_to(ROOT).as_posix()
        if "render_heatmap" not in text:
            problems.append(f"{rel}: does not call render_heatmap()")
        if "folium.Map(" in text:
            problems.append(f"{rel}: builds its own folium.Map - "
                            f"pipeline/map_common.py is the shared renderer")
    for name in names:
        slug = SLUG_OVERRIDES.get(name, name.lower().replace(" ", "_"))
        if (ROOT / "pipeline" / slug).is_dir() and slug not in seen:
            problems.append(f"pipeline/{slug}: no step3_map.py or step4_map.py")
    return problems


def check_cited_outputs():
    """J: outputs/ files promised in prose exist and are committed."""
    import subprocess
    try:
        tracked = set(subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True,
            text=True, check=True).stdout.split("\n"))
    except (OSError, subprocess.CalledProcessError):
        return ["could not run `git ls-files` to check what is committed"]

    cited = {}
    globs = ("app/**/*.py", "docs/**/*.md", "CLAUDE.md")
    for g in globs:
        for q in sorted(ROOT.glob(g)):
            # DECISIONS.md is excluded everywhere for the same reason; a past
            # entry may name a file that has since been renamed, and that is
            # an accurate record rather than a broken promise.
            if not q.is_file() or q.name == "DECISIONS.md":
                continue
            for m in re.finditer(r"outputs/[A-Za-z0-9_./-]+\.(?:csv|html|json)",
                                 read(q)):
                cited.setdefault(m.group(0), set()).add(
                    q.relative_to(ROOT).as_posix())

    problems = []
    for path in sorted(cited):
        where = sorted(cited[path])[:2]
        if not (ROOT / path).exists():
            problems.append(f"{path}: named in {where} but does not exist")
        elif path not in tracked:
            problems.append(
                f"{path}: named in {where}, exists locally but is NOT "
                f"committed - a reader cloning this repository will not find "
                f"it")
    return problems


TABLE_DOCS = ("docs/data_sources.md", "docs/excluded_categories.md",
              "docs/city_master_list.md", "docs/session_roles.md")


def check_tables():
    """I: markdown tables that do not render, or whose rows are ragged."""
    delim = re.compile(r"^\|[\s:|-]+\|\s*$")
    problems = []
    for rel in TABLE_DOCS:
        q = ROOT / rel
        if not q.exists():
            continue
        lines = read(q).split("\n")
        cols = None
        in_fence = False
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if not line.startswith("|"):
                if not line.strip():
                    cols = None        # a blank line ends a table
                continue
            n = line.count("|") - 1
            if delim.match(line):
                cols = n
                continue
            if cols is None:
                # A HEADER row sits immediately above its own delimiter, so at
                # this point it legitimately has no width yet. Look ahead one
                # line before calling it orphaned - the inline version of this
                # check flagged every header in the file.
                nxt = lines[i] if i < len(lines) else ""
                if delim.match(nxt):
                    continue
                problems.append(
                    f"{rel}:{i}: table row with no header above it in the "
                    f"same block - renders as literal text")
            elif n != cols:
                problems.append(
                    f"{rel}:{i}: row has {n} cells, its header has {cols}")
    return problems


# THIS REPOSITORY'S OWN FILES, AND NOTHING ELSE UNDER ITS ROOT.
#
# `.claude/**/*.md` reaches into `.claude/worktrees/<session>/`, and a sibling
# session's worktree contains its own `.venv-lean`. That is how this check came
# to report a broken link in **Streamlit's bundled documentation** - a file
# belonging to a dependency, inside another session's working copy, which this
# project neither wrote nor can fix. A checker that reports other people's
# files trains you to skim its output.
_NOT_OURS = ("/worktrees/", "/site-packages/", "/node_modules/",
             "/.venv", "/__pycache__/")


def ours(path):
    rel = "/" + path.relative_to(ROOT).as_posix()
    return not any(seg in rel for seg in _NOT_OURS)


def check_links():
    """H: relative markdown links that do not resolve."""
    fence = re.compile(r"```.*?```", re.S)
    inline = re.compile(r"`[^`\n]*`")
    link = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    problems = []
    seen = set()
    for g in ("docs/**/*.md", ".claude/**/*.md", "*.md"):
        for q in sorted(ROOT.glob(g)):
            if not q.is_file() or not ours(q) or q.resolve() in seen:
                continue
            seen.add(q.resolve())
            text = read(q)
            # Fenced blocks and inline code are not prose; a query that looks
            # like a link is not a link.
            text = inline.sub(" ", fence.sub(" ", text))
            for m in link.finditer(text):
                tgt = m.group(1).split("#")[0].strip()
                if not tgt or tgt.startswith(("http://", "https://",
                                              "mailto:", "<")):
                    continue
                if not (q.parent / tgt).resolve().exists():
                    problems.append(
                        f"{q.relative_to(ROOT).as_posix()}: "
                        f"link to '{tgt}' does not resolve")
    return problems


def check_licence_hashes():
    """G: docs/licenses/ SHA-256s against the files as committed."""
    import hashlib
    readme = LICENCE_DIR / "README.md"
    if not readme.exists():
        return ["docs/licenses/README.md not found"]
    m = re.search(r"## SHA-256, as retrieved.*?```\n(.*?)```",
                  read(readme), re.S)
    if not m:
        return ["no '## SHA-256, as retrieved' block in docs/licenses/README.md"]
    listed = {}
    for line in m.group(1).strip().split("\n"):
        parts = line.split()
        if len(parts) == 2:
            listed[parts[1]] = parts[0]

    problems = []
    on_disk = {q.name: q for q in LICENCE_DIR.iterdir()
               if q.is_file() and q.name != "README.md" and q.suffix != ".md"}
    for name, digest in sorted(listed.items()):
        q = on_disk.get(name)
        if q is None:
            problems.append(f"{name}: hash listed but the file is gone")
            continue
        # HASH WHAT GIT STORES, NOT WHAT IS ON DISK.
        #
        # docs/licenses/README.md says to compute these "from the COMMITTED
        # file, never from the file you just fetched", because `.gitattributes`
        # sets `* text=auto eol=lf` and git rewrites CRLF on the way in. This
        # check used to read the working tree, which contradicts that on any
        # checkout where a file sits with CRLF - and one does:
        # `cta-developer-license-agreement.html` is 230,064 bytes committed and
        # 232,828 on a Windows working tree. The listed hash was RIGHT and the
        # checker was wrong, which is the worse way round, because the message
        # it printed told you to go and change the correct value.
        raw = q.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if actual != digest:
            normalised = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
            if normalised == digest:
                continue
            problems.append(
                f"{name}: listed {digest[:16]}... but the file hashes to "
                f"{actual[:16]}... ({normalised[:16]}... with CRLF normalised) "
                f"- recompute from the COMMITTED file, not the one you just "
                f"fetched (.gitattributes normalises CRLF)")
    for name in sorted(set(on_disk) - set(listed)):
        problems.append(f"{name}: stored licence with NO hash listed")
    return problems


def notice_subjects(doc):
    """{number: [keyword, ...]} for the notices list.

    The keyword is what a document talking ABOUT that notice would say -
    "Edmonton" rather than "City of Edmonton", "British Columbia" rather than
    "Province of British Columbia".
    """
    out = {}
    for n, heading in notice_headings(doc):
        h = heading.strip().strip("*")
        for prefix in ("City of ", "Province of ", "Ville de ",
                       "Soci\u00e9t\u00e9 de transport de ", "Ayuntamiento de "):
            if h.startswith(prefix):
                h = h[len(prefix):]
        h = re.sub(r"\s*\(.*?\)", "", h).strip()
        if h:
            out[n] = h
    return out


def check_citations(doc):
    """F: does each `item N` still point at the notice it meant?"""
    subjects = notice_subjects(doc)
    if not subjects:
        return [], []
    hard, soft = [], []
    superseded = []
    for g in CITATION_GLOBS:
        for p in sorted(ROOT.glob(g)):
            if not p.is_file() or not ours(p) or p.name in CITATION_SKIP:
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel in CITATION_SKIP_PATHS:
                continue
            text = read(p)
            # A trail, not a claim - see declares_itself_superseded().
            if declares_itself_superseded(text):
                superseded.append(rel)
                continue
            for m in CITATION_RE.finditer(text):
                n = int(m.group(1))
                cited = m.group(0).lower()
                lo = max(0, m.start() - 400)
                window = text[lo:m.end() + 400] + " " + p.stem.replace("_", " ")
                # Disambiguate the namespace before judging the number.
                if not cited.startswith("notice"):
                    # Three other namespaces say "item N" within a sentence
                    # that also names data_sources.md, so the window test
                    # alone is not enough: "Gate item 9" is the deploy-gate
                    # list, "Step 0 item 4" is add-city's, and "#### Item 2"
                    # is a heading in another document's own sweep.
                    before = text[max(0, m.start() - 12):m.start()].lower()
                    if before.endswith("gate ") or before.endswith("step 0 "):
                        continue
                    line_start = text.rfind(chr(10), 0, m.start()) + 1
                    if text[line_start:m.start()].strip().startswith("#"):
                        continue
                    near = text[max(0, m.start() - 120):m.end() + 120]
                    if not NOTICE_WORD_RE.search(near):
                        continue        # some other list's item N
                if n not in subjects:
                    hard.append(f"{rel}: cites item {n}, but the notices list "
                                f"stops at {max(subjects)}")
                    continue
                wl = window.lower()
                here = subjects[n].lower()
                if here in wl:
                    continue                      # cites its own subject: fine
                others = sorted({s for k, s in subjects.items()
                                 if k != n and s.lower() in wl and len(s) > 4})
                if others:
                    hard.append(
                        f"{rel}: cites item {n} ({subjects[n]}), but the text "
                        f"around it names {others} and never {subjects[n]!r}")
                else:
                    soft.append(f"{rel}: item {n} ({subjects[n]}) - nothing "
                                f"nearby names it, so it cannot be verified")
    return hard, soft


def check_master_list(names, regions):
    """E: city_master_list.md's built counts against app/cities.py."""
    if not MASTER_LIST.exists():
        return ["docs/city_master_list.md not found"]
    doc = read(MASTER_LIST)
    problems = []

    m = re.search(r"^##\s+Built\s*[\u2014-]\s*(\d+)", doc, re.M)
    if not m:
        return ["no '## Built - N' heading to check against"]
    claimed_total = int(m.group(1))
    if claimed_total != len(names):
        problems.append(
            f"'## Built - {claimed_total}' but app/cities.py has {len(names)}")

    # per-country: "| **Canada** (5, complete) | ... |"
    actual = {}
    for r in regions:
        country = r
        for d in REGION_DIRECTIONS:
            if country.endswith(d):
                country = country[: -len(d)]
                break
        actual[country] = actual.get(country, 0) + 1

    seen = set()
    for row in re.finditer(r"^\|\s*\*\*([^*]+)\*\*\s*\((\d+)", doc, re.M):
        country, claimed = row.group(1).strip(), int(row.group(2))
        if country not in actual:
            continue
        seen.add(country)
        if claimed != actual[country]:
            problems.append(
                f"'{country} ({claimed})' but app/cities.py has "
                f"{actual[country]}")
    for country, n in sorted(actual.items()):
        if country not in seen:
            problems.append(
                f"'{country}' has {n} cities in app/cities.py and no counted "
                f"row in the built table")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="ignore KNOWN_GAPS and fail on every finding")
    args = ap.parse_args()

    doc = read(DATA_SOURCES)
    headings = [h for h, _ in TABLES] + ["## Geocoding"]
    blocks = {label: section(doc, h, headings) for h, label in TABLES}

    failures, gaps = [], []
    names = city_names()
    print(f"check_provenance: {len(names)} cities in app/cities.py\n")

    # --- A + B, per city ---------------------------------------------------
    for name in names:
        known = name in KNOWN_GAPS and not args.strict
        problems = []

        for alias_source in (TABLE_ALIASES.get(name, (name,)),):
            for label in blocks:
                if not any(
                    re.search(r"^\|\s*\**" + re.escape(a), blocks[label], re.M)
                    for a in alias_source
                ):
                    problems.append(f"no row in {label}")

        slug = SLUG_OVERRIDES.get(name, name.lower().replace(" ", "_"))
        urls, err = resolved_urls(slug)
        if err:
            problems.append(err)
        else:
            # Compare percent-DECODED, both sides. San Francisco's boundary
            # endpoint resolves to `county%3D%27San%20Francisco%27` while
            # data_sources.md records the readable `county='San Francisco'`.
            # Those are the same request and a raw string compare calls them
            # different.
            doc_plain = unquote(doc)
            missing = sorted(
                u for u in urls
                if u not in URL_EXEMPT
                and u not in doc and unquote(u) not in doc_plain
            )
            problems += [f"endpoint not in data_sources.md: {u}"
                         for u in missing]

        if problems:
            (gaps if known else failures).append((name, problems))
        else:
            if name in KNOWN_GAPS and not args.strict:
                failures.append((name, [
                    "listed in KNOWN_GAPS but nothing is missing - delete the "
                    "entry; the list may only shrink"]))
            else:
                print(f"  OK   {name}")

    # --- C + D, notices ----------------------------------------------------
    numbered = notice_headings(doc)
    nums = [n for n, _ in numbered]
    doc_headings = {h for _, h in numbered}
    shown = displayed_notices()

    if nums != list(range(1, len(nums) + 1)):
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        failures.append(("notices", [
            f"numbers are not unique and contiguous from 1: {nums}"
            + (f" (duplicates: {dupes})" if dupes else "")]))

    for h in shown:
        candidate = NOTICE_ALIASES.get(h, h)
        if not any(candidate in dh or dh in candidate for dh in doc_headings):
            failures.append(("notices", [
                f"'{h}' is DISPLAYED in app/components.py but has no numbered "
                f"item in data_sources.md"]))

    print(f"\n  notices: {len(numbered)} numbered, {len(shown)} displayed")

    # --- E, the master list's own counts -------------------------------------
    regions = []
    tree = ast.parse(read(CITIES_PY))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t_, "id", None) == "CITIES" for t_ in node.targets):
            for d in node.value.elts:
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(d.keys, d.values)}
                if pairs.get("region"):
                    regions.append(pairs["region"])
    ml = check_master_list(names, regions)
    if ml:
        failures.append(("city_master_list.md", ml))
    else:
        print("  master list: built counts agree with app/cities.py")

    # --- F, numbered citations still pointing where they meant ---------------
    hard, soft = check_citations(doc)
    if hard:
        failures.append(("numbered citations", hard))
    else:
        print(f"  citations: every `item N` resolves to the notice it names "
              f"({len(soft)} unverifiable)")
    for s in soft:
        print(f"      note: {s}")

    # --- K, invariants a new city could break silently ------------------------
    # `ast.literal_eval`, NOT `node.value` - a negative number is a UnaryOp
    # wrapping a Constant, so `getattr(v, "value", None)` returns None for
    # every western longitude in the file. The first version of this did that
    # and parsed ZERO of sixteen, so the CRS limb below examined nothing while
    # reporting success. Caught by negative-testing the limb rather than by
    # reading it.
    lons = {}
    for node in ast.parse(read(CITIES_PY)).body:
        if isinstance(node, ast.Assign) and any(
                getattr(t_, "id", None) == "CITIES" for t_ in node.targets):
            for d in node.value.elts:
                pairs = {}
                for k, v in zip(d.keys, d.values):
                    key = getattr(k, "value", None)
                    try:
                        pairs[key] = ast.literal_eval(v)
                    except (ValueError, TypeError, SyntaxError):
                        pairs[key] = None
                if pairs.get("name") is not None and pairs.get("lon") is not None:
                    lons[pairs["name"]] = float(pairs["lon"])
    if len(lons) != len(names):
        # A limb that silently examines nothing is worse than one that fails.
        failures.append(("CLAUDE.md invariants", [
            f"read a longitude for only {len(lons)} of {len(names)} cities in "
            f"app/cities.py - the CRS check cannot run"]))
    inv = check_invariants(names, lons)
    if inv:
        failures.append(("CLAUDE.md invariants", inv))
    else:
        print("  invariants: OSM attribution on every map; every CRS matches "
              "its longitude; no map step forks the renderer")

    # --- J, outputs/ files promised in prose ---------------------------------
    cited = check_cited_outputs()
    if cited:
        failures.append(("cited outputs", cited))
    else:
        print("  outputs: every outputs/ file named in prose exists and is "
              "committed")

    # --- I, tables that actually render ---------------------------------------
    tbl = check_tables()
    if tbl:
        failures.append(("markdown tables", tbl))
    else:
        print("  tables: every row sits under a header and matches its width")

    # --- H, relative links in the docs ---------------------------------------
    links = check_links()
    if links:
        failures.append(("markdown links", links))
    else:
        print("  links: every relative markdown link resolves")

    # --- G, the licence store's own integrity -------------------------------
    lic = check_licence_hashes()
    if lic:
        failures.append(("docs/licenses", lic))
    else:
        print("  licences: every stored licence's SHA-256 matches")

    # --- report ------------------------------------------------------------
    if gaps:
        print("\n" + "=" * 70)
        print("OPEN GAPS - these are DEFECTS, not exemptions. Fix and delete")
        print("the KNOWN_GAPS entry. Run with --strict to fail on them.")
        print("=" * 70)
        for name, problems in gaps:
            print(f"\n  {name}  [{KNOWN_GAPS[name]}]")
            for p in problems:
                print(f"      - {p}")

    if failures:
        print("\n" + "=" * 70)
        print("FAILED")
        print("=" * 70)
        for name, problems in failures:
            print(f"\n  {name}")
            for p in problems:
                print(f"      - {p}")
        print("\nA city whose provenance is unrecorded looks exactly like a "
              "city that was checked.\nThat is what this script exists to "
              "tell apart. Record the source; do not\nrelax the check.")
        return 1

    print("\nAll recorded." if not gaps else
          "\nNo new failures, but the open gaps above are still open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
