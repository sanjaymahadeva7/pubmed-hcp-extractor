"""
Logger Module
Creates detailed log files of extraction process
Cloud-safe and Windows-safe
"""
from datetime import datetime
import os

class ExtractionLogger:
    def __init__(self, log_filename='logs/extraction_log.txt'):
        self.log_filename = log_filename
        self.log_file = None
        
    def start_logging(self, config):
        """Start logging session with configuration details"""

        # Create directory if it exists in path
        log_dir = os.path.dirname(self.log_filename)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        self.log_file = open(self.log_filename, 'w', encoding='utf-8')

        # Header
        self.write_separator("=")
        self.log("PUBMED CONTACT EXTRACTION LOG")
        self.log(f"Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.write_separator("=")

        # Configuration
        self.log("\nCONFIGURATION:")
        self.log(f"  Search Query: {config['search_query']}")

        if config.get('date_range', {}).get('enabled', False):
            date_config = config['date_range']
            self.log(f"  Date Range: {date_config['start_date']} to {date_config['end_date']}")
        else:
            self.log("  Date Range: All dates")

        self.log(f"  Target Countries: {', '.join(config['target_countries']) if config['target_countries'] else 'All'}")
        self.log(f"  Results Range: {config['start_result']} to {config['end_result']}")
        self.log(f"  Email Required: {config['email_required']}")
        self.log(f"  Output File: {config['output_filename']}")
        self.log("")

    def log(self, message):
        if self.log_file:
            self.log_file.write(message + "\n")
            self.log_file.flush()

    def write_separator(self, char="-", length=80):
        self.log(char * length)

    def log_search_results(self, pmid_count, total_available):
        self.write_separator()
        self.log("SEARCH RESULTS:")
        self.log(f"  PMIDs Retrieved: {pmid_count}")
        self.log(f"  Total Available: {total_available}")
        self.log("")

    def log_paper_processing_start(self, total_papers):
        self.write_separator()
        self.log(f"PROCESSING {total_papers} PAPERS:")
        self.log("")

    def log_paper_details(self, paper_num, total_papers, metadata, authors_count):
        self.log(f"\n[Paper {paper_num}/{total_papers}]")
        self.log(f"  PMID: {metadata.get('pmid', 'N/A')}")
        self.log(f"  Title: {metadata.get('title', 'N/A')[:100]}")
        self.log(f"  Journal: {metadata.get('journal', 'N/A')}")
        self.log(f"  DOI: {metadata.get('doi', 'N/A')}")
        self.log(f"  Authors Found: {authors_count}")

    def log_contact_extracted(self, contact_data, affiliation_text):
        self.log("      CONTACT EXTRACTED:")
        self.log(f"      Name: {contact_data.get('HCPName', 'N/A')}")
        self.log(f"      Email: {contact_data.get('Email ID', 'N/A')}")
        self.log(f"      Country: {contact_data.get('Country', 'N/A')}")
        self.log(f"      State: {contact_data.get('Province/State', 'N/A')}")
        self.log(f"      City: {contact_data.get('City', 'N/A')}")
        self.log(f"      Postal Code: {contact_data.get('Postal Code', 'N/A')}")
        self.log(f"      TherapyArea: {contact_data.get('TherapyArea', 'N/A')}")
        self.log(f"      Specialty: {contact_data.get('Specialty', 'N/A')}")
        self.log(f"      Sub-Specialty: {contact_data.get('Sub-Specialty', 'N/A')}")
        self.log(f"      Institution: {str(contact_data.get('Affiliation/Institution', 'N/A'))[:80]}")
        self.log(f"      Publication Date: {contact_data.get('Date', 'N/A')}")
        self.log(f"      Paper Title: {str(contact_data.get('Title', 'N/A'))[:100]}")
        self.log(f"      ProfileURL: {contact_data.get('ProfileURL', 'N/A')}")
        self.log(f"      Full Affiliation: {affiliation_text[:150]}")

    def log_contact_skipped(self, author_name, reason):
        self.log(f"    SKIPPED: {author_name} - {reason}")

    def log_extraction_summary(self, stats):
        self.write_separator("=")
        self.log("\nEXTRACTION SUMMARY:")
        self.write_separator("-")
        self.log(f"  Total Papers Processed: {stats.get('papers_processed', 0)}")
        self.log(f"  Papers with Contacts: {stats.get('papers_with_contacts', 0)}")
        self.log(f"  Total Contacts Extracted: {stats.get('total_contacts', 0)}")
        self.log(f"  Total Authors Checked: {stats.get('total_authors_checked', 0)}")
        self.log(f"  Skipped No Email: {stats.get('skipped_no_email', 0)}")
        self.log(f"  Skipped Country: {stats.get('skipped_country', 0)}")
        self.log(f"  Skipped No Affiliation: {stats.get('skipped_no_affiliation', 0)}")

        if stats.get('country_breakdown'):
            self.log("\n  Contacts by Country:")
            for country, count in stats['country_breakdown'].items():
                self.log(f"    {country}: {count}")

        if stats.get('specialty_breakdown'):
            self.log("\n  Contacts by Specialty:")
            for specialty, count in stats['specialty_breakdown'].items():
                self.log(f"    {specialty}: {count}")

        self.log(f"\nExecution Time: {stats.get('execution_time', 'N/A')}")
        self.log(f"Output File: {stats.get('output_file', 'N/A')}")
        self.write_separator("=")
        self.log(f"Session Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.write_separator("=")

    def close(self):
        if self.log_file:
            self.log_file.close()
            print(f"Log saved: {self.log_filename}")
