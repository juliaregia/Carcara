from flask import render_template, request, flash
from app import app
from MyForms import Form
from DateFilter import *
from StringEquivalent import *
import pandas as pd
import numpy as np
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

    # Gráfico casos por dia
    fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=['#b76300'],
                  title='Casos por dia no Estado de São Paulo', hover_data=['Data', 'Total de casos', 'Casos por dia'],
                  template='xgridoff')
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Casos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='stack')
    graf1 = fig1.to_html(full_html=False)

    # Gráfico óbitos por dia
    fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=['#b76300'],
                  title='Óbitos por dia no Estado de São Paulo',
                  hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                  template='xgridoff')
    fig2.update_yaxes(showgrid=False),
    fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Óbitos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='stack')
    graf2 = fig2.to_html(full_html=False)

    # Gráfico total de casos
    fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                   line_shape='linear', template='xgridoff',
                   color_discrete_sequence=['#ac5a00'], title='Crescimento do nº de casos no Estado',
                   hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                   render_mode='auto')
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf3 = fig3.to_html(full_html=False)

    # Gráfico total de óbitos
    fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                   line_shape='linear', template='xgridoff', color_discrete_sequence=['#ac5a00'],
                   line_dash_sequence=['solid'],
                   render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                   title='Crescimento do nº de óbitos no Estado')
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf4 = fig4.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4)


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

    # Evolução 1ª dose
    fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Primeira Dose",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf1 = fig1.to_html(full_html=False)

    # Evolução 2ª dose
    fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig2.update_yaxes(showgrid=False),
    fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Segunda Dose",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf2 = fig2.to_html(full_html=False)

    # Evolução 3ª dose
    fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Terceira Dose",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf3 = fig3.to_html(full_html=False)

    # Evolução dose única
    fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='Data', yaxis_title="Dose Única",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf4 = fig4.to_html(full_html=False)

    # Filtros apenas para dados totais
    final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
    evoludose = evoludose.loc[filterdate]

    # Comparativo entre doses
    fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                  template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig5.update_yaxes(showgrid=False),
    fig5.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf5 = fig5.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                           graf4_evoludose=graf4, graf5_evoludose=graf5)


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
    # Filtro para só aparecer os dados referentes ao Estado de SP como um todo
    leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

    # Ocupação dos leitos de UTI e enfermaria no Estado
    fig1 = px.bar(leitos, x='Data', y='Ocupação dos leitos de UTI e Enfermaria (%)', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Ocupação dos leitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf1 = fig1.to_html(full_html=False)

    # Número de leitos de UTI e enfermaria no Estado
    fig2 = px.bar(leitos, x='Data',
                  y=['Total de leitos de UTI destinados à Covid', 'Total de leitos de Enfermaria destinados à Covid'],
                  template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig2.update_yaxes(showgrid=False),
    fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='group')
    graf2 = fig2.to_html(full_html=False)

    # Número de pacientes em tratamento na UTI e enfermaria no Estado
    fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                  template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Pacientes em tratamento",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='group')
    graf3 = fig3.to_html(full_html=False)

    # Novas internações por dia no Estado
    fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                   y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                   color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                            '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                            '#eb9300', '#ffa800'])
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf4 = fig4.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4)


