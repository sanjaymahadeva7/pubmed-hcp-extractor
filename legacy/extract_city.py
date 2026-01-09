import re

# ============================================================
# MODULE-LEVEL CONSTANTS (created once at import time)
# ============================================================

# Convert to frozenset for O(1) lookup
NON_CITY_TERMS = frozenset([
    'university', 'college', 'hospital', 'medical', 'center', 'centre',
    'school', 'institute', 'department', 'division', 'health', 'system',
    'clinic', 'laboratory', 'research', 'sciences', 'medicine', 'care',
    'faculty', 'academy', 'foundation', 'national', 'international',
    'general', 'memorial', 'regional', 'district', 'public', 'private', 'gedic'
])

STATE_ABBREVIATIONS = frozenset([
    # USA states
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC',
    # Canadian provinces
    'AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT',
    # Australian states
    'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT',
    # Brazilian states
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
    # Indian states
    'AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JH',
    'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OD', 'PB',
    'RJ', 'SK', 'TN', 'TS', 'TR', 'UP', 'UK', 'WB',
    # Mexican states
    'AGS', 'BC', 'BCS', 'CAMP', 'CHIS', 'CHIH', 'COAH', 'COL', 'DF',
    'DGO', 'GTO', 'GRO', 'HGO', 'JAL', 'MEX', 'MICH', 'MOR', 'NAY',
    'NL', 'OAX', 'PUE', 'QRO', 'QROO', 'SLP', 'SIN', 'SON', 'TAB',
    'TAMPS', 'TLAX', 'VER', 'YUC', 'ZAC'
])

INSTITUTIONAL_KEYWORDS = frozenset([
    # English
    'hospital', 'university', 'college', 'institute', 'center', 'centre',
    'clinic', 'laboratory', 'school', 'department', 'faculty', 'academy',
    'foundation', 'ministry', 'government', 'agency', 'authority',
    'commission', 'bureau', 'office', 'service', 'council',
    'medical center', 'medical centre', 'health system', 'health center',
    'research center', 'research centre', 'teaching hospital',
    'medical school', 'school of medicine', 'school of public health',
    # Spanish/Portuguese
    'universidad', 'universidade', 'instituto', 'centro',
    'clinica', 'clínica', 'escuela', 'facultad', 'ministerio',
    'fundación', 'fundacao', 'fundação', 'secretaría', 'secretaria',
    # French
    'hôpital', 'hopital', 'université', 'universite', 'institut',
    'clinique', 'école', 'ecole', 'faculté', 'faculte', 'ministère', 'ministere',
    # German
    'krankenhaus', 'klinikum', 'universität', 'universitaet', 'institut',
    'klinik', 'schule', 'fakultät', 'fakultaet', 'ministerium',
    # Italian
    'ospedale', 'università', 'universita', 'istituto', 'clinica',
    'scuola', 'facoltà', 'facolta', 'ministero',
    # Dutch
    'ziekenhuis', 'universiteit', 'instituut', 'kliniek', 'school',
    'faculteit', 'ministerie',
    # Common institutional words
    'medical', 'health', 'public health', 'clinical', 'national',
    'federal', 'state', 'regional', 'district', 'municipal',
    'sciences', 'science', 'research', 'studies', 'education'
])

KNOWN_CITIES = frozenset([
    # Brazil
    'rio de janeiro', 'sao paulo', 'são paulo', 'brasilia', 'brasília',
    'belo horizonte', 'salvador', 'fortaleza', 'recife', 'porto alegre',
    # Spain
    'santiago de compostela', 'alcalá de henares', 'alcala de henares',
    'jerez de la frontera', 'san sebastián', 'san sebastian',
    'alcázar de san juan', 'alcazar de san juan',
    # Mexico
    'ciudad de méxico', 'ciudad de mexico', 'valle de bravo',
])

