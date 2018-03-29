# ************************************************************/
# API Functions
# Author: Patrick Earl, Tyler Lance
# Created: 03/04/2018
# Updated: 03/23/2017
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
    Function: getbyuser
    Purpose: Gets the User's tasks assigned to them
    Parameters: uname - (string) username for the account
    Return: result - (dict) A json object containing the tasks for the user
    Author: Tyler Lance
    '''
    # cursor documentation: http://initd.org/psycopg/docs/cursor.html
    cur = mysql.connection.cursor()
    # get the accounts userID
    userID = getIdFromEmail(uname)
    # Invalid user
    if userID is None:
        return None
    # get the tasks assigned to the user
    cur.execute('''SELECT task.taskID, task.title FROM task, users, request 
        WHERE users.userID=%s AND users.userID=request.userID AND request.taskID=task.taskID''', (userID,))
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
    # query to gather the details about each step
    cur.execute('''SELECT mainSteps.listOrder, mainSteps.title, mainSteps.mainStepID, mainSteps.stepText, mainSteps.video, mainSteps.audio, mainSteps.requiredItem 
        FROM mainSteps, task 
        WHERE task.taskID =mainSteps.taskID AND task.taskID = %d''' % (int(taskid), ))
    step = cur.fetchall()
    lst = []
    count = 1
    # change the query results to a list and sort it by the order of the steps
    step = sorted(list(step),key=lambda k: k['listOrder'])
    # build the mapping for each main step
    for r in step:
        s = {"$id" : str(count), "mainStepName" : r['title'], "mainStepId": r['mainStepID'], 
            "mainStepText" : r['stepText'], "videoPath": r['video'], "audioPath": r['audio'],
            "requiredItems" : r['requiredItem'] }
        # gather details about the detailed steps
        cur.execute('''SELECT * 
                FROM detailedSteps 
                WHERE mainStepID = %d''' % (r['mainStepID'], ))
        detail = cur.fetchall()
        # change the query results to a list and sort it by the order of the steps
        detail = sorted(list(detail),key=lambda k: k['listOrder'])
        detailed_steps = []
        # add details for each detailed step
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
    # iterate over each completed step and build the data structure
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

def postLoggedInIp(ip, uname, signIn):
    """
    Description: submit to the database the ip address for the active user
    Parameters: ip - (string) ip address of the user connected
                uname - (string) username for the account
                signIn - (bool) T/F for setting the account login status
    Return Value: 0 - possibly change to T/F if successful, have to check what ipaws can recieve
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    user = getIdFromEmail(uname)
    # get the current date and time in the format needed in the database
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if signIn =='true':
        signIn = 1
    elif signIn =='false':
        signIn = 0
    # send query to the database
    cur.execute('''UPDATE `users`
                SET `isLoggedIn`=%d, `lastActive`="%s"
                WHERE `userID`=%d''' % (int(signIn),str(date),int(user),))
    # set the isLoggedIn, lastActive
    mysql.connection.commit()
    return 0
    
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
    userid = cur.fetchone()
    if not userid:
        return None
    return int(userid['userID'])
    
def getTaskFromID(taskID):
    """
    Description: get the task name given the task if
    Parameters: taskID - (int) id of the task
    Return Value: (string) name of the task
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # get the userid of the user given the email
    cur.execute('SELECT task.title FROM task WHERE taskID=%d' % (int(taskID),))
    task = cur.fetchone()
    if not task:
        return None
    return str(task["title"])

def getNameFromID(userID):
    """
    Description: get the first and last name given userID
    Parameters: userID - (int) id of the user
    Return Value: (string) first and last name of the user
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # get the first and last name given the userid
    cur.execute('SELECT fname, lname FROM users WHERE userID=%d' % (int(userID),))
    data = cur.fetchone()
    if not data:
        return None
    return str(data['fname'] + ' ' + data['lname'])
    
def postSurveyResults(SR,SQR):
    """
    Description: store the results of the survey
    Parameters: SR - (dict) dictionary containing data for the surveyResults laid out as:
                SR = {'userID':1,'formID':1,'name':"TylerLance",'timeSpent':45000,'email':"test.com",
                'ipAddr':"123.123.123",'ageGroup':50,'results':"response",'date':"2018-01-25",'comments':""}
                SQR - (list) list containing dictionaries for each completed question, laid out as:
                SQR = [{'questID':1,'response':"sucked"},{'questID':2,'response':"still sucked"}]
    Return Value: (bool) results if the data was able to be stored
    Author: Tyler Lance
    """
    # hard coded data for testing and to understand the function parameters, remove when implementing
    SR = {'userID':4,'formID':12,'name':"",'timeSpent':45000,'email':"test.com",'ipAddr':"123.123.123",'ageGroup':50,'results':"response",'comments':""}
    SQR = [{'questID':1,'response':"sucked"},{'questID':2,'response':"still sucked"}]
    
    cur = mysql.connection.cursor()
    # if name is empty get name from users table
    if not SR['name']:
        cur.execute('SELECT fname,lname FROM users WHERE userID=%d' % (int(SR['userID']),))
        r = cur.fetchone()
        SR['name'] = r['fname'] + ' ' + r['lname']
    # if email is empty get name from users table
    if not SR['email']:
        cur.execute('SELECT email FROM users WHERE userID=%d' % (int(SR['userID']),))
        SR['email'] = cur.fetchone()
    # get the current date and time in the format needed in the database
    SR['date'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # testing - to display query
    #print('''INSERT INTO surveyResults (`userID`,`formID`,`name`,`timeSpent`,`email`,`ipAddr`,`ageGroup`,`results`,`date`,`comments`) 
    #        values(%d,%d,"%s",%d,"%s","%s",%d,"%s","%s","%s")''' % (int(SR['userID']),int(SR['formID']),str(SR['name']),int(SR['timeSpent']),str(SR['email']),str(SR['ipAddr']),int(SR['ageGroup']),str(SR['results']),str(SR['date']),str(SR['comments']),))
	
    # insert into the surveyResults table
    cur.execute('''INSERT INTO surveyResults (`userID`,`formID`,`name`,`timeSpent`,`email`,`ipAddr`,`ageGroup`,`results`,`date`,`comments`) 
            values(%d,%d,"%s",%d,"%s","%s",%d,"%s","%s","%s")''' % (int(SR['userID']),int(SR['formID']),str(SR['name']),int(SR['timeSpent']),str(SR['email']),str(SR['ipAddr']),int(SR['ageGroup']),str(SR['results']),str(SR['date']),str(SR['comments']),))
    # execute the query
    mysql.connection.commit()
    # get the auto increment value
    cur.execute('SELECT LAST_INSERT_ID()')
    id = cur.fetchone()
    # iterate over the question response list
    for r in SQR:
    
        # testing - to display query
        #print('''INSERT INTO surveyQuestResults (`resultID`,`questID`,`response`)
        #        values(%d,%d,"%s")''' %(int(id['LAST_INSERT_ID()']),int(r['questID']),str(r['response']),))
        
        cur.execute('''INSERT INTO surveyQuestResults (`resultID`,`questID`,`response`)
                values(%d,%d,"%s")''' %(int(id['LAST_INSERT_ID()']),int(r['questID']),str(r['response']),))
        # execute the query
        mysql.connection.commit()
    return 0
    
