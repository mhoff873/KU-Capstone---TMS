"""
Helper Methods for the User Assignment page
Author: Dylan Kramer
Created 3/9/2018
"""

from flask_login import current_user
from Forms.models import User, Supervisor, Request, Task
from database import db


def get_assignable_tasks(supervisorID):
    tasks = Task.query.filter_by(supervisorID=supervisorID, activated=True).all()
    return tasks


# def get_assignable_tasks():
    # tasks = Task.query.filter_by(enabled=True).all()
    # return tasks


def get_tasks_assigned(userID,supervisorID):
    requests = None
    if userID is not None:
        requests = Request.query.filter_by(userID=userID, supervisorID=supervisorID).all()
    return requests


def assign_task(userID=None,taskID=None,supervisorID=None):
    request = Request()
    request.isApproved = True
    #request.taskID = task.taskID
    #request.supervisorID = supervisor.supervisorID
    #request.userID = user.userID
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
