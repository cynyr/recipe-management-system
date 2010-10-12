#!/usr/bin/env python
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
def cursormoves1(canvas):
    textobject = canvas.beginText()
    #textobject.setLeading(12)
    textobject.setTextOrigin(inch, 2.5*inch)
    textobject.setFont("Helvetica-Oblique", 14)
    lyrics = """well she hit Net Solutions
and she registered her own .com site now
and filled it up with yahoo profile pics
she snarfed in one night now
and she made 50 million when Hugh Hefner
bought up the rights now
and she'll have fun fun fun
til her Daddy takes the keyboard away
""".split('\n')
    for line in lyrics:
         textobject.textLine(line)
    textobject.setFillGray(0.4)
    textobject.textLines('''
    With many apologies to the Beach Boys
    and anyone else who finds this objectionable
    ''')
    canvas.drawText(textobject)

c = canvas.Canvas("textobject.pdf", pagesize=((6*inch),(4*inch)))
cursormoves1(c)
c.showPage()
c.save()
