"""Watch pipeline/drift_check.py's --render-only pick the right step and refuse
the cities it cannot check.

    python scripts/drift_check_selftest.py

WHY. Render-only is only safe while it runs the MAP step and nothing else:
seven cities have a step 3 that geocodes or address-joins
(step3_geocode.py, step3_place.py) before a step4_map.py, and a mode that ran
"step 3" by number would geocode in a render check, or skip those cities' maps.
It must also refuse, not pass, a city whose processed inputs are missing. So
each case is a small fake city in a temporary tree, run through the real
functions with the module's ROOT pointed at it; the positive control is the
live tree, where every city must have exactly one map step.

NOTHING IN THE REPOSITORY IS MODIFIED: every fake city lives in a temp folder,
and the one subprocess call against the live script uses --list, which runs no
step.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import drift_check  # noqa: E402

# A fake step records that it ran, and whether the offline guard was set.
STEP = (
    "import os, pathlib\n"
    "log = pathlib.Path(__file__).resolve().parents[2] / 'ran.txt'\n"
    "with open(log, 'a', encoding='utf-8') as f:\n"
    "    f.write(pathlib.Path(__file__).name + ' ' + os.environ.get('HEATMAP_NO_NETWORK', '-') + chr(10))\n"
)

failures = []


def expect(label, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + label + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def fake_city(root: Path, name: str, steps, processed: bool | None):
    d = root / "pipeline" / name
    d.mkdir(parents=True)
    for s in steps:
        (d / s).write_text(STEP, encoding="utf-8")
    if processed is not None:
        p = root / "data" / name / "processed"
        p.mkdir(parents=True)
        if processed:
            (p / "stations.csv").write_text("a\n1\n", encoding="utf-8")


def main():
    real_root = drift_check.ROOT
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        drift_check.ROOT = tmp
        try:
            fake_city(tmp, "plain", ["step1_stations.py", "step2_clean_businesses.py", "step3_map.py"], True)
            fake_city(tmp, "geocoded", ["step1_stations.py", "step2_clean_businesses.py",
                                        "step3_geocode.py", "step4_map.py"], True)
            fake_city(tmp, "placed", ["step1_stations.py", "step2_clean_businesses.py",
                                      "step3_place.py", "step4_map.py"], True)
            fake_city(tmp, "no_processed", ["step1_stations.py", "step3_map.py"], None)
            fake_city(tmp, "empty_processed", ["step1_stations.py", "step3_map.py"], False)
            fake_city(tmp, "two_maps", ["step3_map.py", "step4_map.py"], True)
            fake_city(tmp, "no_map", ["step1_stations.py", "step2_clean_businesses.py"], True)

            for city, want in (("plain", "step3_map.py"), ("geocoded", "step4_map.py"),
                               ("placed", "step4_map.py")):
                got = [p.name for p in drift_check.map_steps(city)]
                expect(f"{city}: the map step is {want} alone", got == [want], got)
                expect(f"{city}: not refused", drift_check.render_only_refusal(city) is None)

            for city, needle in (("no_processed", "missing or empty"),
                                 ("empty_processed", "missing or empty"),
                                 ("two_maps", "has 2 step*_map.py"),
                                 ("no_map", "has 0 step*_map.py")):
                why = drift_check.render_only_refusal(city) or ""
                expect(f"{city}: refused, saying '{needle}'", needle in why, why)

            # Run render-only's step list for real: only the map step runs, under
            # the offline guard; the geocode/place step never does.
            for city in ("geocoded", "placed"):
                log = tmp / "ran.txt"
                log.unlink(missing_ok=True)
                ran, _ = drift_check.run_steps(city, only=drift_check.map_steps(city))
                lines = log.read_text(encoding="utf-8").split() if log.exists() else []
                expect(f"{city}: render-only ran step4_map.py and nothing else, offline",
                       ran and lines == ["step4_map.py", "1"], lines)

            # The full path still runs every step, in order.
            log = tmp / "ran.txt"
            log.unlink(missing_ok=True)
            drift_check.run_steps("geocoded")
            names = log.read_text(encoding="utf-8").split()[0::2]
            expect("geocoded: the full check still runs all four steps in order",
                   names == ["step1_stations.py", "step2_clean_businesses.py",
                             "step3_geocode.py", "step4_map.py"], names)
        finally:
            drift_check.ROOT = real_root

    # --changed reaches a city through imports and through an imported
    # TAXONOMY_SYSTEM (audit of 2026-11-03, findings 1 and 9).
    all_cities = drift_check.cities_with_pipelines()
    for path, want in (
            ("pipeline/taxonomies/scian.py", {"mexico_city", "guadalajara", "monterrey"}),
            ("pipeline/taxonomies/naics.py", {"seattle", "vancouver", "los_angeles", "tacoma"}),
            ("pipeline/new_york/step2_clean_businesses.py", {"new_york", "seattle", "buffalo"}),
            ("pipeline/bucharest/step2_clean_businesses.py", {"bucharest", "cluj_napoca"}),
            ("pipeline/kansas_city/step2_clean_businesses.py", {"kansas_city", "tacoma"}),
            ("pipeline/riga/config.py", {"riga", "daugavpils"})):
        got, _ = drift_check.cities_affected([path], all_cities)
        expect(f"--changed: {path} reaches {sorted(want)}", want <= got, sorted(got))
    got, _ = drift_check.cities_affected(["pipeline/guadalajara/step1_stations.py"], all_cities)
    expect("--changed: a city's own step stays that city alone", got == {"guadalajara"}, sorted(got))
    got, why = drift_check.cities_affected(["pipeline/taxonomies/no_such_module.py"], all_cities)
    expect("--changed: a taxonomy no city reaches says so",
           not got and why[0].endswith(drift_check.NO_CITY), why)
    expect("--changed: Mexico's imported TAXONOMY_SYSTEM resolves",
           drift_check.taxonomies_of("guadalajara") == {"scian"}, drift_check.taxonomies_of("guadalajara"))
    expect("--changed: both arms of a conditional TAXONOMY_SYSTEM count",
           drift_check.taxonomies_of("los_angeles") == {"los_angeles", "naics"},
           drift_check.taxonomies_of("los_angeles"))
    blind = [c for c in all_cities if not drift_check.taxonomies_of(c)]
    expect("live tree: every city's TAXONOMY_SYSTEM resolves from source", not blind, blind)

    # A baseline's every figure going silent fails (finding 28).
    real_load = drift_check.baseline.load
    drift_check.baseline.load = lambda city: {"stations": 3}
    try:
        ok, lines = drift_check.baseline.compare("anywhere", {})
        expect("baseline: a stored baseline with nothing emitted fails", not ok, lines)
        drift_check.baseline.load = lambda city: None
        ok, lines = drift_check.baseline.compare("anywhere", {})
        expect("baseline: no baseline and nothing emitted stays a reported gap", ok, lines)
    finally:
        drift_check.baseline.load = real_load

    # Positive control: the live tree. Every city has exactly one map step.
    bad = [c for c in drift_check.cities_with_pipelines() if len(drift_check.map_steps(c)) != 1]
    expect("live tree: every city has exactly one step*_map.py", not bad, ", ".join(bad))

    script = str(ROOT / "pipeline" / "drift_check.py")
    proc = subprocess.run([sys.executable, script, "--render-only", "--update-baseline", "--list"],
                          cwd=ROOT, capture_output=True, text=True)
    # Accepted since 2026-10-12: it merges the map step's figures only.
    expect("--render-only with --update-baseline is accepted",
           proc.returncode == 0 and len(proc.stdout.split()) > 100, proc.stderr)
    proc = subprocess.run([sys.executable, script, "--render-only", "--list"],
                          cwd=ROOT, capture_output=True, text=True)
    listed = proc.stdout.split()
    expect("--render-only --list lists every city and runs nothing",
           proc.returncode == 0 and listed == drift_check.cities_with_pipelines(),
           f"exit {proc.returncode}, {len(listed)} listed")

    if failures:
        sys.exit(f"\n{len(failures)} case(s) failed")
    print("\nOK - render-only selects the map step and refuses what it cannot check")


if __name__ == "__main__":
    main()
