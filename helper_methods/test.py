#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:38:08 2018

@author: nyost
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
    email = "testemail@gmail.com"
    user = list(UserMgmt.get_user(db, email, UserMgmt.USER))
    supervisor = list(UserMgmt.get_user(db, email,
                                        UserMgmt.SUPERVISOR))

    supervisor[3] = "Donald"
    supervisor[4] = "John"
    supervisor[5] = "Trump"
    UserMgmt.edit_user(db, email, supervisor, UserMgmt.SUPERVISOR)
    db.close()
else:
    print("Error: could not connect to database!")