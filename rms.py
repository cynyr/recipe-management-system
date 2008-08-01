#!/usr/bin/env python

import pygtk,gtk,gtk.glade,MySQLdb,gobject,os,string
#import config_parse.ParseConfigFile as ParseConfigFile
from config_parse import ParseConfigFile

class add_new_recipe:
    """A window and functions to add a new recipe"""

    def __init__(self, runaslib=True, update=False, rid=None):
        """Set up the enter new recipie window

        This creates new recipie window. It connects to the database
        and sets up the cursor. It populates a dropdown from
        data in the database.

        """
        
        #set up some default vars
        self.categories=[]
        self.update=update
        self.recipe_id=rid


        #debugging output print whether to update and the rid
        #print (self.update,self.recipe_id)
        # Load Glade XML
        self.xml = gtk.glade.XML("rms_ui.glade")
        self.w = self.xml.get_widget('window1')
        #connect to some windowing events, noteably the close of our window.
        self.xml.signal_connect('on_window1_destroy' , self.exit)
        self.xml.signal_connect('on_window1_keypress' , self.keypress)
        self.xml.signal_connect('on_submit_clicked' , self.submit)
        
        #connect to the DB and get a cursor
        #self.con=MySQLdb.connect(host="localhost", db="rms", user="cynyr", passwd="abbg")
        #opions is the global var with the options in it.
        self.con=MySQLdb.connect(host=options['database_host'],\
                                 db=options['database_db'],\
                                 user=options['database_uid'],\
                                 passwd=options['database_passwd'])
        self.cur=self.con.cursor()
        

        if self.update: 
            self.get_current_data() #populate stuff to use, catagories, types, etc
        self.do_categories()

        #------------------------------------------------
        #How to add things to a combo list or comboentry
        #------------------------------------------------
        self.ce = self.xml.get_widget("ce_types")
        self.l = gtk.ListStore(gobject.TYPE_STRING) #Make a new liststore
        #Get some data
        self.cur.execute("""select type from types order by type""")
        position=0
        place=0
        for row in self.cur:
            #print row
            self.l.append([row[0]]) #Each line needs to be a list
            if self.update and row[0] == self.current_values['type'] :
                position=place
        self.ce.set_model(self.l) #set the model to the list
        self.ce.set_text_column(0) #use the first entry in the list of lists.
        if self.update:
            self.ce.set_active(position)
        else:
            self.ce.set_active(2)
        #-----------------------
        #----End of example-----
        #-----------------------
        if self.update:
            #set the name field to the name
            self.xml.get_widget("e_name").set_text(self.current_values['name'])
            #setting the ingredents textview string
            self.tv_ing=self.xml.get_widget("tv_ing")
            self.tb_ing=self.tv_ing.get_buffer()
            self.tb_ing.set_text(self.current_values["ingredents"])
            #setting the directions textview string
            self.tv_dir=self.xml.get_widget("tv_dir")
            self.tb_dir=self.tv_dir.get_buffer()
            self.tb_dir.set_text(self.current_values['directions'])
            #setting the rating
            self.sb_rating=self.xml.get_widget("sb_rating")
            self.sb_rating.set_value(self.current_values['rank'])
            self.sb_rating.update()

        self.w.show_all()
        if self.update:
            self.xml.get_widget("b_submit").hide()

    def get_current_data(self):
        self.cur.execute("""Select name,type,rank,directions from recipes where id=%s""", (self.recipe_id,))
        self.info=self.cur.fetchall()[0]
        #print self.info
        self.current_values={}
        self.current_values['name']=self.info[0]
        self.current_values['type']=self.info[1]
        self.current_values['rank']=int(self.info[2])
        self.current_values['directions']=self.info[3]
        self.ingredents_strings=[]
        self.cur.execute("""SELECT amount,unit_id,ingredent_id,notes from ingredent_map where recipe_id=%s""",(self.recipe_id,))
        self.cur_ing=self.cur.fetchall()
        for cur_ing_line in self.cur_ing:
            #cur_ing_line  (0,     1,      2,              3)
            #              (amount,unit_id,ingredent_id,   notes)
            self.cur.execute("""SELECT unit FROM units where id=%s""",\
                             (cur_ing_line[1],))
            unit_name=self.cur.fetchall()[0][0]
            self.cur.execute("""SELECT ingredent FROM ingredents where id=%s"""\
                             , (cur_ing_line[2],))
            ingredent_name=self.cur.fetchall()[0][0]
            new_string=cur_ing_line[0] + "," + unit_name + "," + ingredent_name\
                            + "," + cur_ing_line[3].strip() + "\n"
            self.ingredents_strings.append(new_string)
        self.current_values["ingredents"]="".join(self.ingredents_strings)
        self.current_values["catagories"]=[]
        self.cur.execute("""SELECT category_id FROM category_map WHERE id=%s"""\
                         , (self.recipe_id,))
        cur_cat_ids=self.cur.fetchall()
        for id in cur_cat_ids:
            id=id[0]
            self.cur.execute("""SELECT category FROM category WHERE id=%s""",\
                                (id,))
            cur_category=self.cur.fetchone()[0]
            self.current_values["catagories"].append(cur_category)
        #print self.current_values


    def do_categories(self):
        
        #make some checkboxes
        self.vb_cat=self.xml.get_widget('vb_cat')
        self.cur.execute("""select category from category order by category""")
        self.column=999
        for category in self.cur:
            #create a new checkbutton with a label
            self.cb_label=str(category[0])
            self.cb=gtk.CheckButton(label=self.cb_label)
            #hook it's clicked event.
            self.cb.connect("clicked", self.cb_clicked, self.cb_label)
            if self.column > 3: #set to number of columns - 1
                #Create a new hbox
                self.hb=gtk.HBox(True, 0) #create a hbox
                self.vb_cat.add(self.hb) 
                self.column=1 #reset the column count.
                self.hb.add(self.cb)
            else:
                self.hb.add(self.cb)
                self.column = self.column +1
            if self.update and \
             self.cb_label in self.current_values["catagories"]:
                self.cb.set_active(True)
                
        self.e_new_cat=gtk.Entry()
        self.e_new_cat.set_tooltip_text("a comma seperated list of categories")
        self.hb=gtk.HBox(False, 0)
        self.vb_cat.add(self.hb)
        self.hb.add(gtk.Label("Add a new category(s):"))
        self.hb.add(self.e_new_cat)
        
    def cb_clicked(self,widget,name):
        """This is the function to add catagories"""

        #name = widget.get_label() #not needed since data is now being passed
        if widget.get_active():
            print name + " checked"
            self.categories.append(name)
        else:
            self.categories.remove(name)
    def submit(self,widget):
        """Add or modify a recipe to or in the database

        This function adds a recipe the database and extracts needed info
        from the database as well. Needed info is the Max ID number so this
        ones can be found. Also each ingredent and unit ID is needed.

        """
        
        #----Start get Name----
        self.name=self.xml.get_widget("e_name").get_text()
        #print "name: " + self.name
        #----End name-----

        #----Start get type-----
        type=self.xml.get_widget("ce_types").get_active_text()
        #print "type: " + type
        #----End get type-----

        #----Start get rating-----
        rating=self.xml.get_widget("sb_rating").get_value_as_int()
        #print "rating: " + str(rating)
        #----End get rating-----

        #----Start new categories-----
        for cat in self.e_new_cat.get_text().split(','):
            cat=string.capwords(cat)
            if cat != "":
                self.categories.append(cat)
                #print "insert into category (category) values (%s)" % (cat,)
                self.cur.execute("insert into category (category) values (%s)",(cat,))
        #----End new categories-----

        #----Start Getting directions text-----
        self.tb_dir=self.xml.get_widget("tv_dir").get_buffer()
        self.dir_text=self.tb_dir.get_text(self.tb_dir.get_start_iter(), 
                                            self.tb_dir.get_end_iter())
        #----End of directions text-----

        #----Start of getting ingredents text----
        self.tb_ing=self.xml.get_widget("tv_ing").get_buffer()
        self.ing_text=self.tb_ing.get_text(self.tb_ing.get_start_iter(), 
                                            self.tb_ing.get_end_iter())
        #----End of ingredents text-----

        #----Start recipie insert-----
        self.cur.execute("insert into recipes (name,type,rank,directions) VALUES (%s,%s,%s,%s)",(self.name,type,rating,self.dir_text))
        #----Start recipe_id-----
        #self.cur.execute("""select max(id) from recipes""")
        #result=self.cur.fetchmany(1)[0][0]
        #if result==None:
            #self.recipe_id=1
        #else:
            #self.recipe_id=int(result[0])+1
        self.cur.execute("""select id from recipes where name=%s""", (self.name,))
        possible_ids=self.cur.fetchall()
        #print possible_ids
        self.recipe_id=1
        for self.ids in possible_ids:
            self.new_id=self.ids[0]
            print self.new_id
            if self.recipe_id < self.new_id:
                self.recipe_id=self.new_id
        #----End of recipe_id-----

        #-----Start ingredent_map inserts-----
        for line in self.ing_text.split('\n'):
            if line == "":
                break
            else:
                data=line.split(',')
                """ notes for the fields in data
                    0           1       2           3+
                    ammount,    units,  ingredent,  notes"""

                #----Start get ingredent_id-----
                data[0]=data[0].strip()
                data[1]=data[1].strip()
                data[2]=data[2].strip()
                self.cur.execute("select id from ingredents where ingredent=%s", (data[2],))
                ingredent_id=self.cur.fetchone()
                print ingredent_id
                if ingredent_id==None:
                    self.cur.execute("""INSERT INTO ingredents (ingredent) VALUES (%s)""", (data[2],))
                    #self.cur.execute("SELECT MAX(id) from ingredents")
                    self.cur.execute("""SELECT id from ingredents where ingredent=%s""", (data[2],))
                    #ingredent_id=self.cur.fetchone()[0] + 1
                    ingredent_id=self.cur.fetchone()[0]
                else:
                    ingredent_id=ingredent_id[0]
                #----End of ingredent_id-----

                #----Start of unit_id-----
                self.cur.execute("SELECT id FROM units WHERE unit=%s or abbreviation=%s", (data[1],data[1]))

                unit_id=self.cur.fetchone()
                if unit_id == None:
                    self.cur.execute("""INSERT INTO units (unit) VALUES (%s)""", (data[1],))
                    #self.cur.execute("SELECT MAX(id) from units")
                    self.cur.execute("""SELECT id FROM units WHERE unit=%s""", (data[1],))
                    #NEED TO ADD THE FETCH AND GETTING THE ID
                    #unit_id=self.cur.fetchone()[0] + 1
                    unit_id=self.cur.fetchone()[0]
                else:
                    unit_id=unit_id[0]
                #----End of unit_id-----

                #----Start of Notes-----
                if len(data) < 4:
                    notes=""
                else:
                    notes="".join(data[3:])
                #----End of Notes-----

                print "insert into ingredent_map (recipe_id,amount,unit_id,\
                       ingredent_id,notes) values (%s, %s, %s, %s, %s)" % \
                       (self.recipe_id, data[0], unit_id, ingredent_id, notes)

                self.cur.execute("insert into ingredent_map (recipe_id,amount,unit_id, ingredent_id,notes) values (%s, %s, %s, %s, %s)", (self.recipe_id, data[0], unit_id, ingredent_id, notes))
        #-----End ingredent map inserts-----


        #-----Start categories inserts-----
        for cat in self.categories:
            self.cur.execute("select id from category where category=%s",
                                (cat,))
            cat_id=self.cur.fetchone()[0]
            print 'insert into category_map (id,category_id) values (%s,%s)' % (self.recipe_id, cat_id) 
            self.cur.execute("insert into category_map (id,category_id) values (%s,%s)",(self.recipe_id, cat_id) )
        #-----End categories inserts-----
        #print self.dir_text
        self.window.hide()
        self.window.destroy()
        

            

    def keypress(self,widget,data):
        key = gtk.gdk.keyval_name(data.keyval)
        print key
        if key == "Return":
            print self.categories

    def exit(self,widget):
        """quit"""
        self.w.hide()
        main_window.window.show()
        #__main__.home_window.window.show()
        #gtk.main_quit()

