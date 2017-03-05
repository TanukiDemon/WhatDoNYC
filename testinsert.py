# examples: https://neo4j.com/developer/python
from neo4j.v1 import GraphDatabase, basic_auth

print "Starting..."
# Get the Python driver and create a session to issue Cypher queries
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "*"))
session = driver.session()

# Import the csv and read it into a vector
session.run("LOAD CSV WITH HEADERS FROM {file} AS csvline FIELDTERMINATOR ':' CREATE (:testActivity { name: csvline[0], tag: csvline[1], borough: csvline[2], indoors: csvline[3]})", {"file" : "https://drive.google.com/open?id=0B9-NO7e2_MJ1bzVaTWphT0gtT2s"})

# Create a new object for each line from the csv
session.run("CREATE (:testActivity { name: csvline[0], tag: csvline[1], borough: csvline[2], indoors: csvline[3]})")

print "Closing"
session.close()
