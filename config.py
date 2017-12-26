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

basedir = os.path.abspath(os.path.dirname(__file__))


#####     DATABASE     #####
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jessereitz'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# SQLITE test DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
