"""Buenos Aires' land-use survey subtypes (`TIPO2`) - a local taxonomy, not NAICS.

The Relevamiento Usos del Suelo 2022-2024 records every ground-floor use the
surveyors saw, with a coarse `TIPO1` (RESIDENCIAL, UNICOMERCIAL, OFICINAS,
...) and a free-standing `TIPO2` subtype string. There is no code column that
maps to an international standard, so this module enumerates every `TIPO2`
seen among active storefronts, the way `barcelona_activitat` enumerates
`Nom_Activitat` and `dublin_uses` enumerates Dublin's use segments. The bucket
lines follow those two survey precedents and NAICS where they agree.

**Storefront = `TIPO1 == "UNICOMERCIAL"` and `ESTADO == "ACTIVO"`** (87,028
rows, 385 distinct `TIPO2`, measured 2026-09-28). Step 2 applies both filters;
they are named here because they belong with the taxonomy they qualify.
MULTICOMERCIAL (one row per mall or arcade, shops not itemised) and the
RESIDENCIAL subtype "... CON ACTIVIDAD ECONOMICA" (homes) never reach this
module.

**THE PUBLISHED FILE IS MOJIBAKE FOR ACCENTED VOWELS.** `CAFÉ` is stored as
`CAF├ë`: the publisher decoded UTF-8 bytes as code page 437 and re-encoded the
result as UTF-8. `Ñ` survived (it is one character in both). `repair()` undoes
it, and every key below is the repaired spelling, so `classify()` repairs
before it looks up. Never key on the mangled form: a refresh that fixes the
publisher's encoding would silently unmap every accented subtype.
"""

FIELD_LABEL = "Use"
VALUE_COLUMN = "TIPO2"

TYPE_COLUMN = "TIPO1"
TYPE_VALUE = "UNICOMERCIAL"
ACTIVE_COLUMN = "ESTADO"
ACTIVE_VALUE = "ACTIVO"

_MOJIBAKE_MARK = "├"   # the box-drawing lead byte every repaired value carries


def repair(value):
    """Undo the publisher's cp437 round trip; a clean string passes unchanged."""
    if not isinstance(value, str) or _MOJIBAKE_MARK not in value:
        return value
    try:
        return value.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


def _norm(value):
    """Repaired, stripped, upper-cased; "" for anything that is not a string (nan is truthy)."""
    return repair(value).strip().upper() if isinstance(value, str) else ""


# --- Food service: NAICS 722, consumption on or from the premises ----------
_FOOD = {
    "RESTAURANTE",                                  # 2,666
    "CAFÉ",                                         # 1,715
    "COMIDAS PARA LLEVAR",                          # 1,142  takeaway, 722513
    "PIZZERIA",                                     #   988
    "BAR",                                          #   883
    "HELADERIA",                                    #   779  ice-cream parlour, 722515
    "COMIDA RAPIDA",                                #   462
    "EMPANADAS",                                    #   388  takeaway empanada shops
    "CONFITERIA",                                   #   379  OWNER CALL: café-tearoom here
    "PARRILLA",                                     #   333
    "ROTISERIA",                                    #   304  hot takeaway meals
    "CERVECERIA",                                   #   244  beer bar
    "CAFÉ (VTA AL PASO)",                           #    88  counter coffee
    "SANDWICHERIA",                                 #    88
    "DISCOTECA",                                    #    29  7224, Dublin's night club
    "SUSHI",                                        #    18
}

