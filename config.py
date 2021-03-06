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
    DEBUG = os.environ.get('DEBUG') or False

    #####     WTF (forms)     #####
    WTF_CSRF_ENABLED = True

    #####     BCRYPT (password encryption)     #####
    # BCRYPT_HANDLE_LONG_PASSWORDS = True

    #####     DATABASE     #####
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jessereitz'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

class Test_Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    TESTING = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/WebTodoTestDB'
