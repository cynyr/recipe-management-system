l=range(1,17)
columns=3
rows=int(round((len(l)/float(columns))+0.4))
print (len(l),"%ix%i" %(columns,rows))
l2=[[] for x in range(rows)]
for x in range(rows*columns):
    #print(x,c_row)
    try:
        l2[x%rows].append(l[x])
    except IndexError:
        l2[x%rows].append(None)
    #c_row+=1
    #if c_row==rows:
        #c_row=0
    
print l2
#l3 = []
#for x in l2:
    #if len(x)<2:
        #x.append(None)
    #l3.append(x)
#print l3
