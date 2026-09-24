"""Download Rio de Janeiro's raw inputs - thin over pipeline/countries/brazil_fetch.py.
DELIBERATELY NOT NAMED step*.py, so drift_check.py never runs it.

    python pipeline/rio_de_janeiro/fetch_sources.py [--force]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_fetch import run  # noqa: E402
from pipeline.rio_de_janeiro import config  # noqa: E402

EXTRA = [('rio_metro_estacoes_19', 'https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/19/query?where=1%3D1&outFields=*&outSR=4326&f=geojson', 'rio_metro_estacoes_19.geojson', '{'), ('rio_metro_linhas_18', 'https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/18/query?where=1%3D1&outFields=*&outSR=4326&f=geojson', 'rio_metro_linhas_18.geojson', '{')]

if __name__ == "__main__":
    run(config, [(k, url, config.DATA_RAW / name, magic.encode()) for k, url, name, magic in EXTRA])
