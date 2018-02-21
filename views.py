from flask import render_template, request

from app import app
from Forms.forms import CreateAccount, EditUser, AddUser, AssignUser
from helper_methods import UserMgmt


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
