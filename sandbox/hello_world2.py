#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def hello(c):
    #c.drawString(100,100,"Hello World")
    # move the origin up and to the left
    c.translate(inch,inch)
    # define a large font
    c.setFont("Helvetica", 14)
    # choose some colors
    c.setStrokeColorRGB(0.2,0.5,0.3)
    c.setFillColorRGB(1,0,1)
    # draw some lines
    c.line(0,0,0,1.7*inch)
    c.line(0,0,1*inch,0)
    # draw a rectangle
    c.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)
    # make text go straight up
    c.rotate(90)
    # change color
    c.setFillColorRGB(0,0,0.77)
    # say hello (note after rotate the y coord needs to be negative!)
    c.drawString(0.3*inch, -inch, "Hello World")
    c.rotate(-90)
    c.drawString(2*inch, 2*inch, "Testing 1 2 3")



c = canvas.Canvas("hello2.pdf")#, pagesize=((6*72),(4*72)))
hello(c)
c.showPage()
c.save()
