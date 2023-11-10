
add_list=[]
name_list=[]
name_dict={}
for i in range(7,11):
    with open(f"Today/storage/2023-11-{i}/coordination-2023-11-{i}.csv","r" ,encoding='utf-8') as file:
        for i,line in enumerate(file):
            if(i>0):
                line=line.split(',')
                add_list.append([line[0],line[1],line[2].strip(),1])
#print(add_list)
for i,item in enumerate(add_list):
    name_list.append(item[0])
for name in name_list:
    if(name not in name_dict):
        name_dict[name]=100
    else:
        name_dict[name]+=100
print("var points =[")
for i,item in enumerate(add_list):
    print("{lat:"+str(add_list[i][2])+",lng:"+str(add_list[i][1])+",count:"+str(name_dict[add_list[i][0]])+"}",end="")
    if i!=len(add_list)-1:
        print(",",end="")
    else:
        print("\n];")