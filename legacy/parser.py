"""
Parser Module
Extract specific information from affiliation strings
"""
import re

def extract_email(affiliation_text):
    """
    Extract email address from affiliation text
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Email address or None
    """
    if not affiliation_text:
        return None
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    matches = re.findall(email_pattern, affiliation_text)
    
    if matches:
        return matches[0]  # Return first email found
    
    return None

import re

def extract_state(affiliation_text):
    """
    Extract State / Region from affiliation text
    Supports: USA, Germany, UK, France, Italy, Spain
    """
    if not affiliation_text:
        return ''
    
    # ------------------ USA ------------------
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
    
    for abbr, full_name in us_states.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        if re.search(pattern, affiliation_text):
            return full_name
    
    for full_name in us_states.values():
        pattern = r'\b' + re.escape(full_name) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return full_name

    # ------------------ GERMANY ------------------
    germany_states = [
        'Bavaria', 'Bayern', 'Berlin', 'Brandenburg', 'Hamburg', 'Hesse', 'Hessen',
        'Saxony', 'Sachsen', 'Saxony-Anhalt', 'North Rhine-Westphalia', 'NRW',
        'Lower Saxony', 'Niedersachsen', 'Mecklenburg-Western Pomerania',
        'Rhineland-Palatinate', 'Thuringia', 'Thueringen',
        'Schleswig-Holstein', 'Saarland', 'Bremen', 'Baden-Württemberg', 'Baden Wurttemberg'
    ]
    
    for state in germany_states:
        pattern = r'\b' + re.escape(state) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return state

    # ------------------ UNITED KINGDOM ------------------
    uk_regions = [
        'England', 'Scotland', 'Wales', 'Northern Ireland', 'Greater London',
        'London', 'West Midlands', 'East Midlands', 'Yorkshire', 'Kent', 'Surrey',
        'Essex', 'Manchester', 'Lancashire', 'Oxfordshire', 'Cambridgeshire'
    ]
    
    for state in uk_regions:
        pattern = r'\b' + re.escape(state) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return state

    # ------------------ FRANCE ------------------
    france_regions = [
        'Île-de-France', 'Ile-de-France', 'Paris', 'Provence', 'Brittany', 'Bretagne',
        'Normandy', 'Occitanie', 'Nouvelle-Aquitaine', 'Grand Est',
        'Auvergne-Rhône-Alpes', 'Loire', 'Bourgogne', 'Corsica'
    ]
    
    for state in france_regions:
        pattern = r'\b' + re.escape(state) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return state

    # ------------------ ITALY ------------------
    italy_regions = [
        'Lombardy', 'Lombardia', 'Lazio', 'Tuscany', 'Toscana', 'Sicily', 'Sicilia',
        'Veneto', 'Emilia-Romagna', 'Piemonte', 'Piedmont', 'Liguria', 'Calabria',
        'Campania', 'Sardinia', 'Sardegna', 'Apulia', 'Puglia', 'Friuli',
        'Umbria', 'Marche'
    ]
    
    for state in italy_regions:
        pattern = r'\b' + re.escape(state) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return state

    # ------------------ SPAIN ------------------
    spain_regions = [
        'Madrid', 'Comunidad de Madrid', 'Catalonia', 'Catalunya', 'Barcelona',
        'Andalusia', 'Andalucía', 'Valencia', 'Valencian Community',
        'Basque Country', 'Euskadi', 'Galicia', 'Navarre', 'Navarra',
        'Castile', 'Castilla', 'La Rioja', 'Murcia', 'Aragon', 'Balearic Islands'
    ]
    
    for state in spain_regions:
        pattern = r'\b' + re.escape(state) + r'\b'
        if re.search(pattern, affiliation_text, re.IGNORECASE):
            return state

    return ''


