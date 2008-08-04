#!/usr/bin/env python
import MySQLdb
from config_parse import ParseConfigFile

def init_db(cur):
    cur.execute("""create table units (id int(5) auto_increment primary key, unit varchar(50), abbreviation varchar(20), system char(6) default "US")""")

default_options=dict(
    database_host="foo.foo.org",
    database_uid="anon",
    database_passwd="12345",
    database_db="foo",
)
paths=["/etc/rms/rms.conf","/home/cynyr/.config/rms/rms.conf","./rms.conf"]
options=ParseConfigFile(paths,default_options)
try:
    con=MySQLdb.connect(host=options['database_host'],\
                                 db=options['database_db'],\
                                 user=options['database_uid'],\
                                 passwd=options['database_passwd'])
except:
    print "could not connect to db"
cur=con.cursor()
cur.execute("""  """)
