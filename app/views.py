from flask import render_template, redirect, request, Blueprint, url_for, session
import configparser
from .wdnyc import app
from .forms import *
from .models import *
from os import path
from py2neo import Graph, Record
from collections import defaultdict, Counter

my_view = Blueprint('my_view', __name__)

# Used in the signup, login, and forgot routes
def checkIfUserExists(username):
    sqliteSession = get_session()
    return (sqliteSession.query(User).filter(User.username == username).first())

def checkIfEmailExists(email):
    sqliteSession = get_session()
    return (sqliteSession.query(User).filter(User.email == email).first())

def getPy2NeoSession():
    config = configparser.ConfigParser()
    fn = path.join(path.dirname(__file__), 'config.ini')
    config.read(fn)

    remote_graph = Graph(config.get('global', 'py2neoAddress'))
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

        if (checkIfUserExists(form.username.data) and checkIfEmailExists(form.email.data)):
        # If so, return register.html again
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            sqliteSession = get_session()
            newUser = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.name.data, securityQ=form.securityQ.data, answer=form.securityQanswer.data)
            newUser.set_password(form.password.data)
            sqliteSession.add(newUser)
            sqliteSession.commit()

            # Store the user's new username to be used in the wyr route
            session["username"] = form.username.data

            return redirect('/wyr')
    return render_template('signup.html', title='Join us!', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    sqliteSession = get_session()
    form = loginForm(request.form)
    password = form.password.data
    username = form.username.data
    user = sqliteSession.query(User).filter(User.username == username).first()
    if form.validate_on_submit() and checkIfUserExists(form.username.data):
        session['username'] = form.username.data

        if user.check_password(password):
            return redirect('/recs')
        else:
            return render_template('login.html', title="Incorrect Password", form=form)

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

@app.route('/about')
def about():
    return render_template('about.html', title="About What Do NYC")

@app.route('/recs', methods=['GET', 'POST'])
def recs():
    # Get graph object to perform Neo4j queries
    graph = getPy2NeoSession()
    currUser = session['username']

    # Count the number of currUser's activities
    numActivities = graph.run("MATCH (u:User {username: {curr}} )"
                            "-[r:HAS_BEEN_TO]->(a) RETURN count(r)", curr = currUser).evaluate()

    if not numActivities:
        # If user has no connections, get most popular activities with a positive
        # weight that correspond to their personality traits
        # Update this query to only return activities whose labels
        # match the user's traits

        mostPopular = graph.data("MATCH (s)-[h:HAS_BEEN_TO]->(a:Activity),"
                                "(u:User {username:{curr}})"
                                "WHERE a.label = u.trait1 OR a.label = u.trait2 "
                                "OR a.label = u.trait3 OR a.label = u.trait4 "
                                "WITH a, COUNT(h) as c "
                                "ORDER BY c DESC LIMIT 4 "
                                "RETURN a.placeID", curr = currUser)

        recommendations = []
        for m in mostPopular:
            for key, value in a.items():
                recommendations.append(value)

        form = recsForm(request.form)
        form.recommendations.choices = recommendations

        # Pick most popular activitity and pass it along to recs.html
        return render_template('recs.html', title="Your recommendations", form=form)

    # Get all users who rated the same activities as the current user
    similarUsers = graph.run("MATCH (u:User {username: {cUser}} )"
                            "-[:HAS_BEEN_TO{rating:1}]->(a:Activity)"
                            "<-[:HAS_BEEN_TO{rating:1}]-(other:User)"
                            "RETURN DISTINCT other.username", cUser = currUser).data()

    # List of users who meet the similarity cutoff
    possibleUserRecs = []
    # Compute similarity of all similar users
    for sim in similarUsers:
        for key, value in sim.items():
            # Get number of activities both the current user and user in
            # similarUsers list have rated

            numSharedActivities = graph.run("MATCH (u:User {username: {curr}} )"
                                            "-[:HAS_BEEN_TO{rating:1}]->(a)"
                                            "<-[:HAS_BEEN_TO{rating:1}]-"
                                            "(sim:User {username:{sUser}})"
                                            "USING INDEX u:User(username)"
                                            "USING INDEX sim:User(username)"
                                            "RETURN count(a)", sUser = value, curr = currUser).evaluate()

            # 0.2 is the similarity cutoff
            # If the following quotient is greater or equal than 0.2,
            # then the similar user's name is added to possibleUserRecs
            if (numSharedActivities / numActivities >= 0.2):
                possibleUserRecs.append(value)

    # Get activities rated by at the users in possibleUserRecs
    # but not by the current user
    popularActivities = Counter()
    for simUser in possibleUserRecs:
        uniqueActivities = graph.data("MATCH (simUser:User {username:{sUser}})"
                                        "-[:HAS_BEEN_TO{rating:1}]->(a)"
                                        "MATCH (u:User {username:{curr}})"
                                        "WHERE NOT (u)-[:HAS_BEEN_TO]->(a)"
                                        "RETURN a.placeID", sUser = simUser, curr = currUser)

        for a in uniqueActivities:
            for key, value in a.items():
                popularActivities[value] += 1

    # Choices is a list of the four tuples from count with the highest values
    form = recsForm(request.form)
    form.recommendations.choices = [i for i, c in popularActivities.most_common(4)]

    # The most popular activities are passed along to recs.html
    return render_template('recs.html', title="Your recommendations", form=form)
