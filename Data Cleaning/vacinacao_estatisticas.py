import pandas as pd
import numpy as np
import sys
import os
import glob
import time

# Automatação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/estatisticas-vacina/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura do dataframe pelo pandas
df = pd.read_csv(csv, sep=';')

# Renomeando linhas
df.at[1, 'Nomes de medida'] = '3ª Dose'
df.at[0, 'Nomes de medida'] = 'Doses Aplicadas'

# Renomeando colunas
df = df.rename(columns={'Valores de medida': 'Total'})
df = df.rename(columns={'Nomes de medida': 'Dado'})

# Alterando a ordem das linhas
df = df.sort_values(['Dado'], ascending=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/vacinacao-estatisticas.csv", index=False)

print('Dados de vacinacao_estatisticas.py tratados e exportados!' + '\n' + '\n')
