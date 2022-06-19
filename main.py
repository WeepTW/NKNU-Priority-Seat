
import os,sys
sys.path.append(r'.\run')
from run.view2 import record, reservation,cancel
'''
ＲＥＡＤＭＥ！卡在讀取驗證碼圖片
countblock(hour = now().hour, min = now().minute) -> Int ,if >28 then reservation will return error
    計算相應時間的借用格子
cancel() -> None 
    取消所有借用(如有手動借用過或單次借用超過15次會有bug)
record(n=15) -> list: NULL nor [{'area' : '燕巢校區 - 圖資大樓' , 'room' : '研究小間 (14)' , 'time' : '2022/06/12, 09:30~13:30'}]
    查看所有借用(如有手動借用過或單次借用超過15次會有bug)
reseration(token,days=0,startblock=countblock()) -> record(n=1)
    依序借用token的空間
'''

if __name__ == '__main__':
    #LINE Bot
    #reservation(5,days=2)
    #record()
    #cancel()
    print(reservation('Ue487ad1b559280fffc466af017f47e79',32,days = 1,hour = 12,min=0))
    