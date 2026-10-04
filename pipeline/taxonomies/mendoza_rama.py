"""Mendoza's activity register, keyed on the RAM level - a local taxonomy, not NAICS.

The owner's calls (2026-10-04, DECISIONS.md, "Mendoza's
taxonomy"): confiterias as Food service, street stands, veterinary clinics,
arcades and institutes out, and every value marked "UNSURE" below at its best
reading, as written. Its column in scripts/category_continuity_table.py is
"mendoza_rama".

Source: the Municipalidad de la Ciudad de Mendoza's "Listado Comercios por
Actividad 2025" (`data/mendoza/raw/comercios_limpio.json`), one row per
activity item, several rows per business (`comercio_id`). `tipo_actividad`
has three levels:

- RAM (rama): the business type. 8,274 rows; 8,158 of 8,309 businesses
  carry one, 8,047 exactly one, 111 two or more. 418 distinct `desc_full`.
- SUB: tax items under the rama (12,311 rows, 531 distinct). Mixed: trade
  sub-types sit beside signage, scales, motors, refuse and sidewalk-table
  fee lines, so SUB is a second opinion, never the key.
- RUB: fee items (20,464 rows, mostly signage and motors). Not a classifier.
- 130 rows have no `tipo_actividad`; none of them is a RAM row.

The JSON names a rama by `desc_full` only, so every key below is a
`desc_full` value. All measured 2026-10-04 on the cached file.

**Why RAM and not SUB** (premises-taxonomy Step 2, taxonomy_catchall's
arithmetic on the cached file, 2026-10-04): at RAM, 528 of 8,274 rows (6.4%)
name no trade (offices, depots, agents, RAMO INDEFINIDO); at business level
673 of 8,309 (8.1%) have no RAM row naming one, 151 of them no RAM row at
all. SUB is not a finer level: 752 businesses have no SUB row, and 1,212 of
8,309 (14.6%) have none naming a trade, because signage, scale and motor fee
lines share the level. The RAM catch-alls are offices by their own SUB
items (ESCRIT.COMERC.Y/O OF.ADMIN.GRAL on 291 of the 522 catch-all-only
businesses); at most about 40 SUB rows among them name a shop trade, so they
are dropped and disclosed rather than dispatched.

**Business rule** (one bucket per business): `classify_business()`; see
BUCKET_PRIORITY.

**No-RAM businesses** (151): no bucket. 134 of them carry no SUB row either,
so their SUB rows cannot rescue them as a group.

**Encoding**: one RAM value stores N-tilde as byte 0xA5 (code page 850's
N-tilde) read as Latin-1, a yen sign: `PA` + chr(0xA5) + `ALERA`. Both that
spelling and the repaired one are keys, so a publisher fix does not unmap
it. Display is step 2's concern.
"""

FIELD_LABEL = "Actividad (rama)"   # proposal; the register's own word, scheme named
VALUE_COLUMN = "desc_full"
TYPE_COLUMN = "tipo_actividad"
RAM_TYPE = "RAM"
BUSINESS_ID_COLUMN = "comercio_id"

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"

# A business with ramas in two buckets takes the first in this order. The
# order is the screen's (brief, "Classification"): Food service first because
# a restaurant's second rama is usually its alcohol or shop line, not a
# second business. 111 businesses carry more than one rama; 7 carry ramas in
# two in-scope buckets, all Food service with Retail (2026-10-04).
# "Any in-scope rama" (this rule): Food service 713, Retail 3,397, Personal
# services 296, out 3,752, no RAM row 151. "First RAM row in file order"
# differs on 6 businesses only, and file order is not a documented primacy,
# so the order-free rule is the draft's choice.
BUCKET_PRIORITY = [FOOD, RETAIL, PERSONAL]


def legend_label(bucket):
    """Taxonomy-module interface: a local taxonomy returns the bucket name."""
    return bucket


# Diaper shop, as stored (0xA5 for N-tilde) and as repaired.
_MANGLED_PANALERA = "PA" + chr(0xA5) + "ALERA"
_REPAIRED_PANALERA = "PA" + chr(0xD1) + "ALERA"


def _norm(value):
    """Stripped and upper-cased; "" for a non-string (pandas' nan is truthy).

    Strips a trailing newline: `PUESTO DE FLORES` is stored with one.
    """
    return value.strip().upper() if isinstance(value, str) else ""


