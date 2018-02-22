from flask import render_template

#team A start
#from forms import CreateTaskForm
from Forms.forms import CreateTaskForm
#team A end

#team B start
from app import app
from Forms.forms import CreateAccount, EditUser, UpdatePassword, LoginForm, AddUser, AssignUser
from Forms.models import User
import Login
import Update
import bcrypt

@app.route('/', methods=['GET'])
def index():
    """
    Example flask-mysqldb implementation
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users''')
    NOTE: ^ is so so so so so unsecure. SQL injections yall.
    results = cursor.fetchall()
    return results

    If this lib doesn't have all the support we need, we'll need to look at
    using jQuery AJAX embedded within our python.
    """
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
#@login_required
def dashboard():
    createAccountForm = CreateAccount()
    eUser = EditUser()
    aUser = AddUser()
    assUser = AssignUser()
    return render_template('dashboard.html', CreateAccount=createAccountForm,EditUser=eUser,AddUser=aUser,AssignUser=assUser)

    @app.route('/supervisor_account', methods=['GET'])
    #@login_required
    def dashboard():

        eUser = EditUser()
        aUser = AddUser()
        assUser = AssignUser()
        return render_template('supervisor_account.html',EditUser=eUser,AddUser=aUser,AssignUser=assUser)



# login page
@app.route('/login', methods=['POST','GET'])
def login():
    lForm = LoginForm()
    if lForm.validate_on_submit():
        #print (str("Email: {e}").format(e=lForm.email.data))
        #print (str("Password: {p}").format(p=lForm.password.data))
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
    uForm = UpdatePassword()
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

@app.route("/chris/", methods=["GET", "POST"])
def chris():
    form = CreateAccount()
    if form.validate_on_submit():
        return "WOOOT you created and account/no you didn't... I am not adding this :D"
    return render_template("createSupervisorTest.html", form=form)

@app.route("/teambforms/", methods=["GET", "POST"])
def team_b_forms():
    createAccountForm = CreateAccount()
    editUserForm = EditUser()
    if createAccountForm.validate_on_submit:
        return "CreateAccount Form submitted!"
    elif editUserForm.validate_on_submit:
        return "EditUser Form submitted!"
    return render_template("TeamBForms.html", CreateAccount=createAccountForm, EditUser=editUserForm)


@app.route('/task', methods=["GET", "POST"])
#@login_required
def task():
    return render_template('task.html')

#end of team B

#start of team A

@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    form = CreateTaskForm()
    print(form.data)
    print(request.method)
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
        return render_template('create_task.html', form=form)
    elif form.publish.data:
        print('Publish Task')
        return render_template('index.html')
    else:
        print('Checking for detailed step button press.')
        for i, step in enumerate(form.main_step):
            print(i)
            print(step.add_detailed_step.data)
            if step.add_detailed_step.data:
                step.detailed_steps.append_entry()
                #print(f'Adding detailed for main step {i}.')
    return render_template('create_task.html', form=form)

    #end of Team A
