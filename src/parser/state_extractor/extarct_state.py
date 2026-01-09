from .north_america import extract_na_state
from .asia import extract_asia_state
from .europe import extract_europe_state
from .south_america import extract_sa_state
from .generic import extract_generic_state


def extract_state(text, country):

    if not text or not country:
        return ""

    for extractor in (
        extract_na_state,
        extract_asia_state,
        extract_europe_state,
        extract_sa_state,
        extract_generic_state
    ):
        state = extractor(text, country)
        if state:
            return state

    return ""
