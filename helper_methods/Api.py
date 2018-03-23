# ************************************************************/
# API Functions
# Author: Patrick Earl, Tyler Lance
# Created: 03/04/2018
# Updated: 03/08/2017
# Purpose: Functions relating to the API allowing for iPaws to communicate with TMS Database
# Version: Python Version 3.6
# ************************************************************/

import bcrypt
from datetime import datetime
from database import * 
from Forms.models import User
from flask import jsonify

def userLogin(email, password):
    """
    Description: Validate the user login from the database with encrypted passwords
    Parameters: email - (string) email of the account
                password - (string) password of the account
    Return Value: T/F (bool) if the login was valid or not
    Author: Patrick Earl, taken from  Mason
    """

    if email is None or password is None:
        return False
    usr = getHash(email)
    if usr is not None:
        try: 
            if usr.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), usr.password.encode('utf-8')):
                return True 
        except ValueError:
            # Once bcrypt is enable on all passwords this can be removed, at the time of development
            # clear text passwords still existed
            if usr.password.encode('utf-8') == password.encode('utf-8'):
                return True
            return False
    else:
        return False

def getHash(email):
    """
    Description: Returns email associated by account in the database
    Parameters: email - (string) email associated with the account
    Return Value: p - (string) result of the query, otherwise none
    Author: Patrick Earl
    """
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
    # cursor documentation: http://initd.org/psycopg/docs/cursor.html
    cur = mysql.connection.cursor()
    
    # get the accounts userID
    userID = getIdFromEmail(uname)

    # Invalid user
    if userID is None:
        return None

    # userID = result['userID']  # stores the first element which is the userid
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
    """
    Description: returns the details for a specified task
    Parameters: taskid - (int) integer value for the task id, its primary key
    Return Value: lst - (list) containing the necessary data structure containing the data
    Author: Patrick Earl, Tyler Lance
    """
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
    """
    Description: get the details for all completed steps for a task
    Parameters: uname - (string) name of the user's account
                taskid - (int) integer to specify the task, its primary key
    Return Value: lst - (list) containing necessary data pertaining to the main steps completed
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT mainSteps.title, completedSteps.dateTimeCompleted, completedSteps.timeSpent
                FROM mainSteps, users, completedSteps, completedTasks
                WHERE completedSteps.mainStepID = mainSteps.mainStepID AND completedTasks.completedTaskID=completedSteps.completedTaskID AND completedTasks.userID = users.userID AND mainSteps.taskID = %d AND users.email = "%s" AND completedSteps.dateTimeCompleted IS NOT NULL''' % (int(taskid), uname, ))
    r = cur.fetchall()
    count = 1
    lst = []
    for s in r:
        date_string = str(s["dateTimeCompleted"])
        spc = str(s["dateTimeCompleted"]).find(' ')
        ufc = date_string[:spc] + "T" + date_string[spc+1:]
        s = {"$id" : str(count), "mainStepName" : s["title"], "assignedUser" : uname, "dateTimeCompleted" : ufc, "totalTime" : s["timeSpent"]}
        lst.append(s)
        count += 1
    return lst

def getAllCompletedTasksByUser(uname):
    """
    Description: return all completed tasks for a user
    Parameters: uname - (string) username for the user account
    Return Value: lst - (list) containing the necessary api datastructure
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    user = getIdFromEmail(uname)
    # query to get non duplicated task id's completed by the user
    cur.execute('''SELECT completedTasks.taskID, task.title, completedTasks.dateTimeCompleted, completedTasks.totalTime,completedTasks.detailedStepsUsed 
    FROM completedTasks, task 
    WHERE completedTasks.userID=%d AND completedTasks.taskID=task.taskID AND dateTimeCompleted IS NOT NULL''' % (int(user),))
    r = cur.fetchall()
    count = 1
    lst = []
    for s in r:
        # create the data structure using the queried information
        date_string = str(s["dateTimeCompleted"])
        spc = str(s["dateTimeCompleted"]).find(' ')
        ufc = date_string[:spc] + "T" + date_string[spc+1:]
        d = {"$id":str(count),"taskID": int(s['taskID']),"taskName":str(s['title']),"assignedUser":str(uname),"dateTimeCompleted":ufc,"totalTime":int(s['totalTime']),"totalDetailedStepsUsed":int(s['detailedStepsUsed']),"id":int(count)}
        lst.append(d)
        count += 1
    return lst

