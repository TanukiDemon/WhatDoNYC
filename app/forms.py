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

    submit = SubmitField(u'Submit')

class securityQuestion(FlaskForm):
    securityAnswer = StringField('answer', validators=[InputRequired(), Length(min=1, max=35)])

    submit = SubmitField(u'Submit')

class resetPassword(FlaskForm):
    reset1 = PasswordField('reset1', validators=[InputRequired(), Length(min=1, max=15)])

    reset2 = PasswordField('reset2', validators=[InputRequired(), Length(min=1, max=15)])

    submit = SubmitField(u'Submit')

class wouldYouRatherForm(FlaskForm):
    foodOrScience = RadioField('foodVSsci', choices = [('Food/Drink', 'sample delicious foods?'), ('Science', 'perform cool science experiments?')])

    artOrHistory = RadioField('artVShistory', choices = [('Arts', 'talk to famous artists?'), ('History', 'go back in time?')])

    outdoorsOrSports = RadioField('outVSsports', choices=[('Outdoor', 'spend time in a garden?'), ('Sports', 'hike a breathtaking trail?')])

    entertainmentOrMusic = RadioField('entVSmusic', choices=[('Entertainment', 'go to a comedy club?'), ('Music', 'listen to live music?')])

    submit = SubmitField(u'Submit')

class recsForm(FlaskForm):
    recommendations = SelectField(u'Recommendations', choices = [], coerce = int)