# --- Retail: NAICS 44/45, food shops included -------------------------------
_RETAIL = {
    # Food and drink shops
    "KIOSCO", "MAXIKIOSCO", "VERDULERIA", "PANADERIA", "MINIMERCADO",
    "SUPERMERCADO", "HIPERMERCADO", "SUPERMERCADO KOSHER", "CARNICERIA",
    "ALMACEN", "FIAMBRERIA Y QUESERIA", "DIETETICA", "GRANJA", "PESCADERIA",
    "VINOS (VENTA)", "BEBIDAS ALCOHOLICAS", "GOLOSINAS", "BOMBONES Y AFINES",
    "FABRICA DE PASTAS",        # fresh-pasta shop, sold over the counter
    "MEDIALUNAS/FACTURAS", "TORTAS", "GALLETITAS", "MIEL", "HERBORISTERIA",
    "VENTA DE CAFÉ (PRODUCTOS)", "PASTILLAS PARA DEPORTES",
    "VENTA POR VENTANA",        # window-counter sales, the kiosk format
    # Clothing, shoes, accessories
    "INDUMENTARIA", "CALZADO", "LENCERIA", "ACCESORIOS DE VESTIR",
    "MARROQUINERIA", "CARTERAS", "BIJOUTERIE", "JOYERIA", "RELOJERIA",
    "ARTICULOS DE CUERO", "TALABARTERIA", "UNIFORMES ESCOLARES",
    "FERIA AMERICANA", "PIELES (VENTA)", "PELUCAS", "PARAGUAS", "PLATERIA",
    "PIEDRAS PRECIOSAS", "ARTICULOS DE DANZA",
    # Textiles and haberdashery
    "TELAS (VENTA)", "BLANCO", "MERCERIA", "LANAS E HILADOS", "SEDERIA",
    "TAPIZADOS", "CORTINAS DE BAÑO", "CORTINAS PARA ENROLLAR", "ALFOMBRAS",
    # Health and beauty goods
    "FARMACIA Y PERFUMERIA", "PERFUMERIA", "COSMETICOS", "OPTICA",
    "ARTICULOS ORTOPEDICOS", "APARATOS AUDITIVOS", "PRODUCTOS MEDICOS",
    "INSTRUMENTAL MEDICO", "ARTICULOS ODONTOLOGICOS",
    "ACCESORIOS DE PELUQUERIA",
    # Home, hardware, building materials (NAICS 444)
    "FERRETERIA", "BAZAR", "ARTICULOS DE LIMPIEZA", "PINTURERIA",
    "SANITARIOS", "VENTA DE ARTICULOS SANITARIOS", "ART. PLOMERIA Y GAS",
    "MATERIALES PARA LA CONSTRUCCION", "MATERIALES ELECTRICOS", "ILUMINACION",
    "MUEBLES (VENTA)", "MUEBLES PARA OFICINA", "COLCHONES",
    "ARTICULOS DE DECORACION", "ARTICULOS PARA EL HOGAR", "ELECTRODOMESTICOS",
    "COCINAS, CALEFONES", "VENTILADORES DE TECHO", "AIRE ACONDICIONADO",
    "VENTA DE AMOBLAMIENTOS DE COCINA", "VIDRIERIA", "VIDRIOS Y ESPEJOS",
    "ABERTURAS", "PUERTAS BLINDADAS", "CERAMICAS", "AZULEJOS", "REVESTIMIENTOS",
    "PISOS DE MADERA", "MADERERA", "HERRAJES", "ESCALERAS",
    "MAQUINAS Y HERRAMIENTAS", "MATAFUEGOS", "VIVERO", "PLANTAS",
    "FLORES Y PLANTAS", "ARTICULOS DE JARDINERIA", "VELAS",
    # Electronics and computing
    "ARTICULOS ELECTRONICOS", "ACCESORIOS PARA CELULARES", "TELEFONIA CELULAR",
    "TELEFONIA", "PC E INSUMOS PC", "INSUMOS PC E INTERNET",
    "EQUIPOS INFORMATICOS Y ELECTRONICOS", "AUDIO Y VIDEO", "VIDEO JUEGOS",
    "RECARGA DE CARTUCHOS", "PILAS, BATERIAS",
    "MAQUINAS Y EQUIPOS PARA OFICINAS", "HELADERAS Y BALANZAS COMERCIALES (VTA)",
    "EQUIP. GASTRONOMICO", "MAQUINAS DE COSER",
    # Books, stationery, leisure, gifts
    "LIBRERÍA", "LIBROS (VENTA)", "PAPELERIA", "VENTA DIARIOS Y REVISTAS",
    "JUGUETERIA", "JUGUETES USADOS", "COTILLON", "REGALOS", "SOUVENIRS",
    "ARTESANIAS", "ARTICULOS REGIONALES", "ANTIGUEDADES", "ARTICULOS USADOS",
    "GALERIA DE ARTE", "OBRAS DE ARTE", "CUADROS (VENTA)",
    "TALLER DE MARCOS (ENMARCADO DE CUADROS)", "INSTRUMENTOS MUSICALES",
    "DISQUERIA", "VIDEO CLUB", "CASA DE FOTOGRAFIA", "ARTICULOS DEPORTIVOS",
    "BICICLETAS", "CAMPING (VENTA DE ARTS.)", "PESCA (VTA DE ARTS.)",
    "GOLF ARTS.", "BUCEO ARTS.", "APARATOS DE GIMNASIA", "ARMERIA",
    "FUEGOS ARTIFICIALES", "TROFEOS, MEDALLAS, COPAS", "BANDERAS",
    "ESTAMPILLAS", "SANTERIA", "SAHUMERIOS", "TABAQUERIA", "HABANOS",
    "GROW SHOP", "SEX SHOP", "ARTICULOS PARA BEBES", "PAÑALERA",
    "ART. PARA FAB. VELAS Y JABONES", "CAJAS DE CARTON", "ACRILICOS",
    "MANIQUIES", "PRODUCTOS QUIMICOS", "CAMAS SOLARES",
    "ART. SEGURIDAD INDUSTRIAL",
    # Pets
    "ALIMENTOS PARA MASCOTAS", "PRODUCTOS VETERINARIOS",
    # Vehicles and parts: dealers and parts are NAICS 441, as in Dublin and
    # Barcelona; the workshops are repair (811), excluded below
    "CONCESIONARIA AUTOMOTORES", "REPUESTOS AUTOMOTOR", "ACCESORIOS AUTOMOTOR",
    "MOTOS, REPUESTOS Y ACCESORIOS", "BATERIAS AUTOMOTORES", "NEUMATICOS",
    "AUTORADIOS",
}

