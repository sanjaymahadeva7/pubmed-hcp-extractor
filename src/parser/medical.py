import re

def extract_therapy_area(affiliation_text, specialty):
    """
    Extract therapy area based on detected specialty.
    Returns specific therapy keyword if found, else empty string.
    """
    if not affiliation_text:
        return ''

    therapy_map = {
        'Oncology': ['oncology','oncology department','division of oncology','medical oncology','radiation oncology','clinical oncology','cancer center','cancer centre','cancer institute','comprehensive cancer center'],
        'Cardiology': ['cardiology','division of cardiology','department of cardiology','cardiovascular medicine','cardiac medicine','heart institute','cardiac sciences','cardiovascular sciences'],
        'Neurology': ['neurology','division of neurology','department of neurology','neurological sciences','neurosciences','clinical neurology'],
        'Endocrinology': ['endocrinology','division of endocrinology','department of endocrinology','metabolism and endocrinology','endocrine medicine'],
        'Gastroenterology': ['gastroenterology','division of gastroenterology','department of gastroenterology','digestive diseases','digestive health','hepatology'],
        'Pulmonology': ['pulmonology','division of pulmonology','department of pulmonology','respiratory medicine','pulmonary medicine','chest medicine'],
        'Nephrology': ['nephrology','division of nephrology','department of nephrology','renal medicine','kidney medicine'],
        'Immunology': ['immunology','division of immunology','department of immunology','clinical immunology','immune sciences'],
        'Dermatology': ['dermatology','division of dermatology','department of dermatology','cutaneous medicine','skin department'],
        'Orthopedics': ['orthopedics','orthopaedics','division of orthopedics','department of orthopedics','orthopedic surgery','musculoskeletal medicine'],
        'Psychiatry': ['psychiatry','division of psychiatry','department of psychiatry','mental health','behavioral health'],
        'Surgery': ['surgery','surgical department','department of surgery','general surgery','surgical sciences'],
        'Pediatrics': ['pediatrics','paediatrics','division of pediatrics','department of pediatrics','child health','pediatric medicine'],
        'Radiology': ['radiology','department of radiology','division of radiology','radiological sciences','medical imaging','diagnostic imaging'],
        'Emergency Medicine': ['emergency medicine','emergency department','acute care','trauma center'],
        'Internal Medicine': ['internal medicine','department of medicine','general medicine'],
        'Family Medicine': ['family medicine','general practice','primary care'],
        'Obstetrics & Gynecology': ['obstetrics and gynecology','ob gyn','ob-gyn','women’s health','maternal health'],
        'Anesthesiology': ['anesthesiology','anaesthesiology','anesthesia','perioperative medicine'],
        'Pathology': ['pathology','department of pathology','pathological sciences','laboratory medicine'],
        'Hematology': ['hematology','haematology','blood disorders'],
        'Rheumatology': ['rheumatology','autoimmune diseases','connective tissue disease'],
        'Infectious Disease': ['infectious disease','infectious diseases','clinical infection'],
        'Urology': ['urology','department of urology','genitourinary medicine'],
        'Ophthalmology': ['ophthalmology','eye institute','vision sciences'],
        'ENT': ['otolaryngology','ear nose throat','head and neck surgery'],
        'Physical Medicine': ['physical medicine','rehabilitation medicine','pm&r'],
        'Genetics': ['genetics','genomic medicine','medical genetics'],
        'Public Health': ['public health','epidemiology','population health','community medicine']
    }


    text = affiliation_text.lower()

    for therapy_area, keywords in therapy_map.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                return therapy_area
            
    return ''


