from flask_mysqldb import MySQL

from project import app

# This connects to the DB. Obviously we only want to connect when required, so
# this will be of interest to Nate and his DB interface class.
mysql = MySQL(app)

# flask-mysqldb doesn't seem to handle sanitization of variables used in queries,
# we will need to define a way to handle that for security reasons.