def postSurveyForm(SF,SQ):
    """
    Description: store the survey form and all of its questions
    Parameters: SF - (dict) dictionary containing data for the form laid out as:
                SF = {'supervisorID':4,'formTitle':"title example",'description':"form description",'isActive':1}
                SQ - (list) list containing each question and multiple choice questions if necessary, laid out as:
                SQ = [{'questType':"multiple choice",'questText':"How did it go?",'isActive':1,'questOrder':1,
                'surveyMultQuest':[{'questText':"Excellent",'questOrder':1},{'questText':"Poor",'questOrder':2}]},
                {'formID':1,'questType':"open ended",'questText':"How was the survey?",'isActive':1,
                'questOrder':2,'surveyMultQuest':""}]
    Return Value: (bool) results if the data was able to be stored
    Author: Tyler Lance
    """
    # hard coded data for testing and to understand the function parameters, remove when implementing
    # query will fail if the form record is not deleted because the formTitle is a secondary key
    SF = {'supervisorID':4,'formTitle':"title example",'description':"form description",'isActive':1}
    SQ = [{'questType':"multiple choice",'questText':"How did it go?",'isActive':1,'questOrder':1,'surveyMultQuest':[{'questText':"Excellent",'questOrder':1},{'questText':"Poor",'questOrder':2}]},{'formID':1,'questType':"open ended",'questText':"How was the survey?",'isActive':1,'questOrder':2,'surveyMultQuest':""}]
    
    # get the current date and time in the format needed in the database
    SF['dateCreated'] = str(datetime.now().strftime('%Y-%m-%d'))
    SF['dateModified'] = str(datetime.now().strftime('%Y-%m-%d'))
    cur = mysql.connection.cursor()
    # verify the survey form does not already exist
    cur.execute('SELECT formID FROM surveyForm WHERE formTitle="%s"' % (str(SF['formTitle']),))
    formid = cur.fetchone()
    # if the form name already exists in the DB then return false
    if formid:
        # testing - print message that title already exists in db and survey could not be added
        print("TITLE EXISTS IN DB - False was returned and the data was not inserted.")
        return 1
    # insert the record into the form table
    cur.execute('''INSERT INTO surveyForm (`supervisorID`,`formTitle`,`description`,`dateCreated`,`dateModified`,`isActive`) 
            values(%d,"%s","%s","%s","%s",%d)''' % (int(SF['supervisorID']),str(SF['formTitle']),str(SF['description']),str(SF['dateCreated']),str(SF['dateModified']),int(SF['isActive']),))
    mysql.connection.commit()
    # get the auto increment value
    cur.execute('SELECT LAST_INSERT_ID()')
    id = cur.fetchone()
    # iterate over the question list
    for r in SQ:
        # insert the question for the form
        cur.execute('''INSERT INTO surveyQuest (`formID`,`questType`,`questText`,`isActive`,`questOrder`)
                values(%d,"%s","%s",%d,%d)''' %(int(id['LAST_INSERT_ID()']),str(r['questType']),str(r['questText']),int(r['isActive']),int(r['questOrder']),))
        mysql.connection.commit()
        # get the primary key from the survey question
        cur.execute('SELECT LAST_INSERT_ID()')
        questID = cur.fetchone()
        # check if it has multiple questions
        for m in r['surveyMultQuest']:
            # insert the multiple choice responses for the question
            cur.execute('''INSERT INTO surveyMultQuest (`questID`,`questText`,`questOrder`)
                values(%d,"%s",%d)''' %(int(questID['LAST_INSERT_ID()']),str(m['questText']),int(m['questOrder']),))
            mysql.connection.commit()
    return 0
    
