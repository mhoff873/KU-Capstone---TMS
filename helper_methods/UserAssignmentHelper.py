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
    tasks = []
    if userID is not None:
        requests = Request.query.filter_by(userID=userID, supervisorID=supervisorID).all()
    for request in requests:
        task = Task.query.filter_by(taskID=request.taskID).first()
        tasks.append(task)
    return tasks


def assign_task(userID=None,taskID=None,supervisorID=None):
    print('Making Request: ')
    request = Request()
    request.isApproved = True
    print('Is Approved')
    request.taskID = taskID
    print('Task ID ={}'.format(taskID))
    request.supervisorID = supervisorID
    print('Supervisor ID =', supervisorID)
    request.userID = userID
    print('User ID =', userID)
    try:
        db.session.add(request)
        db.session.commit()
        print('Request Stored to DB successfully')
    except Exception:
        db.session.commit()
        print('jk there was and error')
    return request


def delete_request(userID, taskID):
    print('Deleting Request')
    request = Request()
    request = Request.query.filter_by(taskID=taskID, userID=userID).first()
    print('Supervisor ID =', request.supervisorID)
    print('User ID =', request.userID)
    print('Task ID =', request.taskID)
    try:
        db.session.delete(request)
        db.session.commit()
    except Exception:
        db.session.commit()
    return request
