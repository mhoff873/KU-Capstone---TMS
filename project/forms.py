"""
Using flask-wtforms allows you to define forms as class objects. This makes
them easier to handle and implement.
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FieldList, StringField
from flask_wtf.file import FileField


class CreateTaskForm(FlaskForm):
    task_name = StringField('Task Name')

    #Main Steps
    main_step_image = FileField('Upload Image for Main Step')
    main_step_name = StringField('Title of Main Step')
    main_step_text = StringField('Main Step Description')
    main_step_items = StringField('Required Items')
    main_step_media = FileField('Upload Audio/Video')
