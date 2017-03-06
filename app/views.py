from app import app

@app.route('/')
@app.route('/login')
def login():
    return "Login here for your recommendations"
@app.route('/index')
def index():
    return "Hello, World!"