def extract_specialty(affiliation_text):
    """
    Extract specialty from department information in affiliation
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Specialty or None
    """
    if not affiliation_text:
        return None

    # Common department/specialty patterns
    specialties = {
        'Cardiology': ['cardiology', 'cardiovascular medicine', 'cardiac sciences', 'heart institute', 'division of cardiology', 'department of cardiology'],
        'Neurology': ['neurology', 'neurological sciences', 'neurosciences', 'brain sciences', 'department of neurology'],
        'Neurosurgery': ['neurosurgery', 'department of neurosurgery'],
        'Psychiatry': ['psychiatry', 'mental health', 'behavioral health', 'department of psychiatry'],
        'Psychology': ['psychology', 'clinical psychology'],
        'Oncology': ['oncology', 'medical oncology', 'radiation oncology', 'surgical oncology', 'cancer center', 'cancer institute', 'tumor biology'],
        'Hematology': ['hematology', 'haematology', 'blood disorders'],
        'Hematology-Oncology': ['hematology oncology', 'haematology oncology'],
        'Radiation Oncology': ['radiation oncology', 'radiotherapy'],
        'Pediatrics': ['pediatrics', 'paediatrics', 'child health', 'neonatology', 'department of pediatrics'],
        'Neonatology': ['neonatology', 'newborn medicine'],
        'Surgery': ['surgery', 'general surgery', 'surgical sciences', 'department of surgery'],
        'Cardiothoracic Surgery': ['cardiothoracic surgery', 'heart surgery', 'thoracic surgery'],
        'Vascular Surgery': ['vascular surgery'],
        'Plastic Surgery': ['plastic surgery', 'reconstructive surgery'],
        'Orthopedic Surgery': ['orthopedics', 'orthopaedics', 'orthopedic surgery', 'musculoskeletal surgery'],
        'Trauma Surgery': ['trauma surgery'],
        'Urology': ['urology', 'urologic surgery'],
        'Gynecology': ['gynecology', 'gynaecology'],
        'Obstetrics': ['obstetrics', 'maternal medicine'],
        'Obstetrics & Gynecology': ['obstetrics and gynecology', 'ob-gyn', 'women’s health'],
        'Reproductive Medicine': ['reproductive medicine', 'fertility', 'ivf'],
        'Radiology': ['radiology', 'radiological sciences', 'diagnostic imaging', 'medical imaging'],
        'Interventional Radiology': ['interventional radiology'],
        'Nuclear Medicine': ['nuclear medicine'],
        'Pathology': ['pathology', 'anatomic pathology', 'clinical pathology', 'molecular pathology'],
        'Dermatology': ['dermatology', 'skin diseases', 'cutaneous medicine'],
        'Ophthalmology': ['ophthalmology', 'eye institute', 'vision sciences'],
        'Otolaryngology': ['otolaryngology', 'ent', 'ear nose throat'],
        'Pulmonology': ['pulmonology', 'respiratory medicine', 'chest medicine', 'lung diseases'],
        'Critical Care': ['critical care', 'intensive care', 'icu'],
        'Sleep Medicine': ['sleep medicine'],
        'Nephrology': ['nephrology', 'renal medicine', 'kidney diseases'],
        'Dialysis': ['dialysis'],
        'Gastroenterology': ['gastroenterology', 'digestive diseases', 'hepatogastroenterology'],
        'Hepatology': ['hepatology', 'liver diseases'],
        'Endocrinology': ['endocrinology', 'hormone disorders', 'diabetes'],
        'Diabetology': ['diabetology'],
        'Rheumatology': ['rheumatology', 'autoimmune diseases'],
        'Immunology': ['immunology', 'immune disorders'],
        'Allergy': ['allergy', 'allergy and immunology'],
        'Infectious Disease': ['infectious disease', 'tropical medicine'],
        'Microbiology': ['microbiology'],
        'Virology': ['virology'],
        'Parasitology': ['parasitology'],
        'Epidemiology': ['epidemiology'],
        'Public Health': ['public health', 'population health'],
        'Preventive Medicine': ['preventive medicine'],
        'Internal Medicine': ['internal medicine', 'general medicine', 'department of medicine'],
        'Family Medicine': ['family medicine', 'general practice', 'primary care'],
        'Geriatrics': ['geriatrics', 'aging medicine'],
        'Palliative Care': ['palliative care', 'hospice'],
        'Physical Medicine & Rehabilitation': ['physical medicine', 'rehabilitation medicine', 'pm&r'],
        'Sports Medicine': ['sports medicine'],
        'Pain Medicine': ['pain medicine'],
        'Anesthesiology': ['anesthesiology', 'anaesthesiology'],
        'Emergency Medicine': ['emergency medicine', 'acute care'],
        'Toxicology': ['toxicology'],
        'Clinical Pharmacology': ['clinical pharmacology'],
        'Pharmacology': ['pharmacology'],
        'Genetics': ['genetics', 'genomics', 'medical genetics'],
        'Molecular Biology': ['molecular biology'],
        'Cell Biology': ['cell biology'],
        'Biochemistry': ['biochemistry'],
        'Biomedical Research': ['biomedical research', 'translational medicine'],
        'Clinical Research': ['clinical research', 'clinical trials'],
        'Biostatistics': ['biostatistics'],
        'Bioinformatics': ['bioinformatics', 'computational biology'],
        'Health Informatics': ['health informatics'],
        'Health Economics': ['health economics', 'outcomes research'],
        'Nutrition': ['nutrition', 'dietary'],
        'Dietetics': ['dietetics'],
        'Dentistry': ['dentistry', 'oral health'],
        'Oral & Maxillofacial Surgery': ['oral surgery', 'maxillofacial surgery'],
        'Veterinary Medicine': ['veterinary medicine', 'animal health'],
        'Comparative Medicine': ['comparative medicine']
    }



    
    affiliation_lower = affiliation_text.lower()
    
    # Check for department/division/center mentions
    for specialty, keywords in specialties.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, affiliation_lower):
                return specialty
    
    return None

