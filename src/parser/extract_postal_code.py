import re

def extract_postal_code(text):
    if not text:
        return ""

    # ------------------ AUSTRALIA ------------------
    au = re.search(r'\b(NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\s*(\d{4})\b', text, re.I)
    if au:
        return au.group(2)

    # ------------------ UNITED KINGDOM ------------------
    uk = re.search(r'\b([A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b', text, re.I)
    if uk:
        return uk.group(1)

    # ------------------ CANADA ------------------
    ca = re.search(r'\b([A-Z]\d[A-Z]\s?\d[A-Z]\d)\b(?=.*Canada)', text, re.I)
    if ca:
        return ca.group(1)

    # ------------------ GERMANY ------------------
    de = re.search(r'\b\d{5}\b(?=.*(Germany|Deutschland))', text, re.I)
    if de:
        return de.group(0)

    # ------------------ FRANCE ------------------
    fr = re.search(r'\b\d{5}\b(?=.*France)', text, re.I)
    if fr:
        return fr.group(0)

    # ------------------ ITALY ------------------
    it = re.search(r'\b\d{5}\b(?=.*(Italy|Italia))', text, re.I)
    if it:
        return it.group(0)

    # ------------------ SPAIN ------------------
    es = re.search(r'\b\d{5}\b(?=.*(Spain|España))', text, re.I)
    if es:
        return es.group(0)

    # ------------------ NETHERLANDS ------------------
    nl = re.search(r'\b\d{4}\s?[A-Z]{2}\b(?=.*Netherlands)', text, re.I)
    if nl:
        return nl.group(0)

    # ------------------ SWITZERLAND ------------------
    ch = re.search(r'\b\d{4}\b(?=.*Switzerland)', text, re.I)
    if ch:
        return ch.group(0)

    # ------------------ SWEDEN ------------------
    se = re.search(r'\b\d{3}\s?\d{2}\b(?=.*Sweden)', text, re.I)
    if se:
        return se.group(0)

    # ------------------ BELGIUM ------------------
    be = re.search(r'\b\d{4}\b(?=.*Belgium)', text, re.I)
    if be:
        return be.group(0)

    # ------------------ AUSTRIA ------------------
    at = re.search(r'\b\d{4}\b(?=.*Austria)', text, re.I)
    if at:
        return at.group(0)

    # ------------------ PORTUGAL ------------------
    pt = re.search(r'\b\d{4}-\d{3}\b(?=.*Portugal)', text, re.I)
    if pt:
        return pt.group(0)

    # ------------------ BRAZIL ------------------
    br = re.search(r'\b\d{5}-\d{3}\b(?=.*(Brazil|Brasil))', text, re.I)
    if br:
        return br.group(0)

    # ------------------ MEXICO ------------------
    mx = re.search(r'\b\d{5}\b(?=.*Mexico)', text, re.I)
    if mx:
        return mx.group(0)

    # ------------------ JAPAN ------------------
    jp = re.search(r'\b\d{3}-\d{4}\b(?=.*Japan)', text, re.I)
    if jp:
        return jp.group(0)

    # ------------------ CHINA ------------------
    cn = re.search(r'\b\d{6}\b(?=.*China)', text, re.I)
    if cn:
        return cn.group(0)

    # ------------------ INDIA ------------------
    ind = re.search(r'\b\d{6}\b(?=.*India)', text, re.I)
    if ind:
        return ind.group(0)

    # ------------------ USA (LAST & SAFE) ------------------
    if re.search(r'\b(USA|United States|U\.S\.A|U\.S\.)\b', text, re.I):
        us = re.findall(r'\b\d{5}(?:-\d{4})?\b', text)
        if us:
            return us[-1]

    return ""
