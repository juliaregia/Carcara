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

time.sleep(15)

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
