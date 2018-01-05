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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# configuration
from config import Config

###############################
#####     FLASK SETUP     #####
###############################
app = Flask(__name__)
app.config.from_object(Config)
bcryption = Bcrypt(app)
db = SQLAlchemy(app)

print('\n\n\n\n')
print(app.debug)

# application logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('logs/webtodo.log', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('APP STARTUP')

# flask-login
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'




# IMPORTANT:
#   - Cyclical import for views
from app import routes, models
