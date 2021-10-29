import pandas as pd
import numpy as np

# localização dos dataframes
url1 = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Sprint%201/Fontes%20de%20Dados' \
       '/meso_micro_regioes_sp.csv '

# leitura dos arquivos csv pelos pandas
covidsp = pd.read_csv(url1, sep=';')
regiaosp = pd.read_csv(url2)

# Agrupando outro dataframe ao principal, para inserir informações de regiões
regiaosp_tmp = regiaosp.drop(['latitude', 'municipio', 'longitude'], axis=1)
df = covidsp.merge(regiaosp_tmp, left_on=['codigo_ibge'],
                   right_on=['codigo_ibge'], how='inner',
                   suffixes=['_covidsp', '_regiaosp'])

# Data Cleaning

# Renomeando colunas
df.rename(columns={"nome_munic": "Município"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)
df.rename(columns={"area": "Área (Km2)"}, inplace=True)
df.rename(columns={"latitude": "Latitude"}, inplace=True)
df.rename(columns={"longitude": "Longitude"}, inplace=True)
df.rename(columns={"casos_mm7d": "Casos por mm7d"}, inplace=True)
df.rename(columns={"obitos_mm7d": "Óbitos por mm7d"}, inplace=True)
df.rename(columns={"letalidade": "Letalidade"}, inplace=True)
df.rename(columns={"casos": "Total de Casos"}, inplace=True)
df.rename(columns={"casos_novos": "Novos Casos"}, inplace=True)
df.rename(columns={"obitos": "Total de Óbitos"}, inplace=True)
df.rename(columns={"obitos_novos": "Novos Óbitos"}, inplace=True)
df.rename(columns={"mesorregiao": "Mesorregião"}, inplace=True)
df.rename(columns={"microrregiao": "Microrregião"}, inplace=True)
df.rename(columns={"pop": "População"}, inplace=True)

# Deletando colunas sem dados relevantes
df.drop('dia', axis=1, inplace=True)
df.drop('mes', axis=1, inplace=True)
df.drop('nome_drs', axis=1, inplace=True)
df.drop('cod_drs', axis=1, inplace=True)
df.drop('map_leg', axis=1, inplace=True)
df.drop('map_leg_s', axis=1, inplace=True)
df.drop('semana_epidem', axis=1, inplace=True)
df.drop('nome_ra', axis=1, inplace=True)
df.drop('cod_ra', axis=1, inplace=True)
df.drop('pop_60', axis=1, inplace=True)
df.drop('casos_pc', axis=1, inplace=True)
df.drop('obitos_pc', axis=1, inplace=True)

# Mudando a formatação do registro de data
df.loc[:, 'Data'] = pd.Series(pd.to_datetime
                              (df['Data'], infer_datetime_format=True),
                              name='Data', index=df['Data'].index)

# Alterando a "," pelo "." para a conversão em float sem gerar valores NaN
df['Latitude'] = df['Latitude'].str.replace(',', '.')
df['Longitude'] = df['Longitude'].str.replace(',', '.')
df['Casos por mm7d'] = df['Casos por mm7d'].str.replace(',', '.')
df['Óbitos por mm7d'] = df['Óbitos por mm7d'].str.replace(',', '.')
df['Letalidade'] = df['Letalidade'].str.replace(',', '.')

# Corrigindo o formato da área para "km2" sem casas decimais
df['Área (Km2)'] /= 100
df['Área (Km2)'] = df['Área (Km2)'].round(decimals=0).astype(pd.Int64Dtype())

# Alterando o Datatype de algumas colunas
df['Latitude'] = df['Latitude'].apply(pd.to_numeric, downcast='float',
                                      errors='coerce')
df['Longitude'] = df['Longitude'].apply(pd.to_numeric, downcast='float',
                                        errors='coerce')
df['Casos por mm7d'] = df['Casos por mm7d'].apply(pd.to_numeric, downcast='float',
                                                  errors='coerce')
df['Óbitos por mm7d'] = df['Óbitos por mm7d'].apply(pd.to_numeric, downcast='float',
                                                    errors='coerce')
df['Letalidade'] = df['Letalidade'].apply(pd.to_numeric, downcast='float',
                                          errors='coerce')

# Delimitando as casas decimais em colunas float:
df['Casos por mm7d'] = df['Casos por mm7d'].round(decimals=2)
df['Óbitos por mm7d'] = df['Óbitos por mm7d'].round(decimals=2)
df['Letalidade'] = df['Letalidade'].round(decimals=2)

# Excluindo valores ditos "ignorados" pela fonte dos dados
df.drop(df[df.Município == 'Ignorado'].index, inplace=True)
df.dropna().reset_index(drop=True, inplace=True)

# Excluindo linhas nas quais todos os dados variáveis são NaN (45.194 linhas)
df = df.loc[(df['Total de Casos'] + df['Novos Casos'] + df['Total de Óbitos'] +
             df['Novos Óbitos'] != 0)]

# Renomeando os headers para tirar os espaços
df.columns = df.columns.str.replace(' ', '_')

# Forçando a ordenação por data e por fim resetando o index
df = df.sort_values(['Data'], ascending=True)

df = df[[c for c in df.columns if c not in ['index']]]
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
    df = df.to_frame(index=False)
df = df.reset_index().drop('index', axis=1, errors='ignore')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/covid-municipios-sp.csv", index=False)
