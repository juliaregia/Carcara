from flask import render_template, request, flash
from app import app
from MyForms import Form
from DateFilter import *
from StringEquivalent import *
import pandas as pd
import datetime as dt
from datetime import datetime
from dateutil.parser import parse
import plotly.express as px


start_request = []
end_request = []
city_request = []

url1 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-estado-sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-municipios-sp.csv'
url3 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/srag-covid.csv'
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

'''
covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                   'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
covidsp['Data'] = pd.to_datetime(covidsp['Data'])


covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                     'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                     'Mesorregião': 'category', 'Microrregião': 'category'})
covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])


srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
srag['Data'] = pd.to_datetime(srag['Data'])


vacina = pd.read_csv(url4, dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                  'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})


evoludose = pd.read_csv(url5, dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
evoludose['Data'] = pd.to_datetime(evoludose['Data'])


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


isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])


estatis = pd.read_csv(url8)
'''


####################################################################################################################


# ROUTE PÁGINA INICIAL (INDEX)
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


####################################################################################################################


# ROUTES INICIAIS DA PÁGINA DOS MUNICÍPIOS
@app.route("/estado", methods=['GET'])
@app.route("/estado/covidsp", methods=['GET'])
def covidsp_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                       'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    flash_generate(covidsp)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables_covidsp=[covidsp.to_html(classes='data')],
                           titles_covidsp=covidsp.columns.values)


@app.route("/estado/srag", methods=['GET'])
def srag_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
    srag['Data'] = pd.to_datetime(srag['Data'])
    flash_generate(srag)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables_srag=[srag.to_html(classes='data')],
                           titles_srag=srag.columns.values)


@app.route("/estado/vacina", methods=['GET'])
def evoludose_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    evoludose = pd.read_csv(url5,
                            dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
    evoludose['Data'] = pd.to_datetime(evoludose['Data'])
    flash_generate(evoludose)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables_evoludose=[evoludose.to_html(classes='data')],
                           titles_evoludose=evoludose.columns.values)


@app.route("/estado/leitos", methods=['GET'])
def leitos_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
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
    flash_generate(leitos)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables_leitos=[leitos.to_html(classes='data')],
                           titles_leitos=leitos.columns.values)


@app.route("/estado/isolamento-social", methods=['GET'])
def isola_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    flash_generate(isola)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           tables_isola=[isola.to_html(classes='data')],
                           titles_isola=isola.columns.values)


######################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DO ESTADO
@app.route("/estado/covidsp/search", methods=['POST', 'GET'])
def covidsp_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
        print(f'O start agora eh {start_request[-1]}')
        end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
        print(f'O end agora eh {end_request[-1]}')

    covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                       'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    covidsp = date_filter_sp(covidsp, start_request, end_request)

    if not isinstance(covidsp, pd.DataFrame):
        return covidsp
    else:
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               tables_covidsp=[covidsp.to_html(classes='data')],
                               titles_covidsp=covidsp.columns.values)


@app.route("/estado/srag/search", methods=['POST', 'GET'])
def srag_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
        print(f'O start agora eh {start_request[-1]}')
        end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
        print(f'O end agora eh {end_request[-1]}')

    srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
    srag['Data'] = pd.to_datetime(srag['Data'])
    srag = date_filter_sp(srag, start_request, end_request)

    if not isinstance(srag, pd.DataFrame):
        return srag
    else:
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               tables_srag=[srag.to_html(classes='data')],
                               titles_srag=srag.columns.values)


@app.route("/estado/vacina/search", methods=['POST', 'GET'])
def evoludose_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
        print(f'O start agora eh {start_request[-1]}')
        end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
        print(f'O end agora eh {end_request[-1]}')

    evoludose = pd.read_csv(url5,
                            dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                   'Dose Única': 'int32'})
    evoludose['Data'] = pd.to_datetime(evoludose['Data'])
    evoludose = date_filter_sp(evoludose, start_request, end_request)

    if not isinstance(evoludose, pd.DataFrame):
        return evoludose
    else:
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               tables_evoludose=[evoludose.to_html(classes='data')],
                               titles_evoludose=evoludose.columns.values)


@app.route("/estado/leitos/search", methods=['POST', 'GET'])
def leitos_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
        print(f'O start agora eh {start_request[-1]}')
        end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
        print(f'O end agora eh {end_request[-1]}')
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
    leitos = date_filter_sp(leitos, start_request, end_request)

    if not isinstance(leitos, pd.DataFrame):
        return leitos
    else:
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               tables_leitos=[leitos.to_html(classes='data')],
                               titles_leitos=leitos.columns.values)


