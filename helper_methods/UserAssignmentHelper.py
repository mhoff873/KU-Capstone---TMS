"""
Helper Methods for the User Assignment page
Author: Dylan Kramer
Created 3/9/2018
"""

from flask_login import current_user
from Forms.models import User, Supervisor, Request, Task
from database import db
from datetime import datetime

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


def assign_task(userID=None, taskID=None, supervisorID=None):
    print('Making Request: ')
    request = Request()
    request.isApproved = True
    print('Is Approved')
    request.taskID = taskID
    print('Task ID ={}'.format(request.taskID))
    request.supervisorID = supervisorID
    print('Supervisor ID =', request.supervisorID)
    request.userID = userID
    print('User ID =', request.userID)
    request.dateRequested = datetime.utcnow()
    print('Date Requested =', request.dateRequested)
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
    requests = Request.query.filter_by(userID=userID).all()
    for request in requests:
        print('Supervisor ID ='.format(request.supervisorID))
        print('User ID ='.format(request.userID))
        print('Task ID ='.format(request.taskID))
        try:
            db.session.delete(request)
            db.session.commit()
        except Exception:
            db.session.commit()
