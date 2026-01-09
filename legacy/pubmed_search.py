"""
PubMed Search Module
Handles all PubMed API interactions
"""
from Bio import Entrez
import time
import json
import re

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


def extract_paper_metadata(paper, specialty=None):
    """
    Extract basic metadata from a paper record including MeSH terms and keywords
    
    Args:
        paper: PubMed paper record
        specialty: The specialty of the author (optional, used for filtering keywords)
    
    Returns:
        Dictionary with paper metadata
    """
    try:
        article = paper['MedlineCitation']['Article']
        medline = paper['MedlineCitation']
        
        # PubMed ID
        pmid = str(medline['PMID'])
        
        # Title
        title = article.get('ArticleTitle', 'N/A')
        
        # Journal
        journal = article['Journal']['Title'] if 'Journal' in article else 'N/A'
        
        # DOI
        doi = 'N/A'
        if 'ELocationID' in article:
            for eloc in article['ELocationID']:
                if eloc.attributes.get('EIdType') == 'doi':
                    doi = str(eloc)
                    break
        
        # Publication date
        pub_date = extract_publication_date(article)
        
        # Extract MeSH terms
        mesh_terms = []
        if 'MeshHeadingList' in medline:
            for mesh in medline['MeshHeadingList']:
                if 'DescriptorName' in mesh:
                    mesh_terms.append(str(mesh['DescriptorName']))
        
        # Extract Keywords
        keywords = []
        if 'KeywordList' in medline:
            for keyword_list in medline['KeywordList']:
                for keyword in keyword_list:
                    keywords.append(str(keyword))
        
        # Store raw keywords and mesh terms for later specialty-specific filtering
        return {
            'pmid': pmid,
            'title': title,
            'journal': journal,
            'doi': doi,
            'pub_date': pub_date,
            'mesh_terms': mesh_terms,
            'keywords': keywords
        }
    
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def filter_keywords_by_specialty(mesh_terms, keywords, specialty):
    """
    Filter keywords to only include those relevant to the given specialty
    
    Args:
        mesh_terms: List of MeSH terms from paper
        keywords: List of keywords from paper
        specialty: The specialty to filter by (e.g., 'Cardiology')
    
    Returns:
        String of relevant keywords (max 3)
    """
    if not specialty or specialty == 'Not specified':
        return ''
    
    # Define specialty-specific relevant keywords/terms
    specialty_keywords = {
        'Cardiology': [
            'cardiac', 'cardio', 'heart', 'coronary', 'myocardial', 'atrial', 'ventricular',
            'arrhythmia', 'echocardiography', 'angiography', 'stenosis', 'ischemia', 'infarction',
            'hypertension', 'atherosclerosis', 'valve', 'pacemaker', 'stent', 'catheterization',
            'ejection fraction', 'ecg', 'electrocardiogram', 'chest pain', 'angina', 'pericardial',
            'aortic', 'mitral', 'tricuspid', 'pulmonary', 'endocarditis', 'cardiomyopathy',
            'heart failure', 'tachycardia', 'bradycardia', 'fibrillation', 'flutter'
        ],
        'Neurology': [
            'neuro', 'brain', 'cerebral', 'cortical', 'cognitive', 'alzheimer', 'parkinson',
            'stroke', 'seizure', 'epilepsy', 'migraine', 'dementia', 'neuropathy', 'encephalopathy',
            'meningitis', 'sclerosis', 'spinal', 'motor', 'sensory', 'paralysis', 'tremor'
        ],
        'Oncology': [
            'cancer', 'tumor', 'tumour', 'carcinoma', 'malignancy', 'metastasis', 'chemotherapy',
            'radiation', 'oncology', 'neoplasm', 'lymphoma', 'leukemia', 'sarcoma', 'biopsy',
            'staging', 'prognosis', 'survival'
        ],
        'Pediatrics': [
            'pediatric', 'paediatric', 'child', 'infant', 'neonatal', 'adolescent', 'growth',
            'development', 'congenital', 'childhood'
        ],
        'Psychiatry': [
            'psychiatric', 'mental', 'depression', 'anxiety', 'psychosis', 'bipolar', 'schizophrenia',
            'mood', 'behavioral', 'cognitive therapy', 'antidepressant', 'psychotherapy'
        ],
        'Surgery': [
            'surgical', 'operation', 'operative', 'laparoscopic', 'resection', 'anastomosis',
            'procedure', 'incision', 'suture', 'postoperative', 'preoperative'
        ],
        'Nephrology': [
            'kidney', 'renal', 'dialysis', 'glomerular', 'nephropathy', 'creatinine', 'uremia',
            'transplant', 'filtration'
        ],
        'Gastroenterology': [
            'gastro', 'intestinal', 'digestive', 'liver', 'hepatic', 'colon', 'bowel', 'stomach',
            'esophageal', 'pancreatic', 'gallbladder', 'cirrhosis', 'endoscopy', 'colonoscopy'
        ],
        'Pulmonology': [
            'pulmonary', 'lung', 'respiratory', 'breathing', 'asthma', 'copd', 'pneumonia',
            'bronchial', 'ventilation', 'oxygen', 'airway'
        ],
        'Endocrinology': [
            'endocrine', 'diabetes', 'thyroid', 'hormone', 'insulin', 'glucose', 'metabolic',
            'pituitary', 'adrenal', 'pancreas'
        ],
        'Rheumatology': [
            'rheumatoid', 'arthritis', 'joint', 'inflammatory', 'autoimmune', 'lupus',
            'connective tissue', 'musculoskeletal'
        ],
        'Hematology': [
            'hematology', 'blood', 'anemia', 'coagulation', 'platelet', 'hemoglobin',
            'thrombosis', 'leukemia', 'lymphoma'
        ]
    }
    
    # Get relevant keywords for this specialty
    relevant_terms = specialty_keywords.get(specialty, [])
    if not relevant_terms:
        return ''
    
    # Combine all keywords and mesh terms
    all_terms = mesh_terms + keywords
    
    # Filter to only relevant ones
    filtered = []
    for term in all_terms:
        term_lower = term.lower()
        # Check if term contains any of the specialty-relevant keywords
        for relevant_keyword in relevant_terms:
            pattern = r'\b' + re.escape(relevant_keyword) + r'\b'
            if re.search(pattern,term_lower):
                # Skip generic research terms
                if not any(generic in term_lower for generic in ['artificial intelligence', 'machine learning', 
                                                                  'deep learning', 'neural network', 'llm',
                                                                  'retrospective', 'prospective', 'cohort',
                                                                  'male', 'female', 'adult', 'human', 'humans',
                                                                  'aged', 'middle aged', 'young adult']):
                    filtered.append(term)
                    break
    
    # Remove duplicates and limit to top 3
    unique_filtered = list(dict.fromkeys(filtered))[:2]
    
    return ', '.join(unique_filtered) if unique_filtered else ''


