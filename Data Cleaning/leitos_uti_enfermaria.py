import pandas as pd
import numpy as np
import sys
import time
import glob
import os

# Automatação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/leitos/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';',
                 usecols=["datahora", "ocupacao_leitos", "internacoes_7d", "pacientes_uti_ultimo_dia",
                          "total_covid_uti_ultimo_dia", "ocupacao_leitos_ultimo_dia", "internacoes_ultimo_dia",
                          "pacientes_enf_ultimo_dia", "total_covid_enf_ultimo_dia", "nome_drs"],
                 dtype={'nome_drs': 'category', 'internacoes_7d': 'int32', 'pacientes_uti_ultimo_dia': 'int16',
                        'total_covid_uti_ultimo_dia': 'int16', 'internacoes_ultimo_dia': 'int16',
                        'pacientes_enf_ultimo_dia': 'int16', 'total_covid_enf_ultimo_dia': 'int32'})

df.loc[:, 'datahora'] = pd.Series(pd.to_datetime(df['datahora'], dayfirst=True,
                                                 format='%d/%m/%Y', errors='coerce'),
                                  name='datahora')


# Cleaning Data

# Alterando a "," pelo "." para a conversão em float sem gerar valores NaN
df['ocupacao_leitos'] = df['ocupacao_leitos'].str.replace(',', '.')
df['ocupacao_leitos_ultimo_dia'] = df['ocupacao_leitos_ultimo_dia'].str.replace(',', '.')

df['ocupacao_leitos'] = df['ocupacao_leitos'].astype(np.float64).round(decimals=1)
df['ocupacao_leitos_ultimo_dia'] = df['ocupacao_leitos_ultimo_dia'].astype(np.float64).round(decimals=1)

# Renomeando colunas
df.rename(columns={"ocupacao_leitos": "mm7d da Ocupação dos leitos de UTI e Enfermaria (%)"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)
df.rename(columns={"internacoes_7d": "Nº de novas internações nos últimos 7 dias"}, inplace=True)
df.rename(columns={"pacientes_uti_ultimo_dia": "Pacientes em tratamento na UTI"}, inplace=True)
df.rename(columns={"total_covid_uti_ultimo_dia": "Total de leitos de UTI destinados à Covid"}, inplace=True)
df.rename(columns={"ocupacao_leitos_ultimo_dia": "Ocupação dos leitos de UTI e Enfermaria (%)"}, inplace=True)
df.rename(columns={"internacoes_ultimo_dia": "Novos casos de internações (UTI e Enfermaria)"}, inplace=True)
df.rename(columns={"pacientes_enf_ultimo_dia": "Pacientes em tratamento na Enfermaria"}, inplace=True)
df.rename(columns={"total_covid_enf_ultimo_dia": "Total de leitos de Enfermaria destinados à Covid"}, inplace=True)
df.rename(columns={"nome_drs": "Departamento Regional de Saúde"}, inplace=True)

# Ordenando o dataframe por data e resetando o index
df = df.sort_values(['Data'], ascending=True)
df = df.reset_index(drop=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/leitos-uti-enfermaria.csv", index=False)

print('Dados de leitos_uti_enfermaria.py tratados e exportados!' + '\n' + '\n')
