from .city_validator import is_valid_city
from .asia import extract_asia_city
from .europe import extract_europe_city
from .north_america import extract_north_america_city
from .south_america import extract_south_america_city
from .oceania import extract_oceania_city
from .generic import extract_generic_city



def extract_city(text, country):
    if not text or not country:
        return ""

    for extractor in (
        extract_asia_city,
        extract_europe_city,
        extract_north_america_city,
        extract_south_america_city,
        extract_oceania_city,
        extract_generic_city,
    ):
        city = extractor(text, country, is_valid_city)
        if city:
            return city

    return ""
