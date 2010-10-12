#!/usr/bin/env python

from __future__ import print_function

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus import KeepTogether,TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

__all__=['PageSizeError', 'NoteCard', 'Recipe', 'do_print_out']

class PageSizeError(Exception):
    def __init__(self, size):
        self._size=size
    def __str__(self):
        return '%s is an unsupported page size, only 4"x6" is supported currently' % (self._size)

class FourBySixNotecard(BaseDocTemplate):
    def __init__(self,filename, title, author):
        self.filename = filename
        #          (WIDTH,HEIGHT)
        pageSize = (6*inch,4*inch)
        F = Frame(0,0,6*inch,4*inch,
                  leftPadding=0.5*inch,
                  bottomPadding=0.50*inch,
                  rightPadding=0.25*inch,
                  topPadding=0.25*inch,
                  showBoundary=0)
        PT = PageTemplate(id="Notecard", frames=[F,])
        BaseDocTemplate.__init__(self, self.filename,
                                 pageTemplates=[PT,], 
                                 pagesize=pageSize,
                                 showBoundary=0,
                                 leftMargin=0,
                                 rightMargin=0,
                                 topMargin=0,
                                 bottomMargin=0,
                                 allowSplitting=1,
                                 title=title,
                                 author=author)
    def build(self,flowables):
        BaseDocTemplate.build(self, flowables=flowables,
                              filename=self.filename,
                              canvasmaker=canvas.Canvas)
        
class NoteCard(BaseDocTemplate):
    def __init__(self,title, author, filename=None, size=(4,6), sb=0):
        (height,width,) = size
        if not filename:
            self.filename="%s-%sx%s.pdf" % (title,str(height),str(width))
        else:
            self.filename=filename
        pagesize = (width*inch,height*inch)
        F=Frame(0,0,width*inch,height*inch,
                  leftPadding=0.5*inch,
                  bottomPadding=0.50*inch,
                  rightPadding=0.25*inch,
                  topPadding=0.25*inch,
                  showBoundary=sb)
        PT = PageTemplate(id="Notecard", frames=[F,])
        BaseDocTemplate.__init__(self, self.filename,
                                 pageTemplates=[PT,], 
                                 pagesize=pagesize,
                                 showBoundary=sb,
                                 leftMargin=0,
                                 rightMargin=0,
                                 topMargin=0,
                                 bottomMargin=0,
                                 allowSplitting=1,
                                 title=title,
                                 author=author)

    def build(self,flowables):
        BaseDocTemplate.build(self, flowables=flowables,
                              filename=self.filename,
                              canvasmaker=canvas.Canvas)

class IngredientsStyle(ParagraphStyle):
    defaults = {
        'fontName':'Times-Roman',
        'fontSize':10,
        'leading':12,
        'leftIndent':10,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'Times-Roman',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,
        }
    def __init__(self,):
        ParagraphStyle.__init__(self,"ingredentsStyle")

class CenterStyle(ParagraphStyle):
    defaults = {
        'fontName':'Times-Roman',
        'fontSize':10,
        'leading':12,
        'leftIndent':10,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_CENTER,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'Times-Roman',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,
        }
    def __init__(self,):
        ParagraphStyle.__init__(self,"ingredentsStyle")

class Recipe():
    def __init__(self, title="Title", preptime="15", cooktime="30",
                 ingredients=[], instructions=[], author="pyRMS"):
        self.Title=str(title)
        self.Preptime=int(preptime)
        self.Cooktime=int(cooktime)
        self.Ingredients=list(ingredients)
        self.Instructions=list(instructions)
        self.Author=str(author)

    def ingredients_columns(self,columns=2):
        #stupid rounding needs to handle when it splits evenly.
        rows=int(round((len(self.Ingredients)/float(columns))+0.4))
        table = [[] for x in range(rows)]
        for x in range(rows*columns):
            try:
                table[x%rows].append(self.Ingredients[x])
            except IndexError:
                table[x%rows].append("")
        return table

    def __str__(self,):
        return "\n".join([self.Title, 
                            str(self.Preptime),
                            str(self.Cooktime),
                          ] +
                          ["\n",] +
                          self.Ingredients +
                          ["\n",] +
                          self.Instructions)

