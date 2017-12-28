#######################################
#####     models.py - WEBTODO     #####
#######################################
#
# Models for users and list items
#
#######################################

#####     IMPORTS     #####
from app import db

class User(db.Model):
    __tablename__ = 'users'

    # Database Schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    # flask-login properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %s>' % (self.username)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    note = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Task %r>' % (self.title)
