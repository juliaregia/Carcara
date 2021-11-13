"""

url1 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-estado-sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-municipios-sp.csv'
url3 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/srag-covid.csv'
url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinometro-sp.csv'
url5 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/evolucao-aplicacao-doses.csv'
url6 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/leitos-uti-enfermaria.csv'
url7 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/isolamento-social.csv'
url8 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinacao-estatisticas.csv'


covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                   'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
covidsp['Data'] = pd.to_datetime(covidsp['Data'])


covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                     'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                     'Mesorregião': 'category', 'Microrregião': 'category'})
covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])


srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
srag['Data'] = pd.to_datetime(srag['Data'])


vacina = pd.read_csv(url4, dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                  'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})


evoludose = pd.read_csv(url5, dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
evoludose['Data'] = pd.to_datetime(evoludose['Data'])


leitos = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                  'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Nº de novas internações nos últimos 7 dias': 'int32',
                                  'Pacientes em tratamento na UTI': 'int16',
                                  'Total de leitos de UTI destinados à Covid': 'int16',
                                  'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                  'Pacientes em tratamento na Enfermaria': 'int16',
                                  'Total de leitos de Enfermaria destinados à Covid': 'int32'})
leitos['Data'] = pd.to_datetime(leitos['Data'])


isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])


estatis = pd.read_csv(url8)

"""
