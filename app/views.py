from neo4j.v1 import GraphDatabase

from app import app

@app.route('/')

@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    form = registerForm(request.form)
    # Let Storm Path handle things here

    # Serve "Would You Rather" survey
    form = WouldYouRatherForm(request.form)
    if form.validate_on_submit():
        return recommendationResults(form)
    return render_template('recommendations.html', title='Recommendations', form=form)

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    session.run("CREATE (a:Person {username: {uname}, password: {pword}, surveyAnswers: {answers}})",
            {"uname": form.username, "pword": form.password, "answers": form.answers})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login here for your recommendations"

@app.route('/recommendations', methods=['GET'])

