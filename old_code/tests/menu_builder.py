#!/usr/bin/env python
import gtk,pygtk

def build_menu(items):
    mi=gtk.MenuItem(items[0])
    mi.connect("activate", items[1], items[2])
    if type(items[4]) == type(list()):
        mi.add_submenu(build_menu(items[4]))
    return mi





