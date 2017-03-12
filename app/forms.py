from flask_wtf import Form
from wtforms import StringField, SelectMultipleField
from wtforms.validators import InputRequired, Length, ValidationError
import datetime

def isValidInteger(form, field):
    try:
        int(field.data)
    except ValueError:
        raise ValidationError('Field must be of valid zipcode format')

def validateDateFormat(form, field):
    try:
        datetime.datetime.strptime(field.data, '%Y-%m-%d')

    except ValueError:
        raise ValidationError('Date must be in yyyy-mm-dd format')


class registerForm(Form):
    username = StringField('username', validator=[InputRequired(), Length(min=1, max=15)])

    password = StringField('password', validator=[InputRequired(), :ength(min=1, max15)])


class SurveyForm(Form):
    # Multiple choice form
    
