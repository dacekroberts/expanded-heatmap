"""No committed map carries an inline JavaScript array literal too big for a phone to compile.

    python scripts/check_inline_arrays.py              # every outputs/<city>/heatmap*.html
    python scripts/check_inline_arrays.py --report     # the largest literal in each map, pass or fail
    python scripts/check_inline_arrays.py --file X     # one html file (for controls)
    python scripts/check_inline_arrays.py --selftest   # watch it fail, and the escaping hold, on throwaway input

Exits non-zero naming each map whose largest inline array literal has more
than CAP elements. Read-only. `--selftest` imports pipeline/map_common.py and
runs Node, so it needs the pipeline environment; the plain check needs neither.

WHY. WebKit (the engine under every iOS browser) refuses to compile one
inline array literal above roughly 107k-131k elements, and the map goes blank
with no visible error. That blanked Mexico City, Taipei, São Paulo and Seoul on
the owner's iPhone (DECISIONS 2026-09-27). map_common now ships per-business
data as JSON.parse("..."), which the compiler sees as one string token. This
check is what keeps it that way: a Folium upgrade, a new layer written without
the parsed classes, or a city step forking the renderer would each put a big
literal back, and nothing else would notice until a reader's phone did.

WHAT IT COUNTS. The elements of each array literal inside <script> elements,
at that literal's own level: `[[1,2],[3,4]]` is a 2-element literal holding two
2-element literals. Strings, template literals and comments are skipped, so
data inside JSON.parse("...") is not counted - that is the point. Regex
literals are not recognised; the positive control in --selftest is what shows
the tokenizer still sees the literals it must.

THE CAP is well under the measured limit on purpose - the limit was measured on
one phone, and older phones may sit lower. See CAP below.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Largest inline array literal (elements at its own level) a committed map may
# carry. The owner's iPhone 16 Pro (iOS 18.7) compiles 110,861 heat pairs and
# refuses 110,862, a limit on literals made of literals; a flat array of a
# million numbers compiled (2026-09-27). With the data out of literal form the
# exact limit decides nothing, so the owner made this cap final rather than
# provisional. After the JSON.parse fix the largest literal on any re-rendered
# map is about 1,000 elements, so the cap costs nothing and leaves a factor of
# five under the proven figure for slower or older devices.
CAP = 20_000

SCRIPT = re.compile(r"<script\b[^>]*>(.*?)</script\s*>", re.S | re.I)
TOKEN = re.compile(
    r'"(?:[^"\\\n]|\\.)*"'        # double-quoted string
    r"|'(?:[^'\\\n]|\\.)*'"       # single-quoted string
    r"|`(?:[^`\\]|\\.)*`"         # template literal (no nesting needed here)
    r"|//[^\n]*"                  # line comment
    r"|/\*.*?\*/"                 # block comment
    r"|[\[\](){},]",              # structure
    re.S,
)


def literals(js):
    """Yield (elements, offset) for every array literal in a script's text."""
    stack = []  # entries: [kind, commas, open_offset]
    for m in TOKEN.finditer(js):
        tok = m.group()
        if tok in "[({":
            stack.append([tok, 0, m.start()])
        elif tok in "])}":
            want = {"]": "[", ")": "(", "}": "{"}[tok]
            # Unbalanced input (a regex literal we did not recognise): drop to
            # the nearest matching opener rather than miscount everything after.
            while stack and stack[-1][0] != want:
                stack.pop()
            if not stack:
                continue
            kind, commas, start = stack.pop()
            if kind == "[":
                empty = not js[start + 1:m.start()].strip()
                yield (0 if empty else commas + 1), start
        elif tok == ",":
            if stack:
                stack[-1][1] += 1
        # strings and comments: skipped


def largest(html):
    """(elements, snippet) of the largest inline array literal in an HTML file."""
    best, snippet = 0, ""
    for s in SCRIPT.finditer(html):
        js = s.group(1)
        for n, off in literals(js):
            if n > best:
                best, snippet = n, js[off:off + 70].replace("\n", " ")
    return best, snippet


