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