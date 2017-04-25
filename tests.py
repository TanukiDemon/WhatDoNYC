import os
from app.wdnyc import *
import unittest
import tempfile
from app.models import *
from app.views import *
from py2neo import Graph
from flask import session

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

    def test_signup(self):
        # Fields are username, password, email, name, security question number, security question answer
        rv = self.signup('new', 'user', 'fake@com', 'fakename', 2, 'fakeA')
        assert b'You were registered' in rv.data
        # Remove user from database here

    def test_recs(self):
        # Insert test users and activities
        graph = getPy2NeoSession()

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

            currUsername = 'user0'

            # Query for all of the current user's activities
            activities = graph.data("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity)"
                                    "RETURN user, actvy",
                                    uname = currUsername)

            # Get all users who rated the same activities as the current user
            similarUsers = graph.data("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(:Activity)<-[:HAS_BEEN_TO]-(otherUser:User)"
                                      "RETURN otherUser.username",
                                      uname = currUsername)

            # List of users who meet the cutoff
            possibleUserRecs = []

            # Compute similarity of all similar users
            for simUser in similarUsers:
                # Get number of activities both the current user and user in similarUsers list have rated
                sharedActivities = graph.data("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity)<-[:HAS_BEEN_TO]-(simiUser:User {name:{sUser}})"
                                              "RETURN actvy",
                                              uname = currUsername, sUser = simUser["username"])

                # 0.2 is the similarity cutoff
                if (sharedActivities.length / activities.length >= 0.2):
                    possibleUserRecs.append(simUser)

            activities = {}
            # Get activities rated by at least two (or how many?) users in possibleRecs but not by the current user
            for simUser in possibleUserRecs:
                uniqueActivities = graph.data("MATCH (simUser:User {name:{sUser}})-[:HAS_BEEN_TO])->(actvy:Activity)<- NOT ([:HAS_BEEN_TO]-(currUser:User {name:{uname}}))")
                                              "RETURN actvy",
                                              uname = currUsername, sUser = simUser

                for actvy in uniqueActivities:
                    if not actvy in activities:
                        activities[actvy] = 1
                    else:
                        activities[actvy] += 1

            # Returns list of sorted (key, value) tuples in descending order according to the the second tuple element
            sortedActivities = sorted(activities.items(), key=lambda x: x[1], reverse=True)

            # Delete test nodes
            for i in range(0, 4):
                graph.data("MATCH (user:User {username:{uname}}))"
                           "DELETE user",
                           uname = "testUser(%d)" % i)

            for i in range(0, 5):
                graph.data("MATCH (a:Activity {name:{aname}}))"
                           "DELETE user",
                           aname = "testActivity(%d)" % i)

if __name__ == '__main__':
    unittest.main()
