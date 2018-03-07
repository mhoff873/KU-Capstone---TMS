from sqlalchemy import Boolean, DateTime, Column, Integer, String, Date
from datetime import datetime

from database import db


class Task(db.Model):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    Basic task fields that are used for the Task, Main Steps, and Detailed
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
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    """
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
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    """
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
