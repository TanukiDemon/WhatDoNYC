from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError

class signupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])
    
    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35)])

    name = StringField('Email Address', validators=[Length(min=1, max=35)])

class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])

class wouldYouRatherForm(FlaskForm):
    foodOrScience = RadioField('foodVSsci', choices = [('food', 'Food/Drink'), ('sci', 'Science')])
    
    artOrHistory = RadioField('artVShistory', choices = [('art', 'Arts'), ('history', 'History')])
    
    outdoorsOrSports = RadioField('outVSsports', choices=[('out', 'Outdoor'), ('sports', 'Sports')])
    
    entertainmentOrMusic = RadioField('entVSmusic', choices=[('ent', 'Entertainment'), ('music', 'Music')])
