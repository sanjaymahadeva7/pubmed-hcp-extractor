import re

# ============================================================
# COUNTRY DATA — Asia
# ============================================================

INDIAN_STATES = (
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',

    # Union Territories
    'Delhi', 'National Capital Territory of Delhi',
    'Puducherry', 'Pondicherry',
    'Chandigarh',
    'Jammu and Kashmir', 'Jammu & Kashmir',
    'Ladakh',
    'Andaman and Nicobar Islands', 'Andaman & Nicobar',
    'Dadra and Nagar Haveli', 'Daman and Diu',
    'Dadra & Nagar Haveli and Daman & Diu',
    'Lakshadweep'
)


CHINESE_PROVINCES = (
    'Anhui',
    'Beijing', 'Beijing Municipality',
    'Chongqing', 'Chongqing Municipality',
    'Fujian',
    'Gansu',
    'Guangdong',
    'Guangxi', 'Guangxi Zhuang Autonomous Region',
    'Guizhou',
    'Hainan',
    'Hebei',
    'Heilongjiang',
    'Henan',
    'Hubei',
    'Hunan',
    'Inner Mongolia', 'Inner Mongolia Autonomous Region',
    'Jiangsu',
    'Jiangxi',
    'Jilin',
    'Liaoning',
    'Ningxia', 'Ningxia Hui Autonomous Region',
    'Qinghai',
    'Shaanxi',
    'Shandong',
    'Shanghai', 'Shanghai Municipality',
    'Shanxi',
    'Sichuan',
    'Tianjin', 'Tianjin Municipality',
    'Tibet', 'Tibet Autonomous Region',
    'Xinjiang', 'Xinjiang Uyghur Autonomous Region',
    'Yunnan',
    'Zhejiang',

    # Special Administrative Regions
    'Hong Kong', 'Hong Kong SAR',
    'Macau', 'Macao', 'Macau SAR'
)


# ============================================================
# REGEX
# ============================================================

INDIAN_STATES_PATTERN = '|'.join(re.escape(state) for state in INDIAN_STATES)
CHINESE_PROVINCES_PATTERN = '|'.join(re.escape(prov) for prov in CHINESE_PROVINCES)

# India
PATTERN_INDIA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{6}\s*,?\s*India', re.IGNORECASE)
PATTERN_INDIA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + INDIAN_STATES_PATTERN + r')', re.IGNORECASE)
PATTERN_INDIA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*India\b', re.IGNORECASE)

# China
PATTERN_CHINA_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{6}\s*,?\s*(?:China|P\.?R\.? China)', re.IGNORECASE)
PATTERN_CHINA_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(' + CHINESE_PROVINCES_PATTERN + r')', re.IGNORECASE)
PATTERN_CHINA_3 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*(?:China|P\.?R\.? China)\b', re.IGNORECASE)

# Japan
PATTERN_JAPAN_1 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d{3}-\d{4}\s*,?\s*Japan', re.IGNORECASE)
PATTERN_JAPAN_2 = re.compile(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*Japan\b', re.IGNORECASE)

# Turkey
PATTERN_TR_1 = re.compile(r',\s*([A-Z][a-zğüşöçİı]+(?:\s+[A-Z][a-zğüşöçİı]+)*)\s+\d{5}\s*,?\s*(?:Turkey|Türkiye|Turkiye)', re.IGNORECASE)
PATTERN_TR_2 = re.compile(r',\s*([A-Z][a-zğüşöçİı]+(?:\s+[A-Z][a-zğüşöçİı]+)*)\s*,\s*(?:Turkey|Türkiye|Turkiye)\b', re.IGNORECASE)

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_asia_city(text, country, is_valid_city):

    if country == "India":
        match = PATTERN_INDIA_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_INDIA_2.search(text)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            if is_valid_city(city) and city.lower() != state.lower():
                return city

        match = PATTERN_INDIA_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 3:
                return city


    elif country == "China":
        match = PATTERN_CHINA_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_CHINA_2.search(text)
        if match:
            city = match.group(1).strip()
            province = match.group(2).strip()
            if is_valid_city(city) and city.lower() != province.lower():
                return city

        match = PATTERN_CHINA_3.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 3:
                return city


    elif country == "Japan":
        match = PATTERN_JAPAN_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_JAPAN_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city


    elif country == "Turkey":
        match = PATTERN_TR_1.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city):
                return city

        match = PATTERN_TR_2.search(text)
        if match:
            city = match.group(1).strip()
            if is_valid_city(city) and len(city.split()) <= 2:
                return city

    return ""
