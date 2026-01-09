from Bio import Entrez

def initialize_entrez(email, api_key=""):
    """Initialize Entrez with email and optional API key"""
    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key

def build_query_with_dates(base_query, date_config):
    """
    Add date range filter to the query if enabled
    
    Args:
        base_query: Base search query
        date_config: Date configuration dictionary
    
    Returns:
        Complete query with date filter
    """
    if not date_config or not date_config.get('enabled', False):
        return base_query
    
    start_date = date_config.get('start_date', '')
    end_date = date_config.get('end_date', '')
    date_type = date_config.get('date_type', 'pdat')  # pdat = publication date, edat = entry date
    
    if not start_date or not end_date:
        return base_query
    
    # Format: "YYYY/MM/DD"[DateType] : "YYYY/MM/DD"[DateType]
    date_filter = f'("{start_date}"[{date_type}] : "{end_date}"[{date_type}])'
    
    # Add to query
    complete_query = f"({base_query}) AND {date_filter}"
    
    return complete_query