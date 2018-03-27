"""
Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
"""
from flask_login import current_user

from Forms.models import Task, MainStep, DetailedStep, Supervisor, Admin
from database import db


# Req 1
def create_task(form):
    """
    Extracts data from form entering it into our Task, MainStep, DetailedStep
    objects to be entered into the database.
    :param form: The CreateTaskForm.
    :return: The newly created task.
    """
    existing_task = Task.query.filter_by(title=form.title.data).first()
    if existing_task is not None:
        new_task = existing_task
    else:
        new_task = Task(form.title.data)
    if current_user.role == "supervisor":
        new_task.supervisorID = current_user.supervisorID
    elif current_user.role == "admin":
        new_task.supervisorID = current_user.adminID
    new_task.description = form.description.data
    new_task.image = form.image.data
    # 0 = false, 1 = true
    new_task.activated = form.activation.data
    new_task.published = form.publish.data
    try:  # try/excepts to catch IntegrityErrors, if it exists, we update.
        db.session.add(new_task)
        db.session.commit()
    except Exception:
        db.session.commit()
    for i, main_step in enumerate(form.main_steps.entries):
        new_main_step = MainStep(main_step.title.data)
        new_main_step.taskID = new_task.taskID
        new_main_step.stepText = main_step.stepText.data
        new_main_step.listOrder = i+1
        new_main_step.image = main_step.image.data
        try:
            db.session.add(new_main_step)
            db.session.commit()
        except Exception:
            db.session.commit()
        for j, detailed_step in enumerate(main_step.detailed_steps.entries):
            new_detailed_step = DetailedStep(detailed_step.title.data)
            new_detailed_step.mainStepID = new_main_step.taskID
            new_detailed_step.stepText = detailed_step.stepText.data
            new_detailed_step.listOrder = i+1
            new_detailed_step.image = detailed_step.image.data
            try:
                db.session.add(new_detailed_step)
                db.session.commit()
            except Exception:
                db.session.commit()
    return new_task
