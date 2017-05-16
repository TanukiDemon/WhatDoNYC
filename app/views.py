from flask import render_template, redirect, request, Blueprint, url_for, session, flash
import configparser
from .wdnyc import app
from .forms import *
from .models import *
from os import path
from py2neo import Graph, Node
from pandas import DataFrame, concat
from flask_login import LoginManager, login_user, login_required, logout_user

my_view = Blueprint('my_view', __name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    sqliteSession = get_session()
    user = sqliteSession.query(User).filter(User.username == username).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

# Used in the signup, login, and forgot routes
def checkIfUserExists(username):
    sqliteSession = get_session()
    return (sqliteSession.query(User).filter(User.username == username).first())

#Used in signup route
def checkIfEmailExists(email):
    sqliteSession = get_session()
    return (sqliteSession.query(User).filter(User.email == email).first())

def check_for_username_password(username, password):
    sqliteSession = get_session()
    user = sqliteSession.query(User).filter(User.username == username).first()
    return check_password_hash(user.password, password) and user

def check_password(username, password):
    sqliteSession = get_session()
    user = sqliteSession.query(User).filter(User.username == self.username).first()
    return check_password_hash(user.password, self.password)

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

        if (checkIfUserExists(form.username.data) or checkIfEmailExists(form.email.data)):
        # If so, return register.html again
            flash("Username or email already exists")
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            sqliteSession = get_session()
            newUser = User(username=str(form.username.data),
                password=str(form.password.data), email=str(form.email.data),
                name=str(form.name.data), securityQ=int(form.securityQ.data),
                answer=str(form.securityQanswer.data), status = 1)
            newUser.set_password(form.password.data)
            sqliteSession.add(newUser)
            sqliteSession.commit()

            # Store the user's new username to be used in the wyr route
            session["username"] = form.username.data
            login_user(newUser)
            return redirect('/wyr')

    return render_template('signup.html', title='Join us!', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        if check_for_username_password(user.username, form.password.data):
            login_user(user)
            session['username'] = user.username
            return redirect('recs')
        else:
            flash("Username or password is incorrect")
            return render_template('login.html', title='Incorrect login info',
                                    form=form)

    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgotPass():
    sqliteSession = get_session()
    form = forgotPassword(request.form)
    username = form.username.data
    user = sqliteSession.query(User).filter(User.username == username).first()
    if form.validate_on_submit() and checkIfUserExists(form.username.data):
        session['username'] = form.username.data

        return redirect('/secques')
    else:
        return render_template('forgot.html', title="Username does not exist", form=form)

@app.route('/secques', methods = ['GET','POST'])
def secques():
    sqliteSession = get_session()
    #gets all information for current user
    user = sqliteSession.query(User).filter(User.username == session['username']).first()
    form = securityQuestion(request.form)
    form.question.choices = [user.securityQ]
    answer = form.securityAnswer.data

    if checkIfUserExists(user.username):
        if answer == user.securityQAnswer:
            return redirect('/reset')

    return render_template('secques.html', title="Security Question response incorrect", form=form)

@app.route('/reset', methods = ['GET','POST'])
def reset():
    #code to reset password and insert it into the db
    sqliteSession = get_session()
    form = resetPassword(request.form)
    #checks if both passwords match
    if form.reset1.data and form.reset1.data == form.reset2.data:
        user = sqliteSession.query(User).filter(User.username == session['username']).first()
        user.set_password(form.reset2.data)
        sqliteSession.commit()
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
                        "trait2: {t2}, trait3: {t3}, trait4: {t4}, counter: 0, likedVisits: 0})",
                        uname=username, t1=form.foodOrScience.data,
                        t2=form.artOrHistory.data, t3=form.outdoorsOrSports.data,
                        t4=form.entertainmentOrMusic.data)
        return redirect('/recs')

    return render_template('wyr.html', title='wouldYouRatherForm', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title="About What Do NYC")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/about')

# Generates recommendations of the most popular activities
# based on the user's personality traits
def getRecommendationsForTraits(graph, n):
    # Get the required number of recommendations in DataFrame format
    recs = DataFrame(graph.data("MATCH (u:User {username: {curr}}), (a:Activity) "
                                "WHERE a.label = u.trait1 OR a.label = u.trait2 "
                                "OR a.label = u.trait3 OR a.label = u.trait4 "
                                "WITH a as selectActs, u as currU "
                                "MATCH (selectActs), (currU) "
                                "WHERE NOT (currU)-[:HAS_BEEN_TO]->(selectActs) "
                                "RETURN selectActs.placeID, selectActs.name "
                                "LIMIT {lim}", curr = session['username'], lim = n))

    # Feed the place IDs into a list and flip the order of
    # the elements before returning
    r = recs.values.tolist()
    r = [[i[1], i[0]] for i in r]

    # If less than three recommendations were returned, the list is filled
    # with lists containing two empty strings as the recs template expects
    # three recommendations
    lngth = len(r)
    if lngth < 3:
        r += [["", ""]] * (3-lngth)
    return r

@app.route('/recs', methods=['GET', 'POST'])
@login_required
def recs():
    # Get graph object to perform Neo4j queries
    graph = getPy2NeoSession()
    currUser = session['username']
    # Make a form that will be modified later on
    form = recsForm(request.form)

    # Count the number of currUser's activities
    numActivities = graph.run("MATCH (u:User {username: {curr}} )"
                                "SET u.counter = u.counter + 1 "
                                "RETURN u.likedVisits", curr = currUser).evaluate()

    if not numActivities:
        # If user has no connections, get most popular activities with a positive
        # weight that correspond to their personality traits
        form = recsForm(request.form)
        form.recommendations.choices = getRecommendationsForTraits(graph, 3)
        return render_template('recs.html', title="Your recommendations", form=form)

    # Get all users who rated the same activities as the current user
    similarUsers = DataFrame(graph.data("MATCH (u:User {username: {cUser}} )"
                                    "-[:HAS_BEEN_TO{rating:1}]->(a:Activity)"
                                    "<-[:HAS_BEEN_TO{rating:1}]-(other:User) "
                                    "RETURN DISTINCT other.username", cUser = currUser))

    if similarUsers.empty:
        # Get the most popular activities that correspond to user traits
        form.recommendations.choices = getRecommendationsForTraits(graph, 3)
        return render_template('recs.html', title="Your recommendations", form=form)

    # Create the dataframe that will contain possible activities to recommend
    allActivities = DataFrame()
    # Compute similarity of all similar users
    # Can pass in columns of dataframe into numpy vectorized function: beta.cdf(df.a, df.b, df.c)
    for row in similarUsers.itertuples():
        i, uname = row

        # Query for the activities that similar user liked but the current user
        # has never visited
        actsDf = DataFrame(graph.data("MATCH (sim:User {username: {suser}})-"
                                        "[:HAS_BEEN_TO{rating:1}]->(simAct:Activity)"
                                        "WITH simAct as allActs "
                                        "MATCH (allActs) "
                                        "WHERE NOT (:User {username:{curr}})-"
                                        "[:HAS_BEEN_TO]->(allActs) "
                                        "RETURN allActs.placeID as aPlace, "
                                        "allActs.name as aName",
                                        suser = uname, curr = currUser))

        # 0.2 is the similarity cutoff
        shareCount = numActivities - actsDf.shape[0]
        if (shareCount / numActivities >= 0.2):
            # Since the similar user makes the cut off,
            # its dataframe is merged with allActivities
            frames = [allActivities, actsDf]
            allActivities = concat(frames)

    # All similarUsers have had their data processed and data has been
    # merged into allActivities as needed. The duplicated rows are combined
    # and a new column is created that that contains the number of times
    # the a.name value appeared originally
    mergedDf = DataFrame(allActivities.groupby(['aPlace', 'aName']).size().rename('counts'))

    # Sort the rows based on values in counts column
    mostPopularDf = mergedDf.sort_values('counts', ascending=False).head(3)

    # Choices is a list of the four location ids with the highest count values
    form.recommendations.choices =  mostPopularDf.index.values.tolist()

    # If less than four recommendations were made, then generate ones based on
    # the user's traits
    lngth = len(form.recommendations.choices)
    if lngth < 3:
        form.recommendations.choices += getRecommendationsForTraits(graph, 3-lngth)

    # The most popular activities are passed along to recs.html
    return render_template('recs.html', title="Your recommendations", form=form)

@app.route('/singleRec', methods=['GET'])
def singleRec():
    return render_template('singleRec.html', title='Your Recommendation')

@app.route('/feedback')
def feedback():
    graph = getPy2NeoSession()
    rating = int(request.args.get('rating'))
    placeId = request.args.get('placeId')
    # Get a few values needed to run the query
    currUser = session["username"]

    # Add relationship in the database for user to placeId with weight rating
    # If the rating is one, then the user's likedVisits property must be incremented
    if rating == 1:
        graph.run("MATCH (u:User {username:{curr}}), (a:Activity {placeID:{pid}}) "
                    "SET u.likedVisits = u.likedVisits + 1 "
                    "CREATE (u)-[:HAS_BEEN_TO{rating:1, recSetCounter:u.counter}]->(a)",
                    curr = currUser, pid=placeId)

    # Otherwise, there is no reason to update the property
    else:
        graph.run("MATCH (u:User {username:{curr}}), (a:Activity {placeID:{pid}}) "
                    "CREATE (u)-[:HAS_BEEN_TO{rating:0, recSetCounter:u.counter}]->(a)",
                    curr = currUser, pid=placeId)
    return render_template('recs.html', title="Your recommendations")
