from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, RadioField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

class signupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])

    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35)])

    name = StringField('name', validators=[InputRequired(), Length(min=1, max=35)])

    securityQanswer = StringField('securityQanswer', validators=[InputRequired(), Length(min=1, max=35)])

    securityQ = SelectField(u'Security Question', choices=[('1', "What was the last name of your fourth grade teacher?"), ('2', "What were the last four digits of your childhood telephone number?"), ('3', "What was the name of the street you grew up on as a child?")])

class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])

class forgotPassword(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

class wouldYouRatherForm(FlaskForm):
    foodOrScience = RadioField('foodVSsci', choices = [('food', 'Food/Drink'), ('sci', 'Science')])

    artOrHistory = RadioField('artVShistory', choices = [('art', 'Arts'), ('history', 'History')])

    outdoorsOrSports = RadioField('outVSsports', choices=[('out', 'Outdoor'), ('sports', 'Sports')])

    entertainmentOrMusic = RadioField('entVSmusic', choices=[('ent', 'Entertainment'), ('music', 'Music')])
