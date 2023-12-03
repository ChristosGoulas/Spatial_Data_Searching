#Christos Goulas
#A.M.: 2677

import sys 
import time
import io

x_low=float(sys.argv[1])
x_high=float(sys.argv[2])
y_low=float(sys.argv[3])
y_high=float(sys.argv[4])
print("x_low",x_low)
print("x_high",x_high)
print("y_low",y_low)
print("y_high",y_high)
x_array=[]
y_array=[]
#creating a dictionary from grid dir, using as key x,y coordinate and value a list with the other 2 elements of the list
grid_dict=dict()
with open("grid.dir","r") as dir_file:
    first_line=dir_file.readline()
    grid=first_line.split()
    x_min=float(grid[0])
    x_max=float(grid[1])
    y_min=float(grid[2])
    y_max=float(grid[3])
    for line in dir_file:
        l=line.split()
        id=str(l[0])+str(l[1])
        l.pop(0)
        l.pop(0)        
        d={id:l}
        grid_dict.update(d)
dir_file.close()
x_adder=float((x_max-x_min)/10)
y_adder=float((y_max-y_min)/10)
for i in range(0,11):
    x_array.append(x_min+(i*x_adder))
    y_array.append(y_min+(i*y_adder))
print("<--X Array-->")
for i in range(0,11):
    if(len(str(x_array[i]))>6):
        x_array[i]=round(x_array[i],6)
    print(i,":",x_array[i])
print("<--Y Array-->")
for i in range(0,11):
    if(len(str(y_array[i]))>6):
        y_array[i]=round(y_array[i],6)
    print(i,":",y_array[i])

flag_x_low=0
flag_y_low=0
flag_x_high=0
flag_y_high=0
for i in range(0,11):
    if(x_array[i]==x_low) and flag_x_low==0:
        flag_x_low=2
        xl=i
    if(x_array[i]==x_high and flag_x_high==0):
        flag_x_high=2
        xh=i
    if(y_array[i]==y_low and flag_y_low==0):
        flag_y_low=2
        yl=i
    if(y_array[i]==y_high and flag_y_high==0):
        flag_y_high=2
        yh=i
    if(x_low<x_array[i] and flag_x_low==0):
        flag_x_low=1
        if(i==0):
            xl=0
        else:
            xl=i-1
    if(x_high<x_array[i] and flag_x_high==0):
        flag_x_high=1
        if(i==0):
            xh=0
        else:
            xh=i
    if(y_low<y_array[i] and flag_y_low==0):
        flag_y_low=1
        if(i==0):
            yl=0
        else:
            yl=i-1
    if(y_high<y_array[i] and flag_y_high==0):
        flag_y_high=1
        if(i==0):
            yh=0
        else:
            yh=i
print(flag_x_low)
print(flag_x_high)
print(flag_y_low)
print(flag_y_high)
print("xl: ",xl)
print("xh: ",xh)
print("yl: ",yl)
print("yh: ",yh)
read_list=[]
buf=[]
ch=0
print_counter=0
with open("grid.grd","r") as grd_file:
    for x in range(xl,xh):
        for y in range(yl,yh):
            if(x==0 and (y==8 or y==9)):
                continue
            if(flag_x_high==flag_x_low==flag_y_high==flag_y_low==2):
                key=str(x)+str(y)
                read_list=grid_dict.get(key)
                to_seek=int(read_list[0])
                cntr=int(read_list[1])
                grd_file.seek(to_seek)
                while(cntr>0):
                    print(str(x)+" "+str(y)+" "+str(grd_file.readline()))
                    print_counter+=1
                    cntr=cntr-1
            else:
                key=str(x)+str(y)
                read_list=grid_dict.get(key)
                to_seek=int(read_list[0])
                cntr=int(read_list[1])
                grd_file.seek(to_seek)
                if(x==xl or y==yl or x==xh-1 or y==yh-1):
                    while(cntr>0):
                        l=grd_file.readline().split()
                        if(float(l[1])>=x_low and float(l[1])<=x_high and float(l[2])>=y_low and float(l[2])<=y_high):
                            print("CHECKED: "+str(x)+" "+str(y)+" "+str(l[0])+" "+str(l[1])+" "+str(l[2]))
                            print_counter+=1
                        cntr=cntr-1
                else:
                    while(cntr>0):
                        print("UNCHECKED: "+str(x)+" "+str(y)+" "+str(grd_file.readline()))
                        print_counter+=1
                        cntr=cntr-1                    
print("PC:",print_counter)