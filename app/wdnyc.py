import configparser
import os
from neo4j.v1 import GraphDatabase
from flask import Flask, render_template, redirect, flash, request, session
import requests
from os.path import expanduser
import sqlite3 as lite
import sys
from .forms import signupForm, loginForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'myverylongsecretkey'
#csrf = CSRFProtect(app)

def startNeo4JSession():
    config = confiparser.ConfigParser()
    fn = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read('config.ini')
    neo_pw = config['global']['neo4j_password']

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", neo_pw))
    return driver.session()

def checkIfUserExists(session, username, email):
    return (session.query(models.User).filter(models.User.username==form.username).first()) and (session.query(models.User).filter(models.User.email==form.email).first()) 

def loginUser(username, password):
    models.get_session()
    return (session.query(models.User).filter(models.User.username == username).first() != None) and (session.query(models.User).filter(models.User.username == password).first() != None)  


@app.route('/')
def home():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm(request.form)
    if form.validate_on_submit():
        # Check if user is already in database
        session = models.get_session()
        if (checkIfUserExists(session)):
            # If so, return register.html again
            return render_template('signup.html', form=form)

        # Otheriswe, insert the user in mysql database and render survey.html
        else:
            newUser = models.User(username=form.username, password=form.password, email=form.email, firstName=form.name)
            session.add(newUser)
            session.commit()
      
            session['username'] = form.username
            return redirect('/WouldYouRather')
    return render_template('signup.html', title='Recommendations', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and loginUser(form.username, form.password):
        session['username'] = form.username.data
        return redirect('/WouldYouRather')
    
    return render_template('login.html', title="Login", form=form)


@app.route('/wyr', methods=['POST'])
def addUserToGraph():
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


@app.route('/survey')
def survey():
    return render_template('survey.html', title="Survey")


if __name__ == "__main__":
  app.run(host='0.0.0.0')
