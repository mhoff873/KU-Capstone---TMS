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
