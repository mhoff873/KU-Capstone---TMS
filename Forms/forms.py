#
# User Management Forms
# author: Mason Hoffman, Nathan Yost
# created: 2/13/2018
# latest: 2/13/2018
# purpose: Team B's form classes for WTForms
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, BooleanField, FieldList, FormField
from wtforms.validators import InputRequired, EqualTo, Email


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    loginButton = SubmitField('Login')


# Change password Popup form
class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

# Requirement 27, 28
class CreateAccount(FlaskForm):
    """Account creation form. Email validation currently uses a crude RegEx.
    Update to confirmation email in the future"""
    email = StringField('Email', [Email(), InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    is_supervisor = BooleanField("Is Supervisor?")
    submit = SubmitField('Create New Account')


# Requirement 29, 30
class EditUser(FlaskForm):
    person = StringField("Person being editted (ie: email)", [Email(), InputRequired()])
    is_supervisor = BooleanField("Is Supervisor?")
    phone = StringField("Phone")
    fname = StringField("First Name", [InputRequired()])
    mname = StringField("Middle Name")
    lname = StringField("Last Name", [InputRequired()])
    gender = StringField("Gender", [InputRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d")
    affiliation = StringField("Affiliation", [InputRequired()])
    ethnicity = StringField("Ethnicity", [InputRequired()])
    picture = StringField("Picture")
    submit = SubmitField("Edit user")


# Requirement 31
class AddUser(FlaskForm):
    supervisor_email = StringField("Supervisor", [InputRequired()])
    user = BooleanField("Assign User")
    submit = SubmitField("Add User(s)")


# Requirement 33
class AssignUser(FlaskForm):
    supervisor = StringField("Supervisor", [InputRequired()])
    user = StringField("User", [InputRequired()])
    submit = SubmitField("Re-assign user")
