# 导入所需的库
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import jieba
# 要生成词云的文本
from wordcloud import WordCloud, STOPWORDS

from datetime import datetime
def draw_topiccloud():
    now = datetime.now()

    # 加载停用词表，设置常用停用词
    stopwords = set()
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as file:
        for line in file:
            stopwords.add(line.strip())

    text_weighted={}

    with open(f'Today/storage/{now.year}-{now.month}-{now.day}/hotboard-{now.year}-{now.month}-{now.day}.csv', 'r', encoding='utf-8') as file:
        linenum = 0
        for line in file:
            if linenum > 0:
                content = line.split(',')
                words = content[3].strip()
                if(words in text_weighted):
                    text_weighted[words]+=int(content[2].strip())
                else:
                    text_weighted[words]=int(content[2].strip())+100
            linenum += 1
    print(text_weighted)
    text_weighted["暂无"]=0
    font_path = 'C:\\Windows\\Fonts\\simhei.ttf'

    # 创建词云对象
    wordcloud = WordCloud(#stopwords=stopwords, 
                        font_path=font_path, 
                        width = 800, height = 800,
                        background_color ='white',
                        min_font_size = 5).generate_from_frequencies(text_weighted)

    # 显示生成的词云
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.imsave(f"Today/storage/{now.year}-{now.month}-{now.day}/TopicToday-{now.year}-{now.month}-{now.day}.jpg",wordcloud.to_array())