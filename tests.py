import os
from app.wdnyc import *
import unittest
import tempfile
from app.models import *

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
            name=name
            securityQ=securityQ
            securityQanswer=securityA
        ), follow_redirects=True)

    def test_signup(self):
        rv = self.signup('new', 'user', 'fake@com', 'fakename', 'fakeQ', 'fakeA')
        assert b'You were registered' in rv.data
        # Remove user from database here        