# --- Personal services: NAICS 812, plus Dublin's two departures -------------
# (shoe repair, key cutting and garment alterations are 811 but read as
# personal services on a high street; Dublin includes them, so this does)
_PERSONAL = {
    "PELUQUERIA",                                   # 2,645
    "LAVADERO DE ROPA",                             #   934  laundry
    "CENTRO DE ESTETICA CORPORAL",                  #   670
    "BARBERIA",                                     #   661
    "CERRAJERIA",                                   #   469  key cutting
    "MANICURIA Y PEDICURIA",                        #   359
    "TINTORERIA",                                   #   244  dry cleaner
    "COMPOSTURA DE CALZADO",                        #   226  shoe repair
    "ARREGLO DE ROPA",                              #   214  alterations
    "DEPILACION",                                   #   157
    "TATUAJES",                                     #   111
    "SEPELIOS",                                     #    78  death care, 8122
    "SASTRERIA",                                    #    35
    "SOLARIUM",                                     #    34
    "VELATORIO",                                    #    33
    "FUNERARIA",                                    #    32
    "MASAJES",                                      #    29
    "PELUQUERIA MASCOTAS",                          #    27  pet grooming, 812910
    "INSTITUTO DE BELLEZA",                         #    25
    "TAROT", "ASTROLOGIA",                          #    10  812990
}