def extract_country(affiliation_text):
    """
    Extract country from affiliation text
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Country name or None
    """
    if not affiliation_text:
        return None
    
    # Common country names and abbreviations
    countries = {

        # North America
        'US': ['USA','United States','U.S.A','U.S.','United States of America','America'],
        'Canada': ['Canada'],
        'Mexico': ['Mexico','México'],

        # South America
        'Brazil': ['Brazil','Brasil'],
        'Argentina': ['Argentina'],
        'Chile': ['Chile'],
        'Colombia': ['Colombia'],
        'Peru': ['Peru'],
        'Venezuela': ['Venezuela'],
        'Bolivia': ['Bolivia'],
        'Ecuador': ['Ecuador'],
        'Paraguay': ['Paraguay'],
        'Uruguay': ['Uruguay'],
        'Guyana': ['Guyana'],
        'Suriname': ['Suriname'],

        # Europe
        'UK': ['UK','United Kingdom','Great Britain','England','Scotland','Wales','Northern Ireland','Britain'],
        'Ireland': ['Ireland','Éire'],
        'France': ['France','République Française'],
        'Germany': ['Germany','Deutschland'],
        'Italy': ['Italy','Italia'],
        'Spain': ['Spain','España'],
        'Portugal': ['Portugal'],
        'Netherlands': ['Netherlands','The Netherlands','Holland'],
        'Belgium': ['Belgium','België','Belgique'],
        'Switzerland': ['Switzerland','Schweiz','Suisse','Svizzera'],
        'Austria': ['Austria','Österreich'],
        'Sweden': ['Sweden','Sverige'],
        'Norway': ['Norway','Norge'],
        'Finland': ['Finland','Suomi'],
        'Denmark': ['Denmark','Danmark'],
        'Poland': ['Poland','Polska'],
        'Czech Republic': ['Czech Republic','Czechia','Česko'],
        'Slovakia': ['Slovakia'],
        'Hungary': ['Hungary','Magyarország'],
        'Romania': ['Romania'],
        'Bulgaria': ['Bulgaria'],
        'Croatia': ['Croatia','Hrvatska'],
        'Slovenia': ['Slovenia'],
        'Serbia': ['Serbia'],
        'Bosnia and Herzegovina': ['Bosnia','Herzegovina','Bosnia and Herzegovina'],
        'Greece': ['Greece','Hellas','Ελλάδα'],
        'Cyprus': ['Cyprus'],
        'Lithuania': ['Lithuania'],
        'Latvia': ['Latvia'],
        'Estonia': ['Estonia'],
        'Ukraine': ['Ukraine'],
        'Russia': ['Russia','Russian Federation'],
        'Belarus': ['Belarus'],
        'Moldova': ['Moldova'],
        'Iceland': ['Iceland'],
        'Luxembourg': ['Luxembourg'],
        'Malta': ['Malta'],
        'Monaco': ['Monaco'],
        'Andorra': ['Andorra'],
        'Liechtenstein': ['Liechtenstein'],
        'San Marino': ['San Marino'],
        'Vatican City': ['Vatican','Holy See'],

        # Asia
        'India': ['India','Bharat'],
        'China': ['China','PR China','P.R. China','People’s Republic of China'],
        'Japan': ['Japan'],
        'South Korea': ['South Korea','Republic of Korea','Korea'],
        'North Korea': ['North Korea','DPRK'],
        'Taiwan': ['Taiwan','Republic of China'],
        'Singapore': ['Singapore'],
        'Malaysia': ['Malaysia'],
        'Indonesia': ['Indonesia'],
        'Philippines': ['Philippines'],
        'Thailand': ['Thailand'],
        'Vietnam': ['Vietnam'],
        'Cambodia': ['Cambodia'],
        'Laos': ['Laos'],
        'Myanmar': ['Myanmar','Burma'],
        'Sri Lanka': ['Sri Lanka'],
        'Nepal': ['Nepal'],
        'Bangladesh': ['Bangladesh'],
        'Pakistan': ['Pakistan'],
        'Afghanistan': ['Afghanistan'],
        'Iran': ['Iran','Islamic Republic of Iran'],
        'Iraq': ['Iraq'],
        'Saudi Arabia': ['Saudi Arabia','KSA'],
        'UAE': ['UAE','United Arab Emirates'],
        'Qatar': ['Qatar'],
        'Kuwait': ['Kuwait'],
        'Oman': ['Oman'],
        'Yemen': ['Yemen'],
        'Israel': ['Israel'],
        'Palestine': ['Palestine'],
        'Jordan': ['Jordan'],
        'Lebanon': ['Lebanon'],
        'Syria': ['Syria'],
        'Turkey': ['Turkey','Türkiye','Turkiye'],
        'Georgia': ['Georgia'],
        'Armenia': ['Armenia'],
        'Azerbaijan': ['Azerbaijan'],
        'Kazakhstan': ['Kazakhstan'],
        'Uzbekistan': ['Uzbekistan'],
        'Turkmenistan': ['Turkmenistan'],
        'Kyrgyzstan': ['Kyrgyzstan'],
        'Tajikistan': ['Tajikistan'],
        'Mongolia': ['Mongolia'],

        # Africa
        'South Africa': ['South Africa'],
        'Egypt': ['Egypt'],
        'Nigeria': ['Nigeria'],
        'Kenya': ['Kenya'],
        'Ethiopia': ['Ethiopia'],
        'Ghana': ['Ghana'],
        'Morocco': ['Morocco'],
        'Algeria': ['Algeria'],
        'Tunisia': ['Tunisia'],
        'Libya': ['Libya'],
        'Sudan': ['Sudan'],
        'Uganda': ['Uganda'],
        'Tanzania': ['Tanzania'],
        'Zambia': ['Zambia'],
        'Zimbabwe': ['Zimbabwe'],
        'Botswana': ['Botswana'],
        'Namibia': ['Namibia'],
        'Mozambique': ['Mozambique'],
        'Angola': ['Angola'],
        'Cameroon': ['Cameroon'],
        'Ivory Coast': ['Ivory Coast','Côte d’Ivoire'],
        'Senegal': ['Senegal'],
        'Rwanda': ['Rwanda'],
        'Somalia': ['Somalia'],

        # Oceania
        'Australia': ['Australia'],
        'New Zealand': ['New Zealand'],
        'Fiji': ['Fiji'],
        'Papua New Guinea': ['Papua New Guinea'],

        # Middle East extras
        'Bahrain': ['Bahrain'],
        'Cyprus': ['Cyprus']
    }

    
    # Check for each country
    for country, variants in countries.items():
        for variant in variants:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return country
    
    return None

