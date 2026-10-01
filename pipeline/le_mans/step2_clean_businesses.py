"""Le Mans step 2: SIRENE -> the storefronts in scope.

    python pipeline/le_mans/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`, as every French city is;
what is Le Mans's own lives in `config.py`. Scaffolded by
scripts/scaffold_france_batch.py.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.countries.france_register import LAST_RUN, build_storefronts
from pipeline.le_mans import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Le Mans", config.LE_MANS_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    div = out["naf_code"].astype(str).str[:2]
    emit("storefronts", len(out))
    emit("retail", int((div == "47").sum()))
    emit("food", int((div == "56").sum()))
    emit("personal", int((div == "96").sum()))
    emit("named", int((~out["name_is_address"]).sum()))
    emit("masked", LAST_RUN["masked"])
    # The funnel and bucket counts the page quotes, as data beside the map.
    facts = dict(LAST_RUN, storefronts=len(out),
                 retail=int((div == "47").sum()), food=int((div == "56").sum()),
                 personal=int((div == "96").sum()),
                 named=int((~out["name_is_address"]).sum()))
    (config.OUTPUTS / "sirene_facts.json").write_text(
        json.dumps(facts, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
