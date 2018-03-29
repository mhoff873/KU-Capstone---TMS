# ************************************************************/
# Flask request routing to map URLs to code
# Author: Patrick Earl, Tyler Lance, <devs add names here>
# Created: 03/04/2018
# Updated: 03/27/2017
# Purpose: these @app.route map URLs called in the browser to code. each of these
#          routes pulls data from the url (get) or the form (post) and calls the
#          corresponding function in the Api.py file. then gets the results from
#          the function and format the results into a json string object or form.
# Version: Python Version 3.6
# ************************************************************/

from flask import render_template, request, jsonify, redirect, json, flash, url_for
from app import app
from Forms.forms import CreateAccount,CreateSupervisor, EditUser, AddUser, AssignUser, \
    CreateTaskForm, ChangePassword, LoginForm, CreateUser, CreateASurvey, UserAssignmentForm 
from helper_methods import UserMgmt,  TaskHelper, Update, Login, Library, UserAssignmentHelper, Api
from database import *
from flask_login import current_user, login_required, logout_user
from Forms.models import Task, User, Supervisor, Request, SurveyForm, SurveyQuest
from datetime import datetime, timedelta
from flask_weasyprint import HTML, render_pdf
import weasyprint
from flask_mail import Message

@app.route('/', methods=['GET'])
def index():
    return redirect("login", code=302)

@app.route('/api/user/login', methods=['POST'])
def api_login():
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
    results = Api.postMainStepCompleted(d['TaskID'],d['MainStepID'],d['AssignedUser'],d['TotalDetailedStepsUsed'],d['TotalTime'], request.remote_addr)
    return jsonify(results)

@app.route("/api/user/PostTaskCompleted", methods=['POST'])
def postTaskCompleted():
    d = json.loads(request.data)
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

# begin URL dispatching for TMS
#http://tmst.kutztown.edu:5004/api/user/PostSurveyResults/test
# this must be changed from get to post
@app.route("/api/user/PostSurveyResults/<test>", methods=['GET'])
def postSurveyResults(test):
    SR = ""
    SQR = ""
    # created the required dictionary & lists and pass to function
    results = Api.postSurveyResults(SR,SQR)
    return test
    
#http://tmst.kutztown.edu:5004/api/user/PostSurveyForm/test
# this must be changed from get to post
@app.route("/api/user/PostSurveyForm/<test>", methods=['GET'])
def postSurveyForm(test):
    SF = ""
    SQ = ""
    # created the required dictionary & lists and pass to function
    results = Api.postSurveyForm(SF,SQ)
    return test
    
#http://tmst.kutztown.edu:5004/api/user/GetAssignedUsers/4
@app.route("/api/user/GetAssignedUsers/<superID>", methods=['GET'])
def getAssignedUsers(superID):
    # created the required dictionary & lists and pass to function
    results = Api.getAssignedUsers(superID)
    return jsonify(results)

#http://tmst.kutztown.edu:5004/api/user/GetCompletedTasksByUsers/test
# change to post once you are ready to call function
@app.route("/api/user/GetCompletedTasksByUsers/<test>", methods=['GET'])
def getCompletedTasksByUsers(test):
    #d = json.loads(request.data)
    date = "2018-03-15"
    users = [1,4]
    # created the required dictionary & lists and pass to function
    results = Api.getCompletedTasksByUsers(date, users)
    return jsonify(results)
    
#http://tmst.kutztown.edu:5004/api/user/GetCompletedTasksByID/2018-03-01/654706
# change to post once you are ready to call function
@app.route("/api/user/GetCompletedTasksByID/<date>/<ID>", methods=['GET'])
def getCompletedTasksByID(date, ID):
    # created the required dictionary & lists and pass to function
    results = Api.getCompletedTasksByID(date, ID)
    return jsonify(results)
# end API calls

