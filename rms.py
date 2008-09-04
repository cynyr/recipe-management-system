#!/usr/bin/env python

class base_recipe_window:
    """A window and functions to add a new recipe"""

    def __init__(self):
        """Set up the enter new recipie window

        This creates new recipie window. It connects to the database
        and sets up the cursor. It populates a dropdown from
        data in the database.

        """
        self.update=False
        # Load Glade XML
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
        
        #make some checkboxes
        self.vb_cat=self.xml.get_widget('vb_cat')
        self.cur.execute("""select category from categories order by category""")
        categories=list(self.cur.fetchall())
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
                    #hook the clicked event and pass along the lable...
                    #which is silly but needed at the moment.
                    #self.cb.connect("clicked", self.cb_clicked, self.cb_label)
                else:
                    self.cb=gtk.Label("")
                self.hb.add(self.cb)
                
        self.e_new_cat=gtk.Entry()
        self.e_new_cat.set_tooltip_text("a comma seperated list of categories")
        self.hb=gtk.HBox(False, 0)
        self.vb_cat.add(self.hb)
        self.hb.add(gtk.Label("Add a new category(s):"))
        self.hb.add(self.e_new_cat)
        
    def get_active_categories(self):
        l=[]
        for hbox in self.vb_cat.get_children():
            for cb in hbox.get_children():
                if hasattr(cb, "get_active"):
                    if cb.get_active():
                        l.append(cb.get_label())
        return l
    def get_new_categories(self):
        l=[]
        for cat in [x.strip() for x in self.e_new_cat.get_text().split(",")]:
            if cat != "":
                l.append(string.capwords(cat))
        if len(l) >0:
            self.add_new_categories(l)
        return l
    
    def get_current_categories(self):
        l=self.get_active_categories()
        l.extend(self.get_new_categories())
        return l
    
    def add_new_categories(self,cats):
        for cat in cats:
            self.cur.execute("INSERT INTO categories (category) VALUES (%s)",\
                                 (cat,))
    def get_tv_text(self,tv):
        """get all the text from a textview
           
           Either look for a widget in the glade file by the name if a string
           or assume it is a textview type and use that."""
        if type(tv) == type(""):
            tb=self.xml.get_widget(tv).get_buffer()
        else:
            tb=tv.get_buffer()
        text=tb.get_text(tb.get_start_iter(), tb.get_end_iter())
        return text
        
    def add_unit(self, unit):
        try:
            self.cur.execute("""INSERT INTO units (unit) VALUES (%s)""",(unit,))
        except:
            print "add unit failed"
            return False
        else:
            return True

    def get_unit_id(self,unit,add=True):
        self.cur.execute("""SELECT unit_id FROM units WHERE unit=%s""", [unit])
        result=self.cur.fetchone()
        if result == None:
            if add:
                if self.add_unit(unit):
                    self.cur.execute("""SELECT unit_id FROM units WHERE unit=%s""", [unit])
                    id=self.cur.fetchone()[0]
                else:
                    id=None
            else:
                id=None
        else:
            id=result[0]

        return id

    def add_ingredient(self,ingredient):
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
        self.cur.execute("""SELECT ingredient_id FROM ingredients WHERE ingredient=%s""",
                         (ingredient,))
        result=self.cur.fetchone()
        if result == None:
            if add:
                if self.add_ingredient(ingredient):
                    self.cur.execute(
                        """SELECT ingredient_id FROM ingredients WHERE ingredient=%s""",
                        (ingredient,))
                    id=self.cur.fetchone()[0]
                else:
                    id=None
            else:
                id=None
        else:
            id=result[0]

        return id
    
    def get_type_id(self, type):
        self.cur.execute("""SELECT type_id FROM types WHERE type=%s""",(type,))
        result=self.cur.fetchone()
        return result[0]

    def get_form_data(self):
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
        data['ingredients_list']=self.parse_ingredients(data['ingredients_text'])
        return data

    def parse_ingredients(self,txt):
        l=[]
        for line in txt.split('\n'):
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
        """Build a list of lists one list for each line.
        
        Get the various ID's that are needed. Adding units, ingredients
        to the DB as needed.
        arg[1] is the list returned from parse_ingredients()
        arg[2] is the id of the recipe
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
        """build a list of lists to insert categories"""
        l=[]
        for cat in cats:
            self.cur.execute("""SELECT category_id FROM categories WHERE category=%s""",
                                (cat,))
            cat_id=self.cur.fetchone()[0]
            l.append((id,cat_id))
        return l
    
    def exit(self,*args):
        """quit"""
        self.w.hide()
        self.w.destroy()
        main_window.window.show()
        #__main__.home_window.window.show()
        #gtk.main_quit()

class add_new_recipe(base_recipe_window):
    """A window building off of the base window to add a new recipe"""
    def __init__(self):
        base_recipe_window.__init__(self)

        self.xml.signal_connect('on_submit_clicked' , self.submit2)

    def submit2(self,widget):
        """ Add a recipe to the Database

        This function adds a recipie to the database. Using the helper
        functions defined in base_recipe_window"""

        self.cur=con.cursor()
        values=self.get_form_data()
        print values

        #start a transaction. better work on the engine i'm using...
        try:
            #Do all the inserts here, so that it is atomic.
            #Really calling anything that may call something
            #to insert into the DB needs to be done inside of here...
            # I MEAN IT!

            self.cur.execute( """INSERT INTO recipes (name,description,directions,type,rating,prep_time,cook_time) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(values['name'],values['description'],values['directions'],values['type_id'],values['rating'],"00:10","00:30"))
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
        
    def submit(self,widget):
        """Add a recipe to the database

        This function adds a recipe the database and extracts needed info
        from the database as well. Needed info is the ID number so this
        one can be found. Also each ingredient and unit ID is needed.

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
        self.new_cat=[]
        for cat in self.e_new_cat.get_text().split(','):
            if cat != "":
                cat=string.capwords(cat)
                self.new_cat.append(cat)
                #print "insert into category (category) values (%s)" % (cat,)
                self.cur.execute("insert into category (category) values (%s)",(cat,))
        #----End new categories-----

        #----Start Getting directions text-----
        self.tb_dir=self.xml.get_widget("tv_dir").get_buffer()
        self.dir_text=self.tb_dir.get_text(self.tb_dir.get_start_iter(), 
                                            self.tb_dir.get_end_iter())
        #----End of directions text-----

        #----Start of getting ingredients text----
        self.tb_ing=self.xml.get_widget("tv_ing").get_buffer()
        self.ing_text=self.tb_ing.get_text(self.tb_ing.get_start_iter(), 
                                            self.tb_ing.get_end_iter())
        #----End of ingredients text-----

        #----Start of description text-----
        self.tb_desc=self.xml.get_widget("tv_desc").get_buffer()
        self.desc_text=self.tb_desc.get_text(self.tb_desc.get_start_iter(),
                                             self.tb_desc.get_end_iter())

        #----Start recipie insert-----
        self.cur.execute("insert into recipes (name,type,rank,directions,description) VALUES (%s,%s,%s,%s,%s)",(self.name,type,rating,self.dir_text,self.desc_text))
        #----Start recipe_id-----
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

        #-----Start ingredient_map inserts-----
        for line in self.ing_text.split('\n'):
            if line == "":
                break
            else:
                data=line.split(',')
                """ notes for the fields in data
                    0           1       2           3+
                    ammount,    units,  ingredient,  notes"""

                #----Start get ingredient_id-----
                data[0]=data[0].strip()
                data[1]=data[1].strip()
                data[2]=data[2].strip()
                self.cur.execute("select id from ingredients where ingredient=%s", (data[2],))
                ingredient_id=self.cur.fetchone()
                print ingredient_id
                if ingredient_id==None:
                    self.cur.execute("""INSERT INTO ingredients (ingredient) VALUES (%s)""", (data[2],))
                    #self.cur.execute("SELECT MAX(id) from ingredients")
                    self.cur.execute("""SELECT id from ingredients where ingredient=%s""", (data[2],))
                    #ingredient_id=self.cur.fetchone()[0] + 1
                    ingredient_id=self.cur.fetchone()[0]
                else:
                    ingredient_id=ingredient_id[0]
                #----End of ingredient_id-----

                #----Start of unit_id-----
                self.cur.execute("SELECT id FROM units WHERE unit=%s or abbreviation=%s", (data[1],data[1]))

                unit_id=self.cur.fetchone()
                if unit_id == None:
                    self.cur.execute("""INSERT INTO units (unit) VALUES (%s)""", (data[1],))
                    #self.cur.execute("SELECT MAX(id) from units")
                    self.cur.execute("""SELECT id FROM units WHERE unit=%s""", (data[1],))
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

                print "insert into ingredient_map (recipe_id,amount,unit_id,\
                       ingredient_id,notes) values (%s, %s, %s, %s, %s)" % \
                       (self.recipe_id, data[0], unit_id, ingredient_id, notes)

                self.cur.execute("insert into ingredient_map (recipe_id,amount,unit_id, ingredient_id,notes) values (%s, %s, %s, %s, %s)", (self.recipe_id, data[0], unit_id, ingredient_id, notes))
        #-----End ingredient map inserts-----

        #-----Start categories inserts-----
        categories=self.get_active_categories()
        for cat in self.new_cat:
            categories.append(cat)
        for cat in categories:
            self.cur.execute("select id from category where category=%s",
                                (cat,))
            cat_id=self.cur.fetchone()[0]
            print 'insert into category_map (id,category_id) values (%s,%s)' % (self.recipe_id, cat_id) 
            self.cur.execute("insert into category_map (id,category_id) values (%s,%s)",(self.recipe_id, cat_id) )
        #-----End categories inserts-----
        #print self.dir_text
        self.w.hide()
        self.w.destroy()

class current_recipe(base_recipe_window):
    """A recipe window that fills out based on the info stored in the DB

    Needs to be passed a recipe ID number and"""

    def __init__(self,recipe_id=5):
        """An extentension of the recipe window"""#{{{2

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
        if str(type).isdigit():
            self.cur.execute("""SELECT type FROM types WHERE type_id=%s""",
                                (type,))
        else:
            self.cur.execute("""SELECT type_id FROM types WHERE type=%s""",
                                (type,))
        return self.cur.fetchone()[0]
        
    def get_current_data(self):
        self.cur.execute("""Select name,type,rating,directions,description from recipes where recipe_id=%s""", (self.recipe_id,))
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
        for id in cur_cat_ids:
            id=id[0]
            self.cur.execute(
              """SELECT category FROM categories WHERE category_id=%s""",
              (id,))
            cur_category=self.cur.fetchone()[0]
            self.current_values["categories"].append(cur_category)

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
        #set the type
        self.set_type()
        
        for hb in self.vb_cat.get_children():
            for cb in hb.get_children():
                if hasattr(cb, "get_label"):
                    if cb.get_label() in self.current_values["categories"]:
                        cb.set_active(True)
    
    def update2(self,widget):
        self.cur=con.cursor()
        values=self.get_form_data()
        #print values
        #print self.current_values
        try:
            #for key in values:
            #    print key
            #    if key in self.current_values.keys():
            #        if values[key] != self.current_values[key]:
            #            print "update", key
            #        else:
            #            print "not updating", key
            update={}
            update['recipes']=False
            update['ing_map']=False
            update['cat_map']=False
            for key in ["name","type","directions","description","rating"]:
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
                    type=%s,rating=%s WHERE recipe_id=%s""", (values['name']\
                    ,values['description'],values['directions'],values['type_id']\
                    ,values['rating'],self.recipe_id))
            
            if update['ing_map']:
                self.cur.execute("""DELETE FROM ingredient_map WHERE recipe_id=%s""",
                                [self.recipe_id])
                values['ing_map']=self.build_ing_map_inserts(values['ingredients_list'],self.recipe_id)
                if len(values['ing_map']) >0:
                    self.cur.executemany("""INSERT INTO ingredient_map (recipe_id,amount,unit_id,ingredient_id,notes) VALUES (%s,%s,%s,%s,%s)""", values['ing_map'])
            if update['cat_map']:
                cat_del=[x for x in self.current_values['categories'] if not x in values['categories']]
                cat_add=[x for x in values['categories'] if not x in \
                    self.current_values['categories']]
                values['cat_map']=\
                    self.build_cat_map_inserts(cat_add,self.recipe_id)
                self.cur.executemany(
                    """INSERT INTO category_map (recipe_id,category_id)\
                       VALUES (%s,%s)""", values['cat_map'])
                values['cat_map_del']=self.build_cat_map_inserts(cat_del,self.recipe_id)
                if len(values['cat_map_del']) > 0:
                    self.cur.execute("""DELETE FROM category_map WHERE recipe_id=%s\
                                    AND category_id=%s""",values['cat_map_del'])

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

    def start_main_loop(self):
        gtk.main()
    def submit_clicked(self,widget):
        self.searchstring=self.search_entry.get_text()
        print self.searchstring
        self.search=search_results_window(searchline=self.searchstring)
    def add_clicked(self, widget):
        self.window.hide()
        add_new_window= add_new_recipe()
    def show_recipe(self,widget,s_rid=11):
        recipe=add_new_recipe(recipe_id=s_rid)
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

        self.cur=con.cursor()
        searchline="%" + searchline + "%"
        self.cur.execute("""SELECT recipe_id,name,description FROM recipes WHERE name LIKE %s""",\
                         (searchline,))
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
        con=MySQLdb.connect(host=options['database_host'],\
                            db=options['database_db'],\
                            user=options['database_uid'],\
                            passwd=options['database_passwd'])
    main_window=home_window()
    main_window.start_main_loop()
