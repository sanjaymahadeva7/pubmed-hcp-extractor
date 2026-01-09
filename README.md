# PubMed Contact Extractor

A Python-based automated tool to extract researcher contact information (names, emails, affiliations, specialties) from PubMed publications. Perfect for building research collaboration networks, academic outreach, and finding subject matter experts.

---

## 📋 Table of Contents

- [Features]
- [Requirements]
- [Installation]
- [Project Structure]
- [Configuration]
- [Usage]
- [Output Files]
- [Advanced Usage]
- [Troubleshooting]
- [FAQ]
- [License]

---

## ✨ Features

- ✅ **Automated PubMed Search** - Query PubMed with custom search terms
- ✅ **Email Extraction** - Mandatory email extraction from author affiliations
- ✅ **Country Filtering** - Filter contacts by specific countries
- ✅ **Date Range Support** - Search papers within specific date ranges
- ✅ **Specialty Detection** - Automatic specialty and sub-specialty identification
- ✅ **Excel Export** - Formatted Excel output with all contact details
- ✅ **Detailed Logging** - Complete extraction log with paper and contact details
- ✅ **Free to Use** - Uses free PubMed API (no costs involved)
- ✅ **Batch Processing** - Handle large searches by splitting into batches
- ✅ **Progress Tracking** - Real-time progress updates during extraction

---

## 📦 Requirements

### System Requirements
- **Python 3.7 or higher**
- Internet connection (for PubMed API access)
- 50MB free disk space

### Python Libraries
All dependencies are listed in `requirements.txt`:
- `biopython` - PubMed API interaction
- `pandas` - Data manipulation
- `openpyxl` - Excel file generation
- `requests` - HTTP requests

---

## 🚀 Installation

### Step 1: Install Python
Make sure you have Python 3.7+ installed:
```bash
python --version
```

### Step 2: Download the Project
Download all project files to a folder:
```
pubmed_extractor/
├── main.py
├── config.json
├── pubmed_search.py
├── parser.py
├── excel_export.py
├── logger.py
├── requirements.txt
└── README.md
```

### Step 3: Install Dependencies
Open terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Search
Edit `config.json` with your search parameters (see [Configuration] section)

### Step 5: Run the Extractor
```bash
python main.py
```

---

## 📁 Project Structure

### Core Files

| File | Purpose |
|------|---------|
| **main.py** | Main execution file - orchestrates the entire pipeline |
| **config.json** | Configuration file - all search parameters |
| **pubmed_search.py** | Handles PubMed API interactions and paper fetching |
| **parser.py** | Parses affiliations to extract emails, countries, specialties |
| **excel_export.py** | Generates formatted Excel reports |
| **eproject_details** | Generates Project details(can be used for other files also) |
| **logger.py** | Creates detailed extraction logs |
| **requirements.txt** | Python dependencies list |
| **README.md** | This documentation file |

### Generated Files

| File | Description |
|------|-------------|
| **pubmed_contacts.xlsx** | Excel file with extracted contacts |
| **extraction_log.txt** | Detailed log of extraction process |

---

## ⚙️ Configuration

Edit `config.json` to customize your extraction:

### Basic Configuration

```json
{
  "search_query": "Cardiology AND India",
  "target_countries": ["India", "USA", "UK"],
  "start_result": 1,
  "end_result": 100,
  "email_required": true,
  "output_filename": "pubmed_contacts.xlsx",
  "log_filename": "extraction_log.txt",
  "ncbi_email": "your_email@example.com",
  "ncbi_api_key": ""
}
```

### Configuration Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search_query` | string | PubMed search query | `"Cardiology AND USA"` |
| `target_countries` | list | Countries to filter (empty = all) | `["USA", "UK", "India"]` |
| `start_result` | integer | Starting result number (1-indexed) | `1` |
| `end_result` | integer | Ending result number | `100` |
| `email_required` | boolean | Only extract contacts with emails | `true` |
| `output_filename` | string | Name of output Excel file | `"contacts.xlsx"` |
| `log_filename` | string | Name of log file | `"extraction_log.txt"` |
| `ncbi_email` | string | Your email (required by NCBI) | `"user@email.com"` |
| `ncbi_api_key` | string | NCBI API key (optional, for faster access) | `""` |

### Date Range Configuration (Optional)

```json
{
  "date_range": {
    "enabled": true,
    "start_date": "2020/01/01",
    "end_date": "2024/12/31",
    "date_type": "pdat"
  }
}
```

| Parameter | Options | Description |
|-----------|---------|-------------|
| `enabled` | `true`/`false` | Enable/disable date filtering |
| `start_date` | `YYYY/MM/DD` | Start date of publication range |
| `end_date` | `YYYY/MM/DD` | End date of publication range |
| `date_type` | `pdat`/`edat` | `pdat` = publication date, `edat` = entry date |

