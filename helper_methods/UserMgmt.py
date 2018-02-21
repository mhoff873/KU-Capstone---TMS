#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:35:26 2018

@author: nathan
"""
from Forms.models import User, Supervisor
from database import db


def create_account(form):
    user = None
    email = form.email.data
    password = form.password.data
    if form.is_supervisor.data:
        user = Supervisor()
    else:
        user = User()
    user.email = email
    user.password = password
    db.session.add(user)
    db.session.commit()


def edit_user(form):
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
    supervisorID = (Supervisor.query.filter_by(email=supervisor_email).first()).supervisorID
    users = User.query.filter_by(supervisorID=supervisorID).all()
    return users


# Requirement 34
def get_unassigned():
    users = User.query.filter_by(supervisorID=None).all()
    return users


def assign_user(form):
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