def getAssignedUsers(superID):
    """
    Description: get data of the users assigned to the supervisor
    Parameters: superID - (int) supervisor id
    Return Value: (list) containing userId, first name and last name of the assigned users
              ex:  [{'userID': 5, 'fname': 'Tom', 'lname': None}, {'userID': 11, 'fname': 'John', 'lname': 'last'}, {'userID': 18, 'fname': 'Hulk', 'lname': 'Hogan'}]
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # query the database for the a list of the assigned users in the request table
    cur.execute('SELECT userID, fname, lname FROM users WHERE supervisorID="%s"' % (int(superID),))
    userData = cur.fetchall()
    return list(userData)
    
def getCompletedTasksByUsers(date, users):
    """
    Description: get data of the completed tasks of a user or users
    Parameters: users - (list) list of userIDs to pull tasks for
                date - (string) date to search for task completed from then till now, if null then find all
                       ex: 2018-03-09
    Return Value: lstUser - (list) contains completed tasks and the amount of time for each step
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    date = date + " 00:00:00"
    lstUser = []  # list to append each user into
    # iterate over the users list
    for u in users:
        # query the database to get the data on completed tasks that occur after the provided date
        cur.execute('SELECT completedTasks.completedTaskID, task.taskID, task.title, completedTasks.totalTime, completedTasks.dateStarted, completedTasks.dateTimeCompleted, completedTasks.detailedStepsUsed, completedTasks.ipAddr FROM task, completedTasks WHERE completedTasks.taskId=task.taskID AND completedTasks.dateTimeCompleted>="%s" AND completedTasks.userID = %d' % (str(date),int(u),))
        taskData = cur.fetchall()
        lstTask = []
        # iterate over the data to get the completed steps
        for t in taskData:
            taskDict = {'taskID':t['taskID'],'title':t['title'],'totalTime':t['totalTime'],'dateStarted':t['dateStarted'],'dateTimeCompleted':t['dateTimeCompleted'],'detailedStepsUsed':t['detailedStepsUsed'],'ipAddr':t['ipAddr']}
            taskDict['detailedSteps'] = getCompletedStepsByID(t['completedTaskID'])
            lstTask.append(taskDict)
        # sort by date time completed
        lstTask = sorted(lstTask,key=lambda k: k['dateTimeCompleted'], reverse=True)
        userDict = {'userID':u,'completedTasks':lstTask}
        lstUser.append(userDict)
    return lstUser
    