INSTITUTIONAL_INDICATORS = frozenset([
    'university', 'universidad', 'universidade', 'università',
    'institute', 'instituto', 'istituto', 'instituut',
    'ministry', 'ministerio', 'ministério', 'ministero',
    'foundation', 'fundación', 'fundação', 'fondazione',
    'hospital', 'center', 'centre', 'centro',
    'college', 'school', 'faculty', 'department',
    'agency', 'authority', 'commission', 'government'
])

# ============================================================
# COUNTRY-SPECIFIC DATA (module level)
# ============================================================

US_STATES_ABBR = (
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
)

US_STATES_FULL = (
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia'
)

INDIAN_STATES = (
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi', 'Puducherry', 'Chandigarh', 'Jammu and Kashmir', 'Ladakh'
)

UK_COUNTRIES = ('England', 'Scotland', 'Wales', 'Northern Ireland')

CHINESE_PROVINCES = (
    'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi',
    'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan',
    'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia',
    'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin',
    'Tibet', 'Xinjiang', 'Yunnan', 'Zhejiang'
)

GERMAN_STATES = (
    'Baden-Württemberg', 'Baden-Wurttemberg', 'Bavaria', 'Bayern', 'Berlin',
    'Brandenburg', 'Bremen', 'Hamburg', 'Hesse', 'Hessen', 'Lower Saxony',
    'Niedersachsen', 'Mecklenburg-Vorpommern', 'Mecklenburg-Western Pomerania',
    'North Rhine-Westphalia', 'Nordrhein-Westfalen', 'Rhineland-Palatinate',
    'Rheinland-Pfalz', 'Saarland', 'Saxony', 'Sachsen', 'Saxony-Anhalt',
    'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thuringia', 'Thüringen', 'Thuringen'
)

CANADIAN_PROVINCES_FULL = (
    'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
    'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia',
    'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'
)

CANADIAN_PROVINCES_ABBR = ('AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT')

AUSTRALIAN_STATES_FULL = (
    'New South Wales', 'Victoria', 'Queensland', 'South Australia',
    'Western Australia', 'Tasmania', 'Northern Territory',
    'Australian Capital Territory'
)

AUSTRALIAN_STATES_ABBR = ('NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT')

BRAZILIAN_STATES_FULL = (
    'Acre', 'Alagoas', 'Amapá', 'Amapa', 'Amazonas', 'Bahia', 'Ceará', 'Ceara',
    'Distrito Federal', 'Espírito Santo', 'Espirito Santo', 'Goiás', 'Goias',
    'Maranhão', 'Maranhao', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais',
    'Pará', 'Para', 'Paraíba', 'Paraiba', 'Paraná', 'Parana', 'Pernambuco',
    'Piauí', 'Piaui', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul',
    'Rondônia', 'Rondonia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sao Paulo',
    'Sergipe', 'Tocantins'
)

BRAZILIAN_STATES_ABBR = (
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
)

ITALIAN_REGIONS = (
    'Lombardy', 'Lombardia', 'Lazio', 'Tuscany', 'Toscana',
    'Sicily', 'Sicilia', 'Veneto', 'Emilia-Romagna',
    'Piemonte', 'Piedmont', 'Liguria', 'Calabria',
    'Campania', 'Sardinia', 'Sardegna', 'Apulia', 'Puglia',
    'Friuli', 'Umbria', 'Marche', 'Abruzzo', 'Molise',
    'Basilicata', 'Trentino', "Valle d'Aosta"
)

SPANISH_REGIONS = (
    'Comunidad de Madrid', 'Madrid',
    'Catalonia', 'Catalunya', 'Cataluña',
    'Andalusia', 'Andalucía',
    'Valencian Community', 'Valencia', 'Comunidad Valenciana',
    'Basque Country', 'País Vasco', 'Euskadi',
    'Galicia', 'Castile and León', 'Castilla y León',
    'Castilla-La Mancha', 'Canary Islands', 'Islas Canarias',
    'Murcia', 'Aragon', 'Aragón', 'Extremadura',
    'Balearic Islands', 'Islas Baleares',
    'Asturias', 'Navarre', 'Navarra', 'Cantabria', 'La Rioja'
)

