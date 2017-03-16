from flask import Flask
from flask_stormpath import StormpathManager
import configparser
import os

app = Flask(__name__)
from app import views

configPar = configparser.ConfigParser()
confIni = os.path.join(os.path.dirname(__file__), 'config.ini')
configPar.read(confIni)
app.config['SECRET_KEY'] = configPar['global']['sp_secret_key']
app.config['STORMPATH_API_KEY_FILE'] = os.path.join(os.path.dirname(__file__), 'apiKey.properties')
app.config['STORMPATH_APPLICATION'] = 'WhatDoNYC'

stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'

if __name__ == "__main__":
  app.run(host='0.0.0.0')
