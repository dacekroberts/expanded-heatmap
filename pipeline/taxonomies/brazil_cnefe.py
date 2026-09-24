"""IBGE's CNEFE 2022 - the census's own walk of every block - classified from
the enumerator's free-text description of each establishment.

**NATIONAL, NOT PER-CITY.** CNEFE is one file per município in one schema, so
every Brazilian city shares this module and a correction reaches all nine
(france_naf.py's shape). The reader is pipeline/countries/brazil_register.py;
per-city verdicts live in the city's config.

**THE RULES ARE STAGING'S, LIFTED** from scripts/screen_cnefe.py on
2026-09-24 - SPELLING, RULES, VOCAB, the edit-distance pass, the head-noun
classifier with its import-time checks, and the first-name measure - and then
EXTENDED the same day (RULES_VERSION 2, the owner's call), because São Paulo's
map missed about one storefront in six near its stations and many of those
misses were plain words the rules lacked (PIZZA beside PIZZARIA, BURGUER beside
HAMBURGUER). Every figure in the nine Brazilian briefs was measured on version
1. One rename: the screen's `classify(desc_norm)` is `classify_text` here,
because the taxonomy interface's `classify()` takes a row. Written by the São
Paulo build session on the owner's decision of 2026-09-24
(docs/session_roles.md gives shared taxonomy code to staging by default;
staging was told). **The screen is to import its rules from here, so there is
one copy; until it does, the screen is version 1.**

**THE DESCRIPTION IS CLASSIFIED ONCE, IN STEP 2, NEVER AT RENDER.**
`classify_description()` reads `DSC_ESTABELECIMENTO`; the reader stores the
bucket in VALUE_COLUMN and `classify()` reads it back. So the map never needs
the description to put a pin in a bucket - which matters, because at an
address that also holds a dwelling the description must never be shown (the
owner's decision of 2026-09-23, and a condition of the LGPD reading in
docs/data_sources.md).

**A FREE-TEXT TAXONOMY HAS NO CODE LIST, SO ITS CATCH-ALL IS WHAT NO RULE
MATCHED** - 19.7% of São Paulo's establishment rows, mostly bare trade names
(`MUNDO VERDE`). They are dropped rather than guessed, and they are not spread
evenly: more of them in affluent commercial districts. The screen's docstring
carries the rest of the design.
"""
import collections
import re
import unicodedata

FIELD_LABEL = "Category"
VALUE_COLUMN = "cnefe_category"

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


def classify_text(desc_norm):
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
    assert classify_text(_d)[0] == _want, (_d, classify_text(_d), _want)


# --- version 2: words that only RESCUE a row nothing above matched ----------
#
# 1 = staging's rules exactly as screened (scripts/screen_cnefe.py, 2026-09-23)
#     - every figure in the nine Brazilian build briefs was measured on it.
# 2 = 2026-09-24, the owner's call, after São Paulo's map was found to miss
#     about one storefront in six near its stations: WEAK_RULES below.
#
# WEAK, BECAUSE THE FIRST ATTEMPT WAS NOT. The same words added to RULES
# rescued 3,814 unmatched São Paulo rows and also MOVED 238 rows version 1 had
# already placed, mostly wrongly - under "the head noun wins", PET became the
# head of `PET BANHO E TOSA` (pet grooming, a personal service) and of
# `PET ... CLINICA VETERINARIA` (a vet, excluded), and PAO the head of
# `KI PAO DISTRIBUIDORA DE PAES`. A word that names a trade only when nothing
# else in the string does is a fallback, like the edit-distance pass: so these
# are consulted only for a row that is still unmatched after it, and version 2
# cannot change any row version 1 classified - the briefs' figures for
# classified rows stand; only the unmatched share shrinks.
#
# Every word was read first in São Paulo's unmatched rows, its most frequent
# captures listed and read (scratch, 2026-09-24). Whole words, so PAO never
# meets SAO PAULO and PET never PETROBRAS. Read and REJECTED: SOFA (a quarter
# of its rows upholstery repair), FRUTA (street stalls, fruit trucks,
# distributors), PECAS (machine parts as often as shop parts). Earliest match
# wins as above; on a tie, food first, so PAO DE QUEIJO (a café chain) beats
# PAO (a bakery, Retail on the bakery precedent).
RULES_VERSION = 2
WEAK_RULES = [
    ("food service", "Food service", rx(
        r"PIZZA\b", r"BURG(U)?ER\b", "TRATTORIA", "OSTERIA", "BUTE(K|C)",
        r"COFFEE\b", "PAO DE QUEIJO")),
    ("personal services", "Personal services", rx(
        r"HAIR\b", r"MAKE ?UP\b", "DEPIL", r"DRY ?CLEAN", r"BA(BER|RBAR) SHOP\b")),
    ("retail", "Retail", rx(
        "PADOCA", r"PAO\b", r"FRIOS\b", r"JOIAS\b", r"OUTLET\b", r"SHOP\b",
        r"CLOTH(ES|ING)\b", r"PET\b", "INSTRUMENTOS? MUSICA")),
]


