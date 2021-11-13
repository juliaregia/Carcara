import pandas as pd
import numpy as np
import sys
import time
import glob
import os
import datetime as dt
from datetime import datetime


# Automação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/covid_estado/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

url = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/sp.csv'

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';', encoding='latin1',
                 usecols=['Total de casos', 'Casos por dia', 'Óbitos por dia'],
                 dtype={'Total de casos': 'int32', 'Casos por dia': 'int32'})

df2 = pd.read_csv(url, sep=';', dtype={'casos_acum': 'int32', 'obitos_acum': 'int32'})

df2.loc[:, 'datahora'] = pd.Series(pd.to_datetime(df2['datahora'], format='%Y-%m-%d',
                                                  errors='coerce'),
                                   name='datahora')

# Agrupando os dois dataframes que se completam nas informações
df = df2.merge(df, left_on=['casos_acum'], right_on=['Total de casos'],
               how='inner', suffixes=['_1', '_2'])

del df2
df = df.reset_index(drop=True)


# Data Cleaning

# Deletando colunas duplicadas
df.drop('Total de casos', axis=1, inplace=True)

# Padronizando valores "0" errôneamente descritos como NaN e convertendo para int16
df["Óbitos por dia"] = df["Óbitos por dia"].fillna(0)
df["Óbitos por dia"] = df["Óbitos por dia"].astype(np.int16)

# Renomeando colunas
df.rename(columns={"casos_acum": "Total de casos"}, inplace=True)
df.rename(columns={"obitos_acum": "Total de óbitos"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)

# Excluindo dados que estavam duplicados
df = df.sort_values(['Data'], ascending=True)
df = df.drop(df[(df['Óbitos por dia'] == 0) & (df['Casos por dia'] == 0) &
                (df.Data < '2021-01-01')].index)

# Forçando a ordenação por data e por fim resetando o index
df = df.sort_values(['Data'], ascending=True)
df = df.reset_index(drop=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/covid-estado-sp.csv", index=False)

print('Dados de covid_estado_sp.py tratados e exportados!' + '\n' + '\n')
