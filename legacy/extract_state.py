import re

def extract_state(affiliation_text, country):
    """
    Extract State / Region from affiliation text
    Supports multiple countries worldwide
    
    Args:
        affiliation_text: The PRIMARY affiliation text (already filtered)
        country: The country already extracted
    
    Returns:
        State/Region name or empty string
    """
    if not affiliation_text or not country:
        return ''

    
    # ------------------ USA ------------------
    if country == "US":
        us_states = {
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
        
        # Check abbreviations first
        for abbr, full_name in us_states.items():
            pattern = r'\b' + re.escape(abbr) + r'\b'
            if re.search(pattern, affiliation_text):
                return full_name
        
        # Then check full names
        for full_name in us_states.values():
            pattern = r'\b' + re.escape(full_name) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return full_name

    # ------------------ AUSTRALIA ------------------
    elif country == "Australia":
        au_states = {
            'WA': 'Western Australia',
            'NSW': 'New South Wales',
            'VIC': 'Victoria',
            'QLD': 'Queensland',
            'SA': 'South Australia',
            'TAS': 'Tasmania',
            'ACT': 'Australian Capital Territory',
            'NT': 'Northern Territory'
        }
        
        # Check abbreviations first
        for abbr, full in au_states.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', affiliation_text):
                return full
        
        # Then check full names
        for full in au_states.values():
            if re.search(r'\b' + re.escape(full) + r'\b', affiliation_text, re.IGNORECASE):
                return full

    # ------------------ CANADA ------------------
    elif country == "Canada":
        canada_provinces = {
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
        
        # Check abbreviations first
        for abbr, full in canada_provinces.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', affiliation_text):
                return full
        
        # Then check full names (add variants)
        full_names = [
            'Ontario', 'Quebec', 'Québec',
            'British Columbia', 'Alberta', 'Manitoba',
            'Saskatchewan', 'Nova Scotia', 'New Brunswick',
            'Newfoundland and Labrador', 'Newfoundland',
            'Prince Edward Island', 'PEI',
            'Northwest Territories', 'Nunavut', 'Yukon'
        ]
        
        for province in full_names:
            if re.search(r'\b' + re.escape(province) + r'\b', affiliation_text, re.IGNORECASE):
                return province

    # ------------------ INDIA ------------------
    elif country == "India":
        india_states = [
            # All 28 states
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
            'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
            'Mizoram', 'Nagaland', 'Odisha', 'Orissa',  # Orissa is old name
            'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
            'West Bengal',
            # Union Territories
            'Delhi', 'New Delhi', 'Chandigarh', 'Puducherry', 'Pondicherry',
            'Jammu and Kashmir', 'J&K', 'Ladakh',
            'Andaman and Nicobar', 'Lakshadweep', 'Dadra and Nagar Haveli',
            'Daman and Diu'
        ]
        
        for state in india_states:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ CHINA ------------------
    elif country == "China":
        china_regions = [
            # Major municipalities
            'Beijing', 'Shanghai', 'Tianjin', 'Chongqing',
            # Provinces
            'Guangdong', 'Zhejiang', 'Jiangsu', 'Shandong',
            'Sichuan', 'Hubei', 'Hunan', 'Fujian',
            'Anhui', 'Henan', 'Hebei', 'Shaanxi', 'Shanxi',
            'Liaoning', 'Yunnan', 'Guizhou', 'Guangxi',
            'Jiangxi', 'Jilin', 'Heilongjiang', 'Gansu',
            'Inner Mongolia', 'Ningxia', 'Qinghai', 'Xinjiang',
            'Tibet', 'Xizang',
            # SARs
            'Hong Kong', 'Macau', 'Macao'
        ]
        
        for state in china_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ JAPAN ------------------
    elif country == "Japan":
        japan_regions = [
            # Major prefectures
            'Tokyo', 'Osaka', 'Kyoto', 'Kanagawa', 'Aichi',
            'Hokkaido', 'Fukuoka', 'Saitama', 'Chiba',
            'Hiroshima', 'Miyagi', 'Hyogo', 'Shizuoka',
            'Nagano', 'Okinawa', 'Ibaraki', 'Gunma',
            'Tochigi', 'Niigata', 'Fukushima', 'Yamanashi',
            'Nagasaki', 'Kumamoto', 'Kagoshima', 'Ishikawa'
        ]
        
        for state in japan_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ GERMANY ------------------
    elif country == "Germany":
        germany_states = [
            'Bavaria', 'Bayern', 'Berlin', 'Brandenburg', 'Hamburg', 'Hesse', 'Hessen',
            'Saxony', 'Sachsen', 'Saxony-Anhalt', 'North Rhine-Westphalia', 'NRW',
            'Lower Saxony', 'Niedersachsen', 'Mecklenburg-Western Pomerania',
            'Rhineland-Palatinate', 'Thuringia', 'Thueringen', 'Schleswig-Holstein',
            'Saarland', 'Bremen', 'Baden-Württemberg', 'Baden Wurttemberg'
        ]
        
        for state in germany_states:
            pattern = r'\b' + re.escape(state) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return state

    # ------------------ UK ------------------
    elif country == "UK":
        uk_regions = [
            # Countries
            'England', 'Scotland', 'Wales', 'Northern Ireland',
            # Major English regions
            'Greater London', 'London',
            'South East England', 'South West England', 
            'East of England', 'West Midlands', 'East Midlands',
            'Yorkshire and the Humber', 'Yorkshire',
            'North West England', 'North East England',
            # Major counties
            'Kent', 'Surrey', 'Essex', 'Hampshire', 'Hertfordshire',
            'Lancashire', 'Oxfordshire', 'Cambridgeshire', 'Berkshire',
            'Buckinghamshire', 'Devon', 'Cornwall', 'Somerset', 'Dorset',
            'Sussex', 'Suffolk', 'Norfolk', 'Leicestershire', 'Nottinghamshire',
            'Derbyshire', 'Staffordshire', 'Warwickshire', 'Worcestershire',
            'Gloucestershire', 'Wiltshire', 'Northamptonshire',
            # Scottish regions
            'Highland', 'Lothian', 'Strathclyde', 'Fife', 'Grampian',
            # Welsh regions
            'Gwynedd', 'Powys', 'Dyfed', 'Clwyd', 'Glamorgan',
            # City counties
            'Greater Manchester', 'Merseyside', 'Tyne and Wear',
            'West Yorkshire', 'South Yorkshire'
        ]
        
        for state in uk_regions:
            pattern = r'\b' + re.escape(state) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return state

    # ------------------ FRANCE ------------------
    elif country == "France":
        france_regions = [
            # Official 18 regions (with variants)
            'Île-de-France', 'Ile-de-France', 'Ile de France',
            'Auvergne-Rhône-Alpes', 'Auvergne-Rhone-Alpes', 'Auvergne Rhone Alpes',
            'Bourgogne-Franche-Comté', 'Bourgogne-Franche-Comte', 'Bourgogne Franche Comte',
            'Brittany', 'Bretagne',
            'Centre-Val de Loire', 'Centre Val de Loire',
            'Corsica', 'Corse',
            'Grand Est',
            'Hauts-de-France', 'Hauts de France',
            'Normandy', 'Normandie',
            'Nouvelle-Aquitaine', 'Nouvelle Aquitaine',
            'Occitanie',
            'Pays de la Loire',
            'Provence-Alpes-Côte d\'Azur', 'Provence-Alpes-Cote d\'Azur', 
            'PACA', 'Provence', 'Côte d\'Azur', 'Cote d\'Azur',
            # Former regions (still commonly used)
            'Alsace', 'Lorraine', 'Champagne-Ardenne', 'Picardy', 'Picardie',
            'Nord-Pas-de-Calais', 'Aquitaine', 'Limousin', 'Poitou-Charentes',
            'Languedoc-Roussillon', 'Midi-Pyrénées', 'Midi-Pyrenees',
            'Rhône-Alpes', 'Rhone-Alpes', 'Burgundy', 'Bourgogne'
        ]
        
        for state in france_regions:
            pattern = r'\b' + re.escape(state) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return state

    # ------------------ ITALY ------------------
    elif country == "Italy":
        italy_regions = [
            'Lombardy', 'Lombardia', 'Lazio', 'Tuscany', 'Toscana', 'Sicily', 'Sicilia',
            'Veneto', 'Emilia-Romagna', 'Piemonte', 'Piedmont', 'Liguria', 'Calabria',
            'Campania', 'Sardinia', 'Sardegna', 'Apulia', 'Puglia', 'Friuli', 'Umbria', 'Marche'
        ]
        
        for state in italy_regions:
            pattern = r'\b' + re.escape(state) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return state

    # ------------------ SPAIN ------------------
    elif country == "Spain":
        spain_regions = [
            # All 17 autonomous communities
            'Comunidad de Madrid', 'Madrid',
            'Catalonia', 'Catalunya', 'Cataluña',
            'Andalusia', 'Andalucía',
            'Valencian Community', 'Valencia', 'Comunidad Valenciana',
            'Basque Country', 'País Vasco', 'Euskadi',
            'Galicia',
            'Castile and León', 'Castilla y León',
            'Castilla-La Mancha', 'Castile-La Mancha',
            'Canary Islands', 'Islas Canarias', 'Canarias',
            'Murcia', 'Region of Murcia', 'Región de Murcia',
            'Aragon', 'Aragón',
            'Extremadura',
            'Balearic Islands', 'Islas Baleares', 'Baleares',
            'Asturias', 'Principality of Asturias', 'Principado de Asturias',
            'Navarre', 'Navarra', 'Comunidad Foral de Navarra',
            'Cantabria',
            'La Rioja',
            # Major provinces (sometimes used)
            'Barcelona', 'Seville', 'Sevilla', 'Málaga', 'Malaga',
            'Bilbao', 'Zaragoza'
        ]
        
        for state in spain_regions:
            pattern = r'\b' + re.escape(state) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return state

    # ------------------ SOUTH KOREA ------------------
    elif country == "South Korea":
        korea_regions = [
            # Special/Metropolitan cities
            'Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon',
            'Gwangju', 'Ulsan', 'Sejong',
            # Provinces
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
        
        for state in korea_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ NETHERLANDS ------------------
    elif country == "Netherlands":
        netherlands_regions = [
            # All 12 provinces
            'North Holland', 'Noord-Holland',
            'South Holland', 'Zuid-Holland',
            'Utrecht',
            'North Brabant', 'Noord-Brabant',
            'Gelderland',
            'Groningen',
            'Overijssel',
            'Limburg',
            'Friesland', 'Fryslân',
            'Flevoland',
            'Drenthe',
            'Zeeland'
        ]
        
        for state in netherlands_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ SWITZERLAND ------------------
    elif country == "Switzerland":
        switzerland_regions = [
            # Major cantons
            'Zurich', 'Zürich',
            'Geneva', 'Genève', 'Genf',
            'Basel', 'Basel-Stadt', 'Basel-Landschaft',
            'Bern', 'Berne',
            'Vaud', 'Waadt',
            'Ticino', 'Tessin',
            'St. Gallen', 'Sankt Gallen',
            'Aargau',
            'Lucerne', 'Luzern',
            'Valais', 'Wallis',
            'Fribourg', 'Freiburg',
            'Thurgau',
            'Neuchâtel', 'Neuchatel',
            'Graubünden', 'Grisons',
            'Zug', 'Solothurn', 'Schaffhausen',
            'Appenzell', 'Glarus', 'Jura', 'Schwyz',
            'Uri', 'Nidwalden', 'Obwalden'
        ]
        
        for state in switzerland_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ SWEDEN ------------------
    elif country == "Sweden":
        sweden_regions = [
            # Counties (län)
            'Stockholm', 'Stockholms län',
            'Uppsala', 'Uppsala län',
            'Skåne', 'Skåne län',
            'Västra Götaland', 'Västra Götalands län',
            'Östergötland', 'Ostergotland',
            'Jönköping', 'Jonkoping',
            'Kronoberg', 'Kalmar', 'Gotland',
            'Blekinge', 'Halland', 'Värmland', 'Varmland',
            'Dalarna', 'Gävleborg', 'Gavleborg',
            'Västernorrland', 'Vasternorrland',
            'Jämtland', 'Jamtland',
            'Västerbotten', 'Vasterbotten',
            'Norrbotten'
        ]
        
        for state in sweden_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ BELGIUM ------------------
    elif country == "Belgium":
        belgium_regions = [
            'Brussels', 'Flanders', 'Wallonia', 'Brussels-Capital'
        ]
        
        for state in belgium_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ AUSTRIA ------------------
    elif country == "Austria":
        austria_regions = [
            'Vienna', 'Wien',
            'Lower Austria', 'Niederösterreich',
            'Upper Austria', 'Oberösterreich',
            'Salzburg',
            'Tyrol', 'Tirol',
            'Styria', 'Steiermark',
            'Carinthia', 'Kärnten',
            'Vorarlberg',
            'Burgenland'
        ]
        
        for state in austria_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ PORTUGAL ------------------
    elif country == "Portugal":
        portugal_regions = [
            # Districts
            'Lisbon', 'Lisboa',
            'Porto', 'Oporto',
            'Coimbra',
            'Braga',
            'Aveiro',
            'Faro', 'Algarve',
            'Setúbal', 'Setubal',
            'Évora', 'Evora',
            'Beja',
            'Santarém', 'Santarem',
            'Leiria',
            'Viseu',
            'Castelo Branco',
            'Guarda',
            'Bragança', 'Braganca',
            'Vila Real',
            'Viana do Castelo',
            'Portalegre',
            # Autonomous regions
            'Azores', 'Açores', 'Acores',
            'Madeira'
        ]
        
        for state in portugal_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ BRAZIL ------------------
    elif country == "Brazil":
        brazil_states = {
            'AC': 'Acre',
            'AL': 'Alagoas',
            'AP': 'Amapá',
            'AM': 'Amazonas',
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal',
            'ES': 'Espírito Santo',
            'GO': 'Goiás',
            'MA': 'Maranhão',
            'MT': 'Mato Grosso',
            'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais',
            'PA': 'Pará',
            'PB': 'Paraíba',
            'PR': 'Paraná',
            'PE': 'Pernambuco',
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia',
            'RR': 'Roraima',
            'SC': 'Santa Catarina',
            'SP': 'São Paulo',
            'SE': 'Sergipe',
            'TO': 'Tocantins'
        }
        
        # Check abbreviations first
        for abbr, full in brazil_states.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', affiliation_text):
                return full
        
        # Then check full names (with accents and without)
        full_names = [
            'São Paulo', 'Sao Paulo',
            'Rio de Janeiro',
            'Minas Gerais',
            'Paraná', 'Parana',
            'Rio Grande do Sul',
            'Bahia', 'Pernambuco',
            'Ceará', 'Ceara',
            'Santa Catarina',
            'Goiás', 'Goias',
            'Espírito Santo', 'Espirito Santo',
            'Distrito Federal', 'Brasília', 'Brasilia',
            'Pará', 'Para',
            'Paraíba', 'Paraiba',
            'Maranhão', 'Maranhao',
            'Piauí', 'Piaui',
            'Rio Grande do Norte',
            'Rondônia', 'Rondonia',
            'Mato Grosso', 'Mato Grosso do Sul',
            'Amazonas', 'Acre', 'Amapá', 'Amapa',
            'Roraima', 'Tocantins', 'Alagoas', 'Sergipe'
        ]
    
        for state in full_names:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ MEXICO ------------------
    elif country == "Mexico":
        mexico_states = [
            'Mexico City', 'Ciudad de México', 'CDMX',
            'Jalisco',
            'Nuevo León', 'Nuevo Leon',
            'Puebla',
            'Guanajuato',
            'Yucatán', 'Yucatan',
            'Veracruz',
            'Chiapas',
            'Oaxaca',
            'Michoacán', 'Michoacan',
            'Guerrero',
            'Tamaulipas',
            'Sinaloa',
            'Coahuila',
            'Chihuahua',
            'Sonora',
            'San Luis Potosí', 'San Luis Potosi',
            'Hidalgo',
            'Tabasco',
            'Querétaro', 'Queretaro',
            'Morelos',
            'Durango',
            'Zacatecas',
            'Quintana Roo',
            'Aguascalientes',
            'Tlaxcala',
            'Nayarit',
            'Campeche',
            'Baja California',
            'Colima',
            'Baja California Sur'
        ]
        
        for state in mexico_states:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    # ------------------ TURKEY ------------------
    elif country == "Turkey":
        turkey_regions = [
            # Major provinces (il)
            'Istanbul', 'İstanbul',
            'Ankara',
            'Izmir', 'İzmir',
            'Bursa',
            'Antalya',
            'Adana',
            'Gaziantep',
            'Konya',
            'Kocaeli',
            'Mersin', 'İçel',
            'Kayseri',
            'Eskişehir', 'Eskisehir',
            'Diyarbakır', 'Diyarbakir',
            'Samsun',
            'Denizli',
            'Şanlıurfa', 'Sanliurfa',
            'Trabzon',
            'Van',
            'Malatya',
            'Erzurum'
        ]
            
        for state in turkey_regions:
            if re.search(r'\b' + re.escape(state) + r'\b', affiliation_text, re.IGNORECASE):
                return state

    return ''