from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
from run.view import record, reservation,cancel,countblock

import os,sys
sys.path.append(r'.\run')

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('uxVsnPZdc7sMpdkSpB2fUfM2BIMvHAt2qieS58JFnkN7Tcm6vAtB7OQlIw6pWm/KeMPiKipm/FW1xy+c+W/99Y5xwsm4fueZgMrapUP3Q4qXckGlvK2ABdKkQD+MILxLg9bA/53J0kQBVNj/vV+7KgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('93df464b067cee15e60a3f1759471f90')

line_bot_api.push_message('Ub7e9f322724c6b15cab6fc57630e5d8c', TextSendMessage(text='check'))
#line_bot_api.push_message(TextSendMessage(text='請回傳「開始」進行服務~'))#正式來

@app.route("/callback", methods=['POST'])
def callback():
 
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
       
        try:
            print(body,signature)
            handler.handle(body, signature)
            
        
        except InvalidSignatureError:
                abort(400)

        return 'OK'
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####

token = 0
days = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_message_list(event):
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
                 MessageAction(
                     label='確認預約情形',
                     text='確認預約情形' 
                 ),
                 URIAction(
                     label='我自己來！',
                     uri='https://lend.nknu.edu.tw/semac/home/index.html'
                 )
             ]
         )
     )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        token.clear
        return token
    if re.match('圖片',message)or re.match('時刻對照表',message):
        image_message = ImageSendMessage(
            original_content_url='https://q410831143.weebly.com/uploads/1/3/3/8/133895349/rpa_orig.jpg',
            preview_image_url='https://q410831143.weebly.com/uploads/1/3/3/8/133895349/rpa_orig.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
    if re.match('我要預約！',message):
        reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:\n和平校區-\n1.代號 01-研究小間 三天前\n2.代號 02 03-小型團體(4F、5F)(3人) 七天前 \n燕巢校區-\n1.代號 11-研究小間 三天前 \n2.依序代號 12 13 14 15-團體討論室(2A、2B)、欣賞室(2A、2B) 七天前 \n 3.代號 16-討論室(1A、1B、1C、1D、1E)\n\n請輸入您要預約的空間代號\nex.01\n\n如果打錯了 要做新的預約的話 請打「開始」'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('取消預約',message):
        confirm_template_message = TemplateSendMessage(
             alt_text='確定取消',
             template=ConfirmTemplate(
                 text='提醒您 我們會取消所有的借用預約 您確定要取消預約嗎？',
                 actions=[
                     PostbackAction(
                         label='確定取消',
                         display_text='確定取消',
                         data='action=確定取消'
                     ),
                     PostbackAction(
                         label='我按錯了',
                         display_text='我按錯了',
                         data='action=不要取消'
                     ),
                 ]
             )
         )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
    if re.match('確定取消',message):
        reserve_text = cancel(line_bot_api.get_profile('<user_id>'))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('確認預約情形',message):
        reserve_text = record(line_bot_api.get_profile('<user_id>'))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    
    for token in token:
        for day in days: #現在 明天中午 明天下午
            if re.match(token + ' ' + '現在'):
                reservation(line_bot_api.get_profile('<user_id>'),token)
            ds = {0:'今天',1:'明天',2:'後天'}
            for d in ds:
                for t in ['早上','中午','晚上']:
                    if re.match(token + ' ' + d+t):
                        reservation(id,token,days= ds.index(d),min= '0')
            if re.match(token + ' ' +day):
                if day == 0:
                    reservation(id,token)
                else:
                    reservation(id,token,days = day, hour = '08',min = '00')
    
    if re.match('01',message) or re.match('０１',message):
        token = 23
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('02',message) or re.match('０２',message):
        token = 26
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('03',message) or re.match('０３',message):
        token = 27
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
    if re.match('11',message) or re.match('１１',message):
        token = 19
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
    if re.match('12',message) or re.match('１２',message):
        token = 5
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
      
    if re.match('13',message) or re.match('１３',message):
        token = 6
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
   
    if re.match('14',message) or re.match('１４',message):
        token = 7
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
   
    if re.match('15',message) or re.match('１５',message):
        token = 8
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('16',message) or re.match('１６',message):
        token = 32
        reserve_text = '請選擇您要預約的時間(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
 
    if re.match('現在',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('今天上午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 0,hour = '7',min = '55')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('今天中午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 0,hour = '11',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('今天晚上',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 0,hour = '16',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('明天上午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 1,hour = '7',min = '55')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('明天中午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 1,hour = '11',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('明天晚上',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 1,hour = '16',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('後天上午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 2,hour = '7',min = '55')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('後天中午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 2,hour = '11',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('後天晚上',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 2,hour = '16',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('大後天上午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 3,hour = '7',min = '55')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('大後天中午',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 3,hour = '11',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('大後天晚上',message):
        reserve_text = reservation(line_bot_api.get_profile('<user_id>'),token,days = 3,hour = '16',min = '30')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
