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

__all__=['NoteCard', 'Recipe', 'do_print_out']


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
    def __init__(self, title="Title", preptime="0 Min", cooktime="0 Min",
                 servings="4", ingredients=[], instructions=[],
                 author="pyRMS", *args, **kwords):
        self.Title=str(title)
        self.Preptime=str(preptime)
        self.Cooktime=str(cooktime)
        self.Ingredients=list(ingredients)
        self.Instructions=list(instructions)
        self.Author=str(author)
        self.Servings=str(servings)

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

    @property
    def instructions_paragraph(self,):
        return ["".join(["<seq>. ", x]) for x in self.Instructions]

    def __str__(self,):
        return "\n".join([self.Title, 
                            str(self.Preptime),
                            str(self.Cooktime),
                            "Servings: " + str(self.Servings),
                          ] +
                          ["\n",] +
                          self.Ingredients +
                          ["\n",] +
                          self.Instructions)

def get_doc(title, author, size=(4,6), filename=None):
    """Takes a size (H,W), title, and author, and returns a page class.

    get_doc(title, author,size)
    size must be a tuple (height,width) defaults to (4,6).
    returns a tuple of (document,columns), this allows setting of recipe
    columns based on width, as of right now 2 is returned unless size 
    is (11,8.5). 
    """
    
    #add some more logic for guessing columns here. NoteCard accepts any 
    #(height,width) tuple. 
    doc=NoteCard(title, author, size=size, filename=filename)
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
        try:
            lines = list(f)
        except:
            raise
    else:
        lines = txt_file.readlines()
        r = Recipe()
        sections = [x.strip("\n") for x in "".join(lines).split("\n\n",3)]
        [header,r.Ingredients,r.Instructions]=[x.split("\n") for x in sections]
        header=[x.split(":")[-1].strip() for x in header]
        [r.Title, r.Preptime, r.Cooktime, r.Servings] = header
        return r
    return None

def do_print_out(recipe,page_size,filename=None):
    """do_print_out(recipe,page_size,filename=None)

    This makes makes a pdf out of the recipe opject on the size paper requested.
    recipe is a Recipe object.
    page_size is (height,width).
    If no file name is provided the automatic name generator is used. 
    See NoteCard class for more details.
    """

    try:
        page_size=tuple(page_size)
    except TypeError:
        print("size needs to be a iterable")
    else:
        (doc,columns)=get_doc(recipe.Title,
                              recipe.Author,
                              page_size,
                              filename=filename)
        styles = getSampleStyleSheet()
        btext="\xe2\x80\xa2"
        n_style=styles["Normal"]
        c_style=CenterStyle()
        ing_style=IngredientsStyle()
        Story=[]
        spacer=Spacer(1,0.05*inch)

        #Header block
        Story.append(Paragraph(recipe.Title, styles["title"]))
        #string mod works inside vars as well. s="%s"; s%(foo,)
        time_s="Prep Time: %s, Cook Time: %s"
        times=time_s %(recipe.Preptime,recipe.Cooktime)
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
        p = [Paragraph(x,n_style) for x in recipe.instructions_paragraph]
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

