from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField


class Form(FlaskForm):
    municipio_field = StringField('Município')
    startdate_field = DateField('Data inicial', format='%d/%m/%Y', render_kw={'placeholder': 'dd/mm/aaaa'})
    enddate_field = DateField('Data final', format='%d/%m/%Y', render_kw={'placeholder': 'dd/mm/aaaa'})
    submit_field = SubmitField('Pesquisar')
