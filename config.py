# Flask and many of it's plugins require a number of system variables to be set
# This file is used to define those variables and are loaded in app.py.

# App Config
# Secret Key is required for the CSRF tokens generated in our forms. It's a
# security feature for the forms.
SECRET_KEY = 'wefb292h3d9be#@@YEBBCE2NION32UDFEBUE2U202hfeu2onwdsjdf'

#Flask-mysql
MYSQL_HOST = 'localhost'
MYSQL_USER = 'tmstadmin'
MYSQL_PASSWORD = 'humedavid'
MYSQL_DB = 'tmst_db'
MYSQL_CURSORCLASS = 'DictCursor'

# flask-mail
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
#MAIL_DEBUG = True 
MAIL_USERNAME = "kutztms@gmail.com"
MAIL_PASSWORD = "C$C355KU!"
# USE THIS WHEN TESTING STUFF
MAIL_SUPPRESS_SEND = False

# Database Configs
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://tmstadmin:humedavid@localhost:3306/tmst_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
