from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This connects to the DB. Obviously we only want to connect when required, so
# this will be of interest to Nate and his DB interface class.

# need? 
# app = Flask(__name__)

# user and password need to be defined somehow
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost'
db = SQLAlchemy(app)

# flask-mysqldb doesn't seem to handle sanitization of variables used in queries,
# we will need to define a way to handle that for security reasons.

