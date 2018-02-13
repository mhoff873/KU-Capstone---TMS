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


app = Flask(__name__)
app.config.from_object('config')
