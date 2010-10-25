#!/usr/bin/env python

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class FourBySixNotecard(BaseDocTemplate):
    def __init__(self,filename, title, author):
        self.filename = filename
        #          (WIDTH,HEIGHT)
        pageSize = (6*inch,4*inch)
        #Frame(x1, y1, width,height, leftPadding=6, bottomPadding=6,
        #      rightPadding=6, topPadding=6, id=None, showBoundary=0)
        F = Frame(0,0,6*inch,4*inch,
                  leftPadding=0.25*inch,
                  bottomPadding=0.50*inch,
                  rightPadding=0.25*inch,
                  topPadding=0.25*inch,
                  showBoundary=1)
        PT = PageTemplate(id="Notecard", frames=[F,])
        BaseDocTemplate.__init__(self, self.filename,
                                 pageTemplates=[PT,], 
                                 pagesize=pageSize,
                                 showBoundary=1,
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

class ingredentsStyle(ParagraphStyle):
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


def go():
    styles = getSampleStyleSheet()
    doc = FourBySixNotecard("phello2.pdf", "Test Title", "Andrew Frink")
    Story = []
    p = Paragraph("Title", styles["title"])
    Story.append(p)
    #for x in range(3):
        #l.append(["row%i col1" % x, "row%i col2" % i])
    l = [["row%i col1" % x, "row%i col2" % x] for x in range(3)]
    Story.append(Table(l))
    l = [["line of text" for x in range(4)]]
    #style = ParagraphStyle("ingredent", leftIndent=10, bulletText="\xe2\x80\xa2")
    style = ingredentsStyle()
    p = Paragraph("1/2 tablespoons of finely chopped grem en banana peeled",style, bulletText="\xe2\x80\xa2")
    l=[[p,p,p],
       ["test 1", "test 1", "test1"]]
    widths = [45,45,45]
    #Story.append(Table(l, colWidths=widths,))
    Story.append(Table(l,))
    for i in range(3):
        bogustext = ("This is Paragraph number %s. " % i) *2
        p = Paragraph(bogustext, styles["Normal"])
        Story.append(p)
        #Story.append(Spacer(1,0.2*inch))
    doc.build(Story)

go()
