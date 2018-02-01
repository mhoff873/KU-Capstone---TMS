# Flask and many of it's plugins require a number of system variables to be set
# This file is used to define those variables and are loaded in app.py.

# App Config
# Secret Key is required for the CSRF tokens generated in our forms. It's a
# security feature for the forms.
SECRET_KEY = 'wefb292h3d9be#@@YEBBCE2NION32UDFEBUE2U202hfeu2onwdsjdf'

# Database Configs
# See: http://flask-mysqldb.readthedocs.io/en/latest/
MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = ''
MYSQL_PORT = ''
MYSQL_CONNECT_TIMEOUT = 20
