from neo4j.v1 import GraphDatabase
from flask import render_template, redirect, request, Blueprint
from .wdnyc import app
from .forms import *
from .models import *

my_view = Blueprint('my_view', __name__)

# Start a new neo4j session to execute Cypher queries
def startNeo4JSession(config):
    neo_pw = config['global']['neo4j_password']
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", neo_pw))
    return driver.session()

# Used in the signup and login routes
def checkIfUserExists(session, form):
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

    if form.validate():
        print("valid")

    print(checkIfUserExists(session, form))

    print(form.errors)

    if form.validate_on_submit():
        print("WORKED")
        print(checkIfUserExists(session,form))
        #if (checkIfUserExists(session, form)):
        if (1 == 2):
            # If so, return register.html again
            return render_template('signup.html', title="User already exists", form=form)

        # Otheriswe, insert the user in the sqlite database and render wyd.html
        else:
            newUser = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.name.data, securityQ=form.securityQ.data, securityQanswer=form.securityQanswer.data)
            session.add(newUser)
            session.commit()
      
            return render_template('wyr.html', title='Would You Rather', form=form)
    return render_template('signup.html', title='Join us!', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit() and checkIfUserExists(form):
        session['username'] = form.username.data
        return redirect('/wyr')
    
    return render_template('login.html', title="Login", form=form)

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

@app.route('/forgot', methods=['GET', 'POST'])
def forgotPassword():
    if checkIfUserExists(get_session(), form):
        return redirect('/secques')
    else:
        return render_template('forgot.html', title="Username does not exist", form=form)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
