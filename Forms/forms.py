#
# User Management Forms
# author: Mason Hoffman, Nathan Yost
# created: 2/13/2018
# latest: 2/13/2018
# purpose: Team B's form classes for WTForms
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, \
    BooleanField, FieldList, FormField, FileField
from wtforms.validators import InputRequired, EqualTo, Email, DataRequired


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

# need to get rid of this class. needed it for dashboard ->
# sorry Nate
class CreateAccount(FlaskForm):
    email = StringField('Email', [Email(), InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create New Account')


# Requirement 27
class CreateSupervisor(FlaskForm):
    email = StringField('Email', [Email(), InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create New Account')

# Requirement 28
class CreateUser(FlaskForm):
    """Account creation form. Email validation currently uses a crude RegEx.
    Update to confirmation email in the future"""
    email = StringField('Email', [Email(), InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
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


class DetailedStep(FlaskForm):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    """
    detailed_step_title = StringField('Detailed Step Name:')
    detailed_step_description = StringField('Detailed Step Description:')
    detailed_step_image = FileField('Upload Image for Detailed Step:')
    detailed_step_removal = SubmitField('- Detailed Step')
    detailed_step_up = SubmitField('↑')
    detailed_step_down = SubmitField('↓')

    @staticmethod
    def process_data(data):
        return data


class MainStep(FlaskForm):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    """
    main_step_title = StringField('Main Step Title:')
    main_step_description = StringField('Main Step Description:')
    main_step_audio = FileField('Upload Audio:')
    main_step_image = FileField('Upload Image:')
    main_step_video = FileField('Upload Video:')
    detailed_steps = FieldList(FormField(DetailedStep), min_entries=0)
    add_detailed_step = SubmitField('+ Detailed Step')
    main_step_removal = SubmitField('- Main Step')
    main_step_up = SubmitField('Move Main Step ↑')
    main_step_down = SubmitField('Move Main Step ↓')

    @staticmethod
    def process_data(data):
        return data


class CreateTaskForm(FlaskForm):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    """
    task_name = StringField('Task Name:', validators=[DataRequired()])
    task_description = StringField('Description:')
    image = FileField('Upload image for Task:')
    required_items = StringField('Items Required for this Task:')
    main_step = FieldList(FormField(MainStep), min_entries=0)
    add_main_step = SubmitField('+ Main Step')
    save_as_draft = SubmitField('Save to Library as Draft')
    publish = SubmitField('Save to Library and Publish')

    @staticmethod
    def process_data(data):
        return data
