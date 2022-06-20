import sys
sys.path.append(r'.\run')
from run.view import cancel,record,reservation
import time
from numpy import mean
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
t = []
for i in range(3):
    print(i)
    t0 = time.process_time_ns()
    print(reservation('Ue487ad1b559280fffc466af017f47e79',32,days=1,hour=i+5,min=30))
    t.append(time.process_time_ns() - t0)
    print(cancel('Ue487ad1b559280fffc466af017f47e79'))
print(sum(t)/5)
print(t)
