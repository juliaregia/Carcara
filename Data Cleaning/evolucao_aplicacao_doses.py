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
import datetime as dt


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
df.rename(columns={"Dia de Data Registro Vacina": "Data"}, inplace=True)

# Alterando o registro da data para o formato capaz de convertê-lo à datetype64
meses = {' de janeiro de ': '/01/', ' de fevereiro de ': '/02/',
         ' de março de ': '/03/', ' de abril de ': '/04/', ' de maio de ': '/05/',
         ' de junho de ': '/06/', ' de julho de ': '/07/', ' de agosto de ': '/08/',
         ' de setembro de ': '/09/', ' de outubro de ': '/10/',
         ' de novembro de ': '/11/', ' de dezembro de ': '/12/'
         }

dias = {'1/0': '01/0', '1/1': '01/1', '2/0': '02/0', '2/1': '02/1', '3/0': '03/0',
        '3/1': '03/1', '4/0': '04/0', '4/1': '04/1', '5/0': '05/0', '5/1': '05/1',
        '6/0': '06/0', '6/1': '06/1', '7/0': '07/0', '7/1': '07/1', '8/0': '08/0',
        '8/1': '08/1', '9/0': '09/0', '9/1': '09/1'}

coerce = {'101': '11', '102': '12', '103': '13', '104': '14', '105': '15',
          '106': '16', '107': '17',  '108': '18', '109': '19', '201': '21',
          '202/': '22/', '203': '23', '204': '24', '205': '25', '206': '26',
          '207': '27', '208': '28', '209': '29', '301': '31'}

for k, v in meses.items():
    df['Data'] = df['Data'].str.replace(k, v)

for k, v in dias.items():
    df['Data'] = df['Data'].str.replace(k, v)

for k, v in coerce.items():
    df['Data'] = df['Data'].str.replace(k, v)

df.loc[:, 'Data'] = pd.Series(pd.to_datetime(df['Data'], dayfirst=True,
                                             format='%d/%m/%Y', errors='coerce'),
                              name='Data')

# Renomeando os headers para tirar os espaços
df.columns = df.columns.str.replace(' ', '_')

df = df.sort_values(['Data'], ascending=True)
df = df.reset_index(drop=True)

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/evolucao-aplicacao-doses.csv", index=False)