class home_window:
    """The home window that allows basic searching and adding of recipies"""
    
    def __init__ (self, runaslib=True):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.exit)
        self.search_entry=gtk.Entry()
        self.vbox=gtk.VBox()
        self.hbox=gtk.HBox()
        self.label=gtk.Label("Enter name to search for here: ")
        self.hbox.add(self.label)
        self.hbox.add(self.search_entry)
        self.vbox.add(self.hbox)
        self.b_submit=gtk.Button("Submit")
        self.b_submit.connect("clicked", self.submit_clicked)
        self.vbox.add(self.b_submit)
        self.b_add_new=gtk.Button("Add new Recipe")
        self.b_add_new.connect("clicked", self.add_clicked)
        self.vbox.add(self.b_add_new)
        #self.b_show_rid1=gtk.Button("show recipe #11")
        #self.b_show_rid1.connect("clicked", self.show_recipe)
        #self.vbox.add(self.b_show_rid1)
        self.window.add(self.vbox)
        self.window.show_all()
        #gtk.main()

    def start_main_loop(self,):
        gtk.main()
    def submit_clicked(self,widget):
        self.searchstring=self.search_entry.get_text()
        print self.searchstring
        self.search=search_results_window(searchline=self.searchstring)
    def add_clicked(self, widget):
        self.window.hide()
        add_new_window= add_new_recipe()
    def show_recipe(self,widget,s_rid=11):
        recipe=add_new_recipe(update=True, rid=s_rid)
    def exit(self,widget):
        gtk.main_quit()

