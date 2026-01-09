import re

# ============================================================
# COUNTRY DATA — Oceania
# ============================================================

AUSTRALIAN_STATES_FULL = (
    'New South Wales', 'NSW',
    'Victoria', 'VIC',
    'Queensland', 'QLD',
    'South Australia', 'SA',
    'Western Australia', 'WA',
    'Tasmania', 'TAS',
    'Northern Territory', 'NT',
    'Australian Capital Territory', 'ACT',
    'Jervis Bay Territory'
)

AUSTRALIAN_STATES_ABBR = (
    'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT'
)


# ============================================================
# REGEX
# ============================================================

AUSTRALIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in AUSTRALIAN_STATES_FULL)
AUSTRALIAN_ABBR_PATTERN = '|'.join(AUSTRALIAN_STATES_ABBR)

PATTERN_AUSTRALIA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4}\s*,?\s*Australia', re.IGNORECASE)
PATTERN_AUSTRALIA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + AUSTRALIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_AUSTRALIA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + AUSTRALIAN_ABBR_PATTERN + r')\b')
PATTERN_AUSTRALIA_4 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Australia\b', re.IGNORECASE)

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_oceania_city(text, country, is_valid_city):

    if country == "Australia":
        match = PATTERN_AUSTRALIA_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_AUSTRALIA_2.search(text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if is_valid_city(city) and city.lower() != state.lower():
                return city

        match = PATTERN_AUSTRALIA_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_AUSTRALIA_4.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city

    return ""
