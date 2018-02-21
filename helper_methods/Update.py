#
# Password Update Function
# author: Mason Hoffman
# created: 2/14/2018
# latest: 2/14/2018
# purpose: To set a password hash into the database
#

import bcrypt
import DB_Functions
import mysql.connector

# return password hash and salt from database. (salt is stored with the hash)
def setPassword(email,passw):
    db = DB_Functions.connect()
    cursor = db.cursor()
    hash = bcrypt.hashpw(passw.encode('utf8'), bcrypt.gensalt())
    cursor.execute("UPDATE supervisors SET password = '%s' WHERE email = '%s'" % (str(hash,'utf-8'),email))
    #print("UPDATE supervisors SET password = '%s' WHERE email = '%s'" % (str(hash,'utf-8')),email))
    db.commit()
      