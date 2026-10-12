"""Write the place-search boilerplate a built city needs, from a plan file.

    python scripts/place_search_scaffold.py --plan PLAN_JSON [--write]
    python scripts/place_search_scaffold.py --draft-plan OUT_JSON --date DATE [CITY ...]
    python scripts/place_search_scaffold.py --selftest

The script decides nothing about a city. It copies one fixed pattern: a
PLACE_* block at the end of the config, a step2b_place_index.py, one argument
in the map step and one in the page. Whatever does not fit is refused, city by
city, and a plan that is not the shape below is refused whole.

--draft-plan writes a DRAFT plan from what the repository already knows about
each city: the boundary relation its config names, and its local language from
pipeline/travel_packs.py's LOCAL_LANG. A draft decides nothing. It carries a
top-level "draft": true, which --write refuses whole; a session reads the
draft, corrects the relations it could not fill, removes the draft line, and
only then scaffolds from it. With CITY names only those cities are drafted; a
named city with no config.py or an existing PLACE_AREA is reported, left out,
and makes the run exit non-zero. With no CITY, every folder under pipeline/
whose config.py has no PLACE_AREA is drafted, in sorted order. --date is
required with --draft-plan and must be an ISO date (YYYY-MM-DD).

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
_PLACE_AREA_RE = re.compile(r"(?m)^PLACE_AREA\s*=")


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


def _local_lang(root):
    """LOCAL_LANG read from pipeline/travel_packs.py, or None."""
    path = root / "pipeline" / "travel_packs.py"
    try:
        text = _read(path)
    except OSError:
        return None
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "LOCAL_LANG"):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError):
                return None
            return value if isinstance(value, dict) else None
    return None


def _qualifies(name, folder):
    """True when a top-level assignment name is a boundary relation: it holds
    RELATION and one of BOUNDARY, CITY or KOMMUNE, or it is the folder name in
    upper case plus _RELATION. A name holding LINE or SKIPPED never counts."""
    upper = name.upper()
    if "LINE" in upper or "SKIPPED" in upper or "RELATION" not in upper:
        return False
    if name == folder.upper() + "_RELATION":
        return True
    return "BOUNDARY" in upper or "CITY" in upper or "KOMMUNE" in upper


def _boundary_assignments(config_text, folder):
    """{name: value} for the config's qualifying boundary-relation
    assignments, each value read as a literal (None when it is not one)."""
    try:
        tree = ast.parse(config_text)
    except SyntaxError:
        return {}
    found = {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            continue
        name = node.targets[0].id
        if not _qualifies(name, folder):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError):
            value = None
        found[name] = value
    return found


def _relation_value(value, name):
    """(relations, why) for one qualifying assignment's value: relation ids
    in order, and why a reason the value was not a recognised shape (None
    when it was)."""
    if value is None:
        return [], f"{name} is not a literal value"
    if isinstance(value, bool):
        return [], f"{name} is a bool, not a relation shape"
    if isinstance(value, int):
        return [value], None
    if isinstance(value, (list, tuple)):
        if value and all(isinstance(r, int) and not isinstance(r, bool) for r in value):
            return list(value), None
        kind = type(value).__name__
        return [], (f"{name} is an empty {kind}" if not value
                    else f"{name} is a {kind} whose items are not all integers")
    if isinstance(value, dict):
        keys = [k for k in value if isinstance(k, int) and not isinstance(k, bool)]
        if keys:
            return keys, None
        # The Czech configs map a municipality code to its relation:
        # {"582786": 438171}. Every value an integer, no key one.
        values = list(value.values())
        if values and all(isinstance(v, int) and not isinstance(v, bool) for v in values):
            return values, None
        return [], f"{name} is a dict with integers as neither its keys nor its values"
    return [], f"{name} is {type(value).__name__}, not a recognised relation shape"


def _config_relations(config_text, folder):
    """(relations, note) from one config's source: the boundary relation ids
    when exactly one qualifying assignment holds a recognised shape, else an
    empty list and a note that says why."""
    assigns = _boundary_assignments(config_text, folder)
    if not assigns:
        return [], "no boundary relation in the config: look it up"
    if len(assigns) > 1:
        names = ", ".join(sorted(assigns))
        return [], f"{len(assigns)} boundary names ({names}): none chosen, look it up"
    (name, value), = assigns.items()
    relations, why = _relation_value(value, name)
    if why is not None:
        return [], f"{why}, look it up"
    return relations, (f"relation from {name}: confirm it is the boundary the "
                       f"map draws, not a district or a line")


def _draft_cities(root):
    """Sorted folder names under pipeline/ whose config.py exists and does
    not already contain PLACE_AREA."""
    out = []
    for path in sorted((root / "pipeline").iterdir()):
        if not path.is_dir():
            continue
        config = path / "config.py"
        if not config.is_file():
            continue
        try:
            scaffolded = _PLACE_AREA_RE.search(_read(config))
        except (OSError, UnicodeDecodeError):
            scaffolded = None
        if scaffolded:
            continue
        out.append(path.name)
    return out


def _city_entry(folder, config_text, code, language_names, folds):
    """One city's draft entry. code is the city's LOCAL_LANG code, or None
    for the English default."""
    relations, relation_note = _config_relations(config_text, folder)
    languages = [code] if code is not None else ["en"]
    fold = "ja" if code == "ja" and "ja" in folds else None
    clauses = [relation_note]
    if code is None:
        clauses.append("language is the default (English), not a listing")
    elif code not in language_names:
        clauses.append(f"language {code!r} is not built yet")
    else:
        clauses.append("language from LOCAL_LANG")
    if fold == "ja":
        clauses.append("fold ja, as every Japanese city")
    return {"relations": relations, "languages": languages, "fold": fold,
            "note": "; ".join(clauses)}


def draft_plan(root, date, city_names):
    """(ok, lines, plan) for a --draft-plan run. city_names names the cities
    to draft, or [] to draft every pipeline folder with a config.py and no
    PLACE_AREA. plan is the draft object, or None when a required file cannot
    be read."""
    constants = _place_index_constants(root)
    if constants is None:
        return False, ["cannot read LANGUAGE_NAMES and FOLDS from pipeline/place_index.py"], None
    language_names, folds = constants
    lang_map = _local_lang(root)
    if lang_map is None:
        return False, ["cannot read LOCAL_LANG from pipeline/travel_packs.py"], None
    lang_of, twice = {}, {}
    for code, listed in lang_map.items():
        for name in listed:
            if name in lang_of and lang_of[name] != code:
                twice.setdefault(name, [lang_of[name]]).append(code)
            lang_of.setdefault(name, code)
    folders = sorted(set(city_names)) if city_names else _draft_cities(root)
    ok = True
    lines = []
    cities = {}
    filled = empty = default = not_built = 0
    for folder in folders:
        config_path = root / "pipeline" / folder / "config.py"
        if not config_path.is_file():
            if city_names:
                lines.append(f"{folder}: left out (no config.py)")
                ok = False
            continue
        try:
            config_text = _read(config_path)
        except (OSError, UnicodeDecodeError):
            if city_names:
                lines.append(f"{folder}: left out (config.py cannot be read)")
                ok = False
            continue
        if _PLACE_AREA_RE.search(config_text):
            if city_names:
                lines.append(f"{folder}: left out (config already contains PLACE_AREA)")
                ok = False
            continue
        code = lang_of.get(folder)
        entry = _city_entry(folder, config_text, code, language_names, folds)
        if folder in twice:
            entry["languages"] = twice[folder]
            entry["note"] += ("; LOCAL_LANG lists this city under "
                              f"{' and '.join(twice[folder])}: choose")
        cities[folder] = entry
        if entry["relations"]:
            filled += 1
        else:
            empty += 1
        if code is None:
            default += 1
        elif code not in language_names:
            not_built += 1
    lines.append("")
    lines.append(f"Drafted {len(cities)} cities.")
    lines.append(f"  relations filled: {filled}")
    lines.append(f"  relations empty: {empty}")
    lines.append(f"  language default (English): {default}")
    lines.append(f"  language not built yet: {not_built}")
    return ok, lines, {"draft": True, "date": date, "cities": cities}


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
    """(path, text, None) for the city's page among those app/cities.py
    lists: the ONE page that imports pipeline.<folder>.config as a module
    (found by parsing, so a mention in a comment is no import). (None,
    None, why) when no listed page does, or more than one: a regional page
    that also reads the city's config must not get the city's search."""
    wanted = f"pipeline.{folder}.config"
    found = []
    for rel in pages:
        path = root / "app" / rel
        if not path.is_file():
            continue
        try:
            text = _read(path)
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
                modules.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                modules.update(a.name for a in node.names)
        if wanted in modules:
            found.append((path, text))
    if not found:
        return None, None, "page file cannot be found from app/cities.py"
    if len(found) > 1:
        names = ", ".join(sorted(p.name for p, _ in found))
        return None, None, f"more than one listed page imports {wanted} ({names})"
    return found[0][0], found[0][1], None


def _offset(text, lineno, col_bytes):
    """The index in text of an ast position: a 1-based line and a column
    counted in UTF-8 bytes, as ast gives it."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    start = starts[lineno - 1]
    end = text.find("\n", start)
    line = text[start:] if end == -1 else text[start:end]
    return start + len(line.encode("utf-8")[:col_bytes].decode("utf-8"))


