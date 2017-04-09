from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, request, Blueprint, url_for
from .wdnyc import app
from .forms import *
from .models import *

my_view = Blueprint('my_view', __name__)

# Used in the signup, login, and forgot routes
def checkIfUserExists(form):
    session = get_session()
    return (session.query(User).filter(User.username == form.username.data).first())


@app.route('/')
def home():
    return redirect('/index')


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Welcome')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session = get_session()
    form = signupForm(request.form)
    form.securityQ.choices = [(1, "What was the last name of your fourth grade teacher"), (2, "What were the last four digits of your childhood telephone number?"), (3, "What was the name of the street you grew up on?")]
    
    print(form.errors)

    if request.method == 'POST' and form.submit.data and form.validate_on_submit():
        print("WORKED")

        if (checkIfUserExists(form)):
        # If so, return register.html again
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            print("question: ", form.securityQ.data)

            newUser = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.name.data, securityQ=form.securityQ.data, answer=form.securityQanswer.data)

            session.add(newUser)
            session.commit()

            return render_template('wyr.html', title='Would You Rather', form=wouldYouRatherForm(request.form))
    return render_template('signup.html', title='Join us!', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and checkIfUserExists(form):
        #session['username'] = form.username.data
        return redirect('/recs')

    return render_template('login.html', title="Login", form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgotPassword():
    session = get_session()
    form = forgotPassword(request.form)
    if checkIfUserExists(session,form):
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
    
@app.route('/wyr', methods=['POST'])
def wyr():
    # Serve "Would You Rather" survey
    form = wouldYouRatherForm(request.form)
    if 'username' in session:
        username = session['username'] # Get current user's username
    else:
        return render_template('login.html') # User not logged in
    if form.validate_on_submit():
        
        # Add user and their preferences to Neo4j database
        session = startSession()
        session.run("CREATE (a:User {username: {uname}, trait1: {t1}, "
                    "trait2: {t2}, trait3 {t3}, trait4 {t4}})",
                    {"uname": username, "t1": form.foodOrScience,
                     "t2": form.artOrHistory, "t3": form.outdoorsOrSports,
                     "t4": form.entertainmentOrMusic})
        return redirect('/wyr')
    return render_template('wyr.html')


@app.route('/questions')
def about():
    return render_template('about.html', title="Daily Questions")

@app.route('/recs')
def recs():
    '''
    # Query for the current user
    user = session.run("MATCH (user:User {name:{uname}}"
                       "RETURN user",
                       {"uname": username})

    # Query for all of the current user's activities
    activities = session.run("MATCH (user:User {name:{uname}})-[:RATED]->(actvy:Activity)"
                             "RETURN user, actvy",
                             {"uname": username})

    # Get all users who rated the same activities as the current user
    similarUsers = session.run("MATCH (user:User {name:{uname}})-[:RATED]->(:Activity)<-[:RATED]-(otherUser:User)"
                "RETURN otherUser.username",
                {"uname": username})

    # Get users who have been to the same activities as the users that the current user has been two (second degree of separation)
    2ndDegUsers = session.run("MATCH (user:User)-[:RATED]->(actvy1)<-[:RATED]-(similarUser:User),
         (similarUser)-[:RATED]->(actvy2)<-[:RATED]-(similarUser2:User)"
                "WHERE user.name = {uname}"
                "AND   NOT    (user)-[:RATED]->(actvy2)"
                "RETURN similarUser2.username",
                {"uname": username})
    '''
    return render_template('recs.html')
