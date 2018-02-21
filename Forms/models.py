#
# Database Models
# author: Mason Hoffman, Nathaniel Yost
# created: 2/13/2018
# latest: 2/13/2018
# purpose: Team B's classes for db records
#

from database import db
from datetime import datetime


class Base(object):
    """Class that represents a basic person"""
    supervisorID = db.Column("supervisorID", db.Integer, index=True)
    email = db.Column("email", db.String(255), unique=True, index=True)
    password = db.Column("password", db.String(255), index=True)
    phone = db.Column("phone", db.Integer, index=True)
    fname = db.Column("fname", db.String(255), index=True)
    mname = db.Column("mname", db.String(255), index=True)
    lname = db.Column("lname", db.String(255), index=True)
    gender = db.Column("gender", db.String(255), index=True)
    birthday = db.Column("birthday", db.Date, index=True)
    affiliation = db.Column("affiliation", db.String(255), index=True)
    ethnicity = db.Column("ethnicity", db.String(255), index=True)
    active = db.Column("active", db.Boolean, index=True)
    isLoggedIn = db.Column("isLoggedIn", db.Boolean, index=True)
    dateCreated = db.Column("dateCreated", db.DateTime, index=True)
    picture = db.Column("dateCreated", db.DateTime, index=True)

    def __init__(self):
        pass


class User(Base, db.Model):
    """User that is a child of base"""
    __tablename__ = "users"
    lastActive = db.Column("lastActive", db.DateTime, index=True)
    userID = db.Column("userID", db.Integer, primary_key=True)

    # user constructor
    def __init__(self, email=None, password=None):
        # Call parent constructor
        super(User, self).__init__()
        self.email = email
        self.password = password
        self.dateCreated = datetime.utcnow()
        self.lastActive = datetime.utcnow()

    # the informal string representation of a user object
    def __repr__(self):
        return '<User %r>' % (self.email)


class Supervisor(Base, db.Model):
    """Supervisor that is a child of base"""
    __tablename__ = "supervisors"
    supervisorID = db.Column("supervisorID", db.Integer, primary_key=True)

    def __init__(self, email=None, password=None):
        # Call parent constructor
        super(Supervisor, self).__init__()
        self.email = email
        self.password = password
        self.dateCreated = datetime.utcnow()
        self.lastActive = datetime.utcnow()

    def __repr__(self):
        return "<Supervisor %r>" % (self.email)
