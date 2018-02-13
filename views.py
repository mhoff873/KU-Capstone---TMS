from flask import render_template, jsonify, request
from app import app
from flask_cors import CORS # Needed for API requests
from flask_mysqldb import MySQL
import database as db

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


@app.route('/api/user/login', methods=['POST'])
def user_login():
    '''
        Function:   user_login
        Purpose:    Allows Front End to login
        Author:     Patrick Earl
    '''
    user = request.form['username']
    password = request.form['password']
    print("User: " + user + " | Password: " + password)
    results = db.get_user(mysql, user, 0)
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
    print("USERNAME LOGGED IN:" + uname)
	# cursor documentation: http://initd.org/psycopg/docs/cursor.html
    cur = sql.connection.cursor()
	# get the accounts userID
    cur.execute('SELECT userID FROM users WHERE email=%s', [uname])
	# pull the userId from the cursor
    result = cur.fetchone() # returns as ((#,),)
    userID = result[0] # stores the first element which is the userid
    print("USERID: ", userID)
    # get the tasks assigned to the user
    cur.execute('SELECT task.taskID, task.title FROM task, users, request WHERE users.userID=%s AND users.userID=request.userID AND request.taskID=task.taskID', (userID, ))
    record = cur.fetchall()
    print("QUERY RESULTS:")
    print(record)
    
    # formatting of the api, has fixed values for the category name and id
    # because they dont exist in the TMS database
    result = { "$id": "1", "categoryName": "testing", "categoryId": 1}
    lst = [] # list to append each task into
    count = 2 # for the id of each element, as per the api
    # build up the list
    for index in record:
        # create dictionary of the id, taskid and taskname
        dict = {"$id": str(count), "taskId": index[0], "taskName": index[1]}
        # append the dictionary to the list
        lst.append(dict)
        count += 1
    # add the list to the dictionary with the key being tasks
    result["tasks"] = lst 
    result = jsonify([result])
    
    # result = jsonify({'some': 'data'})
    # result.headers.add('Access-Control-Allow-Origin', '*')
    # result.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # result.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
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
