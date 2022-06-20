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

token = []
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
        reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:\n和平校區-\n1.代號 01-研究小間 三天前\n2.代號 02 03-小型團體(4F、5F)(3人) 七天前 \n燕巢校區-\n1.代號 11-研究小間 三天前 \n2.依序代號 12 13 14 15-團體討論室(2A、2B)、欣賞室(2A、2B) 七天前 \n 3.代號 16-討論室(1A、1B、1C、1D、1E)\n請輸入您要預約的空間代號\n如果打錯了 要做新的預約的話 請打「開始」'
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
        #cancel()
        reserve_text = '幫您取消所有預約囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))

    if re.match('確認預約情形',message):
        #record()
        reserve_text = '工程師還在努力開發中~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('01',message) or re.match('０１',message):
        token.append(23)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
        return token
    if re.match('02',message) or re.match('０２',message):
        token.append(26)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
        return token
    if re.match('03',message) or re.match('０３',message):
        token.append(27)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
        return token
    if re.match('11',message) or re.match('１１',message):
        token.append(19)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        
        return token
    if re.match('12',message) or re.match('１２',message):
        token.append(5)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
      
        return token
    if re.match('13',message) or re.match('１３',message):
        token.append(6)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
   
        return token
    if re.match('14',message) or re.match('１４',message):
        token.append(7)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
   
        return token
    if re.match('15',message) or re.match('１５',message):
        token.append(8)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
  
        return token
    if re.match('16',message) or re.match('１６',message):
        token.append(32)
        reserve_text = '請選擇您要預約的時間\n(預約時間辦法請參考圖片-打上「圖片」)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
 
        return token
    if re.match('現在',message):
        token.append(1000)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('今天上午',message):
        token.append(1008)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('今天中午',message):
        token.append(1012)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('今天晚上',message):
        token.append(1016)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('明天上午',message):
        token.append(1108)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('明天中午',message):
        token.append(1112)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('明天晚上',message):
        token.append(1116)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('後天上午',message):
        token.append(1208)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('後天中午',message):
        token.append(1212)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('後天晚上',message):
        token.append(1216)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('大後天上午',message):
        token.append(1308)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('大後天中午',message):
        token.append(1312)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    if re.match('大後天晚上',message):
        token.append(1316)
        reserve_text = '幫你處理囉~'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        return token
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
