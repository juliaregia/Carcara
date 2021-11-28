import pandas as pd
import numpy as np

url1 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-estado-sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-municipios-sp.csv'
url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinometro-sp.csv'
url5 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/evolucao-aplicacao-doses.csv'
url6 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/leitos-uti-enfermaria.csv'
url7 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/isolamento-social.csv'
url8 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinacao-estatisticas.csv'


estatis = pd.read_csv(url8)


# ---------------------------------------  CASOS E ÓBITOS DO ESTADO  ------------------------------------------------ #

covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                   'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
covidsp['Data'] = pd.to_datetime(covidsp['Data'])

# GRÁFICO CASOS POR DIA (Variação nos últimos 7 dias) oie
casos = covidsp[covidsp['Casos por dia']
casos7 = covidsp['Casos por dia'] #7 dias atrás

print(casos)
print(casos7)

x = (casos*100) / casos7-100
print ('Casos em comparação a 7 dias atrás: %.1f' %x, '%')

# GRÁFICO ÓBITOS POR DIA (Variação nos últimos 7 dias)
# GRÁFICO ÓBITOS POR DIA (???)
obi = covidsp['Óbitos por dia'] [107]
obi7 = covidsp['Óbitos por dia'] [100] #7dias atrás

x = (obi*100) / obi7-100
print ('Óbitos em comparação a 7 dias atrás: %.1f' %x, '%')

# GRÁFICO TOTAL DE CASOS (Taxa de Incidência)
pop = 700000
casos = 100

inc = casos / (pop-casos) * 100000
print('Incidência de casos: %.f' %inc, 'a cada 100 mil habitantes')

# GRÁFICO TOTAL DE ÓBITOS (Taxa de Letalidade)
obtotal = covidsp['Total de óbitos'] [107]
casostotal = covidsp['Total de casos'] [107]
obtotal7 = covidsp['Total de óbitos'] [100]
casostotal7 = covidsp['Total de casos'] [100]

let = (obtotal/casostotal) * 100
let7 = (obtotal7/casostotal7) * 100

print('Taxa de letalidade: %.1f' %let, '%')
print('Taxa de letalidade em comparação aos últimos 7 dias: %.1f' %let7, '%')

# ---------------------------------------  VACINAÇÃO DO ESTADO  ------------------------------------------------ #

evoludose = pd.read_csv(url5, dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
evoludose['Data'] = pd.to_datetime(evoludose['Data'])

# EVOLUÇÃO 1ª DOSE (Variação nos últimos 7 dias)
# EVOLUÇÃO 1ª DOSE (???)
dose = evoludose['1ª Dose'] [107]
dose7 = evoludose['1ª Dose'] [100]

evol = (dose*100) / dose7-100
print('Taxa de aplicação da 1ª dose: %.1f' %evol, '% comparado a 7 dias atrás')

# EVOLUÇÃO 2ª DOSE (Variação nos últimos 7 dias)
# EVOLUÇÃO 2ª DOSE (???)
dose = evoludose['2ª Dose'] [107]
dose7 = evoludose['2ª Dose'] [100]

evol = (dose*100) / dose7-100
print('Taxa de aplicação da 2ª dose: %.1f' %evol, '% comparado a 7 dias atrás')

# EVOLUÇÃO 3ª DOSE (Variação nos últimos 7 dias)
# EVOLUÇÃO 3ª DOSE (???)
dose = 500
dose7 = 300

evol = (dose*100) / dose7-100
print('Taxa de aplicação da 3ª dose: %.1f' %evol, '% comparado a 7 dias atrás')

# EVOLUÇÃO DOSE ÚNICA (Variação nos últimos 7 dias)
# EVOLUÇÃO DOSE ÚNICA (???)
dose = 500
dose7 = 300

evol = (dose*100) / dose7-100
print('Taxa de aplicação da dose única: %.1f' %evol, '% comparado a 7 dias atrás')

# COMPARATIVO ENTRE DOSES (???)


# ---------------------------------------  LEITOS DO ESTADO  ------------------------------------------------ #

leitos = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                  'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Nº de novas internações nos últimos 7 dias': 'int32',
                                  'Pacientes em tratamento na UTI': 'int16',
                                  'Total de leitos de UTI destinados à Covid': 'int16',
                                  'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                  'Pacientes em tratamento na Enfermaria': 'int16',
                                  'Total de leitos de Enfermaria destinados à Covid': 'int32'})
leitos['Data'] = pd.to_datetime(leitos['Data'])
leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

# OCUPAÇÃO DOS LEITOS DE UTI E ENFERMARIA NO ESTADO (%) (Variação nos últimos 7 dias)


# NÚMERO DE LEITOS DE UTI E ENFERMARIA NO ESTADO (Número de leitos por pessoa no Estado)


# NÚMERO DE PACIENTES EM TRATAMENTO NA UTI E ENFERMARIA NO ESTADO (???)


# NOVAS INTERNAÇÕES POR DIA NO ESTADO (Variação nos últimos 7 dias)


# ---------------------------------------  ISOLAMENTO DO ESTADO  ------------------------------------------------ #

isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])
isola = isola[isola['Município'] == 'Estado De São Paulo']

# INDICE DE ISOLAMENTO (???)
iso = isola['Índice de Isolamento (%)'] [128]
iso7 = isola['Índice de Isolamento (%)'] [255]
# INDICE DE ISOLAMENTO (Variação dos últimos 7 dias)

ind = (iso*100) / iso7-100
print('Isolamento em relação aos últimos 7 dias: %.1f' %ind, '%')

# ---------------------------------------  CASOS E ÓBITOS MUNICÍPIOS  -------------------------------------------- #

covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                     'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                     'Mesorregião': 'category', 'Microrregião': 'category'})
covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])

# CASOS POR DIA (Variação dos últimos 7 dias)


# ÓBITOS POR DIA (Variação dos últimos 7 dias)


# TOTAL DE CASOS POR MUNICIPIO (Incidencia)


# TOTAL DE OBITOS POR MUNICIPIO (Letalidade)


# ---------------------------------------  VACINA MUNICÍPIOS  -------------------------------------------- #

vacina = pd.read_csv(url4, dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                  'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})

# COMPARATIVO DE APLICAÇAO DAS DOSES ENTRE MUNICIPIOS (Porcentagem da população vacinada *com todas as doses*)


# COMPARATIVO DE DOSES DISTRIBUIDAS ENTRE MUNICIPIOS (Eficácia da aplicação pelo município - Distribuídas/Aplicadas)


# ---------------------------------------  ISOLAMENTO MUNICÍPIOS  -------------------------------------------- #

isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])
isola = isola[isola['Município'] != 'Estado De São Paulo']

# ISOLAMENTO SOCIAL POR MUNICIPIO (Variação nos últimos 7 dias)
