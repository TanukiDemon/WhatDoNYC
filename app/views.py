from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, flash, request
from app import app
import requests
import configparser
import os

def findNewEvents(uname, thold):
    username = uname
    threshold = thold

    query = ('MATCH (a1:`Activity`)<-[:`Has_rated`]-(u1:`User` {username:{username}}) '
    'WITH count(a1) as counta '
    'MATCH (u2:`User`)-[r2:`Has_rated`]->(a1:`Activity`)<-[r1:`Has_rated`]-(u1:`User` {user_id:{user_id}}) '
    'WHERE (NOT u2=u1) AND (abs(r2.rating - r1.rating) <= 1) '
    'WITH u1, u2, tofloat(count(DISTINCT a1))/counta as sim '
    'WHERE sim>{threshold} '

    'MATCH (a:`Activity`)<-[r:`Has_rated`]-(u2) '
    'WHERE (NOT (a)<-[:`Has_rated`]-(u1)) '
    'RETURN DISTINCT a,tofloat(sum(r.rating)) as score ORDER BY score DESC ')

    tx = graph.cypher.begin()
    tx.append(query, {'username': username, 'threshold': threshold})
    result = tx.commit()


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
