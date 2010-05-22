#!/usr/bin/env python
import gtk,pygtk

from kiwi.ui.objectlist import ObjectList, Column

class recipe_info:
    """an Instance that holds recipe data"""
    def __init__(self,data):
        self.r_id=data[0]
        self.name=data[1]
        self.desc=data[2]
    def __str__(self):
        return " ".join([self.name+':', self.desc])

def get_selected(*args,**kwords):
    print objectlist.get_selected()


results=[[5, 'Foo2', 'yummy food'], [6, 'Foobar', 'best foobar evar!']]

#the first argument is the name of the attr in the object for the row that goes
#in the column
my_columns = [  Column("r_id",   title="ID", visible=False),
                Column("name", title="Name", sorted=True),
                Column("desc", title="Description")
             ]
recipes=[recipe_info(x) for x in results]

objectlist = ObjectList(my_columns)
objectlist.add_list(recipes)

w = gtk.Window()
w.connect('delete-event', gtk.main_quit)

vb=gtk.VBox()
vb.add(objectlist)
b=gtk.Button("Click Me!")
b.connect("clicked", get_selected)
vb.add(b)

w.add(vb)

w.show_all()
gtk.main()



