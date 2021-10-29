from flask import render_template, request, flash
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms import validators
from wtforms.validators import ValidationError, NumberRange
import pandas as pd
import datetime as dt
from datetime import datetime
from dateutil.parser import parse
import plotly.express as px


url = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Data%20Cleaning/Dados%20tratados/' \
      'covid-estado-sp.csv '

covid_estado = pd.read_csv(url)
covid_estado['Data'] = pd.to_datetime(covid_estado['Data'])


class Form(FlaskForm):
    municipio_field = StringField('Município')
    startdate_field = DateField('Data inicial', format='%Y-%m-%d')
    enddate_field = DateField('Data final', format='%Y-%m-%d')
    submit_field = SubmitField('Pesquisar')


# Decorator / pagina principal
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


# Redirecionamento pagina estados.html
@app.route("/estados", methods=['POST', 'GET'])
def estado_main():
    form = Form()
    maxi = datetime.now().strftime('%Y-%m-%d')
    mini = covid_estado['Data'].min().strftime('%Y-%m-%d')
    start = covid_estado['Data'].min().strftime('%Y-%m-%d')
    end = covid_estado['Data'].max().strftime('%Y-%m-%d')
    ano_inicial, mes_inicial, dia_inicial = start.split('-')
    ano_final, mes_final, dia_final = end.split('-')
    mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
           'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    dia_inicial = dia_inicial.lstrip('0')
    dia_final = dia_final.lstrip('0')

    if request.method != 'POST':
        flash(f''' Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}, 
              até o dia {dia_final} de {mes[int(mes_final) - 1]} de {ano_final} ''')

    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables=[covid_estado.to_html(classes='data')],
                           titles=covid_estado.columns.values)


# noinspection PyUnreachableCode
@app.route("/estados/search", methods=['POST', 'GET'])
def estado_search():
    form = Form()
    maxi = datetime.now().strftime('%Y-%m-%d')
    mini = covid_estado['Data'].min().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start = parse(request.form['startdate_field']).strftime('%Y-%m-%d')
        else:
            start = covid_estado['Data'].min().strftime('%Y-%m-%d')
        if request.form['enddate_field'] != '':
            end = parse(request.form['enddate_field']).strftime('%Y-%m-%d')
        else:
            end = covid_estado['Data'].max().strftime('%Y-%m-%d')

        # Validações por if statement, retorna a pesquisa no 'else' se for validado
        if start > end:
            flash('A data inicial não pode ser mais recente que a data final')
            return render_template('estados.html', form=form)
        elif start <= '2020-02-25':
            flash(f"Pelo menos uma das datas fornecidas antecede a Pandemia no Estado. Por favor, insira datas "
                  f"a partir de 26/02/2020 até {covid_estado['Data'].max().strftime('%d/%m/%Y')}")
            return render_template('estados.html', form=form)
        elif end > (covid_estado['Data'].max().strftime('%Y-%m-%d')):
            flash(f"Não há por enquanto dados referentes a pelo menos uma das datas requeridas. Por favor, insira "
                  f"datas a partir de 26/02/2020 até {covid_estado['Data'].max().strftime('%d/%m/%Y')}")
            return render_template('estados.html', form=form)
        else:
            ano_inicial, mes_inicial, dia_inicial = start.split('-')
            ano_final, mes_final, dia_final = end.split('-')
            mes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
                   'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
            dia_inicial = dia_inicial.lstrip('0')
            dia_final = dia_final.lstrip('0')
            if start != end:
                flash(f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}, "
                      f"até o dia {dia_final} de {mes[int(mes_final) - 1]} de {ano_final}")
            else:
                flash(f"Visualização dos dados do dia {dia_inicial} de {mes[int(mes_inicial) - 1]} de {ano_inicial}")

            inicial = covid_estado['Data'].searchsorted(dt.datetime.strptime(start, '%Y-%m-%d'))
            final = covid_estado['Data'].searchsorted(dt.datetime.strptime(end, '%Y-%m-%d'))
            covid_estado_filter = covid_estado.iloc[inicial:(final + 1)]

            return render_template('estados.html', form=form, min=mini, max=maxi,
                                   tables=[covid_estado_filter.to_html(classes='data')],
                                   titles=covid_estado_filter.columns.values)


# Redirecionamento pagina 'municipios.html
@app.route("/municipios")
def municipios():
    return render_template('municipios.html')


if __name__ == "__main__":
    app.run(debug=True)
