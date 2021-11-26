from flask import render_template, request, flash, Markup
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
        return flash(Markup(f'<h1 class="datas">Visualização dos dados do dia {dia_inicial} de '
                            f'{mes[int(mes_inicial) - 1]} de {ano_inicial}, até o dia {dia_final} de '
                            f'{mes[int(mes_final) - 1]} de {ano_final}</h1>'))


def date_filter_sp(df, start_request, end_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start = parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d')
        else:
            start = df['Data'].min().strftime('%Y-%m-%d')
        if request.form['enddate_field'] != '':
            end = parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d')
        else:
            end = df['Data'].max().strftime('%Y-%m-%d')
    else:
        try:
            start = str(start_request[-1])
            if start_request[-1] == 'dumby':
                start = df['Data'].min().strftime('%Y-%m-%d')
        except IndexError:
            start = df['Data'].min().strftime('%Y-%m-%d')
        try:
            end = str(end_request[-1])
            if end_request[-1] == 'dumby':
                end = df['Data'].max().strftime('%Y-%m-%d')
        except IndexError:
            end = df['Data'].max().strftime('%Y-%m-%d')

    # Validações por if statement, retorna a pesquisa no 'else' se for validado
    if start > end:
        flash(Markup('<h1 class="datas-erro">A data inicial não pode ser mais recente que a data final</h1>'))
        return render_template('estados.html', form=form, min=mini, max=maxi)
    elif start < (df['Data'].min().strftime('%Y-%m-%d')):
        flash(Markup(f'''<h1 class="datas-erro">Pelo menos uma das datas fornecidas antecede a atual base de dados. 
                     Por favor, insira datas a partir de "{df['Data'].min().strftime('%d/%m/%Y')}" até 
                     "{df['Data'].max().strftime("%d/%m/%Y")}"</h1>'''))
        return render_template('estados.html', form=form, min=mini, max=maxi)
    elif end > (df['Data'].max().strftime('%Y-%m-%d')):
        flash(Markup(f'''<h1 class="datas-erro">Não há por enquanto dados referentes a pelo menos uma das datas 
                     requeridas. Por favor, insira datas a partir de "{df['Data'].min().strftime('%d/%m/%Y')}" até 
                     "{df['Data'].max().strftime("%d/%m/%Y")}" para essa base de dados</h1>'''))
        return render_template('estados.html', form=form, min=mini, max=maxi)
    else:
        mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
               'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        ano_inicial, mes_inicial, dia_inicial = start.split('-')
        ano_final, mes_final, dia_final = end.split('-')
        dia_inicial = dia_inicial.lstrip('0')
        dia_final = dia_final.lstrip('0')
        if start != end:
            flash(Markup(f'''<h1 class="datas">Visualização dos dados do dia {dia_inicial} de 
                         {mes[int(mes_inicial) - 1]} de {ano_inicial}, até o dia {dia_final} de 
                         {mes[int(mes_final) - 1]} de {ano_final}</h1>'''))
        else:
            flash(Markup(f'''<h1 class="datas">Visualização dos dados do dia {dia_inicial} de 
                         {mes[int(mes_inicial) - 1]} de {ano_inicial}</h1>'''))

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
            start = parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d')
        else:
            start = df['Data'].min().strftime('%Y-%m-%d')
        if request.form['enddate_field'] != '':
            end = parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d')
        else:
            end = df['Data'].max().strftime('%Y-%m-%d')
    else:
        try:
            start = str(start_request[-1])
            if start_request[-1] == 'dumby':
                start = df['Data'].min().strftime('%Y-%m-%d')
        except IndexError:
            start = df['Data'].min().strftime('%Y-%m-%d')
        try:
            end = str(end_request[-1])
            if end_request[-1] == 'dumby':
                end = df['Data'].max().strftime('%Y-%m-%d')
        except IndexError:
            end = df['Data'].max().strftime('%Y-%m-%d')

    # Validações por if statement, retorna a pesquisa no 'else' se for validado
    if start > end:
        flash(Markup('<h1 class="datas-erro">A data inicial não pode ser mais recente que a data final</h1>'))
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    elif start < (df['Data'].min().strftime('%Y-%m-%d')):
        flash(Markup(f'''<h1 class="datas-erro">Pelo menos uma das datas fornecidas antecede a atual base de dados. 
                     Por favor, insira datas a partir de "{df['Data'].min().strftime('%d/%m/%Y')}" até 
                     "{df['Data'].max().strftime("%d/%m/%Y")}"</h1>'''))
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    elif end > (df['Data'].max().strftime('%Y-%m-%d')):
        flash(Markup(f'''<h1 class="datas-erro">Não há por enquanto dados referentes a pelo menos uma das datas 
                     requeridas. Por favor, insira datas a partir de "{df['Data'].min().strftime('%d/%m/%Y')}" até 
                     "{df['Data'].max().strftime("%d/%m/%Y")}" para essa base de dados</h1>'''))
        return render_template('municipios.html', form=form, min=mini, max=maxi)
    else:
        mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
               'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        ano_inicial, mes_inicial, dia_inicial = start.split('-')
        ano_final, mes_final, dia_final = end.split('-')
        dia_inicial = dia_inicial.lstrip('0')
        dia_final = dia_final.lstrip('0')
        if start != end:
            flash(Markup(f'''<h1 class="datas">Visualização dos dados do dia {dia_inicial} de 
                  {mes[int(mes_inicial) - 1]} de {ano_inicial}, até o dia {dia_final} de {mes[int(mes_final) - 1]} de 
                  {ano_final}</h1>'''))
        else:
            flash(Markup(f'''<h1 class="datas">Visualização dos dados do dia {dia_inicial} de 
                  {mes[int(mes_inicial) - 1]} de {ano_inicial}</h1>'''))

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
