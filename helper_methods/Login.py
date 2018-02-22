#
# Login Verification Functions
# author: Mason Hoffman
# created: 2/4/2018 (Go eagles!)
# latest: 2/21/2018
# purpose: hash comparison & login verification (requirement 38)
#

import bcrypt
import database
from Forms.models import User, Supervisor
from flask_login import login_user, logout_user

# requirement 38
# root function for login verification
def verifyMain(email,password):
    usr = requestHash(email)
    if usr:      # if the user was found in the table
        if usr.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8')):
            login_user(usr)
            return True  # Lets gooooo!
        else:    # the password hash did not match
            print("Invalid password")
    else:        # the user was not found in the table
        print("This account is not yet registered")
    return False # Something was fucked up

# return password hash and salt from database. (salt is stored with the hash)
def requestHash(submittedEmail):
    p = None
    p = (Supervisor.query.filter_by(email=submittedEmail).first())
    return p if p else None
    
    
      