---

## 🎯 Usage

### Basic Usage

1. **Edit config.json** with your search parameters
2. **Run the extractor**:
   ```bash
   python main.py
   ```
3. **Check the output**:
   - `pubmed_contacts.xlsx` - Excel file with contacts
   - `extraction_log.txt` - Detailed extraction log

### Example Searches

#### Search by Specialty and Country
```json
{
  "search_query": "Cardiology AND USA",
  "target_countries": ["USA"]
}
```

#### Search by Affiliation Type
```json
{
  "search_query": "\"teaching hospital\"[Affiliation] AND oncology",
  "target_countries": ["USA", "UK"]
}
```

#### Search Recent Papers Only
```json
{
  "search_query": "Neurology AND Canada",
  "date_range": {
    "enabled": true,
    "start_date": "2023/01/01",
    "end_date": "2024/12/31",
    "date_type": "pdat"
  }
}
```

#### Advanced Multi-Criteria Search
```json
{
  "search_query": "(\"academic medical center\"[Affiliation] OR \"teaching hospital\"[Affiliation]) AND (cardiology OR oncology) AND United States[Affiliation]",
  "target_countries": ["USA"],
  "date_range": {
    "enabled": true,
    "start_date": "2020/01/01",
    "end_date": "2024/12/31",
    "date_type": "pdat"
  }
}
```

---

## 📊 Output Files

### Excel File (pubmed_contacts.xlsx)

**Columns:**
1. **Country** - Author's country
2. **Name** - Full name of author
3. **Email ID** - Email address
4. **Specialty** - Medical/research specialty
5. **Sub-Specialty** - More specific specialty
6. **Affiliation/Institution** - University/Hospital name
7. **Source** - PubMed ID and Journal name

**Features:**
- Color-coded header row
- Auto-adjusted column widths
- Sortable data
- Professional formatting

### Log File (extraction_log.txt)

**Contents:**
- Configuration details
- Search results summary
- Each paper processed with:
  - PMID, Title, Journal, DOI
  - Authors found
  - Contacts extracted (✓)
  - Contacts skipped with reasons (✗)
- Final statistics:
  - Total papers processed
  - Total contacts extracted
  - Breakdown by country
  - Breakdown by specialty
  - Execution time

---

## 🔧 Advanced Usage

### Handling Large Searches (>10,000 papers)

PubMed API has a **10,000 result limit**. For larger searches, split by date ranges:

**Batch 1: Recent Papers (2020-2024)**
```json
{
  "search_query": "your query here",
  "date_range": {
    "enabled": true,
    "start_date": "2020/01/01",
    "end_date": "2024/12/31",
    "date_type": "pdat"
  },
  "start_result": 1,
  "end_result": 5000,
  "output_filename": "contacts_2020-2024.xlsx",
  "log_filename": "log_2020-2024.txt"
}
```

**Batch 2: Older Papers (2015-2019)**
```json
{
  "date_range": {
    "start_date": "2015/01/01",
    "end_date": "2019/12/31"
  },
  "output_filename": "contacts_2015-2019.xlsx",
  "log_filename": "log_2015-2019.txt"
}
```

### Getting NCBI API Key (Optional - for faster processing)

**Without API Key:** 3 requests/second
**With API Key:** 10 requests/second (FREE)

**Steps:**
1. Go to https://www.ncbi.nlm.nih.gov/account/
2. Create a free NCBI account
3. Go to Settings → API Key Management
4. Click "Create an API Key"
5. Copy the key to `config.json`:
   ```json
   {
     "ncbi_api_key": "your_api_key_here"
   }
   ```

### Supported Countries

The tool recognizes 50+ countries including:
- USA, UK, India, China, Japan
- Germany, France, Canada, Australia
- Brazil, Italy, Spain, Netherlands
- And many more...

See `parser.py` for complete list or add your own!

### Custom Specialty Keywords

