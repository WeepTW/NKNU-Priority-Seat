import os
import sys
sys.path.append(r'.\run')
from run.view import cancel,record,reservation,log
import time
from numpy import mean
import webbrowser
'''
cancel(id) -> None 
    取消所有借用
record(id) -> Str
    查看所有借用
reseration(id,token,days=0, hour = datetime.datetime.now().hour, min = datetime.datetime.now().minute) -> Str | Error Messenage or RentTime
    依序借用token的空間
*id is a messenage api from Line bot, you can add by run.info.xlsx and set api in https://developers.line.biz/console/profile to get the user ID.
Token and max days for rooms:
    23#3 和平-研究小間
    26#7 和平-4F小型團體
    27#7 和平-5F小型團體
    19#3 燕巢-研究小間
    5#7 燕巢-團體討論室2A
    6#7 燕巢-團體討論室2B
    7#7 燕巢-欣賞室2A
    8#7 燕巢-欣賞室2B
    32#7 討論室(1A 1B 1C 1D 1E)
'''
id = 'Ue487ad1b559280fffc466af017f47e79'
exit = False
tokens = {1:23,2:26,3:27,11:19,12:7,13:7,14:7,15:7,16:32}
days = {'現在':0,'今天':0,'明天':1,'後天':2,'大後天':3}
times = {'早上':[8,0],'下午':[12,10],'晚上':[16,50]}
print('請輸入「開始」以開啟選單功能')
while(not exit):
    service = input('Command:')
    s = service.split()
    if service == '開始': print('選單功能 1.我要預約 2.取消預約 3.確認預約的情形 4.我自己來！\n請選擇服務項目')
    elif service == '圖片': print('圖片在Line Bot 0.0')
    elif service == 'exit': break
    elif service == '' or not s[0].isdigit(): print('請重新輸入')
    elif len(s) == 1 and int(s[0]) in range(1,5):
        if int(service) == 1:
            print('Toom tokens with max rent day:\n 01#3 和平-研究小間\n 02#7 和平-4F小型團體\n 03#7 和平-5F小型團體\n 11#3 燕巢-研究小間\n 12#7 燕巢-團體討論室2A\n 13#7 燕巢-團體討論室2B\n 14#7 燕巢-欣賞室2A\n 15#7 燕巢-欣賞室2B\n 3#7 討論室')
            print('請輸入「代號(空格)預約時間」開始預約，預約時間辦法請參考圖片-打上「圖片」')
        elif int(service) == 2: print(cancel(id))
        elif int(service) == 3: print(record(id))
        elif int(service) == 4: webbrowser.open(log(id)[3]); break
        else: print('請重新輸入一次！')
    elif len(s) == 2 and int(s[0]) in list(tokens.keys()):
        if s[1] == '現在': print(reservation(id,tokens[int(s[0])]))
        for day in days.keys():
            for time in list(times.keys()):
                if s[1] == day + time:
                    print(reservation(id,tokens[int(s[0])],days=days[day],hour= times[time][0],min=times[time][1]))
                    continue
        print('請重新輸入一次')
    else: print('請重新輸入一次')
