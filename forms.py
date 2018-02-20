"""
Using flask-wtforms allows you to define forms as class objects. This makes
them easier to handle and implement.
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FieldList, StringField, FormField, \
    SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired


class DetailedStep(FlaskForm):
    detailed_step_title = StringField('Detailed Step Name:')
    detailed_step_description = StringField('Detailed Step Description:')


class MainStep(FlaskForm):
    main_step_title = StringField('Main Step Title:')
    main_step_description = StringField('Main Step Description:')
    main_step_image = FileField('Upload Image for Main Step:')
    main_step_media = FileField('Upload Audio/Video:')
    detailed_steps = FieldList(FormField(DetailedStep), min_entries=0)
    add_detailed_step = SubmitField('+ Detailed Step')


class CreateTaskForm(FlaskForm):
    task_name = StringField('Task Name:', validators=[DataRequired()])
    required_items = StringField('Items Required for this Task:')
    main_step = FieldList(FormField(MainStep), min_entries=1)
    add_main_step = SubmitField('+ Main Step')
    save_as_draft = SubmitField('Save as Draft')
    publish = SubmitField('Publish')
