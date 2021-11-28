from flask import render_template, request, flash, Markup
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
import random


start_request = []
end_request = []
city_request = []
form_start = []
form_end = []
form_city = []


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


palette = ['rgba(220, 119, 13, 0.8)', 'rgba(249, 212, 156, 0.6)', 'rgba(248, 172, 91, 0.9)',
           'rgba(220, 119, 13, 0.5)', 'rgba(249, 212, 156, 0.5)', 'rgba(220, 119, 13, 0.7)',
           'rgba(248, 172, 91, 0.7)', 'rgba(220, 119, 13, 0.2)', 'rgba(248, 172, 91, 0.5)',
           'rgba(220, 119, 13, 0.6)', 'rgba(249, 212, 156, 0.4)', 'rgba(220, 119, 13, 0.9)',
           'rgba(220, 119, 13, 0.4)', 'rgba(220, 119, 13, 0.9)', 'rgba(248, 172, 91, 0.6)',
           'rgba(172, 90, 0, 0.8)', 'rgba(249, 212, 156, 0.8)', 'rgba(249, 212, 156, 0.2)',
           'rgba(172, 90, 0, 0.3)', 'rgba(248, 172, 91, 0.4)', 'rgba(249, 212, 156, 0.9)',
           'rgba(220, 119, 13, 0.7)', 'rgba(220, 119, 13, 0.4)', 'rgba(248, 172, 91, 0.3)',
           'rgba(220, 119, 13, 0.6)', 'rgba(249, 212, 156, 0.3)', 'rgba(220, 119, 13, 0.3)',
           'rgba(220, 119, 13, 0.2)', 'rgba(249, 212, 156, 0.7)', 'rgba(248, 172, 91, 0.8)',
           'rgba(172, 90, 0, 0.5)', 'rgba(248, 172, 91, 0.2)']


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
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                       'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    flash_generate(covidsp)

    # Gráfico casos por dia
    fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=palette,
                  title='<b>Casos por dia no Estado de São Paulo</b>',
                  hover_data=['Data', 'Total de casos', 'Casos por dia'], template='xgridoff')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2000),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Casos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Gráfico óbitos por dia
    fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=palette,
                  title='Óbitos por dia no Estado de São Paulo',
                  hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                  template='xgridoff')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=100),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Óbitos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)

    # Gráfico total de casos
    fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                   line_shape='linear', template='xgridoff',
                   color_discrete_sequence=palette, title='Crescimento do nº de casos no Estado',
                   hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                   render_mode='auto')
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500000),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Total de casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)

    # Gráfico total de óbitos
    fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                   line_shape='linear', template='xgridoff', color_discrete_sequence=palette,
                   line_dash_sequence=['solid'],
                   render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                   title='Crescimento do nº de óbitos no Estado')
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=15000),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Total de óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4)


@app.route("/estado/vacina", methods=['GET'])
def evoludose_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    evoludose = pd.read_csv(url5,
                            dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
    evoludose['Data'] = pd.to_datetime(evoludose['Data'])
    flash_generate(evoludose)

    # Evolução 1ª dose
    fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='Evolução da aplicação da 1ª dose')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Evolução 2ª dose
    fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='Evolução da aplicação da 2ª dose')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)

    # Evolução 3ª dose
    fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='Evolução da aplicação da 3ª dose')
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)

    # Evolução dose única
    fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                  color_discrete_sequence=palette, title='Evolução da aplicação da dose única')
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='Data', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)

    # Filtros apenas para dados totais
    final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
    evoludose = evoludose.loc[filterdate]

    # Comparativo entre doses
    fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                  template='xgridoff',
                  color_discrete_sequence=palette, title='Comparativo entre a aplicação das doses')
    fig5.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=20000),
    fig5.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_tickangle=360, xaxis_title='', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='Última atualização: %d de %b de %y', xaxis_hoverformat='%b %d, %Y')
    graf5 = fig5.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                           graf4_evoludose=graf4, graf5_evoludose=graf5)


