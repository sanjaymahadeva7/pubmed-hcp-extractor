import re

# ============================================================
# COUNTRY DATA — North America
# ============================================================

US_STATES_ABBR = (
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
    'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC',
    'D.C.'
)

US_STATES_FULL = (
    'Alabama','Alaska','Arizona','Arkansas','California','Colorado',
    'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',
    'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
    'Maine','Maryland','Massachusetts','Michigan','Minnesota',
    'Mississippi','Missouri','Montana','Nebraska','Nevada',
    'New Hampshire','New Jersey','New Mexico','New York',
    'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
    'Pennsylvania','Rhode Island','South Carolina','South Dakota',
    'Tennessee','Texas','Utah','Vermont','Virginia','Washington',
    'West Virginia','Wisconsin','Wyoming',
    'District of Columbia','Washington DC','Washington D.C.'
)


CANADIAN_PROVINCES_FULL = (
    'Alberta',
    'British Columbia', 'BC',
    'Manitoba',
    'New Brunswick',
    'Newfoundland and Labrador', 'Newfoundland & Labrador',
    'Northwest Territories',
    'Nova Scotia',
    'Nunavut',
    'Ontario',
    'Prince Edward Island', 'PEI',
    'Quebec', 'Québec',
    'Saskatchewan',
    'Yukon'
)

CANADIAN_PROVINCES_ABBR = (
    'AB','BC','MB','NB','NL','NT','NS','NU','ON','PE','QC','SK','YT','PEI'
)


# ============================================================
# PRECOMPILED REGEX
# ============================================================

US_STATES_FULL_PATTERN = '|'.join(re.escape(state) for state in US_STATES_FULL)
US_STATES_ABBR_PATTERN = '|'.join(US_STATES_ABBR)

CANADIAN_PROVINCES_PATTERN = '|'.join(re.escape(p) for p in CANADIAN_PROVINCES_FULL)
CANADIAN_ABBR_PATTERN = '|'.join(CANADIAN_PROVINCES_ABBR)

# USA
PATTERN_USA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z]{2}\s+\d{5}')
PATTERN_USA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + US_STATES_FULL_PATTERN + r')', re.IGNORECASE)
PATTERN_USA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + US_STATES_ABBR_PATTERN + r')\b')

# Canada
PATTERN_CANADA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+[A-Z]\d[A-Z]\s*\d[A-Z]\d\s*,?\s*Canada', re.IGNORECASE)
PATTERN_CANADA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CANADIAN_PROVINCES_PATTERN + r')', re.IGNORECASE)
PATTERN_CANADA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CANADIAN_ABBR_PATTERN + r')\b')
PATTERN_CANADA_4 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Canada\b', re.IGNORECASE)

# Mexico
PATTERN_MX_1 = re.compile(r',\s*([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)\s+\d{5}\s*,?\s*(?:Mexico|México)', re.IGNORECASE)
PATTERN_MX_2 = re.compile(r',\s*([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)\s*,\s*(?:Mexico|México)\b', re.IGNORECASE)

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_north_america_city(text, country, is_valid_city):

    if country == "US":
        match = PATTERN_USA_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_USA_2.search(text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if is_valid_city(city) and city.lower() != state.lower():
                return city

        match = PATTERN_USA_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 3:
                return city


    elif country == "Canada":
        match = PATTERN_CANADA_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_CANADA_2.search(text)
        if match:
            city = match.group(1).strip()
            province = match.group(2).strip()
            if is_valid_city(city) and city.lower() != province.lower():
                return city

        match = PATTERN_CANADA_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_CANADA_4.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Mexico":
        match = PATTERN_MX_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_MX_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city

    return ""
