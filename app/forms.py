from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, RadioField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class signupForm(FlaskForm):
    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])

    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35)])

    name = StringField('name', validators=[InputRequired(), Length(min=1, max=35)])

    securityQanswer = StringField('securityQanswer', validators=[InputRequired(), Length(min=1, max=35)])

    securityQ = SelectField(u'Security Question', choices = [], coerce = int)

    submit = SubmitField(u'Sign up')

class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=15)])
    
    submit = SubmitField(u'Log In')

class forgotPassword(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])

class wouldYouRatherForm(FlaskForm):
    foodOrScience = RadioField('foodVSsci', choices = [('food', 'Food/Drink'), ('sci', 'Science')])

    artOrHistory = RadioField('artVShistory', choices = [('art', 'Arts'), ('history', 'History')])

    outdoorsOrSports = RadioField('outVSsports', choices=[('out', 'Outdoor'), ('sports', 'Sports')])

    entertainmentOrMusic = RadioField('entVSmusic', choices=[('ent', 'Entertainment'), ('music', 'Music')])
