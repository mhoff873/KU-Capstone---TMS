"""
    Author(s):        Nathan Yost
    Creation Date:    February 27, 2018
    Course:           CSC355
    Purpose:          Library functions and forms dealing with the library.
"""

from Forms.models import Task
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, \
    BooleanField, FieldList, FormField, FileField

def get_tasks(supervisorID=None):
    """
    Gets tasks by supervisor id, or if none specified all tasks available.
    :param supervisorID: ID of the supervisor to look for tasks.
    :return: List of tasks
    """
    tasks = None
    if supervisorID is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(supervisorID=supervisorID).all()
    return tasks


def sort_alphabetically(tasks, reverse=False):
    return sorted(tasks, key=sort_key, reverse=reverse)

def sort_key(task):
    return task.title


# Not sure if this is going to be used...
class TaskForm(FlaskForm):
    submit = SubmitField("blah")
