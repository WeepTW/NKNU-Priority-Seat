from importlib.resources import path
from PIL import Image
import pytesseract
import os

path = os.path.dirname(os.path.realpath(__file__))+ '/captcha.png'
pytesseract.pytesseract.tesseract_cmd = path + 'Tesseract-OCR/tesseract.exe'

def captcha(path = path):
	img=Image.open(path)
	imggray=img.convert('L')
	threshold=170
	pixdata=imggray.load()
	width,height=imggray.size
	for y in range(height):
		for x in range(width):
			if pixdata[x,y]<threshold:
				pixdata[x,y]=0
			else:
				pixdata[x,y]=255
	imgbin=imggray
	pixdata=imgbin.load()
	width,height=imgbin.size
	for y in range(1,height-1):
		for x in range(1,width-1):
			count=0
			#up
			if pixdata[x,y-1]>245:
				count=count+1
			#down
			if pixdata[x,y+1]>245:
				count=count+1
			#left
			if pixdata[x-1,y]>245:
				count=count+1
			#right
			if pixdata[x+1,y]>245:
				count=count+1
			#up-left
			if pixdata[x-1,y-1]>245:
				count=count+1
			#down-left
			if pixdata[x-1,y+1]>245:
				count=count+1
			#up-right
			if pixdata[x+1,y-1]>245:
				count=count+1
			#down-right
			if pixdata[x+1,y+1]>245:
				count=count+1
			#clear
			if count>4:
				pixdata[x,y]=255
	imgclear=imgbin
	return pytesseract.image_to_string(imgclear,config='-c tessedit_char_whitelist=0123456789 --psm 6')

from math import nan
from RPA.Browser.Selenium import Selenium
from numpy import NaN
import pandas as pd
import datetime
#import time

lib = Selenium()
lib.auto_close = "False"

def __log(id):
    user = []
    df = pd.read_excel('D:/user/Program/NKNU-Priority-Seat/run/Info.xlsx',index_col=0)
    if id in list(df['account']):
        friends = []
        for i in range(1,6):
            if  not pd.isna(df.at[id,i]):
                friends.append(str(df.at[id,i]))
        user =  {'account':df.at[id,'account'],'password':df.at[id,'password'],'reservation':df.at[id,'token'],'friends':friends} 
    else:
        return []
    lib.open_available_browser('https://sso.nknu.edu.tw/NewLayout/Ex2/page2.aspx?catagoryId=4')
    notLogIn = True
    while notLogIn:
        lib.screenshot('xpath://*[@id="ssoLogin"]/table/tbody/tr[3]/td[2]/span/span/img', path)
        lib.input_text('uLoginID',str(user['account']))
        lib.input_text('uPassword',str(user['password']))
        lib.input_text('uAuthorizationCodeInput',captcha())
        #lib.click_button('uLogin') 不知道為什麼不用這個就會自己登入了 :(
        notLogIn = lib.is_alert_present('驗證碼輸入不正確！')
    lib.go_to(lib.get_element_attribute('xpath://*[@id="ctl00_phMain_divMenu2"]/div[2]/div[2]/div[10]/div/div/a','href'))
    return [user['reservation'],user['friends']]

def cancel(account):
    if __log(account) == []:
        return ['PermissionError']
    lib.go_to('https://lend.nknu.edu.tw/semac/service/history')
    for i in range(1,16):
        if lib.does_page_contain_button(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]'):
            lib.click_button_when_visible(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]')
            lib.is_alert_present('確定要取消嗎?')
            lib.is_alert_present('取消成功!')
        else:
            break