# --- Food service: NAICS 722, consumption on or from the premises ----------
_FOOD = {
    "RESTAURANT",                           # 237
    # Food service, a measured departure from Buenos Aires (owner, 2026-10-04).
    # Buenos Aires files confiterias as Retail because its survey keeps the
    # cafe-tearooms under CAFE, leaving its confiterias as pastry shops (owner
    # 2026-09-28). Here pastry and bread shops are PANADERIA (98% carry a
    # pastry or bread item), while confiterias carry sidewalk-table permits
    # (69%) and alcohol service (45%) as CAFE BAR (77%, 77%) and RESTAURANT
    # (64%, 91%) do, and the City's own fee and alcohol items group them with
    # cafes ("CONFIT.CAFES,LECHE,CHOCOLATERIA" on 128 of 137, "ALCOHOL
    # CONFITERIA, CAFE BAR" on 55). Measured 2026-10-04.
    "CONFITERIA",                           # 137
    "SANDWICHERIA",                         #  88
    "ROTISERIA",                            #  66  hot takeaway meals, as Buenos Aires
    "HELADERIA",                            #  42  ice-cream parlor, 722515
    "COCINERIA",                            #  40  SUB: COCINERIA 29, ROTISERIA 14
    "CAFE BAR",                             #  39
    "PIZZERIA",                             #  29
    "CAFETERIA",                            #  19
    "ALCOHOL RESTAURANT",                   #  12  alcohol licence of a restaurant
    "CERVECERIA",                           #   7  SUB: CERVECERIA ARTESANAL 4, a brewpub
    "LOCAL BAILES",                         #   6  dance club; nightclubs kept (category_rules)
    "ALCOHOL SANWICHERIAS",                 #   5
    "CAFE TE ETC.",                         #   5
    "ALCOHOL CAFE BAR",                     #   3
    "CANTINA",                              #   2  SUB: restaurant, cafe
    # UNSURE, read as below (owner-accepted 2026-10-04). "Bar americano" was the old name for a hostess bar (R3, out);
    # both businesses' SUB items are ordinary: restaurant, cafe, bar,
    # sidewalk tables. Kept on that evidence.
    "BAR AMERIC.",                          #   2
    "SALON DE TE",                          #   1
}

