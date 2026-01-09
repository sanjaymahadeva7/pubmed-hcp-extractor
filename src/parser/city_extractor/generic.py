import re

# ============================================================
# GENERIC FALLBACK REGEX
# ============================================================

def extract_generic_city(text, country, is_valid_city):

    # City + postal + country
    pattern_generic_1 = re.compile(
        r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{4,6}\s*,?\s*' + re.escape(country) + r'\b',
        re.IGNORECASE
    )

    match = pattern_generic_1.search(text)
    if match:
        city = match.group(1).strip()
        if is_valid_city(city):
            return city

    # City, Country
    pattern_generic_2 = re.compile(
        r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*' + re.escape(country) + r'\b',
        re.IGNORECASE
    )

    match = pattern_generic_2.search(text)
    if match:
        city = match.group(1).strip()
        if is_valid_city(city) and len(city.split()) <= 2:
            return city

    return ""
