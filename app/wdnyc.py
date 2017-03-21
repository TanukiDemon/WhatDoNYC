import configparser
import os
from neo4j.v1 import GraphDatabase
from flask import Flask, render_template, redirect, flash, request
import requests
from os.path import expanduser
import models

app = Flask(__name__)

session = models.get_session()

def startNeo4JSession():
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


@app.route('/register', methods=['POST'])
def register():
    form = registerForm(request.form)
    if form.validate_on_submit():
        # Check if user is already in database
        if (session.query(models.User).filter(models.User.username==form.username).first() != None):
            # User already exists. Return register.html with errors
            return render_template('register.html')
        else if (session.query(models.User).filter(models.User.email==form.email)):
            return render_template('register.html')


        # Then render survey.html
        return render_template('survey.html', title='What You Rather')
    return render_template('register.html', title='Recommendations', form=form)

    session = startSession()
    session.run("CREATE (a:Person {username: {uname}, password: {pword}, surveyAnswers: {answers}})",
            {"uname": form.username, "pword": form.password, "answers": form.answers})

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('recommendations.html', title='Recomendations', form=form)
'''

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