def _find_call(text, name):
    """Where the one call of name sits in text, found by parsing: a mention in
    a docstring, a comment, an import or a def is not a call. Returns a dict
    with the index of its opening and closing parenthesis, the start of its
    first argument and the end of its last (None when it has none), or None
    when the file does not parse or holds no such call or more than one."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and (
        (isinstance(n.func, ast.Name) and n.func.id == name)
        or (isinstance(n.func, ast.Attribute) and n.func.attr == name))]
    if len(calls) != 1:
        return None
    call = calls[0]
    func_end = _offset(text, call.func.end_lineno, call.func.end_col_offset)
    open_i = text.find("(", func_end)
    close_i = _offset(text, call.end_lineno, call.end_col_offset) - 1
    if open_i == -1 or close_i <= open_i or text[close_i] != ")":
        return None
    parts = list(call.args) + list(call.keywords)
    first = last = None
    if parts:
        first = min(_offset(text, p.lineno, p.col_offset) for p in parts)
        last = max(_offset(text, p.end_lineno, p.end_col_offset) for p in parts)
    return {"open": open_i, "close": close_i, "first": first, "last": last}


def _has_comma(tail):
    """True when the text between a call's last argument and its closing
    parenthesis holds a comma outside a comment. No string can sit there."""
    return any("," in line.split("#", 1)[0] for line in tail.split("\n"))


def _add_call_argument(text, name, arg_text):
    """text with arg_text added as the last argument of the one name( call.
    Handles a call on one line and one spread over several lines, with or
    without a trailing comma, keeping the file's own indentation. The last
    argument's end comes from the parse, so a comment, a nested call or a
    string of several lines inside the call cannot move the edit."""
    loc = _find_call(text, name)
    if loc is None:
        raise ValueError(f"{name}( is not exactly one call in the file")
    open_i, close_i, first, last = loc["open"], loc["close"], loc["first"], loc["last"]
    inner = text[open_i + 1:close_i]
    comma = last is not None and _has_comma(text[last:close_i])
    if "\n" not in inner:
        if last is None:
            return text[:close_i] + arg_text + text[close_i:]
        if comma:
            gap = "" if text[close_i - 1] in " \t" else " "
            return text[:close_i] + gap + arg_text + text[close_i:]
        return text[:last] + ", " + arg_text + text[last:]
    nl = text.rfind("\n", open_i + 1, close_i)
    indent = text[nl + 1:close_i]
    if indent.strip():
        raise ValueError(f"the closing parenthesis of {name}( is not on its own line")
    arg_indent = indent + "    "
    if first is not None and "\n" in text[open_i:first]:
        line_start = text.rfind("\n", 0, first) + 1
        arg_indent = text[line_start:first]
        if arg_indent.strip():
            arg_indent = indent + "    "
    head = text[:nl + 1]
    if last is not None and not comma:
        head = text[:last] + "," + text[last:nl + 1]
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


def scaffold_city(root, folder, spec, date, write, pages, language_names, folds,
                  write_file=None):
    """Scaffold one city. Returns (status, reason, lines) where status is
    "done", "would do" or "refused". A refused city writes nothing; a fitting
    city is checked on all four files before any of them is written."""
    write_file = write_file or _write
    reason = _spec_errors(folder, spec, language_names, folds)
    if reason is not None:
        return "refused", reason, []

    config_path = root / "pipeline" / folder / "config.py"
    if not config_path.is_file():
        return "refused", "no config.py", []
    try:
        config_text = _read(config_path)
    except (OSError, UnicodeDecodeError) as exc:
        return "refused", f"config.py cannot be read: {exc}", []
    if _PLACE_AREA_RE.search(config_text):
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
    try:
        map_text = _read(map_path)
    except (OSError, UnicodeDecodeError) as exc:
        return "refused", f"{map_path.name} cannot be read: {exc}", []
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

    page_path, page_text, why = _find_page(root, folder, pages)
    if page_path is None:
        return "refused", why, []
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
        # All four or none: a write that fails part-way puts back every
        # file already written, so a city is never left half scaffolded
        # (and then refused next time for the wrong reason).
        before = {config_path: config_text, map_path: map_text, page_path: page_text}
        written = []
        try:
            for path, text in ((config_path, new_config_text),
                               (step2b_path, new_step2b_text),
                               (map_path, new_map_text),
                               (page_path, new_page_text)):
                written.append(path)
                write_file(path, text)
        except OSError as exc:
            failed = written[-1].name
            left = []
            for path in written:
                try:
                    if path in before:
                        _write(path, before[path])
                    elif path.exists():
                        path.unlink()
                except OSError:
                    left.append(path.name)
            reason = f"writing {failed} failed ({exc}); every file was put back"
            if left:
                reason = (f"writing {failed} failed ({exc}); could NOT put back "
                          f"{', '.join(left)}: restore by hand before running again")
            return "refused", reason, []

    return ("done" if write else "would do"), None, lines


def run_plan(root, plan, write, plan_label="plan.json"):
    """Validate a plan and scaffold each city. Returns (ok, lines)."""
    if not isinstance(plan, dict):
        return False, [f"{plan_label}: the plan must be a JSON object with date and cities"]
    if write and plan.get("draft") not in (None, False):
        return False, [f'{plan_label}: the plan is a draft ("draft": true); a session must '
                       f"read and correct it, then remove the draft line before --write"]
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
        w("pipeline/travel_packs.py",
          'LOCAL_LANG = {"de": ["zurich"], "fr": ["angers"], "ja": ["kobe", "osaka"],\n'
          '             "zh-Hant": ["taipei"]}\n')

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

        # --- --draft-plan cases ----------------------------------------------

        # A single integer boundary relation is drafted as a one-item list,
        # the language from LOCAL_LANG and fold null.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1682248\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "zurich"])
        entry = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]["zurich"]
        report("an integer BOUNDARY_RELATION drafts as a one-item list with its language",
               rc == 0 and entry == {
                   "relations": [1682248], "languages": ["de"], "fold": None,
                   "note": "relation from BOUNDARY_RELATION: confirm it is the boundary "
                           "the map draws, not a district or a line; language from LOCAL_LANG"},
               f"exit {rc}")

        # A dict drafts its integer keys in order, a tuple its items, and the
        # cities file is in sorted order.
        fresh()
        w("pipeline/liverpool/config.py",
          '"""c."""\nBOUNDARY_OSM_RELATIONS = {172987: "Liverpool", 173023: "Sefton"}\n')
        w("pipeline/sydney/config.py", '"""c."""\nBOUNDARY_OSM_RELATION = (1251066, 777)\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13"])
        data = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]
        report("a dict drafts its integer keys in order and a tuple its items, cities sorted",
               rc == 0 and data["liverpool"]["relations"] == [172987, 173023]
               and data["sydney"]["relations"] == [1251066, 777]
               and list(data) == ["liverpool", "sydney"], f"exit {rc}")

        # No boundary relation gives an empty list and a note that says so.
        fresh()
        w("pipeline/angers/config.py", '"""c."""\nNAME = "Angers"\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "angers"])
        entry = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]["angers"]
        report("a config with no boundary relation drafts an empty list and says to look it up",
               rc == 0 and entry["relations"] == []
               and "no boundary relation in the config: look it up" in entry["note"],
               f"exit {rc}")

        # Two qualifying names are never chosen between.
        fresh()
        w("pipeline/duo/config.py", '"""c."""\nBOUNDARY_RELATION = 1\nOSM_BOUNDARY_RELATION = 2\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "duo"])
        entry = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]["duo"]
        report("two qualifying names are not chosen between: empty list, note names both",
               rc == 0 and entry["relations"] == []
               and "BOUNDARY_RELATION" in entry["note"] and "OSM_BOUNDARY_RELATION" in entry["note"],
               f"exit {rc}")

        # LINE_RELATIONS alone is not a boundary.
        fresh()
        w("pipeline/liner/config.py", '"""c."""\nLINE_RELATIONS = {1: "x"}\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "liner"])
        entry = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]["liner"]
        report("LINE_RELATIONS alone is not a boundary: empty list",
               rc == 0 and entry["relations"] == []
               and "no boundary relation in the config: look it up" in entry["note"],
               f"exit {rc}")

        # The language comes from LOCAL_LANG; a city in no list gets the
        # default (English) and a note that says it is the default.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1\n')
        w("pipeline/boston/config.py", '"""c."""\nBOUNDARY_RELATION = 2\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13"])
        data = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]
        report("the language comes from LOCAL_LANG, else the English default with a note",
               rc == 0 and data["zurich"]["languages"] == ["de"]
               and "language from LOCAL_LANG" in data["zurich"]["note"]
               and data["boston"]["languages"] == ["en"]
               and "the default (English), not a listing" in data["boston"]["note"], f"exit {rc}")

        # A language in LOCAL_LANG but not in LANGUAGE_NAMES is still written,
        # the note says it is not built yet, and the summary counts it.
        fresh()
        w("pipeline/taipei/config.py", '"""c."""\nBOUNDARY_RELATION = 3\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "taipei"])
        entry = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]["taipei"]
        report("a language not in LANGUAGE_NAMES is still written and the note says so",
               rc == 0 and entry["languages"] == ["zh-Hant"]
               and "not built yet" in entry["note"]
               and "language not built yet: 1" in out, f"exit {rc}")

        # A Japanese city gets fold ja, a German one null.
        fresh()
        w("pipeline/kobe/config.py", '"""c."""\nBOUNDARY_RELATION = 1\n')
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 2\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13"])
        data = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]
        report("a Japanese city gets fold ja and a German one null",
               rc == 0 and data["kobe"]["fold"] == "ja" and "fold ja" in data["kobe"]["note"]
               and data["zurich"]["fold"] is None, f"exit {rc}")

        # A city with PLACE_AREA is left out of a full draft, and naming it
        # makes the run exit non-zero.
        fresh()
        w("pipeline/kept/config.py", '"""c."""\nBOUNDARY_RELATION = 1\n')
        w("pipeline/held/config.py",
          '"""c."""\nPLACE_AREA = "(id:3609999999)"\nBOUNDARY_RELATION = 2\n')
        out_path = tmp / "draft.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13"])
        data = json.loads(out_path.read_bytes().decode("utf-8"))["cities"]
        good = rc == 0 and "kept" in data and "held" not in data
        out_path2 = tmp / "draft2.json"
        rc2, out2 = run(["--draft-plan", str(out_path2), "--date", "2026-10-13", "held"])
        data2 = json.loads(out_path2.read_bytes().decode("utf-8"))["cities"]
        report("a city with PLACE_AREA is left out of a full draft, and a named one fails the run",
               good and rc2 != 0 and "left out" in out2 and "PLACE_AREA" in out2 and data2 == {},
               f"exit {rc}/{rc2}")

        # An existing OUT_JSON is not overwritten.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1\n')
        out_path = tmp / "draft.json"
        out_path.write_bytes(b'{"keep": true}')
        before = out_path.read_bytes()
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13", "zurich"])
        report("an existing OUT_JSON is not overwritten and the run exits non-zero",
               rc != 0 and out_path.read_bytes() == before and "already exists" in out,
               f"exit {rc}")

        # Two runs to two files give identical bytes, with no carriage return.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1682248\n')
        w("pipeline/angers/config.py", '"""c."""\nNAME = "Angers"\n')
        p1 = tmp / "d1.json"
        p2 = tmp / "d2.json"
        rc1, _ = run(["--draft-plan", str(p1), "--date", "2026-10-13"])
        rc2, _ = run(["--draft-plan", str(p2), "--date", "2026-10-13"])
        b1 = p1.read_bytes()
        report("two runs give identical bytes with no carriage return",
               rc1 == 0 and rc2 == 0 and b1 == p2.read_bytes() and b"\r" not in b1,
               f"exit {rc1}/{rc2}")

        # --write on a plan with "draft": true is refused whole.
        fresh()
        city("alpha", "Alpha", "pages/1_Alpha_Heatmap.py",
             config=fit_config("alpha", "Alpha"), map_src=fit_map("alpha"),
             page_src=fit_page("alpha"))
        cities([("Alpha", "pages/1_Alpha_Heatmap.py")])
        draft_path = tmp / "draft_plan.json"
        draft_path.write_bytes(json.dumps({
            "draft": True, "date": "2026-10-13",
            "cities": {"alpha": {"relations": [], "languages": ["de"], "fold": None,
                                 "note": "no boundary relation in the config: look it up"}}}).encode("utf-8"))
        before = snap()
        rc, out = run(["--plan", str(draft_path), "--write"])
        report('--write on a plan with "draft": true is refused whole and names the draft line',
               rc != 0 and snap() == before and '"draft": true' in out, f"exit {rc}")

        # The same draft without --write runs as a dry run, not a draft refusal.
        rc, out = run(["--plan", str(draft_path)])
        report("the same draft without --write dry-runs, its empty-relations city refused",
               rc != 0 and '"draft": true' not in out and "Nothing was written." in out
               and "relations must be a non-empty list" in out, f"exit {rc}")

        # The corrected plan (draft line gone, relations filled) writes.
        fixed_path = tmp / "fixed_plan.json"
        fixed_path.write_bytes(json.dumps({
            "date": "2026-10-13",
            "cities": {"alpha": {"relations": [7], "languages": ["de"], "fold": None}}}).encode("utf-8"))
        rc, out = run(["--plan", str(fixed_path), "--write"])
        cfg = (tmp / "pipeline/alpha/config.py").read_text(encoding="utf-8")
        report("the corrected plan (draft line gone, relations filled) writes",
               rc == 0 and 'PLACE_AREA = "(id:3600000007)"' in cfg, f"exit {rc}")

        # --draft-plan without --date, and with a non-ISO date, both fail.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1\n')
        out_path = tmp / "draft.json"
        rc1, out1 = run(["--draft-plan", str(out_path)])
        rc2, out2 = run(["--draft-plan", str(out_path), "--date", "13-10-2026"])
        report("--draft-plan without --date or with a non-ISO date exits non-zero with a sentence",
               rc1 != 0 and "date" in out1 and rc2 != 0 and "ISO" in out2,
               f"exit {rc1}/{rc2}")

        # The Czech shape, a municipality code mapped to its relation, drafts
        # the VALUES; a dict with integers on neither side stays empty.
        fresh()
        w("pipeline/brno/config.py", '"""c."""\nOSM_BOUNDARY_RELATIONS = {"582786": 438171}\n')
        w("pipeline/words/config.py", '"""c."""\nOSM_BOUNDARY_RELATIONS = {"a": "b"}\n')
        ok_draft, lines_draft, plan_draft = draft_plan(tmp, "2026-10-13", ["brno", "words"])
        report("a dict of code to relation drafts its values; one with no integers stays empty",
               ok_draft and plan_draft["cities"]["brno"]["relations"] == [438171]
               and plan_draft["cities"]["words"]["relations"] == []
               and "neither" in plan_draft["cities"]["words"]["note"], "")

        # Found by an adversarial review (2026-10-12): each is a way a city's
        # files could be left wrong and look right.
        one = {"relations": [1], "languages": ["de"], "fold": None}

        def scaffolded(folder, name, page_rel, map_src=None, page_src=None, config=None):
            fresh()
            city(folder, name, page_rel,
                 config=config or fit_config(folder, name),
                 map_src=map_src or fit_map(folder), page_src=page_src or fit_page(folder))
            cities([(name, page_rel)])
            return plan("2026-10-13", {folder: one})

        # A call named in the docstring is not the call.
        path = scaffolded("doc", "Doc", "pages/1_Doc_Heatmap.py", map_src=fit_map("doc").replace(
            '"""Step 3 - render doc."""',
            '"""Step 3 - render doc with the shared render_heatmap (pipeline/map_common.py)."""'))
        rc, out = run(["--plan", str(path), "--write"])
        m = (tmp / "pipeline/doc/step3_map.py").read_bytes().decode("utf-8")
        report("a call named in a docstring is left alone; the real call gets the argument",
               rc == 0 and "(pipeline/map_common.py)." in m
               and '        place_index_url=place_index.index_url("doc"),\n    )' in m, f"exit {rc}")

        # A string of several lines as the last argument keeps its text.
        text_arg = ('    render_heatmap(\n        output_path=HEATMAP_HTML,\n'
                    '        map_title="""Line one\n# and line two""",\n    )')
        path = scaffolded("multi", "Multi", "pages/2_Multi_Heatmap.py", map_src=fit_map("multi").replace(
            "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None,\n    )",
            text_arg))
        rc, out = run(["--plan", str(path), "--write"])
        m = (tmp / "pipeline/multi/step3_map.py").read_bytes().decode("utf-8")
        report("a comma never lands inside a string of several lines",
               rc == 0 and '"""Line one\n# and line two""",\n        place_index_url=' in m,
               f"exit {rc}")

        # A page that mentions another city's config in a comment is not its page.
        fresh()
        city("solo", "Solo", "pages/3_Solo_Heatmap.py", config=fit_config("solo", "Solo"),
             map_src=fit_map("solo"), page_src=fit_page("solo"))
        w("app/pages/1_Other_Heatmap.py",
          '"""page other."""\n# reads the same register as pipeline.solo.config\n'
          "from pipeline.other.config import HEATMAP_HTML\n"
          "from components import render_map_help\n\n\nrender_map_help('other')\n")
        cities([("Other", "pages/1_Other_Heatmap.py"), ("Solo", "pages/3_Solo_Heatmap.py")])
        path = plan("2026-10-13", {"solo": one})
        rc, out = run(["--plan", str(path), "--write"])
        report("a page that only mentions the city's config in a comment is not edited",
               rc == 0
               and "search=" not in (tmp / "app/pages/1_Other_Heatmap.py").read_bytes().decode("utf-8")
               and "search='solo'" in (tmp / "app/pages/3_Solo_Heatmap.py").read_bytes().decode("utf-8"),
               f"exit {rc}")

        # Two listed pages importing one config: refused, nothing chosen.
        fresh()
        city("pair", "Pair", "pages/4_Pair_Heatmap.py", config=fit_config("pair", "Pair"),
             map_src=fit_map("pair"), page_src=fit_page("pair"))
        w("app/pages/5_Pair_Regional_Heatmap.py", fit_page("pair"))
        cities([("Pair", "pages/4_Pair_Heatmap.py"), ("Pair (Regional)", "pages/5_Pair_Regional_Heatmap.py")])
        path = plan("2026-10-13", {"pair": one})
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report("two listed pages importing one config refuse the city and change nothing",
               rc != 0 and snap() == before and "more than one listed page" in out, f"exit {rc}")

        # A write that fails on the third file puts the first two back.
        path = scaffolded("half", "Half", "pages/6_Half_Heatmap.py")
        before = snap()

        def failing(target, text):
            if target.name == "step3_map.py":
                raise OSError("the file is locked")
            _write(target, text)

        status, reason, _ = scaffold_city(
            tmp, "half", one, "2026-10-13", True, _cities_pages(tmp),
            {"de": "German"}, (None, "ja"), write_file=failing)
        report("a write that fails part-way puts every file back and says so",
               status == "refused" and snap() == before and "every file was put back" in reason,
               reason)

        # PLACE_AREA named only in a comment is not a scaffolded city.
        path = scaffolded("noted", "Noted", "pages/7_Noted_Heatmap.py",
                          config=fit_config("noted", "Noted") + "# PLACE_AREA goes here later\n")
        rc, out = run(["--plan", str(path), "--write"])
        report("PLACE_AREA in a comment does not refuse the city", rc == 0, f"exit {rc}")
        fresh()
        w("pipeline/noted/config.py", '"""c."""\n# PLACE_AREA goes here later\n')
        out_path = tmp / "draft_noted.json"
        rc, out = run(["--draft-plan", str(out_path), "--date", "2026-10-13"])
        report("a full draft keeps a city whose config only mentions PLACE_AREA",
               rc == 0 and "noted" in json.loads(out_path.read_bytes().decode("utf-8"))["cities"],
               f"exit {rc}")

        # A draft flag that is not exactly true still stops --write.
        path = scaffolded("flag", "Flag", "pages/8_Flag_Heatmap.py")
        outcomes = []
        for flag in ("true", 1):
            path.write_bytes(json.dumps({"draft": flag, "date": "2026-10-13",
                                         "cities": {"flag": one}}).encode("utf-8"))
            before = snap()
            rc, out = run(["--plan", str(path), "--write"])
            outcomes.append(rc != 0 and snap() == before and "draft" in out)
        report('a draft flag written as "true" or 1 stops --write as true does', all(outcomes), "")

        # A draft is not written into the source tree, nor into a new folder.
        fresh()
        w("pipeline/zurich/config.py", '"""c."""\nBOUNDARY_RELATION = 1682248\n')
        rc, out = run(["--draft-plan", str(tmp / "pipeline" / "draft.json"), "--date", "2026-10-13"])
        rc2, out2 = run(["--draft-plan", str(tmp / "no_such" / "draft.json"), "--date", "2026-10-13"])
        report("a draft is refused inside pipeline/ and in a folder that does not exist",
               rc != 0 and not (tmp / "pipeline" / "draft.json").exists() and "inside pipeline/" in out
               and rc2 != 0 and not (tmp / "no_such").exists(), f"exit {rc}/{rc2}")

        # A city listed under two languages is not settled by the last read.
        fresh()
        w("pipeline/travel_packs.py", 'LOCAL_LANG = {"fr": ["twin"], "nl": ["twin"]}\n')
        w("pipeline/twin/config.py", '"""c."""\nBOUNDARY_RELATION = 5\n')
        ok_draft, _, plan_draft = draft_plan(tmp, "2026-10-13", ["twin"])
        report("a city listed under two languages drafts both and says to choose",
               plan_draft["cities"]["twin"]["languages"] == ["fr", "nl"]
               and "choose" in plan_draft["cities"]["twin"]["note"]
               and plan_draft.get("draft") is True, "")

        # A map step that renders through a shared country module holds no
        # render_heatmap call, only a mention in its docstring: 33 of the 218
        # unsearched cities (the French, British and other batches). Refused,
        # with every file unchanged; the docstring is never edited.
        path = scaffolded("shared", "Shared", "pages/9_Shared_Heatmap.py", map_src=(
            '"""Step 3 - all rendering is map_common\'s render_heatmap(); nothing forks it."""\n'
            "import sys\nfrom pathlib import Path\n\n"
            "sys.path.insert(0, str(Path(__file__).parent.parent.parent))\n\n"
            "from pipeline.countries.some_country import render\n"
            "from pipeline.shared import config\n\n"
            'if __name__ == "__main__":\n    render(config, "Shared")\n'))
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report("a map step with no render_heatmap call of its own is refused, docstring untouched",
               rc != 0 and snap() == before and "is not exactly one call" in out, f"exit {rc}")

        # Two calls: refused, neither chosen.
        path = scaffolded("twice", "Twice", "pages/1_Twice_Heatmap.py", map_src=fit_map("twice").replace(
            "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None,\n    )",
            "    render_heatmap(output_path=HEATMAP_HTML)\n    render_heatmap(output_path=HEATMAP_HTML)"))
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report("a map step with two render_heatmap calls is refused",
               rc != 0 and snap() == before and "is not exactly one call" in out, f"exit {rc}")

        # A closing parenthesis that shares its line with the last argument.
        path = scaffolded("tight", "Tight", "pages/2_Tight_Heatmap.py", map_src=fit_map("tight").replace(
            "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None,\n    )",
            "    render_heatmap(\n        output_path=HEATMAP_HTML,\n        label_focus=None)"))
        before = snap()
        rc, out = run(["--plan", str(path), "--write"])
        report("a closing parenthesis on the last argument's line is refused, not reformatted",
               rc != 0 and snap() == before and "not on its own line" in out, f"exit {rc}")

        # A rail line's relations are never a boundary, whatever else the name holds.
        fresh()
        w("pipeline/liner2/config.py", '"""c."""\nCITY_LINE_RELATIONS = [11, 12]\n')
        ok_draft, _, plan_draft = draft_plan(tmp, "2026-10-13", ["liner2"])
        report("a name holding LINE is never a boundary relation",
               plan_draft["cities"]["liner2"]["relations"] == [], "")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


def main(argv=None, root=ROOT):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", help="path to the plan JSON file")
    ap.add_argument("--write", action="store_true", help="write the scaffolded files")
    ap.add_argument("--draft-plan", help="path to write the draft plan JSON file to")
    ap.add_argument("--date", help="ISO date (YYYY-MM-DD), required with --draft-plan")
    ap.add_argument("cities", nargs="*", help="city folder names to draft (default: all)")
    ap.add_argument("--selftest", action="store_true", help="run the self tests")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.draft_plan:
        if not args.date:
            print("--draft-plan needs --date, an ISO date (YYYY-MM-DD)")
            return 2
        if not _iso_date(args.date):
            print(f"--draft-plan needs --date as an ISO date (YYYY-MM-DD), not {args.date!r}")
            return 1
        ok, lines, plan = draft_plan(root, args.date, args.cities)
        for line in lines:
            print(line)
        if plan is None:
            return 1
        out_path = Path(args.draft_plan)
        if out_path.exists():
            print(f"not overwriting {args.draft_plan}: the file already exists")
            return 1
        resolved = out_path.resolve()
        for tree in ("pipeline", "app", "outputs"):
            inside = (root / tree).resolve()
            if inside == resolved or inside in resolved.parents:
                print(f"not writing a draft inside {tree}/: name a file outside "
                      f"the source tree, {args.draft_plan} is not one")
                return 1
        if not out_path.parent.is_dir():
            print(f"the folder of {args.draft_plan} does not exist: create it or "
                  f"name another file")
            return 1
        _write(out_path, json.dumps(plan, ensure_ascii=False, indent=2))
        print(f"Wrote {args.draft_plan}")
        return 0 if ok else 1
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
