#######################################
#####     models.py - WEBTODO     #####
#######################################
#
# Models for users and list items
#
############################

#####     IMPORTS     #####
from app import db

class ListUser(db.Model):
    __tablename__ = 'list-users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %s>' % (self.username)
