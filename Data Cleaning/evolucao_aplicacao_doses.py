from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np
import sys
import os
import glob
import time
import re

# Automação da coleta dos dataframes pelo selenium
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/evolucao-doses"
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
botao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[19]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[19]/div/ul/li/div/a")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(15)

# Automatação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/evolucao-doses/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura do Dataframe pelo pandas
df = pd.read_csv(csv, sep=';')

# Criando novas colunas de tal forma que não tenha linhas duplicadas
col = 'Dose'
condition1 = [df[col] == '1° DOSE']
condition2 = [df[col] == '2° DOSE']
condition3 = [df[col] == '3º DOSE/ADICIONAL']
condition4 = [df[col] == 'UNICA']
choice = [df["Contagem de Dose"]]

df["1ª Dose"] = np.select(condition1, choice, default=np.nan)
df["2ª Dose"] = np.select(condition2, choice, default=np.nan)
df["3ª Dose"] = np.select(condition3, choice, default=np.nan)
df["Dose Única"] = np.select(condition4, choice, default=np.nan)

df = df.groupby('Dia de Data Registro Vacina').agg({'1ª Dose': 'first',
                                                    '2ª Dose': 'first',
                                                    '3ª Dose': 'first',
                                                    'Dose Única': 'first'}).reset_index()

# Ajustando os missing values encontrados para converter em int64:
df["1ª Dose"] = df["1ª Dose"].fillna(0)
df["2ª Dose"] = df["2ª Dose"].fillna(0)
df["3ª Dose"] = df["3ª Dose"].fillna(0)
df["Dose Única"] = df["Dose Única"].fillna(0)

# Ajustando o Datatype de colunas
df["1ª Dose"] = df["1ª Dose"].astype(int)
df["2ª Dose"] = df["2ª Dose"].astype(int)
df["3ª Dose"] = df["3ª Dose"].astype(int)
df["Dose Única"] = df["Dose Única"].astype(int)

# Alterando nome de colunas
df.rename(columns={"Dia de Data Registro Vacina": "Data de Registro"}, inplace=True)