# --- Retail: NAICS 44-45, food shops included --------------------------------
_RETAIL = {
    # Food and drink shops
    "ALMACEN",                              # 236  grocery
    "MINIMARKET",                           # 173
    "QUIOSCO",                              # 105  kiosk shop (SUB: cigarettes, sweets, magazines)
    "PANADERIA",                            #  87
    "VERDULERIA",                           #  43
    "HERBORISTER",                          #  45  herbalist; SUB HERBORISTERIA 43
    "VTA.VINOS",                            #  39
    "MERCADITO",                            #  36
    "FRUTAS VERDU",                         #  29
    "AVES HUEVOS",                          #  27  poultry and egg shop
    "CARNICERIA",                           #  24
    "AUTO SERVICE",                         #  24  SUB AUTOSERVICIO 24: self-service grocery, not a car service
    "ALCOHOL ALMACEN Y/O DESPENSA",         #  15
    "DESPENSA",                             #  13
    "FIAMBRERIA",                           #  13
    "FCA.PASTAS,FIDEOS",                    #  12  fresh-pasta shop; Buenos Aires' FABRICA DE PASTAS is Retail
    "VTA.BEBIDAS",                          #  12  SUB: BOTILLERIA 7, VINOTECA 4
    "SUPER.MERC.",                          #  11
    "PROD.GRANJA",                          #  11  poultry and egg shop
    "P.DIETETICOS",                         #  10
    "ALCOHOL MINIMARKET",                   #   9
    "MINIMERCADO",                          #   8
    "CHOCOLATERIA",                         #   7
    "BOMBONERIA",                           #   6
    "PESCADERIA",                           #   5
    "ALCOHOL KIOSCO",                       #   5
    "ALCOHOL BOTILLERIAS",                  #   5  liquor store
    "ALCOHOL VINERIAS",                     #   4
    "VTA.MIEL",                             #   4
    "GOLOSINAS",                            #   4
    "VTA.PAN",                              #   3
    "ART.PANADER",                          #   3  bakery goods and baking supplies
    "CIGARRERIA",                           #   3
    "ALCOHOL ARTICULOS REGIONALES",         #   2
    "FRUTERIA",                             #   2
    "TOSTADERO",                            #   1  roasted nuts and coffee shop
    "VTA.QUESOS",                           #   1
    "VTA.CARAMELO",                         #   1
    "KIOS.FRU.VER",                         #   1
    "VTA.CAFE",                             #   1
    "VTA.GALLETAS",                         #   1
    "VTA.FIAMBRES",                         #   1
    "CIGARRILLOS",                          #   1
    "VTA.FRUTAS",                           #   1
    "GRANJA AVES",                          #   1
    "PASTAS FRESCAS VTA S/ELABORACION",     #   1
    "FIAM.Y ROTIS",                         #   1  SUB: FIAMBRERIA
    # A market building of fixed shops is kept (category_rules, R1)
    "MERCADO",                              #   1  SUB: AUTOSERVICIO
    # UNSURE, read as below (owner-accepted 2026-10-04). A "feria persa" is a bazaar of small stands under one roof
    # (SUB: FERIA PERSA 5, clothing 2, gifts 2). Kept as a shop; R1 would
    # drop it if each business is one stand rather than the hall.
    "MERCADO PERSA",                        #   9
    # Clothing, shoes, accessories
    "ROPERIA",                              # 650  clothing; SUB ROPAS DE CONFECCION VENTA 591
    "REGALOS",                              #  57
    "ACCESORIOS",                           #  55  SUB: accessories, phones, gifts, auto parts: all goods
    "ZAPATERIA",                            #  50  SUB ZAPATERIA VENTA DE 49; repair is T.ZAPATERIA
    "JOYERIA",                              #  37
    "ART.REGALOS",                          #  25
    "MARROQUINERI",                         #  25
    "RELOJERIA",                            #  24  SUB JOYERIA Y O RELOJERIA 18; repair is T.RELOJERIA
    "LENCERIA",                             #  23
    "CONFECCIONES",                         #  21  SUB ROPAS DE CONFECCION VENTA 16
    "TIENDA",                               #  16  SUB: TIENDA, clothing, perfume, jewelry
    "ZAPATILLERIA",                         #  16
    "BOUTIQUE",                             #  11
    "FANTASIAS",                            #  10  costume jewelry
    "VTA.CALZADOS",                         #   8
    "ART.HOMBRES",                          #   3
    "PELETERIA",                            #   3
    "TALABARTERIA",                         #   3
    "CASA MODAS",                           #   2
    "ART.CALZADOS",                         #   2
    "VTA.MEDIAS",                           #   1
    "VTA.CUEROS",                           #   1
    "MODAS",                                #   1
    # Textiles and haberdashery
    "MERCERIA",                             #  20
    "TEXTILES",                             #  11  SUB TEXTILES,SEDAS,LANAS,ALGODON VT 10
    "ART.TEXTILES",                         #   8
    "VTA.LANAS",                            #   4
    "SEDERIA",                              #   3
    "VTA.CORTINAS",                         #   2
    "BOTONERIA",                            #   1
    "VTA.HILADOS",                          #   1
    "TAPIZADOS",                            #   1  as Buenos Aires; the workshop is T.TAPICERIA
    # Health and beauty goods
    "OPTICA",                               # 103  kept (category_rules: opticians)
    "FARMACIA",                             #  93  kept (category_rules: pharmacies)
    "PERFUMERIA",                           #  43
    "ORTOPEDIA",                            #  25  orthopedic goods, as Buenos Aires
    "ART.MEDICOS",                          #  22  SUB ART.CIRUGIA LABORATORIO Y AFINE 16
    "COSMETICA",                            #  10  SUB: PERFUMERIA 6, cosmetics
    "ART.DENTALES",                         #   3  as Buenos Aires' ARTICULOS ODONTOLOGICOS
    "VTA.COSMETIC",                         #   1
    "ART.PELUQUER",                         #   1  hairdressing supplies, as Buenos Aires
    # Home, hardware, building materials (NAICS 444)
    "FERRETERIA",                           #  72
    "ART.LIMPIEZA",                         #  33
    "ART.ELECTRIC",                         #  30
    "BAZAR",                                #  29
    "ART.HOGAR",                            #  27
    "VTA.MUEBLES",                          #  24
    "MUEBLERIA",                            #  21
    "DECORACIONES",                         #  18  SUB: curtains, home decor (goods, not decorators)
    "ART.PLASTICO",                         #  17
    "MATER.CONST.",                         #  13
    "FLORERIA",                             #  12
    "PINTURERIA",                           #  12
    "ELECTRICIDAD",                         #  10  SUB MATERIALES ELECTRICOS VENTA DE 6
    "SANITARIOS",                           #   9
    "COLCHONERIA",                          #   9
    "CRISTALES",                            #   5  SUB ESPEJOS O VIDRIO VTA 3, as Buenos Aires' VIDRIERIA
    "SEMILLERIA",                           #   4
    "VTA.PUERTAS",                          #   4
    "VTA.ART.PLAS",                         #   4
    "VTA.PLANTAS",                          #   3
    "MATAFUEGOS",                           #   2  as Buenos Aires
    "CERAMICAS",                            #   2
    "VIVERO",                               #   2
    "MBLES.METAL",                          #   2  SUB: furniture sales
    "VTA.ELECTROD",                         #   2
    # UNSURE, read as below (owner-accepted 2026-10-04). Heating; no SUB item names the trade (one SUB is a laundry).
    "CALEFACCION",                          #   2
    "MIMBRERIA",                            #   1
    "VTA.MOSAICO",                          #   1
    "ART.FLORERIA",                         #   1
    "BRONCERIA",                            #   1
    "CORRALON",                             #   1  builders' yard, NAICS 444
    "PROD.QUIMICO",                         #   1  as Buenos Aires' PRODUCTOS QUIMICOS
    "ART. Y/O PROD. P/CULTIVO",             #   1  grow shop, as Buenos Aires
    # Electronics, computing, office machines
    "TELEFONIA CELULAR",                    #  36
    "VTA.TELEFONOS CELULARES Y ACCESORIOS", #  34
    "COMPUTACION",                          #  29  SUB MAQUINAS DE COMPUTACION C/S REP 20
    "ELECTRONICA",                          #  15  SUB: radio, phone and electronics sales
    "IMPLEMENTOS DE COMPUTACION",           #   8
    "MAQUINARIAS",                          #   4  SUB: office machines, plastics; machinery sales
    "MAQ.TEJER",                            #   4  knitting machines, as Buenos Aires' MAQUINAS DE COSER
    "IMPLEMENTOS",                          #   3  SUB: farm implements, pool supplies, butchers' machines
    "MAQ.ESCRIBIR",                         #   3  SUB MAQ.ESCRIB.CALCULAR COMPUT.VTA 3
    "VTA.ARTICULOS INFORMATICA",            #   3
    "ART.COMUNICACIONES",                   #   2
    "TELEVISORES",                          #   1
    "TELEFONIA",                            #   1
    # Books, stationery, leisure, gifts
    "LIBRERIA",                             #  61  SUB LIBRERIA Y ART COLEGIALES 56
    "ART.REGIONAL",                         #  31  regional products
    "ART.Y ALIMENTO P/MASCOTA",             #  26  pet food and supplies
    "JUGUETERIA",                           #  20
    "ART.DEPORTES",                         #  20
    "COTILLON",                             #  16  party goods
    "ART.LIBRERIA",                         #  15
    "VTA.LIBROS",                           #  11
    "ARTESANALES",                          #  10
    "SANTERIA",                             #  12  religious goods
    "ANTIGUEDADES",                         #   9
    "BICICLETERIA",                         #   8
    "ART.CAMPING",                          #   7
    "ARMERIA",                              #   5
    "ART.BEBES",                            #   5
    _MANGLED_PANALERA,                      #   5  diaper shop; see the docstring
    "PAPELERIA",                            #   4
    "ART.FOTOGRAF",                         #   3
    "ART.MUSICA",                           #   3
    "GALERIA ARTE",                         #   3  as Buenos Aires' GALERIA DE ARTE
    "VTA.INSTRUMENTOS MUSICALES",           #   3
    # Framing: Buenos Aires files TALLER DE MARCOS (ENMARCADO DE CUADROS)
    # as Retail. SUB: MARCOS Y CUADROS VTA.
    "T.CUADROS",                            #   5
    "T.MARCOS",                             #   3
    "PIANOS",                               #   1
    "ART.IMPORTAD",                         #   1
    "VTA.REVISTAS",                         #   1
    "ART.DIBUJO",                           #   1
    "VTA.MEDALLAS",                         #   1
    "VTA.DISCOS",                           #   1
    "VTA.IMPLEMENTOS DEPORTIVOS",           #   1
    # Sex shops kept (category_rules, R3). SUB: VENTA ART.USO SEXUAL 2, hardware 1.
    "ART.GRALES",                           #   4
    # UNSURE, read as below (owner-accepted 2026-10-04). Video rental and film distribution (SUB); Buenos Aires keeps
    # VIDEO CLUB as Retail. Two of five are distributors (wholesale).
    "PELICULAS",                            #   5
    # UNSURE, read as below (owner-accepted 2026-10-04). Camera shop or portrait studio: SUB EST.Y/O LAB.FOTOG 7,
    # MATERIAL FOTOGRAFICO VENTA 4. Buenos Aires' CASA DE FOTOGRAFIA and
    # Barcelona's Fotografia (under retail) are kept; ESTUDIO FOTO is the studio.
    "FOTOGRAFIA",                           #   9
    # UNSURE, read as below (owner-accepted 2026-10-04). Second-hand dealers: SUB used furniture 2, used books 2, used
    # tools 1, used clothes 1; but gold buying 2 (Buenos Aires' COMPRA VENTA
    # DE ORO is out, finance) and a property agent 1.
    "COMPRA VENTA",                         #   8
    # Vehicles: dealers, parts, tires, fuel (category_rules, R4)
    "REPUESTOS",                            #  83  SUB REPUESTOS Y ACCESOR.DE AUTOMOT. 58
    "AUTOMOTORES",                          #  25  SUB: car buy-sell 18, dealers 6
    "VTA.REPUESTO",                         #  23
    "EST.SERVICIO",                         #  15  petrol station; SUB carries kiosks and ice sales
    "VTA.MOTOS",                            #   6
    "VTA.NEUMATIC",                         #   5
    "ACUMULADORES",                         #   3  batteries, as Buenos Aires
    "VTA.ACEITES",                          #   3  SUB: lubricants
    "VTA.CUBIERTA",                         #   3  tires
}

