from flask_mysqldb import MySQL

from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager                         
                                
# creates the database session object for connecting later                              
db = SQLAlchemy(app)
mysql = MySQL(app)

# LoginManager allows the application and Flask-Login to work together.
login_manager = LoginManager()
login_manager.init_app(app)

# Login page is 'login'. 
# This will redirect you to login if you try to access a page that requires a login.
login_manager.login_view = 'login'

