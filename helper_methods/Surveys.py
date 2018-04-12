# ************************************************************/
# API Functions
# Author: Tyler Lance, David Yocum
# Created: 04/12/2018
# Updated: 04/12/2018
# Purpose: Functions relating to surveys
# Version: Python Version 3.6
# ************************************************************/

from flask import render_template, request, redirect,url_for, flash, session
from Forms.forms import CreateASurvey
from helper_methods import Api
from database import *
from flask_login import current_user, login_required, logout_user
from Forms.models import Task, User, Supervisor, Request, SurveyForm, SurveyQuest, SurveyResult,SurveyAssigned
from datetime import datetime, timedelta
from wtforms.validators import InputRequired, EqualTo, Email, DataRequired

def handle_surveys(arguments=None,formID=None):
    """
    Description: handle the rendering of the survey management page for the users
    Parameters: arguments - (string) depending on the user option clicked on
                formID - (int) id of the survey, its form
    Return Value: rendered form for the user
    Author: Tyler Lance
    """
    # check if archive survey
    if arguments == 'A':
        if Api.archiveSurvey(formID,0):
	        flash('The survey was successfully archived.', 'success')
    # check if unarchive survey
    elif arguments == 'U':
        if Api.archiveSurvey(formID,1):
            flash('The survey was successfully unarchived.', 'success')
    # check if edit survey
    elif arguments == 'E':
        # redirect to the survey creation form and pass the formID so it can generate the form
        return redirect(url_for("surveyCreation", arguments=formID))
    # check if delete survey
    elif arguments == 'D':
        Api.deleteSurvey(formID)
        flash('The survey was successfully deleted.', 'success')
    # assign survey to task then
    if arguments is not None and arguments.isdigit():
        Api.updateTask(arguments,formID,current_user.supervisorID)
        flash('The task was successfully assigned to the survey.', 'success')
    surveys = SurveyForm.query.all() # the entire result table. get the formID and the name
    survey_list=[]
    task = Api.getCreatedTasks(current_user.supervisorID)
    for s in surveys:
        survey_list.append({'formId':s.formID,'surveyTitle':s.formTitle,'surveyDesc':s.description,'isActive':s.isActive,'task':Api.getAssignedTask(s.formID)})
    return render_template("surveyManagement.html",survey_list=survey_list, task=task)

def handle_survey_results():
    """
    Description: creates the survey result form for all surveys
    Return Value: the rendered html file for the survey results
    Author: Tyler Lance
    """
    return render_template("surveyResults.html",data=Api.getResultsByID(current_user.supervisorID))
    
def handle_displayResult(resultID=None):
    """
    Description: creates the survey result form for an individual survey
    Parameters: resultID - (int) primary key of the result
    Return Value: the rendered html file for the survey results
    Author: Tyler Lance
    """
    return render_template("displayResult.html",data=Api.getResultsByID(current_user.supervisorID), resultID=resultID, question=Api.getResponsesByID(resultID))

def handle_surveyCreation(arguments=None):
    """
    Description: creates the survey form
    Return Value: the rendered html file for the survey being created
    Author: Tyler Lance
    """
    task = Api.getCreatedTasks(current_user.supervisorID)
    if request.method == 'GET':
        # generate form if no arguments were passed
        if arguments is None:
            form = CreateASurvey()
            return render_template("surveysTemp.html", form=form, task=task)
        # if argument was passed then generate the form using the formID given
        else:
            flash('Note: Saving your changes will create a new survey.', 'info')
            form = generateSurvey(arguments)
            return render_template("surveysTemp.html", form=form, task=task)
    else:
        form = CreateASurvey(request.form)
        # if the form was submitted and valid
        if form.save.data and form.validate():
            # verify title does not already exist in db
            if prepareSurveyCreationform(form):
                flash('Survey name already exists.', 'warning')
                return render_template("surveysTemp.html", form=form, task=task)
            else:
                return redirect(url_for('surveys'))
        # if the form was submitted but not valid
        elif form.save.data and not form.validate():
            # display what data was not entered to the user
            if 'title' in form.errors:
                flash('Please fill out the survey name.', 'warning')
            if 'description' in form.errors:
                flash('Please fill out the survey description.', 'warning')
            if 'questions' in form.errors:
                e = form.errors
                r = e['questions']
                if 'stock_question' in r[0]:
                    flash('Please fill out all questions.', 'warning')
                if 'responses' in r[0]:
                    flash('Please fill out all responses.', 'warning')
            return render_template("surveysTemp.html", form=form, task=task)
        if form.add_question.data:
            """Add question to form."""
            form.questions.append_entry()
            return render_template("surveysTemp.html", form=form, task=task)
        if form.delete.data:
            """Delete the current survey - just hyperlink to survey management page."""
            return redirect(url_for('surveys'))
        # process for question buttons
        for i, questions in enumerate(form.questions):
            if questions.delete_a_question.data:
                """Remove question from form."""
                form.questions.entries.pop(i)
                return render_template("surveysTemp.html", form=form, task=task)
            if questions.add_response.data:
                """Add multiple choice answer to question."""
                questions.responses.append_entry()
                return render_template("surveysTemp.html", form=form, task=task)
            for j, response in enumerate(questions.responses):
                if response.delete_response.data:
                    """Add multiple choice answer to question."""
                    questions.responses.entries.pop(j)
                    return render_template("surveysTemp.html", form=form, task=task)
    return render_template("surveysTemp.html", form=form, task=task)

