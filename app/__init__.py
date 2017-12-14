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
from flask import Flask



###############################
#####     FLASK SETUP     #####
###############################
app = Flask(__name__)





# IMPORTANT:
#   - Cyclical import for views
from app import routes