# --- Not a storefront in this project's sense -------------------------------
# Enumerated so an unmapped value means "the survey changed", never "someone
# forgot one".
_NOT_STOREFRONT = {
    # Unidentified: the owner's call at the build (drop and disclose, or draw)
    "SIN IDENTIFICAR",
    # Homes filed under UNICOMERCIAL; never pin a home
    "RESIDENCIAL",
    # Vehicle repair and services (811)
    "TALLER MECANICO DE AUTOMOTORES", "CHAPA Y PINTURA AUTOMOTORES",
    "LAVADERO DE AUTOS", "GOMERIA", "LUBRICENTRO",
    "TALLER ELECTRONICA AUTOMOTORES", "ELECTRICIDAD AUTOMOTORES",
    "REPARACION DE MOTOS", "AIRE ACONDICIONADO AUTOMOTOR",
    "ALARMAS AUTOMOTORES", "TAPICERIA PARA AUTOS", "INYECCION ELECTRONICA AUTOMOTOR",
    "COLOCACION CRISTALES AUTOMOTORES", "CAÑOS DE ESCAPE", "EQUIPOS GNC",
    "POLARIZADO DE VIDRIOS", "RELOJES PARA TAXI", "DEPOSITO AUTOMOTORES",
    # Other repair (811)
    "REPARACION DE ELECTRODOMESTICOS", "REPARACION DE ART. ELECTRONICOS",
    "REPARACION CELULARES", "REPARACION PC", "REPARACION AIRE ACONDICIONADO",
    "REPARACION DE AUDIO Y VIDEO", "REPARACION DE HELADERAS",
    "REPARACION DE LAVARROPAS", "REPARACION RADIO, TV",
    "REPARACION CONTROL REMOTO", "REPARACION DE AUDIO", "REPARACION TELEFONOS",
    "REPARACION DE VIDEO", "ARREGLO INSTRUMENTOS MUSICALES", "TAPICERIA",
    "RESTAURACIONES", "SERVICIOS DE COMPUTACION",
    # Finance, insurance, property, gambling (52, 53, 7132)
    "INMOBILIARIA", "BANCO", "LOTERIA", "COBRO DE FACTURAS", "SEGUROS",
    "SEGUROS DE AUTOS", "GIROS DE DINERO", "CASA DE CAMBIO",
    "SERVICIOS FINANCIEROS", "COMPRA VENTA DE ORO", "CAJERO AUTOMATICO",
    "CAJA DE VALORES", "BOLSA DE COMERCIO", "CRIPTOMONEDA",
    "ADMINISTRACION DE CONSORCIOS", "SUBASTAS", "MEDICINA PREPAGA", "OBRA SOCIAL",
    # Professional and business services (54, 56)
    "ESTUDIO JURIDICO", "ESTUDIO CONTABLE", "ESCRIBANIA",
    "ESTUDIO DE ARQUITECTURA", "DECORACION DE INTERIORES", "DISEÑO GRAFICO",
    "DISEÑOS PUBLICITARIOS", "AGENCIA DE PUBLICIDAD", "CONSULTORA",
    "SERVICIOS EMPRESARIALES (OTROS)", "SERVICIOS GENERALES", "SERVICIO (OTROS)",
    "AGENCIA DE EMPLEO", "AVISOS CLASIFICADOS", "SEGURIDAD PRIVADA",
    "SEGURIDAD E HIGIENE", "FUMIGACIONES", "LIMPIEZA DE EDIFICIOS",
    "SERVICIOS HIGIENE - LIMPIEZA", "JARDINERIA", "FOTOCOPIAS, COPIADO, IMPRESIONES",
    "IMPRENTA", "SERVICIOS GRAFICOS", "CARTELES", "ESTAMPADOS", "EDITORIAL",
    "AGENCIA DE VIAJES Y TURISMO", "LOCUTORIO", "INTERNET",
    # Transport, post, logistics, rental
    "LOGISTICA Y DISTRIBUCION", "REMISERIA", "RADIO TAXIS", "CORREO",
    "MENSAJERIA", "FLETES", "TRANSPORTE", "DEPOSITO",
    "CENTRO DE DISTRIBUCION DE PEDIDOS POR APLICACIONES",
    "CENTRO DE DISTRIBUCION Y RETIRO E-COMMERCE", "DISTRIBUCION DIARIOS Y REVISTAS",
    "ALQUILER AUTOS", "ALQUILER DE MAQUINARIA Y EQUIPO", "ALQUILER DE DISFRACES",
    # Wholesale (42), not retail
    "VENTA POR MAYOR DE ALIMENTOS Y BEBIDAS", "COMERCIO POR MAYOR", "DROGUERIA",
    "FRIGORIFICO", "VENTA DE METALES",
    # Health (62), veterinary (541940)
    "ODONTOLOGIA", "CONSULTORIO MEDICO", "CENTRO DE SALUD",
    "LABORATORIO ANALISIS CLINICOS", "KINESIOLOGIA", "PODOLOGIA",
    "CENTRO DE REHABILITACION", "ACUPUNTURA, DIGITOPUNTURA",
    "LABORATORIO DE RECETAS MAGISTRALES", "VETERINARIA (ATENCION)",
    # Education (61)
    "ENSEÑANZA", "ENSEÑANZA DE IDIOMAS", "ENSEÑANZA DE INFORMATICA",
    "ESCUELA DE DANZAS", "ESCUELA DE ARTE", "ESCUELA DE TEATRO",
    "ESCUELA DE MUSICA", "ESCUELA DE MANEJO", "ESCUELA DE ARTES VISUALES",
    "APOYO ESCOLAR", "ACADEMIA PELUQUERIA", "INSTITUTO DE GASTRONOMIA",
    # Recreation, fitness, culture, events (71, 7223)
    "GIMNASIO", "PILATES", "YOGA", "ARTES MARCIALES", "SALON DE EVENTOS",
    "SALON DE FIESTAS", "SALON DE BAILE", "SALON DE JUEGOS RECREATIVOS",
    "CENTRO CULTURAL", "CALESITA", "PELOTERO", "ESTUDIO DE GRABACION",
    "EMISORA RADIO", "SERVICIO DE CATTERING",
    # Religion, politics, associations (813)
    "ACTIVIDADES RELIGIOSAS", "LOCAL PARTIDARIO", "SINDICATO",
    "ASOCIACION CIVIL", "CENTRO DE JUBILADOS", "ASOCIACION DEPORTIVA Y SOCIAL",
    "ASOCIACIONES PROFESIONALES", "ASOCIACION SOCIAL Y CULTURAL",
    "ASOCIACIONES (OTRAS)", "ASOCIACION VECINAL",
    "ASOCIACIONES EMPRESARIALES Y DE EMPLEADORES", "CASA DE PROVINCIA",
    # Construction, trades, manufacturing
    "HERRERIA", "CARPINTERIA", "CERRAMIENTOS", "ZINGUERIA", "PLOMERIA",
    "ELECTROMECANICA", "CONSTRUCTORA", "ASCENSORES", "MARMOLES",
    "PLASTIFICADO DE PISOS", "FABRICACION INDUMENTARIA",
    "FABRICACION ARTICULOS TEXTILES", "FABRICA DE CORTINAS", "FABRICA DE CALZADO",
    "FABRICA ART. DE PLASTICO", "FABRICA DE BOLSAS", "FABRICA DE BOLSOS",
    "FABRICA DE COLCHONES", "FABRICACION DE MAQUINARIA",
    "FABRICACION DE AUTOPARTES", "FABRICACION DE PAPEL Y SUS PROD.",
    "TORTAS, MASAS, BOMBONES (ELABORACION)",
}

