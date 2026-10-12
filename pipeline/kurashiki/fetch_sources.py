"""Download everything Kurashiki's pipeline reads, and turn the city's PDF
into the text file step 2 reads. NOT a step: drift_check.py never runs this
file, and every step exits naming it when its cache is missing.

    python pipeline/kurashiki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's year-end list of food-business permits in force,
              令和7年度末 (as of 2026-03-31), one PDF from the city's own
              site (page 1004977, CC BY 4.0), then its text: pdftotext
              -table (xpdf), one record a line, written beside the PDF as
              config.PDF_TEXT. Never a hand-written PDF decoder. The whole
              243-page extraction is a heavy job; run this part through the
              gate:
                python scripts/heavy_job.py run --label "kurashiki pdf"
                    --session <session> --peak-gb 1
                    --estimate "a 243-page text PDF" --
                    python pipeline/kurashiki/fetch_sources.py city
  * isj     - MLIT 位置参照情報 for 33202, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Okayama Prefecture administrative
              areas, into the country's shared cache data/japan/raw/ (N02 PDL
              1.0, N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the PDF was downloaded on 2026-10-08 with the
owner's approval, the ISJ files at Step 0 the same day) and recorded, dated
by its modification time; --force re-downloads, and re-extracts the text. The
text is kept while it is newer than the PDF. Each file is recorded in
outputs/kurashiki/provenance.json (bytes, sha256, when); the text's entry
names the tool and its version, since another pdftotext build may space a
line differently (config.source_rows stops on any line it cannot read). The
text file holds what the PDF holds, the operator column included, so it lives
in data/kurashiki/raw/ (gitignored) and is never committed. The rest of the
work is pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kurashiki import config  # noqa: E402


def extract_text(force):
    """The PDF's text by pdftotext -table, kept while newer than the PDF."""
    pdf, txt = config.source_csv("food"), config.PDF_TEXT
    if txt.exists() and not force and txt.stat().st_mtime >= pdf.stat().st_mtime:
        how = "kept (extracted by an earlier run)"
    else:
        exe = shutil.which("pdftotext")
        if not exe:
            sys.exit("pdftotext (xpdf) is not on PATH; the PDF is read with pdftotext only")
        tmp = txt.with_suffix(".part")
        subprocess.run([exe, *config.PDFTOTEXT_ARGS, str(pdf), str(tmp)], check=True)
        tmp.replace(txt)
        how = "extracted"
    version = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    tool = next((ln.strip() for ln in (version.stderr + version.stdout).splitlines() if "version" in ln), "pdftotext")
    pages = txt.read_text(encoding="utf-8").count("\f")
    print(f"  {txt.name:22s} {txt.stat().st_size:>10,} bytes {pages:>7,} pages ({how}; {tool})")
    japan_fetch.record(config, "city_food_text", file=txt.name, made_from=pdf.name,
                       tool=f"{tool} {' '.join(config.PDFTOTEXT_ARGS)}", pages=pages, bytes=txt.stat().st_size,
                       sha256=japan_fetch.sha256(txt), retrieved=japan_fetch.when(txt), how=how)


def fetch_city(cfg, force):
    """The PDF, then its text, then the shared record of the file with its
    row count and header check (config.file_rows reads the text)."""
    _, url, _ = cfg.SOURCE_FILES["food"]
    how = japan_fetch.get(url, cfg.source_csv("food"), force)
    extract_text(force or how == "downloaded")
    japan_fetch.fetch_city(cfg, False)
    if how == "downloaded":
        import json
        entry = json.loads(cfg.PROVENANCE_JSON.read_text(encoding="utf-8"))["city_food"]
        japan_fetch.record(cfg, "city_food", **{**entry, "how": how})


japan_fetch.PARTS["city"] = fetch_city

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
