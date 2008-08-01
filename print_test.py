#!/usr/bin/env python
import pygtk,gtk,pango

def do_print(widget):
    print_op = gtk.PrintOperation()
    settings = None
    
    if settings != None: 
        print_op.set_print_settings(settings)
    
    lines=[]
    for num in range(38):
        lines.append("this is line %i\n" % num)
#print_op.connect("begin_print", begin_print)
    print_op.connect("draw_page", draw_page, lines)
    print_op.set_n_pages(1)
    
    res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG)
    
    if res == gtk.PRINT_OPERATION_RESULT_APPLY:
        settings = print_op.get_print_settings()
    print settings
    
def draw_page(operation, context, page_nr, user_data=None):
        #print page_nr
        cr = context.get_cairo_context()
        width = int(context.get_width())
        height = int(context.get_height())
        print height
        
        cr.rectangle(0, 0, width, HEADER_HEIGHT)
        
        #@cr.set_source_rgb(0.8, 0.8, 0.8);
        cr.fill()
        
        layout = context.create_pango_layout()
        
        desc = pango.FontDescription("sans 14")
        layout.set_font_description(desc)
        

        print layout.get_width(),pango.SCALE
        layout.set_width(width * pango.SCALE)
        text_string="".join(user_data)
        layout.set_text(text_string)
        #layout.set_text("some text very very long things that may or may not get wrapped with the -1 setting.\nShould be wrapped correctly now")
        layout.set_wrap(pango.WRAP_WORD_CHAR)
        layout.set_alignment(pango.ALIGN_LEFT)
        
        x,layout_height = layout.get_size()
        print layout_height
        #print layout.get_line_count()
        print layout.get_iter().get_line_yrange()
        text_height = layout_height / pango.SCALE
        
        #cr.move_to(0,  (HEADER_HEIGHT - text_height) / 2)
        cr.move_to(0,10)
        cr.show_layout(layout)

def exit(widget):
    gtk.main_quit()

HEADER_HEIGHT=0
window=gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect("destroy", exit)
b=gtk.Button("Print nao!")
b.connect("clicked", do_print)
window.add(b)
window.show_all()
gtk.main()

