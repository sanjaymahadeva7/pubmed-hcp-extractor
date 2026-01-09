import re

# ============================================================
# INDIA
# ============================================================

INDIA_STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
    'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
    'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
    'Mizoram', 'Nagaland', 'Odisha', 'Orissa',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
    'West Bengal',
    # Union Territories
    'Delhi', 'New Delhi', 'Chandigarh', 'Puducherry', 'Pondicherry',
    'Jammu and Kashmir', 'J&K', 'Ladakh',
    'Andaman and Nicobar', 'Lakshadweep',
    'Dadra and Nagar Haveli', 'Daman and Diu'
]

# ============================================================
# CHINA
# ============================================================

CHINA_REGIONS = [
    'Beijing', 'Shanghai', 'Tianjin', 'Chongqing',
    'Guangdong', 'Zhejiang', 'Jiangsu', 'Shandong',
    'Sichuan', 'Hubei', 'Hunan', 'Fujian',
    'Anhui', 'Henan', 'Hebei', 'Shaanxi', 'Shanxi',
    'Liaoning', 'Yunnan', 'Guizhou', 'Guangxi',
    'Jiangxi', 'Jilin', 'Heilongjiang', 'Gansu',
    'Inner Mongolia', 'Ningxia', 'Qinghai', 'Xinjiang',
    'Tibet', 'Xizang',
    'Hong Kong', 'Macau', 'Macao'
]

# ============================================================
# JAPAN
# ============================================================

JAPAN_PREFECTURES = [
    'Tokyo', 'Osaka', 'Kyoto', 'Kanagawa', 'Aichi',
    'Hokkaido', 'Fukuoka', 'Saitama', 'Chiba',
    'Hiroshima', 'Miyagi', 'Hyogo', 'Shizuoka',
    'Nagano', 'Okinawa', 'Ibaraki', 'Gunma',
    'Tochigi', 'Niigata', 'Fukushima', 'Yamanashi',
    'Nagasaki', 'Kumamoto', 'Kagoshima', 'Ishikawa'
]

# ============================================================
# SOUTH KOREA
# ============================================================

KOREA_REGIONS = [
    'Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon',
    'Gwangju', 'Ulsan', 'Sejong',
    'Gyeonggi', 'Gyeonggi-do',
    'Gangwon', 'Gangwon-do',
    'North Chungcheong', 'Chungcheongbuk-do',
    'South Chungcheong', 'Chungcheongnam-do',
    'North Jeolla', 'Jeollabuk-do',
    'South Jeolla', 'Jeollanam-do',
    'North Gyeongsang', 'Gyeongsangbuk-do',
    'South Gyeongsang', 'Gyeongsangnam-do',
    'Jeju', 'Jeju-do'
]

# ============================================================
# TURKEY
# ============================================================

TURKEY_PROVINCES = [
    'Istanbul', 'İstanbul', 'Ankara', 'Izmir', 'İzmir',
    'Bursa', 'Antalya', 'Adana', 'Gaziantep', 'Konya',
    'Kocaeli', 'Mersin', 'İçel', 'Kayseri', 'Eskişehir', 'Eskisehir',
    'Diyarbakır', 'Diyarbakir', 'Samsun', 'Denizli',
    'Şanlıurfa', 'Sanliurfa', 'Trabzon', 'Van', 'Malatya', 'Erzurum'
]

# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_asia_state(text, country):

    if country == "India":
        for state in INDIA_STATES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "China":
        for state in CHINA_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Japan":
        for state in JAPAN_PREFECTURES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "South Korea":
        for state in KOREA_REGIONS:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    elif country == "Turkey":
        for state in TURKEY_PROVINCES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    return ""
