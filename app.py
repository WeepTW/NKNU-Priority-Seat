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
                 URIAction(
                     label='我自己來！',
                     uri='https://lend.nknu.edu.tw/semac/home/index.html'
                 )
             ]
         )
     )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    if re.match('我要預約！',message):
        reserve_text = '預約前做個小提醒~依次一個帳號只能借用一個空間\n能借用的空間有:\n和平校區-\n1.研究小間-代號 01 三天前\n2.小型團體(4F、5F)(3人)-代號 02 03 七天前\n燕巢校區-\n1.研究小間-代號 11 三天前\n2.團體討論室(2A、2B)、欣賞室(2A、2B)-依序代號 12 13 14 15 七天前\n 3.討論室(1A、1B、1C、1D、1E)-代號 16\n請書您要預約的空間代號'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('01',message) or re.match('０１',message):
        token.append(23)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('02',message) or re.match('０２',message):
        token.append(26)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('03',message) or re.match('０３',message):
        token.append(27)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('11',message) or re.match('１１',message):
        token.append(19)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('12',message) or re.match('１２',message):
        token.append(5)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('13',message) or re.match('１３',message):
        token.append(6)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('14',message) or re.match('１４',message):
        token.append(7)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('15',message) or re.match('１５',message):
        token.append(8)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('16',message) or re.match('１６',message):
        token.append(32)
        reserve_text = '請選擇您要預約的時間：\n(現在/今天上午/今天中午/今天晚上\n明天上午/明天中午/明天晚上\n後天上午/後天中午/後天晚上\n大後天上午/大後天中午/大後天晚上)'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('現在'):
        token.append('now')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('今天上午'):
        token.append('todaymn')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('今天中午'):
        token.append('todayan')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('今天晚上'):
        token.append('todayev')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('明天上午'):
        token.append('tommn')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('明天中午'):
        token.append('toman')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('明天晚上'):
        token.append('toev')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('後天上午'):
        token.append('datmn')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('後天中午'):
        token.append('datan')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('後天晚上'):
        token.append('datev')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('大後天上午'):
        token.append('daatmn')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('大後天中午'):
        token.append('daatan')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    if re.match('大後天晚上'):
        token.append('daatev')
        reserve_text = '預約成功'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    
    if re.match('取消預約',message):
        reserve_text = '提醒您 我們會取消所有的借用預約 您確定要取消預約嗎? '
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
        confirm_template_message = TemplateSendMessage(
             alt_text='確定取消',
             template=ConfirmTemplate(
                 text='您確定要取消嗎？',
                 actions=[
                     PostbackAction(
                         label='取消',
                         display_text='確定取消',
                         data='action=確定取消'
                     ),
                     PostbackAction(
                         label='繼續',
                         display_text='不要取消',
                         data='action=不要取消'
                     ),
                 ]
             )
         )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
        return 0
    if re.match('確定取消',message):
        #cancel()
        reserve_text = '已取消所有預約'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(reserve_text))
    #學生id匯入
    if line_bot_api.get_profile('<user_id>') == 'Ub7e9f322724c6b15cab6fc57630e5d8c':
        stu_id = '410831143'
        token.append(stu_id)
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
