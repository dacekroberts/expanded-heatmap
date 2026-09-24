"""Screen a Brazilian city from IBGE's CNEFE 2022 - the census address file,
which turns out to be a FIELD SURVEY of every non-residential address.

WHY THIS EXISTS
---------------
Brazil was carried as "CNPJ plus geocoding at national scale". On 2026-09-23
two things changed that: Receita now serves CNPJ only to Brazilian networks
(15 of 16 check nodes reset, the Brazilian one answered 200), and CNEFE 2022
turned out to carry `DSC_ESTABELECIMENTO` - the enumerator's identification of
every establishment - with a field-collected coordinate. No register, no
geocoder: the census walked every block face.

It is national, one schema, so this one script screens every Brazilian city.

WHAT A ROW IS - READ BEFORE COUNTING
------------------------------------
IBGE's dictionary: "Cada registro representa uma especie existente no
endereco" - ONE ROW PER USE-TYPE AT AN ADDRESS, not one per business.
`COD_INDICADOR_ESTAB_ENDERECO` says whether a row stands for 1, 2-10, >10 or
an unknown number of establishments. Section 5 below measures how much that
collapses.

THE TAXONOMY IS FREE TEXT, WHICH IS NEW HERE
--------------------------------------------
Every earlier taxonomy was a code list, where `premises-taxonomy` requires an
explicit home for every value. Rio alone has 118,684 distinct descriptions,
so that rule cannot apply as written. The adaptation:

  * ORDERED keyword rules - exclusions first, so "SALAO DE FESTAS" (an events
    hall) is removed before "SALAO" (a hair salon) can claim it, and
    "DEPOSITO DE BEBIDAS" (a drinks shop) before "DEPOSITO" (a warehouse).
  * The UNMATCHED share is the catch-all, measured like any other catch-all,
    and a fixed random sample of it is printed to be READ - the skill's
    "what does the catch-all actually mean" step, which is the only way to
    know whether storefronts are hiding in it.
  * Buckets follow the NAICS boundaries every built city uses: Retail = 44-45
    minus non-store, Food service = 722 (NOT accommodation), Personal services
    = 812 minus parking. So car washes, auto repair, gyms, shoe and phone
    repair are OUT, however much they read like services. A bakery is RETAIL,
    on the Dublin / Vancouver / Milan precedent (a shop sells goods, a cafe
    sells a sitting).

Usage:
    python scripts/screen_cnefe.py data/rio_de_janeiro/raw/3304557_RIO_DE_JANEIRO.zip
    python scripts/screen_cnefe.py <zip> --sample 120
"""
import argparse
import collections
import csv
import io
import random
import re
import sys
import unicodedata
import zipfile

# --- normalisation ---------------------------------------------------------