def infer_country_from_location(affiliation_text, state, city):
    """
    Infer country from state or city when country is not explicitly mentioned
    
    Args:
        affiliation_text: Full affiliation string
        state: Extracted US state (if any)
        city: Extracted city (if any)
    
    Returns:
        Inferred country name or None
    """
    # If US state is found, country must be US
    if state:
        return 'US'
    
    # If city is a well-known major city, infer country
    city_to_country = {
        # Major US cities
        'New York': 'US', 'Los Angeles': 'US', 'Chicago': 'US', 'Houston': 'US',
        'Philadelphia': 'US', 'Phoenix': 'US', 'San Antonio': 'US', 'San Diego': 'US',
        'Dallas': 'US', 'San Jose': 'US', 'Austin': 'US', 'Jacksonville': 'US',
        'San Francisco': 'US', 'Columbus': 'US', 'Indianapolis': 'US', 'Seattle': 'US',
        'Denver': 'US', 'Washington': 'US', 'Boston': 'US', 'Nashville': 'US',
        'Baltimore': 'US', 'Portland': 'US', 'Las Vegas': 'US', 'Detroit': 'US',
        'Memphis': 'US', 'Louisville': 'US', 'Milwaukee': 'US', 'Albuquerque': 'US',
        'Tucson': 'US', 'Fresno': 'US', 'Sacramento': 'US', 'Mesa': 'US',
        'Atlanta': 'US', 'Kansas City': 'US', 'Miami': 'US', 'Cleveland': 'US',
        'Minneapolis': 'US', 'New Orleans': 'US', 'Tampa': 'US', 'Pittsburgh': 'US',
        
        # UK cities
        'London': 'UK', 'Manchester': 'UK', 'Birmingham': 'UK', 'Liverpool': 'UK',
        'Leeds': 'UK', 'Glasgow': 'UK', 'Edinburgh': 'UK', 'Bristol': 'UK',
        'Cardiff': 'UK', 'Oxford': 'UK', 'Cambridge': 'UK', 'Newcastle': 'UK',
        
        # Canadian cities
        'Toronto': 'Canada', 'Montreal': 'Canada', 'Vancouver': 'Canada', 
        'Calgary': 'Canada', 'Edmonton': 'Canada', 'Ottawa': 'Canada',
        'Winnipeg': 'Canada', 'Quebec City': 'Canada', 'Hamilton': 'Canada',
        
        # Australian cities
        'Sydney': 'Australia', 'Melbourne': 'Australia', 'Brisbane': 'Australia',
        'Perth': 'Australia', 'Adelaide': 'Australia', 'Canberra': 'Australia',
        
        # Indian cities
        'Mumbai': 'India', 'Delhi': 'India', 'Bangalore': 'India', 'Hyderabad': 'India',
        'Chennai': 'India', 'Kolkata': 'India', 'Pune': 'India', 'Ahmedabad': 'India',
        'Jaipur': 'India', 'Lucknow': 'India', 'Chandigarh': 'India',
        
        # European cities
        'Paris': 'France', 'Berlin': 'Germany', 'Munich': 'Germany', 'Hamburg': 'Germany',
        'Rome': 'Italy', 'Milan': 'Italy', 'Madrid': 'Spain', 'Barcelona': 'Spain',
        'Amsterdam': 'Netherlands', 'Brussels': 'Belgium', 'Vienna': 'Austria',
        'Zurich': 'Switzerland', 'Geneva': 'Switzerland', 'Stockholm': 'Sweden',
        'Copenhagen': 'Denmark', 'Oslo': 'Norway', 'Helsinki': 'Finland',
        'Dublin': 'Ireland', 'Lisbon': 'Portugal', 'Prague': 'Czech Republic',
        'Warsaw': 'Poland', 'Budapest': 'Hungary', 'Athens': 'Greece',
        
        # Asian cities
        'Tokyo': 'Japan', 'Osaka': 'Japan', 'Beijing': 'China', 'Shanghai': 'China',
        'Hong Kong': 'China', 'Singapore': 'Singapore', 'Seoul': 'South Korea',
        'Bangkok': 'Thailand', 'Kuala Lumpur': 'Malaysia', 'Jakarta': 'Indonesia',
        'Manila': 'Philippines', 'Taipei': 'China', 'Karachi': 'Pakistan',
        'Lahore': 'Pakistan', 'Islamabad': 'Pakistan', 'Dhaka': 'Bangladesh',
        
        # Middle Eastern cities
        'Dubai': 'UAE', 'Abu Dhabi': 'UAE', 'Riyadh': 'Saudi Arabia',
        'Tel Aviv': 'Israel', 'Jerusalem': 'Israel', 'Istanbul': 'Turkey',
        'Ankara': 'Turkey', 'Cairo': 'Egypt',
        
        # South American cities
        'São Paulo': 'Brazil', 'Rio de Janeiro': 'Brazil', 'Buenos Aires': 'Argentina',
        'Mexico City': 'Mexico', 'Lima': 'Peru', 'Bogotá': 'Colombia',
        
        # African cities
        'Johannesburg': 'South Africa', 'Cape Town': 'South Africa', 'Nairobi': 'South Africa',
        
        # New Zealand
        'Auckland': 'New Zealand', 'Wellington': 'New Zealand', 'Christchurch': 'New Zealand'
    }
    
    if city and city in city_to_country:
        return city_to_country[city]
    
    return None

