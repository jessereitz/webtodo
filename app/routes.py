#######################################
#####     routes.py - WEBTODO     #####
#######################################

from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, SignupForm

@app.route('/')
def index():
    return render_template('index.html', title="Sign In")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Create user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('signup.html', tile='sign up', form=form)
