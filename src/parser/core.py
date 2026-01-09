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