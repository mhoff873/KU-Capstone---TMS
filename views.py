from flask import render_template, request, jsonify

from app import app
from Forms.forms import CreateAccount,CreateSupervisor, EditUser, AddUser, AssignUser, \
    CreateTaskForm, ChangePassword, LoginForm, CreateUser #need to get rid of CreateAccount
from helper_methods import UserMgmt, Tasks, Update, Login
from database import *


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
# @login_required
def dashboard():
    createAccountForm = CreateAccount()
    eUser = EditUser()
    aUser = AddUser()
    assUser = AssignUser()
    return render_template('dashboard.html', CreateAccount=createAccountForm,EditUser=eUser,AddUser=aUser,AssignUser=assUser)


# supervisor account
@app.route('/supervisor_account', methods=['GET'])
# @login_required
def supervisor_account():
    eUser = EditUser()
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
            return render_template('dashboard.html')
        else:
            print("login failed, try again")
    # form submission was invalid
    if lForm.errors:
        for error_field, error_message in lForm.errors.items():
            print("Field : {field}; error : {error}".format(field=error_field, error=error_message))
    # the page has not been submitted before so lets render the form instead
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
def create_supervisor():
    form = CreateSupervisor()
    if form.validate_on_submit():
        UserMgmt.create_supervisor(form)
        eUser = EditUser()
        aUser = AddUser()
        assUser = AssignUser()
        return render_template('supervisor_account.html',EditUser=eUser,AddUser=aUser,AssignUser=assUser)
    return render_template("createSupervisorTest.html", form=form)


#create user page
@app.route("/create_user/", methods=["GET", "POST"])
def create_user():
    form = CreateUser()
    if form.validate_on_submit():
        UserMgmt.create_user(form)
        return "WOOOT you created a new user!"
    return render_template("createUser.html", form=form)

# library
@app.route("/library/", methods=["GET", "POST"])
def library():
    return render_template("library.html")
    

@app.route("/teambforms/", methods=["GET", "POST"])
def team_b_forms():
    # Create Forms
    createAccountForm = CreateAccount()
    editUserForm = EditUser()
    addUserForm = AddUser()
    assignUserForm = AssignUser()
    unassigned_users = [x.email for x in UserMgmt.get_unassigned()]
    if createAccountForm.validate_on_submit():
        UserMgmt.create_account(createAccountForm)
        return "New user created!"
    elif editUserForm.validate_on_submit():
        UserMgmt.edit_user(editUserForm)
        return "EditUser Form submitted!"
    elif addUserForm.validate_on_submit():
        UserMgmt.add_user(addUserForm)
        return str(addUserForm.user.data)  # "Successfully assigned user!"
    elif assignUserForm.validate_on_submit():
        return UserMgmt.assign_user(assignUserForm)
    return render_template("TeamBForms.html",
                           CreateAccount=createAccountForm,
                           EditUser=editUserForm,
                           AddUser=addUserForm,
                           AssignUser=assignUserForm,
                           users=unassigned_users)


# create task
@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    form = CreateTaskForm()
    if request.method == ['GET']:
        return render_template('create_task.html', form=form)
    # When buttons are clicked on the form, it returns a True/False value
    # We use those values to determine which buttons were clicked to add steps
    # accordingly
    if form.add_main_step.data:
        print('Add main step')
        form.main_step.append_entry()
        return render_template('create_task.html', form=form)
    elif form.save_as_draft.data:
        print('Save as draft')
        Tasks.create_task(form)
        return render_template('create_task.html', form=form)
    elif form.publish.data:
        print('Publish Task')
        Tasks.create_task(form)
        return render_template('index.html')
    else:
        print('Checking for detailed step button press.')
        for i, step in enumerate(form.main_step):
            print(i)
            print(step.add_detailed_step.data)
            if step.add_detailed_step.data:
                step.detailed_steps.append_entry()
    return render_template('create_task.html', form=form)
