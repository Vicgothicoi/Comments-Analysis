import gradio as gr
import cv2
import numpy as np
import eliDifference
import textClassify  
import sentiment_analysis
import jd_comment


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

def localRes(wsd_word,sent):
    true_meaning=eliDifference.main(wsd_word,sent)
    return cv_imread('output/'+true_meaning+'_词云'+'.jpg'),cv_imread('output/'+true_meaning+'_评价'+'.jpg')

def OnlineRes(key):
    image1=jd_comment.main(key)
    image2=sentiment_analysis.main()
    return image1,image2

with gr.Blocks() as demo:
    gr.Markdown("请选择功能.")
    with gr.Tab("本地商品评价查询"):
        input1_1 = gr.Textbox(placeholder="请输入查询词:")
        input1_2 = gr.Textbox(placeholder="请输入消歧项:")
        with gr.Row():#水平展示
            output1_1 = gr.Image()
            output1_2 = gr.Image()
        button1 = gr.Button("查询")
    with gr.Tab("浏览器商品评价查询"):
        input2 = gr.Textbox(placeholder="请输入网址:")
        with gr.Row():
            output2_1 = gr.Image()
            output2_2 = gr.Image()
        button2 = gr.Button("查询")
    with gr.Tab("语义消歧"):
        input3_1 = gr.Textbox(placeholder="请输入查询词:")
        input3_2 = gr.Textbox(placeholder="请输入消歧项:")
        output3 = gr.Textbox()#不要用"text"
        button3 = gr.Button("消歧")
    with gr.Tab("文本分类"):
        #with gr.Row():#水平展示
        input4 = gr.Textbox(placeholder="请输入文本")
        output4 = gr.Textbox()
        button4 = gr.Button("分类")

    button1.click(localRes, inputs=[input1_1,input1_2], outputs=[output1_1,output1_2])
    button2.click(OnlineRes, inputs=input2, outputs=[output2_1,output2_2])
    button3.click(eliDifference.main, inputs=[input3_1,input3_2], outputs=output3)
    button4.click(textClassify.main, inputs=input4, outputs=output4)
    
demo.launch()
