'''------------------爬虫-----------------'''
import requests
from lxml import etree
import csv
import jieba
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from datetime import datetime
now = datetime.now()

import os

find_tag = 1
if(find_tag):
     driver = webdriver.Chrome()


def save(name, link, hot, tag):
    os.makedirs("Today/storage", exist_ok=True)
    os.makedirs(f"Today/storage/{now.year}-{now.month}-{now.day}", exist_ok=True)
    with open(f"Today/storage/{now.year}-{now.month}-{now.day}/hotboard-{now.year}-{now.month}-{now.day}.csv", "w", encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(['name'], ['link'], ['hot'], ['tag']))
        writer.writerows(zip(name, link, hot, tag))
        
def check(text):
    seg_list = jieba.cut(text, cut_all=False)
    with open('ciku.txt', 'r', encoding='utf-8') as f:
        keywords = set(f.read().splitlines())
    return any(word in keywords for word in seg_list)

def get_weibo_hot_search(find_tag=find_tag):
    url = "https://s.weibo.com/top/summary"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        'cookie'    : "SINAGLOBAL=5701031797732.083.1638971150198; SUB=_2AkMW7DFkf8NxqwFRmP0QzGvkaIR1zgnEieKgsMC_JRMxHRl-yT9jqhErtRB6PWwfi8IMi4nS63fCLKIwRiYKqexEzF_Q; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFPkNiIHiOqUjBBn8.B.qFu; _s_tentry=cn.bing.com; Apache=9978275422977.867.1639488984604; UOR=,,cn.bing.com; ULV=1639488984639:4:4:1:9978275422977.867.1639488984604:1639061325022"
    }

    response = requests.get(url, headers=headers)
    html_obj = etree.HTML(response.content)

    name_list = html_obj.xpath('//td/span/preceding-sibling::a/text()')
    link_list = html_obj.xpath('//td/span/preceding-sibling::a/@href')
    hot_list  = html_obj.xpath('//td//span/text()')
    tag_list  = []
    if(find_tag):
        for i,name in enumerate(name_list):
            tag_url = f"https://m.s.weibo.com/vtopic/detail_new?click_from=searchpc&q=%23{name}%23"
            driver.get(tag_url)
            if(i==0):
                wait_time=3
            else:
                wait_time=1
            try:
                # 设置WebDriverWait等待时间为100秒
                wait = WebDriverWait(driver, wait_time)
                # 等待直到元素出现
                tag = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='data']")))
                # 如果元素出现，提取文本
                tag_list.append(tag.text.strip() if tag.text else "暂无")
            except TimeoutException:
                tag_list.append("暂无")
            print(name,tag_list[i])
    else:
        for name in name_list :
            tag_list.append("none")


    topics_with_link_and_hot=[]
    for name, add, hot, tag in zip(name_list, link_list,hot_list, tag_list):
        # 假设 'hot' 是之前定义好的字符串
        matches = re.findall(r'\d+', hot)

        # 确保找到了至少一个匹配项
        if matches:
            hot_number = int(matches[0])
        else:
            hot_number = 0  # 或者设置为你认为合适的默认值

        topics_with_link_and_hot.append((name, f"https://s.weibo.com{add}", hot_number, tag))
        print(name,hot_number,tag)

    return topics_with_link_and_hot

def send_spider():
    topics = get_weibo_hot_search()
    save([topic[0] for topic in topics], [topic[1] for topic in topics],[topic[2] for topic in topics],[topic[3] for topic in topics])
