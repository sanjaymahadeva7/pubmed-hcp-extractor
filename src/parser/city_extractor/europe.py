import re

# ============================================================
# COUNTRY DATA — Europe
# ============================================================

UK_COUNTRIES = (
    'England', 'Scotland', 'Wales', 'Northern Ireland',
    'Great Britain', 'Britain',
    'United Kingdom', 'UK'
)


GERMAN_STATES = (
    'Baden-Württemberg', 'Baden-Wurttemberg',
    'Bavaria', 'Bayern',
    'Berlin',
    'Brandenburg',
    'Bremen',
    'Hamburg',
    'Hesse', 'Hessen',
    'Lower Saxony', 'Niedersachsen',
    'Mecklenburg-Vorpommern', 'Mecklenburg-Western Pomerania',
    'North Rhine-Westphalia', 'Nordrhein-Westfalen', 'NRW',
    'Rhineland-Palatinate', 'Rheinland-Pfalz',
    'Saarland',
    'Saxony', 'Sachsen',
    'Saxony-Anhalt', 'Sachsen-Anhalt',
    'Schleswig-Holstein',
    'Thuringia', 'Thüringen', 'Thuringen'
)


ITALIAN_REGIONS = (
    'Lombardy', 'Lombardia',
    'Lazio',
    'Tuscany', 'Toscana',
    'Sicily', 'Sicilia',
    'Veneto',
    'Emilia-Romagna',
    'Piemonte', 'Piedmont',
    'Liguria',
    'Calabria',
    'Campania',
    'Sardinia', 'Sardegna',
    'Apulia', 'Puglia',
    'Friuli', 'Friuli-Venezia Giulia',
    'Umbria',
    'Marche',
    'Abruzzo',
    'Molise',
    'Basilicata',
    'Trentino', 'Trentino-Alto Adige', 'South Tyrol',
    "Valle d'Aosta", 'Aosta Valley'
)


SPANISH_REGIONS = (
    'Comunidad de Madrid', 'Madrid',
    'Catalonia', 'Catalunya', 'Cataluña',
    'Andalusia', 'Andalucía',
    'Valencian Community', 'Valencia', 'Comunidad Valenciana',
    'Basque Country', 'País Vasco', 'Euskadi',
    'Galicia',
    'Castile and León', 'Castilla y León',
    'Castilla-La Mancha',
    'Canary Islands', 'Islas Canarias',
    'Murcia',
    'Aragon', 'Aragón',
    'Extremadura',
    'Balearic Islands', 'Islas Baleares',
    'Asturias', 'Principality of Asturias',
    'Navarre', 'Navarra',
    'Cantabria',
    'La Rioja',
    'Ceuta',
    'Melilla'
)


# ============================================================
# REGEX
# ============================================================

UK_COUNTRIES_PATTERN = '|'.join(re.escape(c) for c in UK_COUNTRIES)
GERMAN_STATES_PATTERN = '|'.join(re.escape(s) for s in GERMAN_STATES)
ITALIAN_REGIONS_PATTERN = '|'.join(re.escape(r) for r in ITALIAN_REGIONS)
SPANISH_REGIONS_PATTERN = '|'.join(re.escape(r) for r in SPANISH_REGIONS)

# UK
PATTERN_UK_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+[A-Z]{1,2}\d{1,2}\s*\d?[A-Z]{2}\s*,?\s*(?:UK|United Kingdom|England|Scotland|Wales)', re.IGNORECASE)
PATTERN_UK_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + UK_COUNTRIES_PATTERN + r')', re.IGNORECASE)
PATTERN_UK_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:UK|United Kingdom)\b', re.IGNORECASE)

# Germany
PATTERN_GERMANY_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*Germany', re.IGNORECASE)
PATTERN_GERMANY_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + GERMAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_GERMANY_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Germany\b', re.IGNORECASE)

# France
PATTERN_FRANCE_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*France', re.IGNORECASE)
PATTERN_FRANCE_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*France\b', re.IGNORECASE)

# Italy
PATTERN_ITALY_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*(?:Italy|Italia)', re.IGNORECASE)
PATTERN_ITALY_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + ITALIAN_REGIONS_PATTERN + r')', re.IGNORECASE)
PATTERN_ITALY_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Italy|Italia)\b', re.IGNORECASE)

