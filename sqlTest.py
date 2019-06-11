#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 08:58:12 2019

@author: ahir.chatterjee
"""

import sqlite3

connection = sqlite3.connect("scrims.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE scrim;")

command = """
CREATE TABLE scrim (
date DATE,
opponent VARCHAR(20),
result CHAR(1),
gameTime TIME,

patch VARCHAR(5));
"""
cursor.execute(command)

scrimData = [("Fnatic","W","2019-06-05","9.11"),
             ("Origen","L","test","9.11"),
             ("Rogue","W","2019-06-05","9.11"),
             ("G2","L","2019-06-06","9.11"),
             ("Misfits Academy","W","2019-06-06","9.11")]

format_str = """INSERT INTO scrim (scrimNumber, opponent, result, date, patch)
    VALUES (NULL, "{opp}", "{res}", "{date}", "{patch}");"""
for scrim in scrimData:
    command = format_str.format(opp=scrim[0],res=scrim[1],date=scrim[2],patch=scrim[3])
    cursor.execute(command)
    
cursor.execute("SELECT * FROM scrim") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("""SELECT opponent FROM scrim WHERE result = "W" """) 
res = cursor.fetchall() 
for r in res:
    print(r)