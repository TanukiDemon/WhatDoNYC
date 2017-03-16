from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, flash, request
from app import app
import requests
import configparser
import os

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
