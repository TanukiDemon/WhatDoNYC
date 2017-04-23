from flask import render_template, redirect, request, Blueprint, url_for, session
import configparser
from .wdnyc import app
from .forms import *
from .models import *
from os import path
from py2neo import Graph

my_view = Blueprint('my_view', __name__)

# Used in the signup, login, and forgot routes
def checkIfUserExists(username):
    sqliteSession = get_session()
    return (sqliteSession.query(User).filter(User.username == username).first())

def getPy2NeoSession():
    remote_graph = Graph("http://52.33.222.241:7474/db/data/")
    return remote_graph

@app.route('/')
def home():
    return redirect('/index')


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')


@app.route('/MHP', methods=['GET'])
def mhp():
    return render_template('MHP.html', title='Mister Hotpot')

@app.route('/HG', methods=['GET'])
def hg():
    return render_template('HG.html', title='Hamilton Grange')

@app.route('/CI', methods=['GET'])
def ci():
    return render_template('CI.html', title='Coney Island')

@app.route('/BH', methods=['GET'])
def bh():
    return render_template('BH.html', title='Bohemian Hall and Beer Garden')

@app.route('/LI', methods=['GET'])
def li():
    return render_template('LI.html', title='Little Italy')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm(request.form)
    form.securityQ.choices = [(1, "What was the last name of your fourth grade teacher"), (2, "What were the last four digits of your childhood telephone number?"), (3, "What was the name of the street you grew up on?")]

    if request.method == 'POST' and form.submit.data and form.validate_on_submit():
        print("WORKED")

        if (checkIfUserExists(form.username.data)):
        # If so, return register.html again
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            sqliteSession = get_session()
            newUser = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.name.data, securityQ=form.securityQ.data, answer=form.securityQanswer.data)

            sqliteSession.add(newUser)
            sqliteSession.commit()

            # Store the user's new username to be used in the wyr route
            session["username"] = form.username.data

            return redirect('/wyr')
    return render_template('signup.html', title='Join us!', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and checkIfUserExists(form.username.data):
        session['username'] = form.username.data
        return redirect('/recs')

    return render_template('login.html', title="Login", form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgotPass():
    form = forgotPassword(request.form)
    if checkIfUserExists(form.username.data):
        session['username'] = form.username.data
        return redirect('/secques')
    else:
        return render_template('forgot.html', title="Username does not exist", form=form)

@app.route('/secques', methods = ['GET','POST'])
def secques():
    #add code print question to screen
    form = securityQuestion(request.form)
    if session.query(User).filter(User.securityQanswer) == form.securityAnswer.data:
        #pass session to reset page
        return redirect('/reset')
    else:
        return render_template('/secques', title="Security Question response incorrect", form=form)

@app.route('/reset', methods = ['GET','POST'])
def reset():
    #code to reset password and insert it into the db
    form = resetPassword(request.form)
    if form.reset1.data == form.reset2.data:
        password = form.reset2.data
        session.commit()
        return redirect('/login')
    else:
        return render_template('reset.html', title = "Password do not match", form = form)

@app.route('/wyr', methods=['GET', 'POST'])
def wyr():
    # Serve "Would You Rather" survey
    form = wouldYouRatherForm(request.form)
    username = session['username'] # Get current user's username
    if form.validate_on_submit():
        # Add user and their preferences to Neo4j database
        graph_session = getPy2NeoSession()
        graph_session.run("CREATE (a:User {username: {uname}, trait1: {t1}, "
                        "trait2: {t2}, trait3: {t3}, trait4: {t4}})",
                        uname=username, t1=form.foodOrScience.data,
                        t2=form.artOrHistory.data, t3=form.outdoorsOrSports.data,
                        t4=form.entertainmentOrMusic.data)
        return redirect('/recs')

    return render_template('wyr.html', title='wouldYouRatherForm', form=form)

@app.route('/questions')
def about():
    return render_template('about.html', title="Daily Questions")

@app.route('/recs', methods=['GET', 'POST'])
def recs():
    # Get graph and cypher objects to perform Neo4j queries
    graph = getPy2NeoSession()
    cypher = graph.cypher
    currUsername = session['username']

    # Query for the current user
    user = cypher.execute("MATCH (user:User {username:{uname}}"
                       "RETURN user",
                       uname = currUsername)

    # Query for all of the current user's activities
    activities = cypher.execute("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity)"
                             "RETURN user, actvy",
                             uname = currUsername)

    # Get all users who rated the same activities as the current user
    similarUsers = cypher.execute("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(:Activity)<-[:HAS_BEEN_TO]-(otherUser:User)"
                "RETURN otherUser.username",
                uname = currUsername)

    # List of users who meet the cutoff
    possibleUserRecs = []

    # Compute similarity of all similar users
    for simUser in similarUsers:
      # Get number of activities both the current user and user in similarUsers list have rated
      sharedActivities = cypher.execute("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity)<-[:HAS_BEEN_TO]-(simiUser:User {name:{sUser}})"
                "RETURN actvy",
                uname = currUsername, sUser = simUser["username"])

      # 0.2 is the similarity cutoff
      if (sharedActivities.length / activities.length >= 0.2):
        possibleUserRecs.append(simUser)

    activities = {}
    # Get activities rated by at least two (or how many?) users in possibleRecs but not by the current user
    for simUser in possibleUserRecs:
        uniqueActivities = cypher.execute("MATCH (simUser:User {name:{sUser}})-[:HAS_BEEN_TO])->(actvy:Activity)<- NOT ([:HAS_BEEN_TO]-(currUser:User {name:{uname}}))")
        "RETURN actvy",
        uname = currUsername, sUser = simUser 
        
        for actvy in uniqueActivities:
            if not actvy in activities:
                activities[actvy] = 1
            else:
                activities[actvy] += 1
    
    # Returns list of sorted (key, value) tuples in descending order according to the the second tuple element
    sortedActivities = sorted(activities.items(), key=lambda x: x[1], reverse=True)
    
    # Pick most popular activitity and pass it along to recs.html
    return render_template('recs.html', sortedActivities[0])
