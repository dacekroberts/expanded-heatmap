"""Fail when a built city's provenance is not recorded.

    python scripts/check_provenance.py [--strict]

WHY A SCRIPT RATHER THAN A RULE
-------------------------------
`CLAUDE.md` makes `docs/data_sources.md` the only record a build can be
reproduced from, and `add-city` Step 0.4 requires every source to be recorded there.
**A city whose provenance is unrecorded looks identical to a city that was
checked**, and a prose rule cannot tell the two apart. Canada (2026-09-21)
and Mexico (2026-09-22) both shipped with endpoints unrecorded.

Both times the country was profiled before any of its cities was built, so
its sources arrived through `add-country` (which writes
`docs/<country>_step0_endpoints.md`) and the per-city step that copies them
into `data_sources.md` was skipped. The check is therefore keyed on the BUILT
CITY, not on the country file.

WHAT IT CHECKS
--------------
  A. Every city in `app/cities.py` has at least one row naming it in each of
     the three provenance tables.
  B. Every URL constant a city's `pipeline/<slug>/config.py` resolves to
     appears verbatim in `data_sources.md`. The strongest check here: it
     catches sources nobody thought of as sources (a naming layer, a parcel
     join, a geocoder).
  C. `app/components.py`'s `_NOTICES` and `data_sources.md`'s numbered notices
     are in bijection. A required string displayed but unexplained, or
     explained but not displayed, fails.
  D. Notice numbers are unique and contiguous from 1. Appending a country's
     block without renumbering once left two item 8s and two item 15s.
  L. A notice BUILT from config credits every file the city reads. Tokyo's
     (notice 56) comes from `pipeline/tokyo/credits.py`, one entry per file
     its ward roster reads; a roster file without a credit (a ward switched
     on later) fails, as does a credit for a file no longer read.
  M. A licence that prescribes its credit WORD FOR WORD is quoted on every
     page of that country. INSEE permits reuse only « sous la forme « Source :
     Insee » »; Paris, Marseille, Toulouse, Lille and Rennes shipped without
     that string until 2026-09-30. The page is parsed, not grepped: only a
     literal passed to an `st.*` call counts (a comment quoting it does not),
     and not one inside an if/try block, where a missing provenance file
     could drop it.
  K. Three `CLAUDE.md` invariants a new city could break silently:

     - **The basemap attribution is on every rendered map, and nothing sits
       on top of it.** ODbL requires it to stay visible, and it is the one
       obligation here breached by OMISSION rather than by a wrong string.
       Since 2026-09-23 the legend's `bottom` must also be clamped against
       the map's own height: unclamped, the legend covered the credit in
       every city at any viewport taller than the map.
     - **Each city's `CRS_PROJECTED` matches its own longitude.** The
       projected CRS is derived per city and NEVER copied; a copied one does
       not error, it measures distances wrong by a few per cent.
     - **Each city's map step calls `render_heatmap()` and builds no
       `folium.Map` of its own**, so the shared renderer is not forked.

  J. Every `outputs/...` file NAMED in a page's prose or in the docs exists and
     is committed. The app reads only one `heatmap.html` per city; these
     files are **promises to a reader** ("the stations excluded are listed in
     `outputs/montreal/excluded_stations.csv`"). `outputs/` is committed and
     `data/` is not, so a page can cite a file that never leaves the machine
     it was built on, and nothing about the page looks wrong.

  I. Every markdown table in the provenance docs renders: no row orphaned
     from its header by intervening prose, and no row whose cell count
     differs from its header's. **Markdown fails silently here**: an orphaned
     row renders as literal pipe-delimited text and looks fine in a diff.
     Seen twice: Edmonton's and Toronto's rows orphaned in two tables, and
     Philadelphia's OPA row with five cells under a six-cell header.

  H. Every relative markdown link in the docs resolves (a brief in
     `docs/build_briefs/` once linked a sibling that needed `../`). Fenced
     code is stripped first, because Overpass QL (`["network"="<Net>"](bbox)`)
     reads like a markdown link and is not one.

  G. Every stored licence in `docs/licenses/` has a SHA-256 listed in that
     directory's README, and it MATCHES. A compliance record, not
     housekeeping: the hashes make the clauses quoted in `data_sources.md`
     checkable against the text actually agreed to. `.gitattributes` sets
     `* text=auto eol=lf`, so a hash taken before git rewrote CRLF to LF
     describes bytes that exist nowhere (two were stale on 2026-09-22).

  F. Every `notice N` / `item N` citation of the notices list still points at
     the notice it MEANT. A range check cannot do this: renumbering on
     2026-09-22 moved Edmonton from item 14 to 15, and
     `docs/build_briefs/edmonton.md` went on saying "item 14 carries it", a
     citation that still RESOLVED, to Calgary. So the check compares the
     cited notice's subject with the subjects named around the citation, and
     fails when they name a different notice's subject.

  E. `docs/city_master_list.md`'s built counts (the total and per country)
     match `app/cities.py`. `CLAUDE.md` says to READ COUNTS OFF that file, so
     its numbers are load-bearing. **A count in a file whose job is to carry
     counts gets checked; a count anywhere else gets deleted**, which is why
     this lives here and not in `check_stale_claims.py`.

KNOWN_GAPS below is a list of DEFECTS, not exemptions. Entries are dated, the
report prints them loudly, and a stale entry (a city that is now recorded)
fails the check, so the list can only shrink. `--strict` ignores it entirely
and is what CI should run once the list is empty.
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
# Split by country 2026-09-27. The entry point keeps the preamble, the numbered
# notices and the deploy gate; each country's rows of the three provenance
# tables, and every section about its cities' sources, live in
# docs/data_sources/<country>.md under the same headings. A and B read the
# entry point and every country file together; C, D and F read the notices,
# which are in the entry point only.
DATA_SOURCES_DIR = ROOT / "docs" / "data_sources"
CITIES_PY = ROOT / "app" / "cities.py"
COMPONENTS_PY = ROOT / "app" / "components.py"
MASTER_LIST = ROOT / "docs" / "city_master_list.md"
LICENCE_DIR = ROOT / "docs" / "licenses"

# Files whose `item N` citations are checked. DECISIONS.md is excluded for the
# usual reason - it records what a citation said on a date.
CITATION_GLOBS = ("docs/**/*.md", ".claude/**/*.md", "CLAUDE.md", "PLAN.md")
CITATION_SKIP = {"DECISIONS.md"}


def is_decisions_log(p):
    """Return True for DECISIONS.md, its weekly archives (docs/decisions/) and
    the build sessions' drafts files (docs/decisions_drafts/): the same dated
    record, excluded for the same reason wherever it sits."""
    return p.name == "DECISIONS.md" or p.parent in (ROOT / "docs" / "decisions",
                                                    ROOT / "docs" / "decisions_drafts")
# The sweep skill quotes the broken citation as a teaching example, and
# check_provenance's own docstring does the same.
CITATION_SKIP_PATHS = {
    ".claude/skills/consistency-sweep/SKILL.md",
    "scripts/check_provenance.py",
}
# "item N" IS AMBIGUOUS. At least three numbered lists exist: the notices list,
# the deploy-gate list under "What closing this fully requires", and
# `global_country_shortlist.md`'s own "#### Item N" probe sweep. Reading all of
# them as notices citations produced thirteen "unverifiable" notes, every one
# a citation of a DIFFERENT list.
#
# So only two forms are treated as notices citations:
#   - "notice N", which is unambiguous; and
#   - "item N" where the surrounding text also says "notice" or names
#     data_sources.md, which is how a cross-file citation of that list reads.
# Anything else is left alone rather than guessed at.
# The number may be bold or quoted: a bold notice number followed by the wrong
# city escaped the plain form, and three stale numbers reached the About page
# (2026-09-30).
CITATION_RE = re.compile(r"\b(?:item|notice)s?\s+[*\"“]*(\d{1,2})\b", re.I)
NOTICE_WORD_RE = re.compile(r"notice|data_sources", re.I)

# A DOCUMENT THAT DECLARES ITSELF SUPERSEDED IS A TRAIL, NOT A CLAIM: its
# citations point at the list AS IT WAS. Checking them is the same mistake as
# checking DECISIONS.md, skipped above because "it records what a citation said
# on a date."
#
# Example: canada-required-notices.md ("SUPERSEDED 2026-09-22 ...") cites
# "Items 9, 10, 14, 16" for "Four municipal OGLs" without naming the cities, so
# the subject test reported item 9 unverifiable. The citation is correct for the
# numbering it was written against; editing a historical trail to satisfy a
# script would run the correction the wrong way round.
SUPERSEDED_RE = re.compile(r"^\W*\*{0,2}SUPERSEDED\b", re.I | re.M)
SUPERSEDED_SCAN_CHARS = 600


def declares_itself_superseded(text):
    """Return True if the document says, up front, that it no longer governs."""
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
    "Lille (Regional)": "lille",
    "Newcastle (Regional)": "newcastle",
    "Birmingham (Regional)": "birmingham",
    "Manchester (Regional)": "manchester",
    "Blackpool (Regional)": "blackpool",
    "Nottingham (Regional)": "nottingham",
    "Washington D.C.": "washington_dc",
    "Montréal": "montreal",
    "Mexico City": "mexico_city",
    # Japan batch (2026-10-02): the macron dropped from the package name.
    "Kōchi": "kochi",
    # Brazil: accents dropped from the package name, and the regional pages'
    # suffix, as for Lille.
    "São Paulo": "sao_paulo",
    "Brasília": "brasilia",
    "Fortaleza (Regional)": "fortaleza",
    "Porto Alegre (Regional)": "porto_alegre",
    "Recife (Regional)": "recife",
    "Santos (Regional)": "santos",
    # Taiwan: Taipei + New Taipei as one regional page (2026-09-25).
    "Taipei (Regional)": "taipei",
    # Mexico: four municipios as one regional page (2026-09-27).
    "Monterrey (Regional)": "monterrey",
    # The France tram batch (2026-09-30): accents dropped, and the regional
    # pages' suffix, as for Lille.
    "Besançon": "besancon",
    "Orléans": "orleans",
    "Saint-Étienne": "saint_etienne",
    "Le Mans": "le_mans",
    "Le Havre": "le_havre",
    "Rouen (Regional)": "rouen",
    "Bordeaux (Regional)": "bordeaux",
    "Nantes (Regional)": "nantes",
    "Grenoble (Regional)": "grenoble",
    "Valenciennes (Regional)": "valenciennes",
    # Canada: Kitchener and Waterloo as one regional page (2026-09-30).
    "Kitchener–Waterloo (Regional)": "kitchener_waterloo",
    # Czechia: accents dropped from the package name; two obce each as one
    # regional page (2026-09-30).
    "Plzeň": "plzen",
    "Liberec (Regional)": "liberec",
    "Most (Regional)": "most",
    # Tram kit (2026-09-30): accents dropped from the package name, as Brazil's.
    "Liepāja": "liepaja",
    "Göteborg": "goteborg",
}

# A city's rows may name it differently from its page title - Vancouver's are
# filed under "Vancouver" and "Surrey" because the build spans two
# municipalities. Map display name -> the names any of which satisfies a table.
TABLE_ALIASES = {
    "Vancouver (Regional)": ("Vancouver", "Surrey"),
    "Guadalajara (Regional)": ("Guadalajara",),
    "Monterrey (Regional)": ("Monterrey",),
    "Miami (Regional)": ("Miami",),
    "Lille (Regional)": ("Lille (Regional)",),
    "Taipei (Regional)": ("Taipei (Regional)",),
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


def provenance_files():
    """The entry point, then every per-country file."""
    return [DATA_SOURCES] + sorted(DATA_SOURCES_DIR.glob("*.md"))


def section(text, heading):
    """Return the slice of `text` under the `## heading` LINE, up to the next
    `## ` heading line, or "" when the file has no such heading.

    Anchored to a whole line because "## Transit feeds" is a substring of the
    "### Transit feeds (GTFS)" heading. Ending at the next `## ` matches the
    single-file version's list of four headings: only `###` headings sat
    between them."""
    m = re.search(r"^" + re.escape(heading) + r"[ \t]*$", text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^## ", text[m.end():], re.M)
    return text[m.start():m.end() + nxt.start()] if nxt else text[m.start():]


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


CLAIM_RE = re.compile(r"(\d+)\s*[–-]\s*(\d+)")


def claimed_notice_numbers():
    """Notice numbers another session has claimed in docs/session_roles.md
    ("the UK six hold 84–96 and the Japan batch 97–108"): every range in the
    sentence that says notice numbers are claimed there. A claim may leave a gap on this branch; check D allows
    exactly those gaps and no others. Delete a claim once its batch lands."""
    path = ROOT / "docs" / "session_roles.md"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    i = text.find("Notice numbers are claimed")
    if i < 0:
        return set()
    sentence = text[i:text.find(".", i)]
    return {n for a, b in CLAIM_RE.findall(sentence) for n in range(int(a), int(b) + 1)}


def notice_headings(doc):
    """(number, heading) for each numbered notice in data_sources.md."""
    sec = doc[doc.index("## Notices this project MUST display when published"):]
    out = []
    for m in re.finditer(r"^\*\*(\d+)\.\s+(.+?)\s+—", sec, re.M):
        out.append((int(m.group(1)), m.group(2).strip().strip("*")))
    return out


def check_built_credits():
    """L: Tokyo's notice is BUILT from pipeline/tokyo/credits.py (notice 56),
    one entry per file, because each of its eight wards is its own publisher
    with its own prescribed credit. Every file the roster
    (pipeline/tokyo/wards.py) reads must have an entry, and no entry may name a
    file the roster does not read - so a ward switched on later cannot reach the
    page uncredited, and a ward switched off does not stay credited (2026-09-28).
    Both modules are import-safe: neither touches data/."""
    sys.path.insert(0, str(ROOT))
    from pipeline.tokyo import credits, wards
    read_files = {f for w in wards.ACTIVE.values()
                  for f in [*w["food"], *(p for ps in w.get("personal", {}).values() for p in ps)]}
    out = [f"Tokyo reads {f} but credits.py has no credit for it" for f in sorted(read_files - set(credits.SOURCES))]
    out += [f"credits.py credits {f}, which Tokyo's roster no longer reads"
            for f in sorted(set(credits.SOURCES) - read_files)]
    if tuple(credits.MHLW_FILES) != tuple(wards.MHLW_WARDS):
        out.append(f"MHLW's slice is read for {wards.MHLW_WARDS} but credited for {credits.MHLW_FILES}")
    return out


# M: country -> (the credit its licence prescribes verbatim, where that is
# recorded). Only strings a licence PRESCRIBES go here - not ones this project
# chose - so an entry is a quotation, and the evidence is the cited file.
PRESCRIBED_CREDITS = {
    "France": ("Source : Insee",
               "docs/licenses/france-licence-ouverte-2.0.md, MUST DISPLAY 1"),
}


def check_prescribed_credits():
    """M: every page of a PRESCRIBED_CREDITS country passes the string to an
    st.* call outside any if/try/with/loop block. Nested in the provenance
    block, a missing provenance file drops the credit with the snapshot (the
    France template did until 2026-09-30); a page that nests it fails."""
    cities = []
    for node in ast.parse(read(CITIES_PY)).body:
        if isinstance(node, ast.Assign) and any(
                getattr(t_, "id", None) == "CITIES" for t_ in node.targets):
            for d in node.value.elts:
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(d.keys, d.values)}
                cities.append(pairs)

    problems = []
    for country, (credit, where) in PRESCRIBED_CREDITS.items():
        # French typography puts a no-break space before the colon; a page
        # that does so still quotes INSEE verbatim.
        pattern = re.compile(re.escape(credit).replace(r"\ ", "[   ]"))
        pages = [c for c in cities if c.get("country") == country]
        if not pages:
            # A limb that examines nothing must not report success.
            problems.append(f"no city in app/cities.py has country "
                            f"'{country}' - PRESCRIBED_CREDITS checked nothing")
        for c in pages:
            page = ROOT / "app" / (c.get("page") or "")
            if not page.is_file():
                problems.append(f"{c.get('name')}: page {c.get('page')} not found")
                continue
            tree = ast.parse(read(page))
            shown = []          # (call, nested inside if/try?)

            def visit(node, nested):
                if (isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Attribute)
                        and getattr(node.func.value, "id", None) == "st"
                        and any(isinstance(n, ast.Constant)
                                and isinstance(n.value, str)
                                and pattern.search(n.value)
                                for a in node.args for n in ast.walk(a))):
                    shown.append(nested)
                for child in ast.iter_child_nodes(node):
                    visit(child, nested or isinstance(
                        node, (ast.If, ast.Try, ast.With, ast.For, ast.While)))

            visit(tree, False)
            if not shown:
                problems.append(f"{c.get('name')} ({c.get('page')}) never "
                                f"displays '{credit}' ({where})")
            elif all(shown):
                problems.append(f"{c.get('name')} ({c.get('page')}) shows "
                                f"'{credit}' only inside a conditional block, "
                                f"so a missing file can drop it - move it out")
    return problems


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
# Each entry still has to contain the city's own longitude, so a copied CRS
# fails here exactly as it does for UTM.
#
# Add an entry only with evidence that the SOURCES ship in it, not because a
# national grid exists. Ireland qualifies because both Tailte Eireann's
# valuation register (Xitm/Yitm) and its boundary layer (wkid 2157) are already
# EPSG:2157, and Dublin sits within a quarter-degree of UTM zone 29's eastern
# edge, where that zone's distortion is worst.
NATIONAL_GRIDS = {
    2157: ("Irish Transverse Mercator", -11.0, -5.0),   # Ireland
    # METROPOLITAN France only. The domain is deliberately tight: SIRENE's
    # geolocation file carries a PER-ROW `epsg` column holding 2154 alongside
    # 2975 (Réunion), 5490 (Antilles) and 2972 (Guyane), so a French build that
    # hard-codes 2154 works in Paris and silently puts every pin in the sea in
    # Fort-de-France. These bounds are what raises.
    2154: ("Lambert-93", -5.5, 10.0),                   # France (métropole)
    # Switzerland: the Stadt Zürich's Gastwirtschaftsbetriebe ships its points
    # in LV95 (`ekoord`/`nkoord`, e.g. 2680564 / 1252613), swisstopo's national
    # grid; OSM's Gemeinde boundaries carry swissBOUNDARIES3D. Zurich, 2026-09-30.
    2056: ("CH1903+ / LV95", 5.9, 10.5),                # Switzerland
}


def check_invariants(names, lons):
    """K: three CLAUDE.md invariants a new city could break silently."""
    problems = []

    # 1. ODbL: the basemap credit must be on every rendered map: PRESENT,
    #    LINKED, and NOT UNDERNEATH THE LEGEND. The third clause dates from
    #    2026-09-23, when the credit was in every file and covered by the
    #    legend in every city at any viewport taller than the map.
    #
    #    Layout cannot be measured by reading HTML, so this checks that the
    #    MECHANISM is present: the legend is position:fixed against the
    #    viewport's bottom edge while the credit is absolutely positioned
    #    against the MAP's, so the legend's `bottom` has to be clamped against
    #    the map's own height or the two collide as soon as the frame is
    #    taller than the map. Both numbers come from the same committed file,
    #    so the map that shipped is compared with the clamp that shipped with
    #    it. The real measurement is scripts/check_map_attribution.js (a
    #    browser hit-test at several viewport heights), but CLAUDE.md skips
    #    deploy-verify for pipeline-only work, and pipeline/map_common.py IS
    #    pipeline-only work; without this half, the only check that sees the
    #    regression is one the rules say not to run.
    #
    #    A LOOP OVER NOTHING PASSES ALL THREE CLAUSES. Clause 3 below is
    #    anchored to `names` (a city with no map script fails); this one fails
    #    when the glob matches no maps, so a renamed map file or a moved
    #    outputs/ cannot report every map credited, linked and clear having
    #    read none. check_scope_disclosure.py has the same guard, the case
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
    #
    #    Every skip below is RECORDED, not just taken. main() already refuses a
    #    run that read fewer longitudes than cities, but a city can still drop
    #    out here with no config at its derived slug, or with a CRS_PROJECTED
    #    that is not a literal this regex reads (an f-string, or a value
    #    imported from pipeline/countries/). Unrecorded, the limb would examine
    #    one city fewer and print the same green line.
    skipped = []
    for name in names:
        slug = SLUG_OVERRIDES.get(name, name.lower().replace(" ", "_"))
        cfg = ROOT / "pipeline" / slug / "config.py"
        lon = lons.get(name)
        if lon is None:
            continue                      # main() reports the missing longitude
        if not cfg.exists():
            skipped.append(f"{name} (no pipeline/{slug}/config.py)")
            continue
        m = re.search(r"CRS_PROJECTED\s*=\s*[\"']EPSG:(\d+)[\"']", read(cfg))
        if not m:
            skipped.append(f"{name} (no literal CRS_PROJECTED = \"EPSG:n\")")
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
    if skipped:
        problems.append(
            f"the CRS check could not examine {len(skipped)} of {len(names)} "
            f"cities: {', '.join(skipped)} - teach it to read that config "
            f"rather than letting the city drop out of the check")

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
            # Decisions logs are excluded everywhere: a past entry may name a
            # file since renamed, which is an accurate record, not a broken
            # promise.
            if not q.is_file() or is_decisions_log(q):
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


# The evidence file holds tables moved out of the master list on 2026-09-27;
# they were checked here before the move and still are. So are the per-country
# files of docs/data_sources/, added by glob in check_tables().
TABLE_DOCS = ("docs/data_sources.md", "docs/excluded_categories.md",
              "docs/city_master_list.md", "docs/city_master_list_evidence.md",
              "docs/tram_city_list.md", "docs/session_roles.md")


def check_tables():
    """I: markdown tables that do not render, or whose rows are ragged."""
    delim = re.compile(r"^\|[\s:|-]+\|\s*$")
    problems = []
    per_country = [q.relative_to(ROOT).as_posix()
                   for q in sorted(DATA_SOURCES_DIR.glob("*.md"))]
    for rel in TABLE_DOCS + tuple(per_country):
        q = ROOT / rel
        if not q.exists():
            # Renaming a document must not quietly retire its table check.
            problems.append(f"{rel}: listed in TABLE_DOCS but does not exist "
                            f"- update TABLE_DOCS with the rename")
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
                # line before calling it orphaned.
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
# session's worktree contains its own `.venv-lean`; unfiltered, this check
# reported a broken link in **Streamlit's bundled documentation**, a file this
# project neither wrote nor can fix. A checker that reports other people's
# files trains its readers to skim its output.
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
        # sets `* text=auto eol=lf` and git rewrites CRLF on the way in. A
        # working tree can still hold CRLF:
        # `cta-developer-license-agreement.html` is 230,064 bytes committed and
        # 232,828 on a Windows working tree. Hashing the working tree would call
        # the correct listed hash wrong and ask for it to be changed.
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


def notice_places(doc):
    """{number: place} - the parenthetical a notice's heading ends with, the
    city or region it is for: "(Palma)", "(Taipei (Regional))". Compared
    without "(Regional)" and case, by norm_place()."""
    out = {}
    for n, heading in notice_headings(doc):
        h = heading.strip().strip("*")
        i = h.find(" (")
        if i >= 0 and h.endswith(")"):
            out[n] = norm_place(h[i + 2:-1])
    return out


def norm_place(text):
    return re.sub(r"[()*]", "", re.sub(r"\(regional\)", "", text.lower())).strip()


# "notice **74 (Palma)**": the place written right after the number.
CITED_PLACE_RE = re.compile(r"\**\s*\(([^()]+(?:\([^()]*\))?)\)")


def check_citations(doc):
    """F: does each `item N` still point at the notice it meant?"""
    subjects = notice_subjects(doc)
    if not subjects:
        return [], []
    places = notice_places(doc)
    by_place = {}
    for k, pl in places.items():
        by_place.setdefault(pl, set()).add(k)
    hard, soft = [], []
    superseded = []
    for g in CITATION_GLOBS:
        for p in sorted(ROOT.glob(g)):
            if not p.is_file() or not ours(p) or is_decisions_log(p):
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
                line_start = text.rfind(chr(10), 0, m.start()) + 1
                line_end = text.find(chr(10), m.end())
                line = text[line_start:line_end if line_end >= 0 else len(text)]
                if line.lstrip().startswith("|"):
                    # A TABLE ROW IS ITS OWN NEIGHBOURHOOD. Its source is named
                    # in its own cells, often more than 400 characters before
                    # the citation, while the rows above and below name other
                    # sources: a 400-character window read 14 rows as citing
                    # the wrong notice (2026-10-01).
                    window = line + " " + p.stem.replace("_", " ")
                else:
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
                # "notice N (Place)" names its notice outright, so judge the
                # place, not the neighbourhood (the About page once showed a
                # stale "notice **69 (Palma)**"). Only a place that IS some
                # notice's place is judged.
                pm = CITED_PLACE_RE.match(text, m.end())
                if pm:
                    cited_place = norm_place(pm.group(1))
                    if cited_place == places.get(n):
                        continue
                    if cited_place in by_place:
                        hard.append(
                            f"{rel}: cites notice {n} ({pm.group(1)}), but notice "
                            f"{n} is {subjects[n]}'s"
                            + (f" ({places[n]})" if n in places else "")
                            + f"; {pm.group(1)} is notice "
                            + ", ".join(str(k) for k in sorted(by_place[cited_place])))
                        continue
                wl = window.lower()
                here = subjects[n].lower()
                if here in wl:
                    continue                      # cites its own subject: fine
                # A row that cites two notices (a feed's and OSM's) names
                # both subjects: each is accounted for by its own citation.
                cited_here = ({int(c.group(1)) for c in CITATION_RE.finditer(line)}
                              if line.lstrip().startswith("|") else set())
                others = sorted({s for k, s in subjects.items()
                                 if k != n and k not in cited_here
                                 and s.lower() in wl and len(s) > 4})
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

    doc = read(DATA_SOURCES)            # the entry point: notices, gate
    files = provenance_files()
    texts = [read(f) for f in files]
    corpus = "\n".join(texts)           # every file: rows and endpoints
    blocks = {label: "\n".join(section(t, h) for t in texts)
              for h, label in TABLES}

    failures, gaps = [], []
    # A glob over nothing would leave only the entry point, which holds no
    # rows, and every city would fail - loudly, but for the wrong reason.
    if len(files) == 1:
        failures.append(("docs/data_sources/", [
            "matched NO per-country files, so checks A and B read the entry "
            "point alone. If the files moved, point DATA_SOURCES_DIR at them"]))
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
            doc_plain = unquote(corpus)
            missing = sorted(
                u for u in urls
                if u not in URL_EXEMPT
                and u not in corpus and unquote(u) not in doc_plain
            )
            problems += [f"endpoint not in data_sources.md or "
                         f"data_sources/*.md: {u}" for u in missing]

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

    # Both lists are read by regex from source text. An empty parse passes C
    # (`[]` is contiguous from 1), and if BOTH come back empty D passes too,
    # and so does F, which takes its subjects from the same parse.
    if not numbered:
        failures.append(("notices", [
            "parsed NO numbered notices from data_sources.md - the '**N. "
            "Heading —' format changed, so checks C, D and F examined nothing"]))
    if not shown:
        failures.append(("notices", [
            "parsed NO entries from app/components.py's _NOTICES - its format "
            "changed, so check D examined nothing"]))

    # A gap is allowed only where docs/session_roles.md records another
    # session's claimed block (parallel batches number their notices on their
    # own branches; owner, 2026-10-02). Every other gap, and any duplicate or
    # out-of-order number, still fails.
    missing = set(range(1, max(nums, default=0) + 1)) - set(nums)
    if nums != sorted(set(nums)) or missing - claimed_notice_numbers():
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        failures.append(("notices", [
            f"numbers are not unique and contiguous from 1: {nums}"
            + (f" (duplicates: {dupes})" if dupes else "")
            + (f" (missing and unclaimed: {sorted(missing - claimed_notice_numbers())})"
               if missing - claimed_notice_numbers() else "")]))

    for h in shown:
        candidate = NOTICE_ALIASES.get(h, h)
        if not any(candidate in dh or dh in candidate for dh in doc_headings):
            failures.append(("notices", [
                f"'{h}' is DISPLAYED in app/components.py but has no numbered "
                f"item in data_sources.md"]))

    print(f"\n  notices: {len(numbered)} numbered, {len(shown)} displayed")

    # --- L, a notice BUILT from config credits every source it reads ----------
    lc = check_built_credits()
    if lc:
        failures.append(("built credits", lc))
    else:
        print("  built credits: every file Tokyo's roster reads has its credit")

    # --- M, credits a licence prescribes word for word ------------------------
    pc = check_prescribed_credits()
    if pc:
        failures.append(("prescribed credits", pc))
    else:
        print(f"  prescribed credits: every page of "
              f"{', '.join(PRESCRIBED_CREDITS)} quotes its licence's credit, "
              f"unconditionally")

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
    # `ast.literal_eval`, NOT `node.value`: a negative number is a UnaryOp
    # wrapping a Constant, so `getattr(v, "value", None)` returns None for
    # every western longitude in the file. Reading `.value` parsed ZERO of
    # sixteen, and the CRS limb below examined nothing while reporting success.
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
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
