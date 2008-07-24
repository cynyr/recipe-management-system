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
            print "could not find file: %s : skipping" % path
        else:
            try:
                config_txt=config_file.readlines()
            except Exception, e:
                print "could not read file"
                break
            else:
                while config_txt.count("\n"):
                    config_txt.remove("\n")
                prev_line=""
                for line in config_txt:
                    #print line[-2:] == '\\\n'
                    if line[-2:] == "\\\n":
                        prev_line=prev_line + line.strip().strip("\\\n")
                        #print prev_line
                    else:    
                        conf_line=prev_line + line.strip("\n").strip()
                        prev_line=""
                        line=line.strip("\n").strip()
                        if conf_line[0] != "#" and conf_line.count("="):
                            entry=conf_line.split("=", 1)
                            default_options[entry[0]]=entry[1].split("#", 1)[0].strip()
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
    print "----------- output --------"
    for key in results:
        print key + "='" + results[key] + "'"
