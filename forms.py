"""
Using flask-wtforms allows you to define forms as class objects. This makes
them easier to handle and implement.
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FieldList, StringField


class CreateTaskForm(FlaskForm):
    task_name = StringField('Task Name')
