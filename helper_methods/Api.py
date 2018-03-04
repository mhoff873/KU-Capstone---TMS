#
# API Functions
# Author: Patrick Earl
# Created: 03/04/2018
# Updated:
# Functions relating to the API 

import bcrypt
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
        print(count)
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
    