@app.route("/estado/leitos", methods=['GET'])
def leitos_main():
    random.shuffle(palette)
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
                  color_discrete_sequence=palette, title='Ocupação dos leitos de UTI e Enfermaria no Estado')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Ocupação dos leitos (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Número de leitos de UTI e enfermaria no Estado
    fig2 = px.bar(leitos, x='Data',
                  y=['Total de leitos de UTI destinados à Covid', 'Total de leitos de Enfermaria destinados à Covid'],
                  template='xgridoff', title='Total de leitos de UTI e Enfermaria destinados à COVID-19',
                  color_discrete_sequence=palette)
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)

    # Número de pacientes em tratamento na UTI e enfermaria no Estado
    fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                  template='xgridoff', title='Total de pacientes nas UTIs e Enfermarias',
                  color_discrete_sequence=palette)
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Pacientes em tratamento",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)

    # Novas internações por dia no Estado
    fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                   y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                   color_discrete_sequence=palette, title='Novas internações por dia no Estado')
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4)


@app.route("/estado/isolamento-social", methods=['GET'])
def isola_main():
    random.shuffle(palette)
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
                  template='xgridoff', title='Índice de Isolamento Social do Estado',
                  color_discrete_sequence=palette)
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)
    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_isola=graf1)


######################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DO ESTADO
@app.route("/estado/covidsp/search", methods=['POST', 'GET'])
def covidsp_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

    covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                       'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    covidsp = date_filter_sp(covidsp, start_request, end_request)

    if not isinstance(covidsp, pd.DataFrame):
        return covidsp
    else:
        # Gráfico casos por dia
        fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=palette,
                      title='Casos por dia no Estado de São Paulo',
                      hover_data=['Data', 'Total de casos', 'Casos por dia'],
                      template='xgridoff')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2000),
        fig1.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Casos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)

        # Gráfico óbitos diários
        fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=palette,
                      title='Óbitos por dia no Estado de São Paulo',
                      hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                      template='xgridoff')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=100),
        fig2.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Óbitos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)

        # Gráfico total de casos
        fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                       line_shape='linear', template='xgridoff',
                       color_discrete_sequence=palette, title='Crescimento do nº de casos no Estado',
                       hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                       render_mode='auto')
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500000),
        fig3.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Total de casos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)

        # Gráfico total de óbitos
        fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                       line_shape='linear', template='xgridoff', color_discrete_sequence=palette,
                       line_dash_sequence=['solid'],
                       render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                       title='Crescimento do nº de óbitos no Estado')
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=15000),
        fig4.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Total de óbitos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4)


@app.route("/estado/vacina/search", methods=['POST', 'GET'])
def evoludose_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

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
                      color_discrete_sequence=palette, title='Evolução da aplicação da 1ª dose')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
        fig1.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)

        # Evolução 2ª dose
        fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                      color_discrete_sequence=palette, title='Evolução da aplicação da 2ª dose')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
        fig2.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)

        # Evolução 3ª dose
        fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                      color_discrete_sequence=palette, title='Evolução da aplicação da 3ª dose')
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
        fig3.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)

        # Evolução dose única
        fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                      color_discrete_sequence=palette, title='Evolução da aplicação da dose única')
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
        fig4.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='Data', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)

        # Filtros apenas para dados totais
        final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
        inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
        evoludose = evoludose.loc[filterdate]

        # Comparativo entre doses
        fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                      template='xgridoff', title='Comparativo entre a aplicação das doses',
                      color_discrete_sequence=palette)
        fig5.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=20000),
        fig5.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_tickangle=360, xaxis_title='', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='Última atualização: %d de %b de %y', xaxis_hoverformat='%b %d, %Y')
        graf5 = fig5.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                               graf4_evoludose=graf4, graf5_evoludose=graf5)


