import re

# Generic pattern for: City, State, Country
GENERIC_STATE_PATTERN = re.compile(r',\s*([A-Z][a-zA-Z\s\-]+?)\s*,\s*[A-Z][a-zA-Z\s]+$')

def extract_generic_state(text, country):
    match = GENERIC_STATE_PATTERN.search(text)
    if match:
        return match.group(1).strip()
    return ""
