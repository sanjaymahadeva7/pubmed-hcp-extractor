import re

def extract_institution(affiliation_text):
    """
    Extract main institution/university name from affiliation
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Institution name or full affiliation if can't parse
    """
    if not affiliation_text:
        return None
    
    # Remove email if present
    clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', affiliation_text)
    
    # Expanded institution keywords (US + Germany + Spain + Italy + France + UK)
    institution_keywords = [
        # English (US, UK, global)
        'University','College','Institute','Hospital','Medical Center','Medical Centre','Clinic',
        'School of Medicine','Medical School','Health Sciences','Faculty of Medicine','Faculty of Health',
        'Academic Medical Center','Teaching Hospital','University Hospital',

        # Germany
        'Universität','Universitaet','Klinik','Klinikum','Universitätsklinikum','Universitaetsklinikum',
        'Hochschule','Fakultät','Fakultaet','Institut','Zentrum','Medizinische Hochschule',
        'Charité','Charite','Universitätsmedizin','Universitaetsmedizin',

        # France
        'Université','Universite','Hôpital','Hopital','Centre Hospitalier','CHU',
        'Institut','Faculté','Faculte','Assistance Publique','Hôpitaux','Hopitaux',
        'Centre de Recherche','Inserm','CNRS','Institut Pasteur',

        # Spain
        'Universidad','Hospital','Centro','Centro Médico','Centro Medico',
        'Instituto','Clínica','Clinica','Facultad','Servicio de','Departamento de',
        'Complejo Hospitalario','Hospital Universitario',

        # Italy
        'Università','Universita','Ospedale','Policlinico','Istituto','Clinica',
        'Azienda Ospedaliera','IRCCS','Fondazione','Dipartimento','Centro',

        # UK specific
        'NHS','Trust','Foundation Trust','Royal','King’s College','Kings College',
        'Imperial College','University College London','UCL','Guy’s','St Thomas’',
        'Great Ormond Street','Oxford','Cambridge'
    ]
    
    # Try to find institution name
    for keyword in institution_keywords:
        pattern = r'([^,\.;]+' + re.escape(keyword) + r'[^,\.;]*)'
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # If no specific institution found, return first part before comma
    parts = clean_text.split(',')
    if parts:
        return parts[0].strip()
    
    return clean_text.strip()