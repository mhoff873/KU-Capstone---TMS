#
# Password Update Function
# author: Mason Hoffman
# created: 2/14/2018
# latest: 2/21/2018
# purpose: To set a password hash into the database (requirement 39)
#

import bcrypt
import models
from models import Supervisor
import database

# return password hash and salt from database. (salt is stored with the hash)
def setPassword(submittedEmail,passw):
    p = None
    p = (Supervisor.query.filter_by(email=submittedEmail).first())
    p.password = bcrypt.hashpw(passw.encode('utf8'), bcrypt.gensalt())
    database.db.session.commit()
      