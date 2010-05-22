#!/usr/bin/env python

try:
    import MySQLdb
except:
    print "no module found with that name."

db = MySQLdb.connect(host="localhost", user="cynyr", passwd="abbg", db="rms")
cursor=db.cursor()

cursor.execute("""drop table test""")
cursor.execute("""create table test (firstname varchar(50),lastname varchar(50))""")
try:
    cursor.execute("""insert into test (firstname,lastname) VALUES ("john","smith")""")
except MySQLdb.Error, e:
    print "An error occurred:", e.args

#cursor.execute( """select %s from test""" , (t,))
#cursor.execute("""select firstname,lastname from test where firstname="john" """)
#for line in cursor.fetchall():
    #if line == None:
        #print "none"
    #else:
        #print line
#print cursor.fetchall()
cursor.execute("""Select id from units where unit=%s""", ('cups',))
cfa=cursor.fetchall()
if cfa != ():
    for line in cfa:
        print line
        print line[0]+1
else:
    print "No results"
