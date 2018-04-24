import os
from flask import render_template, request, jsonify, redirect,url_for, flash, session, json

from app import app
from Forms.forms import CreateAccount,CreateSupervisor, EditSenior, EditSuper, AddUser, AssignUser, \
    CreateTaskForm, ChangePassword, LoginForm, CreateUser, CreateASurvey, TaskAssignmentForm
from helper_methods import UserMgmt,  TaskHelper, Update, Login, Library, TaskAssignmentHelper, Api, Surveys, Reports
from database import *
from flask_login import current_user, login_required, logout_user
from Forms.models import Task, User, Supervisor, Request, SurveyForm, SurveyQuest, SurveyResult,SurveyAssigned
from datetime import datetime, timedelta
from flask_weasyprint import HTML, render_pdf
import weasyprint
from flask_mail import Message
import pygal

@app.route('/', methods=['GET'])
def index():
    return redirect("login", code=302)

@app.route('/api/user/login', methods=['POST'])
def api_login():
    '''
        Function:   user_login
        Purpose:    Allows Front End to login
        Author:     Patrick Earl
    '''
    user = request.form.get('username')
    password = request.form.get('password')
    success = Api.userLogin(user, password)
    if success is False:
        return jsonify({'d': 'sign in failure'})
    else:
        return jsonify({'d': "sign in success"})

@app.route('/api/user/GetByUser/<uname>', methods=['GET'])
def api_getbyuser(uname):
    r = Api.getByUser(uname)
    return jsonify([r])


# For sprint 2

@app.route("/api/user/GetTaskDetails/<taskid>", methods=['GET'])
def getTaskDetails(taskid):
    results = Api.getTaskDetails(taskid)
    return jsonify(results)

@app.route("/api/user/GetAllCompletedSteps/<uname>/<taskid>")
def getAllCompletedSteps(uname, taskid):
    results = Api.getAllCompletedSteps(uname, taskid)
    return jsonify(results)

@app.route("/api/user/PostMainStepCompleted", methods=['POST'])
def postMainStepCompleted():
    d = json.loads(request.data)
    # print(d['MainStepName'])
    results = Api.postMainStepCompleted(d['TaskID'],d['MainStepID'],d['AssignedUser'],d['TotalDetailedStepsUsed'],d['TotalTime'], request.remote_addr)
    return jsonify(results)

@app.route("/api/user/PostTaskCompleted", methods=['POST'])
def postTaskCompleted():
    d = json.loads(request.data)
    # print(d['TaskID'], d['AssignedUser'])
    results = Api.postTaskCompleted(d['TaskID'],d['AssignedUser'],d['TotalTime'],d['TotalDetailedStepsUsed'])
    return jsonify(results)
                
@app.route("/api/user/GetAllCompletedTasksByUser/<uname>", methods=['GET'])
def getAllCompletedTasksByUser(uname):
    results = Api.getAllCompletedTasksByUser(uname)
    return jsonify(results)

@app.route("/api/user/PostLoggedInIp", methods=['POST'])
def postLoggedInIp():
    ip = request.form.get('IpAddress')
    signIn = request.form.get('SignedIn')
    user = request.form.get('Username')
    results = Api.postLoggedInIp(ip,user,signIn)
    return jsonify(results)
# end URL dispatching for iPaws

# supervisor dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if(current_user.role=="supervisor"):
        # query all the information
        tasks  = Task.query.filter_by(supervisorID=current_user.supervisorID).all()
        users  = User.query.filter_by(supervisorID=current_user.supervisorID).all()
        return render_template('dashboard.html', task_list=tasks, user_list=users)
    if(current_user.role=="admin"):
        return redirect("adminDashboard", code=302)

# admin dash
@app.route("/adminDashboard/", methods=["GET", "POST"])
@login_required
def admin_dash():
    if(current_user.role=="supervisor"):
        return redirect("dashboard", code=302)
    if(current_user.role=="admin"):
        supervisors  = Supervisor.query.all()
        users  = User.query.all()
        return render_template("adminDashboard.html", supervisor_list=supervisors, user_list=users)

