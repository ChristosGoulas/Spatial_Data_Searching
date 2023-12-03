#Christos Goulas 
#A.M.:2677

import time
import io
import fileinput

s_time = time.time()
counter=0
x_min=9999999
x_max=-9999999
y_min=9999999
y_max=-9999999
x_array=[]
y_array=[]
with open('Beijing_restaurants.txt','r') as b_file:
    next(b_file)
    for line in b_file:
        sp=line.strip("\n").split(" ")
        if(x_min>float(sp[0])):
            x_min=float(sp[0])
        if(x_max<float(sp[0])):
            x_max=float(sp[0])
        if(y_min>float(sp[1])):
            y_min=float(sp[1])
        if(y_max<float(sp[1])):
            y_max=float(sp[1])
    print("x_min: "+str(x_min))
    print("x_max: "+str(x_max))
    print("y_min: "+str(y_min))
    print("y_max: "+str(y_max))
b_file.close()
x_adder=float((x_max-x_min)/10)
y_adder=float((y_max-y_min)/10)
print("x_adder: ",x_adder)
print("y_adder: ",y_adder)
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
counter=1
tostring=""
with open('Beijing_restaurants.txt','r') as b_file:
    next(b_file)    
    with open('ids.txt','w+') as id_file:
        for b_line in b_file:
            l=b_line.split()
            tostring+=str(counter)
            for i in l:
                tostring+=" "+str(i)
            id_file.write(tostring+"\n")
            tostring=""
            counter+=1
    id_file.close()
b_file.close()


print("Loading...")

#I'm going to save all the information that i want to write to the grd and then write it
dimension=10
list_of_lists=[[[] for _ in range(dimension)] for _ in range(dimension)]
matrix_x=0
matrix_y=0
with open('ids.txt','r') as b_file:
    next(b_file)
    for line in b_file:
        l=line.split()
        for i in range (0,11):
            if(i==10 and float(l[1])==x_array[i]):
                matrix_x=i-1
                break
            if(float(l[1])==x_array[i]):
                matrix_x=i
                break
            if(float(l[1])<x_array[i]):
                matrix_x=i-1
                break
        for i in range(0,11):
            if(i==10 and float(l[2])==y_array[i]):
                matrix_y=i-1
                break
            if(float(l[2])==y_array[i]):
                matrix_y=i
                break
            if(float(l[2])<y_array[i]):
                matrix_y=i-1
                break
        list_of_lists[matrix_x][matrix_y].append(str(l[0])+" "+"%.6f"%float(l[1])+" "+"%.6f"%float(l[2]))
b_file.close()

meta_data=[[int for _ in range(dimension)] for _ in range(dimension)]
chars=0
flag=0
final=0
with open('grid.grd','w+') as grd_file:
    for i in range(0,10):
        for j in range(0,10):
            if(not(list_of_lists[i][j])):
                print(str(i)+" "+str(j)+":"+"EMPTY")
                flag=0
                continue
            if(flag==0):
                temp=grd_file.tell()
                print(temp)
                meta_data[i][j]=chars
                flag=1
            for l in list_of_lists[i][j]:
                final+=1
                chars+=grd_file.write(str(l)+"\n")
            flag=0
        flag=0
grd_file.close()

total=0
with open('grid.dir','w+') as dir_file:
    dir_file.write("%.6f"%x_min+" "+"%.6f"%x_max+" "+"%.6f"%y_min+" "+"%.6f"%y_max+"\n")
    for i in range(0,10):
        for j in range(0,10):
            if(len(list_of_lists[i][j])!=0 and meta_data[i][j]!=int):
                total+=len(list_of_lists[i][j])
                dir_file.write(str(i)+" "+str(j)+" "+str(meta_data[i][j])+" "+str(len(list_of_lists[i][j]))+"\n")
            else:
                continue
dir_file.close()
print("--- %s seconds ---" % (time.time() - s_time))
print("TOTAL: ",total)
print("FINAL: ",final)
print("Total chars: ",chars)