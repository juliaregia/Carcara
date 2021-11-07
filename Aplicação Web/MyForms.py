from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField


class Form(FlaskForm):
    municipio_field = StringField('Município')
    startdate_field = DateField('Data inicial', format='%Y-%m-%d')
    enddate_field = DateField('Data final', format='%Y-%m-%d')
    submit_field = SubmitField('Pesquisar')