def extract_city(affiliation_text):
    """
    Extract city from affiliation text - STRICT MODE
    Only extracts if we're highly confident, otherwise returns empty
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        City name or empty string
    """
    if not affiliation_text:
        return ''
    
    # List of common words that are NOT cities (to avoid false positives)
    non_city_terms = [
        'university', 'college', 'hospital', 'medical', 'center', 'centre',
        'school', 'institute', 'department', 'division', 'health', 'system',
        'clinic', 'laboratory', 'research', 'sciences', 'medicine', 'care'
    ]
    
    # Pattern 1: City between institution and state with ZIP
    # Example: "Stanford University, Palo Alto, CA 94305"
    pattern1 = r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,\s*[A-Z]{2}\s+\d{5}'
    match = re.search(pattern1, affiliation_text)
    if match:
        city = match.group(1).strip()
        # Check it's not a non-city term
        if city.lower() not in non_city_terms:
            return city
    
    # Pattern 2: City before state name (full)
    # Example: "Hospital, Boston, Massachusetts"
    pattern2 = r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,\s*(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming|District of Columbia)'
    match = re.search(pattern2, affiliation_text, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        # Verify it's not the same as the state
        state = match.group(2).strip()
        if city.lower() not in non_city_terms and city.lower() != state.lower():
            return city
    
    # Pattern 3: Very specific format with clear city
    # Example: "Department of X, City Name, State"
    # Only accept if city is 1-2 words and doesn't contain institution keywords
    pattern3 = r',\s*([A-Z][a-z]+)\s*,\s*[A-Z]{2}\b'
    match = re.search(pattern3, affiliation_text)
    if match:
        city = match.group(1).strip()
        if city.lower() not in non_city_terms and len(city.split()) <= 2:
            return city
    
    # If no confident match, return empty
    return ''

def extract_postal_code(affiliation_text):
    """
    Extract postal code from affiliation text
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Postal code or empty string
    """
    if not affiliation_text:
        return ''
    
    # US ZIP code pattern (5 digits or 5+4 format)
    zip_pattern = r'\b(\d{5}(?:-\d{4})?)\b'
    matches = re.findall(zip_pattern, affiliation_text)
    
    if matches:
        return matches[0]
    
    return ''

def extract_therapy_area(affiliation_text, specialty):
    """
    Extract therapy area based on detected specialty.
    Returns specific therapy keyword if found, else empty string.
    """
    if not affiliation_text:
        return ''

    therapy_map = {
        'Oncology': ['oncology','oncology department','division of oncology','medical oncology','radiation oncology','clinical oncology','cancer center','cancer centre','cancer institute','comprehensive cancer center'],
        'Cardiology': ['cardiology','division of cardiology','department of cardiology','cardiovascular medicine','cardiac medicine','heart institute','cardiac sciences','cardiovascular sciences'],
        'Neurology': ['neurology','division of neurology','department of neurology','neurological sciences','neurosciences','clinical neurology'],
        'Endocrinology': ['endocrinology','division of endocrinology','department of endocrinology','metabolism and endocrinology','endocrine medicine'],
        'Gastroenterology': ['gastroenterology','division of gastroenterology','department of gastroenterology','digestive diseases','digestive health','hepatology'],
        'Pulmonology': ['pulmonology','division of pulmonology','department of pulmonology','respiratory medicine','pulmonary medicine','chest medicine'],
        'Nephrology': ['nephrology','division of nephrology','department of nephrology','renal medicine','kidney medicine'],
        'Immunology': ['immunology','division of immunology','department of immunology','clinical immunology','immune sciences'],
        'Dermatology': ['dermatology','division of dermatology','department of dermatology','cutaneous medicine','skin department'],
        'Orthopedics': ['orthopedics','orthopaedics','division of orthopedics','department of orthopedics','orthopedic surgery','musculoskeletal medicine'],
        'Psychiatry': ['psychiatry','division of psychiatry','department of psychiatry','mental health','behavioral health'],
        'Surgery': ['surgery','surgical department','department of surgery','general surgery','surgical sciences'],
        'Pediatrics': ['pediatrics','paediatrics','division of pediatrics','department of pediatrics','child health','pediatric medicine'],
        'Radiology': ['radiology','department of radiology','division of radiology','radiological sciences','medical imaging','diagnostic imaging'],
        'Emergency Medicine': ['emergency medicine','emergency department','acute care','trauma center'],
        'Internal Medicine': ['internal medicine','department of medicine','general medicine'],
        'Family Medicine': ['family medicine','general practice','primary care'],
        'Obstetrics & Gynecology': ['obstetrics and gynecology','ob gyn','ob-gyn','women’s health','maternal health'],
        'Anesthesiology': ['anesthesiology','anaesthesiology','anesthesia','perioperative medicine'],
        'Pathology': ['pathology','department of pathology','pathological sciences','laboratory medicine'],
        'Hematology': ['hematology','haematology','blood disorders'],
        'Rheumatology': ['rheumatology','autoimmune diseases','connective tissue disease'],
        'Infectious Disease': ['infectious disease','infectious diseases','clinical infection'],
        'Urology': ['urology','department of urology','genitourinary medicine'],
        'Ophthalmology': ['ophthalmology','eye institute','vision sciences'],
        'ENT': ['otolaryngology','ear nose throat','head and neck surgery'],
        'Physical Medicine': ['physical medicine','rehabilitation medicine','pm&r'],
        'Genetics': ['genetics','genomic medicine','medical genetics'],
        'Public Health': ['public health','epidemiology','population health','community medicine']
    }


    text = affiliation_text.lower()

    for therapy_area, keywords in therapy_map.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                return therapy_area
            
    return ''


def extract_specialty(affiliation_text):
    """
    Extract specialty from department information in affiliation
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Specialty or None
    """
    if not affiliation_text:
        return None

    # Common department/specialty patterns
    specialties = {
        'Cardiology': ['cardiology', 'cardiovascular medicine', 'cardiac sciences', 'heart institute', 'division of cardiology', 'department of cardiology'],
        'Neurology': ['neurology', 'neurological sciences', 'neurosciences', 'brain sciences', 'department of neurology'],
        'Neurosurgery': ['neurosurgery', 'department of neurosurgery'],
        'Psychiatry': ['psychiatry', 'mental health', 'behavioral health', 'department of psychiatry'],
        'Psychology': ['psychology', 'clinical psychology'],
        'Oncology': ['oncology', 'medical oncology', 'radiation oncology', 'surgical oncology', 'cancer center', 'cancer institute', 'tumor biology'],
        'Hematology': ['hematology', 'haematology', 'blood disorders'],
        'Hematology-Oncology': ['hematology oncology', 'haematology oncology'],
        'Radiation Oncology': ['radiation oncology', 'radiotherapy'],
        'Pediatrics': ['pediatrics', 'paediatrics', 'child health', 'neonatology', 'department of pediatrics'],
        'Neonatology': ['neonatology', 'newborn medicine'],
        'Surgery': ['surgery', 'general surgery', 'surgical sciences', 'department of surgery'],
        'Cardiothoracic Surgery': ['cardiothoracic surgery', 'heart surgery', 'thoracic surgery'],
        'Vascular Surgery': ['vascular surgery'],
        'Plastic Surgery': ['plastic surgery', 'reconstructive surgery'],
        'Orthopedic Surgery': ['orthopedics', 'orthopaedics', 'orthopedic surgery', 'musculoskeletal surgery'],
        'Trauma Surgery': ['trauma surgery'],
        'Urology': ['urology', 'urologic surgery'],
        'Gynecology': ['gynecology', 'gynaecology'],
        'Obstetrics': ['obstetrics', 'maternal medicine'],
        'Obstetrics & Gynecology': ['obstetrics and gynecology', 'ob-gyn', 'women’s health'],
        'Reproductive Medicine': ['reproductive medicine', 'fertility', 'ivf'],
        'Radiology': ['radiology', 'radiological sciences', 'diagnostic imaging', 'medical imaging'],
        'Interventional Radiology': ['interventional radiology'],
        'Nuclear Medicine': ['nuclear medicine'],
        'Pathology': ['pathology', 'anatomic pathology', 'clinical pathology', 'molecular pathology'],
        'Dermatology': ['dermatology', 'skin diseases', 'cutaneous medicine'],
        'Ophthalmology': ['ophthalmology', 'eye institute', 'vision sciences'],
        'Otolaryngology': ['otolaryngology', 'ent', 'ear nose throat'],
        'Pulmonology': ['pulmonology', 'respiratory medicine', 'chest medicine', 'lung diseases'],
        'Critical Care': ['critical care', 'intensive care', 'icu'],
        'Sleep Medicine': ['sleep medicine'],
        'Nephrology': ['nephrology', 'renal medicine', 'kidney diseases'],
        'Dialysis': ['dialysis'],
        'Gastroenterology': ['gastroenterology', 'digestive diseases', 'hepatogastroenterology'],
        'Hepatology': ['hepatology', 'liver diseases'],
        'Endocrinology': ['endocrinology', 'hormone disorders', 'diabetes'],
        'Diabetology': ['diabetology'],
        'Rheumatology': ['rheumatology', 'autoimmune diseases'],
        'Immunology': ['immunology', 'immune disorders'],
        'Allergy': ['allergy', 'allergy and immunology'],
        'Infectious Disease': ['infectious disease', 'tropical medicine'],
        'Microbiology': ['microbiology'],
        'Virology': ['virology'],
        'Parasitology': ['parasitology'],
        'Epidemiology': ['epidemiology'],
        'Public Health': ['public health', 'population health'],
        'Preventive Medicine': ['preventive medicine'],
        'Internal Medicine': ['internal medicine', 'general medicine', 'department of medicine'],
        'Family Medicine': ['family medicine', 'general practice', 'primary care'],
        'Geriatrics': ['geriatrics', 'aging medicine'],
        'Palliative Care': ['palliative care', 'hospice'],
        'Physical Medicine & Rehabilitation': ['physical medicine', 'rehabilitation medicine', 'pm&r'],
        'Sports Medicine': ['sports medicine'],
        'Pain Medicine': ['pain medicine'],
        'Anesthesiology': ['anesthesiology', 'anaesthesiology'],
        'Emergency Medicine': ['emergency medicine', 'acute care'],
        'Toxicology': ['toxicology'],
        'Clinical Pharmacology': ['clinical pharmacology'],
        'Pharmacology': ['pharmacology'],
        'Genetics': ['genetics', 'genomics', 'medical genetics'],
        'Molecular Biology': ['molecular biology'],
        'Cell Biology': ['cell biology'],
        'Biochemistry': ['biochemistry'],
        'Biomedical Research': ['biomedical research', 'translational medicine'],
        'Clinical Research': ['clinical research', 'clinical trials'],
        'Biostatistics': ['biostatistics'],
        'Bioinformatics': ['bioinformatics', 'computational biology'],
        'Health Informatics': ['health informatics'],
        'Health Economics': ['health economics', 'outcomes research'],
        'Nutrition': ['nutrition', 'dietary'],
        'Dietetics': ['dietetics'],
        'Dentistry': ['dentistry', 'oral health'],
        'Oral & Maxillofacial Surgery': ['oral surgery', 'maxillofacial surgery'],
        'Veterinary Medicine': ['veterinary medicine', 'animal health'],
        'Comparative Medicine': ['comparative medicine']
    }



    
    affiliation_lower = affiliation_text.lower()
    
    # Check for department/division/center mentions
    for specialty, keywords in specialties.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, affiliation_lower):
                return specialty
    
    return None