class search_results_window:
    """A results window for a searching for a recipe"""

    def __init__ (self, searchline=""):
        main_window.window.hide()
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.exit)
        self.vbox=gtk.VBox(True,0)
        self.window.add(self.vbox)

        self.con=MySQLdb.connect(host=options['database_host'],\
                                 db=options['database_db'],\
                                 user=options['database_uid'],\
                                 passwd=options['database_passwd'])
        self.cur=self.con.cursor()
        searchline="%" + searchline + "%"
        self.cur.execute("""SELECT id,name FROM recipes WHERE name LIKE %s""",\
                         (searchline,))
        results=self.cur.fetchall()
        print results
        for button_data in results:
            self.b=gtk.Button(button_data[1])
            self.b.connect("clicked", self.show_recipe, button_data[0])
            self.vbox.add(self.b)
        self.window.show_all()

    def show_recipe(self,widget,data):
        self.window.hide()
        recipe=add_new_recipe(update=True,rid=data)

    def exit(self, widget):
        main_window.window.show()
    

    
if __name__ == '__main__':
    default_options=dict(
        database_host="foo.foo.org",
        database_uid="anon",
        database_passwd="12345",
        database_db="foo",
    )
    paths=["/etc/rms/rms.conf","/home/cynyr/.config/rms/rms.conf",]
    options=ParseConfigFile(paths,default_options)
    main_window=home_window()
    main_window.start_main_loop()
