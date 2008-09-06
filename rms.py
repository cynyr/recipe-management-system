#!/usr/bin/env python
#A recipe managment system
#Written by Andrew Frink Andrew.Frink@gmail.com
#licensed under GPLv2 or later at your option.
#There isn't a home page yet.

class base_recipe_window:
    """A window and functions to add a new recipe"""

    def __init__(self):
        """Set up the enter new recipie window

        This creates new recipie window. It connects to the database
        and sets up the cursor. It populates a dropdown from
        data in the database. Closes the cursor when finished.

        """
        #Load Glade XML
        self.xml = gtk.glade.XML("rms_ui.glade")
        self.w = self.xml.get_widget('window1')
        #Make sure that we "exit" when the window is closed
        self.xml.signal_connect('on_window1_destroy' , self.exit)
        
        self.cur=con.cursor()
        
        #add known categories to the window.
        self.do_categories()
        #add types to the window
        self.do_types()

        self.w.show_all()
        self.cur.close()

    def do_types(self):
        """Get the current types, and add them to the drop down.

        Go and get the current types and fill out the combo box.
        Create a liststore, populate it with the current types and 
        then set the liststore to use column 0 and set the active one.
        """
        #------------------------------------------------
        #How to add things to a combo list or comboentry
        #------------------------------------------------
        self.ce = self.xml.get_widget("ce_types")
        self.l = gtk.ListStore(gobject.TYPE_STRING) #Make a new liststore
        #Get some data
        self.cur.execute("""select type from types order by type""")
        for row in self.cur.fetchall():
            self.l.append([row[0]]) #Each line needs to be a list
        self.ce.set_model(self.l) #set the model to the list
        self.ce.set_text_column(0) #use the first entry in the list of lists.
        self.ce.set_active(2)
        #-----------------------
        #----End of example-----
        #-----------------------

    def do_categories(self):
        """Fills out the area that shows the categories"""

        #get the vbox that will hold all of the categories
        self.vb_cat=self.xml.get_widget('vb_cat')
        #get all of the categories
        self.cur.execute(
            """SELECT category FROM categories ORDER BY category""")
        #make a list of the results
        categories=list(self.cur.fetchall())
        #set the number of categories wide
        self.width=4
        while len(categories):
            self.hb=gtk.HBox(True, 0) #create a hbox
            self.vb_cat.add(self.hb)
            for column in range(self.width):
                if len(categories):
                    #set the lable to the one given to us.
                    self.cb_label=categories.pop(0)[0]
                    #create a checkbutton with that label
                    self.cb=gtk.CheckButton(self.cb_label)
                else:
                    self.cb=gtk.Label("")
                self.hb.add(self.cb)
        #make an entry widget and a label and add it to the vbox
        self.e_new_cat=gtk.Entry()
        self.e_new_cat.set_tooltip_text("a comma seperated list of categories")
        self.hb=gtk.HBox(False, 0)
        self.vb_cat.add(self.hb)
        self.hb.add(gtk.Label("Add a new category(s):"))
        self.hb.add(self.e_new_cat)
        
    def get_active_categories(self):
        """Returns a list of the names of the currently checked categories"""
        l=[]
        for hbox in self.vb_cat.get_children():
            for cb in hbox.get_children():
                if hasattr(cb, "get_active"):
                    if cb.get_active():
                        l.append(cb.get_label())
        return l
    def get_new_categories(self):
        """Return a list of the new categories

        Parse the entry widget text and add them to the DB
        and return them as a list
        """
        l=[]
        for cat in [x.strip() for x in self.e_new_cat.get_text().split(",")]:
            if cat != "":
                l.append(string.capwords(cat))
        if len(l) >0:
            self.add_new_categories(l)
        return l
    
    def get_current_categories(self):
        """returns a list of both the active and the new categories"""
        l=self.get_active_categories()
        l.extend(self.get_new_categories())
        return l
    
    def add_new_categories(self,cats):
        """add_new_categories(list())
        
        Adds the list as categories to the DB as categories"""
        self.cur.executemany("INSERT INTO categories (category) VALUES (%s)",\
                              [[x] for x in cats])
    def get_tv_text(self,tv):
        """get all the text from a textview
           
           Either look for a widget in the glade file by the name if a string
           or assume it is a textview and use that."""
        if type(tv) == type(""):
            tb=self.xml.get_widget(tv).get_buffer()
        else:
            tb=tv.get_buffer()
        text=tb.get_text(tb.get_start_iter(), tb.get_end_iter())
        return text
        
    def add_unit(self, unit):
        """add_unit("unit")
        
        Add a new unit to the database with the name unit
        """
        try:
            self.cur.execute("""INSERT INTO units (unit) VALUES (%s)""",(unit,))
        except:
            print "add unit failed"
            return False
        else:
            return True

    def get_unit_id(self,unit,add=True):
        """get_unit_id("unit" add=True)
        
        Get the ID of the unit "unit". If add is True, add it to the DB
        using add_unit("unit") if we can't find it.
        """
        self.cur.execute("""SELECT unit_id FROM units WHERE unit=%s""", [unit])
        result=self.cur.fetchone()
        if result == None:
            if add:
                if self.add_unit(unit):
                    self.cur.execute("""SELECT unit_id FROM units WHERE unit=%s""", [unit])
                    u_id=self.cur.fetchone()[0]
                else:
                    u_id=None
            else:
                u_id=None
        else:
            u_id=result[0]

        return u_id

    def add_ingredient(self,ingredient):
        """add_ingredient("ingredient")
        
        Adds the ingredient to the Database.
        """
        try:
            self.cur.execute(
                """INSERT INTO ingredients (ingredient) VALUES (%s)""",
                (ingredient,))
        except:
            print "add ingredent failed"
            return False
        else:
            return True

    def get_ingredent_id(self, ingredient, add=True):
        """get_ingredient_id("ingredient" add=True)

        Gets the ID of an ingredient matching "ingredient". If add is true,
        "ingredient" will be added to the database using add_ingredient()
        """
        self.cur.execute("""SELECT ingredient_id FROM ingredients WHERE ingredient=%s""",
                         (ingredient,))
        result=self.cur.fetchone()
        if result == None:
            if add:
                if self.add_ingredient(ingredient):
                    self.cur.execute(
                        """SELECT ingredient_id FROM ingredients WHERE ingredient=%s""",
                        (ingredient,))
                    i_id=self.cur.fetchone()[0]
                else:
                    i_id=None
            else:
                i_id=None
        else:
            i_id=result[0]

        return i_id
    
    def get_type_id(self, type):
        """get_type("type')

        Get the ID for "type", currently there is no add_type().
        """
        self.cur.execute("""SELECT type_id FROM types WHERE type=%s""",(type,))
        result=self.cur.fetchone()
        return result[0]

    def get_form_data(self):
        """get_form_data()

        Gets the current values from the recipe_window and returns a dictionary.
        with the following keys:
        type                The text form of the type
        type_id             The Type ID from get_type_id()
        rating              The int of the rating
        categories          A list of categories from get_current_categories()
        directions          The text from the directions textview
        description         The text from the description textview
        ingredients_text    The text from the ingredients textview
        ingredients_list    A list of lists from parse_ingredients()
        prep_time           'hh:mm' preperation time
        cook_time           'hh:mm' cooking time
        """
        data={}
        #get the name
        data['name']=string.capwords(self.xml.get_widget("e_name").get_text().strip())
        #get the type
        data['type']=self.xml.get_widget("ce_types").get_active_text()
        data['type_id']=self.get_type_id(data['type'])
        #get the rating
        data['rating']=self.xml.get_widget("sb_rating").get_value_as_int()
        #get categories
        data['categories']=self.get_current_categories()
        #get directions text
        data['directions']=self.get_tv_text("tv_dir")
        #get description text
        data['description']=self.get_tv_text("tv_desc")
        #get ingredents text
        data['ingredients_text']=self.get_tv_text("tv_ing").strip('\n')
        data['ingredients_list']=\
            self.parse_ingredients(data['ingredients_text'])
        ctime_hours=self.xml.get_widget("sb_ctime_hours").get_value_as_int()
        ctime_min=self.xml.get_widget("sb_ctime_minutes").get_value_as_int()
        data['cook_time']=str(ctime_hours) + ':' + str(ctime_min)
        ptime_hours=self.xml.get_widget("sb_ptime_hours").get_value_as_int()
        ptime_min=self.xml.get_widget("sb_ptime_minutes").get_value_as_int()
        data['prep_time']=str(ptime_hours) + ':' + str(ptime_min)
        return data

    def parse_ingredients(self,txt):
        """Parse text and return a list of lists for each line.

        Each line becomes a a list; _amount,unit,ingredent,notes. 
        If there are no notes, add a empty string to the end. 
        """
        l=[]
        for line in txt.split('\n'):
            #split the line on commas, it would be nice if this could be
            #replaced with something that didn't need the commas
            l1=line.split(',',3)
            if len(l1) > 2:
                if len(l1) < 4:
                    l1.append("")
                l.append([x.strip() for x in l1])
            else:
                #print "the line '" + line + "' is invalid. It is too short"
                break
        return l
        
    def build_ing_map_inserts(self, ing,id):
        """build_ing_map_inserts(ingredients_list,recipe_id)
        
        Build a list of lists one list for each line.
        Get the various ID's that are needed. Adding units, ingredients
        to the DB as needed.
        ingredients_list is the list returned from parse_ingredients()
        recipe_id is the id of the recipe
        """
        #ing mappings
        #0 amount
        #1 unit
        #2 ingredient
        #3 comments -- handled by the ingredients parser
        
        l=[]
        for line in ing:
            amount=line[0]
            unit_id=self.get_unit_id(line[1])
            ing_id=self.get_ingredent_id(line[2])
            comments=line[3]
            l.append((id,amount,unit_id,ing_id,comments))
        return l   
        
    def build_cat_map_inserts(self,cats,id):
        """build_cat_map_inserts(categories,recipe_id)
        
        build a list of lists to insert categories
        """
        l=[]
        for cat in cats:
            self.cur.execute("""SELECT category_id FROM categories WHERE category=%s""",
                                (cat,))
            cat_id=self.cur.fetchone()[0]
            l.append((id,cat_id))
        return l
    
    def exit(self,*args,**kwords):
        """quit, hiding the window, then showing the main window again."""
        self.w.hide()
        self.w.destroy()
        main_window.window.show()

