#
# User Management Forms
# author: Mason Hoffman, Nathan Yost
# created: 2/13/2018
# latest: 2/13/2018
# purpose: Team B's form classes for WTForms
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, \
    BooleanField, FieldList, FormField, FileField, RadioField, SelectField
from wtforms.validators import InputRequired, EqualTo, Email, DataRequired


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    loginButton = SubmitField('Login')


# Change password Popup form
class ChangePassword(FlaskForm):
    email = StringField("Email", [InputRequired()])
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
    #person = StringField("Person being editted (ie: email)", [Email(), InputRequired()])
    #is_supervisor = BooleanField("Is Supervisor?")
    password = StringField("Password", [InputRequired()])
    phone = StringField("Phone")
    fname = StringField("First Name", [InputRequired()])
    mname = StringField("Middle Name")
    lname = StringField("Last Name", [InputRequired()])
    gender = StringField("Gender", [InputRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d")
    affiliation = StringField("Affiliation", [InputRequired()])
    ethnicity = StringField("Ethnicity", [InputRequired()])
    picture = StringField("Picture")
    submit = SubmitField("Submit Edit")


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
    title = StringField('Detailed Step Name:')
    stepText = StringField('Detailed Step Description:')
    image = FileField('Upload Image for Detailed Step:')

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
    title = StringField('Main Step Title:')
    requiredItem = StringField('Required Items:')
    stepText = StringField('Main Step Description:')
    audio = FileField('Upload Audio:')
    image = FileField('Upload Image:')
    video = FileField('Upload Video:')

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
    title = StringField('Task Name:', validators=[DataRequired()])
    description = StringField('Description:')
    image = FileField('Upload image for Task:')

    main_steps = FieldList(FormField(MainStep), min_entries=0)
    add_main_step = SubmitField('+ Main Step')
    # Displays in library only for self AND disabled
    save_as_draft = SubmitField('Save to Library as Draft')
    # Displays in library for everyone AND enables it for user assignment
    publish = SubmitField('Save to Library and Publish')
    # enable/disable button for user assignment
    toggle_enabled = SubmitField('Enable/Disable Task')
    # "Archive" button to re-hide it from everyone
    toggle_activation = SubmitField('Activate/Deactivate Task')

    @staticmethod
    def process_data(data):
        return data


class UserAssignmentForm(FlaskForm):
    assigned_users = SelectField('Select user...', choices=[])
    assign_task_button = SubmitField('Assign Task')
    view_assigned_tasks_button = SubmitField('View Assigned Tasks')
    assign_button = SubmitField('Assign')
    remove_button = SubmitField('Remove')

    @staticmethod
    def process_data(data):
        return data
        
# Yocums create survey form 3/6/18 4:53pm

class SurveyQuestion(FlaskForm):
	stock_question = RadioField ("Did You Have Fun?", choices = [("1","1"),("2","2"),("3","3"),("4","4"),("5","5")])
	delete_a_question = SubmitField("Delete Question")
	rearrange_a_question = SubmitField("Rearrange Question")

class CreateASurvey(FlaskForm):
	save = SubmitField("Save")
	delete = SubmitField("Delete")  
	activate_a_survey = BooleanField("Activate")
	assign_a_survey = BooleanField("Assign")
	questions = FieldList(FormField(SurveyQuestion), min_entries=2)
	add_question = SubmitField("Add a New Question")
        
        