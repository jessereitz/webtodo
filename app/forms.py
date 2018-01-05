######################################
#####     forms.py - WEBTODO     #####
######################################
#
# Forms used by application
#
######################################

#####     IMPORTS     #####
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo

#####     USER FORMS     #####
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class EditUsernameForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditPasswordForm(FlaskForm):
    current_password = PasswordField('current password', validators=[DataRequired()])
    new_password = PasswordField('new password', validators=[DataRequired(), EqualTo('confirm_new_password', message='New passwords must match')])
    confirm_new_password = PasswordField('confirm new password', validators=[DataRequired()])
    submit = SubmitField('Submit')

#####     TASK FORMS     #####
class EditTaskForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    note = TextAreaField('note')
    submit = SubmitField('Submit')
