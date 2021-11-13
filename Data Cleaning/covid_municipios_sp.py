import pandas as pd
import numpy as np

# localização dos dataframes
url1 = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv'
url2 = '/home/sobral/Carcara/Aplicação Web/app/data/meso-micro-regioes-sp.csv'

# leitura dos arquivos csv pelo pandas
df = pd.read_csv(url1, sep=';', usecols=['nome_munic', 'codigo_ibge', 'datahora', 'casos',
                                         'casos_novos', 'obitos', 'obitos_novos'],
                 dtype={'casos': 'int32', 'casos_novos': 'int16', 'obitos': 'int32',
                        'obitos_novos': 'int16', 'nome_munic': 'category', 'codigo_ibge': 'int32'})

df['codigo_ibge'] = df['codigo_ibge'].astype('category')

df.loc[:, 'datahora'] = pd.Series(pd.to_datetime(df['datahora'], format='%Y-%m-%d',
                                                 errors='coerce'),
                                  name='datahora')

df = df.sort_values(['datahora'], ascending=True)
df = df.reset_index(drop=True)

regiaosp = pd.read_csv(url2, usecols=['codigo_ibge', 'mesorregiao', 'microrregiao'],
                       dtype={'mesorregiao': 'category', 'microrregiao': 'category', 'codigo_ibge': 'int32'})

regiaosp['codigo_ibge'] = regiaosp['codigo_ibge'].astype('category')

# Agrupando outro dataframe ao principal, para inserir informações de regiões
df = df.merge(regiaosp, left_on=['codigo_ibge'],
              right_on=['codigo_ibge'], how='inner',
              suffixes=['_df', '_regiaosp'])

df['codigo_ibge'] = df['codigo_ibge'].astype('category')
del regiaosp


# Data Cleaning

# Renomeando colunas
df.rename(columns={"nome_munic": "Município"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)
df.rename(columns={"casos": "Total de Casos"}, inplace=True)
df.rename(columns={"casos_novos": "Novos Casos"}, inplace=True)
df.rename(columns={"obitos": "Total de Óbitos"}, inplace=True)
df.rename(columns={"obitos_novos": "Novos Óbitos"}, inplace=True)
df.rename(columns={"mesorregiao": "Mesorregião"}, inplace=True)
df.rename(columns={"microrregiao": "Microrregião"}, inplace=True)

# Excluindo valores ditos "ignorados" pela fonte dos dados
df.drop(df[df.Município == 'Ignorado'].index, inplace=True)
df.dropna().reset_index(drop=True, inplace=True)

# Excluindo linhas nas quais todos os dados variáveis são NaN (45.194 linhas)
df = df.loc[(df['Total de Casos'] + df['Novos Casos'] + df['Total de Óbitos'] +
             df['Novos Óbitos'] != 0)]

df = df.sort_values(['Data'], ascending=True)
df = df.reset_index(drop=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/covid-municipios-sp.csv", index=False)

print('Dados de covid_municipios_sp.py tratados e exportados!' + '\n' + '\n')
