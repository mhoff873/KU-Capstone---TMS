"""
Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
"""
import speech_recognition as speech_rec
from flask_login import current_user
from werkzeug.utils import secure_filename

from Forms.forms import CreateTaskForm
from Forms.models import Task, MainStep, DetailedStep, Supervisor, Admin, \
    Keyword
from database import db


# Req 1
def create_task(form, files):
    """
    Author: David Schaeffer, February 2018 <dscha959@live.kutztown.edu>
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
    except Exception as e:
        print(e)
        db.session.commit()
    for i, main_step in enumerate(form.main_steps.entries):
        existing_main_step = MainStep.query.filter_by(title=main_step.title.data).first()
        if existing_main_step is not None:
            new_main_step = existing_main_step
        else:
            new_main_step = MainStep(main_step.title.data)
        new_main_step.taskID = new_task.taskID
        new_main_step.requiredInfo = main_step.requiredItem.data
        new_main_step.stepText = main_step.stepText.data
        new_main_step.listOrder = i+1
        new_main_step.image = main_step.image.data
        # if main_step.image.data in files:
        #     print('Image found in request files.')
        #     print(files)
        #     print(main_step.image.data)
        try:
            db.session.add(new_main_step)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.commit()
        for j, detailed_step in enumerate(main_step.detailed_steps.entries):
            existing_detailed_step = DetailedStep.query.filter_by(title=detailed_step.title.data).first()
            if existing_detailed_step is not None:
                new_detailed_step = existing_detailed_step
            else:
                new_detailed_step = DetailedStep(detailed_step.title.data)
            new_detailed_step.mainStepID = new_main_step.mainStepID
            new_detailed_step.stepText = detailed_step.stepText.data
            new_detailed_step.listOrder = i+1
            new_detailed_step.image = detailed_step.image.data
            try:
                db.session.add(new_detailed_step)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.commit()
    keywords = form.keywords.data.split(',')
    print('Keywords: ', keywords)
    for keyword in keywords:
        new_keyword = Keyword(new_task.taskID, keyword)
        db.session.add(new_keyword)
    db.session.commit()
    return new_task


def get_task(task_id: int):
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    :param task_id: ID of task we will be displaying
    :return: A completed task form to be edited by user
    """
    task = Task.query.filter_by(taskID=task_id).first()
    form = CreateTaskForm(obj=task)
    main_steps = MainStep.query.filter_by(taskID=task_id).all()
    for i, main_step in enumerate(main_steps):
        form.main_steps.append_entry(main_step)
        detailed_steps = DetailedStep.query.filter_by(mainStepID=main_step.mainStepID).all()
        for detailed_step in detailed_steps:
            form.main_steps[i].detailed_steps.append_entry(detailed_step)
    keywords_for_task = Keyword.query.filter_by(taskID=task_id).all()
    keywords_string = ''
    for word in keywords_for_task:
        keywords_string += word.word + ', '
    form.keywords.process_data(keywords_string)
    print(form.data)
    return form


def get_audio_transcript():
    """
    Author: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    Gets the audio input from the user's microphone, converts it to text
    :return: The transcript string or empty string if there was an error.
    """
    recognizer = speech_rec.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.pause_threshold = 1.0
    with speech_rec.Microphone() as source:
        print('Recording audio')
        audio = recognizer.listen(source)
    print('No longer recording.')
    try:
        transcript = recognizer.recognize_google(audio)
        print('Google thinks you said: ', transcript)
        return transcript
    except speech_rec.UnknownValueError:
        print('Could not understand you.')
    except speech_rec.RequestError as e:
        print('Could not get results from Google: ', e)
    return ''
