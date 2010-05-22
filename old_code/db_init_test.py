#!/usr/bin/env python
from config_parse import ParseConfigFile

def init_mysql_db(con):
    cur=con.cursor()
    try:
        cur.execute("""DROP TABLE IF EXISTS units""")
        cur.execute("""create table units (id int(5) auto_increment primary key, unit varchar(50), abbreviation varchar(20), system char(6) default "US")""")
        #table recipes create statement.
        cur.execute("""DROP TABLE IF EXISTS recipes""")
        cur.execute("""create table recipes (id int(10) auto_increment primary key, name varchar(50), type varchar(10), rank int(1) default 1, directions mediumtext, preptime int default 0, cooktime int default 0, description varchar(75) default "");""")
        #table ingredients create line.
        cur.execute("""DROP TABLE IF EXISTS ingredients""")
        cur.execute("""create table ingredients (id int(10) primary key auto_increment, ingredient varchar(75));""")
        #table types create line.
        cur.execute("""DROP TABLE IF EXISTS types""")
        cur.execute("""create table types (id int(5) primary key auto_increment, type varchar(10))""")
        #table category create line.
        cur.execute("""DROP TABLE IF EXISTS category""")
        cur.execute("""create table category (id int(10) primary key auto_increment, category varchar(15))""")
        #table category_map
        cur.execute("""DROP TABLE IF EXISTS category_map""")
        cur.execute("""create table category_map (id int(10) primary key auto_increment, category_id int(10))""")
        #table ingredient_map
        cur.execute("""DROP TABLE IF EXISTS ingredient_map""")
        cur.execute("""create table ingredient_map (recipe_id int(10), amount varchar(75), unit_id int(10), ingredient_id int(10), notes varchar(75))""")
    except MySQLdb.Error,e:
        cur.execute("""ROLLBACK""")
        print "rolling back"
        print (e.args)
    else:
        cur.commit()
    for type in ("Breakfast", "Lunch", "Dinner", "Dessert"):
        try:
            cur.execute("""INSERT INTO types (type) VALUES (%s)""", type)
        except MySQLdb.Error,e:
            cur.rollback()
            print "rolling back"
            print (e.args)
        else:
            cur.commit()


def init_psql_db(con):
    cur=con.cursor()
    try:
        #drop the tables we care about...
        #order is important here.
        cur.execute("""DROP TABLE IF EXISTS category_map""")
        cur.execute("""DROP TABLE IF EXISTS ingredient_map""")
        cur.execute("""DROP TABLE IF EXISTS units""")
        cur.execute("""DROP TABLE IF EXISTS ingredients""")
        cur.execute("""DROP TABLE IF EXISTS categories""")
        cur.execute("""DROP TABLE IF EXISTS recipes CASCADE""")
        cur.execute("""DROP TABLE IF EXISTS types""")
        #now add them back. Order is important.
        #types
        cur.execute("CREATE TABLE types (\
                        type_id serial PRIMARY KEY,\
                        type varchar(10) NOT NULL UNIQUE)"
                   )
        #units
        cur.execute("CREATE TABLE units (\
                        unit_id serial PRIMARY KEY,\
                        unit varchar(20) NOT NULL UNIQUE)"
                   )
        #categories
        cur.execute("CREATE TABLE categories (\
                        category_id serial PRIMARY KEY,\
                        category varchar(20) NOT NULL UNIQUE)"
                   )
        #ingredients
        cur.execute("CREATE TABLE ingredients (\
                        ingredient_id serial PRIMARY KEY,\
                        ingredient varchar(30) NOT NULL UNIQUE)"
                   )
        #recipes
        cur.execute("CREATE TABLE recipes (\
                        recipe_id serial PRIMARY KEY,\
                        name varchar(50) NOT NULL,\
                        description text NOT NULL,\
                        directions text NOT NULL,\
                        type integer REFERENCES types\
                         ON DELETE RESTRICT NOT NULL,\
                        rating integer NOT NULL CHECK\
                         (rating >0 and rating <6),\
                        prep_time char(5) NOT NULL DEFAULT '00:10',\
                        cook_time char(5) NOT NULL DEFAULT '00:30')"
                   )
        cur.execute("CREATE TABLE category_map (\
                        recipe_id integer REFERENCES recipes\
                         ON DELETE CASCADE NOT NULL,\
                        category_id integer REFERENCES categories\
                         ON DELETE RESTRICT NOT NULL)"
                   )
        cur.execute("CREATE TABLE ingredient_map (\
                        recipe_id integer REFERENCES recipes\
                         ON DELETE CASCADE NOT NULL,\
                        amount varchar(10) NOT NULL,\
                        unit_id integer REFERENCES units\
                         ON DELETE RESTRICT NOT NULL,\
                        ingredient_id integer REFERENCES ingredients\
                         ON DELETE RESTRICT NOT NULL,\
                        notes varchar(40) DEFAULT '')"
                   )
                        
    except pgdb.DatabaseError,e:
        con.rollback()
        print "rolling back because of:",e
    else:
        con.commit()
        types=[["Breakfast",], ["Lunch",], ["Dinner",], ["Dessert",]]
        try:
            cur.executemany("""INSERT INTO types (type) VALUES (%s)""", types)
        except pgdb.DatabaseError,e:
            con.rollback()
            print "rolling back because of:",e
        else:
            con.commit()
    finally:
        cur.close()
        con.close()
        


if __name__ == "__main__":
    default_options=dict(
        database_host="foo.foo.org",
        database_uid="anon",
        database_passwd="12345",
        database_db="foo",
        database_type="postgres"
    )
    
    paths=["/etc/rms/rms.conf","/home/cynyr/.config/rms/rms.conf","./rms.conf"]
    options=ParseConfigFile(paths,default_options)

    if options['database_type'].lower() == "mysql":
        try:
            import MySQLdb
        except ImportError, e:
            print e
        else:
            try:
                con=MySQLdb.connect(host=options['database_host'],\
                                    db=options['database_db'],\
                                    user=options['database_uid'],\
                                    passwd=options['database_passwd'])
            except MySQLdb.Error,e:
                print e.args
                #print "could not connect to db"
    elif options['database_type'].lower() == "postgres":
        try:
            import pgdb
        except ImportError, e:
            print e
        else:
            try:
                con=pgdb.connect(host=options['database_host'],
                                 database=options['database_db'],
                                 user=options['database_uid'],
                                 password=options['database_passwd'],
                                )
            except pg.DatabaseError,e:
                print e
    else:
        print "Unsupported Database, try again later."


    ans=raw_input("This will erase all data in the database '" + options['database_db'] + "' [Yes/No] ") 
    
    if ans.lower() == "yes":
        print "resetting the DB"
        if options['database_type'].lower() == "postgres":
            init_psql_db(con)
        if options['database_type'].lower() == "mysql":
            init_mysql_db(con)
    else:
        print "Saving the DB"
    #cur.execute("""  """)
