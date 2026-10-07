"""The OpenStreetMap rail-geometry notice, one line per city page.

Each city's page shows only what its own map takes from OpenStreetMap (owner,
2026-10-03: the full notice ran to 690 words on each of 120 pages); the
Required notices page keeps the full list, components.py's notice 1. Every
fragment restates that list's words for one city, so neither may gain a fact
the other lacks. `geometry` is True where the map draws OSM's own line
geometry, which adds the closing sentence about the alignments.

Spelled as app/cities.py spells each city; components.py raises if this set
and the notice's cities differ.
"""

_LINES = (" The alignments drawn are OSM's own geometry; stations, rings and "
          "categories are this project's work.")


def _brazil(place, plural=False):
    return (f"the rail lines and stations of {place}, and "
            f"{'the município boundaries used to select them' if plural else 'its município boundary'}",
            True)


def _korea(place):
    return (f"the subway, light-rail and Korail lines and stations of {place}, and its boundary",
            True)


def _japan(place):
    return (f"the English names of {place}'s stations, though not its lines or boundaries", False)


OSM_RAIL_BY_CITY = {
    "Mexico City (Regional)": ("the rail route geometry and station locations of Mexico City's Metro CDMX "
                    "and Tren Ligero, and the boundaries of Ciudad de México and four State "
                    "of México municipios", True),
    "Guadalajara (Regional)": ("the rail route geometry and station locations of "
                               "Guadalajara's Tren Ligero", True),
    "Monterrey (Regional)": ("the rail route geometry and station locations of Monterrey's "
                             "Metrorrey, with the boundaries of its four municipios", True),
    "Barcelona": ("the rail route geometry and station locations of the Metro de Barcelona, "
                  "including its FGC lines and both funiculars", True),
    "Lille (Regional)": ("the route geometry of Lille's two métro lines", True),
    "Oslo": ("the per-line colors of Oslo's T-bane and tram lines", False),
    "Bergen": ("the color of Bergen's Bybanen line 1", False),
    "Copenhagen": ("Copenhagen's Metro and S-tog lines and stations and the municipal "
                   "boundaries used to select them", True),
    "Aarhus": ("Aarhus's Letbane L2 line and its stops, the municipal boundaries used to "
               "select them and the address points used to place its businesses", True),
    "Kitchener–Waterloo (Regional)": ("Kitchener–Waterloo's ION line and its stops", True),
    "Odense": ("Odense's Letbane line and its stops, the municipal boundary used to select "
               "them and the address points used to place its businesses", True),
    "Liepāja": ("Liepāja's tram line and its stops and the city boundary used to select "
                "them and its businesses", True),
    "Daugavpils": ("Daugavpils's tram lines and their stops and the city boundary used to "
                   "select them and its businesses", True),
    "Buffalo": ("Buffalo's NFTA Metro Rail line and its stations", True),
    "Sacramento": ("Sacramento's SacRT Blue and Gold Lines and their stations, and the "
                   "municipal boundaries used to select them", True),
    "Houston": ("Houston's METRORail Red, Green and Purple Lines and their stations", True),
    "Ottawa": ("Ottawa's O-Train Lines 1, 2 and 4 and their stations", True),
    "Minneapolis": ("Minneapolis's METRO Blue and Green Lines and their stations", True),
    "Pittsburgh": ("Pittsburgh's PRT Red, Blue and Silver Lines and their stations", True),
    "Dallas": ("Dallas's DART Light Rail Red, Blue, Green and Orange Lines and their "
               "stations", True),
    "Kansas City": ("Kansas City's KC Streetcar and its stops", True),
    "Tucson": ("Tucson's Sun Link and its stops", True),
    "Tacoma": ("Tacoma's T Line and its stops", True),
    "New Orleans": ("New Orleans's five streetcar lines and their stops", True),
    "Florence": ("Florence's T1 and T2 tram lines and their stops and the comune boundaries "
                 "used to select them and its businesses", True),
    "Den Haag": ("Den Haag's fourteen HTM tram lines and their stops and the municipal "
                 "boundaries used to select them and its businesses", True),
    "Göteborg": ("Göteborg's tram lines 1 to 13 and their stops and the kommun boundaries "
                 "used to select them and its businesses", True),
    "Zurich": ("Zurich's sixteen VBZ tram lines and their stops and the municipal "
               "boundaries used to select them and its businesses", True),
    "Geneva (Regional)": ("Geneva's five TPG tram lines and their stops and the commune "
                          "boundaries used to select them and its businesses", True),
    "Thessaloniki": ("Thessaloniki's metro line and its stations and the municipal "
                     "boundary used to select them and its businesses", True),
    "Gelsenkirchen": ("Gelsenkirchen's four tram and Stadtbahn lines and their stops, and "
                      "its city boundary", True),
    "Bremen": ("Bremen's eight BSAG tram lines and their stops, and its city boundary", True),
    "Rome": ("Rome's metro and Roma–Viterbo urban lines and their stations, and its city "
             "boundary", True),
    "Palma": ("Palma's Metro M1 and its stations, and the municipal boundaries used to "
              "select them", True),
    "Brno": ("Brno's tram lines", True),
    "Plzeň": ("Plzeň's tram lines and stops, and its boundary", True),
    "Olomouc": ("Olomouc's tram lines and stops, and its boundary", True),
    "Ostrava": ("Ostrava's tram lines and stops, and its boundary", True),
    "Liberec (Regional)": ("the tram lines and stops of Liberec and Jablonec nad Nisou, and "
                           "those towns' boundaries", True),
    "Most (Regional)": ("the tram lines and stops of Most and Litvínov, and those towns' "
                        "boundaries", True),
    "São Paulo": ("São Paulo's metro, VLT and suburban lines and stations, with its CPTM "
                  "Linha 9, and its município boundary", True),
    "Rio de Janeiro (Regional)": ("Rio de Janeiro's metro, VLT and SuperVia lines and "
                                  "stations, and the município boundaries used to select "
                                  "them", True),
    "Belo Horizonte (Regional)": _brazil("Belo Horizonte", True),
    "Brasília": _brazil("Brasília"),
    "Salvador": _brazil("Salvador"),
    "Fortaleza (Regional)": _brazil("Fortaleza", True),
    "Porto Alegre (Regional)": _brazil("Porto Alegre", True),
    "Recife (Regional)": _brazil("Recife", True),
    "Santos (Regional)": _brazil("Santos", True),
    "Prague": ("Prague's city boundary", False),
    "Amsterdam": ("Amsterdam's city boundary", False),
    "Rotterdam": ("Rotterdam's city boundary", False),
    **{c: (f"{c}'s commune boundary, and its neighbors', which name the stations "
           "outside it", False) for c in ("Antwerp", "Ghent", "Charleroi")},
    "Liège": ("Liège's commune boundary", False),
    "Hong Kong": ("Hong Kong's MTR and Light Rail lines and stations, and its boundary", True),
    "Seoul": ("Seoul's subway lines and stations and its boundary", True),
    "Taichung": ("the route of Taichung's Green Line", True),
    "Taoyuan": ("the route of Taoyuan's Airport MRT", True),
    "Taipei (Regional)": ("the metro and light-rail lines and stations of Taipei and New "
                          "Taipei", True),
    "Daegu": _korea("Daegu"),
    "Busan": _korea("Busan"),
    "Incheon": _korea("Incheon"),
    "Goyang": _korea("Goyang"),
    "Seongnam": _korea("Seongnam"),
    "Yongin": _korea("Yongin"),
    "Suwon": _korea("Suwon"),
    "Bucheon": _korea("Bucheon"),
    "Namyangju": _korea("Namyangju"),
    "Ansan": _korea("Ansan"),
    "Uijeongbu": _korea("Uijeongbu"),
    "Anyang (Regional)": ("the subway and Korail lines and stations of Anyang, Gunpo and "
                          "Uiwang, and their boundaries", True),
    "Daejeon": _korea("Daejeon"),
    "Gwangju": _korea("Gwangju"),
    "Gimhae": _korea("Gimhae"),
    "Gimpo": _korea("Gimpo"),
    "Siheung": _korea("Siheung"),
    "Sydney": ("the train and metro routes of Sydney and its City boundary", True),
    "Melbourne": ("the train and metro routes of Melbourne and its City boundary", True),
    "Buenos Aires": ("Buenos Aires's Subte and Premetro routes and its boundary", True),
    "Mendoza": ("Mendoza's Metrotranvía and its stations, and the department boundaries "
                "used to select them", True),
    "Seattle (Regional)": ("Seattle's Link 1 and 2 Lines", True),
    "London": ("the lines and stations of London's Underground, DLR, Elizabeth line and "
               "Overground, and the boundaries used to select them", True),
    "Glasgow": ("the lines and stations of the Glasgow Subway, and the boundaries used to "
                "select them", True),
    "Newcastle (Regional)": ("the lines and stations of the Tyne and Wear Metro, and the "
                             "boundaries used to select them", True),
    "Manchester (Regional)": ("the lines and stations of Manchester Metrolink, and the "
                              "boundaries used to select them", True),
    "Birmingham (Regional)": ("the line and stations of West Midlands Metro, and the "
                              "boundaries used to select them", True),
    "Edinburgh": ("the line and stations of Edinburgh Trams, and the boundaries used to "
                  "select them", True),
    "Sheffield": ("the lines and stations of Sheffield Supertram, and the boundaries used "
                  "to select them", True),
    "Nottingham (Regional)": ("the lines and stations of Nottingham Express Transit, and "
                              "the boundaries used to select them", True),
    "Blackpool (Regional)": ("the line and stations of the Blackpool Tramway, and the "
                             "boundaries used to select them", True),
    "Liverpool (Regional)": ("the lines and stations of Merseyrail, and the boundaries "
                             "used to select them", True),
    "Stockholm": ("Stockholm's Tunnelbana lines and stations and its kommun boundaries", True),
    "Bucharest": ("Bucharest's metro lines and stations and its city and sector boundaries",
                  True),
    "Tbilisi": ("the Tbilisi Metro's lines and stations and the city's boundary", True),
    "Montpellier": ("the tram line geometry of Montpellier", True),
    "Strasbourg": ("the tram line geometry of Strasbourg", True),
    "Le Havre": ("the tram line geometry of Le Havre", True),
    "Caen": ("the tram line geometry of Caen", True),
    "Rouen (Regional)": ("the tram and métro line geometry of Rouen", True),
    "Philadelphia": ("the location of Philadelphia's 11th Street station, which is closed "
                     "for works and not drawn", False),
    **{c: _japan(c) for c in (
        "Kobe", "Osaka", "Sapporo", "Fukuoka", "Kyoto", "Tokyo", "Yokohama", "Hiroshima",
        "Matsuyama", "Toyama", "Kumamoto", "Fukui", "Nagasaki", "Utsunomiya", "Kitakyushu",
        "Sakai", "Hakodate", "Kagoshima", "Okayama", "Kōchi", "Kawasaki", "Yokosuka",
        "Himeji", "Nishinomiya", "Takamatsu", "Toyota", "Yokkaichi", "Ōtsu", "Nara",
        "Hamamatsu", "Higashiōsaka", "Kurume", "Sasebo", "Shimonoseki")},
}


def osm_rail_text(city):
    """The notice's text on one city's page."""
    fragment, geometry = OSM_RAIL_BY_CITY[city]
    return (f"From OpenStreetMap: {fragment}. © OpenStreetMap contributors, available "
            f"under the Open Database License." + (_LINES if geometry else ""))
