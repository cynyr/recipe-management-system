#!/usr/bin/env python
import MySQLdb
from config_parse import ParseConfigFile

def init_db(cur):
    cur.execute("""BEGIN""")
    try:
        cur.execute("""DROP TABLE units IF EXISTS""")
        cur.execute("""create table units (id int(5) auto_increment primary key, unit varchar(50), abbreviation varchar(20), system char(6) default "US")""")
        #table recipes create statement.
        cur.execute("""DROP TABLE recipes IF EXISTS""")
        cur.execute("""create table recipes (id int(10) auto_increment primary key, name varchar(50), type varchar(10), rank int(1) default 1, directions mediumtext, preptime int default 0, cooktime int default 0, description varchar(75) default "");""")
        #table ingredients create line.
        cur.execute("""DROP TABLE ingredients IF EXISTS""")
        cur.execute("""create table ingredients (id int(10) primary key auto_increment, ingredient varchar(75));""")
        #table types create line.
        cur.execute("""DROP TABLE types IF EXISTS""")
        cur.execute("""create table types (id int(5) primary key auto_increment, type varchar(10))""")
        #table category create line.
        cur.execute("""DROP TABLE units IF EXISTS""")
        cur.execute("""create table category (id int(10) primary key auto_increment, category varchar(15))""")
        #table category_map
        cur.execute("""DROP TABLE units IF EXISTS""")
        cur.execute("""create table category_map (id int(10) primary key auto_increment, category_id int(10))""")
        #table ingredient_map
        cur.execute("""DROP TABLE units IF EXISTS""")
        cur.execute("""create table ingredient_map (recipe_id int(10), amount varchar(75), unit_id int(10), ingredent_id int(10), notes varchar(75))""")
    except MySQLdb.Error,e:
        cur.execute("""ROLLBACK""")
        print "rolling back"
        print (e.args)
    for type in ("Breakfast", "Lunch", "Dinner", "Dessert"):
        try:
            cur.execute("""INSERT INTO types (type) VALUES (%s)""", type)
        except MySQLdb.Error,e:
            cur.execute("""ROLLBACK""")
            print "rolling back"
            print (e.args)

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
except MySQLdb.Error,e:
    print e.args
    #print "could not connect to db"

cur=con.cursor()
print options
init_db(cur)
#cur.execute("""  """)