# Begin URL dispatching for TMS
# supervisor dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if(current_user.role=="supervisor"):
        # query all the information
        tasks  = Task.query.filter_by(supervisorID=current_user.supervisorID).all()
        users  = User.query.filter_by(supervisorID=current_user.supervisorID).all()
        requests = Request.query.filter_by(supervisorID=current_user.supervisorID).all()
        
        # form some data dictionaries for use later
        # supervisor_to_users={}
        # user_to_supervisor{}
        
        # mapping of user
        user_2_tasks={}
        task_2_users={}
        
        # a plain array of user and tasks IDs assigned to the Supervisor
        userIDs=[]
        taskIDs=[]
        
        for t in tasks:
            taskIDs.append(t.taskID)
            
        for u in users:
            userIDs.append(u.userID)
            
        if requests:
            for r in requests:
                # structuring ddata
                # { userID : [taskID,*] }
                if r.userID in user_2_tasks:
                    user_2_tasks[r.userID].append(r.taskID)
                else:
                    user_2_tasks[r.userID]=[r.taskID]
                # structuring data
                # { taskID : [userID,*] }
                if r.taskID in task_2_users:
                    task_2_users[r.taskID].append(r.userID)
                else:
                    task_2_users[r.taskID]=[r.userID]
        else:
            print("did not find any requests")
            
        #print(user_to_tasks)
        #print(task_to_users)
            # need a structure that is indexable by userID for the Request object

        return render_template('dashboard.html', task_list=tasks, user_list=users, request_list=requests, task_to_users=task_2_users, user_to_tasks=user_2_tasks,userID_list=userIDs,taskID_list=taskIDs)


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

# survey management
@app.route("/surveys/", methods=["GET", "POST"])
def surveys():
	form = CreateASurvey()
	questions = SurveyQuest.query.all()
	for q in questions:
	    print(q.questionText)
	if form.validate_on_submit():
	    return ("You have Submitted the Survey")
	return render_template("surveysTemp.html", form=form, form_questions = questions)

# link to the logout page to log an account out
@app.route('/logout', methods=['GET'])
#@login_required
def logout_account():
    logout_user()
    return redirect("login", code=302)

