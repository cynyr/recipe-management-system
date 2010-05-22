#!/usr/bin/env python
# A minimal SQLite shell for experiments

try:
    import pgdb
except:
    print "need pgdb"


con = pgdb.connect(
                        host="madadh",
                        user="rms", 
                        password="rmsiscool", 
                        database="rms",
                      )
#cur = con.cursor() #normal cursor, returns tupels
cur = con.cursor()
print con,cur

buffer = ""

print "Enter your SQL commands to execute in mysql."
print "Enter a blank line to exit."

while True:
    line = raw_input()
    if line == "":
        break
    buffer += line
    buffer = buffer.strip()
    cur.execute(buffer)
    if buffer.lstrip().upper().startswith("SELECT"):
        print cur.fetchall()
    buffer = ""
con.commit()
con.close()
