import pandas as pd
import numpy as np
import sys
import time
import glob
import os
import datetime as dt
from datetime import datetime

# Automação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/srag/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';',
                 usecols=['Data de Notificação', 'Municípios', 'Grupo de Idades', 'Evolução',
                          'OUTRAS SRAG', 'Sg Uf'],
                 dtype={'Grupo de Idades': 'int8'})

df['Grupo de Idades'] = df['Grupo de Idades'].astype('category')
df.loc[:, 'Data de Notificação'] = pd.Series(pd.to_datetime(df['Data de Notificação'], dayfirst=True,
                                                            format='%d/%m/%Y', errors='coerce'),
                                             name='Data de Notificação')


# Cleaning Data

# Excluindo dados referentes a outros Estados
df.rename(columns={"Sg Uf": "UF"}, inplace=True)
df.drop(df[df.UF != 'SP'].index, inplace=True)
df.drop('UF', axis=1, inplace=True)

# Excluindo dados referentes a casos de SRAG alheios à covid-19
df.rename(columns={"OUTRAS SRAG": "Doença"}, inplace=True)
df.drop(df[df.Doença != 'COVID 19'].index, inplace=True)
df.drop('Doença', axis=1, inplace=True)

# Renomeando colunas
df.rename(columns={"Grupo de Idades": "Faixa Etária"}, inplace=True)
df.rename(columns={"Municípios": "Município"}, inplace=True)
df.rename(columns={"Data de Notificação": "Data"}, inplace=True)

# Ajustando valores que estão em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, name='Município')
df['Município'] = df['Município'].astype('category')

# Padronizando Missing Values encontrados na coluna "Evolução"
df['Evolução'] = df['Evolução'].fillna(value='Não informado')
df['Evolução'] = df['Evolução'].astype('category')

# Ordenando a coluna "Data de Notificação" e resetando o index
df = df.sort_values(['Data'], ascending=True)
df = df.reset_index(drop=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/srag-covid.csv", index=False)

print('Dados de srag_covid.py tratados e exportados!' + '\n' + '\n')
