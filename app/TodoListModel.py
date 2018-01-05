##########################################
#####     listModel.py - WEBTODO     #####
##########################################
#
# Model for overall list
#
##########################################

from app.models import Task

class TodoList():
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.tasks = user.tasks

    def get_all_tasks(self):
        """ Returns all tasks in list with incomplete tasks first. """
        return self.tasks.order_by(Task.complete.asc()).all()

    def get_task(self, task_id):
        """ Returns task with given task id. """
        return self.tasks.filter_by(id=task_id).first()

    def create_task(self, title, note=None, complete=False):
        """ Creates a task in todolist. Title must not be None. """
        task = Task(title=title, note=note, user_id=self.user.id, complete=complete)
        try:
            self.db.session.add(task)
            self.db.session.commit()
        except Exception:
            raise Exception

    def update_task(self, task, title, note):
        """ Updates the current task with given information. """
        task.title = title
        task.note = note
        try:
            self.db.session.add(task)
            self.db.session.commit()
        except Exception:
            raise Exception


    def mark_task(self, task_id):
        """ If given task is marked complete, mark it incomplete. Else mark it complete. """
        task = self.tasks.filter_by(id=task_id).first()
        if not task:
            return False
        if task.complete:
            task.complete = False
            is_complete = 'incomplete'
        else:
            task.complete = True
            is_complete = 'complete'

        try:
            self.db.session.add(task)
            self.db.session.commit()
            return is_complete
        except Exception:
            raise Exception

    def delete_task(self, task):
        """ Deletes given task. """
        pass
