# Author(s):        Nathan Yost
# Creation Date:    February 27, 2018
# Course:           CSC355
# Purpose:          Library functions and forms dealing with the library.

from Forms.models import Task


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
