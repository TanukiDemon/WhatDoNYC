from flask import Flask
from flask_stormpath import StormpathManager
import configparser
import os

app = Flask(__name__)
from app import views

configPar = configparser.ConfigParser()
fn = os.path.join(os.path.dirname(__file__), 'config.ini')
configPar.read(fn)
app.config['SECRET_KEY'] = configPar['global']['sp_secret_key']
app.config['STORMPATH_API_KEY_FILE'] = os.path.join(os.path.dirname(__file__), 'apiKey.properties')
app.config['STORMPATH_APPLICATION'] = 'myapp'

stormpath_manager = StormpathManager(app)
stormpath_manager.register_view = '.register'
stormpath_manager.login_view = '.login'