def extract_subspecialty(affiliation_text, specialty):
    """
    Extract sub-specialty from the keywords found in affiliation
    Now returns the actual keyword found (e.g., 'cardiovascular', 'cardiac')
    
    Args:
        affiliation_text: Full affiliation string
        specialty: Main specialty already identified
    
    Returns:
        Sub-specialty keyword or None
    """
    if not affiliation_text or not specialty:
        return None
    
    # Use the same specialty keywords - return the actual keyword found
    sub_specialty_keywords = {

        'Cardiology': ['cardiology','cardiovascular','cardiac','heart','heart failure','arrhythmia','atrial fibrillation','ischemia','myocardial infarction','acute coronary syndrome','coronary artery disease','hypertension','hypertensive','cardiomyopathy','valvular','valve disease','cardiac arrest','cardio-oncology','interventional cardiology','electrophysiology','heart transplant','heart transplantation','congenital heart disease','pulmonary hypertension','atherosclerosis','angiography','angioplasty','stent','echocardiography','ecg','ekg'],
        'Neurology': ['neurology','neurological','stroke','ischemic stroke','hemorrhagic stroke','cerebrovascular','epilepsy','seizure','parkinson','parkinson disease','alzheimer','alzheimer disease','dementia','multiple sclerosis','neurodegenerative','neuropathy','neuroinflammation','migraine','headache','brain injury','neuroimaging','neurovascular','movement disorder'],
        'Psychiatry': ['psychiatry','mental health','depression','anxiety','schizophrenia','bipolar disorder','psychosis','mood disorder','major depressive disorder','ptsd','post traumatic stress','suicide','addiction','substance abuse','alcohol use disorder','behavioral disorder'],
        'Oncology': ['oncology','cancer','tumor','tumour','neoplasm','neoplasms','malignancy','malignant','leukemia','lymphoma','myeloma','metastasis','metastatic','solid tumor','breast cancer','lung cancer','prostate cancer','colorectal cancer','immuno-oncology','chemotherapy','radiotherapy','targeted therapy','precision oncology','oncogenomics'],
        'Pediatrics': ['pediatrics','paediatrics','child','children','neonatal','infant','newborn','childhood','congenital','developmental','pediatric oncology','pediatric cardiology','pediatric neurology','growth disorder','genetic disorder'],
        'Surgery': ['surgery','surgical','postoperative','preoperative','laparoscopic','minimally invasive','robotic surgery','general surgery','thoracic surgery','vascular surgery','neurosurgery','orthopedic surgery','trauma surgery','surgical oncology'],
        'Radiology': ['radiology','radiological','imaging','medical imaging','x-ray','ct','ct scan','computed tomography','mri','magnetic resonance imaging','ultrasound','sonography','nuclear medicine','pet scan','interventional radiology'],
        'Dermatology': ['dermatology','skin','psoriasis','eczema','atopic dermatitis','vitiligo','melanoma','skin cancer','acne','rosacea','alopecia','urticaria','dermatitis'],
        'Orthopedics': ['orthopedics','orthopaedics','bone','joint','osteoarthritis','arthritis','joint replacement','hip replacement','knee replacement','fracture','acl','meniscus','sports injury','spine','spinal surgery','osteoporosis'],
        'Ophthalmology': ['ophthalmology','eye','glaucoma','cataract','retina','retinal disease','macular degeneration','diabetic retinopathy','vision loss','cornea','ocular','uveitis'],
        'ENT': ['ent','otolaryngology','ear nose throat','hearing loss','deafness','sinusitis','otitis','tonsillitis','larynx','voice disorder','nasal disorder'],
        'Urology': ['urology','prostate','prostate cancer','urinary','urinary tract','kidney stone','bladder','bladder cancer','renal cancer','erectile dysfunction','male infertility'],
        'Nephrology': ['nephrology','kidney','renal','chronic kidney disease','ckd','renal failure','dialysis','transplant','glomerulonephritis','proteinuria'],
        'Gastroenterology': ['gastroenterology','digestive','ibd','crohn','ulcerative colitis','hepatitis','cirrhosis','liver disease','fatty liver','pancreatitis','gastrointestinal','gi cancer'],
        'Endocrinology': ['endocrinology','diabetes','diabetic','thyroid','hypothyroidism','hyperthyroidism','insulin','metabolic','obesity','pcos','pituitary','adrenal'],
        'Pulmonology': ['pulmonology','respiratory','asthma','copd','chronic obstructive pulmonary disease','interstitial lung disease','pulmonary fibrosis','lung cancer','sleep apnea','tuberculosis'],
        'Rheumatology': ['rheumatology','rheumatoid arthritis','lupus','autoimmune','connective tissue disease','spondyloarthritis','psoriatic arthritis','vasculitis','sjogren','ankylosing spondylitis'],
        'Hematology': ['hematology','haematology','anemia','blood disorder','coagulation','thrombosis','hemophilia','platelet','bone marrow','leukemia','lymphoma'],
        'Infectious Disease': ['infectious','infection','viral','bacterial','fungal','sepsis','covid','hiv','aids','tuberculosis','hepatitis','antimicrobial','antibiotic resistance'],
        'Immunology': ['immunology','immune','autoimmune','immune deficiency','immunodeficiency','allergy','hypersensitivity','immunotherapy','vaccination','vaccine'],
        'Pathology': ['pathology','histopathology','biopsy','tissue','molecular pathology','cytopathology','tumor pathology','diagnostic pathology'],
        'Anesthesiology': ['anesthesiology','anaesthesiology','anesthesia','analgesia','sedation','pain management','perioperative','critical care'],
        'Emergency Medicine': ['emergency medicine','trauma','acute care','critical illness','intensive care','icu','shock','cardiac arrest'],
        'Internal Medicine': ['internal medicine','general medicine','chronic disease','multimorbidity','systemic disease','metabolic syndrome'],
        'Family Medicine': ['family medicine','primary care','general practice','preventive care','community health','screening'],
        'Obstetrics & Gynecology': ['obstetrics','gynecology','gynaecology','pregnancy','childbirth','prenatal','postnatal','fertility','ivf','endometriosis','ovarian','uterine','cervical cancer'],
        'Physical Medicine': ['rehabilitation','physical medicine','physiotherapy','physical therapy','functional recovery','stroke rehab','pain rehabilitation'],
        'Genetics': ['genetics','genomic','genomics','mutation','hereditary','inherited','genetic disorder','precision medicine'],
        'Public Health': ['public health','epidemiology','population health','disease prevention','screening','health policy','health services research']

    }
    
    if specialty not in sub_specialty_keywords:
        return None
    
    affiliation_lower = affiliation_text.lower()
    
    # Return the actual keyword found in the affiliation
    for keyword in sub_specialty_keywords[specialty]:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, affiliation_lower):
            return keyword.title()  # Return capitalized keyword
    
    return None

