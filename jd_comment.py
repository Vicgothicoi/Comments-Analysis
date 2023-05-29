import os
import time
import json
import random
import csv
import re
import cv2

import jieba
import requests
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 词云形状图片
WC_MASK_IMG = 'src/jdicon.jpg'
# 词云字体
WC_FONT_PATH = 'src/simhei.ttf'

# 数据保存文件
COMMENT_FILE_PATH = 'output/jd_comment.txt'
COMMENT_CSV_PATH = 'output/jd_comment.csv'
IMG_PATH='output/jd_ciyun.jpg'

"""
生成本地资料
name = input("Please enter the name:")
COMMENT_FILE_PATH = 'output/'+name+'.txt'
COMMENT_CSV_PATH = 'output/'+name+'.csv'
IMG_PATH='output/'+name+'_词云'+'.jpg'
"""

def spider_comment(page=0, key=0):
    """
    爬取京东指定页的评价数据
    :param page: 爬取第几，默认值为0
    """

    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4646&productId=' + key + '' \
          '&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % page
    kv = {'user-agent': 'Mozilla/5.0', 'Referer': 'https://item.jd.com/'+ key + '.html'}

    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
    # 截取json数据字符串
    r_json_str = r.text[26:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据
    r_json_comments = r_json_obj['comments']
    # 遍历评论对象列表
    for r_json_comment in r_json_comments:
        # 以追加模式换行写入每条评价
        with open(COMMENT_FILE_PATH, 'a+',encoding="utf8") as file:
            file.write(r_json_comment['content'] + '\n')
        # 打印评论对象中的评论内容
        print(r_json_comment['content'])


def batch_spider_comment(key):
    """
    批量爬取京东评价
    """
    # 写入数据前先清空之前的数据
    if os.path.exists(COMMENT_FILE_PATH):
        os.remove(COMMENT_FILE_PATH)
    #key = input("Please enter the address:")
    #key = re.sub("\D","",key)
    #通过range来设定爬取的页面数
    for i in range(10):
        spider_comment(i,key)
        # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
        time.sleep(random.random() * 5)

def txt_change_to_csv():
    with open(COMMENT_CSV_PATH, 'w+', encoding="utf8", newline='')as c:
        writer_csv = csv.writer(c, dialect="excel")
        with open(COMMENT_FILE_PATH, 'r', encoding='utf8')as f:
            # print(f.readlines())
            for line in f.readlines():
                # 去掉str左右端的空格并以空格分割成list
                line_list = line.strip('\n').split(',')
                print(line_list)
                writer_csv.writerow(line_list)


def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open(COMMENT_FILE_PATH,encoding="utf8") as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=False)#精确模式
        wl = " ".join(wordlist)
        print(wl)
        return wl

def create_word_cloud():
    """
    生成词云
    """
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    # 生成词云
    wc.generate(cut_word())
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    wc.to_file(IMG_PATH)
    return cv2.imread(IMG_PATH)


def main(key):
    key = str(key)
    key = re.sub("\D","",key)

    # 爬取数据
    batch_spider_comment(key)

    #转换数据
    txt_change_to_csv()

    # 生成词云
    img = create_word_cloud()
    return img    

if __name__ == '__main__':
    key='https://item.jd.com/100048276065.html'
    img = main(key)
    cv2.namedWindow("img", 0)
    cv2.resizeWindow("img", 720, 720)#调整显示窗口大小
    cv2.imshow('img',img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()