"""Every committed map carries the <html lang> its map step asks for.

    python scripts/check_html_lang.py [--selftest]

WHY. render_heatmap() writes the map, then re-reads it and writes it again to
add `lang` (folium's template has no slot for it). On 2026-10-03 a transient
OSError (Errno 22) on that second write left Kawasaki's and Kyoto's maps as
bare <html> during the touch re-render (mobile-tap-targets drafts), and
check_render_current.py passed them: it compares data, not the root tag.
Without `lang` a browser picks Chinese glyph forms for Japanese text
(pipeline/theme.font_stack, the cjk-text skill).

THE RULE. A city whose map step (pipeline/<slug>/step*map*.py) passes a
literal lang="xx" must ship outputs/<slug>/heatmap.html opening <html lang="xx">;
a city that passes none must ship a bare <html>. Exit 1 on any mismatch.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANG_ARG = re.compile(r"""\blang\s*=\s*["']([A-Za-z]{2,3}(?:-[A-Za-z]{2,4})?)["']""")
HTML_TAG = re.compile(r"<html(?:\s+lang=\"([^\"]*)\")?\s*>")


def wanted_lang(step_source):
    """The lang a map step passes, or None. More than one is an error."""
    found = set(LANG_ARG.findall(step_source))
    if len(found) > 1:
        raise ValueError(f"more than one lang passed: {sorted(found)}")
    return found.pop() if found else None


def shipped_lang(html_head):
    """(has_html_tag, lang or None) from the start of a rendered map."""
    m = HTML_TAG.search(html_head)
    return (m is not None, m.group(1) if m else None)


def verdict(want, html_head):
    """None if the map matches its step, else a one-line problem."""
    has_tag, got = shipped_lang(html_head)
    if not has_tag:
        return "no <html> tag in the first 4 KB"
    if want != got:
        return (f"step passes lang={want!r} but the map opens "
                + (f'<html lang="{got}">' if got else "<html> with no lang"))
    return None


def check():
    problems, n = [], 0
    for step in sorted(ROOT.glob("pipeline/*/step*map*.py")):
        slug = step.parent.name
        out = ROOT / "outputs" / slug / "heatmap.html"
        if not out.exists():
            continue                     # check_render_current.py's concern
        try:
            want = wanted_lang(step.read_text(encoding="utf-8"))
        except ValueError as e:
            problems.append(f"{slug}: {step.name}: {e}")
            continue
        with out.open(encoding="utf-8") as f:
            head = f.read(4096)
        n += 1
        bad = verdict(want, head)
        if bad:
            problems.append(f"{slug}: {bad}")
    return n, problems


def selftest():
    cases = [
        ("ja passed and shipped", 'render_heatmap(x, lang="ja")', '<!DOCTYPE html>\n<html lang="ja">', True),
        ("ja passed, bare tag (the 2026-10-03 case)", 'lang="ja",', "<!DOCTYPE html>\n<html>", False),
        ("none passed, bare tag", "render_heatmap(x)", "<!DOCTYPE html>\n<html>", True),
        ("none passed, lang shipped", "render_heatmap(x)", '<html lang="ko">', False),
        ("zh-HK in single quotes", "lang='zh-HK'", '<html lang="zh-HK">', True),
        ("wrong lang shipped", 'lang="zh-TW"', '<html lang="ja">', False),
        ("no html tag", 'lang="ja"', "<!DOCTYPE html>", False),
    ]
    ok = 0
    for name, step, head, should_pass in cases:
        passed = verdict(wanted_lang(step), head) is None
        if passed == should_pass:
            ok += 1
        else:
            print(f"  FAILED: {name}")
    try:
        wanted_lang('lang="ja" ... lang="ko"')
        print("  FAILED: two langs not refused")
    except ValueError:
        ok += 1
    total = len(cases) + 1
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    if ap.parse_args().selftest:
        return selftest()
    n, problems = check()
    if problems:
        print(f"PROBLEMS {len(problems)}")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"OK: {n} maps carry the <html lang> their map step passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
