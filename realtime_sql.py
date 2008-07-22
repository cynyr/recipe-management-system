#!/usr/bin/env python
# A minimal SQLite shell for experiments

import MySQLdb

con = MySQLdb.connect(host="localhost", user="cynyr", passwd="abbg", db="rms")
cur = con.cursor()

buffer = ""

print "Enter your SQL commands to execute in mysql."
print "Enter a blank line to exit."

while True:
    line = raw_input()
    if line == "":
        break
    buffer += line
    buffer = buffer.strip()
    try:
        cur.execute(buffer)
    except MySQLdb.ProgrammingError, e:
        print "An error occurred:", e.args
    if buffer.lstrip().upper().startswith("SELECT"):
        print cur.fetchall()
    buffer = ""

con.close()
