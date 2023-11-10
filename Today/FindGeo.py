import cpca
import pandas as pd
from io import StringIO
from datetime import datetime
import requests 
import csv


def print_location(add,date=""):
    now = datetime.now()
    add_list=[]
    if date=="":
        date= f"{now.year}-{now.month}-{now.day}"

     # 服务地址
    host = "https://api.map.baidu.com"

    # 接口地址
    uri = "/geocoding/v3"

    # 此处填写你在控制台-应用管理-创建应用后获取的AK
    ak = "dxb2VgoDdf6kDqw0nzIAyeBALqClSAdw"

    params = {
        "address":    add,
        "output":    "json",
        "ak":       ak
    }

    response = requests.get(url = host + uri, params = params)

    if response:
        lng=response.json()["result"]["location"]["lng"]
        lat=response.json()["result"]["location"]["lat"] 
    with open(f"Today/storage/{date}/coordination-{date}.csv", "a", encoding='utf-8', newline='') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerows([[add,str(lng),str(lat)]])
        print(add,lng,lat)



def get_location(date=""):
    now = datetime.now()
    add_list=[]
    if date=="":
        date= f"{now.year}-{now.month}-{now.day}"
    else:
        date=f"2023-{date[:2]}-{date[2:]}"
    with open(f"Today/storage/{date}/location-{date}.csv",'r', encoding='utf-8') as file:
        for i,line in enumerate(file):
            if(i>0):
                line=line.split(',')
                add_list.append(line[1]+line[2]+line[3])
    with open(f"Today/storage/{date}/coordination-{date}.csv", "w", encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(['name'], ['lng'], ['lat']))
    for add in add_list:
        print_location(add,date=date)

   
def find_geo(date=""):
    now = datetime.now()
    if date=="":
        date= f"{now.year}-{now.month}-{now.day}"
    else:
        date=f"2023-{date[:2]}-{date[2:]}"

    hot_str=""
    with open(f"Today/storage/{date}/hotboard-{date}.csv",'r', encoding='utf-8') as file:
        for i,line in enumerate(file):
            if(i>0):
                line=line.split(',')
                hot_str+=line[0]

    location_str = cpca.transform_text_with_addrs(hot_str, pos_sensitive=True)
    location_str=location_str.to_csv()
    data = StringIO(location_str.strip())

    # Create a DataFrame
    df = pd.read_csv(data)

    # Save the DataFrame to a CSV file
    csv_file = f"Today/storage/{date}/location-{date}.csv"
    df.to_csv(csv_file, index=False)

if __name__=="__main__":
    date=input("输入月日")
    find_geo(date)
    get_location(date)
    