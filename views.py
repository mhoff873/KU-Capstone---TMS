from flask import render_template, request, jsonify, redirect,url_for, flash, session, json

from app import app
from Forms.forms import CreateAccount,CreateSupervisor, EditUser, AddUser, AssignUser, \
    CreateTaskForm, ChangePassword, LoginForm, CreateUser, CreateASurvey, TaskAssignmentForm
from helper_methods import UserMgmt,  TaskHelper, Update, Login, Library, TaskAssignmentHelper, Api
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

# survey creation
@app.route("/surveyCreation/", methods=["GET", "POST"])
@app.route("/surveyCreation/<arguments>", methods=["GET", "POST"])
@login_required
def surveyCreation(arguments=None):
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
                print("exists")
                flash('Survey name already exists.', 'warning')
                return render_template("surveysTemp.html", form=form, task=task)
            else:
                print("HERE")
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
                print(r)
                dict2 = {'questText': r[j].response.data, 'questOrder': j+1}
                lstResponses.append(dict2)
            dict['surveyMultQuest'] = lstResponses
        SQ.append(dict)
    return Api.postSurveyForm(SF,SQ)
    
# survey results
@app.route("/survey_results/", methods=["GET", "POST"])
@login_required
def survey_results():
    survey_forms = SurveyForm.query.all() # the entire form table using the formID get the formTitle
    survey_results = SurveyResult.query.all() # the entire result table. get the formID and the name
    surveys_assigned = SurveyAssigned.query.all() # the entire assigned table
    all_the_flippin_tasks = Task.query.all() # all the flippin tasks

    das_struct = []
    
    formID_to_name = {} # result table map
    formID_to_title = {} # surveyForm table map
    formID_to_taskID = {} # assigned table map
    taskID_to_title = {} # task table map
    formID_to_date = {}
    
    formIDs=[] # list of all formIDs from the result table
    
    # formIDs have unique titles in the surveyForms table
    for s in survey_forms:
        formID_to_title[s.formID]=s.formTitle
        # print(formID_to_title[s.formID])
        
    # taskIDs have unique titles in the task table
    for t in all_the_flippin_tasks:
        taskID_to_title[t.taskID]=t.title
        # print(taskID_to_title[t.taskID])
    
    # formIDs have unique names in the result table
    for f in survey_results:
        formID_to_name[f.formID]=f.name
        formID_to_date[f.formID] = f.date
        # print(formID_to_name[f.formID])
        
    # formID to taskID mapping from the assigned table
    for a in surveys_assigned:
        formID_to_taskID[a.formID]=a.taskID
        formIDs.append(a.formID)
        # print(formID_to_taskID[a.formID])
        
    # print(formIDs)
    
    # building das_struct
    for f in formIDs:
        # print(formID_to_name[f]) # prints name of the result
        # print(taskID_to_title[formID_to_taskID[f]]) # prints the title of the task
        # print(formID_to_title[f]) # prints the title of the surveyForm
        das_struct.append({'formID':f,'taskTitle':taskID_to_title[formID_to_taskID[f]],'surveyTitle':formID_to_title[f],'userName':formID_to_name[f],'date':formID_to_date[f]})
    
    # print(das_struct)
    return render_template("surveyResults.html", result_struct=das_struct)
     
# display survey to user
# https://tmst.kutztown.edu:5002/userSurvey/test.com/654706
@app.route("/userSurvey/<username>/<taskID>", methods=["GET","POST"])
def userSurvey(username=None,taskID=None):
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
        # VALIDATE FORM HERE
        # check if the data was submitted
        if form.save.data:
            flash("Your survey has been submitted.", "success")
            # pull the data from the form so that it can be prepared to be stored
            SR = {'userID': form.userID.data, 'formID': Api.getAssignedSurvey(form.taskID.data), 'name': Api.getNameFromID(form.userID.data), 'timeSpent': 0, 'email': "", 'ipAddr': request.remote_addr, 'ageGroup': 0, 'results': "", 'comments': ""}
            SQR = []
            for q in form.questions:
                dict = {}
                if q.stock_question.data == "" or q.stock_question.data is None:
                    dict = {'questID': q.questID.data, 'response': request.form[q.questID.data]}
                # if it was an open ended question
                else:
                    dict = {'questID': q.questID.data, 'response': q.stock_question.data}
                SQR.append(dict)
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
            questions.stock_question.label = q['questText']
            questions.stock_question.data = ""
            if q['questType'] == 'multiple choice':
                for m in q['surveyMultQuest']:
                    responses = questions.responses.append_entry()
                    responses.response.label = m['questText']
    return render_template("userSurvey.html", form=form, task=Api.getTaskFromID(taskID))
    
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
            dictTask["totalTime"]=str(int(li2["totalTime"]/1000)) + " seconds"
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
    Return Value: None
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
    # create list containing dictionaries for each table row
    for li in tasks:
        li["userID"]=Api.getNameFromID(li["userID"])
    html = render_template('pdf.html', supervisor=supervisorID, user=users, tasks=tasks, constraint=sortedBy, date=str(datetime.now().strftime('%A %B %d, %Y %I:%M%p')))
    return render_pdf(HTML(string=html))

