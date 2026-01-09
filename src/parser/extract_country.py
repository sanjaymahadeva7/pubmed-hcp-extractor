import re

def extract_country(affiliation_text):
    """
    Extract country from affiliation text
    
    Args:
        affiliation_text: Full affiliation string
    
    Returns:
        Country name or None
    """
    if not affiliation_text:
        return None
    
    # Common country names and abbreviations
    countries = {

        # North America
        'US': ['USA','United States','U.S.A','U.S.','United States of America','America'],
        'Canada': ['Canada'],
        'Mexico': ['Mexico','México'],

        # South America
        'Brazil': ['Brazil','Brasil'],
        'Argentina': ['Argentina'],
        'Chile': ['Chile'],
        'Colombia': ['Colombia'],
        'Peru': ['Peru'],
        'Venezuela': ['Venezuela'],
        'Bolivia': ['Bolivia'],
        'Ecuador': ['Ecuador'],
        'Paraguay': ['Paraguay'],
        'Uruguay': ['Uruguay'],
        'Guyana': ['Guyana'],
        'Suriname': ['Suriname'],

        # Europe
        'UK': ['UK','United Kingdom','Great Britain','England','Scotland','Wales','Northern Ireland','Britain'],
        'Ireland': ['Ireland','Éire'],
        'France': ['France','République Française'],
        'Germany': ['Germany','Deutschland'],
        'Italy': ['Italy','Italia'],
        'Spain': ['Spain','España'],
        'Portugal': ['Portugal'],
        'Netherlands': ['Netherlands','The Netherlands','Holland'],
        'Belgium': ['Belgium','België','Belgique'],
        'Switzerland': ['Switzerland','Schweiz','Suisse','Svizzera'],
        'Austria': ['Austria','Österreich'],
        'Sweden': ['Sweden','Sverige'],
        'Norway': ['Norway','Norge'],
        'Finland': ['Finland','Suomi'],
        'Denmark': ['Denmark','Danmark'],
        'Poland': ['Poland','Polska'],
        'Czech Republic': ['Czech Republic','Czechia','Česko'],
        'Slovakia': ['Slovakia'],
        'Hungary': ['Hungary','Magyarország'],
        'Romania': ['Romania'],
        'Bulgaria': ['Bulgaria'],
        'Croatia': ['Croatia','Hrvatska'],
        'Slovenia': ['Slovenia'],
        'Serbia': ['Serbia'],
        'Bosnia and Herzegovina': ['Bosnia','Herzegovina','Bosnia and Herzegovina'],
        'Greece': ['Greece','Hellas','Ελλάδα'],
        'Cyprus': ['Cyprus'],
        'Lithuania': ['Lithuania'],
        'Latvia': ['Latvia'],
        'Estonia': ['Estonia'],
        'Ukraine': ['Ukraine'],
        'Russia': ['Russia','Russian Federation'],
        'Belarus': ['Belarus'],
        'Moldova': ['Moldova'],
        'Iceland': ['Iceland'],
        'Luxembourg': ['Luxembourg'],
        'Malta': ['Malta'],
        'Monaco': ['Monaco'],
        'Andorra': ['Andorra'],
        'Liechtenstein': ['Liechtenstein'],
        'San Marino': ['San Marino'],
        'Vatican City': ['Vatican','Holy See'],

        # Asia
        'India': ['India','Bharat'],
        'China': ['China','PR China','P.R. China','People’s Republic of China'],
        'Japan': ['Japan'],
        'South Korea': ['South Korea','Republic of Korea','Korea'],
        'North Korea': ['North Korea','DPRK'],
        'Taiwan': ['Taiwan','Republic of China'],
        'Singapore': ['Singapore'],
        'Malaysia': ['Malaysia'],
        'Indonesia': ['Indonesia'],
        'Philippines': ['Philippines'],
        'Thailand': ['Thailand'],
        'Vietnam': ['Vietnam'],
        'Cambodia': ['Cambodia'],
        'Laos': ['Laos'],
        'Myanmar': ['Myanmar','Burma'],
        'Sri Lanka': ['Sri Lanka'],
        'Nepal': ['Nepal'],
        'Bangladesh': ['Bangladesh'],
        'Pakistan': ['Pakistan'],
        'Afghanistan': ['Afghanistan'],
        'Iran': ['Iran','Islamic Republic of Iran'],
        'Iraq': ['Iraq'],
        'Saudi Arabia': ['Saudi Arabia','KSA'],
        'UAE': ['UAE','United Arab Emirates'],
        'Qatar': ['Qatar'],
        'Kuwait': ['Kuwait'],
        'Oman': ['Oman'],
        'Yemen': ['Yemen'],
        'Israel': ['Israel'],
        'Palestine': ['Palestine'],
        'Jordan': ['Jordan'],
        'Lebanon': ['Lebanon'],
        'Syria': ['Syria'],
        'Turkey': ['Turkey','Türkiye','Turkiye'],
        'Georgia': ['Georgia'],
        'Armenia': ['Armenia'],
        'Azerbaijan': ['Azerbaijan'],
        'Kazakhstan': ['Kazakhstan'],
        'Uzbekistan': ['Uzbekistan'],
        'Turkmenistan': ['Turkmenistan'],
        'Kyrgyzstan': ['Kyrgyzstan'],
        'Tajikistan': ['Tajikistan'],
        'Mongolia': ['Mongolia'],

        # Africa
        'South Africa': ['South Africa'],
        'Egypt': ['Egypt'],
        'Nigeria': ['Nigeria'],
        'Kenya': ['Kenya'],
        'Ethiopia': ['Ethiopia'],
        'Ghana': ['Ghana'],
        'Morocco': ['Morocco'],
        'Algeria': ['Algeria'],
        'Tunisia': ['Tunisia'],
        'Libya': ['Libya'],
        'Sudan': ['Sudan'],
        'Uganda': ['Uganda'],
        'Tanzania': ['Tanzania'],
        'Zambia': ['Zambia'],
        'Zimbabwe': ['Zimbabwe'],
        'Botswana': ['Botswana'],
        'Namibia': ['Namibia'],
        'Mozambique': ['Mozambique'],
        'Angola': ['Angola'],
        'Cameroon': ['Cameroon'],
        'Ivory Coast': ['Ivory Coast','Côte d’Ivoire'],
        'Senegal': ['Senegal'],
        'Rwanda': ['Rwanda'],
        'Somalia': ['Somalia'],

        # Oceania
        'Australia': ['Australia'],
        'New Zealand': ['New Zealand'],
        'Fiji': ['Fiji'],
        'Papua New Guinea': ['Papua New Guinea'],

        # Middle East extras
        'Bahrain': ['Bahrain'],
        'Cyprus': ['Cyprus']
    }

    
    # Check for each country
    for country, variants in countries.items():
        for variant in variants:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, affiliation_text, re.IGNORECASE):
                return country
    
    return None