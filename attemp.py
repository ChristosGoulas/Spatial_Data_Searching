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
flag=0
elements=0
chars_to_write=0
chars=0
with open('ids.txt','r') as read_file:
    with open("grid.grd","w")as write_file:
        with open("grid.dir","w")as dir_file:
            for i in range(0,11):
                for j in range(0,11):
                    if(flag==0):
                        flag=1
                        chars_to_write=chars
                    for line in read_file:
                        l=line.split()
                        if(float(l[1])<x_array[i]):
                            if(float(l[2])<y_array[j]):
                                chars+=write_file.write(l[0]+" "+l[1]+" "+l[2]+"\n")
                                elements+=1
                        if(i==10):
                            if(float(l[1])<=x_array[i] and float(l[2])<y_array[j]):
                                chars+=write_file.write(l[0]+" "+l[1]+" "+l[2]+"\n")
                                elements+=1
                        if(j==10):
                                if(float(l[1])<x_array[i] and float(l[2])<=y_array[j]):
                                    chars+=write_file.write(l[0]+" "+l[1]+" "+l[2]+"\n")
                                    elements+=1 
                        if(i==10 and j==10):
                            if(float(l[1])<=x_array[i] and float(l[2])<=y_array[j]):
                                chars+=write_file.write(l[0]+" "+l[1]+" "+l[2]+"\n")
                                elements+=1
                    read_file.seek(0)
        dir_file.close()
    write_file.close()
read_file.close()
