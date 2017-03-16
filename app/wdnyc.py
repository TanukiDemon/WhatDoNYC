from flask_stormpath import StormpathManager
import configparser
import os
from neo4j.v1 import GraphDatabase
from flask import Flask, render_template, redirect, flash, request
import requests

app = Flask(__name__)

configPar = configparser.ConfigParser()
confIni = os.path.join(os.path.dirname(__file__), 'config.ini')
configPar.read(confIni)
app.config['SECRET_KEY'] = configPar['global']['sp_secret_key']
app.config['STORMPATH_API_KEY_FILE'] = os.path.join(os.path.dirname(__file__), 'apiKey.properties')
app.config['STORMPATH_APPLICATION'] = 'WhatDoNYC'

stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'


def startSession():
    config = confiparser.ConfigParser()
    fn = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read('config.ini')
    neo_pw = config['global']['neo4j_password']

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", neo_pw))
    return driver.session()

@app.route('/')
def home():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')

'''
@app.route('/register', methods=['POST'])
def register():
    form = registerForm(request.form)
    # Let Storm Path handle things here

    # Serve "Would You Rather" survey
    form = WouldYouRatherForm(request.form)
    if form.validate_on_submit():
        return recommendationResults(form)
    return render_template('recommendations.html', title='Recommendations', form=form)

    session = startSession()
    session.run("CREATE (a:Person {username: {uname}, password: {pword}, surveyAnswers: {answers}})",
            {"uname": form.username, "pword": form.password, "answers": form.answers})


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('recommendations.html', title='Recomendations', form=form)
'''

@app.route('/recommendations', methods=['GET'])
def recommendations():
    return render_template('recs.html', title='Recommendations')
'''
    form = SurveyForm(requests.form)
    if not form.validate_on_submit():
        return render_template('recs.html', title='Recommendations', username=uname)

    session = startSession()
    user = session.run('MATCH (n:Person) WHERE n.username={uname}', {"uname": username})
    session.run('match {user}-[r]-()', {"user": user})
'''
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
