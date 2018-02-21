#
# Login Verification Functions
# author: Mason Hoffman
# created: 2/4/2018 (Go eagles!)
# latest: 2/5/2018
# purpose: hash comparison & login verification for the supervisors
#

import bcrypt
import DB_Functions
import mysql.connector

#(encode the input as utf-8 on account creation hash)
#hashed = bcrypt.hashpw(passw.encode('utf8'), bcrypt.gensalt())

# root function for login verification
def verifyMain(email,password):
    print("verifying login")
    hash = requestHash(email)
    print("verifying hash")
    return hash == bcrypt.hashpw(password.encode('utf-8'), hash)

# return password hash and salt from database. (salt is stored with the hash)
def requestHash(email):
    db = DB_Functions.connect()
    cursor = db.cursor()
    cursor.execute("SELECT password FROM supervisors WHERE email = '%s'" % (email,))
    user = None
    user = cursor.fetchone()
    #return the password hash when there is one
    return user[0].encode('utf-8') if user else false
      