class add_new_recipe(base_recipe_window):
    """A window building off of the base window to add a new recipe"""
    def __init__(self):
        base_recipe_window.__init__(self)
        self.xml.signal_connect('on_submit_clicked' , self.submit2)

    def submit2(self,widget):
        """ Add a recipe to the Database

        This function adds a recipie to the database. Using the helper
        functions defined in base_recipe_window
        """

        self.cur=con.cursor()
        values=self.get_form_data()

        try:
            #Do all the inserts here, so that it is atomic.
            #Really calling anything that may call something
            #to insert into the DB needs to be done inside of here...
            # I MEAN IT!

            self.cur.execute( """INSERT INTO recipes (name,description,directions,type,rating,prep_time,cook_time) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(values['name'],values['description'],values['directions'],values['type_id'],values['rating'],values['prep_time'],values['cook_time']))
            self.cur.execute("""SELECT recipe_id FROM recipes WHERE name=%s""",
                             (values['name'],))
            ids=self.cur.fetchall()
            values['recipe_id']=ids[-1][0]

            values['ing_map']=self.build_ing_map_inserts(
                                values['ingredients_list'],
                                values['recipe_id'])
            print values['ing_map']
            self.cur.executemany("""INSERT INTO ingredient_map (recipe_id,amount,unit_id,ingredient_id,notes) VALUES (%s,%s,%s,%s,%s)""",
                                    values['ing_map'])
            values['cat_map']=self.build_cat_map_inserts(
                                values['categories'],
                                values['recipe_id'])
            print values['cat_map']
            self.cur.executemany("""INSERT INTO category_map (recipe_id,category_id) VALUES (%s,%s)""",
                                    values['cat_map'])

    
            print values

        except:
            #any errors at all and we need to rollback the commits.
            errors=sys.exc_info()
            print "rolling back"
            print errors
            for line in traceback.format_tb(errors[-1], 5):
                print line
            con.rollback()
            self.cur.close()
        else:
            #commit the addition of a recipe
            con.commit()
            #for the moment always roll_back
            print "adding recipe now"
            #con.rollback()
            self.cur.close()
            self.exit("done")
        
class current_recipe(base_recipe_window):
    """A recipe window that fills out based on the info stored in the DB

    Needs to be passed a recipe ID number and"""

    def __init__(self,recipe_id=5):
        """An extentension of the recipe window"""

        #store away the recipe_id passed in
        self.recipe_id=recipe_id
        
        #call the base init function
        base_recipe_window.__init__(self)
        
        #make the submit button a update button
        self.b_update=self.xml.get_widget("b_submit")
        self.b_update.set_label("Update")
        self.xml.signal_connect('on_submit_clicked',self.update2)

        #open a new cursor to use
        self.cur=con.cursor()
        #get some data
        self.get_current_data()
        #close the cursor
        self.cur.close()
        #fill out the form with it
        self.fill_out_recipe()
    
    def set_type(self):
        """Set the list to show the correct type"""
        self.ce = self.xml.get_widget("ce_types")
        t_list=[x[0] for x in self.ce.get_model()]
        position=t_list.index(self.current_values['type'])
        self.ce.set_active(position)

    def get_type(self, type):
        """get_type("type"| type_id)

        get the type or type_id. If the argument is all numbers it is
        considered an ID otherwise it is considered a type.
        """
        if str(type).isdigit():
            self.cur.execute("""SELECT type FROM types WHERE type_id=%s""",
                                (type,))
        else:
            self.cur.execute("""SELECT type_id FROM types WHERE type=%s""",
                                (type,))
        return self.cur.fetchone()[0]
        
    def get_current_data(self):
        """get_current_data()

        Retrive the current data for self.recipe_id from the database.
        inserts it into a dictionary with the following keys:
        name        the name
        type_id     the type ID number
        type        the type
        rating      the rating
        directions  the text for the directions
        description the text for the description
        ingredients the text for the ingredients
        categories  the list of the categories
        rating      the rating
        directions  the text for the directions
        description the text for the description
        ingredients the text for the ingredients
        prep_time   'hh:mm' preperation time
        cook_time   'hh:mm' cooking time
        """
        self.cur.execute("""Select name,type,rating,directions,description,prep_time,cook_time from recipes where recipe_id=%s""", (self.recipe_id,))
        self.info=self.cur.fetchall()[0]
        #print self.info
        self.current_values={}
        self.current_values['name']=self.info[0]
        self.current_values['type_id']=self.info[1]
        self.current_values['type']=self.get_type(
                                     self.current_values['type_id'])
        self.current_values['rating']=int(self.info[2])
        self.current_values['directions']=self.info[3]
        self.current_values['description']=self.info[4]
        self.current_values['prep_time']=self.info[5]
        self.current_values['cook_time']=self.info[6]
        self.ingredients_strings=[]
        self.cur.execute("""SELECT amount,unit_id,ingredient_id,notes from ingredient_map where recipe_id=%s""",(self.recipe_id,))
        self.cur_ing=self.cur.fetchall()
        for cur_ing_line in self.cur_ing:
            #cur_ing_line  (0,     1,      2,              3)
            #              (amount,unit_id,ingredient_id,  notes)
            self.cur.execute("""SELECT unit FROM units where unit_id=%s""",
                             (cur_ing_line[1],))
            unit_name=self.cur.fetchall()[0][0]
            self.cur.execute(
             """SELECT ingredient FROM ingredients where ingredient_id=%s""",
             (cur_ing_line[2],))
            ingredient_name=self.cur.fetchall()[0][0]
            self.ingredients_strings.append(
              ",".join([x for x in [cur_ing_line[0],unit_name,ingredient_name,\
              cur_ing_line[3]]if x != ""])+"\n")
        self.current_values["ingredients"]="".join(self.ingredients_strings)
        self.current_values["categories"]=[]
        self.cur.execute("""SELECT category_id FROM category_map WHERE recipe_id=%s"""\
                         , (self.recipe_id,))
        cur_cat_ids=self.cur.fetchall()
        for c_id in cur_cat_ids:
            c_id=c_id[0]
            self.cur.execute(
              """SELECT category FROM categories WHERE category_id=%s""",
              (c_id,))
            cur_category=self.cur.fetchone()[0]
            self.current_values["categories"].append(cur_category)
        print self.current_values

    def fill_out_recipe(self):
        """Fill out the recipe window
        
        This function fills out the base recipe window with data from 
        the database gotten by calling the get_current_data() function.
        Must be called after both base_recipe_window.__init__ and 
        get_current_data(). 
        """

        #set the name field to the name
        self.xml.get_widget("e_name").set_text(self.current_values['name'])
        #setting the ingredients textview string
        self.tv_ing=self.xml.get_widget("tv_ing")
        self.tb_ing=self.tv_ing.get_buffer()
        self.tb_ing.set_text(self.current_values["ingredients"])
        #setting the directions textview string
        self.tv_dir=self.xml.get_widget("tv_dir")
        self.tb_dir=self.tv_dir.get_buffer()
        self.tb_dir.set_text(self.current_values['directions'])
        #setting the description textview string
        self.tv_desc=self.xml.get_widget("tv_desc")
        self.tb_desc=self.tv_desc.get_buffer()
        self.tb_desc.set_text(self.current_values['description'])
        #setting the rating
        self.sb_rating=self.xml.get_widget("sb_rating")
        self.sb_rating.set_value(self.current_values['rating'])
        self.sb_rating.update()
        #setting the prep hours
        self.sb_ptime_hours=self.xml.get_widget("sb_ptime_hours")
        ptime_hours=int(self.current_values['prep_time'].split(':')[0])
        self.sb_ptime_hours.set_value(ptime_hours)
        self.sb_ptime_hours.update()
        #setting the prep minutes
        self.sb_ptime_min=self.xml.get_widget("sb_ptime_minutes")
        ptime_min=int(self.current_values['prep_time'].split(':')[1])
        self.sb_ptime_min.set_value(ptime_min)
        self.sb_ptime_min.update()
        #setting the cook hours
        self.sb_ctime_hours=self.xml.get_widget("sb_ctime_hours")
        ctime_hours=int(self.current_values['cook_time'].split(':')[0])
        self.sb_ctime_hours.set_value(ptime_hours)
        self.sb_ctime_hours.update()
        #setting the cook minutes
        self.sb_ctime_hours=self.xml.get_widget("sb_ctime_minutes")
        ctime_min=int(self.current_values['cook_time'].split(':')[1])
        self.sb_ctime_hours.set_value(ctime_min)
        self.sb_ctime_hours.update()
        
        #set the type
        self.set_type()
        
        for hb in self.vb_cat.get_children():
            for cb in hb.get_children():
                if hasattr(cb, "get_label"):
                    if cb.get_label() in self.current_values["categories"]:
                        cb.set_active(True)
    
    def update2(self,widget):
        """Update the current recipe

        Opens a new cursor, gets the current data checks for differences
        and then changes the database if nessarry
        """

        self.cur=con.cursor()
        values=self.get_form_data()
        try:
            update={}
            update['recipes']=False
            update['ing_map']=False
            update['cat_map']=False
            keys=["name","type","directions","description","rating",
                  "prep_time","cook_time"
                 ]
            for key in keys:
                if values[key] != self.current_values[key]:
                    update['recipes']=True

            self.current_values['ingredients_list']=\
                self.parse_ingredients(self.current_values['ingredients'])
            if values['ingredients_list'] != \
              self.current_values['ingredients_list']:
                update['ing_map']=True
            if values['categories'] != self.current_values['categories']:
                update['cat_map']=True
            
            if update['recipes']:
                self.cur.execute(
                 """UPDATE recipes SET name=%s,description=%s,directions=%s,
                    type=%s,rating=%s,prep_time=%s,cook_time=%s
                    WHERE recipe_id=%s""",\
                    (values['name'],values['description'],values['directions']\
                    ,values['type_id'],values['rating'],values['prep_time']\
                    ,values['cook_time'],self.recipe_id))
            
            if update['ing_map']:
                self.cur.execute("""DELETE FROM ingredient_map WHERE\
                                    recipe_id=%s""", [self.recipe_id])
                values['ing_map']=self.build_ing_map_inserts(values['ingredients_list'],self.recipe_id)
                if len(values['ing_map']) >0:
                    self.cur.executemany("""INSERT INTO ingredient_map \
                        (recipe_id,amount,unit_id,ingredient_id,notes)\
                        VALUES (%s,%s,%s,%s,%s)""", values['ing_map'])
            if update['cat_map']:
                cat_del=[x for x in self.current_values['categories'] if not x in values['categories']]
                cat_add=[x for x in values['categories'] if not x in \
                    self.current_values['categories']]
                values['cat_map']=\
                    self.build_cat_map_inserts(cat_add,self.recipe_id)
                self.cur.executemany(
                    """INSERT INTO category_map (recipe_id,category_id)\
                       VALUES (%s,%s)""", values['cat_map'])
                values['cat_map_del']=\
                    self.build_cat_map_inserts(cat_del,self.recipe_id)
                if len(values['cat_map_del']) > 0:
                    self.cur.execute("""DELETE FROM category_map WHERE\
                      recipe_id=%s AND category_id=%s""",values['cat_map_del'])

        except:
            errors=sys.exc_info()
            print errors
            for line in traceback.format_tb(errors[-1], 5):
                print line
            con.rollback()
        else:
            con.commit()
        finally:
            self.exit("widget")
            self.cur.close()

class home_window:
    """The home window that allows basic searching and adding of recipies"""
    
    def __init__ (self):
        """create the home window

        This is the main window and therefore takes no options.
        """
        #make a window
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        #hook the destroy event
        self.window.connect("destroy", self.exit)
        #make an entry widget and a vbox and an hbox
        self.search_entry=gtk.Entry()
        self.vbox=gtk.VBox()
        self.hbox=gtk.HBox()
        #make a label
        self.label=gtk.Label("Enter name to search for here: ")
        #add the label and entry to the hbox
        self.hbox.add(self.label)
        self.hbox.add(self.search_entry)
        #add the hbox to the vbox
        self.vbox.add(self.hbox)
        #make a submit button, hook it's clicked event and add it to the vbox
        self.b_submit=gtk.Button("Submit")
        self.b_submit.connect("clicked", self.submit_clicked)
        self.vbox.add(self.b_submit)
        #make an add new button hook clicked and add it to the vbox
        self.b_add_new=gtk.Button("Add new Recipe")
        self.b_add_new.connect("clicked", self.add_clicked)
        self.vbox.add(self.b_add_new)
        #add the box to the window and show everything.
        self.window.add(self.vbox)
        self.window.show_all()

    def start_main_loop(self):
        """call gtk.main()"""
        gtk.main()
    def submit_clicked(self,widget):
        """open the search results window"""
        #get the text in the entry box
        self.searchstring=self.search_entry.get_text()
        #print self.searchstring
        #open the results window and give it the text from the entry
        self.search=search_results_window(searchline=self.searchstring)
        self.window.hide()
    def add_clicked(self, widget):
        """open the add new window and hide myself"""
        self.window.hide()
        add_new_window=add_new_recipe()
    def exit(self,widget):
        """call gtk.exit()"""
        gtk.main_quit()

class search_results_window:
    """A results window for a searching for a recipe"""

    def __init__ (self, searchline=""):
        """Search for the name like searchstring"""
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.exit)
        self.vbox=gtk.VBox(True,0)
        self.window.add(self.vbox)

        self.cur=con.cursor()
        searchline="%" + searchline + "%"
        self.cur.execute("""SELECT recipe_id,name,description FROM recipes WHERE name LIKE %s""", (searchline,))
        results=self.cur.fetchall()
        for button_data in results:
            self.hbox=gtk.HBox(True,0)
            self.b=gtk.Button(button_data[1])
            self.b.connect("clicked", self.show_recipe, button_data[0])
            self.l=gtk.Label(button_data[2])
            self.hbox.add(self.b)
            self.hbox.add(self.l)
            self.vbox.add(self.hbox)
        self.window.show_all()

    def show_recipe(self,widget,data):
        self.window.hide()
        recipe=current_recipe(recipe_id=data)

    def exit(self, widget):
        main_window.window.show()
    
if __name__ == '__main__':
    import pygtk,gtk,gtk.glade,gobject,os,string,sys,traceback
    from config_parse import ParseConfigFile
    default_options=dict(
        database_host="localhost",
        database_uid="rms",
        database_passwd="rmsiscool",
        database_db="rms",
        database_type="postgres"
    )
    paths=["/etc/rms/rms.conf","/home/cynyr/.config/rms/rms.conf",]
    options=ParseConfigFile(paths,default_options)
    
    if options['database_type']=="postgres":
        import pgdb
        con=pgdb.connect(host=options['database_host'],\
                            database=options['database_db'],\
                            user=options['database_uid'],\
                            password=options['database_passwd'])
    elif options['database_type']=="mysql":
        import MySQLdb
        con=MySQLdb.connect(host=options['database_host'],\
                            db=options['database_db'],\
                            user=options['database_uid'],\
                            passwd=options['database_passwd'])
    main_window=home_window()
    main_window.start_main_loop()
