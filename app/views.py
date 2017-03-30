from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, flash, request, Blueprint
from .wdnyc import app
from .forms import signupForm, loginForm, wouldYouRatherForm
from .models import *

my_view = Blueprint('my_view', __name__)

# Used in the signup and login routes
def checkIfUserExists(form):
    session = get_session()
    return (session.query(User).filter(and_(User.username == form.username.data, User.password == form.password.data)))


@app.route('/')
def home():
    # Route to the index page
    return render_template('about.html', title='Welcome')


@app.route('/index', methods=['GET'])
def index():
    return render_template('about.html', title='Welcome')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session = get_session()
    form = signupForm(request.form)

    if form.validate():
        print("valid")

    print(form.errors)

    if form.validate_on_submit():
        if (checkIfUserExists(form)):
            # If so, return register.html again
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            newUser = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.name.data)
            session.add(newUser)
            session.commit()
      
            return render_template('wyr.html', title='Would You Rather', form=form)
    return render_template('signup.html', title='Join us!', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and checkIfUserExists(form):
        session['username'] = form.username.data
        return redirect('/WouldYouRather')
    
    return render_template('login.html', title="Login", form=form)


@app.route('/wyr', methods=['POST'])
def wyr():
    # Serve "Would You Rather" survey
    form = wouldYouRatherForm(request.form)
    if 'username' in session:
        username = session['username'] # Get current user's username
    else:
        return render_template('login.html') # User not logged in
    if form.validate_on_submit():
        # Add user and their preferences to Neo4j database
        session = startSession()
        session.run("CREATE (a:User {username: {uname}, trait1: {t1}, "
                    "trait2: {t2}, trait3 {t3}, trait4 {t4}})",
                    {"uname": username, "t1": form.foodOrScience,
                     "t2": form.artOrHistory, "t3": form.outdoorsOrSports,
                     "t4": form.entertainmentOrMusic})
        return redirect('/wyr')
    return render_template('wyr.html')


@app.route('/questions')
def questions():
    return render_template('questions.html', title="Daily Questions")


@app.route('/spotlight')
def spotlight():
    return render_template('spotlight.html', title="Spotlight")
