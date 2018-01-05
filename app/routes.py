#######################################
#####     routes.py - WEBTODO     #####
#######################################

from flask import render_template, flash, redirect, url_for, session, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, loginManager
from app.forms import LoginForm, SignupForm, EditTaskForm, UsernameForm
from app.models import User, Task

@app.before_request
def before_request():
    g.user = current_user

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    if g.user.is_authenticated:
        tasks = g.user.tasks.filter_by(user_id=current_user.id).order_by(Task.complete.asc()).all()
    else:
        tasks = None
    return render_template('index.html', title="home", tasks=tasks)


#####     Task MGMT     ######
@app.route('/createTask', methods=['GET', 'POST'])
@login_required
def create_task():
    form = EditTaskForm()
    # on POST, validate form and create task
    if form.validate_on_submit():
        task_title = form.title.data
        task_note = form.note.data
        task = Task(title=task_title, note=task_note, user_id=current_user.id, complete=False)
        db.session.add(task)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.info('Creation of task failed.')
            abort(500)

        flash("New task successfully created.")
        return redirect(url_for('index'))

    return render_template('editTask.html',
                            form=form,
                            title="create task",
                            editStatus='create')

@app.route('/editTask/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash('Task not found.')
        return redirect(url_for('index'))
    form = EditTaskForm(obj=task)

    # on POST, validate form and update task
    if form.validate_on_submit():
        task.title = form.title.data
        task.note = form.note.data
        db.session.add(task)
        db.session.commit()
        flash("Task successfully updated.")
        return redirect(url_for('index'))

    return render_template('editTask.html',
                            form=form,
                            title="edit task",
                            editStatus='edit')

@app.route('/markTask/<task_id>')
@login_required
def mark_task(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash('Task not found. Unable to mark task.')
        return redirect(url_for('index'))
    if task.complete:
        task.complete = False
        is_completed = 'completed'
    else:
        task.complete = True
        is_completed = 'not completed'
    db.session.add(task)
    db.session.commit()
    flash("Task successfully marked as " + is_completed)
    return redirect(url_for('index'))

@app.route('/deleteTask/<task_id>')
@login_required
def delete_task(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash('Task not found. Unable to delete.')
        return redirect(url_for('index'))

    db.session.delete(task)
    db.session.commit()
    flash("Task successfully deleted.")
    return redirect(url_for('index'))


#####     end Task MGMT     #####


#####     User MGMT     ######
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # on POST, validate form and log user in
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

@app.route('/account')
@login_required
def account():
    if g.user.is_authenticated:
        return render_template('account.html')
    return render_template('index.html', title="home", tasks=tasks)

@app.route('/editUsername', methods=['GET', 'POST'])
@login_required
def edit_username():
    form = UsernameForm()

    if form.validate_on_submit():
        if username_available(form.username.data):
            current_user.username = form.username.data
            db.session.add(current_user)
            db.session.commit()
            flash('Username successfully updated')
            return redirect(url_for('account'))
        else:
            flash('Username unavailable.')
    return render_template('edit_username.html', form=form)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # on POST, validate form and sign user up
    if form.validate_on_submit():
        if username_available(form.username.data):
            newUser = User(username=form.username.data, password=form.password.data)
            db.session.add(newUser)
            db.session.commit()
            flash("New user " + newUser.username + " successfully created!")
            return redirect(url_for('login'))
        else:
            form.username.errors.append("Username taken.")
    return render_template('signup.html', tile='sign up', form=form)

#####     end User MGMT     #####

#####     ERRORS     #####
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title="that's not right"), 500

#####     end ERRORS     #####

#####     HELPERS     #####

def username_available(username):
    """ Returns True if username is available, False if not. """
    if not User.query.filter_by(username=username).first():
        return True
    else:
        return False
