import configparser
from os import path
from neo4j.v1 import GraphDatabase
from flask import Flask
import sqlite3 as lite
from flask_wtf.csrf import CSRFProtect
from flask_cache import Cache

app = Flask(__name__)

config = configparser.ConfigParser()
fn = path.join(path.dirname(__file__), 'config.ini')
config.read(fn)
app.secret_key = config.get('global', 'secret_key')
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from .views import *

if __name__ == "__main__":
  app.run(host='0.0.0.0')
