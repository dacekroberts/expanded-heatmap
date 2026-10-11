"""Gelsenkirchen's sign rule: which survey signs read as a person's own name.

The dot shows the name on the sign (the survey's `Name`); a sign that reads as
a person's own name and nothing more shows the business's category instead
(owner, 2026-10-05, call 1; Liège's and Brussels' rule). config.PERSON_NAMED
holds those signs as KEYS (`pipeline/name_keys.py`), never as names.

`person_sign` is a shape test that PROPOSES them, Liège's
(`pipeline/countries/belgium_logic.person_sign`) with German trade words and
the given names of the Ruhr's population; `chain_signs` keeps a sign found at
two or more points of the survey (a brand, Kansas City's rule, even where it
is a founder's name). The proposals are NOT READ BY EYE in the build (no name
is printed); the privacy review reads them.

    python -m pipeline.gelsenkirchen.signs --person-keys

prints the keys and counts only, never a sign.
"""
import re
import sys
import unicodedata


def normalise_sign(sign):
    """The sign as compared: casefolded, accents and punctuation dropped,
    spaces collapsed. Never displayed."""
    if not isinstance(sign, str):
        return ""
    s = sign.casefold().replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


# Common given names among Gelsenkirchen's population (German, Turkish,
# Arabic and Kurdish, Polish, Italian, Greek, Balkan, Russian and Ukrainian,
# Spanish and Portuguese, English forms), written from general knowledge,
# folded as normalise_sign folds them. A sign of two or three words with one
# of these at either end, and no trade word, reads as a person's own name. Not
# a list of anyone: a given name alone identifies nobody.
GIVEN_NAMES = frozenset("""
achim adam adrian agnes albert alexander alexandra alfred alfons alina alois
andrea andreas andre angela angelika anja anke anna anne annette anton antonia
armin arnold axel barbara bastian beate benedikt benjamin bernd bernhard bettina
birgit bjorn brigitte bruno carina carmen carola carolin carsten christa
christian christiane christina christine christoph christopher claudia clemens
cornelia daniel daniela david denis dennis detlef dieter dietmar dirk doris
dominik dorothea edgar edith elisabeth elke elena ellen emil emma erich erika
ernst erwin eva fabian felix florian frank franz franziska friedrich fritz
gabriele georg gerd gerda gerhard gertrud gisela gregor gudrun gunter gunther
hannah hannelore hans harald hartmut heike heiko heinrich heinz helga helmut
henning herbert hermann hildegard holger horst hubert ilse inge ingo ingrid
irene iris jakob jan jana janina jens jessica joachim jochen johann johanna
johannes jonas jorg josef julia julian jurgen jutta kai karin karl karsten
katharina kathrin katja kerstin kevin klaus konrad kurt lars laura lea lena
leon lisa lothar lukas lutz manfred manuel manuela marc marcel marco margarete
maria marie marina mario marion markus martha martin martina mathias matthias
max maximilian melanie michael michaela monika nadine nicole niklas nina norbert
olaf oliver otto patrick paul paula peter petra philipp rainer ralf ralph regina
reinhard renate rene richard rita robert roland rolf rudolf ruth sabine sabrina
sandra sara sarah sascha sebastian silke simon simone sonja stefan stefanie
steffen stephan susanne sven sylvia tanja thomas thorsten tim timo tobias tom
torsten udo ulrich ulrike ursula ute uwe vanessa vera verena volker walter
werner wilhelm willi wolfgang yvonne
ahmet ali alper arda ayse aysel ayhan aylin baris berkay burak burcu cem cemal
cengiz deniz derya ebru elif emine emre engin erkan esra fatih fatma ferhat
gokhan gul gulsen hakan halil hasan hatice huseyin ibrahim ilker ismail kadir
kemal kenan levent mehmet melek meltem murat mustafa nermin nur ozan ozlem
recep selim serkan sevgi sibel songul suleyman tarik tuba tuncay turgut
ufuk umut volkan yasemin yasin yilmaz yusuf zehra zeynep
abdul abdullah ahmad ahmed aisha amin amir amira anas bilal fadi farid fatima
hamid hassan hussein jamal karim khaled layla mahmoud mariam mohamed mohammad
mohammed muhammad mustapha nabil nadia omar rami samir sami tarek walid yasmin
youssef zainab
agnieszka anna barbara dariusz ewa grzegorz jacek janusz jerzy joanna katarzyna
krzysztof magdalena malgorzata marek marta mariusz michal pawel piotr tomasz
wojciech zbigniew
alessandro angelo antonio carlo carla francesco gianni giovanni giuseppe luca
luigi marcello massimo paolo pietro rosa salvatore sergio vincenzo
dimitrios georgios giorgos ioannis konstantinos nikolaos panagiotis vasilis
dragan goran ivan milan milos nikola zoran
alexei dmitri igor irina natalia natascha olga sergej svetlana tatjana viktor
vladimir
carlos jose juan luis manuel miguel pedro
alain antoine bernard camille celine chantal claude didier dominique emilie
francois gerard guillaume henri isabelle jacques jean jeanne julien louis luc
mario nathalie nicolas philippe pierre sandrine sophie sylvie thierry valerie
vincent yves enzo giulia lucia nico sandro sofia
""".split())

