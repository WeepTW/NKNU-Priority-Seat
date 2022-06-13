from lib2to3.pgen2 import token
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('uxVsnPZdc7sMpdkSpB2fUfM2BIMvHAt2qieS58JFnkN7Tcm6vAtB7OQlIw6pWm/KeMPiKipm/FW1xy+c+W/99Y5xwsm4fueZgMrapUP3Q4qXckGlvK2ABdKkQD+MILxLg9bA/53J0kQBVNj/vV+7KgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('93df464b067cee15e60a3f1759471f90')

line_bot_api.push_message('Ub7e9f322724c6b15cab6fc57630e5d8c', TextSendMessage(text='請回傳「開始」進行服務~'))

@app.route("/callback", methods=['POST'])
def callback():
 
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
 
        try:
            print(body,signature)
            handler.handle(body, signature)
            #user = line_bot_api.get_profile('<user_id>')
        
        except InvalidSignatureError:
                abort(400)

        return 'OK'
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text =event.message.text
    if re.match('開始',message):    
        buttons_template_message = TemplateSendMessage(
        alt_text='選擇服務',
        template=ButtonsTemplate(
        title='請選擇服務項目',
        text='選單功能-TemplateSendMessage',
             actions=[
                 MessageAction(
                     label='我要預約！',
                    text='我要預約！'  
                 ),
                 MessageAction(
                     label='取消預約',
                     text='取消預約' 
                 ),
                 URIAction(
                     label='我自己來！',
                     uri='https://lend.nknu.edu.tw/semac/home/index.html'
                 )
             ]
         )
     )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    if re.match('我要預約！',message):
        reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:\n和平校區-\n1.研究小間 三天前\n2.小型團體(4F、5F)(3人) 七天前\n燕巢校區-\n1.研究小間-代號 spaceC 三天前\n2.團體討論室(2A、2B)、欣賞室(2A、2B) 七天前\n 3.討論室(1A、1B、1C、1D、1E)\n請點選下列表單讓我們替您預約空間喔~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
@handler.add(MessageEvent, message=TextMessage)        
def handle_message_reserve_campus(event):   
    message = text =event.message.text        
    if re.match('我要預約！',message):   
        buttons_template_message_campus = TemplateSendMessage(
        alt_text='校區',
        template=ButtonsTemplate(
        title='請選擇校區',
        text='選單功能-TemplateSendMessage',
             actions=[
                 MessageAction(
                     label='和平',
                     text='和平校區！'  
                 ),
                 MessageAction(
                     label='燕巢',
                     text='燕巢校區' 
                 )
             ]
         )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message_campus)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

