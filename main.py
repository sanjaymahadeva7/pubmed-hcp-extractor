"""
Main Execution File
Orchestrates the entire PubMed extraction pipeline
"""
import json
from datetime import datetime
from src.pubmed_search.core import initialize_entrez, build_query_with_dates
from src.pubmed_search.search import search_pubmed
from src.pubmed_search.fetch import fetch_paper_details
from src.pubmed_search.metadata import extract_paper_metadata, filter_keywords_by_specialty
from src.pubmed_search.authors import extract_authors_with_affiliations

from src.parser.parser import parse_affiliation
from src.parser.core import extract_email
from src.excel_export import create_excel_report, print_summary_statistics
from src.logger import ExtractionLogger


def load_config(config_path='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        print(f"Error: {config_path} not found!")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {config_path}")
        return None

def process_papers(papers, paper_metadata_list, target_countries, email_required=True, logger=None):
    """
    Process all papers and extract author contact information
    
    Args:
        papers: List of PubMed paper records
        paper_metadata_list: List of paper metadata
        target_countries: List of countries to filter
        email_required: Whether email is mandatory
        logger: ExtractionLogger instance
    
    Returns:
        Tuple of (contacts_list, statistics_dict)
    """
    all_contacts = []
    papers_processed = 0
    papers_with_contacts = 0
    
    # Statistics tracking
    stats = {
        'total_authors_checked': 0,
        'skipped_no_email': 0,
        'skipped_country': 0,
        'skipped_no_affiliation': 0,
        'country_breakdown': {},
        'specialty_breakdown': {}
    }
    
    print("\n" + "="*60)
    print("PROCESSING PAPERS AND EXTRACTING CONTACTS")
    print("="*60)
    
    if logger:
        logger.log_paper_processing_start(len(papers))
    
    for paper, metadata in zip(papers, paper_metadata_list):
        papers_processed += 1
        
        if papers_processed % 10 == 0:
            print(f"Processed {papers_processed}/{len(papers)} papers... Found {len(all_contacts)} contacts so far")
        
        # Extract authors with affiliations
        authors = extract_authors_with_affiliations(paper)
        
        if logger:
            logger.log_paper_details(papers_processed, len(papers), metadata, len(authors))
        
        if not authors:
            continue
        
        paper_has_contacts = False
        
        # Process each author
        for author in authors:
            stats['total_authors_checked'] += 1
            
            if not author['affiliation']:
                stats['skipped_no_affiliation'] += 1
                if logger:
                    logger.log_contact_skipped(author['name'], "No affiliation")
                continue
            
            # Parse affiliation
            parsed = parse_affiliation(
                author['affiliation'],
                target_countries=target_countries if target_countries else None
            )
            
            # Skip if no email and email is required
            if not parsed:
                if not extract_email(author['affiliation']):
                    stats['skipped_no_email'] += 1
                    if logger:
                        logger.log_contact_skipped(author['name'], "No email")
                else:
                    stats['skipped_country'] += 1
                    if logger:
                        logger.log_contact_skipped(author['name'], "Country filter")
                continue
            
            if email_required and not parsed.get('email'):
                stats['skipped_no_email'] += 1
                if logger:
                    logger.log_contact_skipped(author['name'], "No email")
                continue
            
            # Get the specialty from parsed affiliation
            author_specialty = parsed['specialty']
            
            # Filter keywords based on author's specialty
            filtered_expertise = filter_keywords_by_specialty(
                metadata.get('mesh_terms', []),
                metadata.get('keywords', []),
                author_specialty
            )
            
            # Create contact record
            contact = {
                'HCPName': author['name'],
                'Country': parsed['country'],
                'Province/State': parsed['state'],
                'City': parsed['city'],
                'Postal Code': parsed['postal_code'],
                'Email ID': parsed['email'],
                'TherapyArea': parsed.get('therapy_area', ''),
                'Specialty': parsed['specialty'],
                'Sub-Specialty': parsed['subspecialty'],
                'Areas Of Expertise': filtered_expertise,
                'Affiliation/Institution': parsed['institution'],
                'ProfileURL': f"https://pubmed.ncbi.nlm.nih.gov/?term={author['name'].replace(' ', '+')}&cauthor_id={metadata['pmid']}",
                'PublicationLinks': f"PMID: {metadata['pmid']} | https://pubmed.ncbi.nlm.nih.gov/{metadata['pmid']}/",
                'Date': metadata.get('pub_date', 'N/A'),
                'Title': metadata.get('title', 'N/A')
            }
            
            all_contacts.append(contact)
            paper_has_contacts = True
            
            # Track statistics
            country = parsed['country']
            specialty = parsed['specialty']
            stats['country_breakdown'][country] = stats['country_breakdown'].get(country, 0) + 1
            stats['specialty_breakdown'][specialty] = stats['specialty_breakdown'].get(specialty, 0) + 1
            
            # Log extracted contact (after contact is fully created)
            if logger:
                logger.log_contact_extracted(contact, author['affiliation'])
        
        if paper_has_contacts:
            papers_with_contacts += 1
    
    print(f"\nProcessing complete!")
    print(f"Papers processed: {papers_processed}")
    print(f"Papers with contacts: {papers_with_contacts}")
    print(f"Total contacts extracted: {len(all_contacts)}")
    
    # Update stats
    stats['papers_processed'] = papers_processed
    stats['papers_with_contacts'] = papers_with_contacts
    stats['total_contacts'] = len(all_contacts)
    
    return all_contacts, stats

def main():
    """Main execution function"""
    start_time = datetime.now()
    
    print("\n" + "="*60)
    print("PUBMED CONTACT EXTRACTOR")
    print("="*60)
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # Initialize logger
    log_filename = config.get('log_filename', 'extraction_log.txt')
    logger = ExtractionLogger(log_filename)
    logger.start_logging(config)
    
    # Display configuration
    print("\nConfiguration:")
    print(f"  Search Query: {config['search_query']}")
    
    # Show date range if enabled
    if config.get('date_range', {}).get('enabled', False):
        date_config = config['date_range']
        print(f"  Date Range: {date_config['start_date']} to {date_config['end_date']}")
        date_type_name = "Publication Date" if date_config.get('date_type') == 'pdat' else "Entry Date"
        print(f"  Date Type: {date_type_name}")
    else:
        print(f"  Date Range: All dates")
    
    print(f"  Target Countries: {', '.join(config['target_countries']) if config['target_countries'] else 'All countries'}")
    print(f"  Results Range: {config['start_result']} to {config['end_result']}")
    print(f"  Email Required: {config['email_required']}")
    print(f"  Output File: {config['output_filename']}")
    print(f"  Log File: {log_filename}")
    
    # Initialize Entrez
    initialize_entrez(
        email=config['ncbi_email'],
        api_key=config.get('ncbi_api_key', '')
    )
    
    # Build complete query with date filter
    complete_query = build_query_with_dates(
        config['search_query'],
        config.get('date_range', {})
    )
    
    # Step 1: Search PubMed
    print("\n" + "="*60)
    print("STEP 1: SEARCHING PUBMED")
    print("="*60)
    pmid_list = search_pubmed(
        query=complete_query,
        start_result=config['start_result'],
        end_result=config['end_result']
    )
    
    if not pmid_list:
        print("No papers found! Exiting.")
        logger.log("\nERROR: No papers found in search results")
        logger.close()
        return
    
    logger.log_search_results(len(pmid_list), len(pmid_list))
    
    # Step 2: Fetch paper details
    print("\n" + "="*60)
    print("STEP 2: FETCHING PAPER DETAILS")
    print("="*60)
    papers = fetch_paper_details(pmid_list)
    
    if not papers:
        print("Failed to fetch paper details! Exiting.")
        logger.log("\nERROR: Failed to fetch paper details")
        logger.close()
        return
    
    # Extract metadata for all papers
    paper_metadata_list = []
    for paper in papers:
        metadata = extract_paper_metadata(paper)
        if metadata:
            paper_metadata_list.append(metadata)
    
    # Step 3: Process papers and extract contacts
    contacts, stats = process_papers(
        papers=papers,
        paper_metadata_list=paper_metadata_list,
        target_countries=config.get('target_countries', None),
        email_required=config['email_required'],
        logger=logger
    )
    
    if not contacts:
        print("\n⚠ No contacts found matching criteria!")
        print("Try:")
        print("  - Broadening search query")
        print("  - Removing country filters")
        print("  - Increasing end_result")
        
        logger.log("\nWARNING: No contacts found matching criteria")
        logger.close()
        return
    
    # Step 4: Create Excel report
    print("\n" + "="*60)
    print("STEP 4: GENERATING EXCEL REPORT")
    print("="*60)
    output_file = create_excel_report(
        data_list=contacts,
        output_filename=config['output_filename']
    )
    
    # Print summary statistics
    print_summary_statistics(contacts)
    
    # Calculate execution time
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds() / 60
    
    # Log final summary
    stats['execution_time'] = f"{execution_time:.2f} minutes"
    stats['output_file'] = output_file
    logger.log_extraction_summary(stats)
    logger.close()
    
    print("\n" + "="*60)
    print("EXTRACTION COMPLETE!")
    print("="*60)
    print(f"\nExcel file saved: {output_file}")
    print(f"Log file saved: {log_filename}")
    print(f"Total contacts: {len(contacts)}")
    print(f"Execution time: {execution_time:.2f} minutes")
    print("\nYou can now open the Excel file to view all contacts.")
    print("Check the log file for detailed extraction information.")

if __name__ == "__main__":
    main()