def check_files(paths, report=False):
    failures = 0
    for p in paths:
        n, snip = largest(p.read_text(encoding="utf-8"))
        bad = n > CAP
        failures += bad
        if bad or report:
            rel = p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
            print(f"{'FAIL' if bad else 'ok  '} {rel}: largest inline array literal "
                  f"{n:,} elements (cap {CAP:,})" + (f" - starts {snip!r}" if bad else ""))
    return failures


def selftest():
    """Watch the check fail where it must, and the renderer's escaping hold."""
    sys.path.insert(0, str(ROOT))
    import folium
    from pipeline.map_common import ParsedFastMarkerCluster, ParsedHeatMap, _js_json

    problems = []

    def expect(name, cond):
        print(f"{'ok  ' if cond else 'FAIL'} {name}")
        if not cond:
            problems.append(name)

    big = CAP + 1
    pairs = [[48.1 + i / 1e6, 2.3] for i in range(big)]
    literal = "<script>var h = L.heatLayer(" + json.dumps(pairs) + ", {});</script>"
    expect("an oversized literal fails, with its count",
           largest(literal)[0] == big)
    expect("the same data as JSON.parse(\"...\") passes",
           largest("<script>var h = L.heatLayer(JSON.parse(" + _js_json(pairs) + "));</script>")[0] <= 2)
    expect("a literal after a comment holding an apostrophe is still counted",
           largest("<script>// don't stop here\nvar d = " + json.dumps(pairs) + ";</script>")[0] == big)
    expect("brackets and commas inside a string are not counted",
           largest("<script>var s = '" + json.dumps(pairs) + "';</script>")[0] <= 1)
    expect("a literal outside <script> is not counted",
           largest("<div>" + json.dumps(pairs) + "</div>")[0] == 0)
    expect("nested literals count at their own level",
           largest("<script>var a = [[1,2,3],[4,5,6]];</script>")[0] == 3)

    try:
        _js_json([[1.0, float("nan")]])
        expect("NaN fails the build", False)
    except ValueError:
        expect("NaN fails the build", True)

    hostile = [
        'Joe\'s "Bar"', "back\\slash \\u0041 not an escape", "</script><script>alert(1)</script>",
        "<!-- <script>", "a & b &amp; c", "東京ラーメン 서울 台北", "line sep para",
        "emoji 🍜", "tab\tnew\nline", "]}), fake", "$1 ${x} `tick`",
    ]
    rows = [[35.0 + i, 139.0, name, 0, 0, 0] for i, name in enumerate(hostile)]
    lit = _js_json(rows)
    expect("no '</' or '<!--' reaches the HTML", "</" not in lit and "<!--" not in lit)
    expect("no raw U+2028/U+2029 reaches the HTML", " " not in lit and " " not in lit)

    m = folium.Map()
    ParsedFastMarkerCluster(rows, callback="function (r) { return L.marker(r); }").add_to(m)
    ParsedHeatMap([r[:2] for r in rows]).add_to(m)
    html = m.get_root().render()
    parsed = re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)', html)
    expect("the rendered map carries both layers as JSON.parse", len(parsed) == 2)
    expect("the rendered map passes this check", largest(html)[0] <= CAP)

    # A real JS engine decodes what the renderer emitted, byte for byte.
    with tempfile.TemporaryDirectory() as d:
        js = Path(d) / "decode.js"
        js.write_text("const out = [" + ",".join(f"JSON.parse({p})" for p in parsed) + "];\n"
                      "process.stdout.write(JSON.stringify(out));\n", encoding="utf-8")
        try:
            got = json.loads(subprocess.run(["node", str(js)], capture_output=True, check=True,
                                            encoding="utf-8").stdout)
            expect("Node decodes the pin rows exactly, hostile names included", got[0] == rows)
            expect("Node decodes the heat points exactly", got[1] == [r[:2] for r in rows])
        except (OSError, subprocess.CalledProcessError) as e:
            expect(f"Node ran ({e})", False)

    print(f"\n{'selftest passed' if not problems else f'selftest FAILED: {len(problems)}'}")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--report", action="store_true", help="print every map, not only failures")
    ap.add_argument("--file", type=Path, help="check one html file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    paths = [a.file.resolve()] if a.file else sorted((ROOT / "outputs").glob("*/heatmap*.html"))
    failures = check_files(paths, report=a.report)
    print(f"{len(paths)} map(s) checked, {failures} over the cap of {CAP:,} elements per inline array literal.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
