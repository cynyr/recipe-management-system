#!/usr/bin/env python

import pygtk,gtk,gtk.glade,MySQLdb,gobject

class testui:
    def __init__(self, runaslib=True):
        # Load Glade XML
        self.xml = gtk.glade.XML("test_ui1.glade")
        self.w = self.xml.get_widget('window1')
        self.w.show_all()
        self.ce = self.xml.get_widget('comboentry1')
        self.e_amount = self.xml.get_widget('e_amount')
        self.e_ingredent = self.xml.get_widget('e_ingredent')
        self.l = gtk.ListStore(gobject.TYPE_STRING)
        self.xml.signal_connect('on_window1_destroy' , self.exit)
        self.xml.signal_connect('on_window1_keypress' , self.keypress)
        self.xml.signal_connect('on_button1_clicked' , self.parse)
        ### A test to set a comboentry's values after the fact
        #for num in range(1,10):
            #l.append( ["testing" +str(num)])
        #self.ce.set_model(l)
        #self.ce.set_text_column(0)

        self.con=MySQLdb.connect(host="localhost", db="rms", user="cynyr", passwd="abbg")
        self.cur=self.con.cursor()
        self.cur.execute("""truncate table data""")
        self.cur.execute("""select * from units""")
        for row in self.cur:
            #print row
            self.l.append([row[1] +" ( " + row[2] + " )"])
        self.ce.set_model(self.l)
        self.ce.set_text_column(0)
    def parse(self):
        print self.e_amount.get_text().strip() + " " + self.ce.get_active_text().split('(')[0].strip() + " of " + self.e_ingredent.get_text()
        
    def keypress(self,widget,data):
        key = gtk.gdk.keyval_name(data.keyval)
        #print key
        if key == "Return":
            self.parse()
    def exit(self,widget):
        gtk.main_quit()


if __name__ == '__main__':
	test = testui()
	gtk.main()