def handle_userSurvey(username=None,taskID=None):
    """
    Description: hangle the rendering of the surveu page for the users
    Parameters: username - (string) email of the user
                taskID - (int) id of the task
    Return Value: rendered form for the user
    Author: Tyler Lance
    """
    userID = Api.getIdFromEmail(username)
    # if the form was posted then pull the form data
    if request.method == 'POST':
        form = CreateASurvey(request.form)
        # check if the data was submitted
        if form.save.data:
            flash("Your survey has been submitted.", "success")
            # pull the data from the form so that it can be prepared to be stored
            SQR = []
            for q in form.questions:
                dict = {}
                if q.questType.data == "multiple choice":
                    dict = {'questID': q.questID.data, 'response': request.form[q.questID.data]}
                # if it was an open ended question
                else:
                    dict = {'questID': q.questID.data, 'response': q.stock_question.data}
                SQR.append(dict)
            SR = {'userID': form.userID.data, 'formID': Api.getAssignedSurvey(form.taskID.data), 'name': Api.getNameFromID(form.userID.data), 'timeSpent': 0, 'email': "", 'ipAddr': request.remote_addr, 'ageGroup': 0, 'results': "", 'comments': ""}
            Api.postSurveyResults(SR, SQR)
            return render_template("userSurveyCompleted.html")
    form = CreateASurvey()
    form.userID.data = int(userID)
    form.taskID.data = int(taskID)
    # get survey for the task
    if Api.getAssignedSurvey(taskID) is not None:
        SF, SQ = Api.getSurvey(Api.getAssignedSurvey(taskID))
        # iterate over each question to append
        for q in SQ:
            questions = form.questions.append_entry()
            questions.questID.data = q['questID']
            questions.questType.data = q['questType']
            questions.stock_question.label = q['questText']
            questions.stock_question.data = ""
            if q['questType'] == 'multiple choice':
                for m in q['surveyMultQuest']:
                    responses = questions.responses.append_entry()
                    responses.response.label = m['questText']
    return render_template("userSurvey.html", form=form, task=Api.getTaskFromID(taskID))

def generateSurvey(formID):
    """
    Description: prepares the survey form to be displayed to the user
    Return Value: the data for the form
    Author: Tyler Lance
    """
    SF, SQ = Api.getSurvey(formID)
    form = CreateASurvey()
    form.title.data = SF['formTitle']
    form.description.data = SF['description']
    if SF['isActive'] == 0:
        form.activate_a_survey.checked = False
    # iterate over each question to append
    for q in SQ:
        questions = form.questions.append_entry()
        questions.stock_question.data = q['questText']
        if q['isActive'] == 0:
            questions.isActive.checked = False
        if q['questType'] == 'multiple choice':
            for m in q['surveyMultQuest']:
                responses = questions.responses.append_entry()
                responses.response.data = m['questText']
    return form
    
def prepareSurveyCreationform(form):
    """
    Description: handles the pulling of data from the form and calling of the api.postSurveyForm method
    Return Value: T/F whether the data was successfully inserted
    Author: Tyler Lance
    """
    # handle the pulling of the data from the form and calling of the api method to store the form
    SF = {'supervisorID': current_user.supervisorID, 'formTitle': form.title.data, 'description': form.description.data, 'isActive': int(form.activate_a_survey.data != 0)}
    SQ = []
    for i,questions in enumerate(form.questions):
        dict = {}
        d = form.questions.entries
        # if the question is open ended because it has no constrained responses
        if len(d[i].responses.entries) == 0:
            dict = {'questType': "open ended", 'questText': d[i].stock_question.data, 'isActive': int(d[i].isActive.data != 0), 'questOrder': i+1, 'surveyMultQuest': ""}
        # else the question has radio buttons to be displayed
        else:
            # create initial dictionary for multiple choice questions
            dict = {'questType': "multiple choice", 'questText': d[i].stock_question.data, 'isActive': int(d[i].isActive.data != 0), 'questOrder': i+1}
            lstResponses = []
            # iterate over the responses
            for j, response in enumerate(questions.responses):
                dict2 = {}
                r = questions.responses.entries
                dict2 = {'questText': r[j].response.data, 'questOrder': j+1}
                lstResponses.append(dict2)
            dict['surveyMultQuest'] = lstResponses
        SQ.append(dict)
    return Api.postSurveyForm(SF,SQ)