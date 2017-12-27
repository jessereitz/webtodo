#########################################
#####     __init__.py - WEBTODO     #####
#########################################
#
# Initializes WebTodo application. See README.txt for more information.
#
############################


###########################
#####     IMPORTS     #####
############################
import os
# extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# configuration
from config import Config

###############################
#####     FLASK SETUP     #####
###############################
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# flask-login
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'




# IMPORTANT:
#   - Cyclical import for views
from app import routes, models