_BUCKET_BY_USE = {}
for _value in _RETAIL:
    _BUCKET_BY_USE[_value] = "Retail"
for _value in _FOOD:
    _BUCKET_BY_USE[_value] = "Food service"
for _value in _PERSONAL:
    _BUCKET_BY_USE[_value] = "Personal services"

KNOWN_USES = _BUCKET_BY_USE.keys() | _NOT_STOREFRONT


def classify(row):
    """Bucket name, or None for a use this project does not count."""
    return _BUCKET_BY_USE.get(_norm(row.get(VALUE_COLUMN)))


def legend_label(bucket):
    return bucket


# --- Import-time proofs ------------------------------------------------------
assert repair("CAF├ë") == "CAFÉ"
assert repair("LIBRER├ìA") == "LIBRERÍA"
assert repair("PAÑALERA") == "PAÑALERA"
assert classify({"TIPO2": "CAF├ë"}) == "Food service"
assert classify({"TIPO2": "Librería"}) == "Retail"
assert classify({"TIPO2": "SIN IDENTIFICAR"}) is None
assert classify({"TIPO2": "RESIDENCIAL"}) is None
assert classify({"TIPO2": float("nan")}) is None and classify({}) is None
assert not (_RETAIL & _FOOD) and not (_RETAIL & _PERSONAL) and not (_FOOD & _PERSONAL)
assert not (_BUCKET_BY_USE.keys() & _NOT_STOREFRONT), (
    "a value cannot be both bucketed and excluded")