@app.route("/estado/leitos/search", methods=['POST', 'GET'])
def leitos_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

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
                      color_discrete_sequence=palette, title='Ocupação dos leitos de UTI e Enfermaria no Estado')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
        fig1.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Ocupação dos leitos (%)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)

        # Número de leitos de UTI e enfermaria no Estado
        fig2 = px.bar(leitos, x='Data', y=['Total de leitos de UTI destinados à Covid',
                                           'Total de leitos de Enfermaria destinados à Covid'], template='xgridoff',
                      color_discrete_sequence=palette,
                      title='Total de leitos de UTI e Enfermaria destinados à COVID-19')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
        fig2.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)

        # Número de pacientes em tratamento na UTI e enfermaria no Estado
        fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                      template='xgridoff', title='Total de pacientes nas UTIs e Enfermarias',
                      color_discrete_sequence=palette)
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
        fig3.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Pacientes em tratamento",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)

        # Novas internações por dia no Estado
        fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                       y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                       color_discrete_sequence=palette, title='Novas internações por dia no Estado')
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500),
        fig4.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4)


@app.route("/estado/isolamento-social/search", methods=['POST', 'GET'])
def isola_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

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
                      template='xgridoff', title='Índice de Isolamento Social do Estado',
                      color_discrete_sequence=palette)
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
        fig1.update_xaxes(tickangle=-45,
                          tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Isolamento Social (%)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_isola=graf1)


####################################################################################################################


# ROUTES INICIAIS DA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios", methods=['GET'])
@app.route("/municipios/covidsp", methods=['GET'])
def covidmuni_main():
    random.shuffle(palette)
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
    flash(Markup(f'<h1 class="cidades"> Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os '
                 f'maiores números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa '
                 f'personalizada.</h1>'))

    # Casos diários por município
    fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município', hover_data=['Novos Casos'],
                  color_discrete_sequence=palette,
                  title='Casos confirmados por dia e por Município', template='xgridoff')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=150),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Novos Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Óbitos diários por municípioo
    fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município', hover_data=['Novos Óbitos'],
                  color_discrete_sequence=palette,
                  title='Óbitos confirmados por dia e por Município', template='xgridoff')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=25),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Novos Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
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
                  color_discrete_sequence=palette)
    fig3.update_xaxes(type='date')
    fig3.update_layout(autosize=True)
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf3 = fig3.to_html(full_html=False)

    # Total de casos por município
    fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                  title='Comparativo entre o total de casos por Município', template='xgridoff',
                  color_discrete_sequence=palette)
    fig4.update_xaxes(type='date')
    fig4.update_layout(autosize=True)
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf4 = fig4.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3, graf4_covidmuni=graf4)


@app.route("/municipios/vacina", methods=['GET'])
def vacina_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, usecols=['Data'])
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    lastupdate = covidsp['Data'].max().strftime("%d/%m/%Y")
    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    flash(Markup(f'<h1 class="vacinometro">Totalização da campanha vacinal por Município '
                 f'<span>(última atualização: {lastupdate})</span></h1>'))

    # Filtro só para 'main' functions:
    vacina = vacina.query(
        "Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == "
        "'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | "
        "Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")
    flash(Markup(f'<h1 class="cidades">Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os '
                 f'maiores números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa '
                 f'personalizada.</h1>'))

    # Comparação entre municípios de aplicação das doses
    fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                        template='xgridoff', title='Aplicação das doses por Município',
                        color_discrete_sequence=palette)
    fig1.update_layout(legend_title_text='Dose Aplicada')
    fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=1000000),
    fig1.update_xaxes(tickangle=-45),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf1 = fig1.to_html(full_html=False)

    # Comparação entre municípios de doses distribuídas
    fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                        color_discrete_sequence=palette, title='Doses distribuídas por Município')
    fig2.update_xaxes(showgrid=False, tickmode="linear", tick0=0, dtick=2500000),
    fig2.update_yaxes(tickangle=-45),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='Doses Distribuídas', yaxis_title="",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf2 = fig2.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_vacina=graf1, graf2_vacina=graf2)


@app.route("/municipios/isolamento-social", methods=['GET'])
def isolamuni_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    # Filtragem padrão para o main:
    isola = isola.query(
        "Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == "
        "'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | "
        "Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")
    final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (isola['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
    filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
    isola = isola.loc[filterdate]
    flash_generate(isola)
    flash(Markup(f'<h1 class="cidades">Dados de São José dos Campos, Jacareí e Caçapava, além de 7 municípios com os '
                 f'maiores números da pandemia no Estado. Para acessar outras cidades, faça uma pesquisa '
                 f'personalizada.</h1>'))

    # Histórico do indice de isolamento nos municipios sp
    fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município',
                  color_discrete_sequence=palette, title='Índice de Isolamento Social por Município')
    fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=10),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       hovermode="x unified", xaxis_title='Data', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)
    return render_template('municipios.html', form=form, min=mini, max=maxi, graf1_isola=graf1)


