import os
import unittest
import tempfile
from py2neo import Graph, Node, Relationship
from flask import session
from app.views import getPy2NeoSession

class FlaskrTestCase(unittest.TestCase):
    def test_recs(self):
        # Insert test users and activities
        graph = getPy2NeoSession()
        tx = graph.begin()

        for i in range(0, 5):
            graph.data("CREATE (actvy: Activity {name:{aName}})", {"aName": "testActivity(%d)" % i})

        for i in range(0, 4):
            graph.data("CREATE (u: User {username:{uname}})", {"uname": "testUser(%d)" % i})


        currUsername = 'testUser0'

        '''
        user 0 is connected to activites 0,1
        user 1 is connected to activities 0, 1, 2, 3, 4
        user 2 is connected to activities 1, 2, 3, 4
        user 3 is connected to activities 1, 4
        '''
        # Initialize the above relationships between each user and activity. Commit these to the database afterwards
        for i in range(0, 2):
            tx.run("MATCH (u:User {username:{uname}}), (a:Activity {name:{aname}}) CREATE (u)-[:HAS_BEEN_TO]->(a)", uname = "testUser0", aname = "testActivity(%d)" % i)

        for i in range(0, 5):
            tx.run("MATCH (u:User {username:{uname}}), (a:Activity {name:{aname}}) CREATE (u)-[:HAS_BEEN_TO]->(a)", uname = "testUser1", aname = "testActivity(%d)" % i)

        for i in range(1, 5):
            tx.run("MATCH (u:User {username:{uname}}), (a:Activity {name:{aname}}) CREATE (u)-[:HAS_BEEN_TO]->(a)", uname = "testUser2", aname = "testActivity(%d)" % i)

        for i in [1,4]:
            tx.run("MATCH (u:User {username:{uname}}), (a:Activity {name:{aname}}) CREATE (u)-[:HAS_BEEN_TO]->(a)", uname = "testUser3", aname = "testActivity(%d)" % i)

        tx.commit()

        # Query for all of the current user's activities
        # activities = graph.run("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity) RETURN actvy", uname = currUsername).evaluate()
        activities = graph.run("MATCH (u:User {username: {uname}})-[:HAS_BEEN_TO]-(b) RETURN b", uname = currUsername).data()
        print(currUsername)
        print(len(activities))
        assert len(activities) == 2

        # Get all users who rated the same activities as the current user
        similarUsers = graph.run("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(:Activity)<-[:HAS_BEEN_TO]-(otherUser:User) RETURN otherUser.username", uname = currUsername).evaluate()

        assert len(similarUsers) == 3

        # List of users who meet the cutoff
        possibleUserRecs = []

        # Compute similarity of all similar users
        for simUser in similarUsers:
            # Get number of activities both the current user and user in similarUsers list have rated
            sharedActivities = graph.data("MATCH (user:User {name:{uname}})-[:HAS_BEEN_TO]->(actvy:Activity)<-[:HAS_BEEN_TO]-(simiUser:User {name:{sUser}}) RETURN actvy", uname = currUsername, sUser = simUser["username"])

            # 0.2 is the similarity cutoff
            if (sharedActivities.length / activities.length >= 0.2):
                possibleUserRecs.append(simUser)

        assert len(possibleUserRecs) == 3

        activities = {}
        # Get activities rated by at least two users in possibleRecs but not by the current user
        for simUser in possibleUserRecs:
            uniqueActivities = graph.run("MATCH (simUser:User {name:{sUser}})-[:HAS_BEEN_TO])->(actvy:Activity)<- NOT ([:HAS_BEEN_TO]-(currUser:User {name:{uname}})) RETURN actvy", uname = currUsername, sUser = simUser).evaluate()

            for actvy in uniqueActivities:
                if not actvy in activities:
                    activities[actvy] = 1
                else:
                    activities[actvy] += 1

        # Returns list of sorted (key, value) tuples in descending order according to the the second tuple element
        sortedActivities = sorted(activities.items(), key=lambda x: x[1], reverse=True)

        assert len(sortedActivities) == 3
        assert sortedActivities[0] == 'testActivity4'
        assert sortedActivities[1] == 'testActivity3'
        assert sortedActivities[2] == 'testActivity2'

        # Delete test nodes
        for i in range(0, 4):
            graph.run("MATCH (user:User {username:{uname}})) DELETE user", uname = "testUser(%d)" % i).evaluate()

        for i in range(0, 5):
            graph.run("MATCH (a:Activity {name:{aname}})) DELETE user", aname = "testActivity(%d)" % i).evaluate()

if __name__ == '__main__':
    unittest.main()
