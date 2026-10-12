"""Write the place-search boilerplate a built city needs, from a plan file.

    python scripts/place_search_scaffold.py --plan PLAN_JSON [--write]
    python scripts/place_search_scaffold.py --selftest

The script decides nothing about a city. It copies one fixed pattern: a
PLACE_* block at the end of the config, a step2b_place_index.py, one argument
in the map step and one in the page. Whatever does not fit is refused, city by
city, and a plan that is not the shape below is refused whole.

PLAN_JSON is a JSON file a session prepares by hand:

    {"date": "2026-10-13",
     "cities": {"zurich": {"relations": [1682248], "languages": ["de"], "fold": null}}}

`date` is an ISO date. Each city key is a folder name under pipeline/.
`relations` is a non-empty list of positive OpenStreetMap relation ids; the
area id is 3600000000 plus each relation id. `languages` is a non-empty list
of codes from pipeline/place_index.py's LANGUAGE_NAMES. `fold` is null or a
string from pipeline/place_index.py's FOLDS.

Without --write the script prints what it would do and changes nothing. With
--write it writes, for each fitting city, its config block, step2b, map
argument and page argument. All four are checked before any file is written,
so a refused city is never left half scaffolded. --selftest runs the cases on
a temporary tree and touches nothing.
"""
import argparse
import ast
import contextlib
import datetime
import io
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_FOLDER_RE = re.compile(r"[A-Za-z0-9_]+")
_SYSPATH_LINE = "sys.path.insert(0, str(Path(__file__).parent.parent.parent))"
_PLACE_IMPORT = "from pipeline import place_index  # noqa: E402"
_PAGE_RE = re.compile(r'"page"\s*:\s*"([^"]+)"')


def _read(path):
    """The file's text, decoded as UTF-8 with line endings normalised to LF."""
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def _write(path, text):
    """Write text as UTF-8 bytes with LF line endings, never carriage returns."""
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def _iso_date(value):
    """True when value is an ISO date string, YYYY-MM-DD."""
    if not isinstance(value, str):
        return False
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _place_index_constants(root):
    """(LANGUAGE_NAMES, FOLDS) read from pipeline/place_index.py, or None."""
    path = root / "pipeline" / "place_index.py"
    try:
        text = _read(path)
    except OSError:
        return None
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    names = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("LANGUAGE_NAMES", "FOLDS")):
            try:
                names[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError):
                pass
    if not isinstance(names.get("LANGUAGE_NAMES"), dict) or not isinstance(names.get("FOLDS"), tuple):
        return None
    return names["LANGUAGE_NAMES"], names["FOLDS"]


def _config_name(text, folder, listed_name=None):
    """(display name, where it came from): the config's NAME, then CITY_NAME,
    then the name app/cities.py gives the city's page (it keeps accents the
    folder name lost: Besançon, Göteborg), then the folder in title case."""
    for key in ("NAME", "CITY_NAME"):
        m = re.search(r"(?m)^" + key + r"\s*=\s*\"([^\"]*)\"", text)
        if m and m.group(1).strip():
            return m.group(1).strip(), "config"
    if listed_name:
        return listed_name, "app/cities.py"
    return folder.replace("_", " ").title(), "the folder name"


def _page_names(root):
    """{page path: city name} from app/cities.py's CITIES, read as literals
    without importing the app; empty when the file cannot be parsed."""
    try:
        tree = ast.parse(_read(root / "app" / "cities.py"))
    except (OSError, SyntaxError):
        return {}
    names = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "CITIES"
                and isinstance(node.value, ast.List)):
            for entry in node.value.elts:
                if not isinstance(entry, ast.Dict):
                    continue
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(entry.keys, entry.values)}
                if isinstance(pairs.get("page"), str) and isinstance(pairs.get("name"), str):
                    names[pairs["page"]] = pairs["name"]
    return names


def _cities_pages(root):
    """The page paths listed under app/cities.py's CITIES entries."""
    try:
        text = _read(root / "app" / "cities.py")
    except OSError:
        return []
    return _PAGE_RE.findall(text)


def _find_page(root, folder, pages):
    """(path, text) for the city's page file among those app/cities.py lists,
    matched by the page's import of pipeline.<folder>.config; (None, None)
    when no listed page is that city's."""
    for rel in pages:
        path = root / "app" / rel
        if not path.is_file():
            continue
        try:
            text = _read(path)
        except OSError:
            continue
        if f"pipeline.{folder}.config" in text:
            return path, text
    return None, None


