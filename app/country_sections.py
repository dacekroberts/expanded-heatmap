"""One country at a time on the two reference pages (What Is Excluded, About the
Data): the country selector, the ?country= deep link, and the split of a
document into its shared part and its per-country parts.

The documents stay whole on disk. The checks read them as written
(check_scope_disclosure.py, check_provenance.py's numbered notices,
check_stray_bullets.py), so the split is made here, at render time, and never
by moving text between files.

HOW A PART IS GIVEN A COUNTRY. A heading names a country when its text names
exactly one country's cities (or the country itself, or an alias below), so a
new city's section ("### Lyon - ...") lands under its country with no edit
here. A heading naming none inherits its parent's country ("#### THREE
CONDITIONS" under Hong Kong's indemnity); one naming cities in two countries
stays shared. Inside the notices section, each numbered notice ("**12. ...")
is its own part, judged by its title the same way. Anything unmatched renders
in the shared part, so a part can be misfiled but never lost.

THE DEEP LINK (contract with the city pages): ?country=<cities.py country>,
URL-encoded. Unknown or missing values open the default, the first country in
cities.COUNTRY_ORDER (the Cities dropdown's order).
"""

import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

import streamlit as st

from cities import CITIES, COUNTRY_ORDER

# Publishers and other names a heading or notice title uses instead of a city.
# Each maps to the country it belongs to. Measured 2026-10-01: without these,
# these notices fell into the shared part.
ALIASES = {
    "SFMTA": "United States",
    "LA Metro": "United States",
    "CTA": "United States",
    "MassDOT": "United States",
    "WMATA": "United States",
    "TransLink": "Canada",
    "Surrey": "Canada",
    "British Columbia": "Canada",
    "Rio": "Brazil",
    "Tailte Éireann": "Ireland",
    "Comune di Milano": "Italy",
    "Île-de-France Mobilités": "France",
    "The French tram cities": "France",
}

