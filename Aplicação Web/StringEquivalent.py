from flask import render_template, request, flash
from collections import Iterable
from MyForms import Form
import pandas as pd
import datetime as dt
from datetime import datetime
from dateutil.parser import parse


url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/app/data/vacinometro-sp.csv'


def flatten(list):
    for item in list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def regex_match(word, match):
    transchar = ''
    converted_word = ''
    list = []
    for char in word:
        if char in match.keys():
            transchar = match.get(char)
            list.append(transchar)
        else:
            transchar = char
            list.append(transchar)
    if list is not None:
        converted_word = ''.join(list)
    else:
        converted_word = word
    return converted_word


def regex_change(word, accent):
    converted_word = ''
    try:
        converted_word = accent[word]
    except KeyError:
        converted_word = word
    return converted_word


def regex_match_list(list, match):
    words = []
    for word in list:
        transchar = ''
        converted_word = ''
        chars = []
        for char in word:
            if char in match.keys():
                transchar = match.get(char)
                chars.append(transchar)

            else:
                transchar = char
                chars.append(transchar)

        if chars is not None:
            converted_word = ''.join(chars)
            words.append(converted_word)
        else:
            converted_word = word
            words.append(converted_word)
    return words


def regex_change_list(lista, accent):
    changes = []
    for word in lista:
        converted_word = ''
        word = word.title()
        if word in accent.keys():
            converted_word = accent[word]
            changes.append(converted_word)
        else:
            converted_word = word
            changes.append(converted_word)
    change = list(flatten(changes))
    return change


def city_filter_srag(df, city_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    dict_match = {'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
                  'É': 'E', 'È': 'E', 'Ẽ': 'E', 'Ê': 'E', 'é': 'e', 'è': 'e', 'ẽ': 'e', 'ê': 'e',
                  'Í': 'I', 'Ì': 'I', 'Î': 'I', 'í': 'i', 'ì': 'i', 'î': 'i', 'Ó': 'O', 'Ò': 'O',
                  'Õ': 'O', 'Ô': 'O', 'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'Ú': 'U', 'Ù': 'U',
                  'Û': 'U', 'ú': 'u', 'ù': 'u', 'û': 'u', 'Ç': 'C', 'ç': 'c'}
    searches = []
    names = []
    if request.method == 'POST':
        if request.form['municipio_field'] != '':
            search = str(request.form.get('municipio_field'))
            searches = search.split(', ')
        else:
            df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | "
                          "Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | "
                          "Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == 'São Bernardo do "
                          "Campo' | Município == 'Santo André'")
            flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                         f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                         f"personalizada." + '\n')
            return df
    else:
        try:
            search = city_request[-1]
            searches = search.split(', ')
            if city_request[-1] == 'dumby':
                df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == "
                              "'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José "
                              "do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == "
                              "'São Bernardo do Campo' | Município == 'Santo André'")
                flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                             f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                             f"personalizada." + '\n')
                return df
        except IndexError:
            df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == "
                          "'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José "
                          "do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == "
                          "'São Bernardo do Campo' | Município == 'Santo André'")
            flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                         f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                         f"personalizada." + '\n')
            return df
    filter = regex_match_list(searches, dict_match)
    dfs = {}
    for item in filter:
        result = df[df.Município.str.contains(item, case=False)]
        if result.empty is False:
            dfs[item] = result
            names.append(item.title())
        else:
            flash('\n' + f'Não há dados referentes à "{item}"' + '\n')
            del item
    names = list(dict.fromkeys(names))
    names = ', '.join(names)
    if len(dfs) >= 2:
        df = pd.concat(dfs.values())
        duplicates = df.duplicated(keep='first')
        df = df[~duplicates]
        flash('\n' + f'Resultados referentes à busca "{names}"' + '\n')
        return df
    elif len(dfs) == 1:
        for v in dfs.values():
            df = v
        flash('\n' + f'Resultados referentes à busca "{names}"' + '\n')
        return df
    else:
        flash('\n' + 'Não há resultados referentes à busca por município' + '\n')
        return render_template('municipios.html', form=form, min=mini, max=maxi)


def city_filter_all(df, city_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    dict_match = {'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
                  'É': 'E', 'È': 'E', 'Ẽ': 'E', 'Ê': 'E', 'é': 'e', 'è': 'e', 'ẽ': 'e', 'ê': 'e',
                  'Í': 'I', 'Ì': 'I', 'Î': 'I', 'í': 'i', 'ì': 'i', 'î': 'i', 'Ó': 'O', 'Ò': 'O',
                  'Õ': 'O', 'Ô': 'O', 'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'Ú': 'U', 'Ù': 'U',
                  'Û': 'U', 'ú': 'u', 'ù': 'u', 'û': 'u', 'Ç': 'C', 'ç': 'c'}
    searches = []
    names = []
    vac = pd.read_csv(url4, usecols=['Município'], dtype={'Município': 'category'})
    vac = vac.values.tolist()
    vac = list(flatten(vac))
    vac = list(dict.fromkeys(vac))
    dict_accent = {}
    for x in vac:
        transx = regex_match(x, dict_match)
        dict_accent[transx] = x
    if request.method == 'POST':
        if request.form['municipio_field'] != '':
            search = str(request.form.get('municipio_field'))
            searches = search.split(', ')
        else:
            df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | "
                          "Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | "
                          "Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == 'São Bernardo do "
                          "Campo' | Município == 'Santo André'")
            flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                         f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                         f"personalizada." + '\n')
            return df
    else:
        try:
            search = city_request[-1]
            searches = search.split(', ')
            if city_request[-1] == 'dumby':
                df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == "
                              "'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José "
                              "do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == "
                              "'São Bernardo do Campo' | Município == 'Santo André'")
                flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                             f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                             f"personalizada." + '\n')
                return df
        except IndexError:
            df = df.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == "
                          "'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José "
                          "do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == "
                          "'São Bernardo do Campo' | Município == 'Santo André'")
            flash('\n' + f"Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os maiores "
                         f"números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa "
                         f"personalizada." + '\n')
            return df
    filter = regex_match_list(searches, dict_match)
    filter = regex_change_list(filter, dict_accent)
    dfs = {}
    filter = list(dict.fromkeys(filter))
    for item in filter:
        result = df[df.Município.str.contains(item, case=False)]
        if result.empty is False:
            dfs[item] = result
            names.append(item.title())
        else:
            flash('\n' + f'Não há dados referentes à "{item}"' + '\n')
            del item
    names = list(dict.fromkeys(names))
    names = ', '.join(names)
    if len(dfs) >= 2:
        df = pd.concat(dfs.values())
        flash('\n' + f'Resultados referentes à busca "{names}"' + '\n')
        return df
    elif len(dfs) == 1:
        for v in dfs.values():
            df = v
        flash('\n' + f'Resultados referentes à busca "{names}"' + '\n')
        return df
    else:
        flash('\n' + 'Não há resultados referentes à busca por município' + '\n')
        return render_template('municipios.html', form=form, min=mini, max=maxi)