# ============================================================
# PRE-COMPILED REGEX PATTERNS (created once)
# ============================================================

# USA patterns
US_STATES_FULL_PATTERN = '|'.join(re.escape(state) for state in US_STATES_FULL)
US_STATES_ABBR_PATTERN = '|'.join(US_STATES_ABBR)

PATTERN_USA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z]{2}\s+\d{5}')
PATTERN_USA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + US_STATES_FULL_PATTERN + r')', re.IGNORECASE)
PATTERN_USA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + US_STATES_ABBR_PATTERN + r')\b')

# India patterns
INDIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in INDIAN_STATES)

PATTERN_INDIA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{6}\s*,?\s*India', re.IGNORECASE)
PATTERN_INDIA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + INDIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_INDIA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*India\b', re.IGNORECASE)

# UK patterns
UK_COUNTRIES_PATTERN = '|'.join(re.escape(c) for c in UK_COUNTRIES)

PATTERN_UK_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+[A-Z]{1,2}\d{1,2}\s*\d?[A-Z]{2}\s*,?\s*(?:UK|United Kingdom|England|Scotland|Wales)', re.IGNORECASE)
PATTERN_UK_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + UK_COUNTRIES_PATTERN + r')', re.IGNORECASE)
PATTERN_UK_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:UK|United Kingdom)\b', re.IGNORECASE)

# China patterns
CHINESE_PROVINCES_PATTERN = '|'.join(re.escape(prov) for prov in CHINESE_PROVINCES)

PATTERN_CHINA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{6}\s*,?\s*(?:China|P\.?R\.? China)', re.IGNORECASE)
PATTERN_CHINA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CHINESE_PROVINCES_PATTERN + r')', re.IGNORECASE)
PATTERN_CHINA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:China|P\.?R\.? China)\b', re.IGNORECASE)

# Japan patterns
PATTERN_JAPAN_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{3}-\d{4}\s*,?\s*Japan', re.IGNORECASE)
PATTERN_JAPAN_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Japan\b', re.IGNORECASE)

# Germany patterns
GERMAN_STATES_PATTERN = '|'.join(re.escape(state) for state in GERMAN_STATES)

PATTERN_GERMANY_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*Germany', re.IGNORECASE)
PATTERN_GERMANY_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + GERMAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_GERMANY_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Germany\b', re.IGNORECASE)

# France patterns
PATTERN_FRANCE_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*France', re.IGNORECASE)
PATTERN_FRANCE_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*France\b', re.IGNORECASE)

# Canada patterns
CANADIAN_PROVINCES_PATTERN = '|'.join(re.escape(prov) for prov in CANADIAN_PROVINCES_FULL)
CANADIAN_ABBR_PATTERN = '|'.join(CANADIAN_PROVINCES_ABBR)

PATTERN_CANADA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+[A-Z]\d[A-Z]\s*\d[A-Z]\d\s*,?\s*Canada', re.IGNORECASE)
PATTERN_CANADA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CANADIAN_PROVINCES_PATTERN + r')', re.IGNORECASE)
PATTERN_CANADA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CANADIAN_ABBR_PATTERN + r')\b')
PATTERN_CANADA_4 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Canada\b', re.IGNORECASE)

# Australia patterns
AUSTRALIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in AUSTRALIAN_STATES_FULL)
AUSTRALIAN_ABBR_PATTERN = '|'.join(AUSTRALIAN_STATES_ABBR)

PATTERN_AUSTRALIA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*,?\s*Australia', re.IGNORECASE)
PATTERN_AUSTRALIA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + AUSTRALIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_AUSTRALIA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + AUSTRALIAN_ABBR_PATTERN + r')\b')
PATTERN_AUSTRALIA_4 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Australia\b', re.IGNORECASE)

# Brazil patterns
BRAZILIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in BRAZILIAN_STATES_FULL)
BRAZILIAN_ABBR_PATTERN = '|'.join(BRAZILIAN_STATES_ABBR)

