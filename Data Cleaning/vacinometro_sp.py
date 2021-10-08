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

# Automação da coleta dos dataframes pelo selenium

# Primeiro dataframe
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/vacinometro"
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
botao1 = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[14]").click()
elemento1 = navegador.find_element_by_css_selector(
    "article.hrf-entry:nth-child(14) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > "
    "a:nth-child(2)")
href1 = elemento1.get_attribute("href")
navegador.get(href1)

# Segundo dataframe
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir2 = "/home/sobral/data/distribuicao"
prefs2 = {'download.default_directory': download_dir2}

options_chrome2 = Options()
options_chrome2.add_argument("start-maximized")
options_chrome2.add_argument("disable-infobars")
options_chrome2.add_argument("--disable-extensions")
options_chrome2.add_argument('--headless')
options_chrome2.add_argument('--no-sandbox')
options_chrome2.add_argument('--disable-dev-shm-usage')
options_chrome2.add_experimental_option('prefs', prefs2)
desired = options_chrome2.to_capabilities()
desired['loggingPrefs'] = {'performance': 'ALL'}

navegador2 = webdriver.Chrome('chromedriver', options=options_chrome2,
                              desired_capabilities=desired)

navegador2.get("https://www.saopaulo.sp.gov.br/planosp/simi/dados-abertos/")
botao2 = navegador2.find_element_by_xpath("/html/body/section[4]/div/div/article[15]/h3").click()
elemento2 = navegador2.find_element_by_xpath("/html/body/section[4]/div/div/article[15]/div/ul/li/div/a")
href2 = elemento2.get_attribute("href")
navegador2.get(href2)

time.sleep(30)

# Automatação do reconhecimento de novos dados pelo Pandas
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
vacinometro["1ª Dose"] = vacinometro["1ª Dose"].astype(int)
vacinometro["2ª Dose"] = vacinometro["2ª Dose"].astype(int)
vacinometro["3ª Dose"] = vacinometro["3ª Dose"].astype(int)
vacinometro["Dose Única"] = vacinometro["Dose Única"].astype(int)

# Alterando nome de colunas
distribuicao.rename(columns={"Municipio": "Município"}, inplace=True)
distribuicao.rename(columns={"Qtd-Doses-Distribuidas": "Doses Distribuídas"}, inplace=True)

# Agrupando outro dataframe ao principal, para inserir informações adicionais
df = vacinometro.merge(distribuicao, left_on=['Município'],
                       right_on=['Município'], how='inner',
                       suffixes=['_vacinometro', '_distribuicao'])

# Reformatando os valores da coluna "Município", que estavam em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, index=df.index, name='Município')
