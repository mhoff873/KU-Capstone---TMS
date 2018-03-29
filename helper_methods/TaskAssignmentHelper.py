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
    """
    Determines what tasks are available to assign by supervisor
    :param supervisorID: int to identify supervisor in DB table
    :return: list of assignable tasks
    """
    tasks = Task.query.filter_by(supervisorID=supervisorID, activated=True).all()
    return tasks


def get_tasks_assigned_to_user(userID, supervisorID):
    """
    Determines what tasks are assigned to given user
    :param user_id: int to identify user in DB table
    :return: list of tasks already assigned
    """
    requests = None
    tasks = []
    if userID is not None:
        requests = Request.query.filter_by(userID=userID, supervisorID=supervisorID).all()
    for request in requests:
        task = Task.query.filter_by(taskID=request.taskID).first()
        tasks.append(task)
    return tasks


def assign_task(userID, taskID, supervisorID):
    """
    :param userID: int to identify user in DB table
    :param taskID: int to identify task in DB table
    :param supervisorID: int to identify supervisor in DB table
    :return: None
    """
    existing_request = Request.query.filter_by(userID=userID, supervisorID=supervisorID, taskID=taskID).first()
    if existing_request is not None:
        # No more assigning duplicate tasks! BAD!
        return
    request = Request()
    request.isApproved = True
    request.taskID = taskID
    request.supervisorID = supervisorID
    request.userID = userID
    request.dateRequested = datetime.utcnow()
    db.session.add(request)
    db.session.commit()


def delete_request(userID, taskID):
    """
    Removes an assigned task from a user.
    :param userID: self-explanatory
    :param taskID: self-explanatory
    :return: None
    """
    request = Request.query.filter_by(userID=userID, taskID=taskID).first()
    db.session.delete(request)
    db.session.commit()


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
