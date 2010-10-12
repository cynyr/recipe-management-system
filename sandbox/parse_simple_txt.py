#!/usr/bin/env python

from __future__ import print_function
import sys

class Time():
    def __init__(self, time):
        self.value=int(time)
    def __int__(self,):
        return self.value
    def __str__(self,):
        return "time: %i min" % (self.value,)

class Recipe():
    def __init__(self, title="Title", preptime="15", cooktime="30",
                 ingredients=[], instructions=[]):
        self.Title=title
        self.Preptime=int(preptime)
        self.Cooktime=int(cooktime)
        self.Ingredients=list(ingredients)
        self.Instructions=list(instructions)

    def __str__(self,):
        return "\n".join([self.Title, 
                            str(self.Preptime),
                            str(self.Cooktime),
                          ] +
                          ["\n",] +
                          self.Ingredients +
                          ["\n",] +
                          self.Instructions)


def parse_simple_txt(f):
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
        sections = "".join(lines).split("\n\n",3)
        [header,r.Ingredients,r.Instructions]=[x.split("\n") for x in sections]
        [r.Title, r.Preptime, r.Cooktime] = header
        print(str(r))
        
    
if __name__ == "__main__":
    parse_simple_txt(sys.argv[1])
