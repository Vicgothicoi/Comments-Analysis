不需要下载其它文件可以直接运行，部分参考自https://github.com/jamosnet/JD-comments-sentiment-analysis

jd_comment.py实现数据爬取、转换、生成词云

sentiment_analysis.py实现生成评价图

textClassify.py实现文本分类

eliDifference.py实现语义消歧

以上每个文件都可以单独运行以测试功能

main.py是主函数，基于Gradio制作WebUI，包含了以上四个文件的功能

src文件夹包含程序使用到的资源，因此如果你要实现“苹果”以外的语义消歧，需要自行准备相关文本（比如爬取百度百科正文，放点相关的文本进去就可以了，使用TF-IDF基于词频消歧）

output文件夹包含程序运行生成的文件，同样只在京东上爬取了苹果（水果）和苹果（手机）的评价，本地商品搜索只支持这两项
