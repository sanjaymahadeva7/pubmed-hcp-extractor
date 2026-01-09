import re

BRAZIL_STATES = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

BRAZIL_FULL_NAMES = [
    'São Paulo', 'Sao Paulo',
    'Rio de Janeiro',
    'Minas Gerais',
    'Paraná', 'Parana',
    'Rio Grande do Sul',
    'Bahia', 'Pernambuco',
    'Ceará', 'Ceara',
    'Santa Catarina',
    'Goiás', 'Goias',
    'Espírito Santo', 'Espirito Santo',
    'Distrito Federal', 'Brasília', 'Brasilia',
    'Pará', 'Para',
    'Paraíba', 'Paraiba',
    'Maranhão', 'Maranhao',
    'Piauí', 'Piaui',
    'Rio Grande do Norte',
    'Rondônia', 'Rondonia',
    'Mato Grosso', 'Mato Grosso do Sul',
    'Amazonas', 'Acre', 'Amapá', 'Amapa',
    'Roraima', 'Tocantins', 'Alagoas', 'Sergipe'
]


def extract_sa_state(text, country):

    if country == "Brazil":
        for abbr, full in BRAZIL_STATES.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', text):
                return full

        for state in BRAZIL_FULL_NAMES:
            if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
                return state

    return ""