PATTERN_BRAZIL_1 = re.compile(r',\s*([A-Z][a-zé]+(?:\s+[A-Z][a-zé]+)*)\s+\d{5}-?\d{3}\s*,?\s*Braz[il]{2}', re.IGNORECASE)
PATTERN_BRAZIL_2 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Zd][a-zãáéíóúç]+)*)\s*,\s*(' + BRAZILIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_BRAZIL_3 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Z][a-zãáéíóúç]+)*)\s*,\s*(' + BRAZILIAN_ABBR_PATTERN + r')\b')
PATTERN_BRAZIL_4 = re.compile(r',\s*([A-Z][a-zãáéíóúç]+(?:\s+[A-Z][a-zãáéíóúç]+)*)\s*,\s*Braz[il]{2}\b', re.IGNORECASE)

# Italy patterns
ITALIAN_REGIONS_PATTERN = '|'.join(re.escape(region) for region in ITALIAN_REGIONS)

PATTERN_ITALY_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{5}\s*,?\s*(?:Italy|Italia)', re.IGNORECASE)
PATTERN_ITALY_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + ITALIAN_REGIONS_PATTERN + r')', re.IGNORECASE)
PATTERN_ITALY_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Italy|Italia)\b', re.IGNORECASE)

# Spain patterns
SPANISH_REGIONS_PATTERN = '|'.join(re.escape(region) for region in SPANISH_REGIONS)

PATTERN_SPAIN_1 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s+\d{5}\s*,?\s*(?:Spain|España)', re.IGNORECASE)
PATTERN_SPAIN_2 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s*,\s*(' + SPANISH_REGIONS_PATTERN + r')', re.IGNORECASE)
PATTERN_SPAIN_3 = re.compile(r',\s*([A-Z][a-zñáéíóúü]+(?:\s+[A-Z][a-zñáéíóúü]+)*)\s*,\s*(?:Spain|España)\b', re.IGNORECASE)

# Netherlands patterns
PATTERN_NL_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*[A-Z]{2}\s*,?\s*(?:Netherlands|Nederland)', re.IGNORECASE)
PATTERN_NL_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Netherlands|Nederland|The Netherlands)\b', re.IGNORECASE)

# Switzerland patterns
PATTERN_CH_1 = re.compile(r',\s*([A-Z][a-zü]+(?:\s+[A-Z][a-zü]+)*)\s+\d{4}\s*,?\s*(?:Switzerland|Schweiz|Suisse|Svizzera)', re.IGNORECASE)
PATTERN_CH_2 = re.compile(r',\s*([A-Z][a-zü]+(?:\s+[A-Z][a-zü]+)*)\s*,\s*(?:Switzerland|Schweiz|Suisse|Svizzera)\b', re.IGNORECASE)

# Sweden patterns
PATTERN_SE_1 = re.compile(r',\s*([A-Z][a-zåäö]+(?:\s+[A-Z][a-zåäö]+)*)\s+\d{3}\s*\d{2}\s*,?\s*(?:Sweden|Sverige)', re.IGNORECASE)
PATTERN_SE_2 = re.compile(r',\s*([A-Z][a-zåäö]+(?:\s+[A-Z][a-zåäö]+)*)\s*,\s*(?:Sweden|Sverige)\b', re.IGNORECASE)

# Belgium patterns
PATTERN_BE_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*,?\s*(?:Belgium|België|Belgique)', re.IGNORECASE)
PATTERN_BE_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:Belgium|België|Belgique)\b', re.IGNORECASE)

# Austria patterns
PATTERN_AT_1 = re.compile(r',\s*([A-Z][a-zöäü]+(?:\s+[A-Z][a-zöäü]+)*)\s+\d{4}\s*,?\s*(?:Austria|Österreich)', re.IGNORECASE)
PATTERN_AT_2 = re.compile(r',\s*([A-Z][a-zöäü]+(?:\s+[A-Z][a-zöäü]+)*)\s*,\s*(?:Austria|Österreich|Osterreich)\b', re.IGNORECASE)

