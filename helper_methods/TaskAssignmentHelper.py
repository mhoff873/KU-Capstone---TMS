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

def assign_to_all_users(supervisor_id, task_id):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    :param supervisor_id: self-explanatory
    :param task_id: self-explanatory
    :return: None
    """
    users = User.query.filter_by(supervisorID=supervisor_id).all()
    for user in users:
        assign_task(user.userID, task_id, supervisor_id)


def remove_from_all_users(supervisor_id, task_id):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    :param supervisor_id: self-explanatory
    :param task_id: self-explanatory
    :return: None
    """
    users = User.query.filter_by(supervisorID=supervisor_id).all()
    for user in users:
        delete_request(user.userID, task_id)


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
    request = Request()
    request.isApproved = True
    request.taskID = taskID
    request.supervisorID = supervisorID
    request.userID = userID
    request.dateRequested = datetime.utcnow()
    db.session.add(request)
    db.session.commit()
    print('Request Stored to DB successfully')


def delete_request(userID, taskID):
    print('Deleting Request')
    request = Request.query.filter_by(userID=userID, taskID=taskID).first()
    print('Supervisor ID ='.format(request.supervisorID))
    print('User ID ='.format(request.userID))
    print('Task ID ='.format(request.taskID))
    db.session.delete(request)
    db.session.commit()
