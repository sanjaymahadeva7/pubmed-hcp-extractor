from Bio import Entrez
import time

def fetch_paper_details(pmid_list, batch_size=100):
    """
    Fetch detailed information for list of PubMed IDs
    
    Args:
        pmid_list: List of PubMed IDs
        batch_size: Number of papers to fetch per request
    
    Returns:
        List of paper records
    """
    all_papers = []
    total = len(pmid_list)
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = pmid_list[i:i+batch_size]
        print(f"Fetching papers {i+1} to {min(i+batch_size, total)} of {total}...")
        
        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=batch,
                rettype="medline",
                retmode="xml"
            )
            records = Entrez.read(handle)
            handle.close()
            
            all_papers.extend(records['PubmedArticle'])
            
            # Be nice to NCBI servers
            time.sleep(0.34)  # ~3 requests per second
            
        except Exception as e:
            print(f"Error fetching batch {i//batch_size + 1}: {e}")
            continue
    
    print(f"Successfully fetched {len(all_papers)} papers")
    return all_papers