# Portugal patterns
PATTERN_PT_1 = re.compile(r',\s*([A-Z][a-zãáàçéêíóôõú]+(?:\s+[A-Z][a-zãáàçéêíóôõú]+)*)\s+\d{4}-\d{3}\s*,?\s*(?:Portugal)', re.IGNORECASE)
PATTERN_PT_2 = re.compile(r',\s*([A-Z][a-zãáàçéêíóôõú]+(?:\s+[A-Z][a-zãáàçéêíóôõú]+)*)\s*,\s*Portugal\b', re.IGNORECASE)

# Mexico patterns
PATTERN_MX_1 = re.compile(r',\s*([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)\s+\d{5}\s*,?\s*(?:Mexico|México)', re.IGNORECASE)
PATTERN_MX_2 = re.compile(r',\s*([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)\s*,\s*(?:Mexico|México)\b', re.IGNORECASE)

# Turkey patterns
PATTERN_TR_1 = re.compile(r',\s*([A-Z][a-zğüşöçİı]+(?:\s+[A-Z][a-zğüşöçİı]+)*)\s+\d{5}\s*,?\s*(?:Turkey|Türkiye|Turkiye)', re.IGNORECASE)
PATTERN_TR_2 = re.compile(r',\s*([A-Z][a-zğüşöçİı]+(?:\s+[A-Z][a-zğüşöçİı]+)*)\s*,\s*(?:Turkey|Türkiye|Turkiye)\b', re.IGNORECASE)


# ============================================================
# HELPER FUNCTION (module level - not recreated per call)
# ============================================================

def _is_valid_city(city_name):
    """Check if the extracted text is a valid city name"""
    if not city_name:
        return False
    
    city_clean = city_name.strip()
    city_lower = city_clean.lower()
    
    # If it's a known city, always accept
    if city_lower in KNOWN_CITIES:
        return True
    
    # Check if ANY institutional keyword appears in the text
    for keyword in INSTITUTIONAL_KEYWORDS:
        if keyword in city_lower:
            return False
    
    # Skip if it's in non-city terms (exact match)
    if city_lower in NON_CITY_TERMS:
        return False
    
    # Skip if it's a state abbreviation (2-4 letter uppercase)
    if city_clean.upper() in STATE_ABBREVIATIONS:
        return False
    
    # Skip if it's too short (likely abbreviation)
    if len(city_clean) <= 2:
        return False
    
    # Skip if all uppercase and short (likely abbreviation)
    if city_clean.isupper() and len(city_clean) <= 4:
        return False
    
    # Skip if contains mostly numbers
    if sum(c.isdigit() for c in city_clean) > len(city_clean) / 2:
        return False
    
    # Check for institutional patterns with "of/de/da"
    if ' of ' in city_lower or ' de ' in city_lower or ' da ' in city_lower:
        # Only reject if it ALSO contains institutional keywords
        for indicator in INSTITUTIONAL_INDICATORS:
            if indicator in city_lower:
                return False
    
    return True


# ============================================================
# MAIN FUNCTION
# ============================================================

