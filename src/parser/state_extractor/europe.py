import re

# ============================================================
# GERMANY
# ============================================================

GERMANY_STATES = [
    'Bavaria', 'Bayern', 'Berlin', 'Brandenburg', 'Hamburg',
    'Hesse', 'Hessen', 'Saxony', 'Sachsen', 'Saxony-Anhalt',
    'North Rhine-Westphalia', 'NRW', 'Lower Saxony', 'Niedersachsen',
    'Mecklenburg-Western Pomerania', 'Rhineland-Palatinate',
    'Thuringia', 'Thueringen', 'Schleswig-Holstein',
    'Saarland', 'Bremen', 'Baden-Württemberg', 'Baden Wurttemberg'
]

# ============================================================
# UK
# ============================================================

UK_REGIONS = [
    'England', 'Scotland', 'Wales', 'Northern Ireland',
    'Greater London', 'London',
    'South East England', 'South West England',
    'East of England', 'West Midlands', 'East Midlands',
    'Yorkshire and the Humber', 'Yorkshire',
    'North West England', 'North East England',
    'Greater Manchester', 'Merseyside', 'Tyne and Wear',
    'West Yorkshire', 'South Yorkshire',
    'Kent', 'Surrey', 'Essex', 'Hampshire', 'Hertfordshire',
    'Lancashire', 'Oxfordshire', 'Cambridgeshire', 'Berkshire',
    'Buckinghamshire', 'Devon', 'Cornwall', 'Somerset', 'Dorset'
]

# ============================================================
# FRANCE
# ============================================================

FRANCE_REGIONS = [
    'Île-de-France', 'Ile-de-France', 'Ile de France',
    'Auvergne-Rhône-Alpes', 'Auvergne-Rhone-Alpes',
    'Bourgogne-Franche-Comté', 'Bourgogne Franche Comte',
    'Brittany', 'Bretagne', 'Normandy', 'Normandie',
    'Nouvelle-Aquitaine', 'Occitanie', 'Pays de la Loire',
    'Provence-Alpes-Côte d\'Azur', 'PACA', 'Corsica', 'Corse'
]

# ============================================================
# ITALY
# ============================================================

ITALY_REGIONS = [
    'Lombardy', 'Lombardia', 'Lazio', 'Tuscany', 'Toscana',
    'Sicily', 'Sicilia', 'Veneto', 'Emilia-Romagna',
    'Piemonte', 'Piedmont', 'Liguria', 'Calabria',
    'Campania', 'Sardinia', 'Sardegna', 'Apulia', 'Puglia',
    'Friuli', 'Umbria', 'Marche'
]

# ============================================================
# SPAIN
# ============================================================

SPAIN_REGIONS = [
    'Comunidad de Madrid', 'Madrid',
    'Catalonia', 'Catalunya', 'Cataluña',
    'Andalusia', 'Andalucía',
    'Valencian Community', 'Valencia',
    'Basque Country', 'País Vasco', 'Euskadi',
    'Galicia', 'Castile and León', 'Castilla y León',
    'Castilla-La Mancha', 'Canary Islands', 'Islas Canarias',
    'Murcia', 'Aragon', 'Aragón', 'Extremadura',
    'Balearic Islands', 'Islas Baleares',
    'Asturias', 'Navarre', 'Navarra', 'Cantabria', 'La Rioja'
]

# ============================================================
# NETHERLANDS
# ============================================================

NETHERLANDS_PROVINCES = [
    'North Holland', 'Noord-Holland',
    'South Holland', 'Zuid-Holland',
    'Utrecht', 'North Brabant', 'Noord-Brabant',
    'Gelderland', 'Groningen', 'Overijssel',
    'Limburg', 'Friesland', 'Fryslân',
    'Flevoland', 'Drenthe', 'Zeeland'
]

# ============================================================
# BELGIUM
# ============================================================

BELGIUM_REGIONS = ['Brussels', 'Flanders', 'Wallonia']

# ============================================================
# AUSTRIA
# ============================================================

AUSTRIA_REGIONS = [
    'Vienna', 'Wien', 'Lower Austria', 'Upper Austria',
    'Salzburg', 'Tyrol', 'Tirol', 'Styria', 'Steiermark',
    'Carinthia', 'Kärnten', 'Vorarlberg', 'Burgenland'
]

# ============================================================
# SWITZERLAND
# ============================================================

SWITZERLAND_CANTONS = [
    'Zurich', 'Zürich', 'Geneva', 'Genève', 'Basel', 'Bern',
    'Vaud', 'Ticino', 'St. Gallen', 'Lucerne', 'Luzern'
]

# ============================================================
# SWEDEN
# ============================================================

SWEDEN_COUNTIES = [
    'Stockholm', 'Uppsala', 'Skåne', 'Västra Götaland',
    'Östergötland', 'Jönköping', 'Kalmar', 'Blekinge'
]

# ============================================================
# PORTUGAL
# ============================================================

PORTUGAL_REGIONS = [
    'Lisbon', 'Lisboa', 'Porto', 'Oporto', 'Coimbra',
    'Braga', 'Faro', 'Algarve', 'Madeira', 'Azores', 'Açores'
]

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_europe_state(text, country):

    if country == "Germany":
        for state in GERMANY_STATES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "UK":
        for state in UK_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "France":
        for state in FRANCE_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Italy":
        for state in ITALY_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Spain":
        for state in SPAIN_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Netherlands":
        for state in NETHERLANDS_PROVINCES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Belgium":
        for state in BELGIUM_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Austria":
        for state in AUSTRIA_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Switzerland":
        for state in SWITZERLAND_CANTONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Sweden":
        for state in SWEDEN_COUNTIES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Portugal":
        for state in PORTUGAL_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    return ""
