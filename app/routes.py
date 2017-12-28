#######################################
#####     routes.py - WEBTODO     #####
#######################################

from flask import render_template, flash, redirect, url_for, session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, loginManager
from app.forms import LoginForm, SignupForm
from app.models import User, Task

@app.before_request
def before_request():
    g.user = current_user

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    
    return render_template('index.html', title="home")

@app.route('/protected')
@login_required
def protected():
    flash("You got it, kid")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                flash('Logged in successfully!')
                return redirect(url_for('index'))
            else:
                form.password.errors.append("Incorrect password.")
        else:
            flash("User not found.")
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if not User.query.filter_by(username=form.username.data).first():
            newUser = User(username=form.username.data, password=form.password.data)
            db.session.add(newUser)
            db.session.commit()
            flash("New user " + newUser.username + " successfully created!")
            return redirect(url_for('login'))
        else:
            form.username.errors.append("Username taken.")
    return render_template('signup.html', tile='sign up', form=form)
