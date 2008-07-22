#!/usr/bin/env python
import re
def ingredents_parse(line):
    line=line.strip().replace('of','')
    print line.find('[1234567890]')
    #if line.count("[1234567890]"):
        #print "we have a number"



buffer = ""
while True:
    line = raw_input()
    if line == "":
        break
    buffer += line
    buffer= buffer.strip()
    ingredents_parse(buffer)
    buffer=""