# --- Personal services: NAICS 812 --------------------------------------------
_PERSONAL = {
    "PELUQUERIA",                           # 137
    "INST.BELLEZA",                         #  57  beauty institute; SUB includes spa and massage (kept)
    "PELUQ.DAMAS",                          #  44  women's hairdresser
    "S.BELLEZA",                            #  20  beauty salon
    "TATUAJES Y PIERCING",                  #  14  tattoo with its own code is kept (R2)
    "LAVAD.ROPA",                           #  13  laundry; SUB LAVADERO MECANICO DE ROPA 12
    "TINTORERIA",                           #  11  dry cleaner
}

# --- Not a storefront in this project's sense --------------------------------
# Every value enumerated, so an unmapped value means "the register changed",
# never "someone forgot one". Reason classes in the comments.
_NOT_STOREFRONT = {
    # Offices and catch-alls. The brief's catch-alls are offices by their SUB
    # items: ESCRITORIO and ADMINISTRAC carry ESCRIT.COMERC.Y/O OF.ADMIN.GRAL
    # (144 of 192, 117 of 170).
    "ESCRITORIO",                           # 192
    "ADMINISTRAC",                          # 170
    "EMPRESA",                              #  54
    "ACTIVIDAD ADMINISTRATIVA SUPERIOR",    #  39
    "ESTUDIO",                              #  39  SUB ESTUDIO PROFESIONAL 29
    "DEPOSITO",                             #  28  storage depots
    "REPRESENTAC.",                         #  21  agents' offices
    "EMPRESA PROGRAMACION INFORMATICA-SOFTWAR",  # 12
    "EMPRESA DE SERVICIOS",                 #   7
    "AGENCIA",                              #   6
    "COMISIONES",                           #   3  commission agents
    "CONSIGNACION",                         #   2  SUB CONSIG.REPRES.AGENTES Y SUCURSA
    "AG.COMERCIAL",                         #   2
    "INFORMACION",                          #   2
    "ESPECIALES",                           #   2  no SUB rows; names nothing
    "PROMOC.VTAS",                          #   1
    "SUCURSAL",                             #   1  "branch"; its one business sells cars
    "RAMO INDEFINIDO",                      #   1  literally "undefined rama"
    "EXPORTADOR",                           #   1
    "GESTORIA",                             #   4
    "DESP.ADUANA",                          #   4  customs broker
    "ADUANA",                               #   1
    "DIBUJANTE",                            #   1
    "ARQUITECTO",                           #   1
    "CONTADOR",                             #  26
    "ESCRIBANO",                            #  29  notary
    "ABOGADO",                              #  18
    "PUBLICIDAD",                           #  15
    "AG.SEGURIDAD PRIVADA",                 #  49
    # Shopping arcades and malls: the premises row of a building whose shops
    # register on their own (Buenos Aires' MULTICOMERCIAL never reaches its module)
    "GALERIA",                              #  10  8 with no SUB; one SUB MC.LET.GALERIA,PASAJE,MERC.
    "CENTRO COMERCIAL - SHOPPING",          #   2
    # Street stalls and stands on the public way. Owner-accepted 2026-10-04: R1 drops food
    # stalls and stands and category_rules drops kiosk carts; no rule names
    # non-food stalls.
    "ESCAPARATE",                           #  38  SUB ESCAPARATE VTA DIARIOS Y REVIST 34: sidewalk newsstands
    "F.FRANCA",                             #  27  feria franca: SUB OCUPACION VIA PUBLICA F.FRANCA 12, produce 13
    "PUESTO DE FLORES",                     #  16  SUB QUIOSCO VTA. DE FLORES RESTO CIUDAD 14
    "OCUP.VIA PUB",                         #   1  SUB OCUPACION VIA PUBLICA F.FRANCA
    "CARRO PANCHO",                         #   1  hot-dog cart (mobile food, R1)
    # Health care (NAICS 62)
    "CONSULTORIO",                          # 509
    "INSTITUTO",                            # 111  SUB: private teaching 38+, medical 34, rehab 11; beauty 2
    "LABORATORIO",                          #  58  analysis labs
    "CLINICA",                              #  35
    "GERIATRICO",                           #  29
    "MEDICINA PREPAGA",                     #  22
    "MEDICO",                               #  21
    "HOGAR ANCIANOS",                       #  12
    "INYECTABLES",                          #  10  SUB INYECTABLES NEBULIZACIONES: nursing
    "HOSPITAL",                             #   5
    "RAYOS X",                              #   5
    "MECAN.DENTAL",                         #   4  dental technician
    "BIOQUIMICO",                           #   4
    "SANATORIO",                            #   1
    # Veterinary clinics out (category_rules). Owner-accepted 2026-10-04: SUB shows pet
    # food and supplies sales beside the clinic (VETERINARIA 15, PRODUCTOS
    # VETERINARIAS VTA 13, ALIMENTOS BALANCEADOS 10); Barcelona's mixed
    # Veterinaris / Mascotes was kept and disclosed.
    "VETERINARIA",                          #  29
    # Lodging (category_rules; premises-taxonomy Step 5)
    "CASA DPTOS",                           # 279  flats; SUB ALQUILER TEMPORARIO HABITACIONES Y/O DEPARTAMENTOS
    "HOTEL",                                #  89
    "HOSPEDAJE",                            #  37
    "HOSTEL",                               #  29
    "ALOJAMIENTO",                          #  25
    "APART-HOTEL",                          #   6
    "ALCOHOL HOTELERIA",                    #   4  a hotel's alcohol licence
    "RESIDENCIAL",                          #   4  Argentine "residencial" is a guest house; SUB PENSION Y HOSPEDAJE 3
    "PENSION HOSP",                         #   3
    "INQUILINATO",                          #   1  rooming house
    "PENSION",                              #   1
    # Parking (category_rules)
    "ESTACIONAM.",                          # 210
    "COCHERA",                              #  36  SUB AUTOMOVIL-GARAGE 24
    "GARAGE",                               #  17  SUB AUTOMOVIL-GARAGE 14
    # Finance, insurance, property (52, 53)
    "SEGUROS",                              #  61
    "MUTUAL",                               #  53  mutual society offices
    "INMOBILIARIA",                         #  51
    "BANCO",                                #  34
    "RECAUDACION ELECTRONICA",              #  22  bill-payment points, as Buenos Aires' COBRO DE FACTURAS
    "AHORRO PREST",                         #  12
    "FINANCIACION",                         #  10
    "COOPERATIVA",                          #   8
    "CAJEROS AUTOMATICOS",                  #   6
    "CREDITOS",                             #   4
    "ASEGURADORA DE RIESGOS DE TRABAJO",    #   3
    "VTA.PROPIED.",                         #   1
    "CAJA AHORRO",                          #   1
    "REMATES",                              #   1  auctions, as Buenos Aires' SUBASTAS
    # Gambling (R5)
    "AG.QUINIELA",                          #  25
    "AG.LOTERIA",                           #   9
    "VTA.LOTERIA",                          #   4
    "SA.QUINIELA",                          #   3
    "AG.PRODE",                             #   1
    # Travel agencies, as Buenos Aires
    "AG.VIAJES",                            # 134
    "TURISMO",                              #  15
    # Business services: printing, copying, call shops, internet (as Buenos Aires)
    "IMPRENTA",                             #  69
    "FOTO COPIAS",                          #  45
    "COPIAS",                               #   1
    "LITOGRAFIA",                           #   2
    "T.GRAFICOS",                           #   2
    "GRABADOS",                             #   9  SUB GRABADOS SELLOS ETC FCA. 6: engraving and stamp making
    # UNSURE, read as below (owner-accepted 2026-10-04). "Venta de sellos": SUB GRABADOS SELLOS ETC FCA. (stamp maker).
    "VTA.SELLOS",                           #   1
    "T.SELLOS",                             #   1
    "ESTUDIO FOTO",                         #   4  portrait studio, NAICS 541921
    "INTERNET",                             #   5
    "CAB.TELEFO.LOCUT.",                    #   4  call shop, as Buenos Aires' LOCUTORIO
    "COMUNICACIONES",                       #   5
    "EMPRESA VENTA ARTICULOS VIA TELEFONICA",  # 4  nonstore retail (category_rules)
    # Wholesale and distribution (NAICS 42)
    "DROGUERIA",                            #  16  as Buenos Aires
    "DISTRIBUIDOR",                         #  14
    "DIST.PROD.ALIM.",                      #   5
    "ALMACEN MAY.",                         #   1
    "ENVASES",                              #   2  SUB ENVASES DE PAPEL FCA O DEP
    # Education (61) and child care (624410)
    "ACADEMIA",                             #  64
    "GUARDERIA",                            #  28  SUB GUARDERIA INFANTIL 16, JARDIN MATERNAL 8
    "COLEGIO",                              #  18
    "JARD.INFANTE",                         #  11
    "I.EDUCACIONAL",                        #   9
    "UNIVERSIDAD",                          #   8
    "ESC.DANZAS",                           #   2
    "CONSERVATOR.",                         #   1
    "T.ARTES",                              #   5  SUB TALLER ARTISTICO, CENTRO CULTURAL
    # Recreation, culture, events, media (71, 51)
    "GIMNASIO",                             #  74
    "CLUB",                                 #  16  SUB INSTITUCION DEPORTIVA 8
    "JUEGOS MECAN",                         #  13  arcade and play-park machines
    "CINE",                                 #   9
    "TEATRO",                               #   1
    "EXIBICION",                            #   1  read as below (owner-accepted 2026-10-04): SUB ARTESANIA MANUAL 1; an exhibition, read as not a shop
    "BANQUETES",                            #   5  SUB CASA DE BANQUETES,LUNCHS: event halls and caterers (R1)
    "VIANDAS",                              #   1  packed-meal catering (R1)
    "S.SOCIALES",                           #   3  SUB: OBRA SOCIAL, yoga
    "SEDE SOCIAL",                          #  10  association premises
    "RADIO",                                #   9  SUB EMPRESA TRASMISORA DE RADIO 6
    "EMISORA",                              #   1
    "CANAL TV",                             #   2
    "EDITORIAL",                            #   5
    "VIDEO PRODUCCIONES",                   #   1
    # Associations, religion, government (813, 92)
    "SINDICATO",                            #  25
    "FUNDACION",                            #   9
    "SALON RELIGIOSO",                      #   6
    "MISION EVANG",                         #   4
    "GBNO.PCIA.",                           #   3  provincial government
    "I.N.V.",                               #   1  Instituto Nacional de Vitivinicultura
    # Funeral (category_rules)
    "POMPAS FBRES",                         #   4
    "COCHERIA",                             #   2  SUB POMPAS FUNEBRES ESCR.VELATORIO
    "AG.SEPELIOS",                          #   1
    # Transport, post, rental
    "ALQ.AUTOS",                            #  13
    "CORREO PRIV.",                         #   6
    "TRANSPORTE",                           #   3
    "EMP.TRANSP.",                          #   2
    "TROLEBUSES",                           #   1
    "MENSAJERIA",                           #   1
    "TRANSP.CARGA",                         #   1
    # Vehicle repair and services (811; R4 keeps repair out)
    "T.MECANICO",                           #  51
    "T.CHAPISTA",                           #  12
    # UNSURE, read as below (owner-accepted 2026-10-04). SUB: car wash 8, clothes laundry 4. Out as a car wash.
    "LAVADERO",                             #  12
    "LAV.ENGRASE",                          #   7
    "GOMERIA",                              #   6  as Buenos Aires
    "T.RECTIFICAC",                         #   4
    "T.CHAP.PINT.",                         #   4
    "INSTALACION G.N.C.",                   #   3  as Buenos Aires' EQUIPOS GNC
    "T.PINTURAS",                           #   2
    "T.VULCANIZ.",                          #   1
    "T.CUBIERTAS",                          #   1
    "T.BALANCEAD",                          #   1
    "T.INST.AUT.",                          #   1
    "T.MEC.DIESEL",                         #   1
    "T.FRENOS",                             #   1
    "T.RADIADOR",                           #   1
    "T.MOTOS",                              #   1
    # Other repair (811), shoe repair, key cutting and tailoring included
    "CERRAJERIA",                           #  24  SUB CERRAJ.COPIA LLAV. 23
    "T.REPARACION",                         #  20
    "T.ELECTRICID",                         #  18
    "T.ZAPATERIA",                          #  10
    "T.TAPICERIA",                          #   9
    "T.CALZADOS",                           #   8
    "T.RELOJERIA",                          #   8
    "T.COSTURA",                            #   8
    "T.TELEVISION",                         #   7
    # UNSURE, read as below (owner-accepted 2026-10-04). Air conditioning: SUB refrigeration workshop 2, appliance
    # depot 2. Buenos Aires keeps AIRE ACONDICIONADO (a shop) as Retail.
    "AIRE ACONDIC",                         #   6
    "T.JOYERIA",                            #   5
    "T.RADIOS",                             #   5
    "T.SERVICIOS",                          #   4
    "T.BOBINAJES",                          #   3
    "T.REFRIGERAC",                         #   3
    "TALLERES",                             #   3
    "T.TELEFONOS",                          #   3
    "MODISTA",                              #   3  dressmaker: tailoring
    "T.AFILADOS",                           #   2
    "T.MAQUINAS",                           #   2
    "T.COMPOSTURA",                         #   2
    "T.ZURCIDOS",                           #   2
    "T.ART.HOGAR",                          #   2
    "T.BICICLETAS",                         #   4
    "T.OPTICA",                             #   1  SUB TALLER REPARACIONES VARIAS
    "T.CERRAJERIA",                         #   1
    "T.LUSTRADOS",                          #   1
    "T.PLISADOS",                           #   1
    "T.MODAS",                              #   1  SUB TALLER DE MODAS Y PIELES
    # Construction, trades, manufacturing
    "FABRICA",                              #   9
    "T.BORDADO",                            #   5
    "MOLINO",                               #   3
    "CARPINTERIA",                          #   3
    "T.TORNERIA",                           #   3
    "T.METALURG.",                          #   3
    "FCA.MUEBLES",                          #   2
    "T.LETREROS",                           #   2
    "FCA.ROPA",                             #   2
    "CONSTRUCCION",                         #   2
    "T.CONFECCION",                         #   2
    "T.CARPINTER.",                         #   2
    "T.MATRICERIA",                         #   1
    "HERRERIA",                             #   1
    "T.HOJALAT.",                           #   1
    "T.HERRERIA",                           #   1
    "FCA.BALDOZAS",                         #   1
    "FCA.PLASTICO",                         #   1
    "METALURGICA",                          #   1
    "T.TEJIDOS",                            #   1
    "EMPRESA ARMADO EQUIPOS INFORMATICO-HARDW",  # 1
    "CARP.METAL.",                          #   1
    "FCA.SUST.ALIM.",                       #   8  food manufacturing
    # UNSURE, read as below (owner-accepted 2026-10-04). Buenos Aires: TORTAS, MASAS, BOMBONES (ELABORACION) out as
    # manufacturing, FABRICA DE PASTAS kept. Followed here.
    "FCA.MASAS",                            #   3
}

