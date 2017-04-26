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
            for i in range(0, 5):
                graph.data("CREATE (actvy: Activity {name:{aName}})",
                    {"aName": "testActivity%d" % i})

            for i in range(0, 4):
                graph.data("CREATE (u: User {username:{uname}})",
                    {"uname": "testUser%d" % i})

            '''
            user 0 is connected to activites 0,1
            user 1 is connected to activities 0, 1, 2, 3, 4
            user 2 is connected to activities 1, 2, 3, 4
            user 3 is connected to activities 1, 4
            '''
            # Initialize the above relationships between each user and activity.
            # Commit these to the database afterwards
            for i in range(0, 2):
                tx.run("MATCH (u:User {username:'testUser0'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO]->(a)", aname = "testActivity%d" % i)

            for i in range(0, 5):
                tx.run("MATCH (u:User {username:'testUser1'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO]->(a)", aname = "testActivity%d" % i)

            for i in range(1, 5):
                tx.run("MATCH (u:User {username:'testUser2'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO]->(a)", aname = "testActivity%d" % i)

            for i in [1,4]:
                tx.run("MATCH (u:User {username:'testUser3'}), (a:Activity {name:{aname}})"
                    "CREATE (u)-[:HAS_BEEN_TO]->(a)", aname = "testActivity%d" % i)

            tx.commit()

            # Query for all of the current user's activities
            activities = graph.run("MATCH (u:User {username: 'testUser0'} )"
                "-[:HAS_BEEN_TO]->(a:Activity) RETURN a").data()

            assert len(activities) == 2

            # Get all users who rated the same activities as the current user
            similarUsers = graph.run("MATCH (u:User {username: 'testUser0'} )"
                "-[:HAS_BEEN_TO]->(a:Activity)<-[:HAS_BEEN_TO]-(other:User)"
                "WHERE NOT (other.username = 'testUser0') RETURN other.username").data()

            similarUsers = set(similarUsers)
            print(len(similarUsers))
            for u in similarUsers:
                print(u)
            assert len(similarUsers) == 3

            # List of users who meet the cutoff
            possibleUserRecs = []

            # Compute similarity of all similar users
            for simUser in similarUsers:
                # Get number of activities both the current user and user in similarUsers list have rated
                sharedActivities = graph.data("MATCH (u:User {username: 'testUser0'} )"
                    "-[:HAS_BEEN_TO]->(a)<-[:HAS_BEEN_TO]-(sim:User {name:{sUser}})"
                    " RETURN a", sUser = simUser["other.username"])

                # 0.2 is the similarity cutoff
                print(len(sharedActivities) / len(activities))
                if (len(sharedActivities) / len(activities) >= 0.2):
                    possibleUserRecs.append(simUser)

            print('Possible user recs: ', possibleUserRecs)
            assert len(possibleUserRecs) == 3

            # activities = {}
            activities = defaultdict(lambda: 0)

            # Get activities rated by at least two users in possibleRecs but not by the current user
            for simUser in possibleUserRecs:
                uniqueActivities = graph.run("MATCH (simUser:User {name:{sUser}} )"
                    "-[:HAS_BEEN_TO])->(a:Activity)<- NOT ([:HAS_BEEN_TO]-"
                    "(currUser:User {name: 'testUser0'}) ) RETURN a", sUser = simUser).data()

                for actvy in uniqueActivities:
                    activities[actvy] += 1
                '''
                for actvy in uniqueActivities:
                    if not actvy in activities:
                        activities[actvy] = 1
                    else:
                        activities[actvy] += 1
                '''

            # Returns list of sorted (key, value) tuples in descending order according to the the second tuple element
            sortedActivities = sorted(activities.items(), key=lambda x: x[1], reverse=True)

            assert len(sortedActivities) == 3
            assert sortedActivities[0] == 'testActivity4'
            assert sortedActivities[1] == 'testActivity3'
            assert sortedActivities[2] == 'testActivity2'

        finally:
            # Delete test nodes and their relationships
            for i in range(0, 4):
                graph.data("MATCH (u:User {username:{uname}}) DETACH DELETE u", uname = "testUser%d" % i)

            for i in range(0, 5):
                graph.data("MATCH (a:Activity {name:{aname}}) DETACH DELETE a", aname = "testActivity%d" % i)

if __name__ == '__main__':
    unittest.main()
