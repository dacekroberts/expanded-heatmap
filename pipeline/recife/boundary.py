"""Recife (Regional)'s scope polygon: the union of config.SCOPE_CODES, by IBGE code."""
from pipeline.countries.brazil_boundary import scope_polygon
from pipeline.recife import config


def city_polygon(verbose=True):
    return scope_polygon(config.OSM_MUNICIPIOS_JSON, config.SCOPE_CODES, config.SCOPE_AREA_KM2,
                         config.CRS_PROJECTED, config.NAME, verbose=verbose)
