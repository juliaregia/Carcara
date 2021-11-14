from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import psutil
import requests
import datetime as dt
from datetime import datetime
import sys
import os
import glob
import pytz
import time
import datetime
import time
from dateutil.parser import parse as parsedate


utc = pytz.UTC
process = "chromedriver"


# Coletando covid_estado
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

r = requests.head(href)
url_date = r.headers['last-modified']
url_date = parsedate(url_date)
print('A última atualização do site foi:', url_date)

list_of_files = glob.glob('/home/sobral/data/covid_estado/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados covid_estado, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/covid_estado")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('covid_estado atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados covid_estado. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')


# Coletando evolucao-doses
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

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[19]/div/div/p[4]")
time.sleep(3)
url_date = versao.text
url_date = url_date.replace('–', ' ')
url_date = url_date[-13:]
url_date = url_date.replace('/', '-')
url_date = '2021-' + url_date
url_date = dt.datetime.strptime(url_date, '%Y-%d-%m %H:%M')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/evolucao-doses/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados evolucao-doses, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/evolucao-doses")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('evolucao-doses atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados evolucao-doses. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')

for proc in psutil.process_iter():
    if proc.name() == process:
        for child in proc.children(recursive=True):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        proc.kill()
    else:
        pass

time.sleep(5)


# Coletando isolamento
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

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[13]/div/div/p[2]")
time.sleep(3)
url_date = versao.text
url_date = url_date[-5:]
url_date = url_date.replace('/', '-')
url_date = url_date + '-2021'
url_date = dt.datetime.strptime(url_date, '%d-%m-%Y')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/isolamento/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados isolamento, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/isolamento")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('isolamento atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados isolamento. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')


# Coletando leitos
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

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[7]/div/div/p[2]")
time.sleep(3)
url_date = versao.text
url_date = url_date[-5:]
url_date = url_date.replace('/', '-')
url_date = url_date + '-2021'
url_date = dt.datetime.strptime(url_date, '%d-%m-%Y')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/leitos/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados leitos, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/leitos")]):
        for i in range(9999):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('leitos atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados leitos. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')

for proc in psutil.process_iter():
    if proc.name() == process:
        for child in proc.children(recursive=True):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        proc.kill()
    else:
        pass

time.sleep(5)


# Coletando srag
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

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[5]/div/div/p[2]")
time.sleep(3)
url_date = versao.text
url_date = url_date[-5:]
url_date = url_date.replace('/', '-')
url_date = url_date + '-2021'
url_date = dt.datetime.strptime(url_date, '%d-%m-%Y')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/srag/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados srag, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/srag")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('srag atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados srag. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')


# Coletando estatisticas-gerais
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/estatisticas-vacina"
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
botao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[20]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[20]/div/ul/li/div/a")
href = elemento.get_attribute("href")

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[20]/div/div/p[4]")
time.sleep(3)
url_date = versao.text
url_date = url_date.replace('–', ' ')
url_date = url_date[-13:]
url_date = url_date.replace('/', '-')
url_date = '2021-' + url_date
url_date = dt.datetime.strptime(url_date, '%Y-%d-%m %H:%M')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/estatisticas-vacina/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados estatisticas-vacina, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in
                   os.listdir("/home/sobral/data/estatisticas-vacina")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('estatisticas-vacina atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados estatisticas-vacina. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')

for proc in psutil.process_iter():
    if proc.name() == process:
        for child in proc.children(recursive=True):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        proc.kill()
    else:
        pass

time.sleep(5)


# Coletando vacinometro
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
botao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[14]").click()
elemento = navegador.find_element_by_css_selector(
    "article.hrf-entry:nth-child(14) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > "
    "a:nth-child(2)")
href = elemento.get_attribute("href")

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[14]/div/div/p[3]")
time.sleep(3)
url_date = versao.text
url_date = url_date.replace('–', ' ')
url_date = url_date[-13:]
url_date = url_date.replace('/', '-')
url_date = '2021-' + url_date
url_date = dt.datetime.strptime(url_date, '%Y-%d-%m %H:%M')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/vacinometro/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados vacinometro, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/vacinometro")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('vacinometro atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados vacinometro. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')


# Coletando distribuicao
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')
download_dir = "/home/sobral/data/distribuicao"
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
botao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[15]/h3").click()
elemento = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[15]/div/ul/li/div/a")
href = elemento.get_attribute("href")

versao = navegador.find_element_by_xpath("/html/body/section[4]/div/div/article[15]/div/div/p[4]")
time.sleep(3)
url_date = versao.text
url_date = url_date.replace('–', ' ')
url_date = url_date[-13:]
url_date = url_date.replace('/', '-')
url_date = '2021-' + url_date
url_date = dt.datetime.strptime(url_date, '%Y-%d-%m %H:%M')
print('A última atualização do site foi:', url_date)
url_date = utc.localize(url_date)

list_of_files = glob.glob('/home/sobral/data/distribuicao/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
file_time = dt.datetime.fromtimestamp(os.path.getmtime(latest_file))
file_time = utc.localize(file_time)

if url_date > file_time:
    print(f'Há atualizações da base de dados distribuicao, data: {url_date}. '
          f'Download iniciando agora...')
    navegador.get(href)
    time.sleep(5)
    for i in range(9999):
        while any([filename.endswith(".crdownload") for filename in os.listdir("/home/sobral/data/distribuicao")]):
            print(f'Baixando...{i + 1}s')
            i = i + 1
            time.sleep(1)
    print('distribuicao atualizado com sucesso!' + '\n')
else:
    print(f'Não há atualizações para a base de dados distribuicao. O último arquivo '
          f'baixado é a versão mais atualizada ({file_time})' + '\n')

for proc in psutil.process_iter():
    if proc.name() == process:
        for child in proc.children(recursive=True):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        proc.kill()
    else:
        pass


time.sleep(5)
print('ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!' + '\n')
time.sleep(5)
os._exit(os.EX_OK)
