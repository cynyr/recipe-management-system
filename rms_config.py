#!/usr/bin/env python
import gtk,pygtk,os
class config_window():

    def __init__(self, parent_window=None, options={}, config_file=""):
        if config_file == "":
            self.config_file=os.environ["HOME"]+".config/rms/rms.conf"
        else:
            self.config_file=config_file
        self.w=gtk.Dialog("Recipe Managenment System Preferances",
                            parent_window,
                            gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
                         )
        keys=["database_passwd","database_host","database_uid",
                  "database_type","database_db", ]

        for x in keys:
            self.hb=gtk.HBox(2,True)
            self.label=gtk.Label(x)
            self.e=gtk.Entry()
            self.hb.add(self.label)
            self.hb.add(self.e)
            try:
                self.e.set_text(options[x])
            except:
                pass
            self.w.vbox.add(self.hb)
        self.w.connect("response", self.response)
        self.w.show_all()
    def response(self,*args):
        if args[1] == -3:
            self.parse_options()
        #self.w.destroy()
        self.exit()
        #print args

    def parse_options(self, *args , **kwords):
        children=self.w.vbox.get_children()
        #print children
        l=[]
        while len(children) > 2:
            c=children.pop(0).get_children()
            if c[1].get_text() != "":
                l.append(c[0].get_label()+"="+c[1].get_text())
        text="\n".join(l)
        header="#Config file auto generated\n"
        cf=open(self.config_file, "w")
        cf.write(header+text)
        cf.close()
        self.exit()
    
    def run(self,*args):
        self.w.run()

    def exit(self,*args):
        self.w.destroy()

if __name__ == "__main__":
    import pygtk,gtk,os
    from config_parse import ParseConfigFile
    paths=["/etc/rms/rms.conf",os.environ['HOME']+"/.config/rms/rms.conf",]
    options=ParseConfigFile(paths)
    #options=[]
    #print options
    cw=config_window(None,options)
    cw.run()
    #gtk.main()
