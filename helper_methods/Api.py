#
# API Functions
# Author: Patrick Earl
# Created: 03/04/2018
# Updated:
# Functions relating to the API 

import bcrypt
from datetime import datetime
from database import * 
from Forms.models import User

# Taken from Mason
def userLogin(email, password):
    usr = getHash(email)
    if usr is not None:
        try: 
            if usr.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8')):
                return True 
        except ValueError:
            print(usr.password)
            print(password)
            if usr.password.encode('utf-8') == password.encode('utf-8'):
                return True
            
    return False

def getHash(email):
    p = None 
    p = (User.query.filter_by(email=email).first())
    return p if p else None

def getByUser(uname):
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
    return result
    
# Returns the details for a specfic task 
def getTaskDetails(taskid):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT mainSteps.title, mainSteps.mainStepID, mainSteps.stepText, mainSteps.video, mainSteps.audio, mainSteps.requiredItem 
        FROM mainSteps, task 
        WHERE task.taskID =mainSteps.taskID AND task.taskID = %d''' % (int(taskid), ))
        
    step = cur.fetchall()
    lst = []
    count = 1
    
    for r in step:

        s = {"$id" : str(count), "mainStepName" : r['title'], "mainStepId": r['mainStepID'], 
            "mainStepText" : r['stepText'], "videoPath": r['video'], "audioPath": r['audio'],
            "requiredItems" : r['requiredItem'] }
        
        cur.execute('''SELECT * 
                FROM detailedSteps 
                WHERE mainStepID = %d''' % (r['mainStepID'], ))
        
        detail = cur.fetchall()
        
        detailed_steps = []
        
        for d in detail:
            count += 1
            d_step = {"$id": str(count), "detailedStepId" : d['detailedStepID'],
            "detailedStepName": d['title'], "imagePath": d['image'], "detailedStepText": d['stepText']}
            detailed_steps.append(d_step)
        
        count += 1
        s['detailedStep'] = detailed_steps
        lst.append(s)
        
    return lst    
    
# Returns all the steps by a given user 
def getAllCompletedSteps(uname, taskid):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT mainSteps.title, users.email, completedSteps.dateTimeCompleted, completedSteps.timeSpent
                FROM mainSteps, users, completedSteps
                WHERE completedSteps.mainStepID = mainSteps.mainStepID AND completedSteps.userID = users.userID AND mainSteps.taskID = %d AND users.email = "%s" AND completedSteps.dateTimeCompleted IS NOT NULL''' % (int(taskid), uname, ))
    r = cur.fetchall()
    count = 1
    lst = []
    for s in r:
        date_string = str(s["dateTimeCompleted"])
        spc = str(s["dateTimeCompleted"]).find(' ')
        ufc = date_string[:spc] + "T" + date_string[spc+1:]
        s = {"$id" : str(count), "mainStepName" : s["title"], "assignedUser" : s["email"], "dateTimeCompleted" : ufc, "totalTime" : s["timeSpent"]}
        lst.append(s)
        count += 1
    return lst
    