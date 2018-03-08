#
# Login Verification Functions
# author: Mason Hoffman
# created: 2/4/2018 (Go eagles!)
# latest: 3/6/2018
# purpose: hash comparison & login verification (requirement 38)
#

import bcrypt
import database
from Forms.models import User, Supervisor, Admin
from flask_login import login_user

determined_role = "unknown"


# Login Manager id loader. Functions for Superisors
@database.login_manager.user_loader
def load_user(id):
    if (globals()['determined_role'] == "supervisor"):
        return Supervisor.query.get(int(id))
    if (globals()['determined_role'] == "admin"):
        return Admin.query.get(int(id))


# requirement 38
# root function for login verification
def verifyMain(email, password):
    acc = requestHash(email)
    if acc:  # if the account was found in either the admin or the supervisor table
        if acc.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), acc.password.encode('utf-8')):
            login_user(acc)
            return True  # Lets gooooo!
        else:  # the password hash did not match
            print("Invalid password")
    else:  # the user was not found in the table
        print("This account is not yet registered")
    return False  # Something was fucked up


# return password hash and salt from database. (salt is stored with the hash)
def requestHash(submittedEmail):
    p = None
    p = (Supervisor.query.filter_by(email=submittedEmail).first())
    if (p):
        globals()['determined_role'] = "supervisor"
        return p
    p = (Admin.query.filter_by(username=submittedEmail).first())
    if (p):
        globals()['determined_role'] = "admin"
        return p
    return None