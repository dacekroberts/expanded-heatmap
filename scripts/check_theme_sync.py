"""Verify `.streamlit/config.toml` agrees with `pipeline/theme.py`.

The project's chrome colours live in one Python module, which the map CSS and
the macro-map CSS both build from. Streamlit's page theme cannot: it is read
from TOML, which cannot import. So that file is the one unavoidable duplicate,
and this script is what stops it drifting.

    python scripts/check_theme_sync.py

Exits non-zero and prints every mismatch if they disagree. Read-only.
"""

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.theme import STREAMLIT_DARK, STREAMLIT_LIGHT  # noqa: E402

CONFIG = ROOT / ".streamlit" / "config.toml"

EXPECTED = {"light": STREAMLIT_LIGHT, "dark": STREAMLIT_DARK}


def main():
    if not CONFIG.exists():
        sys.exit(f"No {CONFIG.relative_to(ROOT)}")

    theme = tomllib.loads(CONFIG.read_text(encoding="utf-8")).get("theme", {})
    problems = []

    for variant, expected in EXPECTED.items():
        block = theme.get(variant)
        if block is None:
            problems.append(
                f"[theme.{variant}] is missing. Both variants must be defined: a bare "
                "[theme] block removes Streamlit's own theme chooser from the main "
                "menu (verified 2026-09-21). See docs/theming.md."
            )
            continue
        for key, want in expected.items():
            got = block.get(key)
            if got is None:
                problems.append(f"[theme.{variant}] {key} is missing (expected {want})")
            elif got.lower() != want.lower():
                problems.append(
                    f"[theme.{variant}] {key} = {got} but pipeline/theme.py says {want}"
                )

    extra = [k for k in theme if k not in EXPECTED and k != "base"]
    if extra:
        problems.append(
            f"[theme] has key(s) {extra} outside the light/dark blocks; a colour set "
            "there applies to both variants and is easy to miss."
        )

    if problems:
        print(f"Theme out of sync ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  - {p}")
        print("\nFix whichever is wrong - the palette's home is pipeline/theme.py.")
        sys.exit(1)

    n = sum(len(v) for v in EXPECTED.values())
    print(f"Theme in sync: {n} values match pipeline/theme.py "
          f"across [theme.light] and [theme.dark].")


if __name__ == "__main__":
    main()
