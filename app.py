from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
#import configparser
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError)
from linebot.models import *
import parser,re

app = Flask(__name__)

# LINE 聊天機器人的基本資料
#config = configparser.ConfigParser()
line_bot_api = LineBotApi('ttavQ7VwlIiP/1iklwyXLxk6iSiaAGzPvWhPNWxTmlhgx5xqPBvjGpm6fXxbSoUwnKU5RgJBxMypA12oJ18Dzao+5DVytLqWMpOLjMQiApOiP7Rq6ffEQzzOVi4BsI/K5qnlSGR8Gg47eW9pAvDl2wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ada8bcabd1841a8dfbe822d8d0035bc5')
line_bot_api.push_message('210clairehuang', TextSendMessage(text='請回傳 「開始」 進行服務'))

# 接收 LINE 的資訊
# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']

#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
    
#     try:
#         events = parser.parse(body, signature)
        
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'
@app.route("/callback", methods=['POST'])
def callback():
 
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
 
        try:
            print(body,signature)
            handler.handle(body, signature)
              # 傳入的事件
        except InvalidSignatureError:
                abort(400)

        return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text =event.message.text
    if re.match('開始',message):
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                title='我的服務',
                text='請選擇服務項目',
                actions=[
                    MessageTemplateAction(
                    label='我要預約！',
                    text='我要預約！'
                    ),
                    MessageTemplateAction(
                    label='取消預約',
                    text='取消預約'
                    ),
                    MessageTemplateAction(
                    label='我自己來',
                    uri='https://sso.nknu.edu.tw/userLogin/login.aspx?cUrl=/StudentProfile/CreditsNote/ApplyStu.aspx'
                    )
                            
                        ]
                    )
                )
            )
                    
    else:
        if re.match('我要預約！',message):
            reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:和平-\n1.研究小間 三天前\n2.小型團體(4F、5F)(3人) 七天前\n燕巢-\n1.研究小間 三天前\n2.團體討論室、欣賞室、討論室 七天前\n請用換行方式依序填入下列資料讓我們替您預約空間喔~\n您的學生id:\n您要預約的校區(和平/燕巢):\n您要預約的空間():\n您要預約的時間(今天/明天/後天/大後天 + 時間):'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(reserve_text))
            return 0
        if re.match('取消預約',message):
            reserve_text = '提醒您 我們會取消所有的借用預約 您確定要取消預約嗎? (若是 請打上: 確定取消)'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(reserve_text))
            return 0
        if re.match('我自己來',message):
            return 0
        if re.match('確定取消',message):
            #cancel()
            return 0
line_bot_api.push_message('210clairehuang', TextSendMessage(text='功能確認'))              


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

