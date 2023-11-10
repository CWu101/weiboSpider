from SendWeiboSpider import send_spider
from TopicCloud import draw_topiccloud
from WordCloud import draw_wordcloud
from FindGeo import find_geo, get_location
if __name__=="__main__":
    send_spider()
    draw_topiccloud()
    draw_wordcloud()
    find_geo()
    get_location()