HEADING = re.compile(r"^(#{2,4}) +(.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
NOTICE = re.compile(r"^\*\*(\d+)\. ")
# Numbered notices are split one by one only inside this section.
NOTICES_SECTION = "Notices this project MUST display when published"

CITY_COUNTS = Counter(c["country"] for c in CITIES)


def _matchers():
    names = {}
    for c in CITIES:
        names[c["name"].split(" (")[0]] = c["country"]
    for country in COUNTRY_ORDER:
        names[country] = country
    names.update(ALIASES)
    # Longest first, so "New York" is tried before "York" and so on.
    return [(re.compile(r"(?<!\w)" + re.escape(n) + r"(?!\w)"), k)
            for n, k in sorted(names.items(), key=lambda nk: -len(nk[0]))]


_MATCHERS = _matchers()


def countries_named(text):
    """The set of countries a heading or title names."""
    found = set()
    for pattern, country in _MATCHERS:
        if pattern.search(text):
            found.add(country)
            text = pattern.sub(" ", text)
    return found


def _title(lines):
    """A numbered notice's title: its opening paragraph up to the first dash."""
    para = []
    for line in lines:
        if not line.strip():
            break
        para.append(line.strip())
    return re.split(r" [—-] ", " ".join(para), maxsplit=1)[0]


def split(text):
    """Cut a document into parts, in document order.

    Each part is a dict: `lines` (its text, heading included), `level` (2-4 for
    a heading part, 5 for a numbered notice, 1 for the text before the first
    heading), `title`, `top` (the title of the level-2 section it sits in) and
    `country` (None for shared).
    """
    parts = []
    current = {"lines": [], "level": 1, "title": "", "top": None, "country": None}
    stack = []          # (level, title, country) of the open headings
    in_notices = False
    fenced = False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        heading = None if fenced else HEADING.match(line)
        notice = None if fenced or not in_notices else NOTICE.match(line)
        if heading:
            parts.append(current)
            level, title = len(heading.group(1)), heading.group(2)
            while stack and stack[-1][0] >= level:
                stack.pop()
            named = countries_named(title)
            if len(named) == 1:
                country = named.pop()
            elif named:
                country = None
            else:
                country = stack[-1][2] if stack else None
            stack.append((level, title, country))
            if level == 2:
                in_notices = title.startswith(NOTICES_SECTION)
            top = next((t for lv, t, _ in stack if lv == 2), None)
            current = {"lines": [line], "level": level, "title": title,
                       "top": top, "country": country}
        elif notice:
            parts.append(current)
            current = {"lines": [line], "level": 5, "title": "",
                       "top": NOTICES_SECTION, "country": None}
        else:
            current["lines"].append(line)
    parts.append(current)
    for part in parts:
        if part["level"] == 5:
            named = countries_named(_title(part["lines"]))
            part["title"] = _title(part["lines"])
            part["country"] = named.pop() if len(named) == 1 else None
    return [p for p in parts if "\n".join(p["lines"]).strip()]


@st.cache_data(show_spinner=False)
def _parts_of(path, mtime_ns):
    return split(Path(path).read_text(encoding="utf-8"))


def parts_of(path):
    """split() of a file, cached per path and modification time. Keyed by
    path: two pages each caching a same-named reader shared one cache entry
    and showed each other's document (2026-10-01)."""
    path = Path(path)
    return _parts_of(str(path), path.stat().st_mtime_ns)


INTERNAL = re.compile(r"<!-- internal -->.*?<!-- /internal -->", re.S)


def public(text):
    """The text a reader sees: every `<!-- internal -->` ... `<!-- /internal -->`
    passage removed (how the project maintains a record, not what it records;
    owner, 2026-10-01). The doc keeps the passage, and GitHub hides the markers.
    An unclosed marker removes nothing, so a typo never swallows the rest of a
    page."""
    text = INTERNAL.sub("", text)
    text = OWNER_TAG.sub(_owner_tag, text)
    return re.sub(r"\n{3,}", "\n\n", text)


# THE DECISION LOG'S ATTRIBUTION TAGS STAY IN THE DOCS, NOT ON THE PAGE
# (owner, 2026-10-03, from the live audit): "(owner, 2026-09-29)", "(owner)",
# "(owner's rule)" and the like, about 300 across the rendered docs. A tag that
# carries a fact after a colon or semicolon keeps the fact: "(owner; 331
# dropped)" reads "(331 dropped)". One whose remainder is only a quoted reply
# goes whole. "a sole owner" and other business owners are not in brackets of
# this form, so they stay. scripts/check_internal_prose.py reads through this.
OWNER_TAG = re.compile(r"[ \t]*\((?:the )?owner\b([^()]*)\)", re.I)


def _owner_tag(match):
    rest = re.split(r"[:;]", match.group(1), maxsplit=1)
    fact = rest[1].strip() if len(rest) == 2 else ""
    if not fact or fact[0] in "\"'“":
        return ""
    whole = match.group(0)
    return whole[:len(whole) - len(whole.lstrip(" \t"))] + f"({fact})"


def shared_text(parts, skip_titles=()):
    """The shared parts, joined back in document order."""
    return "\n".join("\n".join(p["lines"]) for p in parts
                     if p["country"] is None and p["title"] not in skip_titles)


def country_text(parts, country, headed_by=None):
    """One country's parts, each under the level-2 heading it came from.

    `headed_by` maps a level-2 title to the whole text to show above that
    group instead of the bare heading (a section whose subsections are all
    per-country, such as "Excluded in one city", moves with them).
    """
    out, shown = [], None
    headed_by = headed_by or {}
    for p in parts:
        if p["country"] != country:
            continue
        if p["level"] > 2 and p["top"] and p["top"] != shown:
            out.append(headed_by.get(p["top"], f"## {p['top']}"))
        shown = p["top"] if p["level"] > 2 else p["title"]
        out.append("\n".join(p["lines"]))
    return "\n\n".join(out)


def unmatched_report(parts):
    """(title, country) for each part, for a probe or a review."""
    return [(p["level"], p["title"][:90], p["country"]) for p in parts]


def country_link(country):
    """The ?country= query for a country, URL-encoded (the deep link)."""
    return "?country=" + quote(country)


def country_slug(country):
    """A country's file stem under docs/data_sources/ ("United States" ->
    "united-states")."""
    return country.lower().replace(" ", "-")


# The two-step selector's groups: the macro map's regions, with a country's
# sub-regions folded into one group (the United States' and Canada's halves,
# France's two, the Seoul Capital Area). A region not listed is its own group.
REGION_GROUP = {
    "United States West": "North America",
    "United States East": "North America",
    "Canada West": "North America",
    "Canada East": "North America",
    "Mexico": "North America",
    "France North": "Europe",
    "France South": "Europe",
    "Czechia": "Europe",
    "Belgium": "Europe",
    "United Kingdom": "Europe",
    "Seoul Capital Area": "East Asia",
    # Japan's two halves (owner, 2026-10-03). Unfolded, all 34 Japanese cities
    # showed as "Japan West (34)", named after the first city's half.
    "Japan West": "East Asia",
    "Japan East": "East Asia",
}


def _groups():
    """{group: [country, ...]} in COUNTRY_ORDER, groups in first-seen order."""
    group_of = {}
    for c in CITIES:
        group = REGION_GROUP.get(c["region"], c["region"])
        # A country whose cities fall in two groups would be listed under the
        # first only, named after one half: a new split region needs its
        # REGION_GROUP rows.
        if group_of.setdefault(c["country"], group) != group:
            raise ValueError(
                f"country_sections.py: {c['country']} falls in both "
                f"{group_of[c['country']]!r} and {group!r} ({c['region']}); "
                f"fold its regions into one group in REGION_GROUP")
    groups = {}
    for country in COUNTRY_ORDER:
        groups.setdefault(group_of[country], []).append(country)
    return groups, group_of


GROUPS, GROUP_OF = _groups()


def _label(name):
    n = (CITY_COUNTS[name] if name in CITY_COUNTS
         else sum(CITY_COUNTS[k] for k in GROUPS[name]))
    return f"{name} ({n})"


def select_country(key):
    """The selector: a region, then that region's countries. Set from
    ?country= and writing its choice back to the URL so the view can be
    shared. Returns the chosen country.

    Horizontal st.radio rows labeled "<Name> (<n cities>)", the same control
    as the Overview's region selector (cleanup, 2026-10-01). The owner chose the
    two-step form over one radio of every country on 2026-10-01: at 375 px the
    single radio was 396 px tall, the region row is 127 px and the tallest
    country row (Europe, 14 countries) 281 px. A region with one country shows
    no second row.

    The URL is applied only when it changed since this page last wrote it: a
    click updates the widget before the rerun, while the URL still holds the
    previous country, and re-applying it then would undo the click.
    """
    applied = key + "_applied"
    region_key = key + "_region"
    wanted = st.query_params.get("country")
    if wanted not in COUNTRY_ORDER:
        wanted = None
    if wanted and wanted != st.session_state.get(applied):
        st.session_state[applied] = wanted
        st.session_state[region_key] = GROUP_OF[wanted]
        st.session_state[f"{key}_{GROUP_OF[wanted]}"] = wanted

    if st.session_state.get(region_key) not in GROUPS:
        st.session_state[region_key] = GROUP_OF[wanted or COUNTRY_ORDER[0]]
    region = st.radio("Region", list(GROUPS), format_func=_label,
                      horizontal=True, key=region_key)
    options = GROUPS[region]
    country_key = f"{key}_{region}"
    if st.session_state.get(country_key) not in options:
        st.session_state[country_key] = (wanted if wanted in options
                                         else options[0])
    if len(options) == 1:
        country = options[0]
    else:
        country = st.radio("Country", options, format_func=_label,
                           horizontal=True, key=country_key)
    if st.query_params.get("country") != country:
        st.query_params["country"] = country
    st.session_state[applied] = country
    return country
