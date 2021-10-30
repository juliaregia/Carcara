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
download_dir = "/home/sobral/data/unidade-hospitalar"
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
botao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[8]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[8]/div/ul/li[1]/div/a")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(15)

# Automatação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/unidade-hospitalar/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura do dataframe pelo pandas
df = pd.read_csv(csv, sep=';')

# Renomeando colunas
df = df.rename(columns={'Municipio': 'Município'})
df = df.rename(columns={'Nome Fantasia': 'Unidade Hospitalar'})
df = df.rename(columns={'Leitos Ocupados / Enfermaria': 'Leitos de Enfermaria Ocupados'})
df = df.rename(columns={'Leitos Ocupados / UTI': 'Leitos de UTI Ocupados'})
df = df.rename(columns={'DRS Nome': 'Departamento Regional de Saúde'})

# Ajustando os valores das colunas que estão em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, index=df.index, name='Município')
s = df['Unidade Hospitalar'].str.title()
df.loc[:, 'Unidade Hospitalar'] = pd.Series(s, index=df.index,
                                            name='Unidade Hospitalar')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/leitos-unidade-hospitalar.csv", index=False)