def get_doc(title, author, size=(4,6)):
    """Takes a size (H,W), title, and author, and returns a page class.

    get_doc(title, author,size)
    size must be a tuple (height,width) defaults to (4,6).
    returns a tuple of (document,columns), this allows setting of recipe
    columns based on width, as of right now 2 is returned unless size 
    is (11,8.5). 
    """
    
    #add some more logic for guessing columns here. NoteCard accepts any 
    #(height,width) tuple. 
    doc=NoteCard(title, author, size=size)
    columns = (3 if size == (11,8.5) else 2)
    return (doc,columns)

def parse_simple_txt(f):
    """Parses a very simple text file.

    This is fragile, and a more robust parser will need to added in the future.
    Parsers should return a Recipe object. do_print_out() will print
    a recipe object.

    """
    try:
        txt_file=open(f)
    except IOError:
        if isinstance(f,list):
            lines = f
        else:
            raise
    else:
        lines = txt_file.readlines()
        r = Recipe()
        sections = [x.strip("\n") for x in "".join(lines).split("\n\n",3)]
        [header,r.Ingredients,r.Instructions]=[x.split("\n") for x in sections]
        [r.Title, r.Preptime, r.Cooktime] = header
        return r
    return None

def instructions_paragraph(recipe):
    """Add <seq> tags to the front of each Instruction"""
    return ["".join(["<seq>. ", x]) for x in recipe.Instructions]

def do_print_out(recipe,page_size,filename=None):
    """do_print_out(recipe,page_size,filename=None)

    This makes makes a pdf out of the recipe opject on the size paper requested.
    recipe is a recipe object.
    page_size is (height,width).
    If no file name is provided the automatic name generator is used. 
    See NoteCard class for more details.
    """

    try:
        size=tuple(size)
        (doc,columns)=get_doc(recipe.Title, recipe.Author, page_size)
    except PageSizeError as err:
        print(err)
    except TypeError:
        print("size needs to be a iterable")
    else:
        styles = getSampleStyleSheet()
        btext="\xe2\x80\xa2"
        n_style=styles["Normal"]
        c_style=CenterStyle()
        ing_style=IngredientsStyle()
        Story=[]
        spacer=Spacer(1,0.05*inch)

        #Header block
        Story.append(Paragraph(recipe.Title, styles["title"]))
        times="Prep Time: %s Min, Cook Time: %s Min" %(recipe.Preptime,recipe.Cooktime)
        Story.append(Paragraph(times,c_style))
        Story.append(spacer)
        
        #ingredients block
        table=recipe.ingredients_columns(columns)
        table=[[Paragraph(y,ing_style,bulletText=btext) for y in x] for x in table] 
        table=Table(table)
        pad=0
        #make the table take up less space.
        table.setStyle(TableStyle([("BOTTOMPADDING",(0,0),(-1,-1),pad),
                                   ("TOPPADDING", (0,0),(-1,-1),pad),
                                   ("RIGHTPADDING", (0,0),(-1,-1),pad),
                                   ("LEFTPADDING", (0,0),(-1,-1),pad)]))
        Story.append(table)
        Story.append(spacer)
        
        #directions block
        p = [Paragraph(x,n_style) for x in instructions_paragraph(recipe)]
        #fix making more than one printout per python instance.
        #otherwise the directions count overall not per printout.
        p += [Paragraph("<seqreset>",n_style)] 
        Story.append(KeepTogether(p))
        doc.build(Story)



if __name__ == "__main__":
    from sys import argv,exit
    #input_file = argv[1]
    if "--help" in argv:
        print("""Makes pdfs from simple text files, the format follows:

${title}
${preptime} #as an int
${cooktime} #as an int
${2 blank lines}
ingriedients one per line
${2 blank lines}
directions one per line""")
        exit(0)
    for f in argv[1:]:
        recipe=parse_simple_txt(f)
    
        do_print_out(recipe,(4,6))
        do_print_out(recipe,(3,5))
        do_print_out(recipe,(11,8.5))