def _match_close(text, open_i):
    """The index of the closing parenthesis of the call opened at open_i,
    skipping string literals and comments; -1 when it never closes."""
    depth = 0
    i = open_i
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "#":
            end = text.find("\n", i)
            i = n if end == -1 else end
            continue
        if ch in ("'", '"'):
            if text.startswith(ch * 3, i):
                end = text.find(ch * 3, i + 3)
                i = n if end == -1 else end + 3
            else:
                j = i + 1
                while j < n:
                    if text[j] == "\\":
                        j += 2
                        continue
                    if text[j] == ch:
                        j += 1
                        break
                    j += 1
                i = j
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _find_call(text, name):
    """(open_i, close_i) for the one call of name( in text, or None."""
    matches = list(re.finditer(re.escape(name) + r"\s*\(", text))
    if len(matches) != 1:
        return None
    m = matches[0]
    open_i = m.end() - 1
    close_i = _match_close(text, open_i)
    if close_i == -1:
        return None
    return open_i, close_i


def _content_lines(text, start, nl):
    """[(line_start, line_end)] for the non-empty, non-comment lines in
    text[start:nl]."""
    out = []
    i = start
    while i < nl:
        end = text.find("\n", i)
        if end == -1 or end > nl:
            end = nl
        stripped = text[i:end].strip()
        if stripped and not stripped.startswith("#"):
            out.append((i, end))
        i = end + 1
    return out


def _code_end(text, line_start, line_end):
    """The index just after the last code character of one argument line,
    trailing whitespace and a trailing comment set aside."""
    j = line_start
    while j < line_end:
        ch = text[j]
        if ch == "#":
            break
        if ch in ("'", '"'):
            if text.startswith(ch * 3, j):
                k = text.find(ch * 3, j + 3)
                j = line_end if k == -1 or k > line_end else k + 3
            else:
                k = j + 1
                while k < line_end:
                    if text[k] == "\\":
                        k += 2
                        continue
                    if text[k] == ch:
                        k += 1
                        break
                    k += 1
                j = k
            continue
        j += 1
    end = j
    while end > line_start and text[end - 1] in " \t":
        end -= 1
    return end


def _add_call_argument(text, name, arg_text):
    """text with arg_text added as the last argument of the one name( call.
    Handles a call on one line and one spread over several lines, with or
    without a trailing comma, keeping the file's own indentation."""
    loc = _find_call(text, name)
    if loc is None:
        raise ValueError(f"{name}( is not exactly one call in the file")
    open_i, close_i = loc
    inner = text[open_i + 1:close_i]
    if "\n" not in inner:
        insert = arg_text if inner.strip() == "" else ", " + arg_text
        return text[:close_i] + insert + text[close_i:]
    nl = text.rfind("\n", open_i + 1, close_i)
    indent = text[nl + 1:close_i]
    if indent.strip():
        raise ValueError(f"the closing parenthesis of {name}( is not on its own line")
    lines = _content_lines(text, open_i + 1, nl)
    if lines:
        first = text[lines[0][0]:lines[0][1]]
        arg_indent = first[:len(first) - len(first.lstrip(" \t"))]
        last_start, last_end = lines[-1]
        last_code_end = _code_end(text, last_start, last_end)
    else:
        arg_indent = indent + "    "
        last_code_end = None
    head = text[:nl + 1]
    if last_code_end is not None and last_code_end > last_start and text[last_code_end - 1] != ",":
        head = head[:last_code_end] + "," + head[last_code_end:]
    return head + arg_indent + arg_text + ",\n" + indent + text[close_i:]


def _insert_place_index_import(text):
    """text with the place_index import on the line after the sys.path line."""
    if text.count(_SYSPATH_LINE) != 1:
        raise ValueError("the sys.path.insert anchor line is not present exactly once")
    idx = text.index(_SYSPATH_LINE)
    end = text.find("\n", idx)
    if end == -1:
        raise ValueError("the sys.path.insert anchor line has no newline after it")
    return text[:end + 1] + _PLACE_IMPORT + "\n" + text[end + 1:]


def _config_block(date, relations, languages, fold):
    ids = ",".join(str(3600000000 + r) for r in relations)
    langs = ", ".join(f'"{c}"' for c in languages)
    if len(languages) == 1:
        langs += ","
    fold_repr = "None" if fold is None else json.dumps(fold)
    return ("\n"
            f"# --- Place search (scripts/place_search_scaffold.py, {date}) ---\n"
            "\n"
            f'PLACE_AREA = "(id:{ids})"\n'
            f'PLACE_OSM_JSON = DATA_RAW / "osm_places_{date}.json"\n'
            f'PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_{date}.json"\n'
            f"PLACE_LANGUAGES = ({langs})\n"
            f"PLACE_FOLD = {fold_repr}\n"
            "PLACE_REVIEWED = {}\n"
            "PLACE_DROPPED = {}\n")