# survey creation
@app.route("/surveyCreation/", methods=["GET", "POST"])
@app.route("/surveyCreation/<arguments>", methods=["GET", "POST"])
@login_required
def surveyCreation(arguments=None):
    return Surveys.handle_surveyCreation(arguments)
    
# survey results
@app.route("/survey_results/", methods=["GET", "POST"])
@login_required
def survey_results():
    return Surveys.handle_survey_results()

@app.route("/displayResult", methods=["GET", "POST"])
@app.route("/displayResult/", methods=["GET", "POST"])
@app.route("/displayResult/<resultID>", methods=["GET", "POST"])
@login_required
def displayResult(resultID=None):
    return Surveys.handle_displayResult(resultID)
    
# display survey to user
# https://tmst.kutztown.edu:5002/userSurvey/test.com/654706
@app.route("/userSurvey/<username>/<taskID>", methods=["GET","POST"])
def userSurvey(username=None,taskID=None):
    return Surveys.handle_userSurvey(username,taskID)
    
# survey management
@app.route("/surveys/", methods=["GET", "POST"])
@app.route('/surveys/<arguments>/<formID>', methods=["GET"])
@login_required
def surveys(arguments=None,formID=None):
   return Surveys.handle_surveys(arguments,formID)

#*****************This is where the admin reports page is****
#This page was just made so Team UI could see and design the page.
#the app route is correct, reports.html is the name of the page.
# Taken from UI sprint
#(Admin) Reports Page
@app.route('/reports', methods=['GET'])
@app.route('/reports/<arguments>', methods=['GET'])
@login_required
def reports(arguments=None):
    return Reports.handle_reports(arguments)
    
@app.route('/pdf', methods=['GET'])
@app.route('/pdf/<arguments>', methods=['GET'])
@login_required
def pdf(arguments=None):
    return Reports.handle_pdf(arguments)

@app.route('/graph', methods=['GET'])
@app.route('/graph/<arguments>', methods=['GET'])
@login_required
def graph(arguments=None):
    return Reports.handle_graph(arguments)


@app.route('/email', methods=['GET'])
@app.route('/email/<arguments>', methods=['GET'])
@login_required
def email(arguments=None):
    return Reports.handle_email(arguments)
        
# link to the logout page to log an account out
@app.route('/logout', methods=['GET'])
@login_required
def logout_account():
    logout_user()
    session.pop('roles',None)
    return redirect("login", code=302)

# supervisor account
@app.route('/supervisor_account', methods=['GET', "POST"])
@app.route('/supervisor_account/<superID>', methods=['GET', "POST"])
@login_required
def supervisor_account(superID=None):
    if superID:
        supervisor = Supervisor.query.filter_by(supervisorID=superID).first()
    else:
        supervisor = Supervisor.query.filter_by(supervisorID=current_user.supervisorID).first()
    eUser = EditSuper()
    if eUser.validate_on_submit():
        UserMgmt.edit_supervisor(eUser, supervisor)
        return dashboard()
    UserMgmt.populateFieldsSupervisor(supervisor, eUser)
    return render_template('supervisor_account.html',EditUser=eUser, ErrorItems=eUser.errors.items())

#User Account
@app.route("/user_account/<user_ID>", methods=["GET", "POST"])
@login_required
def user_account(user_ID=None):
    if user_ID == None:
        print("no user ID passed to the page")
        return dashboard() # there was no userID passed to the user account page
    user = User.query.filter_by(userID=user_ID).first()
    eUser = EditSenior()
   
    if eUser.validate_on_submit():
        UserMgmt.edit_user(eUser, user)
        return dashboard()
    UserMgmt.populateFieldsUser(user, eUser)
    return render_template("userAccount.html", EditUser=eUser, User=user)
    
# login page
@app.route('/login', methods=['POST','GET'])
def login():
    lForm = LoginForm()
    if lForm.validate_on_submit():
        if Login.verifyMain(lForm.email.data,lForm.password.data):
            print("login sucessful")
            return redirect("dashboard", code=302)
        else:
            print("login failed, try again")
    # form submission was invalid
    if lForm.errors:
        for error_field, error_message in lForm.errors.items():
            print("Field : {field}; error : {error}".format(field=error_field, error=error_message))
    return render_template('login.html', form=lForm)


