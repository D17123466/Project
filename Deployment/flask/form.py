from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired
import requests
from utils import getSelectFieldForm

class ConverterForm(FlaskForm):
    '''
    WTF Form
    '''
    CHOICES = getSelectFieldForm()
    amount = FloatField('Amount', validators=[DataRequired()])
    from_ = SelectField('From',  choices=CHOICES)
    to_ = SelectField('To',  choices=CHOICES)
    submit = SubmitField('Submit')

