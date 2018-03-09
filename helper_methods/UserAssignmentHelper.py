"""
Helper Methods for the User Assignment page
Author: Dylan Kramer
Created 3/9/2018
"""

def get_assignable_tasks(supervisorID=None):
    tasks = None
    if supervisorID is None:
        tasks = Task.query.filter_by(supervisorID=supervisorID).all()
    return tasks

def get_tasks_assigned(userID=None):
    requests = None
    if userID is not None:
        requests = query.filter_by(userID)
    return requests