def extract_publication_date(article):
    """
    Extract publication date from various sources in the article
    Returns date in DD/MM/YYYY format
    
    Args:
        article: Article section of PubMed record
    
    Returns:
        Date string in DD/MM/YYYY format
    """
    import calendar
    
    # Month name to number mapping
    month_map = {
        'jan': '01', 'january': '01',
        'feb': '02', 'february': '02',
        'mar': '03', 'march': '03',
        'apr': '04', 'april': '04',
        'may': '05',
        'jun': '06', 'june': '06',
        'jul': '07', 'july': '07',
        'aug': '08', 'august': '08',
        'sep': '09', 'september': '09',
        'oct': '10', 'october': '10',
        'nov': '11', 'november': '11',
        'dec': '12', 'december': '12'
    }
    
    day = '01'
    month = '01'
    year = None
    
    # Try 1: ArticleDate (Electronic publication date - Epub)
    if 'ArticleDate' in article and article['ArticleDate']:
        date_info = article['ArticleDate'][0]
        year = date_info.get('Year', '')
        month_val = date_info.get('Month', '01')
        day = date_info.get('Day', '01')
        
        # Ensure two digits for day and month
        if month_val.isdigit():
            month = month_val.zfill(2)
        else:
            month = month_map.get(month_val.lower(), '01')
        
        day = str(day).zfill(2)
        
        if year:
            return f"{day}/{month}/{year}"
    
    # Try 2: Journal Issue PubDate (Print publication date)
    if 'Journal' in article and 'JournalIssue' in article['Journal']:
        journal_issue = article['Journal']['JournalIssue']
        if 'PubDate' in journal_issue:
            pub_date = journal_issue['PubDate']
            
            year = pub_date.get('Year', '')
            month_val = pub_date.get('Month', '')
            day = pub_date.get('Day', '01')
            
            # Handle month
            if month_val:
                if month_val.isdigit():
                    month = month_val.zfill(2)
                else:
                    month = month_map.get(month_val.lower(), '01')
            else:
                month = '01'
            
            # Handle day
            if day:
                day = str(day).zfill(2)
            else:
                day = '01'
            
            if year:
                return f"{day}/{month}/{year}"
            
            # Sometimes date is in MedlineDate format like "2021 Jan-Feb"
            if 'MedlineDate' in pub_date:
                medline_date = pub_date['MedlineDate']
                # Extract year (first 4 digits)
                year_match = re.search(r'\b(19|20)\d{2}\b', medline_date)
                if year_match:
                    year = year_match.group(0)
                    
                    # Try to extract month
                    for month_name, month_num in month_map.items():
                        if month_name in medline_date.lower():
                            month = month_num
                            break
                    
                    return f"{day}/{month}/{year}"
    
    # Try 3: DateCompleted or DateRevised
    citation = article.get('MedlineCitation', article)
    for date_field in ['DateCompleted', 'DateRevised', 'DateCreated']:
        if date_field in citation:
            date_info = citation[date_field]
            year = date_info.get('Year', '')
            month = date_info.get('Month', '01').zfill(2)
            day = date_info.get('Day', '01').zfill(2)
            
            if year:
                return f"{day}/{month}/{year}"
    
    # If no date found, return N/A
    return 'N/A'

def extract_authors_with_affiliations(paper):
    """
    Extract all authors with their affiliations from a paper.
    Each affiliation becomes a separate row.
    """

    authors_data = []

    try:
        article = paper['MedlineCitation']['Article']

        if 'AuthorList' not in article:
            return authors_data

        for author in article['AuthorList']:
            last_name = author.get('LastName', '')
            fore_name = author.get('ForeName', '')
            initials = author.get('Initials', '')

            if not last_name:
                continue

            full_name = f"{fore_name} {last_name}".strip()
            if not full_name:
                full_name = f"{initials} {last_name}".strip()

            # No affiliation → still create a row
            if 'AffiliationInfo' not in author:
                authors_data.append({
                    'name': full_name,
                    'affiliation': ''
                })
                continue

            for aff in author['AffiliationInfo']:
                if 'Affiliation' in aff:
                    affiliation_text = aff['Affiliation'].strip()

                    if affiliation_text:
                        authors_data.append({
                            'name': full_name,
                            'affiliation': affiliation_text
                        })

    except Exception as e:
        print(f"Error extracting authors: {e}")

    return authors_data
