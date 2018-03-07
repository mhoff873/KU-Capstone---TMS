"""
Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
"""

from Models.task_models import Task, MainStep, DetailedStep
from database import db


# Req 1
def create_task(form):
    new_task = Task(form.title.data)
    new_task.supervisorID = 1
    new_task.description = form.description.data
    new_task.image = form.image.data
    # 0 = false, 1 = true
    if form.save_as_draft.data:
        new_task.published = 0
        new_task.activated = 0
    if form.publish.data:
        new_task.published = 1
        new_task.activated = 1
    if form.toggle_enabled.data:
        # query for curr status, set to opposite
        pass
    if form.toggle_activation.data:
        # query for curr status, set to opposite
        pass
    db.session.add(new_task)
    db.session.commit()
    print(new_task.taskID)
    # for i, main_step in enumerate(form.main_steps.entries):
    #     new_main_step = MainStep(main_step.title.data)
    #     # Need to query taskID
    #     new_main_step.taskID = 0
    #     new_main_step.stepText = main_step.stepText.data
    #     new_main_step.listOrder = i+1
    #     new_main_step.image = main_step.image.data
    #     for j, detailed_step in enumerate(main_step.detailed_steps.entries):
    #         new_detailed_step = DetailedStep(detailed_step.title.data)
    #         # Need to query mainStepID
    #         new_detailed_step.mainStepID = 0
    #         new_detailed_step.stepText = detailed_step.stepText.data
    #         new_detailed_step.listOrder = i+1
    #         new_detailed_step.image = detailed_step.image.data
    return new_task


# Req 20
def toggle_enabled(taskID):
    pass


# Req 22
def toggle_published(taskID):
    pass
