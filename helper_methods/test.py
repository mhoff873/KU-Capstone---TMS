#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:38:08 2018

@author: nyost
"""

"""INSERT INTO supervisors
        (email, password, fname, mname,
         lname, isLoggedIn, dateCreated, gender,
         active, birthday, ethnicity, picture, affiliation, phone)
        VALUES
        ('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', %s, '%s', '%s', '%s',
        '%s', %s)
        """

import UserMgmt
import mysql.connector
DB_HOST, DB_NAME, DB_PORT = ["localhost", "tmst_db", "3306"]
TIME_OUT = 5


def connect():
    """
    Connects to database, and returns a db object.
    :return: db object that is used to access the database, or None if
                connection fails.
    """
    DB_USER = input("Username: ")
    DB_PASS = input("Pass: ")
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER,
                                       password=DB_PASS, database=DB_NAME,
                                       port=DB_PORT,
                                       connection_timeout=TIME_OUT)
    except Exception:
        return None
db = connect()
if db:
    user = [1, "testemail@gmail.com", "password", 444444444, "first", "middle", "last", "N/A", "NULL", "Kutztown", "white", 1, 0, "NULL", "NULL", "NULL"]
    supervisor = ["testemail@gmail.com", "password", "first", "middle", "last", 0, "NULL", "male", 1, "NULL", "white", "NULL", "Kutztown", 4444444444]
    UserMgmt.create_test(db, user, UserMgmt.USER)
    if UserMgmt.user_exists(db, user[1], UserMgmt.USER):
        print("Created successfully!")
    else:
        print("Could not find user!")
        
    UserMgmt.create_test(db, supervisor, UserMgmt.SUPERVISOR)
    if UserMgmt.user_exists(db, supervisor[0], UserMgmt.SUPERVISOR):
        print("Created successfully!")
    else:
        print("Could not find user!")
else:
    print("Error: could not connect to database!")