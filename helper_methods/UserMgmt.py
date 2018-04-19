#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:35:26 2018

@author: nathan
"""
from Forms.models import User, Supervisor
from database import *
import bcrypt


def create_account(form):
    """
    need to get rid of this create_accout
    need it for now to work on tms
    """
    user = None
    email = form.email.data
    password = form.password.data
    if form.is_supervisor.data:
        user = Supervisor()
    else:
        user = User()
    user.email = email
    user.password = password


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


def edit_supervisor(form, supervisor):
    """
    Allows the admin to edit a supervisor.
    :param form: Form submitted to edit the user/supervisor info.
    :return: N/A
    """
    query = """
            UPDATE supervisors
            SET %s='%s'
            WHERE email='%s'
            """
    email = supervisor.email
    cursor = mysql.connection.cursor()
    if form.phone.data:
        cursor.execute(query % ("phone", form.phone.data, email))
        print(query % ("phone", form.phone.data, email))

    if form.fname.data:
        cursor.execute(query %("fname", form.fname.data, email))
        print(query %("fname", form.fname.data, email))

    if form.mname.data:
        cursor.execute(query % ("mname", form.mname.data, email))

    if form.lname.data:
        cursor.execute(query %("lname", form.lname.data, email))

    if form.gender.data:
        cursor.execute(query % ("gender", form.gender.data, email))

    if form.birthday.data:
        cursor.execute(query % ("birthday", form.birthday.data, email))

    if form.affiliation.data:
        cursor.execute(query % ("affiliation", form.affiliation.data, email))

    if form.ethnicity.data:
        cursor.execute(query % ("ethnicity", form.ethnicity.data, email))

    if form.picture.data:
        cursor.execute(query % ("picture", form.picture.data, email))

    mysql.connection.commit()


def edit_user(form, user):
    """
    Allows the supervisor/admin to edit a user.
    :param form: Form submitted to edit the user/supervisor info.
    :return: N/A
    """
    query = """
            UPDATE users
            SET %s='%s'
            WHERE email='%s'
            """
    email = user.email
    cursor = mysql.connection.cursor()
    if form.phone.data:
        cursor.execute(query % ("phone", form.phone.data, email))
        print(query % ("phone", form.phone.data, email))

    if form.fname.data:
        cursor.execute(query %("fname", form.fname.data, email))
        print(query %("fname", form.fname.data, email))

    if form.mname.data:
        cursor.execute(query % ("mname", form.mname.data, email))

    if form.lname.data:
        cursor.execute(query %("lname", form.lname.data, email))

    if form.gender.data:
        cursor.execute(query % ("gender", form.gender.data, email))

    if form.birthday.data:
        cursor.execute(query % ("birthday", form.birthday.data, email))

    if form.affiliation.data:
        cursor.execute(query % ("affiliation", form.affiliation.data, email))

    if form.ethnicity.data:
        cursor.execute(query % ("ethnicity", form.ethnicity.data, email))

    if form.picture.data:
        cursor.execute(query % ("picture", form.picture.data, email))

    mysql.connection.commit()



# Requirement 32
def get_supervisor_users(supervisor_email):
    """
    Gets list of all users that are under a specified supervisor.
    :param supervisor_email: Email that is used to get the supervisor ID.
    :return: List of users that have the coordinating supervisor ID.
    """
    print(supervisor_email)
    supervisorID = (Supervisor.query.filter_by(email=supervisor_email).first()).supervisorID
    users = User.query.filter_by(supervisorID=supervisorID).all()
    print(users)
    return users


# Requirement 34
def get_unassigned():
    """
    Gets list of all unassigned users.
    :return: List of all users that are not assigned a supervisor.
    """
    users = User.query.filter_by(supervisorID=None).all()
    return users


def assign_user(superID, userID):
    """
    Assigns a user to a supervisor.
    :param form: Form submitted to assign a user to a supervisor.
    :return: N/A
    """
    errors = ""
    supervisor = Supervisor.query.filter_by(supervisorID=superID).first()
    if supervisor is not None:
        user = User.query.filter_by(userID=userID).first()
        if user is not None:
            user.supervisorID = supervisor.supervisorID
            db.session.commit()
        else:
            errors += "Could not find specified user!"
    else:
        errors += "Could not find specified supervisor!"
    return "Successfully assigned user to supervisor!" if errors == "" else errors


def populateFieldsSupervisor(supervisor, form):
    #form.password.data = supervisor.password
    form.phone.data = supervisor.phone
    form.fname.data = supervisor.fname
    form.mname.data = supervisor.mname
    form.lname.data = supervisor.lname
    form.gender.data = supervisor.gender
    form.birthday.data = supervisor.birthday
    form.affiliation.data = supervisor.affiliation
    form.ethnicity.data = supervisor.ethnicity
    form.picture.data = supervisor.picture


def populateFieldsUser(user, form):
    #form.password.data = supervisor.password
    form.phone.data = user.phone
    form.fname.data = user.fname
    form.mname.data = user.mname
    form.lname.data = user.lname
    form.gender.data = user.gender
    form.birthday.data = user.birthday
    form.affiliation.data = user.affiliation
    form.ethnicity.data = user.ethnicity
    form.picture.data = user.picture
