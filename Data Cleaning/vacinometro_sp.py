import pandas as pd
import numpy as np
import sys
import os
import glob
import time

# Automação do reconhecimento de novos dados pelo Pandas
list_of_files1 = glob.glob('/home/sobral/data/vacinometro/*.csv')
latest_file1 = max(list_of_files1, key=os.path.getctime)
csv1 = os.path.abspath(latest_file1)

list_of_files2 = glob.glob('/home/sobral/data/distribuicao/*.csv')
latest_file2 = max(list_of_files2, key=os.path.getctime)
csv2 = os.path.abspath(latest_file2)

# Leitura pelo Pandas dos arquivos csv
vacinometro = pd.read_csv(csv1, sep=';')
distribuicao = pd.read_csv(csv2, sep=';')


# Cleaning Data

# Criando novas colunas de tal forma que não tenha linhas duplicadas
col = 'Dose'
condition1 = [vacinometro[col] == '1° DOSE']
condition2 = [vacinometro[col] == '2° DOSE']
condition3 = [vacinometro[col] == '3º DOSE']
condition4 = [vacinometro[col] == 'UNICA']
choice = [vacinometro["Total Doses Aplicadas"]]

vacinometro["1ª Dose"] = np.select(condition1, choice, default=np.nan)
vacinometro["2ª Dose"] = np.select(condition2, choice, default=np.nan)
vacinometro["3ª Dose"] = np.select(condition3, choice, default=np.nan)
vacinometro["Dose Única"] = np.select(condition4, choice, default=np.nan)

vacinometro = vacinometro.groupby('Município').agg({'1ª Dose': 'first',
                                                    '2ª Dose': 'first',
                                                    '3ª Dose': 'first',
                                                    'Dose Única': 'first'}).reset_index()

# Ajustando os 5 missing values encontrados para converter em int64:
vacinometro["3ª Dose"] = vacinometro["3ª Dose"].fillna(0)
vacinometro["Dose Única"] = vacinometro["Dose Única"].fillna(0)

# Ajustando o Datatype de colunas
vacinometro["1ª Dose"] = vacinometro["1ª Dose"].astype(np.int32)
vacinometro["2ª Dose"] = vacinometro["2ª Dose"].astype(np.int32)
vacinometro["3ª Dose"] = vacinometro["3ª Dose"].astype(np.int32)
vacinometro["Dose Única"] = vacinometro["Dose Única"].astype(np.int32)
distribuicao['Qtd-Doses-Distribuidas'] = distribuicao['Qtd-Doses-Distribuidas'].astype(np.int32)

# Alterando nome de colunas
distribuicao.rename(columns={"Municipio": "Município"}, inplace=True)
distribuicao.rename(columns={"Qtd-Doses-Distribuidas": "Doses Distribuídas"}, inplace=True)

# Agrupando outro dataframe ao principal, para inserir informações adicionais
df = vacinometro.merge(distribuicao, left_on=['Município'],
                       right_on=['Município'], how='inner',
                       suffixes=['_vacinometro', '_distribuicao'])
del vacinometro, distribuicao

# Reformatando os valores da coluna "Município", que estavam em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, index=df.index, name='Município')
df['Município'] = df['Município'].astype('category')

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/vacinometro-sp.csv", index=False)

print('Dados de vacinometro_sp.py tratados e exportados!' + '\n' + '\n')
