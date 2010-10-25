#!/usr/bin/env python

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"

class MyDoc(BaseDocTemplate):
    def __init__(self, pageSize, ):
        pass

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def go():
    doc = SimpleDocTemplate("phello.pdf")
    doc.pagesize=(6*inch,4*inch)
    doc.leftMargin=0.25*inch
    doc.bottommargin=0.25*inch
    #doc.height=3.75*inch
    #doc.width=5.75*inch
    doc.height=4*inch
    doc.width=6*inch
    Story = []
    style = styles["Normal"]
    for i in range(3):
        bogustext = ("This is Paragraph number %s. " % i) *2
        p = Paragraph(bogustext, style)
        Story.append(p)
        #Story.append(Spacer(1,0.2*inch))
    l=[]
    for x in range(3):
        l.append(["row%i col1" % x, "row%i col2" % i])
    Story.append(Table(l))
    Story.append(Paragraph("Hello", styles["Title"]))
    #doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    doc.build(Story)

go()