def record(account,n = 1): #default to show the lastest
    if __log(account) == []:
        return ['PermissionError']
    lib.go_to('https://lend.nknu.edu.tw/semac/service/history')
    s = []
    for i in range(1,n+1):
        if lib.does_page_contain_button(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]'):
            s.append({'area':lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[1]/a'),
                'room':lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[3]/a'),
                'time':lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[4]')})
        else:
            break
    return s



def countblock(hour = datetime.datetime.now().hour, min = datetime.datetime.now().minute):
    # min = 2 ; max = 25
    if hour % 1 == 0 and min % 1 == 0 and 0<= hour < 23 and 0 <= min < 60:
        if min <= 28 :
            block =  (hour-8)*2
        else:
            block =  (hour-8)*2 + 1
        if block < 2:
            return 2
        else:
            return block
    else:
        return 0

def __summit(page,startblock,col,endblock = 15,titular = []):
    col += 1 #col were start from 1
    if page != 1:
        lib.click_element(f'xpath://*[@id="owl-example"]/div[2]/div[1]/div[{page}]')
    for i in range(startblock - (15 - endblock),startblock - (15 - endblock) + 4):
        if i > endblock:
            break
        elif lib.get_element_attribute(f'xpath://*[@id="owl-example"]/div[{page}]/div/div[1]/div/table[2]/tbody/tr[{i}]/td[{col}]/span','class') != 'btn':
            return False
    
    if len(titular) == 0: #新增員編/學號
        for friend in titular: 
            lib.input_text('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div/div/input',friend)
            lib.click_element('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div/div/span[2]/span')
            lib.click_element_when_visible('xpath://*[@id="member_vue"]/div/div/div[3]/button[1]')
            if lib.is_alert_present('沒朋友'): #待調整
                return['Alert:PatheticOutsider']
            submitXpath = ''
    elif len(titular) == 2:
        submitXpath = ''
    elif len(titular) == 5:
        return['Alter:SystemUndelope']
    unsent = True
    if titular == []:
        while unsent:
            lib.screenshot('id=input-captcha-pic', path)
            lib.click_element_when_visible(f'xpath://*[@id="owl-example"]/div[{page}]/div/div[1]/div/table[2]/tbody/tr[{startblock}]/td[{col}]/span')
            lib.input_text('xpath://*[@id="expire_vue"]/div[2]/div/form/div[3]/div/div/input', captcha())
            lib.click_button('xpath://*[@id="expire_vue"]/div[2]/div/form/div[4]/div[2]/button')
            lib.click_button('xpath:/html/body/div[4]/div/div[3]/button[2]')
            lib.click_button_if_visible('xpath:/html/body/div[4]/div/div[3]/button[2]')
            if lib.is_alert_present('申請成功送出，請等候系統處理!'): unsent = True
    else:
        while unsent:
            lib.screenshot('id=input-captcha-pic', filename = path)
            lib.click_element_when_visible(f'xpath://*[@id="owl-example"]/div[{page}]/div/div[1]/div/table[2]/tbody/tr[{startblock}]/td[{col}]/span')
            lib.input_text('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div/input',captcha())
            lib.click_button('xpath://*[@id="expire_vue"]/div[2]/div/form/div[4]/div[2]/button')
            lib.click_button_when_visible('xpath:/html/body/div[4]/div/div[3]/button[2]')
            #AssertionError: Element 'xpath:/html/body/div[4]/div/div[3]/button[2]' not visible after 5 seconds.
            if lib.is_alert_present('申請成功送出，請等候系統處理!'): unsent = True
    return True

def __id(token):
    if token in [5,6,7,8]:
        return 8
    else:
        return token

def reservation(account,token,days = 0,startblock = 16 - countblock()):
    #check input
    if not token in [5,6,7,8,19,23,26,26,27,32]: return ['TokenError']
    if token in [19,23] and not days in range(4) or not days in range(8): return ['DaysError']
    if startblock < 2: return ['RentTimeError:Chaos']
    if startblock > 17: return ['RentTimeError:Overtime']
    user = __log(account)
    if user == []: return ['PermissionError']
    if token == 0: token = user[0]
    lib.go_to('https://lend.nknu.edu.tw/semac/service/index')
    lib.go_to(f'https://lend.nknu.edu.tw/semac/service/expire2/{__id(token)}_{datetime.date.today() + datetime.timedelta(days=days)}')
    print(f'https://lend.nknu.edu.tw/semac/service/expire2/{__id(token)}_{datetime.date.today() + datetime.timedelta(days=days)}')
    #exception
    if lib.get_location() == 'https://lend.nknu.edu.tw/semac/service/index':
        return ['SystemException']
    if lib.get_text('xpath://*[@id="owl-example"]/div[1]/div/div[2]/div/table[2]/tbody/tr[2]/td') == '未設定使用時間':
        return ['TimeException']
    #ordering
    endblock = 15
    if days == 0:
        endblock = countblock()
    if token in [5,6,7,8] and __summit(titular=user[1]) : #燕-小型團體討論室(2A:5 2B:6)、欣賞室(2A:7 2B:8)
        return record()
    elif token == 19: #燕-研究小間(14)
        for i in range(3):
            if i == 0:
                n = 4
            else:
                n = 5
            for j in range(n):
                if __summit(-i+3,startblock,j,titular=user[1]) :
                    return record(account)
    elif token == 32: #燕-討論室(1A 1B 1C 1D 1E 1F)
        for i in range(6):
            if __summit(i//5 +1,startblock,i%5 +1,titular=user[1]):
                    return record(account)
    elif token == 23: #和-研究小間(30)
        for i in range(1,7):
            for j in range(5):
                if __summit(i,startblock,j):
                    return record()
    elif token in [26,27] and __summit(1,startblock,1): #和-小型團體(4F、5F)
        return record()
    else:
        return ['FullHouseError']
    return ['FullHouseError']

def __init__():
    lib.close_all_browsers()
print(reservation(410731220,26,days=1))
