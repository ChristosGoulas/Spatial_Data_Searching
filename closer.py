#Christos Goulas
#A.M.: 2677

import sys 
import time
import io
import queue
import math

def initialize(q,x,y):
    flag=0
    if (x<x_array[0] or x>x_array[10] or y<y_array[0] or y>y_array[10]):
        flag=2
        for i in range(0,11):
            if(x<x_array[i] and i==0):
                matrix_x=i
                break
            if(x>x_array[i] and i==10):
                matrix_x=i-i
                break
            if(x<x_array[i]):
                matrix_x=i-1
                break
        for i in range(0,11):
            if(y<y_array[i] and i==0):
                matrix_y=i
                break
            if(y>y_array[i] and i==10):
                matrix_y=i-i
                break
            if(y<y_array[i]):
                matrix_y=i-1
                break
    if(not(flag==2)):
        for i in range (0,11):
            if(i==10 and x==x_array[i]):
                matrix_x=i-1
                break
            if(x<x_array[i]):
                matrix_x=i-1
                break
        for i in range(0,11):
            if(i==10 and y==y_array[i]):
                matrix_y=i-1
                break
            if(y<y_array[i]):
                matrix_y=i-1
                break
    key=str(matrix_x)+str(matrix_y)
    list_of_cells.append(key)
    if(not(flag==2)):
        print("In grid")
        q.put((float(0),key))
    else:
        print("Out of grid")
        q.put((float(0),key))

def closer_n(q,counter):
    global y_array
    global x_array
    while(counter>0):
        v=q.get()
        if(len(v[1])==2):
            print("You pop a cell")
            with open("grid.grd","r") as grd_file:
                if(not(v=="08" or v=="09")):
                    read_list=grid_dict.get(v[1])
                    to_seek=int(read_list[0])
                    cntr=int(read_list[1])
                    grd_file.seek(to_seek)
                    while(cntr>0):
                        l=grd_file.readline().split()
                        dis=mindist(float(l[1]),float(l[2]))
                        strl=str(l[0])+" "+str(l[1])+" "+str(l[2])
                        q.put((dis,strl))
                        cntr=cntr-1
                temp=v[1]
                x=int(temp[:-1])
                y=int(temp[1:])
                if(((str(x+1)+str(y+1)) in grid_dict) and (not((str(x+1)+str(y+1) in list_of_cells)))):
                    print("+1 +1 Been here")
                    key=str(x+1)+str(y+1)
                    list_of_cells.append(key)
                    new_x=x_array[x+1]
                    new_y=y_array[y+1]
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
                if(((str(x)+str(y+1)) in grid_dict) and (not((str(x)+str(y+1) in list_of_cells)))):
                    key=(str(x)+str(y+1))
                    print("+0 +1 Been here")
                    list_of_cells.append(key)
                    new_x=x
                    new_y=y_array[y+1]
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
                if((str(x+1)+str(y)) in grid_dict  and (not((str(x+1)+str(y) in list_of_cells)))):
                    print("+1 +0 Been here")
                    key=(str(x+1)+str(y))
                    list_of_cells.append(key)
                    new_x=x_array[x+1]
                    new_y=y
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
                if((str(x-1)+str(y-1)) in grid_dict  and (not((str(x-1)+str(y-1) in list_of_cells)))):
                    print("-1 -1 Been here")
                    key=str(x-1)+str(y-1)
                    list_of_cells.append(key)
                    new_x=x_array[x]
                    new_y=y_array[y]
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
                if((str(x)+str(y-1)) in grid_dict and (not((str(x)+str(y-1) in list_of_cells)))):
                    print("+0 -1 Been here")
                    key=(str(x)+str(y-1))
                    list_of_cells.append(key)
                    new_x=x
                    new_y=y_array[y]
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
                if((str(x-1)+str(y)) in grid_dict and (not((str(x-1)+str(y) in list_of_cells)))):
                    print("-1 +0 Been here")
                    key=(str(x-1)+str(y))
                    list_of_cells.append(key)
                    new_x=x
                    new_y=y_array[y]
                    dis=mindist(new_x,new_y)
                    q.put((dis,grid_dict.get(key)))
        else:
            print("print you pop element!")
            counter-=1
            yield str(v)


def mindist(x_check,y_check):
    global x
    global y
    dist = math.sqrt((abs(x_check-x))**2 + abs((y_check-y))**2)
    return dist



q = queue.PriorityQueue()
list_of_cells=[]
k=int(sys.argv[1])
x=float(sys.argv[2])
y=float(sys.argv[3])
grid_dict=dict()
x_array=[]
y_array=[]
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
###############
id="08"
d={id:"0 0"}
id="09"
d={id:"0 0"}
################
x_adder=float((x_max-x_min)/10)
y_adder=float((y_max-y_min)/10)
for i in range(0,11):
    x_array.append(x_min+(i*x_adder))
    y_array.append(y_min+(i*y_adder))
#print("<--X Array-->")
for i in range(0,11):
    if(len(str(x_array[i]))>6):
        x_array[i]=round(x_array[i],6)
    #print(i,":",x_array[i])
#print("<--Y Array-->")
for i in range(0,11):
    if(len(str(y_array[i]))>6):
        y_array[i]=round(y_array[i],6)
    #print(i,":",y_array[i])
##
initialize(q,x,y)
generator=closer_n(q,k)
#print(generator)
i=0
while(i<k):
    print(str(i)+" Element:"+next(generator))
    i+=1