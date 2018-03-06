"""
Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
"""

from Forms.models import Task, MainStep, DetailedStep
from database import db


# Req 1
def create_task(form):
    print(form.task_name.data)
    new_task = Task(form.task_name.data)
    new_task.description = form.task_description.data
    if form.save_as_draft.data:
        new_task.activated = 1
        new_task.published = 1
    else:
        new_task.activated = 0
        new_task.published = 0
    new_task.image = form.image.data

    for i, main_step in enumerate(form.main_step):
        print(main_step.data)
        print(main_step.main_step_title.data)
        new_main_step = MainStep(main_step.main_step_title.data)
        new_main_step.listOrder = i
        new_main_step.stepText = main_step.main_step_description.data
        new_main_step.image = main_step.main_step_image.data
        new_main_step.video = main_step.main_step_media.data
        for j, detailed_step in enumerate(main_step.detailed_steps):
            new_detailed_step = DetailedStep(detailed_step.detailed_step_title.data)
            new_detailed_step.stepText = detailed_step.detailed_step_description.data
            new_detailed_step.listOrder = j
    return


# Req 20
def toggle_enabled(taskID):
    pass


# Req 22
def toggle_published(taskID):
    pass
