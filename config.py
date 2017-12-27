# -*- coding: utf-8 -*-
#######################################
#####     config.py - WEBTODO     #####
#######################################
#
# Configuration for WebTodo application.
#
############################

#####     IMPORTS     #####
import os

# Configuration Object
class Config(object):

    #####     FLASK CONFIGURATION     #####
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or "no guessing"

    #####     WTF (forms)     #####
    WTF_CSRF_ENABLED = True


    #####     DATABASE     #####
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jessereitz'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')