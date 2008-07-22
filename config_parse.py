#!/usr/bin/env python

#import os,sys

#home dir on posix at least is os.environ["HOME"]
#print os.environ["HOME"]
#config_file_path=".config/rms/rms.conf"
#config_dic={}
def ParseConfigFile(paths,default_options={}):
    for path in paths:
        try: 
            config_file=open(path)
        except Exception, e:
            print "could not find file: %s :skipping" % path
        else:
            try:
                config_txt=config_file.readlines()
            except Exception, e:
                print "could not read file"
                break
            else:
                while config_txt.count("\n"):
                    config_txt.remove("\n")
            
                for line in config_txt:
                    line=line.strip("\n").strip()
                    if line[0] != "#" and line.count("="):
                        entry=line.split("=", 1)
                        default_options[entry[0]]=entry[1]
    return default_options

#default_options=dict(
    #database_host="foo.foo.org",
    #database_uid="anon",
    #database_passwd="12345",
    #database_db="foo",
    #)
#
if __name__ == "__main__":
    #paths=["/etc/rms/rms.conf","/home/cynyr/.config/rms/rms.conf",]
    import sys
    results=ParseConfigFile(sys.argv[1:])
    for key in results:
        print key + "=" + results[key]