def getCompletedTasksByID(date, ID):
    """
    Description: get data of the completed tasks
    Parameters: ID - (int) ID of task to get data for
                date - (string) date to search for task completed from then till now, if null then find all
                       ex: 2018-03-09
    Return Value: lstUser - (list) contains completed tasks and the amount of time for each step
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    date = date + " 00:00:00"
    # query the database to get the data on completed tasks that occur after the provided date
    cur.execute('SELECT task.taskID, users.userID, users.fname, users.lname, completedTasks.completedTaskID, task.title, completedTasks.totalTime, completedTasks.dateStarted, completedTasks.dateTimeCompleted, completedTasks.detailedStepsUsed, completedTasks.ipAddr FROM users, task, completedTasks WHERE users.userID=completedTasks.userID AND completedTasks.taskId=task.taskID AND completedTasks.dateTimeCompleted>="%s" AND completedTasks.taskID = %d' % (str(date),int(ID),))
    taskData = cur.fetchall()
    lstTask = []
    # iterate over the data to get the completed steps
    for t in taskData:
        taskDict = {'taskID':t['taskID'],'userID':t['userID'],'fname':t['fname'],'lname':t['lname'],'title':t['title'],'totalTime':t['totalTime'],'dateStarted':t['dateStarted'],'dateTimeCompleted':t['dateTimeCompleted'],'detailedStepsUsed':t['detailedStepsUsed'],'ipAddr':t['ipAddr']}
        taskDict['detailedSteps'] = getCompletedStepsByID(t['completedTaskID'])
        lstTask.append(taskDict)
    # sort by date time completed
    lstTask = sorted(lstTask,key=lambda k: k['dateTimeCompleted'], reverse=True)
    return lstTask
    
def getCompletedStepsByID(ID):
    """
    Description: get data of the completed steps given a task id
    Parameters: ID - (int) ID of task to get data for
    Return Value: lstStep - (list) sorted and contains completed step and the amount of time for each
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # query the database to get the data on the completed steps
    cur.execute('SELECT mainSteps.title, mainSteps.listOrder, completedSteps.detailedStepsUsed, completedSteps.timeSpent, completedSteps.dateTimeCompleted FROM mainSteps, completedSteps WHERE completedSteps.mainStepID=mainSteps.mainStepID AND completedSteps.completedTaskID = %d' % (int(ID),))
    stepData = cur.fetchall()
    lstStep = []
    # iterate over the data to store the individual steps in a list
    for s in stepData:
        lstStep.append(s)
    # sort the order by the list order of the steps, rather than the time they were completed
    lstStep = sorted(list(lstStep),key=lambda k: k['listOrder'])
    return lstStep

def getTasksCreatedByID(superID):
    """
    Description: get all tasks created by the supervisor
    Parameters: superID - (int) supervisor id
    Return Value: lstTasks - (list) list of dictionaries containing the task id and the task name
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # query the database to get the data on the completed steps
    cur.execute('SELECT task.title, task.taskID FROM task WHERE task.published=1 AND task.activated=1 AND task.supervisorID = %d' % (int(superID),))
    tasks = cur.fetchall()
    lstTasks = []
    # iterate over the data to store the task data
    for t in tasks:
        dictTask = {}
        dictTask["title"]=t["title"]
        dictTask["taskID"]=t["taskID"]
        lstTasks.append(dictTask)
    return lstTasks
    
def getUncompletedTaskByID(userID, taskID):
    """
    Description: get the number of uncompleted tasks by a user
    Parameters: userID - (int) user id
                taskID - (int) task id
    Return Value: data - (int) number of times the task was uncompleted
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    # query the database to get the data on the completed steps
    cur.execute('SELECT count(completedTasks.taskID) FROM completedTasks WHERE completedTasks.dateTimeCompleted IS NULL AND completedTasks.userID = %d AND completedTasks.taskID=%d' % (int(userID),int(taskID),))
    data = cur.fetchone()
    if not data:
        return None
    return int(data["count(completedTasks.taskID)"])
    
def getPathForTaskImage(taskID):
    """
    Description: get the path for a tasks image
    Parameters: taskID - (int) task id
    Return Value: img - (string) path to the file
    Author: Tyler Lance
    """
    cur = mysql.connection.cursor()
    img = ""
    # query the database to get the data on the completed steps
    cur.execute('SELECT task.image, task.title FROM task WHERE task.taskID = %d' % (int(taskID),))
    path = cur.fetchone()
    if not path:
        return None
    # check if no image exists, if so pull the default image
    if path["image"] == "" or path["image"] == None:
        img = "default/" + ((path["title"])[:1]).upper() + ".png"
    else:
        img = path["image"]
    return str(img)