# Words that make a sign a trade name whatever else it holds: articles and
# prepositions, trades and premises in German and the English a sign uses,
# and company forms. Folded as normalise_sign folds them.
TRADE_WORDS = frozenset("""
der die das dem den des zum zur am im bei beim und an auf in ins fur mit
the and of my your
gmbh mbh ag kg ug ek ohg gbr co inh inhaber
backerei backer backstube baeckerei konditorei cafe kaffee bistro bar kneipe
pub gaststatte gasthof gasthaus restaurant ristorante trattoria pizzeria pizza
imbiss grill doner doener kebab kebap burger sushi wok asia china thai
eiscafe eisdiele eis trinkhalle kiosk buedchen budchen lotto tabak presse
friseur friseure friseursalon frisur frisuren haar haare hair haarstudio
barber barbershop salon studio kosmetik beauty nails nagel nail tattoo
fusspflege massage spa wellness
apotheke optik optiker akustik horgerate sanitatshaus orthopadie
mode moden fashion boutique schuhe schuh shoes textil textilien
blumen floristik garten zoo tierbedarf
markt supermarkt getranke getrankemarkt metzgerei fleischerei feinkost
lebensmittel shop store laden handel center zentrum
moebel mobel kuche kuchen kuechen raum haus home wohnen deko
schmuck juwelier uhren gold goldschmied
foto handy phone mobile computer elektro elektronik
buch bucher buchhandlung papier schreibwaren
reinigung waescherei wascherei
auto autohaus kfz reifen fahrrad fahrrader rad
reisen reiseburo
sport sports fitness
kinder baby spiel spielwaren
international import export service team club
""".split())

# Particles inside a surname, skipped when counting a name's words.
PARTICLES = frozenset("von van de der den di da del della dos ter ten zu el al bin ibn".split())

_WORD = re.compile(r"^[^\W\d_]+(?:['’\-][^\W\d_]+)*$")
_INITIAL = re.compile(r"^[^\W\d_]\.?$")


def person_sign(sign):
    """Does this sign read as a person's own name and nothing more?

    Two or three words (surname particles aside), letters only, no trade word
    and no company form, and a given name (or a bare initial) at either end:
    "Given Surname", "Surname Given", "G. Surname". A single word, a sign with
    a trade word ("Friseur Surname", "Bei Given") or a digit, "&" or "/" is a
    trade name. A shape test only: it proposes, config.PERSON_NAMED decides,
    and `chain_signs` keeps a founder's name that is a brand.
    """
    if not isinstance(sign, str):
        return False
    raw = sign.strip()
    if not raw or re.search(r"[\d&/@+|]", raw):
        return False
    words = [w.strip(",;:") for w in re.split(r"\s+", raw.replace(".", ". ").strip()) if w]
    words = [w for w in words if w]
    folded = [normalise_sign(w) for w in words]
    if any(f in TRADE_WORDS or any(p in TRADE_WORDS for p in f.split()) for f in folded):
        return False
    core = [(w, f) for w, f in zip(words, folded) if f not in PARTICLES]
    if not 2 <= len(core) <= 3:
        return False
    if not all(_WORD.match(w) or _INITIAL.match(w) for w, _ in core):
        return False

    def given(f):
        return f in GIVEN_NAMES or any(p in GIVEN_NAMES for p in f.split(" ") if p)

    (w0, f0), (w1, f1) = core[0], core[-1]
    return (given(f0) or given(f1) or bool(_INITIAL.match(w0))
            or bool(_INITIAL.match(w1)))


def chain_signs(signs, points):
    """Normalised signs found at two or more distinct points of the survey:
    a brand, kept even where it reads as a founder's name.

    signs: Series of signs; points: Series of hashable point keys, same index."""
    import pandas as pd

    df = pd.DataFrame({"s": signs.map(normalise_sign), "p": points})
    df = df[df["s"] != ""]
    n = df.groupby("s")["p"].nunique()
    return set(n[n >= 2].index)


def person_rows(signs, points):
    """Boolean Series: the sign reads as a person's own name and is not a
    chain's."""
    chains = chain_signs(signs, points)
    return signs.map(person_sign) & ~signs.map(normalise_sign).isin(chains)


def _person_keys():
    """Print the keys of the kept rows' person-shaped signs, and counts.
    Never a sign."""
    from pipeline.gelsenkirchen import config
    from pipeline.gelsenkirchen.step2_clean_businesses import load_survey
    from pipeline.name_keys import keys_of

    df = load_survey()
    pts = df["x25832"].round(1).astype(str) + "," + df["y25832"].round(1).astype(str)
    shaped = df["sign"].map(person_sign)
    hit = person_rows(df["sign"], pts) & df["kept"]
    chains = shaped & df["kept"] & ~hit
    keys = sorted(set(keys_of(df.loc[hit, "sign"]).dropna()))
    print(f"{int(df['kept'].sum()):,} kept rows; {int((shaped & df['kept']).sum())} signs "
          f"person-shaped, {int(chains.sum())} of them found at two or more points (kept as "
          f"brands); {int(hit.sum())} rows withheld, {len(keys)} distinct keys:")
    for i in range(0, len(keys), 4):
        print("    " + ", ".join(f'"{k}"' for k in keys[i:i + 4]) + ",")
    stale = sorted(set(config.PERSON_NAMED) - set(keys))
    print(f"  config.PERSON_NAMED holds {len(config.PERSON_NAMED)}; {len(stale)} no longer proposed")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--person-keys":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        _person_keys()
    else:
        sys.exit("usage: python -m pipeline.gelsenkirchen.signs --person-keys")
