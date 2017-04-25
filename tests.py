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
            graph.data("INSERT (actvy: Activity) {name:{aName}}", aName = ("testActivity(%d)" % i))
        
        for i in range(0, 4):
            graph.data("INSERT (u: User) {username:{uname}}", uname = ("testUser(%d)" % i))

        '''
        user 0 is connected to activites 0,1
        user 1 is connected to activities 0, 1, 2, 3, 4
        user 2 is connected to activities 1, 2, 3, 4
        user 3 is connected to activities 1, 4
        '''
        graph.data("MATCH (u:User {username:{uname}}), (a0:Activity {name:{a0name}}), (a1:Activity {name:{a1name}})" ,
                   "CREATE (u)-[:HAS_BEEN_TO]->(a0)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a1)",
                   uname = 'user0', a0name = 'testActivity0', a1name = 'testActivity1')

        graph.data("MATCH (u:User {username:{uname}}), (a0:Activity {name:{a0name}}), (a1:Activity {name:{a1name}}), (a2:Activity {name:{a2name}}), (a3:Activity {name:{a3name}}), (a4:Activity {name:{a4name}})",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a0)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a1)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a2)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a3)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a4)",
                   uname = 'user1', a0name = 'testActivity0', a1name = 'testActivity1', a2name = 'testActivity2', a3name = 'testActivity3', a4name = 'testActivity4')

        graph.data("MATCH (u:User {username:{uname}}), (a1:Activity {name:{a1name}}), (a2:Activity {name:{a2name}}), (a3:Activity {name:{a3name}}), (a4:Activity {name:{a4name}})",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a1)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a2)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a3)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a4)",
                   uname = 'user2', a1name = 'testActivity1', a2name = 'testActivity2', a3name = 'testActivity3', a4name = 'testActivity4')

        graph.data("MATCH (u:User {username:{uname}}), (a1:Activity {name:{a1name}}), (a4:Activity {name:{a4name}})" ,
                   "CREATE (u)-[:HAS_BEEN_TO]->(a1)",
                   "CREATE (u)-[:HAS_BEEN_TO]->(a4)",
                   uname = 'user3', a1name = 'testActivity1', a4name = 'testActivity4')        

MATCH (u:User {username:'admin'}), (r:Role {name:'ROLE_WEB_USER'})
CREATE (u)-[:HAS_ROLE]->(r)


    def test_signup(self):
        # Fields are username, password, email, name, security question number, security question answer
        rv = self.signup('new', 'user', 'fake@com', 'fakename', 2, 'fakeA')
        assert b'You were registered' in rv.data
        # Remove user from database here        

    def test_recs(self):
        

if __name__ == '__main__':
    unittest.main()
