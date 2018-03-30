"""
Note: Any libraries we will be using must be added to the requirements.txt
file. If you are using an IDE, it may prompt you to auto-add when it detects
libraries not listed in it. You can allow it to do so. If you wish to do it
manually, you must use the exact name used when installing via pip. If you are
unsure of what to do, just leave it be and I can populate the text.

A requirements.txt file when used for python applications allows for the bulk-
installation of all libraries the app uses. It is called via:
```$ pip install -r requirements.txt```
"""
from flask import Flask
from flask_cors import CORS # Needed for API requests
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object('config')
CORS(app)  # This allows Cross site access. Temp solution

# the toolbar is only enabled in debug mode:
app.debug = True
# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'nunyabusiness'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)