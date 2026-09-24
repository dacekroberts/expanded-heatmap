"""Download Brasília's raw inputs - thin over pipeline/countries/brazil_fetch.py.
DELIBERATELY NOT NAMED step*.py, so drift_check.py never runs it.

    python pipeline/brasilia/fetch_sources.py [--force]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_fetch import run  # noqa: E402
from pipeline.brasilia import config  # noqa: E402

EXTRA = [('df_estacoes_metro', 'https://catalogo.ipe.df.gov.br/geoserver/geonode/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=geonode:ESTACOES_METRO', 'df_estacoes_metro.json', '{'), ('df_estacoes_em_construcao', 'https://catalogo.ipe.df.gov.br/geoserver/geonode/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=geonode:ESTACOES_EM_CONSTRUCAO', 'df_estacoes_em_construcao.json', '{')]

if __name__ == "__main__":
    run(config, [(k, url, config.DATA_RAW / name, magic.encode()) for k, url, name, magic in EXTRA])
