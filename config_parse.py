#!/usr/bin/env python
def ParseConfigFile(paths,default_options={}):
    comment_markers=[';','#','//','/']
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
                    if line[-2:] == "\\\n":
                        prev_line=prev_line + line.strip().strip("\\\n")
                    else:    
                        conf_line=prev_line + line.strip("\n").strip()
                        prev_line=""
                        line=line.strip("\n").strip()
                        #if (conf_line[0] != "#" or conf_line[0] != ";") and conf_line.count("="):
                        #if conf_line[0] not in comment_markers and conf_line.count("="):
                        is_comment=False
                        for marker in comment_markers:
                            if conf_line.strip().find(marker) == 0:
                                is_comment=True
                        if not is_comment:
                            entry=conf_line.split("=", 1)
                            value=entry[1]
                            for marker in comment_markers:
                                if entry[1].count(marker):
                                    value=value.split(marker,1)[0].strip()
                            default_options[entry[0]]=value
                        is_comment=False
                            #print (marker,conf_line)
                            #print conf_line,conf_line.strip().find(marker)
                            #if (conf_line.strip().find(marker) != 0) and conf_line.count("=") >=1:
                                #entry=conf_line.split("=", 1)
                                #print entry[1].split(marker, 1)[0].strip()
                                #value=""
                                #for mark in comment_markers:
                                    #if mark in entry[1]:
                                        #value=entry[1].split(mark, 1)[0].strip()
                                #if value=="":
                                    #value=entry[1].strip()
                                #default_options[entry[0]]=value
                                #value=""
    return default_options

if __name__ == "__main__":
    import sys
    results=ParseConfigFile(sys.argv[1:])
    print "----------- output --------"
    for key in results:
        print key + "='" + results[key] + "'"
