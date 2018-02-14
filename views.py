from flask import render_template, jsonify, request
from app import app
from flask_mysqldb import MySQL
from database import *

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
    #print("USERNAME LOGGED IN:" + uname)
	# cursor documentation: http://initd.org/psycopg/docs/cursor.html
    cur = mysql.connection.cursor()
	# get the accounts userID
    cur.execute('SELECT userID FROM users WHERE email=%s', [uname])
	# pull the userId from the cursor
    result = cur.fetchone() # returns as ((#,),)
    print(result)
    # Invalid user
    if result is None:
        return jsonify([])
    
    userID = result['userID'] # stores the first element which is the userid
    # get the tasks assigned to the user
    cur.execute('SELECT task.taskID, task.title FROM task, users, request WHERE users.userID=%s AND users.userID=request.userID AND request.taskID=task.taskID', (userID, ))
    record = cur.fetchall()

    
    # formatting of the api, has fixed values for the category name and id
    # because they dont exist in the TMS database
    result = { "$id": "1", "categoryName": "testing", "categoryId": 1}
    lst = [] # list to append each task into
    count = 2 # for the id of each element, as per the api
    # build up the list

    for index in record:
        # Don't assign a keyword..
        tsks = {}
        if app.config['MYSQL_CURSORCLASS'] == 'DictCursor'
            # create dictionary of the id, taskid and taskname
            tsks = {"$id": str(count), "taskId": index['taskID'], "taskName": index['title']}
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