@app.route("/estado/isolamento-social/search", methods=['POST', 'GET'])
def isola_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
        print(f'O start agora eh {start_request[-1]}')
        end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
        print(f'O end agora eh {end_request[-1]}')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category',
                               'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    isola = date_filter_sp(isola, start_request, end_request)

    if not isinstance(isola, pd.DataFrame):
        return isola
    else:
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               tables_isola=[isola.to_html(classes='data')],
                               titles_isola=isola.columns.values)


####################################################################################################################


# ROUTES INICIAIS DA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios", methods=['GET'])
@app.route("/municipios/covidsp", methods=['GET'])
def covidmuni_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                         'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                         'Mesorregião': 'category', 'Microrregião': 'category'})
    covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])
    flash_generate(covidmuni)
    return render_template('municipios.html', form=form, min=mini, max=maxi)


@app.route("/municipios/srag", methods=['GET'])
def sragmuni_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
    srag['Data'] = pd.to_datetime(srag['Data'])
    flash_generate(srag)
    return render_template('municipios.html', form=form, min=mini, max=maxi)


@app.route("/municipios/vacina", methods=['GET'])
def vacina_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    flash('Totalização da campanha vacinal por Município')
    return render_template('municipios.html', form=form, min=mini, max=maxi)


@app.route("/municipios/isolamento-social", methods=['GET'])
def isolamuni_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    flash_generate(isola)
    return render_template('municipios.html', form=form, min=mini, max=maxi)


###################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios/covidsp/search", methods=['POST', 'GET'])
def covidmuni_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] or request.form['enddate_field'] != '':
            start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
            print(f'O start agora é: {start_request[-1]}')
            end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
            print(f'O end agora é: {end_request[-1]}')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')

    covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                         'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                         'Mesorregião': 'category', 'Microrregião': 'category'})
    covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])
    covidmuni = date_filter_mun(covidmuni, start_request, end_request)

    if not isinstance(covidmuni, pd.DataFrame):
        return covidmuni
    else:
        covidmuni = city_filter_all(covidmuni, city_request)

        if not isinstance(covidmuni, pd.DataFrame):
            return covidmuni
        else:
            fig = px.bar(covidmuni, x='Data', y='Novos Casos', color_discrete_sequence=['#f8ac5b'],
                         title='Novos Casos por Município', hover_data=['Total de Casos'],
                         template='xgridoff')
            fig.update_xaxes(type='date')
            fig.update_layout(autosize=True)
            grafico = fig.to_html(full_html=False)
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   grafico=grafico)


@app.route("/municipios/srag/search", methods=['POST', 'GET'])
def sragmuni_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] or request.form['enddate_field'] != '':
            start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
            print(f'O start agora é: {start_request[-1]}')
            end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
            print(f'O end agora é: {end_request[-1]}')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')

    srag = pd.read_csv(url3, dtype={'Município': 'category', 'Faixa Etária': 'category', 'Evolução': 'category'})
    srag['Data'] = pd.to_datetime(srag['Data'])
    srag = date_filter_mun(srag, start_request, end_request)

    if not isinstance(srag, pd.DataFrame):
        return srag
    else:
        srag = city_filter_srag(srag, city_request)

        if not isinstance(srag, pd.DataFrame):
            return srag
        else:
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   tables_srag=[srag.to_html(classes='data')],
                                   titles_srag=srag.columns.values)


@app.route("/municipios/vacina/search", methods=['POST', 'GET'])
def vacina_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] or request.form['enddate_field'] != '':
            start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
            print(f'O start agora é: {start_request[-1]}')
            end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
            print(f'O end agora é: {end_request[-1]}')
            flash('"Vacinômetro" é uma base de dados que totaliza os números da vacinação por município sem fornecer '
                  'as datas de registro. Por isso, tente filtrá-lo apenas por Município')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')

    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    vacina = city_filter_all(vacina, city_request)

    if not isinstance(vacina, pd.DataFrame):
        return vacina
    else:
        return render_template('municipios.html', form=form, min=mini, max=maxi,
                               tables_vacina=[vacina.to_html(classes='data')],
                               titles_vacina=vacina.columns.values)


@app.route("/municipios/isolamento-social/search", methods=['POST', 'GET'])
def isolamuni_search():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] or request.form['enddate_field'] != '':
            start_request.append(parse(request.form['startdate_field']).strftime('%Y-%m-%d'))
            print(f'O start agora é: {start_request[-1]}')
            end_request.append(parse(request.form['enddate_field']).strftime('%Y-%m-%d'))
            print(f'O end agora é: {end_request[-1]}')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')

    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    isola = date_filter_mun(isola, start_request, end_request)

    if not isinstance(isola, pd.DataFrame):
        return isola
    else:
        isola = city_filter_all(isola, city_request)

        if not isinstance(isola, pd.DataFrame):
            return isola
        else:
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   tables_isola=[isola.to_html(classes='data')],
                                   titles_isola=isola.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
