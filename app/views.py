from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, flash, request
from app import app
#from .forms import SearchForm
from datetime import datetime
import requests
import ConfigParser

def startSession():
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    neo4j-password = config.get('Global', 'neo4j_password')

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", neo4j-password))
    return driver.session()

@app.route('/')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')
    #return "Hello, World!"

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

@app.route('/recommendations', methods=['GET'])
def recommendations(username):
    form = SurveyForm(requests.form)
    if not form.validate_on_submit():
        return render_template('recommendations.html', title='Recommendations', form=form)

    session = startSession()
    user = session.run('MATCH (n:Person) WHERE n.username={uname}', {"uname": username})
    session.run('match {user}-[r]-()', {"user": user})
