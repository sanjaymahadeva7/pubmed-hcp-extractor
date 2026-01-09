import re

# ============================================================
# USA
# ============================================================

US_STATES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}


# ============================================================
# CANADA
# ============================================================

CANADA_PROVINCES = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
}

CANADA_FULL_NAMES = [
    'Ontario', 'Quebec', 'Québec',
    'British Columbia', 'Alberta', 'Manitoba',
    'Saskatchewan', 'Nova Scotia', 'New Brunswick',
    'Newfoundland and Labrador', 'Newfoundland',
    'Prince Edward Island', 'PEI',
    'Northwest Territories', 'Nunavut', 'Yukon'
]


# ============================================================
# MEXICO
# ============================================================

MEXICO_STATES = [
    'Mexico City', 'Ciudad de México', 'CDMX',
    'Jalisco', 'Nuevo León', 'Nuevo Leon',
    'Puebla', 'Guanajuato', 'Yucatán', 'Yucatan',
    'Veracruz', 'Chiapas', 'Oaxaca', 'Michoacán', 'Michoacan',
    'Guerrero', 'Tamaulipas', 'Sinaloa', 'Coahuila', 'Chihuahua',
    'Sonora', 'San Luis Potosí', 'San Luis Potosi', 'Hidalgo',
    'Tabasco', 'Querétaro', 'Queretaro', 'Morelos', 'Durango',
    'Zacatecas', 'Quintana Roo', 'Aguascalientes', 'Tlaxcala',
    'Nayarit', 'Campeche', 'Baja California', 'Baja California Sur',
    'Colima'
]


# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_na_state(text, country):

    # ---------- USA ----------
    if country == "US":
        for abbr, full in US_STATES.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', text):
                return full

        for full in US_STATES.values():
            if re.search(r'\b' + re.escape(full) + r'\b', text, re.IGNORECASE):
                return full


    # ---------- CANADA ----------
    elif country == "Canada":
        for abbr, full in CANADA_PROVINCES.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', text):
                return full

        for prov in CANADA_FULL_NAMES:
            if re.search(r'\b' + re.escape(prov) + r'\b', text, re.IGNORECASE):
                return prov


    # ---------- MEXICO ----------
    elif country == "Mexico":
        for state in MEXICO_STATES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    return ""
