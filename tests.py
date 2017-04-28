import os
import unittest
import tempfile
from py2neo import Graph, Node, Relationship
from flask import session
from app.views import getPy2NeoSession
from collections import defaultdict

class FlaskrTestCase(unittest.TestCase):
    def test_recs(self):
        # Insert test users and activities
        graph = getPy2NeoSession()
        tx = graph.begin()

        try:
            # Create test users and activities with the following relationships
            for i in range(0, 5):
                graph.data("CREATE (actvy: Activity {name:{aName}})",
                    {"aName": "testActivity%d" % i})

            for i in range(0, 4):
                graph.data("CREATE (u: User {username:{uname}})",
                    {"uname": "testUser%d" % i})

            '''
                Initialize the following relationships between each user and activity.
                Commit these to the database afterwards
                user 0 is connected to activites 0,1
                user 1 is connected to activities 0, 1, 2, 3, 4
                user 2 is connected to activities 1, 2, 3, 4
                user 3 is connected to activities 1, 4

            '''
            for i in range(0, 2):
                tx.run("MATCH (u:User {username:'testUser0'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO{weight:1}]->(a)", aname = "testActivity%d" % i)

            for i in range(0, 5):
                tx.run("MATCH (u:User {username:'testUser1'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO{weight:1}]->(a)", aname = "testActivity%d" % i)

            for i in range(1, 5):
                tx.run("MATCH (u:User {username:'testUser2'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO{weight:1}]->(a)", aname = "testActivity%d" % i)

            for i in [1,4]:
                tx.run("MATCH (u:User {username:'testUser3'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO{weight:1}]->(a)", aname = "testActivity%d" % i)

            tx.commit()

            # Query for all of testUser0's activities
            activities = graph.run("MATCH (u:User {username: 'testUser0'} )"
                "-[:HAS_BEEN_TO]->(a:Activity) RETURN a").data()

            assert len(activities) == 2

            # Get all users who rated the same activities as the current user
            similarUsers = graph.run("MATCH (u:User {username: 'testUser0'} )"
                "-[:HAS_BEEN_TO{weight:1}]->(a:Activity)<-[:HAS_BEEN_TO{weight:1}]-(other:User)"
                "WHERE NOT (other.username = 'testUser0') RETURN other.username").data()

            # Create a list of the names of users who share at least one
            # activity with testUser0
            uniqueSimUsers = []
            for sim in similarUsers:
                for key, value in sim.items():
                    uniqueSimUsers.append(value)

            # Remove duplicates
            uniqueSimUsers = set(uniqueSimUsers)
            assert len(uniqueSimUsers) == 3

            # List of users who meet the cutoff
            possibleUserRecs = []

            # Compute similarity of all similar users
            for simUser in uniqueSimUsers:
                # Get number of activities both the current user and user in similarUsers list have rated
                sharedActivities = graph.run("MATCH (u:User {username: 'testUser0'} )"
                    "-[:HAS_BEEN_TO{weight:1}]->(a)<-[:HAS_BEEN_TO{weight:1}]-(sim:User {username:{sUser}})"
                    " RETURN a", sUser = simUser).data()

                # 0.2 is the similarity cutoff
                # If the following quotient is greater or equal than 0.2,
                # then the similar user's name is added to possibleUserRecs
                if (len(sharedActivities) / len(activities) >= 0.2):
                    possibleUserRecs.append(simUser)

            assert len(possibleUserRecs) == 3

            # activities will contain the popularity of activities
            # that will be recommended to testUser0
            activities = defaultdict(lambda: 0)

            # Get activities rated by at least two users in possibleRecs but not by the current user
            for simUser in possibleUserRecs:
                uniqueActivities = graph.data("MATCH (simUser:User {username:{sUser}})"
                    "-[:HAS_BEEN_TO{weight:1}]->(a) MATCH (u:User {username:'testUser0'})"
                    "WHERE NOT (u)-[:HAS_BEEN_TO]->(a) RETURN a.name", sUser = simUser)

                for a in uniqueActivities:
                    for key, value in a.items():
                        activities[value] += 1

            assert(activities['testActivity4'] == 3)
            assert(activities['testActivity3'] == 2)
            assert(activities['testActivity2'] == 2)
            assert(activities['testActivity1'] == 0)
            assert(activities['testActivity0'] == 0)

            # Returns list of sorted (key, value) tuples in descending order according to the the second tuple element
            sortedActivities = sorted(activities.items(), key=lambda x: x[1], reverse=True)

            assert len(sortedActivities) == 5
            assert sortedActivities[0][0] == 'testActivity4'
            assert sortedActivities[1][0] == 'testActivity3' or 'testActivity2'
            assert sortedActivities[2][0] == 'testActivity3' or 'testActivity2'

        finally:
            # Delete test nodes and their relationships
            for i in range(0, 4):
                graph.data("MATCH (u:User {username:{uname}}) DETACH DELETE u", uname = "testUser%d" % i)

            for i in range(0, 5):
                graph.data("MATCH (a:Activity {name:{aname}}) DETACH DELETE a", aname = "testActivity%d" % i)

if __name__ == '__main__':
    unittest.main()
