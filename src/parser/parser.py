from src.parser.core import extract_email, infer_country_from_location
from src.parser.state_extractor.extarct_state import extract_state
from src.parser.city_extractor.extract_city import extract_city
from src.parser.extract_country import extract_country
from src.parser.extract_postal_code import  extract_postal_code
from src.parser.medical import extract_specialty, extract_therapy_area, extract_subspecialty
from src.parser.institution import extract_institution


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
    
    # Step 3: Extract country FIRST
    country = extract_country(primary_affiliation)
    
    # Step 4: If country not found, try to infer it
    if not country:
        # Extract preliminary city/state for inference
        temp_state = extract_state(primary_affiliation, None)
        temp_city = extract_city(primary_affiliation, None)
        country = infer_country_from_location(primary_affiliation, temp_state, temp_city)
    
    # Step 5: Filter by target countries if specified
    if target_countries and country not in target_countries:
        return None
    
    # Step 6: Now extract all fields using the confirmed country
    state = extract_state(primary_affiliation, country)
    city = extract_city(primary_affiliation, country)
    postal_code = extract_postal_code(primary_affiliation)
    
    # Step 7: Validate location consistency (optional - comment out if function not implemented)
    # if state and city:
    #     if not validate_location_consistency(country, state, city):
    #         state = ''  # Clear inconsistent data
    
    # Step 8: Extract medical/institution details
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