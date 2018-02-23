#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:35:26 2018

@author: nathan
"""
from Forms.models import User, Supervisor
from database import db
import bcrypt


def create_user(form):
    """
    Creates a new user with an email and password that is encrypted using
    bcrypt.
    :param form: Form that is submitted to create a new user.
    :return: N/A
    """
    table = "users"

    # Create instance of User model
    user = User()

    # Punch in data from form to user
    user.email = form.email.data
    user.password = bcrypt.hashpw((form.password.data).encode("utf8"), bcrypt.gensalt())

    # Add new user to database
    db.session.add(user)
    db.session.commit()


def create_supervisor(form):
    """
    Creates a new supervisor with an email and a password that is encrypted
    using bcrypt.
    :param form: Form that is submitted to created a new supervisor.
    :return: N/A
    """
    table = "supervisors"

    # Create instance of Supervisor model
    user = Supervisor()

    # Punch in data from form to user
    user.email = form.email.data
    user.password = bcrypt.hashpw((form.password.data).encode("utf8"), bcrypt.gensalt())

    # Add new user to database
    db.session.add(user)
    db.session.commit()


def edit_user(form):
    """
    Allows the supervisor/admin to edit a user.
    :param form: Form submitted to edit the user/supervisor info.
    :return: N/A
    """
    user = None
    if form.is_supervisor.data:
        user = Supervisor.query.filter_by(email=form.person.data).first()
    else:
        user = User.query.filter_by(email=form.person.data).first()
    user.phone = form.phone.data
    user.fname = form.fname.data
    user.mname = form.mname.data
    user.lname = form.lname.data
    user.gender = form.gender.data
    user.birthday = form.birthday.data
    user.affiliation = form.affiliation.data
    user.ethnicity = form.ethnicity.data
    user.picture = form.picture.data
    db.session.commit()


# Requirement 32
def get_supervisor_users(supervisor_email):
    """
    Gets list of all users that are under a specified supervisor.
    :param supervisor_email: Email that is used to get the supervisor ID.
    :return: List of users that have the coordinating supervisor ID.
    """
    supervisorID = (Supervisor.query.filter_by(email=supervisor_email).first()).supervisorID
    users = User.query.filter_by(supervisorID=supervisorID).all()
    return users


# Requirement 34
def get_unassigned():
    """
    Gets list of all unassigned users.
    :return: List of all users that are not assigned a supervisor.
    """
    users = User.query.filter_by(supervisorID=None).all()
    return users


def assign_user(form):
    """
    Assigns a user to a supervisor.
    :param form: Form submitted to assign a user to a supervisor.
    :return: N/A
    """
    errors = ""
    supervisor = Supervisor.query.filter_by(email=form.supervisor.data).first()
    if supervisor is not None:
        user = User.query.filter_by(email=form.user.data).first()
        if user is not None:            
            user.supervisorID = supervisor.supervisorID
            db.session.commit()
        else:
            errors += "There is no user with the name of {}".format(
                    form.user.data)
    else:
        errors += "There is no supervisor with the name of {}".format(
                form.supervisor.data)
    return "Successfully assigned user to supervisor!" if errors == "" else errors