# update password page (currently a page, maybe you will want a popup... whatever)
@app.route('/update', methods=['POST','GET'])
def update():
    uForm = ChangePassword()
    if uForm.validate_on_submit():
        Update.setPassword(uForm.email.data,uForm.password.data)
        # lets go back to the login page to test if the new password works
        return render_template('login.html', form=LoginForm())

    # if form submission was invalid for some reason
    if uForm.errors:
        for error_field, error_message in uForm.errors.items():
            print("Field : {field}; error : {error}".format(field=error_field, error=error_message))
    # the page has not been submitted before so lets render the form instead
    return render_template('update.html', form=uForm)


#create supervisor page
@app.route("/create_supervisor/", methods=["GET", "POST"])
@login_required
def create_supervisor():
    form = CreateSupervisor()
    if form.validate_on_submit():
        UserMgmt.create_supervisor(form)
        return dashboard()
    return render_template("createSupervisorTest.html", form=form)


#create user page
@app.route("/create_user/", methods=["GET", "POST"])
@login_required
def create_user():
    form = CreateUser()
    if form.validate_on_submit():
        email = form.email.data
        UserMgmt.create_user(form)
        user = User.query.filter_by(email=email).first()
        return user_account(user.userID)
    return render_template("createUser.html", form=form)


# library
@app.route("/library/", methods=["GET", "POST"])
@app.route("/library/<arguments>", methods=["GET", "POST"])
@login_required
def library(arguments=None):
    tasks = []

    # Create form(s).
    search_form = Library.SearchForm()

    # Get complete list of all supervisors for dropdown.
    allsupervisors = Library.get_supervisors()

    # selected_id is the current supervisor selected or the current_user logged
    # in if no supervisor was selected from dropdown
    selected_id = current_user.supervisorID
    img = {}
    
    # Check if the form is validated, or whether it was submitted.
    if search_form.validate_on_submit():
        # Uses the search form data to look for tasks that match.
        keyword = search_form.search.data
        tasks = []
        if arguments is not None:
            sort = arguments.split(':')[0]
            if sort == "alpha":
                tasks = Library.sort_alphabetically(Library.search(keyword))
            elif sort == "alpha-rev":
                tasks = Library.sort_alphabetically(Library.search(keyword), reverse=True)
        else:
            tasks = Library.sort_alphabetically(Library.search(keyword))
    else:
        # Check if arguments were passed to page or not.
        if arguments is not None:
            # Arguments are passed in the following format: sort:supervisor_id
            sort, supervisor_id = arguments.split(':')

            # If the tasks were already sorted based on supervisor, keep those
            # tasks and just sort them.
            if supervisor_id != "":
                selected_id = supervisor_id

            # Check sort options
            if sort == "alpha":
                tasks = Library.sort_alphabetically(Library.get_tasks(supervisor_id))
            if sort == "alpha-rev":
                tasks = Library.sort_alphabetically(Library.get_tasks(supervisor_id), reverse=True)
            else: # Default option is to sort alphabetically
                tasks = Library.sort_alphabetically(Library.get_tasks(supervisor_id))
        else:
            tasks = Library.sort_alphabetically(Library.get_tasks(current_user.supervisorID))
        
        # determine the image to pull
    for t in tasks:
            #t.image = Api.getPathForTaskImage(t.taskID)
        img[t.taskID] = Api.getPathForTaskImage(t.taskID)
    return render_template("library.html", tasks=tasks, search=search_form, supervisors=allsupervisors, selectedID=selected_id, img=img)


    
