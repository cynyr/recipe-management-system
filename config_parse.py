#!/usr/bin/env python
def ParseConfigFile(paths,default_options={}):
    """ parse a configuration file and return a dictonary
        
        Parse a config file using the below comment markers, and return
        a dictionary with the option name as the key and the value as the value.
        Trailing comments are supported, 
    """
    comment_markers=[';','#','//','/']
    for path in paths:
        try: 
            #try to open the file
            config_file=open(path)
        except Exception, e:
            #if it fails print a message and try the next file
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
    return default_options

if __name__ == "__main__":
    import sys
    results=ParseConfigFile(sys.argv[1:])
    print "----------- output --------"
    for key in results:
        print key + "='" + results[key] + "'"
