from flask import render_template, request, jsonify, redirect

from Forms.forms import CreateSupervisor, EditUser, AddUser, AssignUser, \
    CreateTaskForm, ChangePassword, LoginForm, CreateUser, UserAssignmentForm
from helper_methods import UserMgmt, TaskHelper, Update, Login, Library
from database import *
from flask_login import current_user, login_required, logout_user
from Forms.models import Task, User, Supervisor


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/user/login', methods=['POST'])
def user_login():
    '''
        Function:   user_login
        Purpose:    Allows Front End to login
        Author:     Patrick Earl
    '''
    user = request.form['username']
    password = request.form['password']
    print(password)
    cur = mysql.connection.cursor()
    # Since we are going to be using encryption, its better this way - Patrick
    cur.execute('SELECT * FROM users WHERE email=%s', (user,))
    results = cur.fetchone()
    print(results)
    if results is None:
        return jsonify({'d': 'sign in failure'})
    else:
        if results['password'] == password:
            return jsonify({'d': "sign in success"})
        else:
            return jsonify({'d': 'sign in failure'})


@app.route('/api/user/GetByUser/<uname>', methods=['GET'])
def getbyuser(uname):
    '''
        Function:       getbyuser
        Purpose:        Gets the User's tasks assigned to them
        Return:         json - A json object containing the tasks for the user
        Author:         Tyler Lance
    '''
    # print("USERNAME LOGGED IN:" + uname)
    # cursor documentation: http://initd.org/psycopg/docs/cursor.html
    cur = mysql.connection.cursor()
    # get the accounts userID
    cur.execute('SELECT userID FROM users WHERE email=%s', [uname])
    # pull the userId from the cursor
    result = cur.fetchone()  # returns as ((#,),)
    print(result)
    # Invalid user
    if result is None:
        return jsonify([])

    userID = result['userID']  # stores the first element which is the userid
    # get the tasks assigned to the user
    cur.execute(
        'SELECT task.taskID, task.title FROM task, users, request WHERE users.userID=%s AND users.userID=request.userID AND request.taskID=task.taskID',
        (userID,))
    record = cur.fetchall()

    # formatting of the api, has fixed values for the category name and id
    # because they dont exist in the TMS database
    result = {"$id": "1", "categoryName": "testing", "categoryId": 1}
    lst = []  # list to append each task into
    count = 2  # for the id of each element, as per the api
    # build up the list

    for index in record:
        # Don't assign a keyword..
        tsks = {}
        if app.config['MYSQL_CURSORCLASS'] == 'DictCursor':
            # create dictionary of the id, taskid and taskname
            tsks = {"$id": str(count), "taskId": index['taskID'],
                    "taskName": index['title']}
        else:
            tsks = {"id": str(count), "taskId": index[0], "taskName": index[1]}
        # append the dictionary to the list
        lst.append(tsks)
        count += 1
    # add the list to the dictionary with the key being tasks
    result["tasks"] = lst
    result = jsonify([result])

    return result


# For sprint 2
'''
@app.route("/api/GetTaskDetails/<taskid>")
def GetTaskDetails(taskid):
    return
@app.route("/api/GetAllCompletedSteps/<uname>/<taskid>")
def GetAllCompletedSteps(uname, taskid):
    return
@app.route("/api/GetByUser/<uname>")
def GetByUser(uname):
    return
'''


# dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    tasks = Task.query.filter_by(supervisorID=current_user.supervisorID).all()
    users = User.query.filter_by(supervisorID=current_user.supervisorID).all()
    return render_template('dashboard.html', task_list=tasks, user_list=users)


# supervisor account
@app.route('/supervisor_account', methods=['GET', "POST"])
@login_required
def supervisor_account():
    eUser = EditUser()
    if eUser.validate_on_submit():
        UserMgmt.edit_supervisor(eUser, current_user)
        return dashboard()
    aUser = AddUser()
    assUser = AssignUser()
    return render_template('supervisor_account.html',EditUser=eUser,AddUser=aUser,AssignUser=assUser)


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


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return login()


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


# create supervisor page
@app.route("/create_supervisor/", methods=["GET", "POST"])
@login_required
def create_supervisor():
    form = CreateSupervisor()
    if form.validate_on_submit():
        UserMgmt.create_supervisor(form)
        eUser = EditUser()
        aUser = AddUser()
        assUser = AssignUser()
        return render_template('supervisor_account.html',EditUser=eUser,AddUser=aUser,AssignUser=assUser)
    return render_template("createSupervisorTest.html", form=form)


# create user page
@app.route("/create_user/", methods=["GET", "POST"])
@login_required
def create_user():
    form = CreateUser()
    if form.validate_on_submit():
        UserMgmt.create_user(form)
        return "WOOOT you created a new user!"
    return render_template("createUser.html", form=form)


# library
@app.route("/library/", methods=["GET", "POST"])
@app.route("/library/<supervisor_id>", methods=["GET", "POST"])
@login_required
def library(supervisor_id=None):
    search_form = Library.SearchForm()
    allsupervisors = Library.get_supervisors()
    tasks = []
    if search_form.validate_on_submit():
        keyword = search_form.search.data
        tasks = Library.search(keyword)
    else:
        # If the form is not submitted then I need to check if I am searching by supervisor
        if supervisor_id is not None:
            tasks = Library.get_tasks(supervisor_id)
        else:
            tasks = Library.get_tasks(current_user.supervisorID)
    return render_template("library.html", tasks=tasks, search=search_form, supervisors=allsupervisors)

#assign tasks to users
@app.route('/user_assignment/', methods=["GET", "POST"])
@login_required
def user_assignment():
    form = UserAssignmentForm()
    users = []
    tasks = []
    if current_user.role == "supervisor":
        users = UserMgmt.get_supervisor_users(current_user.email)
    else:
        users = User.query.all()
    if form.add_task.data:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(taskID=18).first()
    return render_template("user_assignment.html", users=users, tasks=tasks, form=form)


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
