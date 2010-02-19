#!/usr/bin/env python
"""A recipe managment system
Written by Andrew Frink rms.afrink@gmail.com
licensed under GPLv2 or later at your option.
There isn't a home page yet.
"""
import pygtk
import gtk
import gtk.glade
import gobject
import os
import string
import sys
import traceback
import pango
import rms_config
from kiwi.ui.objectlist import ObjectList, Column

class RecipeInfo:
    """an Instance that holds recipe data"""
    def __init__(self,data):
        self.r_id=data[0]
        self.name=data[1]
        self.desc=data[2]
    def __str__(self):
        return " ".join([self.name+':', self.desc])

class RecipeData:
    """
    name                the name
    type                The text form of the type
    type_id             The Type ID from get_type_id()
    rating              The int of the rating
    categories          A list of categories from get_current_categories()
    directions          The text from the directions textview
    description         The text from the description textview
    ingredients_text    The text from the ingredients textview
    ingredients_list    A list of lists from parse_ingredients() 
    """
    
    def __init__(self, *args,**keywords):
        keys=keywords.keys()
        if "name" in keys:
            self.name=keywords['name']
        else:
            self.name=""
        if "type" in keys:
            self.type=keywords['type']
        else:
            self.type=None
        if "type_id" in keys:
            self.type_id=keywords['type_id']
        else:
            self.type_id=None
        if "rating" in keys:
            self.rating=keywords['rating']
        else:
            self.rating=0
        if "categories" in keys:
            self.categories=keywords['categories']
        else:
            self.categories=None
        if "directions" in keys:
            self.directions=keywords['directions']
        else:
            self.directions=""
        if "description" in keys:
            self.description=keywords['description']
        else:
            self.description=""
        if "ingredients_text" in keys:
            self.ingredients_text=keywords['ingredients_text']
        else:
            self.ingredients_text=""
        if "ingredients_list" in keys:
            self.ingredients_list=keywords['ingredients_list']
        else:
            self.ingredients_list=None

    def __str__(self):
        s=""
        nl="\n"
        l=[]
        l.append("Name: " + self.name + ", " + str(self.rating) + " Stars")
        l.append("Description: " + self.description)
        l.append("")
        l.append(self.ingredients_text)
        l.append('')
        l.append(self.directions)
        s=nl.join(l)
        return s

class RecipeData2(RecipeData):
    

