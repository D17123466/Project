from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired
import requests

class ConverterForm(FlaskForm):
    # url = 'https://api.exchangerate-api.com/v4/latest/EUR'
    url = 'https://api.exchangeratesapi.io/latest'
    response = requests.get(url)
    json = response.json()
    rates = json['rates']
    units = [(key, key) for key in rates if key in ['USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW']]
    units.append(('EUR', 'EUR'))
    units = units[::-1]
    
    amount = FloatField('Amount', validators=[DataRequired()])
    from_ = SelectField('From',  choices=units)
    to_ = SelectField('To',  choices=units)
    submit = SubmitField('Submit')