# Reports related stuff below
def generate_report(arguments=None):
    """
    Description: hangle the rendering and passing of the data to the reports page
    Parameters: None or Sorted Options
    Return Value: 
        - SupervisorID - The supervisor requesting the report
        - Users - The users that the report is for
        - lstTask - The list of tasks being returned
        - sortedBy - How the report is sorted (User or Time constraint)
    Author: Tyler Lance
    """
    # Chose which supervisor the report is being generated for
    #supervisorID = current_user.supervisorID
    supervisorID = current_user.supervisorID
    # pull the list of assigned users to the supervisor
    users =  Api.getAssignedUsers(supervisorID)
    # default date for the data if no date is passed
    date = "2000-01-01"
    # what the data is sorted by
    sortedBy = "Showing all entries by date"
    # pull userIDs from the user data
    lstUserIDs = [li['userID'] for li in users]
    # check if arguments were passed to the url
    if arguments is not None:
        sort = arguments.split(':')[0]
        data = arguments.split(':')[1]
        # check if userID was passed via url and that it wasnt all
        if sort == 'userid' and data != 'A':
            # empties the list of userids and adds in the passed one
            lstUserIDs = []
            lstUserIDs.append(int(data))
            sortedBy = "Showing entries for user: " + Api.getNameFromID(int(data))
        # check if date specified was passed to url
        elif sort == 'date':
            if data == 'M':
                date = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 30 days"
            elif data == 'W':
                date = str((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 7 days"
            elif data == 'D':
                date = str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last day"
    # get completed tasks by passing the list and date
    tasks = Api.getCompletedTasksByUsers(date, lstUserIDs)
    lstTask = []
    # create list containing dictionaries for each table row
    for li in tasks:
        for li2 in li["completedTasks"]:
            dictTask = {}
            dictTask["userID"]=Api.getNameFromID(li["userID"])
            dictTask["title"]=li2["title"]
            dictTask["totalTime"]=li2["totalTime"]
            dictTask["dateTimeCompleted"]=li2["dateTimeCompleted"]
            lstTask.append(dictTask)
    # sort the list by date so that the newest entries appear first
    lstTask = sorted(lstTask,key=lambda k: k['dateTimeCompleted'], reverse=True)
    return (supervisorID, users, lstTask, sortedBy)


#*****************This is where the admin reports page is****
#This page was just made so Team UI could see and design the page.
#the app route is correct, reports.html is the name of the page.
# Taken from UI sprint
#(Admin) Reports Page
@app.route('/reports', methods=['GET'])
@app.route('/reports/<arguments>', methods=['GET'])
@login_required
def reports(arguments=None):
    '''
        Description: Generate a report for the users assigned to the supervisor
        Parameters: None or the sorting options
        Return: A rendered template 
        Author: Tyler Lance
    '''
    (supervisorID, users, lstTask, sortedBy) = generate_report(arguments)
    return render_template('reports.html', supervisor=supervisorID, user=users, tasks=lstTask, constraint=sortedBy,  arguments=arguments)

@app.route('/pdf', methods=['GET'])
@app.route('/pdf/<arguments>', methods=['GET'])
@login_required
def pdf(arguments=None):
    """
    Description: Generates a report for all users assigned to the supervisor or for a specifed user
        Returns a pdf
    Parameters: None or the sorting options
    Return Value: pdf
    Author: Patrick Earl
    """
    (supervisorID, users, lstTask, sortedBy) = generate_report(arguments)

    html = render_template('pdf.html', supervisor=supervisorID, user=users, tasks=lstTask, constraint=sortedBy)
    return render_pdf(HTML(string=html))
   

@app.route('/email', methods=['GET'])
@app.route('/email/<arguments>', methods=['GET'])
@login_required
def email(arguments=None):
    """
    Description: 
    Parameters: none
    Return Value: 
    Author: 
    """
    subject = ""

    if arguments is None:
        subject = "Report for supervisor " + current_user.fname + " " + current_user.lname 
    
    msg = Message(subject,
                sender="kutztms@gmail.com",
                recipients=[current_user.email])

    (supervisorID, users, lstTask, sortedBy) = generate_report(arguments)
    html = render_template('pdf.html', supervisor=supervisorID, user=users, tasks=lstTask, constraint=sortedBy, arguments=arguments)
    pdf = weasyprint.HTML(string=html).write_pdf()
    msg.attach('report.pdf', 'application/pdf', pdf)
    msg.html = "<h3 style='text-align:center;'>Report is as an attached pdf</h3>"
    msg.html += "<span style='text-align:center;'>Time of generation: " + datetime.now().strftime('%m-%d-%Y %H:%M:%S') + "</span>"
    msg.html += "<p style='font-size:8px'>This is an automated message, this email is not monitored</p>"
    mail.send(msg)
    flash("Email send succesfully to " + current_user.email, 'success')
    return redirect(url_for('reports', arguments=arguments))
    
# supervisor account
@app.route('/supervisor_account', methods=['GET', "POST"])
@login_required
def supervisor_account():
    eUser = EditUser()
    if eUser.validate_on_submit():
        UserMgmt.edit_supervisor(eUser, current_user)
        return dashboard()
    return render_template('supervisor_account.html',EditUser=eUser)


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
        return user_account(email)
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
    return render_template("library.html", tasks=tasks, search=search_form, supervisors=allsupervisors, selectedID=selected_id)

# user assignment
@app.route('/user_assignment/', methods=["GET", "POST"])
@login_required
def user_assignment():
    form = UserAssignmentForm()
    #"""
    users = []
    tasks = []
    assign = False
    # not sure if this line works below
    if current_user.role == "supervisor":
        users = UserMgmt.get_supervisor_users(current_user.email)
    else:
        users = User.query.all()
    # on add_task button press, show list of tasks
    if form.add_task.data:
        # if current_user == Supervisor:
            # tasks = UserAssignmentHelper.get_assignable_tasks(current_user.supervisorID)
            # assign = True
        # else:
        tasks = UserAssignmentHelper.get_assignable_tasks(current_user.supervisorID)
        return render_template("user_assignment.html", assign=assign, users=users, tasks=tasks, form=form)
    #if form.show_history.data:
        # tasks = UserAssignmentHelper.get_tasks_assigned(users) # how to find which one?
    #if form.assign.data:
        # UserAssignmentHelper.assign_task(user,task,supervisor) # need to find user, task, and super
    #"""
    return render_template("user_assignment.html", assign=assign, users=users, tasks=tasks, form=form)
    

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

    if form.add_main_step.data:
        """Add new main step."""
        form.main_steps.append_entry()
        return render_template('create_task.html', form=form)
    if form.save_as_draft.data:
        """Save task as draft."""
        TaskHelper.create_task(form)
        return render_template('create_task.html', form=form)
    if form.publish.data:
        """Save task as published."""
        TaskHelper.create_task(form)
        return render_template('index.html')
    if form.toggle_enabled.data:
        """Toggles task enabled or not."""
        TaskHelper.toggle_enabled(form)
        return render_template('create_task.html', form=form)
    if form.toggle_activation.data:
        """Toggles task published or not."""
        TaskHelper.toggle_published(form)
        return render_template('create_task.html', form=form)
    for i, main_step in enumerate(form.main_steps):
        # Handling of main step deletion as well as detailed steps
        # addition and deletion which reside inside main steps
        if main_step.main_step_removal.data:
            """User removes a main step."""
            form.main_steps.entries.pop(i)
            return render_template('create_task.html', form=form)
        # if main_step.main_step_up.data and len(form.main_steps) > 1 and i > 0:
        #     """User moves a main step up.
        #     We do nothing if there is only a single main step or they are
        #     attempting to move the first step up."""
        #     new_order = form.main_steps.entries
        #     step_to_move = new_order.pop(i)
        #     new_order.insert(i-1, step_to_move)
        #     form.main_steps = new_order
        #     return render_template('create_task_draft.html', form=form)
        # if main_step.main_step_down.data and len(form.main_steps) > 1 \
        #         and i < len(form.main_steps)-1:
        #     """User moves a main step down.
        #     We do nothing if there is only a single main step or they are
        #     attempting to move the last step down."""
        #     new_order = form.main_steps.entries
        #     step_to_move = new_order.pop(i)
        #     if i+1 == len(form.main_steps):
        #         new_order.append(step_to_move)
        #     else:
        #         new_order.insert(i+1, step_to_move)
        #     form.main_steps = new_order
        #     return render_template('create_task_draft.html', form=form)
        # Handling of detailed step addition, deletion, and moving
        if main_step.add_detailed_step.data:
            """User adds detailed step to a main step."""
            main_step.detailed_steps.append_entry()
            return render_template('create_task.html', form=form)
        for j, detailed_step in enumerate(main_step.detailed_steps):
            if detailed_step.detailed_step_removal.data:
                """User removes a detailed step from a main step.
                We don't care if they remove every detailed step."""
                main_step.detailed_steps.entries.pop(j)
                return render_template('create_task.html', form=form)
    return render_template('create_task.html', form=form)


#User Account
@app.route("/user_account/<user>", methods=["GET", "POST"])
@login_required
def user_account(user):
    eUser = EditUser()
    # DO NOT REMOVE NEXT LINE!!!! PASSWORD WILL SHOW IN FORM. DUNNO WHY :)
    eUser.password.data = ""
    # DO NOT REMOVE ABOVE LINE!!!! SERIOUSLY...
    if eUser.validate_on_submit():
        UserMgmt.edit_user(eUser, user)
        return dashboard()
    return render_template("userAccount.html", EditUser=eUser, User=user)