def classify_weak(desc_norm):
    """(label, bucket) from WEAK_RULES alone, or ("unmatched", None)."""
    best = None
    for i, (label, bucket, pat) in enumerate(WEAK_RULES):
        m = pat.search(desc_norm)
        if m and (best is None or (m.start(), i) < best[:2]):
            best = (m.start(), i, label, bucket)
    return (best[2], best[3]) if best else ("unmatched", None)


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


# --- the taxonomy interface ---------------------------------------------------

def classify_description(raw):
    """(label, bucket, how) for one raw `DSC_ESTABELECIMENTO`; `how` is
    "rules", "edit distance" or "version 2".

    The screen's main loop - normalise and classify, and only when NOTHING
    matched, retry after the edit-distance pass - then, still unmatched, the
    version-2 words. Each fallback can rescue an unmatched row and none can
    re-route a row an earlier stage matched.
    """
    d = norm(raw)
    label, bucket = classify_text(d)
    if label != "unmatched":
        return label, bucket, "rules"
    d2 = fuzzy_fix(d)
    if d2 != d:
        label2, bucket2 = classify_text(d2)
        if label2 != "unmatched":
            return label2, bucket2, "edit distance"
    for text in (d, d2):
        label3, bucket3 = classify_weak(text)
        if label3 != "unmatched":
            return label3, bucket3, "version 2"
    return label, bucket, "rules"


# Version 2's words, and the traps they were read against - through the whole
# pipeline, so a version-1 match is shown to win.
for _raw, _want in [("DOMINOS PIZZA", "food service"), ("ROSSO BURGUER", "food service"),
                    ("CASA DO PAO DE QUEIJO", "food service"), ("COFFEE SHOP", "food service"),
                    ("CASA DO PAO", "retail"), ("MEGA HAIR", "personal services"),
                    ("BABER SHOP", "personal services"),
                    ("SAO PAULO", "unmatched"), ("PETROBRAS", "unmatched"),
                    ("REFORMA DE SOFA", "unmatched"),
                    # version 1 still decides these, as it did before
                    ("PET BANHO E TOSA", "personal services"),
                    ("PET CLINICA VETERINARIA", "office / professional"),
                    ("KI PAO DISTRIBUIDORA DE PAES", "industry / trades"),
                    ("PAO HAMBURGUER", "food service"),
                    ("RECICLAGEM PET", "industry / trades")]:
    assert classify_description(_raw)[0] == _want, (_raw, classify_description(_raw), _want)


def classify(row):
    """The bucket step 2 already stored - see the module docstring."""
    value = row.get(VALUE_COLUMN)
    return value if value in BUCKETS else None


def legend_label(bucket):
    return bucket
