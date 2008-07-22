#!/usr/bin/env python

import os

#for thing in os.environ:
    #print (thing,os.environ[thing])
#home dir on posix at least is os.environ["HOME"]
print os.environ["HOME"]
config_file_path=".config/rms/config"
try: config_file=open(os.environ["HOME"]+ config_file_path, "r")
except Exception, e: raise