def extract_subspecialty(affiliation_text, specialty):
    """
    Extract sub-specialty from the keywords found in affiliation
    Now returns the actual keyword found (e.g., 'cardiovascular', 'cardiac')
    
    Args:
        affiliation_text: Full affiliation string
        specialty: Main specialty already identified
    
    Returns:
        Sub-specialty keyword or None
    """
    if not affiliation_text or not specialty:
        return None
    
    # Use the same specialty keywords - return the actual keyword found
    sub_specialty_keywords = {

        'Cardiology': ['cardiology','cardiovascular','cardiac','heart','heart failure','arrhythmia','atrial fibrillation','ischemia','myocardial infarction','acute coronary syndrome','coronary artery disease','hypertension','hypertensive','cardiomyopathy','valvular','valve disease','cardiac arrest','cardio-oncology','interventional cardiology','electrophysiology','heart transplant','heart transplantation','congenital heart disease','pulmonary hypertension','atherosclerosis','angiography','angioplasty','stent','echocardiography','ecg','ekg'],
        'Neurology': ['neurology','neurological','stroke','ischemic stroke','hemorrhagic stroke','cerebrovascular','epilepsy','seizure','parkinson','parkinson disease','alzheimer','alzheimer disease','dementia','multiple sclerosis','neurodegenerative','neuropathy','neuroinflammation','migraine','headache','brain injury','neuroimaging','neurovascular','movement disorder'],
        'Psychiatry': ['psychiatry','mental health','depression','anxiety','schizophrenia','bipolar disorder','psychosis','mood disorder','major depressive disorder','ptsd','post traumatic stress','suicide','addiction','substance abuse','alcohol use disorder','behavioral disorder'],
        'Oncology': ['oncology','cancer','tumor','tumour','neoplasm','neoplasms','malignancy','malignant','leukemia','lymphoma','myeloma','metastasis','metastatic','solid tumor','breast cancer','lung cancer','prostate cancer','colorectal cancer','immuno-oncology','chemotherapy','radiotherapy','targeted therapy','precision oncology','oncogenomics'],
        'Pediatrics': ['pediatrics','paediatrics','child','children','neonatal','infant','newborn','childhood','congenital','developmental','pediatric oncology','pediatric cardiology','pediatric neurology','growth disorder','genetic disorder'],
        'Surgery': ['surgery','surgical','postoperative','preoperative','laparoscopic','minimally invasive','robotic surgery','general surgery','thoracic surgery','vascular surgery','neurosurgery','orthopedic surgery','trauma surgery','surgical oncology'],
        'Radiology': ['radiology','radiological','imaging','medical imaging','x-ray','ct','ct scan','computed tomography','mri','magnetic resonance imaging','ultrasound','sonography','nuclear medicine','pet scan','interventional radiology'],
        'Dermatology': ['dermatology','skin','psoriasis','eczema','atopic dermatitis','vitiligo','melanoma','skin cancer','acne','rosacea','alopecia','urticaria','dermatitis'],
        'Orthopedics': ['orthopedics','orthopaedics','bone','joint','osteoarthritis','arthritis','joint replacement','hip replacement','knee replacement','fracture','acl','meniscus','sports injury','spine','spinal surgery','osteoporosis'],
        'Ophthalmology': ['ophthalmology','eye','glaucoma','cataract','retina','retinal disease','macular degeneration','diabetic retinopathy','vision loss','cornea','ocular','uveitis'],
        'ENT': ['ent','otolaryngology','ear nose throat','hearing loss','deafness','sinusitis','otitis','tonsillitis','larynx','voice disorder','nasal disorder'],
        'Urology': ['urology','prostate','prostate cancer','urinary','urinary tract','kidney stone','bladder','bladder cancer','renal cancer','erectile dysfunction','male infertility'],
        'Nephrology': ['nephrology','kidney','renal','chronic kidney disease','ckd','renal failure','dialysis','transplant','glomerulonephritis','proteinuria'],
        'Gastroenterology': ['gastroenterology','digestive','ibd','crohn','ulcerative colitis','hepatitis','cirrhosis','liver disease','fatty liver','pancreatitis','gastrointestinal','gi cancer'],
        'Endocrinology': ['endocrinology','diabetes','diabetic','thyroid','hypothyroidism','hyperthyroidism','insulin','metabolic','obesity','pcos','pituitary','adrenal'],
        'Pulmonology': ['pulmonology','respiratory','asthma','copd','chronic obstructive pulmonary disease','interstitial lung disease','pulmonary fibrosis','lung cancer','sleep apnea','tuberculosis'],
        'Rheumatology': ['rheumatology','rheumatoid arthritis','lupus','autoimmune','connective tissue disease','spondyloarthritis','psoriatic arthritis','vasculitis','sjogren','ankylosing spondylitis'],
        'Hematology': ['hematology','haematology','anemia','blood disorder','coagulation','thrombosis','hemophilia','platelet','bone marrow','leukemia','lymphoma'],
        'Infectious Disease': ['infectious','infection','viral','bacterial','fungal','sepsis','covid','hiv','aids','tuberculosis','hepatitis','antimicrobial','antibiotic resistance'],
        'Immunology': ['immunology','immune','autoimmune','immune deficiency','immunodeficiency','allergy','hypersensitivity','immunotherapy','vaccination','vaccine'],
        'Pathology': ['pathology','histopathology','biopsy','tissue','molecular pathology','cytopathology','tumor pathology','diagnostic pathology'],
        'Anesthesiology': ['anesthesiology','anaesthesiology','anesthesia','analgesia','sedation','pain management','perioperative','critical care'],
        'Emergency Medicine': ['emergency medicine','trauma','acute care','critical illness','intensive care','icu','shock','cardiac arrest'],
        'Internal Medicine': ['internal medicine','general medicine','chronic disease','multimorbidity','systemic disease','metabolic syndrome'],
        'Family Medicine': ['family medicine','primary care','general practice','preventive care','community health','screening'],
        'Obstetrics & Gynecology': ['obstetrics','gynecology','gynaecology','pregnancy','childbirth','prenatal','postnatal','fertility','ivf','endometriosis','ovarian','uterine','cervical cancer'],
        'Physical Medicine': ['rehabilitation','physical medicine','physiotherapy','physical therapy','functional recovery','stroke rehab','pain rehabilitation'],
        'Genetics': ['genetics','genomic','genomics','mutation','hereditary','inherited','genetic disorder','precision medicine'],
        'Public Health': ['public health','epidemiology','population health','disease prevention','screening','health policy','health services research']

    }
    
    if specialty not in sub_specialty_keywords:
        return None
    
    affiliation_lower = affiliation_text.lower()
    
    # Return the actual keyword found in the affiliation
    for keyword in sub_specialty_keywords[specialty]:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, affiliation_lower):
            return keyword.title()  # Return capitalized keyword
    
    return None
