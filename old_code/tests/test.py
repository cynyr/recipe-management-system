#!/usr/bin/env python
import readline
import os
import sys
from subprocess import Popen as popen

def findall(char,string):
    s=string
    l=[]
    i,c=0,0
    for foo in range(s.count(char)):
        i=s.find(char)
        l.append(i+c)
        s=s[i+1:]
        c=c+i+1

    return (string,l)

def parse_search_string(s):
    foo,indexes=findall(':',s)
    p=0
    l=[]
    s_len=len(s)
    for i in indexes:
        for j in range(i+1,s_len+1):
            #print (j,s_len)
            if j >= s_len:
                l.append(s[p:j].strip())
                break
            else:
                if s[j] == " ":
                    t=j
                if s[j] == ':':
                    l.append(s[p:t].strip())
                    p=t
                    break
    return [[y.lower() for y in x.split(':')] for x in l]

popen(["xterm","-sb","-sl","10000"])

input=raw_input("Enter Search String: ")
q=parse_search_string(input)
print q
d=dict(q)
print d

