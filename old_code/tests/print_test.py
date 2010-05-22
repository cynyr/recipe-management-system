#!/usr/bin/env python
import pygtk,gtk,pango,gobject

main_window=None
page_setup = None
settings = None

class PrintData:
    text = None
    layout = None
    page_breaks = None

def do_print(widget,text):
    global settings, page_setup
    print_data=PrintData()
    print_data.text="".join(text)
    print_op = gtk.PrintOperation()
    if settings is not None:
        print_op.set_print_settings(settings)

    if page_setup is not None:
        print_op.set_default_page_setup(page_setup)

    print_op.connect("begin_print", begin_print, print_data)
    print_op.connect("draw_page", draw_page, print_data)

    try:
        res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, main_window)
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
    finally:
        print_op.destroy()
    
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

window=gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect("destroy", gtk.main_quit)
b=gtk.Button("Print nao!")
text=["This is a very very very long line to test that wraping lines works, somewhat nicely except that it wasn't long enough so i had to make it much much longer..... . . . . . . . . . . . . . . . . . . .\n",]
for num in range(1,189):
    text.append("this is line %i\n" % num)
b.connect("clicked", do_print, text)
window.add(b)
window.show_all()
gtk.main()