def extract_city(affiliation_text, country):
    """
    Extract city from affiliation text - COUNTRY-SPECIFIC PATTERNS
    Uses specific patterns for each major country for better accuracy
    
    Args:
        affiliation_text: Full affiliation string
        country: Country code/name
    
    Returns:
        City name or empty string
    """
    if not affiliation_text or not country:
        return ''
    
    # ===========================
    # USA PATTERNS
    # ===========================
    if country == "US":
        match = PATTERN_USA_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_USA_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != state.lower():
                return city
        
        match = PATTERN_USA_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 3:
                return city
    
    # ===========================
    # INDIA PATTERNS
    # ===========================
    elif country == "India":
        match = PATTERN_INDIA_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_INDIA_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != state.lower():
                return city
        
        match = PATTERN_INDIA_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 3:
                return city
    
    # ===========================
    # UK PATTERNS
    # ===========================
    elif country == "UK":
        match = PATTERN_UK_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_UK_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_UK_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 3:
                return city
    
    # ===========================
    # CHINA PATTERNS
    # ===========================
    elif country == "China":
        match = PATTERN_CHINA_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_CHINA_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            province = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != province.lower():
                return city
        
        match = PATTERN_CHINA_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 3:
                return city
    
    # ===========================
    # JAPAN PATTERNS
    # ===========================
    elif country == "Japan":
        match = PATTERN_JAPAN_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_JAPAN_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # GERMANY PATTERNS
    # ===========================
    elif country == "Germany":
        match = PATTERN_GERMANY_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_GERMANY_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != state.lower():
                return city
        
        match = PATTERN_GERMANY_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # FRANCE PATTERNS
    # ===========================
    elif country == "France":
        match = PATTERN_FRANCE_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_FRANCE_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # CANADA PATTERNS
    # ===========================
    elif country == "Canada":
        match = PATTERN_CANADA_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_CANADA_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            province = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != province.lower():
                return city
        
        match = PATTERN_CANADA_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_CANADA_4.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # AUSTRALIA PATTERNS
    # ===========================
    elif country == "Australia":
        match = PATTERN_AUSTRALIA_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_AUSTRALIA_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != state.lower():
                return city
        
        match = PATTERN_AUSTRALIA_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_AUSTRALIA_4.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # BRAZIL PATTERNS
    # ===========================
    elif country == "Brazil":
        match = PATTERN_BRAZIL_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_BRAZIL_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != state.lower():
                return city
        
        match = PATTERN_BRAZIL_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_BRAZIL_4.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 3:
                return city
    
    # ===========================
    # ITALY PATTERNS
    # ===========================
    elif country == "Italy":
        match = PATTERN_ITALY_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_ITALY_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            region = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != region.lower():
                return city
        
        match = PATTERN_ITALY_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # SPAIN PATTERNS
    # ===========================
    elif country == "Spain":
        match = PATTERN_SPAIN_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_SPAIN_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            region = match.group(2).strip()
            if _is_valid_city(city) and city.lower() != region.lower():
                return city
        
        match = PATTERN_SPAIN_3.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # NETHERLANDS PATTERNS
    # ===========================
    elif country == "Netherlands":
        match = PATTERN_NL_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_NL_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # SWITZERLAND PATTERNS
    # ===========================
    elif country == "Switzerland":
        match = PATTERN_CH_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_CH_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # SWEDEN PATTERNS
    # ===========================
    elif country == "Sweden":
        match = PATTERN_SE_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_SE_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # BELGIUM PATTERNS
    # ===========================
    elif country == "Belgium":
        match = PATTERN_BE_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_BE_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # AUSTRIA PATTERNS
    # ===========================
    elif country == "Austria":
        match = PATTERN_AT_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_AT_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # PORTUGAL PATTERNS
    # ===========================
    elif country == "Portugal":
        match = PATTERN_PT_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_PT_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # MEXICO PATTERNS
    # ===========================
    elif country == "Mexico":
        match = PATTERN_MX_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_MX_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # TURKEY PATTERNS
    # ===========================
    elif country == "Turkey":
        match = PATTERN_TR_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        match = PATTERN_TR_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    # ===========================
    # FALLBACK FOR REMAINING COUNTRIES
    # ===========================
    else:
        # Generic pattern: City before country name
        pattern_generic_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4,6}\s*,?\s*' + re.escape(country) + r'\b', re.IGNORECASE)
        match = pattern_generic_1.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city):
                return city
        
        pattern_generic_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*' + re.escape(country) + r'\b', re.IGNORECASE)
        match = pattern_generic_2.search(affiliation_text)
        if match:
            city = match.group(1).strip()
            if _is_valid_city(city) and len(city.split()) <= 2:
                return city
    
    return ''