class BaseRecipeWindow:
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
        #Get the menubar
        self.menu=self.xml.get_widget("menubar1")
        #start the file menu
        self.mi_file=gtk.MenuItem("File")
        self.m_file=gtk.Menu()
        self.mi_file.set_submenu(self.m_file)
        self.menu.add(self.mi_file)
        #edit menu
        self.mi_edit=gtk.MenuItem("Edit")
        self.m_edit=gtk.Menu()
        self.mi_edit.set_submenu(self.m_edit)
        self.menu.add(self.mi_edit)
        #help menu
        self.mi_help=gtk.MenuItem("Help")
        self.m_help=gtk.Menu()
        self.mi_help.set_submenu(self.m_help)
        self.menu.add(self.mi_help)


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

        Gets the current values from the recipe_window and returns a RecipeData
        object with the following attrs:
        type                The text form of the type
        type_id             The Type ID from get_type_id()
        rating              The int of the rating
        categories          A list of categories from get_current_categories()
        directions          The text from the directions textview
        description         The text from the description textview
        ingredients_text    The text from the ingredients textview
        ingredients_list    A list of lists from parse_ingredients()
        """
        data=RecipeData()
        #get the name
        data.name=string.capwords(self.xml.get_widget("e_name").get_text().strip())
        #get the type
        data.type=self.xml.get_widget("ce_types").get_active_text()
        data.type_id=self.get_type_id(data.type)
        #get the rating
        data.rating=self.xml.get_widget("sb_rating").get_value_as_int()
        #get categories
        data.categories=self.get_current_categories()
        #get directions text
        data.directions=self.get_tv_text("tv_dir")
        #get description text
        data.description=self.get_tv_text("tv_desc")
        #get ingredents text
        data.ingredients_text=self.get_tv_text("tv_ing").strip('\n')
        data.ingredients_list=self.parse_ingredients(data.ingredients_text)
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

class add_new_recipe(BaseRecipeWindow):
    """A window building off of the base window to add a new recipe"""
    def __init__(self):
        BaseRecipeWindow.__init__(self)
        self.xml.signal_connect('on_submit_clicked' , self.submit2)

    def submit2(self,widget):
        """ Add a recipe to the Database

        This function adds a recipie to the database. Using the helper
        functions defined in BaseRecipeWindow
        """

        self.cur=con.cursor()
        values=self.get_form_data()

        try:
            #Do all the inserts here, so that it is atomic.
            #Really calling anything that may call something
            #to insert into the DB needs to be done inside of here...
            # I MEAN IT!

            self.cur.execute( """INSERT INTO recipes (name,description,directions,type,rating,prep_time,cook_time) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(values.name,values.description,values.directions,values.type_id,values.rating,"00:10","00:30"))
            self.cur.execute("""SELECT recipe_id FROM recipes WHERE name=%s""",
                             (values.name,))
            ids=self.cur.fetchall()
            values.recipe_id=ids[-1][0]

            values.ing_map=self.build_ing_map_inserts(
                                values.ingredients_list,
                                values.recipe_id)
            print values.ing_map
            self.cur.executemany("""INSERT INTO ingredient_map (recipe_id,amount,unit_id,ingredient_id,notes) VALUES (%s,%s,%s,%s,%s)""",
                                    values.ing_map)
            values.cat_map=self.build_cat_map_inserts(
                                values.categories,
                                values.recipe_id)
            print values.cat_map
            self.cur.executemany("""INSERT INTO category_map (recipe_id,category_id) VALUES (%s,%s)""",values.cat_map)

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
        