def _append_config_block(old_text, block):
    """old_text with block appended, the file ending in exactly one newline."""
    return old_text.rstrip("\n") + "\n" + block


def _step2b_text(folder, name, date):
    return f'''"""Step 2b - Build {name}'s place-search index (scripts/place_search_scaffold.py, {date}).

All the work is pipeline/place_index.py (run); this file names the city. Places
only, never business records (DECISIONS.md, "Four ideas assessed before the
large review", item 3). Runs before step 3, whose map carries the index's hash.

Input:  data/{folder}/raw/osm_places_{date}.json        (pipeline/place_index_fetch.py)
        data/{folder}/raw/osm_places_extra_{date}.json  (the same, its second query)
Output: app/static/places/{folder}.json  (served by Streamlit's static serving;
        ODbL 1.0, the notice inside the file);
        outputs/{folder}/place_search.json  (the page's summary: the languages
        its search bullet names, measured)

Run:  python pipeline/{folder}/step2b_place_index.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import place_index  # noqa: E402
from pipeline.{folder} import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    place_index.run(config)
'''


def _spec_errors(folder, spec, language_names, folds):
    """The first reason a plan's city entry is refused, or None."""
    if not _FOLDER_RE.fullmatch(folder):
        return "the city key is not a plain folder name (letters, digits, underscore)"
    if not isinstance(spec, dict):
        return "the city entry is not an object"
    relations = spec.get("relations")
    if not isinstance(relations, list) or not relations:
        return "relations must be a non-empty list"
    for r in relations:
        if not isinstance(r, int) or isinstance(r, bool) or r <= 0:
            return f"relation {r!r} is not a positive integer"
    languages = spec.get("languages")
    if not isinstance(languages, list) or not languages:
        return "languages must be a non-empty list"
    for code in languages:
        if not isinstance(code, str) or code not in language_names:
            return f"language {code!r} is not a key of place_index.LANGUAGE_NAMES"
    fold = spec.get("fold")
    if fold is not None and not isinstance(fold, str):
        return "fold must be null or a string"
    if fold not in folds:
        return f"fold {fold!r} is not one of place_index.FOLDS"
    return None


def scaffold_city(root, folder, spec, date, write, pages, language_names, folds):
    """Scaffold one city. Returns (status, reason, lines) where status is
    "done", "would do" or "refused". A refused city writes nothing; a fitting
    city is checked on all four files before any of them is written."""
    reason = _spec_errors(folder, spec, language_names, folds)
    if reason is not None:
        return "refused", reason, []

    config_path = root / "pipeline" / folder / "config.py"
    if not config_path.is_file():
        return "refused", "no config.py", []
    config_text = _read(config_path)
    if "PLACE_AREA" in config_text:
        return "refused", "config already contains PLACE_AREA", []
    if not re.search(r"(?m)^DATA_RAW\s*=", config_text):
        return "refused", "config has no DATA_RAW", []

    step2b_path = root / "pipeline" / folder / "step2b_place_index.py"
    if step2b_path.exists():
        return "refused", "step2b_place_index.py already exists", []

    map_paths = sorted((root / "pipeline" / folder).glob("step*_map.py"))
    if len(map_paths) != 1:
        return "refused", "not exactly one step*_map.py", []
    map_path = map_paths[0]
    map_text = _read(map_path)
    if "place_index_url" in map_text:
        return "refused", "map step already contains place_index_url", []
    if _PLACE_IMPORT in map_text:
        return "refused", "map step already imports place_index", []
    try:
        new_map_text = _insert_place_index_import(map_text)
        new_map_text = _add_call_argument(
            new_map_text, "render_heatmap",
            f'place_index_url=place_index.index_url("{folder}")')
    except ValueError as exc:
        return "refused", f"map step: {exc}", []

    page_path, page_text = _find_page(root, folder, pages)
    if page_path is None:
        return "refused", "page file cannot be found from app/cities.py", []
    if "search=" in page_text:
        return "refused", "page already contains search=", []
    try:
        new_page_text = _add_call_argument(page_text, "render_map_help",
                                           f"search='{folder}'")
    except ValueError as exc:
        return "refused", f"page: {exc}", []

    listed = _page_names(root).get(page_path.relative_to(root / "app").as_posix())
    name, name_from = _config_name(config_text, folder, listed)
    fell_back = name_from != "config"
    new_config_text = _append_config_block(
        config_text,
        _config_block(date, spec["relations"], spec["languages"], spec["fold"]))
    new_step2b_text = _step2b_text(folder, name, date)

    for label, source in (("config.py", new_config_text),
                          ("step2b_place_index.py", new_step2b_text),
                          (map_path.name, new_map_text),
                          (page_path.name, new_page_text)):
        try:
            compile(source, label, "exec")
        except SyntaxError as exc:
            return "refused", f"{label} does not compile: {exc}", []

    if write:
        lines = [
            f"{folder}: config appended the PLACE_* block",
            f"{folder}: step2b_place_index.py written",
            f"{folder}: {map_path.name} got the place_index import and place_index_url",
            f"{folder}: {page_path.name} got search='{folder}'",
        ]
    else:
        lines = [
            f"{folder}: config would append the PLACE_* block",
            f"{folder}: step2b_place_index.py would be written",
            f"{folder}: {map_path.name} would get the place_index import and place_index_url",
            f"{folder}: {page_path.name} would get search='{folder}'",
        ]
    if fell_back:
        lines.append(f'{folder}: no NAME or CITY_NAME in config; used "{name}" '
                     f"from {name_from} as the name")

    if write:
        _write(config_path, new_config_text)
        _write(step2b_path, new_step2b_text)
        _write(map_path, new_map_text)
        _write(page_path, new_page_text)

    return ("done" if write else "would do"), None, lines


