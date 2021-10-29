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

# Automação da coleta dos dataframes
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/srag"
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
botao1 = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[5]/h3/span").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[5]/div/ul/li[1]/div/a")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(330)

# Automação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/srag/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';')

# Cleaning Data

# Excluindo dados referentes a outros Estados
df.rename(columns={"Sg Uf": "UF"}, inplace=True)
df.drop(df[df.UF != 'SP'].index, inplace=True)

# Excluindo dados referentes a casos de SRAG alheios à covid-19
df.rename(columns={"OUTRAS SRAG": "Doença"}, inplace=True)
df.drop(df[df.Doença != 'COVID 19'].index, inplace=True)

# Deletando colunas sem dados relevantes
df.drop('UF', axis=1, inplace=True)
df.drop('Última Data de Notificação', axis=1, inplace=True)
df.drop('Cs Raca', axis=1, inplace=True)
df.drop('Cs Sexo', axis=1, inplace=True)
df.drop('Quantidade Homens', axis=1, inplace=True)
df.drop('Quantidade Mulheres', axis=1, inplace=True)
df.drop('Quantidade de Casos', axis=1, inplace=True)
df.drop('Cs Raca_ID', axis=1, inplace=True)
df.drop('Cs Sexo_ID', axis=1, inplace=True)
df.drop('Faixa etária', axis=1, inplace=True)
df.drop('EVOLUCAO_NOT_NULL', axis=1, inplace=True)

# Renomeando colunas
df.rename(columns={"Nu Idade N": "Idade do paciente"}, inplace=True)
df.rename(columns={"Grupo de Idades": "Faixa Etária"}, inplace=True)
df.rename(columns={"Municípios": "Município"}, inplace=True)

# Ajustando valores que estão em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, name='Município')
s = df['Doença'].str.title()
df.loc[:, 'Doença'] = pd.Series(s, name='Doença')

# Transformando a coluna de Data de Notificação em Datetime type
df.loc[:, 'Data de Notificação'] = pd.Series(pd.to_datetime(df['Data de Notificação'],
                                                            dayfirst=True, format='%d/%m/%Y',
                                                            errors='coerce'),
                                             name='Data de Notificação')

# Alterando a " " pelo "-" na coluna "Doença"
df['Doença'] = df['Doença'].str.replace(' ', '-')

# Padronizando Missing Values encontrados na coluna "Evolução"
df = df.fillna(value='Não informado')

# Renomeando os headers para tirar os espaços
df.columns = df.columns.str.replace(' ', '_')

# Ordenando a coluna "Data de Notificação" e resetando o index
df = df.reset_index(drop=True)

df = df.sort_values(['Data_de_Notificação'], ascending=True)

df = df[[c for c in df.columns if c not in ['index']]]
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
    df = df.to_frame(index=False)
df = df.reset_index().drop('index', axis=1, errors='ignore')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/srag-covid.csv", index=False)
