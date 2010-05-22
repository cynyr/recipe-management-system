#!/usr/bin/env python
import gtk,pygtk

class ehn_textview(gtk.TextView):
    
    def __init__(self,*args):
        gtk.TextView.__init__(self,*args)

    def get_all_text(self):
        tb=self.get_buffer()
        start=tb.get_start_iter()
        end  =tb.get_end_iter()
        return tb.get_text(start,end)
        


class home_window:
    """The home window that allows basic searching and adding of recipies"""
    
    def __init__ (self, runaslib=True):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.exit)
        self.vbox=gtk.VBox()
        cl=["cb8","cb2","cb0","cb9","cb6",]
        labels=[]
        width=4
        for num in range(10):
            labels.append(["cb"+str(num)])
        labels.append(["qoyeqwoieqow"])
            
        while len(labels):
            self.hbox=gtk.HBox(True,0)
            self.vbox.add(self.hbox)
            for column in range(width):
                if len(labels):
                    self.cb=gtk.CheckButton(labels.pop(0)[0])
                else:
                    self.cb=gtk.Label(" ")
                self.hbox.add(self.cb)

                
            
        #for num in range(5):
            #self.hbox=gtk.HBox()
            #self.vbox.add(self.hbox)
            #for width in range(4):
                #label="checkbox " + str((num*10) +width)
                #cb=gtk.CheckButton(label)
                #self.hbox.add(cb)
        self.etv=ehn_textview()
        self.vbox.add(self.etv)
        self.b=gtk.Button("check")
        self.b.connect("clicked", self.check, cl)
        self.vbox.add(self.b)
        self.b2=gtk.Button("print checked")
        self.b2.connect("clicked", self.list)
        self.b3=gtk.Button("print textview")
        self.b3.connect("clicked", self.test_text)
        self.vbox.add(self.b2)
        self.vbox.add(self.b3)
        self.window.add(self.vbox)
        self.window.show_all()
    
    def test_text(self,widget):
        print self.etv.get_all_text()
    def check(self, widget, l):
        for hb in self.vbox.get_children():
            for cb in hb.get_children():
                if cb.get_label() in l:
                    if cb.get_active():
                        cb.set_active(False)
                    else:
                        cb.set_active(True)

    def list(self, *args):
        l=[]
        for hb in self.vbox.get_children():
            for cb in hb.get_children():
                if hasattr(cb, "get_active"):
                    if cb.get_active():
                         l.append(cb.get_label())
        print l
                                
                            
            

    def start_main_loop(self,):
        gtk.main()
    def exit(self,widget):
        gtk.main_quit()

w=home_window()
w.start_main_loop()
