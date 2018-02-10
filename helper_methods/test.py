#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:38:08 2018

@author: nyost
"""
import DB_Functions
import UserMgmt
DB_HOST, DB_NAME, DB_PORT = ["localhost", "tmst_db", "3306"]
TIME_OUT = 5


db = DB_Functions.connect()
if db:
    print("Connected!")
    email = "pearl464@live.kutztown.edu"
    users = UserMgmt.get_assigned_users(db, email)
    for user in users:
        print(user[2])
    db.close()
    print("Closing DB")
else:
    print("Error: could not connect to database!")
