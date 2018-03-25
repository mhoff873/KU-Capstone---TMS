"""
    Author(s):        Nathan Yost
    Creation Date:    February 27, 2018
    Course:           CSC355
    Purpose:          Library functions and forms dealing with the library.
"""

from Forms.models import Task, Supervisor
from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, DateField, SubmitField, \
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


def get_supervisors():
    return Supervisor.query.all()


def sort_chronologically(tasks, reverse=False):
    """
    Sorts a list of tasks chronologically, ascending or descending.
    :param tasks: List of tasks to be sorted.:
    :param reverse: Optional on whether to sort ascending or descending.
    :return: List of sorted tasks.
    """
    return sorted(tasks, key=chrono_sort_key, reverse=reverse)


def sort_alphabetically(tasks, reverse=False):
    """
    Sorts a list of tasks alphabetically, ascending or descending
    :param tasks: List of tasks to be sorted.
    :param reverse: Optional on whether to sort ascending or descending.
    :return: List of sorted tasks.
    """
    return sorted(tasks, key=alpha_sort_key, reverse=reverse)

def alpha_sort_key(task):
    """
    Allows the sorted functions to sort the tasks based on their title.
    :param task: Task that will be passed in to be sorted.
    :return: Title of each task passed into it.
    """
    return (task.title).lower()

def chrono_sort_key(task):
    """
    Allows the sorted functions to sort the tasks based on their title.
    :param task: Task that will be passed in to be sorted.
    :return: Title of each task passed into it.
    """
    return task.dateCreated

def search(argument):
    """
    Checks for matching keywords to all titles of each task in database.
    :param keyword: Some substring that can be found in a task title.
    :return: List of tasks that match the search criteria.
    """
    alltasks = get_tasks()
    if argument == "*":
        return alltasks
    tasks = []
    if len(argument) == 1:
        for task in alltasks:
            if argument.lower() == (task.title).lower()[0]:
                tasks.append(task)
    else:
        for task in alltasks:
            if argument.lower() in (task.title).lower():
                tasks.append(task)
    return tasks


# Not sure if this is going to be used...
class SearchForm(FlaskForm):
    search = TextField("Library Search Bar")
    submit = SubmitField("Search")