class current_recipe(BaseRecipeWindow):
    """A recipe window that fills out based on the info stored in the DB

    Needs to be passed a recipe ID number and"""

    def __init__(self,recipe_id=5):
        """An extentension of the recipe window"""

        #store away the recipe_id passed in
        self.recipe_id=recipe_id
        
        #call the base init function
        BaseRecipeWindow.__init__(self)
        
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
        self.mi_print=gtk.MenuItem("Print")
        self.mi_print.connect("activate", self.do_print)
        self.m_file.add(self.mi_print)
        self.mi_print.show()
        self.mi_file.show()
    
    def do_print(self,widget):
        self.cur=con.cursor()
        do_print(None,self.get_form_data())
        self.cur.close()

    def set_type(self):
        """Set the list to show the correct type"""
        self.ce = self.xml.get_widget("ce_types")
        t_list=[x[0] for x in self.ce.get_model()]
        position=t_list.index(self.current_values.type)
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
        categories  the list of the categorie       type        the type
        """

        self.cur.execute("""Select name,type,rating,directions,description from recipes where recipe_id=%s""", (self.recipe_id,))
        self.info=self.cur.fetchall()[0]
        #print self.info
        self.current_values=RecipeData()
        self.current_values.name=self.info[0]
        self.current_values.type_id=self.info[1]
        self.current_values.type=self.get_type(
                                     self.current_values.type_id)
        self.current_values.rating=int(self.info[2])
        self.current_values.directions=self.info[3]
        self.current_values.description=self.info[4]
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
        self.current_values.ingredients="".join(self.ingredients_strings)
        self.current_values.categories=[]
        self.cur.execute("""SELECT category_id FROM category_map WHERE recipe_id=%s"""\
                         , (self.recipe_id,))
        cur_cat_ids=self.cur.fetchall()
        for c_id in cur_cat_ids:
            c_id=c_id[0]
            self.cur.execute(
              """SELECT category FROM categories WHERE category_id=%s""",
              (c_id,))
            cur_category=self.cur.fetchone()[0]
            self.current_values.categories.append(cur_category)

    def fill_out_recipe(self):
        """Fill out the recipe window
        
        This function fills out the base recipe window with data from 
        the database gotten by calling the get_current_data() function.
        Must be called after both BaseRecipeWindow.__init__ and 
        get_current_data(). 
        """

        #set the name field to the name
        self.xml.get_widget("e_name").set_text(self.current_values.name)
        #setting the ingredients textview string
        self.tv_ing=self.xml.get_widget("tv_ing")
        self.tb_ing=self.tv_ing.get_buffer()
        self.tb_ing.set_text(self.current_values.ingredients)
        #setting the directions textview string
        self.tv_dir=self.xml.get_widget("tv_dir")
        self.tb_dir=self.tv_dir.get_buffer()
        self.tb_dir.set_text(self.current_values.directions)
        #setting the description textview string
        self.tv_desc=self.xml.get_widget("tv_desc")
        self.tb_desc=self.tv_desc.get_buffer()
        self.tb_desc.set_text(self.current_values.description)
        #setting the rating
        self.sb_rating=self.xml.get_widget("sb_rating")
        self.sb_rating.set_value(self.current_values.rating)
        self.sb_rating.update()
        #set the type
        self.set_type()
        
        for hb in self.vb_cat.get_children():
            for cb in hb.get_children():
                #if hasattr(cb, "get_label"):
                if isinstance(cb, gtk.CheckButton):
                    if cb.get_label() in self.current_values.categories:
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
            for key in ["name","type","directions","description","rating"]:
                if getattr(values,key) != getattr(self.current_values,key):
                    update['recipes']=True

            self.current_values.ingredients_list=\
                self.parse_ingredients(self.current_values.ingredients)
            if getattr(values,'ingredients_list') != \
              getattr(self.current_values,'ingredients_list'):
                update['ing_map']=True
            if getattr(values,'categories') != \
              getattr(self.current_values,'categories'):
                update['cat_map']=True
            
            if update['recipes']:
                self.cur.execute(
                 """UPDATE recipes SET name=%s,description=%s,directions=%s,
                    type=%s,rating=%s WHERE recipe_id=%s""",
                    (values.name ,values.description,values.directions\
                    ,values.type_id,values.rating,self.recipe_id))
            
            if update['ing_map']:
                self.cur.execute("""DELETE FROM ingredient_map WHERE\
                                    recipe_id=%s""", [self.recipe_id])
                values.ing_map=self.build_ing_map_inserts(values.ingredients_list,self.recipe_id)
                if len(values.ing_map) >0:
                    self.cur.executemany("""INSERT INTO ingredient_map \
                        (recipe_id,amount,unit_id,ingredient_id,notes)\
                        VALUES (%s,%s,%s,%s,%s)""", values.ing_map)
            if update['cat_map']:
                cat_del=[x for x in self.current_values.categories if \
                    not x in values.categories]
                cat_add=[x for x in values.categories if not x in \
                    self.current_values.categories]
                values.cat_map=\
                    self.build_cat_map_inserts(cat_add,self.recipe_id)
                self.cur.executemany(
                    """INSERT INTO category_map (recipe_id,category_id)\
                       VALUES (%s,%s)""", values.cat_map)
                values.cat_map_del=\
                    self.build_cat_map_inserts(cat_del,self.recipe_id)
                if len(values.cat_map_del) > 0:
                    self.cur.execute("""DELETE FROM category_map WHERE\
                      recipe_id=%s AND category_id=%s""",values.cat_map_del)

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
        self.menu=gtk.MenuBar()
        self.vbox.add(self.menu)
        for label in ["File","Edit"]:
            self.mi=gtk.MenuItem(label)
            #self.mi.connect("activate", self.test, label)
            self.menu.add(self.mi)
            if label == "Edit":
                self.mi2=gtk.Menu()
                self.pref=gtk.MenuItem("Preferances")
                self.pref.connect("activate", self.test, "Preferances")
                self.mi2.add(self.pref)
                self.mi.set_submenu(self.mi2)
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
        #make a button to plan meals
        self.b_plan = gtk.Button("Meal Plan")
        self.b_plan.connect("clicked", self.plan_clicked)
        self.vbox.add(self.b_plan)
        #make an add new button hook clicked and add it to the vbox
        self.b_add_new=gtk.Button("Add new Recipe")
        self.b_add_new.connect("clicked", self.add_clicked)
        self.vbox.add(self.b_add_new)
        #add the box to the window and show everything.
        self.window.add(self.vbox)
        self.window.show_all()

    def test(self,widget,label):
        if label == "Preferances":
            cfile=os.environ['HOME']+".config/rms/rms.conf"
            cw=rms_config.config_window(self.window,options,cfile)
            cw.run()
            print "getting options"
            get_options()
            print options
            get_db_connection()
        print widget,label

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
    def plan_clicked(self,widget):
        """open the search results window"""
        #get the text in the entry box
        self.searchstring=self.search_entry.get_text()
        #print self.searchstring
        #open the results window and give it the text from the entry
        self.search=MealPlan(searchline=self.searchstring)
        self.window.hide()
    def add_clicked(self, widget):
        """open the add new window and hide myself"""
        self.window.hide()
        add_new_window=add_new_recipe()
    def exit(self,widget):
        """call gtk.main_quit()"""
        gtk.main_quit()

class search_results_window:
    """A results window for a searching for a recipe"""

    def __init__ (self, searchline="", mode=gtk.SELECTION_SINGLE):
        """Search for the name like searchstring"""
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.exit)
        self.window.set_size_request(600, 250)
        self.vbox=gtk.VBox(homogeneous=False,spacing=0)
        self.window.add(self.vbox)

        self.cur=con.cursor()
        if searchline.count(':') !=0:
            search_options=dict(self.parse_search_string(searchline))
            print search_options
            results=[[5, 'Foo2', 'yummy food'], 
                     [6, 'Foobar', 'best foobar evar!']]
        else:
            searchline="%" + searchline + "%"
            self.cur.execute("""SELECT recipe_id,name,description FROM recipes WHERE name LIKE %s""", (searchline,))
            results=self.cur.fetchall()

        my_columns = [  Column("name", title="Name", sorted=True),
                        Column("desc", title="Description")
                     ]
        self.objectlist = ObjectList(my_columns, mode=mode)
        self.objectlist.set_size_request(600,225)
        recipes=[RecipeInfo(x) for x in results]
        self.objectlist.add_list(recipes)
        self.b=gtk.Button("Show Selected")
        self.b.connect("clicked", self.show_recipe2)
        self.vbox.add(self.objectlist)
        self.vbox.add(self.b)

        self.window.show_all()

    def parse_search_string(self,s):
        foo,indexes=findall(':',s)
        p=0
        l=[]
        s_len=len(s)
        for i in indexes:
            for j in range(i+1,s_len+1):
                #print (j,s_len)
                if j >= s_len:
                    l.append(s[p:j].strip())
                    break
                else:
                    if s[j] == " ":
                        t=j
                    if s[j] == ':':
                        l.append(s[p:t].strip())
                        p=t
                        break
        return [[y.lower() for y in x.split(':')] for x in l]
    def show_recipe2(self,widget,*data):
        recipe=self.objectlist.get_selected()
        self.window.hide()
        current_recipe(recipe_id=recipe.r_id)

    def show_recipe(self,widget,data):
        self.window.hide()
        recipe=current_recipe(recipe_id=data)

    def exit(self, widget):
        main_window.window.show()
    
class MealPlan(search_results_window):
    def __init__(self,searchline=""):
        search_results_window.__init__(self, searchline, mode=gtk.SELECTION_MULTIPLE)
        print ObjectList.__init__.__doc__

    def show_recipe2(self,widget,*data):
        recipe=self.objectlist.get_selected_rows()
        self.window.hide()
        current_recipe(recipe_id=recipe[0].r_id)



class PrintData:
    text = None
    layout = None
    page_breaks = None

def get_db_connection():
    global con
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

def get_options():
    from config_parse import ParseConfigFile
    default_options=dict(
        database_host="localhost",
        database_uid="rms",
        database_passwd="rmsiscool",
        database_db="rms",
        database_type="postgres"
    )
    paths=["/etc/rms/rms.conf",os.environ['HOME']+".config/rms/rms.conf",]
    global options
    options=ParseConfigFile(paths,default_options)

def findall(char,string):
    """Findall(char,string)

    Find the index of every instance of char in string and return a tuple
    (string,indexes)"""
    s=string
    l=[]
    i,c=0,0
    for foo in range(s.count(char)):
        i=s.find(char)
        l.append(i+c)
        s=s[i+1:]
        c=c+i+1

    return (string,l)

def do_print(widget,text):
    print text
    global settings, page_setup
    print_data=PrintData()
    print_data.text=str(text)
    print_op = gtk.PrintOperation()
    if settings is not None:
        print_op.set_print_settings(settings)

    if page_setup is not None:
        print_op.set_default_page_setup(page_setup)

    print_op.connect("begin_print", begin_print, print_data)
    print_op.connect("draw_page", draw_page, print_data)

    try:
        res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, main_window.window)
    except gobject.GError, ex:
        error_dialog = gtk.MessageDialog(main_window,
                                         gtk.DIALOG_DESTROY_WITH_PARENT,
                                         gtk._MESSAGE_ERROR,
                                         gtk.BUTTONS_CLOSE,
                                         ("Error printing file:\n%s" % str(ex)))
        error_dialog.connect("response", gtk.Widget.destroy)
        error_dialog.show()
    else:
        if res == gtk.PRINT_OPERATION_RESULT_APPLY:
            settings = print_op.get_print_settings()
    
def begin_print(operation,context, print_data):
    width = context.get_width()
    height = context.get_height()
    print_data.layout = context.create_pango_layout()
    print_data.layout.set_font_description(pango.FontDescription("Sans 12"))
    print_data.layout.set_width(int(width*pango.SCALE))
    print_data.layout.set_text(print_data.text)

    num_lines = print_data.layout.get_line_count()

    page_breaks = []
    page_height = 0

    for line in range(num_lines):
        layout_line = print_data.layout.get_line(line)
        ink_rect, logical_rect = layout_line.get_extents()
        lx, ly, lwidth, lheight = logical_rect
        line_height = lheight / 1024.0
        if page_height + line_height > height:
	    page_breaks.append(line)
	    page_height = 0
        page_height += line_height
    operation.set_n_pages(len(page_breaks) + 1)
    print_data.page_breaks = page_breaks
    
def draw_page(operation, context, page_nr, print_data):
    assert isinstance(print_data.page_breaks, list)
    if page_nr == 0:
        start = 0
    else:
        start = print_data.page_breaks[page_nr - 1]

    try:
        end = print_data.page_breaks[page_nr]
    except IndexError:
        end = print_data.layout.get_line_count()
    
    cr = context.get_cairo_context()

    cr.set_source_rgb(0, 0, 0)
  
    i = 0
    start_pos = 0
    iter = print_data.layout.get_iter()
    while 1:
        if i >= start:
            line = iter.get_line()
            _, logical_rect = iter.get_line_extents()
            lx, ly, lwidth, lheight = logical_rect
            baseline = iter.get_baseline()
            if i == start:
                start_pos = ly / 1024.0
            cr.move_to(lx / 1024.0, baseline / 1024.0 - start_pos)
            cr.show_layout_line(line)
        i += 1
        if not (i < end and iter.next_line()):
            break




if __name__ == '__main__':
    get_options()
    #print options
    get_db_connection()

    global main_window
    global page_setup
    global settings
    page_setup = None
    settings = None

    main_window=home_window()
    main_window.start_main_loop()
