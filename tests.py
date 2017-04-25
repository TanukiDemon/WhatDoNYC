import os
from app.wdnyc import *
import unittest
import tempfile
from app.models import *
from py2neo import Graph

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()

    def tearDown(self):
        os.unlink(app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        rv = self.login('test', 'user')
        assert b'You were logged in' in rv.data
        rv = self.login('tests', 'user')
        assert b'Invalid username' in rv.data
        rv = self.login('test', 'users')
        assert b'Invalid password' in rv.data

    def signup(self, username, password, email, name, securityQ, securityA):
        return self.app.post('/signup', data=dict(
            username=username,
            passwor=password,
            email=email,
            name=name,
            securityQ=securityQ,
            securityQanswer=securityA
        ), follow_redirects=True)

    def recs(self):
        # Insert test users and activities
        for i in range(0, 5):
            graph.data("INSERT (actvy: Activity) {name:{aName}}", aName = ("testActivity" + str(i)))
        
        for i in range(0, 4):
            graph.data("INSERT (u: User) {username:{uname}}", uname = ("testUser" + str(i)))

        # user 0 is connected to activites 0,1
        # user 1 is connected to activities 0, 1, 2, 3, 4
        # user 2 is connected to activities 1, 2, 3, 4
        # user 3 is connected to activities 1, 4

    def test_signup(self):
        # Fields are username, password, email, name, security question number, security question answer
        rv = self.signup('new', 'user', 'fake@com', 'fakename', 2, 'fakeA')
        assert b'You were registered' in rv.data
        # Remove user from database here        

    def test_recs(self):
        

if __name__ == '__main__':
    unittest.main()