# Spain
PATTERN_SPAIN_1 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s+\d{5}\s*,?\s*(?:Spain|España)', re.IGNORECASE)
PATTERN_SPAIN_2 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s*,\s*(' + SPANISH_REGIONS_PATTERN + r')', re.IGNORECASE)
PATTERN_SPAIN_3 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s*,\s*(?:Spain|España)\b', re.IGNORECASE)

# Netherlands
PATTERN_NL_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*[A-Z]{2}\s*,?\s*(?:Netherlands|Nederland)', re.IGNORECASE)
PATTERN_NL_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Netherlands|Nederland|The Netherlands)\b', re.IGNORECASE)

# Switzerland
PATTERN_CH_1 = re.compile(r',\s*([A-Z][a-zü]+(?:\s+[A-Z][a-zü]+)*)\s+\d{4}\s*,?\s*(?:Switzerland|Schweiz|Suisse|Svizzera)', re.IGNORECASE)
PATTERN_CH_2 = re.compile(r',\s*([A-Z][a-zü]+(?:\s+[A-Z][a-zü]+)*)\s*,\s*(?:Switzerland|Schweiz|Suisse|Svizzera)\b', re.IGNORECASE)

# Sweden
PATTERN_SE_1 = re.compile(r',\s*([A-Z][a-zåäö]+(?:\s+[A-Z][a-zåäö]+)*)\s+\d{3}\s*\d{2}\s*,?\s*(?:Sweden|Sverige)', re.IGNORECASE)
PATTERN_SE_2 = re.compile(r',\s*([A-Z][a-zåäö]+(?:\s+[A-Z][a-zåäö]+)*)\s*,\s*(?:Sweden|Sverige)\b', re.IGNORECASE)

# Belgium
PATTERN_BE_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*,?\s*(?:Belgium|België|Belgique)', re.IGNORECASE)
PATTERN_BE_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Belgium|België|Belgique)\b', re.IGNORECASE)

# Austria
PATTERN_AT_1 = re.compile(r',\s*([A-Z][a-zöäü]+(?:\s+[A-Z][a-zöäü]+)*)\s+\d{4}\s*,?\s*(?:Austria|Österreich)', re.IGNORECASE)
PATTERN_AT_2 = re.compile(r',\s*([A-Z][a-zöäü]+(?:\s+[A-Z][a-zöäü]+)*)\s*,\s*(?:Austria|Österreich|Osterreich)\b', re.IGNORECASE)

# Portugal
PATTERN_PT_1 = re.compile(r',\s*([A-Z][a-zãáàçéêíóôõú]+(?:\s+[A-Z][a-zãáàçéêíóôõú]+)*)\s+\d{4}-\d{3}\s*,?\s*(?:Portugal)', re.IGNORECASE)
PATTERN_PT_2 = re.compile(r',\s*([A-Z][a-zãáàçéêíóôõú]+(?:\s+[A-Z][a-zãáàçéêíóôõú]+)*)\s*,\s*Portugal\b', re.IGNORECASE)

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_europe_city(text, country, is_valid_city):

    if country == "UK":
        match = PATTERN_UK_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_UK_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_UK_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 3:
                return city


    elif country == "Germany":
        match = PATTERN_GERMANY_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_GERMANY_2.search(text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if is_valid_city(city) and city.lower() != state.lower():
                return city

        match = PATTERN_GERMANY_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "France":
        match = PATTERN_FRANCE_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_FRANCE_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Italy":
        match = PATTERN_ITALY_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_ITALY_2.search(text)
        if match:
            city = match.group(1).strip()
            region = match.group(2).strip()
            if is_valid_city(city) and city.lower() != region.lower():
                return city

        match = PATTERN_ITALY_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Spain":
        match = PATTERN_SPAIN_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_SPAIN_2.search(text)
        if match:
            city = match.group(1).strip()
            region = match.group(2).strip()
            if is_valid_city(city) and city.lower() != region.lower():
                return city

        match = PATTERN_SPAIN_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Netherlands":
        match = PATTERN_NL_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_NL_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Switzerland":
        match = PATTERN_CH_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_CH_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Sweden":
        match = PATTERN_SE_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_SE_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Belgium":
        match = PATTERN_BE_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_BE_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Austria":
        match = PATTERN_AT_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_AT_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Portugal":
        match = PATTERN_PT_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_PT_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city

    return ""