###################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios/covidsp/search", methods=['POST', 'GET'])
def covidmuni_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

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
                          color_discrete_sequence=palette,
                          title='Casos confirmados por dia e por Município', template='xgridoff')
            fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=150),
            fig1.update_xaxes(tickangle=-45,
                              tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
            fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               xaxis_title='', yaxis_title="Novos Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                               xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
            graf1 = fig1.to_html(full_html=False)

            # Óbitos diários por município
            fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município',
                          hover_data=['Novos Casos', 'Total de Casos'],
                          color_discrete_sequence=palette,
                          title='Óbitos confirmados por dia e por Município', template='xgridoff')
            fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=25),
            fig2.update_xaxes(tickangle=-45,
                              tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
            fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               xaxis_title='', yaxis_title="Novos Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                               xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
            graf2 = fig2.to_html(full_html=False)

            # Filtros apenas para dados totais
            final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
            inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
            filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
            covidmuni = covidmuni.loc[filterdate]

            # Total de mortes por município
            fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município',
                          title='Comparativo do total de óbitos por Município', template='xgridoff',
                          color_discrete_sequence=palette)
            fig3.update_xaxes(type='date')
            fig3.update_layout(autosize=True)
            fig3.update_yaxes(showgrid=False),
            fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Total de Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
            graf3 = fig3.to_html(full_html=False)

            # Total de casos por município
            fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                          title='Comparativo do total de casos por Município', template='xgridoff',
                          color_discrete_sequence=palette)
            fig4.update_xaxes(type='date')
            fig4.update_layout(autosize=True)
            fig4.update_yaxes(showgrid=False),
            fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Total de Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
            graf4 = fig4.to_html(full_html=False)
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   start=form_start[-1], end=form_end[-1], city=form_city[-1],
                                   graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3,
                                   graf4_covidmuni=graf4)


@app.route("/municipios/vacina/search", methods=['POST', 'GET'])
def vacina_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, usecols=['Data'])
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    lastupdate = covidsp['Data'].max().strftime("%d/%m/%Y")
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    flash(Markup(f'<h1 class="vacinometro">Totalização da campanha vacinal por Município '
                 f'<span>(última atualização: {lastupdate})</span></h1>'))
    vacina = city_filter_all(vacina, city_request)

    if not isinstance(vacina, pd.DataFrame):
        return vacina
    else:
        # Comparação entre municípios de aplicação das doses
        fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                            template='xgridoff', title='Aplicação das doses por Município',
                            color_discrete_sequence=palette)
        fig1.update_layout(legend_title_text='Dose Aplicada')
        fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=1000000),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
        graf1 = fig1.to_html(full_html=False)

        # Comparação entre municípios de doses distribuídas
        fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                            color_discrete_sequence=palette, title='Doses distribuídas por Município')
        fig2.update_xaxes(showgrid=False, tickmode="linear", tick0=0, dtick=2500000),
        fig2.update_yaxes(tickangle=-45),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='Doses Distribuídas', yaxis_title="",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
        graf2 = fig2.to_html(full_html=False)
        return render_template('municipios.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1], city=form_city[-1],
                               graf1_vacina=graf1, graf2_vacina=graf2)


@app.route("/municipios/isolamento-social/search", methods=['POST', 'GET'])
def isolamuni_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

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
                          template='xgridoff', title='Índice de Isolamento Social por Município',
                          color_discrete_sequence=palette)
            fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=10),
            fig1.update_xaxes(tickangle=-45,
                              tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
            fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               hovermode="x unified", xaxis_title='Data', yaxis_title="Isolamento Social (%)",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                               xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
            graf1 = fig1.to_html(full_html=False)
            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   start=form_start[-1], end=form_end[-1], city=form_city[-1],
                                   graf1_isola=graf1)


if __name__ == "__main__":
    app.run(debug=True)