def extract_institution(affiliation_text):
    """
    Extract main institution/university name from affiliation
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Institution name or full affiliation if can't parse
    """
    if not affiliation_text:
        return None
    
    # Remove email if present
    clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', affiliation_text)
    
    # Expanded institution keywords (US + Germany + Spain + Italy + France + UK)
    institution_keywords = [
        # English (US, UK, global)
        'University','College','Institute','Hospital','Medical Center','Medical Centre','Clinic',
        'School of Medicine','Medical School','Health Sciences','Faculty of Medicine','Faculty of Health',
        'Academic Medical Center','Teaching Hospital','University Hospital',

        # Germany
        'Universität','Universitaet','Klinik','Klinikum','Universitätsklinikum','Universitaetsklinikum',
        'Hochschule','Fakultät','Fakultaet','Institut','Zentrum','Medizinische Hochschule',
        'Charité','Charite','Universitätsmedizin','Universitaetsmedizin',

        # France
        'Université','Universite','Hôpital','Hopital','Centre Hospitalier','CHU',
        'Institut','Faculté','Faculte','Assistance Publique','Hôpitaux','Hopitaux',
        'Centre de Recherche','Inserm','CNRS','Institut Pasteur',

        # Spain
        'Universidad','Hospital','Centro','Centro Médico','Centro Medico',
        'Instituto','Clínica','Clinica','Facultad','Servicio de','Departamento de',
        'Complejo Hospitalario','Hospital Universitario',

        # Italy
        'Università','Universita','Ospedale','Policlinico','Istituto','Clinica',
        'Azienda Ospedaliera','IRCCS','Fondazione','Dipartimento','Centro',

        # UK specific
        'NHS','Trust','Foundation Trust','Royal','King’s College','Kings College',
        'Imperial College','University College London','UCL','Guy’s','St Thomas’',
        'Great Ormond Street','Oxford','Cambridge'
    ]
    
    # Try to find institution name
    for keyword in institution_keywords:
        pattern = r'([^,\.;]+' + re.escape(keyword) + r'[^,\.;]*)'
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # If no specific institution found, return first part before comma
    parts = clean_text.split(',')
    if parts:
        return parts[0].strip()
    
    return clean_text.strip()

