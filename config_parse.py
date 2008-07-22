#!/usr/bin/env python

import os,sys

#home dir on posix at least is os.environ["HOME"]
print os.environ["HOME"]
config_file_path=".config/rms/rms.conf"
config_dic={}
try: 
    config_file=open(os.environ["HOME"]+ config_file_path, "r")
except Exception, e:
    raise
try:
    config_txt=config_file.readlines()
except Exception, e:
    raise
#print config_file.readlines()
while config_txt.count("\n"):
    config_txt.remove("\n")

for line in config_txt:
    line=line.strip("\n").strip()
    #print line
    #print "the first char is: " + line[0]
    #print line[0] != "#"
    if line[0] != "#" and line.count("="):
        entry=line.split("=", 1)
        #print entry
        config_dic[entry[0]]=entry[1]

print config_dic
