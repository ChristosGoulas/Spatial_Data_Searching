import sys 
import time
import io
import math


def mindist(x_check,y_check):
    global x
    global y
    dist = math.sqrt((abs(x_check-x))**2 + abs((y_check-y))**2)
    return dist

k=int(sys.argv[1])
x=float(sys.argv[2])
y=float(sys.argv[3])
my_list=[]
id_list=[]
for i in range(0,k):
    my_list.append(float(1000000000.0))
    id_list.append("")
with open('ids.txt','r') as id_file:
    for line in id_file:
        l=line.split()
        dis=mindist(float(l[1]),float(l[0]))
        tupl=str(l[0])
        for i in range(0,k):
            if(my_list[i]>=dis):
                my_list.pop(i)
                my_list.append(dis)
                id_list.pop(i)
                id_list.append(tupl)
id_file.close()
for i in range(0,10):
    print(my_list[i])
    print(id_list[i])
