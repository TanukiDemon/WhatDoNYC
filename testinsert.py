#! /usr/bin/python3
# examples: https://neo4j.com/developer/python
from neo4j.v1 import GraphDatabase, basic_auth

def acquireDriver(uris, authToken, config):
    for uri in uris:
	try:
		return GraphDatabase.driver(uri, authToken, config)
        except ServiceUnavailableException:
		# This URI failed, so loop around again if we have another
		print("try again")
    raise ServiceUnavailableException("No valid database URI found")

print("Starting...")
# Get the Python driver and create a session to issue Cypher queries
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4j"))
uri = "bolt://localhost:7687"
driver = acquireDriver(["bolt://localhost:7687", "bolt://52.33.222.241:7687"], basic_auth("neo4j", "neo4j"))
session = driver.session()


# Import the csv and read it into a vector
session.run("LOAD CSV WITH HEADERS FROM {} AS csvline WITH line", {"https://docs.google.com/spreadsheets/d/1N2z21Gg79k6nnWjDBR7YBzecAkELa7ekWiGpYzORV3U/edit?usp=sharing"})

# Create a new object for each line from the csv
for line in csvline:
    session.run("CREATE (a:testActivity { name: line.name, tag: line.tag, borough: line.borough, indoors/outdoors: line.indoors/outdoors })")

session.close()
