#######################################
#####     routes.py - WEBTODO     #####
#######################################

from flask import render_template, flash, redirect, url_for, session, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, loginManager, bcryption
from app.forms import LoginForm, SignupForm, EditTaskForm, EditUsernameForm, EditPasswordForm, DeleteAccountForm
from app.models import User, Task
from app.TodoListModel import TodoList

@app.before_request
def before_request():
    g.user = current_user
    g.todolist = TodoList(db, g.user)

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    if g.user.is_authenticated:
        tasks = g.todolist.get_all_tasks()
    else:
        tasks = None
    return render_template('index.html', title="home", tasks=tasks)


#####     Task MGMT     ######
@app.route('/createTask', methods=['GET', 'POST'])
@login_required
def create_task():
    """ On GET, display create task form. On POST, create task with given
        info. """
    form = EditTaskForm()
    # on POST, validate form and create task
    if form.validate_on_submit():
        try:
            g.todolist.create_task(title=form.title.data, note=form.note.data)
        except Exception:
            app.logger.info('Task creation failed.')
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
    """ On GET, display edit task form with current task info. On POST,
        updates specified task with new info. """
    task = g.todolist.get_task(task_id)
    if not task:
        flash('Task not found.')
        return redirect(url_for('index'))
    form = EditTaskForm(obj=task)
    # on POST, validate form and update task
    if form.validate_on_submit():
        try:
            g.todolist.update_task(task, form.title.data, form.note.data)
        except Exception:
            app.logger.info('Task update failed.')
            abort(500)
        flash("Task successfully updated.")
        return redirect(url_for('index'))

    return render_template('editTask.html',
                            form=form,
                            title="edit task",
                            editStatus='edit')

@app.route('/markTask/<task_id>')
@login_required
def mark_task(task_id):
    try:
        task_marked = g.todolist.mark_task(task_id)
    except Exception:
        app.logger.info('Mark task failed.')
        abort(500)
    if not task_marked:
        flash('Something went wrong. Ensure you are trying to mark a \
                task that exists.')
    else:
        flash("Task successfully marked as " + task_marked)
    return redirect(url_for('index'))

@app.route('/deleteTask/<task_id>')
@login_required
def delete_task(task_id):
    try:
        task_deleted = g.todolist.delete_task(task_id)
    except Exception:
        app.logger.info('Delete task failed.')
        abort(500)
    if task_deleted:
        flash('Task successfully deleted')
    else:
        flash('Something went wrong. Ensure you are trying to delete a \
                task that exists.')
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
            if bcryption.check_password_hash(user.password, form.password.data):
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
    form = EditUsernameForm()

    if form.validate_on_submit():
        if username_available(form.username.data):
            current_user.username = form.username.data
            db.session.add(current_user)
            db.session.commit()
            flash('Username successfully updated')
            return redirect(url_for('account'))
        else:
            form.username.data = None
            flash('Username unavailable.')
    return render_template('edit_username.html', form=form)

@app.route('/editPassword', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()

    if form.validate_on_submit():
        if bcryption.check_password_hash(current_user.password, form.current_password.data):
            current_user.password = bcryption.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.add(current_user)
            db.session.commit()
            flash('Password successfully updated')
            return redirect(url_for('account'))
        else:
            form.current_password.errors.append("Invalid password.")
            flash('Unable to update password.')
    else:
        if request.method == 'POST':
            flash("Unable to update password.")
    return render_template('edit_password.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/deleteAccount', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        username = form.username.data
        pw_candidate = form.password.data
        db_user = User.query.filter_by(username=username).first()
        if db_user == current_user and bcryption.check_password_hash(db_user.password, pw_candidate):
            delete_all_user_tasks(username=username)
            logout_user()
            db.session.delete(db_user)
            db.session.commit()
            flash('Your account has been deleted.')
            return redirect(url_for('index'))
        else:
            flash('Unsuccessful.')
    return render_template('delete_account.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # on POST, validate form and sign user up
    if form.validate_on_submit():
        if username_available(form.username.data):
            pw_hash = bcryption.generate_password_hash(form.password.data).decode('utf-8')
            newUser = User(username=form.username.data, password=pw_hash)
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

def delete_all_user_tasks(username):
    if not username:
        return False

    tasks = g.user.tasks.filter_by(user_id=current_user.id).all()
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
