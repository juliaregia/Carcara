from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np
import sys
import time
import glob
import os

# Automação da coleta dos dataframes pelo selenium
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/leitos"
prefs = {'download.default_directory': download_dir}

options_chrome = Options()
options_chrome.add_argument("start-maximized")
options_chrome.add_argument("disable-infobars")
options_chrome.add_argument("--disable-extensions")
options_chrome.add_argument('--headless')
options_chrome.add_argument('--no-sandbox')
options_chrome.add_argument('--disable-dev-shm-usage')
options_chrome.add_experimental_option('prefs', prefs)
desired = options_chrome.to_capabilities()
desired['loggingPrefs'] = {'performance': 'ALL'}

navegador = webdriver.Chrome('chromedriver', options=options_chrome,
                             desired_capabilities=desired)

navegador.get("https://www.saopaulo.sp.gov.br/planosp/simi/dados-abertos/")
botao1 = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[7]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[7]/div/ul/li[1]/div/a")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(15)

# Automatação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/leitos/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';')

# Cleaning Data

# Deletando colunas sem dados relevantes
df.drop('internacoes_7d_l', axis=1, inplace=True)
df.drop('leitos_pc', axis=1, inplace=True)

# Alterando a "," pelo "." para a conversão em float sem gerar valores NaN
df['pacientes_uti_mm7d'] = df['pacientes_uti_mm7d'].str.replace(',', '.')
df['total_covid_uti_mm7d'] = df['total_covid_uti_mm7d'].str.replace(',', '.')
df['ocupacao_leitos'] = df['ocupacao_leitos'].str.replace(',', '.')
df['internacoes_7v7'] = df['internacoes_7v7'].str.replace(',', '.')
df['ocupacao_leitos_ultimo_dia'] = df['ocupacao_leitos_ultimo_dia'].str.replace(',', '.')
df['pacientes_enf_mm7d'] = df['pacientes_enf_mm7d'].str.replace(',', '.')
df['total_covid_enf_mm7d'] = df['total_covid_enf_mm7d'].str.replace(',', '.')

# Alterando o Datatype de algumas colunas
df['pacientes_uti_mm7d'] = df['pacientes_uti_mm7d'].apply(pd.to_numeric, downcast='float', errors='coerce')
df['total_covid_uti_mm7d'] = df['total_covid_uti_mm7d'].apply(pd.to_numeric, downcast='float', errors='coerce')
df['ocupacao_leitos'] = df['ocupacao_leitos'].apply(pd.to_numeric, downcast='float', errors='coerce')
df['internacoes_7v7'] = df['internacoes_7v7'].apply(pd.to_numeric, downcast='float', errors='coerce')
df['ocupacao_leitos_ultimo_dia'] = df['ocupacao_leitos_ultimo_dia'].apply(pd.to_numeric, downcast='float',
                                                                          errors='coerce')
df['pacientes_enf_mm7d'] = df['pacientes_enf_mm7d'].apply(pd.to_numeric, downcast='float', errors='coerce')
df['total_covid_enf_mm7d'] = df['total_covid_enf_mm7d'].apply(pd.to_numeric, downcast='float', errors='coerce')

# Delimitando as casas decimais em colunas float:
df['pacientes_uti_mm7d'] = df['pacientes_uti_mm7d'].round(decimals=2)
df['total_covid_uti_mm7d'] = df['total_covid_uti_mm7d'].round(decimals=2)
df['ocupacao_leitos'] = df['ocupacao_leitos'].round(decimals=2)
df['internacoes_7v7'] = df['internacoes_7v7'].round(decimals=2)
df['ocupacao_leitos_ultimo_dia'] = df['ocupacao_leitos_ultimo_dia'].round(decimals=2)
df['pacientes_enf_mm7d'] = df['pacientes_enf_mm7d'].round(decimals=2)
df['total_covid_enf_mm7d'] = df['total_covid_enf_mm7d'].round(decimals=2)

# Renomeando colunas
df.rename(columns={"ocupacao_leitos": "mm7d da Ocupação dos leitos de UTI e Enfermaria (%)"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)
df.rename(columns={"total_covid_uti_mm7d": "mm7d do Total de leitos de UTI destinados à Covid"}, inplace=True)
df.rename(columns={"internacoes_7d": "Nº de novas internações nos últimos 7 dias"}, inplace=True)
df.rename(columns={"internacoes_7v7": "Variação no nº de novas internações (%)"}, inplace=True)
df.rename(columns={"pacientes_uti_ultimo_dia": "Pacientes em tratamento na UTI"}, inplace=True)
df.rename(columns={"total_covid_uti_ultimo_dia": "Total de leitos de UTI destinados à Covid"}, inplace=True)
df.rename(columns={"ocupacao_leitos_ultimo_dia": "Ocupação dos leitos de UTI e Enfermaria (%)"}, inplace=True)
df.rename(columns={"internacoes_ultimo_dia": "Novos casos de internações (UTI e Enfermaria)"}, inplace=True)
df.rename(columns={"total_covid_enf_mm7d": "mm7d do Total de leitos de Enfermaria destinados à Covid"}, inplace=True)
df.rename(columns={"pacientes_enf_ultimo_dia": "Pacientes em tratamento na Enfermaria"}, inplace=True)
df.rename(columns={"total_covid_enf_ultimo_dia": "Total de leitos de Enfermaria destinados à Covid"}, inplace=True)
df.rename(columns={"nome_drs": "Departamento Regional de Saúde"}, inplace=True)
df.rename(columns={"pacientes_uti_mm7d": "mm7d do Nº de pacientes em tratamento na UTI"}, inplace=True)
df.rename(columns={"pop": "População"}, inplace=True)
df.rename(columns={"pacientes_enf_mm7d": "mm7d do Nº de pacientes em tratamento na Enfermaria"}, inplace=True)

# Transformando a coluna de Data de Notificação em Datetime type
df.loc[:, 'Data'] = pd.Series(pd.to_datetime(df['Data'], dayfirst=True,
                                             format='%d/%m/%Y', errors='coerce'),
                              name='Data')

# Ordenando o dataframe por data e resetando o index
df = df.reset_index(drop=True)

df = df.sort_values(['Data'], ascending=True)

df = df[[c for c in df.columns if c not in ['index']]]
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
    df = df.to_frame(index=False)
df = df.reset_index().drop('index', axis=1, errors='ignore')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Data Cleaning/Dados tratados/leitos-uti-enfermaria.csv", index=False)
