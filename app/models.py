#######################################
#####     models.py - WEBTODO     #####
#######################################
#
# Models for users and list items
#
#######################################

#####     IMPORTS     #####
from app import db, bcryption

class User(db.Model):
    __tablename__ = 'users'

    # Database Schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def validate_password(self, candidate):
        return bcryption.check_password_hash(self.password, candidate)

    def edit_password(self, current_password, new_password):
        if bcryption.check_password_hash(self.password, current_password):
            self.password = bcryption.generate_password_hash(new_password).decode('utf-8')
            return True
        else:
            return False

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
    title = db.Column(db.String(64), nullable=False)
    note = db.Column(db.String(140))
    complete = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % (self.title)
