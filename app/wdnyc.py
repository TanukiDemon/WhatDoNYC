import configparser
import os
from neo4j.v1 import GraphDatabase
from flask import Flask, render_template, redirect, flash, request
import requests
from os.path import expanduser
import sqlite3 as lite
import sys

app = Flask(__name__)

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


@app.route('/register', methods=['POST'])
def register():
    form = registerForm(request.form)
    if form.validate_on_submit():
        # Check if user is already in database
        session = models.get_session()
        if (checkIfUserExists(session)):
            # If so, return register.html again
            return render_template('register.html')

        # Otheriswe, insert the user in mysql database and render survey.html
        else:
            newUser = models.User(username=form.username, password=form.password, email=form.email, firstName=form.name)
            session.add(newUser)
            session.commit()
            return render_template('survey.html', title='What You Rather')
    else:
        return render_template('register.html', title='Recommendations', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and loginUser(form.username, form.password):
        return render_template('recommendations.html', title='Recomendations', form=form)
    else:
        return render_template('login.html', title="Login")


@app.route('/recommendations', methods=['GET'])
def recommendations():
    return render_template('recs.html', title='Recommendations')


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