@app.route("/estado/isolamento-social", methods=['GET'])
def isola_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    # Filtragem padrão para o main:
    isola = isola[isola['Município'] == 'Estado De São Paulo']
    final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (isola['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
    filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
    isola = isola.loc[filterdate]
    flash_generate(isola)

    # Histórico do indice de isolamento no estado de SP
    fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana',
                  template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf1 = fig1.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_isola=graf1)


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
        # Gráfico casos por dia
        fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=['#f8ac5b'],
                      title='Casos por dia no Estado de São Paulo',
                      hover_data=['Data', 'Total de casos', 'Casos por dia'],
                      template='xgridoff')
        fig1.update_yaxes(showgrid=False),
        fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Casos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'), barmode='stack')
        graf1 = fig1.to_html(full_html=False)

        # Gráfico óbitos diários
        fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=['#f8ac5b'],
                      title='Óbitos por dia no Estado de São Paulo',
                      hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                      template='xgridoff')
        fig2.update_yaxes(showgrid=False),
        fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Óbitos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'), barmode='stack')
        graf2 = fig2.to_html(full_html=False)

        # Gráfico total de casos
        fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                       line_shape='linear', template='xgridoff',
                       color_discrete_sequence=['#ac5a00'], title='Crescimento do nº de casos no Estado',
                       hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                       render_mode='auto')
        fig3.update_yaxes(showgrid=False),
        fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Total de casos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf3 = fig3.to_html(full_html=False)

        # Gráfico total de óbitos
        fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                       line_shape='linear', template='xgridoff', color_discrete_sequence=['#ac5a00'],
                       line_dash_sequence=['solid'],
                       render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                       title='Crescimento do nº de óbitos no Estado')
        fig4.update_yaxes(showgrid=False),
        fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Total de óbitos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf4 = fig4.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4)


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
        # Evolução 1ª dose
        fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig1.update_yaxes(showgrid=False),
        fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Primeira Dose",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf1 = fig1.to_html(full_html=False)

        # Evolução 2ª dose
        fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig2.update_yaxes(showgrid=False),
        fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Segunda Dose",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf2 = fig2.to_html(full_html=False)

        # Evolução 3ª dose
        fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig3.update_yaxes(showgrid=False),
        fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Terceira Dose",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf3 = fig3.to_html(full_html=False)

        # Evolução dose única
        fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig4.update_yaxes(showgrid=False),
        fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='Data', yaxis_title="Dose Única",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf4 = fig4.to_html(full_html=False)

        # Filtros apenas para dados totais
        final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
        inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
        evoludose = evoludose.loc[filterdate]

        # Comparativo entre doses
        fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                      template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig5.update_yaxes(showgrid=False),
        fig5.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf5 = fig5.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                               graf4_evoludose=graf4, graf5_evoludose=graf5)


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
        # Filtro para só aparecer os dados referentes ao Estado de SP como um todo
        leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

        # Ocupação dos leitos de UTI e enfermaria no Estado
        fig1 = px.bar(leitos, x='Data', y='Ocupação dos leitos de UTI e Enfermaria (%)', template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig1.update_yaxes(showgrid=False),
        fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Ocupação dos leitos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf1 = fig1.to_html(full_html=False)

        # Número de leitos de UTI e enfermaria no Estado
        fig2 = px.bar(leitos, x='Data', y=['Total de leitos de UTI destinados à Covid',
                                           'Total de leitos de Enfermaria destinados à Covid'], template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig2.update_yaxes(showgrid=False),
        fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'), barmode='group')
        graf2 = fig2.to_html(full_html=False)

        # Número de pacientes em tratamento na UTI e enfermaria no Estado
        fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                      template='xgridoff',
                      color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                               '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                               '#eb9300', '#ffa800'])
        fig3.update_yaxes(showgrid=False),
        fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Pacientes em tratamento",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'), barmode='group')
        graf3 = fig3.to_html(full_html=False)

        # Novas internações por dia no Estado
        fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                       y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                       color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                '#eb9300', '#ffa800'])
        fig4.update_yaxes(showgrid=False),
        fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf4 = fig4.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4)


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
        # Filtragem padrão para o search:
        isola = isola[isola['Município'] == 'Estado De São Paulo']

        # Histórico do indice de isolamento no estado de SP
        fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana',
                      template='xgridoff',
                      color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d'])
        fig1.update_yaxes(showgrid=False),
        fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='', yaxis_title="Isolamento Social (%)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf1 = fig1.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               graf1_isola=graf1)


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
    # Filtragem padrão dos dataframes com município em 'main' functions:
    final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (covidmuni['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
    filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
    covidmuni = covidmuni.loc[filterdate]
    covidmuni = covidmuni.query(
        "Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == "
        "'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | "
        "Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")
    flash_generate(covidmuni)

    # Casos diários por município
    fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município', hover_data=['Novos Casos'],
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'],
                  title='Casos confirmados por dia e por Município', template='xgridoff')
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Novos Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='stack')
    graf1 = fig1.to_html(full_html=False)

    # Óbitos diários por município
    fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município', hover_data=['Novos Óbitos'],
                  color_discrete_sequence=[['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                            '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                            '#eb9300', '#ffa800']],
                  title='Óbitos confirmados por dia e por Município', template='xgridoff')
    fig2.update_yaxes(showgrid=False),
    fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Novos Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='stack')
    graf2 = fig2.to_html(full_html=False)

    # Filtros apenas para dados totais
    final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
    covidmuni = covidmuni.loc[filterdate]
    covidmuni = covidmuni.query(
        "Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == "
        "'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | "
        "Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")

    # Total de mortes por município
    fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município',
                  title='Comparativo entre o total de óbitos por Município', template='xgridoff',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig3.update_xaxes(type='date')
    fig3.update_layout(autosize=True)
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf3 = fig3.to_html(full_html=False)

    # Total de casos por município
    fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                  title='Comparativo entre o total de casos por Município', template='xgridoff',
                  color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329',
                                           '#ffb41a',
                                           '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900',
                                           '#eb9300',
                                           '#f59e00', '#ffa800'])
    fig4.update_xaxes(type='date')
    fig4.update_layout(autosize=True)
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf4 = fig4.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3, graf4_covidmuni=graf4)


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

    # Filtro só para 'main' functions:
    vacina = vacina.query(
        "Município == 'São Paulo' | Município == 'Guarulhos' | Município == 'Caçapava' | Município == 'Jacareí' | "
        "Município == 'Campinas' | Município == 'São Bernardo Do Campo' | Município == 'Osasco' | Município == 'Santo "
        "André' | Município == 'São José Dos Campos' | Município == 'Sorocaba'")

    # Comparação entre municípios de aplicação das doses
    fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                        template='xgridoff',
                        color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                 '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                 '#eb9300', '#ffa800'])
    fig1.update_layout(legend_title_text='Dose Aplicada')
    fig1.update_yaxes(showgrid=False),
    fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='Município', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf1 = fig1.to_html(full_html=False)

    # Comparação entre municípios de doses distribuídas
    fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                        color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                 '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                 '#eb9300', '#ffa800'])
    fig2.update_yaxes(showgrid=False),
    fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='Doses Distribuídas', yaxis_title="Município",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'))
    graf2 = fig2.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_vacina=graf1, graf2_vacina=graf2)


