#!/usr/bin/env python

from reportlab.pdfgen import canvas
def hello(c):
    c.drawString(100,100,"Hello World")
c = canvas.Canvas("hello.pdf", pagesize=((6*72),(4*72)))
hello(c)
c.showPage()
c.save()
