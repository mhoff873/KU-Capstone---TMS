#
# Database Models
# author: Mason Hoffman, Nathaniel Yost
# created: 2/13/2018
# latest: 2/13/2018
# purpose: Team B's classes for db records
#

from database import db, login_manager
from datetime import datetime
from flask_login import UserMixin  
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Date

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Base(UserMixin, object):
    """Class that represents a basic person"""
    supervisorID = Column("supervisorID", Integer, index=True)
    email = Column("email", String(255), unique=True, index=True)
    password = Column("password", String(255), index=True)
    phone = Column("phone", Integer, index=True)
    fname = Column("fname", String(255), index=True)
    mname = Column("mname", String(255), index=True)
    lname = Column("lname", String(255), index=True)
    gender = Column("gender", String(255), index=True)
    birthday = Column("birthday", Date, index=True)
    affiliation = Column("affiliation", String(255), index=True)
    ethnicity = Column("ethnicity", String(255), index=True)
    active = Column("active", Boolean, index=True)
    isLoggedIn = Column("isLoggedIn", Boolean, index=True)
    dateCreated = Column("dateCreated", DateTime, index=True)
    picture = Column("picture", DateTime, index=True)

    def __init__(self):
        pass


class User(Base, db.Model):
    """User that is a child of base"""
    __tablename__ = "users"
    lastActive = Column("lastActive", DateTime, index=True)
    userID = Column("userID", Integer, primary_key=True)

    # user constructor
    def __init__(self, email=None, password=None):
        # Call parent constructor
        super(User, self).__init__()
        self.email = email
        self.password = password
        self.dateCreated = datetime.utcnow()
        self.lastActive = datetime.utcnow()
    
    def get_id(self):
        return str(self.userID)

    # the informal string representation of a user object
    def __repr__(self):
        return '<User %r>' % (self.email)


class Supervisor(Base, db.Model):
    """Supervisor that is a child of base"""
    __tablename__ = "supervisors"
    supervisorID = Column("supervisorID", Integer, primary_key=True)
    
    def get_id(self):
        return str(self.supervisorID)
        
    def __init__(self, email=None, password=None):
        # Call parent constructor
        super(Supervisor, self).__init__()
        self.email = email
        self.password = password
        self.dateCreated = datetime.utcnow()
        self.lastActive = datetime.utcnow()

    def __repr__(self):
        return "<Supervisor %r>" % (self.email)


class Task(db.Model):
    """Basic task fields that are used for the Task, Main Steps, and Detailed
    Steps"""
    __tablename__ = 'task'
    taskID = Column('taskID', Integer, primary_key=True)
    supervisorID = Column('supervisorID', Integer)
    title = Column('title', String(255))
    description = Column('description', String(255))
    activated = Column('activated', String(255))
    dateCreated = Column('dateCreated', Date)
    dateModified = Column('dateModified', Date)
    lastUsed = Column('lastUsed', DateTime)
    published = Column('published', Boolean)
    image = Column('image', String(255))

    def __init__(self, title=None):
        super(Task, self).__init__()
        self.title = title
        self.dateCreated = datetime.utcnow()
        self.dateModified = datetime.utcnow()
        self.lastUsed = datetime.utcnow()


class MainStep(db.Model):
    __tablename__ = 'mainSteps'
    mainStepID = Column('mainStepID', Integer, primary_key=True)
    taskID = Column('taskID', Integer)
    title = Column('title', String(255))
    requiredInfo = Column('requiredInfo', String(255))
    listOrder = Column('listOrder', Integer)
    requiredItem = Column('requiredItem', String(255))
    stepText = Column('stepText', String(255))
    audio = Column('audio', String(255))
    image = Column('image', String(255))
    video = Column('video', String(255))

    def __init__(self, title=None):
        super(MainStep, self).__init__()
        self.title = title


class DetailedStep(db.Model):
    __tablename__ = 'detailedSteps'
    detailedStepID = Column('detailedStepID', Integer, primary_key=True)
    mainStepID = Column('mainStepID', Integer)
    title = Column('title', String(255))
    stepText = Column('stepText', String(255))
    listOrder = Column('listOrder', Integer)
    image = Column('image', String(255))

    def __init__(self, title=None):
        super(DetailedStep, self).__init__()
        self.title = title
