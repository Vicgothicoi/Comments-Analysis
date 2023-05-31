import pandas as pd
import snownlp
import matplotlib.pyplot as plt
import cv2


COMMENT_CSV_PATH = 'output/jd_comment.csv'
RESULT_PATH = 'output/result.csv'
IMG_PATH='output/fig.jpg'
PROCESSED='output/processed_comment_data.csv'
"""
生成本地资料
name = input("Please enter the name:")
COMMENT_CSV_PATH = 'output/'+name+'.csv'
RESULT_PATH = 'output/'+name+'result.csv'
IMG_PATH='output/'+name+'_评价'+'.jpg'
PROCESSED='output/processed_comment_data.csv'
"""
def read_csv():
    '''读取商品评论数据文件'''
    comment_data = pd.read_csv(COMMENT_CSV_PATH, encoding='utf-8',
                               sep='/n', index_col=None)   #sep='/n'替换了sep='\n'
    #返回评论作为参数
    return comment_data


def clean_data(data):
    '''数据清洗'''
    df = data.dropna()  # 消除缺失数据 NaN为缺失数据
    df = pd.DataFrame(df.iloc[:, 0].unique())  # 数据去重
    return df
    # print('数据清洗后：', len(df))


def clean_repeat_word(raw_str, reverse=False):
    '''去除评论中的重复使用的词汇'''
    if reverse:
        raw_str = raw_str[::-1]#元素从后从往前读取
    res_str = ''
    for i in raw_str:
        if i not in res_str:
            res_str += i
    if reverse:
        res_str = res_str[::-1]
    return res_str


def processed_data(filename):
    '''清洗完毕的数据，并保存'''
    df = clean_data(read_csv())#数据清洗
    ser1 = df.iloc[:, 0].apply(clean_repeat_word)#去除重复词汇
    df2 = pd.DataFrame(ser1.apply(clean_repeat_word, reverse=True))
    df2.to_csv(filename, encoding='utf-8', index_label=None, index=None)

sentiment_list = []

res_list = []


def test(filename, to_filename):
    '''商品评论-情感分析-测试'''
    with open(filename, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            s = snownlp.SnowNLP(line)
            #调用snownlp中情感评分s.sentiments
            if s.sentiments > 0.6:
                res = '喜欢'
                res_list.append(1)
            elif s.sentiments < 0.4:
                res = '不喜欢'
                res_list.append(-1)
            else:
                res = '一般'
                res_list.append(0)
            sent_dict = {
                '情感分析结果': s.sentiments,
                '评价倾向': res,
                '商品评论': line.replace('\n', '')
            }
            sentiment_list.append(sent_dict)
            #print(sent_dict)
        df = pd.DataFrame(sentiment_list)
        df.to_csv(to_filename, index=None, encoding='utf-8',
                  index_label=None, mode='w')


def data_virtualization():
    '''分析结果可视化，以条形图为测试样例'''
    #font = FontProperties(fname='src/simkai.ttf', size=14)

    plt.rcParams['font.sans-serif']=['SimHei'] 
    plt.rcParams['axes.unicode_minus']=False

    likes = len([i for i in res_list if i == 1])
    common = len([i for i in res_list if i == 0])
    unlikes = len([i for i in res_list if i == -1])

    plt.bar([1], [likes], label='喜欢')#（坐标，评论长度，名称）
    plt.bar([2], [common], label='一般')
    plt.bar([3], [unlikes], label='不喜欢')

    x=[1,2,3]
    label=['喜欢','一般','不喜欢']
    plt.xticks(x, label)

    plt.legend()#插入图例
    plt.xlabel('评价种类')
    plt.ylabel('评价数目')
    plt.title(u'商品评论情感分析结果-条形图')#, fontproperties=font)
    plt.savefig(IMG_PATH)
    return cv2.imread(IMG_PATH)
    #plt.show()
'''
def word_cloud_show():
    #将商品评论转为高频词汇的词云
    wl = word_cloud_creation('output/jd_comment.csv')
    wc = word_cloud_settings()
    word_cloud_implementation(wl, wc)
'''

def main():
     processed_data(PROCESSED)#数据清洗

     test(PROCESSED, RESULT_PATH)

     print('数据可视化中...')
     img = data_virtualization()  # 数据可视化
     return img

     print('python程序运行结束。')

if __name__ == '__main__':
    img = main()
    cv2.imshow('img',img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
