import requests
import re
import random
import types
import configparser
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
line_bot_api = LineBotApi('ttavQ7VwlIiP/1iklwyXLxk6iSiaAGzPvWhPNWxTmlhgx5xqPBvjGpm6fXxbSoUwnKU5RgJBxMypA12oJ18Dzao+5DVytLqWMpOLjMQiApOiP7Rq6ffEQzzOVi4BsI/K5qnlSGR8Gg47eW9pAvDl2wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ada8bcabd1841a8dfbe822d8d0035bc5')


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
class TaskStrategy:
    def __init__(self, func=None, event=None):
        self.name = func.__name__ if func else "default"
        self.event = event
        if func:
            self.execute = types.MethodType(func, self)
        print('{} class , task {}'.format(self.__class__.__name__, self.name))

    def execute(self):
        pass

    def reply_message(self, obj):
        line_bot_api.reply_message(self.event.reply_token, obj)

class TemplateStrategy(TaskStrategy):
    def execute(self):
        carousel_template_message = TemplateSendMessage(
            alt_text='目錄 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='服務項目',
                        text='請選擇',
                        actions=[
                            MessageAction(
                                label='我要預約！',
                                text='我要預約'
                            ),
                            MessageAction(
                                label='取消預約',
                                text='取消預約'
                            ),
                            URIAction(
                                label='我自己來',
                                uri='https://sso.nknu.edu.tw/userLogin/login.aspx?cUrl=/StudentProfile/CreditsNote/ApplyStu.aspx'
                            )
                        ]
                    )
                ]
            )
        )

def reserve(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        
        if event.message.text == "我要預約！":
             reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:和平-\n1.研究小間 三天前\n2.小型團體(4F、5F)(3人) 七天前\n燕巢-\n1.研究小間 三天前\n2.團體討論室、欣賞室、討論室 七天前\n請用換行方式依序填入下列資料讓我們替您預約空間喔~\n您的學生id:\n您的密碼:\n您要預約的校區(和平/燕巢):\n您要預約的空間():\n您要預約的時間(上午/下午):'
             line_bot_api.reply_message(
             event.reply_token,
             TextSendMessage(text=reserve_text))
        return 0
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