_BUCKET_BY_RAMA = {}
for _value in _RETAIL:
    _BUCKET_BY_RAMA[_value] = RETAIL
for _value in _FOOD:
    _BUCKET_BY_RAMA[_value] = FOOD
for _value in _PERSONAL:
    _BUCKET_BY_RAMA[_value] = PERSONAL
for _value in _NOT_STOREFRONT:
    _BUCKET_BY_RAMA[_value] = None

# The register's mangled spelling and its repair both resolve.
_BUCKET_BY_RAMA[_REPAIRED_PANALERA] = RETAIL

KNOWN_RAMAS = frozenset(_BUCKET_BY_RAMA)


def classify(row):
    """Bucket name for one RAM row, or None for a rama this project does not count.

    RAISES KeyError on a rama not enumerated here: a new value is a change in
    the register to be read, never a silent drop (the project's convention,
    see vancouver.classify).
    """
    value = _norm(row.get(VALUE_COLUMN))
    if not value:
        return None
    if value not in _BUCKET_BY_RAMA:
        raise KeyError(
            f"Mendoza rama {value!r} is not in mendoza_rama's mapping. Give it "
            f"a bucket or an explicit not-a-storefront entry, with a comment "
            f"saying why, before it reaches the map.")
    return _BUCKET_BY_RAMA[value]


