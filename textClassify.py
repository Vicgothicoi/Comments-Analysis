from hanlp_restful import HanLPClient

def main(text):
    # auth不填则匿名，zh中文，mul多语种
    HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
    return HanLP.text_classification(text, model='news_zh')

if __name__ == '__main__':
    text = '''
    改了好几次，感觉终于可以确定了。
    这次的真丝是做了古董感的米金色染色，法蕾也做了同样的颜色。
    真丝软糯的手感和温柔的光泽感，在即将结束的冬天，显得格外的美好。
    '''
    cla = main(text)
    print("分类结果为：",cla)
