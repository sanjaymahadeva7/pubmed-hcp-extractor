from Bio import Entrez

def search_pubmed(query, start_result=1, end_result=100):
    """
    Search PubMed and return list of PubMed IDs
    
    Args:
        query: Search query string
        start_result: Starting result number (1-indexed)
        end_result: Ending result number (inclusive)
    
    Returns:
        List of PubMed IDs
    """
    print(f"Searching PubMed for: {query}")
    print(f"Fetching results {start_result} to {end_result}")
    
    # PubMed API limit warning
    if start_result > 9999:
        print("\n⚠️  WARNING: PubMed API has a hard limit of 10,000 results (max index 9999)")
        print("⚠️  Cannot fetch results beyond position 9999")
        print("⚠️  Try splitting your search by:")
        print("    - Date ranges (e.g., 2020-2024, 2015-2019)")
        print("    - Specific specialties")
        print("    - Recent papers only (RELDATE filter)")
        return []
    
    # Calculate retstart (0-indexed) and retmax
    retstart = start_result - 1  # Convert to 0-indexed
    retmax = end_result - start_result + 1
    
    # Enforce PubMed's 10,000 limit
    if retstart + retmax > 10000:
        original_end = end_result
        retmax = 10000 - retstart
        end_result = start_result + retmax - 1
        print(f"\n⚠️  WARNING: Adjusted end_result from {original_end} to {end_result}")
        print(f"⚠️  PubMed API cannot return results beyond position 9999")
    
    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retstart=retstart,
            retmax=retmax,
            sort="relevance"
        )
        results = Entrez.read(handle)
        handle.close()
        
        id_list = results["IdList"]
        total_count = int(results.get("Count", 0))
        
        print(f"Found {len(id_list)} papers (Total available: {total_count})")
        
        if total_count > 10000:
            print(f"\n💡 TIP: Your search has {total_count} total papers")
            print(f"💡 But PubMed API can only access the first 10,000")
            print(f"💡 Consider refining your search or splitting by date ranges")
        
        return id_list
    
    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []