"""
Using flask-wtforms allows you to define forms as class objects. This makes
them easier to handle and implement.
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FieldList, StringField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    task_name = StringField('Task Name:', validators=[DataRequired()])
    required_items = StringField('Items Required for this Task:')

    # Main Steps
    main_step_title = StringField('Main Step Name:')
    main_step_description = StringField('Main Step Description:')
    main_step_image = FileField('Upload Image for Main Step:')
    main_step_media = FileField('Upload Audio/Video:')

    # Detailed Steps
    detailed_step_title = StringField('Detailed Step Name:')
    detailed_step_description = StringField('Detailed Step Description:')
