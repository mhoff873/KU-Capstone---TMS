# Flask and many of it's plugins require a number of system variables to be set
# This file is used to define those variables and are loaded in app.py.

# App Config
# Secret Key is required for the CSRF tokens generated in our forms. It's a
# security feature for the forms.
SECRET_KEY = 'wefb292h3d9be#@@YEBBCE2NION32UDFEBUE2U202hfeu2onwdsjdf'

MYSQL_HOST = 'localhost'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = 'tmst_db'
MYSQL_CURSORCLASS = 'DictCursor'

# Database Configs
# Try not to leave passwords on a public facing thing guys
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://*****:*****@localhost:3306/tmst_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

