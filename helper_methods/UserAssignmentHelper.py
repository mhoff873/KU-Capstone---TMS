"""
Helper Methods for the User Assignment page
Author: Dylan Kramer
Created 3/9/2018
"""

from flask_login import current_user
from Forms.models import User, Supervisor, Request, Task
from database import db


def get_assignable_tasks(supervisorID=None):
    """
    Determines what tasks are available to assign by supervisor
    :param supervisorID: int to identify supervisor in DB table
    :return: list of assignable tasks
    """
    tasks = []
    # if supervisorID is None:
    #     tasks = Task.query.filter_by(supervisorID=supervisorID, enabled=True).all()
    # return tasks
    tasks = Task.query.filter_by(supervisorID=current_user.supervisorID, activated=True).all()
    return tasks


# def get_assignable_tasks():
    # tasks = Task.query.filter_by(enabled=True).all()
    # return tasks


def get_tasks_assigned(user_id=None):
    """
    Determines what tasks are assigned to given user
    :param user_id: int to identify user in DB table
    :return: list of tasks already assigned
    """
    requests = None
    if user_id is not None:
        requests = Request.query.filter_by(user_id)
    return requests


def assign_task(userID=None, taskID=None, supervisorID=None):
    """
    # TODO function unused?
    :param userID: int to identify user in DB table
    :param taskID: int to identify task in DB table
    :param supervisorID: int to identify supervisor in DB table
    :return: request: entry in request table
    """
    request = Request()
    request.isApproved = True
    # request.taskID = task.taskID
    # request.supervisorID = supervisor.supervisorID
    # request.userID = user.userID
    try:
        db.session.add(request)
        db.session.commit()
    except Exception:
        db.session.commit()
    return request


def delete_request(request=None):
    """
    # TODO function unused?
    :param request: request object to be deleted
    :return: request: deleted object?
    """
    try:
        db.session.delete(request)
        db.session.commit()
    except Exception:
        db.session.commit()
    return request