@app.route("/municipios/isolamento-social", methods=['GET'])
def isolamuni_main():
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    # Filtragem padrão para o main:
    isola = isola.query(
        "Município == 'São Paulo' | Município == 'São José Dos Campos' | Município == 'Caçapava' | Município == "
        "'Jacareí' | Município == 'Campinas' | Município == 'São José Do Rio Preto' | Município == 'Ribeirão Preto' | "
        "Município == 'Sorocaba' | Município == 'São Bernardo Do Campo' | Município == 'Santo André'")
    final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (isola['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
    filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
    isola = isola.loc[filterdate]
    flash_generate(isola)

    # Histórico do indice de isolamento nos municipios sp
    fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município',
                  color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                           '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                           '#eb9300', '#ffa800'])
    fig1.update_yaxes(showgrid=False),
    fig1.update_traces(hovertemplate=None, )
    fig1.update_layout(autosize=True, margin=dict(t=70, b=0, l=70, r=40),
                       hovermode="x unified",
                       xaxis_tickangle=360,
                       xaxis_title='Data', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                       font=dict(size=18, color='#dc770d'), barmode='stack')
    graf1 = fig1.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi, graf1_isola=graf1)


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
            # Casos diários por município
            fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município',
                          hover_data=['Novos Casos', 'Total de Casos'],
                          color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                   '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                   '#eb9300', '#ffa800'],
                          title='Casos confirmados por dia e por Município', template='xgridoff')
            fig1.update_yaxes(showgrid=False),
            fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Novos Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                               font=dict(size=18, color='#dc770d'), barmode='stack')
            graf1 = fig1.to_html(full_html=False)

            # Óbitos diários por município
            fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município',
                          hover_data=['Novos Casos', 'Total de Casos'],
                          color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                   '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                   '#eb9300', '#ffa800'],
                          title='Óbitos confirmados por dia e por Município', template='xgridoff')
            fig2.update_yaxes(showgrid=False),
            fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Novos Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                               font=dict(size=18, color='#dc770d'), barmode='stack')
            graf2 = fig2.to_html(full_html=False)

            # Filtros apenas para dados totais
            final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
            inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
            filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
            covidmuni = covidmuni.loc[filterdate]

            # Total de mortes por município
            fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município',
                          title='Comparativo do total de óbitos por Município', template='xgridoff',
                          color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                   '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                   '#eb9300', '#ffa800'])
            fig3.update_xaxes(type='date')
            fig3.update_yaxes(showgrid=False),
            fig3.update_layout(autosize=True)
            fig3.update_layout(margin=dict(t=80, b=40, l=85, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='Data', yaxis_title="Total de Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                               font=dict(size=18, color='#dc770d'))
            graf3 = fig3.to_html(full_html=False)

            # Total de casos por município
            fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                          title='Comparativo do total de casos por Município', template='xgridoff',
                          color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                   '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                   '#eb9300', '#ffa800'])
            fig4.update_xaxes(type='date')
            fig4.update_layout(autosize=True)
            fig4.update_yaxes(showgrid=False),
            fig4.update_layout(margin=dict(t=80, b=40, l=85, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='Data', yaxis_title="Total de Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                               font=dict(size=18, color='#dc770d'))
            graf4 = fig4.to_html(full_html=False)
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3,
                                   graf4_covidmuni=graf4)


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
        # Comparação entre municípios de aplicação das doses
        fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                            template='xgridoff',
                            color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                     '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                     '#eb9300', '#ffa800'])
        fig1.update_layout(legend_title_text='Dose Aplicada')
        fig1.update_yaxes(showgrid=False),
        fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='Município', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf1 = fig1.to_html(full_html=False)

        # Comparação entre municípios de doses distribuídas
        fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                            color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                     '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                     '#eb9300', '#ffa800'])
        fig2.update_yaxes(showgrid=False),
        fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                           xaxis_tickangle=360,
                           xaxis_title='Doses Distribuídas', yaxis_title="Município",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                           font=dict(size=18, color='#dc770d'))
        graf2 = fig2.to_html(full_html=False)
        return render_template('municipios.html', form=form, min=mini, max=maxi,
                               graf1_vacina=graf1, graf2_vacina=graf2)


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
            # Histórico do indice de isolamento nos municipios sp
            fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município',
                          template='xgridoff',
                          color_discrete_sequence=['#fbae4d', '#feb03d', '#ffb134', '#ffb41a',
                                                   '#ffb600', '#b76300', '#cc7601', '#d67f01',
                                                   '#eb9300', '#ffa800'])
            fig1.update_yaxes(showgrid=False),
            fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Isolamento Social (%)",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                               font=dict(size=18, color='#dc770d'))
            graf1 = fig1.to_html(full_html=False)
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   graf1_isola=graf1)


if __name__ == "__main__":
    app.run(debug=True)
