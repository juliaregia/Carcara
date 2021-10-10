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
import datetime as dt
from datetime import datetime

# Automação da coleta de um dos dataframes
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/covid_estado"
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

navegador.get("https://www.seade.gov.br/coronavirus/#")
elemento = navegador.find_element_by_xpath("/html/body/div[1]/div[1]/a[1]")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(30)

# Automação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/covid_estado/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

url = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/sp.csv'

# Leitura pelo Pandas do arquivo csv
df1 = pd.read_csv(csv, sep=';', encoding='latin1')
df2 = pd.read_csv(url, sep=';')

# Agrupando os dois dataframes que se completam nas informações
df1 = df1.drop(['Data', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                'Unnamed: 8'], axis=1)
df = df2.merge(df1, left_on=['casos_acum'], right_on=['Total de casos'],
               how='inner', suffixes=['_1', '_2'])

# Data Cleaning

# Deletando colunas duplicadas
df.drop('Total de casos', axis=1, inplace=True)

# Renomeando colunas
df.rename(columns={"casos_acum": "Total de casos"}, inplace=True)
df.rename(columns={"obitos_acum": "Total de óbitos"}, inplace=True)
df.rename(columns={"datahora": "Data"}, inplace=True)

# Mudando a formatação do registro de data para datetime64
df.loc[:, 'Data'] = pd.Series(pd.to_datetime(df['Data'],
                                             infer_datetime_format=True),
                              name='Data', index=df['Data'].index)

# Padronizando valores "0" errôneamente descritos como NaN
df["Óbitos por dia"] = df["Óbitos por dia"].fillna(0)

# Alterando o Datatype da coluna "Óbitos por dia" para int64
df["Óbitos por dia"] = df["Óbitos por dia"].astype(int)

# Excluindo dados que estavam duplicadas
df = df.sort_values(['Data'], ascending=True)

df.rename(columns={"Óbitos por dia": "obitos"}, inplace=True)
df.rename(columns={"Casos por dia": "casos"}, inplace=True)

df = df.drop(df[(df.obitos == 0) & (df.casos == 0) &
                (df.Data < '2021-01-01')].index)

df.rename(columns={"obitos": "Óbitos por dia"}, inplace=True)
df.rename(columns={"casos": "Casos por dia"}, inplace=True)

# Forçando a ordenação por data e por fim resetando o index
df = df.sort_values(['Data'], ascending=True)

df = df[[c for c in df.columns if c not in ['index']]]
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
    df = df.to_frame(index=False)
df = df.reset_index().drop('index', axis=1, errors='ignore')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Data Cleaning/Dados tratados/covid-estado-sp.csv", index=False)