def parse_affiliation(affiliation_text, target_countries=None):
    """
    Parse complete affiliation and extract all fields from the PRIMARY affiliation (the one with email)
    
    Args:
        affiliation_text: Full affiliation string (may contain multiple affiliations separated by |)
        target_countries: List of countries to filter by (optional)
    
    Returns:
        Dictionary with all parsed fields or None if email missing
    """
    if not affiliation_text:
        return None
    
    # Step 1: Split affiliations by " | " separator
    affiliations = affiliation_text.split(' | ')
    
    # Step 2: Find the PRIMARY affiliation (the one containing the email)
    primary_affiliation = None
    email = None
    
    for aff in affiliations:
        email = extract_email(aff)
        if email:
            primary_affiliation = aff
            break  # Use the first affiliation with email
    
    # If no email found in any affiliation, skip this author
    if not email or not primary_affiliation:
        return None
    
    # Step 3: Extract ALL fields from the PRIMARY affiliation only
    state = extract_state(primary_affiliation)
    city = extract_city(primary_affiliation)
    postal_code = extract_postal_code(primary_affiliation)
    country = extract_country(primary_affiliation)
    
    # If country not found, try to infer from state or city
    if not country:
        country = infer_country_from_location(primary_affiliation, state, city)

    # Filter by target countries if specified
    if target_countries and country not in target_countries:
        return None
    
    # Extract location details from primary affiliation
    state = extract_state(primary_affiliation)
    city = extract_city(primary_affiliation)
    postal_code = extract_postal_code(primary_affiliation)
    
    # Extract specialty and therapy area from primary affiliation
    specialty = extract_specialty(primary_affiliation)
    therapy_area = extract_therapy_area(primary_affiliation, specialty)
    subspecialty = extract_subspecialty(primary_affiliation, specialty)
    institution = extract_institution(primary_affiliation)
    
    return {
        'email': email,
        'country': country if country else 'Unknown',
        'state': state if state else '',
        'city': city if city else '',
        'postal_code': postal_code if postal_code else '',
        'therapy_area': therapy_area,
        'specialty': specialty if specialty else 'Not specified',
        'subspecialty': subspecialty if subspecialty else 'Not specified',
        'institution': institution if institution else primary_affiliation[:100]
    }