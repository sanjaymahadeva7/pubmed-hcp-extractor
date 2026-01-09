# Convert to frozenset for O(1) lookup
NON_CITY_TERMS = frozenset([
    'university','college','hospital','medical','center','centre',
    'school','institute','department','division','health','system',
    'clinic','laboratory','research','sciences','medicine','care',
    'faculty','academy','foundation','national','international',
    'general','memorial','regional','district','public','private','gedic',
    'street','st','road','rd','avenue','ave','lane','ln',
    'boulevard','blvd','drive','dr','highway','hwy',
    'block','sector','phase','area','zone','park',
    'downtown','uptown','suburb',
    'north','south','east','west','central',
    'upper','lower','old','new','greater','metro','metropolitan'
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
    'agency', 'authority', 'commission', 'government','hospital',
    'clinic', 'medical', 'university', 'college',
    'health', 'research', 'institute', 'center', 'centre'

])

def is_valid_city(city_name):
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