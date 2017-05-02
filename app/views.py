from flask import render_template, redirect, request, Blueprint, url_for, session
import configparser
from .wdnyc import app
from .wdnyc import cache
from .forms import *
from .models import *
from os import path
from py2neo import Graph, Node
from pandas import DataFrame, concat

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

@cache.cached(timeout=50)
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')

@cache.cached(timeout=50)
@app.route('/MHP', methods=['GET'])
def mhp():
    return render_template('MHP.html', title='Mister Hotpot')

@cache.cached(timeout=50)
@app.route('/HG', methods=['GET'])
def hg():
    return render_template('HG.html', title='Hamilton Grange')

@cache.cached(timeout=50)
@app.route('/CI', methods=['GET'])
def ci():
    return render_template('CI.html', title='Coney Island')

@cache.cached(timeout=50)
@app.route('/BH', methods=['GET'])
def bh():
    return render_template('BH.html', title='Bohemian Hall and Beer Garden')

@cache.cached(timeout=50)
@app.route('/LI', methods=['GET'])
def li():
    return render_template('LI.html', title='Little Italy')

@cache.cached(timeout=50)
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

# Generates recommendations of the most popular activities
# based on the user's personality traits
def generatePopularRecommendations(n, username):
    # Get the required number of recommendations in DataFrame format
    recs = DataFrame(graph.data("MATCH (s)-[h:HAS_BEEN_TO]->(a:Activity),"
                                "(u:User {username:{curr}})"
                                "WHERE a.label = u.trait1 OR a.label = u.trait2 "
                                "OR a.label = u.trait3 OR a.label = u.trait4 "
                                "WITH a, COUNT(h) as c "
                                "ORDER BY c DESC LIMIT {lim} "
                                "RETURN a.placeID", curr = currUser, lim = n))

    # Feed the place IDs into a list
    return recs.values.tolist()

@app.route('/recs', methods=['GET', 'POST'])
def recs():
    # Get graph object to perform Neo4j queries
    graph = getPy2NeoSession()
    currUser = session['username']
    form = recsForm(request.form)

    # Count the number of currUser's activities
    numActivities = graph.run("MATCH (u:User {username: {curr}} )"
                                "SET u.counter = u.counter + 1"
                                "RETURN u.likedVisits", curr = currUser).evaluate()
    if not numActivities:
        # If user has no connections, get most popular activities with a positive
        # weight that correspond to their personality traits
        form = recsForm(request.form)
        form.recommendations.choices = generateRandomRecommendations(4, currUser)

        # Pick most popular activitity and pass it along to recs.html
        return render_template('recs.html', title="Your recommendations", form=form)

    # Get all users who rated the same activities as the current user
    similarUsers = DataFrame(graph.data("MATCH (u:User {username: {cUser}} )"
                            "-[:HAS_BEEN_TO{rating:1}]->(a:Activity)"
                            "<-[:HAS_BEEN_TO{rating:1}]-(other:User) "
                            "RETURN DISTINCT other.username", cUser = currUser))

    if similarUsers.empty:
        return render_template('recs.html', title="Your recommendations", form=form)

    allActivities = DataFrame()
    # Compute similarity of all similar users
    # Can pass in columns of dataframe into numpy vectorized function: beta.cdf(df.a, df.b, df.c)
    for row in similarUsers.itertuples():
        i, uname = row

        # Get number of activities both the current user and user in
        # similarUsers list have rated
        uniqueActivitiesDf = DataFrame(graph.data("MATCH (sim:User {username: {suser}})-[:HAS_BEEN_TO{rating:1}]->(simAct:Activity)"
                                    "WITH simAct as allActs "
                                    "MATCH (allActs) "
                                    "WHERE NOT (:User {username:{curr}})-[:HAS_BEEN_TO]->(allActs) "
                                    "RETURN allActs.placeID as aPlace", suser = uname, curr = currUser))

        # 0.2 is the similarity cutoff
        # If the following quotient is greater or equal than 0.2,
        # then the similar user's name is added to possibleUserRecs
        shareCount = numActivities - uniqueActivitiesDf.shape[0]
        if (shareCount / numActivities >= 0.2):
            # Since the similar user makes the cut off,
            # its dataframe is merged with allActivities
            frames = [allActivities, uniqueActivitiesDf]
            allActivities = concat(frames)

    # All similarUsers have had their data processed and data has been
    # merged into allActivities as need
    # The duplicated rows are combined and a new column is created that
    # that contains the number of times the a.name value appeared originally
    mergedDf = DataFrame(allActivities.groupby('aPlace').size().rename('counts'))

    # Sort the rows based on values in counts column
    mostPopularDf = mergedDf.sort_values('counts', ascending=False).head(4)

    # Choices is a list of the four location ids with the highest count values
    form.recommendations.choices =  mostPopularDf.index.values.tolist()

    # If less than four recommendations were made, then generate ones based on
    # the users' traits
    lngth = len(choices)
    if l < 4:
        form.recommendations.choices += generateRandomRecommendations(4-lngth, currUser)

    # The most popular activities are passed along to recs.html
    return render_template('recs.html', title="Your recommendations", form=form)

@app.route('/recs/<rating>/<placeId>', methods=['GET'])
def addRelation():
    # Get a few values needed to run the query
    currUser = session["username"]
    rule = request.url_rule
    base, rating, placeId = rule.rule.split('/')

    # Add relationship in the database for user to placeId with weight rating
    graph.run("MATCH (u:User {username:{curr}}), (a:Activity {placeID:{pid}})"
                "WHERE count = u.counter"
                "CREATE u-[:HAS_BEEN_TO{rating:{r}}{recSetCounter:count}]->(a)",
                curr = currUser, pid=placeId, r = rating)
