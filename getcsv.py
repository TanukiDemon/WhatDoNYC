# examples: https://neo4j.com/developer/python/
from neo4j.v1 import GraphDatabase, basic_auth

# Get the Python driver and create a session to issue Cypher queries
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4j"))
session = driver.session()

# Import the csv and read it into a vector
session.run("LOAD CSV WITH HEADERS FROM {} AS csvline", {"https://docs.google.com/spreadsheets/d/1kegNRKh-vznoUqP37VXp7J1c-TpGC0OvSQZVdKc8QN4/edit"})

# Create a new object for each line from the csv
for line in csvline:
    session.run("CREATE (a:Activity { name: line.name, placeId: line.placeid, label: line.label, tag1: line.tag_1, tag2: line.tag_2, borough: line.borough, indoors/outdoors: line.indoors/outdoors, priceRange: line.price_range})")

session.close()