@app.route('/graph', methods=['GET'])
@app.route('/graph/<arguments>', methods=['GET'])
@login_required
def graph(arguments=None):
    """
    Description: generate the graphs for the reports
    Parameters: none
    Return Value: none
    Author: Tyler Lance
    """
    display = False
    chart = pygal.HorizontalBar()
    # Get the supervisor ID
    supervisorID = current_user.supervisorID
    # statistics to be displayed under the graph, empty if no arguments
    statistics = []
    sortedBy = ""
    curDate = "2000-01-01"
    # get users assigned to the supervisor
    users =  Api.getAssignedUsers(supervisorID)
    # get list of tasks created by the supervisor
    tasks = Api.getTasksCreatedByID(supervisorID)
    tasks = sorted(tasks,key=lambda k: k['title'])
    # check if arguments were passed to the url
    if arguments is not None:
        # pull the relevant data to determine what graph to display
        date = arguments.split('&')[0]
        date = date.split('=')[1]
        task = arguments.split('&')[1]
        task = task.split('=')[1]
        user = arguments.split('&')[2]
        user = user.split('=')[1]
        submit = arguments.split('&')[3]
        submit = submit.split('=')[1]
        if submit == 'T':
            # determine the time frame for the data to be pulled by
            if date == 'M':
                curDate = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last 30 Days"
            elif date == 'W':
                curDate = str((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last 7 Days"
            elif date == 'D':
                curDate = str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last Day"
            elif date == 'A':
                curDate = "2000-01-01"
                sortedBy = " For All Entries"
            # if a graph needs to be displayed - generates the task graph
            if submit == 'T' and task != 'None':
                display = True
                # get the task name given the id
                chart.title = "Everyones Average Completion Time For " + Api.getTaskFromID(task) + sortedBy
                # get the necessary data for all completed entries for the specified task
                task = Api.getCompletedTasksByID(curDate, task)
                lstTask = []
                for t in task:
                    # if the userid already exists then update the values
                    if any(d['userID'] == t["userID"] for d in lstTask):
                        for i in lstTask:
                            if i["userID"] == t["userID"]:
                                i["totalTime"] = t["totalTime"] + i["totalTime"]
                                i["total"] += 1
                    # otherwise add those values into the dictionary
                    else:
                        dictTask = {}
                        dictTask["userID"] = t["userID"]
                        dictTask["totalTime"] = t["totalTime"]
                        dictTask["total"] = 1
                        dictTask["taskID"] = t["taskID"]
                        lstTask.append(dictTask)
                # iterate over the list to calculate the averages for each user and add it to the chart
                for t in lstTask:
                    chart.add(Api.getNameFromID(t['userID']), int((t['totalTime']/t['total'])/1000))
                    statistics.append(Api.getNameFromID(t['userID']) + ' completed this task ' + str(t['total']) + ' time(s).')
                    statistics.append(Api.getNameFromID(t['userID']) + ' was unable to complete this task ' + str(Api.getUncompletedTaskByID(t['userID'],t['taskID'])) + ' time(s).')
            # to generate the user graph
            elif submit == 'T' and user != 'None':
                display = True
                # get the name of the user
                name = Api.getNameFromID(int(user))
                # generate title for the graph
                chart.title = name + 's Average Task Completion ' + sortedBy
                # get the necessary data for all completed entries for the specified user
                task = Api.getCompletedTasksByUsers(curDate,[user])
                completedTasks = []
                # pull the list of task ids
                for t in task:
                    if t['userID'] == user:
                        completedTasks = t['completedTasks']
                lstTask = []
                for t in completedTasks:
                    # if the task id already exists then update the values
                    if any(d['taskID'] == t["taskID"] for d in lstTask):
                        for i in lstTask:
                            if i["taskID"] == t["taskID"]:
                                i["totalTime"] = t["totalTime"] + i["totalTime"]
                                i["total"] += 1
                    # otherwise add those values into the dictionary
                    else:
                        dictTask = {}
                        dictTask["taskID"] = t["taskID"]
                        dictTask["totalTime"] = t["totalTime"]
                        dictTask["total"] = 1
                        lstTask.append(dictTask)
                # iterate over the list to calculate the averages for each task and add it to the chart
                for t in lstTask:
                    chart.add(Api.getTaskFromID(t['taskID']), int((t['totalTime']/t['total'])/1000))
                    statistics.append(Api.getTaskFromID(t['taskID']) + ' was completed ' + str(t['total']) + ' time(s).')
                    statistics.append(Api.getTaskFromID(t['taskID']) + ' was uncompleted ' + str(Api.getUncompletedTaskByID(int(user),t['taskID'])) + ' time(s).')
            # display message that they need to select a name or task
            if submit == 'T' and user == 'None' and task == 'None':
                flash("You must select either a Senior Name or a Task before a graph can be generated", "warning")
    chart = chart.render_data_uri()
    return render_template('graph.html', supervisor=supervisorID, user=users, task=tasks, chart=chart, statistics=statistics, display=display)


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
    
# survey management
@app.route("/surveys/", methods=["GET", "POST"])
@app.route('/surveys/<arguments>/<formID>', methods=["GET"])
@login_required
def surveys(arguments=None,formID=None):
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
        
# link to the logout page to log an account out
@app.route('/logout', methods=['GET'])
@login_required
def logout_account():
    logout_user()
    return redirect("login", code=302)

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
    user_choices = [(user.userID, user.fname + ' ' + user.lname) for user in
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
        new_task = TaskHelper.create_task(form)
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


@app.route('/edit_task', methods=['GET', 'POST'])
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
        form = TaskHelper.get_task(task_id)
        return render_template('edit_task.html', form=form)
    # Below code runs on POST requests.
    form = CreateTaskForm(request.form)

    if form.save.data:
        """Save task as draft."""
        task = TaskHelper.create_task(form)
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
