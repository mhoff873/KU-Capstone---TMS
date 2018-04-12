# ************************************************************/
# API Functions
# Author: Tyler Lance, Patrick Earl
# Created: 04/12/2018
# Updated: 04/12/2018
# Purpose: Functions relating to reports
# Version: Python Version 3.6
# ************************************************************/

from flask import render_template, request, redirect,url_for, flash, session
from Forms.forms import CreateASurvey
from helper_methods import Api
from database import *
from flask_login import current_user, login_required, logout_user
from Forms.models import Task, User, Supervisor, Request
from datetime import datetime, timedelta
from flask_weasyprint import HTML, render_pdf
import weasyprint
from flask_mail import Message
import pygal

def handle_reports(arguments=None):
    '''
        Description: Generate a report for the users assigned to the supervisor
        Parameters: None or the sorting options
        Return: A rendered template 
        Author: Tyler Lance
    '''
    (supervisorID, users, lstTask, sortedBy, Senior, Constraints) = generate_report(arguments)
    return render_template('reports.html', supervisor=supervisorID, user=users, tasks=lstTask, constraint=sortedBy,  arguments=arguments, Senior=Senior, Constraints=Constraints)
    
def handle_pdf(arguments=None):
    """
    Description: Generates a report for all users assigned to the supervisor or for a specifed user
        Returns a pdf
    Parameters: None or the sorting options
    Return Value: None
    Author: Tyler Lance
    """
    # Chose which supervisor the report is being generated for
    #supervisorID = current_user.supervisorID
    supervisorID = current_user.supervisorID
    # pull the list of assigned users to the supervisor
    users =  Api.getAssignedUsers(supervisorID)
    # default date for the data if no date is passed
    date = "2000-01-01"
    # what the data is sorted by
    sortedBy = "Showing all entries by date"
    # pull userIDs from the user data
    lstUserIDs = [li['userID'] for li in users]
    # check if arguments were passed to the url
    if arguments is not None:
        sort = arguments.split(':')[0]
        data = arguments.split(':')[1]
        # check if userID was passed via url and that it wasnt all
        if sort == 'userid' and data != 'A':
            # empties the list of userids and adds in the passed one
            lstUserIDs = []
            lstUserIDs.append(int(data))
            sortedBy = "Showing entries for user: " + Api.getNameFromID(int(data))
        # check if date specified was passed to url
        elif sort == 'date':
            if data == 'M':
                date = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 30 days"
            elif data == 'W':
                date = str((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 7 days"
            elif data == 'D':
                date = str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last day"
    # get completed tasks by passing the list and date
    tasks = Api.getTasksByUsers(date, lstUserIDs)
    # create list containing dictionaries for each table row
    for li in tasks:
        li["userID"]=Api.getNameFromID(li["userID"])
    html = render_template('pdf.html', supervisor=supervisorID, user=users, tasks=tasks, constraint=sortedBy, date=str(datetime.now().strftime('%A %B %d, %Y %I:%M%p')))
    return render_pdf(HTML(string=html))
    
def handle_graph(arguments=None):
    """
    Description: generate the graphs for the reports
    Parameters: none
    Return Value: none
    Author: Tyler Lance
    """
    display = False
    chart = pygal.HorizontalBar()
    # Get the supervisor ID
    supervisorID = current_user.supervisorID
    # statistics to be displayed under the graph, empty if no arguments
    statistics = []
    sortedBy = ""
    curDate = "2000-01-01"
    # get users assigned to the supervisor
    users =  Api.getAssignedUsers(supervisorID)
    # get list of tasks created by the supervisor
    tasks = Api.getTasksCreatedByID(supervisorID)
    tasks = sorted(tasks,key=lambda k: k['title'])
    # check if arguments were passed to the url
    if arguments is not None:
        # pull the relevant data to determine what graph to display
        date = arguments.split('&')[0]
        date = date.split('=')[1]
        task = arguments.split('&')[1]
        task = task.split('=')[1]
        user = arguments.split('&')[2]
        user = user.split('=')[1]
        submit = arguments.split('&')[3]
        submit = submit.split('=')[1]
        if submit == 'T':
            # determine the time frame for the data to be pulled by
            if date == 'M':
                curDate = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last 30 Days"
            elif date == 'W':
                curDate = str((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last 7 Days"
            elif date == 'D':
                curDate = str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
                sortedBy = " For The Last Day"
            elif date == 'A':
                curDate = "2000-01-01"
                sortedBy = " For All Entries"
            # if a graph needs to be displayed - generates the task graph
            if submit == 'T' and task != 'None':
                display = True
                # get the task name given the id
                chart.title = "Everyones Average Completion Time For " + Api.getTaskFromID(task) + sortedBy
                # get the necessary data for all completed entries for the specified task
                task = Api.getCompletedTasksByID(curDate, task)
                lstTask = []
                for t in task:
                    # if the userid already exists then update the values
                    if any(d['userID'] == t["userID"] for d in lstTask):
                        for i in lstTask:
                            if i["userID"] == t["userID"]:
                                i["totalTime"] = t["totalTime"] + i["totalTime"]
                                i["total"] += 1
                    # otherwise add those values into the dictionary
                    else:
                        dictTask = {}
                        dictTask["userID"] = t["userID"]
                        dictTask["totalTime"] = t["totalTime"]
                        dictTask["total"] = 1
                        dictTask["taskID"] = t["taskID"]
                        lstTask.append(dictTask)
                # iterate over the list to calculate the averages for each user and add it to the chart
                for t in lstTask:
                    chart.add(Api.getNameFromID(t['userID']), int((t['totalTime']/t['total'])/1000))
                    statistics.append(Api.getNameFromID(t['userID']) + ' completed this task ' + str(t['total']) + ' time(s).')
                    statistics.append(Api.getNameFromID(t['userID']) + ' was unable to complete this task ' + str(Api.getUncompletedTaskByID(t['userID'],t['taskID'])) + ' time(s).')
            # to generate the user graph
            elif submit == 'T' and user != 'None':
                display = True
                # get the name of the user
                name = Api.getNameFromID(int(user))
                # generate title for the graph
                chart.title = name + 's Average Task Completion ' + sortedBy
                # get the necessary data for all completed entries for the specified user
                task = Api.getTasksByUsers(curDate,[user])
                completedTasks = []
                # pull the list of task ids
                for t in task:
                    if t['userID'] == user:
                        completedTasks = t['completedTasks']
                lstTask = []
                for t in completedTasks:
                    # if the task id already exists then update the values
                    if any(d['taskID'] == t["taskID"] for d in lstTask):
                        for i in lstTask:
                            if i["taskID"] == t["taskID"]:
                                i["totalTime"] = t["totalTime"] + i["totalTime"]
                                i["total"] += 1
                    # otherwise add those values into the dictionary
                    else:
                        dictTask = {}
                        dictTask["taskID"] = t["taskID"]
                        dictTask["totalTime"] = t["totalTime"]
                        dictTask["total"] = 1
                        lstTask.append(dictTask)
                # iterate over the list to calculate the averages for each task and add it to the chart
                for t in lstTask:
                    chart.add(Api.getTaskFromID(t['taskID']), int((t['totalTime']/t['total'])/1000))
                    statistics.append(Api.getTaskFromID(t['taskID']) + ' was completed ' + str(t['total']) + ' time(s).')
                    statistics.append(Api.getTaskFromID(t['taskID']) + ' was uncompleted ' + str(Api.getUncompletedTaskByID(int(user),t['taskID'])) + ' time(s).')
            # display message that they need to select a name or task
            if submit == 'T' and user == 'None' and task == 'None':
                flash("You must select either a Senior Name or a Task before a graph can be generated", "warning")
    chart = chart.render_data_uri()
    return render_template('graph.html', supervisor=supervisorID, user=users, task=tasks, chart=chart, statistics=statistics, display=display)
    
def handle_email(arguments=None):
    """
    Description: generates and sends the pdf to the email assigned to the supervisor
    Parameters: none
    Return Value:
    Author: Patrick Earl
    """
    subject = ""
    if arguments is None:
        subject = "Report for supervisor " + current_user.fname + " " + current_user.lname 
    
    msg = Message(subject,
                sender="kutztms@gmail.com",
                recipients=[current_user.email])

    (supervisorID, users, lstTask, sortedBy, Senior, Constraints) = generate_report(arguments)
    html = render_template('pdf.html', supervisor=supervisorID, user=users, tasks=lstTask, constraint=sortedBy, arguments=arguments)
    pdf = weasyprint.HTML(string=html).write_pdf()
    msg.attach('report.pdf', 'application/pdf', pdf)
    msg.html = "<h3 style='text-align:center;'>Report is as an attached pdf</h3>"
    msg.html += "<span style='text-align:center;'>Time of generation: " + datetime.now().strftime('%m-%d-%Y %H:%M:%S') + "</span>"
    msg.html += "<p style='font-size:8px'>This is an automated message, this email is not monitored</p>"
    mail.send(msg)
    flash("Email send succesfully to " + current_user.email, 'success')
    return redirect(url_for('reports', arguments=arguments))
    
def generate_report(arguments=None):
    """
    Description: hangle the rendering and passing of the data to the reports page
    Parameters: None or Sorted Options
    Return Value: 
        - SupervisorID - The supervisor requesting the report
        - Users - The users that the report is for
        - lstTask - The list of tasks being returned
        - sortedBy - How the report is sorted (User or Time constraint)
    Author: Tyler Lance
    """
    Senior = "Senior Names"
    Constraints = "Constraints"
    # Chose which supervisor the report is being generated for
    #supervisorID = current_user.supervisorID
    supervisorID = current_user.supervisorID
    # pull the list of assigned users to the supervisor
    users =  Api.getAssignedUsers(supervisorID)
    # default date for the data if no date is passed
    date = "2000-01-01"
    # what the data is sorted by
    sortedBy = "Showing all entries by date"
    # pull userIDs from the user data
    lstUserIDs = [li['userID'] for li in users]
    # check if arguments were passed to the url
    if arguments is not None:
        sort = arguments.split(':')[0]
        data = arguments.split(':')[1]
        # check if userID was passed via url and that it wasnt all
        if sort == 'userid' and data != 'A':
            # empties the list of userids and adds in the passed one
            lstUserIDs = []
            lstUserIDs.append(int(data))
            sortedBy = "Showing entries for user: " + Api.getNameFromID(int(data))
            Senior = Api.getNameFromID(int(data))
        elif sort == 'userid' and data == 'A':
            Senior = "All"
        # check if date specified was passed to url
        elif sort == 'date':
            if data == 'M':
                date = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 30 days"
                Constraints = "Monthly"
            elif data == 'W':
                date = str((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last 7 days"
                Constraints = "Weekly"
            elif data == 'D':
                date = str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
                sortedBy = "Showing entries for the last day"
                Constraints = "Daily"
            else:
                Constraints = "All"
    # get completed tasks by passing the list and date
    tasks = Api.getTasksByUsers(date, lstUserIDs)
    lstTask = []
    # create list containing dictionaries for each table row
    for li in tasks:
        for li2 in li["completedTasks"]:
            dictTask = {}
            dictTask["userID"]=Api.getNameFromID(li["userID"])
            dictTask["title"]=li2["title"]
            dictTask["totalTime"]=str(int(li2["totalTime"]/1000)) + " seconds"
            if li2["dateTimeCompleted"] == 'Uncompleted':
                dictTask["dateTimeCompleted"]='Uncompleted'
                # get percentage for uncompleted task steps
                running = 0
                total = 0
                for t in li2["detailedSteps"]:
                    total += 1
                    if t["dateTimeCompleted"] is not None:
                        running += 1
                dictTask["progress"] = str(int((running / total) * 100)) + '%'
            else:
                dictTask["dateTimeCompleted"]=str(li2["dateTimeCompleted"])
                dictTask["progress"]="100%"
            lstTask.append(dictTask)
    # sort the list by date so that the newest entries appear first
    lstTask = sorted(lstTask,key=lambda k: k['dateTimeCompleted'], reverse=True)
    return (supervisorID, users, lstTask, sortedBy, Senior, Constraints)