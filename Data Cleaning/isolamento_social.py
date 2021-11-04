from typing import Any
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
download_dir = "/home/sobral/data/isolamento"
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
botao1 = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[13]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[13]/div/ul/li/div/a")
href = elemento.get_attribute("href")
navegador.get(href)

time.sleep(15)

# Automação do reconhecimento de novos dados pelo Pandas
list_of_files = glob.glob('/home/sobral/data/isolamento/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
csv = os.path.abspath(latest_file)

# Leitura pelo Pandas do arquivo csv
df = pd.read_csv(csv, sep=';',
                 usecols=['Município1', 'Código Município IBGE', 'Média de Índice De Isolamento',
                          'Data'],
                 dtype={'Município1': 'category', 'Código Município IBGE': 'int32',
                        'Data': 'category'})

df['Código Município IBGE'] = df['Código Município IBGE'].astype('category')


# Cleaning Data

# Renomeando colunas
df.rename(columns={"Município1": "Município"}, inplace=True)
df.rename(columns={"Código Município IBGE": "codigo_ibge"}, inplace=True)
df.rename(columns={"Média de Índice De Isolamento": "Índice de Isolamento (%)"}, inplace=True)
df.rename(columns={"Data": "data_reg"}, inplace=True)

# Ajustando os valores da coluna "Município" que está em caixa alta
s = df['Município'].str.title()
df.loc[:, 'Município'] = pd.Series(s, name='Município')

# Retirando a "%" para a conversão do índice em int8 sem gerar valores null
df['Índice de Isolamento (%)'] = df['Índice de Isolamento (%)'].str.replace('%', '')
df["Índice de Isolamento (%)"] = df["Índice de Isolamento (%)"].astype(np.int8)

# Usando delimitadores para separar a Data do dia da semana
df.loc[:, 'Dia da Semana'] = df['data_reg']
df['Dia da Semana'] = df['Dia da Semana'].str.replace(',', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('1', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('2', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('3', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('4', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('5', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('6', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('7', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('8', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('9', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('0', '')
df['Dia da Semana'] = df['Dia da Semana'].str.replace('/', '')

df['data_reg'] = df['data_reg'].str.replace('segunda-feira, ', '')
df['data_reg'] = df['data_reg'].str.replace('terça-feira, ', '')
df['data_reg'] = df['data_reg'].str.replace('quarta-feira, ', '')
df['data_reg'] = df['data_reg'].str.replace('quinta-feira, ', '')
df['data_reg'] = df['data_reg'].str.replace('sexta-feira, ', '')
df['data_reg'] = df['data_reg'].str.replace('sábado, ', '')
df['data_reg'] = df['data_reg'].str.replace('domingo, ', '')

# Gerando dois dataframes adjacentes para atribuir o ano correto em cada Data

# Dataframe de dados 2020
duplicates = df.duplicated(['data_reg', 'Município'], keep='last')
df_last = df[~duplicates]
del duplicates
df_last.loc[:, 'Data'] = df['data_reg'] + '/2020'
df_last.loc[:, 'Data'] = pd.Series(pd.to_datetime(df_last['Data'], dayfirst=True,
                                                  format='%d/%m/%Y', errors='coerce'),
                                   name='Data')

df_last = df_last.reset_index(drop=True)
df_last = df_last.sort_values(['Data'], ascending=True)

start = df_last['Data'].searchsorted(dt.datetime.strptime('2020-03-17', '%Y-%m-%d'))
end = df_last['Data'].searchsorted(dt.datetime.strptime('2021-01-01', '%Y-%m-%d'))
df_last = df_last.iloc[start:end]

df_last = df_last.reset_index(drop=True)

# Dataframe de dados 2021
duplicates = df.duplicated(['data_reg', 'Município'], keep='first')
df_first = df[~duplicates]
del duplicates
df_first.loc[:, 'Data'] = df['data_reg'] + '/2021'
df_first.loc[:, 'Data'] = pd.Series(pd.to_datetime(df_first['Data'], dayfirst=True,
                                                   format='%d/%m/%Y', errors='coerce'),
                                    name='Data')

df_first = df_first.reset_index(drop=True)
df_first = df_first.sort_values(['Data'], ascending=True)

yesterday = (datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
start = df_first['Data'].searchsorted(dt.datetime.strptime('2021-01-01', '%Y-%m-%d'))
end = df_first['Data'].searchsorted(dt.datetime.strptime(yesterday, '%Y-%m-%d'))
df_first = df_first.iloc[start:end]

df_first = df_first.reset_index(drop=True)

# Agrupando os dataframes com as datas e fazendo os últimos ajustes:
del df
df = pd.concat([df_first, df_last])
del df_first, df_last
df = df.sort_values(['Data'], ascending=True)

duplicates = df.duplicated(['data_reg', 'Município', 'Dia da Semana'], keep='last')
df = df[~duplicates]
del duplicates
df.drop('data_reg', axis=1, inplace=True)

df['Município'] = df['Município'].astype('category')
df['Dia da Semana'] = df['Dia da Semana'].astype('category')

df = df.reset_index(drop=True)

df.info(verbose=False, memory_usage="deep")
print('\n', df.dtypes, '\n')

# Exportando o Dataframe tratado em arquivo csv
df.to_csv("/home/sobral/Carcara/Aplicação Web/app/data/isolamento-social.csv", index=False)
