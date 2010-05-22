#!/usr/bin/env python

class base:
    """a test class"""

    def __init__(self):
        self.greeting="hello"
        self.salutation="goodby"
        self.afermative="yes"
        self.denial="no"
    
    def __str__(self):
        return "%s %s %s %s" % (self.greeting,self.salutation,self.afermative,self.denial)
    
class lvl1(base):
    
    def __init__(self):
        base.__init__(self)
        self.greeting="hi"

b=base()
l1=lvl1()
print b
print l1
