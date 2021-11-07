from flask import render_template, request, flash
from MyForms import Form
import pandas as pd
import datetime as dt
from datetime import datetime
from dateutil.parser import parse


def flash_generate(df):
    mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
           'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    start = df['Data'].min().strftime('%Y-%m-%d')
    end = df['Data'].max().strftime('%Y-%m-%d')
    ano_inicial, mes_inicial, dia_inicial = start.split('-')
    ano_final, mes_final, dia_final = end.split('-')
    dia_inicial = dia_inicial.lstrip('0')
    dia_final = dia_final.lstrip('0')
    if request.method != 'POST':
        return flash('\n' + f" Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de "
                     f"{ano_inicial}, até o dia {dia_final} de {mes[int(mes_final) - 1]} de {ano_final} " + '\n')


def date_filter_sp(df, start_request, end_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start = parse(request.form['startdate_field']).strftime('%Y-%m-%d')
        else:
            start = df['Data'].min().strftime('%Y-%m-%d')
        if request.form['enddate_field'] != '':
            end = parse(request.form['enddate_field']).strftime('%Y-%m-%d')
        else:
            end = df['Data'].max().strftime('%Y-%m-%d')
    else:
        try:
            start = str(start_request[-1])
            end = str(end_request[-1])
        except IndexError:
            start = df['Data'].min().strftime('%Y-%m-%d')
            end = df['Data'].max().strftime('%Y-%m-%d')
    # Validações por if statement, retorna a pesquisa no 'else' se for validado
    if start > end:
        flash('\n' + 'A data inicial não pode ser mais recente que a data final' + '\n')
        return render_template('estados.html', form=form, min=mini, max=maxi)
    elif start < (df['Data'].min().strftime('%Y-%m-%d')):
        flash('\n' + f'''Pelo menos uma das datas fornecidas antecede a atual base de dados. Por favor, insira datas a 
              partir de "{df['Data'].min().strftime('%Y-%m-%d')}" até "{df['Data'].max().strftime("%d/%m/%Y")}"'''
              + '\n')
        return render_template('estados.html', form=form, min=mini, max=maxi)
    elif end > (df['Data'].max().strftime('%Y-%m-%d')):
        flash('\n' + f'''Não há por enquanto dados referentes a pelo menos uma das datas requeridas. Por favor, insira 
              datas a partir de "{df['Data'].min().strftime('%Y-%m-%d')}" até "{df['Data'].max().strftime("%d/%m/%Y")}" 
              para essa base de dados''' + '\n')
        return render_template('estados.html', form=form, min=mini, max=maxi)
    else:
        mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
               'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        ano_inicial, mes_inicial, dia_inicial = start.split('-')
        ano_final, mes_final, dia_final = end.split('-')
        dia_inicial = dia_inicial.lstrip('0')
        dia_final = dia_final.lstrip('0')
        if start != end:
            flash('\n' + f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}"
                         f", até o dia {dia_final} de {mes[int(mes_final) - 1]} de {ano_final}" + '\n')
        else:
            flash('\n' + f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}"
                  + '\n')

        headers = list(df.columns.values)
        for header in headers:
            if ('Data' in header) is True:
                inicial = pd.to_datetime(start, format='%Y-%m-%d')
                inicial = (inicial - dt.timedelta(days=1)).strftime("%Y-%m-%d")
                final = pd.to_datetime(end, format='%Y-%m-%d')
                final = (final + dt.timedelta(days=1)).strftime("%Y-%m-%d")
                filterdate = (df['Data'] > inicial) & (df['Data'] < final)
                df = df.loc[filterdate]
            del header
        del headers
        return df


def date_filter_mun(df, start_request, end_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start = parse(request.form['startdate_field']).strftime('%Y-%m-%d')
        else:
            start = df['Data'].min().strftime('%Y-%m-%d')
        if request.form['enddate_field'] != '':
            end = parse(request.form['enddate_field']).strftime('%Y-%m-%d')
        else:
            end = df['Data'].max().strftime('%Y-%m-%d')
    else:
        try:
            start = str(start_request[-1])
            end = str(end_request[-1])
        except IndexError:
            start = df['Data'].min().strftime('%Y-%m-%d')
            end = df['Data'].max().strftime('%Y-%m-%d')
    # Validações por if statement, retorna a pesquisa no 'else' se for validado
    if start > end:
        flash('\n' + 'A data inicial não pode ser mais recente que a data final' + '\n')
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    elif start < (df['Data'].min().strftime('%Y-%m-%d')):
        flash('\n' + f'''Pelo menos uma das datas fornecidas antecede a atual base de dados. Por favor, insira datas a 
              partir de "{df['Data'].min().strftime('%Y-%m-%d')}" até "{df['Data'].max().strftime("%d/%m/%Y")}"'''
              + '\n')
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    elif end > (df['Data'].max().strftime('%Y-%m-%d')):
        flash('\n' + f'''Não há por enquanto dados referentes a pelo menos uma das datas requeridas. Por favor, insira 
              datas a partir de "{df['Data'].min().strftime('%Y-%m-%d')}" até "{df['Data'].max().strftime("%d/%m/%Y")}" 
              para essa base de dados''' + '\n')
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    else:
        mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
               'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        ano_inicial, mes_inicial, dia_inicial = start.split('-')
        ano_final, mes_final, dia_final = end.split('-')
        dia_inicial = dia_inicial.lstrip('0')
        dia_final = dia_final.lstrip('0')
        if start != end:
            flash('\n' + f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}"
                         f", até o dia {dia_final} de {mes[int(mes_final) - 1]} de {ano_final}" + '\n')
        else:
            flash('\n' + f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}"
                  + '\n')

        headers = list(df.columns.values)
        for header in headers:
            if ('Data' in header) is True:
                inicial = pd.to_datetime(start, format='%Y-%m-%d')
                inicial = (inicial - dt.timedelta(days=1)).strftime("%Y-%m-%d")
                final = pd.to_datetime(end, format='%Y-%m-%d')
                final = (final + dt.timedelta(days=1)).strftime("%Y-%m-%d")
                filterdate = (df['Data'] > inicial) & (df['Data'] < final)
                df = df.loc[filterdate]
            del header
        del headers
        return df
