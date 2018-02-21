# Flask and many of it's plugins require a number of system variables to be set
# This file is used to define those variables and are loaded in app.py.

# App Config
# Secret Key is required for the CSRF tokens generated in our forms. It's a
# security feature for the forms.
SECRET_KEY = 'wefb292h3d9be#@@YEBBCE2NION32UDFEBUE2U202hfeu2onwdsjdf'

# Database Configs
# See: http://flask-mysqldb.readthedocs.io/en/latest/
MYSQL_HOST = 'localhost'
MYSQL_USER = 'nathan'
MYSQL_PASSWORD = 'es92blkh'
MYSQL_DB = 'TMS'
MYSQL_PORT = '3306'
MYSQL_CONNECT_TIMEOUT = 5
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://nathan:es92blkh@localhost:3306/TMS'
SQLALCHEMY_TRACK_MODIFICATIONS = False