# Enumerator spellings measured in Rio and Sao Paulo, fixed before matching.
SPELLING = [
    (r"\bCABELEREIR", "CABELEIREIR"), (r"\bCABELERE", "CABELEIRE"),
    (r"\bESTABELICIMENTO", "ESTABELECIMENTO"), (r"\bMECANICO\b", "MECANICA"),
    (r"\bLANCHONET\b", "LANCHONETE"), (r"\bBORRACHEIRO\b", "BORRACHARIA"),
    (r"\bACOGUE\b", "ACOUGUE"), (r"\bSALAO BELEZA\b", "SALAO DE BELEZA"),
    (r"\bCABELELEIR", "CABELEIREIR"), (r"\bTATOO\b", "TATTOO"),
    (r"\bBARRACHARIA\b", "BORRACHARIA"), (r"\bHORTIFRITE\b", "HORTIFRUTI"),
    (r"\bTRAILLER\b", "TRAILER"), (r"\bBUTECO\b", "BOTECO"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    for pat, rep in SPELLING:
        s = re.sub(pat, rep, s)
    return s


def rx(*words):
    return re.compile(r"\b(" + "|".join(words) + r")")


# --- ordered rules: first match wins ---------------------------------------
# (label, bucket-or-None, compiled pattern). bucket None = excluded, with the
# label as the reason. ORDER IS THE DESIGN - see the module docstring.
RULES = [
    ("vacant", None, rx("VAGO", "VAGA", "VAZIO", "VAZIA", "FECHADO", "FECHADA",
                        "DESOCUPAD", "DESATIVAD", "ABANDONAD", "ALUGA",
                        "SEM USO", "EM OBRA", "EM REFORMA", "INATIV",
                        "TERRENO", "FECHAR", "A VENDA")),
    ("no description", None, re.compile(
        r"^(SEM NOME|NAO TEM|NAO INFORMAD\w*|SEM IDENTIFICACAO|NT|NI|S N|SN|"
        r"SEM|NAO SABE|NAO IDENTIFICAD\w*|X+|0+|SEM DENOMINACAO|INDETERMINADO|"
        r"ESTABELECIMENTO SEM NOME|SEM DESCRICAO|NAO POSSUI|DESCONHECIDO|"
        r"SEM NONE|NAO TEM NOME|SEM PLACA|SEM INDENTIFICACAO|SEM DEFINICAO.*)$")),
    ("not premises", None, re.compile(
        r"^(SITIO|CHACARA|FAZENDA|HORTO|CAMPO DE FUTEBOL|QUADRA|PRACA|PARQUE|"
        r"ESTACAO DE TRATAMENTO|RESERVATORIO|CEMITERIO|CANTEIRO|GRANJA|CANIL|"
        r"GALINHEIRO|CRIADOURO)\b|"
        # EXACT only: "CASA DO NORTE" and "CASA DE CARNES" are shops
        r"^(CASA|TERRACO|PORAO|RESIDENCIA)$|"
        r"\b(CEDAE|COMLURB|SABESP|LIGHT|ENEL|COMGAS|ESTOQUE)\b")),
    ("accommodation", None, rx("HOTEL", "POUSADA", "MOTEL", "PENSAO", "HOSTEL",
                               "ALBERGUE", "FLAT", "APART HOTEL", "HOSPEDAGEM",
                               "REPUBLICA")),
    ("religious", None, rx("IGREJA", "TEMPLO", "CENTRO ESPIRITA", "TERREIRO",
                           "ASSEMBLEIA DE DEUS", "CONGREGACAO", "PAROQUIA",
                           "CAPELA", "MINISTERIO", "BATISTA", "EVANGELIC",
                           "UMBANDA", "CANDOMBLE", "SALAO DO REINO",
                           "TABERNACULO", "MESQUITA", "SINAGOGA")),
    ("events venue", None, rx("SALAO DE FESTA", "SALAO DE EVENTO",
                              "CASA DE FESTA", "CASA DE EVENTO", "ESPACO DE FESTA",
                              "ESPACO DE EVENTO", "BUFFET", "EVENTOS")),
    ("parking / storage", None, rx("GARAGE", "ESTACIONAMENTO", "GALPAO",
                                   "DEPOSITO(?! DE BEBIDA)", "ALMOXARIFADO",
                                   "ARMAZENAGEM", "GUARDA MOVEIS")),
    ("auto / repair", None, rx("OFICINA", "MECANICA", "BORRACHARIA", "FUNILARIA",
                               "LANTERNAGEM", "AUTO ELETRICA", "AUTOELETRICA",
                               "LAVA JATO", "LAVAJATO", "LAVA RAPIDO",
                               "LAVAGEM DE (CARRO|AUTO|VEICULO)", "CONSERTO",
                               "ASSISTENCIA TECNICA", "SAPATEIRO", "CHAVEIRO",
                               "REFRIGERACAO", "RETIFICA", "CAPOTARIA",
                               "ESTOFAD", "COSTUREIRA", "COSTURA", "AJUSTE",
                               "AUTO ELETRICO", "CENTRO AUTOMOTIVO",
                               "AUTO CENTER", "TAPECARIA", "ATELIE")),
    ("industry / trades", None, rx("SERRALHERIA", "MARCENARIA", "METALURGIC",
                                   "CARPINTARIA", "GRAFICA", "CONFECCAO",
                                   "FABRICA", "INDUSTRIA", "SERRARIA",
                                   "TORNEARIA", "VIDRACARIA", "FERRO VELHO",
                                   "RECICLA", "SUCATA", "TECELAGEM",
                                   "CALDEIRARIA", "USINAGEM", "GESSO",
                                   "MARMORARIA", "TRANSPORTADORA",
                                   "ESTAMPARIA", "FERRAMENTARIA", "CONSTRUTORA",
                                   "COMUNICACAO VISUAL", "SERRALHEIRO",
                                   "MARCENEIRO",
                                   # bottled-gas dealers: NAICS non-store fuel
                                   # dealers, excluded with 454 everywhere
                                   r"GAS\b", "SUPERGASBRAS", "ULTRAGAZ",
                                   "LIQUIGAS", "NACIONAL GAS", "ENERGAS",
                                   "DISTRIBUIDORA(?! DE BEBIDA)")),
    ("office / professional", None, rx("ESCRITORIO", "EMPRESA", "CONSULTORIO",
                                       "CLINICA", "DENTISTA", "ODONTO",
                                       "LABORATORIO", "ADVOCACIA", "ADVOGAD",
                                       "CONTABIL", "IMOBILIARIA", "SEGURADORA",
                                       "BANCO", "AGENCIA", "LOTERICA",
                                       "CORRETORA", "ARQUITETURA", "ENGENHARIA",
                                       "COWORKING", "SALAS COMERCIAIS",
                                       "SALA COMERCIAL", "PREDIO COMERCIAL",
                                       "EDIFICIO COMERCIAL", "CENTRO COMERCIAL",
                                       "CONDOMINIO", "PORTARIA", "ADMINISTRACAO",
                                       "VETERINARI", "FISIOTERAPIA",
                                       "PSICOLOG", "LAN HOUSE", "CYBER",
                                       "COPIADORA", "XEROX", "DESPACHANTE",
                                       "FIRMA", "HOSPITAL", "PSIQUIATR",
                                       "TERAPEUT", "EMPRESTIMO", "FINANCEIRA",
                                       "LOCADORA", "ALUGUEL DE", "LOTERIA",
                                       "JOGO DO BICHO", "CAIXA ECONOMICA",
                                       "PODOLOG", "PROTETICO", "ED COMERCIAL")),
    ("public / civic / education", None, rx("ESCOLA", "CRECHE", "CURSO",
                                            "COLEGIO", "FACULDADE",
                                            "AUTO ESCOLA", "AUTOESCOLA",
                                            "PREFEITURA", "INSS", "DELEGACIA",
                                            "CORREIOS", "POSTO DE SAUDE",
                                            "ASSOCIACAO", "SINDICATO", "CLUBE",
                                            "ONG", "INSTITUTO", "FUNDACAO",
                                            "SECRETARIA", "BATALHAO", "QUARTEL",
                                            "BIBLIOTECA", "MUSEU", "TEATRO",
                                            "EXPLICADORA", "REFORCO ESCOLAR",
                                            "PILATES", "DETRAN", "MACUMBA",
                                            "CINEMA", "ACADEMIA", "ESTUDIO",
                                            "STUDIO(?! DE (TATUAGEM|BELEZA))",
                                            "BOATE", "CASA DE SHOW",
                                            "SUBESTACAO", "TORRE", "ANTENA",
                                            "CAIXA ELETRONICO")),
    # --- the three buckets ---
    ("food service", "Food service", rx(
        r"BAR\b", "BARES", "BARZINHO", "BIROSCA", "BOTEQUIM", "BOTECO",
        "QUIOSQUE DE (PRAIA|COCO|LANCHE)", "LANCHONETE", "LANCHES",
        "LANCHE", "RESTAURANTE", "PIZZARIA", r"CAFE\b", "CAFETERIA",
        "SORVETERIA", "SORVETE", "CHURRASCARIA", "CHURRASQUINHO", "PASTELARIA",
        "PASTEL", "FRANGO ASSADO", "ROTISSERIE", "MARMITARIA",
        "HAMBURGUER", "HAMBURGUERIA", "SUSHI", "TEMAKERIA", "ACAI", "ESFIHA",
        "ESFIHARIA", "SALGADO", "QUENTINHA", "MARMITA", "CERVEJARIA",
        "CHOPERIA", "CHOPP", "BISTRO", "CANTINA", "CREPERIA", "TAPIOCA",
        "CALDO DE CANA", r"PUB\b", "TABERNA", "COMIDA", "CULINARIA",
        "GASTRONOMIA", "SELF SERVICE", "PETISCARIA", "SUCOS", "SUCO",
        "TRAILER", "FOOD", "MC ?DONALD", "BURGER KING",
        "BOBS", "SUBWAY", "HABIBS", "SPOLETO", "GIRAFFAS", "STARBUCKS",
        "CHINA IN BOX", "OUTBACK", "KFC", "POPEYES")),
    ("personal services", "Personal services", rx(
        "SALAO", "BARBEARIA", "BARBER", "BARBEIRO", "CABELEIREIR", "CABELO",
        "COIFFEUR", "ESMALTERIA", "NAIL", "MANICURE",
        "PEDICURE", "ESTETICA", "DEPILACAO", "UNHA", "SOBRANCELHA", "BELEZA",
        "LAVANDERIA", "TINTURARIA", "TATUAGEM", "TATTOO", "PIERCING",
        "BANHO E TOSA", "PET SPA", "FUNERARIA", "MASSAGEM", r"SPA\b",
        "MAQUIAGEM", "CILIOS", "BRONZEAMENTO")),
    ("retail", "Retail", rx(
        "LOJA .", "LOJAS", "LOJINHA", "VENDINHA", "TENDINHA", "MERCADO",
        "MERCEARIA", "SUPERMERCADO", "AVIARIO", "SAPATARIA", "BISCOITO",
        "COLCHO", "MADEIREIRA", "PNEUS", "CONCESSIONARIA", "COMERCIO DE ",
        "AVICOLA", "BICICLETARIA", "PRODUTOS? DE LIMPEZA",
        "MATERIA(L|IS) DE LIMPEZA", "FARMA", "BOLOS",
        "CASA E VIDEO", "POSTO (SHELL|IPIRANGA|BR|ALE|PETROBRAS)",
        "MINIMERCADO", "MERCADINHO", "HIPERMERCADO", "ATACAD", "FARMACIA",
        "DROGARIA", "DROGA", "ACOUGUE", "CASA DE CARNE", "HORTIFRUTI",
        "HORTI FRUTI", "SACOLAO", "FRUTARIA", "VERDURAO", "PAPELARIA",
        "BAZAR", "ARMARINHO", "MATERIA(L|IS) DE CONSTRUCAO", "MATERIAIS",
        "OTICA", "PET SHOP", "PETSHOP", "AGROPECUARIA", "RACAO", "RACOES",
        "FLORICULTURA", "FLORES", "LIVRARIA", "BOUTIQUE", "CALCADO",
        "ROUPA", "VESTUARIO", "MODA", "MOVEIS", "ELETRO", "PEIXARIA",
        "DEPOSITO DE BEBIDA", "DISTRIBUIDORA DE BEBIDA", "ADEGA", "BEBIDAS",
        "PERFUMARIA", "COSMETICO", "BIJUTERIA", "BIJU", "CELULAR",
        "BRECHO", "TABACARIA", "BANCA DE JORNA", "JORNALEIRO", "REVISTARIA",
        "AUTO ?PECAS", "MOTO ?PECAS", "MAGAZINE", "UTILIDADES", "EMPORIO",
        "QUITANDA", "PADARIA", "PANIFICADORA", "CONFEITARIA", "DOCERIA",
        "DOCES", r"DOCE\b", "BOMBONIERE", "JOALHERIA", "RELOJOARIA", "INFORMATICA",
        "ARTIGOS", "VARIEDADES", "TECIDOS", "POSTO DE (GASOLINA|COMBUSTIVE)",
        "CONVENIENCIA", "SHOPPING", "GALERIA", "BRINQUEDO", "PRESENTES",
        "ARMAZEM", "FERRAGENS", "FERRAGISTA", "TINTAS", "ELETRICA",
        "HIDRAULICA", "VIDEO ?LOCADORA", "SEX SHOP", "ANTIQUARIO",
        "CASAS BAHIA", "AMERICANAS", "RIACHUELO", "RENNER", "PERNAMBUCANAS",
        "CARREFOUR", "PAO DE ACUCAR", "ASSAI", "OXXO", "RAIA", "DROGASIL",
        "PACHECO", "PAGUE MENOS", "BOTICARIO", "NATURA", "CACAU SHOW",
        "KOPENHAGEN", "MARISA", r"C A\b", "HERING", "CENTAURO",
        # "Casa do Norte" in Sao Paulo is a shop of north-eastern produce
        # (carne de sol, farinha) - it sells goods, so RETAIL on the bakery
        # precedent, not food service.
        "CASA DO NORTE")),
    # --- a generic word that cannot be bucketed ---
    ("catch-all", None, re.compile(
        r"^(COMERCIO|COMERCIAL|LOJA|LOJAS|ESTABELECIMENTO|ESTABELECIMENTO "
        r"COMERCIAL|PONTO COMERCIAL|SALA|SERVICO|SERVICOS|BARRACA|BARRACAO|"
        r"QUIOSQUE|BANCA|BOX|BOXE|CONTAINER|NEGOCIO|COM|BARRAQUINHA|PRESTACAO DE "
        r"SERVICO|PRESTADOR DE SERVICO|ATIVIDADE COMERCIAL|COMERCIO VAREJISTA|"
        r"VENDA|VENDAS|FEIRA|CAMELO|AMBULANTE)$")),
]
BUCKETS = ("Retail", "Food service", "Personal services")


# --- enumerator misspellings, caught by EDIT DISTANCE rather than by listing -
# The unmatched remainder was full of one-letter slips of words the rules
# already know - RESTAUTANTE, CABELEIRO, MADEREIRA, GARRAGEM, HORTIFRUTE,
# METALUGICA. Listing them one at a time is the SPELLING table's job and
# never finishes; this corrects any token within 1 edit (2 for long words) of
# a vocabulary word, applied ONLY to rows that would otherwise be unmatched,
# and cached per distinct token so it stays cheap.
VOCAB = sorted(set("""
RESTAURANTE LANCHONETE PIZZARIA SORVETERIA CHURRASCARIA PASTELARIA CAFETERIA
HAMBURGUERIA BOTEQUIM CERVEJARIA CHOPERIA PETISCARIA TEMAKERIA ESFIHARIA
SORVETES SALGADOS QUENTINHA MARMITARIA CONFEITARIA DOCERIA PADARIA
PANIFICADORA BOMBONIERE MERCEARIA MERCADINHO SUPERMERCADO MINIMERCADO
HORTIFRUTI SACOLAO FRUTARIA VERDURAO ACOUGUE PEIXARIA AVICOLA FARMACIA
DROGARIA PAPELARIA ARMARINHO BIJUTERIA PERFUMARIA COSMETICOS TABACARIA
FLORICULTURA LIVRARIA BOUTIQUE CALCADOS SAPATARIA VESTUARIO MADEIREIRA
FERRAGENS UTILIDADES VARIEDADES MAGAZINE CONVENIENCIA BICICLETARIA
AGROPECUARIA MATERIAIS CONSTRUCAO BARBEARIA CABELEIREIRO CABELEIREIRA
MANICURE PEDICURE ESTETICA DEPILACAO ESMALTERIA LAVANDERIA TINTURARIA
TATUAGEM MAQUIAGEM SOBRANCELHA FUNERARIA GARAGEM ESTACIONAMENTO DEPOSITO
GALPAO OFICINA MECANICA BORRACHARIA FUNILARIA LANTERNAGEM SERRALHERIA
SERRALHEIRO MARCENARIA MARCENEIRO METALURGICA CARPINTARIA VIDRACARIA
TAPECARIA ESTAMPARIA FERRAMENTARIA CONSTRUTORA ESCRITORIO CONSULTORIO
CLINICA LABORATORIO IMOBILIARIA CONTABILIDADE ADVOCACIA IGREJA ASSEMBLEIA
ESCOLA CRECHE ACADEMIA ASSOCIACAO CONDOMINIO RESIDENCIA
""".split()))


def _within(a, b, k):
    """True when Levenshtein(a, b) <= k, with an early exit per row."""
    if abs(len(a) - len(b)) > k:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        if min(cur) > k:
            return False
        prev = cur
    return prev[-1] <= k


_FIX_CACHE = {}
# Indexed by first letter: enumerator slips are almost never in the first
# letter, and comparing every token against every word is tens of millions
# of edit-distance runs on Sao Paulo.
_BY_FIRST = collections.defaultdict(list)
for _w in VOCAB:
    _BY_FIRST[_w[0]].append(_w)
_VOCAB_SET = set(VOCAB)


def fuzzy_fix(desc_norm):
    """Replace each token within 1 edit (2 if 9+ letters) of a VOCAB word."""
    out = []
    for tok in desc_norm.split():
        if len(tok) < 6 or tok in _VOCAB_SET:
            out.append(tok)
            continue
        if tok not in _FIX_CACHE:
            k = 2 if len(tok) >= 9 else 1
            _FIX_CACHE[tok] = next((w for w in _BY_FIRST.get(tok[0], ())
                                    if _within(tok, w, k)), tok)
        out.append(_FIX_CACHE[tok])
    return " ".join(out)


# These win wherever they appear: "LOJA FECHADA" is a closed shop, however
# early LOJA sits in the string.
ABSOLUTE = ("vacant", "no description")


def classify(desc_norm):
    """(label, bucket) for a normalised description; bucket None = not mapped.

    THE HEAD NOUN WINS. A Portuguese trade description puts it first - BAR DO
    CLUBE, DELICIAS DA PRACA, RESTAURANTE DO HOTEL - so the rule whose match
    starts EARLIEST in the string decides, and rule order breaks a tie (which
    is how SALAO DE FESTAS beats SALAO). The first version took the first
    RULE that matched anywhere, and would have dropped all three of those
    examples as a club, a square and a hotel.
    """
    best = None
    for i, (label, bucket, pat) in enumerate(RULES):
        m = pat.search(desc_norm)
        if not m:
            continue
        if label in ABSOLUTE:
            return label, bucket
        cand = (m.start(), i, label, bucket)
        if best is None or cand < best:
            best = cand
    return (best[2], best[3]) if best else ("unmatched", None)


# Import-time checks for the expensive lessons (premises-taxonomy, Step 7).
for _d, _want in [("BAR DO CLUBE", "food service"),
                  ("RESTAURANTE DO HOTEL", "food service"),
                  ("DELICIAS DA PRACA", "unmatched"),   # not excluded as a square
                  ("SALAO DE FESTAS", "events venue"),
                  ("SALAO DE BELEZA", "personal services"),
                  ("LOJA FECHADA", "vacant"), ("DEPOSITO DE BEBIDAS", "retail"),
                  ("DEPOSITO", "parking / storage"), ("PADARIA", "retail"),
                  ("GARAGEM DO MERCADO", "parking / storage"),
                  ("LOJA", "catch-all"), ("CASA DO NORTE", "retail"),
                  ("CASA DE CARNES", "retail"), ("CASA", "not premises")]:
    assert classify(_d)[0] == _want, (_d, classify(_d), _want)


# --- privacy: a first name inside the description --------------------------
# Conservative on purpose: DO/DA + a token that is a common Brazilian first
# name or a diminutive (-INHO/-INHA/-ZINHO). "BAR DA TITA" counts; "CASA DO
# NORTE" and "ESQUINA DA PIZZA" do not.
FIRST_NAMES = set("""
ANA MARIA JOSE JOAO ANTONIO FRANCISCO CARLOS PAULO PEDRO LUCAS LUIZ LUIS
MARCOS GABRIEL RAFAEL DANIEL MARCELO BRUNO EDUARDO FELIPE RAIMUNDO RODRIGO
MANOEL MANUEL MATEUS ANDRE FERNANDO FABIO LEONARDO GUSTAVO GUILHERME LEANDRO
TIAGO THIAGO ANDERSON RICARDO MARCIO JORGE SEBASTIAO ALEXANDRE ROBERTO EDSON
DIEGO VITOR VICTOR SERGIO CLAUDIO JULIO RENATO ROGERIO GERALDO ADRIANO JOAQUIM
SANDRO WAGNER WELLINGTON RONALDO SILVIO MAURO MAURICIO MARIO NELSON OSVALDO
BENEDITO VALDIR VALTER WALTER NILTON MILTON ADEMIR JAIR JAIME CELSO ALMIR
ZECA ZE TONHO TONINHO CHICO NETO JUNIOR JUCA DUDU NANDO BETO BETINHO CACA
FRANCISCA ANTONIA ADRIANA JULIANA MARCIA FERNANDA PATRICIA ALINE SANDRA
CAMILA AMANDA BRUNA JESSICA LETICIA JULIA LUCIANA VANESSA MARIANA GABRIELA
VERA KELLY ROSA ROSANA ROSANGELA SIMONE SONIA TEREZA TERESA LUCIA HELENA
REGINA CRISTINA CLAUDIA DANIELA RENATA LARISSA BEATRIZ CARLA PAULA DEBORA
RAQUEL ELIANE ELAINE EDNA NEIDE CIDA FATIMA GRACA SOCORRO CONCEICAO APARECIDA
LURDES LOURDES DIVA NILDA SELMA TITA TIANA TIDA NINA LULU MARLENE IVONE IRENE
DENISE SUELI SUELY SOLANGE MARINA BIA DUDA NATHALIA NATALIA SANDRINHA VERINHA
MARIZETE MAROCA BRANCA NEGA NEGAO BAIANO BAIANA GAUCHO PARAIBA CEARENSE
ALEMAO PORTUGUES TURCO JAPONES JAPA CHINES CARIOCA MINEIRO NEGUINHO GORDO
GORDINHO MAGRAO CARECA LOIRA LOIRO TIA TIO VO VOVO DONA SEU SR SRA
""".split())
PERSON_TAIL = re.compile(r"\b(DO|DA)\s+([A-Z]{2,})(?:\s+[A-Z]{2,})?$")


def person_name_in(desc_norm):
    m = PERSON_TAIL.search(desc_norm)
    if not m:
        return False
    tok = m.group(2)
    return tok in FIRST_NAMES or re.search(r"(INHO|INHA|ZINHO|ZINHA|AO)$", tok) \
        and tok not in {"PAO", "LEAO", "CORACAO", "ESTACAO", "CONSTRUCAO",
                        "FEIJAO", "SERTAO", "JAPAO", "CAMINHAO", "PORTAO",
                        "BALCAO", "CARVAO", "PISTAO", "SALAO", "MAMAO",
                        "LIMAO", "FOGAO", "SABAO", "BOTAO", "ALEMAO"}


# --- main ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--sample", type=int, default=80,
                    help="random UNMATCHED rows to print for reading")
    args = ap.parse_args()

    z = zipfile.ZipFile(args.zip)
    member = max(z.infolist(), key=lambda i: i.file_size)
    f = io.TextIOWrapper(z.open(member), encoding="utf-8", errors="replace",
                         newline="")
    rd = csv.DictReader(f, delimiter=";")

    home_addr = set()
    rescued = collections.Counter()
    rows = []   # (addr_key, label, bucket, desc_norm, indicator, nv, locality)
    for row in rd:
        # Where the door number is blank and the first complement is a LOTE,
        # the lot IS the address (Brasilia names a block, not a door: 98.5%
        # of its "shared with a dwelling" rows had no number, so street +
        # number merged whole blocks). Owner decision 2026-09-23.
        lot = ""
        if (row["NUM_ENDERECO"].strip() in ("", "0")
                and row["NOM_COMP_ELEM1"].strip() == "LOTE"):
            lot = row["VAL_COMP_ELEM1"].strip()
        key = (row["COD_SETOR"], row["NUM_QUADRA"], row["NUM_FACE"],
               row["NOM_SEGLOGR"], row["NUM_ENDERECO"], row["DSC_MODIFICADOR"],
               lot)
        sp = row["COD_ESPECIE"]
        if sp in ("1", "2"):
            home_addr.add(key)
        elif sp == "6":
            d = norm(row["DSC_ESTABELECIMENTO"])
            label, bucket = classify(d)
            if label == "unmatched":
                d2 = fuzzy_fix(d)
                if d2 != d:
                    label2, bucket2 = classify(d2)
                    if label2 != "unmatched":
                        label, bucket = label2, bucket2
                        rescued[label] += 1
            rows.append((key, label, bucket, d,
                         row["COD_INDICADOR_ESTAB_ENDERECO"], row["NV_GEO_COORD"],
                         row["DSC_LOCALIDADE"].strip()))

    n = len(rows)
    print(f"=== {member.filename}: {n:,} establishment rows (COD_ESPECIE 6)")

    # 1. classification
    by_label = collections.Counter(r[1] for r in rows)
    print("\n1. CLASSIFICATION (ordered rules, first match wins)")
    for label, c in by_label.most_common():
        bucket = next((b for l, b, _ in RULES if l == label), None)
        tag = f"-> {bucket}" if bucket else "   excluded" if label not in (
            "unmatched", "catch-all") else "   ** CATCH-ALL **"
        print(f"   {label:<28} {c:>9,}  {c / n * 100:5.1f}%  {tag}")
    mapped = [r for r in rows if r[2]]
    ca = by_label["catch-all"] + by_label["unmatched"]
    print(f"   MAPPED to a bucket: {len(mapped):,} ({len(mapped) / n * 100:.1f}%)"
          f" | catch-all + unmatched: {ca:,} ({ca / n * 100:.1f}%)")
    for b in BUCKETS:
        c = sum(1 for r in mapped if r[2] == b)
        print(f"      {b:<20} {c:>9,}")
    print(f"   rescued from unmatched by the edit-distance pass: "
          f"{sum(rescued.values()):,} {dict(rescued.most_common(6))}")

    # 2. what the unmatched remainder is - READ it
    un = collections.Counter(r[3] for r in rows if r[1] == "unmatched")
    print(f"\n2. UNMATCHED: {sum(un.values()):,} rows, {len(un):,} distinct. Top 30:")
    for d, c in un.most_common(30):
        print(f"   {c:>6,}  {d[:64]}")
    rng = random.Random(20260923)
    pool = [r[3] for r in rows if r[1] == "unmatched"]
    print(f"   random sample of {args.sample} (seed 20260923) - read these:")
    for d in rng.sample(pool, min(args.sample, len(pool))):
        print("     ", d[:70])

    # 3. privacy
    print("\n3. PRIVACY (mapped rows only)")
    shared = [r for r in mapped if r[0] in home_addr]
    named = [r for r in mapped if person_name_in(r[3])]
    both = [r for r in named if r[0] in home_addr]
    print(f"   at an address that also holds a dwelling : {len(shared):,} "
          f"({len(shared) / len(mapped) * 100:.1f}%)  - UPPER bound: a shop "
          f"under flats shares its number too")
    print(f"   description carries a first name         : {len(named):,} "
          f"({len(named) / len(mapped) * 100:.1f}%)")
    print(f"   BOTH - a first name at a dwelling address: {len(both):,} "
          f"({len(both) / len(mapped) * 100:.1f}%)")
    for r in both[:: max(1, len(both) // 15)][:15]:
        print("      e.g.", r[3][:60])

    # 4. coordinates
    nv = collections.Counter(r[5] for r in mapped)
    print("\n4. COORDINATE LEVEL (mapped rows): "
          + ", ".join(f"{k}={v / len(mapped) * 100:.1f}%" for k, v in
                      sorted(nv.items())))

    # 5. one row per use-type per address: how much does it collapse?
    ind = collections.Counter(r[4] for r in mapped)
    print("\n5. ESTABLISHMENTS PER ROW (mapped rows): "
          + ", ".join(f"{k or '-'}={v / len(mapped) * 100:.1f}%" for k, v in
                      sorted(ind.items()))
          + "   (1 single, 2 two-to-ten, 3 over ten, 4 unknown)")
    # 6. does DROPPING the unmatched remainder skew the map by neighbourhood?
    # Bare trade names ("MUNDO VERDE") cannot be bucketed and are dropped. If
    # affluent districts favour brand names while others write "BAR", the
    # unmatched share varies by place and the map under-draws some districts.
    loc = collections.defaultdict(collections.Counter)
    for r in rows:
        loc[r[6]]["n"] += 1
        loc[r[6]]["drop"] += r[1] in ("unmatched", "catch-all")
    big_locs = [(k, v) for k, v in loc.items() if v["n"] >= 1500]
    shares = sorted((v["drop"] / v["n"] * 100, k, v["n"]) for k, v in big_locs)
    if shares:
        print(f"\n6. UNMATCHED + CATCH-ALL SHARE BY LOCALITY "
              f"({len(shares)} localities with >= 1,500 establishment rows)")
        print(f"   lowest : " + "; ".join(f"{k[:22]} {s:.0f}% (n={n:,})"
                                         for s, k, n in shares[:4]))
        print(f"   highest: " + "; ".join(f"{k[:22]} {s:.0f}% (n={n:,})"
                                         for s, k, n in shares[-4:]))
        vals = [s for s, _, _ in shares]
        print(f"   median {vals[len(vals) // 2]:.0f}%, range "
              f"{vals[0]:.0f}-{vals[-1]:.0f}%")

    per_addr = collections.Counter(r[0][:5] for r in rows)   # ignore modifier
    mall_rows = [r for r in rows if re.search(r"\b(SHOPPING|GALERIA)\b", r[3])]
    mall_addr = collections.Counter(r[0][:5] for r in mall_rows)
    print(f"   rows naming a SHOPPING/GALERIA: {len(mall_rows):,}; at those "
          f"addresses, establishment rows per address:")
    for k, _ in mall_addr.most_common(8):
        sample = next(r[3] for r in mall_rows if r[0][:5] == k)
        print(f"      {per_addr[k]:>5} rows  {k[3][:28]:<28} {k[4]:<6} "
              f"e.g. {sample[:40]}")


if __name__ == "__main__":
    sys.exit(main())
