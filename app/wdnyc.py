import configparser
from os import path
from neo4j.v1 import GraphDatabase
from flask import Flask
import sqlite3 as lite
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

config = configparser.ConfigParser()
fn = path.join(path.dirname(__file__), 'config.ini')
config.read(fn)
app.secret_key = config.get('global', 'secret_key')

from .views import *

if __name__ == "__main__":
  app.run(host='0.0.0.0')