#senior assignment
@app.route("/senior_assignment/", methods=["GET", "POST"])
@app.route("/senior_assignment/<arguments>", methods=["GET", "POST"])
@login_required
def senior_assignment(arguments=None):
    # Get all supervisors
    supervisors = Supervisor.query.all()

    # Get all unassigned users
    users = UserMgmt.get_unassigned()

    if arguments is not None:
        superID, userID = [int(x) for x in arguments.split(':')]
        errors = None
        if superID != -1 and userID != -1:
            errors = UserMgmt.assign_user(superID, userID)
        return render_template("senior_assignment.html", supervisors=supervisors, superID=superID, userID=userID, users=users, errors=errors)
    return render_template("senior_assignment.html", supervisors=supervisors, superID=None, userID=-1, users=users, errors=None)


# user assignment
@app.route('/task_assignment/', methods=["GET", "POST"])
@login_required
def task_assignment():
    """
    Authors: David Schaeffer, March 2018 <dscha959@live.kutztown.edu>
    Handles logic and rendering of user_assignment page
    :return: rendered user_assignment page
    """
    form = TaskAssignmentForm(request.form)
    if current_user.role == "supervisor":
        users = UserMgmt.get_supervisor_users(current_user.email)
    else:
        users = User.query.all()
    # WARNING: If the user doesn't have a first name and a last name in the DB,
    # such as, say, the user was entered for testing purposes,
    # the concatenation of their first name and last name will crash the app.
    user_choices = [(user.userID, str(user.fname) + ' ' + str(user.lname)) for user in
                    users]
    user_choices.append(('all_users', 'All Users'))
    form.assigned_users.choices = user_choices
    if form.assign_task_button.data:
        task_choices = [(task.taskID, task.title) for task
                        in TaskAssignmentHelper.get_assignable_tasks(
                current_user.supervisorID)]
        form.tasks.choices = task_choices
        return render_template("task_assignment.html", form=form)
    if form.view_assigned_tasks_button.data:
        if form.assigned_users.data == 'all_users':
            # Do nothing, because there's no real way to display a list of
            # tasks that happen to assigned to every single one of the users
            # under the supervisor without making a ton of calls.
            pass
        task_choices = [(task.taskID, task.title) for task
                        in TaskAssignmentHelper.get_tasks_assigned_to_user(
                form.assigned_users.data, current_user.supervisorID)]
        form.tasks.choices = task_choices
        return render_template("task_assignment.html", form=form)
    if form.assign_button.data:
        if form.assigned_users.data == 'all_users':
            TaskAssignmentHelper.assign_to_all_users(current_user.supervisorID,
                                                     form.tasks.data)
            flash('Task has been assigned to all users.', 'info')
            return render_template("task_assignment.html", form=form)
        TaskAssignmentHelper.assign_task(form.assigned_users.data,
                                         form.tasks.data,
                                         current_user.supervisorID)
        flash('Task has been assigned to user.', 'info')
        return render_template("task_assignment.html", form=form)
    if form.remove_button.data:
        if form.assigned_users.data == 'all_users':
            flash('Task has been removed from all users.', 'info')
            TaskAssignmentHelper.remove_from_all_users(
                current_user.supervisorID,
                form.tasks.data)
            return render_template("task_assignment.html", form=form)
        flash('Task has been removed from user.', 'info')
        TaskAssignmentHelper.delete_request(form.assigned_users.data,
                                            form.tasks.data)
        return render_template("task_assignment.html", form=form)
    return render_template("task_assignment.html", form=form)
    