# Posts a completed step by adding it to the database
def postMainStepCompleted(taskID, stepID, user, numUsed, time, ip):     
    """
    Description: submit to the database a completed main step
    Parameters: taskID - (int) task id
                stepID - (int) main step id to be completed
                user - (string) username of the account
                numUsed - (int) number of detailed steps used
                time - (int) number of milliseconds to complete step
                ip - (string) ip address of the account connected
    Return Value: 0 - possibly change to T/F if successful, have to check what ipaws can recieve
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    user = getIdFromEmail(user)
    # get the current date and time in the format needed in the database
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # send query to the database
    cur.execute('''SELECT completedTasks.completedTaskID FROM completedTasks WHERE completedTasks.userID=%d AND completedTasks.taskID=%d''' % (int(user),int(taskID),))
    cTaskID = cur.fetchall()

    # if task has not been added to task completed table and the main steps have not been added to completed staps table
    if not cTaskID:
        # get all mainsteps for the task
        cur.execute('SELECT mainSteps.mainStepID FROM mainSteps WHERE mainSteps.taskID=%d' % (int(taskID),))
        r2 = cur.fetchall()
        # add the record into the completed tasks table
        cur.execute('INSERT INTO completedTasks (`taskID`,`userID`,`totalTime`,`dateStarted`,`detailedStepsUsed`,`ipAddr`) values(%d,%d,%d,"%s",%d,"%s")' % (int(taskID),int(user),int(time),str(date),0,str(ip),))
        mysql.connection.commit()

        # get last insert id for the completedTasks
        cur.execute('SELECT LAST_INSERT_ID()')
        cTaskID = cur.fetchall()
        cTaskID = cTaskID[0]
        cTaskID = cTaskID['LAST_INSERT_ID()']
        # add the steps into the completed steps table
        for i in r2:
            # add the records into the completed steps table
            cur.execute('INSERT INTO completedSteps (`completedTaskID`,`mainStepID`,`detailedStepsUsed`,`timeSpent`) values(%d,%d,%d,%d)' % (int(cTaskID),int(i['mainStepID']),0,0,))
            mysql.connection.commit()
    else:
        cTaskID=cTaskID[0]
        cTaskID=cTaskID['completedTaskID']
    
    # update the step in the table
    cur.execute('UPDATE completedSteps SET `detailedStepsUsed`=%d,`timeSpent`=%d,`dateTimeCompleted`="%s" WHERE `completedTaskID`=%d AND `mainStepID`=%d' % (int(numUsed),int(time),str(date),int(cTaskID),int(stepID),))
    mysql.connection.commit()
    
    return 0

# Posts a task step by adding it to the database
def postTaskCompleted(taskID, user, time, numUsed):
    """
    Description: submit to the database a completed task by setting the dateTimeCompleted for the mainSteps inside completeSteps to the current date and time
    Parameters: taskID - (int) primary key for the task to be marked completed
                user - (string) email of the user
                time - (int) time it took to complete the task
                numUsed - (int) number of detailed steps used in the task
    Return Value: 0 - possibly change to T/F if successful, have to check what ipaws can recieve
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    user = getIdFromEmail(user)
    # get the current date and time in the format needed in the database
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # send query to the database
    cur.execute('''UPDATE `completedTasks`
                SET `dateTimeCompleted`="%s", `totalTime`=%d, `detailedStepsUsed`=%d
                WHERE completedTasks.userID=%d AND completedTasks.taskID=%d''' % (str(date), int(time), int(numUsed),int(user),int(taskID),))
    mysql.connection.commit()
    return 0

def postLoggedInIp(data):
    """
    Description: submit to the database the ip address for the active user
    Parameters: data - (dict) containing the keys IpAddress, SignedIn, Username
    Return Value:
    NOTE: this is commented out on ipaws
    TEST: http://tmst.kutztown.edu:5004/api/user/PostLoggedInIp/{"IpAddress":156.12.128.10,"SignedIn":true,"Username":"test.com"}
    """
    return data
    
def getIdFromEmail(uname):
    """
    Description: get the privary key given the username/email
    Parameters: uname - (string) email of the user
    Return Value: (int) primary key of the user account
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # get the userid of the user given the email
    cur.execute('SELECT userID FROM users WHERE email="%s"' % (uname,))
    r = cur.fetchall()
    if not r:
        return None
    userid = r[0]
    return int(userid['userID'])