def run_plan(root, plan, write, plan_label="plan.json"):
    """Validate a plan and scaffold each city. Returns (ok, lines)."""
    if not isinstance(plan, dict):
        return False, [f"{plan_label}: the plan must be a JSON object with date and cities"]
    date = plan.get("date")
    if not _iso_date(date):
        return False, [f"{plan_label}: the plan's date must be an ISO date (YYYY-MM-DD)"]
    cities = plan.get("cities")
    if not isinstance(cities, dict):
        return False, [f"{plan_label}: the plan's cities must be an object of city keys"]
    constants = _place_index_constants(root)
    if constants is None:
        return False, ["cannot read LANGUAGE_NAMES and FOLDS from pipeline/place_index.py"]
    language_names, folds = constants
    pages = _cities_pages(root)

    lines = []
    rows = []
    for folder, spec in cities.items():
        status, reason, city_lines = scaffold_city(
            root, folder, spec, date, write, pages, language_names, folds)
        rows.append((folder, status, reason))
        lines.extend(city_lines)
        if reason is not None:
            lines.append(f"{folder}: refused ({reason})")

    lines.append("")
    lines.append(f"{'CITY':<26} RESULT")
    ok = True
    for folder, status, reason in rows:
        if status == "done":
            lines.append(f"{folder:<26} done")
        elif status == "would do":
            lines.append(f"{folder:<26} would do")
        else:
            lines.append(f"{folder:<26} refused: {reason}")
            ok = False
    return ok, lines


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="place_search_scaffold_"))
    ok = total = 0

    def report(label, good, got=""):
        nonlocal ok, total
        total += 1
        ok += bool(good)
        print(f"  {'ok ' if good else 'BAD'} {label}" + (f": {got}" if got else ""))

    def w(rel, text):
        path = tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

    def fresh():
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True, exist_ok=True)
        w("pipeline/place_index.py",
          'LANGUAGE_NAMES = {"en": "English", "de": "German", "fr": "French", "ja": "Japanese"}\n'
          'FOLDS = (None, "ja")\n')

    def city(folder, name, page_rel, config=None, map_src=None, page_src=None):
        if config is not None:
            w(f"pipeline/{folder}/config.py", config)
        if map_src is not None:
            w(f"pipeline/{folder}/step3_map.py", map_src)
        if page_src is not None:
            w(f"app/{page_rel}", page_src)

    def cities(entries):
        w("app/cities.py", "CITIES = " + json.dumps(
            [{"name": n, "page": p} for n, p in entries], indent=4) + "\n")

    def plan(date, specs):
        path = tmp / "plan.json"
        path.write_bytes(json.dumps({"date": date, "cities": specs}).encode("utf-8"))
        return path

    def snap():
        return {str(p.relative_to(tmp)): p.read_bytes()
                for p in sorted(tmp.rglob("*")) if p.is_file()}

    def run(argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(argv, root=tmp)
        return rc, buf.getvalue()

    def fit_config(folder, name):
        return ('"""config for {0}."""\n'
                "from pathlib import Path\n\n"
                "ROOT = Path(__file__).parent.parent.parent\n"
                'DATA_RAW = ROOT / "data" / "{0}" / "raw"\n'
                'SLUG = "{0}"\n'
                'NAME = "{1}"\n').format(folder, name)

    def fit_map(folder):
        return ('"""Step 3 - render {0}."""\n'
                "import sys\nfrom pathlib import Path\n\n"
                "sys.path.insert(0, str(Path(__file__).parent.parent.parent))\n"
                "from pipeline.map_common import render_heatmap  # noqa: E402\n"
                "from pipeline.{0}.config import HEATMAP_HTML  # noqa: E402\n\n\n"
                "def main():\n"
                "    render_heatmap(\n"
                "        output_path=HEATMAP_HTML,\n"
                "        label_focus=None,\n"
                "    )\n\n\n"
                'if __name__ == "__main__":\n'
                "    main()\n").format(folder)

    def fit_page(folder):
        return ('"""page {0}."""\n'
                "from pipeline.{0}.config import HEATMAP_HTML\n"
                "from components import render_map_help\n\n\n"
                "render_map_help('three business categories')\n").format(folder)

    def refuse(label, reason, spec, *, folder="zeta", name="Zeta",
               page_rel="pages/9_Zeta_Heatmap.py", config=None, map_src=None,
               page_src=None, page_listed=True, extra=None):
        fresh()
        if config is not None:
            w(f"pipeline/{folder}/config.py", config)
        if map_src is not None:
            w(f"pipeline/{folder}/step3_map.py", map_src)
        if page_src is not None:
            w(f"app/{page_rel}", page_src)
        if extra:
            for rel, text in extra.items():
                w(rel, text)
        cities([(name, page_rel)] if page_listed else [("Other", "pages/8_Other_Heatmap.py")])
        path = plan("2026-10-13", {folder: spec})
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report(label, rc != 0 and snap() == before and reason in out, f"exit {rc}")

    try:
        # 1. A dry run changes no byte of any file and exits 0.
        fresh()
        city("alpha", "Alpha", "pages/1_Alpha_Heatmap.py",
             config=fit_config("alpha", "Alpha"), map_src=fit_map("alpha"),
             page_src=fit_page("alpha"))
        cities([("Alpha", "pages/1_Alpha_Heatmap.py")])
        path = plan("2026-10-13", {"alpha": {"relations": [1682248], "languages": ["de"], "fold": None}})
        before = snap()
        rc, out = run(["--plan", str(path)])
        report("dry run changes no byte and exits 0",
               rc == 0 and snap() == before and "would do" in out and "Nothing was written." in out,
               f"exit {rc}")

        # 2. --write on a fitting city: all four files, correct and compiling.
        fresh()
        city("alpha", "Alpha", "pages/1_Alpha_Heatmap.py",
             config=fit_config("alpha", "Alpha"), map_src=fit_map("alpha"),
             page_src=fit_page("alpha"))
        cities([("Alpha", "pages/1_Alpha_Heatmap.py")])
        path = plan("2026-10-13", {"alpha": {"relations": [1682248], "languages": ["de"], "fold": None}})
        rc, out = run(["--plan", str(path), "--write"])
        good = rc == 0
        cfg = (tmp / "pipeline/alpha/config.py").read_text(encoding="utf-8")
        good = good and cfg.endswith("PLACE_DROPPED = {}\n")
        good = good and 'PLACE_AREA = "(id:3601682248)"' in cfg
        good = good and 'PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"' in cfg
        good = good and 'PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"' in cfg
        good = good and 'PLACE_LANGUAGES = ("de",)' in cfg
        good = good and "PLACE_FOLD = None" in cfg
        s2b = tmp / "pipeline/alpha/step2b_place_index.py"
        good = good and s2b.is_file()
        good = good and "Build Alpha's place-search index" in s2b.read_text(encoding="utf-8")
        good = good and "from pipeline.alpha import config" in s2b.read_text(encoding="utf-8")
        m = (tmp / "pipeline/alpha/step3_map.py").read_text(encoding="utf-8")
        good = good and "from pipeline import place_index  # noqa: E402" in m
        good = good and 'place_index_url=place_index.index_url("alpha")' in m
        pg = (tmp / "app/pages/1_Alpha_Heatmap.py").read_text(encoding="utf-8")
        good = good and "search='alpha'" in pg
        for rel in ("pipeline/alpha/config.py", "pipeline/alpha/step2b_place_index.py",
                    "pipeline/alpha/step3_map.py", "app/pages/1_Alpha_Heatmap.py"):
            # Bytes, not text: reading as text on Windows turns a written
            # carriage return back into a newline and hides it.
            src = (tmp / rel).read_bytes().decode("utf-8")
            good = good and "\r" not in src
            try:
                compile(src, rel, "exec")
            except SyntaxError:
                good = False
        report("--write on a fitting city writes all four, compiles, LF only", good, f"exit {rc}")

        # 3. Several relations give one comma-separated area in plan order.
        fresh()
        city("beta", "Beta", "pages/2_Beta_Heatmap.py",
             config=fit_config("beta", "Beta"), map_src=fit_map("beta"), page_src=fit_page("beta"))
        cities([("Beta", "pages/2_Beta_Heatmap.py")])
        path = plan("2026-10-13", {"beta": {"relations": [111, 222, 333], "languages": ["de"], "fold": None}})
        rc, out = run(["--plan", str(path), "--write"])
        cfg = (tmp / "pipeline/beta/config.py").read_text(encoding="utf-8")
        report("several relations give one comma-separated area in plan order",
               rc == 0 and 'PLACE_AREA = "(id:3600000111,3600000222,3600000333)"' in cfg, f"exit {rc}")

        # 4. One language is a one-item tuple; the fold is the quoted string.
        fresh()
        city("gamma", "Gamma", "pages/3_Gamma_Heatmap.py",
             config=fit_config("gamma", "Gamma"), map_src=fit_map("gamma"), page_src=fit_page("gamma"))
        cities([("Gamma", "pages/3_Gamma_Heatmap.py")])
        path = plan("2026-10-13", {"gamma": {"relations": [7], "languages": ["ja"], "fold": "ja"}})
        rc, out = run(["--plan", str(path), "--write"])
        cfg = (tmp / "pipeline/gamma/config.py").read_text(encoding="utf-8")
        report("one language is a one-item tuple and the fold is quoted",
               rc == 0 and 'PLACE_LANGUAGES = ("ja",)' in cfg and 'PLACE_FOLD = "ja"' in cfg, f"exit {rc}")

        # 5. A second --write changes no byte and reports the city refused.
        fresh()
        city("alpha", "Alpha", "pages/1_Alpha_Heatmap.py",
             config=fit_config("alpha", "Alpha"), map_src=fit_map("alpha"),
             page_src=fit_page("alpha"))
        cities([("Alpha", "pages/1_Alpha_Heatmap.py")])
        path = plan("2026-10-13", {"alpha": {"relations": [1682248], "languages": ["de"], "fold": None}})
        run(["--plan", str(path), "--write"])
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report("a second --write changes no byte and refuses the city",
               rc != 0 and snap() == before and "refused" in out
               and "config already contains PLACE_AREA" in out, f"exit {rc}")

        # 6. One refusal case for each listed refusal, each leaving files unchanged.
        fit_spec = {"relations": [1], "languages": ["de"], "fold": None}
        refuse("refuses a city with no config.py", "no config.py", fit_spec,
               config=None, map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a config that already has PLACE_AREA", "config already contains PLACE_AREA",
               fit_spec, config=fit_config("zeta", "Zeta") + 'PLACE_AREA = "(id:3609999999)"\n',
               map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a config with no DATA_RAW", "config has no DATA_RAW", fit_spec,
               config='SLUG = "zeta"\nNAME = "Zeta"\n',
               map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a city whose step2b already exists", "step2b_place_index.py already exists",
               fit_spec, config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"),
               page_src=fit_page("zeta"), extra={"pipeline/zeta/step2b_place_index.py": "# already\n"})
        refuse("refuses a city with two map steps", "not exactly one step*_map.py", fit_spec,
               config=fit_config("zeta", "Zeta"), map_src=None, page_src=fit_page("zeta"),
               extra={"pipeline/zeta/step3_map.py": fit_map("zeta"),
                      "pipeline/zeta/step4_map.py": fit_map("zeta")})
        refuse("refuses a map step with no render_heatmap call",
               "map step: render_heatmap( is not exactly one call", fit_spec,
               config=fit_config("zeta", "Zeta"),
               map_src=('"""m."""\nimport sys\nfrom pathlib import Path\n\n'
                        'sys.path.insert(0, str(Path(__file__).parent.parent.parent))\n'
                        'from pipeline.map_common import render_heatmap  # noqa: E402\n'),
               page_src=fit_page("zeta"))
        refuse("refuses a map step that already has place_index_url",
               "map step already contains place_index_url", fit_spec,
               config=fit_config("zeta", "Zeta"),
               map_src=fit_map("zeta").replace(
                   "label_focus=None,\n",
                   '        label_focus=None,\n        place_index_url=place_index.index_url("zeta"),\n'),
               page_src=fit_page("zeta"))
        refuse("refuses a page not found from app/cities.py",
               "page file cannot be found from app/cities.py", fit_spec,
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"),
               page_src=fit_page("zeta"), page_listed=False)
        refuse("refuses a page with no render_map_help call",
               "page: render_map_help( is not exactly one call", fit_spec,
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"),
               page_src='"""p."""\nfrom pipeline.zeta.config import HEATMAP_HTML\n')
        refuse("refuses a page that already has search=", "page already contains search=", fit_spec,
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"),
               page_src=fit_page("zeta").replace(
                   "render_map_help('three business categories')",
                   "render_map_help('three business categories', search='zeta')"))
        refuse("refuses a language outside LANGUAGE_NAMES",
               "language 'xx' is not a key of place_index.LANGUAGE_NAMES",
               {"relations": [1], "languages": ["xx"], "fold": None},
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a fold outside FOLDS", "fold 'xx' is not one of place_index.FOLDS",
               {"relations": [1], "languages": ["de"], "fold": "xx"},
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses an empty relations list", "relations must be a non-empty list",
               {"relations": [], "languages": ["de"], "fold": None},
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a relation that is not a positive integer",
               "relation 0 is not a positive integer",
               {"relations": [0], "languages": ["de"], "fold": None},
               config=fit_config("zeta", "Zeta"), map_src=fit_map("zeta"), page_src=fit_page("zeta"))
        refuse("refuses a city key that is not a plain folder name",
               "the city key is not a plain folder name (letters, digits, underscore)", fit_spec,
               folder="bad folder", name="Bad", page_rel="pages/9_Bad_Heatmap.py",
               config=fit_config("bad folder", "Bad"), map_src=fit_map("bad folder"),
               page_src=fit_page("bad folder"))

        # 7. A refused city does not stop the next city, and the exit code is non-zero.
        fresh()
        city("good", "Good", "pages/1_Good_Heatmap.py",
             config=fit_config("good", "Good"), map_src=fit_map("good"), page_src=fit_page("good"))
        cities([("Good", "pages/1_Good_Heatmap.py"), ("Bad", "pages/2_Bad_Heatmap.py")])
        path = plan("2026-10-13", {
            "bad": {"relations": [1], "languages": ["de"], "fold": None},
            "good": {"relations": [1682248], "languages": ["de"], "fold": None},
        })
        rc, out = run(["--plan", str(path), "--write"])
        report("a refused city does not stop the next, and the exit code is non-zero",
               rc != 0 and (tmp / "pipeline/good/step2b_place_index.py").is_file()
               and "refused" in out and "done" in out, f"exit {rc}")

        # 8. Single-line and multi-line calls, with and without a trailing comma.
        fresh()
        variants = {
            "sl": ("pages/1_SL_Heatmap.py", "SL",
                   "    render_heatmap(output_path=HEATMAP_HTML, label_focus=None)"),
            "mlc": ("pages/2_MLC_Heatmap.py", "MLC",
                    "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None,\n    )"),
            "mln": ("pages/3_MLN_Heatmap.py", "MLN",
                    "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None\n    )"),
        }
        specs = {}
        for folder, (page_rel, name, call) in variants.items():
            w(f"pipeline/{folder}/config.py", fit_config(folder, name))
            w(f"pipeline/{folder}/step3_map.py", (
                '"""m."""\nimport sys\nfrom pathlib import Path\n\n'
                'sys.path.insert(0, str(Path(__file__).parent.parent.parent))\n'
                'from pipeline.map_common import render_heatmap  # noqa: E402\n'
                'from pipeline.{0}.config import HEATMAP_HTML  # noqa: E402\n\n\n'
                'def main():\n{1}\n\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n').format(folder, call))
            w(f"app/{page_rel}", fit_page(folder))
            specs[folder] = {"relations": [1], "languages": ["de"], "fold": None}
        cities([(name, page_rel) for _, (page_rel, name, _) in variants.items()])
        path = plan("2026-10-13", specs)
        rc, out = run(["--plan", str(path), "--write"])
        good = rc == 0
        for folder, (_, _, _) in variants.items():
            m = (tmp / f"pipeline/{folder}/step3_map.py").read_text(encoding="utf-8")
            good = good and f'place_index_url=place_index.index_url("{folder}")' in m
            try:
                compile(m, f"pipeline/{folder}/step3_map.py", "exec")
            except SyntaxError:
                good = False
        report("single-line and multi-line calls, with and without a trailing comma, all compile",
               good, f"exit {rc}")

        # 9. The page's import line naming render_map_help is left alone.
        fresh()
        city("alpha", "Alpha", "pages/1_Alpha_Heatmap.py",
             config=fit_config("alpha", "Alpha"), map_src=fit_map("alpha"),
             page_src=fit_page("alpha"))
        cities([("Alpha", "pages/1_Alpha_Heatmap.py")])
        path = plan("2026-10-13", {"alpha": {"relations": [1], "languages": ["de"], "fold": None}})
        rc, out = run(["--plan", str(path), "--write"])
        pg = (tmp / "app/pages/1_Alpha_Heatmap.py").read_text(encoding="utf-8")
        report("the import line naming render_map_help is not edited; the call gets search=",
               rc == 0 and "from components import render_map_help" in pg
               and "render_map_help('three business categories', search='alpha')" in pg
               and pg.count("search='alpha'") == 1, f"exit {rc}")

        # 10. A city whose page cannot be edited is refused whole.
        fresh()
        city("delta", "Delta", "pages/4_Delta_Heatmap.py",
             config=fit_config("delta", "Delta"), map_src=fit_map("delta"),
             page_src='"""p."""\nfrom pipeline.delta.config import HEATMAP_HTML\n')
        cities([("Delta", "pages/4_Delta_Heatmap.py")])
        path = plan("2026-10-13", {"delta": {"relations": [1], "languages": ["de"], "fold": None}})
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        good = rc != 0 and snap() == before
        good = good and "PLACE_AREA" not in (tmp / "pipeline/delta/config.py").read_text(encoding="utf-8")
        good = good and "place_index_url" not in (tmp / "pipeline/delta/step3_map.py").read_text(encoding="utf-8")
        report("a city whose page cannot be edited is refused whole, config and map untouched",
               good, f"exit {rc}")

        # 12. A folder name with an underscore is a plain folder name: 21 of
        #     the 218 unsearched cities have one (den_haag, buenos_aires).
        fresh()
        city("two_words", "Two Words", "pages/5_Two_Words_Heatmap.py",
             config=fit_config("two_words", "Two Words"), map_src=fit_map("two_words"),
             page_src=fit_page("two_words"))
        cities([("Two Words", "pages/5_Two_Words_Heatmap.py")])
        path = plan("2026-10-13", {"two_words": {"relations": [1], "languages": ["de"], "fold": None}})
        rc, out = run(["--plan", str(path), "--write"])
        report("a folder name with an underscore is scaffolded",
               rc == 0 and (tmp / "pipeline/two_words/step2b_place_index.py").is_file(),
               f"exit {rc}")

        # 13. With no NAME in the config, the step's docstring takes the name
        #     app/cities.py gives the page, accents kept, not the folder name.
        fresh()
        city("besancon", "Besançon", "pages/6_Besancon_Heatmap.py",
             config=fit_config("besancon", "x").replace('NAME = "x"\n', ""),
             map_src=fit_map("besancon"), page_src=fit_page("besancon"))
        cities([("Besançon", "pages/6_Besancon_Heatmap.py")])
        path = plan("2026-10-13", {"besancon": {"relations": [1], "languages": ["fr"], "fold": None}})
        rc, out = run(["--plan", str(path), "--write"])
        s2b = (tmp / "pipeline/besancon/step2b_place_index.py").read_bytes().decode("utf-8")
        report("a config with no NAME takes the page's name from app/cities.py",
               rc == 0 and "Build Besançon's place-search index" in s2b
               and "from app/cities.py" in out, f"exit {rc}")

        # 11. A plan that is not an object or has a bad date is refused whole.
        fresh()
        path = tmp / "plan_list.json"
        path.write_bytes(b"[]")
        rc, out = run(["--plan", str(path)])
        good = rc != 0 and "plan_list.json" in out and "JSON object" in out
        path2 = tmp / "plan_bad_date.json"
        path2.write_bytes(json.dumps({"date": "13-10-2026", "cities": {}}).encode("utf-8"))
        rc2, out2 = run(["--plan", str(path2)])
        good = good and rc2 != 0 and "plan_bad_date.json" in out2 and "ISO date" in out2
        report("a plan that is not an object or has a bad date is refused whole",
               good, f"exit {rc}/{rc2}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


def main(argv=None, root=ROOT):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", help="path to the plan JSON file")
    ap.add_argument("--write", action="store_true", help="write the scaffolded files")
    ap.add_argument("--selftest", action="store_true", help="run the self tests")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.plan:
        print(__doc__)
        return 2
    try:
        plan = json.loads(Path(args.plan).read_bytes().decode("utf-8"))
    except OSError as exc:
        print(f"cannot read {args.plan}: {exc}")
        return 1
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"cannot read {args.plan}: {exc}")
        return 1
    ok, lines = run_plan(root, plan, args.write, plan_label=args.plan)
    for line in lines:
        print(line)
    if not args.write:
        print("Nothing was written.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
