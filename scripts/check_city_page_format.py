"""Every city page follows the city-page format (owner, 2026-10-01;
`docs/city_page_format.md`, section 1).

    python scripts/check_city_page_format.py              # app/pages/*_Heatmap.py
    python scripts/check_city_page_format.py --selftest   # touches nothing

Reads each page's code, never runs it. FAILS on a page where:
  A. the title (`render_city_title`) is not the first thing rendered, or the
     map (`st.iframe`) is not the very next statement: nothing between the
     title and the map;
  B. `render_site_notices()` is not the last thing rendered (omitting it is a
     license breach, not a cosmetic gap);
  C. `render_map_help`, `render_excluded_stations` or `render_country_links`
     is missing, or comes before the map;
  D. text the page renders (st.markdown, st.caption, st.write, st.info and
     the like) names a repository path, a script, a check or the decision
     log: the reader can open none of them.
What it cannot judge (bullets that read well, American spelling, a claim
that belongs on a reference page) is the publish-city gate's reading step.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "app/pages/*_Heatmap.py"

# Calls that put something on the page before the title are allowed only if
# they render nothing visible: the base font, the hidden city links.
SILENT = {"set_page_config", "set_base_font", "render_city_nav"}
REQUIRED_AFTER_MAP = ("render_map_help", "render_excluded_stations", "render_country_links")
RENDERS_TEXT = {"markdown", "caption", "write", "info", "warning", "success", "error", "text"}
BAD_TEXT = re.compile(r"\b(outputs|pipeline|scripts|data|docs)/|\w\.py\b|DECISIONS\.md|PLAN\.md|"
                      r"\bcheck_\w+|build brief|drift_check")


def call_names(node):
    """Names of the calls in one top-level statement, outermost first."""
    names = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            f = sub.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if name:
                names.append(name)
    return names


def rendering(stmt):
    """True when a top-level statement renders: any call outside imports,
    assignments of plain values and the silent set."""
    if isinstance(stmt, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
        return False
    names = call_names(stmt)
    return bool(names) and not set(names) <= SILENT | {"insert", "str", "Path", "exists"}


def problems(source):
    tree = ast.parse(source)
    body = [s for s in tree.body if rendering(s)]
    names = [call_names(s) for s in body]
    out = []

    def first(name):
        return next((i for i, n in enumerate(names) if name in n), None)

    title, iframe = first("render_city_title"), first("iframe")
    if title is None:
        out.append("A no render_city_title")
    elif title != 0:
        out.append(f"A something renders before the title ({names[0][0]})")
    if iframe is None:
        out.append("A no st.iframe map")
    elif title is not None and iframe != title + 1:
        out.append(f"A something renders between the title and the map ({names[title + 1][0]})")
    if not names or "render_site_notices" not in names[-1]:
        out.append("B render_site_notices() is not the last thing rendered")
    for want in REQUIRED_AFTER_MAP:
        i = first(want)
        if i is None:
            out.append(f"C no {want}")
        elif iframe is not None and i < iframe:
            out.append(f"C {want} comes before the map")
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in RENDERS_TEXT):
            for arg in node.args:
                for sub in ast.walk(arg):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        m = BAD_TEXT.search(sub.value)
                        if m and "No map yet" not in sub.value:
                            out.append(f"D rendered text names {m.group(0)!r} "
                                       f"(line {node.lineno})")
    return out


GOOD = '''
import streamlit as st
from components import render_city_nav, render_city_title
st.set_page_config(page_title="X Heatmap")
set_base_font()
render_city_nav("X")
render_city_title("X")
if HEATMAP_HTML.exists():
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/x/step3_map.py` to generate it.")
render_data_age("X")
st.markdown("""**The lines**

- One line. Stations left out are listed below.""")
render_map_help("business layer")
render_excluded_stations("X")
render_country_links("X")
render_site_notices()
'''


def selftest():
    cases = [
        ("the scaffold's shape", GOOD, 0),
        ("intro above the map", GOOD.replace('if HEATMAP_HTML', 'st.markdown("An intro.")\nif HEATMAP_HTML'), 1),
        ("no title", GOOD.replace('render_city_title("X")\n', ""), 1),
        ("notices not last", GOOD + 'st.markdown("A footnote.")\n', 1),
        ("notices missing", GOOD.replace("render_site_notices()\n", ""), 1),
        ("no map help", GOOD.replace('render_map_help("business layer")\n', ""), 1),
        ("repository path", GOOD.replace("are listed below", "are in outputs/x/excluded_stations.csv"), 1),
        ("decision log", GOOD.replace("One line.", "One line (see DECISIONS.md)."), 1),
        ("caption with a script", GOOD.replace('render_data_age("X")', 'st.caption("Built by step2_clean.py")'), 1),
    ]
    bad = 0
    for name, src, want in cases:
        got = problems(src)
        ok = len(got) == want
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {len(got)} problem(s), expected {want} {got if not ok else ''}")
    print(f"{len(cases) - bad} of {len(cases)} cases behaved as intended.")
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    pages = sorted(ROOT.glob(PAGES))
    found = []
    for p in pages:
        for prob in problems(p.read_text(encoding="utf-8")):
            found.append(f"{p.name}: {prob}")
    for f in found:
        print(f"FAIL {f}")
    if found:
        print(f"{len(found)} problem(s); the format is docs/city_page_format.md, section 1.")
        return 1
    print(f"OK - {len(pages)} city pages follow the format: title, map, ..., notices last; "
          "no repository path in their text.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