def classify_business(ramas):
    """One business's bucket from all of its RAM `desc_full` values.

    Returns (bucket, rama) - the first in-scope bucket in BUCKET_PRIORITY
    order and the rama that earned it, or (None, None). Every rama is
    classified first, so an unknown one raises even beside an in-scope one.
    """
    found = {}
    for rama in ramas:
        bucket = classify({VALUE_COLUMN: rama})
        if bucket is not None and bucket not in found:
            found[bucket] = rama
    for bucket in BUCKET_PRIORITY:
        if bucket in found:
            return bucket, found[bucket]
    return None, None


# --- Import-time proofs ------------------------------------------------------
assert not (_RETAIL & _FOOD) and not (_RETAIL & _PERSONAL) and not (_FOOD & _PERSONAL)
assert not ((_RETAIL | _FOOD | _PERSONAL) & _NOT_STOREFRONT), (
    "a rama cannot be both bucketed and excluded")
assert all(v == v.strip().upper() for v in KNOWN_RAMAS), "keys are normalised"
# Lodging is never a storefront (premises-taxonomy Step 5).
assert all(classify({VALUE_COLUMN: v}) is None
           for v in ("HOTEL", "HOSPEDAJE", "HOSTEL", "ALOJAMIENTO", "CASA DPTOS",
                     "APART-HOTEL", "ALCOHOL HOTELERIA", "RESIDENCIAL"))
# AUTO SERVICE is a self-service grocery (SUB AUTOSERVICIO 24 of 24), not a car service.
assert classify({VALUE_COLUMN: "AUTO SERVICE"}) == RETAIL
assert classify({VALUE_COLUMN: "PUESTO DE FLORES\n"}) is None
assert classify({VALUE_COLUMN: _MANGLED_PANALERA}) == classify({VALUE_COLUMN: _REPAIRED_PANALERA.lower()}) == RETAIL
assert classify({VALUE_COLUMN: float("nan")}) is None and classify({}) is None
assert classify_business(["ALCOHOL RESTAURANT", "ALMACEN"]) == (FOOD, "ALCOHOL RESTAURANT")
assert classify_business(["ESCRITORIO", "CONSULTORIO"]) == (None, None)