# create task
@app.route('/create_task/', methods=['GET', 'POST'])
@login_required
def create_task():
    """
    Author: David Schaeffer March 2018, <dscha959@live.kutztown.edu>
    Called when a supervisor wishes to create a new task from scratch.
    :return: the rendered task creation page
    """
    if request.method == 'GET':
        form = CreateTaskForm()
        return render_template('create_task.html', form=form)
    # Below code runs on POST requests.
    form = CreateTaskForm(request.form)

    # HERE BE SPEECH!
    # if form.voice_button_title.data:
    #     form.title.process_data(TaskHelper.get_audio_transcript())
    #     return render_template('create_task.html', form=form)
    # if form.voice_button_description.data:
    #     form.description.process_data(TaskHelper.get_audio_transcript())
    #     return render_template('create_task.html', form=form)
    # Now on to the boring stuff
    if form.save.data:
        """Save task."""
        new_task = TaskHelper.create_task(form,request.files)
        flash('Your task was successfully saved!', 'info')
        return redirect(url_for('edit_task', task_id=new_task.taskID))
    if form.add_main_step.data:
        """Add new main step."""
        form.main_steps.append_entry()
        return render_template('create_task.html', form=form)
    for i, main_step in enumerate(form.main_steps):
        # Handling of main step deletion as well as detailed steps
        # addition and deletion which reside inside main steps
        # if main_step.voice_button_title.data:
        #     main_step.title.process_data(TaskHelper.get_audio_transcript())
        # if main_step.voice_button_requiredItems.data:
        #     main_step.requiredItems.process_data(TaskHelper.get_audio_transcript())
        # if main_step.voice_button_stepText.data:
        #     main_step.stepText.process_data(TaskHelper.get_audio_transcript())
        if main_step.main_step_removal.data:
            """User removes a main step."""
            form.main_steps.entries.pop(i)
            return render_template('create_task.html', form=form)
        if main_step.add_detailed_step.data:
            """User adds detailed step to a main step."""
            main_step.detailed_steps.append_entry()
            return render_template('create_task.html', form=form)
        for j, detailed_step in enumerate(main_step.detailed_steps):
            # if detailed_step.voice_button_title.data:
            #     detailed_step.title.process_data(TaskHelper.get_audio_transcript())
            # if detailed_step.voice_button_stepText.data:
            #     detailed_step.stepText.process_data(TaskHelper.get_audio_transcript())
            if detailed_step.detailed_step_removal.data:
                main_step.detailed_steps.entries.pop(j)
                return render_template('create_task.html', form=form)
    return render_template('create_task.html', form=form)


@app.route('/edit_task/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def edit_task(task_id=None):
    """
    Author: David Schaeffer March 2018, <dscha959@live.kutztown.edu>
    Called when a supervisor wishes to edit an existing task.
    :return: the rendered task editing page
    """
    if task_id is not None:
        print('TASK ID: ', task_id)
        task_image = None
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'T={}'.format(task_id)), 'rb') as task_image:
            task_image = task_image.read()
        main_step_ids = []  # Contains tuples: (step number, step id)
        detailed_step_ids = []  # Contains dict of tuples: 'main step number': (detailed step number, step id)
        for i, main_step in enumerate(TaskHelper.get_main_steps_for_task(task_id)):
            main_step_ids.append((i+1, main_step.mainStepID))
            for j, detailed_step in enumerate(TaskHelper.get_detailed_steps_for_main_step(main_step.mainStepID)):
                detailed_step_ids.append({i+1: (j+1, detailed_step.detailedStepID)})
        form = TaskHelper.get_form_filled_with_task(task_id)
        return render_template('edit_task.html', form=form,
                               task_image=task_image,
                               main_step_ids=main_step_ids,
                               detailed_step_ids=detailed_step_ids)
    # Below code runs on POST requests.
    form = CreateTaskForm(request.form)

    if form.save.data:
        """Save task as draft."""
        task = TaskHelper.create_task(form, request.files)
        flash('Your task was successfully saved!', 'info')
        return render_template('edit_task.html', form=form, task_id=task.taskID)
    if form.add_main_step.data:
        """Add new main step."""
        form.main_steps.append_entry()
        return render_template('edit_task.html', form=form)
    for i, main_step in enumerate(form.main_steps):
        # Handling of main step deletion as well as detailed steps
        # addition and deletion which reside inside main steps
        if main_step.main_step_removal.data:
            """User removes a main step."""
            form.main_steps.entries.pop(i)
            return render_template('edit_task.html', form=form)
        if main_step.add_detailed_step.data:
            """User adds detailed step to a main step."""
            main_step.detailed_steps.append_entry()
            return render_template('edit_task.html', form=form)
        for j, detailed_step in enumerate(main_step.detailed_steps):
            if detailed_step.detailed_step_removal.data:
                main_step.detailed_steps.entries.pop(j)
                return render_template('edit_task.html', form=form)
    return render_template('edit_task.html', form=form)


