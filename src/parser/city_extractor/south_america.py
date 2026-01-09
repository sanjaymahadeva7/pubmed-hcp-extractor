import re

# ============================================================
# COUNTRY DATA — South America
# ============================================================

BRAZILIAN_STATES_FULL = (
    'Acre',
    'Alagoas',
    'Amapá', 'Amapa',
    'Amazonas',
    'Bahia',
    'Ceará', 'Ceara',
    'Distrito Federal', 'Federal District',
    'Espírito Santo', 'Espirito Santo',
    'Goiás', 'Goias',
    'Maranhão', 'Maranhao',
    'Mato Grosso',
    'Mato Grosso do Sul',
    'Minas Gerais',
    'Pará', 'Para',
    'Paraíba', 'Paraiba',
    'Paraná', 'Parana',
    'Pernambuco',
    'Piauí', 'Piaui',
    'Rio de Janeiro',
    'Rio Grande do Norte',
    'Rio Grande do Sul',
    'Rondônia', 'Rondonia',
    'Roraima',
    'Santa Catarina',
    'São Paulo', 'Sao Paulo',
    'Sergipe',
    'Tocantins'
)

BRAZILIAN_STATES_ABBR = (
    'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA',
    'MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN',
    'RS','RO','RR','SC','SP','SE','TO'
)


# ============================================================
# REGEX
# ============================================================

BRAZILIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in BRAZILIAN_STATES_FULL)
BRAZILIAN_ABBR_PATTERN = '|'.join(BRAZILIAN_STATES_ABBR)

PATTERN_BRAZIL_1 = re.compile(r',\s*([A-Z][a-zé]+(?:\s+[A-Z][a-zé]+)*)\s+\d{5}-?\d{3}\s*,?\s*Braz[il]{2}', re.IGNORECASE)
PATTERN_BRAZIL_2 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Zd][a-zãáéíóúç]+)*)\s*,\s*(' + BRAZILIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_BRAZIL_3 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Z][a-zãáéíóúç]+)*)\s*,\s*(' + BRAZILIAN_ABBR_PATTERN + r')\b')
PATTERN_BRAZIL_4 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Z][a-zãáéíóúç]+)*)\s*,\s*Braz[il]{2}\b', re.IGNORECASE)

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_south_america_city(text, country, is_valid_city):

    if country == "Brazil":
        match = PATTERN_BRAZIL_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_BRAZIL_2.search(text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if is_valid_city(city) and city.lower() != state.lower():
                return city

        match = PATTERN_BRAZIL_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_BRAZIL_4.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 3:
                return city

    return ""