Edit `parser.py` to add custom specialties:
```python
specialties = {
    'Your Specialty': ['keyword1', 'keyword2', 'keyword3'],
    # Add more...
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No papers found"
**Solutions:**
- Check your search query syntax
- Try a broader search term
- Disable date filters temporarily
- Verify internet connection

#### 2. "No contacts found matching criteria"
**Solutions:**
- Remove country filters (set to empty list `[]`)
- Try a broader date range
- Increase `end_result` value
- Check if papers actually have affiliations with emails

#### 3. "Cannot fetch results beyond 9999"
**Solutions:**
- Split search by date ranges
- Use more specific search terms
- Process in multiple batches

#### 4. "Import Error" or "Module not found"
**Solutions:**
```bash
pip install --upgrade -r requirements.txt
```

#### 5. Rate Limit Errors
**Solutions:**
- Get a free NCBI API key (increases limit)
- Reduce batch size
- Add delays between runs

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `config.json not found` | Missing config file | Create config.json in same folder |
| `Invalid JSON` | Syntax error in config | Check JSON formatting |
| `PubMed API error` | Network/API issue | Check internet, try again later |
| `Email not provided` | Missing NCBI email | Add your email to config.json |

---

## ❓ FAQ

### Q: Is this tool free to use?
**A:** Yes! Completely free. Uses PubMed's free public API.

### Q: Do I need a PubMed account?
**A:** No, but providing your email in config is required by NCBI policy.

### Q: How many papers can I process?
**A:** Up to 10,000 per search due to PubMed API limits. Split large searches by date ranges.

### Q: Why are some contacts skipped?
**A:** Common reasons:
- No email in affiliation (email is mandatory)
- Country doesn't match filter
- No affiliation information available

### Q: Can I extract from specific journals?
**A:** Yes! Use: `"Journal Name"[Journal] AND your_query`

### Q: How accurate is specialty detection?
**A:** ~80-90% accurate. Based on department keywords in affiliations.

### Q: Can I customize output columns?
**A:** Yes! Edit `excel_export.py` to modify columns.

### Q: How long does extraction take?
**A:** Approximately:
- 100 papers: 1-2 minutes
- 1000 papers: 10-15 minutes
- 5000 papers: 45-60 minutes

### Q: Can I run multiple extractions in parallel?
**A:** Yes, but respect API rate limits (use API key for better limits).

---

## 📝 Example Workflow

### Complete Example: Extract USA Cardiologists

**Step 1: Configure**
```json
{
  "search_query": "Cardiology AND United States[Affiliation]",
  "target_countries": ["USA"],
  "start_result": 1,
  "end_result": 1000,
  "date_range": {
    "enabled": true,
    "start_date": "2020/01/01",
    "end_date": "2024/12/31",
    "date_type": "pdat"
  },
  "email_required": true,
  "output_filename": "usa_cardiologists_2020-2024.xlsx",
  "log_filename": "extraction_log_cardiology.txt",
  "ncbi_email": "yourname@email.com",
  "ncbi_api_key": ""
}
```

**Step 2: Run**
```bash
python main.py
```

**Step 3: Check Output**
- Open `usa_cardiologists_2020-2024.xlsx`
- Review `extraction_log_cardiology.txt` for details

**Step 4: Repeat for More Papers**
Change `start_result` and `end_result`:
```json
{
  "start_result": 1001,
  "end_result": 2000,
  "output_filename": "usa_cardiologists_batch2.xlsx"
}
```

---

## 🎓 PubMed Query Tips

### Basic Operators
- `AND` - Both terms must be present
- `OR` - Either term can be present
- `NOT` - Exclude terms

### Field Tags
- `[Affiliation]` - Search in author affiliations
- `[Author]` - Search by author name
- `[Journal]` - Search by journal name
- `[Title]` - Search in article titles

### Examples
```
# Multiple specialties
"cardiology OR oncology OR neurology"

# Specific institutions
"Harvard[Affiliation] OR Stanford[Affiliation]"

# Hospital types
"teaching hospital"[Affiliation] AND oncology

# Exclude terms
cardiology NOT pediatric
```

---

## 📞 Support

### Getting Help
1. Check this README thoroughly
2. Review the log file for detailed error information
3. Check PubMed search results manually to verify your query
4. Ensure all dependencies are installed correctly

### Reporting Issues
When reporting issues, include:
- Your `config.json` (remove your email/API key)
- Error messages from console
- Relevant sections from log file
- Python version (`python --version`)

---

## 📄 License

This tool is provided as-is for research and educational purposes. Users are responsible for complying with PubMed's Terms of Service and applicable data privacy laws.

**Important Notes:**
- Respect PubMed API rate limits
- Use extracted data ethically and legally
- Comply with GDPR and other privacy regulations
- Do not use for spam or unsolicited communications

---

## Acknowledgments

- **NCBI/PubMed** - For providing free API access
- **Biopython** - For excellent PubMed integration
- All open-source library contributors

---

## 📈 Version History

### Version 1.0 (Current)
- Initial release
- PubMed search and extraction
- Email-mandatory extraction
- Country filtering
- Date range support
- Excel export
- Detailed logging

---

## Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] config.json edited with your search query
- [ ] Your email added to config.json
- [ ] Run `python main.py`
- [ ] Check output Excel and log files