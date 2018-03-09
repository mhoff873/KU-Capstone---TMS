"""
Helper Methods for the User Assignment page
Author: Dylan Kramer
Created 3/9/2018
"""

from Forms.models import User, Supervisor, Request, Task
from database import db


def get_assignable_tasks(supervisorID=None):
    tasks = None
    if supervisorID is None:
        tasks = Task.query.filter_by(supervisorID=supervisorID, enabled=True).all()
    return tasks


def get_tasks_assigned(userID=None):
    requests = None
    if userID is not None:
        requests = query.filter_by(userID)
    return requests


def assign_task(user=None,task=None,supervisor=None):
    request = Request()
    request.isApproved = True
    request.taskID = task.taskID
    request.supervisorID = supervisor.supervisorID
    request.userID = user.userID
    try:
        db.session.add(request)
        db.session.commit()
    except Exception:
        db.session.commit()
    return request


def delete_request(request=None):
    try:
        db.session.delete(request)
        db.session.commit()
    except Exception:
        db.session.commit()
    return request
